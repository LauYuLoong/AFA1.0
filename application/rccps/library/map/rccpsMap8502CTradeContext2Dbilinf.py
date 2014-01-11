# -*- coding: gbk -*-
##################################################################
#   农信银系统 TradeContext 字典到 bilinf 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap8502CTradeContext2Dbilinf.py
#   修改时间:   Thu Jun 19 11:48:55 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BILVER'):
        to_dict['BILVER'] = TradeContext.BILVER
        AfaLoggerFunc.tradeDebug('bilinf[BILVER] = ' + str(to_dict['BILVER']))
    else:
        AfaLoggerFunc.tradeWarn("汇票版本号不能为空")
        return False

    if TradeContext.existVariable('BILNO'):
        to_dict['BILNO'] = TradeContext.BILNO
        AfaLoggerFunc.tradeDebug('bilinf[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeWarn("汇票号码不能为空")
        return False

    if TradeContext.existVariable('BILRS'):
        to_dict['BILRS'] = TradeContext.BILRS
        AfaLoggerFunc.tradeDebug('bilinf[BILRS] = ' + str(to_dict['BILRS']))
    else:
        AfaLoggerFunc.tradeWarn("汇票往来标识不能为空")
        return False

    if TradeContext.existVariable('BILTYP'):
        to_dict['BILTYP'] = TradeContext.BILTYP
        AfaLoggerFunc.tradeDebug('bilinf[BILTYP] = ' + str(to_dict['BILTYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILTYP不存在")

    if TradeContext.existVariable('BILDAT'):
        to_dict['BILDAT'] = TradeContext.BILDAT
        AfaLoggerFunc.tradeDebug('bilinf[BILDAT] = ' + str(to_dict['BILDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILDAT不存在")

    if TradeContext.existVariable('PAYWAY'):
        to_dict['PAYWAY'] = TradeContext.PAYWAY
        AfaLoggerFunc.tradeDebug('bilinf[PAYWAY] = ' + str(to_dict['PAYWAY']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PAYWAY不存在")

    if TradeContext.existVariable('REMBNKCO'):
        to_dict['REMBNKCO'] = TradeContext.REMBNKCO
        AfaLoggerFunc.tradeDebug('bilinf[REMBNKCO] = ' + str(to_dict['REMBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.REMBNKCO不存在")

    if TradeContext.existVariable('REMBNKNM'):
        to_dict['REMBNKNM'] = TradeContext.REMBNKNM
        AfaLoggerFunc.tradeDebug('bilinf[REMBNKNM] = ' + str(to_dict['REMBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.REMBNKNM不存在")

    if TradeContext.existVariable('PAYBNKCO'):
        to_dict['PAYBNKCO'] = TradeContext.PAYBNKCO
        AfaLoggerFunc.tradeDebug('bilinf[PAYBNKCO] = ' + str(to_dict['PAYBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PAYBNKCO不存在")

    if TradeContext.existVariable('PAYBNKNM'):
        to_dict['PAYBNKNM'] = TradeContext.PAYBNKNM
        AfaLoggerFunc.tradeDebug('bilinf[PAYBNKNM] = ' + str(to_dict['PAYBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PAYBNKNM不存在")

    if TradeContext.existVariable('PYRACC'):
        to_dict['PYRACC'] = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug('bilinf[PYRACC] = ' + str(to_dict['PYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRACC不存在")

    if TradeContext.existVariable('PYRNAM'):
        to_dict['PYRNAM'] = TradeContext.PYRNAM
        AfaLoggerFunc.tradeDebug('bilinf[PYRNAM] = ' + str(to_dict['PYRNAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRNAM不存在")

    if TradeContext.existVariable('PYRADDR'):
        to_dict['PYRADDR'] = TradeContext.PYRADDR
        AfaLoggerFunc.tradeDebug('bilinf[PYRADDR] = ' + str(to_dict['PYRADDR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRADDR不存在")

    if TradeContext.existVariable('PYEACC'):
        to_dict['PYEACC'] = TradeContext.PYEACC
        AfaLoggerFunc.tradeDebug('bilinf[PYEACC] = ' + str(to_dict['PYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYEACC不存在")

    if TradeContext.existVariable('PYENAM'):
        to_dict['PYENAM'] = TradeContext.PYENAM
        AfaLoggerFunc.tradeDebug('bilinf[PYENAM] = ' + str(to_dict['PYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYENAM不存在")

    if TradeContext.existVariable('PYEADDR'):
        to_dict['PYEADDR'] = TradeContext.PYEADDR
        AfaLoggerFunc.tradeDebug('bilinf[PYEADDR] = ' + str(to_dict['PYEADDR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYEADDR不存在")

    if TradeContext.existVariable('PYHACC'):
        to_dict['PYHACC'] = TradeContext.PYHACC
        AfaLoggerFunc.tradeDebug('bilinf[PYHACC] = ' + str(to_dict['PYHACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYHACC不存在")

    if TradeContext.existVariable('PYHNAM'):
        to_dict['PYHNAM'] = TradeContext.PYHNAM
        AfaLoggerFunc.tradeDebug('bilinf[PYHNAM] = ' + str(to_dict['PYHNAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYHNAM不存在")

    if TradeContext.existVariable('PYHADDR'):
        to_dict['PYHADDR'] = TradeContext.PYHADDR
        AfaLoggerFunc.tradeDebug('bilinf[PYHADDR] = ' + str(to_dict['PYHADDR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYHADDR不存在")

    if TradeContext.existVariable('PYITYP'):
        to_dict['PYITYP'] = TradeContext.PYITYP
        AfaLoggerFunc.tradeDebug('bilinf[PYITYP] = ' + str(to_dict['PYITYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYITYP不存在")

    if TradeContext.existVariable('PYIACC'):
        to_dict['PYIACC'] = TradeContext.PYIACC
        AfaLoggerFunc.tradeDebug('bilinf[PYIACC] = ' + str(to_dict['PYIACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYIACC不存在")

    if TradeContext.existVariable('PYINAM'):
        to_dict['PYINAM'] = TradeContext.PYINAM
        AfaLoggerFunc.tradeDebug('bilinf[PYINAM] = ' + str(to_dict['PYINAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYINAM不存在")

    if TradeContext.existVariable('BILAMT'):
        to_dict['BILAMT'] = TradeContext.BILAMT
        AfaLoggerFunc.tradeDebug('bilinf[BILAMT] = ' + str(to_dict['BILAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILAMT不存在")

    if TradeContext.existVariable('OCCAMT'):
        to_dict['OCCAMT'] = TradeContext.OCCAMT
        AfaLoggerFunc.tradeDebug('bilinf[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OCCAMT不存在")

    if TradeContext.existVariable('RMNAMT'):
        to_dict['RMNAMT'] = TradeContext.RMNAMT
        AfaLoggerFunc.tradeDebug('bilinf[RMNAMT] = ' + str(to_dict['RMNAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RMNAMT不存在")

    if TradeContext.existVariable('CUR'):
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('bilinf[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR不存在")

    if TradeContext.existVariable('SEAL'):
        to_dict['SEAL'] = TradeContext.SEAL
        AfaLoggerFunc.tradeDebug('bilinf[SEAL] = ' + str(to_dict['SEAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SEAL不存在")

    if TradeContext.existVariable('USE'):
        to_dict['USE'] = TradeContext.USE
        AfaLoggerFunc.tradeDebug('bilinf[USE] = ' + str(to_dict['USE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.USE不存在")

    if TradeContext.existVariable('REMARK'):
        to_dict['REMARK'] = TradeContext.REMARK
        AfaLoggerFunc.tradeDebug('bilinf[REMARK] = ' + str(to_dict['REMARK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.REMARK不存在")

    if TradeContext.existVariable('HPCUSQ'):
        to_dict['HPCUSQ'] = TradeContext.HPCUSQ
        AfaLoggerFunc.tradeDebug('bilinf[HPCUSQ] = ' + str(to_dict['HPCUSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.HPCUSQ不存在")

    if TradeContext.existVariable('HPSTAT'):
        to_dict['HPSTAT'] = TradeContext.HPSTAT
        AfaLoggerFunc.tradeDebug('bilinf[HPSTAT] = ' + str(to_dict['HPSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.HPSTAT不存在")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('bilinf[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1不存在")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('bilinf[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2不存在")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('bilinf[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3不存在")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('bilinf[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4不存在")

    return True

