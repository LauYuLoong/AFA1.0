# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).Ʊ�ݲ�ѯ����
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   �޸�ʱ��:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_pjcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1125CTradeContext2Dpjcbka_dict,rccpsDBFunc

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
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
        AfaLoggerFunc.tradeInfo("Ʊ�ݲ�ѯ�鸴�Ǽǲ��д�����ͬ��ѯ����,�˱���Ϊ�ظ�����,ֱ�ӽ�����һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
        out_context_dict['STRINFO']  = '�ظ�����'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>��������Ƿ��ظ�����")
    
    #==========ΪƱ�ݲ�ѯ�鸴�Ǽǲ��ֵ丳ֵ================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪƱ�ݲ�ѯ�鸴�Ǽǲ��ֵ丳ֵ")
    
    TradeContext.ISDEAL = PL_ISDEAL_UNDO
    
    pjcbka_insert_dict = {}
    if not rccpsMap1125CTradeContext2Dpjcbka_dict.map(pjcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","ΪƱ�ݲ�ѯ�鸴�Ǽǲ��ֵ丳ֵ�쳣")
        
    AfaLoggerFunc.tradeInfo(">>>����ΪƱ�ݲ�ѯ�鸴�Ǽǲ��ֵ丳ֵ")
    
    #==========�Ǽ�Ʊ�ݲ�ѯ�鸴�Ǽǲ�======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�Ʊ�ݲ�ѯ�鸴�Ǽǲ�")
    AfaLoggerFunc.tradeInfo(">>>" + str(TradeContext.SNDBNKNM))
    
    ret = rccpsDBTrcc_pjcbka.insertCmt(pjcbka_insert_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�Ǽ�Ʊ�ݲ�ѯ�鸴�Ǽǲ��쳣") 
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ�Ʊ�ݲ�ѯ�鸴�Ǽǲ�")
    
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
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow("S999","����ͨѶ��ִ�����쳣")
        
    return True
