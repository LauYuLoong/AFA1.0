# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).���ȷ�������Ľ���
#==============================================================================
#   �����ļ�:   TRCC006_1143.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر�� 
#   �޸�ʱ��:   2008-11-03
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc
import rccpsDBTrcc_wtrbka


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).���ȷ�������Ľ���[TRCC006_1143]����***' )
    
    #�ж��Ƿ��ظ�����
    AfaLoggerFunc.tradeInfo(">>>��ʼ�ж��Ƿ��ظ�����")
    
    sel_dict = {'COTRCNO':TradeContext.TRCNO,'COTRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_wtrbka.selectu(sel_dict)
    
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','�ж��Ƿ��ظ����ȷ�ϱ���,��ѯͨ��ͨ��ҵ��Ǽǲ���ͬ�����쳣')
        
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('ͨ��ͨ��ҵ��Ǽǲ��д�����ͬ����,�ظ�����,����Ӧ����')
        TradeContext.STRINFO  = "�ظ�����"
    else:
        #��ѯԭ������Ϣ
        AfaLoggerFunc.tradeInfo(">>>���ظ�����,��ʼ��ѯԭ������Ϣ")
        
        wtrbka_dict = {}
        
        if not rccpsDBFunc.getTransWtrAK(TradeContext.SNDBNKCO,TradeContext.TRCDAT,TradeContext.ORTRCNO,wtrbka_dict):
            AfaFlowControl.ExitThisFlow('S999',"��ѯԭ������Ϣ�쳣")
            
        TradeContext.BJEDTE = wtrbka_dict['BJEDTE']
        TradeContext.BSPSQN = wtrbka_dict['BSPSQN']
        TradeContext.PYEACC = wtrbka_dict['PYEACC']
        TradeContext.PYENAM = wtrbka_dict['PYENAM']
        TradeContext.OCCAMT = wtrbka_dict['OCCAMT']
        TradeContext.BESBNO = wtrbka_dict['BESBNO']
        
        AfaLoggerFunc.tradeInfo(">>>������ѯԭ������Ϣ")
        
        
        #��齻�׵�ǰ״̬�Ƿ�Ϊȷ�����˳ɹ�,�Ǵ�״̬��������
        AfaLoggerFunc.tradeInfo(">>>��ʼ�жϽ��׵�ǰ״̬�Ƿ�Ϊȷ�����˳ɹ�")
        
        stat_dict = {}
        
        if not rccpsState.getTransStateCur(TradeContext.BJEDTE,TradeContext.BSPSQN,stat_dict):
            return AfaFlowControl.ExitThisFlow('S999',"��ȡԭ���׵�ǰ״̬�쳣")
            
        #if not (stat_dict['BCSTAT'] == PL_BCSTAT_CONFACC and stat_dict['BDWFLG'] == PL_BDWFLG_SUCC):
        #    return AfaFlowControl.ExitThisFlow('S999',"ԭ���׵�ǰ״̬��ȷ�����˳ɹ�,��������")
        
        AfaLoggerFunc.tradeInfo(">>>�����жϽ��׵�ǰ״̬�Ƿ�Ϊȷ�����˳ɹ�")
        
        #����ͨ��ͨ�ҵǼǲ����ȷ�������Ϣ
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ͨ��ͨ�ҵǼǲ����ȷ�������Ϣ")
        
        wtrbka_where_dict = {}
        wtrbka_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
            
        wtrbka_update_dict = {}
        wtrbka_update_dict = {'COTRCDAT':TradeContext.TRCDAT,'COTRCNO':TradeContext.TRCNO,'COMSGFLGNO':TradeContext.MSGFLGNO}
            
        ret = rccpsDBTrcc_wtrbka.update(wtrbka_update_dict,wtrbka_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow('S999',"����ͨ��ͨ�ҵǼǲ����ȷ�������Ϣ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ͨ��ͨ�ҵǼǲ����ȷ�������Ϣ")
        
        
        #����ҵ��״̬Ϊ�Զ����˴�����
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ�Զ����˴�����")
        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CONFACC,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ�Զ����˴������쳣')
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ�Զ����˴�����")
        
        #������������
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������")
        
        TradeContext.HostCode = '8813'                               #����8813�����ӿ�
        TradeContext.RCCSMCD  = PL_RCCSMCD_HDLZ                      #����ժҪ���룺�������
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #�跽�˻�:ũ��������������
        TradeContext.SBNM = "ũ��������������"
        TradeContext.RBAC = TradeContext.PYEACC                      #�����˻�:�տ����˻�
        TradeContext.RBNM = TradeContext.PYENAM                      #��������:�տ��˻���
        TradeContext.OCCAMT = str(TradeContext.OCCAMT)
        
        #=====add by pgt 12-5====
        TradeContext.CTFG = '7'                                      #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
        TradeContext.PKFG = 'T'                                      #ͨ��ͨ�ұ�ʶ                                   
        
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        
        AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo(">>>����������������")
        
        #��������������,����ҵ��״̬Ϊ�Զ����˳ɹ���ʧ��
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����ҵ��״̬Ϊ�Զ����˳ɹ���ʧ��")
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BJETIM']  = TradeContext.BJETIM
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['SBAC']    = TradeContext.SBAC
        stat_dict['ACNM']    = TradeContext.SBNM
        stat_dict['RBAC']    = TradeContext.RBAC
        stat_dict['OTNM']    = TradeContext.RBNM
        stat_dict['PRCCO']   = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("����������[" + TradeContext.errorCode + "],����������Ϣ[" + TradeContext.errorMsg +"]")
        if TradeContext.errorCode == '0000':
            #=====����ũ�����ɹ�,����״̬Ϊ�Զ����˳ɹ�====
            stat_dict['TRDT']    = TradeContext.TRDT
            stat_dict['TLSQ']    = TradeContext.TLSQ
            stat_dict['BCSTAT']  = PL_BCSTAT_AUTO
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            TradeContext.STRINFO = '�ɹ�'
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ�Զ����˳ɹ��쳣")
            
            AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ�Զ����˳ɹ����")
        else:
            #=====����ũ����ʧ��,����״̬Ϊ�Զ�����ʧ��====       
            stat_dict['BCSTAT']  = PL_BCSTAT_AUTO
            stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
            TradeContext.STRINFO = '�����Զ�����ʧ��'
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ�Զ�����ʧ���쳣")
            
            AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ�Զ�����ʧ�����")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    #Ϊ���ȷ��Ӧ���ĸ�ֵ
    TradeContext.sysType  = 'rccpst'
    TradeContext.MSGTYPCO = 'SET010'
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
    TradeContext.PRCCO    = 'RCCI0000'
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).���ȷ�������Ľ���[TRCC006_1143]�˳�***' )
    
    return True


#=====================���׺���===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).���ȷ�������Ľ���[TRCC006_1143]����***' )
    
    #����afe�������жϴ��ȷ��Ӧ�����Ƿ��ͳɹ�,����¼��־
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo(">>>���ȷ��Ӧ���ķ��ͳɹ�")
    else:
        AfaLoggerFunc.tradeInfo(">>>���ȷ��Ӧ���ķ���ʧ��,�ȴ��Է����������")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).���ȷ�������Ľ���[TRCC006_1143]�˳�***' )
    
    return True
        
