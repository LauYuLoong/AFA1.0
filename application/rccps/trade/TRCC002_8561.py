# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.�������� 3.���ļ���).�����ֽ�ͨ��
#==============================================================================
#   �����ļ�:   TRCC002_8561.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-10-20
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,time
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsGetFunc
import rccpsMap8563CTradeContext2Dwtrbka_dict


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�����ֽ�ͨ��[TRCC002_8561]����***' )
    #=================��Ҫ�Լ��===============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")
    
    #��鱾�����Ƿ���ͨ��ͨ��ҵ��Ȩ��
    if not rccpsDBFunc.chkTDBESAuth(TradeContext.BESBNO):
        return AfaFlowControl.ExitThisFlow("S999","��������ͨ��ͨ��ҵ��Ȩ��")
    
    #�ŵ���Ϣ
    if TradeContext.PYETYP == '0':
        if TradeContext.SCTRKINF == '':
            return AfaFlowControl.ExitThisFlow("�ŵ���Ϣ����Ϊ��")
        
        #if TradeContext.THTRKINF == '':
        #    return AfaFlowControl.ExitThisFlow("�ŵ���Ϣ����Ϊ��")
            
        if len(TradeContext.SCTRKINF) > 37:
            return AfaFlowControl.ExitThisFlow('S999','�ŵ���Ϣ�Ƿ�')
            
        #if len(TradeContext.THTRKINF) > 104:
        #    return AfaFlowControl.ExitThisFlow('S999','�ŵ���Ϣ�Ƿ�')
    elif TradeContext.PYETYP == '2':
        TradeContext.SCTRKINF = ''.rjust(37,'0')
        TradeContext.THTRKINF = ''.rjust(37,'0')
        
    #���ۺ���
    if TradeContext.PYETYP == '1':
        if TradeContext.BNKBKNO == '':
            return AfaFlowControl.ExitThisFlow('���ۺ��벻��Ϊ��')
    elif TradeContext.PYETYP == '3':
        TradeContext.BNKBKNO = ''
    
    AfaLoggerFunc.tradeInfo(">>>������Ҫ�Լ��")
    
    #=================�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�===================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN      #���ͳ�Ա�к�
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN      #���ճ�Ա�к�
    TradeContext.TRCNO    = TradeContext.SerialNo       #������ˮ��
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate    #���Ĺ�������
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.TRCDAT + TradeContext.TRCNO  #���ı�ʶ��
    TradeContext.OPRNO    = PL_TDOPRNO_TC               #ҵ������:�����ֽ�ͨ��
    TradeContext.DCFLG    = PL_DCFLG_CRE                #�����ʶ:����
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #������ʶ:����
    #if TradeContext.PYITYP == '0' or '2':
    #    TradeContext.TRCCO = '3000002'                  #���״���:3000002���ֽ�ͨ��
    #elif TradeContext.PYITYP == '1' or '3':
    #    TradeContext.TRCCO = '3000004'                  #���״���:3000004���ֽ�ͨ��
    #else:
    #    return AfaFlowContorl.ExitThisFlow("S999","�տ����˻����ͷǷ�")
    TradeContext.PYRMBRCO = TradeContext.SNDSTLBIN
    TradeContext.PYEMBRCO = TradeContext.RCVSTLBIN
    
    wtrbka_dict = {}
    if not rccpsMap8563CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
        return AfaFlowContorl.ExitThisFlow("S999","Ϊͨ��ͨ��ҵ��Ǽǲ���ֵ�쳣")
        
    if not rccpsDBFunc.insTransWtr(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽ�ͨ��ͨ��ҵ��Ǽǲ��쳣')
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
    
    #=================����ҵ��״̬Ϊ���˴�����=================================
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
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���˴�����")
    
    #=================Ϊ����������׼��=========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ����������׼��")
    
    TradeContext.HostCode = '8813' 
       
    TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
    TradeContext.CATR = '0'                                         #��ת��ʶ:0-�ֽ�
    TradeContext.RCCSMCD  = PL_RCCSMCD_XJTCWZ                         #����ժҪ��:�ֽ�ͨ������
    TradeContext.SBAC = ''
    TradeContext.ACNM = ''
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "ũ��������������"
    TradeContext.CTFG = '7'                                         #��ת��ʶ:��ת-0
    
    AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
    
    if TradeContext.CHRGTYP == '0':
        #�ֽ���ȡ������
        TradeContext.ACUR = '2'                                         #�ظ����� 
        
        TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
        TradeContext.I2CATR = '0'                                       #��ת��ʶ:0-�ֽ�
        TradeContext.I2TRAM = TradeContext.CUSCHRG                      #�����ѽ��
        TradeContext.I2SMCD = PL_RCCSMCD_SXF                            #����ժҪ��:������
        TradeContext.I2SBAC = ''
        TradeContext.I2ACNM = ''
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #�����˺�:ͨ��ͨ��������
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM = "ũ����������"
        TradeContext.I2CTFG = '8'                                       #��ת��ʶ:����ת-1
    elif TradeContext.CHRGTYP == '1':
        #�ֽ�ͨ���޷���ȡ�����˻�������
        return AfaFlowControl.ExitThisFlow("S999","�ֽ�ͨ���޷�ת����ȡ������")
    elif TradeContext.CHRGTYP == '2':
        AfaLoggerFunc.tradeInfo(">>>����������")
    else:
        return AfaFlowControl.ExitThisFlow("S999","�Ƿ���������ȡ��ʽ")
        
    if TradeContext.existVariable("I2SBAC") and TradeContext.existVariable('I2RBAC'):
        AfaLoggerFunc.tradeInfo("�跽�˺�2:[" + TradeContext.I2SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�2:[" + TradeContext.I2RBAC + "]")
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ����������׼��")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�����ֽ�ͨ��[TRCC002_8561]�˳�***' )
    
    return True


#=====================�����д���(�޸���ˮ,��������,����ǰ����)===============
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.��������).�����ֽ�ͨ��[TRCC002_8561]����***' )
    
    #=================����ҵ��״̬Ϊ���˳ɹ���ʧ��=============================
    
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
    
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���˳ɹ�")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_ACC
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRTCNT']  = 1
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ���˳ɹ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���˳ɹ�")
        
    else:
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ����ʧ��")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_ACC
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ����ʧ��")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    #=================Ϊ����ũ����������׼��===================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ����ũ����������׼��")
    
    TradeContext.MSGTYPCO = 'SET003'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = ''
    TradeContext.OPRTYPNO = '30'
    TradeContext.ROPRTPNO = ''
    TradeContext.TRANTYP  = '0'
    
    TradeContext.CUR = 'CNY'
    TradeContext.LOCCUSCHRG = TradeContext.CUSCHRG
    TradeContext.CUSCHRG = '0.00'
    
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ����ũ����������׼��")
    
    
    #=================����ҵ��״̬Ϊ���ʹ�����=================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����״̬Ϊ���ʹ�����")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ���ʹ������쳣")
    
    AfaLoggerFunc.tradeInfo(">>>��������״̬Ϊ���ʹ�����")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.��������).�����ֽ�ͨ��[TRCC002_8561]�˳�***' )
    return True
    
        
#=====================���׺���===============================================
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(3.���ļ���).�����ֽ�ͨ��[TRCC002_8561]����***' )
    
    #=================����ҵ��״̬Ϊ���ͳɹ���ʧ��,������ʧ�����Զ�Ĩ��========
    
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
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���ͳɹ�")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ���ͳɹ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���ͳɹ�")
        
    else:
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ����ʧ��")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ����ʧ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ����ʧ��")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        
        #=============��������Ĩ��=============================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬ΪĨ�˴�����")
        
        #=====���⴦��  �ر�� 20081127 ��8813Ĩ��,������µ�ǰ����ˮ�Ž��м���====
        if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
            return AfaFlowControl.ExisThisFlow('S999',"�����µ�ǰ����ˮ���쳣")
        
        
        #ΪĨ�˻�Ʒ�¼��ֵ
        TradeContext.HostCode='8813'
        
        TradeContext.PKFG = 'T'                                         #ͨ��ͨ�ұ�ʶ
        TradeContext.RVFG = '2'                                         #�����ֱ�־ 2
        TradeContext.CATR = '0'                                         #��ת��ʶ:0-�ֽ�
        TradeContext.RCCSMCD = PL_RCCSMCD_XJTCWZ                        #����ժҪ��:�ֽ�ͨ������
        TradeContext.SBAC = ''
        TradeContext.ACNM = ''
        TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ       #�����˺�
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM = "ũ��������������"
        TradeContext.CTFG = '7'                                         #��ת��ʶ:��ת-0
        
        AfaLoggerFunc.tradeInfo("�跽�˺�1:[" + TradeContext.SBAC + "]")
        AfaLoggerFunc.tradeInfo("�����˺�1:[" + TradeContext.RBAC + "]")
        
        if TradeContext.CHRGTYP == '0':
            #�ֽ���ȡ������
            TradeContext.ACUR   = '2'                                       #�ظ�����
            
            TradeContext.I2PKFG = 'T'                                       #ͨ��ͨ�ұ�ʶ
            TradeContext.I2RVFG = '2'                                       #�����ֱ�־ 2
            TradeContext.I2CATR = '0'                                       #��ת��ʶ:0-�ֽ�
            TradeContext.I2TRAM = TradeContext.LOCCUSCHRG                   #�����ѽ��
            TradeContext.I2SMCD = PL_RCCSMCD_SXF                            #����ժҪ��:������
            TradeContext.I2SBAC = ''
            TradeContext.I2ACNM = ''
            TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_TCTDSXF      #�����˺�:ͨ��ͨ��������
            TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
            TradeContext.I2OTNM = "ũ����������"
            TradeContext.I2CTFG = '8'                                       #��ת��ʶ:����ת-1
        
        
        #====����ҵ��״̬ΪĨ�˴�����====
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ΪĨ�˴������쳣')
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬ΪĨ�˴�����")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
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
            stat_dict['PRTCNT'] = 1                            #��ӡ����
            
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
        
    TradeContext.errorCode = '0000'
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(3.���ļ���).�����ֽ�ͨ��[TRCC002_8561]�˳�***' )
    return True
