# -*- coding: gbk -*-
##################################################################
#   农信银系统 TradeContext 字典到 trcbka_dict 字典映射函数
#
#   作    者：  关彬捷
#   程序文件:   rccpsMap1101CTradeContext2Dtrcbka_dict.py
#   修改时间:   Sat Jun  7 11:31:34 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('trcbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeWarn("交易日期不能为空")
        return False

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('trcbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeWarn("报单序号不能为空")
        return False

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('trcbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeWarn("往来标志不能为空")
        return False

    if TradeContext.existVariable('BESBNO'):
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('trcbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeWarn("机构号不能为空")
        return False

    if TradeContext.existVariable('BEACSB'):
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('trcbka_dict[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB不存在")

    if TradeContext.existVariable('BETELR'):
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('trcbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeWarn("柜员号不能为空")
        return False

    if TradeContext.existVariable('BEAUUS'):
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('trcbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS不存在")

    if TradeContext.existVariable('BBSSRC'):
        to_dict['BBSSRC'] = TradeContext.BBSSRC
        AfaLoggerFunc.tradeDebug('trcbka_dict[BBSSRC] = ' + str(to_dict['BBSSRC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BBSSRC不存在")

    if TradeContext.existVariable('DCFLG'):
        to_dict['DCFLG'] = TradeContext.DCFLG
        AfaLoggerFunc.tradeDebug('trcbka_dict[DCFLG] = ' + str(to_dict['DCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.DCFLG不存在")

    if TradeContext.existVariable('OPRNO'):
        to_dict['OPRNO'] = TradeContext.OPRNO
        AfaLoggerFunc.tradeDebug('trcbka_dict[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRNO不存在")

    if TradeContext.existVariable('OPRATTNO'):
        to_dict['OPRATTNO'] = TradeContext.OPRATTNO
        AfaLoggerFunc.tradeDebug('trcbka_dict[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRATTNO不存在")

    if TradeContext.existVariable('NCCWKDAT'):
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('trcbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeWarn("中心日期不能为空")
        return False

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('trcbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeWarn("交易码不能为空")
        return False

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('trcbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT不存在")

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('trcbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeWarn("校验流水号不能为空")
        return False

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('trcbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeWarn("发送行号不能为空")
        return False

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('trcbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeWarn("发送行名不能为空")
        return False

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('trcbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeWarn("接收行号不能为空")
        return False

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('trcbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeWarn("接收行名不能为空")
        return False

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('trcbka_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO不存在")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('trcbka_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO不存在")

    if TradeContext.existVariable('CUR'):
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('trcbka_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeWarn("币种不能为空")
        return False

    if TradeContext.existVariable('OCCAMT'):
        to_dict['OCCAMT'] = TradeContext.OCCAMT
        AfaLoggerFunc.tradeDebug('trcbka_dict[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeWarn("金额不能为空")
        return False

    if TradeContext.existVariable('CHRGTYP'):
        to_dict['CHRGTYP'] = TradeContext.CHRGTYP
        AfaLoggerFunc.tradeDebug('trcbka_dict[CHRGTYP] = ' + str(to_dict['CHRGTYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CHRGTYP不存在")

    if TradeContext.existVariable('LOCCUSCHRG'):
        to_dict['LOCCUSCHRG'] = TradeContext.LOCCUSCHRG
        AfaLoggerFunc.tradeDebug('trcbka_dict[LOCCUSCHRG] = ' + str(to_dict['LOCCUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.LOCCUSCHRG不存在")

    if TradeContext.existVariable('CUSCHRG'):
        to_dict['CUSCHRG'] = TradeContext.CUSCHRG
        AfaLoggerFunc.tradeDebug('trcbka_dict[CUSCHRG] = ' + str(to_dict['CUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUSCHRG不存在")

    if TradeContext.existVariable('PYRACC'):
        to_dict['PYRACC'] = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug('trcbka_dict[PYRACC] = ' + str(to_dict['PYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRACC不存在")

    if TradeContext.existVariable('PYRNAM'):
        to_dict['PYRNAM'] = TradeContext.PYRNAM
        AfaLoggerFunc.tradeDebug('trcbka_dict[PYRNAM] = ' + str(to_dict['PYRNAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRNAM不存在")

    if TradeContext.existVariable('PYRADDR'):
        to_dict['PYRADDR'] = TradeContext.PYRADDR
        AfaLoggerFunc.tradeDebug('trcbka_dict[PYRADDR] = ' + str(to_dict['PYRADDR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRADDR不存在")

    if TradeContext.existVariable('PYEACC'):
        to_dict['PYEACC'] = TradeContext.PYEACC
        AfaLoggerFunc.tradeDebug('trcbka_dict[PYEACC] = ' + str(to_dict['PYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYEACC不存在")

    if TradeContext.existVariable('PYENAM'):
        to_dict['PYENAM'] = TradeContext.PYENAM
        AfaLoggerFunc.tradeDebug('trcbka_dict[PYENAM] = ' + str(to_dict['PYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYENAM不存在")

    if TradeContext.existVariable('PYEADDR'):
        to_dict['PYEADDR'] = TradeContext.PYEADDR
        AfaLoggerFunc.tradeDebug('trcbka_dict[PYEADDR] = ' + str(to_dict['PYEADDR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYEADDR不存在")

    if TradeContext.existVariable('SEAL'):
        to_dict['SEAL'] = TradeContext.SEAL
        AfaLoggerFunc.tradeDebug('trcbka_dict[SEAL] = ' + str(to_dict['SEAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SEAL不存在")

    if TradeContext.existVariable('USE'):
        to_dict['USE'] = TradeContext.USE
        AfaLoggerFunc.tradeDebug('trcbka_dict[USE] = ' + str(to_dict['USE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.USE不存在")

    if TradeContext.existVariable('REMARK'):
        to_dict['REMARK'] = TradeContext.REMARK
        AfaLoggerFunc.tradeDebug('trcbka_dict[REMARK] = ' + str(to_dict['REMARK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.REMARK不存在")

    if TradeContext.existVariable('BILTYP'):
        to_dict['BILTYP'] = TradeContext.BILTYP
        AfaLoggerFunc.tradeDebug('trcbka_dict[BILTYP] = ' + str(to_dict['BILTYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILTYP不存在")

    if TradeContext.existVariable('BILDAT'):
        to_dict['BILDAT'] = TradeContext.BILDAT
        AfaLoggerFunc.tradeDebug('trcbka_dict[BILDAT] = ' + str(to_dict['BILDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILDAT不存在")

    if TradeContext.existVariable('BILNO'):
        to_dict['BILNO'] = TradeContext.BILNO
        AfaLoggerFunc.tradeDebug('trcbka_dict[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILNO不存在")

    if TradeContext.existVariable('COMAMT'):
        to_dict['COMAMT'] = TradeContext.COMAMT
        AfaLoggerFunc.tradeDebug('trcbka_dict[COMAMT] = ' + str(to_dict['COMAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.COMAMT不存在")

    if TradeContext.existVariable('OVPAYAMT'):
        to_dict['OVPAYAMT'] = TradeContext.OVPAYAMT
        AfaLoggerFunc.tradeDebug('trcbka_dict[OVPAYAMT] = ' + str(to_dict['OVPAYAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OVPAYAMT不存在")

    if TradeContext.existVariable('CPSAMT'):
        to_dict['CPSAMT'] = TradeContext.CPSAMT
        AfaLoggerFunc.tradeDebug('trcbka_dict[CPSAMT] = ' + str(to_dict['CPSAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CPSAMT不存在")

    if TradeContext.existVariable('RFUAMT'):
        to_dict['RFUAMT'] = TradeContext.RFUAMT
        AfaLoggerFunc.tradeDebug('trcbka_dict[RFUAMT] = ' + str(to_dict['RFUAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RFUAMT不存在")

    if TradeContext.existVariable('CERTTYPE'):
        to_dict['CERTTYPE'] = TradeContext.CERTTYPE
        AfaLoggerFunc.tradeDebug('trcbka_dict[CERTTYPE] = ' + str(to_dict['CERTTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTTYPE不存在")

    if TradeContext.existVariable('CERTNO'):
        to_dict['CERTNO'] = TradeContext.CERTNO
        AfaLoggerFunc.tradeDebug('trcbka_dict[CERTNO] = ' + str(to_dict['CERTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTNO不存在")

    if TradeContext.existVariable('BOJEDT'):
        to_dict['BOJEDT'] = TradeContext.BOJEDT
        AfaLoggerFunc.tradeDebug('trcbka_dict[BOJEDT] = ' + str(to_dict['BOJEDT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOJEDT不存在")

    if TradeContext.existVariable('BOSPSQ'):
        to_dict['BOSPSQ'] = TradeContext.BOSPSQ
        AfaLoggerFunc.tradeDebug('trcbka_dict[BOSPSQ] = ' + str(to_dict['BOSPSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BOSPSQ不存在")

    if TradeContext.existVariable('ORTRCDAT'):
        to_dict['ORTRCDAT'] = TradeContext.ORTRCDAT
        AfaLoggerFunc.tradeDebug('trcbka_dict[ORTRCDAT] = ' + str(to_dict['ORTRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCDAT不存在")

    if TradeContext.existVariable('ORTRCCO'):
        to_dict['ORTRCCO'] = TradeContext.ORTRCCO
        AfaLoggerFunc.tradeDebug('trcbka_dict[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCCO不存在")

    if TradeContext.existVariable('ORTRCNO'):
        to_dict['ORTRCNO'] = TradeContext.ORTRCNO
        AfaLoggerFunc.tradeDebug('trcbka_dict[ORTRCNO] = ' + str(to_dict['ORTRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCNO不存在")

    if TradeContext.existVariable('ORSNDBNK'):
        to_dict['ORSNDBNK'] = TradeContext.ORSNDBNK
        AfaLoggerFunc.tradeDebug('trcbka_dict[ORSNDBNK] = ' + str(to_dict['ORSNDBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORSNDBNK不存在")

    if TradeContext.existVariable('ORRCVBNK'):
        to_dict['ORRCVBNK'] = TradeContext.ORRCVBNK
        AfaLoggerFunc.tradeDebug('trcbka_dict[ORRCVBNK] = ' + str(to_dict['ORRCVBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORRCVBNK不存在")

    if TradeContext.existVariable('STRINFO'):
        to_dict['STRINFO'] = TradeContext.STRINFO
        AfaLoggerFunc.tradeDebug('trcbka_dict[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.STRINFO不存在")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('trcbka_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1不存在")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('trcbka_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2不存在")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('trcbka_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3不存在")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('trcbka_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4不存在")

    return True

