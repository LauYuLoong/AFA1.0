# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��ģ��.
#=================================================================
#   �����ļ�:   3001.py
#   �޸�ʱ��:   2007-10-15 
##################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc
from types import *

def main( ):
    
    AfaLoggerFunc.tradeInfo('=======��˰����ģ�忪ʼ=======')

    try:
        #=============��ʼ�����ر��ı���====================
        TradeContext.tradeResponse=[]
        
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #begin 20100625 �������޸�
        #TradeContext.sysId       = "AG2008"
        TradeContext.sysId       = TradeContext.appNo
        #end

        TradeContext.agentFlag   = "01"
        TradeContext.__respFlag__='0'

        #=============����ӿ�1====================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
                
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
            
        else:
            AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleMainFst( ) :
                raise AfaFlowControl.flowException( )
        
        #=============�Զ����====================
        AfaFunc.autoPackData()

        AfaLoggerFunc.tradeInfo('=======��˰����ģ�����=======')
        
    except AfaFlowControl.flowException, e:
        #�����쳣
        AfaFlowControl.exitMainFlow( )

    except AfaFlowControl.accException:
        #�����쳣
        AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        #Ĭ���쳣
        AfaFlowControl.exitMainFlow( str( e ) )
