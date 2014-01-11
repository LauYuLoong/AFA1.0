# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�����˽���.������ѯӦ���Ľ���
#=================================================================
#   �����ļ�:   TRCC004_1150.py
#   �޸�ʱ��:   2008-10-21
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc
import rccpsDBTrcc_balbka
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("��ִ���Ի�����(���ز���)  ����")
    
    #=====У���������Ч��====
    AfaLoggerFunc.tradeInfo("У���������Ч��")
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A099','û��ί������')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A099','û�н�����ˮ��')
        
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','û�з������к�')
        
    #=====����Ƿ��ж�Ӧ��������====
    AfaLoggerFunc.tradeInfo("����Ƿ��ж�Ӧ��������")
    balbka_where_dict = {'TRCDAT':TradeContext.ORMFN[10:18],'TRCNO':TradeContext.ORMFN[18:],'SNDMBRCO':TradeContext.ORMFN[:10]}
    res = rccpsDBTrcc_balbka.selectu(balbka_where_dict)
    if( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','����Ӧ��������ʧ��')
        
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','û�ж�Ӧ��������')   
        
             
    #=====��֯�����ֵ�====
    AfaLoggerFunc.tradeInfo("��ʼ��֯�����ֵ�")
    update_dict = {}
    update_dict['AVLBAL']  = TradeContext.AVLBAL
    update_dict['ACCBAL']  = TradeContext.ACCBAL
    update_dict['PRCCO']   = TradeContext.PRCCO
    #update_dict['PRCINFO'] = "AFE���ͳɹ������յ�Ӧ����"
    update_dict['STRINFO'] = TradeContext.STRINFO
    where_dict = {}
    where_dict['TRCDAT']   = TradeContext.TRCDAT
    where_dict['TRCNO']    = TradeContext.TRCNO
    where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    
    #=====��������ѯ�Ǽǲ�====
    AfaLoggerFunc.tradeInfo("��������ѯ�Ǽǲ�")
    res = rccpsDBTrcc_balbka.updateCmt(update_dict,where_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','��������ѯ�Ǽǲ�ʧ��')

    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '���׳ɹ�'
    
    AfaLoggerFunc.tradeInfo("��ִ���Ի�����(���ز���)  �˳�")
    
    return True