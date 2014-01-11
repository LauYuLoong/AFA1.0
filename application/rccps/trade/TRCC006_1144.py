# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ������.�Զ���������
#=================================================================
#   �����ļ�:   TRCC006_1144.py
#   �޸�ʱ��:   2008-11-05
#   ���ߣ�      ������
#   ��    ��:   �յ��Զ������Ǽǲ�,����ԭ���״����ж��ǳ���ԭ����
#               ҵ���ǳ������˳�������.
#               �����ԭ����ҵ��,ֱ�ӵ���8820�弴��,ͬ��������
#               ��������˳�������,Ҫ�ж�ԭҵ���Ƿ��ѱ�����,���ԭ
#               ҵ���ѱ�����,��Ҫ����8813���¼���,���ԭҵ����δ��
#               ����,����ԭҵ��״̬�����Ƿ���Ҫ��������״̬����ֱ��
#               ���سɹ�����                
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaAfeFunc,AfaDBFunc,HostContext
import rccpsDBTrcc_atcbka,rccpsDBTrcc_wtrbka,rccpsState,rccpsDBTrcc_spbsta,rccpsHostFunc,rccpsGetFunc
import rccpsMap1144CTradeContext2Datcbka_dict,rccpsDBTrcc_mpcbka,rccpsUtilTools,rccpsDBTrcc_wtrbka
import rccpsEntries,rccpsDBTrcc_sstlog
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("ũ����ϵͳ������.���������(1.���ز���).��̨�������˽���[TRCC006_1144]����")
    AfaLoggerFunc.tradeDebug(">>>BJEDTE==" + TradeContext.BJEDTE)
    AfaLoggerFunc.tradeDebug(">>>BSPSQN==" + TradeContext.BSPSQN)
    #=====�ж��Ƿ�Ϊ�ظ�����====
    AfaLoggerFunc.tradeInfo(">>>�ж��Ƿ�Ϊ�ظ�����")
    
    where_dict = {}
    where_dict = {'MSGFLGNO':TradeContext.MSGFLGNO}

    record = rccpsDBTrcc_atcbka.selectu(where_dict)
    if( record == None ):
        AfaLoggerFunc.tradeDebug(">>>���ҳ����Ǽǲ��쳣,��������,�ȴ��������·����Զ���������")
        return AfaFlowControl.ExitThisFlow('A099',"���ҳ����Ǽǲ��쳣,��������,�ȴ��������·����Զ���������")    
    elif( len(record) > 0 ):    #�ظ�����
        AfaLoggerFunc.tradeDebug(">>>�Զ����������ظ�") 
        #=====Ϊ�����Զ������ɹ����ͳɹ���ִ====
        #TradeContext.MSGTYPCO = 'SET010'                 #���������
        #TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
        #TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
        #TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
        #TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
        #TradeContext.STRINFO  = '�Զ����������ظ�'       #����
        #
        #return True        
        TradeContext.BJEDTE = record['BJEDTE']
        TradeContext.BSPSQN = record['BSPSQN']
    else:       
        #TradeContext.OR_BJEDTE = TradeContext.BJEDTE #Ϊ�������atcbka��ʱ���ֵ丳ֵ
        #TradeContext.OR_BSPSQN = TradeContext.BSPSQN #Ϊ�������atcbka��ʱ���ֵ丳ֵ      
        #=====��ʼ�Ǽ��Զ������Ǽǲ�====
        AfaLoggerFunc.tradeDebug(">>>�Ǽ��Զ������Ǽǲ�")
        
        atcbka_dict = {}
        if not rccpsMap1144CTradeContext2Datcbka_dict.map(atcbka_dict):
            AfaLoggerFunc.tradeDebug(">>>�Զ������Ǽǲ��ֵ丳ֵʧ��,��������,�ȴ��Զ����������´�����")
            return AfaFlowControl.ExitThisFlow('A099',"�Զ������Ǽǲ��ֵ丳ֵʧ��")     
            
        res = rccpsDBTrcc_atcbka.insertCmt(atcbka_dict)      
        if( res == -1):
            AfaLoggerFunc.tradeDebug(">>>�Զ������Ǽǲ���������ʧ��,���ݿ���,��������")
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('A099',"�����Ǽǲ���������ʧ��") 
        else:
            AfaDBFunc.CommitSql()
    
    #=====�ж����������Ƿ���ͬ====
    if TradeContext.NCCWKDAT != TradeContext.NCCworkDate:
        AfaLoggerFunc.tradeDebug(">>>����ԭ����ʧ��,δ�յ�ԭ����,ֱ�ӻظ��ɹ�����")
         
        #=====Ϊ�����Զ������ɹ����ͳɹ���ִ====
        TradeContext.MSGTYPCO = 'SET010'                 #���������
        TradeContext.PRCCO    = 'RCCI0006'               #���ķ�����
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
        TradeContext.STRINFO  = '�������ڲ��Ϸ�'         #����
        
        return True        
            
    #=====�ж�ԭ���״���====
    if TradeContext.ORTRCCO == '3000504':
        #=====3000504 ��̨��������====
        AfaLoggerFunc.tradeDebug('>>>����ԭ����ҵ���Ƿ����')

        mpcbka_where = {'MSGFLGNO':TradeContext.ORMFN}
        record = rccpsDBTrcc_mpcbka.selectu(mpcbka_where)

        if record == None:
            AfaLoggerFunc.tradeDebug('>>>����ԭ����ҵ���쳣,��������,�ȴ������ٴη����Զ�����')
            return AfaFlowControl.ExitThisFlow('S999','��������')
            
        elif len(record) <= 0:
            AfaLoggerFunc.tradeDebug('>>>����ԭ����ҵ���,�ظ��ɹ�')
            #=====Ϊ���س����ɹ����ͳɹ���ִ====
            TradeContext.MSGTYPCO = 'SET010'                 #���������
            TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
            TradeContext.STRINFO  = 'ԭ����ҵ���ѳ����ɹ�'       #����
        
            return True        
            #return AfaFlowControl.ExitThisFlow('S999','��������')
        else:
            AfaLoggerFunc.tradeDebug('>>>���ҳ���ҵ��ɹ�')
            
        #=====��ԭ������� ԭ�������ڸ��µ������Ǽǲ���====
        AfaLoggerFunc.tradeInfo('>>>����ԭ�������\ԭ��������')
        
        atcbka_where={}
        atcbka_where['BJEDTE'] = TradeContext.BJEDTE      #��������
        atcbka_where['BSPSQN'] = TradeContext.BSPSQN      #�������
        
        atcbka_dict ={}
        atcbka_dict['BOJEDT']  = record['BJEDTE']    #ԭ��������
        atcbka_dict['BOSPSQ']  = record['BSPSQN']    #ԭ�������
        atcbka_dict['STRINFO'] = TradeContext.STRINFO     #���� 
        atcbka_dict['ORTRCDAT']= record['TRCDAT']    #ԭί������
        atcbka_dict['BESBNO']  = record['BESBNO']    #ԭ������
        atcbka_dict['OPRNO']   = PL_TDOPRNO_CZ            #ҵ������

        ret = rccpsDBTrcc_atcbka.update(atcbka_dict,atcbka_where)
        AfaLoggerFunc.tradeDebug('>>>ret=='+str(ret))
        if ret <= 0:
            AfaDBFunc.RollbackSql( )
            return AfaFlowControl.ExitThisFlow('S999', "�����Զ������Ǽǲ�ԭ������ź�ԭ���������쳣,��������")
        else:
            AfaDBFunc.CommitSql( )
        
        AfaLoggerFunc.tradeInfo(">>>�������³����Ǽǲ�ԭ�������ں�ԭ�������")

        #=====ͨ�������Ǽǲ�����ԭҵ��====
        AfaLoggerFunc.tradeDebug('>>>ͨ�������Ǽǲ���ԭ������ź�ԭ�������ڲ�ѯԭҵ��')

        wtr_where = {'BJEDTE':record['BOJEDT'],'BSPSQN':record['BOSPSQ']}
        wtr_dict = rccpsDBTrcc_wtrbka.selectu(wtr_where)

        if wtr_dict == None:
            AfaLoggerFunc.tradeDebug('>>>ͨ�������Ǽǲ���ԭ������ź�ԭ�������ڲ�ѯԭ�����쳣,��������,�ȴ������ٴη����Զ�����')
            return AfaFlowControl.ExitThisFlow('S999','��������')
        elif len(wtr_dict) <= 0:
            AfaLoggerFunc.tradeDebug('>>>ͨ�������Ǽǲ���ԭ������ź�ԭ�������ڲ�ѯԭ���װ�,��������,�ȴ������ٴη����Զ�����')
            return AfaFlowControl.ExitThisFlow('S999','��������')
        else:
            AfaLoggerFunc.tradeDebug('>>>����ԭҵ��ɹ�')

        #=====ȡԭҵ���ҵ��״̬====
        AfaLoggerFunc.tradeDebug('>>>ȡԭҵ��ҵ��״̬')

        spb_where = {'BJEDTE':wtr_dict['BJEDTE'],'BSPSQN':wtr_dict['BSPSQN']}
        spb_dict = rccpsDBTrcc_spbsta.selectu(spb_where)

        if spb_dict == None:
            AfaLoggerFunc.tradeDebug('>>>ȡԭҵ��ҵ��״̬�쳣,��������,�ȴ������ٴη����Զ�����')
            return AfaFlowControl.ExitThisFlow('S999','��������')
        elif len(spb_dict) <= 0:
            AfaLoggerFunc.tradeDebug('>>>ȡԭҵ��ҵ��״̬ʧ��,��������,�ȴ������ٴη����Զ�����')
            return AfaFlowControl.ExitThisFlow('S999','��������')
        else:
            AfaLoggerFunc.tradeDebug('>>>ȡԭҵ��ҵ��״̬�ɹ�')

        #�ر��  20081226  ������ѯ���׵�ǰ״̬��ϸ��Ϣ
        #��ѯ���׵�ǰ״̬��ϸ��Ϣ
        sstlog_where = {'BJEDTE':wtr_dict['BJEDTE'],'BSPSQN':wtr_dict['BSPSQN'],'BCURSQ':spb_dict['BCURSQ']}
        spb_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where)
        
        if( spb_dict == None ):
            return AfaFlowControl.ExitThisFlow('S999','ȡԭҵ��ҵ��״̬��ϸ��Ϣ�쳣,��������,�ȴ������ٴη����Զ�����')
        elif len(spb_dict) <= 0:
            return AfaFlowControl.ExitThisFlow('S999','ȡԭҵ��ҵ��״̬��ϸ��Ϣʧ��,��������,�ȴ������ٴη����Զ�����')
        else:
            AfaLoggerFunc.tradeDebug('>>>ȡԭҵ��ҵ��״̬��ϸ��Ϣ�ɹ�')
            
        
        #�ر��  20081226  ���������׵�ǰ״̬Ϊ�Զ��ۿ�,�Զ�����,����,����������״̬,��ֱ�Ӿܾ��˳���
        if (spb_dict['BCSTAT'] == PL_BCSTAT_AUTO or spb_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spb_dict['BCSTAT'] == PL_BCSTAT_CANC or spb_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spb_dict['BDWFLG'] == PL_BDWFLG_WAIT:
            return AfaFlowControl.ExitThisFlow('S999','ԭҵ������״̬δ֪,��������,�ȴ������ٴη����Զ�����')
            
        #�ر��  20081226  ���������׵�ǰ״̬Ϊ�Զ��ۿ�,�Զ�����,����,����ʧ��״̬,�����8816��ѯ����״̬
        if (spb_dict['BCSTAT'] == PL_BCSTAT_AUTO or spb_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spb_dict['BCSTAT'] == PL_BCSTAT_CANC or spb_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spb_dict['BDWFLG'] == PL_BDWFLG_FAIL:
            AfaLoggerFunc.tradeDebug('>>>����8816���Ҹ�ҵ��[' + wtr_dict['BSPSQN'] + ']״̬')

            TradeContext.HostCode = '8816'                   #����������
            TradeContext.OPFG     = '1'                      #��ѯ����
            TradeContext.NBBH     = 'RCC'                    #����ҵ���ʶ
            TradeContext.FEDT     = spb_dict['FEDT']         #ԭǰ������
            TradeContext.RBSQ     = spb_dict['RBSQ']         #ԭǰ����ˮ��
            TradeContext.DAFG     = '1'                      #Ĩ/���˱�־  1:��  2:Ĩ
            TradeContext.BESBNO   = spb_dict['BESBNO']       #������
            TradeContext.BETELR   = spb_dict['BETELR']       #��Ա��
            
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            #=====������������====
            if TradeContext.errorCode == '0000':
                #�������ѳɹ���������,�޸�ԭ����״̬Ϊ���˳ɹ�
                AfaLoggerFunc.tradeInfo("�������ѳɹ���������,�޸�ԭ����״̬Ϊ���˳ɹ�")
                stat_dict = {}
                stat_dict['BJEDTE'] = spb_dict['BJEDTE']
                stat_dict['BSPSQN'] = spb_dict['BSPSQN']
                stat_dict['BCSTAT'] = spb_dict['BCSTAT']
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['TRDT']   = HostContext.O1DADT           #��������
                stat_dict['TLSQ']   = HostContext.O1AMTL           #������ˮ
                stat_dict['MGID']   = '0000'
                stat_dict['STRINFO']= '�����ɹ�'
                
                if not rccpsState.setTransState(stat_dict):
                    return AfaFlowControl.ExitThisFlow('S999','����ԭ����ҵ��״̬Ϊ���˳ɹ��쳣,��������,�ȴ��´γ���') 
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
                    
                #���²�ѯ������״̬
                spb_dict['BDWFLG'] = PL_BDWFLG_SUCC
                spb_dict['TRDT']   = HostContext.O1DADT
                spb_dict['TLSQ']   = HostContext.O1AMTL
            
            elif TradeContext.errorCode == 'XCR0001':
                AfaLoggerFunc.tradeInfo(">>>��������ԭ���׼���ʧ��,��������")
                
            else:
                AfaLoggerFunc.tradeInfo(">>>��ѯԭ��������״̬�쳣,���ؾܾ�Ӧ��")
                
                #�ع�ԭ����������״̬Ϊ����ǰ״̬
                AfaLoggerFunc.tradeInfo(">>>��ʼ�ع�ԭ����������״̬Ϊ����ǰ״̬")
                
                spbsta_dict = {}
                if not rccpsState.getTransStateDes(spb_dict['BJEDTE'],spb_dict['BSPSQN'],spbsta_dict,1):
                    return AfaFlowControl.ExitThisFlow('S999','��ѯԭ���������׳���ǰ״̬�쳣')
                
                if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],spbsta_dict['BCSTAT'],spbsta_dict['BDWFLG']):
                    return AfaFlowControl.ExitThisFlow('S999','�ع�״̬Ϊ����ǰ״̬�쳣')
                else:
                    AfaDBFunc.CommitSql()
                    
                sstlog_dict = {}
                sstlog_dict['BJEDTE']    =  spbsta_dict['BJEDTE']
                sstlog_dict['BSPSQN']    =  spbsta_dict['BSPSQN']
                sstlog_dict['BCSTAT']    =  spbsta_dict['BCSTAT']
                sstlog_dict['BDWFLG']    =  spbsta_dict['BDWFLG']
                sstlog_dict['NOTE3']     =  '�������ױ�����,�ع�Ϊ����ǰ״̬'
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
                    
                AfaLoggerFunc.tradeInfo(">>>�����ع�ԭ����������״̬Ϊ����ǰ״̬")
                
                #=====Ϊ���س����ɹ����;ܾ���ִ====
                TradeContext.MSGTYPCO = 'SET010'                 #���������
                TradeContext.PRCCO    = 'RCCO1006'               #���ķ�����
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
                TradeContext.STRINFO  = 'ԭ��������״̬δ֪'     #����
                
                return True

        #=====�ж�ԭҵ��ҵ��״̬====
        #=====PL_BCSTAT_CANC ����====
        if not (spb_dict['BCSTAT'] == PL_BCSTAT_CANC and spb_dict['BDWFLG'] == PL_BDWFLG_SUCC):
            #=====ԭҵ��δ����,ֱ�ӻظ��ɹ�����====
            AfaLoggerFunc.tradeDebug(">>>ԭ����δ�����ɹ�,�ظ��ɹ�")
         
            #=====Ϊ���س����ɹ����ͳɹ���ִ====
            TradeContext.MSGTYPCO = 'SET010'                 #���������
            TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
            TradeContext.STRINFO  = 'ԭ����ҵ���ѳ����ɹ�'   #����
        
            return True
        elif spb_dict['TRDT'] == '' and spb_dict['TLSQ'] == '':
            #=====ԭҵ������ɹ�,��δĨ��,�ع�����ǰ״̬,�ظ������ɹ�====
            AfaLoggerFunc.tradeDebug(">>>ԭҵ������ɹ�,��δĨ��,�ع�����ǰ״̬,�ظ������ɹ�")
            
            #�ع�ԭ����������״̬Ϊ����ǰ״̬
            AfaLoggerFunc.tradeInfo(">>>��ʼ�ع�ԭ����������״̬Ϊ����ǰ״̬")
            
            spbsta_dict = {}
            if not rccpsState.getTransStateDes(spb_dict['BJEDTE'],spb_dict['BSPSQN'],spbsta_dict,1):
                return AfaFlowControl.ExitThisFlow('S999','��ѯԭ���������׳���ǰ״̬�쳣')
            
            if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],spbsta_dict['BCSTAT'],spbsta_dict['BDWFLG']):
                return AfaFlowControl.ExitThisFlow('S999','�ع�״̬Ϊ����ǰ״̬�쳣')
            else:
                AfaDBFunc.CommitSql()
                
            sstlog_dict = {}
            sstlog_dict['BJEDTE']    =  spbsta_dict['BJEDTE']
            sstlog_dict['BSPSQN']    =  spbsta_dict['BSPSQN']
            sstlog_dict['BCSTAT']    =  spbsta_dict['BCSTAT']
            sstlog_dict['BDWFLG']    =  spbsta_dict['BDWFLG']
            sstlog_dict['NOTE3']     =  '�������ױ�����,�ع�Ϊ����ǰ״̬'
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
                
            AfaLoggerFunc.tradeInfo(">>>�����ع�ԭ����������״̬Ϊ����ǰ״̬")
         
            #=====Ϊ���س����ɹ����ͳɹ���ִ====
            TradeContext.MSGTYPCO = 'SET010'                 #���������
            TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
            TradeContext.STRINFO  = 'ԭ����ҵ���ѳ����ɹ�'   #����
            
            return True
        else:
            AfaLoggerFunc.tradeDebug('>>>׼������8813�ٴμ���')

        #=====����ǰ��ֵ����====
        AfaLoggerFunc.tradeDebug('>>>����ǰ��ֵ����')

        if rccpsGetFunc.GetRBSQ(PL_BRSFLG_RCV) == -1 :
            return AfaFlowControl.ExitThisFlow('S999','��������ǰ����ˮ��ʧ��,��������')

        TradeContext.BESBNO    =  wtr_dict['BESBNO']           #������
        TradeContext.BETELR    =  wtr_dict['BETELR']           #��Ա��
        TradeContext.BEAUUS    =  wtr_dict['BEAUUS']           #��Ȩ��Ա
        TradeContext.BEAUPS    =  wtr_dict['BEAUPS']           #��Ȩ����
        TradeContext.TERMID    =  wtr_dict['TERMID']           #�ն˺�
        TradeContext.HostCode  =  '8813'                       #����������
        TradeContext.PYRACC    =  wtr_dict['PYRACC']           #�������˻�
        TradeContext.PYRNAM    =  wtr_dict['PYRNAM']           #����������
        TradeContext.OCCAMT    =  str(wtr_dict['OCCAMT'])      #���
        TradeContext.CUSCHRG   =  str(wtr_dict['CUSCHRG'])     #�����ѽ��
        TradeContext.BANKNO    =  wtr_dict['BNKBKNO']          #���ۺ���
        
        if wtr_dict['TRCCO'] in ('3000002','3000004'):
            #=====ͨ��====
            AfaLoggerFunc.tradeDebug('>>>ͨ��')

            TradeContext.RCCSMCD  =  PL_RCCSMCD_XJTCLZ                       #ժҪ����  PL_RCCSMCD_XJTCLZ  ͨ������
            TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #�跽�˻�:ũ��������������
            TradeContext.SBNM     = "ũ��������������"
            TradeContext.RBAC     = wtr_dict['PYEACC']                       #�����˻�:�տ����˻�
            TradeContext.RBNM     = wtr_dict['PYENAM']                       #��������:�տ��˻���
            TradeContext.OCCAMT = str(wtr_dict['OCCAMT'])
            #=====add by pgt 12-4====
            TradeContext.CTFG      = '7'                                    #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
            TradeContext.PKFG      = 'T'                                    #ͨ��ͨ�ұ�ʶ                                   
            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        elif wtr_dict['TRCCO'] in ('3000102','3000104'):
            #=====ͨ��====
            AfaLoggerFunc.tradeDebug('>>>ͨ��')

            if float(wtr_dict['CUSCHRG']) <= 0:
                #=====�Է��ֽ���ȡ�����ѻ��շ�====
                AfaLoggerFunc.tradeDebug('>>>�ֽ���ȡ������')
 
                TradeContext.RCCSMCD  = PL_RCCSMCD_XJTDLZ                     #����ժҪ����
                TradeContext.SBAC = TradeContext.PYRACC                       #�跽�˻�:�������˻�
                TradeContext.ACNM = TradeContext.PYRNAM                       #�跽���� �����˻���
                TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ     #�����˻�:ũ��������������
                TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                TradeContext.RBNM = 'ũ��������������'                        #��������
                #=====add by pgt 12-4====
                TradeContext.CTFG      = '7'                                  #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
                TradeContext.PKFG      = 'T'                                  #ͨ��ͨ�ұ�ʶ                                   

                if wtr_dict['TRCCO'] == '3000104':
                    TradeContext.WARNTNO = '49' + TradeContext.BANKNO
                else:
                    TradeContext.WARNTNO = TradeContext.SBAC[6:18]
            else:
                #=====�Է�ת����ȡ������====
                AfaLoggerFunc.tradeDebug('>>>ת����ȡ������')

                TradeContext.ACUR    =  '3'                                         #���˴���
                #=========���׽��============
                TradeContext.RCCSMCD  =  PL_RCCSMCD_XJTDLZ                          #ժҪ����
                TradeContext.SBAC  =  TradeContext.PYRACC                           #�跽�˺�
                TradeContext.ACNM  =  TradeContext.PYRNAM                           #�跽����
                TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
                TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM  =  '������ʱ����'                                #��������
                TradeContext.CTFG  = '7'                                            #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
                TradeContext.PKFG  = 'T'                                            #ͨ��ͨ�ұ�ʶ                                   

                AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
                AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )

                #=========�������������뻧===========
                TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
                TradeContext.I2SBAC  =  TradeContext.PYRACC                           #�跽�˺�
                TradeContext.I2ACNM  =  TradeContext.PYRNAM                           #�跽����
                TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
                TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
                TradeContext.I2OTNM  =  '������ʱ����'                                #��������
                TradeContext.I2TRAM  =  str(TradeContext.CUSCHRG)                      #������
                TradeContext.I2CTFG  = '8'                                             #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
                TradeContext.I2PKFG  = 'T'                                             #ͨ��ͨ�ұ�ʶ                                   

                AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
                AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )

                #=========���׽��+������===================
                TradeContext.I3SMCD    =  PL_RCCSMCD_XJTDLZ                               #ժҪ����
                TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
                TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
                TradeContext.I3ACNM    =  '������ʱ����'                                #�跽����
                TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�����˺�
                TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
                TradeContext.I3OTNM    =  'ũ��������'                                  #��������
                TradeContext.I3TRAM    =  rccpsUtilTools.AddDot(TradeContext.OCCAMT,TradeContext.CUSCHRG) #������
                TradeContext.I3CTFG  = '9'                                              #���� �����ѱ�ʶ  7 ���� 8������ 9 ����������                                            
                TradeContext.I3PKFG  = 'T'                                              #ͨ��ͨ�ұ�ʶ                                   

                #=====ƾ֤����====
                if wtr_dict['TRCCO'] ==  '3000102':
                    #=====��====
                    TradeContext.WARNTNO = TradeContext.SBAC[6:18]
                    TradeContext.I2WARNTNO = TradeContext.I2SBAC[6:18]
                else:
                    #=====��====
                    TradeContext.WARNTNO   = '49' + TradeContext.BANKNO
                    TradeContext.I2WARNTNO = '49' + TradeContext.BANKNO
        elif wtr_dict['TRCCO'] in ('3000003','3000005'):
            #=====��ת��====
            AfaLoggerFunc.tradeDebug('>>>��ת��')

            TradeContext.RCCSMCD  =  PL_RCCSMCD_XJTCLZ                       #ժҪ����  PL_RCCSMCD_XJTCLZ  ͨ������
            TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #�跽�˻�:ũ��������������
            TradeContext.SBNM     = "ũ��������������"
            TradeContext.RBAC     = wtr_dict['PYEACC']                       #�����˻�:�տ����˻�
            TradeContext.RBNM     = wtr_dict['PYENAM']                       #��������:�տ��˻���
            TradeContext.OCCAMT = str(wtr_dict['OCCAMT'])
            #=====add by pgt 12-4====
            TradeContext.CTFG      = '7'                                    #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
            TradeContext.PKFG      = 'T'                                    #ͨ��ͨ�ұ�ʶ
            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        elif wtr_dict['TRCCO'] in ('3000103','3000105'):
            #=====��ת��====
            AfaLoggerFunc.tradeDebug('>>>��ת��')

            if( float(TradeContext.CUSCHRG) <= 0 ):
                #=====�ֽ�====
                AfaLoggerFunc.tradeDebug('>>>�ֽ���ȡ������')

                TradeContext.RCCSMCD  = PL_RCCSMCD_YZBWZ#����ժҪ����
                TradeContext.SBAC = TradeContext.PYRACC                       #�跽�˻�:�������˻�
                TradeContext.ACNM = TradeContext.PYRNAM                       #�跽���� �����˻���
                TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ     #�����˻�:ũ��������������
                TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                TradeContext.RBNM = 'ũ��������������'                        #��������:
                TradeContext.CTFG =  '7'                                      #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
                TradeContext.PKFG =  'T'                                      #ͨ��ͨ�ұ�ʶ                                   

                if wtr_dict['TRCCO'] == '3000103':
                    TradeContext.WARNTNO = TradeContext.SBAC[6:18]
                else:
                    TradeContext.WARNTNO = '49' + TradeContext.BANKNO

                AfaLoggerFunc.tradeDebug( '>>>�跽�˺�:' + TradeContext.SBAC )
                AfaLoggerFunc.tradeDebug( '>>>�����˺�:' + TradeContext.RBAC )
                AfaLoggerFunc.tradeDebug( '>>>ƾ֤����:' + TradeContext.WARNTNO )
            else:
                #=====ת��=====
                AfaLoggerFunc.tradeDebug('>>>ת����ȡ������')

                TradeContext.ACUR    =  '3'                                           #���˴���
                #=========���׽��============
                TradeContext.RCCSMCD  =  PL_RCCSMCD_YZBWZ                               #ժҪ����
                TradeContext.SBAC  =  TradeContext.PYRACC                           #�跽�˺�
                TradeContext.ACNM  =  TradeContext.PYRNAM                           #�跽����
                TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
                TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM  =  '������ʱ����'                                #��������
                TradeContext.OCCAMT  =  str(TradeContext.OCCAMT)                       #������
                TradeContext.CTFG  = '7'                                            #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
                TradeContext.PKFG  = 'T'                                            #ͨ��ͨ�ұ�ʶ                                   

                AfaLoggerFunc.tradeDebug( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
                AfaLoggerFunc.tradeDebug( '>>>���׽��:�����˺�' + TradeContext.RBAC )

                #=========�������������뻧===========
                TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
                TradeContext.I2SBAC  =  TradeContext.PYRACC                           #�跽�˺�
                TradeContext.I2ACNM  =  TradeContext.PYRNAM                           #�跽����
                TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
                TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
                TradeContext.I2OTNM  =  '������ʱ����'                                #��������
                TradeContext.I2TRAM  =  str(TradeContext.CUSCHRG)                      #������
                TradeContext.I2CTFG  = '8'                                            #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
                TradeContext.I2PKFG  = 'T'                                            #ͨ��ͨ�ұ�ʶ                                    

                AfaLoggerFunc.tradeDebug( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
                AfaLoggerFunc.tradeDebug( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )

                #=========���׽��+������===================
                TradeContext.I3SMCD    =  PL_RCCSMCD_YZBWZ                               #ժҪ����
                TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
                TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
                TradeContext.I3ACNM    =  '������ʱ����'                                #�跽����
                TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�����˺�
                TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
                TradeContext.I3OTNM    =  'ũ��������'                                  #��������
                TradeContext.I3TRAM    =  rccpsUtilTools.AddDot(TradeContext.OCCAMT,TradeContext.CUSCHRG) #������
                TradeContext.I3CTFG    = '9'                                            #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
                TradeContext.I3PKFG    = 'T'                                            #ͨ��ͨ�ұ�ʶ                                   
                AfaLoggerFunc.tradeDebug( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
                AfaLoggerFunc.tradeDebug( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )

                if wtr_dict['TRCCO'] == '3000103':
                    TradeContext.WARNTNO   = TradeContext.SBAC[6:18]
                    TradeContext.I2WARNTNO = TradeContext.I2SBAC[6:18]
                else:
                    TradeContext.WARNTNO   = '49' + TradeContext.BANKNO
                    TradeContext.I2WARNTNO = '49' + TradeContext.BANKNO
        else:
            AfaLoggerFunc.tradeInfo('>>>ԭ���������')
            return AfaFlowControl.ExitThisFlow('S999','��������')

        #=====����״̬====
        if wtr_dict['TRCCO'] in ('3000002','3000004','3000003','3000005'):
            #=====ͨ�� ��ת�� ״̬Ϊ:�Զ�����====
            TradeContext.BCSTAT = PL_BCSTAT_AUTO
        else:
            #=====ͨ�� ��ת�� ״̬Ϊ:�Զ��ۿ�====
            TradeContext.BCSTAT = PL_BCSTAT_AUTOPAY

        #=====��ʼ����״̬====
        #if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,PL_BDWFLG_WAIT):
        if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],TradeContext.BCSTAT,PL_BDWFLG_WAIT):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ�Զ�����/�ۿ�-�������쳣')
        else:
            AfaDBFunc.CommitSql()

        #=====��ʼ����������ͨѶ====
        AfaLoggerFunc.tradeInfo('>>>׼����ʼ������ͨѶ')

        rccpsHostFunc.CommHost( TradeContext.HostCode )

        #=====������������====
        AfaLoggerFunc.tradeInfo('>>>������������')

        sstlog = {}
        sstlog['BJEDTE']  =  wtr_dict['BJEDTE']
        sstlog['BSPSQN']  =  wtr_dict['BSPSQN']
        sstlog['BCSTAT']  =  TradeContext.BCSTAT
        sstlog['MGID']    =  TradeContext.errorCode

        if TradeContext.errorCode == '0000':
            sstlog['TRDT']  =  TradeContext.TRDT             #��������
            sstlog['TLSQ']  =  TradeContext.TLSQ             #������ˮ
            sstlog['BDWFLG']=  PL_BDWFLG_SUCC
            sstlog['STRINFO'] = '�������ױ�����,��������ɹ�'               #����
        else:
            sstlog['BDWFLG']=  PL_BDWFLG_FAIL
            sstlog['STRINFO'] = TradeContext.errorMsg        #����
            
        #=====����״̬====
        if not rccpsState.setTransState(sstlog):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬�쳣")
        else:
            AfaDBFunc.CommitSql()

        #=====�����ɹ��󷵻���ȷ��ִ����====
        AfaLoggerFunc.tradeInfo('>>>���ͳɹ���ִ')

        TradeContext.MSGTYPCO = 'SET010'                 #���������
        TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
        TradeContext.STRINFO  = '�ɹ�'                   #����

        return True
    elif TradeContext.ORTRCCO == '3000505':
        #=====3000505 ����ҵ��====
        AfaLoggerFunc.tradeDebug('>>>����ԭ����ҵ���Ƿ����')
        
        #�ر��  20081230  ��ԭҵ��Ϊ����,ֱ�ӻظ������ɹ�Ӧ��
        
        AfaLoggerFunc.tradeInfo('>>>���ͳɹ���ִ')

        TradeContext.MSGTYPCO = 'SET010'                 #���������
        TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
        TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
        TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
        TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
        TradeContext.STRINFO  = '�ɹ�'                   #����
        
        return True
    else:
        #=====����ԭ����/��������ҵ��====
     
        #=====����ԭ�����Ƿ����====
        AfaLoggerFunc.tradeDebug(">>>����ԭ�����Ƿ����")
        
        where_dict = {'MSGFLGNO':TradeContext.ORMFN}
        wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
        
        if( wtrbka_dict == -1 ):
            AfaLoggerFunc.tradeInfo(">>>����ԭ����ʧ��,ԭҵ��������ˮ��["+str(TradeContext.ORTRCNO)+"]")
            return AfaFlowControl.ExitThisFlow('A099',"����ԭ����ʧ��,��������,�ȴ������Զ�����")
            
        if( len(wtrbka_dict) == 0 ):
            #=====δ���ҵ�ԭ����====
            AfaLoggerFunc.tradeDebug(">>>����ԭ����ʧ��,δ�յ�ԭ����,ֱ�ӻظ��ɹ�����")
         
            #=====Ϊ���س����ɹ����ͳɹ���ִ====
            TradeContext.MSGTYPCO = 'SET010'                 #���������
            TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
            TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
            TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
            TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
            TradeContext.STRINFO  = '�ɹ�'                   #����
        
            return True        
        else:
            #=====����ԭ���׳ɹ�====
            AfaLoggerFunc.tradeInfo(">>>����ԭ���׳ɹ�")
            
            #=====��ԭ������� ԭ�������ڸ��µ������Ǽǲ���====
            AfaLoggerFunc.tradeInfo('>>>����ԭ�������\ԭ��������')
            
            atcbka_where={}
            atcbka_where['BSPSQN'] = TradeContext.BSPSQN      #�������
            atcbka_where['BJEDTE'] = TradeContext.BJEDTE      #��������
            
            atcbka_dict ={}
            atcbka_dict['BOJEDT']  = wtrbka_dict['BJEDTE']    #ԭ��������
            atcbka_dict['BOSPSQ']  = wtrbka_dict['BSPSQN']    #ԭ�������
            #�ر��  20081225  ���³����Ǽǲ��еǼǻ�����Ϊԭ���׻�����
            atcbka_dict['BESBNO']  = wtrbka_dict['BESBNO']    #ԭ������
            atcbka_dict['STRINFO'] = TradeContext.STRINFO     #���� 
            atcbka_dict['ORTRCDAT']= wtrbka_dict['TRCDAT']    #ԭί������
            atcbka_dict['OPRNO']   = PL_TDOPRNO_CZ            #ҵ������

            ret = rccpsDBTrcc_atcbka.update(atcbka_dict,atcbka_where)
            
            if ret <= 0:
                AfaDBFunc.RollbackSql( )
                return AfaFlowControl.ExitThisFlow('S999', "�����Զ������Ǽǲ�ԭ������ź�ԭ���������쳣,��������")
            else:
                AfaDBFunc.CommitSql( )
            
            AfaLoggerFunc.tradeInfo(">>>�������³����Ǽǲ�ԭ�������ں�ԭ�������")
            
            #=====����ԭ����ҵ��״̬====
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

            
            #�ر��  20081226  ���������׵�ǰ״̬Ϊ�Զ��ۿ�,�Զ�����,����,����������״̬,�˳�,�ȴ��¸���������
            if (spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTO or spbsta_dict['BCSTAT'] == PL_BCSTAT_AUTOPAY or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC or spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL) and  spbsta_dict['BDWFLG'] == PL_BDWFLG_WAIT:
                return AfaFlowControl.ExitThisFlow('S999','ԭҵ������״̬δ֪,��������,�ȴ������ٴη����Զ�����')

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
                    AfaLoggerFunc.tradeInfo(">>>��ѯԭ��������״̬�쳣,���ؾܾ�Ӧ��,�ȴ��´γ�������")
                    #=====Ϊ���س����ܾ���ִ��ֵ====
                    TradeContext.MSGTYPCO = 'SET010'                 #���������
                    TradeContext.PRCCO    = 'RCCO1006'               #���ķ�����
                    TradeContext.STRINFO  = 'ԭ��������״̬δ֪'     #����
                    TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
                    TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
                    TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
                    
                    return True

            #=====���������ʱ�ʶ���г���״̬�ж�====
            if( wtrbka_dict['BRSFLG'] == PL_BRSFLG_RCV ):
                #=====����ҵ��====
                AfaLoggerFunc.tradeDebug(">>>����ҵ��")

                #=====PL_BCSTAT_AUTOPAY   �Զ��ۿ�====
                #=====PL_BCSTAT_CONFPAY   ȷ�ϸ���====
                #=====PL_BCSTAT_CONFACC   ȷ������====
                #=====PL_BCSTAT_MFERFE    �ܾ�====
                #=====PL_BCSTAT_CANC      ��̨����====
                #=====PL_BCSTAT_CANCEL    �Զ�����====
                if( ((spbsta_dict['BCSTAT']==PL_BCSTAT_AUTO or spbsta_dict['BCSTAT']==PL_BCSTAT_AUTOPAY) and spbsta_dict['BDWFLG']==PL_BDWFLG_FAIL) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_MFERFE  and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CANC    and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CANCEL  and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CONFPAY and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC) \
                    or (spbsta_dict['BCSTAT'] == PL_BCSTAT_CONFACC and spbsta_dict['BDWFLG'] == PL_BDWFLG_SUCC)):
                    #=====���������====
                    AfaLoggerFunc.tradeDebug(">>>ԭҵ��["+str(spbsta_dict['BSPSQN'])+"]����ʧ�ܻ򱻾ܾ���������Զ���������ȷ��,������Ĩ��,���ͳɹ�����")

                    if spbsta_dict['BCSTAT'] not in (PL_BCSTAT_MFERFE,PL_BCSTAT_CANC,PL_BCSTAT_CANCEL):
                        AfaLoggerFunc.tradeDebug('>>>����ԭҵ��״̬Ϊ�Զ�����-�ɹ�')
                        if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC):
                            AfaDBFunc.RollbackSql()
                            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ�Զ�����-�ɹ��쳣')
                        else:
                            AfaDBFunc.CommitSql( )
                    else:
                        AfaLoggerFunc.tradeDebug('>>>ԭҵ��״̬Ϊ[�ܾ�/����/����],����Ҫ����״̬')
 
                    #=====ԭ��������Ĩ��,���س����ɹ�Ӧ��====
                    TradeContext.MSGTYPCO = 'SET010'                 #���������
                    TradeContext.PRCCO    = 'RCCI0000'               #���ķ�����
                    TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
                    TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
                    TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
                    TradeContext.STRINFO  = 'ԭҵ������ɹ�'         #����
            
                    return True
                else:
                    #=====����ԭҵ��״̬Ϊ����-������====
                    AfaLoggerFunc.tradeDebug('>>>����ԭҵ��״̬Ϊ�Զ�����-������')
            
                    #=====ֱ�ӵ���8820����ԭҵ��====
                    TradeContext.BOSPSQ   = spbsta_dict['BSPSQN']    #ԭ�������
                    TradeContext.BOJEDT   = spbsta_dict['BJEDTE']    #ԭ��������
                    TradeContext.HostCode = '8820'                   #����������
                    
                    if not rccpsState.newTransState(spbsta_dict['BJEDTE'],spbsta_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_WAIT):
                        AfaDBFunc.RollbackSql()
                        return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ�Զ������������쳣')
                    else:
                        AfaDBFunc.CommitSql( )
            
                    #=====����������8820Ĩ�˴���==== 
                    AfaLoggerFunc.tradeDebug('>>>����������8820Ĩ�˴���')
            
                    rccpsHostFunc.CommHost( TradeContext.HostCode ) 
            
                    #=====�ж���������====
                    sstlog_dict={}
                    sstlog_dict['BJEDTE']  =  spbsta_dict['BJEDTE']
                    sstlog_dict['BSPSQN']  =  spbsta_dict['BSPSQN']
                    sstlog_dict['BCSTAT']  =  PL_BCSTAT_CANCEL       #����
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
                        sstlog_dict['STRINFO']   =  TradeContext.errorMsg  #����
                        TradeContext.PRCCO       =  'NN1IA999'
                        TradeContext.STRINFO     =  'ԭҵ�����ʧ�� ' + TradeContext.errorMsg
            
                    #=====�޸�ԭҵ��״̬====
                    AfaLoggerFunc.tradeDebug('>>>�޸�ԭҵ��״̬')
            
                    res = rccpsState.setTransState(sstlog_dict)
            
                    if( res == False ):
                        AfaDBFunc.RollbackSql()
                        return AfaFlowControl.ExitThisFlow('A099', '���ı������Ľ���״̬ʧ��')
                    else:
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
                    
                    return True
            else:
                #=====����ҵ��====
                AfaLoggerFunc.tradeDebug(">>>����ҵ��")
                
                #=====���ͻ�ִ====
                AfaLoggerFunc.tradeDebug('>>>���;ܾ���ִ���Է���')
                
                #=====Ϊ���س����ɹ����ͳɹ���ִ====
                TradeContext.MSGTYPCO = 'SET010'                 #���������
                TradeContext.PRCCO    = 'RCCO1006'               #���ķ�����
                TradeContext.STRINFO  = '����ҵ��ֻ������������'     #����
                TradeContext.ORMFN    = TradeContext.MSGFLGNO    #�ο����ı�ʾ��
                TradeContext.SNDSTLBIN= TradeContext.RCVMBRCO    #���ͳ�Ա�к�
                TradeContext.RCVSTLBIN= TradeContext.SNDMBRCO    #���ճ�Ա�к�
                
    AfaLoggerFunc.tradeInfo("ũ����ϵͳ������.���������(1.���ز���).��̨�������˽���[TRCC006_1144]����")
    
    return True
def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo("ũ����ϵͳ������.���������(2.���Ļ�ִ).��̨�������˽���[TRCC006_1144]����")
    AfaLoggerFunc.tradeDebug(">>>errorCode[" + TradeContext.errorCode + "]")
    
    #=====�ж�afe���ؽ��====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ���ĳɹ�')
    else:
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ����ʧ��')
    
    AfaLoggerFunc.tradeInfo("ũ����ϵͳ������.���������(2.���Ļ�ִ).��̨�������˽���[TRCC006_1144]����")
    
    return True                                 
