# -*- coding: gbk -*-
##########################################################
#       名称：银保通日终函数                             #
#       日期：2009-04-01                                 #
#       时间：15:15                                      #
#       所属：赞同科技                                   #
##########################################################
import TradeContext, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc,AfaUtilTools,AfaLoggerFunc
import HostContext,AfaHostFunc,HostComm,ConfigParser
import os
from types import *
from datetime import *


################################################################################
#           银保通.公共函数
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
#           银保通.文件转换
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
#           银保通.公共函数
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
#       银保通对账
#       功能：生成第三方联机回执文件
#       日期：2008-11-04
#       说明：
#       银行编码(10)+交易日期(8)+银行区域代码(10)+储蓄所代码(10)+交易码(7)+
#       银行流水号(30)+保单号(20)+金额(12位，带小数点)+销售渠道（2位）
#       银行编码默认为"01",银行区域代码"ANHNX00001",销售渠道"01"
###########################################################
def CreCpicLjFile(logger):
    logger.info( "开始生成银保通联机交易回执文件" )
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
    print "-------------< [生成通银保通联机回执文件:共 " + str(len(records)) + "条成功记录] >------------"
    logger.info( "< [生成通银保通联机回执文件:共 " + str(len(records)) + "条成功记录] >")
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
        logger.info( "结束生成银保通联机回执文件(无记录)" )
        f.close()
    f.close()
    logger.info( "结束生成银保通联机回执文件" )
    return 0
################################################################################
#           银保通.公共函数
# 功    能：取获取文件
# 参数说明：
# 事    例：
# 
################################################################################
def getFile(logger):
    logger.info('开始接受文件'+TradeContext.fileName)
    os.system( TradeContext.getFile )
    logger.info('结束接受文件'+TradeContext.fileName)
    return 0
################################################################################
#           银保通.公共函数
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
#           银保通.公共函数
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
# 功    能：生成银保通报表
# 参数说明：
# 事    例：
# 
################################################################################
def CreatTotalReport(logger):
    try:
        resulBrno = None
        i = 0
        splitStr = "|"
        tmpStr = ""

        #如果是查询第一页的数据，将打印文件返回
        if( TradeContext.I1STAR == "1" ):
            TradeContext.PBDAFILE = TradeContext.workDate+"_"+TradeContext.brno+"_"+TradeContext.tellerno+"_"+TradeContext.reportType+".txt"
            PfileName = os.environ['HOME']+"/afa/data/ybt/report/P_"+TradeContext.PBDAFILE
            TradeContext.P_PBDAFILE = "P_" + TradeContext.PBDAFILE
            logger.info ( " 打印文件路径名称  "+PfileName)
            try:
                Pf = file(PfileName,"w")
            except:
                logger.info("生成打印文件["+PfileName+"]失败")
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "生成打印文件["+PfileName+"]失败"
                return -2
            
            logger.info ( " 开始生成银保通总报表文件，日期为["+TradeContext.startdate+">>>>>"+TradeContext.enddate+"]" )
            
            sqlcount = "select brno,salerno,unitno,productid,count(*),sum(cast(amount as decimal(15,2))) from (select "
            if ( len(str(TradeContext.instno.strip()))>0):
                sqlcount = sqlcount + " brno,"
            else:
                sqlcount = sqlcount + " '' as brno,"
            if ( len(str(TradeContext.salerno.strip()))>0):
                sqlcount = sqlcount + "  trim(substr(note6,1,abs((locate('|',note6,1)-1)))) as salerno,"
            else:
                sqlcount = sqlcount + " '' as salerno,"
            if ( len(str(TradeContext.insuid.strip()))>0):
                sqlcount = sqlcount + " unitno,"
            else:
                sqlcount = sqlcount + " '' as unitno,"
            if ( len(str(TradeContext.productid.strip()))>0):
                sqlcount = sqlcount + " trim(substr(note8,1,abs((locate('|',note8,1)-1)))) as productid,"
            else:
                sqlcount = sqlcount + " '' as productid,"
            sqlcount=sqlcount+"amount from afa_maintransdtl"
            sqlcount = sqlcount + " where sysid = '"+TradeContext.sysId+"' and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            if ( TradeContext.sbgd=='02' and TradeContext.USGD=="20"):
                #省联社主管可以查询所有业务
                if( len(str(TradeContext.instno.strip()))>0):
                    sqlcount = sqlcount + " and brno='"+TradeContext.instno+"'"
            elif ( TradeContext.sbgd=='33' and TradeContext.USGD=="20"):
                #联社财务部可以查询本联社
                if( len(str(TradeContext.instno.strip()))>0):
                    sqlcount = sqlcount + " and brno='"+TradeContext.instno+"'"
                else:
                    sqlcount = sqlcount + " and brno like '"+TradeContext.brno[0:6]+"%'"
            elif ( TradeContext.sbgd!='02' and TradeContext.sbgd!='33' and TradeContext.USGD=="20"):
                #本机构主管可查询本机构所有业务
                sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
            else:
                sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
                sqlcount = sqlcount + " and tellerno ='"+TradeContext.tellerno+"'"
            if ( len(str(TradeContext.salerno.strip()))>0):
                sqlcount = sqlcount + " and trim(substr(note6,1,abs((locate('|',note6,1)-1))))='"+TradeContext.salerno+"'"
            if ( len(str(TradeContext.insuid.strip()))>0):
                sqlcount = sqlcount + " and unitno='"+TradeContext.insuid+"'"
            if ( len(str(TradeContext.productid.strip()))>0):
                sqlcount = sqlcount + " and trim(substr(note8,1,abs((locate('|',note8,1)-1))))='"+TradeContext.productid+"'"
            if ( TradeContext.startdate == TradeContext.workDate ):
                 sqlcount = sqlcount + "and chkflag = '9' and corpstatus='0'"
            else:
                 sqlcount = sqlcount + "and chkflag = '0' "
            sqlcount = sqlcount + " and bankstatus = '0' and revtranf = '0' "
            sqlcount = sqlcount + " ) t1 group by brno,salerno,unitno,productid"
                                 
            logger.info( "查询语句为:"+str(sqlcount))
            resulBrno = AfaDBFunc.SelectSql(sqlcount)
            logger.info( "查询结果:"+str(len(resulBrno)) )
            
            if resulBrno is None:
                logger.info("查询银保通数据:数据库操作异常"+sqlcount)
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "查询网点号:数据库操作异常"+sqlcount
                return -2
            elif ( len(resulBrno) == 0 ):
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "未查询到相关的交易记录"
                return -3
            else:
                TradeContext.RecAllCount = str(len(resulBrno))
            
            tmpStr = "".ljust(40) + "代理保险汇总表\n"
            tmpStr = tmpStr + "      起始日期:  " + TradeContext.startdate + "                                 终止日期:" + TradeContext.workDate + "\n"
            tmpStr = tmpStr + "".ljust(132,"=") + "\n"
            tmpStr = tmpStr + "      机构号      营销员员工号  保险公司                险种                          笔数   保险金额        \n"
            Pf.write(tmpStr)
            
            for i in range( 0, len(resulBrno) ):
                tmpStr = "      "
                tmpStr = tmpStr + str(resulBrno[i][0]).ljust(12,' ')      																	#机构号
                tmpStr = tmpStr + str(resulBrno[i][1]).ljust(14,' ')      																	#营销员员工号
                tmpStr = tmpStr + getUnitName(TradeContext.sysId,str(resulBrno[i][2])).ljust(24,' ')      	#保险公司名称
                tmpStr = tmpStr + str(resulBrno[i][3]).ljust(30,' ')      																	#险种名称
                tmpStr = tmpStr + str(resulBrno[i][4]).ljust(7,' ')       																	#笔数
                tmpStr = tmpStr + str(resulBrno[i][5]).ljust(14,' ')     																		#保险金额
                tmpStr = tmpStr + "\n"
                logger.info("查询汇总tmpStr["+str(i)+"]:"+str(tmpStr))
                Pf.write(tmpStr)
            
            #打印文件表底
            tmpStr = ""
            tmpStr = "\n" + "".ljust(6) + "制表:" + TradeContext.tellerno + "\n"
            Pf.write(tmpStr)
            Pf.close()
             
        #返回查询记录
        sqlcount = "select * from (select brno,salerno,unitno,productid,tnum,tamount,rownumber() OVER () AS rn from (select brno,salerno,unitno,productid,count(*) as tnum,sum(cast(amount as decimal(15,2))) as tamount"
        sqlcount = sqlcount + " from (select "
        if ( len(str(TradeContext.instno.strip()))>0):
            sqlcount = sqlcount + " brno,"
        else:
            sqlcount = sqlcount + " '' as brno,"
        if ( len(str(TradeContext.salerno.strip()))>0):
            sqlcount = sqlcount + "  trim(substr(note6,1,abs((locate('|',note6,1)-1)))) as salerno,"
        else:
            sqlcount = sqlcount + " '' as salerno,"
        if ( len(str(TradeContext.insuid.strip()))>0):
            sqlcount = sqlcount + " unitno,"
        else:
            sqlcount = sqlcount + " '' as unitno,"
        if ( len(str(TradeContext.productid.strip()))>0):
            sqlcount = sqlcount + " trim(substr(note8,1,abs((locate('|',note8,1)-1)))) as productid,"
        else:
            sqlcount = sqlcount + " '' as productid,"
        sqlcount=sqlcount+"amount from afa_maintransdtl"
        sqlcount = sqlcount + " where sysid = '"+TradeContext.sysId+"' and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
        if ( TradeContext.sbgd=='02' and TradeContext.USGD=="20"):
            #省联社主管可以查询所有业务
            if( len(str(TradeContext.instno.strip()))>0):
                sqlcount = sqlcount + " and brno='"+TradeContext.instno+"'"
        elif ( TradeContext.sbgd=='33' and TradeContext.USGD=="20"):
            #联社财务部可以查询本联社
            if( len(str(TradeContext.instno.strip()))>0):
                sqlcount = sqlcount + " and brno='"+TradeContext.instno+"'"
            else:
                sqlcount = sqlcount + " and brno like '"+TradeContext.brno[0:6]+"%'"
        elif ( TradeContext.sbgd!='02' and TradeContext.sbgd!='33' and TradeContext.USGD=="20"):
                #本机构主管可查询本机构所有业务
            sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
        else:
            sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
            sqlcount = sqlcount + " and tellerno ='"+TradeContext.tellerno+"'"
        if ( len(str(TradeContext.salerno.strip()))>0):
            sqlcount = sqlcount + " and trim(substr(note6,1,abs((locate('|',note6,1)-1))))='"+TradeContext.salerno+"'"
        if ( len(str(TradeContext.insuid.strip()))>0):
            sqlcount = sqlcount + " and unitno='"+TradeContext.insuid+"'"
        if ( len(str(TradeContext.productid.strip()))>0):
            sqlcount = sqlcount + " and trim(substr(note8,1,abs((locate('|',note8,1)-1))))='"+TradeContext.productid+"'"
        if ( TradeContext.startdate == TradeContext.workDate ):
            sqlcount = sqlcount + "and chkflag = '9' and corpstatus='0'"
        else:
            sqlcount = sqlcount + "and chkflag = '0' "
        sqlcount = sqlcount + " and bankstatus = '0' and revtranf = '0' "
        sqlcount = sqlcount + " ) t1 group by brno,salerno,unitno,productid) a ) b where b.rn between "+TradeContext.I1STAR+" and "+str(int(TradeContext.I1STAR)+int(TradeContext.I1RCNM)-1)
        
        logger.info( "查询语句为:"+str(sqlcount))
        resulBrno = AfaDBFunc.SelectSql(sqlcount)
        logger.info( "查询结果:"+str(len(resulBrno)) )
        
        if resulBrno is None:
            logger.info("查询银保通数据:数据库操作异常"+sqlcount)
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "查询网点号:数据库操作异常"+sqlcount
            return -2
        elif ( len(resulBrno) == 0 ):
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg = "未查询到相关的交易记录"
            return -3
        else:
            TradeContext.RecAllCount = str(len(resulBrno))
            
        INSTNO = []
        SALERNO = []
        INSUID = []
        PRODUCTID = []
        NUM = []
        AMOUNT = []        
        for i in range( 0, len(resulBrno) ):
            INSTNO.append(str(resulBrno[i][0]))
            SALERNO.append(str(resulBrno[i][1]))
            INSUID.append(getUnitName(TradeContext.sysId,str(resulBrno[i][2])))
            PRODUCTID.append(str(resulBrno[i][3]))
            NUM.append(str(resulBrno[i][4]))
            AMOUNT.append(str(resulBrno[i][5]))
            
        TradeContext.INSTNO = INSTNO
        TradeContext.SALERNO = SALERNO
        TradeContext.INSUID = INSUID
        TradeContext.PRODUCTID = PRODUCTID
        TradeContext.NUM = NUM
        TradeContext.AMOUNT = AMOUNT
        TradeContext.O1ACUR = TradeContext.RecAllCount
              
        return 0
    except Exception ,e:
        TradeContext.errorCode = "0001"
        TradeContext.errorMsg = "银保通明细查询错误 ["+str(e)+"]"
        logger.info("银保通明细查询错误 ["+str(e)+"]")
        return -3



################################################################################
#           报表生成.生成明细报表
# 功    能：生成银保通明细报表
# 参数说明：
# 事    例：
# 
################################################################################
def CreatDetailReport(logger):
    try:
        resulBrno = None
        i = 0
        splitStr = "|"
        tmpStr = ""
        
        #如果是查询第一页的数据，将打印文件返回
        if( TradeContext.I1STAR == "1" ):
            logger.info ( " 开始生成银保通明细报表文件，日期为["+TradeContext.startdate+">>>>>"+TradeContext.enddate+"]" )
            #打印文件
            TradeContext.PBDAFILE = TradeContext.workDate+"_"+TradeContext.brno+"_"+TradeContext.tellerno+"_"+TradeContext.reportType+".txt"
            PfileName = os.environ['HOME']+"/afa/data/ybt/report/P_"+TradeContext.PBDAFILE
            TradeContext.P_PBDAFILE = "P_" + TradeContext.PBDAFILE
            logger.info ( " 打印文件路径名称  "+PfileName)
            try:
                Pf = file(PfileName,"w")
            except:
                logger.info("生成打印文件["+PfileName+"]失败")
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "生成打印文件["+PfileName+"]失败"
                return -2
            
            sqlcount = "select brno,unitno,workdate,note8,bankserno,agentserialno,note9,userno,note4,cast(amount as decimal(15,2)) as amount from afa_maintransdtl"
            sqlcount = sqlcount + " where sysid = '"+TradeContext.sysId+"' and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
            if ( TradeContext.sbgd=='02' and TradeContext.USGD=="20"):
                #省联社主管可以查询所有业务
                if( len(str(TradeContext.INSTNO.strip()))>0):
                    sqlcount = sqlcount + " and brno='"+TradeContext.INSTNO+"'"
            elif ( TradeContext.sbgd=='33' and TradeContext.USGD=="20"):
                #联社财务部可以查询本联社
                if( len(str(TradeContext.INSTNO.strip()))>0):
                    sqlcount = sqlcount + " and brno='"+TradeContext.INSTNO+"'"
                else:
                    sqlcount = sqlcount + " and brno like '"+TradeContext.brno[0:6]+"%'"
            elif ( TradeContext.sbgd!='02' and TradeContext.sbgd!='33' and TradeContext.USGD=="20"):
                #本机构主管可查询本机构所有业务
                sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
            else:
                sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
                sqlcount = sqlcount + " and tellerno ='"+TradeContext.tellerno+"'"
            if ( len(str(TradeContext.insuid.strip()))>0):                                                            
                sqlcount = sqlcount + " and unitno='"+TradeContext.insuid+"'"
            if ( len(str(TradeContext.productid.strip()))>0):                                                         
                sqlcount = sqlcount + " and note8 like '"+TradeContext.productid+"|%|%|%|'" 
            if ( len(str(TradeContext.TRANSRNO.strip()))>0):                                                          
                sqlcount = sqlcount + " and agentserialno='"+TradeContext.TRANSRNO+"'"
            if ( len(str(TradeContext.PAYACC.strip()))>0):                                                            
                sqlcount = sqlcount + " and draccno='"+TradeContext.PAYACC+"'" 
            if ( len(str(TradeContext.PAYCARD.strip()))>0):                                                           
                sqlcount = sqlcount + " and craccno='"+TradeContext.PAYCARD+"'"                                       
            if ( len(str(TradeContext.APPLNO.strip()))>0):                                                            
                sqlcount = sqlcount + " and note9 like '%|"+TradeContext.APPLNO+"|%|%'"                               
            if ( len(str(TradeContext.TBR_NAME.strip()))>0):                                                          
                sqlcount = sqlcount + " and note4 like '"+TradeContext.TBR_NAME+"|%|'"                                
            if ( str(TradeContext.PREMIUM.strip())!='0.00'):                                                          
                sqlcount = sqlcount + " and amount ='"+TradeContext.PREMIUM+"'"                                       
            if ( len(str(TradeContext.salerno.strip()))>0):                                                           
                sqlcount = sqlcount + " and trim(left(note6,abs((locate('|',note6,1)-1))))='"+TradeContext.salerno+"'"
            if ( TradeContext.startdate == TradeContext.workDate ):
                 sqlcount = sqlcount + " and chkflag = '9' and corpstatus='0'"
            else:
                 sqlcount = sqlcount + " and chkflag = '0' "
            sqlcount = sqlcount + " and bankstatus = '0' and revtranf = '0' "
            sqlcount = sqlcount + " order by agentserialno,workdate"
                   
            logger.info( "查询语句为:"+str(sqlcount) )
            resulBrno = AfaDBFunc.SelectSql(sqlcount)
            logger.info( "查询结果:"+str(len(resulBrno)) )
            
            if resulBrno is None:
                logger.info("查询银保通数据:数据库操作异常"+sqlcount)
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "查询银保通数据:数据库操作异常"+sqlcount
                return -2
            elif ( len(resulBrno) == 0 ):
                TradeContext.errorCode = "0000"
                TradeContext.errorMsg = "未查询到相关的交易记录"
                return -3
            else:
                TradeContext.O1ACUR = str(len(resulBrno))
            
            tmpStr = "".ljust(40) + "代理保险明细表\n"
            tmpStr = tmpStr + "      起始日期:  " + TradeContext.startdate + "                                 终止日期:" + TradeContext.workDate + "\n"
            tmpStr = tmpStr + "".ljust(110,"=") + "\n"
            tmpStr = tmpStr + "机构代码   保险公司   交易日期 险种      交易流水 保单号                     保单印刷号 客户名称 保费金额     \n"
            Pf.write(tmpStr)
            
            for i in range( 0, len(resulBrno) ):
                tmpStr = ""
                tmpStr = tmpStr + str(resulBrno[i][0]).ljust(11,' ')     		        														#机构号
                tmpStr = tmpStr + getUnitName(TradeContext.sysId,str(resulBrno[i][1])).ljust(11,' ')      			#保险公司
                tmpStr = tmpStr + str(resulBrno[i][2]).ljust(9,' ')      																			#交易日期
                if (len(resulBrno[i][3].split('|'))>1):
                    tmpStr = tmpStr + str(resulBrno[i][3].split('|')[0]).ljust(10,' ')       										#险种名称
                else:
                    tmpStr = tmpStr + "".ljust(10,' ')
                #tmpStr = tmpStr + str(resulBrno[i][4]).ljust(11,' ')      																			#账务流水
                tmpStr = tmpStr + str(resulBrno[i][5]).ljust(9,' ')       																			#交易流水
                if (len(resulBrno[i][6].split('|'))>1):
                    tmpStr = tmpStr + str(resulBrno[i][6].split('|')[2]).ljust(27,' ')      										#保单号
                else:
                    tmpStr = tmpStr + "".ljust(26,' ')
                tmpStr = tmpStr + str(resulBrno[i][7]).ljust(11,' ')      																			#保单印刷号
                if (len(resulBrno[i][8].split('|'))>1):
                    tmpStr = tmpStr + str(resulBrno[i][8]).split('|')[0].ljust(9,' ')      										#客户名称
                else:
                    tmpStr = tmpStr + "".ljust(9,' ')    
                tmpStr = tmpStr + str(resulBrno[i][9]).ljust(13,' ')      																			#保费金额
                tmpStr = tmpStr + "\n"
                logger.info("查询明细tmpStr["+str(i)+"]:"+str(tmpStr))
                Pf.write(tmpStr)
            
            #查询合计金额
            sql="select sum(amount) from ("+sqlcount+") as t1"
            logger.info( "查询语句为:"+str(sql) )
            resulBrno = AfaDBFunc.SelectSql(sql)
            logger.info( "查询结果:"+str(resulBrno) )
            
            if resulBrno is None:
                logger.info("查询银保通数据:数据库操作异常"+sqlcount)
                TradeContext.errorCode = "0001"
                TradeContext.errorMsg = "查询银保通数据:数据库操作异常"+sqlcount
                return -2
            elif ( len(resulBrno) == 0 ):
                TradeContext.errorCode = "0000"
                TradeContext.errorMsg = "未查询到相关的交易记录"
                return -3
            else:
                totalamount = str(resulBrno[0][0])
            #打印文件表底
            tmpStr = "\n"+"".ljust(87,' ')+"合计金额："+totalamount
            tmpStr = tmpStr+"\n" + "".ljust(6) + "制表:" + TradeContext.tellerno + "\n"
            Pf.write(tmpStr)
            Pf.close()
        
        #返回查询记录
        sqlcount = "select * from (select brno,unitno,workdate,note8,bankserno,agentserialno,note9,userno,note4,cast(amount as decimal(15,2)) as amount,rownumber() OVER (ORDER BY agentserialno,workdate ASC) AS rn from afa_maintransdtl"
        sqlcount = sqlcount + " where sysid = '"+TradeContext.sysId+"' and workdate >= '"+TradeContext.startdate+"' and workdate <= '"+TradeContext.enddate+"'"
        if ( TradeContext.sbgd=='02' and TradeContext.USGD=="20"):
            #省联社主管可以查询所有业务
            if( len(str(TradeContext.INSTNO.strip()))>0):
                sqlcount = sqlcount + " and brno='"+TradeContext.INSTNO+"'"
        elif ( TradeContext.sbgd=='33' and TradeContext.USGD=="20"):
            #联社财务部可以查询本联社
            if( len(str(TradeContext.INSTNO.strip()))>0):
                sqlcount = sqlcount + " and brno='"+TradeContext.INSTNO+"'"
            else:
                sqlcount = sqlcount + " and brno like '"+TradeContext.brno[0:6]+"%'"
        elif ( TradeContext.sbgd!='02' and TradeContext.sbgd!='33' and TradeContext.USGD=="20"):
            #本机构主管可查询本机构所有业务
            sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
        else:
            sqlcount = sqlcount + " and brno='"+TradeContext.brno+"'"
            sqlcount = sqlcount + " and tellerno ='"+TradeContext.tellerno+"'"
        if ( len(str(TradeContext.insuid.strip()))>0):
            sqlcount = sqlcount + " and unitno='"+TradeContext.insuid+"'"
        if ( len(str(TradeContext.productid.strip()))>0):
            sqlcount = sqlcount + " and note8 like '"+TradeContext.productid+"|%|%|%|'"
        if ( len(str(TradeContext.TRANSRNO.strip()))>0):
            sqlcount = sqlcount + " and agentserialno='"+TradeContext.TRANSRNO+"'"
        if ( len(str(TradeContext.PAYACC.strip()))>0):
            sqlcount = sqlcount + " and draccno='"+TradeContext.PAYACC+"'"
        if ( len(str(TradeContext.PAYCARD.strip()))>0):
            sqlcount = sqlcount + " and craccno='"+TradeContext.PAYCARD+"'"
        if ( len(str(TradeContext.APPLNO.strip()))>0):
            sqlcount = sqlcount + " and note9 like '%|"+TradeContext.APPLNO+"|%|%'"
        if ( len(str(TradeContext.TBR_NAME.strip()))>0):
            sqlcount = sqlcount + " and note4 like '"+TradeContext.TBR_NAME+"|%|'"
        if ( str(TradeContext.PREMIUM.strip())!='0.00'):
            sqlcount = sqlcount + " and amount ='"+TradeContext.PREMIUM+"'"
        if ( len(str(TradeContext.salerno.strip()))>0):
            sqlcount = sqlcount + " and trim(left(note6,abs((locate('|',note6,1)-1))))='"+TradeContext.salerno+"'"
        if ( TradeContext.startdate == TradeContext.workDate ):
            sqlcount = sqlcount + " and chkflag = '9' and corpstatus='0'"
        else:
            sqlcount = sqlcount + " and chkflag = '0' "
        sqlcount = sqlcount + " and bankstatus = '0' and revtranf = '0' "
        sqlcount = sqlcount + " ) a where a.rn between "+TradeContext.I1STAR+" and "+str(int(TradeContext.I1STAR)+int(TradeContext.I1RCNM)-1)
        
        logger.info( "查询语句为:"+str(sqlcount) )
        resulBrno = AfaDBFunc.SelectSql(sqlcount)
        logger.info( "查询结果:"+str(resulBrno) )
        
        if resulBrno is None:
            logger.info("查询银保通数据:数据库操作异常"+sqlcount)
            TradeContext.errorCode = "0001"
            TradeContext.errorMsg = "查询网点号:数据库操作异常"+sqlcount
            return -2
        elif ( len(resulBrno) == 0 ):
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg = "未查询到相关的交易记录"
            return -3
        else:
            TradeContext.O1ACUR = str(len(resulBrno)) 
        
        INSTNO = []
        INSUID = []
        TRANDATE = []
        PRODUCTID =[]
        ACCSRNO = []
        TRANSRNO =[]
        POLICY=[]
        BD_PRINT_NO =[] 
        TBR_NAME = []
        PREMIUM=[]
        for i in range( 0, len(resulBrno) ):
            INSTNO.append(str(resulBrno[i][0]))
            INSUID.append(getUnitName(TradeContext.sysId,str(resulBrno[i][1])))
            TRANDATE.append(str(resulBrno[i][2]))
            if (len(resulBrno[i][3].split('|'))>1):
                PRODUCTID.append(str(resulBrno[i][3].split('|')[0]))
            else:
                PRODUCTID.append("")
            ACCSRNO.append(str(resulBrno[i][4]))
            TRANSRNO.append(str(resulBrno[i][5]))
            if (len(resulBrno[i][6].split('|'))>1):
                POLICY.append(str(resulBrno[i][6].split('|')[2]))
            else:
                POLICY.append("")
            BD_PRINT_NO.append(str(resulBrno[i][7]))
            if (len(resulBrno[i][8].split('|'))>1):
                TBR_NAME.append(str(resulBrno[i][8]).split('|')[0])
            else:
                TBR_NAME.append("")
            PREMIUM.append(str(resulBrno[i][9]))
        
        TradeContext.INSTNO = INSTNO
        TradeContext.INSUID = INSUID
        TradeContext.TRANDATE = TRANDATE
        TradeContext.PRODUCTID = PRODUCTID
        TradeContext.ACCSRNO = ACCSRNO
        TradeContext.TRANSRNO = TRANSRNO
        TradeContext.POLICY = POLICY
        TradeContext.BD_PRINT_NO=BD_PRINT_NO
        TradeContext.TBR_NAME=TBR_NAME
        TradeContext.PREMIUM = PREMIUM
        
        return 0
    except Exception ,e:
        TradeContext.errorCode = "0001"
        TradeContext.errorMsg = "生成银保通报表错误 ["+str(e)+"]"
        logger.info("生成银保通报表错误 ["+str(e)+"]")
        return -3



################################################################################     
 #  银保通公共函数 swap()                                                   
 # 功    能：转换不同保险公司的类型                                                      
 # 参数说明：                                                                         
 # 事    例：                                                                         
 #                                                                                    
 ################################################################################ 
def swap( ):                                                                         
                                                                                    
    filename = '/home/maps/afa/application/ybt/config/busino_' + TradeContext.unitno + '.conf'    #配置文件名
    AfaLoggerFunc.tradeInfo('文件名：' + filename)
    
    sexType   = 'sexType'                                                                      #sexType:配置文件的性别选项
    idType    = 'idType'                                                                       #证件类型 
    tormType  = 'tormType'                                                                     #保险期间类型   
    payMethod = 'payMethod'                                                                    #缴费方式
    Rela      = 'Rela'                                                                         #关系
    workType  = 'workType'                                                                     #职业类别          
    
    #转换性别类型
    if (TradeContext.existVariable( "tbr_sex" ) and len(TradeContext.tbr_sex.strip()) > 0 ):                                                                     
        AfaLoggerFunc.tradeInfo("映射前的性别："+ TradeContext.tbr_sex  )
        TradeContext.pre_tbr_sex = TradeContext.tbr_sex
        if not datamap(sexType,TradeContext.tbr_sex,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '该保险公司不存在该种性别选项，请检查录入项'                     
            return False                                                    
        else:                                                                         
            TradeContext.tbr_sex = datamap(sexType,TradeContext.tbr_sex,filename)
    else:
         TradeContext.tbr_sex=''
    AfaLoggerFunc.tradeInfo("映射后的性别："+ TradeContext.tbr_sex )
         
    #转换证件类型
    #投保人证件类型
    if (TradeContext.existVariable( "tbr_idtype" ) and len(TradeContext.tbr_idtype.strip()) > 0 ):                                                                     
        AfaLoggerFunc.tradeInfo("映射前的投保人证件类型："+ TradeContext.tbr_idtype )
        TradeContext.pre_tbr_idtype = TradeContext.tbr_idtype
        if not datamap(idType,TradeContext.tbr_idtype,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '该保险公司不存在该种投保人证件类型选项，请检查录入项'                     
            raise AfaFlowControl.flowException()                                                              
        else:                                                                         
            TradeContext.tbr_idtype = datamap(idType,TradeContext.tbr_idtype,filename)
    else:
         TradeContext.tbr_idtype='' 
    AfaLoggerFunc.tradeInfo("映射后的投保人证件类型："+ TradeContext.tbr_idtype )
    
    
    
    #被保人证件类型 
    if (TradeContext.existVariable( "bbr_idtype" ) and len(TradeContext.bbr_idtype.strip()) > 0 ):                                                                     
        AfaLoggerFunc.tradeInfo("映射前的被保人证件类型："+ TradeContext.bbr_idtype )
        TradeContext.pre_bbr_idtype = TradeContext.bbr_idtype  
        if not datamap(idType,TradeContext.bbr_idtype,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '该保险公司不存在该种被保人类型选项，请检查录入项'                     
            raise AfaFlowControl.flowException()                                                              
        else:                                                                         
            TradeContext.bbr_idtype = datamap(idType,TradeContext.bbr_idtype,filename)
    else:
         TradeContext.bbr_idtype=''
    AfaLoggerFunc.tradeInfo("映射后的被保人证件类型："+ TradeContext.bbr_idtype ) 
    
    
    #受益人证件类型
    if (TradeContext.existVariable( "syr_idtype" )): 
        TradeContext.pre_syr_idtype = TradeContext.syr_idtype
        for i in range(0,len(TradeContext.syr_idtype)):
            if len(TradeContext.syr_idtype[i].strip()) > 0:
                AfaLoggerFunc.tradeInfo("映射前的受益人证件类型："+ TradeContext.syr_idtype[i] ) 
                if not datamap(idType,TradeContext.syr_idtype[i],filename):                                           
                    TradeContext.errorCode = 'E9999'                                               
                    TradeContext.errorMsg  = '该保险公司不存在该种受益人证件类型选项，请检查录入项'                     
                    raise AfaFlowControl.flowException()                                                            
                else:                                                                         
                    TradeContext.syr_idtype[i] = datamap(idType,TradeContext.syr_idtype[i],filename)
                AfaLoggerFunc.tradeInfo("映射后的受益人证件类型："+ TradeContext.syr_idtype[i] )
    else:
         TradeContext.syr_idtype='' 
        
  
   
    #保险期间类型 
    if (TradeContext.existVariable( "tormtype" ) and len(TradeContext.tormtype.strip()) > 0 ):
        TradeContext.pre_tormtype = TradeContext.tormtype
        AfaLoggerFunc.tradeInfo("映射前的保险期间类型："+ TradeContext.tormtype ) 
        if not datamap(tormType,TradeContext.tormtype,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '该保险公司不存在该种保险期间类型选项，请检查录入项'                     
            raise AfaFlowControl.flowException()                                                              
        else:                                                                         
            TradeContext.tormtype = datamap(tormType,TradeContext.tormtype,filename)
    else:
         TradeContext.tormtype=''  
    AfaLoggerFunc.tradeInfo("映射后的保险期间类型："+ TradeContext.tormtype )    
    
    
    #缴费方式
    if (TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
        TradeContext.pre_paymethod = TradeContext.paymethod
        AfaLoggerFunc.tradeInfo("映射前的缴费方式："+ TradeContext.pre_paymethod )
        if not datamap(payMethod,TradeContext.paymethod,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '该保险公司不存在该种缴费方式选项，请检查录入项'                     
            raise AfaFlowControl.flowException()                                                             
        else:                                                                         
            TradeContext.paymethod = datamap(payMethod,TradeContext.paymethod,filename)
    else:
         TradeContext.paymethod=''
   
    AfaLoggerFunc.tradeInfo("映射后的缴费方式："+ TradeContext.paymethod )
   
   
    #关系
    #与投保人关系 
    if (TradeContext.existVariable( "tbr_bbr_rela" ) and len(TradeContext.tbr_bbr_rela.strip()) > 0 ): 
        TradeContext.pre_tbr_bbr_rela = TradeContext.tbr_bbr_rela
        AfaLoggerFunc.tradeInfo("映射前的与投保人关系>>>>>>>>>>>>>>："+ TradeContext.pre_tbr_bbr_rela )
        AfaLoggerFunc.tradeInfo("映射前的与投保人关系："+ TradeContext.tbr_bbr_rela )
        if not datamap(Rela,TradeContext.tbr_bbr_rela,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '该保险公司不存在该种投保人与被保人关系选项，请检查录入项'                     
            raise AfaFlowControl.flowException()                                                             
        else:                                                                         
            TradeContext.tbr_bbr_rela = datamap(Rela,TradeContext.tbr_bbr_rela,filename)
    else:
         TradeContext.tbr_bbr_rela=''       
    AfaLoggerFunc.tradeInfo("映射后的与投保人关系："+ TradeContext.tbr_bbr_rela )
    
    
    #与受益人关系 
    if (TradeContext.existVariable( "syr_bbr_rela" ) ): 
        TradeContext.pre_syr_bbr_rela = TradeContext.syr_bbr_rela
        for i in range(0,len(TradeContext.syr_bbr_rela)):
            if len(TradeContext.syr_bbr_rela[i].strip()) > 0:
                AfaLoggerFunc.tradeInfo("映射前的与受益人关系："+ TradeContext.syr_bbr_rela[i] + '第' + str(i) + '次')
                if not datamap(Rela,TradeContext.syr_bbr_rela[i],filename):                                           
                    TradeContext.errorCode = 'E9999'                                               
                    TradeContext.errorMsg  = '该保险公司不存在该种受益人与被保人关系选项，请检查录入项'                     
                    raise AfaFlowControl.flowException()                                                              
                else:                                                                         
                    TradeContext.syr_bbr_rela[i] = datamap(Rela,TradeContext.syr_bbr_rela[i],filename)
                AfaLoggerFunc.tradeInfo("映射后的与受益人关系："+ TradeContext.syr_bbr_rela[i] )  
    else:
         TradeContext.syr_bbr_rela=''
    
      
    
    #职业
    if (TradeContext.existVariable( "bbr_worktype" ) and len(TradeContext.bbr_worktype.strip()) > 0 ):
        TradeContext.pre_bbr_worktype = TradeContext.bbr_worktype
        AfaLoggerFunc.tradeInfo("映射前的职业："+ TradeContext.bbr_worktype )
        if not datamap(workType,TradeContext.bbr_worktype,filename):                                           
            TradeContext.errorCode = 'E9999'                                               
            TradeContext.errorMsg  = '该保险公司不存在该种职业类别选项，请检查录入项'                     
            raise AfaFlowControl.flowException()                                                              
        else:                                                                         
            TradeContext.bbr_worktype = datamap(workType,TradeContext.bbr_worktype,filename)
    else:
         TradeContext.bbr_worktype=''      
    AfaLoggerFunc.tradeInfo("映射后的职业："+ TradeContext.bbr_worktype )
 
 
         
################################################################################     
# 银保通公共函数 datemap()                                                   
# 功    能：转换不同保险公司的类型                                                      
# 参数说明：                                                                         
# 事    例：                                                                         
#                                                                                    
################################################################################        
         
def datamap(var,option,filename):

    try:

        config = ConfigParser.ConfigParser( )
       
        config.readfp ( open( filename ) )
        var = config.get( var,option)
        
        return var

    except Exception, e:
        AfaLoggerFunc.tradeInfo("转换异常，异常信息："+ str(e) )
        TradeContext.errorCode = "E0001"
        TradeContext.errorMsg  = "选项映射错误，请检查录入项"
        return False         

################################################################################     
# 银保通公共函数                                                    
# 功    能：根据保险公司代码查询保险公司名称                                                      
# 参数说明：                                                                         
# 事    例：                                                                         
#                                                                                    
################################################################################        
         
def getUnitName(sysid,unitno):
    sql="select unitsname from afa_unitadm where sysid='"+sysid+"' and unitno='"+unitno+"'"
    result = AfaDBFunc.SelectSql(sql)
    if result is None:
        TradeContext.errorCode = "0001"
        TradeContext.errorMsg = "查询保险公司信息:数据库操作异常"+sql
        return -2
    elif ( len(result) == 0 ):
        return str(unitno)
    else:
        return result[0][0]

################################################################################
# 银保通文件生成                                  
# 功    能：根据不同的保险公司生成相应的现金价值文件                           
# 参数说明：                                                                  
# 事    例：                                                                   
#                                                                              
################################################################################    
def createFile( ):
    
    TradeContext.cashFileName = TradeContext.brno + "_" + TradeContext.tellerno + "_" + TradeContext.unitno + "_cash.txt"
    fileName = os.environ['HOME'] + "/afa/data/ybt/cash/" + TradeContext.cashFileName
    
    #生成中国人寿现金价值文件
    if TradeContext.unitno == '0001':
        return createZgrsFile( fileName )
        
    #生成太平洋现金价值文件
    elif TradeContext.unitno == '0002':
        return createCpicFile( fileName )
        
    #生成华夏现金价值文件
    elif TradeContext.unitno == '0003':
        return createHXFile( fileName )
        
    #生成幸福人寿现金价值文件
    elif TradeContext.unitno =='0004':
        return createHappyFile( fileName )
        
    #生成泰康人寿现金价值文件               
    elif TradeContext.unitno =='0005':      
        return createTaikangFile( fileName )
        
    #生成人保寿险现金价值文件               
    elif TradeContext.unitno =='0006':      
        return createRbsxFile( fileName ) 
    
    #生成生命人寿现金价值文件
    elif TradeContext.unitno =='0007':
        return createLifeFile( fileName )
        
    #生成人保健康现金价值文件
    elif TradeContext.unitno =='0008':
        return createRbjkFile( fileName )
        
    else:
        TradeContext.errorCode = 'F001'
        TradeContext.errorMsg  = '没有该保险公司代码，生成现金价值文件失败'
        return False

################################################################################
# 银保通文件生成                                  
# 功    能：生成太平洋现金价值文件                           
# 参数说明：                                                                  
# 事    例：                                                                   
#                                                                              
################################################################################            
def createCpicFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '太平洋---开始生成现金价值表【' + fileName + '】' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #根据实际需要先空出47行
        for i in range( 47 ):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " 保单现金价值（元/份）".ljust( 105,  " " ) + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.year1.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year2.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year3.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year4.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year5.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year6.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year7.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.cash1.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash2.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash3.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash4.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash5.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash6.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash7.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.year8.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year9.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year10.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year11.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year12.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year13.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year14.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.cash8.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash9.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash10.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash11.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash12.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash13.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash14.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '太平洋--生成现金价值表成功' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "太平洋--生成现金价值表失败"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

################################################################################
# 银保通文件生成                                  
# 功    能：生成中国人寿现金价值文件                           
# 参数说明：                                                                  
# 事    例：                                                                   
#                                                                              
################################################################################            
def createZgrsFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '中国人寿---开始生成现金价值表【' + fileName + '】' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #根据实际需要，先空出8行
        for i in range(0,8):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(37,' ') + "现    金    价    值    表\n\n"
        tmpStr = tmpStr + "".ljust(32,' ') + "（以保单载明的每1000元保险费为标准）\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "险种名称："
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')
        tmpStr = tmpStr + "保单合同号："
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "保单年度末".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ')
        tmpStr = tmpStr + "保单年度末".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ')
        tmpStr = tmpStr + "保单年度末".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ')
        for i in range(0,int(TradeContext.cashnum)):
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')
            if i != 0 and (i+1)%3 == 0:
                tmpStr = tmpStr + "\n"
                tmpStr = tmpStr + "".ljust(8,' ')
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '中国人寿--生成现金价值表成功' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "中国人寿--生成现金价值表失败"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

################################################################################
# 银保通文件生成                                  
# 功    能：生成华夏现金价值文件                           
# 参数说明：                                                                  
# 事    例：                                                                   
#                                                                              
################################################################################            
def createHXFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '华夏---开始生成现金价值表【' + fileName + '】' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #根据实际需要先空出4行
        for i in range(4): 
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " 保单现金价值".ljust( 105,  " " ) + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.year1.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year2.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year3.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year4.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year5.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year6.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year7.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.cash1.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash2.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash3.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash4.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash5.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash6.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash7.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.year8.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year9.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year10.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year11.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year12.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year13.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.year14.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        tmpStr = tmpStr + " " + TradeContext.cash8.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash9.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash10.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash11.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash12.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash13.ljust(14," ")
        tmpStr = tmpStr + " " + TradeContext.cash14.ljust(14," ") + " \n"
        tmpStr = tmpStr + " ".ljust( 105,"-" ) +  " \n"
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '华夏--生成现金价值表成功' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F00333"
        TradeContext.errorMsg  = "华夏--生成现金价值表失败"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

################################################################################
# 银保通文件生成                                  
# 功    能：生成幸福人寿现金价值文件                           
# 参数说明：                                                                  
# 事    例：                                                                   
#                                                                              
################################################################################            
def createHappyFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '幸福人寿---开始生成现金价值表【' + fileName + '】' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #根据实际需要，先空出8行
        for i in range(0,8):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(37,' ') + "现    金    价    值    表\n\n"
        tmpStr = tmpStr + "".ljust(32,' ') + "（以保单载明的每1000元保险费为标准）\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "险种名称："
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')
        tmpStr = tmpStr + "保单合同号："
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "保单年度末".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ')
        tmpStr = tmpStr + "保单年度末".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ')
        tmpStr = tmpStr + "保单年度末".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ')
        for i in range(0,int(TradeContext.CashCount)):
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')
            if i != 0 and (i+1)%3 == 0:
                tmpStr = tmpStr + "\n"
                tmpStr = tmpStr + "".ljust(8,' ')
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '幸福人寿--生成现金价值表成功' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "幸福人寿--生成现金价值表失败"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

################################################################################            
# 银保通文件生成                                                                            
# 功    能：生成泰康人寿现金价值文件                                                        
# 参数说明：                                                                                
# 事    例：                                                                                
#                                                                                           
################################################################################            
def createTaikangFile( fileName ):                                                            
                                                                                            
    AfaLoggerFunc.tradeInfo( '泰康人寿---开始生成现金价值表【' + fileName + '】' )          
                                                                                            
    try:                                                                                    
        cashFile = file( fileName,"w" )                                                     
                                                                                            
        tmpStr = ""                                                                         
        #根据实际需要，先空出8行                                                            
        for i in range(0,8):                                                                
            tmpStr = tmpStr + "\n"                                                          
        tmpStr = tmpStr + "".ljust(37,' ') + "现  金  价  值  金  额  表\n\n"               
        tmpStr = tmpStr + "".ljust(32,' ') + "(以1000元年交保险费为单位【注】)\n\n"     
        tmpStr = tmpStr + "".ljust(8,' ') + "险种名称："                                    
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')                            
        tmpStr = tmpStr + "保单合同号："                                                    
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"                        
        tmpStr = tmpStr + "".ljust(8,' ') + "保单年度".ljust(16,' ')                      
        tmpStr = tmpStr + "年末现金价值".ljust(16,' ')                                          
        tmpStr = tmpStr + "保单年度".ljust(16,' ')                                        
        tmpStr = tmpStr + "年末现金价值".ljust(16,' ')                                          
        tmpStr = tmpStr + "保单年度".ljust(16,' ')                                        
        tmpStr = tmpStr + "年末现金价值 单位：元".ljust(16,' ') + "\n\n"                                 
        tmpStr = tmpStr + "".ljust(8,' ')                                                   
        for i in range(0,int(TradeContext.CashCount)):                                      
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')                            
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')                            
            if i != 0 and (i+1)%3 == 0:                                                     
                tmpStr = tmpStr + "\n"                                                      
                tmpStr = tmpStr + "".ljust(8,' ')                                           
                                                                                            
        cashFile.write( tmpStr )                                                            
                                                                                            
        cashFile.close( )                                                                   
                                                                                            
        AfaLoggerFunc.tradeInfo( '泰康人寿--生成现金价值表成功' )                           
                                                                                            
        return True                                                                         
                                                                                            
    except Exception ,e:                                                                    
        cashFile.close( )                                                                   
        AfaLoggerFunc.tradeInfo( str(e) )                                                   
        TradeContext.errorCode = "F001"                                                     
        TradeContext.errorMsg  = "泰康人寿--生成现金价值表失败"                             
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )                                    
        return False                     
        
################################################################################            
# 银保通文件生成                                                                            
# 功    能：生成人保寿险现金价值文件                                                        
# 参数说明：                                                                                
# 事    例：                                                                                
#                                                                                           
################################################################################            
def createRbsxFile( fileName ):                                                            
                                                                                            
    AfaLoggerFunc.tradeInfo( '人保寿险---开始生成现金价值表【' + fileName + '】' )          
                                                                                            
    try:                                                                                    
        cashFile = file( fileName,"w" )                                                     
                                                                                            
        tmpStr = ""                                                                         
        #根据实际需要，先空出8行                                                            
        for i in range(0,8):                                                                
            tmpStr = tmpStr + "\n"                                                          
        tmpStr = tmpStr + "".ljust(37,' ') + "现    金    价    值    表\n\n"               
        tmpStr = tmpStr + "".ljust(32,' ') + "（以保单载明的每1000元保险费为标准）\n\n"     
        tmpStr = tmpStr + "".ljust(8,' ') + "险种名称："                                    
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')                            
        tmpStr = tmpStr + "保单合同号："                                                    
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"                        
        tmpStr = tmpStr + "".ljust(8,' ') + "保单年度末".ljust(16,' ')                      
        tmpStr = tmpStr + "现金价值".ljust(16,' ')                                          
        tmpStr = tmpStr + "保单年度末".ljust(16,' ')                                        
        tmpStr = tmpStr + "现金价值".ljust(16,' ')                                          
        tmpStr = tmpStr + "保单年度末".ljust(16,' ')                                        
        tmpStr = tmpStr + "现金价值".ljust(16,' ') + "\n\n"                                 
        tmpStr = tmpStr + "".ljust(8,' ')                                                   
        for i in range(0,int(TradeContext.CashCount)):                                      
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')                            
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')                            
            if i != 0 and (i+1)%3 == 0:                                                     
                tmpStr = tmpStr + "\n"                                                      
                tmpStr = tmpStr + "".ljust(8,' ')                                           
                                                                                            
        cashFile.write( tmpStr )                                                            
                                                                                            
        cashFile.close( )                                                                   
                                                                                            
        AfaLoggerFunc.tradeInfo( '人保寿险--生成现金价值表成功' )                           
                                                                                            
        return True                                                                         
                                                                                            
    except Exception ,e:                                                                    
        cashFile.close( )                                                                   
        AfaLoggerFunc.tradeInfo( str(e) )                                                   
        TradeContext.errorCode = "F001"                                                     
        TradeContext.errorMsg  = "人保寿险--生成现金价值表失败"                             
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )                                    
        return False                                                                        
                                                       
################################################################################
# 银保通文件生成                                  
# 功    能：生成生命人寿现金价值文件                           
# 参数说明：                                                                  
# 事    例：                                                                   
#                                                                              
################################################################################            
def createLifeFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '生命人寿---开始生成现金价值表【' + fileName + '】' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #根据实际需要，先空出8行
        for i in range(0,8):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(37,' ') + "现    金    价    值    表\n\n"
        tmpStr = tmpStr + "".ljust(32,' ') + "（以保单载明的每1000元保险费为标准）\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "险种名称："
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')
        tmpStr = tmpStr + "保单合同号："
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "年度/年龄".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ')
        tmpStr = tmpStr + "年度/年龄".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ')
        tmpStr = tmpStr + "年度/年龄".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ')
        for i in range(0,int(TradeContext.CashCount)):
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')
            if i != 0 and (i+1)%3 == 0:
                tmpStr = tmpStr + "\n"
                tmpStr = tmpStr + "".ljust(8,' ')
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '生命人寿--生成现金价值表成功' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "生命人寿--生成现金价值表失败"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False                                                                                    

################################################################################
# 银保通文件生成                                  
# 功    能：生成人保健康现金价值文件                           
# 参数说明：                                                                  
# 事    例：                                                                   
#                                                                              
################################################################################            
def createRbjkFile( fileName ):
    
    AfaLoggerFunc.tradeInfo( '人保健康---开始生成现金价值表【' + fileName + '】' )
    
    try:
        cashFile = file( fileName,"w" )
        
        tmpStr = ""
        #根据实际需要，先空出8行
        for i in range(0,8):
            tmpStr = tmpStr + "\n"
        tmpStr = tmpStr + "".ljust(37,' ') + "现    金    价    值    表\n\n"
        tmpStr = tmpStr + "".ljust(32,' ') + "（以保单载明的每1000元保险费为标准）\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "险种名称："
        tmpStr = tmpStr + TradeContext.productname.ljust(40,' ')
        tmpStr = tmpStr + "保单合同号："
        tmpStr = tmpStr + TradeContext.policy.ljust(40,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ') + "年度/年龄".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ')
        tmpStr = tmpStr + "年度/年龄".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ')
        tmpStr = tmpStr + "年度/年龄".ljust(16,' ')
        tmpStr = tmpStr + "现金价值".ljust(16,' ') + "\n\n"
        tmpStr = tmpStr + "".ljust(8,' ')
        for i in range(0,int(TradeContext.CashCount)):
            tmpStr = tmpStr + TradeContext.year[i].ljust(16,' ')
            tmpStr = tmpStr + TradeContext.cash[i].ljust(16,' ')
            if i != 0 and (i+1)%3 == 0:
                tmpStr = tmpStr + "\n"
                tmpStr = tmpStr + "".ljust(8,' ')
        
        cashFile.write( tmpStr )
        
        cashFile.close( )
        
        AfaLoggerFunc.tradeInfo( '人保健康--生成现金价值表成功' )
        
        return True
        
    except Exception ,e:
        cashFile.close( )
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode = "F001"
        TradeContext.errorMsg  = "人保健康--生成现金价值表失败"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False                                                                                    
