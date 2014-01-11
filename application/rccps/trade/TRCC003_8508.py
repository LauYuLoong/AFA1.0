# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���Ĳ���).����ֹ������
#===============================================================================
#   �����ļ�:   TRCC003_8508.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsMap8508CTradeContext2Dexistp_dict,rccpsDBTrcc_existp,rccpsGetFunc
from types import *
from rccpsConst import *

#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('>>>��ʼ�������ֹ���������')
    #=====��ʼȡ������ˮ��Ϣ====
    trcbka = {}
    ret = rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka)   
    if ret == False:
        return AfaFlowControl.ExitThisFlow('M999','ȡ������Ϣʧ��')

    AfaLoggerFunc.tradeInfo('trckba=' + str(trcbka))
    TRCCO  =  trcbka['TRCCO']

    #=====�Ƿ���Ҫ�ж�״̬������״̬�����ҵ����====
    if trcbka['BJEDTE'] != TradeContext.BJEDTE:
        return AfaFlowControl.ExitThisFlow('M999','��ǰ������['+TradeContext.BJEDTE+']�������ͽ���ֹ������')
    if not (trcbka['BCSTAT'] == PL_BCSTAT_MFESTL and trcbka['BDWFLG'] == PL_BDWFLG_SUCC): 
        return AfaFlowControl.ExitThisFlow('M999','��ǰ״̬['+str(trcbka['BCSTAT'])+']�������ͽ���ֹ������')
    if TRCCO[0:2]  != '20': 
        return AfaFlowControl.ExitThisFlow('M999','��ǰҵ������['+str(trcbka['TRCCO'])+']�������ͽ���ֹ������')
    if trcbka['BRSFLG'] != PL_BRSFLG_SND:
        return AfaFlowControl.ExitThisFlow('M999','��ǰ������ʶ['+str(trcbka['BRSFLG'])+']�������ͽ���ֹ������')

    #=====��ʼ���ֵ丳ֵ====
    TradeContext.ORTRCCO   = trcbka['TRCCO']
    TradeContext.CUR       = trcbka['CUR']
    TradeContext.OCCAMT    = trcbka['OCCAMT']
    TradeContext.RCVBNKCO  = trcbka['RCVBNKCO']
    TradeContext.RCVBNKNM  = trcbka['RCVBNKNM']
    existp_dict = {}
    if not rccpsMap8508CTradeContext2Dexistp_dict.map(existp_dict):
        return AfaFlowControl.ExitThisFlow('M999', '�ֵ丳ֵ����')

    #=====��ʼ���볷��ֹ���Ǽǲ�====
    if not rccpsDBTrcc_existp.insertCmt(existp_dict):
        return AfaFlowControl.ExitThisFlow('D002', '�������ݿ����,RollBack�ɹ�')
    else:
        AfaLoggerFunc.tradeInfo('COMMIT�ɹ�')

    #=====ͨ�������к�ȡ��Ա�кź�����====
    TradeContext.RCVBNKCO = trcbka['RCVBNKCO']
    TradeContext.RCVBNKNM = trcbka['RCVBNKNM']
    rccpsGetFunc.GetRcvBnkCo(trcbka['RCVBNKCO'])
   
    #=====��ֵȡ����====
    TradeContext.ORTRCDAT = trcbka['TRCDAT']
    TradeContext.ORTRCNO  = trcbka['TRCNO']
    TradeContext.ORSNDBNK = trcbka['SNDBNKCO']
    TradeContext.ORRCVBNK = trcbka['RCVBNKCO']
    TradeContext.ORCUR    = trcbka['CUR']
    TradeContext.OROCCAMT = str(trcbka['OCCAMT'])
    TradeContext.ORTRCCO  = trcbka['TRCCO']
    TradeContext.OPRTYPNO = '99'
    TradeContext.ROPRTYPNO =TradeContext.ORTRCCO[0:2] 
    return True

#=====================���׺���================================================
def SubModuleDoSnd():
    #=====�ж�afe����====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)

    TradeContext.errorMsg  =  '���ķ��ͳɹ�' 
    
    return True
    
