# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 pbdata �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap1122CTradeContext2Dpbdata.py
#   �޸�ʱ��:   Wed Jun 18 17:32:39 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('pbdata[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeWarn("ί�����ڲ���Ϊ��")
        return False

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('pbdata[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeWarn("������ˮ�Ų���Ϊ��")
        return False

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('pbdata[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeWarn("�������кŲ���Ϊ��")
        return False

    if TradeContext.existVariable('NCCWKDAT'):
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('pbdata[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCWKDAT������")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('pbdata[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('pbdata[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('EFCTDAT'):
        to_dict['EFCTDAT'] = TradeContext.EFCTDAT
        AfaLoggerFunc.tradeDebug('pbdata[EFCTDAT] = ' + str(to_dict['EFCTDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.EFCTDAT������")

    if TradeContext.existVariable('PBDATYP'):
        to_dict['PBDATYP'] = TradeContext.PBDATYP
        AfaLoggerFunc.tradeDebug('pbdata[PBDATYP] = ' + str(to_dict['PBDATYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PBDATYP������")

    if TradeContext.existVariable('PBDAFILE'):
        to_dict['PBDAFILE'] = TradeContext.PBDAFILE
        AfaLoggerFunc.tradeDebug('pbdata[PBDAFILE] = ' + str(to_dict['PBDAFILE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PBDAFILE������")

    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('pbdata[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1������")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('pbdata[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2������")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('pbdata[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3������")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('pbdata[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4������")

    return True

