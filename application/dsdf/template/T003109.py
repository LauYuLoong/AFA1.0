# -*- coding: gbk -*-
################################################################################
#   ���մ���.Ȩ�޼��ģ��
#===============================================================================
#   ģ���ļ�:   003109.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.Ȩ�޼��ģ��[' + TradeContext.TemplateCode + ']����******')
    
    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]


        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================����ӿ�(ǰ����)==================================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )

        except Exception, e:
            AfaLoggerFunc.tradeInfo( e )

        else:
            AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )


        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
            
            
        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )


        #=====================�жϽ���״̬======================================
        if not AfaFunc.ChkTradeStatus( ) :
            raise AfaFlowControl.flowException( )
 
 
        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd():
                raise AfaFlowControl.flowException( )
                
                
        #=====================�Զ����==========================================
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '���׳ɹ�'
        AfaFunc.autoPackData()

        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.Ȩ�޼��ģ��[' + TradeContext.TemplateCode + ']�˳�******')
        
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
