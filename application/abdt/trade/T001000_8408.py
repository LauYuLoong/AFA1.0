# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��������ϸά��
#===============================================================================
#   �����ļ�:   T001000_8408.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AfaFunc,AbdtFunc
from types import *


#=====================������ϸά��==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********������ϸά��(8408)��ʼ**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��


    #�жϵ�λЭ���Ƿ���Ч
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    AfaLoggerFunc.tradeInfo('**********������ϸά��(8408)����**********')


    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True
