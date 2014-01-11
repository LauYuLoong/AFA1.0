# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز���).��Ʊ����������ѯ
#===============================================================================
#   �����ļ�:   TRCC001_8555.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �˹�ͨ
#   �޸�ʱ��:   2008-08-01
################################################################################
import rccpsDBTrcc_bilinf
import TradeContext,AfaLoggerFunc,os,AfaFlowControl
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8555]����***' )
    
    #=====�жϽӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "BILRS" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '���б��б�ʶ[BILRS]������')
        
    if( not TradeContext.existVariable( "BILVER" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��Ʊ�汾��[BILVER]������')
        
    if( not TradeContext.existVariable( "BILNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��Ʊ����[BILNO]������')
    
    #=====��ʼ��֯��ѯ�ֵ�====
    where_dict={'BILRS':TradeContext.BILRS,'BILVER':TradeContext.BILVER,'BILNO':TradeContext.BILNO}
    
    #=====��ѯ��Ʊ��Ϣ�Ǽǲ�====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯ��Ʊ��Ϣ�Ǽǲ�")
    res_bilinf=rccpsDBTrcc_bilinf.selectu(where_dict)
    if( res_bilinf == None ):
        return AfaFlowControl.ExitThisFlow('A099', '��ѯ��Ʊ��Ϣ�Ǽǲ�ʧ��')
        
    if( len(res_bilinf) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099', '�޴˻�Ʊ��Ϣ')
        
    #=====���ӻ������ж�====
    if res_bilinf['NOTE3'] != TradeContext.BESBNO:
        return AfaFlowControl.ExitThisFlow('S999', '����Ʊ�Ǳ�����ǩ��,��ֹ�ύ')
        
    #=====��ʼΪ����ӿڸ�ֵ====
    TradeContext.REMBNKCO = res_bilinf['REMBNKCO']
    TradeContext.REMBNKNM = res_bilinf['REMBNKNM']
    TradeContext.PAYBNKCO = res_bilinf['PAYBNKCO']
    TradeContext.PAYBNKNM = res_bilinf['PAYBNKNM']
    TradeContext.BILDAT   = res_bilinf['BILDAT'] 
    TradeContext.BILTYP   = res_bilinf['BILTYP'] 
    TradeContext.BILNO    = res_bilinf['BILNO'] 
    TradeContext.BILVER   = res_bilinf['BILVER'] 
    TradeContext.PYRACC   = res_bilinf['PYRACC'] 
    TradeContext.PYRNAM   = res_bilinf['PYRNAM'] 
    TradeContext.PYRADDR  = res_bilinf['PYRADDR'] 
    TradeContext.CUR      = res_bilinf['CUR'] 
    TradeContext.BILAMT   = str(res_bilinf['BILAMT']) 
    TradeContext.OCCAMT   = str(res_bilinf['OCCAMT']) 
    TradeContext.RMNAMT   = str(res_bilinf['RMNAMT']) 
    TradeContext.PYEACC   = res_bilinf['PYEACC'] 
    TradeContext.PYENAM   = res_bilinf['PYENAM'] 
    TradeContext.PYEADDR  = res_bilinf['PYEADDR'] 
    TradeContext.PYHACC   = res_bilinf['PYHACC'] 
    TradeContext.PYHNAM   = res_bilinf['PYHNAM'] 
    TradeContext.PYHADDR  = res_bilinf['PYHADDR'] 
    TradeContext.USE      = res_bilinf['USE'] 
    TradeContext.REMARK   = res_bilinf['REMARK'] 
    TradeContext.SEAL     = res_bilinf['SEAL'] 
    TradeContext.HPSTAT   = res_bilinf['HPSTAT'] 
    TradeContext.PAYWAY     = res_bilinf['PAYWAY'] 
    
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
    
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8555]�˳�***' )
    return True
