# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ trccan_dict �ֵ䵽 TradeContext �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8507Dtrccan_dict2CTradeContext.py
#   �޸�ʱ��:   Wed Jul 23 17:17:19 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict):
        
    if from_dict.has_key('BRSFLG'):
        TradeContext.BRSFLG = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('TradeContext.BRSFLG = ' + str(TradeContext.BRSFLG))
    else:
        AfaLoggerFunc.tradeWarn("������־����Ϊ��")
        return False

    if from_dict.has_key('BSPSQN'):
        TradeContext.BSPSQN = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('TradeContext.BSPSQN = ' + str(TradeContext.BSPSQN))
    else:
        AfaLoggerFunc.tradeWarn("������Ų���Ϊ��")
        return False

    if from_dict.has_key('BJEDTE'):
        TradeContext.BJEDTE = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('TradeContext.BJEDTE = ' + str(TradeContext.BJEDTE))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if from_dict.has_key('CONT'):
        TradeContext.CONT = from_dict['CONT']
        AfaLoggerFunc.tradeDebug('TradeContext.CONT = ' + str(TradeContext.CONT))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['CONT']������")

    if from_dict.has_key('ORTRCCO'):
        TradeContext.ORTRCCO = from_dict['ORTRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCCO = ' + str(TradeContext.ORTRCCO))
    else:
        AfaLoggerFunc.tradeWarn("ԭ���״��벻��Ϊ��")
        return False

    if from_dict.has_key('NCCWKDAT'):
        TradeContext.NCCworkDate = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.NCCworkDate = ' + str(TradeContext.NCCworkDate))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if from_dict.has_key('TRCCO'):
        TradeContext.TRCCO = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('TradeContext.TRCCO = ' + str(TradeContext.TRCCO))
    else:
        AfaLoggerFunc.tradeWarn("���״��벻��Ϊ��")
        return False

    if from_dict.has_key('CUR'):
        TradeContext.CUR = from_dict['CUR']
        AfaLoggerFunc.tradeDebug('TradeContext.CUR = ' + str(TradeContext.CUR))
    else:
        AfaLoggerFunc.tradeWarn("���ֲ���Ϊ��")
        return False

    if from_dict.has_key('OCCAMT'):
        TradeContext.OCCAMT = from_dict['OCCAMT']
        AfaLoggerFunc.tradeDebug('TradeContext.OCCAMT = ' + str(TradeContext.OCCAMT))
    else:
        AfaLoggerFunc.tradeWarn("���׽���Ϊ��")
        return False

    if from_dict.has_key('TRCDAT'):
        TradeContext.ORTRCDAT = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCDAT = ' + str(TradeContext.ORTRCDAT))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        TradeContext.ORTRCNO = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORTRCNO = ' + str(TradeContext.ORTRCNO))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['TRCNO']������")

    if from_dict.has_key('SNDBNKCO'):
        TradeContext.ORSNDBNKCO = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORSNDBNKCO = ' + str(TradeContext.ORSNDBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        TradeContext.ORSNDBNKNM = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.ORSNDBNKNM = ' + str(TradeContext.ORSNDBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        TradeContext.ORRCVBNKCO = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('TradeContext.ORRCVBNKCO = ' + str(TradeContext.ORRCVBNKCO))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        TradeContext.ORRCVBNKNM = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('TradeContext.ORRCVBNKNM = ' + str(TradeContext.ORRCVBNKNM))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['RCVBNKNM']������")

    if from_dict.has_key('BOJEDT'):
        TradeContext.BOJEDT = from_dict['BOJEDT']
        AfaLoggerFunc.tradeDebug('TradeContext.BOJEDT = ' + str(TradeContext.BOJEDT))
    else:
        AfaLoggerFunc.tradeWarn("ԭ�������ڲ���Ϊ��")
        return False

    if from_dict.has_key('BOSPSQ'):
        TradeContext.BOSPSQ = from_dict['BOSPSQ']
        AfaLoggerFunc.tradeDebug('TradeContext.BOSPSQ = ' + str(TradeContext.BOSPSQ))
    else:
        AfaLoggerFunc.tradeWarn("ԭ������Ų���Ϊ��")
        return False

    if from_dict.has_key('NOTE1'):
        TradeContext.NOTE1 = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE1 = ' + str(TradeContext.NOTE1))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        TradeContext.NOTE2 = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE2 = ' + str(TradeContext.NOTE2))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        TradeContext.NOTE3 = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE3 = ' + str(TradeContext.NOTE3))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        TradeContext.NOTE4 = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('TradeContext.NOTE4 = ' + str(TradeContext.NOTE4))
    else:
        AfaLoggerFunc.tradeDebug("trccan_dict['NOTE4']������")

    if from_dict.has_key('BESBNO'):
        TradeContext.BESBNO = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('TradeContext.BESBNO = ' + str(TradeContext.BESBNO))
    else:
        AfaLoggerFunc.tradeWarn("�����Ų���Ϊ��")
        return False

    if from_dict.has_key('BETELR'):
        TradeContext.BETELR = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('TradeContext.BETELR = ' + str(TradeContext.BETELR))
    else:
        AfaLoggerFunc.tradeWarn("��Ա�Ų���Ϊ��")
        return False

    return True

