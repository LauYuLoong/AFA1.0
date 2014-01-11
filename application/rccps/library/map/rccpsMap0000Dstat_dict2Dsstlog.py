# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ stat_dict �ֵ䵽 sstlog �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dstat_dict2Dsstlog.py
#   �޸�ʱ��:   Mon Jun 23 17:35:54 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('sstlog[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeWarn("�������ڲ���Ϊ��")
        return False

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('sstlog[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeWarn("������Ų���Ϊ��")
        return False

    if from_dict.has_key('BCURSQ'):
        to_dict['BCURSQ'] = from_dict['BCURSQ']
        AfaLoggerFunc.tradeDebug('sstlog[BCURSQ] = ' + str(to_dict['BCURSQ']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BCURSQ']������")

    if from_dict.has_key('BESBNO'):
        to_dict['BESBNO'] = from_dict['BESBNO']
        AfaLoggerFunc.tradeDebug('sstlog[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BESBNO']������")

    if from_dict.has_key('BEACSB'):
        to_dict['BEACSB'] = from_dict['BEACSB']
        AfaLoggerFunc.tradeDebug('sstlog[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BEACSB']������")

    if from_dict.has_key('BETELR'):
        to_dict['BETELR'] = from_dict['BETELR']
        AfaLoggerFunc.tradeDebug('sstlog[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BETELR']������")

    if from_dict.has_key('BEAUUS'):
        to_dict['BEAUUS'] = from_dict['BEAUUS']
        AfaLoggerFunc.tradeDebug('sstlog[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BEAUUS']������")

    if from_dict.has_key('FEDT'):
        to_dict['FEDT'] = from_dict['FEDT']
        AfaLoggerFunc.tradeDebug('sstlog[FEDT] = ' + str(to_dict['FEDT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['FEDT']������")

    if from_dict.has_key('RBSQ'):
        to_dict['RBSQ'] = from_dict['RBSQ']
        AfaLoggerFunc.tradeDebug('sstlog[RBSQ] = ' + str(to_dict['RBSQ']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['RBSQ']������")

    if from_dict.has_key('TRDT'):
        to_dict['TRDT'] = from_dict['TRDT']
        AfaLoggerFunc.tradeDebug('sstlog[TRDT] = ' + str(to_dict['TRDT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['TRDT']������")

    if from_dict.has_key('TLSQ'):
        to_dict['TLSQ'] = from_dict['TLSQ']
        AfaLoggerFunc.tradeDebug('sstlog[TLSQ] = ' + str(to_dict['TLSQ']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['TLSQ']������")

    if from_dict.has_key('SBAC'):
        to_dict['SBAC'] = from_dict['SBAC']
        AfaLoggerFunc.tradeDebug('sstlog[SBAC] = ' + str(to_dict['SBAC']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['SBAC']������")

    if from_dict.has_key('ACNM'):
        to_dict['ACNM'] = from_dict['ACNM']
        AfaLoggerFunc.tradeDebug('sstlog[ACNM] = ' + str(to_dict['ACNM']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['ACNM']������")

    if from_dict.has_key('RBAC'):
        to_dict['RBAC'] = from_dict['RBAC']
        AfaLoggerFunc.tradeDebug('sstlog[RBAC] = ' + str(to_dict['RBAC']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['RBAC']������")

    if from_dict.has_key('OTNM'):
        to_dict['OTNM'] = from_dict['OTNM']
        AfaLoggerFunc.tradeDebug('sstlog[OTNM] = ' + str(to_dict['OTNM']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['OTNM']������")

    if from_dict.has_key('DASQ'):
        to_dict['DASQ'] = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('sstlog[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['DASQ']������")

    if from_dict.has_key('MGID'):
        to_dict['MGID'] = from_dict['MGID']
        AfaLoggerFunc.tradeDebug('sstlog[MGID] = ' + str(to_dict['MGID']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['MGID']������")

    if from_dict.has_key('PRCCO'):
        to_dict['PRCCO'] = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('sstlog[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['PRCCO']������")

    if from_dict.has_key('STRINFO'):
        to_dict['STRINFO'] = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('sstlog[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['STRINFO']������")

    if from_dict.has_key('BCSTAT'):
        to_dict['BCSTAT'] = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('sstlog[BCSTAT] = ' + str(to_dict['BCSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BCSTAT']������")
        return False

    if from_dict.has_key('BDWFLG'):
        to_dict['BDWFLG'] = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('sstlog[BDWFLG] = ' + str(to_dict['BDWFLG']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BDWFLG']������")
        return False

    if from_dict.has_key('PRTCNT'):
        to_dict['PRTCNT'] = from_dict['PRTCNT']
        AfaLoggerFunc.tradeDebug('sstlog[PRTCNT] = ' + str(to_dict['PRTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['PRTCNT']������")

    if from_dict.has_key('BJETIM'):
        to_dict['BJETIM'] = from_dict['BJETIM']
        AfaLoggerFunc.tradeDebug('sstlog[BJETIM] = ' + str(to_dict['BJETIM']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BJETIM']������")

    if from_dict.has_key('NOTE1'):
        to_dict['NOTE1'] = from_dict['NOTE1']
        AfaLoggerFunc.tradeDebug('sstlog[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['NOTE1']������")

    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('sstlog[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['NOTE2']������")

    if from_dict.has_key('NOTE3'):
        to_dict['NOTE3'] = from_dict['NOTE3']
        AfaLoggerFunc.tradeDebug('sstlog[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['NOTE3']������")

    if from_dict.has_key('NOTE4'):
        to_dict['NOTE4'] = from_dict['NOTE4']
        AfaLoggerFunc.tradeDebug('sstlog[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['NOTE4']������")

    return True

