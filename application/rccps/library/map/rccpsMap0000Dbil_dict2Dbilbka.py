# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ bil_dict �ֵ䵽 bilbka �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dbil_dict2Dbilbka.py
#   �޸�ʱ��:   Sun Sep 14 16:24:51 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('bilbka[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('bilbka[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BSPSQN']������")

    if from_dict.has_key('BRSFLG'):
        to_dict['BRSFLG'] = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('bilbka[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BRSFLG']������")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('bilbka[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        to_dict['BEACSB'] = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('bilbka[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BEACSB']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('bilbka[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('bilbka[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BEAUUS']������")

    if from_dict.has_key('BEAUPS'):
        to_dict['BEAUPS'] = from_dict['BEAUPS']
        AfaLoggerFunc.tradeDebug('bilbka[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BEAUPS']������")

    if from_dict.has_key('TERMID'):
        to_dict['TERMID'] = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('bilbka[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['TERMID']������")

    if from_dict.has_key('BBSSRC'):
        to_dict['BBSSRC'] = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('bilbka[BBSSRC] = ' + str(to_dict['BBSSRC']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BBSSRC']������")

    if from_dict.has_key('DASQ'):
        to_dict['DASQ'] = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('bilbka[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['DASQ']������")

    if from_dict.has_key('DCFLG'):
        to_dict['DCFLG'] = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('bilbka[DCFLG] = ' + str(to_dict['DCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['DCFLG']������")

    if from_dict.has_key('OPRNO'):
        to_dict['OPRNO'] = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('bilbka[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['OPRNO']������")

    if from_dict.has_key('OPRATTNO'):
        to_dict['OPRATTNO'] = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('bilbka[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['OPRATTNO']������")

    if from_dict.has_key('NCCWKDAT'):
        to_dict['NCCWKDAT'] = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('bilbka[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NCCWKDAT']������")

    if from_dict.has_key('TRCCO'):
        to_dict['TRCCO'] = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('bilbka[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['TRCCO']������")

    if from_dict.has_key('TRCDAT'):
        to_dict['TRCDAT'] = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('bilbka[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        to_dict['TRCNO'] = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('bilbka[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['TRCNO']������")

    if from_dict.has_key('SNDMBRCO'):
        to_dict['SNDMBRCO'] = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('bilbka[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['SNDMBRCO']������")

    if from_dict.has_key('RCVMBRCO'):
        to_dict['RCVMBRCO'] = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('bilbka[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['RCVMBRCO']������")

    if from_dict.has_key('SNDBNKCO'):
        to_dict['SNDBNKCO'] = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('bilbka[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        to_dict['SNDBNKNM'] = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('bilbka[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        to_dict['RCVBNKCO'] = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('bilbka[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        to_dict['RCVBNKNM'] = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('bilbka[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['RCVBNKNM']������")

    if from_dict.has_key('BILVER'):
        to_dict['BILVER'] = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('bilbka[BILVER] = ' + str(to_dict['BILVER']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILVER']������")

    if from_dict.has_key('BILNO'):
        to_dict['BILNO'] = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('bilbka[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILNO']������")

    if from_dict.has_key('CHRGTYP'):
        to_dict['CHRGTYP'] = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('bilbka[CHRGTYP] = ' + str(to_dict['CHRGTYP']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['CHRGTYP']������")

    if from_dict.has_key('LOCCUSCHRG'):
        to_dict['LOCCUSCHRG'] = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('bilbka[LOCCUSCHRG] = ' + str(to_dict['LOCCUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['LOCCUSCHRG']������")

    if from_dict.has_key('BILRS'):
        to_dict['BILRS'] = from_dict['BILRS']
        AfaLoggerFunc.tradeDebug('bilbka[BILRS] = ' + str(to_dict['BILRS']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['BILRS']������")

    if from_dict.has_key('HPCUSQ'):
        to_dict['HPCUSQ'] = from_dict['HPCUSQ']
        AfaLoggerFunc.tradeDebug('bilbka[HPCUSQ] = ' + str(to_dict['HPCUSQ']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['HPCUSQ']������")

    if from_dict.has_key('HPSTAT'):
        to_dict['HPSTAT'] = from_dict['HPSTAT']
        AfaLoggerFunc.tradeDebug('bilbka[HPSTAT] = ' + str(to_dict['HPSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['HPSTAT']������")

    if from_dict.has_key('CERTTYPE'):
        to_dict['CERTTYPE'] = from_dict['CERTTYPE']
        AfaLoggerFunc.tradeDebug('bilbka[CERTTYPE] = ' + str(to_dict['CERTTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['CERTTYPE']������")

    if from_dict.has_key('CERTNO'):
        to_dict['CERTNO'] = from_dict['CERTNO']
        AfaLoggerFunc.tradeDebug('bilbka[CERTNO] = ' + str(to_dict['CERTNO']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['CERTNO']������")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('bilbka[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('bilbka[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('bilbka[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('bilbka[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("bil_dict['NOTE4']������")

    return True

