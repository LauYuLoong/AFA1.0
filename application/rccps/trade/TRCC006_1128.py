# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).��Լ��Ҳ鸴����
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   �޸�ʱ��:   2008-06-11
################################################################################
#   �޸���  :   ������
#   �޸�ʱ��:   2008-07-21
#   ��    ��:   �޸ı���������
################################################################################
#   �޸���  :   �ر��
#   �޸�ʱ��:   2008-07-26
#   ��    ��:   �޸ĵǼǵǼǲ�����
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1128CTradeContext2Dhdcbka_dict

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    #==========�ж��Ƿ��ظ�����,������ظ�����,ֱ�ӽ�����һ����================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    hdcbka_where_dict = {}
    hdcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    hdcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    hdcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    #hdcbka_where_dict['TRCDAT']   = TradeContext.ORQYDAT
    #hdcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    
    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ������쳣")
    if len(hdcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��д�����ͬ�鸴����,�˱���Ϊ�ظ�����,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #�����Ա�к�
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>��������Ƿ��ظ�����")
    
    #==========�ж��Ƿ����ԭ��ѯ����===========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ����ԭ��ѯ����")
    hdcbka_where_dict = {}
    hdcbka_where_dict['SNDBNKCO'] = TradeContext.RCVBNKCO
    hdcbka_where_dict['TRCDAT']   = TradeContext.OQTDAT
    hdcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    #or_hdcbka_where_dict['TRCNO']    = TradeContext.ORTRCNO
    #or_hdcbka_where_dict['TRCDAT']   = TradeContext.ORTRCDAT
    
    or_hdcbka_dict = {}
    or_hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    
    if or_hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У��ԭ��ѯ����ʧ��") 
    
    if len(or_hdcbka_dict) <= 0:
        AfaLoggerFunc.tradeInfo("��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��в�����ԭ��ѯ����,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
        out_context_dict['STRINFO']  = '��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��в�����ԭ��ѯ����'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #�����Ա�к�
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>��������Ƿ����ԭ��ѯ����")
    
    #==========Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ")
    
    TradeContext.BOJEDT  = or_hdcbka_dict['BJEDTE']
    TradeContext.BOSPSQ  = or_hdcbka_dict['BSPSQN']
    #TradeContext.CUR     = or_hdcbka_dict['CUR']
    #TradeContext.OCCAMT  = str(or_hdcbka_dict['OCCAMT'])
    TradeContext.ORTRCCO = or_hdcbka_dict['TRCCO']
    #=========�ر�� �޸� ����,���,�������˺�,�տ����˺�,��������,��������
    #TradeContext.PYRACC  = or_hdcbka_dict['PYRACC']
    #TradeContext.PYEACC  = or_hdcbka_dict['PYEACC'] 
    TradeContext.ISDEAL  = PL_ISDEAL_ISDO
    
    if TradeContext.ORCUR == 'CNY':
        TradeContext.CUR  =   '01'                     #ԭ����
    else:
        TradeContext.CUR  =   TradeContext.ORCUR       #ԭ����

    TradeContext.OCCAMT   =   TradeContext.OROCCAMT    #ԭ���
    
    #=====�ź� 20091010 ���� �������䵽ԭ���׻��� ====
    TradeContext.BESBNO = or_hdcbka_dict['BESBNO']     #���ջ�����
    
    rccpsGetFunc.GetSndBnkCo(TradeContext.SNDBNKCO)
    rccpsGetFunc.GetRcvBnkCo(TradeContext.RCVBNKCO)
    
    hdcbka_insert_dict = {}
    if not rccpsMap1128CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ�쳣")
        
    AfaLoggerFunc.tradeInfo(">>>����Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ")
    #==========�Ǽǻ�Բ�ѯ�鸴���ɸ�ʽ�Ǽǲ�=======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�ǼǴ˲鸴ҵ��")
    
    ret = rccpsDBTrcc_hdcbka.insert(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��쳣")
        
    AfaLoggerFunc.tradeInfo(">>>�����ǼǴ˲鸴ҵ��")
    
    #======����ԭ��ѯ������Ϣ===================================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ��ѯҵ����Ϣ")
    
    or_hdcbka_update_dict = {}
    or_hdcbka_update_dict['ISDEAL']   = PL_ISDEAL_ISDO
    
    
    orhdcbka_where_dict = {}
    orhdcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    orhdcbka_where_dict['TRCDAT']   = TradeContext.OQTDAT
    orhdcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    ret = rccpsDBTrcc_hdcbka.update(or_hdcbka_update_dict,orhdcbka_where_dict)
    if (ret <= 0):
        return AfaFlowControl.ExitThisFlow("S999","����ԭ��ѯҵ����Ϣ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>��������ԭ��ѯҵ����Ϣ")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
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
    TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #�����Ա�к�
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    return True 
    
#=====================���׺���================================================
def SubModuleDoSnd():

    #=====�ж�afe���ؽ��
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True 
