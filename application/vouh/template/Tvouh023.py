# -*- coding: gbk -*-
###################################################################
#    ��    ��:    Tvouh023.py
#    ˵    ��:    ƾ֤����-->����ƾ֤���������ļ�
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11�� 
#    ά����¼:   
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools,  AfaFlowControl, AfaDBFunc, os ,HostContext ,sys
from types import *
import VouhFunc,VouhHostFunc
TradeContext.sysType = 'cron'
#AfaFunc,datetime

def MatchData():
    try:
        #=============��ȡ��ǰϵͳʱ��==========================
        sLstTrxDay  = AfaUtilTools.GetSysDate( )
        sLstTrxTime = AfaUtilTools.GetSysTime( )
        
        #=============��ȡǰһ�������=========================================
        #sLstTrxDay  = (datetime.datetime(int(sLstTrxDay[:4]),int(sLstTrxDay[4:6]),int(sLstTrxDay[6:8]))-datetime.timedelta(days=1)).strftime("%Y%m%d")
        
        #��ѯ����δ�ɹ�����
        sqlStr = "select distinct WORKDATE from VOUH_MODIFY where chkflag != '0' and TRANSTATUS = '0'"
        records = AfaDBFunc.SelectSql( sqlStr )
        VouhFunc.WrtLog('>>>' + sqlStr)

        if( records == None ):
            VouhFunc.WrtLog('>>>��ѯ����')

        elif( len( records ) == 0 ):
            VouhFunc.WrtLog('>>>������������')

        else:
            for i in range(len(records)):
                print records[i][0]
                SendData(records[i][0])
            
        #=============�����˳�====================
    except Exception, e:
        print str(e) 
        
###############################�������ʷ���############################################
def SendData(sLstTrxDay):
    #��ѯ������Ϣ
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
        print "��ѯ����"
        raise AfaFlowControl.flowException( )
    elif( len( records ) == 0 ):
        print "��ѯΪ��"
        raise AfaFlowControl.flowException( )
    
    rBankFile= os.environ['AFAP_HOME'] + '/data/vouh/vh'+ sLstTrxDay
    
    #����ҵ�񱨱��ļ�
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
        #д�뱨���ļ�
        bFp.write(wbuffer + '\n')
    
    #�ر��ļ�
    bFp.close()
    
    sFileName = "vh" + sLstTrxDay
    dFileName = "TPCZFILE.TP" + sLstTrxDay
    if not VouhFunc.FormatFile("1",sFileName,dFileName):
        TradeContext.errorCode, TradeContext.errorMsg= "S999","ת�����������ļ������쳣"
        raise Exception,TradeContext.errorMsg
    #�ϴ��ļ�
    AfaLoggerFunc.tradeInfo("�ϴ��ļ�")
    print ">>>�ϴ��ļ�"
    VouhFunc.putHost("TPCZFILE.TP" + sLstTrxDay)
    #��������
    
    HostContext.I1SBNO = '3400008889'
    HostContext.I1USID = '999986'
    HostContext.I1WSNO = '1234567890'
    HostContext.I1FINA = "TP" + sLstTrxDay
    HostContext.I1COUT = total
    print ">>>��������"
    if not VouhHostFunc.CommHost('8828'):
        print ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg
        
    print ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg
    
    #�޸Ķ��ʱ�־
    if not UpdChkFlag('0',sLstTrxDay):
        return Flase
    
    return True
        
######################################�޸�ƾ֤״̬########################################
def UpdStatus(sStatus):

    VouhFunc.WrtLog('>>>�޸�ƾ֤״̬')
    
    #'ǩ��״̬(0-ǩ�� 1-ǩ��)';

    updSql = "UPDATE VOUH_PARAMETER SET STATUS='" + str(sStatus) + "'"

    VouhFunc.WrtLog(updSql)

    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result <= 0 ):
        VouhFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        VouhFunc.WrtLog('>>>������:�޸�ƾ֤״̬,���ݿ��쳣')
        return False

    VouhFunc.WrtLog('>>>�޸�ƾ֤״̬ ---> �ɹ�')

    return True
    
############################�޸Ķ��ʱ�־########################################
def UpdChkFlag(chkFlag,wrokDate):
    VouhFunc.WrtLog('>>>�޸Ķ��ʱ�־')
    
    updSql = "UPDATE VOUH_MODIFY SET CHKFLAG ='" + chkFlag + "' WHERE WORKDATE = '" + wrokDate + "' \
                and TRANSTATUS = '0'"
    
    VouhFunc.WrtLog(updSql)
    
    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result <= 0 ):
        VouhFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        VouhFunc.WrtLog('>>>������:�޸Ķ��ʱ�־,���ݿ��쳣')
        return False

    VouhFunc.WrtLog('>>>�޸Ķ��ʱ�־ ---> �ɹ�')

    return True
    
###########################################������###########################################
if __name__=='__main__':

    print('**********�м�ҵ��ƾ֤���������ʼ**********')
    
    sProcType   = sys.argv[1]

    if ( sProcType == '01' ):
        VouhFunc.WrtLog('>>>ǩ��')
        if not UpdStatus(1):
            sys.exit(-1)


    elif ( sProcType == '02' ):
        VouhFunc.WrtLog('>>>ǩ��')
        if not UpdStatus(0):
            sys.exit(-1)


    elif ( sProcType == '03' ):
        
        VouhFunc.WrtLog('>>>ǿ��ǩ��')
        if not UpdStatus(0):
            sys.exit(-1)

        VouhFunc.WrtLog('>>>����������')
        if not MatchData():
            sys.exit(-1)

    else:
        VouhFunc.WrtLog('�������ʹ���,����')
        sys.exit(-2)


    print '**********�м�ҵ��ƾ֤��������**********'

    sys.exit(0)

    

#=============���ش�����,������Ϣ===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True

