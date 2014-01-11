# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز���).����ר������������ѯ
#===============================================================================
#   �����ļ�:   TRCC001_8586.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ź�
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsMap8554Dtrcbka2CTradeContext,rccpsDBTrcc_trcbka
from types import *

#=====================���Ի�����(���ز���)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8554]����***' )
    
    ##===�ź�������20091230==== 
    trcbka_where_dict1={}
    trcbka_where_dict1 = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}            
 
    #==========��ѯ��ҵǼǲ����ҵ����Ϣ=======================================
    trcbka_dict = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict1)  
    
    if trcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ѯ���ҵ��Ǽǲ�������Ϣ�쳣' )
        
    if len(trcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '���ҵ��Ǽǲ����޴˽�����Ϣ' )
    if trcbka_dict['BESBNO'] != TradeContext.BESBNO :
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǳ�����ҵ��!' )
    ##====end=================
    
    #=====��ѯ��ҵ�����Ϣ====
    trcbka = {}
    bka = rccpsDBFunc.getTransTrc(TradeContext.BJEDTE,TradeContext.BSPSQN,trcbka)
    if bka == False:
        return  AfaFlowControl.ExitThisFlow('M999','��ѯ������Ϣʧ��') 
    else:
        AfaLoggerFunc.tradeInfo( '>>>��ѯ�ɹ�' )
        #=====�ֵ丳ֵ��TradeContext====
        rccpsMap8554Dtrcbka2CTradeContext.map(trcbka)
        
    TradeContext.OCCAMT    = str(trcbka['OCCAMT'])              #���
    TradeContext.LOCCUSCHRG    = str(trcbka['LOCCUSCHRG'])      #�����ѽ�� ������20091228  �ź�
    
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '��ѯ�ɹ�'

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8554]�˳�***' )
    return True
