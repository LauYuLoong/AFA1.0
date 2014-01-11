# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.�������� 3.���Ļ�ִ).��Ʊ�⸶����
#===============================================================================
#   �����ļ�:   TRCC005_1113.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-08-12
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
import AfaAfeFunc
import rccpsDBFunc,rccpsState,rccpsDBTrcc_bilbka,rccpsMap0000Dout_context2CTradeContext
import rccpsMap1113CTradeContext2Dbilbka,rccpsDBFunc,rccpsHostFunc,AfaFlowControl
import rccpsDBTrcc_bilinf

from types import *
from rccpsConst import *

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( "====��ʼ��Ʊ�⸶���մ���====" )

    #=====�ж��Ƿ��ظ�����====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_bilbka.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','�ж��Ƿ��ظ����ģ���ѯ���ҵ��Ǽǲ���ͬ�����쳣')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('��Ʊҵ��Ǽǲ��д�����ͬ����,�ظ�����,������һ����')
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
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ظ�����'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        #=====����afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','�ظ����ģ��˳���������')

    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ��ظ�����")
    

    #=====����ת��====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'
    
    TradeContext.DCFLG = '1'
    TradeContext.HPSTAT= PL_HPSTAT_PAYC     #�⸶ 02
    TradeContext.OPRNO = PL_HPOPRNO_JF
    
    #=====�������ݿ�====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��¼���ݿ����")
    
    bilbka_dict = {}
    if not rccpsMap1113CTradeContext2Dbilbka.map(bilbka_dict):
        return AfaFlowControl.ExitThisFlow("S999","Ϊ��Ʊҵ��Ǽǲ���ֵ�쳣")
        
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǻ�Ʊҵ��Ǽǲ��쳣')
    
    AfaDBFunc.CommitSql()    
    AfaLoggerFunc.tradeInfo(">>>������¼���ݿ����")     
    
    #=====����״̬Ϊ����====
    sstlog   = {}
    sstlog['BSPSQN']   = TradeContext.BSPSQN
    sstlog['BJEDTE']   = TradeContext.BJEDTE
    sstlog['BCSTAT']   = PL_BCSTAT_BNKRCV
    sstlog['BDWFLG']   = PL_BDWFLG_SUCC

    #=====����״̬Ϊ ����-�ɹ� ====
    if not rccpsState.setTransState(sstlog):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit�ɹ�')
        
    #=====���û�Ʊҵ��Ǽǲ�����Ϣ�Ǽǲ�״̬====
    #=====���û�Ʊ״̬Ϊ�⸶====
    AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬Ϊ�⸶")
    
    if not rccpsState.newBilState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_HPSTAT_PAYC):
        return AfaFlowControl.ExitThisFlow("S999","���û�Ʊ״̬�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬Ϊ�⸶")
    
    #=====commit����====
    AfaDBFunc.CommitSql()
    
    #=====���û�Ʊ�⸶���====
    bil_dict = {}
    bil_dict['BILNO']  = TradeContext.BILNO
    bil_dict['BILVER'] = TradeContext.BILVER
    bil_dict['BILRS']  = TradeContext.BILRS
    bil_end = {}
    bil_end['OCCAMT']  = TradeContext.OCCAMT
    bil_end['RMNAMT']  = TradeContext.RMNAMT
    bil_end['PAYBNKCO']= TradeContext.SNDBNKCO
    bil_end['PAYBNKNM']= TradeContext.SNDBNKNM
    
    ret = rccpsDBTrcc_bilinf.update(bil_end,bil_dict)
    if (ret <= 0):
        return AfaFlowControl.ExitThisFlow("S999","���»�Ʊ��Ϣ�쳣")
    AfaDBFunc.CommitSql() 
    
    AfaLoggerFunc.tradeInfo('>>>commit�ɹ�')
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ�ж��Ƿ���ڶ�������")
    
    if float(TradeContext.RMNAMT) != 0.00:
        AfaLoggerFunc.tradeInfo(">>>�ڶ��μ��˸�ֵ����")
        
        TradeContext.ACUR   = '2'   #����ѭ������
        TradeContext.TRFG   = '9'   #ƾ֤�����ʶ'
        TradeContext.I2CETY = ''    #ƾ֤����
        TradeContext.I2TRAM = TradeContext.RMNAMT   #������
        TradeContext.I2SMCD = PL_RCCSMCD_HPJF       #ժҪ����
        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_DYKJQ   #�����˺�
        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_HCHK    #�跽�˺�
        TradeContext.I2REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ  #�����˺�
        
        #=====�����˺�У��λ====
        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2REAC = rccpsHostFunc.CrtAcc(TradeContext.I2REAC,25)
        
    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ���ڶ�������")
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯���������������˲���")
    #=====��֯���ķ�����������====
    TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ #�����˺�
    TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_HCHK     #�跽�˺�
    TradeContext.REAC    =  TradeContext.BESBNO + PL_ACC_NXYDXZ   #�����˺�
  
    #=====�����˺�У��λ====
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
    TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC,25)
    
    TradeContext.HostCode = '8813'
    #�ر�� 20081007
    #TradeContext.NOTE3    = '��������'
    TradeContext.NOTE3    = ''
    TradeContext.RCCSMCD = PL_RCCSMCD_HPJF       #ժҪ����
        
    AfaLoggerFunc.tradeInfo(">>>������֯���������������˲���")
    AfaLoggerFunc.tradeInfo(">>>��ʼ���µǼǲ�״̬") 
    
    #�ر�� 20081007 �ļ���״̬Ϊ�Զ�����
    #TradeContext.BCSTAT  = PL_BCSTAT_ACC    #����
    TradeContext.BCSTAT  = PL_BCSTAT_AUTO    #�Զ�����
    TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #������
    
    #=====����sstlog��״̬��¼====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '����״̬['+TradeContext.BCSTAT+']['+TradeContext.BDWFLG+']ʧ��,ϵͳ�Զ��ع�')
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
    
    AfaLoggerFunc.tradeInfo(">>>�������µǼǲ�״̬") 
    
    return True
#=====================�����д���(�޸���ˮ,��������,����ǰ����)================
def SubModuleDoSnd():
    #=====��ʼ���ֵ丳ֵ====
    AfaLoggerFunc.tradeInfo('>>>�������˺���')
    sst_dict = {}
    sst_dict['BSPSQN']  = TradeContext.BSPSQN            #�������
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BSPSQN=['+TradeContext.BSPSQN+']')
    sst_dict['BJEDTE']  = TradeContext.BJEDTE            #��������
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BJEDTE=['+TradeContext.BJEDTE+']')
    sst_dict['SBAC']    = TradeContext.SBAC              #�跽�˺�
    AfaLoggerFunc.tradeDebug('>>>test by lyl as SBAC=['+TradeContext.SBAC+']')
    sst_dict['NOTE3']   = TradeContext.NOTE3             #��ע3
    AfaLoggerFunc.tradeDebug('>>>test by lyl as NOTE3 =['+TradeContext.NOTE3 +']')
    sst_dict['BJETIM']  = TradeContext.BJETIM            #����ʱ��
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BJETIM=['+TradeContext.BJETIM+']')
    sst_dict['MGID']   = TradeContext.errorCode           #����������Ϣ
    AfaLoggerFunc.tradeDebug('>>>test by lyl as MGID =['+str(sst_dict['MGID']) +']')
    sst_dict['STRINFO']  = TradeContext.errorMsg         #����������Ϣ
    AfaLoggerFunc.tradeDebug('>>>test by lyl as STRINFO =['+str(sst_dict['STRINFO']) +']')
    sst_dict['BETELR']  = TradeContext.BETELR            #��Ա��
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BETELR=['+TradeContext.BETELR+']')
    sst_dict['RBAC']    = TradeContext.RBAC              #�����˺�
    AfaLoggerFunc.tradeDebug('>>>test by lyl as RBAC  =['+TradeContext.RBAC +']')
    sst_dict['BCSTAT']  = PL_BCSTAT_AUTO                 #�Զ����˳ɹ�
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BCSTAT=['+str(sst_dict['BCSTAT']) +']')
    sst_dict['BESBNO']  = TradeContext.BESBNO            #������
    AfaLoggerFunc.tradeDebug('>>>test by lyl as BESBNO=['+TradeContext.BESBNO+']')

    #=====��ʼ�ж��������ؽ��====
    out_context_dict = {}
    if TradeContext.errorCode == '0000':
        if( TradeContext.existVariable('DASQ') and len(TradeContext.DASQ) != 0 ):
            sst_dict['DASQ']    = TradeContext.DASQ              #�������
            AfaLoggerFunc.tradeDebug('>>>test by lyl as DASQ  =['+TradeContext.DASQ +']')
            sst_dict['RBAC']    = TradeContext.REAC              #�����˺�
            AfaLoggerFunc.tradeDebug('>>>test by lyl as RBAC  =['+TradeContext.RBAC +']')
            sst_dict['BCSTAT']  = PL_BCSTAT_HANG                 #�Զ����� 71
            AfaLoggerFunc.tradeDebug('>>>test by lyl as BCSTAT=['+str(sst_dict['BCSTAT']) +']')
            if len(sst_dict['NOTE3']) == 0:
                sst_dict['NOTE3'] = "����������"
        else:
            sst_dict['RBAC']    = TradeContext.RBAC              #�����˺�
            AfaLoggerFunc.tradeDebug('>>>test by lyl as RBAC  =['+TradeContext.RBAC +']')
            sst_dict['BCSTAT']  = PL_BCSTAT_AUTO                 #�Զ����� 70
            AfaLoggerFunc.tradeDebug('>>>test by lyl as BCSTAT=['+str(sst_dict['BCSTAT']) +']')

        sst_dict['BDWFLG']  = PL_BDWFLG_SUCC         #�ɹ�
        AfaLoggerFunc.tradeDebug('>>>test by lyl as BDWFLG=['+str(sst_dict['BDWFLG']) +']')
        sst_dict['TRDT']    = TradeContext.TRDT             #��������
        AfaLoggerFunc.tradeDebug('>>>test by lyl as TRDT  =['+TradeContext.TRDT   +']')
        sst_dict['TLSQ']    = TradeContext.TLSQ             #������ˮ
        AfaLoggerFunc.tradeDebug('>>>test by lyl as TLSQ  =['+TradeContext.TLSQ   +']')
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ɹ�'
    else:
        sst_dict['BDWFLG']  = PL_BDWFLG_FAIL         #ʧ��
        out_context_dict['PRCCO']    = 'RCCI1056'
        out_context_dict['STRINFO']  = '��������'
            
    AfaLoggerFunc.tradeDebug('>>>��ǰҵ��״̬[' + str(sst_dict['BCSTAT']) + ']')
    AfaLoggerFunc.tradeDebug('>>>��ǰ��ת��־[' + str(sst_dict['BDWFLG']) + ']')
    
    #=====����״̬Ϊ ����/����-�ɹ� ====
    if not rccpsState.setTransState(sst_dict):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeDebug('>>>commit�ɹ�')


    #=====��ʼ����ͨѶ��ִ������Ϣ====
    AfaLoggerFunc.tradeInfo('>>>��ʼ��֯ͨѶ��ִ����')

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

    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    return True
#=====================���׺���================================================
def SubModuleDoTrd():
    #=====�ж�afe���ؽ��====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ���ĳɹ�')
    else:
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ����ʧ��')
        
    return True
