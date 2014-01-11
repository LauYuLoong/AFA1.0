# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡ.ͨ��ͨ��������������
#=================================================================
#   �����ļ�:   TRCC001_8580.py
#   �޸�ʱ��:   2008-10-23
#   ���ߣ�      �˹�ͨ
##################################################################

import rccpsDBTrcc_wtrbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("���Ի�����(���ز���)")
    
    #=====У������ĺϷ���====
    if( not TradeContext.existVariable( "BJEDTE" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '�������ڲ�����')
    
    if( not TradeContext.existVariable( "BSPSQN" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '������Ų�����')
        
    #=====��֯��ѯ�ֵ�====
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BESBNO':TradeContext.BESBNO}
    
    #=====��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�====
    AfaLoggerFunc.tradeInfo("��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�")
    record = rccpsDBTrcc_wtrbka.selectu(where_dict)
    if( record == None ):
        return AfaFlowControl.ExitThisFlow('A099', '��ѯͨ��ͨ��ҵ��Ǽǲ�ʧ��')
        
    elif( len(record) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099', '��ѯͨ��ͨ��ҵ��Ǽǲ�Ϊ��')
        
    else:
#        #=====�ж��Ƿ�Ϊ����ҵ��====
#        if( record['BRSFLG'] == PL_BRSFLG_RCV ):
#            return AfaFlowControl.ExitThisFlow('A099', '�ñ�ҵ��������ҵ��')
            
        #=====��ʼ��֯����ӿ�====
        AfaLoggerFunc.tradeInfo("��ʼ��֯����ӿ�")    
          
        TradeContext.BJEDTE     = record['BJEDTE']
        TradeContext.BSPSQN     = record['BSPSQN']
        TradeContext.BRSFLG     = record['BRSFLG']
        TradeContext.BESBNO     = record['BESBNO']   
        TradeContext.BETELR     = record['BETELR']
        TradeContext.BEAUUS     = record['BEAUUS']
        TradeContext.DCFLG      = record['DCFLG']
        TradeContext.OPRNO      = record['OPRNO']
        TradeContext.NCCWKDAT   = record['NCCWKDAT']
        TradeContext.TRCCO      = record['TRCCO']
        TradeContext.TRCDAT     = record['TRCDAT']
        TradeContext.TRCNO      = record['TRCNO']
        TradeContext.COTRCNO    = record['COTRCNO']
        TradeContext.SNDMBRCO   = record['SNDMBRCO']
        TradeContext.RCVMBRCO   = record['RCVMBRCO']
        TradeContext.SNDBNKCO   = record['SNDBNKCO']
        TradeContext.SNDBNKNM   = record['SNDBNKNM']
        TradeContext.RCVBNKCO   = record['RCVBNKCO']
        TradeContext.RCVBNKNM   = record['RCVBNKNM']
        TradeContext.CUR        = record['CUR']
        TradeContext.OCCAMT     = str(record['OCCAMT'])
        TradeContext.CHRGTYP    = record['CHRGTYP']
        TradeContext.CUSCHRG    = str(record['CUSCHRG'])
        TradeContext.PYRACC     = record['PYRACC']
        TradeContext.PYRNAM     = record['PYRNAM']
        TradeContext.PYEACC     = record['PYEACC']
        TradeContext.PYENAM     = record['PYENAM']
        TradeContext.STRINFO    = record['STRINFO']
        TradeContext.CERTTYPE   = record['CERTTYPE']
        TradeContext.CERTNO     = record['CERTNO']
        TradeContext.BNKBKNO    = record['BNKBKNO']
        TradeContext.BNKBKBAL   = str(record['BNKBKBAL'])
        
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '���׳ɹ�'
    
    return True
        