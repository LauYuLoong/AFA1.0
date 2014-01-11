# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ sstlog �ֵ䵽 stat_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dsstlog2Dstat_dict.py
#   �޸�ʱ��:   Mon Jun 23 17:35:34 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('stat_dict[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('stat_dict[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeWarn("������Ų���Ϊ��")
        return False

    if from_dict.has_key('BCURSQ'):
        to_dict['BCURSQ'] = from_dict['BCURSQ']
        AfaLoggerFunc.tradeDebug('stat_dict[BCURSQ] = ' + str(to_dict['BCURSQ']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['BCURSQ']������")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('stat_dict[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        to_dict['BEACSB'] = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('stat_dict[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['BEACSB']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('stat_dict[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('stat_dict[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['BEAUUS']������")

    if from_dict.has_key('FEDT'):
        to_dict['FEDT'] = from_dict['FEDT']
        AfaLoggerFunc.tradeDebug('stat_dict[FEDT] = ' + str(to_dict['FEDT']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['FEDT']������")

    if from_dict.has_key('RBSQ'):
        to_dict['RBSQ'] = from_dict['RBSQ']
        AfaLoggerFunc.tradeDebug('stat_dict[RBSQ] = ' + str(to_dict['RBSQ']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['RBSQ']������")

    if from_dict.has_key('TRDT'):
        to_dict['TRDT'] = from_dict['TRDT']
        AfaLoggerFunc.tradeDebug('stat_dict[TRDT] = ' + str(to_dict['TRDT']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['TRDT']������")

    if from_dict.has_key('TLSQ'):
        to_dict['TLSQ'] = from_dict['TLSQ']
        AfaLoggerFunc.tradeDebug('stat_dict[TLSQ] = ' + str(to_dict['TLSQ']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['TLSQ']������")

    if from_dict.has_key('SBAC'):
        to_dict['SBAC'] = from_dict['SBAC']
        AfaLoggerFunc.tradeDebug('stat_dict[SBAC] = ' + str(to_dict['SBAC']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['SBAC']������")

    if from_dict.has_key('ACNM'):
        to_dict['ACNM'] = from_dict['ACNM']
        AfaLoggerFunc.tradeDebug('stat_dict[ACNM] = ' + str(to_dict['ACNM']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['ACNM']������")

    if from_dict.has_key('RBAC'):
        to_dict['RBAC'] = from_dict['RBAC']
        AfaLoggerFunc.tradeDebug('stat_dict[RBAC] = ' + str(to_dict['RBAC']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['RBAC']������")

    if from_dict.has_key('OTNM'):
        to_dict['OTNM'] = from_dict['OTNM']
        AfaLoggerFunc.tradeDebug('stat_dict[OTNM] = ' + str(to_dict['OTNM']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['OTNM']������")

    if from_dict.has_key('DASQ'):
        to_dict['DASQ'] = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('stat_dict[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['DASQ']������")

    if from_dict.has_key('MGID'):
        to_dict['MGID'] = from_dict['MGID']
        AfaLoggerFunc.tradeDebug('stat_dict[MGID] = ' + str(to_dict['MGID']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['MGID']������")

    if from_dict.has_key('PRCCO'):
        to_dict['PRCCO'] = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('stat_dict[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['PRCCO']������")

    if from_dict.has_key('STRINFO'):
        to_dict['STRINFO'] = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('stat_dict[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['STRINFO']������")

    if from_dict.has_key('BCSTAT'):
        to_dict['BCSTAT'] = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('stat_dict[BCSTAT] = ' + str(to_dict['BCSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['BCSTAT']������")
        return False

    if from_dict.has_key('BDWFLG'):
        to_dict['BDWFLG'] = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('stat_dict[BDWFLG] = ' + str(to_dict['BDWFLG']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['BDWFLG']������")
        return False

    if from_dict.has_key('PRTCNT'):
        to_dict['PRTCNT'] = from_dict['PRTCNT']
        AfaLoggerFunc.tradeDebug('stat_dict[PRTCNT] = ' + str(to_dict['PRTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['PRTCNT']������")

    if from_dict.has_key('BJETIM'):
        to_dict['BJETIM'] = from_dict['BJETIM']
        AfaLoggerFunc.tradeDebug('stat_dict[BJETIM] = ' + str(to_dict['BJETIM']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['BJETIM']������")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('stat_dict[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('stat_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('stat_dict[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('stat_dict[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("sstlog['NOTE4']������")

    return True

