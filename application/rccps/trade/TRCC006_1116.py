# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).ͷ��Ԥ�����Ľ���
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-24
#   ��    �ܣ�  ͷ�粻��
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
import rccpsDBTrcc_cshalm,rccpsMap0000Dout_context2CTradeContext,rccpsGetFunc

from types import *
from rccpsConst import *

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    #==========�ж��Ƿ��ظ�����,������ظ�����,ֱ�ӽ�����һ����================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    cshalm_where_dict = {}
    cshalm_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    cshalm_where_dict['TRCDAT']   = TradeContext.TRCDAT
    cshalm_where_dict['TRCNO']    = TradeContext.TRCNO

    cshalm_dict = rccpsDBTrcc_cshalm.selectu(cshalm_where_dict)

    if cshalm_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ������쳣")

    if len(cshalm_dict) > 0:
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

    #=====���ֵ丳ֵ====
    cshalm = {}
    cshalm['BJEDTE']   =  TradeContext.BJEDTE       #��������
    cshalm['BSPSQN']   =  TradeContext.BSPSQN       #�������
    #cshalm['NCCWKDAT'] =  TradeContext.NCCworkDate  #��������
    #�ر�� 20080924 �������ڸ�ֵ�����е���������
    cshalm['NCCWKDAT'] =  TradeContext.NCCWKDAT     #��������
    cshalm['TRCCO']    =  TradeContext.TRCCO        #���״���
    cshalm['TRCDAT']   =  TradeContext.TRCDAT       #ί������
    cshalm['TRCNO']    =  TradeContext.TRCNO        #������ˮ��
    cshalm['SNDBNKCO'] =  TradeContext.SNDBNKCO     #�����к�
    cshalm['RCVBNKCO'] =  TradeContext.RCVBNKCO     #�����к�
    #=====����ת��====
    if TradeContext.CUR == 'CNY':
        cshalm['CUR']  =  '01'                      #����
    cshalm['POSITION'] =  TradeContext.POSITION     #ͷ�統ǰ���
    cshalm['POSALAMT'] =  TradeContext.POSALAMT     #ͷ��Ԥ�����

    #=====�Ǽ�ͷ��Ԥ���Ǽǲ�====
    AfaLoggerFunc.tradeInfo('>>>��ʼ�Ǽ�ͷ��Ԥ���Ǽǲ�')
    AfaLoggerFunc.tradeInfo('>>>�ֵ䣺' + str(cshalm))
    ret = rccpsDBTrcc_cshalm.insertCmt(cshalm)
    if ret <= 0:
        #=====���ͻ�ִ�ֵ丳ֵ====
        TradeContext.PRCCO    = 'RCCS1105'
        TradeContext.STRINFO  = '��������'
    else:
        TradeContext.PRCCO    = 'RCCI0000'
        TradeContext.STRINFO  = '�ɹ�'
 
    #=====����ͨ���ִ====
    TradeContext.sysType  = 'rccpst'
    TradeContext.ORTRCCO  = TradeContext.TRCCO
    TradeContext.TRCCO    = '9900503'
    TradeContext.MSGTYPCO = 'SET008'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.ORMFN    = TradeContext.MSGFLGNO
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ROPRTPNO = TradeContext.OPRTYPNO
    TradeContext.OPRTYPNO = '99'
    TradeContext.TRANTYP  = '0'

    #=====ͨ�������к�ȡ�����ͳ�Ա�к�====
    rccpsGetFunc.GetRcvBnkCo(TradeContext.RCVBNKCO)
    
    #=====ͨ�������к�ȡ�����ͳ�Ա�к�====
    rccpsGetFunc.GetSndBnkCo(TradeContext.SNDBNKCO)

    TradeContext.tmp      = TradeContext.SNDSTLBIN
    TradeContext.SNDSTLBIN= TradeContext.RCVSTLBIN
    TradeContext.RCVSTLBIN= TradeContext.tmp

    return True
#=====================���׺���================================================
def SubModuleDoSnd():
    #=====�ж�afe����====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True

