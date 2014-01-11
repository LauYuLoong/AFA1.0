# -*- coding: gbk -*-
##################################################################
#   农信银系统 TradeContext 字典到 rekbal_dict 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap8557CTradeContext2Drekbal_dict.py
#   修改时间:   Fri Jul 25 14:36:28 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('rekbal_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BJEDTE不存在")
        return False

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('rekbal_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BSPSQN不存在")
        return False

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('rekbal_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRSFLG不存在")

    if TradeContext.existVariable('BOJEDT'):
        to_dict['BOJEDT'] = TradeContext.BOJEDT
        AfaLoggerFunc.tradeDebug('rekbal_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOJEDT不存在")
        return False

    if TradeContext.existVariable('BOSPSQ'):
        to_dict['BOSPSQ'] = TradeContext.BOSPSQ
        AfaLoggerFunc.tradeDebug('rekbal_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOSPSQ不存在")
        return False

    if TradeContext.existVariable('NCCworkDate'):
        to_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        AfaLoggerFunc.tradeDebug('rekbal_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCworkDate不存在")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('rekbal_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT不存在")

    if TradeContext.existVariable('SerialNo'):
        to_dict['TRCNO'] = TradeContext.SerialNo
        AfaLoggerFunc.tradeDebug('rekbal_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SerialNo不存在")

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('rekbal_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO不存在")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('rekbal_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO不存在")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('rekbal_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO不存在")
    
    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('rekbal_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM不存在")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('rekbal_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO不存在")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('rekbal_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO不存在")
        
    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('rekbal_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM不存在")

    if TradeContext.existVariable('CUR'):
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('rekbal_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR不存在")

    if TradeContext.existVariable('LBDCFLG'):
        to_dict['LBDCFLG'] = TradeContext.LBDCFLG
        AfaLoggerFunc.tradeDebug('rekbal_dict[LBDCFLG] = ' + str(to_dict['LBDCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.LBDCFLG不存在")

    if TradeContext.existVariable('LSTDTBAL'):
        to_dict['LSTDTBAL'] = TradeContext.LSTDTBAL
        AfaLoggerFunc.tradeDebug('rekbal_dict[LSTDTBAL] = ' + str(to_dict['LSTDTBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.LSTDTBAL不存在")

    if TradeContext.existVariable('NTTDCFLG'):
        to_dict['NTTDCFLG'] = TradeContext.NTTDCFLG
        AfaLoggerFunc.tradeDebug('rekbal_dict[NTTDCFLG] = ' + str(to_dict['NTTDCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NTTDCFLG不存在")

    if TradeContext.existVariable('NTTBAL'):
        to_dict['NTTBAL'] = TradeContext.NTTBAL
        AfaLoggerFunc.tradeDebug('rekbal_dict[NTTBAL] = ' + str(to_dict['NTTBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NTTBAL不存在")

    if TradeContext.existVariable('BALDCFLG'):
        to_dict['BALDCFLG'] = TradeContext.BALDCFLG
        AfaLoggerFunc.tradeDebug('rekbal_dict[BALDCFLG] = ' + str(to_dict['BALDCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BALDCFLG不存在")

    if TradeContext.existVariable('TODAYBAL'):
        to_dict['TODAYBAL'] = TradeContext.TODAYBAL
        AfaLoggerFunc.tradeDebug('rekbal_dict[TODAYBAL] = ' + str(to_dict['TODAYBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TODAYBAL不存在")

    if TradeContext.existVariable('AVLBAL'):
        to_dict['AVLBAL'] = TradeContext.AVLBAL
        AfaLoggerFunc.tradeDebug('rekbal_dict[AVLBAL] = ' + str(to_dict['AVLBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.AVLBAL不存在")

    if TradeContext.existVariable('NTODAYBAL'):
        to_dict['NTODAYBAL'] = TradeContext.NTODAYBAL
        AfaLoggerFunc.tradeDebug('rekbal_dict[NTODAYBAL] = ' + str(to_dict['NTODAYBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NTODAYBAL不存在")

    if TradeContext.existVariable('CHKRST'):
        to_dict['CHKRST'] = TradeContext.CHKRST
        AfaLoggerFunc.tradeDebug('rekbal_dict[CHKRST] = ' + str(to_dict['CHKRST']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CHKRST不存在")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('rekbal_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1不存在")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('rekbal_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2不存在")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('rekbal_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3不存在")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('rekbal_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4不存在")

    return True

