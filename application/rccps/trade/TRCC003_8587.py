# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��̨����
#==============================================================================
#   �����ļ�:   TRCC003_8587.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-12-3
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsEntries,rccpsHostFunc,rccpsGetFunc
import rccpsDBTrcc_jstbka
import rccpsMap8563CTradeContext2Dwtrbka_dict

#==========����ǰ����(���ز���,����ǰ����)==========
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��̨����[TRCC003_8587]����***' )

    #=====��������Ϸ���====
    if not TradeContext.existVariable("BOJEDT"):
        return AfaFlowControl.ExitThisFlow('A099','ԭ�������ڲ���Ϊ��')  
        
    if not TradeContext.existVariable("BOSPSQ"):
        return AfaFlowControl.ExitThisFlow('A099','ԭ������Ų���Ϊ��')

    #=====��ѯԭ������Ϣ====
    wtr_dict = {}
    
    if rccpsDBFunc.getTransWtr(TradeContext.BOJEDT,TradeContext.BOSPSQ,wtr_dict):
        AfaLoggerFunc.tradeInfo(">>>ͨ��ͨ�ҵǼǲ����ҵ�ԭ����")
    else:
        return AfaFlowControl.ExitThisFlow('S0999','����ԭ������Ϣʧ��')
    
    swtr_dict = wtr_dict
    
    #=====�ж�ԭ�����Ƿ�Ϊ����====
    if( wtr_dict['BRSFLG'] != PL_BRSFLG_SND):
        return AfaFlowControl.ExitThisFlow('A099','�˽��׷�����,��ֹ����')
    
    #====�ж��˻���������====
    if TradeContext.DCFLG == '0':
        TradeContext.CBFLG = TradeContext.PYITYP
    else:
        TradeContext.CBFLG = TradeContext.PYOTYP
        
    #====�ж�ԭ����״̬====
    AfaLoggerFunc.tradeInfo("��ʼ�ж�ԭ������Ϣ�Ƿ�������")
    
    if (wtr_dict['BCSTAT'] != PL_BCSTAT_CANC and wtr_dict['BDWFLG'] != PL_BDWFLG_SUCC):
        return AfaFlowControl.ExitThisFlow("S999","����״̬["+str(wtr_dict['BCSTAT'])+"],��ֹ����")
        
    AfaLoggerFunc.tradeInfo("�����ж�ԭ������Ϣ�Ƿ�������")
    
    #=================�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�===================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")

    #=====================��ȡ������ˮ��====================================
    if rccpsGetFunc.GetRccSerialno( ) == -1 :
        raise AfaFlowControl.flowException( )
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN      #���ͳ�Ա�к�
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN      #���ճ�Ա�к�
    TradeContext.TRCNO    = TradeContext.SerialNo       #������ˮ��
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate    #���Ĺ�������
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.TRCDAT + TradeContext.SerialNo  #���ı�ʶ��
    TradeContext.OPRNO    = PL_TDOPRNO_BZ               #ҵ������:�����ֽ�ͨ��
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #������ʶ:����
    TradeContext.PYRMBRCO = TradeContext.SNDSTLBIN
    TradeContext.PYEMBRCO = TradeContext.RCVSTLBIN
    TradeContext.NOTE1    = TradeContext.BOJEDT
    TradeContext.NOTE2    = TradeContext.BOSPSQ
    TradeContext.TRCCO    = '3000505'
    
    wtrbka_dict = {}
    if not rccpsMap8563CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
        return AfaFlowContorl.ExitThisFlow("S999","Ϊͨ��ͨ��ҵ��Ǽǲ���ֵ�쳣")
        
    if(TradeContext.DCFLG == '0'):
        wtrbka_dict['DCFLG'] = '1'
    elif(TradeContext.DCFLG == '1'):
        wtrbka_dict['DCFLG'] = '2'
    else:
        return AfaFlowControl.ExitThisFlow('S999','�Ƿ������ʾ')
        
    if not rccpsDBFunc.insTransWtr(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽ�ͨ��ͨ��ҵ��Ǽǲ��쳣')
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
    
    #=====�ж�ԭ�����Ƿ�Ϊ��ת����ͨ��====
    if swtr_dict['TRCCO'] in ('3000102','3000103','3000104','3000105') and swtr_dict['CHRGTYP'] == '1':
        TradeContext.CUSCHRG = str(swtr_dict['CUSCHRG'])
    else:
        TradeContext.CUSCHRG = "0.00"
        
    #=====����ũ�������ģ�Ϊ���͹��汨����׼��====
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET009'   
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN    = swtr_dict['MSGFLGNO']
    TradeContext.TRCCO    = "3000505"
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "30"
    TradeContext.ROPRTPNO = "30"
    TradeContext.TRANTYP  = "0"
    #=====ҵ��Ҫ�ؼ�====
    TradeContext.CUR      = "CNY"
    TradeContext.OCCAMT   = str(TradeContext.OCCAMT)
    #TradeContext.OCCAMT   = str(wtr_dict['OCCAMT'])
    TradeContext.CUSCHRG  = str(TradeContext.CUSCHRG)
    TradeContext.ORTRCCO  = str(swtr_dict['TRCCO'])
    TradeContext.ORTRCNO  = str(swtr_dict['TRCNO'])

    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow("S999","����ԭ���׵�ǰ״̬Ϊ����-�������쳣")
        
    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ����-������")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    return True

#==========���׺���(���ز���,���ĺ���)==========
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('>>>���ĺ���')
    
    if TradeContext.errorCode == '0000':
        TradeContext.BDWFLG = PL_BDWFLG_SUCC
    else:
        TradeContext.BDWFLG = PL_BDWFLG_FAIL
        
    sstlog_dict={}
    sstlog_dict['BSPSQN']  = TradeContext.BSPSQN
    sstlog_dict['BJEDTE']  = TradeContext.BJEDTE
    sstlog_dict['BCSTAT']  = PL_BCSTAT_SND
    sstlog_dict['BDWFLG']  = TradeContext.BDWFLG
    
    if not rccpsState.setTransState(sstlog_dict):
        AfaDBFunc.RollBackSql()
        return AfaFlowControl.ExitThisFlow("S999","�޸�ԭ���׵�ǰ״̬Ϊ����-�ɹ��쳣")
    else:
        AfaDBFunc.CommitSql( )
        AfaLoggerFunc.tradeInfo(">>>�����޸�ԭ����״̬Ϊ����-�ɹ�")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��̨����[TRCC003_8587]�˳�***' )
    return True
    
