# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 hdcbka_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap1129CTradeContext2Dhdcbka_dict.py
#   �޸�ʱ��:   Sat Jul 26 18:20:00 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BJEDTE������")
        return False

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BSPSQN������")
        return False

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRSFLG������")
        return False

    if TradeContext.existVariable('BESBNO'):
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBNO������")

    if TradeContext.existVariable('BETELR'):
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BETELR������")

    if TradeContext.existVariable('BEAUUS'):
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS������")

    if TradeContext.existVariable('NCCWKDAT'):
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('hdcbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCWKDAT������")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('hdcbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT������")

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO������")

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO������")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO������")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO������")

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('hdcbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM������")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('hdcbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM������")

    if TradeContext.existVariable('BOJEDT'):
        to_dict['BOJEDT'] = TradeContext.BOJEDT
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOJEDT������")

    if TradeContext.existVariable('BOSPSQ'):
        to_dict['BOSPSQ'] = TradeContext.BOSPSQ
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOSPSQ������")

    if TradeContext.existVariable('ORTRCCO'):
        to_dict['ORTRCCO'] = TradeContext.ORTRCCO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCCO������")

    if TradeContext.existVariable('CUR'):
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('hdcbka_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR������")

    if TradeContext.existVariable('OCCAMT'):
        to_dict['OCCAMT'] = TradeContext.OCCAMT
        AfaLoggerFunc.tradeDebug('hdcbka_dict[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OCCAMT������")

    if TradeContext.existVariable('CONT'):
        to_dict['CONT'] = TradeContext.CONT
        AfaLoggerFunc.tradeDebug('hdcbka_dict[CONT] = ' + str(to_dict['CONT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CONT������")

    if TradeContext.existVariable('PYRACC'):
        to_dict['PYRACC'] = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug('hdcbka_dict[PYRACC] = ' + str(to_dict['PYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRACC������")

    if TradeContext.existVariable('PYRNAM'):
        to_dict['PYRNAM'] = TradeContext.PYRNAM
        AfaLoggerFunc.tradeDebug('hdcbka_dict[PYRNAM] = ' + str(to_dict['PYRNAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRNAM������")

    if TradeContext.existVariable('PYEACC'):
        to_dict['PYEACC'] = TradeContext.PYEACC
        AfaLoggerFunc.tradeDebug('hdcbka_dict[PYEACC] = ' + str(to_dict['PYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYEACC������")

    if TradeContext.existVariable('PYENAM'):
        to_dict['PYENAM'] = TradeContext.PYENAM
        AfaLoggerFunc.tradeDebug('hdcbka_dict[PYENAM] = ' + str(to_dict['PYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYENAM������")

    if TradeContext.existVariable('ISDEAL'):
        to_dict['ISDEAL'] = TradeContext.ISDEAL
        AfaLoggerFunc.tradeDebug('hdcbka_dict[ISDEAL] = ' + str(to_dict['ISDEAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ISDEAL������")
        return False

    if TradeContext.existVariable('PRCCO'):
        to_dict['PRCCO'] = TradeContext.PRCCO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PRCCO������")

    if TradeContext.existVariable('STRINFO'):
        to_dict['STRINFO'] = TradeContext.STRINFO
        AfaLoggerFunc.tradeDebug('hdcbka_dict[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.STRINFO������")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('hdcbka_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1������")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('hdcbka_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2������")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('hdcbka_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3������")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('hdcbka_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4������")

    return True

