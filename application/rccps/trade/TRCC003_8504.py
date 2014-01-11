# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Ʊ��Ʊ
#===============================================================================
#   �����ļ�:   TRCC003_8504.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-08-06
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc
import rccpsMap8504CTradeContext2Dbilbka,rccpsMap8504Dbilinf2CTradeContext
import rccpsDBTrcc_bilinf,rccpsDBTrcc_bilbka


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊ��Ʊ[TRCC003_8504]����***' )
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    AfaLoggerFunc.tradeInfo("BJEDTE=[" + TradeContext.BJEDTE + "]")
    
    #����Ʊ״̬,��ǩ����⸶״̬��ֹ�ύ
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ʊ״̬")
    
    bilinf_dict = {}
    if not rccpsDBFunc.getInfoBil(TradeContext.BILVER,TradeContext.BILNO,PL_BILRS_INN,bilinf_dict):
        return AfaFlowControl.ExitThisFlow("S999","��ѯ��Ʊ��Ϣ�쳣")
        
    AfaLoggerFunc.tradeInfo("----->" + bilinf_dict['REMBNKCO'])
    AfaLoggerFunc.tradeInfo("----->" + TradeContext.SNDBNKCO)
        
    if bilinf_dict['REMBNKCO'] != TradeContext.SNDBNKCO:
        return AfaFlowControl.ExitThisFlow("S999","���зǴ˻�Ʊ��Ʊ��,��ֹ�ύ")
        
    if bilinf_dict['HPSTAT'] != PL_HPSTAT_SIGN and bilinf_dict['HPSTAT'] != PL_HPSTAT_DEHG and bilinf_dict['HPSTAT'] != PL_HPSTAT_HANG:
        return AfaFlowControl.ExitThisFlow("S999","�˻�Ʊ��ǰ״̬��[ǩ��,��ʧ,���],��ֹ�ύ")
    
    #=====���Ӳ�ѯ��Ʊҵ��Ǽǲ�rcc_bilbka��Ϣ����ѯ����Ϊ����Ʊ��Ϣrcc_bilinf�Ǽǲ�note1��note2====
    #bilbka_dict = {}
    #bilbka_where_dict = {'BJEDTE':bilinf_dict['NOTE1'],'BSPSQN':bilinf_dict['NOTE2']}
    #bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    #if( bilbka_dict == None ):
    #    return AfaFlowControl.ExitThisFlow("S999","��ѯ��Ʊҵ��Ǽǲ��쳣")
    #    
    #if( len(bilbka_dict) == 0 ):
    #    return AfaFlowControl.ExitThisFlow("S999","��ѯ��Ʊҵ��Ǽ�Ϊ��")
        
    #bilinf_dict['BBSSRC'] = bilbka_dict['BBSSRC']
    #bilinf_dict['DASQ']   = bilbka_dict['DASQ']
    
    
    #=====ȡǩ�����׵�BBSSRC��DASQ�ֶΣ���ֵ��bilinf_dict�ֵ���====
    #=====����bilinf_dict['BBSSRC'] = bilbka_dict['BBSSRC']====
    
    
    #����Ʊ��Ϣӳ�䵽TradeContext��
    if not rccpsMap8504Dbilinf2CTradeContext.map(bilinf_dict):
        return False
    
    AfaLoggerFunc.tradeInfo(">>>��������Ʊ״̬")
    
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
    if TradeContext.OPRFLG == '0':
        TradeContext.OPRNO    = PL_HPOPRNO_TP           #ҵ������:��Ʊ��Ʊ
    else:
        TradeContext.OPRNO    = PL_HPOPRNO_CF           #ҵ������:��Ʊ���ڸ���
    TradeContext.DCFLG    = PL_DCFLG_DEB                #�����ʶ:���
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #������ʶ:����
    TradeContext.TRCCO    = '2100103'                   #���״���:2100103��Ʊ��Ʊ
    
    bilbka_dict = {}
    if not rccpsMap8504CTradeContext2Dbilbka.map(bilbka_dict):
        return False
    
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǻ�Ʊҵ��Ǽǲ��쳣')
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ�Ʊҵ��Ǽǲ�")
    
    #���»�Ʊ��Ϣ�Ǽǲ�
    AfaLoggerFunc.tradeInfo(">>>��ʼ���»�Ʊ��Ϣ�Ǽǲ�")
    
    bilinf_update_dict = {}
    if TradeContext.OPRFLG == '0':
        
        #=================У�������˺Ż���======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼУ�������˺Ż���")
        
        TradeContext.HostCode = '8810'
        
        TradeContext.ACCNO = bilinf_dict['PYRACC']
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNO)
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNM)
        
        if TradeContext.ACCNM != bilinf_dict['PYRNAM']:
            return AfaFlowControl.ExitThisFlow('S999',"�����˺Ż�������")
            
        if TradeContext.ACCST != '0' and TradeContext.ACCST != '2':
            return AfaFlowControl.ExitThisFlow('S999','�����˺�״̬������')
        
        AfaLoggerFunc.tradeInfo(">>>����У�������˺Ż���")
        
        bilinf_update_dict['PYIACC'] = bilinf_dict['PYRACC']
        bilinf_update_dict['PYINAM'] = bilinf_dict['PYRNAM']
        
    elif TradeContext.OPRFLG == '1':
        #bilinf_update_dict['PYIACC'] = TradeContext.PYIACC
        #bilinf_update_dict['PYINAM'] = TradeContext.PYINAM
        #��������Ϊ���ڸ���ʱ,�����˺�Ϊ�������˺�
        bilinf_update_dict['PYIACC'] = TradeContext.BESBNO + PL_ACC_NXYDXZ
        bilinf_update_dict['PYINAM'] = "ũ����������"
    else:
        return AfaFlowControl.ExitThisFlow('S999','�������ͷǷ�')
    bilinf_update_dict['OCCAMT'] = TradeContext.OCCAMT
    bilinf_update_dict['RMNAMT'] = TradeContext.RMNAMT
    
    bilinf_where_dict = {}
    bilinf_where_dict['BILVER'] = TradeContext.BILVER
    bilinf_where_dict['BILNO']  = TradeContext.BILNO
    
    ret = rccpsDBTrcc_bilinf.update(bilinf_update_dict,bilinf_where_dict)
    
    if ret == None:
        return AfaFlowControl.ExitThisFlow("S999","���»�Ʊ��Ϣ�Ǽǲ��쳣")
        
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�޶�Ӧ�Ļ�Ʊ��Ϣ")
        
    AfaLoggerFunc.tradeInfo(">>>�������»�Ʊ��Ϣ�Ǽǲ�")
    
    #���ý���״̬Ϊ���ʹ�����
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
    
    #Ϊ����ũ������׼��
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ����ũ������׼��")
    
    TradeContext.MSGTYPCO = 'SET002'
    TradeContext.TRCCO    = '2100103'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = ''
    TradeContext.OPRTYPNO = '21'
    TradeContext.ROPRTPNO = ''
    TradeContext.TRANTYP  = '0'
    TradeContext.OCCAMT   = str(TradeContext.BILAMT)
    TradeContext.BILAMT   = str(TradeContext.BILAMT)
    
    #begin 20110614 ����̩ �޸� ����ũ�������ĵ�Ʊ��Ϊ8λ
    TradeContext.BILNO = TradeContext.BILNO[-8:]
    #end
    
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ����ũ������׼��")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊ��Ʊ[TRCC003_8504]�˳�***' )
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).��Ʊ��Ʊ[TRCC003_8504]����***' )
    
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
        AfaLoggerFunc.tradeInfo("����ũ�����ɹ�")
        AfaLoggerFunc.tradeInfo("��ʼ����ҵ��״̬Ϊ���ͳɹ�")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ���ͳɹ��쳣")
        
        AfaLoggerFunc.tradeInfo("��������ҵ��״̬Ϊ���ͳɹ�")
        
    else:
        #����ũ����ʧ��,����ҵ��״̬Ϊ����ʧ��
        AfaLoggerFunc.tradeInfo("����ũ����ʧ��")
        AfaLoggerFunc.tradeInfo("��ʼ����ҵ��״̬Ϊ����ʧ��")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
        
        AfaLoggerFunc.tradeInfo("��������ҵ��״̬Ϊ����ʧ��")
    
    #COMMIT
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).��Ʊ��Ʊ[TRCC003_8504]�˳�***' )
    return True
    
