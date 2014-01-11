# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯҵ��.����״̬��ѯ
#=================================================================
#   �����ļ�:   TRCC001_8554.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-12
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_mbrifa
import AfaFlowControl

from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8545]����***' )
    
    #=====�жϽӿ��Ƿ����====
    if not TradeContext.existVariable("OPRTYPNO"):
        return AfaFlowControl.ExitThisFlow('M999','ҵ������[OPRTYPNO]������')

    #=====�ж�OPRTYPNO�ǻ�Ʊʱ��ѯ���ҵ����Ϣ====
    #=====PL_TRCCO_HP 21 ��Ʊ====
    #=====PL_TRCCO_HD 20 ���====
    #=====PL_TRCCO_TCTD 30 ͨ��ͨ��====
    
    #=====��Ʊʹ�õ����ں͹���״̬ͬ���====
    if TradeContext.OPRTYPNO == PL_TRCCO_HP:
        OPRTYPNO = PL_TRCCO_HD
    elif TradeContext.OPRTYPNO == PL_TRCCO_HD:
        OPRTYPNO = PL_TRCCO_HD
    elif TradeContext.OPRTYPNO == PL_TRCCO_TCTD:
        OPRTYPNO = PL_TRCCO_TCTD
    else:
        return AfaFlowControl.ExitThisFlow('M999','ҵ������[OPRTYPNO]����')
       
    #=====���кŲ�ѯ====
    sqldic={'OPRTYPNO':OPRTYPNO}
    
    #=====��ѯ���ݿ⣬�õ���ѯ�����====
    records=rccpsDBTrcc_mbrifa.selectu(sqldic)  
    if records==None:
        return AfaflowControl.ExitThisFlow('M999','���ݿ����ʧ��')
    if len(records) <= 0 :
        return AfaflowControl.ExitThisFlow('M999','��������������')
 

    TradeContext.NCCworkDate = records['NWWKDAT']       #���Ĺ�������
    TradeContext.NWSYSST     = records['NWSYSST']       #����״̬
    TradeContext.errorMsg="��ѯ�ɹ�"
    TradeContext.errorCode="0000"
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8545]�˳�***' )
    return True
