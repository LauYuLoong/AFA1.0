# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AbdtFunc.py
# �ļ���ʶ��
# ժ    Ҫ������ҵ�񹫹���
#
# ��ǰ�汾��2.0
# ��    �ߣ�XZH
# ������ڣ�2008��06��10��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext,AfaUtilTools,AfaFunc,AfaDBFunc,ConfigParser,sys,os,time,AfaHostFunc,AfaLoggerFunc,HostContext
from types import *

#========================��λЭ��У��=============================
def ChkUnitInfo( ):
    AfaLoggerFunc.tradeInfo('>>>�жϵ�λЭ���Ƿ���Ч')

    try:
        sql = ""
        sql = "SELECT SIGNUPMODE,GETUSERNOMODE,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO,AGENTTYPE,VOUHNO FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + TradeContext.Appno       + "'" + " AND "        #ҵ����
        sql = sql + "BUSINO=" + "'" + TradeContext.PayeeUnitno + "'" + " AND "        #��λ���
        sql = sql + "STATUS=" + "'" + "1"                      + "'"                  #״̬

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ��λЭ����Ϣ�쳣' )
    
        if ( len(records) <= 0 ):
            return ExitSubTrade( '9000', 'û�е�λЭ����Ϣ,���ܽ��д������')

        #����None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.SIGNUPMODE    = str(records[0][0])                             #ǩԼ��ʽ
        TradeContext.GETUSERNOMODE = str(records[0][1])                             #�̻��ͻ���Ż�ȡ��ʽ
        TradeContext.STARTDATE     = str(records[0][2])                             #��Ч����
        TradeContext.ENDDATE       = str(records[0][3])                             #ʧЧ����
        TradeContext.STARTTIME     = str(records[0][4])                             #����ʼʱ��
        TradeContext.ENDTIME       = str(records[0][5])                             #������ֹʱ��
        TradeContext.ACCNO         = str(records[0][6])                             #�Թ��˻�
        TradeContext.AGENTTYPE     = str(records[0][7])                             #ί�з�ʽ
        TradeContext.VOUHNO        = str(records[0][8])                             #ƾ֤��(�ڲ��ʻ�)

        AfaLoggerFunc.tradeInfo( "TranDate=[" + TradeContext.TranDate + "]" )

        if ( (TradeContext.STARTDATE > TradeContext.TranDate) or (TradeContext.TranDate > TradeContext.ENDDATE) ):
            return ExitSubTrade( '9000', '�õ�λί��Э�黹û����Ч���ѹ���Ч��')

        if ( (TradeContext.STARTTIME > TradeContext.TranTime) or (TradeContext.TranTime > TradeContext.ENDTIME) ):
            return ExitSubTrade( '9000', '�Ѿ�������ϵͳ�ķ���ʱ��,��ҵ�������[' + s_StartDate + ']-[' + s_EndDate + ']ʱ�������')

        if ((TradeContext.SIGNUPMODE=="1") and (TradeContext.GETUSERNOMODE=="1")):
            #���͵�ͨѶǰ�ò��ӵ�������ȡЭ��
            return True

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�жϵ�λЭ����Ϣ�Ƿ����ʧ��')

#========================�˻���ѯ(����)=============================
def QueryAccInfo( ):
    AfaLoggerFunc.tradeInfo(">>>��ѯ�˻���Ϣ(����)")

    try:
        #ͨѶ�����
        HostContext.I1TRCD = '8810'                        #����������
        HostContext.I1SBNO = TradeContext.brno             #�ý��׵ķ������
        HostContext.I1USID = TradeContext.tellerno         #���׹�Ա��
        HostContext.I1AUUS = TradeContext.authteller       #��Ȩ��Ա
        HostContext.I1AUPS = TradeContext.authtellerpwd    #��Ȩ��Ա����
        HostContext.I1WSNO = TradeContext.termId           #�ն˺�
        HostContext.I1ACNO = TradeContext.PayerAccno       #�ʺ�
        HostContext.I1CYNO = '01'                          #����

        #if ( TradeContext.I1PASSCHKFLAG == "1" ):
        #    HostContext.I1CFFG = "0"                       #����У���־(��Ҫ)
        #else:
        #    HostContext.I1CFFG = "1"                       #����У���־(����Ҫ)
        HostContext.I1CFFG = '1'

        HostContext.I1PSWD = ''                            #����
        HostContext.I1CETY = ''                            #ƾ֤����
        HostContext.I1CCSQ = ''                            #ƾ֤����
        HostContext.I1CTFG = '0'                           #�����־

        #������ͨѶ
        if not AfaHostFunc.CommHost('8810'):
            return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )
            
        #��������������Ϣ
        TradeContext.USERNAME   = HostContext.O1CUNM        #�û�����
        TradeContext.IDTYPE     = HostContext.O1IDTY        #֤������
        TradeContext.IDCODE     = HostContext.O1IDNO        #֤������
        TradeContext.ACCSTATUS  = HostContext.O1ACST        #�˻�״̬

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '��ѯ�˻���Ϣ(����)�쳣')

#========================�˻���ѯ(VMENUֱ�Ӳ�ѯ)=============================
def VMENU_QueryAccInfo():
    AfaLoggerFunc.tradeInfo('>>>��ѯ�˻���Ϣ')

    try:
        #ͨѶ�����
        HostContext.I1TRCD = '8810'                        #����������
        HostContext.I1SBNO = TradeContext.I1SBNO           #�ý��׵ķ������
        HostContext.I1USID = TradeContext.I1USID           #���׹�Ա��
        HostContext.I1AUUS = TradeContext.I1AUUS           #��Ȩ��Ա
        HostContext.I1AUPS = TradeContext.I1AUPS           #��Ȩ��Ա����
        HostContext.I1WSNO = TradeContext.I1WSNO           #�ն˺�
        HostContext.I1ACNO = TradeContext.I1ACCNO          #�ʺ�
        HostContext.I1CYNO = '01'                          #����
        HostContext.I1CFFG = '1'                           #����У���־(0-��Ҫ,1-����Ҫ)
        HostContext.I1PSWD = ''                            #����
        HostContext.I1CETY = TradeContext.I1VOUHTYPE       #ƾ֤����
        HostContext.I1CCSQ = TradeContext.I1VOUHNO         #ƾ֤����
        HostContext.I1CTFG = TradeContext.I1CHFLAG         #�����־

        #������ͨѶ
        if not AfaHostFunc.CommHost('8810'):
            return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )

        if ( HostContext.O1REKD == '900' ):
            return ExitSubTrade( '9000', '�Ǹ��˽��㻧,���ܲ���' )

        TradeContext.tradeResponse.append(['O1USERNAME', HostContext.O1CUNM])   #�ͻ�����
        TradeContext.tradeResponse.append(['O1IDTYPE',   HostContext.O1IDTY])   #֤������
        TradeContext.tradeResponse.append(['O1IDCODE',   HostContext.O1IDNO])   #֤������
        TradeContext.tradeResponse.append(['O1MAFG',     HostContext.O1MAFG])   #��˾��/���˿���־(0:��λ 1:����)
        TradeContext.tradeResponse.append(['O1REKD',     HostContext.O1REKD])   #�˻�����(���⴦��900-�Ǹ��˽��㻧)
        TradeContext.tradeResponse.append(['O1ACBL',     HostContext.O1ACBL])   #�˻����
        TradeContext.tradeResponse.append(['O1CUBL',     HostContext.O1CUBL])   #�������
        TradeContext.tradeResponse.append(['O1DATA',     HostContext.O1ITEM])   #������Ϣ(��Ŀ����)

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '��ѯ�˻���Ϣ�쳣(����)' )

#========================�˳�ģ��=============================
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
         
#========================��ȡ���������ļ�=============================      
def getBatchConfig( cfgFileName = None ): 

    try:
        config = ConfigParser.ConfigParser( )
        if ( cfgFileName == None ):
            cfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open( cfgFileName ) )
        TradeContext.BATCH_APPTRFG    = config.get( 'BATCH', 'APPTRFG' )
        TradeContext.BATCH_MAXCOUNT   = config.get( 'BATCH', 'MAXCOUNT' )
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '��ȡ�����ļ��쳣' )