# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).Ʊ�ݲ鸴����
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   �޸�ʱ��:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_pjcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1126CTradeContext2Dpjcbka_dict

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).Ʊ�ݲ鸴����[RCC00R6_1126]����***' )
    
    #==========�ж��Ƿ��ظ�����,������ظ�����,ֱ�ӽ�����һ����================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    pjcbka_where_dict = {}
    pjcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    pjcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    pjcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    pjcbka_dict = rccpsDBTrcc_pjcbka.selectu(pjcbka_where_dict)
    
    if pjcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ������쳣")
        
        return True
        
    if len(pjcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("Ʊ�ݲ鸴�鸴�Ǽǲ��д�����ͬ�鸴����,�˱���Ϊ�ظ�����,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
    or_pjcbka_where_dict = {}
    or_pjcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    or_pjcbka_where_dict['TRCDAT']   = TradeContext.OQTDAT
    or_pjcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    or_pjcbka_dict = {}
    or_pjcbka_dict = rccpsDBTrcc_pjcbka.selectu(or_pjcbka_where_dict)
    
    if or_pjcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У��ԭ��ѯ����ʧ��") 
    
    if len(or_pjcbka_dict) <= 0:
        AfaLoggerFunc.tradeInfo("Ʊ�ݲ鸴�鸴�Ǽǲ��в�����ԭ��ѯ����,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
    
    #==========ΪƱ�ݲ鸴�鸴�Ǽǲ��ֵ丳ֵ================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪƱ�ݲ鸴�鸴�Ǽǲ��ֵ丳ֵ")
    
    TradeContext.BRSFLG = '1'
    
    if or_pjcbka_dict.has_key('BJEDTE'):
        TradeContext.BOJEDT = or_pjcbka_dict['BJEDTE']
    
    if or_pjcbka_dict.has_key('BSPSQN'):
        TradeContext.BOSPSQ = or_pjcbka_dict['BSPSQN']
    
    #�ر�� 20080728 ɾ��
    #if TradeContext.existVariable('TRCCO'):
    #    TradeContext.ORTRCCO = TradeContext.TRCCO
    TradeContext.ORTRCCO = or_pjcbka_dict['TRCCO']
    
    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    AfaLoggerFunc.tradeDebug(">>>SNDBNKNM" + str(TradeContext.SNDBNKNM) )
    
    pjcbka_insert_dict = {}
    if not rccpsMap1126CTradeContext2Dpjcbka_dict.map(pjcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","ΪƱ�ݲ鸴�鸴�Ǽǲ��ֵ丳ֵ�쳣")
        
    AfaLoggerFunc.tradeInfo(">>>����ΪƱ�ݲ鸴�鸴�Ǽǲ��ֵ丳ֵ")
    
    #==========�Ǽǻ�Բ�ѯ�鸴���ɸ�ʽ�Ǽǲ�=======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�ǼǴ˲鸴ҵ��")
    
    ret = rccpsDBTrcc_pjcbka.insert(pjcbka_insert_dict)
    
    if ret <= 0:
        if not AfaDBFunc.RollbackSql():
            AfaFlowControl.ExitThisFlow("S999","Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        
        return AfaFlowControl.ExitThisFlow("S999","�Ǽ�Ʊ�ݲ鸴�鸴�Ǽǲ��쳣")
        
    AfaLoggerFunc.tradeInfo(">>>�����ǼǴ˲鸴ҵ��")
    
    #======����ԭ��ѯ������Ϣ===================================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ��ѯҵ����Ϣ")
    
    or_pjcbka_update_dict = {}
    or_pjcbka_update_dict['ISDEAL']   = PL_ISDEAL_ISDO
    
    ret = rccpsDBTrcc_pjcbka.update(or_pjcbka_update_dict,or_pjcbka_where_dict)
    if (ret <= 0):
        if not AfaDBFunc.RollbackSql():
            AfaFlowControl.ExitThisFlow("S999","Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        
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
    
    return True 
#=====================���׺���================================================
def SubModuleDoSnd():
    
    return True 
