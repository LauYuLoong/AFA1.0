# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.�������� 3.���Ĳ���).�����˻�
#===============================================================================
#   �����ļ�:   TRCC003_8509.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsDBTrcc_trcbka,rccpsState,rccpsHostFunc
from types import *
from rccpsConst import *


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    #====��ʼȡ��ˮ�Ŷ�Ӧ��Ϣ====
    trcbka_dict = {}
    dict = rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka_dict)
    if dict == False:
        return AfaFlowControl.ExitThisFlow('M999','ȡ������Ϣʧ��')

    #=====�жϳ�����Ϣ====
    if trcbka_dict['BRSFLG'] != PL_BRSFLG_RCV:
        return AfaFlowControl.ExitThisFlow('M999','ԭ����Ϊ����ҵ�񣬲������˻����')
    if TradeContext.BESBNO != trcbka_dict["BESBNO"]:
        return AfaFlowControl.ExitThisFlow('M999','�����������˻�')
    if str(trcbka_dict['TRCCO']) == '2000009':
        return AfaFlowControl.ExitThisFlow('M999','��Լ���ҵ�������˻�')
    if str(trcbka_dict['TRCCO']) == '2000004':
        return AfaFlowControl.ExitThisFlow('M999','�˻�ҵ�������ٴ��˻�')
    if str(trcbka_dict['TRCCO'])[0:2] != '20':
        return AfaFlowControl.ExitThisFlow('M999','�ǻ��ҵ�������˻�')
    if trcbka_dict["BCSTAT"] != PL_BCSTAT_HANG:   #�Զ�����״̬ 1 �ɹ�
         return AfaFlowControl.ExitThisFlow('M999','��ǰҵ��״̬Ϊ['+str(trcbka_dict["BCSTAT"])+']�������˻�' )

    TradeContext.ORSNDBNK    = trcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNK    = trcbka_dict['RCVBNKCO']
    TradeContext.ORSNDBNKNM  = trcbka_dict['SNDBNKNM']
    TradeContext.ORRCVBNKNM  = trcbka_dict['RCVBNKNM']

    #=====��ʼ�������ݿ�====
    trcbka_dict["BRSFLG"]    = TradeContext.BRSFLG
    trcbka_dict["BOJEDT"]    = trcbka_dict["BJEDTE"]
    trcbka_dict["BOSPSQ"]    = trcbka_dict["BSPSQN"]
    trcbka_dict["ORTRCDAT"]  = trcbka_dict["TRCDAT"]
    trcbka_dict["ORTRCCO"]   = trcbka_dict["TRCCO"] 
    trcbka_dict["ORTRCNO"]   = trcbka_dict["TRCNO"] 
    trcbka_dict["ORSNDBNK"]  = trcbka_dict["SNDBNKCO"]
    trcbka_dict["ORRCVBNK"]  = trcbka_dict["RCVBNKCO"]
    trcbka_dict["BJEDTE"]    = TradeContext.BJEDTE
    trcbka_dict["BSPSQN"]    = TradeContext.BSPSQN
    trcbka_dict["BJETIM"]    = TradeContext.BJETIM
    trcbka_dict["TRCDAT"]    = TradeContext.TRCDAT
    trcbka_dict["STRINFO"]   = TradeContext.STRINFO
    trcbka_dict["TRCCO"]     = TradeContext.TRCCO
    trcbka_dict["TRCNO"]     = TradeContext.SerialNo
    trcbka_dict["SNDBNKCO"]  = TradeContext.SNDBNKCO
    trcbka_dict["SNDBNKNM"]  = TradeContext.SNDBNKNM
    trcbka_dict["SNDMBRCO"]  = TradeContext.SNDSTLBIN
    trcbka_dict["RCVBNKCO"]  = TradeContext.RCVBNKCO
    trcbka_dict["RCVBNKNM"]  = TradeContext.RCVBNKNM
    trcbka_dict["RCVMBRCO"]  = TradeContext.RCVSTLBIN
    trcbka_dict["OPRNO"]     = "09"
    trcbka_dict["BBSSRC"]    = "3"
    trcbka_dict["BETELR"]    = TradeContext.BETELR
    trcbka_dict["TERMID"]    = TradeContext.TERMID
    
    #=====������ 2008-09-17 ע�Ͷ�ҵ�����͵ĸ��ղ���====
    #trcbka_dict["OPRATTNO"]  = ""
    
    trcbka_dict["NCCWKDAT"]  = TradeContext.NCCworkDate
    trcbka_dict["SEAL"]      = ""

    #=====Ϊ�����˻㱨�ĸ�ֵ====
    TradeContext.OPRTYPNO    =  '20'   #���
    TradeContext.ORTRCCO     = trcbka_dict['ORTRCCO']
    TradeContext.ORTRCDAT    = trcbka_dict['ORTRCDAT']
    TradeContext.ORTRCNO     = trcbka_dict['ORTRCNO']
    TradeContext.ORPYRACC    = trcbka_dict['PYRACC']
    TradeContext.ORPYRNAM    = trcbka_dict['PYRNAM']
    TradeContext.ORPYEACC    = trcbka_dict['PYEACC']
    TradeContext.ORPYENAM    = trcbka_dict['PYENAM']
    TradeContext.PYRACC      = trcbka_dict['PYRACC']
    TradeContext.PYRNAM      = trcbka_dict['PYRNAM']
    TradeContext.PYRADDR     = trcbka_dict['PYRADDR']
    TradeContext.PYEACC      = trcbka_dict['PYEACC']
    TradeContext.PYENAM      = trcbka_dict['PYENAM']
    TradeContext.PYEADDR     = trcbka_dict['PYEADDR']
    
    
    
    AfaLoggerFunc.tradeInfo( '�ֵ�trccan_dict��' + str(trcbka_dict) )

    #=====��ʼ�������ݿ�====
    if not rccpsDBFunc.insTransTrc(trcbka_dict):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D002', '�������ݿ����,RollBack�ɹ�')

    #=====commit����====
    if not AfaDBFunc.CommitSql():
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D011', '���ݿ�Commitʧ��')
    else:
        AfaLoggerFunc.tradeDebug('COMMIT�ɹ�')


    #=====����sstlog����״̬Ϊ������-������====
    status = {}
    status['BJEDTE']     = TradeContext.BJEDTE
    status['BSPSQN']     = TradeContext.BSPSQN
    status['BCSTAT']     = PL_BCSTAT_ACC
    status['BDWFLG']     = PL_BDWFLG_WAIT

    if not rccpsState.setTransState(status):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit�ɹ�')

    #=====��������8813====
    TradeContext.HostCode  = '8813'
    TradeContext.OCCAMT    = str(trcbka_dict['OCCAMT'])     #���
    TradeContext.RCCSMCD   = PL_RCCSMCD_LTH                 #����ժҪ���룺�����˻�
    TradeContext.DASQ      = trcbka_dict['DASQ']
    #=====��ʼƴ������˺�====
    TradeContext.RBAC =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ
    #TradeContext.SBAC =  TradeContext.BESBNO + PL_ACC_NXYDXZ

    #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
    #TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
    AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
    #AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )

    return True
#=====================���ĺ���================================================
def SubModuleDoSnd():

    AfaLoggerFunc.tradeInfo( '>>>��ʼ�ж��������ؽ��' )
    status_dict = {}
    status_dict['BSPSQN']  = TradeContext.BSPSQN       #�������
    status_dict['BJEDTE']  = TradeContext.BJEDTE       #��������
    status_dict['BCSTAT']  = PL_BCSTAT_ACC             #����

    #=====�ж��������ؽ��====
    if TradeContext.errorCode != '0000':
        status_dict['BDWFLG']  = PL_BDWFLG_FAIL        #ʧ��
        status_dict['STRINFO'] = TradeContext.errorMsg
        #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        status_dict['BDWFLG']  = PL_BDWFLG_SUCC        #�ɹ�
        status_dict['TRDT']    = TradeContext.TRDT     #��������
        status_dict['TLSQ']    = TradeContext.TLSQ     #������ˮ��
        status_dict['MGID']    = TradeContext.MGID     #����������Ϣ
        status_dict['DASQ']    = TradeContext.DASQ     #�������

    #=====�޸��˻��¼��״̬====
    if not rccpsState.setTransState(status_dict):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit�ɹ�')

    #=====�ж��������ؽ��,�Ƿ��������====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow('D011', '�ñ�ҵ�������ˣ��������˻�')
        #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)

    #=====������¼��״̬Ϊ������-������====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '����״̬ʧ��,ϵͳ�Զ��ع�')
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()

    #=====��������====
    TradeContext.ROPRTPNO  =  '20'

    return True
#=====================���׺���================================================
def SubModuleDoTrd():
    AfaLoggerFunc.tradeDebug('>>>��ʼ����AFE���ؽ��')
    status = {}
    status['BSPSQN']  = TradeContext.BSPSQN       #�������
    status['BJEDTE']  = TradeContext.BJEDTE       #��������
    status['BCSTAT']  = PL_BCSTAT_SND             #����
    #=====��ʼ�ж�afe���ؽ��====
    if TradeContext.errorCode != '0000':
         status['BDWFLG']  = PL_BDWFLG_FAIL       #ʧ��
         #==== �ź�����20091216 �˻�ҵ����MFEʧ�ܸ���ԭҵ��״̬=====
         #===========�˻�ҵ��,����ԭ���׹��˴��������==============
         AfaLoggerFunc.tradeInfo(">>>��ʼ����ԭ���׹��˴��������(8509)")
        
         orstat_dict = {}
         orstat_dict['BJEDTE'] = TradeContext.BOJEDT
         orstat_dict['BSPSQN'] = TradeContext.BOSPSQ
         orstat_dict['BCSTAT'] = PL_BCSTAT_HANG
         orstat_dict['BDWFLG'] = PL_BDWFLG_FAIL
         if TradeContext.existVariable('DASQ'):
            orstat_dict['DASQ']   = TradeContext.DASQ
        
         if not rccpsState.setTransState(orstat_dict):
            return False
            
         AfaLoggerFunc.tradeInfo(">>>��������ԭ���׹��˴��������(8509)")
         
    else:
         status['BDWFLG']  = PL_BDWFLG_SUCC       #�ɹ�

    #=====�޸��˻��¼��״̬====
    if not rccpsState.setTransState(status):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit�ɹ�')

    #�ر�� 2008-07-23
    #�˴�������ԭ����״̬Ϊ�˻�,�������ִ���޸�
    ##=====����ԭ��¼״̬Ϊ���˻㣭�ɹ�====
    #if not rccpsState.newTransState(TradeContext.BOJEDT,TradeContext.BOSPSQ,PL_BCSTAT_QTR,PL_BDWFLG_SUCC):
    #    #=====RollBack����====
    #    AfaDBFunc.RollbackSql()
    #    return AfaFlowControl.ExitThisFlow('M999', '����״̬ʧ��,ϵͳ�Զ��ع�')
    #else:
    #    #=====commit����====
    #    AfaDBFunc.CommitSql()

    
    return True
