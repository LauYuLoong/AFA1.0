# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ bilbka �ֵ䵽 bil_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dbilbka2Dbil_dict.py
#   �޸�ʱ��:   Sun Sep 14 16:25:28 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('bil_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('bil_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BSPSQN']������")

    if from_dict.has_key('BRSFLG'):
        to_dict['BRSFLG'] = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('bil_dict[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BRSFLG']������")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('bil_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        to_dict['BEACSB'] = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('bil_dict[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEACSB']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('bil_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('bil_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEAUUS']������")

    if from_dict.has_key('BEAUPS'):
        to_dict['BEAUPS'] = from_dict['BEAUPS']
        AfaLoggerFunc.tradeDebug('bil_dict[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEAUPS']������")

    if from_dict.has_key('TERMID'):
        to_dict['TERMID'] = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('bil_dict[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TERMID']������")

    if from_dict.has_key('BBSSRC'):
        to_dict['BBSSRC'] = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('bil_dict[BBSSRC] = ' + str(to_dict['BBSSRC']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BBSSRC']������")

    if from_dict.has_key('DASQ'):
        to_dict['DASQ'] = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('bil_dict[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['DASQ']������")

    if from_dict.has_key('DCFLG'):
        to_dict['DCFLG'] = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('bil_dict[DCFLG] = ' + str(to_dict['DCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['DCFLG']������")

    if from_dict.has_key('OPRNO'):
        to_dict['OPRNO'] = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('bil_dict[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['OPRNO']������")

    if from_dict.has_key('OPRATTNO'):
        to_dict['OPRATTNO'] = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('bil_dict[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['OPRATTNO']������")

    if from_dict.has_key('NCCWKDAT'):
        to_dict['NCCWKDAT'] = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('bil_dict[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NCCWKDAT']������")

    if from_dict.has_key('TRCCO'):
        to_dict['TRCCO'] = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('bil_dict[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCCO']������")

    if from_dict.has_key('TRCDAT'):
        to_dict['TRCDAT'] = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('bil_dict[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        to_dict['TRCNO'] = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('bil_dict[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCNO']������")

    if from_dict.has_key('SNDMBRCO'):
        to_dict['SNDMBRCO'] = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('bil_dict[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDMBRCO']������")

    if from_dict.has_key('RCVMBRCO'):
        to_dict['RCVMBRCO'] = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('bil_dict[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVMBRCO']������")

    if from_dict.has_key('SNDBNKCO'):
        to_dict['SNDBNKCO'] = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('bil_dict[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        to_dict['SNDBNKNM'] = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('bil_dict[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        to_dict['RCVBNKCO'] = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('bil_dict[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        to_dict['RCVBNKNM'] = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('bil_dict[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVBNKNM']������")

    if from_dict.has_key('BILVER'):
        to_dict['BILVER'] = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('bil_dict[BILVER] = ' + str(to_dict['BILVER']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILVER']������")

    if from_dict.has_key('BILNO'):
        to_dict['BILNO'] = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('bil_dict[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILNO']������")

    if from_dict.has_key('CHRGTYP'):
        to_dict['CHRGTYP'] = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('bil_dict[CHRGTYP] = ' + str(to_dict['CHRGTYP']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CHRGTYP']������")

    if from_dict.has_key('LOCCUSCHRG'):
        to_dict['LOCCUSCHRG'] = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('bil_dict[LOCCUSCHRG] = ' + str(to_dict['LOCCUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['LOCCUSCHRG']������")

    if from_dict.has_key('BILRS'):
        to_dict['BILRS'] = from_dict['BILRS']
        AfaLoggerFunc.tradeDebug('bil_dict[BILRS] = ' + str(to_dict['BILRS']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILRS']������")

    if from_dict.has_key('HPCUSQ'):
        to_dict['HPCUSQ'] = from_dict['HPCUSQ']
        AfaLoggerFunc.tradeDebug('bil_dict[HPCUSQ] = ' + str(to_dict['HPCUSQ']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['HPCUSQ']������")

    if from_dict.has_key('HPSTAT'):
        to_dict['HPSTAT'] = from_dict['HPSTAT']
        AfaLoggerFunc.tradeDebug('bil_dict[HPSTAT] = ' + str(to_dict['HPSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['HPSTAT']������")

    if from_dict.has_key('CERTTYPE'):
        to_dict['CERTTYPE'] = from_dict['CERTTYPE']
        AfaLoggerFunc.tradeDebug('bil_dict[CERTTYPE] = ' + str(to_dict['CERTTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CERTTYPE']������")

    if from_dict.has_key('CERTNO'):
        to_dict['CERTNO'] = from_dict['CERTNO']
        AfaLoggerFunc.tradeDebug('bil_dict[CERTNO] = ' + str(to_dict['CERTNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CERTNO']������")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('bil_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('bil_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('bil_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('bil_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE4']������")

    return True

