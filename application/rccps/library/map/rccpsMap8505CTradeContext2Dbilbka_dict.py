# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 bilbka_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8505CTradeContext2Dbilbka_dict.py
#   �޸�ʱ��:   Sun Sep 14 16:28:22 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('bilbka_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('bilbka_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeWarn("������Ų���Ϊ��")
        return False

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('bilbka_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeWarn("������־����Ϊ��")
        return False

    if TradeContext.existVariable('BESBNO'):
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('bilbka_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeWarn("�����Ų���Ϊ��")
        return False

    if TradeContext.existVariable('BEACSB'):
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('bilbka_dict[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB������")

    if TradeContext.existVariable('BETELR'):
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('bilbka_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeWarn("��Ա�Ų���Ϊ��")
        return False

    if TradeContext.existVariable('BEAUUS'):
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('bilbka_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS������")

    if TradeContext.existVariable('BEAUPS'):
        to_dict['BEAUPS'] = TradeContext.BEAUPS
        AfaLoggerFunc.tradeDebug('bilbka_dict[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUPS������")

    if TradeContext.existVariable('TERMID'):
        to_dict['TERMID'] = TradeContext.TERMID
        AfaLoggerFunc.tradeDebug('bilbka_dict[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TERMID������")

    if TradeContext.existVariable('BBSSRC'):
        to_dict['BBSSRC'] = TradeContext.BBSSRC
        AfaLoggerFunc.tradeDebug('bilbka_dict[BBSSRC] = ' + str(to_dict['BBSSRC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BBSSRC������")

    if TradeContext.existVariable('DASQ'):
        to_dict['DASQ'] = TradeContext.DASQ
        AfaLoggerFunc.tradeDebug('bilbka_dict[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.DASQ������")

    if TradeContext.existVariable('DCFLG'):
        to_dict['DCFLG'] = TradeContext.DCFLG
        AfaLoggerFunc.tradeDebug('bilbka_dict[DCFLG] = ' + str(to_dict['DCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.DCFLG������")

    if TradeContext.existVariable('OPRNO'):
        to_dict['OPRNO'] = TradeContext.OPRNO
        AfaLoggerFunc.tradeDebug('bilbka_dict[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRNO������")

    if TradeContext.existVariable('OPRATTNO'):
        to_dict['OPRATTNO'] = TradeContext.OPRATTNO
        AfaLoggerFunc.tradeDebug('bilbka_dict[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRATTNO������")

    if TradeContext.existVariable('NCCworkDate'):
        to_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        AfaLoggerFunc.tradeDebug('bilbka_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('bilbka_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeWarn("�����벻��Ϊ��")
        return False

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('bilbka_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT������")

    if TradeContext.existVariable('SerialNo'):
        to_dict['TRCNO'] = TradeContext.SerialNo
        AfaLoggerFunc.tradeDebug('bilbka_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SerialNo������")

    if TradeContext.existVariable('SNDSTLBIN'):
        to_dict['SNDMBRCO'] = TradeContext.SNDSTLBIN
        AfaLoggerFunc.tradeDebug('bilbka_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDSTLBIN������")

    if TradeContext.existVariable('RCVSTLBIN'):
        to_dict['RCVMBRCO'] = TradeContext.RCVSTLBIN
        AfaLoggerFunc.tradeDebug('bilbka_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVSTLBIN������")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('bilbka_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeWarn("�����кŲ���Ϊ��")
        return False

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('bilbka_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeWarn("������������Ϊ��")
        return False

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('bilbka_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('bilbka_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM������")

    if TradeContext.existVariable('BILVER'):
        to_dict['BILVER'] = TradeContext.BILVER
        AfaLoggerFunc.tradeDebug('bilbka_dict[BILVER] = ' + str(to_dict['BILVER']))
    else:
        AfaLoggerFunc.tradeWarn("Ʊ�ݰ汾�Ų���Ϊ��")
        return False

    if TradeContext.existVariable('BILNO'):
        to_dict['BILNO'] = TradeContext.BILNO
        AfaLoggerFunc.tradeDebug('bilbka_dict[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeWarn("Ʊ�ݺ��벻��Ϊ��")
        return False

    if TradeContext.existVariable('BILRS'):
        to_dict['BILRS'] = TradeContext.BILRS
        AfaLoggerFunc.tradeDebug('bilbka_dict[BILRS] = ' + str(to_dict['BILRS']))
    else:
        AfaLoggerFunc.tradeWarn("Ʊ�ݱ�ʶ����Ϊ��")
        return False

    return True

