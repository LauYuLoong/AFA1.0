# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 pjcbka_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap1125DTradeContext2Dpjcbka_dict.py
#   �޸�ʱ��:   Mon Jun 23 09:08:34 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('workDate'):
        to_dict['BJEDTE'] = from_dict['workDate']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['workDate']������")
        return False

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BSPSQN']������")
        return False

    if from_dict.has_key('BRSFLG'):
        to_dict['BRSFLG'] = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BRSFLG']������")
        return False

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BESBNO']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BEAUUS']������")

    if from_dict.has_key('NCCworkDate'):
        to_dict['NCCWKDAT'] = from_dict['NCCworkDate']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['NCCworkDate']������")

    if from_dict.has_key('TRCCO'):
        to_dict['TRCCO'] = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['TRCCO']������")

    if from_dict.has_key('TRCDAT'):
        to_dict['TRCDAT'] = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        to_dict['TRCNO'] = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['TRCNO']������")

    if from_dict.has_key('SNDBNKCO'):
        to_dict['SNDBNKCO'] = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        to_dict['SNDBNKNM'] = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        to_dict['RCVBNKCO'] = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        to_dict['RCVBNKNM'] = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['RCVBNKNM']������")

    if from_dict.has_key('BOJEDT'):
        to_dict['BOJEDT'] = from_dict['BOJEDT']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BOJEDT']������")

    if from_dict.has_key('BOSPSQ'):
        to_dict['BOSPSQ'] = from_dict['BOSPSQ']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BOSPSQ']������")

    if from_dict.has_key('ORTRCCO'):
        to_dict['ORTRCCO'] = from_dict['ORTRCCO']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['ORTRCCO']������")

    if from_dict.has_key('BILDAT'):
        to_dict['BILDAT'] = from_dict['BILDAT']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BILDAT] = ' + str(to_dict['BILDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BILDAT']������")

    if from_dict.has_key('BILNO'):
        to_dict['BILNO'] = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BILNO']������")

    if from_dict.has_key('BilPNam'):
        to_dict['BilPNam'] = from_dict['BilPNam']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BilPNam] = ' + str(to_dict['BilPNam']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BilPNam']������")

    if from_dict.has_key('BilEndDt'):
        to_dict['BilEndDt'] = from_dict['BilEndDt']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BilEndDt] = ' + str(to_dict['BilEndDt']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BilEndDt']������")

    if from_dict.has_key('BILAMT'):
        to_dict['BILAMT'] = from_dict['BILAMT']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BILAMT] = ' + str(to_dict['BILAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['BILAMT']������")

    if from_dict.has_key('PYENAM'):
        to_dict['PYENAM'] = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[PYENAM] = ' + str(to_dict['PYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['PYENAM']������")

    if from_dict.has_key('HonBnkNm'):
        to_dict['HonBnkNm'] = from_dict['HonBnkNm']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[HonBnkNm] = ' + str(to_dict['HonBnkNm']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['HonBnkNm']������")

    if from_dict.has_key('CONT'):
        to_dict['CONT'] = from_dict['CONT']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[CONT] = ' + str(to_dict['CONT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['CONT']������")

    if from_dict.has_key('ISDEAL'):
        to_dict['ISDEAL'] = from_dict['ISDEAL']
        AfaLoggerFunc.tradeDebug('pjcbka_dict[ISDEAL] = ' + str(to_dict['ISDEAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext['ISDEAL']������")
        return False

    return True

