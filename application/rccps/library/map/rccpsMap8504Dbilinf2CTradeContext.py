# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ bilinf �ֵ䵽 TradeContext �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8504Dbilinf2CTradeContext.py
#   �޸�ʱ��:   Wed Sep 17 14:55:23 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BILVER'):
        TradeContext.BILVER = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('TradeContext.BILVER = ' + str(TradeContext.BILVER))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['BILVER']������")

    if from_dict.has_key('BILNO'):
        TradeContext.BILNO = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BILNO = ' + str(TradeContext.BILNO))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['BILNO']������")

    if from_dict.has_key('BILRS'):
        TradeContext.BILRS = from_dict['BILRS']
        AfaLoggerFunc.tradeDebug('TradeContext.BILRS = ' + str(TradeContext.BILRS))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['BILRS']������")

    if from_dict.has_key('BILTYP'):
        TradeContext.BILTYP = from_dict['BILTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.BILTYP = ' + str(TradeContext.BILTYP))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['BILTYP']������")

    if from_dict.has_key('BILDAT'):
        TradeContext.BILDAT = from_dict['BILDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BILDAT = ' + str(TradeContext.BILDAT))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['BILDAT']������")

    if from_dict.has_key('PAYWAY'):
        TradeContext.PAYWAY = from_dict['PAYWAY']
        AfaLoggerFunc.tradeDebug('TradeContext.PAYWAY = ' + str(TradeContext.PAYWAY))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PAYWAY']������")

    if from_dict.has_key('REMBNKCO'):
        TradeContext.REMBNKCO = from_dict['REMBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.REMBNKCO = ' + str(TradeContext.REMBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['REMBNKCO']������")

    if from_dict.has_key('REMBNKNM'):
        TradeContext.REMBNKNM = from_dict['REMBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.REMBNKNM = ' + str(TradeContext.REMBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['REMBNKNM']������")

    if from_dict.has_key('PAYBNKCO'):
        TradeContext.PAYBNKCO = from_dict['PAYBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.PAYBNKCO = ' + str(TradeContext.PAYBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PAYBNKCO']������")

    if from_dict.has_key('PAYBNKNM'):
        TradeContext.PAYBNKNM = from_dict['PAYBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.PAYBNKNM = ' + str(TradeContext.PAYBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PAYBNKNM']������")

    if from_dict.has_key('PYRACC'):
        TradeContext.PYRACC = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRACC = ' + str(TradeContext.PYRACC))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYRACC']������")

    if from_dict.has_key('PYRNAM'):
        TradeContext.PYRNAM = from_dict['PYRNAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRNAM = ' + str(TradeContext.PYRNAM))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYRNAM']������")

    if from_dict.has_key('PYRADDR'):
        TradeContext.PYRADDR = from_dict['PYRADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRADDR = ' + str(TradeContext.PYRADDR))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYRADDR']������")

    if from_dict.has_key('PYEACC'):
        TradeContext.PYEACC = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEACC = ' + str(TradeContext.PYEACC))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYEACC']������")

    if from_dict.has_key('PYENAM'):
        TradeContext.PYENAM = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYENAM = ' + str(TradeContext.PYENAM))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYENAM']������")

    if from_dict.has_key('PYEADDR'):
        TradeContext.PYEADDR = from_dict['PYEADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEADDR = ' + str(TradeContext.PYEADDR))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYEADDR']������")

    if from_dict.has_key('PYHACC'):
        TradeContext.PYHACC = from_dict['PYHACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYHACC = ' + str(TradeContext.PYHACC))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYHACC']������")

    if from_dict.has_key('PYHNAM'):
        TradeContext.PYHNAM = from_dict['PYHNAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYHNAM = ' + str(TradeContext.PYHNAM))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYHNAM']������")

    if from_dict.has_key('PYHADDR'):
        TradeContext.PYHADDR = from_dict['PYHADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYHADDR = ' + str(TradeContext.PYHADDR))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYHADDR']������")

    if from_dict.has_key('PYITYP'):
        TradeContext.PYITYP = from_dict['PYITYP']
        AfaLoggerFunc.tradeDebug('TradeContext.PYITYP = ' + str(TradeContext.PYITYP))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYITYP']������")

    if from_dict.has_key('PYIACC'):
        TradeContext.PYIACC = from_dict['PYIACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYIACC = ' + str(TradeContext.PYIACC))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYIACC']������")

    if from_dict.has_key('PYINAM'):
        TradeContext.PYINAM = from_dict['PYINAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYINAM = ' + str(TradeContext.PYINAM))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['PYINAM']������")

    if from_dict.has_key('BILAMT'):
        TradeContext.BILAMT = from_dict['BILAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.BILAMT = ' + str(TradeContext.BILAMT))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['BILAMT']������")

    if from_dict.has_key('CUR'):
        TradeContext.CUR = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('TradeContext.CUR = ' + str(TradeContext.CUR))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['CUR']������")

    if from_dict.has_key('SEAL'):
        TradeContext.SEAL = from_dict['SEAL']
        AfaLoggerFunc.tradeDebug('TradeContext.SEAL = ' + str(TradeContext.SEAL))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['SEAL']������")

    if from_dict.has_key('USE'):
        TradeContext.USE = from_dict['USE']
        AfaLoggerFunc.tradeDebug('TradeContext.USE = ' + str(TradeContext.USE))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['USE']������")

    if from_dict.has_key('REMARK'):
        TradeContext.REMARK = from_dict['REMARK']
        AfaLoggerFunc.tradeDebug('TradeContext.REMARK = ' + str(TradeContext.REMARK))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['REMARK']������")

    if from_dict.has_key('HPCUSQ'):
        TradeContext.HPCUSQ = from_dict['HPCUSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.HPCUSQ = ' + str(TradeContext.HPCUSQ))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['HPCUSQ']������")

    if from_dict.has_key('HPSTAT'):
        TradeContext.HPSTAT = from_dict['HPSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.HPSTAT = ' + str(TradeContext.HPSTAT))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['HPSTAT']������")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("bilinf['NOTE4']������")

    return True

