# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ Info �ֵ䵽 TradeContext �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8522DInfo2CTradeContext.py
#   �޸�ʱ��:   Fri Jul 18 16:09:56 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("Info['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("Info['BSPSQN']������")

    if from_dict.has_key('BCURSQ'):
        TradeContext.BCURSQ = from_dict['BCURSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.BCURSQ = ' + str(TradeContext.BCURSQ))
    else:
        AfaLoggerFunc.tradeDebug("Info['BCURSQ']������")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("Info['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("Info['BEACSB']������")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("Info['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("Info['BEAUUS']������")

    if from_dict.has_key('FEDT'):
        TradeContext.FEDT = from_dict['FEDT']
        AfaLoggerFunc.tradeDebug('TradeContext.FEDT = ' + str(TradeContext.FEDT))
    else:
        AfaLoggerFunc.tradeDebug("Info['FEDT']������")

    if from_dict.has_key('RBSQ'):
        TradeContext.RBSQ = from_dict['RBSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.RBSQ = ' + str(TradeContext.RBSQ))
    else:
        AfaLoggerFunc.tradeDebug("Info['RBSQ']������")

    if from_dict.has_key('TRDT'):
        TradeContext.TRDT = from_dict['TRDT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRDT = ' + str(TradeContext.TRDT))
    else:
        AfaLoggerFunc.tradeDebug("Info['TRDT']������")

    if from_dict.has_key('TLSQ'):
        TradeContext.TLSQ = from_dict['TLSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.TLSQ = ' + str(TradeContext.TLSQ))
    else:
        AfaLoggerFunc.tradeDebug("Info['TLSQ']������")

    if from_dict.has_key('SBAC'):
        TradeContext.SBAC = from_dict['SBAC']
        AfaLoggerFunc.tradeDebug('TradeContext.SBAC = ' + str(TradeContext.SBAC))
    else:
        AfaLoggerFunc.tradeDebug("Info['SBAC']������")

    if from_dict.has_key('ACNM'):
        TradeContext.ACNM = from_dict['ACNM']
        AfaLoggerFunc.tradeDebug('TradeContext.ACNM = ' + str(TradeContext.ACNM))
    else:
        AfaLoggerFunc.tradeDebug("Info['ACNM']������")

    if from_dict.has_key('RBAC'):
        TradeContext.RBAC = from_dict['RBAC']
        AfaLoggerFunc.tradeDebug('TradeContext.RBAC = ' + str(TradeContext.RBAC))
    else:
        AfaLoggerFunc.tradeDebug("Info['RBAC']������")

    if from_dict.has_key('OTNM'):
        TradeContext.OTNM = from_dict['OTNM']
        AfaLoggerFunc.tradeDebug('TradeContext.OTNM = ' + str(TradeContext.OTNM))
    else:
        AfaLoggerFunc.tradeDebug("Info['OTNM']������")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("Info['DASQ']������")

    if from_dict.has_key('MGID'):
        TradeContext.MGID = from_dict['MGID']
        AfaLoggerFunc.tradeDebug('TradeContext.MGID = ' + str(TradeContext.MGID))
    else:
        AfaLoggerFunc.tradeDebug("Info['MGID']������")

    if from_dict.has_key('PRCCO'):
        TradeContext.PRCCO = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.PRCCO = ' + str(TradeContext.PRCCO))
    else:
        AfaLoggerFunc.tradeDebug("Info['PRCCO']������")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("Info['STRINFO']������")

    if from_dict.has_key('BCSTAT'):
        TradeContext.BCSTAT = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BCSTAT = ' + str(TradeContext.BCSTAT))
    else:
        AfaLoggerFunc.tradeDebug("Info['BCSTAT']������")

    if from_dict.has_key('BDWFLG'):
        TradeContext.BDWFLG = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BDWFLG = ' + str(TradeContext.BDWFLG))
    else:
        AfaLoggerFunc.tradeDebug("Info['BDWFLG']������")

    if from_dict.has_key('PRTCNT'):
        TradeContext.PRTCNT = from_dict['PRTCNT']
        AfaLoggerFunc.tradeDebug('TradeContext.PRTCNT = ' + str(TradeContext.PRTCNT))
    else:
        AfaLoggerFunc.tradeDebug("Info['PRTCNT']������")

    if from_dict.has_key('BJETIM'):
        TradeContext.BJETIM = from_dict['BJETIM']
        AfaLoggerFunc.tradeDebug('TradeContext.BJETIM = ' + str(TradeContext.BJETIM))
    else:
        AfaLoggerFunc.tradeDebug("Info['BJETIM']������")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("Info['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("Info['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("Info['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("Info['NOTE4']������")

    if from_dict.has_key('BILVER'):
        TradeContext.BILVER = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('TradeContext.BILVER = ' + str(TradeContext.BILVER))
    else:
        AfaLoggerFunc.tradeDebug("Info['BILVER']������")

    if from_dict.has_key('BILNO'):
        TradeContext.BILNO = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BILNO = ' + str(TradeContext.BILNO))
    else:
        AfaLoggerFunc.tradeDebug("Info['BILNO']������")

    if from_dict.has_key('BILRS'):
        TradeContext.BILRS = from_dict['BILRS']
        AfaLoggerFunc.tradeDebug('TradeContext.BILRS = ' + str(TradeContext.BILRS))
    else:
        AfaLoggerFunc.tradeDebug("Info['BILRS']������")

    if from_dict.has_key('BILTYP'):
        TradeContext.BILTYP = from_dict['BILTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.BILTYP = ' + str(TradeContext.BILTYP))
    else:
        AfaLoggerFunc.tradeDebug("Info['BILTYP']������")

    if from_dict.has_key('BILDAT'):
        TradeContext.BILDAT = from_dict['BILDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BILDAT = ' + str(TradeContext.BILDAT))
    else:
        AfaLoggerFunc.tradeDebug("Info['BILDAT']������")

    if from_dict.has_key('PAYWAY'):
        TradeContext.PAYWAY = from_dict['PAYWAY']
        AfaLoggerFunc.tradeDebug('TradeContext.PAYWAY = ' + str(TradeContext.PAYWAY))
    else:
        AfaLoggerFunc.tradeDebug("Info['PAYWAY']������")

    if from_dict.has_key('REMBNKCO'):
        TradeContext.REMBNKCO = from_dict['REMBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.REMBNKCO = ' + str(TradeContext.REMBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("Info['REMBNKCO']������")

    if from_dict.has_key('REMBNKNM'):
        TradeContext.REMBNKNM = from_dict['REMBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.REMBNKNM = ' + str(TradeContext.REMBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("Info['REMBNKNM']������")

    if from_dict.has_key('PAYBNKCO'):
        TradeContext.PAYBNKCO = from_dict['PAYBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.PAYBNKCO = ' + str(TradeContext.PAYBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("Info['PAYBNKCO']������")

    if from_dict.has_key('PAYBNKNM'):
        TradeContext.PAYBNKNM = from_dict['PAYBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.PAYBNKNM = ' + str(TradeContext.PAYBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("Info['PAYBNKNM']������")

    if from_dict.has_key('PYRACC'):
        TradeContext.PYRACC = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRACC = ' + str(TradeContext.PYRACC))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYRACC']������")

    if from_dict.has_key('PYRNAM'):
        TradeContext.PYRNAM = from_dict['PYRNAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRNAM = ' + str(TradeContext.PYRNAM))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYRNAM']������")

    if from_dict.has_key('PYRADDR'):
        TradeContext.PYRADDR = from_dict['PYRADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRADDR = ' + str(TradeContext.PYRADDR))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYRADDR']������")

    if from_dict.has_key('PYEACC'):
        TradeContext.PYEACC = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEACC = ' + str(TradeContext.PYEACC))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYEACC']������")

    if from_dict.has_key('PYENAM'):
        TradeContext.PYENAM = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYENAM = ' + str(TradeContext.PYENAM))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYENAM']������")

    if from_dict.has_key('PYEADDR'):
        TradeContext.PYEADDR = from_dict['PYEADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEADDR = ' + str(TradeContext.PYEADDR))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYEADDR']������")

    if from_dict.has_key('PYHACC'):
        TradeContext.PYHACC = from_dict['PYHACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYHACC = ' + str(TradeContext.PYHACC))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYHACC']������")

    if from_dict.has_key('PYHNAM'):
        TradeContext.PYHNAM = from_dict['PYHNAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYHNAM = ' + str(TradeContext.PYHNAM))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYHNAM']������")

    if from_dict.has_key('PYHADDR'):
        TradeContext.PYHADDR = from_dict['PYHADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYHADDR = ' + str(TradeContext.PYHADDR))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYHADDR']������")

    if from_dict.has_key('PYITYP'):
        TradeContext.PYITYP = from_dict['PYITYP']
        AfaLoggerFunc.tradeDebug('TradeContext.PYITYP = ' + str(TradeContext.PYITYP))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYITYP']������")

    if from_dict.has_key('PYIACC'):
        TradeContext.PYIACC = from_dict['PYIACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYIACC = ' + str(TradeContext.PYIACC))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYIACC']������")

    if from_dict.has_key('PYINAM'):
        TradeContext.PYINAM = from_dict['PYINAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYINAM = ' + str(TradeContext.PYINAM))
    else:
        AfaLoggerFunc.tradeDebug("Info['PYINAM']������")

    if from_dict.has_key('BILAMT'):
        TradeContext.BILAMT = from_dict['BILAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.BILAMT = ' + str(TradeContext.BILAMT))
    else:
        AfaLoggerFunc.tradeDebug("Info['BILAMT']������")

    if from_dict.has_key('OCCAMT'):
        TradeContext.OCCAMT = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.OCCAMT = ' + str(TradeContext.OCCAMT))
    else:
        AfaLoggerFunc.tradeDebug("Info['OCCAMT']������")

    if from_dict.has_key('RMNAMT'):
        TradeContext.RMNAMT = from_dict['RMNAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.RMNAMT = ' + str(TradeContext.RMNAMT))
    else:
        AfaLoggerFunc.tradeDebug("Info['RMNAMT']������")

    if from_dict.has_key('CUR'):
        TradeContext.CUR = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('TradeContext.CUR = ' + str(TradeContext.CUR))
    else:
        AfaLoggerFunc.tradeDebug("Info['CUR']������")

    if from_dict.has_key('SEAL'):
        TradeContext.SEAL = from_dict['SEAL']
        AfaLoggerFunc.tradeDebug('TradeContext.SEAL = ' + str(TradeContext.SEAL))
    else:
        AfaLoggerFunc.tradeDebug("Info['SEAL']������")

    if from_dict.has_key('USE'):
        TradeContext.USE = from_dict['USE']
        AfaLoggerFunc.tradeDebug('TradeContext.USE = ' + str(TradeContext.USE))
    else:
        AfaLoggerFunc.tradeDebug("Info['USE']������")

    if from_dict.has_key('REMARK'):
        TradeContext.REMARK = from_dict['REMARK']
        AfaLoggerFunc.tradeDebug('TradeContext.REMARK = ' + str(TradeContext.REMARK))
    else:
        AfaLoggerFunc.tradeDebug("Info['REMARK']������")

    if from_dict.has_key('HPCUSQ'):
        TradeContext.HPCUSQ = from_dict['HPCUSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.HPCUSQ = ' + str(TradeContext.HPCUSQ))
    else:
        AfaLoggerFunc.tradeDebug("Info['HPCUSQ']������")

    if from_dict.has_key('HPSTAT'):
        TradeContext.HPSTAT = from_dict['HPSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.HPSTAT = ' + str(TradeContext.HPSTAT))
    else:
        AfaLoggerFunc.tradeDebug("Info['HPSTAT']������")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("Info['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("Info['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("Info['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("Info['NOTE4']������")

    return True

