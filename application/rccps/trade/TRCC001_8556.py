# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.�����к�����
#=================================================================
#   �����ļ�:   TRCC001_8556.py
#   �޸�ʱ��:   2008-06-05
##################################################################
import rccpsDBTrcc_paybnk,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������.�����к�����[RCC001_8556]����***' )
    
    #=====�жϽӿ��Ƿ����====
    if not TradeContext.existVariable("BANKBIN"):
        return AfaFlowControl.ExitThisFlow('S999','�к�[BANKBIN]������')

    #=====���кŲ�ѯ====
    sqldic={'BANKBIN':TradeContext.BANKBIN,'NOTE1':'1'}
        
    #=====��ѯ���ݿ⣬�õ���ѯ�����====
    records=rccpsDBTrcc_paybnk.selectu(sqldic)
    
    if records == None:
        return AfaFlowControl.ExitThisFlow('S999','��ѯ�����к����ݿ�ʧ��')
    if len(records) <= 0 :
        return AfaFlowControl.ExitThisFlow('S999','�޴��к���Ϣ')
        
    TradeContext.BANKNAM = records['BANKNAM']       #����
    TradeContext.errorMsg="��ѯ�ɹ�"
    TradeContext.errorCode="0000"
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������.�����к�����[RCC001_8556]�˳�***' )
    return True
