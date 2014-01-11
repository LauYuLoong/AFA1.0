# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.�����ʽ�����
#   ���������������������ʽ����㵽�����У�11�ң�
#=================================================================
#   �����ļ�:   TTPS001_0331112.py
#   �޸�ʱ��:   2007-8-18 13:43
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,AfaDBFunc,TipsFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('��˰����_�����ʽ����㿪ʼ[TTPS001_0331112]' )
    TradeContext.TransCode='0331112'
    try:
        #=============��ȡ��ǰϵͳʱ��====================
        #TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        TradeContext.__agentAccno__ = TradeContext.payeeAcct    #�����й��������ר����Ϊ�����˻�
        AfaLoggerFunc.tradeInfo( '������ר��:'+TradeContext.__agentAccno__)
        sqlStr = "SELECT BRNO,ACCNO FROM TIPS_BRANCH_ADM WHERE PAYBKCODE = '" + TradeContext.payBkCode.strip() + "' AND "
        sqlStr = sqlStr+" PAYEEBANKNO = '" + TradeContext.payeeBankNo.strip() + "' "
        AfaLoggerFunc.tradeInfo( sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            return TipsFunc.ExitThisFlow( 'A0002', '������Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            AfaLoggerFunc.tradeError( sqlStr )
            return TipsFunc.ExitThisFlow( 'A0003', '�޻�����Ϣ' )
        else:
            records=UtilTools.ListFilterNone( records )
            for i in range( 0, len( records ) ):
                AfaLoggerFunc.tradeInfo( 'brno:'+records[i][0] +' accno:'+records[i][1])
                #=============���㣺����������������з������Ҫ����1391��Ŀ���====================
                #ͳ����������˲�������Ϊת�˽��
                if not DoSumAmount(records[i][0]):
                    return TipsFunc.ExitThisFlow( 'A0027', '���ܷ�����ʧ��' )
                #TradeContext.amount='1'
                
                if (TradeContext.amount)>0 :
                    #���Ļ����Ƿ��Ѿ�����
                    sqlStr_qs = "SELECT COUNT(*) FROM TIPS_MAINTRANSDTL WHERE TAXPAYCODE = '-' "
                    sqlStr_qs = sqlStr_qs + "AND  DRACCNO = '"+records[i][1]+"' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE1 = '" + TradeContext.chkDate + "' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE2 = '" + TradeContext.chkAcctOrd + "' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE3 = '" + TradeContext.payBkCode.strip()   + "' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE4 = '" + TradeContext.payeeBankNo.strip() + "' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE6 = '1'" 
                    AfaLoggerFunc.tradeInfo( sqlStr_qs )
                    Records_qs = AfaDBFunc.SelectSql( sqlStr_qs )
                    if(Records_qs == None or Records_qs < 0):
                        return TipsFunc.ExitThisFlow( 'A0002', '��ˮ������쳣:'+AfaDBFunc.sqlErrMsg )
                    elif (Records_qs[0][0]==0): 
                        TradeContext.channelCode    = '009'
                        TradeContext.catrFlag       = '1'         #�ֽ�ת�˱�־
                        TradeContext.tellerno       = '999986'                   #
                        TradeContext.termId         = 'tips'
                        TradeContext.brno           = records[i][0]              #
                        TradeContext.zoneno         = TradeContext.brno[0:3]
                        TradeContext.accno          = records[i][1]              #����4401�˻���Ϊ�跽�˻�
                        TradeContext.amount         =str(TradeContext.amount)
                        AfaLoggerFunc.tradeInfo( '�跽:'+TradeContext.accno+'����:' +TradeContext.__agentAccno__)
                        TradeContext.taxPayCode     = '-'
                        TradeContext.tradeType      = 'T'                       #ת���ཻ��
                        TradeContext.taxPayName     = '������ˮ'
                        TradeContext.note1          = TradeContext.chkDate            
                        TradeContext.note2          = TradeContext.chkAcctOrd         
                        TradeContext.note3          = TradeContext.payBkCode.strip()  
                        TradeContext.note4          = TradeContext.payeeBankNo.strip()
                        TradeContext.note6          = '1'       #������ˮ
                        TradeContext.revTranF       = '0'
                        TradeContext.workTime       =UtilTools.GetSysTime( )
                        TradeContext.taxTypeNum     = '0'
                        
                        #====��ȡժҪ����=======
                        if not AfaFlowControl.GetSummaryCode():
                            return False
                        
                        #=============��ȡƽ̨��ˮ��====================
                        if TipsFunc.GetSerialno( ) == -1 :
                            AfaLoggerFunc.tradeInfo('>>>������:��ȡƽ̨��ˮ���쳣' )
                            return TipsFunc.ExitThisFlow( 'A0027', '��ȡ��ˮ��ʧ��' )
                        #
                        #=============������ˮ��====================
                        if not TipsFunc.InsertDtl( ) :
                            return TipsFunc.ExitThisFlow( 'A0027', '������ˮ��ʧ��' )
                        
                        #=============������ͨѶ====================
                        TipsFunc.CommHost()
                        
                        #=============������������״̬====================
                        TipsFunc.UpdateDtl( 'TRADE' )
                        
                        if TradeContext.errorCode!='0000':
                            AfaLoggerFunc.tradeFatal( '�������ʧ�ܣ�['+TradeContext.errorCode+']'+ TradeContext.errorMsg)
                            return False
                    else:
                        continue    #�Ѿ����㣬������һ������
        AfaLoggerFunc.tradeInfo('��˰����_�����ʽ��������[TTPS001_0331112]' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
#���ܳɹ������� 
def DoSumAmount(psSubUnitno):
    sSqlStr = "SELECT sum(cast(amount as decimal(17,2))) FROM TIPS_MAINTRANSDTL WHERE  NOTE1 ='"+TradeContext.chkDate+"'"
    sSqlStr = sSqlStr + " AND NOTE2 ='" + TradeContext.chkAcctOrd+"'"
    sSqlStr = sSqlStr + " AND NOTE3 ='" + TradeContext.payBkCode.strip()+"'"
    sSqlStr = sSqlStr + " AND NOTE4 ='" + TradeContext.payeeBankNo.strip()+"'"
    sSqlStr = sSqlStr + " AND CHKFLAG='0' AND CORPCHKFLAG='0'"
    AfaLoggerFunc.tradeInfo( sSqlStr )
    SumRecords = AfaDBFunc.SelectSql( sSqlStr )
    if(SumRecords == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return TipsFunc.ExitThisFlow( 'A0002', '��ˮ�������쳣:'+AfaDBFunc.sqlErrMsg )
    else:
        SumRecords=UtilTools.ListFilterNone( SumRecords ,'0')
        TradeContext.amount=SumRecords[0][0]
        AfaLoggerFunc.tradeInfo( '���ܻ���������'+str(TradeContext.amount) )
    return True

