# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ.���������
#=================================================================
#   �����ļ�:   rccpsChkTrcbka.py
#   �޸�ʱ��:   2008-06-07
##################################################################
import TradeContext,AfaLoggerFunc
from types import *
import exceptions,os,time

################################################################################
# ������:    ChkTrcbka()
# ����:      �� 
# ����ֵ��    True  ����״̬�ɹ�    False ����״̬ʧ��
# ����˵����  �����е��ֶ��Ƿ���� 
# ��дʱ�䣺   2008-6-5
# ���ߣ�       ������
################################################################################
def ChkTrcbka():
    #=====��ʼ�ֶμ��====
    AfaLoggerFunc.tradeInfo( '>>>��ʼTrcbka���ֶμ��' )
    #=====�жϽ��������Ƿ����====
    if  TradeContext.existVariable( "BEJDTE" ):
        trcbka["BJEDTE"] = TradeContext.BJEDTE
    else:
        TradeContext.errorCode = 'O201'
        TradeContext.errorMsg  = '�������ڲ�����'
        return False
    #=====�жϱ�������Ƿ����====
    if  TradeContext.existVariable( "BSPSQN" ):
        trcbka["BSPSQN"] = TradeContext.BSPSQN
    else:
        TradeContext.errorCode = 'M006'
        TradeContext.errorMsg  = '������Ų�����'
        return False
    #====�ж������˱�ʶ�Ƿ����====
    if  TradeContext.existVariable( "BRSFLG" ):
        trcbka["BRSFLG"] = TradeContext.BRSFLG
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg = '�����˱�ʶ������'
        return False
    #=====�жϻ������Ƿ����====
    if TradeContext.existVariable( "BESBNO" ):
        trcbka["BESBNO"] = TradeContext.BESBNO
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '�����Ų�����'
        return False
    #====�ж�����������Ƿ����====
    if TradeContext.existVariable( "BEACSB" ):
        trcbka["BEACSB"] = TradeContext.BEACSB
    else:
        trcbka["BEACSB"] = ''
    #=====�жϹ�Ա���Ƿ����====
    if TradeContext.existVariable( "BETELR" ):
        trcbka["BETELR"] = TradeContext.BEACSB
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '��Ա�Ų�����'
        return False
    #=====�ж���Ȩ��Ա��====
    if TradeContext.existVariable( "BEAUUS" ):
        trcbka["BEAUUS"] = TradeContext.BEAUUS
    else:
        trcbka["BEAUUS"] = ''
    #====�жϽ����־�Ƿ����====
    if TradeContext.existVariable( "DCFLG" ):
        trcbka["DCFLG"] = TradeContext.DCFLG
    else:
        trcbka["DCFLG"] = ''
    #=====�ж�ҵ������Ƿ����====
    if TradeContext.existVariable( "OPRNO" ):
        trcbka["OPRNO"] = TradeContext.OPRNO
    else:
        trcbka["DCFLG"] = ''
    #=====�ж�ҵ�������Ƿ����====
    if TradeContext.existVariable( "OPRATTNO" ):
        trcbka["OPRATTNO"] = TradeContext.OPRATTNO
    else:
        trcbka["OPRATTNO"] = ''
    #=====�ж����������Ƿ����====
    if TradeContext.existVariable( "NCCWKDAT" ):
        trcbka["NCCWKDAT"]= TradeContext.NCCWKDAT
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '�������ڲ�����'
        return False
    #=====�жϽ��״����Ƿ����====
    if TradeContext.existVariable( "TRCCO" ):
        trcbka["TRCCO"] = TradeContext.TRCCO
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '���״��벻����'
        return False
    #=====�ж�ί�������Ƿ����====
    if TradeContext.existVariable( 'TRCDAT' ):
        trcbka['TRCDAT'] = TradeContext.TRCDAT
    else:
        trcbka['TRCDAT'] = ''
    #=====�жϽ�����ˮ���Ƿ����====
    if TradeContext.existVariable( 'TRCNO' ):
        trcbka['TRCNO'] = TradeContext.TRCNO
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '������ˮ�Ų�����'
        return False
    #=====�жϷ����к��Ƿ����====
    if TradeContext.existVariable( 'SNDBNKCO' ):
        trcbka['SNDBNKCO'] = TradeContext.SNDBNKCO
    else:
        trcbka['SNDBNKCO'] = ''
    #=====�жϷ��������Ƿ����====
    if TradeContext.existVariable( 'SNDBNKNM' ):
        trcbka['SNDBNKCO'] = TradeContext.SNDBNKNM
    else:
        trcbka['SNDBNKCO'] = ''
    #=====�жϽ����к��Ƿ����====
    if TradeContext.existVariable( 'RCVBNKCO' ):
        trcbka['RCVBNKCO'] = TradeContext.RCVBNKCO
    else:
        trcbka['RCVBNKCO'] = ''
    #====�жϽ��������Ƿ����====
    if TradeContext.existVariable( 'RCVBNKNM' ):
        trcbka['RCVBNKNM'] = TradeContext.RCVBNKNM
    else:
        trcbka['RCVBNKNM'] = ''
    #=====�жϽ��������Ƿ����====
    if TradeContext.existVariable( 'CUR' ):
        trcbka['CUR'] = TradeContext.CUR
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '���ֲ�����'
        return False
    #=====�жϽ��׽���Ƿ����====
    if TradeContext.existVariable( 'OCCAMT' ):
        trcbka['OCCAMT'] = TradeContext.OCCAMT
    else:
        TradeContext.errorCode = 'M999'
        TradeContext.errorMsg  = '���׽�����'
        return False
    #=====�ж���������ȡ��ʽ�Ƿ����====
    if TradeContext.existVariable( 'CHRGTYP' ):
        trcbka['CHRGTYP'] = TradeContext.CHRGTYP
    else:
        trcbka['CHRGTYP'] = ''
    #=====�жϱ��ؿͻ��������Ƿ����====
    if TradeContext.existVariable( 'LOCCUSCHRG' ):
        trcbka['LOCCUSCHRG'] = TradeContext.LOCCUSCHRG
    else:
        trcbka['LOCCUSCHRG'] = ''
    #=====�ж���ؿͻ��������Ƿ����====
    if TradeContext.existVariable( 'CUSCHRG' ):
        trcbka['CUSCHRG'] = TradeContext.CUSCHRG
    else:
        trcbka['CUSCHRG'] = ''
    #=====�жϸ������˺��Ƿ����====
    if TradeContext.existVariable( 'PYRACC' ):
        trcbka['PYRACC'] = TradeContext.PYRACC
    else:
        trcbka['PYRACC'] = ''
    #=====�жϸ����˻����Ƿ����====
    if TradeContext.existVariable( 'PYRNAM' ):
        trcbka['PYRNAM'] = TradeContext.PYRNAM
    else:
        trcbka['PYRNAM'] = ''
    #=====�жϸ����˵�ַ�Ƿ����====
    if TradeContext.existVariable( 'PYRADDR' ):
        trcbka['PYRADDR'] = TradeContext.PYRADDR
    else:
        trcbka['PYRADDR'] = ''
    #=====�ж��տ����˺��Ƿ����====
    if TradeContext.existVariable( 'PYEACC' ):
        trcbka['PYEACC'] = TradeContext.PYEACC
    else:
        trcbka['PYEACC'] = ''
    #=====�ж��տ��˻����Ƿ����====
    if TradeContext.existVariable( 'PYENAM' ):
        trcbka['PYENAM'] = TradeContext.PYENAM
    else:
        trcbka['PYENAM'] = ''   
    #=====�жϸ����˵�ַ�Ƿ����====
    if TradeContext.existVariable( 'PYEADDR' ):
        trcbka['PYEADDR'] = TradeContext.PYEADDR
    else:
        trcbka['PYEADDR'] = ''
    #=====�ж���Ѻ�Ƿ����====
    if TradeContext.existVariable( 'SEAL' ):
        trcbka['SEAL'] = TradeContext.SEAL
    else:
        trcbka['SEAL'] = ''
    #=====�ж���;�Ƿ����====
    if TradeContext.existVariable( 'USE' ):
        trcbka['USE'] = TradeContext.USE
    else:
        trcbka['USE'] = ''
    #=====�жϱ�ע�Ƿ����====
    if TradeContext.existVariable( 'REMARK' ):
        trcbka['REMARK'] = TradeContext.REMARK
    else:
        trcbka['REMARK'] = ''
    #=====�ж�Ʊ�������Ƿ����====
    if TradeContext.existVariable( 'BILTYP' ):
        trcbka['BILTYP'] = TradeContext.BILTYP
    else:
        trcbka['BILTYP'] = ''
    #=====�ж�Ʊ�������Ƿ����====
    if TradeContext.existVariable( 'BILDAT' ):
        trcbka['BILDAT'] = TradeContext.BILDAT
    else:
        trcbka['BILDAT'] = ''
    #=====�ж�Ʊ�ݺ����Ƿ����====
    if TradeContext.existVariable( 'BILNO' ):
        trcbka['BILNO'] = TradeContext.BILNO
    else:
        trcbka['BILNO'] = ''
    #=====�ж�ԭ���ս���Ƿ����====
    if TradeContext.existVariable( 'COMAMT' ):
        trcbka['COMAMT'] = TradeContext.COMAMT
    else:
        trcbka['COMAMT'] = ''
    #=====�ж϶ึ����Ƿ����====
    if TradeContext.existVariable( 'OVPAYAMT' ):
        trcbka['OVPAYAMT'] = TradeContext.OVPAYAMT
    else:
        trcbka['OVPAYAMT'] = ''
    #=====�ж��⳥�����Ƿ����====
    if TradeContext.existVariable( 'CPSAMT' ):
        trcbka['CPSAMT'] = TradeContext.CPSAMT
    else:
        trcbka['CPSAMT'] = ''
    #=====�жϾܸ�����Ƿ����====
    if TradeContext.existVariable( 'RFUAMT' ):
        trcbka['RFUAMT'] = TradeContext.RFUAMT
    else:
        trcbka['RFUAMT'] = ''
    #=====�ж�ƾ֤�����Ƿ����====
    if TradeContext.existVariable( 'CERTTYPE' ):
        trcbka['CERTTYPE'] = TradeContext.CERTTYPE
    else:
        trcbka['CERTTYPE'] = ''
    #=====�ж�ƾ֤�����Ƿ����====
    if TradeContext.existVariable( 'CERTNO' ):
        trcbka['CERTNO'] = TradeContext.CERTNO
    else:
        trcbka['CERTNO'] = ''
    #=====�ж�ԭ���������Ƿ����====
    if TradeContext.existVariable( 'BOJEDT' ):
        trcbka['BOJEDT'] = TradeContext.BOJEDT
    else:
        trcbka['BOJEDT'] = ''
    #=====�ж�ԭ��������Ƿ����====
    if TradeContext.existVariable( 'BOSPSQ' ):
        trcbka['BOSPSQ'] = TradeContext.BOSPSQ
    else:
        trcbka['BOSPSQ'] = ''
    #=====�ж�ԭί�������Ƿ����====
    if TradeContext.existVariable( 'ORTRCDAT' ):
        trcbka['ORTRCDAT'] = TradeContext.ORTRCDAT
    else:
        trcbka['ORTRCDAT'] = ''
    #=====�ж�ԭ���״����Ƿ����====
    if TradeContext.existVariable( 'ORTRCCO' ):
        trcbka['ORTRCCO'] = TradeContext.ORTRCCO
    else:
        trcbka['ORTRCCO'] = ''
    #=====�ж�ԭ������ˮ���Ƿ����====
    if TradeContext.existVariable( 'ORTRCNO' ):
        trcbka['ORTRCNO'] = TradeContext.ORTRCNO
    else:
        trcbka['ORTRCNO'] = ''
    #=====�ж�ԭ�����к��Ƿ����====
    if TradeContext.existVariable( 'ORSNDBNK' ):
        trcbka['ORSNDBNK'] = TradeContext.ORSNDBNK
    else:
        trcbka['ORSNDBNK'] = ''
    #=====�ж�ԭ�����к��Ƿ����====
    if TradeContext.existVariable( 'ORRCVBNK' ):
        trcbka['ORRCVBNK'] = TradeContext.ORRCVBNK
    else:
        trcbka['ORRCVBNK'] = ''
    #=====�жϸ����Ƿ����====
    if TradeContext.existVariable( 'STRINFO' ):
        trcbka['STRINFO'] = TradeContext.STRINFO
    else:
        trcbka['STRINFO'] = ''
    #=====�жϱ�ע1�Ƿ����====
    if TradeContext.existVariable( 'NOTE1' ):
        trcbka['NOTE1'] = TradeContext.NOTE1
    else:
        trcbka['NOTE1'] = ''
    #=====�жϱ�ע2�Ƿ����====
    if TradeContext.existVariable( 'NOTE2' ):
        trcbka['NOTE2'] = TradeContext.NOTE2
    else:
        trcbka['NOTE2'] = ''
    #=====�жϱ�ע3�Ƿ����====
    if TradeContext.existVariable( 'NOTE3' ):
        trcbka['NOTE3'] = TradeContext.NOTE3
    else:
        trcbka['NOTE3'] = ''
    #=====�жϱ�ע4�Ƿ����====
    if TradeContext.existVariable( 'NOTE4' ):
        trcbka['NOTE4'] = TradeContext.NOTE4
    else:
        trcbka['NOTE4'] = ''
    return trcbka
