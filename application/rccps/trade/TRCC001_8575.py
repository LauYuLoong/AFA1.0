# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).����ѯ�Ǽǲ���ѯ
#===============================================================================
#   ģ���ļ�:   TRCC001_8575.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-11-21
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_balbka

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).����ѯ�Ǽǲ���ѯ[TRCC001_8575]����***' )
    
    #=====�ж�����ӿ��Ƿ����====
    if( not TradeContext.existVariable( "BJEDTE" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[BJEDTE]������')
        
    if( not TradeContext.existVariable( "BSPSQN" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '�������[BSPSQN]������')
        
    #=====��֯��ѯ�ֵ�====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ�")
    
    wheresql_dic={}
    wheresql_dic['BJEDTE']=TradeContext.BJEDTE
    wheresql_dic['BESBNO']=TradeContext.BESBNO
    
    if(len(TradeContext.BSPSQN) != 0):
        wheresql_dic['BSPSQN']=TradeContext.BSPSQN
    
    #=====��ʼ��ѯ���ݿ�====
    records=rccpsDBTrcc_balbka.selectu(wheresql_dic)
    AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ�����')
    else: 
        pass
    
#    =====�жϷ�����====
#    if records['PRCCO']!='RCCI0000':
#        #=====����ӿڸ�ֵ====
#        AfaLoggerFunc.tradeInfo(">>>����ӿڸ�ֵ")        
#        TradeContext.errorMsg  = records['PRCCO'] +' '+ records['PRCINFO']
#        if len(TradeContext.errorMsg) != 1:
#            TradeContext.errorCode = 'A099'
#        else:
#            #=====ǰ̨�ж�Ϊ�˽����������ѯ====
#            TradeContext.errorCode = '9999'
#            TradeContext.errorMsg  = '�س����ٴβ�ѯ���,���Ժ�...'
#        AfaLoggerFunc.tradeDebug(">>>errorMsg["+str(TradeContext.errorMsg)+']')
#        AfaLoggerFunc.tradeDebug(">>>errorCode["+str(TradeContext.errorCode)+']')
#    else:
#        AfaLoggerFunc.tradeInfo(">>>����ӿڸ�ֵ")
#        TradeContext.errorCode = '0000'
#        TradeContext.errorMsg  = '�ɹ�'
#        TradeContext.BJEDTE = records['BJEDTE']
#        TradeContext.BSPSQN = records['BSPSQN']
#        TradeContext.AVLBAL = str(records['AVLBAL'])
#        TradeContext.ACCBAL = str(records['ACCBAL'])
#    
    AfaLoggerFunc.tradeInfo(">>>����ӿڸ�ֵ")       
    TradeContext.errorCode = '0000'       
    TradeContext.errorMsg  = '�ɹ�'    
    TradeContext.PRCCO  = records['PRCCO']
    TradeContext.STRINFO= records['STRINFO']              
    TradeContext.BJEDTE = records['BJEDTE']          
    TradeContext.BSPSQN = records['BSPSQN']          
    TradeContext.AVLBAL = str(records['AVLBAL'])     
    TradeContext.ACCBAL = str(records['ACCBAL'])     

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����ѯ�Ǽǲ���ѯ[TRCC001_8575]�˳�***')
    return True