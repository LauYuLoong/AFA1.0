# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��������ϸ¼��
#===============================================================================
#   �����ļ�:   T001000_8407.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AbdtFunc
from types import *


#=====================������ϸ¼��==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********������ϸ¼��(8407)��ʼ**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��


    #�жϵ�λЭ���Ƿ���Ч
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    AfaLoggerFunc.tradeInfo('**********������ϸ¼��(8407)����**********')


    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True
