# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).ҵ��״̬�鸴���Ľ���
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_ztcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1108CTradeContext2Dztcbka

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ҵ��״̬�鸴���Ľ���[RCC00R6_1108]����***' )
    
    #==========�ж��Ƿ��ظ�����,������ظ�����,ֱ�ӽ�����һ����=================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    ztcbka_where_dict = {}
    ztcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    ztcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    ztcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    ztcbka_dict = rccpsDBTrcc_ztcbka.selectu(ztcbka_where_dict)
    
    if ztcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ�����ʧ��")
    
    if len(ztcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("ҵ��״̬�Ǽǲ��д�����ͬ�鸴����,�˱���Ϊ�ظ�����,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
        #======ΪͨѶ��ִ���ĸ�ֵ===============================================
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ظ�����'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>��������Ƿ��ظ�����")
    
    #==========�ж��Ƿ����ԭ��ѯ����===========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ����ԭ��ѯ����")
    or_ztcbka_where_dict = {}
    or_ztcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    or_ztcbka_where_dict['TRCDAT']   = TradeContext.OQTDAT
    or_ztcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    or_ztcbka_dict = {}
    or_ztcbka_dict = rccpsDBTrcc_ztcbka.selectu(or_ztcbka_where_dict)
    
    if or_ztcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У��ԭ��ѯ����ʧ��") 
    
    if len(or_ztcbka_dict) <= 0:
        AfaLoggerFunc.tradeInfo("ҵ��״̬�Ǽǲ��в�����ԭ��ѯ����,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
        #======ΪͨѶ��ִ���ĸ�ֵ===============================================
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = 'ҵ��״̬�Ǽǲ��в�����ԭ��ѯ����'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>��������Ƿ����ԭ��ѯ����")
        
    
    #==========Ϊҵ��״̬�鸴�鸴�Ǽǲ��ֵ丳ֵ=================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��ҵ��״̬�Ǽǲ��ֵ丳ֵ")
    
    if or_ztcbka_dict.has_key('BJEDTE'):
        TradeContext.BOJEDT = or_ztcbka_dict['BJEDTE']
    
    if or_ztcbka_dict.has_key('BSPSQN'):
        TradeContext.BOSPSQ = or_ztcbka_dict['BSPSQN']
    
    if TradeContext.existVariable('TRCCO'):
        TradeContext.ORTRCCO = TradeContext.TRCCO
        
    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    
    ztcbka_insert_dict = {}
    if not rccpsMap1108CTradeContext2Dztcbka.map(ztcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","Ϊ�鸴ҵ���ֵ丳ֵ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ��ҵ��״̬�Ǽǲ��ֵ丳ֵ")
    #==========�Ǽ�ҵ��״̬�鸴�鸴�Ǽǲ�=======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�ǼǴ˲鸴ҵ��")
    
    ret = rccpsDBTrcc_ztcbka.insert(ztcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�Ǽ�״̬�鸴�Ǽǲ��쳣") 
    
    AfaLoggerFunc.tradeInfo(">>>�����ǼǴ˲鸴ҵ��")
    
    #======����ԭ��ѯ������Ϣ===================================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ��ѯҵ����Ϣ")
    
    or_ztcbka_update_dict = {}
    or_ztcbka_update_dict['NCCTRCST'] = TradeContext.NCCTRCST
    or_ztcbka_update_dict['MBRTRCST'] = TradeContext.MBRTRCST
    or_ztcbka_update_dict['ISDEAL']   = PL_ISDEAL_ISDO
    
    ret = rccpsDBTrcc_ztcbka.update(or_ztcbka_update_dict,or_ztcbka_where_dict)
    if (ret <= 0):
        return AfaFlowControl.ExitThisFlow("S999","����ԭ��ѯҵ����Ϣ�쳣") 
        
    if not AfaDBFunc.CommitSql():
        AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    AfaLoggerFunc.tradeInfo(">>>��������ԭ��ѯҵ����Ϣ")
    #======ΪͨѶ��ִ���ĸ�ֵ===================================================
    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '�ɹ�'
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ҵ��״̬�鸴���Ľ���[RCC00R6_1108]�˳�***' )
    
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).ҵ��״̬�鸴���Ľ���[RCC00R6_1108]����***' )
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).ҵ��״̬�鸴���Ľ���[RCC00R6_1108]�˳�***' )
    return True
        
