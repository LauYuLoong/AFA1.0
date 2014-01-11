# -*- coding: gbk -*-
###############################################################################
# 文件名称：AhXnbFunc.py
# 摘    要：安徽省新农保批量业务公共库
# 当前版本：1.0
# 作    者：蔡永贵
# 完成日期：2010年12月15日
###############################################################################
import TradeContext,AfaUtilTools,AfaDBFunc,ConfigParser,os,AfaLoggerFunc
from types import *
#sys,time,

#=====================判断单位协议是否有效=====================
def ChkUnitInfo( ):

    AfaLoggerFunc.tradeInfo('>>>判断单位协议是否有效')

    try:
        sql = ""
        sql = "SELECT SIGNUPMODE,GETUSERNOMODE,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO,AGENTTYPE,VOUHNO FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "        #业务编号
        sql = sql + "BUSINO=" + "'" + TradeContext.I1BUSINO + "'" + " AND "        #单位编号
        sql = sql + "STATUS=" + "'" + "1"                   + "'"                  #状态

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询单位协议信息异常' )
        if ( len(records) <= 0 ):
            return ExitSubTrade( '9000', '没有单位协议信息,不能进行此类操作')

        #过滤None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.SIGNUPMODE    = str(records[0][0])                             #签约方式
        TradeContext.GETUSERNOMODE = str(records[0][1])                             #商户客户编号获取方式
        TradeContext.STARTDATE     = str(records[0][2])                             #生效日期
        TradeContext.ENDDATE       = str(records[0][3])                             #失效日期
        TradeContext.STARTTIME     = str(records[0][4])                             #服务开始时间
        TradeContext.ENDTIME       = str(records[0][5])                             #服务终止时间
        TradeContext.ACCNO         = str(records[0][6])                             #对公账户
        TradeContext.AGENTTYPE     = str(records[0][7])                             #委托方式
        TradeContext.VOUHNO        = str(records[0][8])                             #凭证号(内部帐户)

        AfaLoggerFunc.tradeInfo( "WorkDate=[" + TradeContext.WorkDate + "]" )

        if ( (TradeContext.STARTDATE > TradeContext.WorkDate) or (TradeContext.WorkDate > TradeContext.ENDDATE) ):
            return ExitSubTrade( '9000', '该单位委托协议还没有生效或已过有效期')

        if ( (TradeContext.STARTTIME > TradeContext.WorkTime) or (TradeContext.WorkTime > TradeContext.ENDTIME) ):
            return ExitSubTrade( '9000', '已经超过该系统的服务时间,该业务必须在[' + s_StartDate + ']-[' + s_EndDate + ']时间段运行')

        if ((TradeContext.SIGNUPMODE=="1") and (TradeContext.GETUSERNOMODE=="1")):
            #发送到通讯前置并从第三方获取协议
            return True

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断单位协议信息是否存在失败')
        
        
#=====================抛出并打印提示信息=====================
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg
        AfaLoggerFunc.tradeInfo( errorMsg )
    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True
    else:
        return False
        
        
#=====================更新ahnx_file表中的状态=====================
def UpdateFileStatus(BatchNo, Status, ProcMsg, workTime):
    
    AfaLoggerFunc.tradeInfo( '更新ahnx_file表：BATCHNO=' + BatchNo + ' ' + Status + ' ' + workTime)

    try:
        sql = "UPDATE AHNX_FILE SET "
        sql = sql + " STATUS  ='" + Status   + "',"       #状态
        sql = sql + " PROCMSG ='" + ProcMsg  + "',"       #处理信息描述
        sql = sql + " WORKTIME='" + workTime + "'"        #操作时间
        sql = sql + " WHERE"
        sql = sql + " BATCHNO ='" + BatchNo  + "'"        #委托号
        
        AfaLoggerFunc.tradeInfo( '更新ahnx_file表处理状态sql：' + sql )
        
        result = AfaDBFunc.UpdateSqlCmt( sql )
        if (result <= 0):
            return ExitSubTrade( 'D001', '更新ahnx_file表失败')
            
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade( '9999', '更新ahnx_file表异常')
        

#=====================读取配置信息=====================
def getBatchFile( ConfigNode ):
    try:
        #读取FTP配置文件
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        
        config.readfp( open( configFileName ) )
        
        TradeContext.ABDT_PDIR    = config.get(ConfigNode,'ABDT_BDIR')     #批量上传文件存放路径
        TradeContext.ABDT_GDIR    = config.get(ConfigNode,'ABDT_GDIR')     #批量回盘文件存放路径
        TradeContext.XNB_BSDIR    = config.get(ConfigNode,'XNB_BSDIR')     #新农保转换前的路径
        TradeContext.XNB_BDDIR    = config.get(ConfigNode,'XNB_BDDIR')     #新农保转换后的路径
        
        
        return True
        
    except Exception, e:
        return ExitSubTrade( 'E0001', "读取配置文件异常：" + str(e))


#====================错误信息写入文件=================
def UpdateBatchInfo(pBatchNo, pStatus, pMessage,pInfo=0):
    AfaLoggerFunc.tradeInfo('>>>修改批次状态:[' + pStatus + ']' + pMessage)

    try:
        #-----1,将错误信息更新到ahxnb_file表的PROCMSG中
        sql = ""
        sql = "UPDATE AHNX_FILE SET "
        sql = sql + "STATUS="   +  "'" + pStatus     + "',"     #状态
        sql = sql + "PROCMSG="  +  "'" + pMessage    + "'"      #原因
        sql = sql + " WHERE BATCHNO = '" + pBatchNo  + "'"      #委托号"

        AfaLoggerFunc.tradeInfo(sql)
        result = AfaDBFunc.UpdateSqlCmt( sql )
        
        if ( result <= 0 ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '修改批次的状态失败')
            
        #-----1.1,批量签约的错误信息文件名为上传文件。
        sql = ""
        sql = sql + "select FILETYPE,FILENAME from AHNX_FILE"
        sql = sql + " where BATCHNO = '"+ pBatchNo +"'"
        
        AfaLoggerFunc.tradeInfo(sql)
        record = AfaDBFunc.SelectSql( sql )
        
        if record==None:
            return ExitSubTrade("D0001" ,"查询AHNX_FILE失败")
        elif(len(record) == 0):
            return ExitSubTrade("D0001" ,"无此信息")
        else:
            TradeContext.procFileType = record[0][0].strip()
            TradeContext.procFileName = record[0][1].strip()
        
        if( TradeContext.procFileType == '4' ):     #批量签约
            if pInfo:
                path_procmsg = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + TradeContext.procFileName
                fp_procmsg = open(path_procmsg,"a")
                fp_procmsg.write(pInfo + "\n")
                fp_procmsg.close()
            
        else:
            #-----2,把错误信息写入到错误文件中
            if pInfo:
                path_procmsg = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + pBatchNo + '.TXT'
                fp_procmsg = open(path_procmsg,"a")
                fp_procmsg.write(pInfo + "\n")
                fp_procmsg.close()

        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade( '9999', '修改批次的状态异常')
        

#=========================删除详细处理信息文件=========================
def DelProcmsgFile(pBatchNo):
    AfaLoggerFunc.tradeInfo('>>>删除详细处理信息文件')

    try:
        #-----1.1,批量签约的错误信息文件名为上传文件。
        sql = ""
        sql = sql + "select FILETYPE,FILENAME from AHNX_FILE"
        sql = sql + " where BATCHNO = '"+ pBatchNo +"'"
        
        AfaLoggerFunc.tradeInfo(sql)
        record = AfaDBFunc.SelectSql( sql )
        
        if record==None:
            return ExitSubTrade("D0001" ,"查询AHNX_FILE失败")
        elif(len(record) == 0):
            if( pBatchNo[0:6] == 'YHKHFS' ):
                procmsgFile = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + pBatchNo + '.TXT'
                if ( os.path.exists(procmsgFile) and os.path.isfile(procmsgFile) ):
                    cmdstr = "rm " + procmsgFile
                    AfaLoggerFunc.tradeInfo('>>>删除命令:' + cmdstr)
                    os.system(cmdstr)
                    return True
                    
                else:
                    AfaLoggerFunc.tradeInfo('详细处理信息文件[AHXNB_PROCMSG' + pBatchNo + '.TXT],不存在')
                    return True
                    
            return ExitSubTrade("D0001" ,"无此信息")
        else:
            TradeContext.procFileType = record[0][0].strip()
            TradeContext.procFileName = record[0][1].strip()
        
        if( TradeContext.procFileType == '4' ):     #批量签约
            procmsgFile = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + TradeContext.procFileName
            
            if ( os.path.exists(procmsgFile) and os.path.isfile(procmsgFile) ):
                cmdstr = "rm " + procmsgFile
                AfaLoggerFunc.tradeInfo('>>>删除命令:' + cmdstr)
                os.system(cmdstr)
                return True
                
            else:
                AfaLoggerFunc.tradeInfo('详细处理信息文件[AHXNB_PROCMSG' + TradeContext.procFileName + '],不存在')
                return True
        
        else:
            procmsgFile = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + pBatchNo + '.TXT'
            
            if ( os.path.exists(procmsgFile) and os.path.isfile(procmsgFile) ):
                cmdstr = "rm " + procmsgFile
                AfaLoggerFunc.tradeInfo('>>>删除命令:' + cmdstr)
                os.system(cmdstr)
                return True
                
            else:
                AfaLoggerFunc.tradeInfo('详细处理信息文件[AHXNB_PROCMSG' + pBatchNo + '.TXT')
                return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade( '9999', '删除详细处理信息文件异常')

#====================开户错误信息写入文件=================
def WriteInfo(FileName,Info):
    try:
        path_procmsg = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + FileName + '.TXT'
        fp_procmsg = open(path_procmsg,"a")
        fp_procmsg.write(Info + "\n")
        fp_procmsg.close()

        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade( '9999', '开户错误信息写入文件异常')