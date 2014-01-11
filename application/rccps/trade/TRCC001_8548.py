# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).ʡ���Ļ���ά��
#===============================================================================
#   �����ļ�:   TRCC001_8548.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر�� 
#   �޸�ʱ��:   2008-06-16
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_subbra,rccpsMap8548Dsubbra2CTradeContext,rccpsMap8548CTradeContext2Dsubbra

#=====================���Ի�����(���ز���)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***����.���������(1.���ز���).ʡ���Ļ���ά��[TRC001_8548]����***' )
    
    #=================�ж��Ƿ�ʡ��������========================================
    AfaLoggerFunc.tradeDebug(">>>��ʼУ�����Ȩ��,ֻ��ʡ�������Ĳ������˽���")
    
    if TradeContext.BESBNO != PL_BESBNO_BCLRSB:
        return AfaFlowControl.ExitThisFlow("S999","����������������,�޴˽���Ȩ��")
    
    AfaLoggerFunc.tradeDebug(">>>����У�����Ȩ��")
    
    #=================��Ҫ��У��================================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ��У��")
    
    #=====0 ����====
    if TradeContext.OPRNO == '0':
        #=================У��˻����Ƿ��Ѵ���==================================
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        subbra_dict = rccpsDBTrcc_subbra.selectu(subbra_where_dict)
        
        if subbra_dict == None:
            return AfaFlowControl.ExitThisFlow("S999","У������Ƿ��Ѵ����쳣")
        if len(subbra_dict) > 0:
            return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��д��ڴ˻���")
    #=====0 ���ӻ� 1 �޸�====   
    if TradeContext.OPRNO == '0' or TradeContext.OPRNO == '1':
        #=================У��ũ����ϵͳ�к��Ƿ��ѱ�����========================
        subbra_where_sql = "BANKBIN = '" + TradeContext.BANKBIN + "' and BESBNO != '" + TradeContext.BRNO + "'"
        subbra_count = rccpsDBTrcc_subbra.count(subbra_where_sql)
        
        if subbra_count < 0:
            return AfaFlowControl.ExitThisFlow("S999","У��ũ����ϵͳ�к��Ƿ��ѱ������쳣")        
        if subbra_count > 0:
            return AfaFlowControl.ExitThisFlow("S999","ũ����ϵͳ�к��ѱ��������������,��ֹ�ύ")
        
    AfaLoggerFunc.tradeInfo(">>>������Ҫ��У��")
    
    #=================�жϲ�������  3  ��ѯ====
    if TradeContext.OPRNO == '3':
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯ������Ϣ")
        
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        subbra_dict = {}
        subbra_dict = rccpsDBTrcc_subbra.selectu(subbra_where_dict)
        
        if subbra_dict == None:
            return AfaFlowControl.ExitThisFlow("S999","��ѯ�����Ǽǲ��쳣")
        if len(subbra_dict) <= 0:
            return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��в����ڴ˻���")
        else:
            rccpsMap8548Dsubbra2CTradeContext.map(subbra_dict)
            
        AfaLoggerFunc.tradeInfo(">>>������ѯ������Ϣ")
    #=================��������Ϊ 0  ����====    
    elif TradeContext.OPRNO == '0':
        AfaLoggerFunc.tradeInfo(">>>��ʼ����������Ϣ")
        
        subbra_insert_dict = {}
        rccpsMap8548CTradeContext2Dsubbra.map(subbra_insert_dict)
        
        ret = rccpsDBTrcc_subbra.insertCmt(subbra_insert_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","����������Ϣ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������������Ϣ")
    #=================��������Ϊ 1  �޸�====    
    elif TradeContext.OPRNO == '1':
        
        AfaLoggerFunc.tradeInfo(">>>��ʼ�޸Ļ�����Ϣ")
        
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        subbra_update_dict = {}
        rccpsMap8548CTradeContext2Dsubbra.map(subbra_update_dict)
        
        ret = rccpsDBTrcc_subbra.updateCmt(subbra_update_dict,subbra_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","�޸Ļ�����Ϣ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�����޸Ļ�����Ϣ")
    #=================��������Ϊ 2  ɾ��====
    elif TradeContext.OPRNO == '2':       
        AfaLoggerFunc.tradeInfo(">>>��ʼɾ��������Ϣ")
        
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        ret = rccpsDBTrcc_subbra.deleteCmt(subbra_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","ɾ��������Ϣ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ɾ��������Ϣ")
    
    else:
        #=================�������ͷǷ�==========================================
        return AfaFlowControl.ExitThisFlow("S999","�������ͷǷ�")
        
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '����ɹ�'
    
    AfaLoggerFunc.tradeInfo( '***����.���������(1.���ز���).ʡ���Ļ���ά��[TRC001_8548]�˳�***' )
    
    return True
