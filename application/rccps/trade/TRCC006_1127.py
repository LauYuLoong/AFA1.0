# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).��Լ��Ҳ�ѯ����
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   �޸�ʱ��:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_hdcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1127CTradeContext2Dhdcbka_dict
import rccpsDBFunc,rccpsGetFunc

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    #==========�ж��Ƿ��ظ�����,������ظ�����,ֱ�ӽ�����һ����================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    hdcbka_where_dict = {}
    hdcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    hdcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    hdcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    
    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ������쳣")
        
        return True
        
    if len(hdcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��д�����ͬ��ѯ����,�˱���Ϊ�ظ�����,ֱ�ӽ�����һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
    
    #�ر�� 20080725 ���Ӳ�ѯԭ������Ϣ ��δ�ҵ�ԭ������Ϣ�򷵻�ͨѶ��ִ
    #=========��ѯԭ��Լ��ҽ�����Ϣ===========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ������Ϣ")
    
    tran_dict = {}
    if not rccpsDBFunc.getTransTrcPK(TradeContext.RCVMBRCO,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
        AfaLoggerFunc.tradeInfo("���ҵ��Ǽǲ��в����ڴ˲�ѯ������ѯ����Լ��ҽ���,ֱ�ӽ�����һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
        out_context_dict['STRINFO']  = '�����ڴ˲�ѯ������ѯ����Լ���ҵ��'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>������ѯԭ������Ϣ")
    
    
    #==========Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ")
    
    TradeContext.ISDEAL = PL_ISDEAL_UNDO
    TradeContext.ORTRCCO  = tran_dict['TRCCO']
    TradeContext.BOJEDT = tran_dict['BJEDTE']
    TradeContext.BOSPSQ = tran_dict['BSPSQN']
    
    #=====�ź� 20091010 ���� �������䵽ԭ���׻��� ====
    TradeContext.BESBNO = tran_dict['BESBNO']          #���ջ����� 
    
    #�ر�� 20070725 �޸ı���,���,��������,��������
    #TradeContext.CUR    = tran_dict['CUR']
    #TradeContext.OCCAMT = str(tran_dict['OCCAMT'])
    #TradeContext.PYRACC = tran_dict['PYRACC']
    #TradeContext.PYEACC = tran_dict['PYEACC']
    #TradeContext.SNDBNKNM = tran_dict['RCVBNKNM']
    #TradeContext.RCVBNKNM = tran_dict['SNDBNKNM']
    
    if TradeContext.ORCUR == 'CNY':
        TradeContext.CUR  =   '01'                     #ԭ����
    else:
        TradeContext.CUR  =   TradeContext.ORCUR       #ԭ����

    TradeContext.OCCAMT   =   TradeContext.OROCCAMT    #ԭ���
    
    rccpsGetFunc.GetSndBnkCo(TradeContext.SNDBNKCO)
    rccpsGetFunc.GetRcvBnkCo(TradeContext.RCVBNKCO)
    
    hdcbka_insert_dict = {}
    if not rccpsMap1127CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ�쳣")
        
    AfaLoggerFunc.tradeInfo(">>>����Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ")
    #==========�Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ�======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ�")
    
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ�")
    
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
