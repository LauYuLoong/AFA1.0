# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز���).�����˻�����ѯ����
#===============================================================================
#   �����ļ�:   TRCC001_8558.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-07-25
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_rekbal

#=====================���Ի�����(���ز���)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8558]����***' )
    
    #=====�ж϶��������Ƿ����====
    if not TradeContext.existVariable('CHKDAT'):
       return AfaFlowControl.ExitThisFlow('S999','��������[CHKDAT]������')

    #=====�����ѯrekbal====
    rek_sel = {}
    rek_sel['NCCWKDAT']  =  TradeContext.CHKDAT

    record = rccpsDBTrcc_rekbal.selectu(rek_sel)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','��ѯ�����˻����֪ͨ�Ǽǲ��쳣')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','��ѯ�����˻����֪ͨ�Ǽǲ��޼�¼')
    else:
        TradeContext.CHKRST = record['CHKRST']              #���˽��
        TradeContext.OCCAMT = str(record['TODAYBAL'])       #�������

    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '�ɹ�'
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8558]�˳�***' )
    return True
