# -*- coding: gbk -*-
################################################################################
#  ��̨����-����ѯ�˻�ά��.��ѯģ��
#===============================================================================
#   ģ���ļ�:   TFTCZ001.py
#   �޸�ʱ��:   2012-09-17
#   ��    ��:   �º�
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******��̨����-����ѯ�˻�ά��ģ��['+TradeContext.TemplateCode+']����******')
    
    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]
                
        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

       # #=====================�ж�Ӧ��ϵͳ״̬==================================
       # if not AfaFunc.ChkSysStatus( ) :
       #     raise AfaFlowControl.flowException( )             
       #         
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
       
        
        #=====================�Զ����==========================================
        AfaFunc.autoPackData()
        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('************��̨����-����ѯ�˻�ά��ģ��['+TradeContext.TemplateCode+']�˳�******')


    except AfaFlowControl.flowException, e:
        #AfaFlowControl.exitMainFlow( str(e) )
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        #AfaFlowControl.exitMainFlow( str(e) )
        AfaFlowControl.exitMainFlow( )        
