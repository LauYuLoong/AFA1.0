# -*- coding: gbk -*-
################################################################################
#   ���մ���.���ɴ���ģ��
#===============================================================================
#   ģ���ļ�:   003106.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaHostFunc,AfaAfeFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.���ɴ���ģ��[' + TradeContext.TemplateCode + ']����******')

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

        #=====================�ж��̻�״̬======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================�ж�����״̬======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================��ȡƽ̨��ˮ��====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )


        #���ز���
        if( TradeContext.existVariable( "localFlag" ) ):
            if ( TradeContext.localFlag == '1' ):
                #����ӿ�(����)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoSnd():
                        raise AfaFlowControl.flowException( )

        #��������
        if( TradeContext.existVariable( "hostFlag" ) ):
            if ( TradeContext.hostFlag == '1' ):

                #�ж������ӿڴ����Ƿ����
                if( not TradeContext.existVariable( "hostCode" ) ):
                    return AfaFlowControl.ExitThisFlow( 'A0001', '��������[hostCode]ֵ������,����ʧ��' )

                #����������
                AfaHostFunc.CommHost(TradeContext.hostCode)

                #����ӿ�(����)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoTrd():
                        raise AfaFlowControl.flowException( )

        #��ҵ����
        if( TradeContext.existVariable( "corpFlag" ) ):
            if ( TradeContext.corpFlag == '1' ):

                #��ͨѶǰ�ý���
                AfaAfeFunc.CommAfe()

                #����ӿ�(����)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoFth():
                        raise AfaFlowControl.flowException( )


        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoFth():
                raise AfaFlowControl.flowException( )
        
        #=====================�Զ����==========================================
        AfaFunc.autoPackData()

        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.���ɴ���ģ��[' + TradeContext.TemplateCode + ']�˳�******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
