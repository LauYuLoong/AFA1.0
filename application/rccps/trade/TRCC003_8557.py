# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���Ĳ���).�����˻�����ִ����
#===============================================================================
#   �����ļ�:   TRCC003_8557.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-07-25
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_rekbal,rccpsMap8557CTradeContext2Drekbal_dict

#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('>>>��ʼ�����˻�����ִ���ͽ���')

    #=====�ж��ֶ�ֵ�Ƿ����====
    if not TradeContext.existVariable('CHKDAT'):
        return AfaFlowControl.ExitThisFlow('S999','�������ڲ���Ϊ��')
    if not TradeContext.existVariable('OCCAMT'):
        return AfaFlowControl.ExitThisFlow('S999','��������Ϊ��')
    if not TradeContext.existVariable('CHKRST'):
        return AfaFlowControl.ExitThisFlow('S999','���˽������Ϊ��')

    #=====�����ѯrekbal====
    rek_sel = {}
    rek_sel['NCCWKDAT']  =  TradeContext.CHKDAT
    rek_sel['BRSFLG']    =  PL_BRSFLG_RCV

    record = rccpsDBTrcc_rekbal.selectu(rek_sel)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','��ѯ�����˻����֪ͨ�Ǽǲ��쳣')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','��ѯ�����˻����֪ͨ�Ǽǲ��޼�¼')
    else:
        TradeContext.BOJEDT  =  record['BJEDTE']
        TradeContext.BOSPSQ  =  record['BSPSQN']
        TradeContext.TODAYBAL=  record['TODAYBAL']
        TradeContext.LSTDTBAL=  record['LSTDTBAL']
        TradeContext.LBDCFLG =  record['LBDCFLG']
        TradeContext.NTTDCFLG=  record['NTTDCFLG']
        TradeContext.NTTBAL  =  record['NTTBAL']
        TradeContext.BALDCFLG=  record['BALDCFLG']
        TradeContext.AVLBAL  =  record['AVLBAL']
        

    #=====TradeContext���ֵ丳ֵ====
    TradeContext.NTODAYBAL   =  TradeContext.OCCAMT
    TradeContext.SNDMBRCO    =  record['RCVMBRCO']
    TradeContext.RCVMBRCO    =  record['SNDMBRCO']

    rekbal_dict = {}
    if not rccpsMap8557CTradeContext2Drekbal_dict.map(rekbal_dict):
        return AfaFlowControl.ExitThisFlow('S999','�ֵ丳ֵ����')
    
    ret = rccpsDBTrcc_rekbal.insertCmt(rekbal_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999','�Ǽ������˻����֪ͨ�Ǽǲ��쳣')

    #=====��ֵ����ũ��������====
    TradeContext.ORTRCDAT  =  record['TRCDAT']
    TradeContext.ORTRCNO   =  record['TRCNO']
    TradeContext.TODAYBAL  =  TradeContext.OCCAMT
    TradeContext.OPRTYPNO  =  '99'
    TradeContext.ROPRTPNO  =  '99'
    TradeContext.ORMFN     =  record['SNDMBRCO'] + TradeContext.ORTRCDAT + TradeContext.ORTRCNO 
    
    return True
#=====================���׺���================================================
def SubModuleDoSnd():

    #====�ж�afe����====
    if TradeContext.errorCode == '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '�ɹ�'
    return True
    
