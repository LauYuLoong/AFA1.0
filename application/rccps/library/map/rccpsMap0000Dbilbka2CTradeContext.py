# -*- coding: gbk -*-
##################################################################
#   农信银系统 bilbka 字典到 TradeContext 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap0000Dbilbka2CTradeContext.py
#   修改时间:   Thu Sep 18 11:01:53 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BJEDTE']不存在")

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BSPSQN']不存在")

    if from_dict.has_key('BRSFLG'):
        TradeContext.BRSFLG = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BRSFLG = ' + str(TradeContext.BRSFLG))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BRSFLG']不存在")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BESBNO']不存在")

    if from_dict.has_key('BEACSB'):
        TradeContext.BEACSB = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('TradeContext.BEACSB = ' + str(TradeContext.BEACSB))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEACSB']不存在")

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BETELR']不存在")

    if from_dict.has_key('BEAUUS'):
        TradeContext.BEAUUS = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUUS = ' + str(TradeContext.BEAUUS))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEAUUS']不存在")

    if from_dict.has_key('BEAUPS'):
        TradeContext.BEAUPS = from_dict['BEAUPS']
        AfaLoggerFunc.tradeDebug('TradeContext.BEAUPS = ' + str(TradeContext.BEAUPS))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEAUPS']不存在")

    if from_dict.has_key('TERMID'):
        TradeContext.TERMID = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('TradeContext.TERMID = ' + str(TradeContext.TERMID))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TERMID']不存在")

    if from_dict.has_key('BBSSRC'):
        TradeContext.BBSSRC = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('TradeContext.BBSSRC = ' + str(TradeContext.BBSSRC))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BBSSRC']不存在")

    if from_dict.has_key('DASQ'):
        TradeContext.DASQ = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('TradeContext.DASQ = ' + str(TradeContext.DASQ))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['DASQ']不存在")

    if from_dict.has_key('DCFLG'):
        TradeContext.DCFLG = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.DCFLG = ' + str(TradeContext.DCFLG))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['DCFLG']不存在")

    if from_dict.has_key('OPRNO'):
        TradeContext.OPRNO = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRNO = ' + str(TradeContext.OPRNO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['OPRNO']不存在")

    if from_dict.has_key('OPRATTNO'):
        TradeContext.OPRATTNO = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRATTNO = ' + str(TradeContext.OPRATTNO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['OPRATTNO']不存在")

    if from_dict.has_key('NCCWKDAT'):
        TradeContext.NCCWKDAT = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.NCCWKDAT = ' + str(TradeContext.NCCWKDAT))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NCCWKDAT']不存在")

    if from_dict.has_key('TRCCO'):
        TradeContext.TRCCO = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCCO = ' + str(TradeContext.TRCCO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCCO']不存在")

    if from_dict.has_key('TRCDAT'):
        TradeContext.TRCDAT = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCDAT = ' + str(TradeContext.TRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCDAT']不存在")

    if from_dict.has_key('TRCNO'):
        TradeContext.TRCNO = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCNO = ' + str(TradeContext.TRCNO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCNO']不存在")

    if from_dict.has_key('SNDMBRCO'):
        TradeContext.SNDMBRCO = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDMBRCO = ' + str(TradeContext.SNDMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDMBRCO']不存在")

    if from_dict.has_key('RCVMBRCO'):
        TradeContext.RCVMBRCO = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVMBRCO = ' + str(TradeContext.RCVMBRCO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVMBRCO']不存在")

    if from_dict.has_key('SNDBNKCO'):
        TradeContext.SNDBNKCO = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKCO = ' + str(TradeContext.SNDBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDBNKCO']不存在")

    if from_dict.has_key('SNDBNKNM'):
        TradeContext.SNDBNKNM = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBNKNM = ' + str(TradeContext.SNDBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDBNKNM']不存在")

    if from_dict.has_key('RCVBNKCO'):
        TradeContext.RCVBNKCO = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKCO = ' + str(TradeContext.RCVBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVBNKCO']不存在")

    if from_dict.has_key('RCVBNKNM'):
        TradeContext.RCVBNKNM = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVBNKNM = ' + str(TradeContext.RCVBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVBNKNM']不存在")

    if from_dict.has_key('BILVER'):
        TradeContext.BILVER = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('TradeContext.BILVER = ' + str(TradeContext.BILVER))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILVER']不存在")

    if from_dict.has_key('BILNO'):
        TradeContext.BILNO = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BILNO = ' + str(TradeContext.BILNO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILNO']不存在")

    if from_dict.has_key('CHRGTYP'):
        TradeContext.CHRGTYP = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.CHRGTYP = ' + str(TradeContext.CHRGTYP))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CHRGTYP']不存在")

    if from_dict.has_key('LOCCUSCHRG'):
        TradeContext.LOCCUSCHRG = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('TradeContext.LOCCUSCHRG = ' + str(TradeContext.LOCCUSCHRG))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['LOCCUSCHRG']不存在")

    if from_dict.has_key('BILRS'):
        TradeContext.BILRS = from_dict['BILRS']
        AfaLoggerFunc.tradeDebug('TradeContext.BILRS = ' + str(TradeContext.BILRS))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILRS']不存在")

    if from_dict.has_key('HPCUSQ'):
        TradeContext.HPCUSQ = from_dict['HPCUSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.HPCUSQ = ' + str(TradeContext.HPCUSQ))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['HPCUSQ']不存在")

    if from_dict.has_key('HPSTAT'):
        TradeContext.HPSTAT = from_dict['HPSTAT']
        AfaLoggerFunc.tradeDebug('TradeContext.HPSTAT = ' + str(TradeContext.HPSTAT))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['HPSTAT']不存在")

    if from_dict.has_key('CERTTYPE'):
        TradeContext.CERTTYPE = from_dict['CERTTYPE']
        AfaLoggerFunc.tradeDebug('TradeContext.CERTTYPE = ' + str(TradeContext.CERTTYPE))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CERTTYPE']不存在")

    if from_dict.has_key('CERTNO'):
        TradeContext.CERTNO = from_dict['CERTNO']
        AfaLoggerFunc.tradeDebug('TradeContext.CERTNO = ' + str(TradeContext.CERTNO))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CERTNO']不存在")

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE1']不存在")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE2']不存在")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE3']不存在")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE4']不存在")

    return True

