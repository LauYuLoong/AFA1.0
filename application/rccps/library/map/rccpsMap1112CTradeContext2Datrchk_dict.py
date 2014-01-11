# -*- coding: gbk -*-
##################################################################
#   农信银系统 TradeContext 字典到 atrchk_dict 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap1112CTradeContext2Datrchk_dict.py
#   修改时间:   Sat Jun  7 16:19:49 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('atrchk_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO不存在")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('atrchk_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT不存在")
        return False

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('atrchk_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO不存在")

    if TradeContext.existVariable('ROPRTYPNO'):
        to_dict['ROPRTYPNO'] = TradeContext.ROPRTYPNO
        AfaLoggerFunc.tradeDebug('atrchk_dict[ROPRTYPNO] = ' + str(to_dict['ROPRTYPNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ROPRTYPNO不存在")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('atrchk_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO不存在")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('atrchk_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO不存在")

    if TradeContext.existVariable('CUR'):
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('atrchk_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR不存在")

    if TradeContext.existVariable('RDTCNT'):
        to_dict['RDTCNT'] = TradeContext.RDTCNT
        AfaLoggerFunc.tradeDebug('atrchk_dict[RDTCNT] = ' + str(to_dict['RDTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RDTCNT不存在")

    if TradeContext.existVariable('RDTAMT'):
        to_dict['RDTAMT'] = TradeContext.RDTAMT
        AfaLoggerFunc.tradeDebug('atrchk_dict[RDTAMT] = ' + str(to_dict['RDTAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RDTAMT不存在")

    if TradeContext.existVariable('RCTCNT'):
        to_dict['RCTCNT'] = TradeContext.RCTCNT
        AfaLoggerFunc.tradeDebug('atrchk_dict[RCTCNT] = ' + str(to_dict['RCTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCTCNT不存在")

    if TradeContext.existVariable('RCTAMT'):
        to_dict['RCTAMT'] = TradeContext.RCTAMT
        AfaLoggerFunc.tradeDebug('atrchk_dict[RCTAMT] = ' + str(to_dict['RCTAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCTAMT不存在")

    if TradeContext.existVariable('SCTCNT'):
        to_dict['SCTCNT'] = TradeContext.SCTCNT
        AfaLoggerFunc.tradeDebug('atrchk_dict[SCTCNT] = ' + str(to_dict['SCTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SCTCNT不存在")

    if TradeContext.existVariable('SCTAMT'):
        to_dict['SCTAMT'] = TradeContext.SCTAMT
        AfaLoggerFunc.tradeDebug('atrchk_dict[SCTAMT] = ' + str(to_dict['SCTAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SCTAMT不存在")

    if TradeContext.existVariable('SDTCNT'):
        to_dict['SDTCNT'] = TradeContext.SDTCNT
        AfaLoggerFunc.tradeDebug('atrchk_dict[SDTCNT] = ' + str(to_dict['SDTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SDTCNT不存在")

    if TradeContext.existVariable('SDTAMT'):
        to_dict['SDTAMT'] = TradeContext.SDTAMT
        AfaLoggerFunc.tradeDebug('atrchk_dict[SDTAMT] = ' + str(to_dict['SDTAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SDTAMT不存在")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('atrchk_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1不存在")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('atrchk_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2不存在")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('atrchk_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3不存在")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('atrchk_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4不存在")

    return True

