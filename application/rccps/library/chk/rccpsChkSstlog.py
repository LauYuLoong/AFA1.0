# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ.���������
#=================================================================
#   �����ļ�:   rccpsChkSstlog.py
#   �޸�ʱ��:   2008-06-07
##################################################################
import TradeContext,AfaLoggerFunc
from types import *
import exceptions,os,time

################################################################################
# ������:    ChkSstlog()
# ����:      �� 
# ����ֵ��    True  ����״̬�ɹ�    False ����״̬ʧ��
# ����˵����  �����е��ֶ��Ƿ���� 
# ��дʱ�䣺   2008-6-5
# ���ߣ�       ������
################################################################################
def ChkSstlog():
    #=====��ʼ�ֶμ��====
    AfaLoggerFunc.tradeInfo( '>>>��ʼSstlog���ֶμ��' )
    #=====�жϽ��������Ƿ����====
    if  TradeContext.existVariable( "BEJDTE" ):
        sstlog["BJEDTE"] = TradeContext.BJEDTE
    else:
        TradeContext.errorCode = 'O201'
        TradeContext.errorMsg  = '�������ڲ�����'
        return False
    #=====�жϱ�������Ƿ����====
    if  TradeContext.existVariable( "BSPSQN" ):
        sstlog["BSPSQN"] = TradeContext.BSPSQN
    else:
        TradeContext.errorCode = 'M006'
        TradeContext.errorMsg  = '������Ų�����'
        return False
    #====�ж�״̬�Ƿ����====
    if TradeContext.existVariable( "BCSTAT" ):
        sstlog["BCSTAT"] = TradeContext.BCSTAT
    else:
        sstlog["BCSTAT"] = ''
    #=====�ж���ת�����־�Ƿ����====
    if TradeContext.existVariable( "BDWFLG" ):
        sstlog["BDWFLG"] = TradeContext.BDWFLG
    else:
        sstlog["BDWFLG"] = ''
    #=====�жϱ�ע1�Ƿ����====
    if TradeContext.existVariable( 'NOTE1' ):
        sstlog['NOTE1'] = TradeContext.NOTE1
    else:
        sstlog['NOTE1'] = ''
    #=====�жϱ�ע2�Ƿ����====
    if TradeContext.existVariable( 'NOTE2' ):
        sstlog['NOTE2'] = TradeContext.NOTE2
    else:
        sstlog['NOTE2'] = ''
    #=====�жϱ�ע3�Ƿ����====
    if TradeContext.existVariable( 'NOTE3' ):
        sstlog['NOTE3'] = TradeContext.NOTE3
    else:
        sstlog['NOTE3'] = ''
    #=====�жϱ�ע4�Ƿ����====
    if TradeContext.existVariable( 'NOTE4' ):
        sstlog['NOTE4'] = TradeContext.NOTE4
    else:
        sstlog['NOTE4'] = ''
    return sstlog
