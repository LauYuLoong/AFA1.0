# -*- coding: gbk -*-
###############################################################################
# 文件名称：AbdtManager.py
# 文件标识：
# 摘    要：批量公共库
#
# 当前版本：2.0
# 作    者：XZH
# 完成日期：2008年06月10日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import TradeContext,UtilTools,AfaFunc,AfaDBFunc,ConfigParser,sys,os,time,LoggerHandler,HostComm,HostContext
from types import *

abdtLogger = LoggerHandler.getLogger( 'abdt' )

#=========================日志==================================================
def WrtLog(logstr):

    if ( TradeContext.existVariable('BATCH_TRACE') ):

        if ( TradeContext.BATCH_TRACE   == 'off' ):
            #不输出日志
            return True

        elif ( TradeContext.BATCH_TRACE == 'file' ):
            #向文件输出
            abdtLogger.info(logstr)

        elif ( TradeContext.BATCH_TRACE == 'all' ):
            #向文件和屏幕同时输出
            abdtLogger.info(logstr)
            print logstr

        elif ( TradeContext.BATCH_TRACE == 'stdout' ):
            #向屏幕输出
            print logstr

    else:
        #默认向文件和屏幕同时输出
        abdtLogger.info(logstr)
        print logstr

    return True


#=========================交易异常时退出本处理流程==============================
def ExitThisFlow( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode= errorCode
        TradeContext.errorMsg = errorMsg

        WrtLog( '>>>[' + errorCode + ']' + errorMsg )

    if( TradeContext.errorCode.isdigit( )==True and long( TradeContext.errorCode )==0 ):
        return True

    else:
        return False




#=========================读取批量配置文件中信息=================================
def GetBatchConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.BATCH_HOSTIP   = config.get('BATCH', 'HOSTIP')
        TradeContext.BATCH_USERNO   = config.get('BATCH', 'USERNO')
        TradeContext.BATCH_PASSWD   = config.get('BATCH', 'PASSWD')
        TradeContext.BATCH_LDIR     = config.get('BATCH', 'LDIR')
        TradeContext.BATCH_RDIR     = config.get('BATCH', 'RDIR')
        TradeContext.BATCH_CLEARDAY = config.get('BATCH', 'CLEARDAY')
        TradeContext.BATCH_CYCTIME  = config.get('BATCH', 'CYCTIME')
        TradeContext.BATCH_TRACE    = config.get('BATCH', 'TRACE')
        TradeContext.BATCH_MAXNUM   = config.get('BATCH', 'MAXNUM')

        WrtLog(':::BATCH_HOSTIP   = ' + TradeContext.BATCH_HOSTIP)
        WrtLog(':::BATCH_USERNO   = ' + TradeContext.BATCH_USERNO)
        WrtLog(':::BATCH_PASSWD   = ' + TradeContext.BATCH_PASSWD)
        WrtLog(':::BATCH_LDIR     = ' + TradeContext.BATCH_LDIR)
        WrtLog(':::BATCH_RDIR     = ' + TradeContext.BATCH_RDIR)
        WrtLog(':::BATCH_CLEARDAY = ' + TradeContext.BATCH_CLEARDAY)
        WrtLog(':::BATCH_CYCTIME  = ' + TradeContext.BATCH_CYCTIME)
        WrtLog(':::BATCH_TRACE    = ' + TradeContext.BATCH_TRACE)
        WrtLog(':::BATCH_MAXNUM   = ' + TradeContext.BATCH_MAXNUM)

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9000', '读取批量配置文件异常')



#=========================查询单位信息==========================================
def QueryBusiInfo():

    try:
        sql = "SELECT APPNAME,BUSINAME,ACCNO,AGENTTYPE,VOUHNO FROM ABDT_UNITINFO WHERE "
        sql = sql +       "APPNO="    + "'" + TradeContext.APPNO  + "'"        #业务编号
        sql = sql + " AND BUSINO="    + "'" + TradeContext.BUSINO + "'"        #单位编号
        sql = sql + " AND STATUS="    + "'" + "1"                 + "'"        #状态(0:注销,1:正常)

        WrtLog(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '查询单位信息异常')

        if ( len(records) == 0 ):
            return ExitThisFlow( '9000', '没有查询单位信息')


        TradeContext.APPNAME   = str(records[0][0]).strip()        #业务名称
        TradeContext.BUSINAME  = str(records[0][1]).strip()        #单位名称
        TradeContext.ACCNO     = str(records[0][2]).strip()        #银行账户(单位帐户)
        TradeContext.AGENTTYPE = str(records[0][3]).strip()        #委托方式
        TradeContext.VOUHNO    = str(records[0][4]).strip()        #凭证号(内部帐户)

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '查询单位信息异常')



#=========================修改批次提交日期或操作日期============================
def UpdateBatchDate(pBatchNo, pDate, pTime):

    WrtLog('>>>修改批次提交时间=' + TradeContext.WorkDate + ' ' + TradeContext.WorkTime)

    try:

        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET "
        sql = sql + "BATCHDATE=" +  "'" + TradeContext.WorkDate    + "',"        #日期
        sql = sql + "BATCHTIME=" +  "'" + TradeContext.WorkTime    + "'"         #时间

        sql = sql + " WHERE "

        sql = sql + "BATCHNO=" + "'" + pBatchNo    + "'"                         #委托号

        WrtLog(sql)

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if (result <= 0):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '修改批次提交日期或操作日期失败')

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '修改批次提交日期或操作日期异常')


#=========================把批量文件移到目录DUST中==============================
def MoveFileToDust():

    WrtLog('>>>把批量文件移到目录DUST中')

    try:
        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        sFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/dust/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + TradeContext.WorkTime + '_' + 'X'
        #end

        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            cmdstr = "mv " + sFileName + " " + dFileName
            WrtLog('>>>转移命令:' + cmdstr)
            os.system(cmdstr)
            return True
            
        else:
            return ExitThisFlow( '9000', '批量处理数据文件不存在,请查询原因')

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '批量文件移到目录DUST异常')



#=========================修改批次的状态========================================
def UpdateBatchInfo(pBatchNo, pStatus, pMessage,pInfo=0):

    WrtLog('>>>修改批次状态:[' + pStatus + ']' + pMessage)

    try:
        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET "
        sql = sql + "STATUS="   +  "'" + pStatus     + "',"     #状态
        sql = sql + "PROCMSG="  +  "'" + pMessage    + "',"     #原因
        
        #begin
        #关彬捷  20090330  增加详细处理信息文件名(NOTE4)
        if pInfo:
            sql = sql + "NOTE4=" + "'abdt_procmsg" + pBatchNo + ".txt'"  #详细处理信息文件名
        else:
            sql = sql + "NOTE4=''"                                       #详细处理信息文件名
        #end

        sql = sql + " WHERE "

        sql = sql + "BATCHNO=" + "'" + pBatchNo    + "'"        #委托号

        WrtLog(sql)

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if ( result <= 0 ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '修改批次的状态失败')

        #begin
        #关彬捷  20090330  如果存在参数pInfo(详细处理信息),则将详细信息写入到详细信息文件中
        if pInfo:
            path_procmsg = os.environ['AFAP_HOME'] + '/data/batch/procmsg/abdt_procmsg' + pBatchNo + '.txt'
            
            fp_procmsg = open(path_procmsg,"a")
            
            fp_procmsg.write(pInfo + "\n")
            
            fp_procmsg.close()
        #end

        #如果批次为已撤消状态,则把批量文件移到目录DUST中
        if ( pStatus == '40' ):
            MoveFileToDust()

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '修改批次的状态异常')




#==修改批次提交状态,开始提交处理置NOTE1为1,处理结束或者异常退出置NOTE1为0=======
def UpdateBatchInfoTJ(pBatchNo, pStatus):

    WrtLog('>>>修改提交状态:'+pBatchNo+'[' + pStatus + ']' )

    try:
        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET"
        sql = sql + " NOTE1=" +  "'" + pStatus    + "'"         #提交状态
        sql = sql + " WHERE "

        sql = sql + "BATCHNO=" + "'" + pBatchNo    + "'"        #委托号

        WrtLog(sql)

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if ( result <= 0 ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '修改批次提交状态失败')

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '修改批次提交状态异常')



#=========================校验客户信息表========================================
def ChkCustInfo(pAppNo, pBusiNo, pAccNo):

    WrtLog('>>>校验客户信息:'+ pAppNo+'|'+pBusiNo+'|'+pAccNo)

    try:
        sql = ""
        sql = "SELECT * FROM ABDT_CUSTINFO WHERE"
        sql = sql + " APPNO='"          + pAppNo  + "'"
        sql = sql + " AND BUSINO='"     + pBusiNo + "'"
        sql = sql + " AND ACCNO='"      + pAccNo  + "'"
        sql = sql + " AND STARTDATE<='" + TradeContext.WorkDate + "'"
        sql = sql + " AND ENDDATE>='"   + TradeContext.WorkDate + "'"

        WrtLog(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '校验客户信息失败')

        if ( len(records) == 0 ):
            return ExitThisFlow( '9000', '没有客户信息')
       
        #20110620  曾照泰修改 取出全额或部分扣款标识
        TradeContext.PartFlag = records[0][11]
        #end
        
        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '查询客户信息异常')



#=========================生成AS400批量格式文件=================================
def CrtBatchFile(curBatchNo):

    WrtLog('>>>生成AS400批量格式文件')

    summary_code = '258'
    
    #begin 20100107 蔡永贵增加 摘要名称
    summary_name = ' '
    #end

    ret = 0
    try:
        #校验有效期
        if ( TradeContext.WorkDate > TradeContext.ENDDATE ):
            UpdateBatchInfo(curBatchNo, "40", "自动撤消,批次过期")
            return ExitThisFlow( "9000", "自动撤消,批次过期" )


        #查询摘要代码
        sqlstr = "SELECT SUMNO,SUMNAME FROM AFA_SUMMARY WHERE SYSID='" + TradeContext.APPNO + "'"
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records == None or len(records) == 0 ):
            WrtLog('>>>没有发现摘要代码')
            summary_code = '258'
        else:
            summary_code = records[0][0].strip()
            
            #begin 20100107 蔡永贵增加 摘要名称
            summary_name = records[0][1].strip()
            #end


        #判断文件是否存在
        m_totalnum = 0
        m_totalamt = 0
        iCount     = 0

        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        bFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        sFileName = os.environ['AFAP_HOME'] + '/data/batch/swap/SWAP_' + TradeContext.BUSINO + TradeContext.NOTE2 + '.TXT'
        #end

        #begin
        #关彬捷  20090330  删除详细处理信息文件
        DelProcmsgFile(curBatchNo)
        
        #关彬捷  20090330  初始化明细处理标识符  procFlag(0-正常,1-异常)
        procFlag = 0
        #end

        if ( os.path.exists(bFileName) ):
            #打开文件
            bfp = open(bFileName, "r")

            #创建交换文件
            sfp= open(sFileName,  "w")

            #读取一行
            linebuf = bfp.readline()
            iline=0
            while ( len(linebuf) > 0 ):
                iline=iline+1
                
                #财政特殊处理(修改人：徐忠和，修改日期：20080402)
                if ( (len(linebuf) != 100) and (len(linebuf) != 101) and  (len(linebuf) != 118) and (len(linebuf) != 119)):
                    
                    #begin  关彬捷  20090330 
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据格式错:第" + str(iline) + "行")
                    #return ExitThisFlow( "9000", "自动撤消,批量数据格式错:第" + str(iline)+  "行")
                    
                    UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据格式错:第" + str(iline) + "行")
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end

                #汇总信息
                if ( linebuf[0] == "1" ):
                    s_rectype    = linebuf[0:1].lstrip().rstrip()          #记录类型
                    s_appno      = linebuf[1:7].lstrip().rstrip()          #业务编号
                    s_busino     = linebuf[7:21].lstrip().rstrip()         #单位编号
                    s_agenttype  = linebuf[21:22].lstrip().rstrip()        #委托方式
                    s_accno      = linebuf[22:45].lstrip().rstrip()        #对公帐号
                    s_remark     = linebuf[45:65].lstrip().rstrip()        #备用
                    s_status     = linebuf[65:66].lstrip().rstrip()        #状态
                    s_totalnum   = linebuf[66:76].lstrip().rstrip()        #总笔数
                    s_totalamt   = linebuf[76:93].lstrip().rstrip()        #总金额
                    s_retcode    = linebuf[93:100].lstrip().rstrip()       #返回码

                    #校验数据合法性
                    if ( not (s_agenttype.isdigit() and (len(s_accno)==0 or len(s_accno)==19 or len(s_accno)==23) and s_status.isdigit() and s_totalnum.isdigit()) ):
                        
                        #begin  关彬捷  20090330 
                        
                        #bfp.close()
                        #sfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(汇总):第" + str(iline) + "行")
                        #return ExitThisFlow( "9000", "自动撤消,批量数据非法(汇总):第" + str(iline) + "行")
                        
                        UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(汇总):第" + str(iline) + "行")
                        procFlag = 1
                        linebuf = bfp.readline()
                        continue
                        #end

                #明细信息
                elif ( linebuf[0] == '2' ):
                    m_rectype    = linebuf[0:1].lstrip().rstrip()               #记录类型
                    
                    #20120409 陈浩修改添加--AG07
                    #if ( TradeContext.APPNO[0:4] == 'AG08' ):
                    if ( TradeContext.APPNO[0:4] == 'AG08' or TradeContext.APPNO[0:4] == 'AG07'):
                        #财政特殊处理(修改人：徐忠和，修改日期：20080402),处理方式为：把6位资金代码从客户标识中拆离
                        m_custid     = linebuf[1:26].lstrip().rstrip()          #客户标识(开户编码(15位)+年度(4位)+项目编码(3位)+发放批次编码(3位)+资金代码(6位)
                        m_agenttype  = linebuf[39:40].lstrip().rstrip()         #委托方式
                        m_accno      = linebuf[40:63].lstrip().rstrip()         #个人帐号
                        m_remark     = linebuf[63:83].lstrip().rstrip()         #备用
                        m_status     = linebuf[83:84].lstrip().rstrip()         #状态
                        m_tradenum   = linebuf[84:94].lstrip().rstrip()         #笔数
                        m_tradeamt   = linebuf[94:111].lstrip().rstrip()        #金额
                        m_retcode    = linebuf[111:118].lstrip().rstrip()       #返回码
                    else:
                        m_custid     = linebuf[1:21].lstrip().rstrip()          #客户标识
                        m_agenttype  = linebuf[21:22].lstrip().rstrip()         #委托方式
                        m_accno      = linebuf[22:45].lstrip().rstrip()         #个人帐号
                        m_remark     = linebuf[45:65].lstrip().rstrip()         #备用
                        m_status     = linebuf[65:66].lstrip().rstrip()         #状态
                        m_tradenum   = linebuf[66:76].lstrip().rstrip()         #笔数
                        m_tradeamt   = linebuf[76:93].lstrip().rstrip()         #金额
                        m_retcode    = linebuf[93:100].lstrip().rstrip()        #返回码

                    #校验数据合法性
                    if ( not (m_agenttype.isdigit() and m_accno.isdigit() and m_status.isdigit() and m_tradenum.isdigit()) ):
                        
                        #begin  关彬捷  20090330 
                        
                        #bfp.close()
                        #sfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(明细行):第" + str(iline) + "行")
                        #return ExitThisFlow( "9000", "自动撤消,批量数据非法(明细行):第" + str(iline) + "行")
                        
                        UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(明细行):第" + str(iline) + "行")
                        procFlag = 1
                        linebuf = bfp.readline()
                        continue
                        #end

                    #筛选状态为正常的记录
                    if ( m_status == '1' ):

                        #统计金额和笔数
                        m_totalnum = m_totalnum + 1
                        m_totalamt = m_totalamt + (long)((float)(m_tradeamt)*100 + 0.1)

                        if ( s_agenttype == '3' ):

                            #校验客户信息是合法
                            if not ChkCustInfo(TradeContext.APPNO, TradeContext.BUSINO, m_accno):
                                
                                #begin  关彬捷  20090330 
                                
                                #bfp.close()
                                #sfp.close()
                                #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(客户未签约):第" + str(iline) + "行")
                                #return ExitThisFlow( "9000", "自动撤消,批量数据非法(客户未签约):第" + str(iline) + "行")
                                
                                UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(客户未签约):第" + str(iline) + "行")
                                procFlag = 1
                                linebuf = bfp.readline()
                                continue
                                #end

                        #记录文件
                        onelinebuf = ''
                        onelinebuf = onelinebuf + TradeContext.APPNO            + "|"        #代理业务号 
                        onelinebuf = onelinebuf + TradeContext.WorkDate         + "|"        #批量委托日期
                        onelinebuf = onelinebuf + TradeContext.BATCHNO[4:16]    + "|"        #批量委托号
                        onelinebuf = onelinebuf + TradeContext.WorkDate         + "|"        #前置日期
                        onelinebuf = onelinebuf + "000000000000"                + "|"        #前置流水号
                        onelinebuf = onelinebuf + TradeContext.WorkDate         + "|"        #外系统帐务日期
                        onelinebuf = onelinebuf + TradeContext.WorkDate         + "|"        #创建日期             
                        onelinebuf = onelinebuf + "000000000000"                + "|"        #创建流水号
                        onelinebuf = onelinebuf + " "                           + "|"        #蓝红字标志(0-蓝字,1-红字)
                        onelinebuf = onelinebuf + TradeContext.BRNO             + "|"        #交易机构
                        
                        #begin 20100107 蔡永贵修改 999990为从网银渠道提交的柜员号
                        if(TradeContext.USERNO == '999990'):
                            onelinebuf = onelinebuf + TradeContext.USERNO       + "|"         #交易柜员号
                        else:
                            onelinebuf = onelinebuf + '999986'                      + "|"     #交易柜员
                        #end
                        
                        
                        iCount = iCount+1
                        onelinebuf = onelinebuf + str(iCount)                   + "|"        #组号
                        onelinebuf = onelinebuf + "1 "                          + "|"        #组内序号

                        if ( s_agenttype == '3' ):
                            #批扣(对私)
                            onelinebuf = onelinebuf + m_accno                   + "|"        #借方账号
                            onelinebuf = onelinebuf + m_remark                  + "|"        #借方账户名称
                        else:
                            #批付(对公)
                            onelinebuf = onelinebuf + TradeContext.VOUHNO       + "|"        #借方账号
                            onelinebuf = onelinebuf + s_remark                  + "|"        #借方账户名称

                        onelinebuf = onelinebuf + " "                           + "|"        #销帐序号
                        onelinebuf = onelinebuf + "N"                           + "|"        #密码校验方式('N' 表示不校验 其它值都表示需要校验)
                        onelinebuf = onelinebuf + " "                           + "|"        #密码
                        onelinebuf = onelinebuf + " "                           + "|"        #支付密码
                       
                        #20110620 曾照泰修改 证件种类存放全额或部分扣款标识
                        if ( s_agenttype == '3' ):
                            onelinebuf = onelinebuf + TradeContext.PartFlag         + "|"        #证件种类
                        else:
                            onelinebuf = onelinebuf + " "                           + "|"         #证件种类  
                        #end
                        
                        onelinebuf = onelinebuf + " "                           + "|"        #证件号码
                        onelinebuf = onelinebuf + "0"                           + "|"        #证件校验标志(0-不校验,1-校验)
                        onelinebuf = onelinebuf + ""                            + "|"        #凭证种类
                        onelinebuf = onelinebuf + " "                           + "|"        #凭证号
                        onelinebuf = onelinebuf + "0"                           + "|"        #存折支票标志
                        onelinebuf = onelinebuf + "1"                           + "|"        #凭证处理标志

                        if ( s_agenttype == '3' ):
                            #批扣(对公)
                            onelinebuf = onelinebuf + TradeContext.VOUHNO       + "|"        #贷方账号
                            onelinebuf = onelinebuf + s_remark                  + "|"        #贷方账户名称
                        else:
                            #批付(对私)
                            onelinebuf = onelinebuf + m_accno                   + "|"        #贷方账号
                            onelinebuf = onelinebuf + m_remark                  + "|"        #贷方账户名称

                        onelinebuf = onelinebuf + "01"                          + "|"        #币种
                        onelinebuf = onelinebuf + "0"                           + "|"        #钞汇标志
                        onelinebuf = onelinebuf + "1"                           + "|"        #现转标志(0-现金,1-转帐)
                        onelinebuf = onelinebuf + " "                           + "|"        #往来帐标志(0-往帐,1-来帐)
                        onelinebuf = onelinebuf + m_tradeamt.rjust(15,'0')      + "|"        #发生额
                        onelinebuf = onelinebuf + summary_code                  + "|"        #摘要代码
                        
                        #begin 20100107 蔡永贵 修改摘要说明
                        #onelinebuf = onelinebuf + " "                           + "|"        #摘要说明
                        onelinebuf = onelinebuf + summary_name                  + "|"        #摘要说明
                        #end
                        
                        onelinebuf = onelinebuf + "0"                           + "|"        #户名效验标志
                        onelinebuf = onelinebuf + " "                           + "|"        #冻结编号
                        onelinebuf = onelinebuf + " "                           + "|"        #磁道2信息
                        onelinebuf = onelinebuf + " "                           + "|"        #磁道3信息
                        onelinebuf = onelinebuf + TradeContext.BUSINO           + "|"        #附加信息1(机构标识)
                        onelinebuf = onelinebuf + s_accno                       + "|"        #附加信息2
                        onelinebuf = onelinebuf + m_custid                      + "|"        #挂帐账号(客户标识)

                        sfp.write(onelinebuf + '\n')
                else:
                    
                    #begin  关彬捷  20090330 
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据格式错(行类型):第" + str(iline) + "行")
                    #return ExitThisFlow( "9000", "自动撤消,批量数据格式错(行类型):第" + str(iline) + "行")
                    
                    UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据格式错(行类型):第" + str(iline) + "行")
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end

                #从文件中读取一行
                linebuf = bfp.readline()

            #关闭文件
            bfp.close()
            sfp.close()
            
            #begin  关彬捷  20090330 
            if (procFlag == 1):
                return ExitThisFlow( "9000", "自动撤消,原因已写入详细处理文件")
            #end

            #判断总笔数,总金额
            ls_totalnum = (long)(s_totalnum)
            lm_totalnum = (long)(m_totalnum)

            ls_totalamt = (long)(((float)(s_totalamt)) * 100 + 0.1)
            lm_totalamt = m_totalamt

            WrtLog('>>>申请笔数=%d 申请金额=%d 明细笔数=%d 明细金额=%d' % (ls_totalnum, ls_totalamt, lm_totalnum, lm_totalamt))

            if ( (ls_totalnum!=lm_totalnum) or (ls_totalamt!=lm_totalamt) ):
                UpdateBatchInfo(curBatchNo, "40", "自动撤消:批量文件总笔数和总金额与申请的不符")
                return ExitThisFlow( "9000", "自动撤消,批量文件总笔数和总金额与申请的不符")

            #上传主机文件(本地)
            hFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_1'

            mv_cmdstr="mv " + sFileName + " " + hFileName
            os.system(mv_cmdstr)

            return True

        else:
            UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量处理数据文件不存在")
            return ExitThisFlow( "9000", "自动撤消,批量处理数据文件不存在")


    except Exception, e:
        bfp.close()
        sfp.close()
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '生成AS400批量格式文件异常')


#=========================FTP处理函数===========================================
def ftpfile(ftptype, sfilename, rfilename):

    try:
        #创建文件
        
        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        ftpShell = os.environ['AFAP_HOME'] + '/data/batch/shell/ftphost_' + TradeContext.BUSINO + TradeContext.NOTE2 + '.sh'
        #end
        
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.BATCH_HOSTIP + '\n')
        WrtLog('>>>>ip=' + TradeContext.BATCH_HOSTIP)
        ftpFp.write('user ' + TradeContext.BATCH_USERNO + ' ' + TradeContext.BATCH_PASSWD + '\n')

        if (ftptype==0):
            #上传文件
            ftpFp.write('cd '  + TradeContext.BATCH_RDIR + '\n')
            ftpFp.write('lcd ' + TradeContext.BATCH_LDIR + '\n')
            ftpFp.write('bin ' + '\n')
            ftpFp.write('put ' + sfilename + ' AGENT.' + rfilename + '\n')
        else:
            #下载文件
            ftpFp.write('cd '  + TradeContext.BATCH_RDIR + '\n')
            ftpFp.write('lcd ' + TradeContext.BATCH_LDIR + '\n')
            ftpFp.write('bin ' + '\n')
            ftpFp.write('get ' +  rfilename + ' ' + sfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        os.system(ftpcmd)

        return True

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>FTP处理异常')
        return False


#=========================发送记帐通知==========================================
def SendToHost(curBatchNo):

    WrtLog('>>>发送记帐通知(SendToHost)')

    try:
        HostFileName = 'A' + curBatchNo[8:16] + '1'

        #通讯区打包
        HostContext.I1TRCD = '8814'                        #主机交易码
        HostContext.I1SBNO = TradeContext.BRNO             #该交易的发起机构
        HostContext.I1USID = '999986'                      #交易柜员号
        HostContext.I1AUUS = ""                            #授权柜员
        HostContext.I1AUPS = ""                            #授权柜员密码
        HostContext.I1WSNO = "AFAP_BATCH"                  #终端号
        HostContext.I1CLDT = TradeContext.WorkDate         #批量委托日期
        HostContext.I1UNSQ = TradeContext.BATCHNO[4:16]    #批量委托号
        HostContext.I1NBBH = TradeContext.APPNO            #代理业务号
        
        #begin 20100107 蔡永贵增加 999990为从网银渠道提交的柜员号
        if(TradeContext.USERNO == '999990'):
            HostContext.I1USID = TradeContext.USERNO       #交易柜员号
        #end
        
        #begin 20091110 蔡永贵 修改事务标志
        #HostContext.I1OPFG = "2"                           #事务标志(1-单笔事务 2-整体事务)
        #如果是日间处理，则赋1，主机在处理日间时有3个状态(0-处理失败，1-正在处理，2-处理成功，当处于0和1状态时都返回失败)
        #主机处理日终时有2个状态(0-处理失败，1-处理成功)，为了避免当状态为1的时候把日终的也搞成失败，故此区分
        if (TradeContext.NOTE3 == "0"):
            HostContext.I1OPFG = "1"
        else:
            HostContext.I1OPFG = "2"
        #end
        
        ########################################################################################
        #20090922 蔡永贵 修改原因：增加处理标志
        ########################################################################################
        #HostContext.I1TRFG = "1"                           #处理标志(0-即时处理 1-日终处理)
        HostContext.I1TRFG = TradeContext.NOTE3            #处理标志(0-即时处理 1-日终处理)
        ########################################################################################
        HostContext.I1RPTF = "0"                           #重复标志(0-单次处理 1-多次处理)
        HostContext.I1STDT = TradeContext.STARTDATE        #批量起始日期
        HostContext.I1ENDT = TradeContext.ENDDATE          #批量截止日期
        HostContext.I1COUT = TradeContext.TOTALNUM         #委托总笔数
        HostContext.I1TOAM = TradeContext.TOTALAMT         #委托总金额
        HostContext.I1FINA = HostFileName                  #上送文件名称

        HostTradeCode = "8814".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8814.map', HostTradeCode, "0002" )
        if ( HostContext.host_Error ):
            WrtLog('>>>主机交易失败=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)

            if ( HostContext.host_ErrorType == 5 ):
                #超时
                return 0
            else:
                return -1

        else:
            #JSY0065：记录已存在
            if ( HostContext.O1MGID == "AAAAAAA" ):
                WrtLog('>>>通知记帐结果=[' + HostContext.O1MGID + ']交易成功')
#                WrtLog('返回结果:' + HostContext.O1ACUR)                          #重复次数
#                WrtLog('返回结果:' + HostContext.O1TRDT)                          #交易日期
#                WrtLog('返回结果:' + HostContext.O1TRTM)                          #交易时间
#                WrtLog('返回结果:' + HostContext.O1TLSQ)                          #柜员流水号
#                WrtLog('返回结果:' + HostContext.O1CLDT)                          #批量委托日期
#                WrtLog('返回结果:' + HostContext.O1UNSQ)                          #批量委托号
#                WrtLog('返回结果:' + HostContext.O1NBBH)                          #代理业务号
                return 0

            elif ( HostContext.O1MGID == "FILE001" ):
                #文件不存在
                WrtLog('>>>通知记帐结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

            elif ( HostContext.O1MGID == "JSY0065" ):
                #记录已存在
                WrtLog('>>>通知记帐结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return 0

            else:
                WrtLog('>>>通知记帐结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>发送记帐通知异常')
        return -1

#20091103  蔡永贵  增加方法CallHost，调用主机8877做日间批量记账
#=========================发送日间记账批量申请通知==========================================
def CallHost(curBatchNo):

    WrtLog('>>>发送日间记账批量申请通知(CallHost)')

    try:
        HostFileName = 'A' + curBatchNo[8:16] + '1'

        #通讯区打包
        HostContext.I1TRCD = '8877'                        #主机交易码
        HostContext.I1SBNO = TradeContext.BRNO             #该交易的发起机构
        HostContext.I1USID = '999986'                      #交易柜员号
        HostContext.I1AUUS = ""                            #授权柜员
        HostContext.I1AUPS = ""                            #授权柜员密码
        HostContext.I1WSNO = "AFAP_BATCH"                  #终端号
        HostContext.I1CLDT = TradeContext.WorkDate         #批量委托日期
        HostContext.I1UNSQ = TradeContext.BATCHNO[4:16]    #批量委托号
        HostContext.I1FINA = HostFileName                  #上送文件名称

        HostTradeCode = "8877".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8877.map', HostTradeCode, "0002" )
        if ( HostContext.host_Error ):
            WrtLog('>>>主机交易失败=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)

            if ( HostContext.host_ErrorType == 5 ):
                #超时
                return 0
            else:
                return -1

        else:
            #JSY0065：记录已存在
            if ( HostContext.O1MGID == "AAAAAAA" ):
                WrtLog('>>>通知记帐结果=[' + HostContext.O1MGID + ']交易成功')
#                WrtLog('返回结果:' + HostContext.O1ACUR)                          #重复次数
#                WrtLog('返回结果:' + HostContext.O1TRDT)                          #交易日期
#                WrtLog('返回结果:' + HostContext.O1TRTM)                          #交易时间
#                WrtLog('返回结果:' + HostContext.O1TLSQ)                          #柜员流水号
#                WrtLog('返回结果:' + HostContext.O1CLDT)                          #批量委托日期
#                WrtLog('返回结果:' + HostContext.O1UNSQ)                          #批量委托号
#                WrtLog('返回结果:' + HostContext.O1NBBH)                          #代理业务号
                return 0

            elif ( HostContext.O1MGID == "FILE001" ):
                #文件不存在
                WrtLog('>>>通知记帐结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

            elif ( HostContext.O1MGID == "JSY0065" ):
                #记录已存在
                WrtLog('>>>通知记帐结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return 0

            else:
                WrtLog('>>>通知记帐结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>发送记帐通知异常')
        return -1


#=========================下载批量处理结果文件==================================
def RecvResultFile(curBatchNo):

    WrtLog('>>>下载批量处理结果文件(RecvResultFile)')

    try:
    
        HostFileName = 'A' + curBatchNo[8:16] + '2'
        HostBatchNo  = curBatchNo[4:16]

        #通讯区打包
        HostContext.I1TRCD = '8815'                        #主机交易码
        HostContext.I1SBNO = TradeContext.BRNO             #该交易的发起机构
        HostContext.I1USID = '999986'                      #交易柜员号
        HostContext.I1AUUS = ""                            #授权柜员
        HostContext.I1AUPS = ""                            #授权柜员密码
        HostContext.I1WSNO = ""                            #终端号
        HostContext.I1NBBH = TradeContext.APPNO            #代理业务号
        HostContext.I1CLDT = TradeContext.BATCHDATE        #批量委托日期
        HostContext.I1UNSQ = HostBatchNo                   #批量委托号
        HostContext.I1FINA = HostFileName                  #下传文件名
        HostContext.I1DWFG = "2"                           #下传标志(0-返回成功明细,1-返回失败明细,2-全部返回)

        HostTradeCode = "8815".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8815.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            WrtLog('>>>主机交易失败=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)

            #超时
            if ( HostContext.host_ErrorType == 5 ):
                return 1
            else:
                return -1

        else:
            #XCR0001:记录不存在 AGR0005:数据未处理
            if ( HostContext.O1MGID == "AAAAAAA" ):
                WrtLog('>>>生成处理结果=[' + HostContext.O1MGID + ']交易成功')
                WrtLog('返回结果:主机流水号  = ' + HostContext.O1TLSQ)        #主机流水号
                WrtLog('返回结果:代理业务号  = ' + HostContext.O1NBBH)        #代理业务号
                WrtLog('返回结果:批量委托号  = ' + HostContext.O1CLDT)        #批量委托日期
                WrtLog('返回结果:批量委托号  = ' + HostContext.O1UNSQ)        #批量委托号
                WrtLog('返回结果:主机流水号  = ' + HostContext.O1AMTL)        #交易主机流水号
                WrtLog('返回结果:交易日期    = ' + HostContext.O1DATE)        #交易日期
                WrtLog('返回结果:交易时间    = ' + HostContext.O1TIME)        #交易时间
                WrtLog('返回结果:主机信息标识= ' + HostContext.O1MSSG)        #主机信息标识
                WrtLog('返回结果:事务标志    = ' + HostContext.O1OPFG)        #事务标志(1-单笔事务 2-整体事务)
                WrtLog('返回结果:处理标志    = ' + HostContext.O1TRFG)        #处理标志(0-即时处理 1-日终处理)
                WrtLog('返回结果:重复标志    = ' + HostContext.O1RPTF)        #重复标志(0-单次处理 1-多次处理)
                WrtLog('返回结果:批量起始日期= ' + HostContext.O1STDT)        #批量起始日期
                WrtLog('返回结果:批量截止日期= ' + HostContext.O1ENDT)        #批量截止日期
                WrtLog('返回结果:委托总笔数  = ' + HostContext.O1COUT)        #委托总笔数
                WrtLog('返回结果:委托总金额  = ' + HostContext.O1TOAM)        #委托总金额
                WrtLog('返回结果:成功总笔数  = ' + HostContext.O1SUCN)        #成功总笔数
                WrtLog('返回结果:成功总金额  = ' + HostContext.O1AMAO)        #成功总金额
                WrtLog('返回结果:失败总笔数  = ' + HostContext.O1FACN)        #失败总笔数
                WrtLog('返回结果:失败总金额  = ' + HostContext.O1AMOT)        #失败总金额
                WrtLog('返回结果:下传文件名称= ' + HostContext.O1FINA)        #下传文件名称

                #转换
                HostTotalNum = (long)(HostContext.O1COUT)
                HostTotalAmT = (float)(HostContext.O1TOAM)
                HostSuccNum  = (long)(HostContext.O1SUCN)
                HostSuccAmT  = (float)(HostContext.O1AMAO)
                HostFailNum  = (long)(HostContext.O1FACN)
                HostFailAmT  = (float)(HostContext.O1AMOT)

                HostContext.O1COUT = str(HostTotalNum)
                HostContext.O1TOAM = str(HostTotalAmT)
                HostContext.O1SUCN = str(HostSuccNum)
                HostContext.O1AMAO = str(HostSuccAmT)
                HostContext.O1FACN = str(HostFailNum)
                HostContext.O1AMOT = str(HostFailAmT)

                UpdateBatchDate(curBatchNo,HostContext.O1DATE, HostContext.O1TIME)
                WrtLog('>>>修改交易时间['+ HostContext.O1DATE + ':' + HostContext.O1TIME +']')
                return 0

            elif ( HostContext.O1MGID == "ACR8803" ):
                WrtLog('>>>下载批量处理结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return 1

            else:
                WrtLog('>>>下载批量处理结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>下载批量处理结果异常')
        return -1


#=========================查询主机结果文件是否生成==============================
def ChkHostFile(curBatchNo):

    WrtLog('>>>查询主机结果文件是否生成(ChkHostFile)')

    try:
    
        HostFileName = 'A' + curBatchNo[8:16] + '2'
        HostBatchNo  = curBatchNo[4:16]

        #通讯区打包
        HostContext.I1TRCD = '8819'                        #交易码
        HostContext.I1SBNO = TradeContext.BRNO             #交易机构号
        HostContext.I1USID = '999986'                      #交易柜员号
        HostContext.I1AUUS = ""                            #授权柜员
        HostContext.I1AUPS = ""                            #授权柜员密码
        HostContext.I1WSNO = ""                            #终端号
        HostContext.I1NBBH = TradeContext.APPNO            #代理业务标识
        HostContext.I1CLDT = TradeContext.BATCHDATE        #原批量日期
        HostContext.I1UNSQ = HostBatchNo                   #原批量委托号
        HostContext.I1FILE = HostFileName                  #删除文件名
        HostContext.I1OPFG = '0'                           #操作标志(0-查询 1-删除上传文件 2-删除下传文件)

        HostTradeCode = "8819".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8819.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            WrtLog('>>>主机交易失败=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return -1

        else:
            #XCR0001:记录不存在 AGR0005:数据未处理
            if ( HostContext.O1MGID == "AAAAAAA" ):
                WrtLog('>>>查询处理结果=[' + HostContext.O1MGID + ']交易成功')
                WrtLog('返回结果:重复次数     = ' + HostContext.O1ACUR)        #重复次数
                WrtLog('返回结果:交易日期     = ' + HostContext.O1TRDT)        #交易日期
                WrtLog('返回结果:交易时间     = ' + HostContext.O1TRTM)        #交易时间
                WrtLog('返回结果:柜员流水     = ' + HostContext.O1TLSQ)        #柜员流水
                WrtLog('返回结果:代理业务标识 = ' + HostContext.O1NBBH)        #代理业务标识
                WrtLog('返回结果:批量委托日期 = ' + HostContext.O1CLDT)        #批量委托日期
                WrtLog('返回结果:批量委托号   = ' + HostContext.O1UNSQ)        #批量委托号
                WrtLog('返回结果:下传文件名   = ' + HostContext.O1FILE)        #下传文件名
                WrtLog('返回结果:文件状态     = ' + HostContext.O1STCD)        #文件状态(0-未生成 1-已生成 2-已删除)
                WrtLog('返回结果:委托总笔数   = ' + HostContext.O1COUT)        #委托总笔数
                WrtLog('返回结果:委托总金额   = ' + HostContext.O1TOAM)        #委托总金额
                WrtLog('返回结果:成功总笔数   = ' + HostContext.O1SUCN)        #成功总笔数
                WrtLog('返回结果:成功总金额   = ' + HostContext.O1AMAO)        #成功总金额
                WrtLog('返回结果:失败总笔数   = ' + HostContext.O1FACN)        #失败总笔数
                WrtLog('返回结果:失败总金额   = ' + HostContext.O1AMOT)        #失败总金额

                WrtLog('O1STCD='+HostContext.O1STCD)

                if (HostContext.O1STCD == '1'):
                    #转换
                    HostTotalNum = (long)(HostContext.O1COUT)
                    HostTotalAmT = (float)(HostContext.O1TOAM)
                    HostSuccNum  = (long)(HostContext.O1SUCN)
                    HostSuccAmT  = (float)(HostContext.O1AMAO)
                    HostFailNum  = (long)(HostContext.O1FACN)
                    HostFailAmT  = (float)(HostContext.O1AMOT)

                    HostContext.O1COUT = str(HostTotalNum)
                    HostContext.O1TOAM = str(HostTotalAmT)
                    HostContext.O1SUCN = str(HostSuccNum)
                    HostContext.O1AMAO = str(HostSuccAmT)
                    HostContext.O1FACN = str(HostFailNum)
                    HostContext.O1AMOT = str(HostFailAmT)

                    #UpdateBatchDate(curBatchNo,HostContext.O1TRDT, HostContext.O1TRTM)
                    #WrtLog('>>>修改交易时间['+ HostContext.O1TRDT + ':' + HostContext.O1TRTM +']')

                    return 0
                else:
                    return -1

            elif ( HostContext.O1MGID == "XCR0001" ):
                #记录不存在
                WrtLog('>>>查询处理结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return 1

            else:
                WrtLog('>>>查询处理结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>查询主机处理结果异常')
        return -1


#=========================格式化文件============================================
def FormatFile(ProcType, sFileName, dFileName):

    WrtLog('>>>格式化文件:' + ProcType + ' ' + sFileName + ' ' + dFileName)

    try:

        srcFileName    = os.environ['AFAP_HOME'] + '/data/batch/host/' + sFileName
        dstFileName    = os.environ['AFAP_HOME'] + '/data/batch/host/' + dFileName

        if (ProcType == "1"):
            #ascii->ebcd
            #调用格式:cvt2ebcdic -T 源文本文件 -P 目标物理文件 -F fld格式文件 [ -D 间隔符 ]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ebcdic'
            fldFileName = os.environ['AFAP_HOME'] + '/data/cvt/agent01.fld'
            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName 

        else:
            #ebcd->ascii
            #调用格式:cvt2ascii -T 生成文本文件 -P 物理文件 -F fld文件 [-D 间隔符] [-S] [-R]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
            fldFileName = os.environ['AFAP_HOME'] + '/data/cvt/agent02.fld'
            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName 
        #WrtLog('>>>转码：' + cmdstr)

        ret = os.system(cmdstr)                      
        if ( ret != 0 ):                             
            ret = False
        else:                                        
            ret = True

        return ret

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>格式化文件异常')
        return False


#=========================创建单位回盘文件======================================
def CrtBusiFile(curBatchNo):

    WrtLog('>>>创建单位回盘文件(CrtBusiFile)')

    try:
        rHostFile= os.environ['AFAP_HOME'] + '/data/batch/host/' +  curBatchNo + '_4'
        
        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        rBusiFile= os.environ['AFAP_HOME'] + '/data/batch/down/' +  TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + '.RET'
        #end

        #创建企业回盘文件
        bFp = open(rBusiFile, "w")

        #写入汇总语句
        wbuffer = '1'                                                  + '|'          #记录类型(1-汇总 2-明细)
        wbuffer = wbuffer + TradeContext.APPNO.ljust(6, ' ')           + '|'          #业务编号
        wbuffer = wbuffer + TradeContext.BUSINO.ljust(14, ' ')         + '|'          #单位编号
        wbuffer = wbuffer + TradeContext.AGENTTYPE                     + '|'          #委托方式(3-批扣， 4-批付)
        wbuffer = wbuffer + TradeContext.ACCNO.ljust(23, ' ')          + '|'          #对公帐号
                                                                  
        if ( len(TradeContext.BUSINAME)> 20 ):                                   
            wbuffer = wbuffer + TradeContext.BUSINAME[0:20]            + '|'          #备用(单位名称)
        else:                                                                    
            wbuffer = wbuffer + TradeContext.BUSINAME.ljust(20, ' ')   + '|'          #备用(单位名称)
                                                                                 
        wbuffer = wbuffer + '1'                                        + '|'          #状态
        wbuffer = wbuffer + TradeContext.TOTALNUM.rjust(10, ' ')       + '|'          #总笔数
        wbuffer = wbuffer + TradeContext.TOTALAMT.rjust(17, ' ')       + '|'          #总金额
        wbuffer = wbuffer + ' '.rjust(8,  ' ')                         + '|'          #返回码
        wbuffer = wbuffer + TradeContext.SUCCNUM.rjust(10, ' ')        + '|'          #成功笔数
        wbuffer = wbuffer + TradeContext.SUCCAMT.rjust(17, ' ')        + '|'          #成功金额
        wbuffer = wbuffer + TradeContext.FAILNUM.rjust(10, ' ')        + '|'          #失败笔数
        wbuffer = wbuffer + TradeContext.FAILAMT.rjust(17, ' ')        + '|'          #失败金额
        wbuffer = wbuffer + ' '.ljust(7,  ' ')                         + '|'          #备用
        wbuffer = wbuffer + '\n'                                                 
                                                                                 
        bFp.write(wbuffer)                                                       
        #打开主机下载文件                                                        
        hFp = open(rHostFile, "r")                                               
                                                                                 
        #读取一行                                                                
        linebuf = hFp.readline()                                                 
        while ( len(linebuf) > 0 ):

            if ( len(linebuf) < 994 ):
                hFp.close()
                bFp.close()
                return ExitThisFlow( '9000', '该批次下载文件格式错误,请检查')

            swapbuf = linebuf[0:994].split('<fld>')

            #写入明细信息
            
            #begin 20100413 蔡永贵   由于文件中没有分隔符，使用不便，修改为为每个字段后加上'|'分隔符
            wbuffer = '2'                                              + '|'       #记录类型(1-汇总,2-明细)
            wbuffer = wbuffer + swapbuf[25].strip().ljust(21, ' ')     + '|'       #客户标识

            if ( TradeContext.AGENTTYPE == '3' ):
                wbuffer = wbuffer + '4'                                + '|'       #委托方式(3-批扣,4-批付)
                wbuffer = wbuffer + swapbuf[14].strip().ljust(23, ' ') + '|'       #活期帐号
                wbuffer = wbuffer + swapbuf[15].strip().ljust(20, ' ') + '|'       #客户姓名
            else:
                wbuffer = wbuffer + '3'                                + '|'       #委托方式(3-批扣,4-批付)
                wbuffer = wbuffer + swapbuf[20].strip().ljust(23, ' ') + '|'       #活期帐号
                wbuffer = wbuffer + swapbuf[21].strip().ljust(20, ' ') + '|'       #客户姓名

            wbuffer = wbuffer + '1'                                    + '|'       #状态
            wbuffer = wbuffer + '1'.rjust(10, ' ')                     + '|'       #笔数
            wbuffer = wbuffer + swapbuf[28].strip().rjust(17, ' ')     + '|'       #金额
            
            tmp_retcode = swapbuf[5].strip()

            retstr = ''
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                if ( TradeContext.AGENTTYPE == '3' ):
                    retstr = "代扣成功"
                else:
                    retstr = "代发成功"
            else:
                if ( TradeContext.AGENTTYPE == '3' ):
                    retstr = "代扣失败"
                else:
                    retstr = "代发失败"
             
            #begin 20110616 曾照泰修改   新增全额或部分扣款的标识位 和应扣金额字段   其中全额或部分扣款标识位存放在会钞标识字段中
            #应扣金额存在在错误信息描述中
            #wbuffer = wbuffer +swapbuf[30].strip().ljust(1, ' ')         + '|'    #会钞标识在代扣时存放的为全额或部分扣款标识 
            cashflag = swapbuf[30].strip()                                         #取出会钞标识的值 代扣时为ABCD代发时为0
            if(cashflag.replace('.','')).isdigit():                                #如果是数字表示代发
                wbuffer =wbuffer +' '.strip().rjust(1,' ')                + '|'    #代发时为空
            else:
                wbuffer =wbuffer +cashflag.strip().rjust(1,' ')            + '|'   #代扣时存放ABCD标识
            
            amount  =  swapbuf[6].strip()
            if (amount.replace('.','')).isdigit():                                 #如果是数字 说明代扣成功该字段存放的是应扣金额
                wbuffer =wbuffer + amount.strip().rjust(17,' ')         + '|'      #代扣成功时存放应扣金额
                errormsg = ' '
            elif (len(amount)==0):                                                 #如果为空 说明是代发  
                wbuffer =wbuffer +' '.strip().rjust(17,' ')          + '|'         #代发成功时为应扣金额空值 
                errormsg = ' '
                
            else:                                                                  #如果不为空也不为数字 说明是代发代扣失败   
                wbuffer =wbuffer +' '.strip().rjust(17,' ')          + '|'         #代发代扣失败时应扣金额也为空
                errormsg = swapbuf[6].strip()               
            wbuffer = wbuffer + retstr.rjust(8, ' ')                  + '|'       #成功失败说明

            
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                tmp_retcode = "AAAAAAA"
            
            wbuffer = wbuffer + tmp_retcode.ljust(7,  ' ')             + '|'       #返回码
            
            wbuffer = wbuffer + errormsg.strip().ljust(62,' ')         + '|'       #返回信息
            wbuffer = wbuffer + '\n'
            #end 20110616 曾照泰 修改

            bFp.write(wbuffer)

            linebuf = hFp.readline()

        hFp.close()
        bFp.close()
        return True

    except Exception, e:
        hFp.close()
        bFp.close()
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '创建单位回盘文件异常')


#=========================创建银行报表文件======================================
def CrtBankFile(curBatchNo):

    WrtLog('>>>创建银行报表文件(CrtBankFile)')

    try:

        rHostFile= os.environ['AFAP_HOME'] + '/data/batch/host/' +  curBatchNo + '_4'
        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        rBankFile= os.environ['AFAP_HOME'] + '/data/batch/down/' +  TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + '.RPT'
        #end

        #创建业务报表文件
        bFp = open(rBankFile, "w")

        #写入标题
        bFp.write('\n\n\n                      ********** 批量处理业务报表(委托号:' + curBatchNo + ') **********\n\n\n')

        #写入汇总语句
        bFp.write('业务代码=' + TradeContext.APPNO.ljust(23,' ')    + ' 业务名称=' +    TradeContext.APPNAME   + '\n')
        bFp.write('单位编码=' + TradeContext.BUSINO.ljust(23,' ')   + ' 单位名称=' +    TradeContext.BUSINAME  + '\n')
        bFp.write('单位帐号=' + TradeContext.ACCNO.ljust(23,' ')    + ' 内部帐号=' +    TradeContext.VOUHNO    + '\n')
        bFp.write('交易日期=' + TradeContext.BATCHDATE + '\n')
        bFp.write('总 笔 数=' + TradeContext.TOTALNUM.ljust(23,' ') + ' 总 金 额=' +    TradeContext.TOTALAMT  + '\n')
        bFp.write('成功笔数=' + TradeContext.SUCCNUM.ljust(23,' ')  + ' 成功金额=' +    TradeContext.SUCCAMT   + '\n')
        bFp.write('失败笔数=' + TradeContext.FAILNUM.ljust(23,' ')  + ' 失败金额=' +    TradeContext.FAILAMT   + '\n')

        bFp.write('----------------------------------------------------------------------------------------------------------\n')
        bFp.write('序号   客户标识                  银行帐/卡号             客户姓名                          金额    结果(1:成功 0-失败) \n')
        bFp.write('----------------------------------------------------------------------------------------------------------\n')

        #打开主机下载文件
        hFp = open(rHostFile, "r")

        ireccount=0

        #读取一行
        linebuf = hFp.readline()
        while ( len(linebuf) > 0 ):

            if ( len(linebuf) < 994 ):
                hFp.close()
                bFp.close()
                return ExitThisFlow( '9999', '该批次下载文件格式错误,请检查')

            ireccount=ireccount+1

            swapbuf = linebuf[0:994].split('<fld>')

            #写入明细信息
            wbuffer = ''
            wbuffer = wbuffer + str(ireccount).ljust(7, ' ')                  #序号(20080402,XZH,从10修改为7)
            wbuffer = wbuffer + swapbuf[25].strip().ljust(26, ' ')            #客户标识(20080402,XZH,从21修改为25)

            if ( TradeContext.AGENTTYPE == '3' ):
                wbuffer = wbuffer + swapbuf[14].strip().ljust(24, ' ')        #活期帐号
                wbuffer = wbuffer + swapbuf[15].strip().ljust(21, ' ')        #客户姓名
            else:
                wbuffer = wbuffer + swapbuf[20].strip().ljust(24, ' ')        #活期帐号
                wbuffer = wbuffer + swapbuf[21].strip().ljust(21, ' ')        #客户姓名

            wbuffer = wbuffer + swapbuf[28].strip().rjust(17, ' ')            #金额

            tmp_retcode = swapbuf[5].strip()
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                wbuffer = wbuffer + '1'.rjust(5,  ' ')                        #返回码(1-成功)
            else:
                wbuffer = wbuffer + '0'.rjust(5,  ' ')                        #返回码(0-失败)

            wbuffer = wbuffer + '\n'
            bFp.write(wbuffer)

            linebuf = hFp.readline()

        hFp.close()
        bFp.close()

        return True

    except Exception, e:
        hFp.close()
        bFp.close()
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '创建单位回盘文件异常')





































######################################################################################################################
#功能描述：文件转换、校验(外围)
######################################################################################################################
def SQ_OTHER_Proc(curBatchNo):


    WrtLog('>>>申请处理(SQ_OTHER_Proc)')


    ret = 0
    try:
        #校验有效期
        iline=0
        if ( TradeContext.WorkDate > TradeContext.ENDDATE ):
            UpdateBatchInfo(curBatchNo, "40", "自动撤消,批次过期")
            return ExitThisFlow( "9000", "自动撤消,批次过期")

        #判断文件是否存在
        m_totalnum = 0
        m_totalamt = 0
        
        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        bFileName = os.environ['AFAP_HOME'] + '/data/batch/swap/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        sFileName = os.environ['AFAP_HOME'] + '/data/batch/swap/OTHER_SWAP_AFA.TXT'
        iFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        #end
        
        swapbuf   = ''

        #begin
        #关彬捷  20090330  删除详细处理信息文件
        DelProcmsgFile(curBatchNo)
        
        #关彬捷  20090330  初始化明细处理标识符  procFlag(0-正常,1-异常)
        procFlag = 0
        #end
        
        if ( os.path.exists(bFileName) ):

            #打开文件
            bfp = open(bFileName, "r")

             #创建文件
            sfp= open(sFileName,  "w")

            #生成批量汇总信息
            recinfo = "1"                                                     #记录类型(1-汇总 2-明细)
            recinfo = recinfo + TradeContext.APPNO.ljust(6, ' ')              #业务编号
            recinfo = recinfo + TradeContext.BUSINO.ljust(14, ' ')            #单位编号
            recinfo = recinfo + TradeContext.AGENTTYPE.ljust(1, ' ')          #委托方式(3-批扣 4-批付)
            recinfo = recinfo + TradeContext.ACCNO.ljust(23, ' ')             #对公帐号

            if ( len(TradeContext.BUSINAME) > 20 ):
                recinfo = recinfo + TradeContext.BUSINAME[0:20]               #备用(单位名称)
            else:
                recinfo = recinfo + TradeContext.BUSINAME.ljust(20, ' ')      #备用(单位名称)

            recinfo = recinfo + '1'                                           #状态(0-忽略 1-正常)
            recinfo = recinfo + TradeContext.TOTALNUM.rjust(10, ' ')          #总笔数
            recinfo = recinfo + TradeContext.TOTALAMT.rjust(17, ' ')          #总金额
            recinfo = recinfo + ' '.ljust(7, ' ')                             #返回码

            sfp.write(recinfo + '\n')

            #读取一行
            linebuf = bfp.readline()
            iline=0
            while ( len(linebuf) > 20 ):
                iline=iline+1
                swapbuf = UtilTools.rStripChar(linebuf, '\n')
                databuf = swapbuf.split('|')
                WrtLog("=============line" + str(iline) + "==============")

                if ( len(databuf) != 4 and len(databuf) != 5 ):
                    
                    #begin  关彬捷  20090330
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "自动撤消,数据格式错误(数据项个数错):第" + str(iline) + "行")
                    #return ExitThisFlow( "9000", "自动撤消,数据格式错误(数据项个数错):第" + str(iline) + "行" )
                    
                    UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","数据格式错误(数据项个数错):第" + str(iline) + "行")
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end

                m_custid   = databuf[0].lstrip().rstrip()
                m_accno    = databuf[1].lstrip().rstrip()
                m_custname = databuf[2].lstrip().rstrip()
                m_tradeamt = databuf[3].lstrip().rstrip()

                chkFlag = 0
                #校验数据是否合法
                if ( not (m_accno.isdigit() and (len(m_accno)==19 or len(m_accno)==23)) ):
                    
                    #begin  关彬捷  20090330
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(帐号非法):第" + str(iline) + "行")
                    #return ExitThisFlow("9000", "自动撤消,批量数据非法(帐号非法):第" + str(iline) + "行")
                    
                    UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(帐号非法):第" + str(iline) + "行" + ",账号为:" + m_accno )
                    procFlag = 1
                    chkFlag  = 1
                    #linebuf = bfp.readline()
                    #continue
                    ##end

                if  not (m_tradeamt.replace('.','')).isdigit() :
                    
                    #begin  关彬捷  20090330
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(金额非法):第" + str(iline) + "行")
                    #return ExitThisFlow("9000", "自动撤消,批量数据非法(金额非法):第" + str(iline) + "行")
                    
                    UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(金额非法):第" + str(iline) + "行" + ",账号为:" + m_accno)
                    procFlag = 1
                    chkFlag  = 1
                    #linebuf = bfp.readline()
                    #continue
                    ##end

                if chkFlag == 1:
                    linebuf = bfp.readline()
                    continue

                if ( TradeContext.AGENTTYPE == '3' ):           #批量代扣
                    #需要校验每笔批扣数据是否已经注册
                    if not  ChkCustInfo(TradeContext.APPNO, TradeContext.BUSINO, m_accno):
                        
                        #begin  关彬捷  20090330
                        
                        #bfp.close()
                        #sfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(客户未签约):第"+str(iline) + "行")
                        #return ExitThisFlow("9000", "自动撤消,批量数据非法(客户未签约):第" + str(iline) + "行")
                        
                        UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(客户未签约):第"+str(iline) + "行" + ",账号为:" + m_accno)
                        procFlag = 1
                        linebuf = bfp.readline()
                        continue
                        #end

                    m_agenttype = '4'

                elif ( TradeContext.AGENTTYPE == '4' ):         #批量代发
                     m_agenttype = '3'

                else:
                    #类型错误
                    
                    #begin  关彬捷  20090330
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "自动撤消,委托方式错误:第" + str(iline) + "行")
                    #return ExitThisFlow("9000", "自动撤消,委托方式错误:第" + str(iline) + "行")
                    
                    UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","委托方式错误:第" + str(iline) + "行" + ",账号为:" + m_accno)
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end


                #生成批量明细信息
                recinfo = "2"                                             #记录类型(1-汇总 2-明细)



                #20120409 陈浩修改添加--AG07
                #if ( TradeContext.APPNO[0:4] == 'AG08' ):
                if ( TradeContext.APPNO[0:4] == 'AG08' or TradeContext.APPNO[0:4] == 'AG07'):
                    #财政特殊处理(修改人：徐忠和，修改日期：20080402)
                    recinfo = recinfo + m_custid.ljust(38, ' ')           #客户标识(真实情况＝31位)
                else:
                    recinfo = recinfo + m_custid.ljust(20, ' ')           #客户标识


                recinfo = recinfo + m_agenttype                           #委托方式(3-批扣 4-批付)

                recinfo = recinfo + m_accno.ljust(23, ' ')                #活期帐号

                if ( len(m_custname)> 20 ):
                    recinfo = recinfo + m_custname[0:20]                  #客户姓名
                else:
                    recinfo = recinfo + m_custname.ljust(20, ' ')         #客户姓名

                recinfo = recinfo + '1'                                   #状态(0-忽略 1-正常)
                recinfo = recinfo + '1'.rjust(10, ' ')                    #总笔数
                recinfo = recinfo + m_tradeamt.rjust(17, ' ')             #总金额
                recinfo = recinfo + ' '.ljust(7, ' ')                     #返回码

                sfp.write(recinfo + '\n')

                m_totalnum = m_totalnum + 1
                m_totalamt = m_totalamt + (long)((float)(m_tradeamt)*100 + 0.1)

                #从文件中读取一行
                linebuf = bfp.readline()

            bfp.close()
            sfp.close()
            
            #begin  关彬捷  20090330 
            if (procFlag == 1):
                return ExitThisFlow( "9000", "自动撤消,原因已写入详细处理文件")
            #end

            #转换
            ls_totalnum = (long)(TradeContext.TOTALNUM)
            lm_totalnum = (long)(m_totalnum)
            ls_totalamt = (long)((float)(TradeContext.TOTALAMT)*100 + 0.1)
            lm_totalamt = m_totalamt

            WrtLog('>>>申请笔数=%d 申请金额=%d 明细笔数=%d 明细金额=%d' % (ls_totalnum, ls_totalamt, lm_totalnum, lm_totalamt))


            #判断总笔数,总金额
            if ( (ls_totalnum!=lm_totalnum) or (ls_totalamt!=lm_totalamt) ):
                UpdateBatchInfo(curBatchNo, "40", "自动撤消:批量文件总笔数和总金额与申请的不符")
                return ExitThisFlow("9000", "自动撤消,批量文件总笔数和总金额与申请的不符")


            #把生成内部格式批量处理文件移到内部目录中
            cmdstr = "mv " + sFileName + " " + iFileName
            os.system(cmdstr)

            #删除原始文件
            cmdstr = "rm " + bFileName
            os.system(cmdstr)

            UpdateBatchInfo(curBatchNo, "11", "数据转换-校验成功->待联社审批")
            
            #################################################################
            #20090927 蔡永贵增加  即时处理不需要经联社和中心审批
            #----------------------------------------------------------------
            if ( TradeContext.NOTE3 == '0' ):
                UpdateBatchInfo( curBatchNo, "21", "即时处理->待提交" )
                return ExitThisFlow( "0000", "即时处理->待提交" )
            #################################################################
            
            return ExitThisFlow("0000", "数据转换-校验成功->待联社审批")

        else:
            UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量处理数据文件不存在")
            return ExitThisFlow("9000", "自动撤消,批量处理数据文件不存在")

    except Exception, e:
        bfp.close()
        sfp.close()
        WrtLog( str(e) )
        UpdateBatchInfo(curBatchNo, "40", "申请处理(外围)异常(请检查数据文件)")
        return ExitThisFlow( '9999', '申请处理(外围)异常')





######################################################################################################################
#功能描述：申请处理(VMENU)
######################################################################################################################
def SQ_VMENU_Proc(curBatchNo):


    WrtLog('>>>申请处理(SQ_VMENU_Proc)')


    ret = 0
    try:
        #校验有效期
        if ( TradeContext.WorkDate > TradeContext.ENDDATE ):
            UpdateBatchInfo(curBatchNo, '40', '自动撤消,批次过期')
            return ExitThisFlow( '9000', '自动撤消,批次过期')


        #判断文件是否存在
        m_totalnum = 0
        m_totalamt = 0
        
        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        bFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        #end

        WrtLog(bFileName)
        
        #begin
        #关彬捷  20090330  删除详细处理信息文件
        DelProcmsgFile(curBatchNo)
        
        #关彬捷  20090330  初始化明细处理标识符  procFlag(0-正常,1-异常)
        procFlag = 0
        #end

        if ( os.path.exists(bFileName) ):

            #打开文件
            bfp = open(bFileName, "r")

            #读取一行
            linebuf = bfp.readline()
            iline=0
            while ( len(linebuf) > 0 ):
                iline=iline+1
                if ( (len(linebuf) != 100) and (len(linebuf) != 101) ):
                    
                    #begin  关彬捷  20090330
                    
                    #bfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据格式错:第" + str(iline) + "行")
                    #return ExitThisFlow( "9000", "自动撤消,批量数据格式错:第" + str(iline) + "行")
                    
                    UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据格式错:第" + str(iline) + "行")
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end

                #汇总信息
                if ( linebuf[0] == '1' ):
                    s_rectype    = linebuf[0:1].lstrip().rstrip()          #记录类型
                    s_appno      = linebuf[1:7].lstrip().rstrip()          #业务编号
                    s_busino     = linebuf[7:21].lstrip().rstrip()         #单位编号
                    s_agenttype  = linebuf[21:22].lstrip().rstrip()        #委托方式
                    s_accno      = linebuf[22:45].lstrip().rstrip()        #对公帐号
                    s_remark     = linebuf[45:65].lstrip().rstrip()        #备用
                    s_status     = linebuf[65:66].lstrip().rstrip()        #状态
                    s_totalnum   = linebuf[66:76].lstrip().rstrip()        #总笔数
                    s_totalamt   = linebuf[76:93].lstrip().rstrip()        #总金额
                    s_retcode    = linebuf[93:100].lstrip().rstrip()       #返回码

                    chkFlag = 0
                    #校验数据合法性
                    if ( not (s_agenttype.isdigit() and (len(s_accno)==0 or len(s_accno)==23) and s_status.isdigit() and s_totalnum.isdigit()) ):
                        
                        #begin  关彬捷  20090330
                        
                        #bfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(汇总):第" + str(iline) + "行")
                        #return ExitThisFlow("9000", "自动撤消,批量数据非法(汇总):第" + str(iline) + "行")
                        
                        UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(汇总):第" + str(iline) + "行"+",账号为:"+linebuf[22:45].lstrip().rstrip())
                        procFlag = 1
                        chkFlag = 1
                        #linebuf = bfp.readline()
                        #continue
                        ##end
                        
                    if not (s_totalamt.replace('.','')).isdigit():
                        
                        #begin  关彬捷  20090330
                        
                        #bfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(汇总):第" + str(iline) + "行")
                        #return ExitThisFlow("9000", "自动撤消,批量数据非法(汇总):第" + str(iline) + "行")
                        
                        UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(汇总):第" + str(iline) + "行"+",账号为:"+linebuf[22:45].lstrip().rstrip())
                        procFlag = 1
                        chkFlag = 1
                        #linebuf = bfp.readline()
                        #continue
                        ##end
                        
                    #begin  关彬捷  20090330
                    if chkFlag == 1:
                        linebuf = bfp.readline()
                        continue
                    #end

                #明细信息
                elif ( linebuf[0] == '2' ):
                    m_rectype    = linebuf[0:1].lstrip().rstrip()          #记录类型
                    m_custid     = linebuf[1:21].lstrip().rstrip()         #客户标识
                    m_agenttype  = linebuf[21:22].lstrip().rstrip()        #委托方式
                    m_accno      = linebuf[22:45].lstrip().rstrip()        #个人帐号
                    m_remark     = linebuf[45:65].lstrip().rstrip()        #备用
                    m_status     = linebuf[65:66].lstrip().rstrip()        #状态
                    m_tradenum   = linebuf[66:76].lstrip().rstrip()        #笔数
                    m_tradeamt   = linebuf[76:93].lstrip().rstrip()        #金额
                    m_retcode    = linebuf[93:100].lstrip().rstrip()       #返回码

                    chkFlag = 0
                    #校验数据合法性
                    if ( not (m_agenttype.isdigit() and m_accno.isdigit() and m_status.isdigit() and m_tradenum.isdigit()) ):
                        
                        #begin  关彬捷  20090330
                        
                        #bfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(明细):第"+str(iline) + "行")
                        #return ExitThisFlow("9000", "自动撤消,批量数据非法(明细):第" + str(iline) + "行")
                        
                        UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(明细):第"+str(iline) + "行"+",账号为:"+linebuf[22:45].lstrip().rstrip())
                        procFlag = 1
                        chkFlag = 1
                        #linebuf = bfp.readline()
                        #continue
                        ##end
                        
                    if not (m_tradeamt.replace('.','')).isdigit():
                        
                        #begin  关彬捷  20090330
                        
                        #bfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(明细):第"+str(iline) + "行")
                        #return ExitThisFlow("9000", "自动撤消,批量数据非法(明细):第" + str(iline) + "行")
                        
                        UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(明细):第"+str(iline) + "行"+",账号为:"+linebuf[22:45].lstrip().rstrip())
                        procFlag = 1
                        chkFlag = 1
                        #linebuf = bfp.readline()
                        #continue
                        ##end
                        
                    #begin  关彬捷  20090330
                    if chkFlag == 1:
                        linebuf = bfp.readline()
                        continue
                    #end

                    #筛选状态为正常的记录
                    if ( m_status == '1' ):

                        #统计金额和笔数
                        m_totalnum = m_totalnum + 1
                        m_totalamt = m_totalamt + (long)((float)(m_tradeamt) * 100 + 0.1)

                        if ( s_agenttype == '3' ):
                            if ( m_agenttype != '4' ):
                                
                                #begin  关彬捷  20090330
                                
                                #bfp.close()
                                #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(委托方式不匹配):第" + str(iline) + "行")
                                #return ExitThisFlow("9000", "自动撤消,批量数据非法(委托方式不匹配):第" + str(iline) + "行")
                                
                                UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(委托方式不匹配):第" + str(iline) + "行"+",账号为:"+linebuf[22:45].lstrip().rstrip())
                                procFlag = 1
                                linebuf = bfp.readline()
                                continue
                                #end


                            #校验客户信息是合法
                            if not ChkCustInfo(TradeContext.APPNO, TradeContext.BUSINO, m_accno):
                                
                                #begin  关彬捷  20090330
                                
                                #bfp.close()
                                #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(客户未签约):第" + str(iline) + "行")
                                #return ExitThisFlow("9000", "自动撤消,批量数据非法(客户未签约):第" + str(iline) + "行")
                                
                                UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(客户未签约):第" + str(iline) + "行"+",账号为:"+linebuf[22:45].lstrip().rstrip())
                                procFlag = 1
                                linebuf = bfp.readline()
                                continue
                                #end

                        elif ( s_agenttype == '4' ):
                            if ( m_agenttype != '3' ):
                                
                                #begin  关彬捷  20090330
                                
                                #bfp.close()
                                #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(委托方式不匹配):第" + str(iline) + "行")
                                #return ExitThisFlow("9000", "自动撤消,批量数据非法(委托方式不匹配):第" + str(iline) + "行")
                                
                                UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(委托方式不匹配):第" + str(iline) + "行"+",账号为:"+linebuf[22:45].lstrip().rstrip())
                                procFlag = 1
                                linebuf = bfp.readline()
                                continue
                                #end

                        else:
                            
                            #begin  关彬捷  20090330
                            
                            #bfp.close()
                            #UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量数据非法(委托方式错):第" + str(iline) + "行")
                            #return ExitThisFlow("9000", "自动撤消,批量数据非法(委托方式错):第" + str(iline) + "行")
                            
                            UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","批量数据非法(委托方式错):第" + str(iline) + "行"+",账号为:"+linebuf[22:45].lstrip().rstrip())
                            procFlag = 1
                            linebuf = bfp.readline()
                            continue
                            #end

                else:
                    
                    #begin  关彬捷  20090330
                    
                    #bfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "自动撤消,记录标志错,第" + str(iline) + '行')
                    #return ExitThisFlow("9000", "自动撤消,记录标志错:第" + str(iline) + "行")
                    
                    UpdateBatchInfo(curBatchNo, "40", "自动撤消,原因见详细信息","记录标志错,第" + str(iline) + '行'+",账号为:"+linebuf[22:45].lstrip().rstrip())
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end


                #从文件中读取一行
                linebuf = bfp.readline()

            #关闭文件
            bfp.close()
            
            #begin  关彬捷  20090330 
            if (procFlag == 1):
                return ExitThisFlow( "9000", "自动撤消,原因已写入详细处理文件")
            #end

            #转换
            ls_totalnum = (long)(s_totalnum)
            lm_totalnum = (long)(m_totalnum)

            ls_totalamt = (long)(((float)(s_totalamt)) * 100 + 0.1)
            lm_totalamt = m_totalamt

            WrtLog('>>>申请笔数=%d 申请金额=%d 明细笔数=%d 明细金额=%d' % (ls_totalnum, ls_totalamt, lm_totalnum, lm_totalamt))

            #判断总笔数,总金额
            if ( (ls_totalnum!=lm_totalnum) or (ls_totalamt!=lm_totalamt) ):
                UpdateBatchInfo(curBatchNo, "40", "自动撤消:批量文件总笔数和总金额与申请的不符")
                return ExitThisFlow("9000", "自动撤消,批量文件总笔数和总金额与申请的不符")


            UpdateBatchInfo(curBatchNo, "11", "数据校验成功->待联社审批")
            
            #################################################################
            #20090927 蔡永贵增加  即时处理不需要经联社和中心审批
            #----------------------------------------------------------------
            if ( TradeContext.NOTE3 == '0' ):
                UpdateBatchInfo( curBatchNo, "21", "即时处理->待提交" )
                return ExitThisFlow( "0000", "即时处理->待提交" )
            #################################################################
                
            return ExitThisFlow("0000", "数据校验成功->待联社审批")


        else:
            UpdateBatchInfo(curBatchNo, "40", "自动撤消,批量处理数据文件不存在:文件名=" + bFileName)
            return ExitThisFlow("9000", "自动撤消,批量处理数据文件不存在:文件名=" + bFileName)


    except Exception, e:
        bfp.close()
        WrtLog( str(e) )
        UpdateBatchInfo(curBatchNo, "40", "申请处理(VMENU)异常(请检查数据文件)")
        return ExitThisFlow( '9999', '申请处理(VMENU)异常')





######################################################################################################################
#功能描述：提交处理
######################################################################################################################
def TJ_Proc(curBatchNo):


    WrtLog('>>>提交处理(TJ_Proc)')


    try:
        if TradeContext.existVariable('NOTE1'):
            if TradeContext.NOTE1=='1':
                return ExitThisFlow( '9000', '该批次由别的交易渠道正在提交,本次提交不受理')


        #修改批次状态为正在提交
        UpdateBatchInfoTJ(curBatchNo, "1")

        sFileName   = curBatchNo + '_1'
        dFileName   = curBatchNo + '_2'
        lFileName   = curBatchNo + '_2'
        rFileName   = 'A' + curBatchNo[8:16] + '1'


        #生成主机批量文件
        if not CrtBatchFile(curBatchNo) :
            UpdateBatchInfoTJ(curBatchNo, "0")
            return ExitThisFlow( '9000', '生成提交文件失败')


        WrtLog('>>>生成提交文件['+ sFileName  +']')


        #ASC->BCD
        if not FormatFile("1", sFileName, dFileName):
            UpdateBatchInfoTJ(curBatchNo, "0")
            UpdateBatchInfo(curBatchNo, "40", "自动撤消,格式化文件失败")
            return ExitThisFlow( '9000', '自动撤消,格式化文件失败')


        WrtLog('>>>生成主机文件['+ dFileName  +']')


        if not ftpfile(0, lFileName, rFileName):
            UpdateBatchInfoTJ(curBatchNo, "0")
            return ExitThisFlow( '9000', '提交处理FTP失败')


        WrtLog('>>>上传主机文件['+ rFileName  +']')


        #修改提交时间
        if not UpdateBatchDate(curBatchNo,TradeContext.WorkDate,TradeContext.WorkTime) :
            UpdateBatchInfoTJ(curBatchNo, "0")
            return ExitThisFlow( '9000', '修改提交时间失败')


        WrtLog('>>>修改提交时间['+ TradeContext.WorkDate + ':' + TradeContext.WorkTime  +']')


        #通知主机进行批量作业
        ret = SendToHost(curBatchNo)
        if ( ret < 0 ):
            UpdateBatchInfoTJ(curBatchNo, "0")
            return ExitThisFlow( '9000', '提交处理通知失败')
        
        #20091103  蔡永贵  增加调用日间批量方法
        if( TradeContext.NOTE3 == '0'):
            #通知主机进行日间批量记账作业    
            ret = CallHost(curBatchNo)
            #if ( ret < 0 ):
            #    UpdateBatchInfoTJ(curBatchNo, "0")
            #    return ExitThisFlow( '9000', '日间批量记账失败')


        UpdateBatchInfoTJ(curBatchNo, "0")


        UpdateBatchInfo(curBatchNo, "22", "提交处理成功->已提交")


        WrtLog('>>>状态：提交处理成功->已提交[状态:21->22]')

        return True


    except Exception, e:
        WrtLog( str(e) )
        UpdateBatchInfoTJ(curBatchNo, "0")
        return ExitThisFlow( '9999', '提交处理异常')


######################################################################################################################
#功能描述：请求生成结果文件
######################################################################################################################
def SC_Proc(curBatchNo):


    WrtLog('>>>请求生成结果文件(SC_Proc)')


    try:
        ret = RecvResultFile(curBatchNo)
        if ( ret < 0 ):
            return ExitThisFlow( '9000', '下载批量处理结果文件失败')


        if ( ret == 0 ):
            sql = ""
            sql = "UPDATE ABDT_BATCHINFO SET "
#           sql = sql + "TOTALNUM=" +  "'" + HostContext.O1SUCN    + "',"         #委托总笔数
#           sql = sql + "TOTALAMT=" +  "'" + HostContext.O1SUCN    + "',"         #委托总金额
            sql = sql + "SUCCNUM="  +  "'" + HostContext.O1SUCN    + "',"         #成功总笔数
            sql = sql + "SUCCAMT="  +  "'" + HostContext.O1AMAO    + "',"         #成功总金额
            sql = sql + "FAILNUM="  +  "'" + HostContext.O1FACN    + "',"         #失败总笔数
            sql = sql + "FAILAMT="  +  "'" + HostContext.O1AMOT    + "'"          #失败总金额

            sql = sql + " WHERE "

            sql = sql + "BATCHNO=" + "'" + curBatchNo    + "'"        #委托号

            WrtLog(sql)

            retcode = AfaDBFunc.UpdateSqlCmt( sql )
            if (retcode <= 0):
                return ExitThisFlow( '9000', '修改批次的处理结果信息失败')


            UpdateBatchInfo(curBatchNo, "31", "主机已经生成文件->正在提回")

            WrtLog('>>>主机已经生成文件->正在提回')
                
            return True

        else:
            UpdateBatchInfo(curBatchNo, "30", "主机处理成功->待提回")

            WrtLog('>>>状态：主机处理成功->待提回')

            return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '生成批量结果文件异常')




######################################################################################################################
#功能描述：查询主机结果文件是否已经生成
######################################################################################################################
def CX_Proc(curBatchNo):

    WrtLog('>>>查询主机结果文件是否已经生成(CX_Proc)')

    try:
        ret = ChkHostFile(curBatchNo)
        if ( ret < 0 ):
            return ExitThisFlow( '9000', '查询主机结果文件是否已经生成,失败')

        if ( ret == 1):
            UpdateBatchInfo(curBatchNo, "22", "提交处理成功->已提交(等待主机处理...)")
            return ExitThisFlow( '9000', '提交处理成功->已提交(等待主机处理...)')


        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET "
#       sql = sql + "TOTALNUM=" +  "'" + HostContext.O1SUCN    + "',"         #委托总笔数
#       sql = sql + "TOTALAMT=" +  "'" + HostContext.O1SUCN    + "',"         #委托总金额
        sql = sql + "SUCCNUM="  +  "'" + HostContext.O1SUCN    + "',"         #成功总笔数
        sql = sql + "SUCCAMT="  +  "'" + HostContext.O1AMAO    + "',"         #成功总金额
        sql = sql + "FAILNUM="  +  "'" + HostContext.O1FACN    + "',"         #失败总笔数
        sql = sql + "FAILAMT="  +  "'" + HostContext.O1AMOT    + "'"          #失败总金额

        sql = sql + " WHERE "

        sql = sql + "BATCHNO=" + "'" + curBatchNo    + "'"        #委托号

        WrtLog(sql)

        retcode = AfaDBFunc.UpdateSqlCmt( sql )
        if (retcode <= 0):
            return ExitThisFlow( '9000', '修改批次的处理结果信息失败')

        UpdateBatchInfo(curBatchNo, "31", "主机已经生成文件->正在提回")

        WrtLog('>>>状态：主机已经生成文件->正在提回')

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '查询批量状态异常')


######################################################################################################################
#功能描述：提回处理
######################################################################################################################
def TH_Proc(curBatchNo):


    WrtLog('>>>提回处理(TH_Proc)')


    try:
        #本地(主机下载)
        lFileName = curBatchNo + '_3'

        #主机
        rFileName = 'A' + curBatchNo[8:16] + '2'

        sFileName = curBatchNo + '_3'
        dFileName = curBatchNo + '_4'

        if not ftpfile(1, lFileName, rFileName) :
            return ExitThisFlow( '9000', '提回处理FTP(获取)失败[主机文件:'+ rFileName +']')


        WrtLog('>>>下载主机文件['+ sFileName  +']')


        #BCD->ASC
        if not FormatFile("2", sFileName, dFileName):
            return ExitThisFlow( '9000', '格式化主机批量文件失败[本地文件:'+ lFileName +']')


        WrtLog('>>>生成提回文件['+ dFileName  +']')

        UpdateBatchInfo(curBatchNo, "32", "提回处理成功->已提回")

        WrtLog('>>>状态：提回处理成功->已提回')

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '提回处理异常')



######################################################################################################################
#功能描述：回盘处理
######################################################################################################################
def HP_Proc(curBatchNo):

    WrtLog('>>>回盘处理(HP_Proc)')

    try:
        #生成回盘文件
        
        #20120409 陈浩修改添加--AG07
        #if ( TradeContext.APPNO[0:4] == 'AG08' ):
        if ( TradeContext.APPNO[0:4] == 'AG08' or TradeContext.APPNO[0:4] == 'AG07'):
            #财政特殊处理(修改人：徐忠和，修改日期：20080402)
            #查询资金代码
            if not QueryZJDM() :
                return False

            if not CrtBusiFileCZ(curBatchNo):
                return False

        else:
            if not CrtBusiFile(curBatchNo):
                return False

        WrtLog('>>>生成回盘文件成功')

        #生成报表文件
        if not CrtBankFile(curBatchNo) :
            return False

        WrtLog('>>>生成业务报表成功')

        UpdateBatchInfo(curBatchNo, "88", "该批次处理已经结束")
            
        return True


    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '回盘处理异常')



















#############################################################################################################
#  财政代发特殊处理方法，修改人:XZH   修改日期:20080402
#############################################################################################################

#查询资金代码
def QueryZJDM():

    WrtLog('>>>查询资金代码(QueryZJDM)')

    try:
        sql = "SELECT CZZJDM,ZJDMMC,NOTE1,NOTE2 FROM ABDT_CZDZB WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.APPNO  + "'"        #业务编号

        WrtLog(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '资金代码信息失败')

        if ( len(records) == 0 ):
            return ExitThisFlow( '9000', '没有资金代码信息')

        else:
            TradeContext.CZZJDM  = str(records[0][0]).strip()           #资金代码
            TradeContext.CZZJDMMC= str(records[0][1]).strip()           #单位名称
            TradeContext.CZNOTE1 = str(records[0][2]).strip()           #备注1
            TradeContext.CZNOTE2 = str(records[0][3]).strip()           #备注2
            return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '查询资金代码异常')



#创建单位回盘文件
def CrtBusiFileCZ(curBatchNo):

    WrtLog('>>>创建单位回盘文件(CrtBusiFileCZ)')

    try:
        #主机返回文件
        rHostFile= os.environ['AFAP_HOME'] + '/data/batch/host/' +  curBatchNo + '_4'
        WrtLog(rHostFile)

        #乡级回盘文件
        
        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        rBusiFile= os.environ['AFAP_HOME'] + '/data/batch/down/' +  TradeContext.CZZJDM + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + '.RET'
        #end
        
        WrtLog(rBusiFile)

        #省级回盘文件
        
        #begin
        #20091102  蔡永贵  由于同一机构一天可以传多笔，为避免文件被覆盖，修改文件命名，在机构号后均加上批次号（NOTE2）
        qBusiFile= os.environ['AFAP_HOME'] + '/data/batch/down/' +  TradeContext.CZZJDM + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + '.TXT'
        #end
        
        WrtLog(qBusiFile)

        #打开主机下载文件
        chFp = open(rHostFile, "r")
            
        #创建企业回盘文件
        cbFp = open(rBusiFile, "w")
        cqFp = open(qBusiFile, "w")

        #写入汇总语句
        wbuffer = ''
        wbuffer = wbuffer + TradeContext.TOTALNUM + '|'                   #总笔数
        wbuffer = wbuffer + TradeContext.TOTALAMT + '|'                   #总金额
        wbuffer = wbuffer + TradeContext.SUCCNUM  + '|'                   #成功笔数
        wbuffer = wbuffer + TradeContext.SUCCAMT  + '|'                   #成功金额
        wbuffer = wbuffer + TradeContext.FAILNUM  + '|'                   #失败笔数
        wbuffer = wbuffer + TradeContext.FAILAMT  + '|'                   #失败金额
        wbuffer = wbuffer + '\n'

        WrtLog("================0=====================")
        
        cbFp.write(wbuffer)
        
        WrtLog("================1=====================")
        
        cqFp.write(wbuffer)
        
        WrtLog("================2=====================")
            
        #WrtLog(wbuffer)
        
        WrtLog("================3=====================")

        #读取一行
        linebuf = chFp.readline()

        WrtLog("================5=====================")

        while ( len(linebuf) > 0 ):

            if ( len(linebuf) < 994 ):
                chFp.close()
                cbFp.close()
                cqFp.close()
                return ExitThisFlow( '9000', '该批次下载文件格式错误,请检查')

            swapbuf = linebuf[0:994].split('<fld>')
            #WrtLog(linebuf)
            #写入明细信息
            wbuffer = ''
            wbuffer = swapbuf[25].strip() + TradeContext.CZZJDM + '|'       #客户标识            
            if ( TradeContext.AGENTTYPE == '3' ):
                wbuffer = wbuffer + swapbuf[14].strip() + '|'               #活期帐号
                wbuffer = wbuffer + swapbuf[15].strip() + '|'               #客户姓名
            else:
                wbuffer = wbuffer + swapbuf[20].strip() + '|'               #活期帐号
                wbuffer = wbuffer + swapbuf[21].strip() + '|'               #客户姓名

            wbuffer = wbuffer + swapbuf[28].strip()     + '|'               #金额
            tmp_retcode = swapbuf[5].strip()
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                #成功
                wbuffer = wbuffer + swapbuf[3].strip()      + '|'           #记帐日期
                tmp_retcode = '0'
            else:
                #失败
                wbuffer = wbuffer +                          '|'           #记帐日期(失败,则为空)
                tmp_retcode = '1'

            #WrtLog("================6=====================")

            #省级回盘文件
            cqFp.write(wbuffer + '\n')

            #WrtLog("================7=====================")

            wbuffer = wbuffer + tmp_retcode             + '|'               #标志(返回码)
            tmp_retcode = swapbuf[5].strip()
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                #成功
                tmp_retcode = '代发成功'
            wbuffer = wbuffer + tmp_retcode             + '|'               #错误信息
            wbuffer = wbuffer + '\n'

            #WrtLog("================8=====================")
                
            #乡级回盘文件
            cbFp.write(wbuffer)
            
            #WrtLog("================9=====================")
            
            #读取主机返回文件的下一行
            linebuf = chFp.readline()

            #WrtLog("================A=====================")
                
        chFp.close()

        WrtLog("================B=====================")

        cbFp.close()

        WrtLog("================C=====================")

        cqFp.close()
            
        WrtLog("================D=====================")
            
        return True

    except Exception, e:
        WrtLog( str(e) )

        WrtLog("================E=====================")
            
        chFp.close()
        
        WrtLog("================F=====================")
        
        cbFp.close()
        
        WrtLog("================G=====================")
        
        cqFp.close()
            
        WrtLog("================H=====================")
            
        return ExitThisFlow( '9999', '创建单位回盘文件异常')
        

#关彬捷  20090330  删除详细处理信息文件
def DelProcmsgFile(pBatchNo):
    
    WrtLog('>>>删除详细处理信息文件')

    try:
        procmsgFile = os.environ['AFAP_HOME'] + '/data/batch/procmsg/abdt_procmsg' + pBatchNo + ".txt"

        if ( os.path.exists(procmsgFile) and os.path.isfile(procmsgFile) ):
            cmdstr = "rm " + procmsgFile
            WrtLog('>>>删除命令:' + cmdstr)
            os.system(cmdstr)
            return True
            
        else:
            WrtLog('详细处理信息文件[abdt_procmsg' + pBatchNo + '.txt]不存在')

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '删除详细处理信息文件异常')
