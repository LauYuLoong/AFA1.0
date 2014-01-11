# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).��ѯ�����
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   �޸�ʱ��:   2008-06-11
################################################################################
#   �޸���  ��  ������
#   �޸�ʱ�䣺  2008-07-07
#   ��    �ܣ�  �޸Ľ�����workDateΪBJEDTE
################################################################################
#   �޸���  ��  �˹�ͨ
#   �޸�ʱ�䣺  2008-10-29
#   ��    �ܣ�  ����ͨ��ͨ�Ҳ���
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc,rccpsDBFunc
import rccpsDBTrcc_hdcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1118CTradeContext2Dhdcbka_dict

from types import *
from rccpsConst import *
#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    #=====�õ����˲�ѯ��Ĳο�ҵ������====
    ROPRTPNO = TradeContext.ROPRTPNO
    
    #==========�ж��Ƿ��ظ�����,������ظ�����,ֱ�ӽ�����һ����================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    hdcbka_where_dict = {}
    hdcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    hdcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    hdcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    #hdcbka_where_dict['TRCNO']    = TradeContext.ORTRCNO 
    
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
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ظ�����'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        AfaAfeFunc.CommAfe()
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>��������Ƿ��ظ�����")
    
    #=====�жϽ�������====
    if( TradeContext.ROPRTPNO == '20' ):    #���
        AfaLoggerFunc.tradeInfo("�����Ҵ���")
        #==========Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ================================
        AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ")
        
        tran_dict = {}
        #if not rccpsDBFunc.getTransTrcPK(TradeContext.ORMFN[:10],TradeContext.ORMFN[10:18],TradeContext.ORMFN[18:26],tran_dict):
        if not rccpsDBFunc.getTransTrcAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
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
            out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
            out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
            out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
            out_context_dict['OPRTYPNO'] = '99'
            out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
            out_context_dict['TRANTYP']  = '0'
            out_context_dict['ORTRCCO']  = TradeContext.TRCCO
            out_context_dict['PRCCO']    = 'RCCI0000'
            out_context_dict['STRINFO']  = '��ԭ��ҽ���'
        
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
            AfaAfeFunc.CommAfe()
        
            return AfaFlowControl.ExitThisFlow('S999','��ԭ���ף������˱���') 
        
        if tran_dict.has_key('BJEDTE'):
            TradeContext.BOJEDT = tran_dict['BJEDTE']
        
        if tran_dict.has_key('BSPSQN'):
            TradeContext.BOSPSQ = tran_dict['BSPSQN']
        
        TradeContext.ISDEAL = PL_ISDEAL_UNDO
        TradeContext.PYRACC = tran_dict['PYRACC']     #�������˺�
        TradeContext.PYEACC = tran_dict['PYEACC']     #�տ����˺�
        
        #=====�ź� 20091010 ���� �������䵽ԭ���׻��� ====
        TradeContext.BESBNO = tran_dict['BESBNO']     #���ջ�����
        
        hdcbka_insert_dict = {}
        if not rccpsMap1118CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
            return AfaFlowControl.ExitThisFlow("S999","Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ�쳣")
            
        AfaLoggerFunc.tradeInfo(">>>����Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ")
        
    elif( TradeContext.ROPRTPNO == '30' ):    #ͨ��ͨ��
        AfaLoggerFunc.tradeInfo("����ͨ��ͨ�Ҵ���")
        #==========Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ================================
        AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ")
        
        wtrbka_dict = {}
        if not rccpsDBFunc.getTransWtrAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,wtrbka_dict):
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
            out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
            out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
            out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
            out_context_dict['OPRTYPNO'] = '99'
            out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
            out_context_dict['TRANTYP']  = '0'
            out_context_dict['ORTRCCO']  = TradeContext.TRCCO
            out_context_dict['PRCCO']    = 'RCCI0000'
            out_context_dict['STRINFO']  = '��ԭͨ��ͨ�ҽ���'
        
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
            AfaAfeFunc.CommAfe()
        
            return AfaFlowControl.ExitThisFlow('S999','��ԭ���ף������˱���') 
        
        if wtrbka_dict.has_key('BJEDTE'):
            TradeContext.BOJEDT = wtrbka_dict['BJEDTE']
        
        if wtrbka_dict.has_key('BSPSQN'):
            TradeContext.BOSPSQ = wtrbka_dict['BSPSQN']
        
        TradeContext.ISDEAL = PL_ISDEAL_UNDO
        TradeContext.PYRACC = wtrbka_dict['PYRACC']     #�������˺�
        TradeContext.PYEACC = wtrbka_dict['PYEACC']     #�տ����˺�
        
        
        hdcbka_insert_dict = {}
        if not rccpsMap1118CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
            return AfaFlowControl.ExitThisFlow("S999","Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ�쳣")
            
        AfaLoggerFunc.tradeInfo(">>>����Ϊ��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��ֵ丳ֵ")
        
    else:
        return AfaFlowControl.ExitThisFlow("S999","û�д˽�������")
          
    #==========�Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ�======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ�")

    hdcbka_insert_dict['BRSFLG']   =   PL_BRSFLG_RCV        #����
    if TradeContext.ORCUR == 'CNY':
        hdcbka_insert_dict['CUR']      =   '01'   #ԭ����
    else:
        hdcbka_insert_dict['CUR']      =   TradeContext.ORCUR   #ԭ����

    hdcbka_insert_dict['OCCAMT']   =   TradeContext.OROCCAMT #ԭ���
    
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��쳣") 
    
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ�Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ�")
    
    #======ΪͨѶ��ִ���ĸ�ֵ===================================================��ִǰ����ֻҪ�����ֶ�.1.2.ĩ
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
