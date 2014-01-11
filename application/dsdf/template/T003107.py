# -*- coding: gbk -*-
################################################################################
#   ���մ���.�ͻ�ά��ģ��
#===============================================================================
#   ģ���ļ�:   003107.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc,AfaHostFunc,AfaAfeFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.�ͻ�ά��ģ��[' + TradeContext.TemplateCode + ']����******')
    
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
            AfaLoggerFunc.tradeInfo( e )

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


        #У��ͻ���Ϣ�Ϸ���(����)
        if( TradeContext.existVariable( "hostFlag" ) ):
            if ( TradeContext.hostFlag == '1' ):

                #�ж������ӿڴ����Ƿ����
                if( not TradeContext.existVariable( "hostCode" ) ):
                    return AfaFlowControl.ExitThisFlow( 'A0001', '��������[hostCode]ֵ������,����ʧ��' )

                #����������
                AfaHostFunc.CommHost(TradeContext.hostCode)

                #����ӿ�(����)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoSnd():
                        raise AfaFlowControl.flowException( )

        #У��ͻ���Ϣ�Ϸ���(��ҵ/��ѯ/ͬ��)
        if( TradeContext.existVariable( "corpFlag" ) ):
            if ( TradeContext.corpFlag == '1' ):

                #��ͨѶǰ�ý���
                AfaAfeFunc.CommAfe()

                #����ӿ�(����)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoTrd():
                        raise AfaFlowControl.flowException( )

        #�ͻ���Ϣά��
        if ( TradeContext.existVariable( "custFlag" ) and TradeContext.custFlag=='1') :
            if ( not TradeContext.existVariable( "procType" ) ) :
                return AfaFlowControl.ExitThisFlow( 'A0001', '��������[procType]ֵ������,����ʧ��' )

            if TradeContext.procType == '1' :
                #��ѯ
                QueryCustInfo( )
                
            if TradeContext.procType == '2' :
                #����
                AddCustInfo( )

            if TradeContext.procType == '3' :
                #�޸�
                UpdateCustInfo( )

            if TradeContext.procType == '4' :
                #ע��
                DeleteCustInfo( )

        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoFth():
                raise AfaFlowControl.flowException( )
                
                
        #=====================�Զ����==========================================
        AfaFunc.autoPackData()

        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.�ͻ�ά��ģ��[' + TradeContext.TemplateCode + ']�˳�******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )


################################################################################
def QueryCustInfo():
    AfaLoggerFunc.tradeInfo('>>>��ѯ�ͻ���Ϣ-Э���ѯ')
    return True
    
def AddCustInfo():
    AfaLoggerFunc.tradeInfo('>>>�����ͻ���Ϣ-�ͻ�ǩԼ')
    return True

def UpdateCustInfo():
    AfaLoggerFunc.tradeInfo('>>>�޸Ŀͻ���Ϣ-�޸�Э��')
    return True

def DeleteCustInfo():
    AfaLoggerFunc.tradeInfo('>>>ע���ͻ���Ϣ-�ͻ���Լ')
    return True
