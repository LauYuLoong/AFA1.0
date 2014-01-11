# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).�Զ�����
#==============================================================================
#   �����ļ�:   TRCC003_8582.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-12-03
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_atcbka
import rccpsMap8582CTradeContext2Datcbka_dict


#=====================����ǰ����(���ز���,����ǰ����)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�Զ�����[TRCC003_8582]����***' )
    
    #=====У������ĺϷ���====
    if not TradeContext.existVariable("BOJEDT"):
        return AfaFlowControl.ExitThisFlow('A099','ԭ�������ڲ���Ϊ��')  
        
    if not TradeContext.existVariable("BOSPSQ"):
        return AfaFlowControl.ExitThisFlow('A099','ԭ������Ų���Ϊ��')
        
    #if not TradeContext.existVariable("RESNNM"):
    #    return AfaFlowControl.ExitThisFlow('A099','����ԭ����Ϊ��')
    
    #��ѯԭ������Ϣ
    trc_dict = {}
    
    if rccpsDBFunc.getTransWtr(TradeContext.BOJEDT,TradeContext.BOSPSQ,trc_dict):
        AfaLoggerFunc.tradeInfo(">>>ͨ��ͨ�ҵǼǲ����ҵ�ԭ����")
        
    elif rccpsDBFunc.getTransMpc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trc_dict):
        AfaLoggerFunc.tradeInfo(">>>�����Ǽǲ����ҵ�ԭ����")
        
    else:
        return AfaFlowControl.ExitThisFlow("S999","�޴˽���")
        
    #�ж�ԭ�����Ƿ�Ϊ����
    if( trc_dict['BRSFLG'] != PL_BRSFLG_SND):
        return AfaFlowControl.ExitThisFlow('A099','�˽��׷�����,��ֹ����')
        
    #�жϱ��������׵������Ƿ�Ϊ����
    if( trc_dict['NCCWKDAT'] != TradeContext.NCCworkDate ):
        return AfaFlowControl.ExitThisFlow('A099','�˽��׷ǵ��ս���,��ֹ����')
        
    #�жϵ�ǰ�����Ƿ�Ϊԭ���׻���
    if( trc_dict['BESBNO'] != TradeContext.BESBNO ):
        return AfaFlowControl.ExitThisFlow('A099','��ǰ������ԭ���׻���,��ֹ����')
    
    #�жϵ�ǰ��Ա�Ƿ�Ϊԭ���׹�Ա
    if( trc_dict['BETELR'] != TradeContext.BETELR ):
        return AfaFlowControl.ExitThisFlow('A099','��ǰ��Ա��ԭ���׹�Ա,��ֹ����')
        
    if trc_dict['TRCCO'] in('3000002','3000003','3000004','3000005','3000102','3000103','3000104','3000105','3000505'):
        AfaLoggerFunc.tradeInfo(">>>ԭ����Ϊͨ���ͨ�������ཻ��")
        
        #�ж�ԭ���׵�ǰ״̬�Ƿ���Գ���
        #ԭ���׵�ǰ״̬Ϊ:���ʹ�����,���ͳɹ�,����ʧ��,�������
        if not ((trc_dict['BCSTAT'] == PL_BCSTAT_SND and (trc_dict['BDWFLG'] == PL_BDWFLG_WAIT or trc_dict['BDWFLG'] == PL_BDWFLG_SUCC)) or (trc_dict['BCSTAT'] == PL_BCSTAT_ACC) and trc_dict['BDWFLG'] == PL_BDWFLG_FAIL):
            return AfaFlowControl.ExitThisFlow("S999","�˽��׵�ǰ״̬Ϊ[" + trc_dict['BCSTAT'] + "][" + trc_dict['BDWFLG'] + "],��ֹ����")
        
        #�Ǽǳ����Ǽǲ�
        AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǳ����Ǽǲ�")
        
        TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
        TradeContext.RCVMBRCO = trc_dict['RCVMBRCO']
        TradeContext.ORTRCDAT = trc_dict['TRCDAT']
        TradeContext.OPRNO    = PL_TDOPRNO_CZ
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.NCCworkDate + TradeContext.SerialNo
        TradeContext.ORMFN    = trc_dict['MSGFLGNO']
        TradeContext.TRCCO    = "3000506" 
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.ORTRCCO  = trc_dict['TRCCO']
        TradeContext.ORTRCNO  = trc_dict['TRCNO']
        TradeContext.SNDBNKCO = trc_dict['SNDBNKCO']
        TradeContext.SNDBNKNM = trc_dict['SNDBNKNM']
        TradeContext.RCVBNKCO = trc_dict['RCVBNKCO']
        TradeContext.RCVBNKNM = trc_dict['RCVBNKNM']
        
        insert_dict = {}
        
        rccpsMap8582CTradeContext2Datcbka_dict.map(insert_dict)
        
        ret = rccpsDBTrcc_atcbka.insertCmt(insert_dict)
        
        if( ret <= 0 ):
            return AfaFlowControl.ExitThisFlow('S999','�Ǽ��Զ������Ǽǲ�ʧ��')
        
        AfaLoggerFunc.tradeInfo(">>>�����Ǽǳ����Ǽǲ�")
        
        #��ԭ���׵�ǰ״̬�ǳ���������,������ԭ����״̬Ϊ����������
        #if not (trc_dict['BCSTAT'] == PL_BCSTAT_CANCEL and trc_dict['BDWFLG'] == PL_BDWFLG_WAIT):
        #    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ����������")
        #    
        #    if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_WAIT):
        #        return AfaFlowControl.ExitThisFlow("S999","����ԭ���׵�ǰ״̬Ϊ�����������쳣")
        #
        #    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ����������")
        #    
        #if not AfaDBFunc.CommitSql( ):
        #    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        #    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
        #Ϊ����������׼��
        #=====����ͷ====
        TradeContext.MSGTYPCO = 'SET009'
        TradeContext.RCVSTLBIN= trc_dict['RCVMBRCO']
        #TradeContext.SNDBRHCO = TradeContext.BESBNO
        #TradeContext.SNDCLKNO = TradeContext.BETELR
        #TradeContext.SNDTRDAT = TradeContext.BJEDTE
        #TradeContext.SNDTRTIM = TradeContext.BJETIM
        #TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
        #TradeContext.ORMFN    = wtr_dict['MSGFLGNO']
        #TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.OPRTYPNO = "30"
        TradeContext.ROPRTPNO = "30"
        TradeContext.TRANTYP  = "0"
        #=====ҵ��Ҫ�ؼ�====
        TradeContext.CUR      = trc_dict['CUR']
        TradeContext.OCCAMT   = str(trc_dict['OCCAMT'])
        
        #�����Ѵ���
        if trc_dict['TRCCO'] == '3000002' or trc_dict['TRCCO'] == '3000003' or trc_dict['TRCCO'] == '3000004' or trc_dict['TRCCO'] == '3000005':
            TradeContext.CUSCHRG  = "0.00"
        elif trc_dict['TRCCO'] == '3000102' or trc_dict['TRCCO'] == '3000103' or trc_dict['TRCCO'] == '3000104' or trc_dict['TRCCO'] == '3000105':
            if trc_dict['CHRGTYP'] == '1':
                TradeContext.CUSCHRG = str(trc_dict['CUSCHRG'])
            else:
                TradeContext.CUSCHRG = '0.00'
                
        TradeContext.PYRACC   = trc_dict['PYRACC']
        TradeContext.PYRNAM   = trc_dict['PYRNAM']
        TradeContext.PYEACC   = trc_dict['PYEACC']
        TradeContext.PYENAM   = trc_dict['PYENAM']
        TradeContext.CURPIN   = ""
        TradeContext.STRINFO  = ""
        TradeContext.PRCCO    = ""
        #=====��չҪ�ؼ�====
        TradeContext.RESNCO = TradeContext.RESNNM  
        
        
    elif trc_dict['TRCCO'] == '3000504':
        AfaLoggerFunc.tradeInfo(">>>ԭ����Ϊ��������")
        
        if trc_dict['PRCCO'].lstrip() != "":
            return AfaFlowControl.ExitThisFlow("S999","���յ�����Ӧ��,��ֹ�����˳�������")
        
        wtr_dict = {}
        
        if not rccpsDBFunc.getTransWtr(trc_dict['BOJEDT'],trc_dict['BOSPSQ'],wtr_dict):
            return AfaFlowControl.ExitThisFlow("S999","ͨ��ͨ�ҵǼǲ���δ�ҵ�ԭ����������")
            
        #��ԭ���������׵�ǰ״̬Ϊ����,��ֹ�����˳�������
        if wtr_dict['BCSTAT'] == PL_BCSTAT_CANC:
            return AfaFlowControl.ExitThisFlow("S999","ԭ�����������ѱ������ɹ���ʧ��,��ֹ�����˳�������")
            
        #�Ǽǳ����Ǽǲ�
        AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǳ����Ǽǲ�")
        
        TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
        TradeContext.RCVMBRCO = trc_dict['RCVMBRCO']
        TradeContext.ORTRCDAT = trc_dict['TRCDAT']
        TradeContext.OPRNO    = PL_TDOPRNO_CZ
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.NCCworkDate + TradeContext.SerialNo
        TradeContext.ORMFN    = trc_dict['MSGFLGNO']
        TradeContext.TRCCO    = "3000506"
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.ORTRCCO  = trc_dict['TRCCO']
        TradeContext.ORTRCNO  = trc_dict['TRCNO']
        TradeContext.SNDBNKCO = trc_dict['SNDBNKCO']
        TradeContext.SNDBNKNM = trc_dict['SNDBNKNM']
        TradeContext.RCVBNKCO = trc_dict['RCVBNKCO']
        TradeContext.RCVBNKNM = trc_dict['RCVBNKNM']
        
        insert_dict = {}
        
        rccpsMap8582CTradeContext2Datcbka_dict.map(insert_dict)
        
        ret = rccpsDBTrcc_atcbka.insertCmt(insert_dict)
        
        if( ret <= 0 ):
            return AfaFlowControl.ExitThisFlow('S999','�Ǽ��Զ������Ǽǲ�ʧ��')
        
        AfaLoggerFunc.tradeInfo(">>>�����Ǽǳ����Ǽǲ�")
        
        #Ϊ����������׼��
        #=====����ͷ====
        TradeContext.MSGTYPCO = 'SET009'
        TradeContext.RCVSTLBIN= trc_dict['RCVMBRCO']
        #TradeContext.SNDBRHCO = TradeContext.BESBNO
        #TradeContext.SNDCLKNO = TradeContext.BETELR
        #TradeContext.SNDTRDAT = TradeContext.BJEDTE
        #TradeContext.SNDTRTIM = TradeContext.BJETIM
        #TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
        #TradeContext.ORMFN    = wtr_dict['MSGFLGNO']
        #TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.OPRTYPNO = "30"
        TradeContext.ROPRTPNO = "30"
        TradeContext.TRANTYP  = "0"
        #=====ҵ��Ҫ�ؼ�====
        TradeContext.CUR      = wtr_dict['CUR']
        TradeContext.OCCAMT   = str(wtr_dict['OCCAMT'])
        
        #�����Ѵ���
        if wtr_dict['TRCCO'] == '3000002' or wtr_dict['TRCCO'] == '3000003' or wtr_dict['TRCCO'] == '3000004' or wtr_dict['TRCCO'] == '3000005':
            TradeContext.CUSCHRG  = "0.00"
        elif wtr_dict['TRCCO'] == '3000102' or wtr_dict['TRCCO'] == '3000103' or wtr_dict['TRCCO'] == '3000104' or wtr_dict['TRCCO'] == '3000105':
            if wtr_dict['CHRGTYP'] == '1':
                TradeContext.CUSCHRG = str(wtr_dict['CUSCHRG'])
            else:
                TradeContext.CUSCHRG = '0.00'
                
        TradeContext.PYRACC   = wtr_dict['PYRACC']
        TradeContext.PYRNAM   = wtr_dict['PYRNAM']
        TradeContext.PYEACC   = wtr_dict['PYEACC']
        TradeContext.PYENAM   = wtr_dict['PYENAM']
        TradeContext.CURPIN   = ""
        TradeContext.STRINFO  = ""
        TradeContext.PRCCO    = ""
        #=====��չҪ�ؼ�====
        TradeContext.RESNCO = TradeContext.RESNNM  
        
    else:
        return AfaFlowControl.ExitThisFlow("S999","ԭ���׷�ͨ���ͨ�������ཻ�׻��������,��ֹ����")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�Զ�����[TRCC003_8582]����***' )
    
    return True


#=====================���׺���===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).�Զ�����[TRCC003_8582]����***' )
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    #�ж��Ƿ��ͳɹ�
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo(">>>�������ķ��ͳɹ�")
        
    else:
        AfaLoggerFunc.tradeInfo(">>>�������ķ���ʧ��")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).�Զ�����[TRCC003_8582]����***' )
    
    return True
    
