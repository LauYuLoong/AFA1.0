# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��˰���к�������.����ɷѳ���
#=================================================================
#   �����ļ�:   TPS001_8454.py
#   �޸�ʱ��:   2007-10-23
##################################################################

import TradeContext, UtilTools, AfaFlowControl
#, os, AfaLoggerFunc��LoggerHandler, 
import AfaAfeFunc,TipsFunc

def SubModuleMainFst( ):
    TradeContext.appNo  =   'AG2010'
    TradeContext.busiNo =   '00000000000001'
    TradeContext.__agentEigen__='0'
    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]
        
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate = UtilTools.GetSysDate( )
        TradeContext.workTime = UtilTools.GetSysTime( )

        #============У�鹫���ڵ����Ч��==================
        if ( not TipsFunc.Cancel_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        #=============�ж�Ӧ��״̬====================
        if( not TipsFunc.ChkAppStatus( ) ):
            raise AfaFlowControl.flowException( )
        
        ##������ջ��أ���ȡ������Ϣ
        #if not TipsFunc.ChkTaxOrgCode():
        #    return False
        
        #=============�жϷ����������Ƿ�ƥ��ԭ����====================
        if( not TipsFunc.ChkRevInfo( TradeContext.preAgentSerno ) ):
            raise AfaFlowControl.flowException( )
        
        #=============��ȡƽ̨��ˮ��====================
        if( not TipsFunc.GetSerialno( ) ):
            raise AfaFlowControl.flowException( )

        #=============������ˮ��====================
        if( not TipsFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )

        #=============�������ͨѶ====================
        AfaAfeFunc.CommAfe( )

        #=============���½�����ˮ====================
        if( not TipsFunc.UpdateDtl( 'CORP' ) ):
            raise AfaFlowControl.flowException( )

        #=============������ͨѶ====================
        TipsFunc.CommHost( )
        #TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
        #TradeContext.bankSerno = '10000000'        #��Ա��ˮ��
        #TradeContext.bankCode  = 'AAAAAAA'        #�������ش���
        #TradeContext.__status__='0'
        
        errorCode=TradeContext.errorCode

        #=============���½�����ˮ====================
        if( not TipsFunc.UpdateDtl( 'BANK' ) ):
            if errorCode == '0000':
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
            raise AfaFlowControl.flowException( )

        #=============���·�Ʊ��ϢΪ����====================
        if( not TransBillFunc.UpdateBill( ) ):
            TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
            raise AfaFlowControl.flowException( )

    except AfaFlowControl.flowException, e:
        return False
    except Exception, e:
        return AfaFlowControl.ExitThisFlow('A9999','ϵͳ�쳣'+str(e) )
    return True
 
def SubModuleMainSnd ():
    return True
