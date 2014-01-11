# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ.���������
#=================================================================
#   �����ļ�:   rccpsChkSpbsta.py
#   �޸�ʱ��:   2008-06-07
##################################################################
import TradeContext,AfaLoggerFunc
from types import *
import exceptions,os,time

################################################################################
# ������:    ChkSpbsta()
# ����:      �� 
# ����ֵ��    True  ����״̬�ɹ�    False ����״̬ʧ��
# ����˵����  �����е��ֶ��Ƿ���� 
# ��дʱ�䣺   2008-6-5
# ���ߣ�       ������
################################################################################
def ChkSpbsta():
    #=====��ʼ�ֶμ��====
    AfaLoggerFunc.tradeInfo( '>>>��ʼSpbsta���ֶμ��' )
    #=====�жϽ��������Ƿ����====
    if  TradeContext.existVariable( "BEJDTE" ):
        spbsta["BJEDTE"] = TradeContext.BJEDTE
    else:
        TradeContext.errorCode = 'O201'
        TradeContext.errorMsg  = '�������ڲ�����'
        return False
    #=====�жϱ�������Ƿ����====
    if  TradeContext.existVariable( "BSPSQN" ):
        spbsta["BSPSQN"] = TradeContext.BSPSQN
    else:
        TradeContext.errorCode = 'M006'
        TradeContext.errorMsg  = '������Ų�����'
        return False
    #====�ж�״̬�Ƿ����====
    if TradeContext.existVariable( "BCSTAT" ):
        spbsta["BCSTAT"] = TradeContext.BCSTAT
    else:
        spbsta["BCSTAT"] = ''
    #=====�ж���ת�����־�Ƿ����====
    if TradeContext.existVariable( "BDWFLG" ):
        spbsta["BDWFLG"] = TradeContext.BDWFLG
    else:
        spbsta["BDWFLG"] = ''
    #=====�жϱ�ע1�Ƿ����====
    if TradeContext.existVariable( 'NOTE1' ):
        spbsta['NOTE1'] = TradeContext.NOTE1
    else:
        spbsta['NOTE1'] = ''
    #=====�жϱ�ע2�Ƿ����====
    if TradeContext.existVariable( 'NOTE2' ):
        spbsta['NOTE2'] = TradeContext.NOTE2
    else:
        spbsta['NOTE2'] = ''
    #=====�жϱ�ע3�Ƿ����====
    if TradeContext.existVariable( 'NOTE3' ):
        spbsta['NOTE3'] = TradeContext.NOTE3
    else:
        spbsta['NOTE3'] = ''
    #=====�жϱ�ע4�Ƿ����====
    if TradeContext.existVariable( 'NOTE4' ):
        spbsta['NOTE4'] = TradeContext.NOTE4
    else:
        spbsta['NOTE4'] = ''
    return spbsta
