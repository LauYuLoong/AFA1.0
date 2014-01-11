# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).ͨ��ͨ�Ҵ��ʴ����ʶά��
#===============================================================================
#   ģ���ļ�:   TRCC001_8590.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-12-30
################################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
import os,time,rccpsDBTrcc_tddzcz
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8590]ͨ��ͨ�Ҵ��ʴ����ʶά������***' )
    
    AfaLoggerFunc.tradeInfo('���Ի�����(���ز���)')
    
    #=====�жϽӿڱ����Ƿ����====
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','�����кŲ���Ϊ��' )
        
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A009','ί�����ڲ���Ϊ��')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A009','������ˮ�Ų���Ϊ��')
        
    if not TradeContext.existVariable("BJEDTE"):
        return AfaFlowControl.ExitThisFlow('A009','�������ڲ���Ϊ��')
        
    if not TradeContext.existVariable("BSPSQN"):
        return AfaFlowControl.ExitThisFlow('A009','������Ų���Ϊ��')
    
    AfaLoggerFunc.tradeInfo('���Ի��������(���ز���)') 
       
    #=====���޸��ֵ丳ֵ====
    update_dict = {'ISDEAL':'1','NOTE3':'����δ��������,ֱ���޸Ĵ��˴����ʶΪ�Ѵ���'}
                    
    where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,\
                  'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
    
#    #=====�жϴ����ʶ����====                                     
#    if( TradeContext.ISDEAL == '1' ):                              
#        return AfaFlowControl.ExitThisFlow('S999','�˴����ʶ����')
#    else:                                                          
#        pass                                                       

    tddzcz_dict = {}
    tddzcz_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if tddzcz_dict == None:
        return AfaFlowControl.ExitThisFlow('S999','��ѯ�˴�����Ϣ�쳣')
        
    if len(tddzcz_dict) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','���˵Ǽǲ����޴˴���')
        
    if tddzcz_dict['ISDEAL'] == '1':
        return AfaFlowControl.ExitThisFlow('S999','�˴��˴��˴����ʶΪ�Ѵ���,��ֹ�ύ')

    #=====�޸����ݿ��е�����====
    AfaLoggerFunc.tradeInfo("ͨ��ͨ�Ҵ��ʴ����ʶ�޸�")
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A099','�޸�ͨ��ͨ�Ҵ��ʴ����ʶʧ��')
    elif( res == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','���׼�¼������')
    
    #=====������ӿڸ�ֵ====
    TradeContext.errorCode = "0000"
    TradeContext.errorMsg  = "�޸�ͨ��ͨ�Ҵ��ʴ����ʶ�ɹ�"
    TradeContext.ISDEAL    = '1'

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8590]ͨ��ͨ�Ҵ��ʴ����ʶά���˳�***' )
    
    return True      