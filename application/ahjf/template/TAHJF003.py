# -*- coding: gbk -*-
################################################################################
#   ���ս���.����ģ��.��ȥ������.�ٳ�����
#===============================================================================
#   ģ���ļ�:   TAHJF003.py
#   �޸�ʱ��:   2010-08-18
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaTransDtlFunc,AfaAfeFunc,AfaFlowControl,AfaHostFunc,TransBillFunc,AhjfAdminFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******���ս�������ģ��['+TradeContext.TemplateCode+']����******')
    try:

        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]

        #��ȡ��ǰϵͳʱ��
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
                
        #=====================����ӿ�(ǰ����)==================================
        subModuleExistFlag = 0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
        else:
            AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )
                

        #=====================У�鹫���ڵ����Ч��==============================
        if( not AfaFunc.Cancel_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )

        #=====================�жϵ�λ״̬======================================
        if not AhjfAdminFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )

        #=====================�жϷ����������Ƿ�ƥ��ԭ����======================
        if( not AfaFunc.ChkRevInfo( ) ):
            raise AfaFlowControl.flowException( )

        #=====================��ȡƽ̨��ˮ��====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
            
        TradeContext.subUnitno =  "000000"
        TradeContext.__agentEigen__ = "00000000"
        TradeContext.unitno    = "0001"
        TradeContext.__respFlag__='0'

        #=====================������ˮ��========================================
        if( not AfaTransDtlFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )

        #=====================�������ͨ����====================================
        AfaAfeFunc.CommAfe( )
        #TradeContext.__status__, TradeContext.errorCode, TradeContext.errorMsg, TradeContext.bankCode = '0','0000', '�������ɹ�','0'

        #=====================����ӿ�(�д���)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd( ) :
                raise AfaFlowControl.flowException( )
      
        #=====================���½�����ˮ======================================
        if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
            raise AfaFlowControl.flowException( )

        #=====================����������========================================
        AfaHostFunc.CommHost()
        #TradeContext.__status__, TradeContext.errorCode, TradeContext.errorMsg, TradeContext.bankCode = '0','0000', '�����ɹ�','0'


        #=====================���½�����ˮ======================================
        if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
            if TradeContext.errorCode == '0000':
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                
            raise AfaFlowControl.flowException( )

        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoTrd():
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                
                raise AfaFlowControl.flowException( )

        #=====================�Զ����==========================================
        AfaFunc.autoPackData()

        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******���ս�������ģ��['+TradeContext.TemplateCode+']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
