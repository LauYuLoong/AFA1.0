# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ subbra �ֵ䵽 TradeContext �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8549Dsubbra2CTradeContext.py
#   �޸�ʱ��:   Tue Jun 24 16:14:01 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BESBNO'):
        TradeContext.BRNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BRNO = ' + str(TradeContext.BRNO))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BESBNO']������")

    if from_dict.has_key('BESBNM'):
        TradeContext.BRNM = from_dict['BESBNM']
        AfaLoggerFunc.tradeDebug('TradeContext.BRNM = ' + str(TradeContext.BRNM))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BESBNM']������")

    if from_dict.has_key('BESBTP'):
        TradeContext.BESBTP = from_dict['BESBTP']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBTP = ' + str(TradeContext.BESBTP))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BESBTP']������")

    if from_dict.has_key('BTOPSB'):
        TradeContext.BTOPSB = from_dict['BTOPSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BTOPSB = ' + str(TradeContext.BTOPSB))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BTOPSB']������")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BEACSB']������")

    if from_dict.has_key('BANKBIN'):
        TradeContext.BANKBIN = from_dict['BANKBIN']
        AfaLoggerFunc.tradeDebug('TradeContext.BANKBIN = ' + str(TradeContext.BANKBIN))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BANKBIN']������")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("subbra['STRINFO']������")

    if from_dict.has_key('SUBFLG'):
        TradeContext.SUBFLG = from_dict['SUBFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.SUBFLG = ' + str(TradeContext.SUBFLG))
    else:
        AfaLoggerFunc.tradeDebug("subbra['SUBFLG']������")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("subbra['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("subbra['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("subbra['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("subbra['NOTE4']������")

    return True

