# -*- coding: gbk -*-
##################################################################
#   农信银系统 trcbka_dict 字典到 trccan_dict 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap8507Dtrcbka_dict2Dtrccan_dict.py
#   修改时间:   Wed Jun 11 15:14:44 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BRSFLG'):
        to_dict['BRSFLG'] = from_dict['BRSFLG']
        AfaLoggerFunc.tradeInfo('to_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeWarn("往来标志不可为空")
        return False

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeInfo('to_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['BEAUUS']不存在")

    if from_dict.has_key('NCCWKDAT'):
        to_dict['NCCWKDAT'] = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeInfo('to_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeWarn("中心日期不可为空")
        return False

    if from_dict.has_key('TRCCO'):
        to_dict['ORTRCCO'] = from_dict['TRCCO']
        AfaLoggerFunc.tradeInfo('to_dict[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeWarn("原交易代码不可为空")
        return False

    if from_dict.has_key('TRCDAT'):
        to_dict['TRCDAT'] = from_dict['TRCDAT']
        AfaLoggerFunc.tradeInfo('to_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['TRCDAT']不存在")

    if from_dict.has_key('TRCNO'):
        to_dict['TRCNO'] = from_dict['TRCNO']
        AfaLoggerFunc.tradeInfo('to_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['TRCNO']不存在")

    if from_dict.has_key('SNDBNKCO'):
        to_dict['SNDBNKCO'] = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeInfo('to_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['SNDBNKCO']不存在")

    if from_dict.has_key('SNDBNKNM'):
        to_dict['SNDBNKNM'] = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeInfo('to_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['SNDBNKNM']不存在")

    if from_dict.has_key('RCVBNKCO'):
        to_dict['RCVBNKCO'] = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeInfo('to_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['RCVBNKCO']不存在")

    if from_dict.has_key('RCVBNKNM'):
        to_dict['RCVBNKNM'] = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeInfo('to_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['RCVBNKNM']不存在")

    if from_dict.has_key('BJEDTE'):
        to_dict['BOJEDT'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeInfo('to_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeWarn("原交易日期不可为空")
        return False

    if from_dict.has_key('BSPSQN'):
        to_dict['BOSPSQ'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeInfo('to_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeWarn("原报单序号不可为空")
        return False

    if from_dict.has_key('CUR'):
        to_dict['CUR'] = from_dict['CUR']
        AfaLoggerFunc.tradeInfo('to_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeWarn("币种不可为空")
        return False

    if from_dict.has_key('OCCAMT'):
        to_dict['OCCAMT'] = from_dict['OCCAMT']
        AfaLoggerFunc.tradeInfo('to_dict[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeWarn("交易金额不可为空")
        return False

    if from_dict.has_key('CLRESPN'):
        to_dict['CLRESPN'] = from_dict['CLRESPN']
        AfaLoggerFunc.tradeInfo('to_dict[CLRESPN] = ' + str(to_dict['CLRESPN']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['CLRESPN']不存在")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeInfo('to_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['NOTE1']不存在")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeInfo('to_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['NOTE2']不存在")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeInfo('to_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['NOTE3']不存在")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeInfo('to_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeWarn("trcbka_dict['NOTE4']不存在")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeInfo('to_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeWarn("机构号不可为空")
        return False

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeInfo('to_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeWarn("柜员号不可为空")
        return False

    return True

