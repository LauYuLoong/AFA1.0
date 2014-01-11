# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).�۱�ת��Ӧ���Ľ���
#==============================================================================
#   �����ļ�:   TRCC006_1155.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر�� 
#   �޸�ʱ��:   2008-10-21
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsGetFunc,rccpsHostFunc,rccpsEntries
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_atcbka,rccpsDBTrcc_mpcbka


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo(" ũ����ϵͳ������.���������(1.���ز���).�۱�ת��Ӧ���Ľ���[TRCC006_1155]���� ")

    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)

    #=================��Ҫ�Լ��===============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")
    #=================�������ѱ����������,��ֹͣ����================================
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ���˽����Ƿ��ѱ�����")
    
    where_sql = "ORMFN = '" + TradeContext.ORMFN + "'"
    
    ret = rccpsDBTrcc_atcbka.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","��ѯ�����Ǽǲ��쳣,�˳�������")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��д��ڶԴ˽��׵ĳ���,�˳�������")
        
    AfaLoggerFunc.tradeInfo(">>>�������˽����Ƿ��ѱ�����")
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ���˽����Ƿ��ѱ�����")
    
    ret = rccpsDBTrcc_mpcbka.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","��ѯ�����Ǽǲ��쳣,�˳�������")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��д��ڶԴ˽��׵ĳ���,�˳�������")
        
    AfaLoggerFunc.tradeInfo(">>>�������˽����Ƿ��ѱ�����")
        
    AfaLoggerFunc.tradeInfo(">>>������Ҫ�Լ��")
    
    #=================ƥ��ԭ������Ϣ===========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼƥ��ԭ����")
    
    wtr_dict = {}
    
    if not rccpsDBFunc.getTransWtrAK(TradeContext.SNDBNKCO,TradeContext.TRCDAT,TradeContext.TRCNO,wtr_dict):
        return AfaFlowControl.ExitThisFlow('S999', "δ�ҵ�ԭ���������,ֹͣ����")
    
    TradeContext.BJEDTE  = wtr_dict['BJEDTE']
    TradeContext.BSPSQN  = wtr_dict['BSPSQN']
    TradeContext.TRCCO   = wtr_dict['TRCCO']
    TradeContext.BESBNO  = wtr_dict['BESBNO']
    TradeContext.BETELR  = wtr_dict['BETELR']
    TradeContext.OCCAMT  = str(wtr_dict['OCCAMT'])
    TradeContext.CHRGTYP = wtr_dict['CHRGTYP']
    TradeContext.LOCCUSCHRG = str(wtr_dict['CUSCHRG'])
    TradeContext.PYRTYP  = wtr_dict['PYRTYP']
    TradeContext.PYRACC  = wtr_dict['PYRACC']
    TradeContext.PYRNAM  = wtr_dict['PYRNAM']
    TradeContext.CERTTYPE = wtr_dict['CERTTYPE']
    TradeContext.CERTNO  = wtr_dict['CERTNO']
    TradeContext.TERMID  = wtr_dict['TERMID']
    TradeContext.WARNTNO = wtr_dict['BNKBKNO']
    
    AfaLoggerFunc.tradeInfo(">>>����ƥ��ԭ����")
    
    #=================��Ӧ���Ļظ��ܾ�,������״̬Ϊ�ܾ�,ֹͣ����=============
    if TradeContext.PRCCO != 'RCCI0000':
        AfaLoggerFunc.tradeInfo(">>>�Է����ؾܾ�Ӧ��")
        #=============����ҵ��״̬Ϊ�ܾ�������=================================
        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�ܾ��������쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
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
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
        #=============��������Ĩ��=============================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬ΪĨ�˴�����")
        
        
        #=====���⴦��  �ر�� 20081127 ��8813Ĩ��,������µ�ǰ����ˮ�Ž��м���====
        if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
            return AfaFlowControl.ExisThisFlow('S999',"�����µ�ǰ����ˮ���쳣")
              
        
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
        entries_dict['RCCSMCD']  = PL_RCCSMCD_CZ
        TradeContext.BRSFLG      = PL_BRSFLG_SND
        
        rccpsEntries.KZBZYWZMZ(entries_dict)
          
        #====����ҵ��״̬ΪĨ�˴�����====        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ΪĨ�˴������쳣')
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬ΪĨ�˴�����")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
        #====�Զ�Ĩ��====
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������Ĩ��")
        
        #=====����Ĩ�������ӿ�====
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo(">>>������������Ĩ��")
        
        stat_dict = {}
        
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['MGID']    = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        if TradeContext.errorCode == '0000':
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
            AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬ΪĨ��ʧ��")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ĩ�˳ɹ��쳣')
            
            AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬ΪĨ��ʧ��")
            
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
        return AfaFlowControl.ExitThisFlow("S999","�Է��ܾ�,ֹͣ����")
    
    else:
        AfaLoggerFunc.tradeInfo(">>>�Է����سɹ�Ӧ��")

    #=================����ҵ��״̬Ϊȷ�ϸ������=============================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊȷ�ϸ������")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CONFPAY,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊȷ�ϸ�������쳣")
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊȷ�ϸ������")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    #=================���´��ȷ��ί�����ںͽ�����ˮ��=========================
    AfaLoggerFunc.tradeInfo(">>>��ʼ���´��ȷ��ί�����ںͽ�����ˮ��")
    
    wtrbka_update_dict = {}
    wtrbka_update_dict['COTRCDAT'] = TradeContext.TRCDAT
    wtrbka_update_dict['COTRCNO']  = TradeContext.SerialNo
    wtrbka_update_dict['COMSGFLGNO'] = TradeContext.RCVMBRCO + TradeContext.TRCDAT + TradeContext.SerialNo
    
    wtrbka_where_dict = {}
    wtrbka_where_dict['BJEDTE'] = TradeContext.BJEDTE
    wtrbka_where_dict['BSPSQN'] = TradeContext.BSPSQN
    
    ret = rccpsDBTrcc_wtrbka.update(wtrbka_update_dict,wtrbka_where_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999', "���´��ȷ��ί�����ںͽ�����ˮ���쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�������´��ȷ��ί�����ںͽ�����ˮ��")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    #=================Ϊ���ȷ����������׼��=================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ���ȷ����������׼��")
    
    TradeContext.MSGTYPCO = 'SET009'
    TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO
    TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    #TradeContext.SNDTRDAT = TradeContext.BJEDTE
    #TradeContext.SNDTRTIM = TradeContext.BJETIM
    #TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = TradeContext.ORMFN
    TradeContext.OPRTYPNO = '30'
    TradeContext.ROPRTPNO = '30'
    TradeContext.TRANTYP  = '0'
    
    TradeContext.ORTRCCO  = TradeContext.TRCCO
    TradeContext.ORTRCNO  = TradeContext.TRCNO
    TradeContext.TRCCO    = '3000503'
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.CURPIN   = ""
    TradeContext.STRINFO  = '�յ����Ӧ��,�Զ����ʹ��ȷ��'
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ���ȷ����������׼��")
    
    AfaLoggerFunc.tradeInfo(" ũ����ϵͳ������.���������(1.���ز���).����ת��Ӧ���Ľ���[TRCC006_1155]�˳� ")
    return True


#=====================���׺���===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo(" ũ����ϵͳ������.���������(2.���Ļ�ִ).����ת��Ӧ���Ľ���[TRCC006_1155]���� ")

    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['BCSTAT']  = PL_BCSTAT_CONFPAY
    stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
    stat_dict['PRCCO']   = TradeContext.errorCode
    stat_dict['STRINFO'] = TradeContext.errorMsg
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        #=====����ũ�����ɹ�,����״̬Ϊȷ�ϸ���ɹ�====
        stat_dict['BCSTAT']  = PL_BCSTAT_CONFPAY
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊȷ�ϸ���ɹ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊȷ�ϸ���ɹ�")
    else:
        #=====����ũ����ʧ��,����״̬Ϊȷ�ϸ���ʧ��====       
        stat_dict['BCSTAT']  = PL_BCSTAT_CONFPAY
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊȷ�ϸ���ʧ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊȷ�ϸ���ʧ��")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    AfaLoggerFunc.tradeInfo(" ũ����ϵͳ������.���������(2.���Ļ�ִ).����ת��Ӧ���Ľ���[TRCC006_1155]�˳� ")
    
    return True
        
