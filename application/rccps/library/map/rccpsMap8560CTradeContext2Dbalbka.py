# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 balbka �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8560CTradeContext2Dbalbka.py
#   �޸�ʱ��:   Thu Oct 23 09:59:46 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('balbka[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BJEDTE������")

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('balbka[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BSPSQN������")

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('balbka[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRSFLG������")

    if TradeContext.existVariable('BESBNO'):
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('balbka[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBNO������")

    if TradeContext.existVariable('BEACSB'):
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('balbka[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB������")

    if TradeContext.existVariable('BETELR'):
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('balbka[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BETELR������")

    if TradeContext.existVariable('BEAUUS'):
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('balbka[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS������")

    if TradeContext.existVariable('BEAUPS'):
        to_dict['BEAUPS'] = TradeContext.BEAUPS
        AfaLoggerFunc.tradeDebug('balbka[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUPS������")

    if TradeContext.existVariable('TERMID'):
        to_dict['TERMID'] = TradeContext.TERMID
        AfaLoggerFunc.tradeDebug('balbka[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TERMID������")

    if TradeContext.existVariable('OPRNO'):
        to_dict['OPRNO'] = TradeContext.OPRNO
        AfaLoggerFunc.tradeDebug('balbka[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRNO������")

    if TradeContext.existVariable('OPRATTNO'):
        to_dict['OPRATTNO'] = TradeContext.OPRATTNO
        AfaLoggerFunc.tradeDebug('balbka[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRATTNO������")

    if TradeContext.existVariable('NCCWKDAT'):
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('balbka[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCWKDAT������")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('balbka[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('balbka[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT������")

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('balbka[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO������")

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('balbka[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO������")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('balbka[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO������")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('balbka[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO������")

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('balbka[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM������")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('balbka[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('balbka[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM������")

    if TradeContext.existVariable('CUR'):
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('balbka[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR������")

    if TradeContext.existVariable('CHRGTYP'):
        to_dict['CHRGTYP'] = TradeContext.CHRGTYP
        AfaLoggerFunc.tradeDebug('balbka[CHRGTYP] = ' + str(to_dict['CHRGTYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CHRGTYP������")

    if TradeContext.existVariable('LOCCUSCHRG'):
        to_dict['LOCCUSCHRG'] = TradeContext.LOCCUSCHRG
        AfaLoggerFunc.tradeDebug('balbka[LOCCUSCHRG] = ' + str(to_dict['LOCCUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.LOCCUSCHRG������")

    if TradeContext.existVariable('CUSCHRG'):
        to_dict['CUSCHRG'] = TradeContext.CUSCHRG
        AfaLoggerFunc.tradeDebug('balbka[CUSCHRG] = ' + str(to_dict['CUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUSCHRG������")

    if TradeContext.existVariable('PYRACC'):
        to_dict['PYRACC'] = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug('balbka[PYRACC] = ' + str(to_dict['PYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYRACC������")

    if TradeContext.existVariable('PYEACC'):
        to_dict['PYEACC'] = TradeContext.PYEACC
        AfaLoggerFunc.tradeDebug('balbka[PYEACC] = ' + str(to_dict['PYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PYEACC������")

    if TradeContext.existVariable('STRINFO'):
        to_dict['STRINFO'] = TradeContext.STRINFO
        AfaLoggerFunc.tradeDebug('balbka[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.STRINFO������")

    if TradeContext.existVariable('CERTTYPE'):
        to_dict['CERTTYPE'] = TradeContext.CERTTYPE
        AfaLoggerFunc.tradeDebug('balbka[CERTTYPE] = ' + str(to_dict['CERTTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTTYPE������")

    if TradeContext.existVariable('CERTNO'):
        to_dict['CERTNO'] = TradeContext.CERTNO
        AfaLoggerFunc.tradeDebug('balbka[CERTNO] = ' + str(to_dict['CERTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTNO������")

    if TradeContext.existVariable('BNKBKNO'):
        to_dict['BNKBKNO'] = TradeContext.BNKBKNO
        AfaLoggerFunc.tradeDebug('balbka[BNKBKNO] = ' + str(to_dict['BNKBKNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BNKBKNO������")

    if TradeContext.existVariable('AVLBAL'):
        to_dict['AVLBAL'] = TradeContext.AVLBAL
        AfaLoggerFunc.tradeDebug('balbka[AVLBAL] = ' + str(to_dict['AVLBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.AVLBAL������")

    if TradeContext.existVariable('ACCBAL'):
        to_dict['ACCBAL'] = TradeContext.ACCBAL
        AfaLoggerFunc.tradeDebug('balbka[ACCBAL] = ' + str(to_dict['ACCBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ACCBAL������")

    if TradeContext.existVariable('PRCCO'):
        to_dict['PRCCO'] = TradeContext.PRCCO
        AfaLoggerFunc.tradeDebug('balbka[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PRCCO������")

    if TradeContext.existVariable('PRCINFO'):
        to_dict['PRCINFO'] = TradeContext.PRCINFO
        AfaLoggerFunc.tradeDebug('balbka[PRCINFO] = ' + str(to_dict['PRCINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PRCINFO������")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('balbka[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1������")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('balbka[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2������")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('balbka[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3������")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('balbka[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4������")
        
    if TradeContext.existVariable('MSGFLGNO'):
        to_dict['MSGFLGNO'] = TradeContext.MSGFLGNO
        AfaLoggerFunc.tradeDebug('balbka[MSGFLGNO] = ' + str(to_dict['MSGFLGNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.MSGFLGNO������")

    return True

