# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.������������ѯ����
#=================================================================
#   �����ļ�:   TRCC001_8574.py
#   �޸�ʱ��:   2008-10-20
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
import os,rccpsDBTrcc_chgtbl
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8574]����***' )
    
    AfaLoggerFunc.tradeInfo('���Ի�����(���ز���)')
    
    #=====�жϽӿڱ����Ƿ����====
    if not TradeContext.existVariable("BPSBNO"):
        return AfaFlowControl.ExitThisFlow('A099','���˻����Ų���Ϊ��' )
        
    if not TradeContext.existVariable("TRCCO"):
        return AfaFlowControl.ExitThisFlow('A099','���״��벻��Ϊ��' )
        
    #=====�������====
    FeiLv = 0
    ShangXian = 0
    XiaXian = 0
    
    #=====��ѯ����====
    AfaLoggerFunc.tradeInfo("��ʼ��ѯ����")
    
    #=====��֯��ѯ�ֵ�====
    where_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':'0'}
    
    #=====��ѯ���ݿ�====
    AfaLoggerFunc.tradeInfo("��ѯ����ά�����õ�����")
    res = rccpsDBTrcc_chgtbl.selectu(where_dict)
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҷ��ʽ��Ϊ��')
            
    elif( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҷ���ʧ��')
        
    else:  
        FeiLv = float(res['CHGDATA']) * float(TradeContext.OCCAMT)  
        
        AfaLoggerFunc.tradeInfo("����Ϊ��" + str(FeiLv))
        
    #=====��ѯ��������====
    AfaLoggerFunc.tradeInfo("��ʼ��ѯ��������")
    
    #=====��֯��ѯ�ֵ�====
    where_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':'1'}
    
    #=====��ѯ���ݿ�====
    AfaLoggerFunc.tradeInfo("��ѯ����ά�����õ���������")
    res = rccpsDBTrcc_chgtbl.selectu(where_dict)
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҷ������޽��Ϊ��')
            
    elif( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҷ�������ʧ��')
        
    else: 
        ShangXian = float(res['CHGDATA']) 
        AfaLoggerFunc.tradeInfo("����Ϊ��" + str(ShangXian))
        
        
    #=====��ѯ��������====
    AfaLoggerFunc.tradeInfo("��ʼ��ѯ��������")
    
    #=====��֯��ѯ�ֵ�====
    where_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':'2'}
    
    #=====��ѯ���ݿ�====
    AfaLoggerFunc.tradeInfo("��ѯ����ά�����õ���������")
    res = rccpsDBTrcc_chgtbl.selectu(where_dict)
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҷ������޽��Ϊ��')
            
    elif( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҷ�������ʧ��')
        
    else: 
        XiaXian = float(res['CHGDATA']) 
        AfaLoggerFunc.tradeInfo("����Ϊ��" + str(XiaXian))      
        
    #=====ͨ���Ƚϵó�����====
    AfaLoggerFunc.tradeInfo("ͨ���Ƚϵó�����")
    
    if( FeiLv >= ShangXian ):
        Commission = ShangXian
        
    elif( FeiLv <= XiaXian ):
        Commission = XiaXian
        
    else:
        Commission = FeiLv
        
    #=====������ӿڸ�ֵ====
    TradeContext.CUSCHRG = str(Commission)
    AfaLoggerFunc.tradeInfo("CUSCHRG=" + TradeContext.CUSCHRG)
    
    TradeContext.errorCode = "0000"
    TradeContext.errorMsg = "��ѯ�ɹ�"
    
    AfaLoggerFunc.tradeInfo('���Ի�����(���ز���) �˳�')
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8574]�˳�***' )
    
    return True