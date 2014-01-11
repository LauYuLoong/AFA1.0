# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).ͨ��ͨ�ҽ�����Ϣ������ѯ
#===============================================================================
#   ģ���ļ�:   TRCC001_8592.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-12-30
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������(1.���ز���).ͨ��ͨ�ҽ�����Ϣ������ѯ[TRCC001_8592]����***' )
    
    #=====��Ҫ�Լ��====
    #=====�ж�����ӿ��Ƿ����====
    if( not TradeContext.existVariable( "TRCDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', 'ί������[TRCDAT]������')
        
    if( not TradeContext.existVariable( "SNDBNKCO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '�����к�[SNDBNKCO]������')
        
    if( not TradeContext.existVariable( "TRCNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '������ˮ��[TRCNO]������')
        
    #=====��֯��ѯ�ֵ�====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ�")
    
    wheresql_dic={}
    wheresql_dic['TRCDAT']=TradeContext.TRCDAT
    wheresql_dic['SNDBNKCO']=TradeContext.SNDBNKCO
    wheresql_dic['TRCNO']=TradeContext.TRCNO
    
    #=====��ʼ��ѯ���ݿ�====
    records=rccpsDBTrcc_wtrbka.selectu(wheresql_dic)
    AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
    if(records==None):                                        
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
    elif(len(records)==0):
        records=rccpsDBTrcc_tddzmx.selectu(wheresql_dic)
        AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
        elif(len(records)==0):
            return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ�����')
        else:
            #=====����ӿڸ�ֵ====
            AfaLoggerFunc.tradeInfo(">>>����ӿڸ�ֵ")       
            TradeContext.errorCode = '0000'                  
            TradeContext.errorMsg  = '�ɹ�'                  
            TradeContext.BJEDTE    = records['BJEDTE']       
            TradeContext.BSPSQN    = records['BSPSQN']       
            TradeContext.SNDBNKCO  = records['SNDBNKCO']     
            TradeContext.SNDBNKNM  = records['SNDBNKNM']     
            TradeContext.RCVBNKCO  = records['RCVBNKCO']     
            TradeContext.RCVBNKNM  = records['RCVBNKNM']     
            TradeContext.PYEACC    = records['PYEACC']       
            TradeContext.PYENAM    = ""       
            TradeContext.PYRACC    = records['PYRACC']       
            TradeContext.PYRNAM    = ""      
            TradeContext.OCCAMT    = str(records['OCCAMT'])  
            TradeContext.CUSCHRG   = str(records['CUSCHRG']) 
            TradeContext.CUR       = '01'          
            TradeContext.STRINFO   = records['STRINFO']      
    else:
        #=====����ӿڸ�ֵ====
        AfaLoggerFunc.tradeInfo(">>>����ӿڸ�ֵ")       
        TradeContext.errorCode = '0000'       
        TradeContext.errorMsg  = '�ɹ�'    
        TradeContext.BJEDTE    = records['BJEDTE']
        TradeContext.BSPSQN    = records['BSPSQN']             
        TradeContext.SNDBNKCO  = records['SNDBNKCO']          
        TradeContext.SNDBNKNM  = records['SNDBNKNM'] 
        TradeContext.RCVBNKCO  = records['RCVBNKCO']
        TradeContext.RCVBNKNM  = records['RCVBNKNM']
        TradeContext.PYEACC    = records['PYEACC']
        TradeContext.PYENAM    = records['PYENAM']
        TradeContext.PYRACC    = records['PYRACC']
        TradeContext.PYRNAM    = records['PYRNAM']
        TradeContext.OCCAMT    = str(records['OCCAMT'])
        TradeContext.CUSCHRG   = str(records['CUSCHRG'])
        TradeContext.CUR       = records['CUR']
        TradeContext.STRINFO   = records['STRINFO']

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)ͨ��ͨ�ҽ�����Ϣ������ѯ[TRCC001_8592]�˳�***')
    return True
    
     
        
    
    