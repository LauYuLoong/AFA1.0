# -*- coding: gbk -*-
###################################################################
#    文    件:    Tvouh023.py
#    说    明:    凭证管理-->生成凭证主机对帐文件
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日 
#    维护纪录:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools,  AfaFlowControl, AfaDBFunc, os ,HostContext ,sys
from types import *
import VouhFunc,VouhHostFunc
TradeContext.sysType = 'cron'
#AfaFunc,datetime

def MatchData():
    try:
        #=============获取当前系统时间==========================
        sLstTrxDay  = AfaUtilTools.GetSysDate( )
        sLstTrxTime = AfaUtilTools.GetSysTime( )
        
        #=============获取前一天的日期=========================================
        #sLstTrxDay  = (datetime.datetime(int(sLstTrxDay[:4]),int(sLstTrxDay[4:6]),int(sLstTrxDay[6:8]))-datetime.timedelta(days=1)).strftime("%Y%m%d")
        
        #查询对帐未成功日期
        sqlStr = "select distinct WORKDATE from VOUH_MODIFY where chkflag != '0' and TRANSTATUS = '0'"
        records = AfaDBFunc.SelectSql( sqlStr )
        VouhFunc.WrtLog('>>>' + sqlStr)

        if( records == None ):
            VouhFunc.WrtLog('>>>查询错误')

        elif( len( records ) == 0 ):
            VouhFunc.WrtLog('>>>已与主机对帐')

        else:
            for i in range(len(records)):
                print records[i][0]
                SendData(records[i][0])
            
        #=============程序退出====================
    except Exception, e:
        print str(e) 
        
###############################主机对帐发送############################################
def SendData(sLstTrxDay):
    #查询对帐信息
    sqlStr = "select WORKDATE,HOSTDATE,VOUHSERIAL,HOSTSERIAL,char(sum(int(VOUHNUM))) \
            from VOUH_MODIFY  \
            where WORKDATE = '" + sLstTrxDay + "' \
            and TRANSTATUS = '0'\
            group by WORKDATE,HOSTDATE,VOUHSERIAL,HOSTSERIAL \
            order by int(VOUHSERIAL)"
    
    records = AfaDBFunc.SelectSql( sqlStr )
    print sqlStr
    AfaLoggerFunc.tradeInfo(sqlStr)
    if( records == None ):
        print "查询错误"
        raise AfaFlowControl.flowException( )
    elif( len( records ) == 0 ):
        print "查询为空"
        raise AfaFlowControl.flowException( )
    
    rBankFile= os.environ['AFAP_HOME'] + '/data/vouh/vh'+ sLstTrxDay
    
    #创建业务报表文件
    bFp = open(rBankFile, "w")
    
    records=AfaUtilTools.ListFilterNone( records )
    total = len(records)
    for i in range( len( records ) ):
        wbuffer = ''
        
        wbuffer = wbuffer +(records[i][0].strip()).ljust(8,' ') + "|"
        wbuffer = wbuffer +(records[i][1].strip()).ljust(8,' ') + "|"
        wbuffer = wbuffer +(records[i][2].strip()).ljust(8,' ') + "|"
        wbuffer = wbuffer +(records[i][3].strip()).ljust(10,' ') + "|"
        wbuffer = wbuffer +(records[i][4].strip()).ljust(10,' ') + "|"
        #写入报表文件
        bFp.write(wbuffer + '\n')
    
    #关闭文件
    bFp.close()
    
    sFileName = "vh" + sLstTrxDay
    dFileName = "TPCZFILE.TP" + sLstTrxDay
    if not VouhFunc.FormatFile("1",sFileName,dFileName):
        TradeContext.errorCode, TradeContext.errorMsg= "S999","转换主机对账文件编码异常"
        raise Exception,TradeContext.errorMsg
    #上传文件
    AfaLoggerFunc.tradeInfo("上传文件")
    print ">>>上传文件"
    VouhFunc.putHost("TPCZFILE.TP" + sLstTrxDay)
    #主机对帐
    
    HostContext.I1SBNO = '3400008889'
    HostContext.I1USID = '999986'
    HostContext.I1WSNO = '1234567890'
    HostContext.I1FINA = "TP" + sLstTrxDay
    HostContext.I1COUT = total
    print ">>>主机对帐"
    if not VouhHostFunc.CommHost('8828'):
        print ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg
        
    print ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg
    
    #修改对帐标志
    if not UpdChkFlag('0',sLstTrxDay):
        return Flase
    
    return True
        
######################################修改凭证状态########################################
def UpdStatus(sStatus):

    VouhFunc.WrtLog('>>>修改凭证状态')
    
    #'签到状态(0-签退 1-签到)';

    updSql = "UPDATE VOUH_PARAMETER SET STATUS='" + str(sStatus) + "'"

    VouhFunc.WrtLog(updSql)

    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result <= 0 ):
        VouhFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        VouhFunc.WrtLog('>>>处理结果:修改凭证状态,数据库异常')
        return False

    VouhFunc.WrtLog('>>>修改凭证状态 ---> 成功')

    return True
    
############################修改对帐标志########################################
def UpdChkFlag(chkFlag,wrokDate):
    VouhFunc.WrtLog('>>>修改对帐标志')
    
    updSql = "UPDATE VOUH_MODIFY SET CHKFLAG ='" + chkFlag + "' WHERE WORKDATE = '" + wrokDate + "' \
                and TRANSTATUS = '0'"
    
    VouhFunc.WrtLog(updSql)
    
    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result <= 0 ):
        VouhFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        VouhFunc.WrtLog('>>>处理结果:修改对帐标志,数据库异常')
        return False

    VouhFunc.WrtLog('>>>修改对帐标志 ---> 成功')

    return True
    
###########################################主函数###########################################
if __name__=='__main__':

    print('**********中间业务凭证管理操作开始**********')
    
    sProcType   = sys.argv[1]

    if ( sProcType == '01' ):
        VouhFunc.WrtLog('>>>签到')
        if not UpdStatus(1):
            sys.exit(-1)


    elif ( sProcType == '02' ):
        VouhFunc.WrtLog('>>>签退')
        if not UpdStatus(0):
            sys.exit(-1)


    elif ( sProcType == '03' ):
        
        VouhFunc.WrtLog('>>>强行签退')
        if not UpdStatus(0):
            sys.exit(-1)

        VouhFunc.WrtLog('>>>与主机对帐')
        if not MatchData():
            sys.exit(-1)

    else:
        VouhFunc.WrtLog('操作类型错误,请检查')
        sys.exit(-2)


    print '**********中间业务凭证操作结束**********'

    sys.exit(0)

    

#=============返回错误码,错误信息===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

