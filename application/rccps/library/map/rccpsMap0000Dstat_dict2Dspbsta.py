# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ stat_dict �ֵ䵽 spbsta �ֵ�ӳ�亯��
#
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsMap0000Dstat_dict2Dspbsta.py
#   �޸�ʱ��:   Mon Jun 23 17:37:08 2008
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(from_dict,to_dict):
        
    if from_dict.has_key('BJEDTE'):
        to_dict['BJEDTE'] = from_dict['BJEDTE']
        AfaLoggerFunc.tradeDebug('spbsta[BJEDTE] = ' + str(to_dict['BJEDTE']))
    else:
        AfaLoggerFunc.tradeWarn("BJEDTE����Ϊ��")
        return False

    if from_dict.has_key('BSPSQN'):
        to_dict['BSPSQN'] = from_dict['BSPSQN']
        AfaLoggerFunc.tradeDebug('spbsta[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BSPSQN']������")
        return False

    if from_dict.has_key('BCURSQ'):
        to_dict['BCURSQ'] = from_dict['BCURSQ']
        AfaLoggerFunc.tradeDebug('spbsta[BCURSQ] = ' + str(to_dict['BCURSQ']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BCURSQ']������")

    if from_dict.has_key('BCSTAT'):
        to_dict['BCSTAT'] = from_dict['BCSTAT']
        AfaLoggerFunc.tradeDebug('spbsta[BCSTAT] = ' + str(to_dict['BCSTAT']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BCSTAT']������")
        return False

    if from_dict.has_key('BDWFLG'):
        to_dict['BDWFLG'] = from_dict['BDWFLG']
        AfaLoggerFunc.tradeDebug('spbsta[BDWFLG] = ' + str(to_dict['BDWFLG']))
    else:
        AfaLoggerFunc.tradeDebug("stat_dict['BDWFLG']������")
        return False

    return True

