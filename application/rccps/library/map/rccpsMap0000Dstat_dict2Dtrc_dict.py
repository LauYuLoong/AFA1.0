# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ stat_dict �ֵ䵽 trc_dict �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dstat_dict2Dtrc_dict.py
#   �޸�ʱ��:   Mon Jun 16 20:04:21 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('FEDT'):
        to_dict['FEDT'] = from_dict['FEDT']
        AfaLoggerFunc.tradeDebug('trc_dict[FEDT] = ' + str(to_dict['FEDT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['FEDT']������")

    if from_dict.has_key('RBSQ'):
        to_dict['RBSQ'] = from_dict['RBSQ']
        AfaLoggerFunc.tradeDebug('trc_dict[RBSQ] = ' + str(to_dict['RBSQ']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['RBSQ']������")

    if from_dict.has_key('TRDT'):
        to_dict['TRDT'] = from_dict['TRDT']
        AfaLoggerFunc.tradeDebug('trc_dict[TRDT] = ' + str(to_dict['TRDT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['TRDT']������")

    if from_dict.has_key('TLSQ'):
        to_dict['TLSQ'] = from_dict['TLSQ']
        AfaLoggerFunc.tradeDebug('trc_dict[TLSQ] = ' + str(to_dict['TLSQ']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['TLSQ']������")

    if from_dict.has_key('SBAC'):
        to_dict['SBAC'] = from_dict['SBAC']
        AfaLoggerFunc.tradeDebug('trc_dict[SBAC] = ' + str(to_dict['SBAC']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['SBAC']������")

    if from_dict.has_key('ACNM'):
        to_dict['ACNM'] = from_dict['ACNM']
        AfaLoggerFunc.tradeDebug('trc_dict[ACNM] = ' + str(to_dict['ACNM']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['ACNM']������")

    if from_dict.has_key('RBAC'):
        to_dict['RBAC'] = from_dict['RBAC']
        AfaLoggerFunc.tradeDebug('trc_dict[RBAC] = ' + str(to_dict['RBAC']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['RBAC']������")

    if from_dict.has_key('OTNM'):
        to_dict['OTNM'] = from_dict['OTNM']
        AfaLoggerFunc.tradeDebug('trc_dict[OTNM] = ' + str(to_dict['OTNM']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['OTNM']������")

    if from_dict.has_key('DASQ'):
        to_dict['DASQ'] = from_dict['DASQ']
        AfaLoggerFunc.tradeDebug('trc_dict[DASQ] = ' + str(to_dict['DASQ']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['DASQ']������")

    if from_dict.has_key('MGID'):
        to_dict['MGID'] = from_dict['MGID']
        AfaLoggerFunc.tradeDebug('trc_dict[MGID] = ' + str(to_dict['MGID']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['MGID']������")

    if from_dict.has_key('PRCCO'):
        to_dict['PRCCO'] = from_dict['PRCCO']
        AfaLoggerFunc.tradeDebug('trc_dict[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['PRCCO']������")

    if from_dict.has_key('STRINFO'):
        to_dict['STRINFO'] = from_dict['STRINFO']
        AfaLoggerFunc.tradeDebug('trc_dict[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['STRINFO']������")

    if from_dict.has_key('BCSTAT'):
        to_dict['BCSTAT'] = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('trc_dict[BCSTAT] = ' + str(to_dict['BCSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BCSTAT']������")

    if from_dict.has_key('BDWFLG'):
        to_dict['BDWFLG'] = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('trc_dict[BDWFLG] = ' + str(to_dict['BDWFLG']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BDWFLG']������")

    if from_dict.has_key('PRTCNT'):
        to_dict['PRTCNT'] = from_dict['PRTCNT']
        AfaLoggerFunc.tradeDebug('trc_dict[PRTCNT] = ' + str(to_dict['PRTCNT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['PRTCNT']������")

    if from_dict.has_key('BJETIM'):
        to_dict['BJETIM'] = from_dict['BJETIM']
        AfaLoggerFunc.tradeDebug('trc_dict[BJETIM] = ' + str(to_dict['BJETIM']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BJETIM']������")
        
    #===�ź�����20091230===
    if from_dict.has_key('NOTE2'):
        to_dict['NOTE2'] = from_dict['NOTE2']
        AfaLoggerFunc.tradeDebug('trc_dict[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['NOTE2']������")

    return True

