# -*- coding: gbk -*-
################################################################################
#   ����ҵ��.ͨ��ģ��
#===============================================================================
#   ģ���ļ�:   AHXNB002.py
#   �޸�ʱ��:   2010-12-15
################################################################################
import TradeContext

TradeContext.sysType = "ahxnb"

import AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc

from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('********����ʡ��ũ��.����ģ��['+TradeContext.TemplateCode+']����********')

    try:
    
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]

       
        #=====================��ȡϵͳ����ʱ��==================================
        TradeContext.WorkDate=AfaUtilTools.GetSysDate( )
        TradeContext.WorkTime=AfaUtilTools.GetSysTime( )
        
        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )


        #=====================��̬���ؽ��׽ű�==================================
        trxModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            trxModuleHandle=__import__( trxModuleName )

        except Exception, e:
            AfaLoggerFunc.tradeInfo(e)
            raise AfaFlowControl.flowException( 'A0001', '���ؽ��׽ű�ʧ�ܻ��׽ű�������' )


        #=====================������ũ��ҵ����Ի�����==========================
        if not trxModuleHandle.TrxMain( ) :
            raise AfaFlowControl.flowException( TradeContext.errorCode, TradeContext.errorMsg)


        #=====================�Զ����==========================================
        AfaFunc.autoPackData()


        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('********����ʡ��ũ��.����ģ��['+TradeContext.TemplateCode+']�˳�********')


    except AfaFlowControl.flowException, e:
        #�����쳣
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #�����쳣
        AfaFunc.autoPackData()

    except Exception, e:
        #Ĭ���쳣
        AfaFlowControl.exitMainFlow( str( e ) )
        

