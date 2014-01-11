# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨ��ͨ�ҳ���Ӧ���Ľ���
#=================================================================
#   �����ļ�:   TRCC004_1162.py
#   �޸�ʱ��:   2008-12-01
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,AfaDBFunc
from types import *
from rccpsConst import *
import rccpsState,rccpsGetFunc,rccpsHostFunc,rccpsDBFunc,rccpsEntries
import rccpsDBTrcc_mpcbka,rccpsDBTrcc_atcbka

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨ��ͨ�ҳ���Ӧ���Ľ���[TRC004_1162]����***' )
    
    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #��ѯ�����Ǽǲ����Ƿ��жԴ˳������׵ĳ���
    AfaLoggerFunc.tradeInfo(">>>��ʼ���˳��������Ƿ��ѱ�����")
    
    where_sql = "ORMFN = '" + TradeContext.ORMFN + "'"
    
    ret = rccpsDBTrcc_atcbka.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","��ѯ�����Ǽǲ��쳣,�˳�������")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","�����Ǽǲ��д��ڶԴ˳������׵ĳ���,�˳�������")
        
    AfaLoggerFunc.tradeInfo(">>>�������˳��������Ƿ��ѱ�����")
    
    #=====���Ĺ�Ա�źͻ�����Ϊ�����Ա�š����������====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ���Ĺ�Ա�ţ�������")
    
    #=====���ҳ������׵���Ϣ=====
    mpcbka_where_dict = {}
    mpcbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
    
    mpcbka_record = rccpsDBTrcc_mpcbka.selectu(mpcbka_where_dict)
    
    if(mpcbka_record == None):
        return AfaFlowControl.ExitThisFlow("S999","��ѯԭ����������Ϣ�쳣")
        
    if(len(mpcbka_record) <= 0):
        return AfaFlowControl.ExitThisFlow("S999","δ�ҵ�ԭ����������Ϣ,��������")
        
    #=====�������ź͹�Ա�Ÿ�ֵ====
    TradeContext.BETELR = mpcbka_record['BETELR']
    TradeContext.BESBNO = mpcbka_record['BESBNO']
    
    AfaLoggerFunc.tradeInfo("<<<<<<���Ĺ�Ա�ţ������Ž���")
    
        
    #���³����Ǽǲ����ķ�����Ϣ
    AfaLoggerFunc.tradeInfo(">>>��ʼ���³����Ǽǲ����ķ�����Ϣ")
    
    mpcbka_update_dict = {}
    mpcbka_update_dict['PRCCO'] = TradeContext.PRCCO
    mpcbka_update_dict['STRINFO'] = TradeContext.STRINFO
    
    ret = rccpsDBTrcc_mpcbka.update(mpcbka_update_dict,mpcbka_where_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","���³����Ǽǲ��쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�������³����Ǽǲ����ķ�����Ϣ")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    #=====��ѯ������������Ϣ====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ��ѯ�������Ľ��׵���Ϣ")
    
    wtrbka_record = {}
    
    if not rccpsDBFunc.getTransWtr(mpcbka_record['BOJEDT'],mpcbka_record['BOSPSQ'],wtrbka_record):
        return AfaFlowControl.ExitThisFlow("S999","��ѯ������ԭ������ϸ��Ϣ�쳣")
        
    AfaLoggerFunc.tradeInfo("<<<<<<������ѯ�������Ľ��׵���Ϣ")
    
    #====Ϊ�ն˺ź�������ʶ��ֵ====
    TradeContext.TERMID = wtrbka_record['TERMID']
    TradeContext.BRSFLG = wtrbka_record['BRSFLG']
    
    #=====�ж϶Է��г����Ƿ�ɹ�=====
    AfaLoggerFunc.tradeInfo("<<<<<<�ж϶Է��г����Ƿ�ɹ�PRCCO=[" + TradeContext.PRCCO + "]")
    if(TradeContext.PRCCO == 'RCCI0000' or TradeContext.PRCCO == 'RCCO1106'):
        AfaLoggerFunc.tradeInfo("<<<<<<�Է��г����ɹ�")
        
        #=====������������====
        AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������������")
        
        #=====ȡ���һ�����˳ɹ�״̬��ǰ�����ں�ǰ����ˮ��====
        stat_list = []
        
        if rccpsState.getTransStateSetm(wtrbka_record['BJEDTE'],wtrbka_record['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,stat_list):
            
            entries_dict = {}
            entries_dict['FEDT']     = stat_list[0]['FEDT']
            entries_dict['RBSQ']     = stat_list[0]['RBSQ']
            entries_dict['PYRACC']   = wtrbka_record['PYRACC']
            entries_dict['PYRNAM']   = wtrbka_record['PYRNAM']
            entries_dict['PYEACC']   = wtrbka_record['PYEACC']
            entries_dict['PYENAM']   = wtrbka_record['PYENAM']
            entries_dict['OCCAMT']   = wtrbka_record['OCCAMT']
            entries_dict['CHRGTYP']  = wtrbka_record['CHRGTYP']
            entries_dict['CUSCHRG']  = wtrbka_record['CUSCHRG']
            entries_dict['RCCSMCD']  = PL_RCCSMCD_CX
            TradeContext.BRSFLG      = wtrbka_record['BRSFLG']
            
            #����ͨ������Ĩ�˻�Ʒ�¼��ֵ
            if wtrbka_record['TRCCO'] == '3000002' or wtrbka_record['TRCCO'] == '3000004':
                rccpsEntries.KZTCWZMZ(entries_dict)
            
            #���۱�ת������Ĩ�˻�Ʒ�¼��ֵ
            if wtrbka_record['TRCCO'] == '3000003' or wtrbka_record['TRCCO'] == '3000005':
                rccpsEntries.KZBZYWZMZ(entries_dict)
                
            #����ͨ������Ĩ�˻�Ʒ�¼��ֵ
            if wtrbka_record['TRCCO'] == '3000102' or wtrbka_record['TRCCO'] == '3000104':
                rccpsEntries.KZTDWZMZ(entries_dict)
            
            #������ת������Ĩ�˻�Ʒ�¼��ֵ
            if wtrbka_record['TRCCO'] == '3000103' or wtrbka_record['TRCCO'] == '3000105':
                rccpsEntries.KZYZBWZMZ(entries_dict)
            
            
            #=====�����µ�ǰ�����ں�ǰ����ˮ��,���Ҹ��µ����ݿ���====
            if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
                return AfaFlowControl.ExisThisFlow('S999',"�����µ�ǰ����ˮ���쳣")
            
            #����ԭ����״̬Ϊ����������
            AfaLoggerFunc.tradeInfo('>>>��ʼ����ԭ����״̬Ϊ����������')
            if not rccpsState.newTransState(mpcbka_record['BOJEDT'],mpcbka_record['BOSPSQ'],PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�����������쳣")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                
            AfaLoggerFunc.tradeInfo('>>>��������ԭ����״̬Ϊ����������')
            
            #=====���������ӿں���=====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            AfaLoggerFunc.tradeInfo("<<<<<<��������Ĩ�˽���")
            
        else:
            AfaLoggerFunc.tradeInfo(">>>ԭ����δ����,������Ĩ��")
            
            #����ԭ����״̬Ϊ����������
            AfaLoggerFunc.tradeInfo('>>>��ʼ����ԭ����״̬Ϊ����������')
            if not rccpsState.newTransState(mpcbka_record['BOJEDT'],mpcbka_record['BOSPSQ'],PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�����������쳣")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                
            AfaLoggerFunc.tradeInfo('>>>��������ԭ����״̬Ϊ����������')
            
            TradeContext.errorCode = '0000'
            TradeContext.errorMsg  = 'ԭ����δ����,������Ĩ��'
            
            
        #��������������Ϣ,���ý���״̬
        
        stat_dict = {}
        stat_dict['BJEDTE'] = wtrbka_record['BJEDTE']
        stat_dict['BSPSQN'] = wtrbka_record['BSPSQN']
        stat_dict['MGID']   = TradeContext.errorCode
        stat_dict['STRINFO']= TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        if(TradeContext.errorCode == '0000'):
            #=====����ԭ����״̬Ϊ�����ɹ�====
            AfaLoggerFunc.tradeInfo("<<<<<<<��ʼ����ԭ����״̬Ϊ�����ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_CANC
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            if TradeContext.existVariable('TRDT'):
                stat_dict['TRDT']   = TradeContext.TRDT
            if TradeContext.existVariable('TLSQ'):
                stat_dict['TLSQ']   = TradeContext.TLSQ
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬�����ɹ��쳣')
            
            AfaLoggerFunc.tradeInfo("<<<<<<<��������ԭ����״̬Ϊ�����ɹ�")
            
        else:
            #=====����ԭ����״̬Ϊ����ʧ��====
            AfaLoggerFunc.tradeInfo("<<<<<<<��ʼ����ԭ����״̬Ϊ����ʧ��")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_CANC
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬����ʧ���쳣')
                
            AfaLoggerFunc.tradeInfo("<<<<<<<��������ԭ����״̬Ϊ����ʧ��")
            
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<�Է��г����ܾ�Ӧ��,������ԭ����״̬")
        
        ##����ԭ����״̬Ϊ����������
        #AfaLoggerFunc.tradeInfo('>>>��ʼ����ԭ����״̬Ϊ����������')
        #
        #if not rccpsState.newTransState(wtrbka_record['BJEDTE'],wtrbka_record['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
        #    return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�����������쳣")
        #
        #AfaLoggerFunc.tradeInfo('>>>��������ԭ����״̬Ϊ����������')
        #
        #if not AfaDBFunc.CommitSql( ):
        #    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        #    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        #    
        ##=====����ԭ����״̬Ϊ����ʧ��====
        #AfaLoggerFunc.tradeInfo("<<<<<<<��ʼ����ԭ����״̬Ϊ����ʧ��")
        #
        #stat_dict = {}
        #stat_dict['BJEDTE'] = wtrbka_record['BJEDTE']
        #stat_dict['BSPSQN'] = wtrbka_record['BSPSQN']
        #stat_dict['PRCCO']  = TradeContext.PRCCO
        #stat_dict['STRINFO']= TradeContext.STRINFO
        #stat_dict['BCSTAT'] = PL_BCSTAT_CANC
        #stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
        #
        #if not rccpsState.setTransState(stat_dict):
        #    return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬����ʧ���쳣')
        #    
        #AfaLoggerFunc.tradeInfo("<<<<<<<��������ԭ����״̬Ϊ����ʧ��")
        
    
                
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨ��ͨ�ҳ���Ӧ���Ľ���[TRC004_1162]�˳�***' )
    
    return True
