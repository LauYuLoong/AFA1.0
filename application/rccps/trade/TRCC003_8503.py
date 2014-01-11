# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Ʊ����
#===============================================================================
#   �����ļ�:   TRCC003_8503.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-08-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsMap8503Dbilinf2CTradeContext,rccpsMap8503CTradeContext2Dbilbka
import rccpsDBTrcc_bilbka

#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊ����[TRCC003_8503]����***' )
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #У�鵱ǰ��Ʊ״̬�Ƿ�Ϊǩ������
    AfaLoggerFunc.tradeInfo(">>>��ʼУ�鵱ǰ��Ʊ״̬�Ƿ�Ϊǩ������")
    
    bilinf_dict = {}
    if not rccpsDBFunc.getInfoBil(TradeContext.BILVER,TradeContext.BILNO,PL_BILRS_INN,bilinf_dict):
        return AfaFlowControl.ExitThisFlow("S999","��ѯ��Ʊ��Ϣ�쳣")
        
    if bilinf_dict['REMBNKCO'] != TradeContext.SNDBNKCO:
        return AfaFlowControl.ExitThisFlow("S999","���зǴ˻�Ʊ��Ʊ��,��ֹ�ύ")
        
    if bilinf_dict['BILDAT'] != TradeContext.BJEDTE:
        return AfaFlowControl.ExitThisFlow("S999","�ǽ���ǩ���Ļ�Ʊ,��ֹ�ύ")
        
    if bilinf_dict['HPSTAT'] != PL_HPSTAT_SIGN and bilinf_dict['HPSTAT'] != PL_HPSTAT_DEHG and bilinf_dict['HPSTAT'] != PL_HPSTAT_HANG:
        return AfaFlowControl.ExitThisFlow("S999","�˻�Ʊ��ǰ״̬��[ǩ��,��ʧ,���],��ֹ�ύ")
    
        
    #=====ͨ�����ڣ�������Ų�ѯ��Ʊҵ��Ǽǲ�rcc_bilbka��ȡ���ʽ���Դ��====
    #=====�˹�ͨ���������====
    bilbka_where_dict = {'BJEDTE':bilinf_dict['NOTE1'],'BSPSQN':bilinf_dict['NOTE2']}
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    if( bilbka_dict == None ):
        return AfaFlowControl.ExitThisFlow("S999","��ѯ��Ʊҵ��Ǽǲ��쳣")
        
    if( len(bilbka_dict) <= 0 ):
        return AfaFlowControl.ExitThisFlow("S999","��ѯ��Ʊҵ��Ǽǲ�Ϊ��")
        
    #=====�˹�ͨ 0916 �жϹ�Ա�ͻ����Ƿ�Ϊǩ����Ա�ͻ���====
    if( bilbka_dict['BETELR'] != TradeContext.BETELR ):
        return AfaFlowControl.ExitThisFlow("S999","�˹�Ա����¼���Ա")
        
    #if( bilbka_dict['BESBNO'] != TradeContext.BESBNO):
    #    return AfaFlowControl.ExitThisFlow("S999","�˻�������¼�����")
        
    #��ǩ�����׵��ʽ���Դ��ֵ��������
    TradeContext.BBSSRC = bilbka_dict['BBSSRC']
    
    #����Ʊ��Ϣӳ�䵽TradeContext��
    if not rccpsMap8503Dbilinf2CTradeContext.map(bilinf_dict):
        return False
    
    AfaLoggerFunc.tradeInfo(">>>����У�鵱ǰ��Ʊ״̬�Ƿ�Ϊǩ������")
    
    #��Ʊ�ཻ�׽��ճ�Ա��Ϊ������
    TradeContext.RCVSTLBIN = PL_RCV_CENTER
    
    #������Ϊǩ��ʱ�Ĵ�������
    TradeContext.RCVBNKCO  = TradeContext.PAYBNKCO
    TradeContext.RCVBNKNM  = TradeContext.PAYBNKNM
    
    #�Ǽǻ�Ʊҵ��Ǽǲ�
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ�Ʊҵ��Ǽǲ�")
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRNO    = PL_HPOPRNO_CX               #ҵ������:����
    TradeContext.DCFLG    = PL_DCFLG_DEB                #�����ʶ:���
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #������ʶ:����
    TradeContext.TRCCO    = '2100101'                   #���״���:2100101��Ʊ����
    
    bilbka_dict = {}
    if not rccpsMap8503CTradeContext2Dbilbka.map(bilbka_dict):
        return False
    
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǻ�Ʊҵ��Ǽǲ��쳣')
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ�Ʊҵ��Ǽǲ�")
    
    #����ҵ��״̬Ϊ���ʹ�����
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���ʹ�����")
    
    stat_dict = {}
    stat_dict['BJEDTE'] = TradeContext.BJEDTE
    stat_dict['BSPSQN'] = TradeContext.BSPSQN
    stat_dict['BCSTAT'] = PL_BCSTAT_SND
    stat_dict['BDWFLG'] = PL_BDWFLG_WAIT
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','����״̬Ϊ���ʹ������쳣')
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���ʹ�����")
    
    #COMMIT
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    #Ϊ����ũ����������׼��
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ����ũ����������׼��")
    
    TradeContext.MSGTYPCO = 'SET001'
    TradeContext.TRCCO    = '2100101'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = ""
    TradeContext.OPRTYPNO = '21'
    TradeContext.ROPRTPNO = ''
    TradeContext.TRANTYP  = '0'
    TradeContext.OCCAMT   = str(TradeContext.BILAMT)
    TradeContext.BILAMT   = str(TradeContext.BILAMT)
    
    #begin 20110614 ����̩ �޸� ����ũ�������ĵ�Ʊ��Ϊ8λ
    TradeContext.BILNO = TradeContext.BILNO[-8:]
    #end
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ����ũ����������׼��")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊ����[TRCC003_8503]�˳�***' )
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).��Ʊ����[TRCC003_8503]����***' )
    
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['BCSTAT']  = PL_BCSTAT_SND
    stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
    stat_dict['PRCCO']   = TradeContext.errorCode
    stat_dict['STRINFO'] = TradeContext.errorMsg
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        #����ũ�����ɹ�,����ҵ��״̬Ϊ���ͳɹ�
        AfaLoggerFunc.tradeInfo(">>>����ũ���������ĳɹ�")
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���ͳɹ�")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ���ͳɹ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���ͳɹ�")
        
    else:
        #����ũ����ʧ��,����ҵ��״̬Ϊ����ʧ��
        AfaLoggerFunc.tradeInfo(">>>����ũ����������ʧ��")
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ����ʧ��")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ����ʧ��")
    
    #COMMIT
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).��Ʊ����[TRCC003_8503]�˳�***' )
    
    return True
    
