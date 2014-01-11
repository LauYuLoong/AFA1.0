# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨѶ��ִ���Ľ���
#===============================================================================
#   �����ļ�:   TRCC004_1111.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,rccpsState
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsDBTrcc_bilinf,rccpsEntries
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_hpcbka,rccpsDBTrcc_pjcbka,rccpsDBTrcc_ztcbka,rccpsDBTrcc_trccan,rccpsDBTrcc_mrqtbl,rccpsDBTrcc_existp,rccpsDBTrcc_rekbal


#=====================��ִ���Ի�����(���ز���)==================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨѶ��ִ���Ľ���[TRC004_1111]����***' )
    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
        
    #=================���ҵ������==============================================
    if TradeContext.ROPRTPNO == "20":
        #==========ʵʱ���ҵ��=================================================
        AfaLoggerFunc.tradeInfo(">>>ԭҵ������Ϊ20,���ҵ��")

        #==========���ݷ����к�,ί������,������ˮ�Ų�ѯԭ������Ϣ===============
        AfaLoggerFunc.tradeInfo(">>>��ʼ���ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")
        ORSNDMBRCO = TradeContext.ORMFN[:10]
        ORTRCDAT   = TradeContext.ORMFN[10:18]
        ORTRCNO    = TradeContext.ORMFN[18:]
        
        trc_dict = {}
        if not rccpsDBFunc.getTransTrcPK(ORSNDMBRCO,ORTRCDAT,ORTRCNO,trc_dict):
            return False
        
        AfaLoggerFunc.tradeInfo(">>>�������ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")

        #==========���ԭҵ��״̬�Ƿ�Ϊ����=====================================
        if trc_dict['BCSTAT'] != PL_BCSTAT_SND:
            return AfaFlowControl.ExitThisFlow("S999","��ǰ����״̬�Ƿ���״̬,ֹͣ����")
        
        #==========�������ķ���������ԭ����״̬=================================
        AfaLoggerFunc.tradeInfo(">>>���Ĵ�����Ϊ[" + TradeContext.PRCCO + "]")
        
        stat_dict = {}
        stat_dict['BJEDTE'] = trc_dict['BJEDTE']
        stat_dict['BSPSQN'] = trc_dict['BSPSQN']
        stat_dict['BESBNO'] = trc_dict['BESBNO']
        stat_dict['BETELR'] = TradeContext.BETELR
        stat_dict['PRCCO']  = TradeContext.PRCCO
        stat_dict['STRINFO']= TradeContext.STRINFO
        if TradeContext.PRCCO == "RCCI0000":
            #==========���ķ��ر�ʾ�ɹ��Ĵ�����,��ʼ����״̬Ϊ����==============
            AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ����")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERCV,PL_BDWFLG_WAIT):
                return False
                
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFERCV
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
            
            AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ����")
            
        elif TradeContext.PRCCO == "RCCO1078" or TradeContext.PRCCO == "RCCO1079":
            #==========���ķ��ر�ʾ�ŶӵĴ�����,��ʼ����״̬Ϊ�Ŷ�==============
            AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ�Ŷ�")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFEQUE,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFEQUE
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
            
            AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ�Ŷ�")
            
        else:
            #==========���ķ��ر�ʾ�ܾ��Ĵ�����,��ʼ����״̬Ϊ�ܾ�==============
            AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ�ܾ�")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFERFE
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
                
            AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ�ܾ�")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            #==========���õ�ǰ����Ϊԭ����====================================
            TradeContext.BESBNO = trc_dict['BESBNO']
            TradeContext.BETELR = trc_dict['BETELR']
            TradeContext.TERMID = trc_dict['TERMID']
            
            #==========����ԭ����״̬ΪĨ�˴�����==============================
            AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬ΪĨ�˴�����")
            
            TradeContext.NOTE3 = "���ľܾ�,�����Զ�Ĩ��"
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo(">>>Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
            AfaLoggerFunc.tradeInfo(">>>��������״̬ΪĨ�˴�����")
            #==========��������Ĩ��============================================
            AfaLoggerFunc.tradeInfo(">>>��ʼ����Ĩ��")
            
            ##====== �ź� Ĩ�˲��� ������20091112 ==============##
            #�������Ĩ���ֵ丳ֵ
            input_dict = {}
            input_dict['BJEDTE']     = trc_dict['BJEDTE']
            input_dict['BSPSQN']     = trc_dict['BSPSQN']
            if len(trc_dict['PYRACC']) != 0 :       
                 input_dict['PYRACC']     = trc_dict['PYRACC']
            else:
                 input_dict['PYRACC']     = ''
            input_dict['OCCAMT']     = str(trc_dict['OCCAMT'])
            input_dict['BBSSRC']     = trc_dict['BBSSRC']
            input_dict['BESBNO']     = TradeContext.BESBNO
            
            #���û������Ĩ��
            rccpsEntries.HDWZMZ(input_dict)
            
            #=====�����������˽ӿ�====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            AfaLoggerFunc.tradeInfo(">>>��������Ĩ��")
            stat_dict['PRCCO'] = ''
            if TradeContext.errorCode == '0000':
                #==========����ԭ����״̬ΪĨ�˳ɹ�============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬ΪĨ�˳ɹ�")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                if TradeContext.existVariable('TRDT'):
                    AfaLoggerFunc.tradeInfo("TRDT:" + TradeContext.TRDT)
                    stat_dict['TRDT'] = TradeContext.TRDT
                if TradeContext.existVariable('TLSQ'):
                    AfaLoggerFunc.tradeInfo("TLSQ:" + TradeContext.TLSQ)
                    stat_dict['TLSQ'] = TradeContext.TLSQ
                if TradeContext.existVariable('DASQ'):
                    AfaLoggerFunc.tradeInfo("DASQ:" + TradeContext.DASQ)
                    stat_dict['DASQ']   = TradeContext.DASQ
                stat_dict['MGID']   = TradeContext.errorCode
                stat_dict['STRINFO']= TradeContext.errorMsg
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>��������״̬ΪĨ�˳ɹ�")
                
                if trc_dict['TRCCO'] == '2000004':
                    #===========�˻�ҵ��,����ԭ���׹��˴��������==============
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ���׹��˴��������")
                    
                    orstat_dict = {}
                    orstat_dict['BJEDTE'] = trc_dict['BOJEDT']
                    orstat_dict['BSPSQN'] = trc_dict['BOSPSQ']
                    orstat_dict['BCSTAT'] = PL_BCSTAT_HANG
                    orstat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    if TradeContext.existVariable('DASQ'):
                        orstat_dict['DASQ']   = TradeContext.DASQ
                    
                    if not rccpsState.setTransState(orstat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ���׹��˴��������")
                
            else:
                #==========����ԭ����״̬ΪĨ��ʧ��============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬ΪĨ��ʧ��")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
                stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
                if TradeContext.existVariable('TRDT'):
                    AfaLoggerFunc.tradeInfo("TRDT:" + TradeContext.TRDT)
                    stat_dict['TRDT'] = TradeContext.TRDT
                if TradeContext.existVariable('TLSQ'):
                    AfaLoggerFunc.tradeInfo("TLSQ:" + TradeContext.TLSQ)
                    stat_dict['TLSQ'] = TradeContext.TLSQ 
                if TradeContext.existVariable('DASQ'):
                    AfaLoggerFunc.tradeInfo("DASQ:" + TradeContext.DASQ)
                    stat_dict['DASQ']   = TradeContext.DASQ
                stat_dict['MGID']   = TradeContext.errorCode
                stat_dict['STRINFO']= TradeContext.errorMsg
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>��������״̬ΪĨ��ʧ��")
            
    elif TradeContext.ROPRTPNO == "21":
        #==========ȫ����Ʊҵ��================================================
        AfaLoggerFunc.tradeInfo(">>>ԭҵ������Ϊ21,��Ʊҵ��")
        
        #==========���ݷ����к�,ί������,������ˮ�Ų�ѯԭ������Ϣ==============
        AfaLoggerFunc.tradeInfo(">>>��ʼ���ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")
        ORSNDMBRCO = TradeContext.ORMFN[:10]
        ORTRCDAT   = TradeContext.ORMFN[10:18]
        ORTRCNO    = TradeContext.ORMFN[18:]
        
        trc_dict = {}
        if not rccpsDBFunc.getTransBilPK(ORSNDMBRCO,ORTRCDAT,ORTRCNO,trc_dict):
            return False
        
        if not rccpsDBFunc.getInfoBil(trc_dict['BILVER'],trc_dict['BILNO'],trc_dict['BILRS'],trc_dict):
            return False

        TradeContext.ORTRCCO = trc_dict['TRCCO']
        
        AfaLoggerFunc.tradeInfo(">>>�������ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")

        #==========���ԭҵ��״̬�Ƿ�Ϊ����====================================
        if trc_dict['BCSTAT'] != PL_BCSTAT_SND:
            return AfaFlowControl.ExitThisFlow("S999","��ǰ����״̬�Ƿ���״̬,ֹͣ����")
        
        #==========�������ķ���������ԭ����״̬================================
        AfaLoggerFunc.tradeInfo(">>>���Ĵ�����Ϊ[" + TradeContext.PRCCO + "]")
        
        stat_dict = {}
        stat_dict['BJEDTE'] = trc_dict['BJEDTE']
        stat_dict['BSPSQN'] = trc_dict['BSPSQN']
        stat_dict['BESBNO'] = trc_dict['BESBNO']
        stat_dict['BETELR'] = TradeContext.BETELR
        stat_dict['PRCCO']  = TradeContext.PRCCO
        stat_dict['STRINFO']= TradeContext.STRINFO
        
        if TradeContext.PRCCO == "RCCI0000":
            #==========���ķ��ر�ʾ�ɹ��Ĵ�����,��ʼ����״̬Ϊ����=============
            AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ����")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERCV,PL_BDWFLG_WAIT):
                return False
                
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFERCV
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
            
            AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ����")
            
        elif TradeContext.PRCCO == "RCCO1078" or TradeContext.PRCCO == "RCCO1079":
            #==========���ķ��ر�ʾ�ŶӵĴ�����,��ʼ����״̬Ϊ�Ŷ�=============
            AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ�Ŷ�")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFEQUE,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFEQUE
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
            
            AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ�Ŷ�")
            
        else:
            #==========���ķ��ر�ʾ�ܾ��Ĵ�����,��ʼ����״̬Ϊ�ܾ�=============
            AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ�ܾ�")
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_MFERFE
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
                
            AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ�ܾ�")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            #==========���ԭ����Ϊ��Ʊǩ��,���Զ�Ĩ��=========================
            if TradeContext.ORTRCCO == '2100001':
                
                #==========���õ�ǰ����Ϊԭ����,��ǰ��ԱΪԭ��Ա===============
                TradeContext.BESBNO = trc_dict['BESBNO']
                TradeContext.BETELR = trc_dict['BETELR']
                TradeContext.TERMID = trc_dict['TERMID']
                
                #==========����ԭ����״̬ΪĨ�˴�����==========================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬ΪĨ�˴�����")
                
                TradeContext.NOTE3 = "���ľܾ�,�����Զ�Ĩ��"
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
                    return False
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                AfaLoggerFunc.tradeInfo(">>>��������״̬ΪĨ�˴�����")
                #==========��������Ĩ��========================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����Ĩ��")
                
                #=====����ʽ���ԴΪ�����ˣ�ʹ��8813���ֳ���====
                if trc_dict['BBSSRC'] == '3':                                              #������
                    TradeContext.BJEDTE   = trc_dict['BJEDTE']
                    TradeContext.BSPSQN   = trc_dict['BSPSQN']
                    TradeContext.OCCAMT   = str(trc_dict['BILAMT'])                        #Ĩ�˽��Ϊ��Ʊ���
                    TradeContext.HostCode = '8813'
                    TradeContext.RCCSMCD  = PL_RCCSMCD_HPQF                                #����ժҪ��:��Ʊǩ��
                    TradeContext.DASQ     = ''
                    TradeContext.RVFG     = '0'                                            #�����ֱ�־ 0
                    TradeContext.SBAC     =  TradeContext.BESBNO  +  PL_ACC_HCHK           #�跽�˺�(��Ʊǩ��,�������)
                    TradeContext.RBAC     =  TradeContext.BESBNO  +  PL_ACC_NXYDXZ         #�����˺�(��ũ����������)
                    #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
                    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                    AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
                    AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
                else:
                    TradeContext.BOJEDT  = trc_dict['BJEDTE']
                    TradeContext.BOSPSQ  = trc_dict['BSPSQN']
                    TradeContext.HostCode='8820'
                
                #=====�����������˽ӿ�====
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
                AfaLoggerFunc.tradeInfo(">>>��������Ĩ��")
                if TradeContext.errorCode == '0000':
                    #==========����ԭ����״̬ΪĨ�˳ɹ�========================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬ΪĨ�˳ɹ�")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    if TradeContext.existVariable('TRDT'):
                        AfaLoggerFunc.tradeInfo("TRDT:" + TradeContext.TRDT)
                        stat_dict['TRDT'] = TradeContext.TRDT
                    if TradeContext.existVariable('TLSQ'):
                        AfaLoggerFunc.tradeInfo("TLSQ:" + TradeContext.TLSQ)
                        stat_dict['TLSQ'] = TradeContext.TLSQ 
                    if TradeContext.existVariable('DASQ'):
                        AfaLoggerFunc.tradeInfo("DASQ:" + TradeContext.DASQ)
                        stat_dict['DASQ']   = TradeContext.DASQ
                    stat_dict['MGID']   = TradeContext.errorCode
                    stat_dict['STRINFO']= TradeContext.errorMsg
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������״̬ΪĨ�˳ɹ�")
                else:
                    #==========����ԭ����״̬ΪĨ��ʧ��========================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬ΪĨ��ʧ��")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
                    stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
                    if TradeContext.existVariable('TRDT'):
                        AfaLoggerFunc.tradeInfo("TRDT:" + TradeContext.TRDT)
                        stat_dict['TRDT'] = TradeContext.TRDT
                    if TradeContext.existVariable('TLSQ'):
                        AfaLoggerFunc.tradeInfo("TLSQ:" + TradeContext.TLSQ)
                        stat_dict['TLSQ'] = TradeContext.TLSQ
                    if TradeContext.existVariable('DASQ'):
                        AfaLoggerFunc.tradeInfo("DASQ:" + TradeContext.DASQ)
                        stat_dict['DASQ']   = TradeContext.DASQ
                    stat_dict['MGID']   = TradeContext.errorCode
                    stat_dict['STRINFO']= TradeContext.errorMsg
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������״̬ΪĨ��ʧ��")
                    
            #==========���ԭ����Ϊ��Ʊ��Ʊ,������ʵ�ʽ�����ͽ�����=======
            if TradeContext.ORTRCCO == '2100103':
                AfaLoggerFunc.tradeInfo(">>>��Ʊ��Ʊ,��ʼ����ʵ�ʽ�����ͽ�����")
                
                bilinf_update_dict = {}
                bilinf_update_dict['OCCAMT'] = "0.00"
                bilinf_update_dict['RMNAMT'] = "0.00"
                
                bilinf_where_dict = {}
                bilinf_where_dict['BILVER'] = trc_dict['BILVER']
                bilinf_where_dict['BILNO']  = trc_dict['BILNO']
                
                ret = rccpsDBTrcc_bilinf.update(bilinf_update_dict,bilinf_where_dict)
                
                if ret == None:
                    return AfaFlowControl.ExitThisFlow("S999","���»�Ʊ��Ϣ�Ǽǲ��쳣")
                    
                if ret <= 0:
                    return AfaFlowControl.ExitThisFlow("S999","�޶�Ӧ�Ļ�Ʊ��Ϣ")
                
                AfaLoggerFunc.tradeInfo(">>>��Ʊ��Ʊ,��������ʵ�ʽ�����ͽ�����")
            
    elif TradeContext.ROPRTPNO == "99":
        #==========��Ϣ��ҵ��==================================================
        AfaLoggerFunc.tradeInfo(">>>ԭҵ������Ϊ99,��Ϣ��ҵ��")
        
        #==========���ݷ����к�,ί������,������ˮ�Ų�ѯԭ������Ϣ===========
        AfaLoggerFunc.tradeInfo(">>>��ʼ���ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")
        bka_where_dict = {}
        bka_where_dict['SNDMBRCO'] = TradeContext.ORMFN[:10]
        bka_where_dict['TRCDAT']   = TradeContext.ORMFN[10:18]
        bka_where_dict['TRCNO']    = TradeContext.ORMFN[18:]
            
        bka_update_dict = {}
        bka_update_dict['PRCCO']   = TradeContext.PRCCO
        bka_update_dict['STRINFO'] = TradeContext.STRINFO
        
        #==========��ѯ��Ҳ�ѯ�鸴�Ǽǲ�======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯ��Ҳ�ѯ�鸴�Ǽǲ�")
        
        bka_dict = rccpsDBTrcc_hdcbka.selectu(bka_where_dict)
        
        if bka_dict == None:
            return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ҳ�ѯҵ��Ǽǲ��쳣")
            
        if len(bka_dict) > 0:
            #======��Ҳ�ѯ�鸴�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ=========
            AfaLoggerFunc.tradeInfo(">>>��Ҳ�ѯ�鸴�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ")
            
            ret = rccpsDBTrcc_hdcbka.updateCmt(bka_update_dict,bka_where_dict)
            
            if ret <= 0:
                return AfaFlowControl.ExitThisFlow("S999", "���»�ִ��Ϣ�쳣")
            
            AfaLoggerFunc.tradeInfo(">>>�������»�ִ��Ϣ")
            
            if (bka_dict['TRCCO'] == '9900512' or bka_dict['TRCCO'] == '9900523') and TradeContext.PRCCO != 'RCCI0000':
                #======���\��Լ��Ҳ鸴ҵ��,���ķ�����ǳɹ�,�޸�ԭ��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴==
                AfaLoggerFunc.tradeInfo(">>>���\��Լ��Ҳ鸴ҵ��,���ķ�����ǳɹ�")
                AfaLoggerFunc.tradeInfo(">>>��ʼ�޸�ԭ���\��Լ��Ҳ�ѯ���ײ�ѯ�鸴��ʶΪδ�鸴")
                
                bka_update_dict = {'ISDEAL':PL_ISDEAL_UNDO}
                bka_where_dict = {'BJEDTE':bka_dict['BOJEDT'],'BSPSQN':bka_dict['BOSPSQ']}
                
                ret = rccpsDBTrcc_hdcbka.updateCmt(bka_update_dict,bka_where_dict)
                
                if ret <= 0:
                    return AfaFlowControl.ExitThisFlow("S999", "����ԭ���\��Լ��Ҳ�ѯ���ײ�ѯ�鸴��ʶΪδ�鸴�쳣")
                
                AfaLoggerFunc.tradeInfo(">>>�����޸�ԭ���\��Լ��Ҳ�ѯ���ײ�ѯ�鸴��ʶΪδ�鸴")
                
        else:
            #======��Ҳ�ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯƱ�ݲ�ѯ�鸴�Ǽǲ�====
            AfaLoggerFunc.tradeInfo(">>>��Ҳ�ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯƱ�ݲ�ѯ�鸴�Ǽǲ�")
            
            bka_dict = rccpsDBTrcc_pjcbka.selectu(bka_where_dict)
            
            if bka_dict == None:
                return AfaFlowControl.ExitThisFlow("S999", "��ѯƱ�ݲ�ѯҵ��Ǽǲ��쳣")
            
            if len(bka_dict) > 0:
                #======Ʊ�ݲ�ѯ�鸴�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ====
                AfaLoggerFunc.tradeInfo(">>>Ʊ�ݲ�ѯ�鸴�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ")
                
                ret = rccpsDBTrcc_pjcbka.updateCmt(bka_update_dict,bka_where_dict)
                
                if ret <= 0:
                    return AfaFlowControl.ExitThisFlow("S999", "���»�ִ��Ϣ�쳣")
                    
                AfaLoggerFunc.tradeInfo(">>>�������»�ִ��Ϣ")
                
                if bka_dict['TRCCO'] == '9900521' and TradeContext.PRCCO != 'RCCI0000':
                    #======Ʊ�ݲ鸴ҵ��,���ķ�����ǳɹ�,�޸�ԭ��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴==
                    AfaLoggerFunc.tradeInfo(">>>Ʊ�ݲ鸴ҵ��,���ķ�����ǳɹ�")
                    AfaLoggerFunc.tradeInfo(">>>��ʼ�޸�ԭƱ�ݲ�ѯ���ײ�ѯ�鸴��ʶΪδ�鸴")
                    
                    bka_update_dict = {'ISDEAL':PL_ISDEAL_UNDO}
                    bka_where_dict = {'BJEDTE':bka_dict['BOJEDT'],'BSPSQN':bka_dict['BOSPSQ']}
                    
                    ret = rccpsDBTrcc_pjcbka.updateCmt(bka_update_dict,bka_where_dict)
                    
                    if ret <= 0:
                        return AfaFlowControl.ExitThisFlow("S999", "����ԭƱ�ݲ�ѯ���ײ�ѯ�鸴��ʶΪδ�鸴�쳣")
                    
                    AfaLoggerFunc.tradeInfo(">>>�����޸�ԭƱ�ݲ�ѯ���ײ�ѯ�鸴��ʶΪδ�鸴")
                
            else:
                #======Ʊ�ݲ�ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ��Ʊ��ѯ�鸴�Ǽǲ�====
                AfaLoggerFunc.tradeInfo(">>>Ʊ�ݲ�ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ��Ʊ��ѯ�鸴�Ǽǲ�")
                
                bka_dict = rccpsDBTrcc_hpcbka.selectu(bka_where_dict)
                
                if bka_dict == None:
                    return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊ��ѯҵ��Ǽǲ��쳣")
                    
                if len(bka_dict) > 0:
                    #======��Ʊ��ѯ�鸴�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ====
                    AfaLoggerFunc.tradeInfo(">>>��Ʊ��ѯ�鸴�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ")
                    
                    ret = rccpsDBTrcc_hpcbka.updateCmt(bka_update_dict,bka_where_dict)
                    
                    if ret <= 0:
                        return AfaFlowControl.ExitThisFlow("S999", "���»�ִ��Ϣ�쳣")
                        
                    AfaLoggerFunc.tradeInfo(">>>�������»�ִ��Ϣ")
                    
                    if bka_dict['TRCCO'] == '9900527' and TradeContext.PRCCO != 'RCCI0000':
                        #======��Ʊ�鸴ҵ��,���ķ�����ǳɹ�,�޸�ԭ��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴==
                        AfaLoggerFunc.tradeInfo(">>>��Ʊ�鸴ҵ��,���ķ�����ǳɹ�")
                        AfaLoggerFunc.tradeInfo(">>>��ʼ�޸�ԭ��Ʊ��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴")
                        
                        bka_update_dict = {'ISDEAL':PL_ISDEAL_UNDO}
                        bka_where_dict = {'BJEDTE':bka_dict['BOJEDT'],'BSPSQN':bka_dict['BOSPSQ']}
                        
                        ret = rccpsDBTrcc_hpcbka.updateCmt(bka_update_dict,bka_where_dict)
                        
                        if ret <= 0:
                            return AfaFlowControl.ExitThisFlow("S999", "����ԭ��Ʊ��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴�쳣")
                        
                        AfaLoggerFunc.tradeInfo(">>>�����޸�ԭ��Ʊ��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴")
                    
                else:
                    #======��Ʊ��ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ֧��ҵ��״̬��ѯ�鸴�Ǽǲ�====
                    AfaLoggerFunc.tradeInfo(">>>��Ʊ��ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ֧��ҵ��״̬��ѯ�鸴�Ǽǲ�")
                    
                    bka_dict = rccpsDBTrcc_ztcbka.selectu(bka_where_dict)
                    
                    if bka_dict == None:
                        return AfaFlowControl.ExitThisFlow("S999", "��ѯҵ��״̬��ѯҵ��Ǽǲ��쳣")
                        
                    if len(bka_dict) > 0:
                        #======ҵ��״̬��ѯ�鸴�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ====
                        AfaLoggerFunc.tradeInfo(">>>ҵ��״̬��ѯ�鸴�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ")
                        
                        ret = rccpsDBTrcc_ztcbka.updateCmt(bka_update_dict,bka_where_dict)
                        
                        if ret <= 0:
                            return AfaFlowControl.ExitThisFlow("S999", "���»�ִ��Ϣ�쳣")
                            
                        AfaLoggerFunc.tradeInfo(">>>�������»�ִ��Ϣ")
                        
                        if bka_dict['TRCCO'] == '9900507' and TradeContext.PRCCO != 'RCCI0000':
                            #======֧��ҵ��״̬�鸴ҵ��,���ķ�����ǳɹ�,�޸�ԭ��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴==
                            AfaLoggerFunc.tradeInfo(">>>֧��ҵ��״̬�鸴ҵ��,���ķ�����ǳɹ�")
                            AfaLoggerFunc.tradeInfo(">>>��ʼ�޸�ԭ֧��ҵ��״̬��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴")
                            
                            bka_update_dict = {'ISDEAL':PL_ISDEAL_UNDO}
                            bka_where_dict = {'BJEDTE':bka_dict['BOJEDT'],'BSPSQN':bka_dict['BOSPSQ']}
                            
                            ret = rccpsDBTrcc_hpcbka.updateCmt(bka_update_dict,bka_where_dict)
                            
                            if ret <= 0:
                                return AfaFlowControl.ExitThisFlow("S999", "����ԭ֧��ҵ��״̬��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴�쳣")
                            
                            AfaLoggerFunc.tradeInfo(">>>�����޸�ԭ֧��ҵ��״̬��ѯ���ײ�ѯ�鸴��ʶΪδ�鸴")
                        
                    else:
                        #==֧��ҵ��״̬��ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ��������Ǽǲ�==
                        AfaLoggerFunc.tradeInfo(">>>֧��ҵ��״̬��ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ��������Ǽǲ�")
                        
                        bka_dict = rccpsDBTrcc_trccan.selectu(bka_where_dict)
                        
                        if bka_dict == None:
                            return AfaFlowControl.ExitThisFlow("S999", "��ѯ�ʽ��������Ǽǲ��쳣")
                            
                        if len(bka_dict) > 0:
                            #==��������Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ=========
                            AfaLoggerFunc.tradeInfo(">>>��������Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ")
                            
                            ret = rccpsDBTrcc_trccan.updateCmt(bka_update_dict,bka_where_dict)
                            
                            if ret <= 0:
                                return AfaFlowControl.ExitThisFlow("S999","���»�ִ��Ϣ�쳣")
                                
                            AfaLoggerFunc.tradeInfo(">>>�������»�ִ��Ϣ")
                        else:
                            #==��������Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ����ֹ���Ǽǲ�==
                            AfaLoggerFunc.tradeInfo(">>>֧��ҵ��״̬��ѯ�鸴�Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ����ֹ���Ǽǲ�")
                            
                            bka_dict = rccpsDBTrcc_existp.selectu(bka_where_dict)
                            
                            if bka_dict == None:
                                return AfaFlowControl.ExitThisFlow("S999", "��ѯ����ֹ���Ǽǲ��쳣")
                                
                            if len(bka_dict) > 0:
                                #==����ֹ���Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ===========
                                AfaLoggerFunc.tradeInfo(">>>����ֹ���Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ")
                                
                                ret = rccpsDBTrcc_existp.updateCmt(bka_update_dict,bka_where_dict)
                                
                                if ret <= 0:
                                    return AfaFlowControl.ExitThisFlow("S999","���»�ִ��Ϣ�쳣")
                                    
                                AfaLoggerFunc.tradeInfo(">>>�������»�ִ��Ϣ")
                            else:
                                #==����ֹ���Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ�ʽ��������Ǽǲ�==
                                AfaLoggerFunc.tradeInfo(">>>����ֹ���Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ�ʽ��������Ǽǲ�")
                                
                                bka_dict = rccpsDBTrcc_mrqtbl.selectu(bka_where_dict)
                                
                                if bka_dict == None:
                                    return AfaFlowControl.ExitThisFlow("S999", "��ѯ�ʽ��������Ǽǲ��쳣")
                                    
                                if len(bka_dict) > 0:
                                    #==�ʽ��������Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ=========
                                    AfaLoggerFunc.tradeInfo(">>>�ʽ��������Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ")
                                    
                                    ret = rccpsDBTrcc_mrqtbl.updateCmt(bka_update_dict,bka_where_dict)
                                    
                                    if ret <= 0:
                                        return AfaFlowControl.ExitThisFlow("S999","���»�ִ��Ϣ�쳣")
                                        
                                    AfaLoggerFunc.tradeInfo(">>>�������»�ִ��Ϣ")
                                else:
                                    #==�ʽ��������Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ�����˻����֪ͨ�Ǽǲ�==
                                    AfaLoggerFunc.tradeInfo(">>>�ʽ��������Ǽǲ���δ�ҵ�ԭ������Ϣ,��ʼ��ѯ�����˻����֪ͨ�Ǽǲ�")
                                    
                                    bka_dict = rccpsDBTrcc_rekbal.selectu(bka_where_dict)
                                    
                                    if bka_dict == None:
                                        return AfaFlowControl.ExitThisFlow("S999", "��ѯ�����˻����֪ͨ�Ǽǲ��쳣")
                                    
                                    if len(bka_dict) > 0:
                                        #==�����˻����֪ͨ�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ==
                                        AfaLoggerFunc.tradeInfo(">>�����˻����֪ͨ�Ǽǲ����ҵ�ԭ������Ϣ,��ʼ���»�ִ��Ϣ")
                                        
                                        ret = rccpsDBTrcc_rekbal.updateCmt(bka_update_dict,bka_where_dict)
                                        
                                        if ret <= 0:
                                            return AfaFlowControl.ExitThisFlow("S999","���»�ִ��Ϣ�쳣")
                                            
                                        AfaLoggerFunc.tradeInfo(">>>�������»�ִ��Ϣ")
                                        
                                    else:
                                        #==δ�ҵ�ԭ������Ϣ,��������===========  
                                        return AfaFlowControl.ExitThisFlow("S999", "δ�ҵ�ԭ������Ϣ,��������")
    
    else:
        #==========ԭҵ�����ͷǷ�==============================================
        return AfaFlowControl.ExitThisFlow("S999", "ԭҵ������[" + TradeContext.ROPRTPNO + "]�Ƿ�")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.��ִ�����(1.��ִ����).ͨѶ��ִ���Ľ���[TRC004_1111]�˳�***' )
    return True
