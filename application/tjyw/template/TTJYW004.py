  # -*- coding: gbk -*-
################################################################################
#   ����ͨ.��ѯģ��.��ȥ������,��ȥ����
#===============================================================================
#   ģ���ļ�:   TTJYW004.py
#   �޸�ʱ��:   2012-08-20
#   ��   �ߣ�   �º�
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaAfeFunc,AfaFlowControl
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******ͳ��ҵ�����ڲ�ѯģ��[' + TradeContext.TemplateCode + ']����******')
    try:
        
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]
        
        #��ȡ��ǰϵͳʱ��
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
            
                                                                                  
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
                                                                                  
       
        #===============================================================
        TradeContext.errorCode='0000'   
            
        #=====================�Զ����==========================================
        AfaFunc.autoPackData()
        
        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******ͳ��ҵ�����ڲ�ѯģ��[' + TradeContext.TemplateCode + ']�˳�******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )       
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
