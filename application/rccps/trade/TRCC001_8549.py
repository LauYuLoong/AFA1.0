# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).�����Ļ���ά��
#===============================================================================
#   �����ļ�:   TRCC001_8549.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-16
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_subbra,rccpsMap8549Dsubbra2CTradeContext,rccpsMap8549CTradeContext2Dsubbra

#=====================���Ի�����(���ز���)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***����.���������(1.���ز���).�����Ļ���ά��[TRC001_8549]����***' )

    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ��У��")
    #=====У����������Ա���Ƿ�Ϊͬһ����  20091116 �ź� =======
    if TradeContext.OPRNO != '3':
        if TradeContext.BESBNO[0:6] != TradeContext.BRNO[0:6] :
            return AfaFlowControl.ExitThisFlow("S999","����ͬһ��������������ҵ��")
    #===== END ==================================================
    
    #=====У�����Ȩ��  3  ��ѯ====   
    if TradeContext.OPRNO != '3':
        chk_subbra_where_dict = {}
        chk_subbra_where_dict['BESBNO'] = TradeContext.BESBNO
        chk_subbra_where_dict['SUBFLG'] = '1'
        chk_subbra_dict = rccpsDBTrcc_subbra.selectu(chk_subbra_where_dict)
        
        if chk_subbra_dict == None:
            return AfaFlowControl.ExitThisFlow("S999","��ѯ��������Ϣ�쳣")
        if len(chk_subbra_dict) <= 0:
            return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��в����ڱ�����,�������޲���Ȩ��")
            
#===== �ź� ע����20091116=======     
#        else:
#            if chk_subbra_dict['BESBTP'] != '31':   #�������Է����������
#                return AfaFlowControl.ExitThisFlow("S999","����������������������,��ֹ�ύ")
#                
#            elif TradeContext.BTOPSB != TradeContext.BESBNO:
#                return AfaFlowControl.ExitThisFlow("S999","�˻����Ǳ�������������,��ֹ����ѯ������κδ���")
    
    #=================��Ҫ��У��================================================

    #=====0  ����====
#    if TradeContext.OPRNO == '0':
#        #=================У��˻����Ƿ��Ѵ���==================================
#        subbra_where_dict = {}
#        subbra_where_dict['BESBNO'] = TradeContext.BRNO
#        
#        subbra_dict = rccpsDBTrcc_subbra.selectu(subbra_where_dict)
#        
#        if subbra_dict == None:
#            return AfaFlowControl.ExitThisFlow("S999","У������Ƿ��Ѵ����쳣")
#        if len(subbra_dict) > 0:
#            return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��д��ڴ˻���")
    #=====0  ���ӻ� 1  �޸�====
#    #if TradeContext.OPRNO == '0' or TradeContext.OPRNO == '1':
#        #=================У��ũ����ϵͳ�к��Ƿ��ѱ�����========================
#        subbra_where_sql = "BANKBIN = '" + TradeContext.BANKBIN + "' and BESBNO != '" + TradeContext.BRNO + "'"
#        subbra_count = rccpsDBTrcc_subbra.count(subbra_where_sql)
#        
#        if subbra_count < 0:
#            return AfaFlowControl.ExitThisFlow("S999","У��ũ����ϵͳ�к��Ƿ��ѱ������쳣")       
#        if subbra_count > 0:
#            return AfaFlowControl.ExitThisFlow("S999","ũ����ϵͳ�к��ѱ��������������,��ֹ�ύ")
#            
    AfaLoggerFunc.tradeInfo(">>>������Ҫ��У��")
    
    #=====�жϲ�������  3  ��ѯ====
    if( TradeContext.OPRNO == "3" ):
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯ������Ϣ")
        
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        subbra_dict = rccpsDBTrcc_subbra.selectu(subbra_where_dict)
        
        if subbra_dict == None:
            return AfaFlowControl.ExitThisFlow("S999","��ѯ�����Ǽǲ��쳣")
        if len(subbra_dict) <= 0:
            return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��в����ڴ˻���")
        else:
            rccpsMap8549Dsubbra2CTradeContext.map(subbra_dict)
            
        AfaLoggerFunc.tradeInfo(">>>������ѯ������Ϣ")
    #=====��������Ϊ0  ����====
    elif TradeContext.OPRNO == '0':
        AfaLoggerFunc.tradeInfo(">>>��ʼ����������Ϣ")
        
        #=====У��˻����Ƿ��Ѵ���====
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        subbra_dict = rccpsDBTrcc_subbra.selectu(subbra_where_dict)
        
        if subbra_dict == None:
            return AfaFlowControl.ExitThisFlow("S999","У������Ƿ��Ѵ����쳣")
        if len(subbra_dict) > 0:
            return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��д��ڴ˻���")
        
        #=====�����»���====
        subbra_insert_dict = {}
        rccpsMap8549CTradeContext2Dsubbra.map(subbra_insert_dict)
        ret = rccpsDBTrcc_subbra.insertCmt(subbra_insert_dict)
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","����������Ϣ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������������Ϣ")
        
#===== �ź� ע����20091116=======   
#=====��������Ϊ1  �޸�====
#    elif TradeContext.OPRNO == '1':       
#        AfaLoggerFunc.tradeInfo(">>>��ʼ�޸Ļ�����Ϣ")
#        
#        subbra_where_dict = {}
#        subbra_where_dict['BESBNO'] = TradeContext.BRNO
#        
#        subbra_update_dict = {}
#        rccpsMap8549CTradeContext2Dsubbra.map(subbra_update_dict)
#        
#        ret = rccpsDBTrcc_subbra.updateCmt(subbra_update_dict,subbra_where_dict)
#        
#        if ret <= 0:
#            return AfaFlowControl.ExitThisFlow("S999","�޸Ļ�����Ϣ�쳣")
#        
#        AfaLoggerFunc.tradeInfo(">>>�����޸Ļ�����Ϣ")
    #=====��������Ϊ2  ɾ��====
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

    AfaLoggerFunc.tradeInfo( '***����.���������(1.���ز���).�����Ļ���ά��[TRC001_8549]�˳�***' )
    return True
