# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ trcbka_dict �ֵ䵽 ztcbka_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8529Dtrcbka_dict2Dztcbka_dict.py
#   �޸�ʱ��:   Wed Jul  2 11:35:49 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BSPSQN']������")

    if from_dict.has_key('BRSFLG'):
        to_dict['BRSFLG'] = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BRSFLG']������")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        to_dict['BEACSB'] = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BEACSB']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BEAUUS']������")

    if from_dict.has_key('NCCWKDAT'):
        to_dict['NCCWKDAT'] = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['NCCWKDAT']������")

    if from_dict.has_key('TRCCO'):
        to_dict['TRCCO'] = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['TRCCO']������")

    if from_dict.has_key('TRCDAT'):
        to_dict['TRCDAT'] = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        to_dict['TRCNO'] = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['TRCNO']������")

    if from_dict.has_key('SNDBNKCO'):
        to_dict['SNDBNKCO'] = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        to_dict['SNDBNKNM'] = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        to_dict['RCVBNKCO'] = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        to_dict['RCVBNKNM'] = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['RCVBNKNM']������")

    if from_dict.has_key('BOJEDT'):
        to_dict['BOJEDT'] = from_dict['BOJEDT']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BOJEDT']������")

    if from_dict.has_key('BOSPSQ'):
        to_dict['BOSPSQ'] = from_dict['BOSPSQ']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['BOSPSQ']������")

    if from_dict.has_key('ORTRCCO'):
        to_dict['ORTRCCO'] = from_dict['ORTRCCO']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['ORTRCCO']������")

    if from_dict.has_key('CUR'):
        to_dict['CUR'] = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['CUR']������")

    if from_dict.has_key('OCCAMT'):
        to_dict['OCCAMT'] = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['OCCAMT']������")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('ztcbka_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("trcbka_dict['NOTE4']������")

    return True

