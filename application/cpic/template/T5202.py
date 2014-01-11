# -*- coding: gbk -*-
################################################################################
#   ���մ���.ģ��2.�ɷ�ģ��(1.���� 2.��ҵ)
#===============================================================================
#   ģ���ļ�:   004202.py
#   �޸�ʱ��:   2006-04-06
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaAfeFunc,AfaFlowControl,TransBillFunc,AfaTransDtlFunc,Party3Context,AfaHostFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******̫���ɷ�ģ��['+TradeContext.TemplateCode+']����******')
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
                
        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================У�鹫���ڵ����Ч��==============================
        if( not AfaFunc.Pay_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )
            
        #=====================�жϵ�λ״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================�жϽ���״̬==================================
        if not AfaFunc.ChkActStatus( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================��ȡƽ̨��ˮ��====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
            
        #=====================������ˮ��========================================
        if not AfaTransDtlFunc.InsertDtl( ) :
            raise AfaFlowControl.flowException( )
            
        #=====================������ͨѶ========================================
        
        AfaHostFunc.CommHost()
        
        #TradeContext.__status__, TradeContext.errorCode, TradeContext.errorMsg, TradeContext.bankCode = '0','0000', '�����ɹ�','0'
        
        #=====================������������״̬==================================
        if( not AfaTransDtlFunc.UpdateDtl( 'BANK' ) ):
            if( TradeContext.__status__=='2' ):
                TradeContext.accMsg = TradeContext.errorMsg
                raise AfaFlowControl.accException( )
            raise AfaFlowControl.flowException( )
        AfaLoggerFunc.tradeInfo("���½���״̬���")
        #=====================����ӿ�(�д���)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd( ) :
                raise AfaFlowControl.flowException( )

        #=====================��ͨѶǰ�ý���====================================
        
        AfaAfeFunc.CommAfe()
        
        #=====================���µ���������״̬================================
        if( not AfaTransDtlFunc.UpdateDtl( 'CORP' ) ):
            if( TradeContext.__status__=='2' and TradeContext.__autoRevTranCtl__=='2' ):
                raise AfaFlowControl.flowException( )
            else:
                TradeContext.accMsg = TradeContext.errorMsg
                raise AfaFlowControl.accException( )

        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoTrd():
                if( TradeContext.__status__=='2' and TradeContext.__autoRevTranCtl__=='2' ):
                    raise AfaFlowControl.flowException( )
                else:
                    TradeContext.accMsg = TradeContext.errorMsg
                    raise AfaFlowControl.accException( )
        
        #=====================��Ʊ��Ϣ����======================================
        if TradeContext.errorCode=='0000' and TradeContext.existVariable( "billData" ):
            if not ( TransBillFunc.InsertBill( TradeContext.billData ) ) :
                raise AfaFlowControl.flowException( )

        #=====================�Զ����==========================================
        
        AfaFunc.autoPackData()
        
        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******̫���ɷ�ģ��['+TradeContext.TemplateCode+']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException,e:
    
        AfaLoggerFunc.tradeInfo('�Զ�����')

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
            AfaFlowControl.exitMainFlow( )
        else:
            AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
