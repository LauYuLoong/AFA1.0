# -*- coding: gbk -*-
##################################################################
#   农信银系统 trcbka 字典到 TradeContext 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap0000Dtrcbka2CTradeContext.py
#   修改时间:   Wed Jun  4 17:58:30 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BJEDTE']不存在")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BSPSQN']不存在")

    if from_dict.has_key('BRSFLG'):
        TradeContext.BRSFLG = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BRSFLG = ' + str(TradeContext.BRSFLG))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BRSFLG']不存在")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BESBNO']不存在")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BEACSB']不存在")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BETELR']不存在")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BEAUUS']不存在")

    if from_dict.has_key('TERMID'):
        TradeContext.TERMID = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('TradeContext.TERMID = ' + str(TradeContext.TERMID))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['TERMID']不存在")

    if from_dict.has_key('BBSSRC'):
        TradeContext.BBSSRC = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('TradeContext.BBSSRC = ' + str(TradeContext.BBSSRC))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BBSSRC']不存在")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['DASQ']不存在")

    if from_dict.has_key('DCFLG'):
        TradeContext.DCFLG = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.DCFLG = ' + str(TradeContext.DCFLG))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['DCFLG']不存在")

    if from_dict.has_key('OPRNO'):
        TradeContext.OPRNO = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRNO = ' + str(TradeContext.OPRNO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['OPRNO']不存在")

    if from_dict.has_key('OPRATTNO'):
        TradeContext.OPRATTNO = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRATTNO = ' + str(TradeContext.OPRATTNO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['OPRATTNO']不存在")

    if from_dict.has_key('NCCWKDAT'):
        TradeContext.NCCWKDAT = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.NCCWKDAT = ' + str(TradeContext.NCCWKDAT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NCCWKDAT']不存在")

    if from_dict.has_key('TRCCO'):
        TradeContext.TRCCO = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCCO = ' + str(TradeContext.TRCCO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['TRCCO']不存在")

    if from_dict.has_key('TRCDAT'):
        TradeContext.TRCDAT = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCDAT = ' + str(TradeContext.TRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['TRCDAT']不存在")

    if from_dict.has_key('TRCNO'):
        TradeContext.TRCNO = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCNO = ' + str(TradeContext.TRCNO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['TRCNO']不存在")

    if from_dict.has_key('SNDMBRCO'):
        TradeContext.SNDMBRCO = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDMBRCO = ' + str(TradeContext.SNDMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['SNDMBRCO']不存在")

    if from_dict.has_key('RCVMBRCO'):
        TradeContext.RCVMBRCO = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVMBRCO = ' + str(TradeContext.RCVMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['RCVMBRCO']不存在")

    if from_dict.has_key('SNDBNKCO'):
        TradeContext.SNDBNKCO = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKCO = ' + str(TradeContext.SNDBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['SNDBNKCO']不存在")

    if from_dict.has_key('SNDBNKNM'):
        TradeContext.SNDBNKNM = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKNM = ' + str(TradeContext.SNDBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['SNDBNKNM']不存在")

    if from_dict.has_key('RCVBNKCO'):
        TradeContext.RCVBNKCO = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKCO = ' + str(TradeContext.RCVBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['RCVBNKCO']不存在")

    if from_dict.has_key('RCVBNKNM'):
        TradeContext.RCVBNKNM = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKNM = ' + str(TradeContext.RCVBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['RCVBNKNM']不存在")

    if from_dict.has_key('CUR'):
        TradeContext.CUR = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('TradeContext.CUR = ' + str(TradeContext.CUR))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CUR']不存在")

    if from_dict.has_key('OCCAMT'):
        TradeContext.OCCAMT = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.OCCAMT = ' + str(TradeContext.OCCAMT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['OCCAMT']不存在")

    if from_dict.has_key('CHRGTYP'):
        TradeContext.CHRGTYP = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.CHRGTYP = ' + str(TradeContext.CHRGTYP))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CHRGTYP']不存在")

    if from_dict.has_key('LOCCUSCHRG'):
        TradeContext.LOCCUSCHRG = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('TradeContext.LOCCUSCHRG = ' + str(TradeContext.LOCCUSCHRG))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['LOCCUSCHRG']不存在")

    if from_dict.has_key('CUSCHRG'):
        TradeContext.CUSCHRG = from_dict['CUSCHRG']
        AfaLoggerFunc.tradeDebug('TradeContext.CUSCHRG = ' + str(TradeContext.CUSCHRG))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CUSCHRG']不存在")

    if from_dict.has_key('PYRACC'):
        TradeContext.PYRACC = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRACC = ' + str(TradeContext.PYRACC))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYRACC']不存在")

    if from_dict.has_key('PYRNAM'):
        TradeContext.PYRNAM = from_dict['PYRNAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRNAM = ' + str(TradeContext.PYRNAM))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYRNAM']不存在")

    if from_dict.has_key('PYRADDR'):
        TradeContext.PYRADDR = from_dict['PYRADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYRADDR = ' + str(TradeContext.PYRADDR))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYRADDR']不存在")

    if from_dict.has_key('PYEACC'):
        TradeContext.PYEACC = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEACC = ' + str(TradeContext.PYEACC))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYEACC']不存在")

    if from_dict.has_key('PYENAM'):
        TradeContext.PYENAM = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('TradeContext.PYENAM = ' + str(TradeContext.PYENAM))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYENAM']不存在")

    if from_dict.has_key('PYEADDR'):
        TradeContext.PYEADDR = from_dict['PYEADDR']
        AfaLoggerFunc.tradeDebug('TradeContext.PYEADDR = ' + str(TradeContext.PYEADDR))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['PYEADDR']不存在")

    if from_dict.has_key('SEAL'):
        TradeContext.SEAL = from_dict['SEAL']
        AfaLoggerFunc.tradeDebug('TradeContext.SEAL = ' + str(TradeContext.SEAL))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['SEAL']不存在")

    if from_dict.has_key('USE'):
        TradeContext.USE = from_dict['USE']
        AfaLoggerFunc.tradeDebug('TradeContext.USE = ' + str(TradeContext.USE))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['USE']不存在")

    if from_dict.has_key('REMARK'):
        TradeContext.REMARK = from_dict['REMARK']
        AfaLoggerFunc.tradeDebug('TradeContext.REMARK = ' + str(TradeContext.REMARK))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['REMARK']不存在")

    if from_dict.has_key('BILTYP'):
        TradeContext.BILTYP = from_dict['BILTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.BILTYP = ' + str(TradeContext.BILTYP))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BILTYP']不存在")

    if from_dict.has_key('BILDAT'):
        TradeContext.BILDAT = from_dict['BILDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.BILDAT = ' + str(TradeContext.BILDAT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BILDAT']不存在")

    if from_dict.has_key('BILNO'):
        TradeContext.BILNO = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BILNO = ' + str(TradeContext.BILNO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BILNO']不存在")

    if from_dict.has_key('COMAMT'):
        TradeContext.COMAMT = from_dict['COMAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.COMAMT = ' + str(TradeContext.COMAMT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['COMAMT']不存在")

    if from_dict.has_key('OVPAYAMT'):
        TradeContext.OVPAYAMT = from_dict['OVPAYAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.OVPAYAMT = ' + str(TradeContext.OVPAYAMT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['OVPAYAMT']不存在")

    if from_dict.has_key('CPSAMT'):
        TradeContext.CPSAMT = from_dict['CPSAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.CPSAMT = ' + str(TradeContext.CPSAMT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CPSAMT']不存在")

    if from_dict.has_key('RFUAMT'):
        TradeContext.RFUAMT = from_dict['RFUAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.RFUAMT = ' + str(TradeContext.RFUAMT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['RFUAMT']不存在")

    if from_dict.has_key('CERTTYPE'):
        TradeContext.CERTTYPE = from_dict['CERTTYPE']
        AfaLoggerFunc.tradeDebug('TradeContext.CERTTYPE = ' + str(TradeContext.CERTTYPE))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CERTTYPE']不存在")

    if from_dict.has_key('CERTNO'):
        TradeContext.CERTNO = from_dict['CERTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.CERTNO = ' + str(TradeContext.CERTNO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['CERTNO']不存在")

    if from_dict.has_key('BOJEDT'):
        TradeContext.BOJEDT = from_dict['BOJEDT']
        AfaLoggerFunc.tradeDebug('TradeContext.BOJEDT = ' + str(TradeContext.BOJEDT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BOJEDT']不存在")

    if from_dict.has_key('BOSPSQ'):
        TradeContext.BOSPSQ = from_dict['BOSPSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.BOSPSQ = ' + str(TradeContext.BOSPSQ))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['BOSPSQ']不存在")

    if from_dict.has_key('ORTRCDAT'):
        TradeContext.ORTRCDAT = from_dict['ORTRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCDAT = ' + str(TradeContext.ORTRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORTRCDAT']不存在")

    if from_dict.has_key('ORTRCCO'):
        TradeContext.ORTRCCO = from_dict['ORTRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCCO = ' + str(TradeContext.ORTRCCO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORTRCCO']不存在")

    if from_dict.has_key('ORTRCNO'):
        TradeContext.ORTRCNO = from_dict['ORTRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCNO = ' + str(TradeContext.ORTRCNO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORTRCNO']不存在")

    if from_dict.has_key('ORSNDBNK'):
        TradeContext.ORSNDBNK = from_dict['ORSNDBNK']
        AfaLoggerFunc.tradeDebug('TradeContext.ORSNDBNK = ' + str(TradeContext.ORSNDBNK))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORSNDBNK']不存在")

    if from_dict.has_key('ORRCVBNK'):
        TradeContext.ORRCVBNK = from_dict['ORRCVBNK']
        AfaLoggerFunc.tradeDebug('TradeContext.ORRCVBNK = ' + str(TradeContext.ORRCVBNK))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['ORRCVBNK']不存在")

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['STRINFO']不存在")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NOTE1']不存在")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NOTE2']不存在")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NOTE3']不存在")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("trcbka['NOTE4']不存在")

    return True

