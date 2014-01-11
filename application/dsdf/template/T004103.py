# -*- coding: gbk -*-
################################################################################
#   ���մ���.ģ��1.����ģ��
#===============================================================================
#   ģ���ļ�:   004103.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaTransDtlFunc,TransBillFunc,AfaHostFunc,AfaFlowControl
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.ģ��1.����ģ��['+TradeContext.TemplateCode+']����******')

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
        if( not AfaFunc.Cancel_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )


        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )


        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )


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
            
        #=====================���·�Ʊ��Ϣ(����)================================
        if( not TransBillFunc.UpdateBill( ) ):
            TradeContext.errorMsg='ȡ�����׳ɹ� '+TradeContext.errorMsg
            raise AfaFlowControl.flowException( )

        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd():
                raise AfaFlowControl.flowException( )

        #=====================�Զ����==========================================
        AfaFunc.autoPackData()

        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.ģ��1.����ģ��['+TradeContext.TemplateCode+']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
