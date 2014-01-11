# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).���ʿ��ƽ�����Ϣ������ѯ  ���潻��
#===============================================================================
#   ģ���ļ�:   TRCC001_8596.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����̩
#   �޸�ʱ��:   2011-05-23
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������(1.���ز���).���ʿ��ƽ�����Ϣ������ѯ[TRCC001_8596]����***' )
    
    #=====��Ҫ�Լ��====
    #=====�ж�����ӿ��Ƿ����====
    TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )
    if( not TradeContext.existVariable( "ORTRCDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', 'ԭί������[ORTRCDAT]������')
        
    if( not TradeContext.existVariable( "ORSNDBNK" ) ):
        return AfaFlowControl.ExitThisFlow('A099', 'ԭ�����к�[ORSNDBNK]������')
        
    if( not TradeContext.existVariable( "ORTRCNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', 'ԭ������ˮ��[ORTRCNO]������')
        
    #=====��֯��ѯ�ֵ�====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ�")
    
    wheresql_dic={}
    wheresql_dic['TRCDAT'] =TradeContext.ORTRCDAT
    wheresql_dic['SNDBNKCO']=TradeContext.ORSNDBNK
    wheresql_dic['TRCNO']=TradeContext.ORTRCNO
    
    #=====��ʼ��ѯ���ݿ�====
    records=rccpsDBTrcc_wtrbka.selectu(wheresql_dic)          #��ѯ���ʿ��ƽ�صǼǲ� 
    AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
    if(records==None):                                        
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
    elif(len(records)==0):
        records=rccpsDBTrcc_tddzmx.selectu(wheresql_dic)      #��ѯ���ʿ��ƽ�ض�����ϸ��Ϣ�Ǽǲ�
        AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
        elif(len(records)==0):
            return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ�����')
        else:
            #=====����ӿڸ�ֵ====
            AfaLoggerFunc.tradeInfo(">>>����ӿڸ�ֵ")       
            TradeContext.errorCode         = '0000'                  
            TradeContext.errorMsg          = '�ɹ�'   
            TradeContext.ORTRCCO           = records['TRCCO']         #ԭ���״���         
            TradeContext.ORSNDSUBBNK       = records['SNDMBRCO']      #ԭ�����Ա�к�     
            TradeContext.ORRCVSUBBNK       = records['RCVMBRCO']      #ԭ���ճ�Ա�к�      
            TradeContext.ORRCVBNK          = records['RCVBNKCO']      #ԭ�����к�    
            TradeContext.ORPYRACC          = records['PYRACC']        #ԭ�������˺�  
            TradeContext.ORPYRNAM          = ''                       #ԭ����������
            TradeContext.ORPYEACC          = records['PYEACC']        #ԭ�տ����˺�  
            TradeContext.ORPYENAM          = ''                       #ԭ�տ�������      
            TradeContext.CUR               = records['CUR']           #����
            TradeContext.OCCAMT            = str(records['OCCAMT'])   #ԭ���׽��
            TradeContext.CHRG              = str(records['CUSCHRG'])  #ԭ������
              
    else:
        #=====����ӿڸ�ֵ====
        AfaLoggerFunc.tradeInfo(">>>����ӿڸ�ֵ")       
        TradeContext.errorCode         = '0000'       
        TradeContext.errorMsg          = '�ɹ�'  
        TradeContext.BSPSQN            = records['BSPSQN'] 
        TradeContext.ORTRCCO           = records['TRCCO']         #ԭ���״���         
        TradeContext.ORSNDSUBBNK       = records['SNDMBRCO']      #ԭ�����Ա�к�     
        TradeContext.ORRCVSUBBNK       = records['RCVMBRCO']      #ԭ���ճ�Ա�к�      
        TradeContext.ORRCVBNK          = records['RCVBNKCO']      #ԭ�����к�    
        TradeContext.ORPYRACC          = records['PYRACC']        #ԭ�������˺�  
        TradeContext.ORPYRNAM          = records['PYRNAM']        #ԭ����������
        TradeContext.ORPYEACC          = records['PYEACC']        #ԭ�տ����˺�  
        TradeContext.ORPYENAM          = records['PYENAM']        #ԭ�տ�������      
        TradeContext.CUR               = records['CUR']           #����
        TradeContext.OCCAMT            = str(records['OCCAMT'])   #ԭ���׽��
        TradeContext.CHRG              = str(records['CUSCHRG'])  #ԭ������

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)���ʿ��ƽ�ؽ�����Ϣ������ѯ[TRCC001_8596]�˳�***')
    return True
