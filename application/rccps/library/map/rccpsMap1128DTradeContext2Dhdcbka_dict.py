# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 hdcbka_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap1128DTradeContext2Dhdcbka_dict.py
#   �޸�ʱ��:   Wed Jun 25 09:57:27 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('workDate'):
        to_dict['BJEDTE'] = from_dict['workDate']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['workDate']������")
        return False

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BSPSQN']������")
        return False

    if from_dict.has_key('BRSFLG'):
        to_dict['BRSFLG'] = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BRSFLG']������")
        return False

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BESBNO']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BEAUUS']������")

    if from_dict.has_key('NCCworkDate'):
        to_dict['NCCWKDAT'] = from_dict['NCCworkDate']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['NCCworkDate']������")

    if from_dict.has_key('TRCCO'):
        to_dict['TRCCO'] = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['TRCCO']������")

    if from_dict.has_key('TRCDAT'):
        to_dict['TRCDAT'] = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        to_dict['TRCNO'] = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['TRCNO']������")

    if from_dict.has_key('SNDBNKCO'):
        to_dict['SNDBNKCO'] = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        to_dict['SNDBNKNM'] = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        to_dict['RCVBNKCO'] = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        to_dict['RCVBNKNM'] = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['RCVBNKNM']������")

    if from_dict.has_key('BOJEDT'):
        to_dict['BOJEDT'] = from_dict['BOJEDT']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BOJEDT']������")

    if from_dict.has_key('BOSPSQ'):
        to_dict['BOSPSQ'] = from_dict['BOSPSQ']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BOSPSQ']������")

    if from_dict.has_key('ORTRCCO'):
        to_dict['ORTRCCO'] = from_dict['ORTRCCO']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['ORTRCCO']������")

    if from_dict.has_key('CUR'):
        to_dict['CUR'] = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['CUR']������")

    if from_dict.has_key('OCCAMT'):
        to_dict['OCCAMT'] = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['OCCAMT']������")

    if from_dict.has_key('CONT'):
        to_dict['CONT'] = from_dict['CONT']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[CONT] = ' + str(to_dict['CONT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['CONT']������")

    if from_dict.has_key('PYRACC'):
        to_dict['PYRACC'] = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[PYRACC] = ' + str(to_dict['PYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['PYRACC']������")

    if from_dict.has_key('PYEACC'):
        to_dict['PYEACC'] = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[PYEACC] = ' + str(to_dict['PYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['PYEACC']������")

    if from_dict.has_key('ISDEAL'):
        to_dict['ISDEAL'] = from_dict['ISDEAL']
        AfaLoggerFunc.tradeDebug('hdcbka_dict[ISDEAL] = ' + str(to_dict['ISDEAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['ISDEAL']������")
        return False

    return True

