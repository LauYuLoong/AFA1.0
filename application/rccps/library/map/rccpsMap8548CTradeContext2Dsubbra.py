# -*- coding: gbk -*-
##################################################################
#   农信银系统 TradeContext 字典到 subbra 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap8548CTradeContext2Dsubbra.py
#   修改时间:   Tue Jun 24 16:13:38 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BRNO'):
        to_dict['BESBNO'] = TradeContext.BRNO
        AfaLoggerFunc.tradeDebug('subbra[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRNO不存在")

    if TradeContext.existVariable('BRNM'):
        to_dict['BESBNM'] = TradeContext.BRNM
        AfaLoggerFunc.tradeDebug('subbra[BESBNM] = ' + str(to_dict['BESBNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRNM不存在")

    if TradeContext.existVariable('BESBTP'):
        to_dict['BESBTP'] = TradeContext.BESBTP
        AfaLoggerFunc.tradeDebug('subbra[BESBTP] = ' + str(to_dict['BESBTP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBTP不存在")

    if TradeContext.existVariable('BTOPSB'):
        to_dict['BTOPSB'] = TradeContext.BTOPSB
        AfaLoggerFunc.tradeDebug('subbra[BTOPSB] = ' + str(to_dict['BTOPSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BTOPSB不存在")

    if TradeContext.existVariable('BEACSB'):
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('subbra[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB不存在")

    if TradeContext.existVariable('BANKBIN'):
        to_dict['BANKBIN'] = TradeContext.BANKBIN
        AfaLoggerFunc.tradeDebug('subbra[BANKBIN] = ' + str(to_dict['BANKBIN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BANKBIN不存在")

    if TradeContext.existVariable('STRINFO'):
        to_dict['STRINFO'] = TradeContext.STRINFO
        AfaLoggerFunc.tradeDebug('subbra[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.STRINFO不存在")

    if TradeContext.existVariable('SUBFLG'):
        to_dict['SUBFLG'] = TradeContext.SUBFLG
        AfaLoggerFunc.tradeDebug('subbra[SUBFLG] = ' + str(to_dict['SUBFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SUBFLG不存在")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('subbra[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1不存在")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('subbra[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2不存在")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('subbra[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3不存在")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('subbra[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4不存在")

    return True

