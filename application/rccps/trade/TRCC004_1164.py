# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�����˽���.���ʿ���/���Ӧ���Ľ���    #�ҷ�����������ʿ��ƺͽ�ص��������ر��� ������Ϊ�����з��ʹ��ʿ��ƽ��������
#=================================================================
#   �����ļ�:   TRCC004_1164.py
#   �޸�ʱ��:   2011��05-16
#   ���ߣ�      ����̩
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc
import rccpsDBTrcc_acckj
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
    AfaLoggerFunc.tradeInfo("����Ƿ��ж�Ӧ��������")  #
    acckj_where_dict = {'TRCDAT':TradeContext.ORMFN[10:18],'TRCNO':TradeContext.ORMFN[18:],'SNDMBRCO':TradeContext.ORMFN[:10]} #�Ӳο����ı�ʶ����ȡ����
    res = rccpsDBTrcc_acckj.selectu(acckj_where_dict)
    if( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','����Ӧ��������ʧ��')
        
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','û�ж�Ӧ��������')   
        
             
    #=====��֯�����ֵ�====
    AfaLoggerFunc.tradeInfo("��ʼ��֯�����ֵ�")
    update_dict = {}
    
    if(TradeContext.TRCCO=='3000508'):   #���´��ʿ��Ʒ��ؽ��
        if (TradeContext.PRCCO=='RCCI0000'):
            update_dict['CONSTS']  = '0'
        else:
            update_dict['CONSTS']  = '1'  
            update_dict['STRINFO']   = "���ʿ���ʧ�ܣ�" + TradeContext.STRINFO 
        update_dict['PRCCO']     = TradeContext.PRCCO                                #������    
        update_dict['BALANCE']   = TradeContext.BALANCE                              #�˻�ʵ�ʽ��
        update_dict['STRINFO']   = TradeContext.STRINFO                              #��Ӧ��Ϣ�����ԣ�   
    
    if(TradeContext.TRCCO=='3000509'):  #���´��ʽ�ط��ؽ��
        if (TradeContext.PRCCO=='RCCI0000'):
            update_dict['UNCONRST']  = '0'
        else:
            update_dict['UNCONRST']  = '1'    
            update_dict['STRINFO']   = "���ʽ��ʧ�ܣ�"+ TradeContext.STRINFO 
        update_dict['PRCCO']     = TradeContext.PRCCO                                #������     
        update_dict['STRINFO']   = TradeContext.STRINFO                              #��Ӧ��Ϣ�����ԣ�   
   
    where_dict = {}
    where_dict['TRCDAT']     = TradeContext.TRCDAT                   #ί������
    where_dict['TRCNO']      = TradeContext.TRCNO                    #������ˮ��
    where_dict['SNDBNKCO']   = TradeContext.SNDBNKCO                 #�������к�
    
    #=====���´��ʿ��ƽ�صǼǲ�====
    AfaLoggerFunc.tradeInfo("���´��ʿ��ƽ�صǼǲ�")
    res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','���´��ʿ��ƽ�صǼǲ�')

    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '���׳ɹ�'
    
    AfaLoggerFunc.tradeInfo("��ִ���Ի�����(���ز���)  �˳�")
    
    return True