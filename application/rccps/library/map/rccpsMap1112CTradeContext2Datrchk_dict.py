# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 atrchk_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap1112CTradeContext2Datrchk_dict.py
#   �޸�ʱ��:   Sat Jun  7 16:19:49 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('atrchk_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO������")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('atrchk_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT������")
        return False

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('atrchk_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO������")

    if TradeContext.existVariable('ROPRTYPNO'):
        to_dict['ROPRTYPNO'] = TradeContext.ROPRTYPNO
        AfaLoggerFunc.tradeDebug('atrchk_dict[ROPRTYPNO] = ' + str(to_dict['ROPRTYPNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ROPRTYPNO������")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('atrchk_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('atrchk_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('CUR'):
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('atrchk_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR������")

    if TradeContext.existVariable('RDTCNT'):
        to_dict['RDTCNT'] = TradeContext.RDTCNT
        AfaLoggerFunc.tradeDebug('atrchk_dict[RDTCNT] = ' + str(to_dict['RDTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RDTCNT������")

    if TradeContext.existVariable('RDTAMT'):
        to_dict['RDTAMT'] = TradeContext.RDTAMT
        AfaLoggerFunc.tradeDebug('atrchk_dict[RDTAMT] = ' + str(to_dict['RDTAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RDTAMT������")

    if TradeContext.existVariable('RCTCNT'):
        to_dict['RCTCNT'] = TradeContext.RCTCNT
        AfaLoggerFunc.tradeDebug('atrchk_dict[RCTCNT] = ' + str(to_dict['RCTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCTCNT������")

    if TradeContext.existVariable('RCTAMT'):
        to_dict['RCTAMT'] = TradeContext.RCTAMT
        AfaLoggerFunc.tradeDebug('atrchk_dict[RCTAMT] = ' + str(to_dict['RCTAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCTAMT������")

    if TradeContext.existVariable('SCTCNT'):
        to_dict['SCTCNT'] = TradeContext.SCTCNT
        AfaLoggerFunc.tradeDebug('atrchk_dict[SCTCNT] = ' + str(to_dict['SCTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SCTCNT������")

    if TradeContext.existVariable('SCTAMT'):
        to_dict['SCTAMT'] = TradeContext.SCTAMT
        AfaLoggerFunc.tradeDebug('atrchk_dict[SCTAMT] = ' + str(to_dict['SCTAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SCTAMT������")

    if TradeContext.existVariable('SDTCNT'):
        to_dict['SDTCNT'] = TradeContext.SDTCNT
        AfaLoggerFunc.tradeDebug('atrchk_dict[SDTCNT] = ' + str(to_dict['SDTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SDTCNT������")

    if TradeContext.existVariable('SDTAMT'):
        to_dict['SDTAMT'] = TradeContext.SDTAMT
        AfaLoggerFunc.tradeDebug('atrchk_dict[SDTAMT] = ' + str(to_dict['SDTAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SDTAMT������")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('atrchk_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1������")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('atrchk_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2������")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('atrchk_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3������")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('atrchk_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4������")

    return True

