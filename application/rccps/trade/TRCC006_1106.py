# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).��������Ӧ���Ľ���
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-24
#   ��    �ܣ�  ���ճ��������Ӧ���޸ĵǼǲ���ԭ��¼״̬
################################################################################
#   �޸���  :   �ر��
#   �޸�����:   �޸ĵǼ����ݿ�
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_ztcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1107CTradeContext2Dztcbka
import rccpsMap1106CTradeContext2Dtrccan_dict,rccpsDBTrcc_trccan,rccpsDBFunc,rccpsState,time
import rccpsDBTrcc_trcbka,rccpsHostFunc
#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    time.sleep(10)
    AfaLoggerFunc.tradeInfo('>>>���볷��Ӧ�����')
    #==========�ж��Ƿ��ظ�����,������ظ�����,ֱ�ӽ�����һ����================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    trccan_where_dict = {}
    trccan_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    trccan_where_dict['TRCDAT']   = TradeContext.TRCDAT
    trccan_where_dict['TRCNO']    = TradeContext.TRCNO

    trc_dict = rccpsDBTrcc_trccan.selectu(trccan_where_dict)

    if trc_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ������쳣")

    if len(trc_dict) > 0:
        AfaLoggerFunc.tradeInfo("��Ҳ�ѯ�鸴���ɸ�ʽ�Ǽǲ��д�����ͬ�鸴����,�˱���Ϊ�ظ�����,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
        #======ΪͨѶ��ִ���ĸ�ֵ===============================================
        out_context_dict = {}
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
        out_context_dict['STRINFO']  = '�ظ�����'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #�����Ա�к�

        return True

    AfaLoggerFunc.tradeInfo(">>>��������Ƿ��ظ�����")

    #==========���ݷ����к�,ί������,������ˮ�Ų�ѯԭ������Ϣ===========
    AfaLoggerFunc.tradeInfo(">>>��ʼ���ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")
    dict_where = {}
    dict_where['SNDBNKCO']  = TradeContext.OQTSBNK
    dict_where['TRCDAT']    = TradeContext.OCADAT
    dict_where['TRCNO']     = TradeContext.OCATNO

    dict = rccpsDBTrcc_trccan.selectu(dict_where)
    if dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ������쳣")

    tran_dict_where = {}
    tran_dict_where['BJEDTE']  =  dict['BOJEDT']
    tran_dict_where['BSPSQN']  =  dict['BOSPSQ']

    tran_dict = rccpsDBTrcc_trcbka.selectu(tran_dict_where)
    if tran_dict <= 0:
        return AfaFlowControl.ExitThisFlow("S999","δ�ҵ�ԭ����")

    AfaLoggerFunc.tradeInfo(">>>�������ݷ����к�,ί������,������ˮ�Ų�ѯ������Ϣ")

    #=====��TradeContext���ֵ�trccan_dict��ֵ====
    TradeContext.BBSSRC  =  tran_dict['BBSSRC']
    TradeContext.BOJEDT  =  dict['BJEDTE']
    TradeContext.BOSPSQ  =  dict['BSPSQN']
    TradeContext.ORTRCCO =  dict['TRCCO']
    TradeContext.CUR     =  '01'
    TradeContext.OCCAMT  =  str(dict['OCCAMT'])

    AfaLoggerFunc.tradeDebug('>>>�ʽ���Դ['+TradeContext.BBSSRC+']')

    trccan_dict = {}
    if not rccpsMap1106CTradeContext2Dtrccan_dict.map(trccan_dict):
        return AfaFlowControl.ExitThisFlow('S999','��ֵ����')

    #=====����Ǽǲ�rcc_trccan====
    AfaLoggerFunc.tradeDebug('>>>��ʼ�������ݿ�')
    ret = rccpsDBTrcc_trccan.insertCmt(trccan_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999','�������ݿ⳷������Ǽǲ�trccan����,��������') 

    #=====����ԭ��������״̬====
    trc_update = {}
    trc_update_where = {}
    trc_update_where['BJEDTE'] = TradeContext.BOJEDT
    trc_update_where['BSPSQN'] = TradeContext.BSPSQN
    trc_update['CLRESPN']= TradeContext.CLRESPN
    ret = rccpsDBTrcc_trccan.updateCmt(trc_update,trc_update_where)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999','�޸ĳ�������Ǽǲ�ԭ��¼״̬����,��������')

    #=====ԭ��ҽ�����ˮ��,8820Ĩ��ʹ��====
    TradeContext.BOJEDT  =  tran_dict['BJEDTE']
    TradeContext.BOSPSQ  =  tran_dict['BSPSQN']

    #=====�жϳ���Ӧ���־�Ƿ�������  0-������  1-�������� ====
    if TradeContext.CLRESPN  ==  '1':
        #=====���ͽ���������ִ====
        AfaLoggerFunc.tradeDebug('>>>���Ĳ�������,���ͳɹ���ִ')
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
        return True

    AfaLoggerFunc.tradeDebug('>>>����������,�������������')

    #=====����sstlog����ԭ��¼״̬Ϊ��Ĩ��-������====
    TradeContext.BCSTAT  = PL_BCSTAT_HCAC
    TradeContext.BDWFLG  = PL_BDWFLG_WAIT

    if not rccpsState.newTransState(dict['BOJEDT'],dict['BOSPSQ'],TradeContext.BCSTAT,TradeContext.BDWFLG):
        return AfaFlowControl.ExitThisFlow('S999','����״̬����,�����˱���')
    
    #=====commit����====
    AfaDBFunc.CommitSql()


    AfaLoggerFunc.tradeDebug('>>>��ʼ�������ӿڸ�ֵ')
    #=====������������/Ĩ������====
    if TradeContext.BBSSRC == '3':
        #=====������Ҫ����8813�����ּ���====
        TradeContext.HostCode = '8813'
        TradeContext.RCCSMCD = '614'                                      #������
        TradeContext.DASQ    = ''
        TradeContext.RVFG    = '0'                                        #�����ֱ�־ 0
        #�ر�� 20080728 �޸�Ĩ�˹���ԭ��
        #TradeContext.NOTE3   = '��������������ּ��˳���'
        TradeContext.NOTE3   = '����������,�Զ�Ĩ��'
        TradeContext.RBAC    =  TradeContext.BESBNO  +  PL_ACC_NXYDXZ     #�����˺�
        TradeContext.SBAC    =  TradeContext.BESBNO  +  PL_ACC_NXYDQSWZ   #�跽�˺�
        #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
        AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
    else:
        TradeContext.HostCode = '8820'
        
        #�ر�� 20080728 �޸�Ĩ�˹���ԭ��
        #TradeContext.NOTE3   = '����������Ĩ��'
        TradeContext.NOTE3   = '����������,�Զ�Ĩ��'

    AfaLoggerFunc.tradeDebug('>>>����sstlog����ԭ����״̬�ɹ�,��ʼ���½���״̬')
    #=====����sstlog��־״̬Ϊ:Ĩ��-������====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
        return AfaFlowControl.ExitThisFlow('S999','����״̬����,�����˱���')
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()

    AfaLoggerFunc.tradeDebug('>>>��ʼ������������')
    AfaLoggerFunc.tradeDebug('>>>�������״���['+TradeContext.HostCode+']')
    #=====����������Ĩ�˲���====
    rccpsHostFunc.CommHost(TradeContext.HostCode)
   
    #=====�ж��������ؽ������״̬====
    sstlog_dict = {}
    sstlog_dict['BJEDTE'] = TradeContext.BJEDTE
    AfaLoggerFunc.tradeDebug('>>>��������['+TradeContext.BJEDTE+']')
    sstlog_dict['BSPSQN'] = TradeContext.BSPSQN
    AfaLoggerFunc.tradeDebug('>>>�������['+TradeContext.BSPSQN+']')
    sstlog_dict['BCSTAT']  = TradeContext.BCSTAT
    AfaLoggerFunc.tradeDebug('>>>ҵ��״̬['+TradeContext.BCSTAT+']')
    sstlog_dict['NOTE4']  = TradeContext.errorMsg
    AfaLoggerFunc.tradeDebug('>>>����������Ϣ['+TradeContext.errorMsg+']')
    sstlog_dict['NOTE3']   = TradeContext.NOTE3
    AfaLoggerFunc.tradeDebug('>>>NOTE3['+TradeContext.NOTE3+']')
    AfaLoggerFunc.tradeDebug('>>>errorCode['+TradeContext.errorCode+']')
    if TradeContext.existVariable('TRDT'):
        sstlog_dict['TRDT']   = TradeContext.TRDT
        AfaLoggerFunc.tradeDebug('>>>��������['+TradeContext.TRDT+']')
    if TradeContext.existVariable('TLSQ'):
        sstlog_dict['TLSQ']   = TradeContext.TLSQ
        AfaLoggerFunc.tradeDebug('>>>������ˮ['+TradeContext.TLSQ+']')

    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeDebug('>>>����')

        if TradeContext.HostCode == '8813':
            sstlog_dict['DASQ']   = TradeContext.DASQ
            AfaLoggerFunc.tradeDebug('>>>�������['+TradeContext.DASQ+']')
            sstlog_dict['SBAC']   = TradeContext.SBAC
            AfaLoggerFunc.tradeDebug('>>>�跽�˺�['+TradeContext.SBAC+']')
            sstlog_dict['RBAC']   = TradeContext.RBAC
            AfaLoggerFunc.tradeDebug('>>>�����˺�['+TradeContext.RBAC+']')

        AfaLoggerFunc.tradeDebug('>>>����2')
        sstlog_dict['BDWFLG'] = PL_BDWFLG_SUCC
    else:
        AfaLoggerFunc.tradeDebug('>>>����1')
        sstlog_dict['BDWFLG'] = PL_BDWFLG_FAIL

    AfaLoggerFunc.tradeDebug('>>>����������Ϣ')
    #=====����ԭ����״̬====
    if not rccpsState.setTransState(sstlog_dict):
        return AfaFlowControl.ExitThisFlow('S999','��������������Ϣ����,��������')
    
    #=====commit����====
    AfaDBFunc.CommitSql()

    #=====���ý���״̬====
    sstlog_dict['BJEDTE']  = TradeContext.BOJEDT
    sstlog_dict['BSPSQN']  = TradeContext.BOSPSQ

    if not rccpsState.setTransState(sstlog_dict):
        return AfaFlowControl.ExitThisFlow('S999','��������������Ϣ����,��������')
    
    #=====commit����====
    AfaDBFunc.CommitSql()


    #=====���ͻ�ִ,��������====
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
    
    return True
#=====================���׺���================================================
def SubModuleDoSnd():
    #=====�ж�afe���ؽ��====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True
