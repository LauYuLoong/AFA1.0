# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 wtrbka_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap1137CTradeContext2Dwtrbka_dict.py
#   �޸�ʱ��:   Tue Dec  2 17:16:12 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeWarn("������Ų���Ϊ��")
        return False

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeWarn("������ʶ����Ϊ��")
        return False

    if TradeContext.existVariable('BESBNO'):
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBNO������")

    if TradeContext.existVariable('BEACSB'):
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB������")

    if TradeContext.existVariable('BETELR'):
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BETELR������")

    if TradeContext.existVariable('BEAUUS'):
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS������")

    if TradeContext.existVariable('BEAUPS'):
        to_dict['BEAUPS'] = TradeContext.BEAUPS
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUPS������")

    if TradeContext.existVariable('TERMID'):
        to_dict['TERMID'] = TradeContext.TERMID
        AfaLoggerFunc.tradeDebug('wtrbka_dict[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TERMID������")

    if TradeContext.existVariable('BBSSRC'):
        to_dict['BBSSRC'] = TradeContext.BBSSRC
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BBSSRC] = ' + str(to_dict['BBSSRC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BBSSRC������")

    if TradeContext.existVariable('DASQ'):
        to_dict['DASQ'] = TradeContext.DASQ
        AfaLoggerFunc.tradeDebug('wtrbka_dict[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.DASQ������")

    if TradeContext.existVariable('DCFLG'):
        to_dict['DCFLG'] = TradeContext.DCFLG
        AfaLoggerFunc.tradeDebug('wtrbka_dict[DCFLG] = ' + str(to_dict['DCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.DCFLG������")

    if TradeContext.existVariable('OPRNO'):
        to_dict['OPRNO'] = TradeContext.OPRNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRNO������")

    if TradeContext.existVariable('OPRATTNO'):
        to_dict['OPRATTNO'] = TradeContext.OPRATTNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRATTNO������")

    if TradeContext.existVariable('NCCWKDAT'):
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('wtrbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCWKDAT������")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('wtrbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT������")

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO������")

    if TradeContext.existVariable('MSGFLGNO'):
        to_dict['MSGFLGNO'] = TradeContext.MSGFLGNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[MSGFLGNO] = ' + str(to_dict['MSGFLGNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.MSGFLGNO������")

    if TradeContext.existVariable('COTRCDAT'):
        to_dict['COTRCDAT'] = TradeContext.COTRCDAT
        AfaLoggerFunc.tradeDebug('wtrbka_dict[COTRCDAT] = ' + str(to_dict['COTRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.COTRCDAT������")

    if TradeContext.existVariable('COTRCNO'):
        to_dict['COTRCNO'] = TradeContext.COTRCNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[COTRCNO] = ' + str(to_dict['COTRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.COTRCNO������")

    if TradeContext.existVariable('COMSGFLGNO'):
        to_dict['COMSGFLGNO'] = TradeContext.COMSGFLGNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[COMSGFLGNO] = ' + str(to_dict['COMSGFLGNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.COMSGFLGNO������")

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO������")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO������")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO������")

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('wtrbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM������")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('wtrbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM������")

    if TradeContext.existVariable('CUR'):
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('wtrbka_dict[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR������")

    if TradeContext.existVariable('OCCAMT'):
        to_dict['OCCAMT'] = TradeContext.OCCAMT
        AfaLoggerFunc.tradeDebug('wtrbka_dict[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OCCAMT������")

    if TradeContext.existVariable('CHRGTYP'):
        to_dict['CHRGTYP'] = TradeContext.CHRGTYP
        AfaLoggerFunc.tradeDebug('wtrbka_dict[CHRGTYP] = ' + str(to_dict['CHRGTYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CHRGTYP������")

    if TradeContext.existVariable('LOCCUSCHRG'):
        to_dict['LOCCUSCHRG'] = TradeContext.LOCCUSCHRG
        AfaLoggerFunc.tradeDebug('wtrbka_dict[LOCCUSCHRG] = ' + str(to_dict['LOCCUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.LOCCUSCHRG������")

    if TradeContext.existVariable('CUSCHRG'):
        to_dict['CUSCHRG'] = TradeContext.CUSCHRG
        AfaLoggerFunc.tradeDebug('wtrbka_dict[CUSCHRG] = ' + str(to_dict['CUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUSCHRG������")

    if TradeContext.existVariable('PYRTYP'):
        to_dict['PYRTYP'] = TradeContext.PYRTYP
        AfaLoggerFunc.tradeDebug('wtrbka_dict[PYRTYP] = ' + str(to_dict['PYRTYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRTYP������")

    if TradeContext.existVariable('PYRACC'):
        to_dict['PYRACC'] = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug('wtrbka_dict[PYRACC] = ' + str(to_dict['PYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRACC������")

    if TradeContext.existVariable('PYRNAM'):
        to_dict['PYRNAM'] = TradeContext.PYRNAM
        AfaLoggerFunc.tradeDebug('wtrbka_dict[PYRNAM] = ' + str(to_dict['PYRNAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRNAM������")

    if TradeContext.existVariable('PYRADDR'):
        to_dict['PYRADDR'] = TradeContext.PYRADDR
        AfaLoggerFunc.tradeDebug('wtrbka_dict[PYRADDR] = ' + str(to_dict['PYRADDR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRADDR������")

    if TradeContext.existVariable('PYETYP'):
        to_dict['PYETYP'] = TradeContext.PYETYP
        AfaLoggerFunc.tradeDebug('wtrbka_dict[PYETYP] = ' + str(to_dict['PYETYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYETYP������")

    if TradeContext.existVariable('PYEACC'):
        to_dict['PYEACC'] = TradeContext.PYEACC
        AfaLoggerFunc.tradeDebug('wtrbka_dict[PYEACC] = ' + str(to_dict['PYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYEACC������")

    if TradeContext.existVariable('PYENAM'):
        to_dict['PYENAM'] = TradeContext.PYENAM
        AfaLoggerFunc.tradeDebug('wtrbka_dict[PYENAM] = ' + str(to_dict['PYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYENAM������")

    if TradeContext.existVariable('PYEADDR'):
        to_dict['PYEADDR'] = TradeContext.PYEADDR
        AfaLoggerFunc.tradeDebug('wtrbka_dict[PYEADDR] = ' + str(to_dict['PYEADDR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYEADDR������")

    if TradeContext.existVariable('STRINFO'):
        to_dict['STRINFO'] = TradeContext.STRINFO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.STRINFO������")

    if TradeContext.existVariable('CERTTYPE'):
        to_dict['CERTTYPE'] = TradeContext.CERTTYPE
        AfaLoggerFunc.tradeDebug('wtrbka_dict[CERTTYPE] = ' + str(to_dict['CERTTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTTYPE������")

    if TradeContext.existVariable('CERTNO'):
        to_dict['CERTNO'] = TradeContext.CERTNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[CERTNO] = ' + str(to_dict['CERTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTNO������")

    if TradeContext.existVariable('BNKBKNO'):
        to_dict['BNKBKNO'] = TradeContext.BNKBKNO
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BNKBKNO] = ' + str(to_dict['BNKBKNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BNKBKNO������")

    if TradeContext.existVariable('BNKBKBAL'):
        to_dict['BNKBKBAL'] = TradeContext.BNKBKBAL
        AfaLoggerFunc.tradeDebug('wtrbka_dict[BNKBKBAL] = ' + str(to_dict['BNKBKBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BNKBKBAL������")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('wtrbka_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1������")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('wtrbka_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2������")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('wtrbka_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3������")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('wtrbka_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4������")

    return True

