# -*- coding: gbk -*-
##################################################################
#   ũ����.ũ����.��ѯ��ӡҵ��.��BIN�кŲ�ѯ
#=================================================================
#   �����ļ�:   TRCC001_8551.py
#   �޸�ʱ��:   2008-11-12
#   ���ߣ�      ����
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc
import rccpsDBTrcc_cadbnk,rccpsDBTrcc_paybnk
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('***ũ����ϵͳ������.���������(1.���ز���)��BIN�кŲ�ѯ[TRCC001_8551]����***')
    
    start_no = 1                            #��ʼ����
    sel_size = 10                           #��ѯ����
    
    #=====У���������Ч��====
    AfaLoggerFunc.tradeInfo("У���������Ч��")
    
    if not (TradeContext.existVariable( "CARDBIN" ) and TradeContext.CARDBIN != "" ):
        return AfaFlowControl.ExitThisFlow('A099','��BIN[CARDBIN]������' )
    
    #===== ��鿨BINλ��====     
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ���")
    i = 12
    bankcode = ""
    while( i >=6 ):
        cardbin = TradeContext.CARDBIN[:i]
        wheresql = "CARDBIN like '" + cardbin + "%'"
        ordersql = " order by CARDBIN DESC"
        
        AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
        record = rccpsDBTrcc_cadbnk.selectm(start_no,sel_size,wheresql,ordersql)
        if( record == None ):
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )  
            
        elif( len(record) == 0 ):
            i = i-1 
            
        else:
            bankcode = record[0]['BANKBIN']
            break
    
    if( i < 6 ):
        return AfaFlowControl.ExitThisFlow('A099','�޴˿�BIN' )
   
    TradeContext.BANKBIN = bankcode
        
    #=====���ɲ�ѯ����====
    wheresql_dic={}
    wheresql_dic['BANKBIN']=TradeContext.BANKBIN
    AfaLoggerFunc.tradeInfo( "wheresql_dic="+TradeContext.BANKBIN)
                
    #=====��ʼ��ѯ���ݿ�====
    records=rccpsDBTrcc_paybnk.selectu(wheresql_dic)
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ�����')
    else:    
        #=====����ӿ�====
        TradeContext.BANKNAM=records['BANKNAM']
    
    #=====����ӿڸ�ֵ====
    AfaLoggerFunc.tradeInfo(">>>����ӿڸ�ֵ")
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '�ɹ�'
    TradeContext.BANKBIN = bankcode
    
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)��BIN�кŲ�ѯ[TRCC001_8551]�˳�***')
    return True
    