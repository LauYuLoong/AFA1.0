# -*- coding: gbk -*-
################################################################################
#   ����ͨ.����ģ��.ֻ������
#===============================================================================
#   ģ���ļ�:   TZHHF003.py
#   �޸�ʱ��:   2011-01-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaTransDtlFunc,AfaFlowControl,AfaHostFunc
import AfaTjFunc,TransBillFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******ͳ��ҵ�����ģ��['+TradeContext.TemplateCode+']����******')
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

        #=====================�ж��̻�״̬======================================
   #20120706�º�ע�� 
   #begin
   #     if not AfaFunc.ChkUnitStatus( ) :
   #         raise AfaFlowControl.flowException( )

   #     #=====================�ж�����״̬======================================
   #     if not AfaFunc.ChkChannelStatus( ) :
   #         raise AfaFlowControl.flowException( )

        #=====================�жϵ�λ״̬======================================
        if not AfaTjFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )

        #======================================================================
        TradeContext.__agentEigen__ = "00000000"

    #end 
        #=====================�жϷ����������Ƿ�ƥ��ԭ����======================
        if( not AfaFunc.ChkRevInfo( ) ):
            raise AfaFlowControl.flowException( )

        #=====================��ȡƽ̨��ˮ��====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
        
        #=====================������ˮ��========================================
        if( not AfaTransDtlFunc.InsertDtl( ) ):
            raise AfaFlowControl.flowException( )        

        #=====================����������========================================
        AfaHostFunc.CommHost()

        #=====================���½�����ˮ======================================
        if( not AfaTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if TradeContext.errorCode == '0000':
                TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
                
            raise AfaFlowControl.flowException( )
        
        TradeContext.errorCode='0000'
        #=====================�Զ����==========================================
        AfaFunc.autoPackData()

        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******ͳ��ҵ�����ģ��['+TradeContext.TemplateCode+']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
