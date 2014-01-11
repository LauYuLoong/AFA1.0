# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ������.��̨��������
#=================================================================
#   �����ļ�:   TRCC006_1145.py
#   �޸�ʱ��:   2008-11-05
#   ���ߣ�      ������
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaAfeFunc,AfaDBFunc
import rccpsDBTrcc_mpcbka,rccpsDBTrcc_wtrbka,rccpsState,rccpsDBTrcc_spbsta,rccpsHostFunc,HostContext
import rccpsMap1145CTradeContext2Dmpcbka_dict,rccpsDBTrcc_atcbka,rccpsDBTrcc_sstlog
from types import *
from rccpsConst import *
import time

def SubModuleDoFst():
    #time.sleep(60)
        
    AfaLoggerFunc.tradeInfo("ũ����ϵͳ������.���������(1.���ز���).��̨�������˽���[TRCC006_1145]����")
    
    #=====�ж��Ƿ�Ϊ�ظ�����====
    AfaLoggerFunc.tradeInfo(">>>�ж��Ƿ�Ϊ�ظ�����")

    where_dict = {}
    where_dict = {'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_mpcbka.selectu(where_dict)

    if( record == None ):
        AfaLoggerFunc.tradeDebug(">>>���ҳ����Ǽǲ��쳣,��������,�ȴ����ķ����Զ���������")
        return AfaFlowControl.ExitThisFlow('A099',"���ҳ����Ǽǲ��쳣")
    elif( len(record) > 0 ):    #�ظ�����
        AfaLoggerFunc.tradeDebug(">>>���������ظ�")
    else:
        AfaLoggerFunc.tradeDebug(">>>���ظ�����")
        
        #=====��ʼ�Ǽǹ�̨�����Ǽǲ�====
        AfaLoggerFunc.tradeDebug(">>>��ʼ�Ǽǳ����Ǽǲ�")

        #TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
        TradeContext.ORTRCDAT = TradeContext.TRCDAT

        mpcbka_insert_dict = {}
        if not rccpsMap1145CTradeContext2Dmpcbka_dict.map(mpcbka_insert_dict):
            AfaLoggerFunc.tradeDebug("Ϊ�����Ǽǲ��ֵ丳ֵʧ��")
            return AfaFlowControl.ExitThisFlow('S999','Ϊ�ֵ丳ֵʧ��,��������,�ȴ������Զ�����')
            
        res = rccpsDBTrcc_mpcbka.insertCmt(mpcbka_insert_dict)      
        if( res == -1):
            AfaLoggerFunc.tradeDebug(">>>�Ǽǳ����Ǽǲ�ʧ��")
            return AfaFlowControl.ExitThisFlow('S999','�������ݿ�ʧ��,��������,�ȴ������Զ�����')
        
        #=====commit����====
        AfaDBFunc.CommitSql()

    #=====�����Զ������Ǽǲ��Ƿ���ڼ�¼====
    AfaLoggerFunc.tradeDebug(">>>�ж��Ƿ�����Զ���������")

    atcbka_where = {'ORMFN':TradeContext.MSGFLGNO}
    atcbka_dict  = rccpsDBTrcc_atcbka.selectu(atcbka_where)

    if( len(atcbka_dict) > 0 ):
        #=====����ҵ������Զ���������,���±�����Ϊ����ʧ��,�ظ�����ʧ�ܱ���====
        AfaLoggerFunc.tradeDebug('>>>�Ѵ����Զ���������,�ܾ�����,�ظ��ܾ�����')
        
        #=====Ϊ���س����ɹ����;ܾ���ִ====
        TradeContext.MSGTYPCO = 'SET010'                 #���������
        TradeContext.PRCCO    = 'NN1IA999'               #���ķ�����
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
        TradeContext.STRINFO  = 'ԭ�������Զ�����,�������ٴγ���'               #����

        return True
    else:
        AfaLoggerFunc.tradeDebug('>>>δ���ҵ���Գ������ĵ��Զ���������,���̼���')

    #=====����ԭ�����Ƿ����====
    AfaLoggerFunc.tradeDebug(">>>����ԭ�����Ƿ����")

    where_dict = {'TRCDAT':TradeContext.ORMFN[10:18],'TRCNO':TradeContext.ORTRCNO,'SNDBNKCO':TradeContext.SNDBNKCO}
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)

    if( wtrbka_dict == -1 ):
        AfaLoggerFunc.tradeInfo(">>>����ԭ����ʧ��,ԭҵ��������ˮ��["+str(TradeContext.ORTRCNO)+"]")
        return AfaFlowControl.ExitThisFlow('A099',"����ԭ����ʧ��,��������,�ȴ������Զ�����")
        
    if( len(wtrbka_dict) == 0 ):
        #=====δ���ҵ�ԭ����====
        AfaLoggerFunc.tradeDebug(">>>����ԭ����ʧ��,δ�յ�ԭ����,ֱ�ӻظ��ܾ�����")
     
        #=====Ϊ���س����ɹ����ͳɹ���ִ====
        TradeContext.MSGTYPCO = 'SET010'                 #���������
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
        #�ر��  20081222  �޸�:���δ�ҵ�ԭҵ��,�򷵻ؾܾ�Ӧ��
        TradeContext.PRCCO    = 'NN1IA999'               #���ķ�����
        TradeContext.STRINFO  = '�޴˽���'               #����

        return True
    else:
        #=====����ԭ���׳ɹ�====
        AfaLoggerFunc.tradeInfo(">>>����ԭ���׳ɹ�")

        #=====��ԭ������� ԭ�������ڸ��µ������Ǽǲ���====
        AfaLoggerFunc.tradeInfo('>>>����ԭ�������\ԭ��������')

        mpcbka_where={}
        mpcbka_where['BSPSQN'] = TradeContext.BSPSQN      #�������
        mpcbka_where['BJEDTE'] = TradeContext.BJEDTE      #��������

        mpcbka_dict ={}
        mpcbka_dict['BOJEDT']  = wtrbka_dict['BJEDTE']    #ԭ��������
        mpcbka_dict['BOSPSQ']  = wtrbka_dict['BSPSQN']    #ԭ�������
        mpcbka_dict['BESBNO']  = wtrbka_dict['BESBNO']    #ԭ������
        mpcbka_dict['STRINFO'] = TradeContext.STRINFO     #���� 
        mpcbka_dict['OPRNO']   = PL_TDOPRNO_CX            #ҵ������

        ret = rccpsDBTrcc_mpcbka.update(mpcbka_dict,mpcbka_where)

        if ret <= 0:
            AfaDBFunc.RollBackSql( )
            return AfaFlowControl.ExitThisFlow('S999', "���³����Ǽǲ�ԭ������ź�ԭ���������쳣,��������")
        else:
            AfaDBFunc.CommitSql( )

        AfaLoggerFunc.tradeInfo(">>>�������³����Ǽǲ�ԭ�������ں�ԭ�������")
        
        #=====����ԭ����ҵ��ҵ��״̬====
        AfaLoggerFunc.tradeInfo(">>>����ԭҵ��״̬")

        spbsta_where = {'BJEDTE':wtrbka_dict['BJEDTE'],'BSPSQN':wtrbka_dict['BSPSQN']}
        spbsta_dict = rccpsDBTrcc_spbsta.selectu(spbsta_where)

        if( spbsta_dict == None ):
            AfaLoggerFunc.tradeDebug(">>>����ԭҵ��״̬ʧ��,��������ʧ�ܱ���")
     
            #=====Ϊ���س����ɹ����;ܾ���ִ====
            TradeContext.MSGTYPCO = 'SET010'                 #���������
            TradeContext.PRCCO    = 'RCCO1006'               #���ķ�����
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
            TradeContext.STRINFO  = '�����д���ʧ��'         #����

            return True
            
        #�ر��  20081226  ������ѯ���׵�ǰ״̬��ϸ��Ϣ
        #��ѯ���׵�ǰ״̬��ϸ��Ϣ
        sstlog_where = {'BJEDTE':wtrbka_dict['BJEDTE'],'BSPSQN':wtrbka_dict['BSPSQN'],'BCURSQ':spbsta_dict['BCURSQ']}
        spbsta_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where)
        
        if( spbsta_dict == None ):
            AfaLoggerFunc.tradeDebug(">>>����ԭҵ��״̬ʧ��,��������ʧ�ܱ���")
     
            #=====Ϊ���س����ɹ����;ܾ���ִ====
            TradeContext.MSGTYPCO = 'SET010'                 #���������
            TradeContext.PRCCO    = 'RCCO1006'               #���ķ�����
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
            TradeContext.STRINFO  = '�����д���ʧ��'         #����

            return True
            
        #�ر��  20081226  ���������׵�ǰ״̬Ϊ�Զ��ۿ�,�Զ�����,����,����������״̬,��ֱ�Ӿܾ��˳���
        if (spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTO or spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spbsta_dict['BDWFLG'] == PL_BDWFLG_WAIT:
            #=====Ϊ���س����ɹ����;ܾ���ִ====
            TradeContext.MSGTYPCO = 'SET010'                 #���������
            TradeContext.PRCCO    = 'RCCO1006'               #���ķ�����
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
            TradeContext.STRINFO  = 'ԭ��������״̬δ֪'     #����

            return True
        
        #�ر��  20081226  ���������׵�ǰ״̬Ϊ�Զ��ۿ�,�Զ�����,����,����ʧ��״̬,�����8816��ѯ����״̬
        if (spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTO or spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spbsta_dict['BDWFLG'] == PL_BDWFLG_FAIL:
            AfaLoggerFunc.tradeDebug('>>>����8816���Ҹ�ҵ��[' + wtrbka_dict['BSPSQN'] + ']״̬')

            TradeContext.HostCode = '8816'                   #����������
            TradeContext.OPFG     = '1'                      #��ѯ����
            TradeContext.NBBH     = 'RCC'                    #����ҵ���ʶ
            TradeContext.FEDT     = spbsta_dict['FEDT']      #ԭǰ������
            TradeContext.RBSQ     = spbsta_dict['RBSQ']      #ԭǰ����ˮ��
            TradeContext.DAFG     = '1'                      #Ĩ/���˱�־  1:��  2:Ĩ
            TradeContext.BESBNO   = spbsta_dict['BESBNO']    #������
            TradeContext.BETELR   = spbsta_dict['BETELR']    #��Ա��
            
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            #=====������������====
            if TradeContext.errorCode == '0000':
                #�������ѳɹ���������,�޸�ԭ����״̬Ϊ���˳ɹ�
                AfaLoggerFunc.tradeInfo("�������ѳɹ���������,�޸�ԭ����״̬Ϊ���˳ɹ�")
                stat_dict = {}
                stat_dict['BJEDTE'] = spbsta_dict['BJEDTE']
                stat_dict['BSPSQN'] = spbsta_dict['BSPSQN']
                stat_dict['BCSTAT'] = spbsta_dict['BCSTAT']
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['TRDT']   = HostContext.O1DADT           #��������
                stat_dict['TLSQ']   = HostContext.O1AMTL           #������ˮ
                stat_dict['MGID']   = '0000'
                stat_dict['STRINFO']= '�����ɹ�'
                
                if not rccpsState.setTransState(stat_dict):
                    return AfaFlowControl.ExitThisFlow('S999','����ԭ����ҵ��״̬Ϊ���˳ɹ��쳣')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                    
                #���²�ѯ������״̬
                spbsta_dict['BDWFLG'] = PL_BDWFLG_SUCC
                spbsta_dict['TRDT']   = HostContext.O1DADT
                spbsta_dict['TLSQ']   = HostContext.O1AMTL
            
            elif TradeContext.errorCode == 'XCR0001':
                AfaLoggerFunc.tradeInfo(">>>��������ԭ���׼���ʧ��,��������")
                
            else:
                AfaLoggerFunc.tradeInfo(">>>��ѯԭ��������״̬�쳣,���ؾܾ�Ӧ��")
                #=====Ϊ���س����ɹ����;ܾ���ִ====
                TradeContext.MSGTYPCO = 'SET010'                 #���������
                TradeContext.PRCCO    = 'RCCO1006'               #���ķ�����
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
                TradeContext.STRINFO  = 'ԭ��������״̬δ֪'     #����
                
                return True

        #=====���������ʱ�ʶ���г���״̬�ж�====
        if( wtrbka_dict['BRSFLG'] == PL_BRSFLG_RCV ):
            #=====����ҵ��====
            AfaLoggerFunc.tradeDebug(">>>����ҵ��")

            #=====PL_BCSTAT_AUTOPAY  �Զ��ۿ�====
            #=====PL_BCSTAT_AUTO     �Զ�����====
            #=====PL_BCSTAT_CONFPAY   ȷ�ϸ���====
            #=====PL_BCSTAT_CONFACC   ȷ������====
            #=====PL_BCSTAT_MFERFE   �ܾ�====
            #=====PL_BCSTAT_CANC     ����====
            #=====PL_BCSTAT_CANCEL   ����====
            if( ((spbsta_dict['BCSTAT']==PL_BCSTAT_AUTO or spbsta_dict['BCSTAT']==PL_BCSTAT_AUTOPAY) and spbsta_dict['BDWFLG']==PL_BDWFLG_FAIL) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_MFERFE and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC   and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CONFPAY and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CONFACC and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC)):
                #=====���������====
                AfaLoggerFunc.tradeDebug(">>>ԭҵ��["+str(spbsta_dict['BSPSQN'])+"]����ʧ�ܻ򱻾ܾ�,���ͳɹ�����")

                #=====���ݽ���״̬��������-�ɹ�״̬====
                if spbsta_dict['BCSTAT'] not in (PL_BCSTAT_MFERFE,PL_BCSTAT_CANC,PL_BCSTAT_CANCEL):
                    #=====����ԭҵ��״̬Ϊ����-�ɹ�====
                    AfaLoggerFunc.tradeDebug('>>>����ԭҵ��״̬Ϊ����-�ɹ�')

                    if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_SUCC):
                        AfaDBFunc.RollBackSql()
                        return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ����-�ɹ��쳣')
                    else:
                        AfaDBFunc.CommitSql()
                else:
                    AfaLoggerFunc.tradeDebug('>>>ԭҵ��״̬Ϊ[�ܾ�/����/����],����Ҫ����״̬')
    
                #=====Ϊ���س����ɹ����;ܾ���ִ====
                TradeContext.MSGTYPCO = 'SET010'                 #���������
                TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
                TradeContext.STRINFO  = 'ԭҵ������ɹ�'         #����

                return True
            else:
        
                #=====ֱ�ӵ���8820����ԭҵ��====
                status={}
                if not rccpsState.getTransStateCur(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],status):
                    return AfaFlowControl.ExitThisFlow('S999','ȡԭҵ��������ˮ�ź�����ʧ��,��������')

                TradeContext.BOSPSQ   = status['RBSQ']    #ԭ�������
                TradeContext.BOJEDT   = status['FEDT']    #ԭ��������
                TradeContext.HostCode = '8820'                   #����������
                
                #=====����ԭҵ��״̬Ϊ����-������====
                AfaLoggerFunc.tradeDebug('>>>����ԭҵ��״̬Ϊ����-������')

                if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
                    AfaDBFunc.RollBackSql()
                    return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ����-�������쳣')
                else:
                    AfaDBFunc.CommitSql()

                #=====����������8820Ĩ�˴���==== 
                AfaLoggerFunc.tradeDebug('>>>����������8820Ĩ�˴���')

                rccpsHostFunc.CommHost( TradeContext.HostCode ) 

                #=====�ж���������====
                sstlog_dict={}
                sstlog_dict['BJEDTE']  =  spbsta_dict['BJEDTE']
                sstlog_dict['BSPSQN']  =  spbsta_dict['BSPSQN']
                sstlog_dict['BCSTAT']  =  PL_BCSTAT_CANC
                sstlog_dict['MGID']    =  TradeContext.errorCode #����������
                if TradeContext.existVariable('BOJEDT'):           #ǰ������
                    sstlog_dict['FEDT'] = TradeContext.BOJEDT
                if TradeContext.existVariable('BOSPSQ'):           #ǰ����ˮ��
                    sstlog_dict['RBSQ'] = TradeContext.BOSPSQ
                if TradeContext.existVariable('TRDT'):           #��������
                    sstlog_dict['TRDT'] = TradeContext.TRDT
                if TradeContext.existVariable('TLSQ'):           #������ˮ��
                    sstlog_dict['TLSQ'] = TradeContext.TLSQ

                #�ر��  20090219  ���ӳ����ɹ��������������ж�:SXR0010(�˱ʽ����ѱ�����)
                if TradeContext.errorCode in ('0000','SXR0010'):
                    #=====����״̬====
                    sstlog_dict['BDWFLG']    =  PL_BDWFLG_SUCC       #��ת��ʶ PL_BDWFLG_SUCC �ɹ�
                    sstlog_dict['STRINFO']   =  '���˳����ɹ�'       #����
                    TradeContext.PRCCO       =  'RCCI0000'
                    TradeContext.STRINFO     =  'ԭҵ������ɹ�'
                else:
                    sstlog_dict['BDWFLG']    =  PL_BDWFLG_FAIL       #��ת��ʶ PL_BDWFLG_FAIL ʧ��
                    sstlog_dict['MGID']      =  TradeContext.errorCode #����������
                    sstlog_dict['STRINFO']   =  TradeContext.errorMsg  #����������Ϣ
                    TradeContext.PRCCO       =  'NN1IA999'
                    TradeContext.STRINFO     =  'ԭҵ�����ʧ�� ' + TradeContext.errorMsg

                #=====�޸�ԭҵ��״̬====
                AfaLoggerFunc.tradeDebug('>>>�޸�ԭҵ��״̬')

                res = rccpsState.setTransState(sstlog_dict)

                if( res == False ):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099', '���ı������Ľ���״̬ʧ��')

                AfaDBFunc.CommitSql( )
                
                #�ر�� 20081226  �޸��������ʧ����ع�����ǰ״̬
                if TradeContext.errorCode not in ('0000','SXR0010'):
                    #����ʧ��,�ع�״̬Ϊ����ǰ״̬
                    if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],spbsta_dict['BCSTAT'],spbsta_dict['BDWFLG']):
                        AfaDBFunc.RollBackSql()
                        return AfaFlowControl.ExitThisFlow('S999','�ع�״̬Ϊ����ǰ״̬�쳣')
                    else:
                        AfaDBFunc.CommitSql()
                        
                    sstlog_dict = {}
                    sstlog_dict['BJEDTE']    =  spbsta_dict['BJEDTE']
                    sstlog_dict['BSPSQN']    =  spbsta_dict['BSPSQN']
                    sstlog_dict['BCSTAT']    =  spbsta_dict['BCSTAT']
                    sstlog_dict['BDWFLG']    =  spbsta_dict['BDWFLG']
                    sstlog_dict['NOTE3']     =  'ԭҵ�����ʧ��,�ع�Ϊ����ǰ״̬'
                    if spbsta_dict.has_key('FEDT'):           #ǰ������
                        sstlog_dict['FEDT']  =  spbsta_dict['FEDT']
                    if spbsta_dict.has_key('RBSQ'):           #ǰ����ˮ��
                        sstlog_dict['RBSQ']  =  spbsta_dict['RBSQ']
                    if spbsta_dict.has_key('TRDT'):           #��������
                        sstlog_dict['TRDT']  =  spbsta_dict['TRDT']
                    if spbsta_dict.has_key('TLSQ'):           #������ˮ��
                        sstlog_dict['TLSQ']  =  spbsta_dict['TLSQ']
                    sstlog_dict['MGID']      =  spbsta_dict['MGID'] #����������
                    sstlog_dict['STRINFO']   =  spbsta_dict['STRINFO']  #����������Ϣ
                    
                    if not rccpsState.setTransState(sstlog_dict):
                        return AfaFlowControl.ExitThisFlow('S999','�ع�״̬Ϊ����ǰ״̬��ϸ��Ϣ�쳣')
                    else:
                        AfaDBFunc.CommitSql()

                #=====���ͻ�ִ====
                AfaLoggerFunc.tradeDebug('>>>���ͳɹ���ִ���Է���')
           
                #=====Ϊ���س����ɹ����ͳɹ���ִ====
                TradeContext.MSGTYPCO = 'SET010'                 #���������
                #TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
                #TradeContext.STRINFO  = 'ԭҵ������ɹ�'         #����
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
        else:
            #=====����ҵ��====
            AfaLoggerFunc.tradeDebug(">>>����ҵ��")

            #=====���ͻ�ִ====
            AfaLoggerFunc.tradeDebug('>>>���ͳɹ���ִ���Է���')
           
            #=====Ϊ���س����ɹ����ͳɹ���ִ====
            TradeContext.MSGTYPCO = 'SET010'                 #���������
            TradeContext.PRCCO    = 'RCCO1006'               #���ķ�����
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
            TradeContext.STRINFO  = '����ҵ��ֻ����������'     #����

    AfaLoggerFunc.tradeInfo("ũ����ϵͳ������.���������(1.���ز���).��̨�������˽���[TRCC006_1145]�˳�")
    
    return True
                         

def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo("ũ����ϵͳ������.���������(2.���Ļ�ִ).��̨�������˽���[TRCC006_1145]����")
    AfaLoggerFunc.tradeInfo("errorCodeΪ��" + TradeContext.errorCode)
    
    #=====�ж�afe���ؽ��====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ���ĳɹ�')
    else:
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ����ʧ��')
    
    AfaLoggerFunc.tradeInfo("���׺���  �˳�")
    
    AfaLoggerFunc.tradeInfo("ũ����ϵͳ������.���������(2.���Ļ�ִ).��̨�������˽���[TRCC006_1145]�˳�")
    
    return True                                 
