# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ hpdzmx �ֵ䵽 TradeContext �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dhpdzmx2CTradeContext.py
#   �޸�ʱ��:   Wed Jul  2 14:21:31 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('SNDBNKCO'):
        TradeContext.SNDBNKCO = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKCO = ' + str(TradeContext.SNDBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['SNDBNKCO']������")

    if from_dict.has_key('TRCDAT'):
        TradeContext.TRCDAT = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCDAT = ' + str(TradeContext.TRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        TradeContext.TRCNO = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCNO = ' + str(TradeContext.TRCNO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['TRCNO']������")

    if from_dict.has_key('NCCWKDAT'):
        TradeContext.NCCWKDAT = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.NCCWKDAT = ' + str(TradeContext.NCCWKDAT))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['NCCWKDAT']������")

    if from_dict.has_key('MSGTYPCO'):
        TradeContext.MSGTYPCO = from_dict['MSGTYPCO']
        AfaLoggerFunc.tradeDebug('TradeContext.MSGTYPCO = ' + str(TradeContext.MSGTYPCO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['MSGTYPCO']������")

    if from_dict.has_key('RCVMBRCO'):
        TradeContext.RCVMBRCO = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVMBRCO = ' + str(TradeContext.RCVMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['RCVMBRCO']������")

    if from_dict.has_key('SNDMBRCO'):
        TradeContext.SNDMBRCO = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDMBRCO = ' + str(TradeContext.SNDMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['SNDMBRCO']������")

    if from_dict.has_key('TRCCO'):
        TradeContext.TRCCO = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCCO = ' + str(TradeContext.TRCCO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['TRCCO']������")

    if from_dict.has_key('SNDBRHCO'):
        TradeContext.SNDBRHCO = from_dict['SNDBRHCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBRHCO = ' + str(TradeContext.SNDBRHCO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['SNDBRHCO']������")

    if from_dict.has_key('SNDCLKNO'):
        TradeContext.SNDCLKNO = from_dict['SNDCLKNO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDCLKNO = ' + str(TradeContext.SNDCLKNO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['SNDCLKNO']������")

    if from_dict.has_key('SNDTRDAT'):
        TradeContext.SNDTRDAT = from_dict['SNDTRDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDTRDAT = ' + str(TradeContext.SNDTRDAT))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['SNDTRDAT']������")

    if from_dict.has_key('SNDTRTIM'):
        TradeContext.SNDTRTIM = from_dict['SNDTRTIM']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDTRTIM = ' + str(TradeContext.SNDTRTIM))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['SNDTRTIM']������")

    if from_dict.has_key('MSGFLGNO'):
        TradeContext.MSGFLGNO = from_dict['MSGFLGNO']
        AfaLoggerFunc.tradeDebug('TradeContext.MSGFLGNO = ' + str(TradeContext.MSGFLGNO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['MSGFLGNO']������")

    if from_dict.has_key('ORMFN'):
        TradeContext.ORMFN = from_dict['ORMFN']
        AfaLoggerFunc.tradeDebug('TradeContext.ORMFN = ' + str(TradeContext.ORMFN))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['ORMFN']������")

    if from_dict.has_key('OPRTYPNO'):
        TradeContext.OPRTYPNO = from_dict['OPRTYPNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRTYPNO = ' + str(TradeContext.OPRTYPNO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['OPRTYPNO']������")

    if from_dict.has_key('ROPRTPNO'):
        TradeContext.ROPRTPNO = from_dict['ROPRTPNO']
        AfaLoggerFunc.tradeDebug('TradeContext.ROPRTPNO = ' + str(TradeContext.ROPRTPNO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['ROPRTPNO']������")

    if from_dict.has_key('SNDBNKNM'):
        TradeContext.SNDBNKNM = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKNM = ' + str(TradeContext.SNDBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        TradeContext.RCVBNKCO = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKCO = ' + str(TradeContext.RCVBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        TradeContext.RCVBNKNM = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKNM = ' + str(TradeContext.RCVBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['RCVBNKNM']������")

    if from_dict.has_key('CUR'):
        TradeContext.CUR = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('TradeContext.CUR = ' + str(TradeContext.CUR))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['CUR']������")

    if from_dict.has_key('OCCAMT'):
        TradeContext.OCCAMT = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.OCCAMT = ' + str(TradeContext.OCCAMT))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['OCCAMT']������")

    if from_dict.has_key('PYRACC'):
        TradeContext.PYRACC = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRACC = ' + str(TradeContext.PYRACC))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['PYRACC']������")

    if from_dict.has_key('PYRNAM'):
        TradeContext.PYRNAM = from_dict['PYRNAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRNAM = ' + str(TradeContext.PYRNAM))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['PYRNAM']������")

    if from_dict.has_key('PYRADDR'):
        TradeContext.PYRADDR = from_dict['PYRADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRADDR = ' + str(TradeContext.PYRADDR))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['PYRADDR']������")

    if from_dict.has_key('PYEACC'):
        TradeContext.PYEACC = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEACC = ' + str(TradeContext.PYEACC))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['PYEACC']������")

    if from_dict.has_key('PYENAM'):
        TradeContext.PYENAM = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYENAM = ' + str(TradeContext.PYENAM))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['PYENAM']������")

    if from_dict.has_key('PYEADDR'):
        TradeContext.PYEADDR = from_dict['PYEADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEADDR = ' + str(TradeContext.PYEADDR))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['PYEADDR']������")

    if from_dict.has_key('OPRATTNO'):
        TradeContext.OPRATTNO = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRATTNO = ' + str(TradeContext.OPRATTNO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['OPRATTNO']������")

    if from_dict.has_key('SEAL'):
        TradeContext.SEAL = from_dict['SEAL']
        AfaLoggerFunc.tradeDebug('TradeContext.SEAL = ' + str(TradeContext.SEAL))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['SEAL']������")

    if from_dict.has_key('BILDAT'):
        TradeContext.BILDAT = from_dict['BILDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BILDAT = ' + str(TradeContext.BILDAT))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['BILDAT']������")

    if from_dict.has_key('BILNO'):
        TradeContext.BILNO = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BILNO = ' + str(TradeContext.BILNO))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['BILNO']������")

    if from_dict.has_key('BILVER'):
        TradeContext.BILVER = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('TradeContext.BILVER = ' + str(TradeContext.BILVER))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['BILVER']������")

    if from_dict.has_key('PAYWAY'):
        TradeContext.PAYWAY = from_dict['PAYWAY']
        AfaLoggerFunc.tradeDebug('TradeContext.PAYWAY = ' + str(TradeContext.PAYWAY))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['PAYWAY']������")

    if from_dict.has_key('BILAMT'):
        TradeContext.BILAMT = from_dict['BILAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.BILAMT = ' + str(TradeContext.BILAMT))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['BILAMT']������")

    if from_dict.has_key('RMNAMT'):
        TradeContext.RMNAMT = from_dict['RMNAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.RMNAMT = ' + str(TradeContext.RMNAMT))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['RMNAMT']������")

    if from_dict.has_key('USE'):
        TradeContext.USE = from_dict['USE']
        AfaLoggerFunc.tradeDebug('TradeContext.USE = ' + str(TradeContext.USE))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['USE']������")

    if from_dict.has_key('REMARK'):
        TradeContext.REMARK = from_dict['REMARK']
        AfaLoggerFunc.tradeDebug('TradeContext.REMARK = ' + str(TradeContext.REMARK))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['REMARK']������")

    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['BSPSQN']������")

    if from_dict.has_key('BCSTAT'):
        TradeContext.BCSTAT = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BCSTAT = ' + str(TradeContext.BCSTAT))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['BCSTAT']������")

    if from_dict.has_key('BDWFLG'):
        TradeContext.BDWFLG = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BDWFLG = ' + str(TradeContext.BDWFLG))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['BDWFLG']������")

    if from_dict.has_key('EACTYP'):
        TradeContext.EACTYP = from_dict['EACTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.EACTYP = ' + str(TradeContext.EACTYP))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['EACTYP']������")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("hpdzmx['NOTE4']������")

    return True

