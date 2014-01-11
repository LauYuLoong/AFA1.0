# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.��ִ�����(1.��ִ����).�Զ�����Ӧ���Ľ���
#==============================================================================
#   �����ļ�:   TRCC004_1161.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-12-04
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsState,rccpsGetFunc,rccpsHostFunc,rccpsDBFunc,rccpsEntries
import rccpsDBTrcc_mpcbka,rccpsDBTrcc_atcbka


#=====================��ִ���Ի�����(���ز���)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨ��ͨ�ҳ���Ӧ���Ľ���[TRC004_1161]����***' )
    
    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #��ѯԭ����������Ϣ
    atcbka_dict = {}
    
    atcbka_where_dict = {}
    atcbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
    
    atcbka_dict = rccpsDBTrcc_atcbka.selectu(atcbka_where_dict)
    
    if atcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","��ѯԭ����������Ϣ�쳣")
        
    if len(atcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow("S999","δ�ҵ�ԭ����������Ϣ,��������")
        
    #��ѯԭ�����������Ƿ��ѿ�ʼ������
    mpcbka_dict = {}
    
    mpcbka_where_dict = {}
    mpcbka_where_dict['ORMFN'] = atcbka_dict['ORMFN']
    
    mpcbka_dict = rccpsDBTrcc_mpcbka.selectu(mpcbka_where_dict)
    
    if mpcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","��ѯԭ����������Ϣ�쳣")
        
    if len(mpcbka_dict) > 0:
        return AfaFlowControl.ExitThisFlow("S999","ԭ�����ѿ�ʼ����,ֹͣ��������Ӧ��")
        
    #=====�������ź͹�Ա�Ÿ�ֵ====
    TradeContext.BETELR = atcbka_dict['BETELR']
    TradeContext.BESBNO = atcbka_dict['BESBNO']
    
    #���³����Ǽǲ����ķ�����Ϣ
    AfaLoggerFunc.tradeInfo(">>>��ʼ���³����Ǽǲ����ķ�����Ϣ")
    
    atcbka_update_dict = {}
    atcbka_update_dict['PRCCO'] = TradeContext.PRCCO
    atcbka_update_dict['STRINFO'] = TradeContext.STRINFO
    
    ret = rccpsDBTrcc_atcbka.update(atcbka_update_dict,atcbka_where_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","���³����Ǽǲ��쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�������³����Ǽǲ����ķ�����Ϣ")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    if atcbka_dict['ORTRCCO'] != '3000504':
        AfaLoggerFunc.tradeInfo(">>>ԭ����������Ϊͨ���ͨ�������ཻ��")
        
        #��ѯԭ������������Ϣ
        wtr_dict = {}
        
        if not rccpsDBFunc.getTransWtr(atcbka_dict['BOJEDT'],atcbka_dict['BOSPSQ'],wtr_dict):
            return AfaFlowControl.ExitThisFlow("S999","��ѯԭ������������Ϣ�쳣")
        
        #���ԭ���������׵�ǰ״̬��Ϊ����,��ʾ���յ�����Ӧ��,ֹͣ����
        if wtr_dict['BCSTAT'] == PL_BCSTAT_CANCEL:
            return AfaFlowControl.ExitThisFlow("S999","���յ�����Ӧ��,��������")
        
        TradeContext.TERMID = wtr_dict['TERMID']
        TradeContext.BRSFLG = wtr_dict['BRSFLG']
        
        
        
        #��ԭ����������Ϊͨ���ཻ��,ӦĨ��
        if wtr_dict['TRCCO'] in ('3000002','3000003','3000004','3000005'):
            
            AfaLoggerFunc.tradeInfo(">>>��ʼ��������Ĩ��")
            
            #ΪĨ�˸�ֵ��Ʒ�¼
            entries_dict = {}
            entries_dict['FEDT']     = wtr_dict['BJEDTE']
            entries_dict['RBSQ']     = wtr_dict['BSPSQN']
            entries_dict['PYRACC']   = wtr_dict['PYRACC']
            entries_dict['PYRNAM']   = wtr_dict['PYRNAM']
            entries_dict['PYEACC']   = wtr_dict['PYEACC']
            entries_dict['PYENAM']   = wtr_dict['PYENAM']
            entries_dict['OCCAMT']   = wtr_dict['OCCAMT']
            entries_dict['CHRGTYP']  = wtr_dict['CHRGTYP']
            entries_dict['CUSCHRG']  = wtr_dict['CUSCHRG']
            entries_dict['RCCSMCD']  = PL_RCCSMCD_CX
            TradeContext.BRSFLG      = wtr_dict['BRSFLG']
            
            if TradeContext.ORTRCCO == '3000002' or TradeContext.ORTRCCO == '3000004':
                rccpsEntries.KZTCWZMZ(entries_dict)
            
            if TradeContext.ORTRCCO == '3000003' or TradeContext.ORTRCCO == '3000005':
                rccpsEntries.KZBZYWZMZ(entries_dict)
                
            #=====�����µ�ǰ�����ں�ǰ����ˮ��====
            if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
                return AfaFlowControl.ExisThisFlow('S999',"�����µ�ǰ����ˮ���쳣")
            
            #����ԭ����״̬Ϊ����������
            AfaLoggerFunc.tradeInfo('>>>��ʼ����ԭ����״̬Ϊ����������')
                
            if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�����������쳣")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
            AfaLoggerFunc.tradeInfo('>>>��������ԭ����״̬Ϊ����������')
            
            #=====���������ӿ�=====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            AfaLoggerFunc.tradeInfo(">>>����������������")
            
        else:
            AfaLoggerFunc.tradeInfo(">>>ԭ����δ����,������Ĩ��")
            
            #����ԭ����״̬Ϊ����������
            AfaLoggerFunc.tradeInfo('>>>��ʼ����ԭ����״̬Ϊ����������')
                
            if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�����������쳣")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
            AfaLoggerFunc.tradeInfo('>>>��������ԭ����״̬Ϊ����������')
            
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg  = "����ǰδ����,������Ĩ��"
           
        #��������������Ϣ,���ý���״̬ 
        stat_dict = {}
        
        stat_dict['BJEDTE']  = wtr_dict['BJEDTE']
        stat_dict['BSPSQN']  = wtr_dict['BSPSQN']
        stat_dict['MGID']    = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        if TradeContext.errorCode == '0000':
            #����ԭ����״̬Ϊ�����ɹ�
            AfaLoggerFunc.tradeInfo("<<<<<<<��ʼ����ԭ����״̬Ϊ�����ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_CANCEL
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            if TradeContext.existVariable('TRDT'):
                stat_dict['TRDT']   = TradeContext.TRDT
            if TradeContext.existVariable('TLSQ'):
                stat_dict['TLSQ']   = TradeContext.TLSQ
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ�����ɹ��쳣')
            
            AfaLoggerFunc.tradeInfo("<<<<<<<��������ԭ����״̬Ϊ�����ɹ�")
        else:
            #����ԭ����״̬Ϊ����ʧ��
            AfaLoggerFunc.tradeInfo("<<<<<<<��ʼ����ԭ����״̬Ϊ����ʧ��")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_CANCEL
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ����ʧ���쳣')
            
            AfaLoggerFunc.tradeInfo("<<<<<<<��������ԭ����״̬Ϊ�����ɹ�")
            
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
    else:
        AfaLoggerFunc.tradeInfo(">>>ԭ����������Ϊ��������")
        
        #��ѯԭ����������ϸ��Ϣ
        AfaLoggerFunc.tradeInfo(">>>�������ױ�������[" + atcbka_dict['BOJEDT'] + "]�������[" + atcbka_dict['BOSPSQ'] + "]")
        
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ����������ϸ��Ϣ")
        
        mpc_dict = {}
        
        if not rccpsDBFunc.getTransMpc(atcbka_dict['BOJEDT'],atcbka_dict['BOSPSQ'],mpc_dict):
            return AfaFlowControl.ExitThisFlow("S999","��ѯԭ����������ϸ��Ϣ�쳣")
            
        AfaLoggerFunc.tradeInfo(">>>������ѯԭ����������ϸ��Ϣ")
        
        #��ѯԭ������������ϸ��Ϣ
        AfaLoggerFunc.tradeInfo(">>>���������ױ�������[" + mpc_dict['BOJEDT'] + "]�������[" + mpc_dict['BOSPSQ'] + "]")
        
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ������������ϸ��Ϣ")
        
        wtr_dict = {}
        
        if not rccpsDBFunc.getTransWtr(mpc_dict['BOJEDT'],mpc_dict['BOSPSQ'],wtr_dict):
            return AfaFlowControl.ExitThisFlow("S999","��ѯԭ������������ϸ��Ϣ�쳣")
            
        AfaLoggerFunc.tradeInfo(">>>������ѯԭ������������ϸ��Ϣ")
        
        #���³����Ǽǲ�
        AfaLoggerFunc.tradeInfo(">>>��ʼ���³����Ǽǲ�")
        
        mpcbka_update_dict = {}
        mpcbka_update_dict['PRCCO'] = "RCCI1000"
        mpcbka_update_dict['STRINFO'] = "�������ױ��ɹ�����"
        
        mpcbka_where_dict = {}
        mpcbka_where_dict['BJEDTE'] = mpc_dict['BJEDTE']
        mpcbka_where_dict['BSPSQN'] = mpc_dict['BSPSQN']
        
        ret = rccpsDBTrcc_mpcbka.update(mpcbka_update_dict,mpcbka_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("���³����Ǽǲ�������ͷ�����Ϣ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�������³����Ǽǲ�")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨ��ͨ�ҳ���Ӧ���Ľ���[TRC004_1161]�˳�***' )
    
    return True
