# -*- coding: gbk -*-
################################################################################
#   ����ҵ��.ͨ��ģ��
#===============================================================================
#   ģ���ļ�:   ABS001.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc

from types import *


def main( ):


    AfaLoggerFunc.tradeInfo('********abs.ͨ��ģ�����********')


    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]

       
        #=====================��ȡϵͳ����ʱ��==================================
        TradeContext.TranDate=AfaUtilTools.GetSysDate( )
        TradeContext.TranTime=AfaUtilTools.GetSysTime( )


        #=====================��̬���ؽ��׽ű�==================================
        trxModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            trxModuleHandle=__import__( trxModuleName )


        except Exception, e:
            AfaLoggerFunc.tradeInfo(e)
            raise AfaFlowControl.flowException( 'A0001', '���ؽ��׽ű�ʧ�ܻ��׽ű�������' )


        #=====================����ҵ����Ի�����================================
        if not trxModuleHandle.TrxMain( ) :
            raise AfaFlowControl.accException( )


        #=====================�Զ����==========================================
        AfaFunc.autoPackData()


        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('********����ҵ��.ͨ��ģ��['+TradeContext.TemplateCode+']�˳�********')


    except AfaFlowControl.flowException, e:
        #�����쳣
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #�����쳣
        AfaFunc.autoPackData()

    except Exception, e:
        #Ĭ���쳣
        AfaFlowControl.exitMainFlow( str( e ) )
