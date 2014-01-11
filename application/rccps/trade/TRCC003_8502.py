# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Ʊ�⸶
#===============================================================================
#   �����ļ�:   TRCC003_8502.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-17
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,miya
import rccpsDBTrcc_bilbka
import rccpsMap8502CTradeContext2Dbilbka,rccpsMap8502CTradeContext2Dbilinf

#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊ�⸶[TRCC003_8502]����***' )
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #�ô�������Ϊ�������к�
    TradeContext.PAYBNKCO = TradeContext.SNDBNKCO
    TradeContext.PAYBNKNM = TradeContext.SNDBNKNM
    
    if TradeContext.BILTYP == PL_BILTYP_CASH:
        #=================�ֽ��Ʊ�ó�Ʊ���˺�Ϊ2431�˺ſ�Ŀ========================
        TradeContext.PYHACC = TradeContext.BESBNO + PL_ACC_NXYDXZ
        TradeContext.PYHACC = rccpsHostFunc.CrtAcc(TradeContext.PYHACC,25)
        
    AfaLoggerFunc.tradeInfo("TradeContext.PYHACC=" + TradeContext.PYHACC)
    AfaLoggerFunc.tradeInfo("TradeContext.PYHNAM=" + TradeContext.PYHNAM)
    
    #=================���ױ�Ҫ�Լ��============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ���ױ�Ҫ�Լ��")
    
    if abs(float(TradeContext.BILAMT) - float(TradeContext.OCCAMT) - float(TradeContext.RMNAMT)) >= 0.001:
        return AfaFlowControl.ExitThisFlow("S999","������ǳ�Ʊ�����ʵ�ʽ�����֮��")
    
    AfaLoggerFunc.tradeInfo(">>>�������ױ�Ҫ�Լ��")
    
    #=================�����Ƿ��ظ�����==========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼУ���ظ�����")
    
    bilbka_where_dict = {}
    bilbka_where_dict['BILRS']   = PL_BILRS_OUT
    bilbka_where_dict['BILVER']  = TradeContext.BILVER
    bilbka_where_dict['BILNO']   = TradeContext.BILNO
    bilbka_where_dict['HPSTAT']  = PL_HPSTAT_PAYC
    
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    if bilbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","��ѯԭ��Ʊ��Ϣ�쳣,У���ظ�����ʧ��")
        
    if len(bilbka_dict) > 0:
        return AfaFlowControl.ExitThisFlow("S999","�˻�Ʊ�ѱ��⸶,�ظ�����,��ֹ�ύ")
    
    AfaLoggerFunc.tradeInfo(">>>����У���ظ�����")
    
    if TradeContext.BILTYP != PL_BILTYP_CASH:
        #=================У�������˺Ż���======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼУ�������˺Ż���")
        
        TradeContext.HostCode = '8810'
        
        TradeContext.ACCNO = TradeContext.PYHACC
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNO)
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNM)
        
        if TradeContext.ACCNM != TradeContext.PYHNAM:
            return AfaFlowControl.ExitThisFlow('S999',"�˺Ż�������")
            
        if TradeContext.ACCST != '0' and TradeContext.ACCST != '2':
            return AfaFlowControl.ExitThisFlow('S999','�����˺�״̬������')
        
        AfaLoggerFunc.tradeInfo(">>>����У�������˺Ż���")
    
    #=================У���Ʊ��Ѻ==============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼУ���Ʊ��Ѻ")
    
    if TradeContext.BILTYP == PL_BILTYP_CASH:
        TYPE = PL_TYPE_XJHP
    elif TradeContext.BILTYP == PL_BILTYP_TRAN:
        TYPE = PL_TYPE_ZZHP
    else:
        return AfaFlowControl.ExitThisFlow("S999","��Ʊ���ͷǷ�")
    
    AfaLoggerFunc.tradeDebug('TradeContext��Ѻ:' + TradeContext.SEAL )
    
    MIYA = TradeContext.SEAL
    TRCDAT = TradeContext.BILDAT
    TRCNO = TradeContext.BILNO
    REMBNKCO  = TradeContext.REMBNKCO                  #ǩ����
    PAYBNKCO  = TradeContext.PAYBNKCO                  #��������
    REMBNKCO  = REMBNKCO.rjust(12,'0')
    PAYBNKCO  = PAYBNKCO.rjust(12,'0')
    AMOUNT = str(TradeContext.BILAMT).split('.')[0] + str(TradeContext.BILAMT).split('.')[1]
    AMOUNT = AMOUNT.rjust(15,'0')
    INFO   = ""
    
    AfaLoggerFunc.tradeDebug('��������(0-��Ѻ 1-��Ѻ):' + str(PL_SEAL_DEC) )
    AfaLoggerFunc.tradeDebug('ҵ������(1-�ֽ��Ʊ 2-ת�˻�Ʊ 3-���ӻ��ҵ��):' + TYPE )
    AfaLoggerFunc.tradeDebug('��Ʊ����:' + TRCDAT )
    AfaLoggerFunc.tradeDebug('��Ʊ����:' + TRCNO )
    AfaLoggerFunc.tradeDebug('��Ʊ���:' + str(AMOUNT) )
    AfaLoggerFunc.tradeDebug('��Ʊ�к�:' + str(REMBNKCO) )
    AfaLoggerFunc.tradeDebug('�������к�:' + str(PAYBNKCO) )
    AfaLoggerFunc.tradeDebug('��Ʊ��Ѻ:' + MIYA )
    AfaLoggerFunc.tradeDebug('OTHERINFO[' + str(INFO) + ']')
    
    AfaLoggerFunc.tradeDebug('TradeContext��Ѻ:' + TradeContext.SEAL )
    
    #====begin ������ 20110215 �޸�====
    #ret = miya.DraftEncrypt(PL_SEAL_DEC,TYPE,TRCDAT,TRCNO,AMOUNT,REMBNKCO,PAYBNKCO,INFO,MIYA)
    ret = miya.DraftEncrypt(PL_SEAL_DEC,TYPE,TRCDAT,TradeContext.TMP_BILNO,AMOUNT,REMBNKCO,PAYBNKCO,INFO,MIYA)
    #============end============
    
    AfaLoggerFunc.tradeDebug('TradeContext��Ѻ:' + TradeContext.SEAL )
    
    AfaLoggerFunc.tradeDebug( 'ret=' + str(ret) )
    
    if ret == 9005:
        return AfaFlowControl.ExitThisFlow('S999','��Ѻ��,����ҵ��Ҫ�غ���Ѻ')
    elif ret > 0:
        return AfaFlowControl.ExitThisFlow('S999','������Ѻ������ʧ��')
    
    AfaLoggerFunc.tradeInfo(">>>����У���Ʊ��Ѻ")
    
    #=================�Ǽǻ�Ʊ�Ǽǲ�========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ�Ʊ�Ǽǲ�")
    
    #=================Ϊ��Ʊҵ��Ǽǲ���ֵ==================================
    TradeContext.OPRNO    = PL_HPOPRNO_JF                #ҵ�����ͽ⸶
    TradeContext.DCFLG    = PL_DCFLG_CRE
    TradeContext.BILRS    = PL_BILRS_OUT
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = '1000000000'
    
    bilbka_dict = {}
    if not rccpsMap8502CTradeContext2Dbilbka.map(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','Ϊ��Ʊҵ��Ǽǲ���ֵ�쳣')
    
    #=================�Ǽǻ�Ʊҵ��Ǽǲ�====================================
    
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǻ�Ʊҵ��Ǽǲ��쳣')
    
    #=================Ϊ��Ʊ��Ϣ�Ǽǲ���ֵ==================================
    
    bilinf_dict = {}
    if not rccpsMap8502CTradeContext2Dbilinf.map(bilinf_dict):
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        return AfaFlowControl.ExitThisFlow('S999','Ϊ��Ʊ��Ϣ�Ǽǲ���ֵ�쳣')
        
    bilinf_dict['NOTE3'] = TradeContext.BESBNO    #�����׻�����ֵ����Ʊ��Ϣ�Ǽǲ���note3�ֶ�
    
    #=================�Ǽǻ�Ʊ��Ϣ�Ǽǲ�====================================
    
    if not rccpsDBFunc.insInfoBil(bilinf_dict):
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǻ�Ʊ��Ϣ�Ǽǲ��쳣')
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ�Ʊ�Ǽǲ�")
    
    #=================����״̬Ϊ���ʹ�����======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���ʹ�����")
    
    stat_dict = {}
    stat_dict['BJEDTE'] = TradeContext.BJEDTE
    stat_dict['BSPSQN'] = TradeContext.BSPSQN
    stat_dict['BCSTAT'] = PL_BCSTAT_SND
    stat_dict['BDWFLG'] = PL_BDWFLG_WAIT
    if not rccpsState.setTransState(stat_dict):
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        return AfaFlowControl.ExitThisFlow('S999','����״̬Ϊ���ʹ������쳣')
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���ʹ�����")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊ�⸶[TRCC003_8502]����***' )
    
    #=================Ϊ��Ʊ�⸶���ĸ�ֵ========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ�⸶���ĸ�ֵ")
    
    TradeContext.MSGTYPCO = "SET008"
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "21"
    TradeContext.ROPRTPNO = ""
    TradeContext.TRANTYP  = "0"
    TradeContext.ORTRCCO  = ""
    
    TradeContext.TRCCO     = '2100100'
    TradeContext.TRCNO     = TradeContext.SerialNo
    TradeContext.RCVSTLBIN = TradeContext.RCVMBRCO
    TradeContext.OPRATTNO  = ""
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ�⸶���ĸ�ֵ")
    
    return True

#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).��Ʊ�⸶[TRCC003_8502]����***' )
    
    #=================�ж�afe�Ƿ��ͳɹ�=======================================
    if TradeContext.errorCode != '0000':
        #=============AFE����ʧ��,����״̬Ϊ����ʧ��============================
        AfaLoggerFunc.tradeInfo('>>>AFE����ʧ��,��ʼ����״̬Ϊ����ʧ��')
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        stat_dict['PRCCO']   = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999','����״̬Ϊ����ʧ���쳣')
            
        AfaLoggerFunc.tradeInfo('>>>��������״̬Ϊ����ʧ��')
    else:
        #=============AFE���ͳɹ�,����״̬Ϊ���ͳɹ�============================
        AfaLoggerFunc.tradeInfo('>>>AFE���ͳɹ�,��ʼ����״̬Ϊ���ͳɹ�')
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRCCO']   = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999','����״̬Ϊ���ͳɹ��쳣')
            
        AfaLoggerFunc.tradeInfo('>>>��������״̬Ϊ���ͳɹ�')
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '����ũ�������ĳɹ�'
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).��Ʊ�⸶[TRCC003_8502]����***' )
    
    return True
    
