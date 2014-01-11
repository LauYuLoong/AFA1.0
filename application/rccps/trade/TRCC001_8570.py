# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.ͨ��ͨ��ҵ�����ά��
#=================================================================
#   �����ļ�:   TRCC001_8570.py
#   �޸�ʱ��:   2008-10-20
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
import os,time,rccpsDBTrcc_chgtbl
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8570]����***' )
    
    AfaLoggerFunc.tradeInfo('���Ի�����(���ز���)')
    
    #=====�жϽӿڱ����Ƿ����====
    if not TradeContext.existVariable("BPSBNO"):
        return AfaFlowControl.ExitThisFlow('A099','���˻����Ų���Ϊ��' )
        
    if not TradeContext.existVariable("OPRFLG"):
        return AfaFlowControl.ExitThisFlow('A009','�������Ͳ���Ϊ��')
        
    if not TradeContext.existVariable("CHGTYP"):
        return AfaFlowControl.ExitThisFlow('A009','���ʴ��벻��Ϊ��')
        
    if not TradeContext.existVariable("TRCCO"):
        return AfaFlowControl.ExitThisFlow('A009','���״��벻��Ϊ��')

    #=====��õ�ǰϵͳʱ��====
    TradeContext.NOW_TIME = str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    
    #=====�жϲ�������====
    if( TradeContext.OPRFLG == '0' ):
        AfaLoggerFunc.tradeInfo("ͨ��ͨ�ҷ��ʲ�ѯ")
        
        #=====���ɲ�ѯ�ֵ�====
        select_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':TradeContext.CHGTYP}
        
        #=====��ѯ���ݿ��е�����====
        AfaLoggerFunc.tradeInfo("ͨ��ͨ�ҷ��ʲ�ѯ")
        res = rccpsDBTrcc_chgtbl.selectu(select_dict)
        if( len(res) == 0 ):
            return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҷ��ʽ��Ϊ��')
            
        elif( res == None ):
            return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҷ���ʧ��')
        
        else:    
            #=====������ӿڸ�ֵ====
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg = "��ѯͨ��ͨ�ҷ��ʳɹ�"
            TradeContext.TRCCO    = res['TRCCO']
            TradeContext.CHGTYP   = res['CHGTYP']
            TradeContext.CHGNAM   = res['CHGNAM']
            TradeContext.CHGDATA  = res['CHGDATA']
            TradeContext.EFCTDAT  = res['EFCTDAT']
            TradeContext.INVDATE  = res['INVDATE']
            TradeContext.BPSBNO   = res['BPSBNO']
            
            
    elif( TradeContext.OPRFLG == '1' ):
        AfaLoggerFunc.tradeInfo("ͨ��ͨ�ҷ�������")
    
        #=====�ж�Ҫ��ӵĽ��׵ķ����Ƿ��Ѿ�����====
        AfaLoggerFunc.tradeInfo("�ж�Ҫ��ӵĽ��׵ķ����Ƿ��Ѿ�����")
        where_dict = {}
        select_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':TradeContext.CHGTYP}
        res = rccpsDBTrcc_chgtbl.selectu(select_dict)
        if( len(res) != 0 ):
            return AfaFlowControl.ExitThisFlow('A099','Ҫ��ӵķ��������Ѿ�����')
    
        AfaLoggerFunc.tradeInfo("�ж�Ҫ��ӵĽ��׵ķ��ʲ�����")
        #=====�������ֵ丳ֵ====
        insert_dict = {'BESBNO':TradeContext.BESBNO,'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,\
                       'CHGTYP':TradeContext.CHGTYP,'CHGNAM':TradeContext.CHGNAM,'CHGDATA':TradeContext.CHGDATA,\
                       'EFCTDAT':TradeContext.EFCTDAT,'INVDATE':TradeContext.INVDATE} 
       
                       
        #=====�����ݿ��в����¼====
        AfaLoggerFunc.tradeInfo("ͨ��ͨ�ҷ�������")   
        res = rccpsDBTrcc_chgtbl.insertCmt(insert_dict)
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A099','����ͨ��ͨ�ҷ���ʧ��')
            
        #=====������ӿڸ�ֵ====
        TradeContext.errorCode = "0000"
        TradeContext.errorMsg = "����ͨ��ͨ�ҷ��ʳɹ�"
        
    elif( TradeContext.OPRFLG == '2' ):
        AfaLoggerFunc.tradeInfo("ͨ��ͨ�ҷ����޸�")
        
        #=====���޸��ֵ丳ֵ====
        update_dict = {'BESBNO':TradeContext.BESBNO,'CHGNAM':TradeContext.CHGNAM,\
                       'CHGDATA':TradeContext.CHGDATA,'EFCTDAT':TradeContext.EFCTDAT,\
                       'INVDATE':TradeContext.INVDATE,'UPDTIME':TradeContext.NOW_TIME}
                        
        where_dict = {'BPSBNO':TradeContext.BPSBNO,'TRCCO':TradeContext.TRCCO,'CHGTYP':TradeContext.CHGTYP}

        #=====�޸����ݿ��е�����====
        AfaLoggerFunc.tradeInfo("ͨ��ͨ�ҷ����޸�")
        res = rccpsDBTrcc_chgtbl.updateCmt(update_dict,where_dict)
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A099','�޸�ͨ��ͨ�ҷ���ʧ��')
            
        #=====������ӿڸ�ֵ====
        TradeContext.errorCode = "0000"
        TradeContext.errorMsg = "�޸�ͨ��ͨ�ҷ��ʳɹ�"

    AfaLoggerFunc.tradeInfo('���Ի�����(���ز���) �˳�')
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8570]�˳�***' )
    
    return True      
    
        