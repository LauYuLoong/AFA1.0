# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 mrqtbl �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8544CTradeContext2Dmrqtbl.py
#   �޸�ʱ��:   Tue Jun 24 11:51:25 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('mrqtbl[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('mrqtbl[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeWarn("������Ų���Ϊ��")
        return False

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('mrqtbl[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('mrqtbl[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO������")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('mrqtbl[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO������")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('mrqtbl[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO������")

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('mrqtbl[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM������")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('mrqtbl[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('mrqtbl[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM������")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('mrqtbl[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT������")

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('mrqtbl[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO������")

    if TradeContext.existVariable('NPCBKID'):
        to_dict['NPCBKID'] = TradeContext.NPCBKID
        AfaLoggerFunc.tradeDebug('mrqtbl[NPCBKID] = ' + str(to_dict['NPCBKID']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NPCBKID������")

    if TradeContext.existVariable('NPCBKNM'):
        to_dict['NPCBKNM'] = TradeContext.NPCBKNM
        AfaLoggerFunc.tradeDebug('mrqtbl[NPCBKNM] = ' + str(to_dict['NPCBKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NPCBKNM������")

    if TradeContext.existVariable('NPCACNT'):
        to_dict['NPCACNT'] = TradeContext.NPCACNT
        AfaLoggerFunc.tradeDebug('mrqtbl[NPCACNT] = ' + str(to_dict['NPCACNT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NPCACNT������")

    if TradeContext.existVariable('OCCAMT'):
        to_dict['OCCAMT'] = TradeContext.OCCAMT
        AfaLoggerFunc.tradeDebug('mrqtbl[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OCCAMT������")

    if TradeContext.existVariable('REMARK'):
        to_dict['REMARK'] = TradeContext.REMARK
        AfaLoggerFunc.tradeDebug('mrqtbl[REMARK] = ' + str(to_dict['REMARK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.REMARK������")

    if TradeContext.existVariable('PRCCO'):
        to_dict['PRCCO'] = TradeContext.PRCCO
        AfaLoggerFunc.tradeDebug('mrqtbl[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PRCCO������")

    if TradeContext.existVariable('STRINFO'):
        to_dict['STRINFO'] = TradeContext.STRINFO
        AfaLoggerFunc.tradeDebug('mrqtbl[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.STRINFO������")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('mrqtbl[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1������")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('mrqtbl[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2������")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('mrqtbl[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4������")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('mrqtbl[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3������")

    return True

