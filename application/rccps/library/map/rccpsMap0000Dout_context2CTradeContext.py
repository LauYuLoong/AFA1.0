# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ out_context �ֵ䵽 TradeContext �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dout_context2CTradeContext.py
#   �޸�ʱ��:   Thu Jun 19 19:46:54 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('sysType'):
        TradeContext.sysType = from_dict['sysType']
        AfaLoggerFunc.tradeDebug('TradeContext.sysType = ' + str(TradeContext.sysType))
    else:
        AfaLoggerFunc.tradeDebug("out_context['sysType']������")
        return False

    if from_dict.has_key('TRCCO'):
        TradeContext.TRCCO = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCCO = ' + str(TradeContext.TRCCO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['TRCCO']������")
        return False

    if from_dict.has_key('MSGTYPCO'):
        TradeContext.MSGTYPCO = from_dict['MSGTYPCO']
        AfaLoggerFunc.tradeDebug('TradeContext.MSGTYPCO = ' + str(TradeContext.MSGTYPCO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['MSGTYPCO']������")
        return False

    if from_dict.has_key('SNDMBRCO'):
        TradeContext.SNDSTLBIN = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDSTLBIN = ' + str(TradeContext.SNDSTLBIN))
    else:
        AfaLoggerFunc.tradeDebug("out_context['SNDMBRCO']������")
        return False

    if from_dict.has_key('RCVMBRCO'):
        TradeContext.RCVSTLBIN = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('TradeContext.RCVSTLBIN = ' + str(TradeContext.RCVSTLBIN))
    else:
        AfaLoggerFunc.tradeDebug("out_context['RCVMBRCO']������")
        return False

    if from_dict.has_key('SNDBRHCO'):
        TradeContext.SNDBRHCO = from_dict['SNDBRHCO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDBRHCO = ' + str(TradeContext.SNDBRHCO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['SNDBRHCO']������")
        return False

    if from_dict.has_key('SNDCLKNO'):
        TradeContext.SNDCLKNO = from_dict['SNDCLKNO']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDCLKNO = ' + str(TradeContext.SNDCLKNO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['SNDCLKNO']������")
        return False

    if from_dict.has_key('SNDTRDAT'):
        TradeContext.SNDTRDAT = from_dict['SNDTRDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDTRDAT = ' + str(TradeContext.SNDTRDAT))
    else:
        AfaLoggerFunc.tradeDebug("out_context['SNDTRDAT']������")
        return False

    if from_dict.has_key('SNDTRTIM'):
        TradeContext.SNDTRTIM = from_dict['SNDTRTIM']
        AfaLoggerFunc.tradeDebug('TradeContext.SNDTRTIM = ' + str(TradeContext.SNDTRTIM))
    else:
        AfaLoggerFunc.tradeDebug("out_context['SNDTRTIM']������")
        return False

    if from_dict.has_key('MSGFLGNO'):
        TradeContext.MSGFLGNO = from_dict['MSGFLGNO']
        AfaLoggerFunc.tradeDebug('TradeContext.MSGFLGNO = ' + str(TradeContext.MSGFLGNO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['MSGFLGNO']������")
        return False

    if from_dict.has_key('ORMFN'):
        TradeContext.ORMFN = from_dict['ORMFN']
        AfaLoggerFunc.tradeDebug('TradeContext.ORMFN = ' + str(TradeContext.ORMFN))
    else:
        AfaLoggerFunc.tradeDebug("out_context['ORMFN']������")
        return False

    if from_dict.has_key('NCCWKDAT'):
        TradeContext.NCCWKDAT = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.NCCWKDAT = ' + str(TradeContext.NCCWKDAT))
    else:
        AfaLoggerFunc.tradeDebug("out_context['NCCWKDAT']������")
        return False

    if from_dict.has_key('OPRTYPNO'):
        TradeContext.OPRTYPNO = from_dict['OPRTYPNO']
        AfaLoggerFunc.tradeDebug('TradeContext.OPRTYPNO = ' + str(TradeContext.OPRTYPNO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['OPRTYPNO']������")
        return False

    if from_dict.has_key('ROPRTPNO'):
        TradeContext.ROPRTPNO = from_dict['ROPRTPNO']
        AfaLoggerFunc.tradeDebug('TradeContext.ROPRTPNO = ' + str(TradeContext.ROPRTPNO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['ROPRTPNO']������")
        return False

    if from_dict.has_key('TRANTYP'):
        TradeContext.TRANTYP = from_dict['TRANTYP']
        AfaLoggerFunc.tradeDebug('TradeContext.TRANTYP = ' + str(TradeContext.TRANTYP))
    else:
        AfaLoggerFunc.tradeDebug("out_context['TRANTYP']������")
        return False

    if from_dict.has_key('ORTRCCO'):
        TradeContext.ORTRCCO = from_dict['ORTRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCCO = ' + str(TradeContext.ORTRCCO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['ORTRCCO']������")
        return False

    if from_dict.has_key('PRCCO'):
        TradeContext.PRCCO = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.PRCCO = ' + str(TradeContext.PRCCO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['PRCCO']������")
        return False

    if from_dict.has_key('STRINFO'):
        TradeContext.STRINFO = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('TradeContext.STRINFO = ' + str(TradeContext.STRINFO))
    else:
        AfaLoggerFunc.tradeDebug("out_context['STRINFO']������")
        return False

    return True

