# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 bilbka �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8504CTradeContext2Dbilbka.py
#   �޸�ʱ��:   Sun Sep 14 16:27:41 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
        
    if TradeContext.existVariable('BJEDTE'):
        to_dict['BJEDTE'] = TradeContext.BJEDTE
        AfaLoggerFunc.tradeDebug('bilbka[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if TradeContext.existVariable('BSPSQN'):
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('bilbka[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeWarn("������Ų���Ϊ��")
        return False

    if TradeContext.existVariable('BRSFLG'):
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('bilbka[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeWarn("������ʶ����Ϊ��")
        return False

    if TradeContext.existVariable('BESBNO'):
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('bilbka[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBNO������")

    if TradeContext.existVariable('BEACSB'):
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('bilbka[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB������")

    if TradeContext.existVariable('BETELR'):
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('bilbka[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BETELR������")

    if TradeContext.existVariable('BEAUUS'):
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('bilbka[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS������")

    if TradeContext.existVariable('BEAUPS'):
        to_dict['BEAUPS'] = TradeContext.BEAUPS
        AfaLoggerFunc.tradeDebug('bilbka[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUPS������")

    if TradeContext.existVariable('TERMID'):
        to_dict['TERMID'] = TradeContext.TERMID
        AfaLoggerFunc.tradeDebug('bilbka[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TERMID������")

    if TradeContext.existVariable('BBSSRC'):
        to_dict['BBSSRC'] = TradeContext.BBSSRC
        AfaLoggerFunc.tradeDebug('bilbka[BBSSRC] = ' + str(to_dict['BBSSRC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BBSSRC������")

    if TradeContext.existVariable('DASQ'):
        to_dict['DASQ'] = TradeContext.DASQ
        AfaLoggerFunc.tradeDebug('bilbka[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.DASQ������")

    if TradeContext.existVariable('DCFLG'):
        to_dict['DCFLG'] = TradeContext.DCFLG
        AfaLoggerFunc.tradeDebug('bilbka[DCFLG] = ' + str(to_dict['DCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.DCFLG������")

    if TradeContext.existVariable('OPRNO'):
        to_dict['OPRNO'] = TradeContext.OPRNO
        AfaLoggerFunc.tradeDebug('bilbka[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRNO������")

    if TradeContext.existVariable('OPRATTNO'):
        to_dict['OPRATTNO'] = TradeContext.OPRATTNO
        AfaLoggerFunc.tradeDebug('bilbka[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPRATTNO������")

    if TradeContext.existVariable('NCCWKDAT'):
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('bilbka[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCWKDAT������")

    if TradeContext.existVariable('TRCCO'):
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('bilbka[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")

    if TradeContext.existVariable('TRCDAT'):
        to_dict['TRCDAT'] = TradeContext.TRCDAT
        AfaLoggerFunc.tradeDebug('bilbka[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCDAT������")

    if TradeContext.existVariable('TRCNO'):
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('bilbka[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO������")

    if TradeContext.existVariable('SNDMBRCO'):
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('bilbka[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO������")

    if TradeContext.existVariable('RCVMBRCO'):
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('bilbka[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO������")

    if TradeContext.existVariable('SNDBNKCO'):
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('bilbka[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO������")

    if TradeContext.existVariable('SNDBNKNM'):
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('bilbka[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM������")

    if TradeContext.existVariable('RCVBNKCO'):
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('bilbka[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('RCVBNKNM'):
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('bilbka[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM������")

    if TradeContext.existVariable('BILVER'):
        to_dict['BILVER'] = TradeContext.BILVER
        AfaLoggerFunc.tradeDebug('bilbka[BILVER] = ' + str(to_dict['BILVER']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILVER������")

    if TradeContext.existVariable('BILNO'):
        to_dict['BILNO'] = TradeContext.BILNO
        AfaLoggerFunc.tradeDebug('bilbka[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILNO������")

    if TradeContext.existVariable('CHRGTYP'):
        to_dict['CHRGTYP'] = TradeContext.CHRGTYP
        AfaLoggerFunc.tradeDebug('bilbka[CHRGTYP] = ' + str(to_dict['CHRGTYP']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CHRGTYP������")

    if TradeContext.existVariable('LOCCUSCHRG'):
        to_dict['LOCCUSCHRG'] = TradeContext.LOCCUSCHRG
        AfaLoggerFunc.tradeDebug('bilbka[LOCCUSCHRG] = ' + str(to_dict['LOCCUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.LOCCUSCHRG������")

    if TradeContext.existVariable('BILRS'):
        to_dict['BILRS'] = TradeContext.BILRS
        AfaLoggerFunc.tradeDebug('bilbka[BILRS] = ' + str(to_dict['BILRS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BILRS������")

    if TradeContext.existVariable('HPCUSQ'):
        to_dict['HPCUSQ'] = TradeContext.HPCUSQ
        AfaLoggerFunc.tradeDebug('bilbka[HPCUSQ] = ' + str(to_dict['HPCUSQ']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.HPCUSQ������")

    if TradeContext.existVariable('HPSTAT'):
        to_dict['HPSTAT'] = TradeContext.HPSTAT
        AfaLoggerFunc.tradeDebug('bilbka[HPSTAT] = ' + str(to_dict['HPSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.HPSTAT������")

    if TradeContext.existVariable('CERTTYPE'):
        to_dict['CERTTYPE'] = TradeContext.CERTTYPE
        AfaLoggerFunc.tradeDebug('bilbka[CERTTYPE] = ' + str(to_dict['CERTTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTTYPE������")

    if TradeContext.existVariable('CERTNO'):
        to_dict['CERTNO'] = TradeContext.CERTNO
        AfaLoggerFunc.tradeDebug('bilbka[CERTNO] = ' + str(to_dict['CERTNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTNO������")

    return True

