# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ records �ֵ䵽 TradeContext �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8522Drecords2CTradeContext.py
#   �޸�ʱ��:   Sat Oct 25 15:21:30 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("records['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("records['BSPSQN']������")

    if from_dict.has_key('BRSFLG'):
        TradeContext.BRSFLG = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BRSFLG = ' + str(TradeContext.BRSFLG))
    else:
        AfaLoggerFunc.tradeDebug("records['BRSFLG']������")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("records['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("records['BEACSB']������")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("records['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("records['BEAUUS']������")

    if from_dict.has_key('BEAUPS'):
        TradeContext.BEAUPS = from_dict['BEAUPS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUPS = ' + str(TradeContext.BEAUPS))
    else:
        AfaLoggerFunc.tradeDebug("records['BEAUPS']������")

    if from_dict.has_key('TERMID'):
        TradeContext.TERMID = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('TradeContext.TERMID = ' + str(TradeContext.TERMID))
    else:
        AfaLoggerFunc.tradeDebug("records['TERMID']������")

    if from_dict.has_key('BBSSRC'):
        TradeContext.BBSSRC = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('TradeContext.BBSSRC = ' + str(TradeContext.BBSSRC))
    else:
        AfaLoggerFunc.tradeDebug("records['BBSSRC']������")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("records['DASQ']������")

    if from_dict.has_key('DCFLG'):
        TradeContext.DCFLG = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.DCFLG = ' + str(TradeContext.DCFLG))
    else:
        AfaLoggerFunc.tradeDebug("records['DCFLG']������")

    if from_dict.has_key('OPRNO'):
        TradeContext.OPRNO = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRNO = ' + str(TradeContext.OPRNO))
    else:
        AfaLoggerFunc.tradeDebug("records['OPRNO']������")

    if from_dict.has_key('OPRATTNO'):
        TradeContext.OPRATTNO = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRATTNO = ' + str(TradeContext.OPRATTNO))
    else:
        AfaLoggerFunc.tradeDebug("records['OPRATTNO']������")

    if from_dict.has_key('NCCWKDAT'):
        TradeContext.NCCWKDAT = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.NCCWKDAT = ' + str(TradeContext.NCCWKDAT))
    else:
        AfaLoggerFunc.tradeDebug("records['NCCWKDAT']������")

    if from_dict.has_key('TRCCO'):
        TradeContext.TRCCO = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCCO = ' + str(TradeContext.TRCCO))
    else:
        AfaLoggerFunc.tradeDebug("records['TRCCO']������")

    if from_dict.has_key('TRCDAT'):
        TradeContext.TRCDAT = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCDAT = ' + str(TradeContext.TRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("records['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        TradeContext.TRCNO = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCNO = ' + str(TradeContext.TRCNO))
    else:
        AfaLoggerFunc.tradeDebug("records['TRCNO']������")

    if from_dict.has_key('MSGFLGNO'):
        TradeContext.MSGFLGNO = from_dict['MSGFLGNO']
        AfaLoggerFunc.tradeDebug('TradeContext.MSGFLGNO = ' + str(TradeContext.MSGFLGNO))
    else:
        AfaLoggerFunc.tradeDebug("records['MSGFLGNO']������")

    if from_dict.has_key('COTRCDAT'):
        TradeContext.COTRCDAT = from_dict['COTRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.COTRCDAT = ' + str(TradeContext.COTRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("records['COTRCDAT']������")

    if from_dict.has_key('COTRCNO'):
        TradeContext.COTRCNO = from_dict['COTRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.COTRCNO = ' + str(TradeContext.COTRCNO))
    else:
        AfaLoggerFunc.tradeDebug("records['COTRCNO']������")

    if from_dict.has_key('COMSGFLGNO'):
        TradeContext.COMSGFLGNO = from_dict['COMSGFLGNO']
        AfaLoggerFunc.tradeDebug('TradeContext.COMSGFLGNO = ' + str(TradeContext.COMSGFLGNO))
    else:
        AfaLoggerFunc.tradeDebug("records['COMSGFLGNO']������")

    if from_dict.has_key('SNDMBRCO'):
        TradeContext.SNDMBRCO = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDMBRCO = ' + str(TradeContext.SNDMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("records['SNDMBRCO']������")

    if from_dict.has_key('RCVMBRCO'):
        TradeContext.RCVMBRCO = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVMBRCO = ' + str(TradeContext.RCVMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("records['RCVMBRCO']������")

    if from_dict.has_key('SNDBNKCO'):
        TradeContext.SNDBNKCO = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKCO = ' + str(TradeContext.SNDBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("records['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        TradeContext.SNDBNKNM = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKNM = ' + str(TradeContext.SNDBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("records['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        TradeContext.RCVBNKCO = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKCO = ' + str(TradeContext.RCVBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("records['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        TradeContext.RCVBNKNM = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKNM = ' + str(TradeContext.RCVBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("records['RCVBNKNM']������")

    if from_dict.has_key('CUR'):
        TradeContext.CUR = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('TradeContext.CUR = ' + str(TradeContext.CUR))
    else:
        AfaLoggerFunc.tradeDebug("records['CUR']������")

    if from_dict.has_key('OCCAMT'):
        TradeContext.OCCAMT = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.OCCAMT = ' + str(TradeContext.OCCAMT))
    else:
        AfaLoggerFunc.tradeDebug("records['OCCAMT']������")

    if from_dict.has_key('CHRGTYP'):
        TradeContext.CHRGTYP = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.CHRGTYP = ' + str(TradeContext.CHRGTYP))
    else:
        AfaLoggerFunc.tradeDebug("records['CHRGTYP']������")

    if from_dict.has_key('LOCCUSCHRG'):
        TradeContext.LOCCUSCHRG = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('TradeContext.LOCCUSCHRG = ' + str(TradeContext.LOCCUSCHRG))
    else:
        AfaLoggerFunc.tradeDebug("records['LOCCUSCHRG']������")

    if from_dict.has_key('CUSCHRG'):
        TradeContext.CUSCHRG = from_dict['CUSCHRG']
        AfaLoggerFunc.tradeDebug('TradeContext.CUSCHRG = ' + str(TradeContext.CUSCHRG))
    else:
        AfaLoggerFunc.tradeDebug("records['CUSCHRG']������")

    if from_dict.has_key('PYRACC'):
        TradeContext.PYRACC = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRACC = ' + str(TradeContext.PYRACC))
    else:
        AfaLoggerFunc.tradeDebug("records['PYRACC']������")

    if from_dict.has_key('PYRNAM'):
        TradeContext.PYRNAM = from_dict['PYRNAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRNAM = ' + str(TradeContext.PYRNAM))
    else:
        AfaLoggerFunc.tradeDebug("records['PYRNAM']������")

    if from_dict.has_key('PYRADDR'):
        TradeContext.PYRADDR = from_dict['PYRADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRADDR = ' + str(TradeContext.PYRADDR))
    else:
        AfaLoggerFunc.tradeDebug("records['PYRADDR']������")

    if from_dict.has_key('PYEACC'):
        TradeContext.PYEACC = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEACC = ' + str(TradeContext.PYEACC))
    else:
        AfaLoggerFunc.tradeDebug("records['PYEACC']������")

    if from_dict.has_key('PYENAM'):
        TradeContext.PYENAM = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYENAM = ' + str(TradeContext.PYENAM))
    else:
        AfaLoggerFunc.tradeDebug("records['PYENAM']������")

    if from_dict.has_key('PYEADDR'):
        TradeContext.PYEADDR = from_dict['PYEADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEADDR = ' + str(TradeContext.PYEADDR))
    else:
        AfaLoggerFunc.tradeDebug("records['PYEADDR']������")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("records['STRINFO']������")

    if from_dict.has_key('CERTTYPE'):
        TradeContext.CERTTYPE = from_dict['CERTTYPE']
        AfaLoggerFunc.tradeDebug('TradeContext.CERTTYPE = ' + str(TradeContext.CERTTYPE))
    else:
        AfaLoggerFunc.tradeDebug("records['CERTTYPE']������")

    if from_dict.has_key('CERTNO'):
        TradeContext.CERTNO = from_dict['CERTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.CERTNO = ' + str(TradeContext.CERTNO))
    else:
        AfaLoggerFunc.tradeDebug("records['CERTNO']������")

    if from_dict.has_key('BNKBKNO'):
        TradeContext.BNKBKNO = from_dict['BNKBKNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BNKBKNO = ' + str(TradeContext.BNKBKNO))
    else:
        AfaLoggerFunc.tradeDebug("records['BNKBKNO']������")

    if from_dict.has_key('BNKBKBAL'):
        TradeContext.BNKBKBAL = from_dict['BNKBKBAL']
        AfaLoggerFunc.tradeDebug('TradeContext.BNKBKBAL = ' + str(TradeContext.BNKBKBAL))
    else:
        AfaLoggerFunc.tradeDebug("records['BNKBKBAL']������")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("records['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("records['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("records['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("records['NOTE4']������")

    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("records['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("records['BSPSQN']������")

    if from_dict.has_key('BCURSQ'):
        TradeContext.BCURSQ = from_dict['BCURSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.BCURSQ = ' + str(TradeContext.BCURSQ))
    else:
        AfaLoggerFunc.tradeDebug("records['BCURSQ']������")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("records['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("records['BEACSB']������")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("records['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("records['BEAUUS']������")

    if from_dict.has_key('FEDT'):
        TradeContext.FEDT = from_dict['FEDT']
        AfaLoggerFunc.tradeDebug('TradeContext.FEDT = ' + str(TradeContext.FEDT))
    else:
        AfaLoggerFunc.tradeDebug("records['FEDT']������")

    if from_dict.has_key('RBSQ'):
        TradeContext.RBSQ = from_dict['RBSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.RBSQ = ' + str(TradeContext.RBSQ))
    else:
        AfaLoggerFunc.tradeDebug("records['RBSQ']������")

    if from_dict.has_key('TRDT'):
        TradeContext.TRDT = from_dict['TRDT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRDT = ' + str(TradeContext.TRDT))
    else:
        AfaLoggerFunc.tradeDebug("records['TRDT']������")

    if from_dict.has_key('TLSQ'):
        TradeContext.TLSQ = from_dict['TLSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.TLSQ = ' + str(TradeContext.TLSQ))
    else:
        AfaLoggerFunc.tradeDebug("records['TLSQ']������")

    if from_dict.has_key('SBAC'):
        TradeContext.SBAC = from_dict['SBAC']
        AfaLoggerFunc.tradeDebug('TradeContext.SBAC = ' + str(TradeContext.SBAC))
    else:
        AfaLoggerFunc.tradeDebug("records['SBAC']������")

    if from_dict.has_key('ACNM'):
        TradeContext.ACNM = from_dict['ACNM']
        AfaLoggerFunc.tradeDebug('TradeContext.ACNM = ' + str(TradeContext.ACNM))
    else:
        AfaLoggerFunc.tradeDebug("records['ACNM']������")

    if from_dict.has_key('RBAC'):
        TradeContext.RBAC = from_dict['RBAC']
        AfaLoggerFunc.tradeDebug('TradeContext.RBAC = ' + str(TradeContext.RBAC))
    else:
        AfaLoggerFunc.tradeDebug("records['RBAC']������")

    if from_dict.has_key('OTNM'):
        TradeContext.OTNM = from_dict['OTNM']
        AfaLoggerFunc.tradeDebug('TradeContext.OTNM = ' + str(TradeContext.OTNM))
    else:
        AfaLoggerFunc.tradeDebug("records['OTNM']������")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("records['DASQ']������")

    if from_dict.has_key('MGID'):
        TradeContext.MGID = from_dict['MGID']
        AfaLoggerFunc.tradeDebug('TradeContext.MGID = ' + str(TradeContext.MGID))
    else:
        AfaLoggerFunc.tradeDebug("records['MGID']������")

    if from_dict.has_key('PRCCO'):
        TradeContext.PRCCO = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.PRCCO = ' + str(TradeContext.PRCCO))
    else:
        AfaLoggerFunc.tradeDebug("records['PRCCO']������")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("records['STRINFO']������")

    if from_dict.has_key('BCSTAT'):
        TradeContext.BCSTAT = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BCSTAT = ' + str(TradeContext.BCSTAT))
    else:
        AfaLoggerFunc.tradeDebug("records['BCSTAT']������")

    if from_dict.has_key('BDWFLG'):
        TradeContext.BDWFLG = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BDWFLG = ' + str(TradeContext.BDWFLG))
    else:
        AfaLoggerFunc.tradeDebug("records['BDWFLG']������")

    if from_dict.has_key('PRTCNT'):
        TradeContext.PRTCNT = from_dict['PRTCNT']
        AfaLoggerFunc.tradeDebug('TradeContext.PRTCNT = ' + str(TradeContext.PRTCNT))
    else:
        AfaLoggerFunc.tradeDebug("records['PRTCNT']������")

    if from_dict.has_key('BJETIM'):
        TradeContext.BJETIM = from_dict['BJETIM']
        AfaLoggerFunc.tradeDebug('TradeContext.BJETIM = ' + str(TradeContext.BJETIM))
    else:
        AfaLoggerFunc.tradeDebug("records['BJETIM']������")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("records['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("records['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("records['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("records['NOTE4']������")

    return True

