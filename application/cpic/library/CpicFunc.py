# -*- coding: gbk -*-
##########################################################
#       名称：安贷宝日终函数                             #
#       日期：2009-04-01                                 #
#       时间：15:15                                      #
#       所属：赞同科技                                   #
##########################################################
import TradeContext, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc,AfaUtilTools,AfaLoggerFunc
import HostContext,AfaHostFunc,HostComm,AfaAhAdb
import os
from types import *
from datetime import *


################################################################################
#           安贷宝.公共函数
# 功    能：发起联机业务对帐请求
# 参数说明：
# 事    例：
# 
################################################################################
def HostCkgDetail(logger):
    logger.info( "对账变量初始化" )
    HostContext.I1TRCD = '8837'                        #主机交易码
    HostContext.I1SBNO = "3400008889"                  #该交易的发起机构(省清算中心)
    HostContext.I1USID = '999986'                      #交易柜员号
    HostContext.I1AUUS = ""                            #授权柜员
    HostContext.I1AUPS = ""                            #授权柜员密码
    HostContext.I1WSNO = ""                            #终端号
    HostContext.I1STDT = TradeContext.corpDate         #起始日期
    HostContext.I1EDDT = TradeContext.corpDate         #结束日期
    #HostContext.I1NBBH = TradeContext.sysId            #代理业务号(太保: AG2011)
    HostTradeCode = "8837".ljust(10,' ')
    #logger.info( "HostTradeCode = " + str(HostTradeCode) )
    HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8837.map', HostTradeCode, "9002" )
    if(HostContext.existVariable("O1MGID")):
        if(HostContext.O1MGID == "AAAAAAA"):
            logger.info( "发起联机对帐请求成功")
            return 0
        else:
            logger.info("通讯成功，主机错误，主机返回信息为:["+HostContext.O1INFO+"]")
            return -1
    else:
        logger.info( "与主机通讯异常，请检查")
        return -2
    return 0
################################################################################
#           安贷宝.文件转换
# 功    能：与主机对账文件转换
# 参数说明：
# 事    例：
# 
################################################################################
def FileTransfer(logger):
    logger.info( "开始转换文件" )
    try:
        dstFileName    = os.environ['AFAP_HOME'] + '/data/cpic/host/' + TradeContext.corpDate + "_HOSTDZ"
        srcFileName    = os.environ['AFAP_HOME'] + '/data/cpic/host/' + TradeContext.fileName
        #调用格式:cvt2ascii -T 生成文本文件 -P 物理文件 -F fld文件 [-D 间隔符] [-S] [-R]
        CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
        fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/tbsca.fld'
        cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName
        logger.info( "cmdstr = " + str(cmdstr) )
        
        ret = os.system(cmdstr)
        if ( ret != 0 ):
            return -1
        else:
            return 0
    except Exception, e:
        logger.info(e)
        logger.info('格式化文件异常')
        return -1
    return 0
################################################################################
#           安贷宝.公共函数
# 功    能：主机对帐(修改中间流水)
# 参数说明：
# 事    例：对账文件格式
#           交易序号0|代理业务号1|外系统日期2|前置日期3|前置流水号4|主机日期5|主机流水号6|冲账标志7|现转标志8
#           |往来帐标志9|交易金额10|金额标示11|记录状态12|备用字段１13|备用字段２14|备用字段３15
#           
################################################################################
def loadMdtlFile(logger):
    logger.info( "开始读入主机对账文件" )
    total ,mistake= 0 ,0
    try:
        sFileName = os.environ['AFAP_HOME'] + '/data/cpic/host/' + TradeContext.corpDate + "_HOSTDZ"
        f = file(sFileName,"r")
    except:
        return -1
    while( True ):
        sLine = f.readline()
        print sLine
        logger.info(sLine)
        sLine=sLine.replace('\r','')
        sLine=sLine.replace('\n','')
#        logger.info(str(len(sLine)))
        total = total + 1
        if(len(sLine) == 0):
            break
        arrayList = sLine.split("|")
        if(len(arrayList) > 6):
            TradeContext.hostAgentSeriano        = arrayList[4].strip()
            #print TradeContext.hostAgentSeriano
            TradeContext.hostDate                = arrayList[5].strip()
            #print TradeContext.hostDate
            TradeContext.hostSeriano             = arrayList[6].strip()
            #print TradeContext.hostSeriano
            #TradeContext.hostErrCode             = arrayList[3].strip()
            #print TradeContext.hostErrCode
            #TradeContext.hostErrMsg              = arrayList[4].strip()
            #print TradeContext.hostErrMsg
            if(UpdateAfaDetail( logger ) == 0 ):
                #print "对帐成功"
                continue
            else:
                #print "对帐失败"
                continue
        else:
            mistake = mistake + 1
            continue
    logger.info( "结束读入主机对账文件" )
    if(mistake > 0):
        TradeContext.rFile = "读文件共有["+str(total)+"]条记录,有["+str(mistake)+"]条格式有误."
    else:
        TradeContext.rFile = ""
    TradeContext.returnMsg = TradeContext.rFile+ "读入主机对账文件结束"
    f.close()
    return 0
#---------------------------------------------------------------------------------------------------------
def UpdateAfaDetail(logger):
    #if(TradeContext.hostErrCode == "0000"): #主机返回对账信息,"0"表示成功,"1"表示失败
    #    chkflag = "0"
    #else:
    #    chkflag = "1"
    try:
        sql = "UPDATE AFA_MAINTRANSDTL SET bankcode = '0000',chkflag = '0'"
        sql = sql + " where agentserialno = '"+TradeContext.hostAgentSeriano+"'"
        logger.info( "更新中间业务流水表 " + str(sql) )
        retCode = AfaDBFunc.UpdateSqlCmt(sql)
        #print 'retCode = '+str(retCode)
        if(retCode < 1):
            logger.info("fail")
            return -2
        else:
            return 0
    except Exception , e:
        logger.info(sql+"\n\n"+str(e))
        return -1
#----------------------------------------------------------------------------------------------------------
###########################################################
#       安贷宝对账
#       功能：生成第三方联机回执文件
#       日期：2008-11-04
#       说明：
#       银行编码(10)+交易日期(8)+银行区域代码(10)+储蓄所代码(10)+交易码(7)+
#       银行流水号(30)+保单号(20)+金额(12位，带小数点)+销售渠道（2位）
#       银行编码默认为"01",银行区域代码"ANHNX00001",销售渠道"01"
###########################################################
def CreCpicLjFile(logger):
    logger.info( "开始生成安贷宝联机交易回执文件" )
    TradeContext.table = 'AFA_MAINTRANSDTL'
    splitStr = "|"
    emptyStr = " "
    psFilePath = os.environ['HOME']+"/afa/data/cpic/cpic/"+TradeContext.fileName
    try:
        f = file( psFilePath,"w")
    except:
        logger.info( "生成文件"+TradeContext.fileName+"失败" )
        return -1
    
    sqlUpdate = "UPDATE "+TradeContext.table+" SET corpchkflag ='0' WHERE sysId ='"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "' "
    sqlUpdate = sqlUpdate + "AND workdate = '"+TradeContext.corpDate+"' AND chkflag = '0' and revtranf = '0' and bankstatus = '0'"
    #print sqlUpdate
    logger.info("更新chkflag>>>>>>"+str(sqlUpdate))
    records = AfaDBFunc.UpdateSqlCmt( sqlUpdate )
    #print 'records = '+str(records)
    if(records < 0):
        return -2
    '''用户编号,金额,流水号'''
    sql = "SELECT workdate,brno,agentserialno,note5,amount "
    sql = sql + "FROM "+TradeContext.table+" WHERE sysId ='"+TradeContext.sysId+"'"
    sql = sql + "AND workdate = '"+TradeContext.corpDate+"' AND chkflag = '0' and revtranf = '0' and bankstatus = '0'"
    #print sql
    logger.info("查询数据>>>>>>"+str(sql))
    records = AfaDBFunc.SelectSql( sql )
    print "-------------< [生成通安贷宝联机回执文件:共 " + str(len(records)) + "条成功记录] >------------"
    logger.info( "< [生成通安贷宝联机回执文件:共 " + str(len(records)) + "条成功记录] >")
    if ( len(records) > 0 ):
        for i in range(0,len(records)):
            tmpStr = ""
            #银行编码
            tmpStr = tmpStr + "01" +splitStr
            #交易日期
            tmpStr = tmpStr + records[i][0].strip() +splitStr
            #银行区域代码
            tmpStr = tmpStr + "ANHNX00001" +splitStr
            #储蓄所代码
            tmpStr = tmpStr + records[i][1].strip()  +splitStr
            #交易码
            tmpStr = tmpStr + "6000113" +splitStr
            #银行流水号
            tmpStr = tmpStr + records[i][2].strip()  +splitStr
            #保单号
            tmpStr = tmpStr + records[i][3].strip()  +splitStr
            #金额
            tmpStr = tmpStr + records[i][4].strip()  +splitStr
            #销售渠道
            tmpStr = tmpStr + "01|\n"
            f.write( tmpStr )
        f.close()
    else:
        logger.info( "结束生成安贷宝联机回执文件(无记录)" )
        f.close()
    f.close()
    logger.info( "结束生成安贷宝联机回执文件" )
    return 0
################################################################################
#           安贷宝.公共函数
# 功    能：取获取文件
# 参数说明：
# 事    例：
# 
################################################################################
def getFile(logger):
    logger.info('开始接收文件'+TradeContext.fileName)
    os.system( TradeContext.getFile )
    logger.info('结束接收文件'+TradeContext.fileName)
    return 0
################################################################################
#           安贷宝.公共函数
# 功    能：发送文件
# 参数说明：
# 事    例：
# 
################################################################################
def putFile(logger):
    logger.info('开始发送文件'+TradeContext.fileName)
    os.system( TradeContext.putFile )
    logger.info('结束发送文件'+TradeContext.fileName)
    return 0
################################################################################
#           安贷宝.公共函数
# 功    能：测试文件是否存在
# 参数说明：
# 事    例：
# 
################################################################################
def isExistFile(logger):
    logger.info( "开始测试文件是否存在" )
    psFilePath = TradeContext.filePath + TradeContext.fileName
    try:
        f = file( psFilePath,"r")
    except:
        logger.info( "文件"+TradeContext.fileName+"不存在" )
        return -1
    f.close()
    logger.info( "结束测试文件是否存在" )
    return 0
    
    
################################################################################
#           报表生成.生成汇总报表
# 功    能：生成安贷宝报表
# 参数说明：
# 事    例：
# 
################################################################################
def CreatReport(logger):
    try:
        resulBrno = None
        i = 0
        splitStr = "|"
        #判断是否是对公帐户所在网点
        sqlbrno = "select note1 from afa_unitadm where sysid = '" + TradeContext.sysId + "' and unitno = '" + TradeContext.unitno + "'"
        logger.info("查询对公帐户所在网点："+sqlbrno)
        resultb = AfaDBFunc.SelectSql(sqlbrno)
        if resultb is None:
            logger.info("数据库操作异常"+sqlbrno)
            return -1
        elif(len(resultb)) == 0:
            logger.info("应用不存在请核对")
            TradeContext.errorCode = "0002"
            TradeContext.errorMsg = "应用不存在"
            return 0
        else:
            logger.info("数据库中网点号"+resultb[0][0])
            TradeContext.brnoAll = resultb[0][0]
        TradeContext.corpDate = TradeContext.workDate
        logger.info ( " 打印日期  "+TradeContext.corpDate)
        TradeContext.PBDAFILE = TradeContext.corpDate+"_"+TradeContext.brno+"_"+TradeContext.tellerno+"_"+TradeContext.reportType+".txt"
        fileName = os.environ['HOME']+"/afa/data/cpic/report/"+TradeContext.PBDAFILE
        logger.info ( " 文件路径名称  "+fileName)
        try:
            f = file(fileName,"w")
        except:
            logger.info("生成文件["+fileName+"]失败")
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "生成文件["+fileName+"]失败"
            return -2
            
        #打印文件
        PfileName = os.environ['HOME']+"/afa/data/cpic/report/P_"+TradeContext.PBDAFILE
        TradeContext.P_PBDAFILE = "P_" + TradeContext.PBDAFILE
        logger.info ( " 打印文件路径名称  "+PfileName)
        try:
            Pf = file(PfileName,"w")
        except:
            logger.info("生成打印文件["+PfileName+"]失败")
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "生成打印文件["+PfileName+"]失败"
            return -2
        # 如果为明细报表返回记录条数
        #if ( TradeContext.reportType == "2" ):
        #    sqltrade = "select agentserialno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
        #    if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
        #        sqltrade = sqltrade + " and note7 = '"+TradeContext.ProCode+"'"
        #    #sqltrade = sqltrade + " and brno = '"+TradeContext.EBrno+"'"
        #    sqltrade = sqltrade + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
        #    sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
        #    sqltrade = sqltrade + " and bankstatus = '0' and corpstatus = '0' and revtranf = '0' order by agentserialno"
        #    logger.info( "查询记录条数"+str(sqltrade) )
        #    resultrade = AfaDBFunc.SelectSql(sqltrade)
        #    if resultrade is None:
        #        logger.info("查询明细:数据库操作异常"+sqltrade)
        #        TradeContext.errorCode = "0001"
        #        TradeContext.errorMsg = "查询明细:数据库操作异常"+sqltrade
        #        return -2
        #    else:
        #        TradeContext.RecCount = str(len(resultrade))
        logger.info ( " 开始生成安贷宝总报表文件，日期为["+TradeContext.startdate+">>>>>"+TradeContext.enddate+"]" )
        logger.info ( " TradeContext.brnoAll  ["+TradeContext.brnoAll+"]" )
        logger.info ( " TradeContext.brno     ["+TradeContext.brno+"]" )
        logger.info ( " TradeContext.Brno     ["+TradeContext.Brno+"]" )
        #logger.info ( " TradeContext.brnoFlag ["+TradeContext.brnoFlag+"]" )
        logger.info ( " TradeContext.ProSel   ["+TradeContext.ProSel+"]" )
        logger.info ( " TradeContext.ProCode  ["+TradeContext.ProCode+"]" )
        
        #主办行若不送机构号,查询打印所有机构报表;若送机构号,单独查询打印此机构报表;
        #非主办行只能查询打印本机构报表
        
        #主办行若不送机构号,查询打印所有机构报表
        if ( TradeContext.brno == TradeContext.brnoAll and TradeContext.Brno.strip() == ""):
            sqlbrno = "select distinct brno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
            if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                sqlbrno = sqlbrno + " and note7 = '"+TradeContext.ProCode+"'"
            
            #begin 20100618 蔡永贵  为了能够查询当日未对账明细修改查询条件
            if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                sqlbrno = sqlbrno + " and chkflag = '9' and corpchkflag = '9'"
            else:
                sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            #end
            
            sqlbrno = sqlbrno + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            #sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            sqlbrno = sqlbrno + " and bankstatus = '0' and revtranf = '0' order by brno"
        #elif ( TradeContext.existVariable( "brnoFlag" ) and TradeContext.brnoFlag.strip() == "0" ):
        #    sqlbrno = "select distinct brno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
        #    if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
        #        sqlbrno = sqlbrno + " and note7 = '"+TradeContext.ProCode+"'"
        #    sqlbrno = sqlbrno + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
        #    sqlbrno = sqlbrno + " and brno like '%"+TradeContext.brno[0:6]+"%'"
        #    sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
        #    sqlbrno = sqlbrno + " and bankstatus = '0' and corpstatus = '0' and revtranf = '0' order by brno"
        #主办行查询打印指定机构报表
        elif ( TradeContext.brno == TradeContext.brnoAll and TradeContext.Brno.strip() != ""):
            sqlbrno = "select distinct brno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
            if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                sqlbrno = sqlbrno + " and note7 = '"+TradeContext.ProCode+"'"
            sqlbrno = sqlbrno + " and brno = '"+TradeContext.Brno+"'"
            
            #begin 20100618 蔡永贵  为了能够查询当日未对账明细修改查询条件
            if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                sqlbrno = sqlbrno + " and chkflag = '9' and corpchkflag = '9'"
            else:
                sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            #end
            
            sqlbrno = sqlbrno + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            #sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            sqlbrno = sqlbrno + " and bankstatus = '0' and revtranf = '0'"
        #非主办行只能查询打印本机构报表
        else:
            sqlbrno = "select distinct brno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
            if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                sqlbrno = sqlbrno + " and note7 = '"+TradeContext.ProCode+"'"
            sqlbrno = sqlbrno + " and brno = '"+TradeContext.brno+"'"
            
            #begin 20100618 蔡永贵  为了能够查询当日未对账明细修改查询条件
            if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                sqlbrno = sqlbrno + " and chkflag = '9' and corpchkflag = '9'"
            else:
                sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            #end
            
            sqlbrno = sqlbrno + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            #sqlbrno = sqlbrno + " and chkflag = '0' and corpchkflag = '0'"
            sqlbrno = sqlbrno + " and bankstatus = '0'  and revtranf = '0'"
        logger.info( "查询网点号"+str(sqlbrno) )
        resulBrno = AfaDBFunc.SelectSql(sqlbrno)
        logger.info( "查询结果"+str(len(resulBrno)) )
        if resulBrno is None:
            logger.info("查询网点号:数据库操作异常"+sqlbrno)
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "查询网点号:数据库操作异常"+sqlbrno
            return -2
        elif ( len(resulBrno) == 0 ):
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg = "未查询到相关的交易记录"
            return -3
        else:
            TradeContext.RecAllCount = 0
            reccount = 1
            #打印文件表头
            if TradeContext.reportType == "1":
                tmpStr = "".ljust(40) + "代理保险汇总表\n"
            else:
                tmpStr = "".ljust(40) + "代理保险明细表\n"
            tmpStr = tmpStr + "      机构代码:  " + TradeContext.brno + "\n"
            tmpStr = tmpStr + "      起止日期:  " + TradeContext.startdate + "-" + TradeContext.enddate + "      打印日期:" + TradeContext.workDate + "\n"
#            tmpStr = tmpStr + "".ljust(132,"=") + "\n"
            if TradeContext.reportType == "1":
                tmpStr = tmpStr + "".ljust(100,"=") + "\n"
                tmpStr = tmpStr + "      机构号      险种名称           中文说明                笔数         保险金额\n"
                
            else:
                tmpStr = tmpStr + "".ljust(151,"=") + "\n"
                tmpStr = tmpStr + "      机构代码    交易日期        险种名称    中文说明               主机流水           投保单号        客户名称            保费金额           交易流水\n"
                tmpStr = tmpStr + "".ljust(151,"=") + "\n"
            Pf.write(tmpStr)
            
            for i in range (0,len(resulBrno)):
                TradeContext.EBrno = str(resulBrno[i][0])
                #判断报表类型生成不同的报表
                logger.info("reportType=[" + TradeContext.reportType + "]")
                if ( TradeContext.reportType == "1" ):
                    logger.info ( " [" + TradeContext.EBrno + "]生成汇总表 " )
                    resulCount = None
                    sqlcount = "select count(*),sum(cast(amount as decimal(15,2)) ) from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
                    if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                        sqlcount = sqlcount + " and note7 = '"+TradeContext.ProCode+"'"
                    sqlcount = sqlcount + " and brno = '"+str(TradeContext.EBrno)+"'"
                    
                    #begin 20100618 蔡永贵  为了能够查询当日未对账明细修改查询条件
                    if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                        sqlcount = sqlcount + " and chkflag = '9' and corpchkflag = '9'"
                    else:
                        sqlcount = sqlcount + " and chkflag = '0' and corpchkflag = '0'"
                    #end
                    
                    sqlcount = sqlcount + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
                    #sqlcount = sqlcount + " and chkflag = '0' and corpchkflag = '0'"
                    sqlcount = sqlcount + " and bankstatus = '0'  and revtranf = '0'"
                    logger.info( "生成汇总表：每个网点汇总"+str(sqlcount) )
                    resulCount = AfaDBFunc.SelectSql(sqlcount)
                    if resulCount is None:
                        logger.info("查询汇总:数据库操作异常"+sqlcount)
                        TradeContext.errorCode = "0001"
                        TradeContext.errorMsg = "查询汇总:数据库操作异常"+sqlcount
                        return -2
                    else:
                        TradeContext.RecAllCount += 1
                        TradeContext.Dcount  = resulCount[0][0]
                        TradeContext.Damount = resulCount[0][1]
                        tmpStr = ""
                        tmpStr = tmpStr + str(TradeContext.EBrno) + splitStr      #网点号
                        tmpStr = tmpStr + str(TradeContext.ProCode) + splitStr    #保险类型
                        tmpStr = tmpStr + str(TradeContext.Dcount) +splitStr      #总记录条数
                        tmpStr = tmpStr + str(TradeContext.Damount) +splitStr     #总金额
                        tmpStr = tmpStr + "\n"
                        logger.info("查询汇总:tmpStr      "+str(tmpStr))
                        if (reccount >= int(TradeContext.RecStrNo)) and (reccount <= int(TradeContext.RecStrNo) + 10):
                            f.write(tmpStr)
                        
                        #打印文件
                        tmpStr = "".ljust(6)
                        tmpStr = tmpStr + str(TradeContext.EBrno).ljust(12)       #网点号
                        tmpStr = tmpStr + str(TradeContext.ProCode).ljust(19)     #保险类型
                        #关彬捷 20091124 根据单位编码获取保险公司信息
                        AfaAhAdb.ADBGetInfoByUnitno()
                        tmpStr = tmpStr + str(TradeContext.PlanName).ljust(24)    #险种名称
                        ##打印文件中加个中文说明
                        #if str(TradeContext.ProCode) == str(1):
                        #    tmpStr = tmpStr + "安贷宝                ".ljust(24) #中文说明
                        #if str(TradeContext.ProCode) == str(2):
                        #    tmpStr = tmpStr + "华夏借款人意外伤害保险".ljust(24) #中文说明
                        tmpStr = tmpStr + str(TradeContext.Dcount).ljust(13)      #总记录条数
                        tmpStr = tmpStr + str(TradeContext.Damount).ljust(28)     #总金额
                        tmpStr = tmpStr + "\n" + "".ljust(100,"-") + "\n"
                        Pf.write(tmpStr)
                        
                        reccount += 1
                else:
                    logger.info ( " [" + TradeContext.EBrno + "]生成明细表 " )
                    #返回前台总记录条数
                    resulDetail = None
                    j = 0
                    sqldetail = "select brno,workdate,note7,bankserno,userno,username,amount,revtranf,agentserialno from afa_maintransdtl where sysid = '"+TradeContext.sysId+"' and unitno = '" + TradeContext.unitno + "'"
                    if ( TradeContext.existVariable( "ProSel" ) and TradeContext.ProSel.strip() == "0" ):
                        sqldetail = sqldetail + " and note7 = '"+TradeContext.ProCode+"'"
                    sqldetail = sqldetail + " and brno = '"+TradeContext.EBrno+"'"
                    
                    #begin 20100618 蔡永贵  为了能够查询当日未对账明细修改查询条件
                    if ( TradeContext.startdate == TradeContext.enddate and TradeContext.startdate == TradeContext.workDate ):
                        sqldetail = sqldetail + " and chkflag = '9' and corpchkflag = '9'"
                    else:
                        sqldetail = sqldetail + " and chkflag = '0' and corpchkflag = '0'"
                    #end
                    
                    sqldetail = sqldetail + " and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
                    #sqldetail = sqldetail + " and chkflag = '0' and corpchkflag = '0'"
                    sqldetail = sqldetail + " and bankstatus = '0'  and revtranf = '0' order by agentserialno"
                    logger.info( str(sqldetail) )
                    resulDetail = AfaDBFunc.SelectSql(sqldetail)
                    if resulDetail is None:
                        logger.info("查询明细:数据库操作异常"+sqldetail)
                        TradeContext.errorCode = "0001"
                        TradeContext.errorMsg = "查询明细:数据库操作异常"+sqldetail
                        return -2
                    else:
                        TradeContext.RecAllCount = TradeContext.RecAllCount + len(resulDetail)
                        #如果没有交易记录则返回
                        if ( len(resulDetail) > 0 ):
                            for j in range (0,len(resulDetail)):
                                # 机构代码   交易日期   险种类型   主机流水    保单号码        客户名称      保费金额   交易流水 冲销标志
                                tmpStr = ""
                                tmpStr = tmpStr + str(resulDetail[j][0]).strip() + splitStr      #机构代码
                                tmpStr = tmpStr + str(resulDetail[j][1]).strip() + splitStr      #交易日期
                                tmpStr = tmpStr + str(resulDetail[j][2]).strip() + splitStr      #险种类型
                                tmpStr = tmpStr + str(resulDetail[j][3]).strip() + splitStr      #主机流水
                                tmpStr = tmpStr + str(resulDetail[j][4]).strip() + splitStr      #保单号码
                                tmpStr = tmpStr + str(resulDetail[j][5]).strip() + splitStr      #客户名称
                                tmpStr = tmpStr + str(resulDetail[j][6]).strip() + splitStr      #保费金额
                                #begin 20100730 蔡永贵 增加明细查询打印中台交易流水字段
                                tmpStr = tmpStr + str(resulDetail[j][8]).strip() + splitStr      #交易流水
                                #end
                                tmpStr = tmpStr + "\n"
                                AfaLoggerFunc.tradeInfo("reccount0 = [" + str(reccount) + "]")
                                if (reccount >= int(TradeContext.RecStrNo)) and (reccount < int(TradeContext.RecStrNo) + 10):
                                    AfaLoggerFunc.tradeInfo("reccount = [" + str(reccount) + "]")
                                    f.write(tmpStr)
                                    
                                tmpStr = "".ljust(6)
                                tmpStr = tmpStr + str(resulDetail[j][0]).ljust(12)      #机构代码
                                tmpStr = tmpStr + str(resulDetail[j][1]).ljust(16)      #交易日期 
                                tmpStr = tmpStr + str(resulDetail[j][2]).ljust(12)      #险种名称
                                #begin 20100203 蔡永贵增加 根据单位编码获取保险公司信息
                                AfaAhAdb.ADBGetInfoByUnitno()
                                tmpStr = tmpStr + str(TradeContext.PlanName).ljust(24)    #险种名称
                                #end   
                                #打印文件中加个中文说明
                                #if str(resulDetail[j][2]) == str(1):
                                    #tmpStr = tmpStr + "安贷宝                ".ljust(24) #中文说明
                                #if str(resulDetail[j][2]) == str(2):
                                    #tmpStr = tmpStr + "华夏借款人意外伤害保险".ljust(24) #中文说明
                                tmpStr = tmpStr + str(resulDetail[j][3]).ljust(19)      #主机流水
                                tmpStr = tmpStr + str(resulDetail[j][4]).ljust(16)      #保单号码
                                tmpStr = tmpStr + str(resulDetail[j][5]).ljust(12)      #客户名称
                                tmpStr = tmpStr + str(resulDetail[j][6]).ljust(10)      #保费金额

                                #begin 20100730 蔡永贵 增加明细查询打印中台交易流水字段
                                tmpStr = tmpStr + str(resulDetail[j][8]).rjust(19)      #交易流水
                                #end

                                tmpStr = tmpStr + "\n" + "".ljust(151,"-") + "\n"
                                Pf.write(tmpStr)
                                
                                reccount += 1
                        else:
                            logger.info( "结束生成生成明细文件(无记录)" )
                            f.close()
                            
            #打印文件表底
            if TradeContext.reportType == "1":
                tmpStr = "\n" + "".ljust(6) + "制表:" + TradeContext.tellerno + "\n"
            else:
                tmpStr = "\n" + "".ljust(6) + "制表:" + TradeContext.tellerno.ljust(10) + "会计:".ljust(15) + "出纳:".ljust(15) + "复核:".ljust(15) + "会计主管:\n"
            Pf.write(tmpStr)
            
            f.close()
            if (int(TradeContext.RecAllCount) - int(TradeContext.RecStrNo) >= 10):
                TradeContext.RecCount = 10
            else:
                TradeContext.RecCount = int(TradeContext.RecAllCount) - int(TradeContext.RecStrNo) + 1
                
            if TradeContext.RecCount <= 0:
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "起始笔数非法"
                return -2
                
            TradeContext.RecCount = str(TradeContext.RecCount)
            TradeContext.RecAllCount = str(TradeContext.RecAllCount)
            AfaLoggerFunc.tradeInfo("RecCount=[" + TradeContext.RecCount + "]")
            AfaLoggerFunc.tradeInfo("RecAllCount=[" + TradeContext.RecAllCount + "]")
            return 0
    except Exception ,e:
        TradeContext.errorCode = "0001"
        TradeContext.errorMsg = "生成安贷宝报表错误 ["+str(e)+"]"
        logger.info("生成安贷宝报表错误 ["+str(e)+"]")
        return -3
