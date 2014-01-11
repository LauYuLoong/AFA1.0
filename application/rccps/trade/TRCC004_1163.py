# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.��ִ�����ģ��(1.��ִ����).����Ӧ����
#==============================================================================
#   �����ļ�:   TRCC004_1163.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-12-04
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_atcbka,rccpsDBTrcc_spbsta,rccpsDBTrcc_wtrbka
import rccpsHostFunc,rccpsGetFunc,rccpsUtilTools,AfaAfeFunc

#=====================��ִ���Ի�����(���ز���)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC004_1163]����***' )

    #=====�ж��Ƿ�����Զ���������====
    AfaLoggerFunc.tradeDebug('>>>�ж��Ƿ�����Զ���������')

    atcbka_where={'ORMFN':TradeContext.MSGFLGNO}
    atcbka_dict  = rccpsDBTrcc_atcbka.selectu(atcbka_where)

    if( len(atcbka_dict) > 0 ):
        #=====����ҵ������Զ���������,���±�����Ϊ����ʧ��,�ظ�����ʧ�ܱ���====
        AfaLoggerFunc.tradeDebug('>>>�Ѵ����Զ���������,��������')
        return AfaFlowControl.ExitThisFlow('S999','�����Զ��������ģ���������')
    else:
        AfaLoggerFunc.tradeDebug('>>>δ���ҵ���Բ������ĵ��Զ���������,���̼���')

    #=====�ж�ԭ���������Ƿ����====
    AfaLoggerFunc.tradeDebug('>>>�ж��Ƿ����ԭ��������')

    wtrbka_where={'MSGFLGNO':TradeContext.ORMFN}
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where)

    wtrbka_temp_dict = wtrbka_dict

    if len(wtrbka_dict) <= 0:
        AfaLoggerFunc.tradeDebug('>>>δ�ҵ�ԭ�������ģ��������ģ������κδ���')
        return AfaFlowControl.ExitThisFlow('S999','δ�ҵ�ԭ�������ģ��������ģ������κδ���')
    else:
        AfaLoggerFunc.tradeDebug('>>>�ҵ�ԭ�������ģ��������̴���')

    #=====����ԭҵ��====
    AfaLoggerFunc.tradeDebug('>>>��ѯԭҵ��')

    wtrbka_where={'BJEDTE':wtrbka_dict['NOTE1'],'BSPSQN':wtrbka_dict['NOTE2']}
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where)

    if len(wtrbka_dict) <= 0:
        AfaLoggerFunc.tradeDebug('>>>δ�ҵ�ԭҵ���������ģ������κδ���')
        return AfaFlowControl.ExitThisFlow('S999','δ�ҵ�ԭҵ���������ģ������κδ���')
    else:
        AfaLoggerFunc.tradeDebug('>>>�ҵ�ԭҵ�񣬼������̴���')

    #=====����ԭҵ��״̬====
    AfaLoggerFunc.tradeDebug('>>>����ԭҵ��״̬')

    spb_where = {'BJEDTE':wtrbka_dict['BJEDTE'],'BSPSQN':wtrbka_dict['BSPSQN']}
    spb_dict  = rccpsDBTrcc_spbsta.selectu(spb_where)

    if len(spb_dict) <= 0:
        AfaLoggerFunc.tradeDebug('>>>����ԭҵ��״̬ʧ�ܣ��������ģ������κδ���')
        return AfaFlowControl.ExitThisFlow('S999','����ԭҵ��״̬ʧ�ܣ��������ģ������κδ���')
    else:
        AfaLoggerFunc.tradeDebug('>>>����ԭҵ��״̬�ɹ����������̴���')

    #=====�ж�ԭҵ��״̬�Ƿ�������в�������¼====
    if spb_dict['BCSTAT'] != PL_BCSTAT_CANC and spb_dict['BDWFLG'] != PL_BDWFLG_SUCC:
        AfaLoggerFunc.tradeDebug('>>>ԭҵ��״̬['+str(spbsta_dict['BCSTAT'])+'�����������������ģ������κδ���')
        return AfaFlowControl.ExitThisFlow('S999','ԭҵ�����������������ģ������κδ���')
    else:
        AfaLoggerFunc.tradeDebug('>>>ԭҵ����벹���������̴���')
        
    #=================��Ӧ���Ļظ��ܾ�,������״̬Ϊ�ܾ�,ֹͣ����=============
    if TradeContext.PRCCO != 'RCCI0000':
        AfaLoggerFunc.tradeInfo(">>>�Է����ؾܾ�Ӧ��")
        
        #=============����ҵ��״̬Ϊ�ܾ�������=================================
        
        if not rccpsState.newTransState(wtrbka_temp_dict['BJEDTE'],wtrbka_temp_dict['BSPSQN'],PL_BCSTAT_MFERFE,PL_BDWFLG_SUCC):
            return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�ܾ��������쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
        return AfaFlowControl.ExitThisFlow("S999","�Է��ܾ�,ֹͣ����")
    else:
        AfaLoggerFunc.tradeInfo(">>>�Է����سɹ�Ӧ��")

    #=====���˽ӿ�8813I1��ֵ����====
    TradeContext.HostCode  =  '8813'
    TradeContext.BESBNO    =  wtrbka_dict['BESBNO']          #������
    TradeContext.BETELR    =  wtrbka_dict['BETELR']          #��Ա��
    TradeContext.TERMID    =  wtrbka_dict['TERMID']          #�ն˺�
    TradeContext.BJEDTE    =  wtrbka_dict['BJEDTE']          #��������
    TradeContext.BSPSQN    =  wtrbka_dict['BSPSQN']          #�������

    #=====�жϽ��״��룬����������====
    if TradeContext.ORTRCCO in ('3000002','3000004'):
        #=====ͨ��====
        AfaLoggerFunc.tradeDebug('>>>ͨ��ҵ����')
    elif TradeContext.ORTRCCO in ('3000102','3000104'):
        #=====ͨ��====
        AfaLoggerFunc.tradeDebug('>>>ͨ��ҵ����')

        if( wtrbka_dict['CHRGTYP'] != '1'):
            TradeContext.RCCSMCD  = PL_RCCSMCD_XJTDWZ                     #����ժҪ����
            TradeContext.RBAC =  ''                       #�跽�˻�:�������˻�
            TradeContext.RBNM =  '�ֽ�'                       #�跽���� �����˻���
            TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSWZ     #�����˻�:ũ��������������
            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
            TradeContext.ACNM = 'ũ��������������'                        #��������:
            TradeContext.CTFG =  '7'                                      #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������
            TradeContext.PKFG =  'T'                                      #ͨ��ͨ�ұ�ʶ
            TradeContext.CATR =  '0'                                      #�ֽ�

            AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )

        else:
            #=====ת��====
            TradeContext.ACUR    =  '3'                                           #���˴���
            TradeContext.I3TRAM  =  str(TradeContext.CUSCHRG)                       #������
            TradeContext.I2TRAM  =  str(TradeContext.OCCAMT)                       #������
            TradeContext.OCCAMT  =  rccpsUtilTools.AddDot(TradeContext.OCCAMT,TradeContext.CUSCHRG) #������

            #=========���׽��+������===================
            TradeContext.RCCSMCD    =  PL_RCCSMCD_XJTDWZ                               #ժҪ����
            TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
            TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
            TradeContext.ACNM    =  '������ʱ����'                                #�跽����
            TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
            TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
            TradeContext.OTNM    =  'ũ��������'                                  #��������
            TradeContext.CTFG  = '9'                                              #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������
            TradeContext.PKFG  = 'T'                                              #ͨ��ͨ�ұ�ʶ
            AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
            #=========���׽��============
            TradeContext.I2SMCD  =  PL_RCCSMCD_XJTDWZ                               #ժҪ����
            TradeContext.I2RBAC  =  ''                           #�跽�˺�
            TradeContext.I2ACNM  =  TradeContext.PYRNAM                           #�跽����
            TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
            TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
            TradeContext.I2CTFG  = '7'                                            #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������
            TradeContext.I2PKFG  = 'T'                                            #ͨ��ͨ�ұ�ʶ
            TradeContext.I2CATR =  '0'                                      #�ֽ�
            AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
            AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
            #=========�������������뻧===========
            TradeContext.I3SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
            TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
            TradeContext.I3ACNM  =  TradeContext.PYRNAM                           #�跽����
            TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
            TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
            TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
            TradeContext.I3OTNM  =  '������ʱ����'                                #��������
            TradeContext.I3CTFG  = '8'                                              #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������
            TradeContext.I3PKFG  = 'T'                                              #ͨ��ͨ�ұ�ʶ
            AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I3SBAC )
            AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I3RBAC )

    elif TradeContext.ORTRCCO in ('3000003','3000005'):
        #=====��ת��====
        AfaLoggerFunc.tradeDebug('>>>��ת��ҵ����')
    elif TradeContext.ORTRCCO in ('3000103','3000105'):
        #=====��ת��====
        AfaLoggerFunc.tradeDebug('>>>��ת��ҵ����')

        #=====�ж���������ȡ��ʽ====
        if wtrbka_dict['CHRGTYP'] == '1':
            #=====ת��====
            TradeContext.ACUR    =  '3'                                     #���˴���
            TradeContext.I3TRAM  =  str(TradeContext.CUSCHRG)                      #������ ������
            TradeContext.I2TRAM  =  str(TradeContext.OCCAMT)                       #������ ����
            TradeContext.OCCAMT  =  str(float(TradeContext.OCCAMT) + float(TradeContext.CUSCHRG)) #������
            #=========���׽��+������===================
            TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                              #ժҪ����  PL_RCCSMCD_YZBWZ ��ת��
            TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
            TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
            TradeContext.ACNM    =  'ũ��������'                                  #�跽����
            TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS           #�����˺�
            TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
            TradeContext.OTNM    =  'Ӧ����'                                    #��������
            TradeContext.CTFG  = '9'                                              #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������
            TradeContext.PKFG  = 'T'                                              #ͨ��ͨ�ұ�ʶ
            AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
            #=========���׽��============
            TradeContext.I2SMCD  =  PL_RCCSMCD_YZBWZ                              #ժҪ����
            TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
            TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
            TradeContext.I2ACNM  =  'Ӧ����'                                    #�跽����
            TradeContext.I2RBAC  =  TradeContext.PYEACC                           #�����˺�
            TradeContext.I2OTNM  =  TradeContext.PYENAM                           #��������
            TradeContext.I2CTFG  = '7'                                              #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������
            TradeContext.I2PKFG  = 'T'                                              #ͨ��ͨ�ұ�ʶ
            AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
            AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
            #=========�������������뻧===========
            TradeContext.I3SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
            TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
            TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
            TradeContext.I3ACNM  =  'Ӧ����'                                    #�跽����
            TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
            TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
            TradeContext.I3OTNM  =  '����������'                                  #��������
            TradeContext.I3CTFG  = '8'                                              #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������
            TradeContext.I3PKFG  = 'T'                                              #ͨ��ͨ�ұ�ʶ
        else:
            #=====���շѻ����ֽ�====
            TradeContext.ACUR    =  '1'                                           #���˴���
            TradeContext.RCCSMCD =  PL_RCCSMCD_YZBWZ                                #ժҪ����
            TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
            TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
            TradeContext.RBAC    =  TradeContext.PYEACC                           #�����˺�
            TradeContext.OTNM    =  TradeContext.PYENAM                           #��������
            TradeContext.CTFG  = '7'                                              #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������
            TradeContext.PKFG  = 'T'                                              #ͨ��ͨ�ұ�ʶ
    else:
        #=====ԭ���״������������====
        AfaLoggerFunc.tradeDebug('>>>ԭ���״������������')
        return AfaFlowControl.ExitThisFlow('S999','ԭ���״������������')

    #=====��������ǰ����ˮ��====
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
        return AfaFlowControl.ExitThisFlow('S999','��������ǰ����ˮ��ʧ��,��������')

    #=====modify  by pgt 12-8====
    if wtrbka_temp_dict['DCFLG'] == PL_DCFLG_DEB:
#    if TradeContext.ORTRCCO in ('3000102','3000104','3000103','3000105'):
        #=====ͨ�ҡ���ת��====
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_AUTOPAY,PL_BDWFLG_WAIT):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','�����Զ��ۿ������ʧ�ܣ���������')
        else:
            AfaDBFunc.CommitSql()

        #=====�������������====
        rccpsHostFunc.CommHost( TradeContext.HostCode )

        #=====�ж���������====
        sstlog_dict={}
        sstlog_dict['BJEDTE']  =  TradeContext.BJEDTE
        sstlog_dict['BSPSQN']  =  TradeContext.BSPSQN
        sstlog_dict['BCSTAT']  =  PL_BCSTAT_AUTOPAY
        if TradeContext.errorCode == '0000':
            sstlog_dict['BDWFLG'] =  PL_BDWFLG_SUCC
            sstlog_dict['RBSQ']   =  TradeContext.RBSQ
            sstlog_dict['TLSQ']   =  TradeContext.TLSQ
            sstlog_dict['TRDT']   =  TradeContext.TRDT
            sstlog_dict['MGID']   =  TradeContext.errorCode
            sstlog_dict['STRINFO']=  '�����������˳ɹ�'
            AfaLoggerFunc.tradeInfo('>>>�������˳ɹ�')
        else:
            sstlog_dict['BDWFLG'] =  PL_BDWFLG_FAIL
            sstlog_dict['MGID']   =  TradeContext.errorCode
            sstlog_dict['STRINFO']=  TradeContext.errorMsg
            AfaLoggerFunc.tradeInfo('>>>��������ʧ��')

        if not rccpsState.setTransState(sstlog_dict):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','�޸��Զ��ۿ�ɹ���ʧ�ܣ���������')
        else:
            AfaDBFunc.CommitSql()
    else:
        #====ͨ�桢��ת��====
        AfaLoggerFunc.tradeDebug('>>>����ȷ�ϸ��������')

        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CONFACC,PL_BDWFLG_SUCC):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','����ȷ�ϸ��������ʧ�ܣ���������')
        else:
            AfaDBFunc.CommitSql()

        #=================Ϊ���ȷ����������׼��=================================
        AfaLoggerFunc.tradeInfo(">>>��ʼΪ���ȷ����������׼��")

        #=====================��ȡ������ˮ��====================================
        if rccpsGetFunc.GetRccSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )

        TradeContext.MSGTYPCO = 'SET009'
        TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO
        TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO
        TradeContext.SNDBRHCO = TradeContext.BESBNO
        TradeContext.SNDCLKNO = TradeContext.BETELR
        TradeContext.ORMFN    = TradeContext.ORMFN 
        TradeContext.OPRTYPNO = '30'
        TradeContext.ROPRTPNO = '30'
        TradeContext.TRANTYP  = '0'
        TradeContext.ORTRCCO  = '3000505' 
        TradeContext.ORTRCNO  = TradeContext.TRCNO
        TradeContext.TRCCO    = '3000503'
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.CURPIN   = ""
        TradeContext.STRINFO  = '�յ�����Ӧ��,�Զ����ʹ��ȷ��'

        AfaLoggerFunc.tradeInfo(">>>���״���["+str(TradeContext.TRCCO)+"]")
        AfaLoggerFunc.tradeInfo(">>>����Ϊ���ȷ����������׼��")
 
        #=====����ԭ��¼�Ĵ��ȷ���ֶ�====
        #=====modify by pgt 12-8====
        wtr_up_where = {'BJEDTE':wtrbka_temp_dict['BJEDTE'],'BSPSQN':wtrbka_temp_dict['BSPSQN']}
#        wtr_up_where = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        wtr_end_dict = {}
        wtr_end_dict['COTRCDAT']  = TradeContext.TRCDAT
        wtr_end_dict['COTRCNO']   = TradeContext.TRCNO
        wtr_end_dict['TRCNO']     = TradeContext.ORTRCNO
        wtr_end_dict['COMSGFLGNO']= TradeContext.SNDBNKCO+TradeContext.TRCDAT+TradeContext.TRCNO
        wtr_end_dict['MSGFLGNO']  = TradeContext.MSGFLGNO

        rccpsDBTrcc_wtrbka.update(wtr_end_dict,wtr_up_where)
        AfaDBFunc.CommitSql()

        AfaAfeFunc.CommAfe()
 
        if TradeContext.errorCode == '0000':
            AfaLoggerFunc.tradeInfo('>>>���ͳɹ�')
        else:
            AfaLoggerFunc.tradeInfo('>>>����ʧ��')

    return True
