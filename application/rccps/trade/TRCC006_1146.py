# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ������.��������
#=================================================================
#   �����ļ�:   TRCC006_1146.py
#   �޸�ʱ��:   2008-11-04
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
import rccpsDBTrcc_jstbka,rccpsMap1146CTradeContext2Dwtrbka_dict,rccpsDBTrcc_wtrbka,rccpsUtilTools
import rccpsDBTrcc_spbsta,AfaDBFunc,rccpsGetFunc,rccpsState,rccpsHostFunc,rccpsDBTrcc_atcbka
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("ũ����.ͨ��ͨ������.��������[T" + TradeContext.TemplateCode + '_' + TradeContext.TransCode+"]����")
    
    AfaLoggerFunc.tradeInfo("����ǰ����(�Ǽ���ˮ,����ǰ����)  ����")
    
    #==============================��֯Ӧ����===========================================
    AfaLoggerFunc.tradeInfo("��֯Ӧ���Ŀ�ʼ")
    Ormfn = TradeContext.MSGFLGNO
    Rcvmbrco = TradeContext.SNDMBRCO
    Sndmbrco = TradeContext.RCVMBRCO
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET010' #���������
    TradeContext.RCVSTLBIN = Rcvmbrco #���ܷ���Ա�к�
    TradeContext.SNDSTLBIN = Sndmbrco #���ͷ���Ա�к�
    TradeContext.SNDBRHCO = TradeContext.BESBNO         #�����������
    TradeContext.SNDCLKNO = TradeContext.BETELR         #�����й�Ա��
    TradeContext.SNDTRDAT = TradeContext.BJEDTE         #�����н�������
    TradeContext.SNDTRTIM = TradeContext.BJETIM         #�����н���ʱ��
    TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.BJEDTE + TradeContext.SerialNo  #���ı�ʾ��
    TradeContext.ORMFN    = Ormfn          #�ο����ı�ʾ��
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate   #���Ĺ�������
    TradeContext.OPRTYPNO = '30'     #ҵ������
    TradeContext.ROPRTPNO = '30'     #�ο�ҵ������
    TradeContext.TRANTYP  = '0'      #��������
    TradeContext.CURPIN   = ""  #��ؿͻ�����
    
    TradeContext.PRCCO    = "NN1IA999"
    TradeContext.STRINFO  = "�������޷�����" 
    
    AfaLoggerFunc.tradeInfo("��֯Ӧ���Ľ���")
    
    AfaLoggerFunc.tradeInfo("����ǰ����(�Ǽ���ˮ,����ǰ����)  �˳�")
    
    return True
    
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("���׺��� ����")
    
    #=====�ж�afe�Ƿ��ͳɹ�====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ���ĳɹ�')
    else:
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ����ʧ��')
        
    AfaLoggerFunc.tradeInfo("���׺��� �˳�")
    
    AfaLoggerFunc.tradeInfo("ũ����.ͨ��ͨ������.��������[T" + TradeContext.TemplateCode + '_' + TradeContext.TransCode+"]�˳�")
    
    return True
