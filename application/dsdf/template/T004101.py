# -*- coding: gbk -*-
################################################################################
#   ���մ���.ģ��1.��ѯģ��
#===============================================================================
#   ģ���ļ�:   004101.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.ģ��1.��ѯģ��['+TradeContext.TemplateCode+']����******')

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
            AfaLoggerFunc.tradeInfo( e)
            
        else:
            AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )


        #=====================У�鹫���ڵ����Ч��==============================
        if( not AfaFunc.Query_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )
                    
        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
        
        
        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd():
                raise AfaFlowControl.flowException( )
        
        #=============�Զ����====================
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '���׳ɹ�'
        
        AfaFunc.autoPackData()

        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.ģ��1.��ѯģ��['+TradeContext.TemplateCode+']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
