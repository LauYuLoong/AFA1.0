# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���Ļ�ִ).����ֹ�� 
#===============================================================================
#   �����ļ�:   TRCC006_1130.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-26
#   ��    �ܣ�  ����ֹ��������գ��ж��Ƿ����ֹ��������ֹ��ʱ���������˻㱨��
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,AfaAfeFunc,rccpsMap0000Dout_context2CTradeContext,rccpsHostFunc
import rccpsDBTrcc_existp,rccpsMap1130CTradeContext2Dexistp


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    #=====�ж��Ƿ��ظ�����====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_existp.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','�ж��Ƿ��ظ����ģ���ѯ���ҵ��Ǽǲ���ͬ�����쳣')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('����ֹ��ҵ��Ǽǲ��д�����ͬ����,�ظ�����,������һ����')
        #=====ΪͨѶ��ִ���ĸ�ֵ====
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
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = trc_dict['TRCCO']
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ظ�����'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        #=====����afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','�ظ����ģ��˳���������')

    #=====���ݷ����к�,ί������,������ˮ�Ų�ѯԭ������Ϣ===========
    AfaLoggerFunc.tradeInfo(">>>��ʼ���ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")
    trc_dict = {}
    if not rccpsDBFunc.getTransTrcPK(TradeContext.SNDMBRCO,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,trc_dict):
        return AfaFlowControl.ExitThisFlow('S999','���ҵ��Ǽǲ����޴˽���,��������') 

    AfaLoggerFunc.tradeInfo(">>>�������ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")

    #=====��Ҫ�������ֹ��ҵ��Ǽǲ�existp====
    existp = {}
    if not rccpsMap1130CTradeContext2Dexistp.map(existp):
        return AfaFlowControl.ExitThisFlow('S999','�ֵ丳ֵ����,��������')

    existp['BOJEDT']  =  trc_dict['BJEDTE']
    existp['BOSPSQ']  =  trc_dict['BSPSQN']
    existp['CUR']     =  '01'
    
    #=====�ź� 20091203 ���� �������䵽ԭ���׻��� ====
    existp['BESBNO']     =  trc_dict['BESBNO']
    
    ret = rccpsDBTrcc_existp.insertCmt(existp)
    if ret < 0:
        return AfaFlowControl.ExitThisflow('S999','����ֹ��ҵ��Ǽǲ�����,��������')

    #======���ԭҵ��״̬�Ƿ�Ϊ�Զ����ˣ��ɹ�====
    #if not (trc_dict['BCSTAT'] != PL_BCSTAT_HANG and trc_dict['BDWFLG'] != PL_BDWFLG_SUCC ):
    if (trc_dict['BCSTAT'] != PL_BCSTAT_HANG or trc_dict['TRCCO'][:2] != '20' or trc_dict['TRCCO'] == '2000009'):
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
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = trc_dict['TRCCO']
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ñ�ҵ�������ˣ��������˻�'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #�����Ա�к�

        #=====����afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','�ظ����ģ��˳���������')

    TradeContext.BOSPSQ   = trc_dict['BSPSQN']
    TradeContext.BOJEDT   = trc_dict['BJEDTE']
    TradeContext.ORPYRACC = trc_dict['PYRACC']
    TradeContext.ORPYRNAM = trc_dict['PYRNAM']
    TradeContext.ORPYEACC = trc_dict['PYEACC']
    TradeContext.ORPYENAM = trc_dict['PYENAM']
    TradeContext.ORTRCCO  = trc_dict['TRCCO']

    #=====���ҵ��Ǽǲ�trcbka��ֵ����һ����¼====
    trc_dict['BOJEDT']  =  trc_dict['BJEDTE']
    trc_dict['BOSPSQ']  =  trc_dict['BSPSQN']
    trc_dict['ORTRCDAT']=  trc_dict['TRCDAT']
    trc_dict['ORTRCNO'] =  trc_dict['TRCNO']
    trc_dict['ORTRCCO'] =  trc_dict['TRCCO']
    trc_dict['TRCCO']   =  '2000004'
    trc_dict['OPRNO']   =  '09'
    trc_dict['DCFLG']   =  PL_DCFLG_CRE
    trc_dict['BJEDTE']  =  TradeContext.BJEDTE
    trc_dict['BSPSQN']  =  TradeContext.BSPSQN
    trc_dict['TRCDAT']  =  TradeContext.TRCDAT
    trc_dict['TRCNO']   =  TradeContext.SerialNo
    trc_dict['BRSFLG']  =  PL_BRSFLG_SND                  #����
    trc_dict['BBSSRC']  =  '3'                            #������
    #=====���ճ�Ա�к��뷢�ͳ�Ա�кŻ���====
    TradeContext.temp   =  trc_dict['SNDMBRCO']
    trc_dict['SNDMBRCO']=  trc_dict['RCVMBRCO']
    trc_dict['RCVMBRCO']=  TradeContext.temp 

    #=====�����к��뷢���кŻ���====
    TradeContext.temp   =  trc_dict['SNDBNKCO']
    trc_dict['SNDBNKCO']=  trc_dict['RCVBNKCO']
    trc_dict['RCVBNKCO']=  TradeContext.temp 

    #=====���������뷢����������====
    TradeContext.temp   =  trc_dict['SNDBNKNM']
    trc_dict['SNDBNKNM']=  trc_dict['RCVBNKNM']
    trc_dict['RCVBNKNM']=  TradeContext.temp 

    #=====��ʼ�������ݿ�====
    if not rccpsDBFunc.insTransTrc(trc_dict):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D002', '�������ݿ����,RollBack�ɹ�')
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('������ҵ��Ǽǲ���COMMIT�ɹ�')

    #=====����״̬Ϊ����-������====
    sstlog   = {}
    sstlog['BSPSQN']   = TradeContext.BSPSQN
    sstlog['BJEDTE']   = TradeContext.BJEDTE
    sstlog['BCSTAT']   = PL_BCSTAT_ACC
    sstlog['BDWFLG']   = PL_BDWFLG_WAIT

    if not rccpsState.setTransState(sstlog):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit�ɹ�')

    #=====��ʼƴ������˺�====
    TradeContext.DASQ  = trc_dict['DASQ']
    TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ
    TradeContext.OCCAMT= TradeContext.OROCCAMT
    TradeContext.HostCode = '8813'

    #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
    AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
 
    rccpsHostFunc.CommHost(TradeContext.HostCode)

    AfaLoggerFunc.tradeInfo( '>>>��ʼ�ж��������ؽ��' )
    status_dict = {}
    status_dict['BSPSQN']  = TradeContext.BSPSQN       #�������
    status_dict['BJEDTE']  = TradeContext.BJEDTE       #��������
    status_dict['BCSTAT']  = PL_BCSTAT_ACC             #����

    #=====�ж��������ؽ��====
    if TradeContext.errorCode != '0000':
        status_dict['BDWFLG']  = PL_BDWFLG_FAIL        #ʧ��
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
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.TRCDAT
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.ORTRCCO 
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ñ�ҵ�������ˣ��������˻�'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #�����Ա�к�

        #=====����afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','�ñ�ҵ���ѱ����������������˻�')

    #=====������¼��״̬Ϊ������-������====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '����״̬ʧ��,ϵͳ�Զ��ع�')
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()

    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.TRCDAT
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.ORTRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '�ɹ�'

    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

    TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #�����Ա�к�

    return True
#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeDebug('>>>��ʼ����AFE���ؽ��')
    status = {}
    status['BSPSQN']  = TradeContext.BSPSQN       #�������
    status['BJEDTE']  = TradeContext.BJEDTE       #��������
    status['BCSTAT']  = PL_BCSTAT_SND             #����
    status['STRINFO'] = TradeContext.errorMsg
    #=====��ʼ�ж�afe���ؽ��====
    if TradeContext.errorCode != '0000':
        status['BDWFLG']       = PL_BDWFLG_FAIL       #ʧ��
    else:
        status['BDWFLG']       = PL_BDWFLG_SUCC       #�ɹ�

    #=====�޸��˻��¼��״̬====
    if not rccpsState.setTransState(status):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()

    AfaLoggerFunc.tradeDebug('>>>ͨѶ��ִ����ɹ�')
    
    #=====�����˻㱨��2000004====
    TradeContext.sysType  = 'rccpst'
    TradeContext.TRCCO    = '2000004'
    TradeContext.MSGTYPCO = 'SET005'
    TradeContext.OPRTYPNO =  '20'   #���
    TradeContext.STRINFO  = '�յ�����ֹ��,ϵͳ�Զ��˻�' 
   
    #=====�����к��뷢���кŻ���====
    TradeContext.TEMP     = TradeContext.RCVBNKCO
    TradeContext.RCVBNKCO = TradeContext.SNDBNKCO
    TradeContext.SNDBNKCO = TradeContext.TEMP

    #=====���������뷢����������====
    TradeContext.NAME     = TradeContext.RCVBNKNM
    TradeContext.RCVBNKNM = TradeContext.SNDBNKNM
    TradeContext.SNDBNKNM = TradeContext.NAME

    #=====����afe====
    AfaAfeFunc.CommAfe()

    #=====��ʼ�ж�afe���ؽ��====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        AfaLoggerFunc.tradeDebug('>>>�����˻�ɹ�')

    return True
