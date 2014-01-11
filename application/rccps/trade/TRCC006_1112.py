# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���Ļ�ִ).���ܺ˶Ա��Ľ���
#===============================================================================
#   �����ļ�:   TRCC006_1112.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-07-07
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_atrchk,rccpsMap1112CTradeContext2Datrchk_dict
import rccpsMap0000Dout_context2CTradeContext


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('>>>������ܺ˶Ա��Ľ���')
    #=====�ж��Ƿ��ظ�����====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_atrchk.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','�ж��Ƿ��ظ����ģ���ѯ���ܺ˶Ա��ĵǼǲ���ͬ�����쳣')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('���ҵ��Ǽǲ��д�����ͬ����,�ظ�����,������һ����')
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

        #=====����afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','�ظ����ģ��˳���������')

    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ��ظ�����")

    #=====��ֵ��ʼ�ǼǵǼǲ�====
    atrchk_dict = { }
    if not rccpsMap1112CTradeContext2Datrchk_dict.map(atrchk_dict):
        return AfaFlowControl.ExitThisFlow('S999','�ֵ丳ֵ����')

    if TradeContext.existVariable('CUR') and TradeContext.CUR == 'CNY':
        sel_dict['CUR'] = '01'
        
    #=====����Ǽǲ�====
    record = rccpsDBTrcc_atrchk.insert(sel_dict)
    if record <= 0:
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǻ�Һ˶Ա��ĵǼǲ��쳣")

    AfaDBFunc.CommitSql()

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
    out_context_dict['STRINFO']  = '�ɹ�'

    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    return True
#=====================���׺���================================================
def SubModuleDoSnd():

    #=====�ж����ķ���====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True
