# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز���).����������ѯ
#===============================================================================
#   �����ļ�:   TRCC001_8554.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsMap8554Dtrcbka2CTradeContext,rccpsDBTrcc_trcbka
from types import *

#=====================���Ի�����(���ز���)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8554]����***' )
    
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
