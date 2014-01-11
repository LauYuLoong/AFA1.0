# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).�����ִ���Ľ���
#===============================================================================
#   �����ļ�:   TRCC004_1109.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,time
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsDBTrcc_bilinf,rccpsEntries
import rccpsMap0000Dout_context2CTradeContext


#=====================��ִ���Ի�����(���ز���)==================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�����ִ���Ľ���[TRCC006_1109]����***' )
    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
    
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #==========���ҵ������====================================================
    if TradeContext.ROPRTPNO == "20":
        AfaLoggerFunc.tradeInfo(">>>ԭҵ������Ϊ20,���ҵ��")

        #==========���ݷ����к�,ί������,������ˮ�Ų�ѯԭ������Ϣ==============
        AfaLoggerFunc.tradeError(">>>��ʼ���ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")
        ORSNDMBRCO = TradeContext.ORMFN[:10]
        ORTRCDAT   = TradeContext.ORMFN[10:18]
        ORTRCNO    = TradeContext.ORMFN[18:]

        trc_dict = {}
        if not rccpsDBFunc.getTransTrcPK(ORSNDMBRCO,ORTRCDAT,ORTRCNO,trc_dict):
            return False
        
        AfaLoggerFunc.tradeError(">>>�������ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")

        #==========���ԭҵ���Ƿ�MFE����=======================================
        tmp_stat_dict = {}
        if not rccpsState.getTransStateSet(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERCV,PL_BDWFLG_SUCC,tmp_stat_dict):
            return AfaFlowControl.ExitThisFlow("S999","ԭ���ҵ��MFE��δ����,ֹͣ����")
        
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
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                return False
                
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
            
            stat_dict['BCSTAT']  = PL_BCSTAT_MFESTL
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return False
                
            AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ����")
            
            #==========���˽���Ϊ�˻�,����ԭ����Ϊ�˻�״̬=====================
            if trc_dict['TRCCO'] == '2000004':
                AfaLoggerFunc.tradeInfo(">>>�˻㽻��,��ʼ����ԭ����Ϊ�˻�״̬")
                
                if not rccpsState.newTransState(trc_dict['BOJEDT'],trc_dict['BOSPSQ'],PL_BCSTAT_QTR,PL_BDWFLG_WAIT):
                    return False
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                th_stat_dict = {}
                th_stat_dict['BJEDTE'] = trc_dict['BOJEDT']
                th_stat_dict['BSPSQN'] = trc_dict['BOSPSQ']
                th_stat_dict['BESBNO'] = trc_dict['BESBNO']
                th_stat_dict['BETELR'] = trc_dict['BETELR']
                th_stat_dict['BCSTAT'] = PL_BCSTAT_QTR
                th_stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                
                if not rccpsState.setTransState(th_stat_dict):
                    return False
                    
                AfaLoggerFunc.tradeInfo(">>>�˻㽻��,��������ԭ����Ϊ�˻�״̬")
            
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
            
            #==========���õ�ǰ����Ϊԭ����====================================
            TradeContext.BESBNO = trc_dict['BESBNO']
            TradeContext.BETELR = trc_dict['BETELR']
            TradeContext.TERMID = '9999999999'
            
            #==========����ԭ����״̬ΪĨ�˴�����==============================
            AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬ΪĨ�˴�����")
            
            TradeContext.NOTE3 = "���ľܾ�,�����Զ�Ĩ��"
            
            if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
                return False
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
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
            
            #=====���ü��˺����ӿ�====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            AfaLoggerFunc.tradeInfo(">>>��������Ĩ��")
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
        AfaLoggerFunc.tradeInfo(">>>ԭҵ������Ϊ21,��Ʊҵ��")
        
        #==========���ݷ����к�,ί������,������ˮ�Ų�ѯԭ������Ϣ==============
        AfaLoggerFunc.tradeError(">>>��ʼ���ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ����Ʊ��Ϣ")
        ORSNDMBRCO = TradeContext.ORMFN[:10]
        ORTRCDAT   = TradeContext.ORMFN[10:18]
        ORTRCNO    = TradeContext.ORMFN[18:]
    
        trc_dict = {}
        if not rccpsDBFunc.getTransBilPK(ORSNDMBRCO,ORTRCDAT,ORTRCNO,trc_dict):
            return False
            
        if not rccpsDBFunc.getInfoBil(trc_dict['BILVER'],trc_dict['BILNO'],trc_dict['BILRS'],trc_dict):
            return False

        AfaLoggerFunc.tradeInfo('trc_dict=' + str(trc_dict))
        
        TradeContext.ORTRCCO = trc_dict['TRCCO']
        TradeContext.BJEDTE  = trc_dict['BJEDTE']
        TradeContext.BSPSQN  = trc_dict['BSPSQN']
        
        AfaLoggerFunc.tradeError(">>>�������ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ����Ʊ��Ϣ")

        #==========���ԭҵ���Ƿ�MFE����=======================================
        tmp_stat_dict = {}
        if not rccpsState.getTransStateSet(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFERCV,PL_BDWFLG_SUCC,tmp_stat_dict):
            return AfaFlowControl.ExitThisFlow("S999","ԭ��Ʊҵ��MFE��δ����,ֹͣ����")
        
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
            
            #===========ԭ���״���=============================================
            AfaLoggerFunc.tradeInfo("TradeContext.ORTRCCO=[" + TradeContext.ORTRCCO + "]")
            
            #===========���ԭ���״���Ϊ��Ʊǩ��,���û�Ʊ״̬Ϊǩ��============
            if TradeContext.ORTRCCO == '2100001':
                AfaLoggerFunc.tradeInfo(">>>ԭ���״���Ϊǩ��")
                
                #=======����ҵ��״̬Ϊ���㴦����=============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ���㴦����")
                
                if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","����ҵ��״̬Ϊ���㴦�����쳣")
                
                AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ���㴦����")
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                #=======���û�Ʊ״̬Ϊǩ��=====================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬Ϊǩ��")
                
                if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_SIGN):
                    return AfaFlowControl.ExitThisFlow("S999","���û�Ʊ״̬�쳣")
                
                AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬Ϊǩ��")
                
                #==========����ԭ����״̬Ϊ����ɹ�
                AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ����ɹ�")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['PRCCO']  = TradeContext.PRCCO
                stat_dict['STRINFO']= TradeContext.STRINFO
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ����ɹ�")
                
            #===========���ԭ���״���Ϊ��Ʊ�⸶,������������,�ɹ������û�Ʊ״̬Ϊ�⸶
            elif TradeContext.ORTRCCO == '2100100':
                #=======ԭ���״���Ϊ��Ʊ�⸶===================================
                AfaLoggerFunc.tradeInfo(">>>ԭ���״���Ϊ�⸶")
                #===========����ԭ����ҵ��״̬Ϊ���˴�����=====================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ�������˴�����")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","����ԭ����״̬Ϊ�������˴������쳣")
                
                AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ�������˴�����")
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                #===========�������˳�ʼ��=====================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ�������˳�ʼ��")
                
                TradeContext.BESBNO   = trc_dict['BESBNO']
                TradeContext.BETELR   = trc_dict['BETELR']
                TradeContext.TERMID   = trc_dict['TERMID']
                TradeContext.BEAUUS   = trc_dict['BEAUUS']
                TradeContext.BEAUPS   = trc_dict['BEAUPS']
                
                TradeContext.HostCode = '8813'
                TradeContext.RCCSMCD  = PL_RCCSMCD_HPJF                        #����ժҪ��:��Ʊ�⸶
                TradeContext.OCCAMT   = str(trc_dict['OCCAMT'])
                TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_NXYDQSWZ  #��ũ��������������
                TradeContext.ACNM     = "ũ��������������"
                TradeContext.RBAC     = trc_dict['PYHACC']                     #����Ʊ���˺�
                TradeContext.OTNM     = trc_dict['PYHNAM']                   
                TradeContext.REAC     = TradeContext.BESBNO + PL_ACC_NXYDXZ    #�����˻�
                
                #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
                TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                
                AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
                AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
                AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.REAC )
                
                AfaLoggerFunc.tradeInfo(">>>�����������˳�ʼ��")
                #===========������������=======================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ������������")
                
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
                AfaLoggerFunc.tradeInfo(">>>����������������")
                
                if TradeContext.errorCode == '0000':
                    #=======����ԭҵ��״̬Ϊ���˳ɹ�===========================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ�������˳ɹ�")
                    
                    stat_dict = {}
                    stat_dict['BJEDTE'] = TradeContext.BJEDTE
                    stat_dict['BSPSQN'] = TradeContext.BSPSQN
                    stat_dict['BESBNO'] = TradeContext.BESBNO              #������
                    stat_dict['BETELR'] = TradeContext.BETELR              #��Ա��
                    stat_dict['TERMID'] = TradeContext.TERMID              #�ն˺�
                    stat_dict['BCSTAT'] = PL_BCSTAT_ACC                    #��ˮ״̬
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC                   #��ת�����ʶ
                    if TradeContext.existVariable('TRDT'):
                        stat_dict['TRDT']   = TradeContext.TRDT            #��������
                    if TradeContext.existVariable('TLSQ'):
                        stat_dict['TLSQ']   = TradeContext.TLSQ            #������ˮ
                    if TradeContext.existVariable('DASQ'):
                        stat_dict['DASQ']   = TradeContext.DASQ            #���������
                    stat_dict['SBAC']   = TradeContext.SBAC                #�跽�˺�
                    stat_dict['RBAC']   = TradeContext.RBAC                #�����˺�
                    stat_dict['MGID']   = TradeContext.errorCode           #����������
                    stat_dict['STRINFO']= TradeContext.errorMsg            #����������Ϣ
                    stat_dict['PRTCNT']  = 1
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ�������˳ɹ�")
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    #=======����ҵ��״̬Ϊ���㴦����=============================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ���㴦����")
                    
                    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                        return AfaFlowControl.ExitThisFlow("S999","����ҵ��״̬Ϊ���㴦�����쳣")
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ���㴦����")
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    #=======���û�Ʊ״̬Ϊ�⸶=================================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬Ϊ�⸶")
                    
                    if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_PAYC):
                        return AfaFlowControl.ExitThisFlow("S999","���û�Ʊ״̬�쳣")
                    
                    AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬Ϊ�⸶")
                    
                    #=======����ԭҵ��״̬Ϊ����ɹ�===========================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ����ɹ�")
                    
                    #stat_dict = {}
                    #stat_dict['BJEDTE']  = TradeContext.BJEDTE
                    #stat_dict['BSPSQN']  = TradeContext.BSPSQN
                    #stat_dict['BESBNO']  = TradeContext.BESBNO              #������
                    #stat_dict['BETELR']  = TradeContext.BETELR              #��Ա��
                    #stat_dict['TERMID']  = TradeContext.TERMID              #�ն˺�
                    stat_dict['BCSTAT']  = PL_BCSTAT_MFESTL                 #��ˮ״̬
                    stat_dict['BDWFLG']  = PL_BDWFLG_SUCC                   #��ת�����ʶ
                    stat_dict['PRCCO']   = TradeContext.PRCCO               #���ķ�����
                    stat_dict['STRINFO'] = TradeContext.STRINFO             #���ķ�����Ϣ
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ����ɹ�")
                    
                else:
                    #=======����ԭҵ��״̬Ϊ����ʧ��=====================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ��������ʧ��")
                    
                    #stat_dict = {}
                    #stat_dict['BJEDTE'] = TradeContext.BJEDTE
                    #stat_dict['BSPSQN'] = tradeContext.BSPSQN
                    #stat_dict['BESBNO'] = TradeContext.BESBNO              #������                         
                    #stat_dict['BETELR'] = TradeContext.BETELR              #��Ա��        
                    #stat_dict['TERMID'] = TradeContext.TERMID              #�ն˺�         
                    stat_dict['BCSTAT'] = PL_BCSTAT_ACC                    #��ˮ״̬         
                    stat_dict['BDWFLG'] = PL_BDWFLG_FAIL                   #��ת�����ʶ     
                    if TradeContext.existVariable('TRDT'):                                 
                        stat_dict['TRDT']   = TradeContext.TRDT            #��������     
                    if TradeContext.existVariable('TRDT'):                                 
                        stat_dict['TLSQ']   = TradeContext.TLSQ            #������ˮ     
                    if TradeContext.existVariable('DASQ'):                                
                        stat_dict['DASQ']   = TradeContext.DASQ            #���������     
                    stat_dict['MGID']   = TradeContext.errorCode           #����������    
                    stat_dict['STRINFO']= TradeContext.errorMsg            #����������Ϣ
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ��������ʧ��")
                    
            #===========���ԭ���״���Ϊ��Ʊ����,��������Ĩ��,�ɹ������û�Ʊ״̬Ϊ����
            if TradeContext.ORTRCCO == '2100101':
                AfaLoggerFunc.tradeInfo(">>>ԭ���״��볷��")
                
                #=======����ԭ����״̬ΪĨ�˴�����=============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ����Ĩ�˴�����")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","����ԭ����״̬Ϊ����Ĩ�˴������쳣")
                
                AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ����Ĩ�˴�����")
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                #=======����Ĩ�˳�ʼ��=========================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����Ĩ�˳�ʼ��")
                
                TradeContext.BESBNO   = trc_dict['BESBNO']
                TradeContext.BETELR   = trc_dict['BETELR']
                TradeContext.TERMID   = trc_dict['TERMID']
                TradeContext.BEAUUS   = trc_dict['BEAUUS']
                TradeContext.BEAUPS   = trc_dict['BEAUPS']
                
                #=====����ʽ���ԴΪ�����ˣ�ʹ��8813���ֳ���====
                if trc_dict['BBSSRC'] == '3':                                              #������
                    TradeContext.BJEDTE   = trc_dict['BJEDTE']                              #trc_dict[NOTE1]Ϊǩ�����׵ı�������
                    TradeContext.BSPSQN   = trc_dict['BSPSQN']                              #trc_dict[NOTE2]Ϊǩ�����׵ı������
                    TradeContext.OCCAMT   = str(trc_dict['BILAMT'])                        #Ĩ�˽��Ϊ��Ʊ���
                    TradeContext.HostCode = '8813'
                    TradeContext.RCCSMCD  = PL_RCCSMCD_HPCX                                #����ժҪ��:��Ʊ����
                    TradeContext.DASQ     = ''
                    TradeContext.RVFG     = '0'                                            #�����ֱ�־ 0
                    TradeContext.SBAC     =  TradeContext.BESBNO  +  PL_ACC_HCHK           #�跽�˺�(��Ʊ����,�������)
                    TradeContext.RBAC     =  TradeContext.BESBNO  +  PL_ACC_NXYDXZ         #�����˺�(��ũ����������)
                    #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
                    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                    AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
                    AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
                else:
                    #TradeContext.BOJEDT  = trc_dict['NOTE1']                               #trc_dict[NOTE1]Ϊǩ�����׵ı�������
                    #TradeContext.BOSPSQ  = trc_dict['NOTE2']                               #trc_dict[NOTE2]Ϊǩ�����׵ı������
                    #TradeContext.HostCode='8820'
                    
                    #�ر�� 20080922 ����,�Ǵ�����,��8813�Ǻ�����
                    TradeContext.BJEDTE   = trc_dict['BJEDTE']                             #��������
                    TradeContext.BSPSQN   = trc_dict['BSPSQN']                             #�������
                    TradeContext.OCCAMT   = "-" + str(trc_dict['BILAMT'])                  #Ĩ�˽��Ϊ��Ʊ���
                    TradeContext.HostCode = '8813'
                    TradeContext.DASQ     = ''
                    TradeContext.SBAC     = trc_dict['PYRACC']                             #�跽�˺�(��Ʊ����,��ͻ���(����))
                    TradeContext.ACNM     = trc_dict['PYRNAM']                             #�跽����(��Ʊ����,��ͻ���(����))
                    TradeContext.RBAC     = TradeContext.BESBNO  +  PL_ACC_HCHK            #�����˺�(��������(����))
                    TradeContext.OTNM     = "������"                                     #��������(��������(����))
                    #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
                    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                    
                    AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
                    AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
                
                AfaLoggerFunc.tradeInfo(">>>��������Ĩ�˳�ʼ��")
                
                #=======��������Ĩ��===========================================
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
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
                    stat_dict['PRTCNT']  = 1
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������״̬ΪĨ�˳ɹ�")
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    #==========����ԭ����״̬Ϊ���㴦����======================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ���㴦����")
                    
                    if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                        return AfaFlowControl.ExitThisFlow("S999","����ԭ����״̬Ϊ�������㴦�����쳣")
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ���㴦����")
                    
                    
                    
                    #=======���û�Ʊ״̬Ϊ����=====================================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬Ϊ����")
                        
                    if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_CANC):
                        return AfaFlowControl.ExitThisFlow("S999","���û�Ʊ״̬�쳣")
                    
                    AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬Ϊ����")
                    
                    #==========����ԭ����״̬Ϊ����ɹ�
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ����ɹ�")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    stat_dict['PRCCO']  = TradeContext.PRCCO
                    stat_dict['STRINFO']= TradeContext.STRINFO
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ����ɹ�")
                    
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
                
            #===========���ԭ���״���Ϊ��Ʊ��ʧ,���û�Ʊ״̬Ϊ��ʧ
            if TradeContext.ORTRCCO == '2100102':
                AfaLoggerFunc.tradeInfo(">>>ԭ���״���Ϊ��ʧ")
                
                #==========����ԭ����״̬Ϊ���㴦����======================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ���㴦����")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","����ԭ����״̬Ϊ�������㴦�����쳣")
                
                AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ���㴦����")
                
                #COMMIT
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                #=======���û�Ʊ״̬Ϊ��ʧ=====================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬Ϊ��ʧ")
                    
                if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_HANG):
                    return AfaFlowControl.ExitThisFlow("S999","���û�Ʊ״̬�쳣")
                
                AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬Ϊ��ʧ")
                
                #==========����ԭ����״̬Ϊ����ɹ�============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ����ɹ�")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['PRCCO']  = TradeContext.PRCCO
                stat_dict['STRINFO']= TradeContext.STRINFO
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ����ɹ�")
                
            #===========���ԭ���״���Ϊ��Ʊ,���û�Ʊ״̬Ϊ��Ʊ================
            if TradeContext.ORTRCCO == '2100103':
                AfaLoggerFunc.tradeInfo(">>>ԭ���״���Ϊ��Ʊ")
                
                #=======����ԭ����״̬Ϊ���˴�����=============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ���˴�����")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","����ԭ����״̬Ϊ�������˴������쳣")
                
                AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ���˴�����")
                
                #COMMIT
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                #=======�������˳�ʼ��=========================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ�������˳�ʼ��")
                
                TradeContext.BESBNO   = trc_dict['BESBNO']
                TradeContext.BETELR   = trc_dict['BETELR']
                TradeContext.TERMID   = trc_dict['TERMID']
                TradeContext.BEAUUS   = trc_dict['BEAUUS']
                TradeContext.BEAUPS   = trc_dict['BEAUPS']
                
                TradeContext.HostCode = '8813'
                TradeContext.RCCSMCD  = PL_RCCSMCD_HPTK                        #����ժҪ��:��Ʊ��Ʊ
                TradeContext.OCCAMT   = str(trc_dict['OCCAMT'])
                TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_HCHK      #�������
                TradeContext.ACNM     = "������"
                TradeContext.RBAC     = trc_dict['PYIACC']                     #����Ʊ�����˺�
                TradeContext.OTNM     = trc_dict['PYINAM']
                TradeContext.REAC     = TradeContext.BESBNO + PL_ACC_NXYDXZ    #�����˻�
                
                #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
                TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                
                AfaLoggerFunc.tradeInfo( '�跽�˺�1:' + TradeContext.SBAC )
                AfaLoggerFunc.tradeInfo( '�����˺�1:' + TradeContext.RBAC )
                AfaLoggerFunc.tradeInfo( '�����˺�1:' + TradeContext.REAC )
                
                AfaLoggerFunc.tradeInfo(">>>��ʼ�ж��Ƿ���ڶ�������")
                #=====�жϼ��˴���====
                AfaLoggerFunc.tradeInfo("trc_dict['RMNAMT']=" + str(trc_dict['RMNAMT']))
                if float(trc_dict['RMNAMT']) > 0.001:
                    AfaLoggerFunc.tradeInfo(">>>�ڶ��μ��˸�ֵ����")
                    
                    TradeContext.ACUR   = '2'   #����ѭ������
                    TradeContext.TRFG   = '9'   #ƾ֤�����ʶ'
                    TradeContext.I2CETY = ''    #ƾ֤����
                    TradeContext.I2SMCD = PL_RCCSMCD_HPTK                      #����ժҪ��:��Ʊ�˿�
                    TradeContext.I2TRAM = str(trc_dict['RMNAMT'])              #������
                    TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_HCHK    #�������
                    TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_DYKJQ   #��ũ���������
                    TradeContext.I2REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ  #�����˺�
                    
                    #=====�����˺�У��λ====
                    TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
                    TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
                    TradeContext.I2REAC = rccpsHostFunc.CrtAcc(TradeContext.I2REAC,25)
                    
                    AfaLoggerFunc.tradeInfo( '�跽�˺�2:' + TradeContext.I2SBAC )
                    AfaLoggerFunc.tradeInfo( '�����˺�2:' + TradeContext.I2RBAC )
                    AfaLoggerFunc.tradeInfo( '�����˺�2:' + TradeContext.I2REAC )
                    
                AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ���ڶ�������")
                
                AfaLoggerFunc.tradeInfo(">>>�����������˳�ʼ��")
                
                #=======������������===========================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ������������")
                
                rccpsHostFunc.CommHost( TradeContext.HostCode )
                
                AfaLoggerFunc.tradeInfo(">>>��ʼ������������")
                
                if TradeContext.errorCode == '0000':
                    #===�������˳ɹ�,����ԭ����״̬Ϊ���˳ɹ�==================
                    AfaLoggerFunc.tradeInfo(">>>�������˳ɹ�")
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ���˳ɹ�")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_ACC
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
                    stat_dict['PRTCNT']  = 1
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ���˳ɹ�")
                    
                    #COMMIT
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    #=======���û�Ʊҵ��״̬Ϊ���㴦����=======================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ���㴦����")
                    
                    if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                        return AfaFlowControl.ExitThisFlow("S999","����ԭ����״̬Ϊ���㴦�����쳣")
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ���㴦����")
                    
                    #COMMIT
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    #=======���û�Ʊ״̬Ϊ��Ʊ=====================================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬Ϊ��Ʊ")
                    
                    if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_RETN):
                        return AfaFlowControl.ExitThisFlow("S999","���û�Ʊ״̬�쳣")
                    
                    AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬Ϊ��Ʊ")
                    
                    #=======���û�Ʊҵ��״̬Ϊ����ɹ�=========================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ����ɹ�")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    stat_dict['PRCCO']  = TradeContext.PRCCO
                    stat_dict['STRINFO']= TradeContext.STRINFO
                    
                    if not rccpsState.setTransState(stat_dict):
                        return False
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ����ɹ�")
                
                else:
                    #===��������ʧ��,����ԭ����״̬Ϊ����ʧ��==================
                    AfaLoggerFunc.tradeInfo(">>>��������ʧ��")
                    AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ����ʧ��")
                    
                    stat_dict['BCSTAT'] = PL_BCSTAT_ACC
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
                    
                    AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ����ʧ��")
                    
            #===========���ԭ���״���Ϊ���,���û�Ʊ״̬Ϊ���=========
            if TradeContext.ORTRCCO == '2100104':
                AfaLoggerFunc.tradeInfo(">>>ԭ���״���Ϊ���")
                
                #==========����ԭ����״̬Ϊ���㴦����======================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ����״̬Ϊ���㴦����")
                
                if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
                    return AfaFlowControl.ExitThisFlow("S999","����ԭ����״̬Ϊ�������㴦�����쳣")
                
                AfaLoggerFunc.tradeInfo(">>>��������ԭ����״̬Ϊ���㴦����")
                
                #COMMIT
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                #=======���û�Ʊ״̬Ϊ���===============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬Ϊ���")
                
                if not rccpsState.newBilState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_HPSTAT_DEHG):
                    return AfaFlowControl.ExitThisFlow("S999","���û�Ʊ״̬�쳣")
                
                AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬Ϊ���")
                
                #==========����ԭ����״̬Ϊ����ɹ�============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ����ɹ�")
                
                stat_dict['BCSTAT'] = PL_BCSTAT_MFESTL
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['PRCCO']  = TradeContext.PRCCO
                stat_dict['STRINFO']= TradeContext.STRINFO
                
                if not rccpsState.setTransState(stat_dict):
                    return False
                
                AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ����ɹ�")
                
        elif TradeContext.PRCCO == "RCCO1078" or TradeContext.PRCCO == "RCCO1079":
            #==========���ķ��ر�ʾ�ŶӵĴ�����,��ʼ����״̬Ϊ�Ŷ�======
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
            #==========���ķ��ر�ʾ�ܾ��Ĵ�����,��ʼ����״̬Ϊ�ܾ�======
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
                    stat_dict['PRTCNT']  = 1
                    
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

    else:
        #==========ԭҵ�����ͷǷ�==============================================
        return AfaFlowControl.ExitThisFlow("S999", "ҵ������[" + TradeContext.ROPRTPNO + "]�Ƿ�")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    #================ΪͨѶ��ִ���ĸ�ֵ========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪͨѶ��ִ���ĸ�ֵ")
    
    #======ΪͨѶ��ִ���ĸ�ֵ==================================================
    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '�ɹ�'
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    AfaLoggerFunc.tradeInfo(">>>����ΪͨѶ��ִ���ĸ�ֵ")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�����ִ���Ľ���[TRCC006_1109]�˳�***' )
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).�����ִ���Ľ���[TRCC006_1109]����***' )
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(errorCode,errorMsg)
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).�����ִ���Ľ���[TRCC006_1109]�˳�***' )
    return True
