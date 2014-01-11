# -*- coding: gbk -*-
##################################################################
#   农信银系统 TransTrc 字典到 TradeContext 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap8522DTransTrc2CTradeContext.py
#   修改时间:   Fri Jul 18 17:29:24 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BJEDTE']不存在")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BSPSQN']不存在")

    if from_dict.has_key('BRSFLG'):
        TradeContext.BRSFLG = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BRSFLG = ' + str(TradeContext.BRSFLG))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BRSFLG']不存在")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BESBNO']不存在")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BEACSB']不存在")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BETELR']不存在")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BEAUUS']不存在")

    if from_dict.has_key('TERMID'):
        TradeContext.TERMID = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('TradeContext.TERMID = ' + str(TradeContext.TERMID))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['TERMID']不存在")

    if from_dict.has_key('BBSSRC'):
        TradeContext.BBSSRC = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('TradeContext.BBSSRC = ' + str(TradeContext.BBSSRC))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BBSSRC']不存在")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['DASQ']不存在")

    if from_dict.has_key('DCFLG'):
        TradeContext.DCFLG = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.DCFLG = ' + str(TradeContext.DCFLG))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['DCFLG']不存在")

    if from_dict.has_key('OPRNO'):
        TradeContext.OPRNO = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRNO = ' + str(TradeContext.OPRNO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['OPRNO']不存在")

    if from_dict.has_key('OPRATTNO'):
        TradeContext.OPRATTNO = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRATTNO = ' + str(TradeContext.OPRATTNO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['OPRATTNO']不存在")

    if from_dict.has_key('NCCWKDAT'):
        TradeContext.NCCWKDAT = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.NCCWKDAT = ' + str(TradeContext.NCCWKDAT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['NCCWKDAT']不存在")

    if from_dict.has_key('TRCCO'):
        TradeContext.TRCCO = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCCO = ' + str(TradeContext.TRCCO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['TRCCO']不存在")

    if from_dict.has_key('TRCDAT'):
        TradeContext.TRCDAT = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCDAT = ' + str(TradeContext.TRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['TRCDAT']不存在")

    if from_dict.has_key('TRCNO'):
        TradeContext.TRCNO = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCNO = ' + str(TradeContext.TRCNO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['TRCNO']不存在")

    if from_dict.has_key('SNDMBRCO'):
        TradeContext.SNDMBRCO = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDMBRCO = ' + str(TradeContext.SNDMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['SNDMBRCO']不存在")

    if from_dict.has_key('RCVMBRCO'):
        TradeContext.RCVMBRCO = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVMBRCO = ' + str(TradeContext.RCVMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['RCVMBRCO']不存在")

    if from_dict.has_key('SNDBNKCO'):
        TradeContext.SNDBNKCO = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKCO = ' + str(TradeContext.SNDBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['SNDBNKCO']不存在")

    if from_dict.has_key('SNDBNKNM'):
        TradeContext.SNDBNKNM = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKNM = ' + str(TradeContext.SNDBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['SNDBNKNM']不存在")

    if from_dict.has_key('RCVBNKCO'):
        TradeContext.RCVBNKCO = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKCO = ' + str(TradeContext.RCVBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['RCVBNKCO']不存在")

    if from_dict.has_key('RCVBNKNM'):
        TradeContext.RCVBNKNM = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKNM = ' + str(TradeContext.RCVBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['RCVBNKNM']不存在")

    if from_dict.has_key('CUR'):
        TradeContext.CUR = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('TradeContext.CUR = ' + str(TradeContext.CUR))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['CUR']不存在")

    if from_dict.has_key('OCCAMT'):
        TradeContext.OCCAMT = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.OCCAMT = ' + str(TradeContext.OCCAMT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['OCCAMT']不存在")

    if from_dict.has_key('CHRGTYP'):
        TradeContext.CHRGTYP = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.CHRGTYP = ' + str(TradeContext.CHRGTYP))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['CHRGTYP']不存在")

    if from_dict.has_key('LOCCUSCHRG'):
        TradeContext.LOCCUSCHRG = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('TradeContext.LOCCUSCHRG = ' + str(TradeContext.LOCCUSCHRG))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['LOCCUSCHRG']不存在")

    if from_dict.has_key('CUSCHRG'):
        TradeContext.CUSCHRG = from_dict['CUSCHRG']
        AfaLoggerFunc.tradeDebug('TradeContext.CUSCHRG = ' + str(TradeContext.CUSCHRG))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['CUSCHRG']不存在")

    if from_dict.has_key('PYRACC'):
        TradeContext.PYRACC = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRACC = ' + str(TradeContext.PYRACC))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['PYRACC']不存在")

    if from_dict.has_key('PYRNAM'):
        TradeContext.PYRNAM = from_dict['PYRNAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRNAM = ' + str(TradeContext.PYRNAM))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['PYRNAM']不存在")

    if from_dict.has_key('PYRADDR'):
        TradeContext.PYRADDR = from_dict['PYRADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRADDR = ' + str(TradeContext.PYRADDR))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['PYRADDR']不存在")

    if from_dict.has_key('PYEACC'):
        TradeContext.PYEACC = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEACC = ' + str(TradeContext.PYEACC))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['PYEACC']不存在")

    if from_dict.has_key('PYENAM'):
        TradeContext.PYENAM = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYENAM = ' + str(TradeContext.PYENAM))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['PYENAM']不存在")

    if from_dict.has_key('PYEADDR'):
        TradeContext.PYEADDR = from_dict['PYEADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEADDR = ' + str(TradeContext.PYEADDR))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['PYEADDR']不存在")

    if from_dict.has_key('SEAL'):
        TradeContext.SEAL = from_dict['SEAL']
        AfaLoggerFunc.tradeDebug('TradeContext.SEAL = ' + str(TradeContext.SEAL))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['SEAL']不存在")

    if from_dict.has_key('USE'):
        TradeContext.USE = from_dict['USE']
        AfaLoggerFunc.tradeDebug('TradeContext.USE = ' + str(TradeContext.USE))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['USE']不存在")

    if from_dict.has_key('REMARK'):
        TradeContext.REMARK = from_dict['REMARK']
        AfaLoggerFunc.tradeDebug('TradeContext.REMARK = ' + str(TradeContext.REMARK))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['REMARK']不存在")

    if from_dict.has_key('BILTYP'):
        TradeContext.BILTYP = from_dict['BILTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.BILTYP = ' + str(TradeContext.BILTYP))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BILTYP']不存在")

    if from_dict.has_key('BILDAT'):
        TradeContext.BILDAT = from_dict['BILDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BILDAT = ' + str(TradeContext.BILDAT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BILDAT']不存在")

    if from_dict.has_key('BILNO'):
        TradeContext.BILNO = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BILNO = ' + str(TradeContext.BILNO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BILNO']不存在")

    if from_dict.has_key('COMAMT'):
        TradeContext.COMAMT = from_dict['COMAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.COMAMT = ' + str(TradeContext.COMAMT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['COMAMT']不存在")

    if from_dict.has_key('OVPAYAMT'):
        TradeContext.OVPAYAMT = from_dict['OVPAYAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.OVPAYAMT = ' + str(TradeContext.OVPAYAMT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['OVPAYAMT']不存在")

    if from_dict.has_key('CPSAMT'):
        TradeContext.CPSAMT = from_dict['CPSAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.CPSAMT = ' + str(TradeContext.CPSAMT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['CPSAMT']不存在")

    if from_dict.has_key('RFUAMT'):
        TradeContext.RFUAMT = from_dict['RFUAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.RFUAMT = ' + str(TradeContext.RFUAMT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['RFUAMT']不存在")

    if from_dict.has_key('CERTTYPE'):
        TradeContext.CERTTYPE = from_dict['CERTTYPE']
        AfaLoggerFunc.tradeDebug('TradeContext.CERTTYPE = ' + str(TradeContext.CERTTYPE))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['CERTTYPE']不存在")

    if from_dict.has_key('CERTNO'):
        TradeContext.CERTNO = from_dict['CERTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.CERTNO = ' + str(TradeContext.CERTNO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['CERTNO']不存在")

    if from_dict.has_key('BOJEDT'):
        TradeContext.BOJEDT = from_dict['BOJEDT']
        AfaLoggerFunc.tradeDebug('TradeContext.BOJEDT = ' + str(TradeContext.BOJEDT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BOJEDT']不存在")

    if from_dict.has_key('BOSPSQ'):
        TradeContext.BOSPSQ = from_dict['BOSPSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.BOSPSQ = ' + str(TradeContext.BOSPSQ))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BOSPSQ']不存在")

    if from_dict.has_key('ORTRCDAT'):
        TradeContext.ORTRCDAT = from_dict['ORTRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCDAT = ' + str(TradeContext.ORTRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['ORTRCDAT']不存在")

    if from_dict.has_key('ORTRCCO'):
        TradeContext.ORTRCCO = from_dict['ORTRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCCO = ' + str(TradeContext.ORTRCCO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['ORTRCCO']不存在")

    if from_dict.has_key('ORTRCNO'):
        TradeContext.ORTRCNO = from_dict['ORTRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCNO = ' + str(TradeContext.ORTRCNO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['ORTRCNO']不存在")

    if from_dict.has_key('ORSNDBNK'):
        TradeContext.ORSNDBNK = from_dict['ORSNDBNK']
        AfaLoggerFunc.tradeDebug('TradeContext.ORSNDBNK = ' + str(TradeContext.ORSNDBNK))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['ORSNDBNK']不存在")

    if from_dict.has_key('ORRCVBNK'):
        TradeContext.ORRCVBNK = from_dict['ORRCVBNK']
        AfaLoggerFunc.tradeDebug('TradeContext.ORRCVBNK = ' + str(TradeContext.ORRCVBNK))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['ORRCVBNK']不存在")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['STRINFO']不存在")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['NOTE1']不存在")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['NOTE2']不存在")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['NOTE3']不存在")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['NOTE4']不存在")

    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BJEDTE']不存在")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BSPSQN']不存在")

    if from_dict.has_key('BCURSQ'):
        TradeContext.BCURSQ = from_dict['BCURSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.BCURSQ = ' + str(TradeContext.BCURSQ))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BCURSQ']不存在")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BESBNO']不存在")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BEACSB']不存在")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BETELR']不存在")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BEAUUS']不存在")

    if from_dict.has_key('FEDT'):
        TradeContext.FEDT = from_dict['FEDT']
        AfaLoggerFunc.tradeDebug('TradeContext.FEDT = ' + str(TradeContext.FEDT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['FEDT']不存在")

    if from_dict.has_key('RBSQ'):
        TradeContext.RBSQ = from_dict['RBSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.RBSQ = ' + str(TradeContext.RBSQ))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['RBSQ']不存在")

    if from_dict.has_key('TRDT'):
        TradeContext.TRDT = from_dict['TRDT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRDT = ' + str(TradeContext.TRDT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['TRDT']不存在")

    if from_dict.has_key('TLSQ'):
        TradeContext.TLSQ = from_dict['TLSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.TLSQ = ' + str(TradeContext.TLSQ))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['TLSQ']不存在")

    if from_dict.has_key('SBAC'):
        TradeContext.SBAC = from_dict['SBAC']
        AfaLoggerFunc.tradeDebug('TradeContext.SBAC = ' + str(TradeContext.SBAC))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['SBAC']不存在")

    if from_dict.has_key('ACNM'):
        TradeContext.ACNM = from_dict['ACNM']
        AfaLoggerFunc.tradeDebug('TradeContext.ACNM = ' + str(TradeContext.ACNM))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['ACNM']不存在")

    if from_dict.has_key('RBAC'):
        TradeContext.RBAC = from_dict['RBAC']
        AfaLoggerFunc.tradeDebug('TradeContext.RBAC = ' + str(TradeContext.RBAC))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['RBAC']不存在")

    if from_dict.has_key('OTNM'):
        TradeContext.OTNM = from_dict['OTNM']
        AfaLoggerFunc.tradeDebug('TradeContext.OTNM = ' + str(TradeContext.OTNM))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['OTNM']不存在")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['DASQ']不存在")

    if from_dict.has_key('MGID'):
        TradeContext.MGID = from_dict['MGID']
        AfaLoggerFunc.tradeDebug('TradeContext.MGID = ' + str(TradeContext.MGID))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['MGID']不存在")

    if from_dict.has_key('PRCCO'):
        TradeContext.PRCCO = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.PRCCO = ' + str(TradeContext.PRCCO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['PRCCO']不存在")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['STRINFO']不存在")

    if from_dict.has_key('BCSTAT'):
        TradeContext.BCSTAT = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BCSTAT = ' + str(TradeContext.BCSTAT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BCSTAT']不存在")

    if from_dict.has_key('BDWFLG'):
        TradeContext.BDWFLG = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BDWFLG = ' + str(TradeContext.BDWFLG))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BDWFLG']不存在")

    if from_dict.has_key('PRTCNT'):
        TradeContext.PRTCNT = from_dict['PRTCNT']
        AfaLoggerFunc.tradeDebug('TradeContext.PRTCNT = ' + str(TradeContext.PRTCNT))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['PRTCNT']不存在")

    if from_dict.has_key('BJETIM'):
        TradeContext.BJETIM = from_dict['BJETIM']
        AfaLoggerFunc.tradeDebug('TradeContext.BJETIM = ' + str(TradeContext.BJETIM))
    else:
        AfaLoggerFunc.tradeDebug("TransTrc['BJETIM']不存在")

    

    return True

