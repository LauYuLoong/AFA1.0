# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.��ִ�����ģ��(1.��ִ����).���ȷ��Ӧ���Ľ���
#==============================================================================
#   �����ļ�:   TRCC004_0000.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-10-22
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_mpcbka,rccpsDBTrcc_atcbka


#=====================��ִ���Ի�����(���ز���)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo(" ũ����ϵͳ������.���������(1.��ִ����).���ȷ��Ӧ���Ľ���[TRCC004_1160]���� ")
    
    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #=================ƥ��ԭ������Ϣ===========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼƥ��ԭ��������Ϣ")
    
    wtr_dict = {}
    if not rccpsDBFunc.getTransWtrCK(TradeContext.SNDBNKCO,TradeContext.TRCDAT,TradeContext.TRCNO,wtr_dict):
        return AfaFlowControl.ExitThisFlow('S999', "ƥ��ԭ��������Ϣ�쳣")
    
    TradeContext.BJEDTE = wtr_dict['BJEDTE']
    TradeContext.BSPSQN = wtr_dict['BSPSQN']
    
    AfaLoggerFunc.tradeInfo(">>>����ƥ��ԭ��������Ϣ")
    
    #=================��Ҫ�Լ��===============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ���б�Ҫ�Լ��")
    
    #=================����˽����ѱ����������,��ֹͣ����============================
    
    where_sql = "ORMFN = '" + wtr_dict['MSGFLGNO'] + "'"
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ���˽����Ƿ��ѱ�����")
    
    ret = rccpsDBTrcc_atcbka.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","��ѯ�����Ǽǲ��쳣,�˳�������")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��д��ڶԴ˽��׵ĳ���,�˳�������")
        
    AfaLoggerFunc.tradeInfo(">>>�������˽����Ƿ��ѱ�����")
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ���˽����Ƿ��ѱ�����")
    
    ret = rccpsDBTrcc_mpcbka.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","��ѯ�����Ǽǲ��쳣,�˳�������")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��д��ڶԴ˽��׵ĳ���,�˳�������")
        
    AfaLoggerFunc.tradeInfo(">>>�������˽����Ƿ��ѱ�����")
    
    AfaLoggerFunc.tradeInfo(">>>�������б�Ҫ�Լ��")
    
    #=================����ҵ��״̬Ϊ����=======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���㴦����")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ���㴦�����쳣")
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���㴦����")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ����ɹ�")
    
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['BCSTAT']  = PL_BCSTAT_MFESTL
    stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
    stat_dict['PRCCO']   = TradeContext.PRCCO
    stat_dict['STRINFO'] = TradeContext.STRINFO
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ɹ��쳣")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ����ɹ�")
    
    AfaLoggerFunc.tradeInfo(" ũ����ϵͳ������.���������(1.��ִ����).���ȷ��Ӧ���Ľ���[TRCC004_1160]�˳� ")
    
    return True
