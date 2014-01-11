# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨ��ͨ��ҵ���ִ���Ľ���
#==============================================================================
#   �����ļ�:   TRCC004_1147.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-10-22
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsGetFunc,rccpsEntries
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_balbka,rccpsDBTrcc_atcbka,rccpsDBTrcc_mpcbka


#=====================��ִ���Ի�����(���ز���)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨ��ͨ��ҵ���ִ���Ľ���[TRC004_1147]����***' )
    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #=================ƥ��ԭ������Ϣ===========================================
    wtrbka_where_dict = {}
    wtrbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
    
    wtrbka_dict = {}
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
    if wtrbka_dict == None:
        return AfaFlowControl.ExitThisFlow('S999', "��ѯͨ��ͨ��ҵ����Ϣ�Ǽǲ��쳣")
    
    if len(wtrbka_dict) > 0:
        TradeContext.BJEDTE  = wtrbka_dict['BJEDTE']
        TradeContext.BSPSQN  = wtrbka_dict['BSPSQN']
        TradeContext.TRCCO   = wtrbka_dict['TRCCO']
        TradeContext.BESBNO  = wtrbka_dict['BESBNO']
        TradeContext.BETELR  = wtrbka_dict['BETELR']
        TradeContext.OCCAMT  = str(wtrbka_dict['OCCAMT'])
        TradeContext.CHRGTYP = wtrbka_dict['CHRGTYP']
        TradeContext.LOCCUSCHRG = str(wtrbka_dict['CUSCHRG'])
        TradeContext.PYETYP  = wtrbka_dict['PYETYP']
        TradeContext.PYEACC  = wtrbka_dict['PYEACC']
        TradeContext.PYENAM  = wtrbka_dict['PYENAM']
        TradeContext.PYRTYP  = wtrbka_dict['PYRTYP']
        TradeContext.PYRACC  = wtrbka_dict['PYRACC']
        TradeContext.PYRNAM  = wtrbka_dict['PYRNAM']
        TradeContext.CERTTYPE = wtrbka_dict['CERTTYPE']
        TradeContext.CERTNO  = wtrbka_dict['CERTNO']
        TradeContext.TERMID  = wtrbka_dict['TERMID']
        TradeContext.WARNTNO = wtrbka_dict['BNKBKNO']
        
        #============����ԭ����״̬Ϊ�ܾ�======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����ҵ��״̬Ϊ�ܾ�������")
        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�ܾ��������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ԭ����ҵ��״̬Ϊ�ܾ�������")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����ҵ��״̬Ϊ�ܾ��ɹ�")
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRCCO']   = TradeContext.PRCCO
        stat_dict['STRINFO'] = TradeContext.STRINFO
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ�ܾ��ɹ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ԭ����ҵ��״̬Ϊ�ܾ��ɹ�")
        
    else:
        AfaLoggerFunc.tradeInfo(">>>ͨ��ͨ��ҵ��Ǽǲ���δ�ҵ�ԭ��������Ϣ,��ʼ��ѯԭ���ȷ����Ϣ")
        wtrbka_where_dict = {}
        wtrbka_where_dict['COMSGFLGNO'] = TradeContext.ORMFN
        
        wtrbka_dict = {}
        wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
        
        if wtrbka_dict == None:
            return AfaFlowControl.ExitThisFlow('S999', "��ѯͨ��ͨ��ҵ����Ϣ�Ǽǲ��쳣")
        
        if len(wtrbka_dict) > 0:
            TradeContext.BJEDTE  = wtrbka_dict['BJEDTE']
            TradeContext.BSPSQN  = wtrbka_dict['BSPSQN']
            TradeContext.TRCCO   = wtrbka_dict['TRCCO']
            TradeContext.BESBNO  = wtrbka_dict['BESBNO']
            TradeContext.BETELR  = wtrbka_dict['BETELR']
            TradeContext.OCCAMT  = str(wtrbka_dict['OCCAMT'])
            TradeContext.CHRGTYP = wtrbka_dict['CHRGTYP']
            TradeContext.LOCCUSCHRG = str(wtrbka_dict['CUSCHRG'])
            TradeContext.PYETYP  = wtrbka_dict['PYETYP']
            TradeContext.PYEACC  = wtrbka_dict['PYEACC']
            TradeContext.PYENAM  = wtrbka_dict['PYENAM']
            TradeContext.PYRTYP  = wtrbka_dict['PYRTYP']
            TradeContext.PYRACC  = wtrbka_dict['PYRACC']
            TradeContext.PYRNAM  = wtrbka_dict['PYRNAM']
            TradeContext.CERTTYPE = wtrbka_dict['CERTTYPE']
            TradeContext.CERTNO  = wtrbka_dict['CERTNO']
            TradeContext.TERMID  = wtrbka_dict['TERMID']
            TradeContext.WARNTNO = wtrbka_dict['BNKBKNO']
            
            #============����ԭ����״̬Ϊ�ܾ�======================================
            AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����ҵ��״̬Ϊ�ܾ�������")
            
            if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�ܾ��������쳣")
            
            AfaLoggerFunc.tradeInfo(">>>��������ԭ����ҵ��״̬Ϊ�ܾ�������")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����ҵ��״̬Ϊ�ܾ��ɹ�")
            
            stat_dict = {}
            stat_dict['BJEDTE']  = TradeContext.BJEDTE
            stat_dict['BSPSQN']  = TradeContext.BSPSQN
            stat_dict['BESBNO']  = TradeContext.BESBNO
            stat_dict['BETELR']  = TradeContext.BETELR
            stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            stat_dict['PRCCO']   = TradeContext.PRCCO
            stat_dict['STRINFO'] = TradeContext.STRINFO
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ�ܾ��ɹ��쳣")
            
            AfaLoggerFunc.tradeInfo(">>>��������ԭ����ҵ��״̬Ϊ�ܾ��ɹ�")
            
        else:
            AfaLoggerFunc.tradeInfo(">>>ͨ��ͨ��ҵ��Ǽǲ���δ�ҵ�ԭ���ȷ����Ϣ,��ʼ��ѯ����ѯ�Ǽǲ�")
            balbka_where_dict = {}
            balbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
            
            balbka_dict = {}
            balbka_dict = rccpsDBTrcc_balbka.selectu(balbka_where_dict)
            
            if balbka_dict == None:
                return AfaFlowControl.ExitThisFlow('S999', "��ѯ����ѯ�Ǽǲ��쳣")
                
            if len(balbka_dict) > 0:
                TradeContext.TRCCO = balbka_dict['TRCCO']
                
                #=====����ԭ����ѯ���׷�����=================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����ѯ���׷�����")
                
                balbka_update_dict = {}
                balbka_update_dict['PRCCO']   = TradeContext.PRCCO
                balbka_update_dict['STRINFO'] = TradeContext.STRINFO
                
                ret = rccpsDBTrcc_balbka.update(balbka_update_dict,balbka_where_dict)
                
                if ret <= 0:
                    return AfaFlowControl.ExitThisFlow('S999', "����ԭ����ѯ���׷������쳣")
                
                AfaLoggerFunc.tradeInfo(">>>��������ԭ����ѯ���׷�����")
            else:
                AfaLoggerFunc.tradeInfo(">>>����ѯ�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ�Զ������Ǽǲ�")
                atcbka_where_dict = {}
                atcbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
                
                atcbka_dict = {}
                atcbka_dict = rccpsDBTrcc_atcbka.selectu(atcbka_where_dict)
                
                if atcbka_dict == None:
                    return AfaFlowControl.ExitThisFlow('S999', "��ѯ�Զ������Ǽǲ��쳣")
                    
                if len(atcbka_dict) > 0:
                    TradeContext.BOJEDT = atcbka_dict['BOJEDT']
                    TradeContext.BOSPSQ = atcbka_dict['BOSPSQ']
                    TradeContext.TRCCO  = atcbka_dict['TRCCO']
                    
                    #====�����Զ��������׷�����================================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ�Զ��������׷�����")
                    
                    atcbka_update_dict = {}
                    atcbka_update_dict['PRCCO']   = TradeContext.PRCCO
                    atcbka_update_dict['STRINFO'] = TradeContext.STRINFO
                    
                    ret = rccpsDBTrcc_atcbka.update(atcbka_update_dict,atcbka_where_dict)
                    
                    if ret<= 0:
                        return AfaFlowControl.ExitThisFlow('S999', "����ԭ�������׷������쳣")
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ�Զ��������׷�����")
                    
                    #====����ԭ����������ҵ��״̬Ϊ����ʧ��================
                    #AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����������ҵ��״̬Ϊ����ʧ��")
                    #
                    #stat_dict = {}
                    #stat_dict['BJEDTE']  = TradeContext.BOJEDT
                    #stat_dict['BSPSQN']  = TradeContext.BOSPSQ
                    #stat_dict['BCSTAT']  = PL_BCSTAT_CANC
                    #stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
                    #stat_dict['PRCCO']   = TradeContext.PRCCO
                    #stat_dict['STRINFO'] = TradeContext.STRINFO
                    #
                    #if not rccpsState.setTransState(stat_dict):
                    #    return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
                    #
                    #AfaLoggerFunc.tradeInfo(">>>��������ԭ����������ҵ��״̬Ϊ����ʧ��")
                else:
                    AfaLoggerFunc.tradeInfo(">>>�Զ������Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ��������Ǽǲ�")
                    mpcbka_where_dict = {}
                    mpcbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
                    
                    mpcbka_dict = {}
                    mpcbka_dict = rccpsDBTrcc_mpcbka.selectu(mpcbka_where_dict)
                    
                    if mpcbka_dict == None:
                        return AfaFlowControl.ExitThisFlow('S999', "��ѯ��������Ǽǲ��쳣")
                        
                    if len(mpcbka_dict) > 0:
                        TradeContext.BOJEDT  = mpcbka_dict['BOJEDT']
                        TradeContext.BOSPSQ  = mpcbka_dict['BOSPSQ']
                        TradeContext.TRCCO   = mpcbka_dict['TRCCO']
                        TradeContext.ORTRCCO = mpcbka_dict['ORTRCCO']
                        TradeContext.BESBNO  = mpcbka_dict['BESBNO']
                        TradeContext.BETELR  = mpcbka_dict['BETELR']
                        TradeContext.TERMID  = mpcbka_dict['TERMID']
                        
                        #====���¹�̨�������׷�����================================
                        AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ��̨�������׷�����")
                        
                        mpcbka_update_dict = {}
                        mpcbka_update_dict['PRCCO']   = TradeContext.PRCCO
                        mpcbka_update_dict['STRINFO'] = TradeContext.STRINFO
                        
                        ret = rccpsDBTrcc_mpcbka.update(mpcbka_update_dict,mpcbka_where_dict)
                        
                        if ret <=0:
                            return AfaFlowControl.ExitThisFlow('S999', "����ԭ����������׷������쳣")
                            
                        AfaLoggerFunc.tradeInfo(">>>��������ԭ����������׷�����")
                        
                        #====����ԭ����������ҵ��״̬Ϊ����ʧ��================
                        #AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����������ҵ��״̬Ϊ����������")
                        #
                        #if not rccpsState.newTransState(TradeContext.BOJEDT,TradeContext.BOSPSQ,PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
                        #    return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
                        #
                        #AfaLoggerFunc.tradeInfo(">>>��������ԭ����������ҵ��״̬Ϊ����������")
                        #
                        #if not AfaDBFunc.CommitSql( ):
                        #    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        #    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                        #AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                        #
                        #AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����������ҵ��״̬Ϊ����ʧ��")
                        #
                        #stat_dict = {}
                        #
                        #stat_dict['BJEDTE']  = TradeContext.BJEDTE
                        #stat_dict['BSPSQN']  = TradeContext.BSPSQN
                        #stat_dict['PRCCO']   = TradeContext.PRCCO
                        #stat_dict['STRINFO'] = TradeContext.STRINFO
                        #stat_dict['BCSTAT']  = PL_BCSTAT_CANC
                        #stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
                        #
                        #AfaLoggerFunc.tradeInfo(">>>��������ԭ����������ҵ��״̬Ϊ����ʧ��")
                    
                    else:
                        return AfaFlowControl.ExitThisFlow('S999', "δ�ҵ�ԭ������Ϣ,��������")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    #=================��ԭ����Ϊͨ�潻��,��ʼ�Զ�Ĩ��==========================
    if TradeContext.TRCCO == '3000002' or TradeContext.TRCCO == '3000003' or TradeContext.TRCCO == '3000004' or TradeContext.TRCCO == '3000005':
        
        #=====���⴦��  �ر�� 20081127 ��8813Ĩ��,������µ�ǰ����ˮ�Ž��м���====
        if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
            return AfaFlowControl.ExisThisFlow('S999',"�����µ�ǰ����ˮ���쳣")
        else:
            AfaLoggerFunc.tradeInfo(">>>�ɹ������µ�ǰ����ˮ��")
        
        #ΪĨ�˸�ֵ��Ʒ�¼
        entries_dict = {}
        entries_dict['FEDT']     = TradeContext.BJEDTE
        entries_dict['RBSQ']     = TradeContext.BSPSQN
        entries_dict['PYRACC']   = TradeContext.PYRACC
        entries_dict['PYRNAM']   = TradeContext.PYRNAM
        entries_dict['PYEACC']   = TradeContext.PYEACC
        entries_dict['PYENAM']   = TradeContext.PYENAM
        entries_dict['OCCAMT']   = TradeContext.OCCAMT
        entries_dict['CHRGTYP']  = TradeContext.CHRGTYP
        entries_dict['CUSCHRG']  = TradeContext.LOCCUSCHRG
        entries_dict['RCCSMCD']  = PL_RCCSMCD_CX
        TradeContext.BRSFLG      = PL_BRSFLG_SND
        
        if TradeContext.TRCCO == '3000002' or TradeContext.TRCCO == '3000004':
            rccpsEntries.KZTCWZMZ(entries_dict)
        
        if TradeContext.TRCCO == '3000003' or TradeContext.TRCCO == '3000005':
            rccpsEntries.KZBZYWZMZ(entries_dict)
        
        #=============����ԭ����ҵ��״̬ΪĨ�˴�����===========================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����ҵ��״̬ΪĨ�˴�����")
        
        #====����ҵ��״̬ΪĨ�˴�����====
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ΪĨ�˴������쳣')
        
        AfaLoggerFunc.tradeInfo(">>>��������ԭ����ҵ��״̬ΪĨ�˴�����")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
        #=============��ʼ��������Ĩ��=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����Ĩ��")
        
        #=====����Ĩ�������ӿ�====
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo(">>>��������Ĩ��")
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        
        stat_dict = {}
        
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['MGID']    = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        if TradeContext.errorCode == '0000':
            #=========����ԭ����ҵ��״̬ΪĨ�˳ɹ�=============================
            AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬ΪĨ�˳ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            stat_dict['TRDT']   = TradeContext.TRDT
            stat_dict['TLSQ']   = TradeContext.TLSQ
            stat_dict['PRTCNT'] = 1
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ĩ�˳ɹ��쳣')
            
            AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬ΪĨ�˳ɹ�")
        
        else:
            #=========����ԭ����ҵ��״̬ΪĨ��ʧ��=============================
            AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬ΪĨ��ʧ��")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ĩ�˳ɹ��쳣')
            
            AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬ΪĨ��ʧ��")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨ��ͨ��ҵ���ִ���Ľ���[TRC004_1147]�˳�***' )
    
    return True
