# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ECHO����ģ��(���Ļ�ִ)
#===============================================================================
#   ģ���ļ�:   TRCC007.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,TradeFunc,AfaFlowControl,os,AfaAfeFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('***ũ����ϵͳ: ECHO����ģ��['+TradeContext.TemplateCode+']����***')
    try:
        #=====================��ʼ�����ر��ı���================================
        #TradeContext.tradeResponse=[]

        TradeContext.sysId = 'RCC01'
        TradeContext.TRCCO = '9900517'
 
        #=====================������ͨѶ(��ִ)==================================
        AfaAfeFunc.CommAfe()

        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo('***ũ����ϵͳ: ECHO����ģ��['+TradeContext.TemplateCode+']�˳�***')


    except AfaFlowControl.flowException, e:
        #�����쳣
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #�����쳣
        AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        #Ĭ���쳣
        AfaFlowControl.exitMainFlow( str(e) )
