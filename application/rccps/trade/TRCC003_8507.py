# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���Ĳ���).��������
#===============================================================================
#   �����ļ�:   TRCC003_8507.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsDBTrcc_trccan,rccpsMap8507Dtrcbka_dict2Dtrccan_dict
import rccpsMap8507Dtrccan_dict2CTradeContext
from types import *
from rccpsConst import *


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    #====��ʼȡ��ˮ�Ŷ�Ӧ��Ϣ====
    trcbka_dict = {}
    dict = rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka_dict)
    if dict == False:
        return AfaFlowControl.ExitThisFlow('M999','ȡ������Ϣʧ��')

    #=====�жϳ�����Ϣ====
    if TradeContext.BESBNO != trcbka_dict["BESBNO"]:
        return AfaFlowControl.ExitThisFlow('M999','��������������')
    if TradeContext.BETELR != trcbka_dict["BETELR"]:
        return AfaFlowControl.ExitThisFlow('M999','��������Ա����')
    if TradeContext.BJEDTE != trcbka_dict["BJEDTE"]:
        return AfaFlowControl.ExitThisFlow('M999','��������ճ���')
    if trcbka_dict["BCSTAT"] != PL_BCSTAT_MFEQUE:  #41 �Ŷ�״̬ 1 �ɹ�
         return AfaFlowControl.ExitThisFlow('M999','��ǰҵ��״̬Ϊ['+trcbka_dict["BCSTAT"]+']��������' )
    if trcbka_dict["BRSFLG"] != PL_BRSFLG_SND:    #����
         return AfaFlowControl.ExitThisFlow('M999','��ǰҵ��״̬Ϊ����ҵ��������' )

    #=====��ʼ�������ݿ�====
    trccan_dict = {}
    if not rccpsMap8507Dtrcbka_dict2Dtrccan_dict.map(trcbka_dict,trccan_dict):
         return AfaFlowControl.ExitThisFlow('M999','�ֵ丳ֵ����')
    
    trccan_dict["CONT"]   = TradeContext.CONT
    trccan_dict["TRCCO"]  = TradeContext.TRCCO
    trccan_dict["BJEDTE"] = TradeContext.BJEDTE
    trccan_dict["BSPSQN"] = TradeContext.BSPSQN
    trccan_dict['CLRESPN'] = PL_ISDEAL_UNDO
    trccan_dict['RCVBNKCO'] = PL_RCV_CENTER
    trccan_dict['RCVBNKNM'] = PL_RCV_CENNAM 
    trccan_dict['RCVMBRCO'] = PL_RCV_CENTER
    trccan_dict['SNDMBRCO'] = TradeContext.SNDSTLBIN
    trccan_dict['TRCNO']    = TradeContext.SerialNo
    AfaLoggerFunc.tradeInfo( '�ֵ�trccan_dict��' + str(trccan_dict) )

    #=====��ʼ���볷��ҵ��Ǽǲ�====
    ret = rccpsDBTrcc_trccan.insert(trccan_dict)
    if ret <= 0:
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D011','���ݿ�ROLLBAKCʧ��')

    #=====commit����====
    AfaDBFunc.CommitSql()
    AfaLoggerFunc.tradeInfo('>>>commit succ')

    #=====���ֵ���TradeContext��ֵ====
    if not rccpsMap8507Dtrccan_dict2CTradeContext.map(trccan_dict):
         return AfaFlowControl.ExitThisFlow('M999','�ֵ丳ֵ����')

    #====�ֹ���ֵһЩ�ֶ�====
    TradeContext.OROCCAMT = str(TradeContext.OCCAMT)    #ԭ���׽��
    AfaLoggerFunc.tradeDebug('>>>ԭ���׽��' + str(TradeContext.OROCCAMT))
    TradeContext.ROPRTPNO = trcbka_dict['TRCCO'][:2]           #�ο�ҵ������
    AfaLoggerFunc.tradeDebug('>>>�ο�ҵ������' + TradeContext.ROPRTPNO)
    TradeContext.OPRTYPNO = '99'
    AfaLoggerFunc.tradeDebug('>>>ҵ������' + TradeContext.OPRTYPNO)
    TradeContext.ORMFN    = str(trcbka_dict['SNDMBRCO']) + str(trcbka_dict['TRCDAT']) + str(trcbka_dict['TRCNO'])     #�ο����ı�ʶ��
    AfaLoggerFunc.tradeDebug('>>>�ο�����' + TradeContext.ORMFN)
    TradeContext.ORRCVBNK = trcbka_dict['RCVBNKCO']
    TradeContext.RCVBNKCO = PL_RCV_CENTER
    TradeContext.RCVBNKNM = PL_RCV_CENNAM 
    TradeContext.RCVSTLBIN = PL_RCV_CENTER
    TradeContext.ORTRCNO   = trcbka_dict['TRCNO']
    
    TradeContext.ORSNDBNKCO=trccan_dict['SNDBNKCO']
    AfaLoggerFunc.tradeInfo("TradeContext.ORSNDBNKCO:"+TradeContext.ORSNDBNKCO)
    AfaLoggerFunc.tradeInfo("TradeContext.BOSPSQ:"+TradeContext.BOSPSQ)

    return True
#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeDebug('>>>��ʼ����AFE���ؽ��')
    #=====��ʼ�ж�afe���ؽ��====
    if TradeContext.errorCode != '0000':
         return AfaFlowControl.ExitThisFlow('M999','����ũ��������ʧ��')
    
    return True
    
