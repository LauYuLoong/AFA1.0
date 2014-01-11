# -*- coding: gbk -*-
################################################################################
#   ���մ���.��������ģ��
#===============================================================================
#   ģ���ļ�:   003108.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.��������ģ��[' + TradeContext.TemplateCode + ']����******')

    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]


        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        
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

        if ( not TradeContext.existVariable( "procType" ) ) :
            return AfaFlowControl.ExitThisFlow( 'A0001', '��������[procType]ֵ������,����ʧ��' )


        if TradeContext.procType == '1' :
            #���������ֵ�
            if not DownLoadBaseParam( ) :
                return AfaFlowControl.ExitThisFlow( 'A0001', '���������ֵ�ʧ��' )

        if TradeContext.procType == '2' :
            #����ҵ�����
            if not DownLoadAppParam( )  :
                return AfaFlowControl.ExitThisFlow( 'A0001', '����ҵ�����ʧ��' )

        if TradeContext.procType == '3' :
            #���ؽ����б�
            if not DownLoadTradeList( ) :
                return AfaFlowControl.ExitThisFlow( 'A0001', '���ؽ����б�ʧ��' )

            
        #=====================����ӿ�(����)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd():
                raise AfaFlowControl.flowException( )
                
                
        #=====================�Զ����==========================================
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '���׳ɹ�'
        AfaFunc.autoPackData()


        #=====================�����˳�==========================================
        AfaLoggerFunc.tradeInfo('******���մ���.��������ģ��[' + TradeContext.TemplateCode + ']�˳�******')
        
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )

################################################################################
def DownLoadBaseParam( ):
    AfaLoggerFunc.tradeInfo('>>>���������ֵ�')
    return True


def DownLoadAppParam( ):
    AfaLoggerFunc.tradeInfo('>>>����ҵ�����')
    return True


def DownLoadTradeList( ):
    AfaLoggerFunc.tradeInfo('>>>���ؽ����б�')
    return True
