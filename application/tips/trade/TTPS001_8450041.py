# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.TIPS������ϸ����
#      9  ��ʼ
#      2  ������
#      3  �������������
#      4  ���Ķ������
#      0  ����ɹ�
#      1  ����ʧ��
#
#=================================================================
#   �����ļ�:   TTPS001_8450041.py
#   �޸�ʱ��:   2007-5-28 10:28
#   �� �� �ߣ�  ������
#   �޸�ʱ�䣺  2011-5-17
#   �޸����ݣ�  ɾ��ԭ�д���ע��
#               ���������ɹ�ʱ,�޸�ԭ����״̬Ϊ3-����
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,TipsFunc
import AfaDBFunc,ConfigParser,os
#,HostContext,HostComm
#import time,AfaUtilTools,TipsHostFunc,tipsConst,rccpsHostFunc,rccpsCronFunc
from types import *
#from tipsConst import *

#��ȡ���������ļ�����Ϣ
def GetLappConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOST_HOSTIP   = config.get('HOST_DZ', 'HOSTIP')
        TradeContext.HOST_USERNO   = config.get('HOST_DZ', 'USERNO')
        TradeContext.HOST_PASSWD   = config.get('HOST_DZ', 'PASSWD')
        TradeContext.HOST_LDIR     = config.get('HOST_DZ', 'LDIR')
        TradeContext.HOST_RDIR     = config.get('HOST_DZ', 'RDIR')
        TradeContext.CORP_CDIR     = config.get('HOST_DZ', 'CDIR')
        TradeContext.BANK_CDIR     = config.get('HOST_DZ', 'BDIR')
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return 0

    except Exception, e:
        print str(e)
        return -1


def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('��˰����_���˴���ʼ[TTPS001_8450041]' )
    try:
        #=============��ȡ��ǰϵͳʱ��====================
        #TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        #============����ֵ����Ч��У��============
        if( not TradeContext.existVariable( "chkAcctOrd" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkAcctOrd]ֵ������!' )
        if( not TradeContext.existVariable( "chkDate" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkDate]ֵ������!' )
        if( not TradeContext.existVariable( "chkAcctType" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkAcctType]ֵ������!' )
        if( not TradeContext.existVariable( "payeeBankNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[payeeBankNo]ֵ������!' )
        if( not TradeContext.existVariable( "payBkCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[payBkCode]ֵ������!' )
        #TradeContext.workDate=TradeContext.chkDate
        AfaLoggerFunc.tradeInfo('>>>�������ڣ�'+TradeContext.chkDate+'�������Σ�'+TradeContext.chkAcctOrd)
        
        #====�ж�Ӧ��״̬=======
        if not TipsFunc.ChkAppStatus():
            return False
        #====��ȡ������Ϣ=======
        if not TipsFunc.ChkLiquidStatus():
            return False
        
        #��ʼ��������
        if not UpdateBatchAdm('2','','������������ݽ��ж���') :
            return TipsFunc.ExitThisFlow( 'A0001', '��������״̬ʧ��!' )
        
        totalnum_succ=0
        totalamt_succ=0

        #�����ˮ���м�ҵ�����
        AfaLoggerFunc.tradeInfo('>>>�����ˮ���м�ҵ�����')
        sqlStr = "SELECT accno,amount,status,corpserialno FROM TIPS_CHECKDATA WHERE "
        sqlStr =sqlStr +" workDate = '"         + TradeContext.chkDate              + "'"
        sqlStr =sqlStr +" AND BATCHNO = '"      + TradeContext.chkAcctOrd           + "'"
        sqlStr =sqlStr +" AND PAYEEBANKNO ='"   + TradeContext.payeeBankNo.strip()    + "'"   
        sqlStr =sqlStr +" AND PAYBKCODE ='"     + TradeContext.payBkCode.strip()  + "'"
        sqlStr =sqlStr +" order by corpserialno"
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('������ϸ������쳣:'+AfaDBFunc.sqlErrMsg)
            UpdateBatchAdm('1','','����ʧ��:���ݿ��쳣(TIPS_CHECKDATA)')
            return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
        else:
            AfaLoggerFunc.tradeInfo('����������:'+str(len(Records)))
            for i in range(0, len(Records)):
                if (Records[i][2]=='0' ): #�ѳɹ�
                    continue
                if (Records[i][2]=='1' ): #�ѳɹ�
                    continue
                elif Records[i][2]=='9':    #��ˮ��δ����
                    #׼�����м�ҵ�����
                    ChkFlag = '*'
                    #�Ȳ�ѯ���ݿ��м�¼�Ƿ����
                    sqlstr_m = "SELECT AMOUNT,DRACCNO,SERIALNO,CORPCHKFLAG,BANKSTATUS FROM TIPS_MAINTRANSDTL WHERE"
                    sqlstr_m = sqlstr_m + " CORPTIME='"  + TradeContext.chkDate.strip()  + "'"
                    sqlstr_m = sqlstr_m + " AND CORPSERNO='"  + Records[i][3].strip()        + "'"
                    sqlstr_m = sqlstr_m + " AND NOTE3 = '" + TradeContext.payBkCode.strip() + "'"
                    sqlstr_m = sqlstr_m + " AND NOTE4 = '" + TradeContext.payeeBankNo.strip() + "'"
                    sqlstr_m = sqlstr_m + " AND BANKSTATUS = '0' AND REVTRANF='0'"
                    AfaLoggerFunc.tradeInfo(sqlstr_m)
                    records_m = AfaDBFunc.SelectSql( sqlstr_m )
                    if ( records_m==None ):
                        AfaLoggerFunc.tradeFatal('���ݿ��쳣:��ѯҵ����ˮ��'+AfaDBFunc.sqlErrMsg)
                        UpdateBatchAdm('1','','����ʧ��:���ݿ��쳣(TIPS_MAINTRANSDTL)')
                        return TipsFunc.ExitThisFlow( 'A0027', '�м�ҵ����ˮ������쳣' )
                    if (len(records_m) == 0 ):
                        AfaLoggerFunc.tradeInfo(Records[i])
                        UpdateBatchAdm('1','','����ʧ��:����ȱ��жึ���¼')
                        #������˻�ִ����
                        TradeContext.OriPayBankNo  =TradeContext.payBkCode
                        TradeContext.OriChkDate    =TradeContext.chkDate
                        TradeContext.OriChkAcctOrd =TradeContext.chkAcctOrd
                        TradeContext.OriPayeeBankNo=TradeContext.payeeBankNo
                        TradeContext.Result        ='24030'
                        TradeContext.AddWord       ='���ʲ�����TIPS����ҵ���жึ���¼'
                        subModuleName = 'TTPS001_032111'
                        subModuleHandle=__import__( subModuleName )
                        AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
                        if not subModuleHandle.SubModuleMainFst( ) :
                            return False
                        return TipsFunc.ExitThisFlow( '24030', '���ʲ�����TIPS����ҵ���жึ���¼' )
                    else:
                        if (records_m[0][3]=='0' ): #�ѳɹ�
                            continue
                        if (records_m[0][3]=='1' ): #�ѳɹ�
                            continue
                        elif records_m[0][3]=='9':    #��ˮ��δ����
                            c_tradeamt = (long)((float)(Records[i][1].strip())*100 + 0.1)
                            m_tradeamt = (long)((float)(records_m[0][0].strip())*100 + 0.1)
                            if ( c_tradeamt != m_tradeamt ):
                                UpdateBatchAdm('1','','����ʧ��:��ˮ����')
                                #������˻�ִ����
                                TradeContext.OriPayBankNo  =TradeContext.payBkCode
                                TradeContext.OriChkDate    =TradeContext.chkDate
                                TradeContext.OriChkAcctOrd =TradeContext.chkAcctOrd
                                TradeContext.OriPayeeBankNo=TradeContext.payeeBankNo
                                TradeContext.Result        ='24030'
                                TradeContext.AddWord       ='����ʧ��,����'
                                subModuleName = 'TTPS001_032111'
                                subModuleHandle=__import__( subModuleName )
                                AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
                                if not subModuleHandle.SubModuleMainFst( ) :
                                    return False
                                return TipsFunc.ExitThisFlow( '24030', '����ʧ��,����' )
                        ChkFlag = '0'
                        totalnum_succ = totalnum_succ+1
                        totalamt_succ = totalamt_succ + c_tradeamt
                
                    #�޸ļ�¼����״̬,�������ںͳ���
                    sqlstr_m = "UPDATE TIPS_MAINTRANSDTL SET CORPCHKFLAG='" + ChkFlag + "',NOTE1='"+TradeContext.chkDate+"',NOTE2='"+TradeContext.chkAcctOrd+"'"
                    #sqlstr_m = sqlstr_m + " ,CHKFLAG = '0'"
                    #sqlstr_m = sqlstr_m + " ,NOTE3 = '" + TradeContext.payBkCode + "',NOTE4 = '" + TradeContext.payeeBankNo + "' WHERE"
                    sqlstr_m = sqlstr_m + " WHERE"
                    sqlstr_m = sqlstr_m + " CORPTIME='"  + TradeContext.chkDate.strip()  + "'"
                    sqlstr_m = sqlstr_m + " AND CORPSERNO='"  + Records[i][3].strip()        + "'"
                    sqlstr_m = sqlstr_m + " AND NOTE3 = '" + TradeContext.payBkCode.strip() + "'"
                    sqlstr_m = sqlstr_m + " AND NOTE4 = '" + TradeContext.payeeBankNo.strip() + "'"
                    sqlstr_m = sqlstr_m + " AND BANKSTATUS = '0' AND REVTRANF='0'"
                    AfaLoggerFunc.tradeInfo(sqlstr_m)
                    retcode = AfaDBFunc.UpdateSqlCmt( sqlstr_m )
                    if (retcode==None or retcode <= 0):
                        UpdateBatchAdm('1','','����ʧ��:���ݿ��쳣(������ϸ��)2')
                        return TipsFunc.ExitThisFlow( 'A0027', '�޸ļ�¼����״̬,���ݿ��쳣' )
        
        #��������״̬
        if not UpdateBatchAdm('3','0000','�����������') :
            return TipsFunc.ExitThisFlow( 'A0001', '��������״̬ʧ��!' )
        
        #��ȡ�����ļ�����Ϣ
        GetLappConfig( )
        
        #���ж���
        if(TradeContext.chkAcctType=='1'):
            #���� ���б�TIPS�����ˮ
            if not rev_proc():
                return TipsFunc.ExitThisFlow( 'A0027', '�����쳣' )            
        
        #������˻�ִ����
        TradeContext.OrMsgRef  =TradeContext.MsgRef
        TradeContext.OriPayBankNo  =TradeContext.payBkCode
        TradeContext.OriChkDate    =TradeContext.chkDate
        TradeContext.OriChkAcctOrd =TradeContext.chkAcctOrd
        TradeContext.OriPayeeBankNo=TradeContext.payeeBankNo
        TradeContext.Result        ='90000'
        TradeContext.AddWord       ='�������'
        subModuleName = 'TTPS001_032111'
        subModuleHandle=__import__( subModuleName )
        AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
        if not subModuleHandle.SubModuleMainFst( ) :
            UpdateBatchAdm('1','','����ʧ��:���Ͷ��˻�ִʧ��')
            return False
        if not UpdateBatchAdm('5','0000','���ж��˻�ִ�������') :
            return TipsFunc.ExitThisFlow( 'A0001', '��������״̬ʧ��!' )
   
        #�������
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='���׳ɹ�'
        
        AfaLoggerFunc.tradeInfo('��˰����_���˴������[TTPS001_8450041]' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))

#��������״̬
def UpdateBatchAdm(status,errorCode,errMsg):
    AfaLoggerFunc.tradeInfo('>>>��������״̬['+status+']'+errorCode+errMsg)
    sqlStr = "UPDATE TIPS_CHECKADM SET DEALSTATUS='"+status+"',errorcode='"+errorCode+"',ERRORMSG='"+errMsg+"'"
    sqlStr =sqlStr +" WHERE  workDate  = '" + TradeContext.chkDate         + "'"
    sqlStr =sqlStr +" AND BATCHNO = '"      + TradeContext.chkAcctOrd      + "'"
    sqlStr =sqlStr +" AND PAYBKCODE ='"     + TradeContext.payBkCode.strip()  + "'"
    sqlStr =sqlStr +" AND PAYEEBANKNO ='"   + TradeContext.payeeBankNo.strip()    + "'"   
    AfaLoggerFunc.tradeInfo(sqlStr )
    records=AfaDBFunc.UpdateSqlCmt( sqlStr )
    if( records <0 ):
        return TipsFunc.ExitThisFlow( 'A0027', '���ݿ����' )
    return True

#��������  ���ж˱�TIPS�����ˮ
def rev_proc():
    #��ѯ��Ҫ��������ϸ
    AfaLoggerFunc.tradeInfo('>>>��ѯ��Ҫ��������ϸ')
    sql_m="select taxpaycode,amount,serialno,zoneno,brno,tellerno,bankstatus,corpstatus from tips_maintransdtl "
    sql_m=sql_m+" where corpTime='"+TradeContext.chkDate +"' and  revtranf='0' and bankstatus='0' and corpchkflag='9' "
    sql_m=sql_m+" and note3='"+TradeContext.payBkCode.strip()+"' and note4='"+TradeContext.payeeBankNo.strip()+"'"
    AfaLoggerFunc.tradeInfo(sql_m)
    records_m=AfaDBFunc.SelectSql(sql_m)
    if records_m==None:
        return TipsFunc.ExitThisFlow( 'A0027', '���ݿ��쳣' )
    elif(len(records_m)==0):
        AfaLoggerFunc.tradeInfo('>>>û����Ҫ��������ϸ')
        return True
    else:
        records_m=UtilTools.ListFilterNone( records_m )
        for i in range(0,len(records_m)):
            TradeContext.taxPayCode     =records_m[i][0]   #�û���
            TradeContext.amount         =records_m[i][1]   #���
            TradeContext.preAgentSerno  =records_m[i][2]   #ԭ������ˮ��
            TradeContext.zoneno         =records_m[i][3]    
            TradeContext.brno           =records_m[i][4]    
            TradeContext.teller         =records_m[i][5] 
            
            TradeContext.channelCode = '007'
            TradeContext.workDate = TradeContext.chkDate
            TradeContext.workTime = UtilTools.GetSysTime( )
            TradeContext.appNo      ='AG2010'
            TradeContext.busiNo     ='00000000000001'
            
            TradeContext.TransCode = '8450041'
            
            #============У�鹫���ڵ����Ч��==================
            if ( not TipsFunc.Cancel_ChkVariableExist( ) ):
                raise TipsFunc.flowException( )
            
            #=============�ж�Ӧ��״̬====================
            #if( not TipsFunc.ChkAppStatus( ) ):
            #    raise TipsFunc.flowException( )
            
            #=============�жϷ����������Ƿ�ƥ��ԭ����====================
            if( not TipsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
                raise TipsFunc.flowException( )
            
            #=============��ȡƽ̨��ˮ��====================
            if( not TipsFunc.GetSerialno( ) ):
                raise TipsFunc.flowException( )
            
            #=============������ˮ��====================
            if( not TipsFunc.InsertDtl( ) ):
                raise TipsFunc.flowException( )
            
            #=============������ͨѶ====================
            TipsFunc.CommHost( )
            
            errorCode=TradeContext.errorCode
            if TradeContext.errorCode=='SXR0010' :  #ԭ���������ѳ��������ɳɹ�����
                TradeContext.__status__='0'
                TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
            
            #=============���½�����ˮ====================
            if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
                if errorCode == '0000':
                    TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                raise TipsFunc.flowException( )
                
            #===== add by liu.yl at 2011/5/17 ====
            #===== ��������ԭ����״̬Ϊ3-���� ====
            if TradeContext.errorCode == '0000':
                sql_u = "update tips_maintransdtl set bankstatus='3', errormsg='���ж��˳����ɹ�' "
                sql_u = sql_u + " where corpTime='" + TradeContext.chkDate
                sql_u = sql_u + "' and serialno='" + TradeContext.preAgentSerno               #ԭ������ˮ��
                sql_u = sql_u + "' and note3='"+TradeContext.payBkCode.strip()
                sql_u = sql_u + "' and note4='"+TradeContext.payeeBankNo.strip()+"'"
                
                rec = AfaDBFunc.UpdateSqlCmt(sql_u)
                if rec < 0:
                    TipsFunc.WrtLog(sql_u)
                    TradeContext.errorCode, TradeContext.errorMsg = "S999",'���ݿ��쳣'
                    TipsFunc.exitMainFlow()
                AfaLoggerFunc.tradeInfo('>>>������ˮ��:' + TradeContext.preAgentSerno + '�����ɹ�')
    return True