# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 jstbka_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap1146CTradeContext2Djstbka_dict.py
#   �޸�ʱ��:   Fri Dec  5 11:18:52 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('jstbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BJEDTE������")

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('jstbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BSPSQN������")

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('jstbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRSFLG������")

    if TradeContext.existVariable('BESBNO'):
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('jstbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBNO������")

    if TradeContext.existVariable('BEACSB'):
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('jstbka_dict[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB������")

    if TradeContext.existVariable('BETELR'):
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('jstbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BETELR������")

    if TradeContext.existVariable('BEAUUS'):
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('jstbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS������")

    if TradeContext.existVariable('BEAUPS'):
        to_dict['BEAUPS'] = TradeContext.BEAUPS
        AfaLoggerFunc.tradeDebug('jstbka_dict[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUPS������")

    if TradeContext.existVariable('TERMID'):
        to_dict['TERMID'] = TradeContext.TERMID
        AfaLoggerFunc.tradeDebug('jstbka_dict[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TERMID������")

    if TradeContext.existVariable('OPRNO'):
        to_dict['OPRNO'] = TradeContext.OPRNO
        AfaLoggerFunc.tradeDebug('jstbka_dict[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRNO������")

    if TradeContext.existVariable('OPRATTNO'):
        to_dict['OPRATTNO'] = TradeContext.OPRATTNO
        AfaLoggerFunc.tradeDebug('jstbka_dict[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRATTNO������")

    if TradeContext.existVariable('NCCWKDAT'):
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('jstbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCWKDAT������")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('jstbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('jstbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT������")

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('jstbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO������")

    if TradeContext.existVariable('MSGFLGNO'):
        to_dict['MSGFLGNO'] = TradeContext.MSGFLGNO
        AfaLoggerFunc.tradeDebug('jstbka_dict[MSGFLGNO] = ' + str(to_dict['MSGFLGNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.MSGFLGNO������")

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('jstbka_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO������")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('jstbka_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO������")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('jstbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO������")

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('jstbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM������")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('jstbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('jstbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM������")

    if TradeContext.existVariable('BOJEDT'):
        to_dict['BOJEDT'] = TradeContext.BOJEDT
        AfaLoggerFunc.tradeDebug('jstbka_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOJEDT������")

    if TradeContext.existVariable('BOSPSQ'):
        to_dict['BOSPSQ'] = TradeContext.BOSPSQ
        AfaLoggerFunc.tradeDebug('jstbka_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOSPSQ������")

    if TradeContext.existVariable('RESNCO'):
        to_dict['RESNCO'] = TradeContext.RESNCO
        AfaLoggerFunc.tradeDebug('jstbka_dict[RESNCO] = ' + str(to_dict['RESNCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RESNCO������")

    if TradeContext.existVariable('PRCCO'):
        to_dict['PRCCO'] = TradeContext.PRCCO
        AfaLoggerFunc.tradeDebug('jstbka_dict[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PRCCO������")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('jstbka_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1������")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('jstbka_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2������")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('jstbka_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3������")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('jstbka_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4������")

    return True

