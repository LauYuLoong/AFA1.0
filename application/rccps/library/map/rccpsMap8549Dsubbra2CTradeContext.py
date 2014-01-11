# -*- coding: gbk -*-
##################################################################
#   农信银系统 subbra 字典到 TradeContext 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap8549Dsubbra2CTradeContext.py
#   修改时间:   Tue Jun 24 16:14:01 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BESBNO'):
        TradeContext.BRNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BRNO = ' + str(TradeContext.BRNO))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BESBNO']不存在")

    if from_dict.has_key('BESBNM'):
        TradeContext.BRNM = from_dict['BESBNM']
        AfaLoggerFunc.tradeDebug('TradeContext.BRNM = ' + str(TradeContext.BRNM))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BESBNM']不存在")

    if from_dict.has_key('BESBTP'):
        TradeContext.BESBTP = from_dict['BESBTP']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBTP = ' + str(TradeContext.BESBTP))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BESBTP']不存在")

    if from_dict.has_key('BTOPSB'):
        TradeContext.BTOPSB = from_dict['BTOPSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BTOPSB = ' + str(TradeContext.BTOPSB))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BTOPSB']不存在")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BEACSB']不存在")

    if from_dict.has_key('BANKBIN'):
        TradeContext.BANKBIN = from_dict['BANKBIN']
        AfaLoggerFunc.tradeDebug('TradeContext.BANKBIN = ' + str(TradeContext.BANKBIN))
    else:
        AfaLoggerFunc.tradeDebug("subbra['BANKBIN']不存在")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("subbra['STRINFO']不存在")

    if from_dict.has_key('SUBFLG'):
        TradeContext.SUBFLG = from_dict['SUBFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.SUBFLG = ' + str(TradeContext.SUBFLG))
    else:
        AfaLoggerFunc.tradeDebug("subbra['SUBFLG']不存在")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("subbra['NOTE1']不存在")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("subbra['NOTE2']不存在")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("subbra['NOTE3']不存在")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("subbra['NOTE4']不存在")

    return True

