# -*- coding: gbk -*-
##################################################################
#   农信银系统 TradeContext 字典到 pjcbka_dict 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap1126CTradeContext2Dpjcbka_dict.py
#   修改时间:   Mon Jul 28 18:16:33 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BJEDTE不存在")
        return False

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BSPSQN不存在")
        return False

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRSFLG不存在")
        return False

    if TradeContext.existVariable('BESBNO'):
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBNO不存在")

    if TradeContext.existVariable('BETELR'):
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BETELR不存在")

    if TradeContext.existVariable('BEAUUS'):
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS不存在")

    if TradeContext.existVariable('NCCworkDate'):
        to_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        AfaLoggerFunc.tradeDebug('pjcbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCworkDate不存在")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO不存在")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('pjcbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT不存在")

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO不存在")

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO不存在")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO不存在")

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('pjcbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM不存在")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO不存在")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO不存在")

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('pjcbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM不存在")

    if TradeContext.existVariable('BOJEDT'):
        to_dict['BOJEDT'] = TradeContext.BOJEDT
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOJEDT不存在")

    if TradeContext.existVariable('BOSPSQ'):
        to_dict['BOSPSQ'] = TradeContext.BOSPSQ
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOSPSQ不存在")

    if TradeContext.existVariable('ORTRCCO'):
        to_dict['ORTRCCO'] = TradeContext.ORTRCCO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCCO不存在")

    if TradeContext.existVariable('BILDAT'):
        to_dict['BILDAT'] = TradeContext.BILDAT
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BILDAT] = ' + str(to_dict['BILDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILDAT不存在")

    if TradeContext.existVariable('BILNO'):
        to_dict['BILNO'] = TradeContext.BILNO
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILNO不存在")

    if TradeContext.existVariable('BILPNAM'):
        to_dict['BILPNAM'] = TradeContext.BILPNAM
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BILPNAM] = ' + str(to_dict['BILPNAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILPNAM不存在")

    if TradeContext.existVariable('BILENDDT'):
        to_dict['BILENDDT'] = TradeContext.BILENDDT
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BILENDDT] = ' + str(to_dict['BILENDDT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILENDDT不存在")

    if TradeContext.existVariable('BILAMT'):
        to_dict['BILAMT'] = TradeContext.BILAMT
        AfaLoggerFunc.tradeDebug('pjcbka_dict[BILAMT] = ' + str(to_dict['BILAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILAMT不存在")

    if TradeContext.existVariable('PYENAM'):
        to_dict['PYENAM'] = TradeContext.PYENAM
        AfaLoggerFunc.tradeDebug('pjcbka_dict[PYENAM] = ' + str(to_dict['PYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYENAM不存在")

    if TradeContext.existVariable('HONBNKNM'):
        to_dict['HONBNKNM'] = TradeContext.HONBNKNM
        AfaLoggerFunc.tradeDebug('pjcbka_dict[HONBNKNM] = ' + str(to_dict['HONBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.HONBNKNM不存在")

    if TradeContext.existVariable('CONT'):
        to_dict['CONT'] = TradeContext.CONT
        AfaLoggerFunc.tradeDebug('pjcbka_dict[CONT] = ' + str(to_dict['CONT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CONT不存在")

    if TradeContext.existVariable('ISDEAL'):
        to_dict['ISDEAL'] = TradeContext.ISDEAL
        AfaLoggerFunc.tradeDebug('pjcbka_dict[ISDEAL] = ' + str(to_dict['ISDEAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ISDEAL不存在")
        return False

    return True

