# -*- coding: gbk -*-
################################################################################
#   ����ͨ.�ɷ�ģ��.ֻȥ����
#===============================================================================
#   ģ���ļ�:   TZHHF001.py
#   �޸�ʱ��:   2011-01-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,TransBillFunc,AfaTransDtlFunc
import AfaTjFunc,AfaHostFunc

from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******ͳ��ҵ��ɷ�ģ��['+TradeContext.TemplateCode+']����******')
    try:
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]
        
        #��ȡ��ǰϵͳʱ��
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================�ж�Ӧ��ϵͳ״̬==================================
    
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( ) 
    
        
    #20120711�º�ע�ͣ���� 
    #begin      
        #��� 
        #=====================�жϵ�λ״̬======================================
        if not AfaTjFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )
        
        
        
        #=====================����ӿ�(����)==================================                       
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
        if( not AfaFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )
            
        #=====================�жϵ�λ״̬======================================   
    #    if not AfaFunc.ChkUnitStatus( ) :
    #        raise AfaFlowControl.flowException( )
    #
    #    #=====================�ж�����״̬======================================
    #    if not AfaFunc.ChkChannelStatus( ) :
    #        raise AfaFlowControl.flowException( )
    #        
    #    #=====================�жϽ���״̬=====================================
    #    if not AfaFunc.ChkActStatus( ) :
    #        raise AfaFlowControl.flowException( )
    
        #=====================�жϵ�λ״̬======================================
        if not AfaTjFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )
        
        #======================================================================
        TradeContext.__agentEigen__ = "00000000"
        
   #end      
        #=====================��ȡƽ̨��ˮ��====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
              
        #=====================������ˮ��========================================
        if not AfaTransDtlFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================������ͨѶ========================================
        
        AfaHostFunc.CommHost()
        
        #=====================������������״̬==================================
        if( not AfaTransDtlFunc.UpdateDtl( 'TRADE' ) ):
            if( TradeContext.__status__=='2' ):
                TradeContext.accMsg = TradeContext.errorMsg
                raise AfaFlowControl.accException( )
            raise AfaFlowControl.flowException( )
                   
        #=====================��Ʊ��Ϣ����======================================
        if TradeContext.errorCode=='0000' and TradeContext.existVariable( "billData" ):
            if not ( TransBillFunc.InsertBill( TradeContext.billData ) ) :
                raise AfaFlowControl.flowException( )
        
        TradeContext.errorCode='0000'
        #=====================�Զ����==========================================
        
        AfaFunc.autoPackData()
        
        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******ͳ��ҵ��ɷ�ģ��['+TradeContext.TemplateCode+']�˳�******')
    
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException,e:
    
        AfaLoggerFunc.tradeInfo('�����쳣��Ϣ: ' + str(e))
        AfaLoggerFunc.tradeInfo('�Զ�����')

        TradeContext.__autoRevTranCtl__ = "1"      #�����Զ�����

        #=====================�Զ�����==========================================
        if ( TradeContext.__autoRevTranCtl__=='1' or TradeContext.__autoRevTranCtl__=='2' ) :
            TradeContext.revTranF='2'
            TradeContext.preAgentSerno=TradeContext.agentSerialno

            #=====================��ȡ������ˮ��================================
            if AfaFunc.GetSerialno( ) == -1 :
                raise AfaFlowControl.exitMainFlow( )
                
            #=====================������ˮ��====================================
            if not AfaTransDtlFunc.InsertDtl( ) :
                raise AfaFlowControl.exitMainFlow( )

            #=====================������ͨѶ====================================
            AfaHostFunc.CommHost( )

            #=====================������������״̬==============================
            if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
                raise AfaFlowControl.exitMainFlow( )
                
            TradeContext.errorCode = 'A0048'
            TradeContext.errorMsg  = '[' + TradeContext.accMsg + ']����ʧ��,ϵͳ�Զ������ɹ�'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            
            AfaFlowControl.exitMainFlow( )
        else:
            AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
