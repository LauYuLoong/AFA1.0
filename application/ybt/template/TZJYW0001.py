# -*- coding: gbk -*-
################################################################################
#   ��ѯģ��.��ȥ������,��ȥ����
#===============================================================================
#   ģ���ļ�:   001000.py
#   ԭ �� �ߣ�  LLJ
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc

from types import *


def main( ):


    AfaLoggerFunc.tradeInfo('********�м�ҵ���ѯģ��['+TradeContext.TemplateCode+']����********')


    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]

       
        #=====================��ȡϵͳ����ʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        

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
        AfaLoggerFunc.tradeInfo('********�м�ҵ���ѯģ��['+TradeContext.TemplateCode+']�˳�********')


    except AfaFlowControl.flowException, e:
        #�����쳣
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #�����쳣
        AfaFunc.autoPackData()

    except Exception, e:
        #Ĭ���쳣
        AfaFlowControl.exitMainFlow( str( e ) )
