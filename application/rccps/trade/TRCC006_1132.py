# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).��Ʊ�鸴�����
#===============================================================================
#   �����ļ�:   TRCC006_1132.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-20
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_hpcbka
import rccpsMap0000Dout_context2CTradeContext,rccpsMap1132CTradeContext2Dhpcbka


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("***ũ����ϵͳ������.���������(1.���ز���).��Ʊ�鸴�����[TRC006_1132]����***")
    
    #================����Ƿ��ظ�����===========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    
    hpcbka_where_dict = {}
    hpcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    hpcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    hpcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    hpcbka_dict = rccpsDBTrcc_hpcbka.selectu(hpcbka_where_dict)
    
    if hpcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ������쳣") 
        
    if len(hpcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("ҵ��״̬�Ǽǲ��д�����ͬ�鸴����,�˱���Ϊ�ظ�����,ֱ�ӽ�����һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
    
    #================�ж��Ƿ����ԭ��ѯ����=====================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ����ԭ��ѯ����")
    
    or_hpcbka_where_dict = {}
    or_hpcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    or_hpcbka_where_dict['TRCDAT']   = TradeContext.ORQYDAT
    or_hpcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    or_hpcbka_dict = rccpsDBTrcc_hpcbka.selectu(or_hpcbka_where_dict)
    
    if or_hpcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","��ѯԭ��ѯ������Ϣ�쳣")
        
    if len(or_hpcbka_dict) <= 0:
        AfaLoggerFunc.tradeInfo("��Ʊ�Ǽǲ��в�����ԭ��ѯ����,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
        #======ΪͨѶ��ִ���ĸ�ֵ===============================================
        out_context_dict = {}
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
        out_context_dict['STRINFO']  = '��Ʊ��ѯ�鸴�Ǽǲ��в�����ԭ��ѯ����'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>��������Ƿ����ԭ��ѯ����")
    
    #================Ϊ��Ʊ��ѯ�鸴�Ǽǲ��ֵ丳ֵ===============================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Ʊ��ѯ�鸴�Ǽǲ���ֵ")
    
    #=====����ת��====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'
    
    TradeContext.BOJEDT = or_hpcbka_dict['BJEDTE']
    TradeContext.BOSPSQ = or_hpcbka_dict['BSPSQN']
    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    TradeContext.PYEACC = TradeContext.ORPYENAM
    
    hpcbka_dict = {}
    if not rccpsMap1132CTradeContext2Dhpcbka.map(hpcbka_dict):
        return AfaFlowControl.ExitThisFlow("S999","Ϊ��Ʊ��ѯ�鸴�Ǽǲ���ֵ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ��Ʊ��ѯ�鸴�Ǽǲ���ֵ")
    
    #================�Ǽǲ�ѯ�鸴�Ǽǲ�=========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǲ�ѯ�鸴�Ǽǲ�")
    
    ret = rccpsDBTrcc_hpcbka.insertCmt(hpcbka_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǻ�Ʊ��ѯ�鸴�Ǽǲ��쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǲ�ѯ�鸴�Ǽǲ�")
    
    #================ΪͨѶ��ִ���ĸ�ֵ=========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪͨѶ��ִ���ĸ�ֵ")
    
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
    
    AfaLoggerFunc.tradeInfo(">>>����ΪͨѶ��ִ���ĸ�ֵ")
    
    #=====pgt 0910 ����ԭ���׵Ĳ鸴״̬====
    AfaLoggerFunc.tradeInfo(">>>����ԭ���ײ鸴��ʾ")
    or_hpcbka_where_dict = {}
    or_hpcbka_where_dict = {'BJEDTE':or_hpcbka_dict['BJEDTE'],'BSPSQN':or_hpcbka_dict['BSPSQN']}
    or_hpcbka_update_dict = {'ISDEAL':'1'}
    ret = rccpsDBTrcc_hpcbka.updateCmt(or_hpcbka_update_dict,or_hpcbka_where_dict)
    if( ret < 0 ):
        return AfaFlowControl.ExitThisFlow("S999", "�Ǽǻ�Ʊ��ѯ�鸴�Ǽǲ��쳣")
    
    AfaLoggerFunc.tradeInfo("***ũ����ϵͳ������.���������(1.���ز���).��Ʊ��ѯ�����[TRC006_1132]����***")
    
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("***ũ����ϵͳ������.���������(2.���Ļ�ִ).��Ʊ�鸴�����[TRC006_1132]����***")
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(errorCode,errorMsg)
    
    AfaLoggerFunc.tradeInfo("***ũ����ϵͳ������.���������(2.���Ļ�ִ).��Ʊ�鸴�����[TRC006_1132]����***")
    
    return True
        
