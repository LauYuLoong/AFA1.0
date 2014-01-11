# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).��ͨ�������Ľ���
#==============================================================================
#   �����ļ�:   TRCC006_1136.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��  
#   �޸�ʱ��:   2008-10-29
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc  
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_atcbka
import rccpsMap1136CTradeContext2Dwtrbka_dict


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��ͨ�������Ľ���[TRCC006_1136]����***' )
    
    #�ж��Ƿ��ظ�����
    AfaLoggerFunc.tradeInfo(">>>��ʼ�ж��Ƿ��ظ�����")
    
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_wtrbka.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','�ж��Ƿ��ظ����ģ���ѯͨ��ͨ��ҵ��Ǽǲ���ͬ�����쳣')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('ͨ��ͨ��ҵ��Ǽǲ��д�����ͬ����,�ظ�����,���ؾܾ�Ӧ����')
        #=====ΪӦ���ĸ�ֵ====
        TradeContext.sysType  = 'rccpst'
        TradeContext.MSGTYPCO = 'SET006'
        TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO
        TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO
        TradeContext.SNDBRHCO = TradeContext.BESBNO
        TradeContext.SNDCLKNO = TradeContext.BETELR
        #TradeContext.SNDTRDAT = TradeContext.BJEDTE
        #TradeContext.SNDTRTIM = TradeContext.BJETIM
        TradeContext.ORMFN    = TradeContext.MSGFLGNO
        #TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.SerialNo
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.OPRTYPNO = '30'
        TradeContext.ROPRTPNO = TradeContext.OPRTYPNO
        TradeContext.TRANTYP  = '0'
    
        TradeContext.CUR      = 'CNY'
        TradeContext.PRCCO    = 'NN1IM101'
        TradeContext.STRINFO  = "�ظ�����"

        #=====����afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','�ظ����ģ��˳���������')

    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ��ظ�����")
    
    #�Ǽ�ͨ��ͨ�ҵǼǲ�
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
    
    #=====����ת��====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'
        
    #=====��������ȡ��ʽ=====
    if float(TradeContext.CUSCHRG) > 0.001:
        TradeContext.CHRGTYP = '1'
    else:
        TradeContext.CHRGTYP = '0'
        
    #====��ʼ���ֵ丳ֵ====
    wtrbka_dict = {}
    if not rccpsMap1136CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('M999', '�ֵ丳ֵ����')
    
    wtrbka_dict['DCFLG'] = PL_DCFLG_CRE                  #�����ʶ
    wtrbka_dict['OPRNO'] = PL_TDOPRNO_TC                 #ҵ������
    
    #=====��ʼ�������ݿ�====
    if not rccpsDBFunc.insTransWtr(wtrbka_dict):
        return False
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
    
    #����ҵ��״̬Ϊ�������׳ɹ�
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���׳ɹ�")
    
    stat_dict   = {}
    stat_dict['BSPSQN']   = TradeContext.BSPSQN
    stat_dict['BJEDTE']   = TradeContext.BJEDTE
    stat_dict['BCSTAT']   = PL_BCSTAT_BNKRCV
    stat_dict['BDWFLG']   = PL_BDWFLG_SUCC
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬���׳ɹ��쳣')
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���׳ɹ�")
    
    #����ҵ��״̬Ϊȷ�����˴�����
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊȷ�����˴�����")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CONFACC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊȷ�����˴������쳣')
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊȷ�����˴�����")
    
    #��ʼ��������
    TradeContext.PRCCO = 'RCCI0000'
    TradeContext.STRINFO = "�ɹ�"
    TradeContext.BCSTAT = PL_BCSTAT_CONFACC #״̬:ȷ�ϸ���
    TradeContext.BCSTATNM = "ȷ�ϸ���"
    #���б�Ҫ�Լ��,��У��ͨ��,�򷵻سɹ�Ӧ����,��У��δͨ��,�򷵻ؾܾ�Ӧ����
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")
    AfaLoggerFunc.tradeInfo(">>>��ѯ�����˻��ɹ�")

    #�������Ǽǲ����Ƿ��д˱�ҵ��ĳ���ҵ��,�����򷵻ؾܾ�Ӧ����,������ҵ��״̬Ϊ����������
    if TradeContext.PRCCO == 'RCCI0000':
        atcbka_where_dict = {}
        atcbka_where_dict['ORMFN'] = TradeContext.MSGFLGNO

        atcbka_dict = rccpsDBTrcc_atcbka.selectu(atcbka_where_dict)
        
        if atcbka_dict == None:
            #return AfaFlowControl.ExitThisFlow('S999', "��ѯ�����Ǽǲ��쳣")
            AfaLoggerFunc.tradeInfo(">>>��ѯ�����Ǽǲ��쳣")
            TradeContext.PRCCO = 'NN1ID003'
            TradeContext.STRINFO = "ϵͳ����,��ѯ�����Ǽǲ��쳣"
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
        
        else:
            if len(atcbka_dict) <= 0:
                AfaLoggerFunc.tradeInfo(">>>�˽���δ������,����У��")

            else:
                AfaLoggerFunc.tradeInfo(">>>�˽����ѱ�����,���ؾܾ�Ӧ����")
                TradeContext.PRCCO = 'NN1IO307'
                TradeContext.STRINFO = "�˽����ѱ�����"
                TradeContext.BCSTAT = PL_BCSTAT_CANC

    #�Ʊ�����#
    sql = "SELECT ischkactname,ischklate FROM rcc_chlabt where transcode='"+TradeContext.TransCode+"' and channelno= '"+(TradeContext.SNDCLKNO)[6:8]+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql( sql)
    if (records == None):
        return False
    elif (len(records) == 0):
        AfaLoggerFunc.tradeDebug("��ѯ���Ϊ��,��ѯ����[" + sql + "]")
        return False
    AfaLoggerFunc.tradeDebug(str(records))
        
    #У���˻�״̬�Ƿ��������˺Ż����Ƿ����
    if TradeContext.PRCCO == 'RCCI0000':
    
        #���������ӿڲ�ѯ�˻���Ϣ
        TradeContext.HostCode = '8810'

        TradeContext.ACCNO = TradeContext.PYEACC
        #TradeContext.WARNTNO = TradeContext.BNKBKNO

        AfaLoggerFunc.tradeDebug("ACCNO :" + TradeContext.ACCNO)
        #AfaLoggerFunc.tradeDebug("WARNTNO :" + TradeContext.WARNTNO)

        rccpsHostFunc.CommHost( TradeContext.HostCode )

        if TradeContext.errorCode != '0000':
            #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
            AfaLoggerFunc.tradeInfo("��ѯ�˻���Ϣ�쳣,����������[" + TradeContext.errorCode + "],����������Ϣ[" + TradeContext.errorMsg +"]")
            TradeContext.PRCCO = rccpsDBFunc.HostErr2RccErr(TradeContext.errorCode)
            TradeContext.STRINFO = "��ѯ�����˻���Ϣʧ�� " + TradeContext.errorMsg
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
        else:
            AfaLoggerFunc.tradeInfo(">>>��ѯ�����˻��ɹ�")
            
            #if TradeContext.BESBNO != PL_BESBNO_BCLRSB:
            #    AfaLoggerFunc.tradeInfo(">>>" + TradeContext.BESBNO + ">>>" + TradeContext.ACCSO)
            #    if( TradeContext.BESBNO[:6] != TradeContext.ACCSO[:6] ):
            #        AfaLoggerFunc.tradeInfo(">>>����編�����˽���")
            #        TradeContext.PRCCO = 'NN1IO999'
            #        TradeContext.STRINFO = "���������˻������в�����ͬһ����"
            #        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            #        TradeContext.BCSTATNM = "�ܾ�"
            
            #��鱾�����Ƿ���ͨ��ͨ��ҵ��Ȩ��
            if not rccpsDBFunc.chkTDBESAuth(TradeContext.ACCSO):
                TradeContext.PRCCO = 'NN1IO999'
                TradeContext.STRINFO = "���˻�����������ͨ��ͨ��ҵ��Ȩ��"
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "�ܾ�"
            
            if TradeContext.PRCCO == 'RCCI0000':
                AfaLoggerFunc.tradeInfo(">>>��ʼ���»�����Ϊ��������")
                TradeContext.BESBNO = TradeContext.ACCSO
                wtrbka_update_dict = {'BESBNO':TradeContext.ACCSO}
                wtrbka_where_dict  = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
                ret = rccpsDBTrcc_wtrbka.updateCmt(wtrbka_update_dict,wtrbka_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo(">>>���»�����Ϊ���������쳣")
                    TradeContext.PRCCO = 'RCCI1000'
                    TradeContext.STRINFO = "ϵͳ����,��������������쳣"
                    TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "�ܾ�"
                
                else:
                    AfaLoggerFunc.tradeInfo(">>>���»�����Ϊ���������ɹ�")
                    AfaLoggerFunc.tradeDebug("�������ػ���ACCNM :[" + TradeContext.ACCNM + "]")
                    AfaLoggerFunc.tradeDebug("���Ľ��ջ���PYENAM:[" + TradeContext.PYENAM + "]")
                    AfaLoggerFunc.tradeDebug("���������˻�״̬ACCST:[" + TradeContext.ACCST + "]")
                    
                    
                    if TradeContext.ACCNM != TradeContext.PYENAM:
                        #�Ʊ�����#
                        if(records[0][0]=='1'):
                            AfaLoggerFunc.tradeInfo(">>>�˺Ż�������")
                            TradeContext.PRCCO = 'NN1IA102'
                            TradeContext.STRINFO = '�˺Ż�������'
                            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                            TradeContext.BCSTATNM  = "�ܾ�"
                    
                    elif TradeContext.ACCST != '0' and TradeContext.ACCST != '2':
                        AfaLoggerFunc.tradeInfo(">>>�˻�״̬������")
                        TradeContext.PRCCO = 'NN1IA999'
                        TradeContext.STRINFO = '�˻�״̬������'
                        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM  = "�ܾ�"
                        
                    elif not (TradeContext.ACCCD == '0428' and TradeContext.ACCEM == '21111'):
                        AfaLoggerFunc.tradeInfo(">>>���˻��Ǹ��˽��㻧")
                        TradeContext.PRCCO   = 'NN1IA999'
                        TradeContext.STRINFO = '���˻��Ǹ��˽��㻧'
                        TradeContext.BCSTAT  = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM  = "�ܾ�"
                    
    #У��ƾ֤״̬�Ƿ�����
    #if TradeContext.PRCCO == 'RCCI0000':
    #    #���������ӿڲ�ѯƾ֤��Ϣ
    #    TradeContext.HostCode = '8811'
    #
    #    TradeContext.ACCNO = TradeContext.PYEACC
    #    TradeContext.WARNTNO = TradeContext.BNKBKNO
    #
    #    AfaLoggerFunc.tradeDebug("ACCNO :" + TradeContext.ACCNO)
    #    AfaLoggerFunc.tradeDebug("WARNTNO :" + TradeContext.WARNTNO)
    #
    #    rccpsHostFunc.CommHost( TradeContext.HostCode )
    #
    #    if TradeContext.errorCode != '0000':
    #        #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    #        AfaLoggerFunc.tradeInfo("��ѯƾ֤��Ϣ�쳣,����������[" + TradeContext.errorCode + "],����������Ϣ[" + TradeContext.errorMsg +"]")
    #        TradeContext.PRCCO = 'RCCI1000'
    #        TradeContext.STRINFO = "��ѯ����ƾ֤��Ϣʧ�� " + TradeContext.errorMsg
    #        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
    #        TradeContext.BCSTATNM = "�ܾ�"
    #
    #    else:
    #        #��ѯ�ɹ�
    #        AfaLoggerFunc.tradeInfo(">>>��ѯ����ƾ֤��Ϣ�ɹ�")
    #        AfaLoggerFunc.tradeInfo(">>>ƾ֤��ϢACCSTCD:[" + TradeContext.ACCSTCD + "]")
    #        
    #        if TradeContext.ACCSTCD != '0':
    #            TradeContext.PRCCO    = 'RCCI1000'
    #            TradeContext.STRINFO  = '�˻�ƾ֤״̬������'
    #            TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
    #            TradeContext.BCSTATNM = "�ܾ�"

    AfaLoggerFunc.tradeInfo(">>>������Ҫ�Լ��")
    
    #ΪӦ���ĸ�ֵ
    TradeContext.sysType  = 'rccpst'
    TradeContext.MSGTYPCO = 'SET006'
    TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO
    TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    #TradeContext.SNDTRDAT = TradeContext.BJEDTE
    #TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.ORMFN    = TradeContext.MSGFLGNO
    #TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.SerialNo
    #TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = '30'
    TradeContext.ROPRTPNO = TradeContext.OPRTYPNO
    TradeContext.TRANTYP  = '0'
    
    TradeContext.CUR      = 'CNY'
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��ͨ�������Ľ���[TRCC006_1136]�˳�***' )
    return True


#=====================���׺���===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).��ͨ�������Ľ���[TRCC006_1136]����***' )
    
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['PRCCO']   = TradeContext.PRCCO
    stat_dict['STRINFO'] = TradeContext.STRINFO
    
    #����afe�������ж�Ӧ�����Ƿ��ͳɹ�,��������Ӧҵ��״̬
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        #=====����ũ�����ɹ�,����״̬Ϊȷ������\�ܾ�\�����ɹ�====
        stat_dict['BCSTAT']  = TradeContext.BCSTAT
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ�����쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�ɹ�����ҵ��״̬Ϊ" + TradeContext.BCSTATNM + "�ɹ�")
    else:
        #=====����ũ����ʧ��,����״̬Ϊȷ������\�ܾ�\����ʧ��====       
        stat_dict['BCSTAT']  = TradeContext.BCSTAT
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ����ʧ��")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).��ͨ�������Ľ���[TRCC006_1136]�˳�***' )
    return True
        
