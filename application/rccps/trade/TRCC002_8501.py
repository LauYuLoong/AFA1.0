# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.�������� 3.���ļ���).��Ʊǩ��
#===============================================================================
#   �����ļ�:   TRCC002_0000.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-07-30
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,miya
import rccpsDBTrcc_bilbka,rccpsDBTrcc_bilinf
import rccpsMap8501CTradeContext2Dbilbka,rccpsMap8501CTradeContext2Dbilinf


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊǩ��[TRCC002_8501]����***' )
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #=====��Ʊ�ཻ�׽��ճ�Ա��Ϊ������====
    TradeContext.RCVSTLBIN = PL_RCV_CENTER
    
    #=====��Ʊ����Ϊ��ǰ��������====
    TradeContext.BILDAT = TradeContext.BJEDTE
    
    #=====��Ʊ��Ϊ�����к�====
    TradeContext.REMBNKCO = TradeContext.SNDBNKCO
    TradeContext.REMBNKNM = TradeContext.SNDBNKNM
    
    #=====���ɻ�Ʊ��Ѻ=====
    AfaLoggerFunc.tradeInfo(">>>��ʼ���ɻ�Ʊ��Ѻ")
    
    #=====���ݻ�Ʊ���͸�ֵ��Ѻҵ������ͶҸ���ʽ====
    #=====PL_BILTYP_CASH  �ֽ�  PL_TYPE_XJHP  �ֽ��Ʊ====
    #=====PL_BILTYP_TRAN  ת��  PL_TYPE_ZZHP  ת�˻�Ʊ====
    if TradeContext.BILTYP == PL_BILTYP_CASH:
        TYPE = PL_TYPE_XJHP
        TradeContext.PAYWAY = PL_PAYWAY_CASH        
    elif TradeContext.BILTYP == PL_BILTYP_TRAN:
        TYPE = PL_TYPE_ZZHP
        TradeContext.PAYWAY = PL_PAYWAY_TRAN        
    else:
        return AfaFlowControl.ExitThisFlow("S999","��Ʊ���ͷǷ�")
    
    #=====�ʽ���ԴΪ1-���˽��㻧ʱ����Ҫ����8811У��֧������====
    if TradeContext.BBSSRC == '1':
        TradeContext.HostCode = '8811'
        TradeContext.ACCNO    = TradeContext.PYRACC     #�������˻�

        rccpsHostFunc.CommHost( '8811' )
       
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow('S999','��ѯƾ֤��Ϣ����')
        else:
            if TradeContext.PAYTYP != TradeContext.HPAYTYP:
                return AfaFlowControl.ExitThisFlow('S999','֧����������')
                
    MIYA      = "".rjust(10,' ')
    TRCDAT    = TradeContext.BILDAT                    #ί������
    TRCNO     = TradeContext.BILNO                     #��Ʊ����
    REMBNKCO  = TradeContext.REMBNKCO                  #ǩ����
    PAYBNKCO  = TradeContext.PAYBNKCO                  #��������
    REMBNKCO  = REMBNKCO.rjust(12,'0')
    PAYBNKCO  = PAYBNKCO.rjust(12,'0')
    AMOUNT    = str(TradeContext.BILAMT).split('.')[0] + str(TradeContext.BILAMT).split('.')[1]
    AMOUNT    = AMOUNT.rjust(15,'0')
    INFO      = ""
    
    AfaLoggerFunc.tradeDebug('��������(0-��Ѻ 1-��Ѻ):' + str(PL_SEAL_ENC) )
    AfaLoggerFunc.tradeDebug('ҵ������(1-�ֽ��Ʊ 2-ת�˻�Ʊ 3-���ӻ��ҵ��):' + TYPE )
    AfaLoggerFunc.tradeDebug('��Ʊ����:' + TRCDAT )
    AfaLoggerFunc.tradeDebug('��Ʊ����:' + TRCNO )
    AfaLoggerFunc.tradeDebug('��Ʊ���:' + str(AMOUNT) )
    AfaLoggerFunc.tradeDebug('��Ʊ�к�:' + str(REMBNKCO) )
    AfaLoggerFunc.tradeDebug('�������к�:' + str(PAYBNKCO) )
    AfaLoggerFunc.tradeDebug('��Ʊ��Ѻ:' + MIYA )
    AfaLoggerFunc.tradeDebug('OTHERINFO[' + str(INFO) + ']')
    
    #====begin ������ 20110215 �޸�====
    #ret = miya.DraftEncrypt(PL_SEAL_ENC,TYPE,TRCDAT,TRCNO,AMOUNT,REMBNKCO,PAYBNKCO,INFO,MIYA)
    ret = miya.DraftEncrypt(PL_SEAL_ENC,TYPE,TRCDAT,TradeContext.TMP_BILNO,AMOUNT,REMBNKCO,PAYBNKCO,INFO,MIYA)
    #============end============
    
    AfaLoggerFunc.tradeDebug( 'ret=' + str(ret) )
    
    if ret > 0:
        return AfaFlowControl.ExitThisFlow('S999','������Ѻ������������Ѻʧ��')
    
    TradeContext.SEAL = MIYA
    
    AfaLoggerFunc.tradeDebug('TradeContext��Ѻ:' + TradeContext.SEAL )
    AfaLoggerFunc.tradeInfo(">>>�������ɻ�Ʊ��Ѻ")
    
    #=====�Ǽǻ�Ʊҵ��Ǽǲ�====
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ�Ʊҵ��Ǽǲ�")
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN      #���ͳ�Ա�к�
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN      #���ճ�Ա�к�
    TradeContext.TRCNO    = TradeContext.SerialNo       #������ˮ��
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate    #���Ĺ�������
    TradeContext.OPRNO    = PL_HPOPRNO_QF               #ҵ������:��Ʊǩ��
    TradeContext.DCFLG    = PL_DCFLG_CRE                #�����ʶ:����
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #������ʶ:����
    TradeContext.TRCCO    = '2100001'                   #���״���:2100001��Ʊǩ��
    
    bilbka_dict = {}
    if not rccpsMap8501CTradeContext2Dbilbka.map(bilbka_dict):
        return AfaFlowContorl.ExitThisFlow("S999","Ϊ��Ʊҵ��Ǽǲ���ֵ�쳣")
        
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǻ�Ʊҵ��Ǽǲ��쳣')
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ�Ʊҵ��Ǽǲ�")
    
    #=====�Ǽǻ�Ʊ��Ϣ�Ǽǲ�====
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ�Ʊ��Ϣ�Ǽǲ�")
    
    TradeContext.NOTE1 = TradeContext.BJEDTE
    TradeContext.NOTE2 = TradeContext.BSPSQN
    TradeContext.NOTE3 = TradeContext.BESBNO
    
    bilinf_dict = {}
    if not rccpsMap8501CTradeContext2Dbilinf.map(bilinf_dict):
        return AfaFlowContorl.ExitThisFlow("S999","Ϊ��Ʊ��Ϣ�Ǽǲ���ֵ�쳣")
        
    if not rccpsDBFunc.insInfoBil(bilinf_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǻ�Ʊ��Ϣ�Ǽǲ��쳣')
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ�Ʊ��Ϣ�Ǽǲ�")
    
    #=====����ҵ��״̬Ϊ���˴�����====
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���˴�����")
    
    stat_dict = {}
    stat_dict['BJEDTE'] = TradeContext.BJEDTE       #��������
    stat_dict['BSPSQN'] = TradeContext.BSPSQN       #�������
    stat_dict['BCSTAT'] = PL_BCSTAT_ACC             #PL_BCSTAT_ACC ����
    stat_dict['BDWFLG'] = PL_BDWFLG_WAIT            #PL_BDWFLG_WAIT ������
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','����״̬Ϊ���˴������쳣')
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���˴�����")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    #=====Ϊ����������׼��====
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ����������׼��")
    
    #=====�Ǵ�����,�踶�����˺�,������,�跽�˺Ÿ���====
    if TradeContext.BBSSRC != '3':
        TradeContext.SBAC = TradeContext.PYRACC     #�跽�˺�
        TradeContext.ACNM = TradeContext.PYRNAM
    else:
        TradeContext.SBAC = ''
        TradeContext.ACNM = ''
    
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_HCHK           #�����˺�
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "������"
    
    AfaLoggerFunc.tradeInfo("�跽�˺�:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�:[" + TradeContext.RBAC + "]")
    
    #=====���п�,ƾ֤����ȡ�˺ŵ�7��18λ====
    if TradeContext.BBSSRC == '0':
        TradeContext.WARNTNO = TradeContext.SBAC[6:18]
        AfaLoggerFunc.tradeDebug("ƾ֤����:[" + TradeContext.WARNTNO + "]")
        
    
    TradeContext.HostCode = '8813'    
    TradeContext.OCCAMT = TradeContext.BILAMT                       #��Ʊ���
    TradeContext.RCCSMCD  = PL_RCCSMCD_HPQF                         #����ժҪ��:��Ʊǩ��    
    TradeContext.ACUR = '2'                                         #�ظ�����    
    TradeContext.TRFG = '4'                                         #ƾ֤�����ʶ
    
    AfaLoggerFunc.tradeDebug("TradeContext.TRFG=[" + TradeContext.TRFG + "]")
    AfaLoggerFunc.tradeDebug("TradeContext.PASSWD=[" + TradeContext.PASSWD + "]")
    AfaLoggerFunc.tradeDebug("TradeContext.WARNTNO=[" + TradeContext.WARNTNO + "]")
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ����������׼��")
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊǩ��[TRCC002_8501]�˳�***' )
    return True
#=====================�����д���(�޸���ˮ,��������,����ǰ����)================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.��������).��Ʊǩ��[TRCC002_8501]����***' )
    
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['SBAC']    = TradeContext.SBAC
    stat_dict['ACNM']    = TradeContext.ACNM
    stat_dict['RBAC']    = TradeContext.RBAC
    stat_dict['OTNM']    = TradeContext.OTNM
    if TradeContext.existVariable('TRDT'):
        stat_dict['TRDT'] = TradeContext.TRDT
    if TradeContext.existVariable('TLSQ'):
        stat_dict['TLSQ'] = TradeContext.TLSQ
    stat_dict['MGID']    = TradeContext.errorCode
    stat_dict['STRINFO'] = TradeContext.errorMsg
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        #====�������˳ɹ�,����״̬Ϊ���˳ɹ�====
        stat_dict['BCSTAT']  = PL_BCSTAT_ACC
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRTCNT']  = 1
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ���˳ɹ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ���˳ɹ�")
    else:
        #=====��������ʧ��,����״̬Ϊ����ʧ��====
        stat_dict['BCSTAT']  = PL_BCSTAT_ACC
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ����ʧ��")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    #====����ҵ��״̬Ϊ���ʹ�����====
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���ʹ�����")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ���ʹ������쳣")
    
    AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ���ʹ�����")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    #====Ϊ����ũ������׼��====    
    TradeContext.MSGTYPCO = 'SET001'
    TradeContext.TRCCO    = '2100001'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = ''
    TradeContext.OPRTYPNO = '21'
    TradeContext.ROPRTPNO = ''
    TradeContext.TRANTYP  = '0'
    
    #begin 20110614 ����̩ �޸� ����ũ�������ĵ�Ʊ��Ϊ8λ
    TradeContext.BILNO = TradeContext.BILNO[-8:]
    #end
    
    AfaLoggerFunc.tradeInfo(">>>Ϊ����ũ������׼��")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.��������).��Ʊǩ��[TRCC002_8501]�˳�***' )
    return True   
#=====================���׺���================================================
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(3.���ļ���).��Ʊǩ��[TRCC002_8501]����***' )
    
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
        #=====����ũ�����ɹ�,����״̬Ϊ���ͳɹ�====
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ���ͳɹ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ���ͳɹ�")
    else:
        #=====����ũ����ʧ��,����״̬Ϊ����ʧ��====       
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ����ʧ��")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
        #====�Զ�Ĩ��====
        AfaLoggerFunc.tradeInfo(">>>��ʼ�Զ�Ĩ��")
        
        #====����ҵ��״̬ΪĨ�˴�����====        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ΪĨ�˴������쳣')
        
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬ΪĨ�˴�����")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
        #=====��������Ĩ��====
        #=====����ʽ���ԴΪ�����ˣ�ʹ��8813���ֳ���====
        TradeContext.BOJEDT = TradeContext.BJEDTE           #��ǰ�����ڸ�ֵ
        TradeContext.BOSPSQ = TradeContext.BSPSQN           #��ǰ����ˮ�Ÿ�ֵ
        if TradeContext.BBSSRC  ==  '3':      #������
            TradeContext.HostCode= '8813'
            TradeContext.DASQ    = ''
            TradeContext.RVFG    = '0'        #�����ֱ�־ 0����
            TradeContext.SBAC    =  TradeContext.BESBNO  +  PL_ACC_HCHK       #�跽�˺�
            TradeContext.RBAC    =  TradeContext.BESBNO  +  PL_ACC_NXYDXZ     #�����˺�
            #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
            TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
            AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
        else:
            TradeContext.HostCode='8820'

        #=====����Ĩ�������ӿ�====
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        if TradeContext.HostCode == '8813':
            stat_dict['SBAC']    = TradeContext.SBAC
            stat_dict['RBAC']    = TradeContext.RBAC
        if TradeContext.existVariable('TRDT'):
            stat_dict['TRDT'] = TradeContext.TRDT
        if TradeContext.existVariable('TLSQ'):
            stat_dict['TLSQ'] = TradeContext.TLSQ
        stat_dict['MGID']    = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        if TradeContext.errorCode == '0000':
            #=====����Ĩ�˳ɹ�,����ҵ��״̬ΪĨ�˳ɹ�====           
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ĩ�˳ɹ��쳣')
            
            AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬ΪĨ�˳ɹ�")
        else:
            #=====����Ĩ��ʧ��,����ҵ��״̬ΪĨ��ʧ��====
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ĩ�˳ɹ��쳣')
            
            AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬ΪĨ��ʧ��")
        
        AfaLoggerFunc.tradeInfo(">>>�����Զ�Ĩ��")

    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(3.���ļ���).��Ʊǩ��[TRCC002_8501]�˳�***' )
    return True
