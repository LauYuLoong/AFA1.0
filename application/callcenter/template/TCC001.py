# -*- coding: gbk -*-
################################################################################
#   ��������.ģ��1.ת��ģ��(1.����)
#===============================================================================
#   ģ���ļ�:   0001.py
#   �޸�ʱ��:   2009-03-13
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaTransDtlFunc,TransBillFunc,AfaHostFunc,AfaFlowControl
from types import *
import ccHostFunc

def main( ):

    AfaLoggerFunc.tradeInfo('******��������.ģ��1.ת��ģ��['+TradeContext.TemplateCode+']����******')
    
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
                
        #=====================����������========================================
        ccHostFunc.CommHost(TradeContext.TransCode) 


        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd():
                raise AfaFlowControl.flowException( )


        #=====================�Զ����==========================================
        AfaFunc.autoPackData()

        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******��������.ģ��1.ת��ģ��['+TradeContext.TemplateCode+']�˳�******')


    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
