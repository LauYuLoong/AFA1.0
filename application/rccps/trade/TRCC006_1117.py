# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).�����˻����֪ͨ����
#===============================================================================
#   ģ���ļ�:   TRCC006_1117.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-24
#   ��    �ܣ�  �����˻����֪ͨ����
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
import rccpsDBTrcc_rekbal,rccpsMap0000Dout_context2CTradeContext

from types import *
from rccpsConst import *

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('>>>���������˻����֪ͨ���Ľ���')
    #=====�ж��Ƿ��ظ�����====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_rekbal.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','�ж��Ƿ��ظ����ģ���ѯ�����˻����֪ͨ�Ǽǲ���ͬ�����쳣')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('�����˻����Ǽǲ��д�����ͬ����,�ظ�����,������һ����')
        #=====ΪͨѶ��ִ���ĸ�ֵ====
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

        return True 
    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ��ظ�����")

    #=====���ֵ丳ֵ====
    rekbal = {}
    rekbal['BJEDTE']   =  TradeContext.BJEDTE       #��������
    rekbal['BSPSQN']   =  TradeContext.BSPSQN       #�������
    #rekbal['NCCWKDAT'] =  TradeContext.NCCworkDate  #��������
    #�ر�� 20080924 �������ڸ�ֵ�����е���������
    rekbal['NCCWKDAT'] =  TradeContext.NCCWKDAT     #��������
    rekbal['TRCCO']    =  TradeContext.TRCCO        #���״���
    rekbal['TRCDAT']   =  TradeContext.TRCDAT       #ί������
    rekbal['TRCNO']    =  TradeContext.TRCNO        #������ˮ��
    rekbal['SNDBNKCO'] =  TradeContext.SNDBNKCO     #�����к�
    rekbal['RCVBNKCO'] =  TradeContext.RCVBNKCO     #�����к�
    #=====����ת��====
    if TradeContext.CUR == 'CNY':
        rekbal['CUR']  =  '01'                      #����
    rekbal['LBDCFLG']  =  TradeContext.LBDCFLG      #�����������־
    rekbal['LSTDTBAL'] =  TradeContext.LSTDTBAL     #�������
    rekbal['NTTDCFLG'] =  TradeContext.NTTDCFLG     #�������������־
    rekbal['NTTBAL']   =  TradeContext.NTTBAL       #���������
    rekbal['BALDCFLG'] =  TradeContext.BALDCFLG     #�����������־
    rekbal['TODAYBAL'] =  TradeContext.TODAYBAL     #�������
    rekbal['AVLBAL']   =  TradeContext.AVLBAL       #�������
    rekbal['BRSFLG']   =  PL_BRSFLG_RCV
    rekbal['SNDMBRCO'] =  TradeContext.SNDMBRCO     #�����Ա�к�
    rekbal['RCVMBRCO'] =  TradeContext.RCVMBRCO     #���ճ�Ա�к�

    #=====�Ǽ������˻����֪ͨ�Ǽǲ�====
    out_context_dict = {}
    AfaLoggerFunc.tradeInfo('>>>��ʼ�Ǽ������˻����֪ͨ�Ǽǲ�')
    ret = rccpsDBTrcc_rekbal.insertCmt(rekbal)
    if ret <= 0:
        #=====���ͻ�ִ�ֵ丳ֵ====
        out_context_dict['PRCCO']    = 'RCCS1105'
        out_context_dict['STRINFO']  = '��������'
    else:
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ɹ�'
 
    #=====����ͨ���ִ====
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
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo

    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    return True
#=====================���׺���================================================
def SubModuleDoSnd():
    #=====�ж�afe����====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True

