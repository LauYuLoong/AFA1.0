# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).�ʽ��������
#===============================================================================
#   �����ļ�:   TRCC003_8544.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-23
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_mrqtbl
import rccpsMap8544CTradeContext2Dmrqtbl


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�ʽ��������[TRCC003_8544]����***' )
    
    #=================��Ҫ�Լ��================================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")
    
    if TradeContext.BESBNO != PL_BESBNO_BCLRSB:
        return AfaFlowControl.ExitThisFlow('S999','�������޴˽���Ȩ��')
        
    AfaLoggerFunc.tradeInfo(">>>������Ҫ�Լ��")
    
    #=================�Ǽ��ʽ��������Ǽǲ�====================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ��ʽ��������Ǽǲ�")
    
    TradeContext.TRCCO    = "9900525"
    TradeContext.TRCDAT   = TradeContext.BJEDTE
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
    #TradeContext.RCVMBRCO = "1000000000"
    
    mrqtbl_dict = {}
    if not rccpsMap8544CTradeContext2Dmrqtbl.map(mrqtbl_dict):
        return AfaFlowControl.ExitThisFlow('S999','Ϊ�ʽ��������Ǽǲ����ĸ�ֵ�쳣')
        
    ret = rccpsDBTrcc_mrqtbl.insertCmt(mrqtbl_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999','�Ǽ��ʽ��������ǼǱ��쳣')
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ��ʽ��������Ǽǲ�")
    
    #=================Ϊ�ʽ�������뱨�ĸ�ֵ====================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ�ʽ�������뱨�ĸ�ֵ")
    
    TradeContext.MSGTYPCO = "SET008"
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.TRCNO
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "99"
    TradeContext.ROPRTPNO = ""
    TradeContext.TRANTYP  = "0"
    TradeContext.ORTRCCO  = ""
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ�ʽ�������뱨�ĸ�ֵ")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�ʽ��������[TRCC003_8544]����***' )
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).�ʽ��������[TRCC003_8544]����***' )
    
    #=================�ж�afe�Ƿ��ͳɹ�=======================================
    if TradeContext.errorCode != '0000':
        #=============AFE����ʧ��,����PRCCO��STRINFO============================
        mrqtbl_where_dict = {}
        mrqtbl_where_dict['BJEDTE'] = TradeContext.BJEDTE
        mrqtbl_where_dict['BSPSQN'] = TradeContext.BSPSQN
        
        mrqtbl_update_dict = {}
        mrqtbl_update_dict['PRCCO']   = "S999"
        mrqtbl_update_dict['STRINFO'] = "����AFE�쳣"
        return AfaFlowControl.ExitThisFlow('S999','AFE�����쳣')
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).�ʽ��������[TRCC003_8544]�˳�***' )
    return True
    
