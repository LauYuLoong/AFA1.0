# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ bilbka �ֵ䵽 ztcbka �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap8529Dbilbka2Dztcbka.py
#   �޸�ʱ��:   Sun Sep 14 16:30:04 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('ztcbka[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('ztcbka[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BSPSQN']������")

    if from_dict.has_key('BRSFLG'):
        to_dict['BRSFLG'] = from_dict['BRSFLG']
        AfaLoggerFunc.tradeDebug('ztcbka[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BRSFLG']������")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('ztcbka[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        to_dict['BEACSB'] = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('ztcbka[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEACSB']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('ztcbka[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('ztcbka[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEAUUS']������")

    if from_dict.has_key('BEAUPS'):
        to_dict['BEAUPS'] = from_dict['BEAUPS']
        AfaLoggerFunc.tradeDebug('ztcbka[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEAUPS']������")

    if from_dict.has_key('TERMID'):
        to_dict['TERMID'] = from_dict['TERMID']
        AfaLoggerFunc.tradeDebug('ztcbka[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TERMID']������")

    if from_dict.has_key('BBSSRC'):
        to_dict['BBSSRC'] = from_dict['BBSSRC']
        AfaLoggerFunc.tradeDebug('ztcbka[BBSSRC] = ' + str(to_dict['BBSSRC']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BBSSRC']������")

    if from_dict.has_key('DASQ'):
        to_dict['DASQ'] = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('ztcbka[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['DASQ']������")

    if from_dict.has_key('DCFLG'):
        to_dict['DCFLG'] = from_dict['DCFLG']
        AfaLoggerFunc.tradeDebug('ztcbka[DCFLG] = ' + str(to_dict['DCFLG']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['DCFLG']������")

    if from_dict.has_key('OPRNO'):
        to_dict['OPRNO'] = from_dict['OPRNO']
        AfaLoggerFunc.tradeDebug('ztcbka[OPRNO] = ' + str(to_dict['OPRNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['OPRNO']������")

    if from_dict.has_key('OPRATTNO'):
        to_dict['OPRATTNO'] = from_dict['OPRATTNO']
        AfaLoggerFunc.tradeDebug('ztcbka[OPRATTNO] = ' + str(to_dict['OPRATTNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['OPRATTNO']������")

    if from_dict.has_key('NCCWKDAT'):
        to_dict['NCCWKDAT'] = from_dict['NCCWKDAT']
        AfaLoggerFunc.tradeDebug('ztcbka[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NCCWKDAT']������")

    if from_dict.has_key('TRCCO'):
        to_dict['TRCCO'] = from_dict['TRCCO']
        AfaLoggerFunc.tradeDebug('ztcbka[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCCO']������")

    if from_dict.has_key('TRCDAT'):
        to_dict['TRCDAT'] = from_dict['TRCDAT']
        AfaLoggerFunc.tradeDebug('ztcbka[TRCDAT] = ' + str(to_dict['TRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCDAT']������")

    if from_dict.has_key('TRCNO'):
        to_dict['TRCNO'] = from_dict['TRCNO']
        AfaLoggerFunc.tradeDebug('ztcbka[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRCNO']������")

    if from_dict.has_key('SNDMBRCO'):
        to_dict['SNDMBRCO'] = from_dict['SNDMBRCO']
        AfaLoggerFunc.tradeDebug('ztcbka[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDMBRCO']������")

    if from_dict.has_key('RCVMBRCO'):
        to_dict['RCVMBRCO'] = from_dict['RCVMBRCO']
        AfaLoggerFunc.tradeDebug('ztcbka[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVMBRCO']������")

    if from_dict.has_key('SNDBNKCO'):
        to_dict['SNDBNKCO'] = from_dict['SNDBNKCO']
        AfaLoggerFunc.tradeDebug('ztcbka[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDBNKCO']������")

    if from_dict.has_key('SNDBNKNM'):
        to_dict['SNDBNKNM'] = from_dict['SNDBNKNM']
        AfaLoggerFunc.tradeDebug('ztcbka[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SNDBNKNM']������")

    if from_dict.has_key('RCVBNKCO'):
        to_dict['RCVBNKCO'] = from_dict['RCVBNKCO']
        AfaLoggerFunc.tradeDebug('ztcbka[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVBNKCO']������")

    if from_dict.has_key('RCVBNKNM'):
        to_dict['RCVBNKNM'] = from_dict['RCVBNKNM']
        AfaLoggerFunc.tradeDebug('ztcbka[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RCVBNKNM']������")

    if from_dict.has_key('BILVER'):
        to_dict['BILVER'] = from_dict['BILVER']
        AfaLoggerFunc.tradeDebug('ztcbka[BILVER] = ' + str(to_dict['BILVER']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILVER']������")

    if from_dict.has_key('BILNO'):
        to_dict['BILNO'] = from_dict['BILNO']
        AfaLoggerFunc.tradeDebug('ztcbka[BILNO] = ' + str(to_dict['BILNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILNO']������")

    if from_dict.has_key('CHRGTYP'):
        to_dict['CHRGTYP'] = from_dict['CHRGTYP']
        AfaLoggerFunc.tradeDebug('ztcbka[CHRGTYP] = ' + str(to_dict['CHRGTYP']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CHRGTYP']������")

    if from_dict.has_key('LOCCUSCHRG'):
        to_dict['LOCCUSCHRG'] = from_dict['LOCCUSCHRG']
        AfaLoggerFunc.tradeDebug('ztcbka[LOCCUSCHRG] = ' + str(to_dict['LOCCUSCHRG']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['LOCCUSCHRG']������")

    if from_dict.has_key('BILRS'):
        to_dict['BILRS'] = from_dict['BILRS']
        AfaLoggerFunc.tradeDebug('ztcbka[BILRS] = ' + str(to_dict['BILRS']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BILRS']������")

    if from_dict.has_key('HPCUSQ'):
        to_dict['HPCUSQ'] = from_dict['HPCUSQ']
        AfaLoggerFunc.tradeDebug('ztcbka[HPCUSQ] = ' + str(to_dict['HPCUSQ']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['HPCUSQ']������")

    if from_dict.has_key('HPSTAT'):
        to_dict['HPSTAT'] = from_dict['HPSTAT']
        AfaLoggerFunc.tradeDebug('ztcbka[HPSTAT] = ' + str(to_dict['HPSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['HPSTAT']������")

    if from_dict.has_key('CERTTYPE'):
        to_dict['CERTTYPE'] = from_dict['CERTTYPE']
        AfaLoggerFunc.tradeDebug('ztcbka[CERTTYPE] = ' + str(to_dict['CERTTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CERTTYPE']������")

    if from_dict.has_key('CERTNO'):
        to_dict['CERTNO'] = from_dict['CERTNO']
        AfaLoggerFunc.tradeDebug('ztcbka[CERTNO] = ' + str(to_dict['CERTNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['CERTNO']������")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('ztcbka[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('ztcbka[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('ztcbka[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('ztcbka[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE4']������")

    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('ztcbka[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BJEDTE']������")

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('ztcbka[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BSPSQN']������")

    if from_dict.has_key('BCURSQ'):
        to_dict['BCURSQ'] = from_dict['BCURSQ']
        AfaLoggerFunc.tradeDebug('ztcbka[BCURSQ] = ' + str(to_dict['BCURSQ']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BCURSQ']������")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('ztcbka[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        to_dict['BEACSB'] = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('ztcbka[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEACSB']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('ztcbka[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('ztcbka[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BEAUUS']������")

    if from_dict.has_key('FEDT'):
        to_dict['FEDT'] = from_dict['FEDT']
        AfaLoggerFunc.tradeDebug('ztcbka[FEDT] = ' + str(to_dict['FEDT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['FEDT']������")

    if from_dict.has_key('RBSQ'):
        to_dict['RBSQ'] = from_dict['RBSQ']
        AfaLoggerFunc.tradeDebug('ztcbka[RBSQ] = ' + str(to_dict['RBSQ']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RBSQ']������")

    if from_dict.has_key('TRDT'):
        to_dict['TRDT'] = from_dict['TRDT']
        AfaLoggerFunc.tradeDebug('ztcbka[TRDT] = ' + str(to_dict['TRDT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TRDT']������")

    if from_dict.has_key('TLSQ'):
        to_dict['TLSQ'] = from_dict['TLSQ']
        AfaLoggerFunc.tradeDebug('ztcbka[TLSQ] = ' + str(to_dict['TLSQ']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['TLSQ']������")

    if from_dict.has_key('SBAC'):
        to_dict['SBAC'] = from_dict['SBAC']
        AfaLoggerFunc.tradeDebug('ztcbka[SBAC] = ' + str(to_dict['SBAC']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['SBAC']������")

    if from_dict.has_key('ACNM'):
        to_dict['ACNM'] = from_dict['ACNM']
        AfaLoggerFunc.tradeDebug('ztcbka[ACNM] = ' + str(to_dict['ACNM']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['ACNM']������")

    if from_dict.has_key('RBAC'):
        to_dict['RBAC'] = from_dict['RBAC']
        AfaLoggerFunc.tradeDebug('ztcbka[RBAC] = ' + str(to_dict['RBAC']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['RBAC']������")

    if from_dict.has_key('OTNM'):
        to_dict['OTNM'] = from_dict['OTNM']
        AfaLoggerFunc.tradeDebug('ztcbka[OTNM] = ' + str(to_dict['OTNM']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['OTNM']������")

    if from_dict.has_key('DASQ'):
        to_dict['DASQ'] = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('ztcbka[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['DASQ']������")

    if from_dict.has_key('MGID'):
        to_dict['MGID'] = from_dict['MGID']
        AfaLoggerFunc.tradeDebug('ztcbka[MGID] = ' + str(to_dict['MGID']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['MGID']������")

    if from_dict.has_key('PRCCO'):
        to_dict['PRCCO'] = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('ztcbka[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['PRCCO']������")

    if from_dict.has_key('STRINFO'):
        to_dict['STRINFO'] = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('ztcbka[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['STRINFO']������")

    if from_dict.has_key('BCSTAT'):
        to_dict['BCSTAT'] = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('ztcbka[BCSTAT] = ' + str(to_dict['BCSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BCSTAT']������")

    if from_dict.has_key('BDWFLG'):
        to_dict['BDWFLG'] = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('ztcbka[BDWFLG] = ' + str(to_dict['BDWFLG']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BDWFLG']������")

    if from_dict.has_key('PRTCNT'):
        to_dict['PRTCNT'] = from_dict['PRTCNT']
        AfaLoggerFunc.tradeDebug('ztcbka[PRTCNT] = ' + str(to_dict['PRTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['PRTCNT']������")

    if from_dict.has_key('BJETIM'):
        to_dict['BJETIM'] = from_dict['BJETIM']
        AfaLoggerFunc.tradeDebug('ztcbka[BJETIM] = ' + str(to_dict['BJETIM']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['BJETIM']������")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('ztcbka[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('ztcbka[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('ztcbka[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('ztcbka[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("bilbka['NOTE4']������")

    return True

