# -*- coding: gbk -*-
##################################################################
#   农信银系统 bil_dict 字典到 bilinf 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap0000Dbil_dict2Dbilinf.py
#   修改时间:   Thu Jun 19 11:49:53 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BILVER'):
        to_dict['BILVER'] = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('bilinf[BILVER] = ' + str(to_dict['BILVER']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILVER']不存在")

    if from_dict.has_key('BILNO'):
        to_dict['BILNO'] = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('bilinf[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILNO']不存在")

    if from_dict.has_key('BILRS'):
        to_dict['BILRS'] = from_dict['BILRS']
        AfaLoggerFunc.tradeDebug('bilinf[BILRS] = ' + str(to_dict['BILRS']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILRS']不存在")

    if from_dict.has_key('BILTYP'):
        to_dict['BILTYP'] = from_dict['BILTYP']
        AfaLoggerFunc.tradeDebug('bilinf[BILTYP] = ' + str(to_dict['BILTYP']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILTYP']不存在")

    if from_dict.has_key('BILDAT'):
        to_dict['BILDAT'] = from_dict['BILDAT']
        AfaLoggerFunc.tradeDebug('bilinf[BILDAT] = ' + str(to_dict['BILDAT']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILDAT']不存在")

    if from_dict.has_key('PAYWAY'):
        to_dict['PAYWAY'] = from_dict['PAYWAY']
        AfaLoggerFunc.tradeDebug('bilinf[PAYWAY] = ' + str(to_dict['PAYWAY']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PAYWAY']不存在")

    if from_dict.has_key('REMBNKCO'):
        to_dict['REMBNKCO'] = from_dict['REMBNKCO']
        AfaLoggerFunc.tradeDebug('bilinf[REMBNKCO] = ' + str(to_dict['REMBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['REMBNKCO']不存在")

    if from_dict.has_key('REMBNKNM'):
        to_dict['REMBNKNM'] = from_dict['REMBNKNM']
        AfaLoggerFunc.tradeDebug('bilinf[REMBNKNM] = ' + str(to_dict['REMBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['REMBNKNM']不存在")

    if from_dict.has_key('PAYBNKCO'):
        to_dict['PAYBNKCO'] = from_dict['PAYBNKCO']
        AfaLoggerFunc.tradeDebug('bilinf[PAYBNKCO] = ' + str(to_dict['PAYBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PAYBNKCO']不存在")

    if from_dict.has_key('PAYBNKNM'):
        to_dict['PAYBNKNM'] = from_dict['PAYBNKNM']
        AfaLoggerFunc.tradeDebug('bilinf[PAYBNKNM] = ' + str(to_dict['PAYBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PAYBNKNM']不存在")

    if from_dict.has_key('PYRACC'):
        to_dict['PYRACC'] = from_dict['PYRACC']
        AfaLoggerFunc.tradeDebug('bilinf[PYRACC] = ' + str(to_dict['PYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYRACC']不存在")

    if from_dict.has_key('PYRNAM'):
        to_dict['PYRNAM'] = from_dict['PYRNAM']
        AfaLoggerFunc.tradeDebug('bilinf[PYRNAM] = ' + str(to_dict['PYRNAM']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYRNAM']不存在")

    if from_dict.has_key('PYRADDR'):
        to_dict['PYRADDR'] = from_dict['PYRADDR']
        AfaLoggerFunc.tradeDebug('bilinf[PYRADDR] = ' + str(to_dict['PYRADDR']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYRADDR']不存在")

    if from_dict.has_key('PYEACC'):
        to_dict['PYEACC'] = from_dict['PYEACC']
        AfaLoggerFunc.tradeDebug('bilinf[PYEACC] = ' + str(to_dict['PYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYEACC']不存在")

    if from_dict.has_key('PYENAM'):
        to_dict['PYENAM'] = from_dict['PYENAM']
        AfaLoggerFunc.tradeDebug('bilinf[PYENAM] = ' + str(to_dict['PYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYENAM']不存在")

    if from_dict.has_key('PYEADDR'):
        to_dict['PYEADDR'] = from_dict['PYEADDR']
        AfaLoggerFunc.tradeDebug('bilinf[PYEADDR] = ' + str(to_dict['PYEADDR']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYEADDR']不存在")

    if from_dict.has_key('PYHACC'):
        to_dict['PYHACC'] = from_dict['PYHACC']
        AfaLoggerFunc.tradeDebug('bilinf[PYHACC] = ' + str(to_dict['PYHACC']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYHACC']不存在")

    if from_dict.has_key('PYHNAM'):
        to_dict['PYHNAM'] = from_dict['PYHNAM']
        AfaLoggerFunc.tradeDebug('bilinf[PYHNAM] = ' + str(to_dict['PYHNAM']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYHNAM']不存在")

    if from_dict.has_key('PYHADDR'):
        to_dict['PYHADDR'] = from_dict['PYHADDR']
        AfaLoggerFunc.tradeDebug('bilinf[PYHADDR] = ' + str(to_dict['PYHADDR']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYHADDR']不存在")

    if from_dict.has_key('PYITYP'):
        to_dict['PYITYP'] = from_dict['PYITYP']
        AfaLoggerFunc.tradeDebug('bilinf[PYITYP] = ' + str(to_dict['PYITYP']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYITYP']不存在")

    if from_dict.has_key('PYIACC'):
        to_dict['PYIACC'] = from_dict['PYIACC']
        AfaLoggerFunc.tradeDebug('bilinf[PYIACC] = ' + str(to_dict['PYIACC']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYIACC']不存在")

    if from_dict.has_key('PYINAM'):
        to_dict['PYINAM'] = from_dict['PYINAM']
        AfaLoggerFunc.tradeDebug('bilinf[PYINAM] = ' + str(to_dict['PYINAM']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['PYINAM']不存在")

    if from_dict.has_key('BILAMT'):
        to_dict['BILAMT'] = from_dict['BILAMT']
        AfaLoggerFunc.tradeDebug('bilinf[BILAMT] = ' + str(to_dict['BILAMT']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILAMT']不存在")

    if from_dict.has_key('OCCAMT'):
        to_dict['OCCAMT'] = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('bilinf[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['OCCAMT']不存在")

    if from_dict.has_key('RMNAMT'):
        to_dict['RMNAMT'] = from_dict['RMNAMT']
        AfaLoggerFunc.tradeDebug('bilinf[RMNAMT] = ' + str(to_dict['RMNAMT']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['RMNAMT']不存在")

    if from_dict.has_key('CUR'):
        to_dict['CUR'] = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('bilinf[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['CUR']不存在")

    if from_dict.has_key('SEAL'):
        to_dict['SEAL'] = from_dict['SEAL']
        AfaLoggerFunc.tradeDebug('bilinf[SEAL] = ' + str(to_dict['SEAL']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['SEAL']不存在")

    if from_dict.has_key('USE'):
        to_dict['USE'] = from_dict['USE']
        AfaLoggerFunc.tradeDebug('bilinf[USE] = ' + str(to_dict['USE']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['USE']不存在")

    if from_dict.has_key('REMARK'):
        to_dict['REMARK'] = from_dict['REMARK']
        AfaLoggerFunc.tradeDebug('bilinf[REMARK] = ' + str(to_dict['REMARK']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['REMARK']不存在")

    if from_dict.has_key('HPCUSQ'):
        to_dict['HPCUSQ'] = from_dict['HPCUSQ']
        AfaLoggerFunc.tradeDebug('bilinf[HPCUSQ] = ' + str(to_dict['HPCUSQ']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['HPCUSQ']不存在")

    if from_dict.has_key('HPSTAT'):
        to_dict['HPSTAT'] = from_dict['HPSTAT']
        AfaLoggerFunc.tradeDebug('bilinf[HPSTAT] = ' + str(to_dict['HPSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['HPSTAT']不存在")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('bilinf[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NOTE1']不存在")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('bilinf[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NOTE2']不存在")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('bilinf[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NOTE3']不存在")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('bilinf[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NOTE4']不存在")

    return True

