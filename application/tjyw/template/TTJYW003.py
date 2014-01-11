  # -*- coding: gbk -*-
################################################################################
#   ����ͨ.��ѯģ��.��ȥ������,��ȥ����
#===============================================================================
#   ģ���ļ�:   YBT004.py
#   �޸�ʱ��:   2011-01-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaAfeFunc,AfaFlowControl,AfaTjFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******ͳ��ҵ�����ڲ�ѯģ��[' + TradeContext.TemplateCode + ']����******')
    try:
        
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]
        
        #��ȡ��ǰϵͳʱ��
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================�ж�Ӧ��ϵͳ״̬==================================  
            
        if not AfaFunc.ChkSysStatus( ) :                                          
            raise AfaFlowControl.flowException( ) 
        
     #20120711ע�� �޸�
     #begin
        #=====================�жϵ�λ״̬======================================
        if not AfaTjFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )
            
     #end                                    
                                                                                  
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
        #if( not AfaFunc.Query_ChkVariableExist( ) ):
        #    raise AfaFlowControl.flowException( )
        
        #=====================�ж��̻�״̬======================================
        #if not AfaFunc.ChkUnitStatus( ) :
        #    raise AfaFlowControl.flowException( )
        
        #=====================�ж�����״̬======================================
        #if not AfaFunc.ChkChannelStatus( ) :
        #    raise AfaFlowControl.flowException( )
        
        #=====================��ȡƽ̨��ˮ��====================================
        #if AfaFunc.GetSerialno( ) == -1 :
        #    raise AfaFlowControl.flowException( )
        
        TradeContext.errorCode='0000'       
        #=====================�Զ����==========================================
        AfaFunc.autoPackData()
        
        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******ͳ��ҵ�����ڲ�ѯģ��[' + TradeContext.TemplateCode + ']�˳�******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )       
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
