# -*- coding: gbk -*-
##################################################################
#   农信银系统 Trans 字典到 TradeContext 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap8522DTrans2CTradeContext.py
#   修改时间:   Fri Jul 18 16:07:37 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BJEDTE']不存在")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BSPSQN']不存在")

    if from_dict.has_key('BCURSQ'):
        TradeContext.BCURSQ = from_dict['BCURSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.BCURSQ = ' + str(TradeContext.BCURSQ))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BCURSQ']不存在")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BESBNO']不存在")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BEACSB']不存在")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BETELR']不存在")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BEAUUS']不存在")

    if from_dict.has_key('FEDT'):
        TradeContext.FEDT = from_dict['FEDT']
        AfaLoggerFunc.tradeDebug('TradeContext.FEDT = ' + str(TradeContext.FEDT))
    else:
        AfaLoggerFunc.tradeDebug("Trans['FEDT']不存在")

    if from_dict.has_key('RBSQ'):
        TradeContext.RBSQ = from_dict['RBSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.RBSQ = ' + str(TradeContext.RBSQ))
    else:
        AfaLoggerFunc.tradeDebug("Trans['RBSQ']不存在")

    if from_dict.has_key('TRDT'):
        TradeContext.TRDT = from_dict['TRDT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRDT = ' + str(TradeContext.TRDT))
    else:
        AfaLoggerFunc.tradeDebug("Trans['TRDT']不存在")

    if from_dict.has_key('TLSQ'):
        TradeContext.TLSQ = from_dict['TLSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.TLSQ = ' + str(TradeContext.TLSQ))
    else:
        AfaLoggerFunc.tradeDebug("Trans['TLSQ']不存在")

    if from_dict.has_key('SBAC'):
        TradeContext.SBAC = from_dict['SBAC']
        AfaLoggerFunc.tradeDebug('TradeContext.SBAC = ' + str(TradeContext.SBAC))
    else:
        AfaLoggerFunc.tradeDebug("Trans['SBAC']不存在")

    if from_dict.has_key('ACNM'):
        TradeContext.ACNM = from_dict['ACNM']
        AfaLoggerFunc.tradeDebug('TradeContext.ACNM = ' + str(TradeContext.ACNM))
    else:
        AfaLoggerFunc.tradeDebug("Trans['ACNM']不存在")

    if from_dict.has_key('RBAC'):
        TradeContext.RBAC = from_dict['RBAC']
        AfaLoggerFunc.tradeDebug('TradeContext.RBAC = ' + str(TradeContext.RBAC))
    else:
        AfaLoggerFunc.tradeDebug("Trans['RBAC']不存在")

    if from_dict.has_key('OTNM'):
        TradeContext.OTNM = from_dict['OTNM']
        AfaLoggerFunc.tradeDebug('TradeContext.OTNM = ' + str(TradeContext.OTNM))
    else:
        AfaLoggerFunc.tradeDebug("Trans['OTNM']不存在")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("Trans['DASQ']不存在")

    if from_dict.has_key('MGID'):
        TradeContext.MGID = from_dict['MGID']
        AfaLoggerFunc.tradeDebug('TradeContext.MGID = ' + str(TradeContext.MGID))
    else:
        AfaLoggerFunc.tradeDebug("Trans['MGID']不存在")

    if from_dict.has_key('PRCCO'):
        TradeContext.PRCCO = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.PRCCO = ' + str(TradeContext.PRCCO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['PRCCO']不存在")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['STRINFO']不存在")

    if from_dict.has_key('BCSTAT'):
        TradeContext.BCSTAT = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BCSTAT = ' + str(TradeContext.BCSTAT))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BCSTAT']不存在")

    if from_dict.has_key('BDWFLG'):
        TradeContext.BDWFLG = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BDWFLG = ' + str(TradeContext.BDWFLG))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BDWFLG']不存在")

    if from_dict.has_key('PRTCNT'):
        TradeContext.PRTCNT = from_dict['PRTCNT']
        AfaLoggerFunc.tradeDebug('TradeContext.PRTCNT = ' + str(TradeContext.PRTCNT))
    else:
        AfaLoggerFunc.tradeDebug("Trans['PRTCNT']不存在")

    if from_dict.has_key('BJETIM'):
        TradeContext.BJETIM = from_dict['BJETIM']
        AfaLoggerFunc.tradeDebug('TradeContext.BJETIM = ' + str(TradeContext.BJETIM))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BJETIM']不存在")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NOTE1']不存在")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NOTE2']不存在")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NOTE3']不存在")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NOTE4']不存在")

    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BJEDTE']不存在")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BSPSQN']不存在")

    if from_dict.has_key('BRSFLG'):
        TradeContext.BRSFLG = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BRSFLG = ' + str(TradeContext.BRSFLG))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BRSFLG']不存在")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BESBNO']不存在")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BEACSB']不存在")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BETELR']不存在")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BEAUUS']不存在")

    if from_dict.has_key('TERMID'):
        TradeContext.TERMID = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('TradeContext.TERMID = ' + str(TradeContext.TERMID))
    else:
        AfaLoggerFunc.tradeDebug("Trans['TERMID']不存在")

    if from_dict.has_key('BBSSRC'):
        TradeContext.BBSSRC = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('TradeContext.BBSSRC = ' + str(TradeContext.BBSSRC))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BBSSRC']不存在")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("Trans['DASQ']不存在")

    if from_dict.has_key('DCFLG'):
        TradeContext.DCFLG = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.DCFLG = ' + str(TradeContext.DCFLG))
    else:
        AfaLoggerFunc.tradeDebug("Trans['DCFLG']不存在")
        
    if from_dict.has_key('OPRNO'):
        TradeContext.OPRNO = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRNO = ' + str(TradeContext.OPRNO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['OPRNO']不存在")

    if from_dict.has_key('OPRATTNO'):
        TradeContext.OPRATTNO = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRATTNO = ' + str(TradeContext.OPRATTNO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['OPRATTNO']不存在")

    if from_dict.has_key('NCCWKDAT'):
        TradeContext.NCCWKDAT = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.NCCWKDAT = ' + str(TradeContext.NCCWKDAT))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NCCWKDAT']不存在")

    if from_dict.has_key('TRCCO'):
        TradeContext.TRCCO = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCCO = ' + str(TradeContext.TRCCO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['TRCCO']不存在")

    if from_dict.has_key('TRCDAT'):
        TradeContext.TRCDAT = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCDAT = ' + str(TradeContext.TRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("Trans['TRCDAT']不存在")

    if from_dict.has_key('TRCNO'):
        TradeContext.TRCNO = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCNO = ' + str(TradeContext.TRCNO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['TRCNO']不存在")

    if from_dict.has_key('SNDMBRCO'):
        TradeContext.SNDMBRCO = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDMBRCO = ' + str(TradeContext.SNDMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['SNDMBRCO']不存在")

    if from_dict.has_key('RCVMBRCO'):
        TradeContext.RCVMBRCO = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVMBRCO = ' + str(TradeContext.RCVMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['RCVMBRCO']不存在")

    if from_dict.has_key('SNDBNKCO'):
        TradeContext.SNDBNKCO = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKCO = ' + str(TradeContext.SNDBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['SNDBNKCO']不存在")

    if from_dict.has_key('SNDBNKNM'):
        TradeContext.SNDBNKNM = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKNM = ' + str(TradeContext.SNDBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("Trans['SNDBNKNM']不存在")

    if from_dict.has_key('RCVBNKCO'):
        TradeContext.RCVBNKCO = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKCO = ' + str(TradeContext.RCVBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['RCVBNKCO']不存在")

    if from_dict.has_key('RCVBNKNM'):
        TradeContext.RCVBNKNM = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKNM = ' + str(TradeContext.RCVBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("Trans['RCVBNKNM']不存在")

    if from_dict.has_key('BILVER'):
        TradeContext.BILVER = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('TradeContext.BILVER = ' + str(TradeContext.BILVER))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BILVER']不存在")

    if from_dict.has_key('BILNO'):
        TradeContext.BILNO = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BILNO = ' + str(TradeContext.BILNO))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BILNO']不存在")

    if from_dict.has_key('CHRGTYP'):
        TradeContext.CHRGTYP = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.CHRGTYP = ' + str(TradeContext.CHRGTYP))
    else:
        AfaLoggerFunc.tradeDebug("Trans['CHRGTYP']不存在")

    if from_dict.has_key('LOCCUSCHRG'):
        TradeContext.LOCCUSCHRG = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('TradeContext.LOCCUSCHRG = ' + str(TradeContext.LOCCUSCHRG))
    else:
        AfaLoggerFunc.tradeDebug("Trans['LOCCUSCHRG']不存在")

    if from_dict.has_key('BILRS'):
        TradeContext.BILRS = from_dict['BILRS']
        AfaLoggerFunc.tradeDebug('TradeContext.BILRS = ' + str(TradeContext.BILRS))
    else:
        AfaLoggerFunc.tradeDebug("Trans['BILRS']不存在")

    if from_dict.has_key('HPCUSQ'):
        TradeContext.HPCUSQ = from_dict['HPCUSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.HPCUSQ = ' + str(TradeContext.HPCUSQ))
    else:
        AfaLoggerFunc.tradeDebug("Trans['HPCUSQ']不存在")

    if from_dict.has_key('HPSTAT'):
        TradeContext.HPSTAT = from_dict['HPSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.HPSTAT = ' + str(TradeContext.HPSTAT))
    else:
        AfaLoggerFunc.tradeDebug("Trans['HPSTAT']不存在")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NOTE1']不存在")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NOTE2']不存在")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NOTE3']不存在")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("Trans['NOTE4']不存在")

    return True

