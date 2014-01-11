# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).ͨ��ͨ�Ҵ����ֹ���ת
#===============================================================================
#   ģ���ļ�:   TRCC001_8591.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-12-16
################################################################################
#   �޸��ߣ�    �˹�ͨ
#   �޸�ʱ�䣺  20081225
#   �޸����ݣ�  ���Ӷ�����״̬�����Ĵ���
#################################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsState,AfaDBFunc,rccpsHostFunc,rccpsFunc,rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_spbsta,rccpsDBTrcc_notbka
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8591]ͨ��ͨ�Ҵ��ʴ����ʶά������***' )
    
    AfaLoggerFunc.tradeInfo('���Ի�����(���ز���)')
    
    #=====�жϽӿڱ����Ƿ����====
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','�����кŲ���Ϊ��' )
        
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A009','ί�����ڲ���Ϊ��')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A009','������ˮ�Ų���Ϊ��')
        
    if not TradeContext.existVariable("BJEDTE"):
        return AfaFlowControl.ExitThisFlow('A009','�������ڲ���Ϊ��')
        
    if not TradeContext.existVariable("BSPSQN"):
        return AfaFlowControl.ExitThisFlow('A009','������Ų���Ϊ��')
    
    AfaLoggerFunc.tradeInfo('���Ի��������(���ز���)') 
    
    #=====�õ�nccwkdat====
    if not rccpsFunc.GetNCCDate( ) :                   #NCCworkDate
        raise AfaFlowControl.flowException( )
    
    #=====��ѯ���˵Ǽǲ�====
    where_dict = {}
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
    tddzcz_record = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if(tddzcz_record == None):
        return AfaFlowControl.ExitThisFlow('A009','��ѯ���˵Ǽǲ�ʧ��')
        
    elif(len(tddzcz_record) == 0):
        return AfaFlowControl.ExitThisFlow('A009','��ѯ���˵Ǽǲ�Ϊ��')
        
    else:
        AfaLoggerFunc.tradeInfo("��ѯ���˵Ǽǲ��ɹ�")
    
    #=====��ѯԭҵ�����Ϣ====
    AfaLoggerFunc.tradeInfo('��ѯԭҵ����Ϣ')
    where_dict = {}
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
    wtrbka_record = rccpsDBTrcc_wtrbka.selectu(where_dict)
    if(wtrbka_record == None):
        return AfaFlowControl.ExitThisFlow('A009','��ѯҵ��Ǽǲ�ʧ��')
        
    elif(len(wtrbka_record) == 0):
        return AfaFlowControl.ExitThisFlow('A009','��ѯҵ��Ǽǲ�Ϊ��')   
        
    else:
        AfaLoggerFunc.tradeInfo('��ѯҵ��Ǽǲ��ɹ�') 
        
    #=====��ѯҵ��ĵ�ǰ��Ϣ====
    wtr_dict = {}
    if not rccpsDBFunc.getTransWtr(TradeContext.BJEDTE,TradeContext.BSPSQN,wtr_dict):
        return AfaFlowControl.ExitThisFlow('A009','��ѯҵ��ĵ�ǰ��Ϣʧ��')
        
    if(wtr_dict['BRSFLG'] == PL_BRSFLG_SND):
        sstlog_dict = {}
        if not rccpsState.getTransStateSet(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_ACC,PL_BDWFLG_SUCC,sstlog_dict):
            return AfaFlowControl.ExitThisFlow('A009','��ѯҵ��״̬��Ϣʧ��')
            
        wtr_dict['FEDT'] = sstlog_dict['FEDT']
        wtr_dict['RBSQ'] = sstlog_dict['RBSQ']
        
    TradeContext.CLDT = wtr_dict['FEDT']
    TradeContext.UNSQ = wtr_dict['RBSQ']
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :   #RBSQ
        return AfaFlowControl.ExitThisFlow('A099','����ǰ����ˮ��ʧ��')
    TradeContext.FEDT=AfaUtilTools.GetHostDate( )    #FEDT
    
    #=====�жϵ�ǰҵ���Ƿ��Ѿ���ת====
    if(wtr_dict['BCSTAT'] == PL_BCSTAT_TRAS and wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC):
        return AfaFlowControl.ExitThisFlow('A009','�������Ѿ���ת')
        
        
    #=====�ж�ҵ���������ʾ====
    AfaLoggerFunc.tradeInfo('<<<<<<�ж�ҵ���������ʾ')
    if(wtrbka_record['BRSFLG'] == PL_BRSFLG_SND):
        AfaLoggerFunc.tradeInfo('<<<<<<ҵ��Ϊ����')
        acc    = 0    
        hcac   = 0   
        canc   = 0
        cancel = 0
        
        #=====��ѯ�Ƿ��м��˳ɹ���״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_ACC,PL_BDWFLG_SUCC,sstlog_list):
            acc = len(sstlog_list)
        #=====��ѯ�Ƿ���Ĩ�˵�״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_SUCC,sstlog_list):
            hcac = len(sstlog_list)
        #=====��ѯ�Ƿ��г�����״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CANC,PL_BDWFLG_SUCC,sstlog_list):
            canc = len(sstlog_list)
        #=====��ѯ�Ƿ��г�����״̬====
        ssltog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC,sstlog_list):
            cancel = len(sstlog_list)
        
        #=====�ж��Ƿ���Ҫ����״̬����====
        AfaLoggerFunc.tradeInfo('<<<<<<�ж��Ƿ���Ҫ����״̬����')
        if(acc - (hcac + canc + cancel) >= 0):
            AfaLoggerFunc.tradeInfo('<<<<<<��Ҫ��������״̬����')
                
            TradeContext.BETELR   = PL_BETELR_AUTO
            TradeContext.BRSFLG   = wtrbka_record['BRSFLG']    
            TradeContext.CHRGTYP  = wtrbka_record['CHRGTYP']
            TradeContext.BESBNO   = wtrbka_record['BESBNO'] 
            #=====���۴���/��ת���====
            if(wtrbka_record['TRCCO'] in ('3000002','3000003','3000004','3000005')):
                AfaLoggerFunc.tradeInfo('���۴���/��ת���')
                TradeContext.HostCode = '8813' 
                TradeContext.ACUR     = '1'
                TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSWZ          #�跽�˺�
                TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
                TradeContext.ACNM     = 'ũ��������������'                                 #�跽����
                TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYWZ             #�����˺�
                TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM     = 'ũ��������'                                       #��������
                TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'])                       #������
                TradeContext.PKFG     = 'W'
                TradeContext.CTFG     = '7'
                    
            #=====����ȡ��/���ת����====
            elif(wtrbka_record['TRCCO'] in ('3000102','3000103','3000104','3000105')): 
                AfaLoggerFunc.tradeInfo('����ȡ��/���ת����')
                if(wtrbka_record['CHRGTYP'] == '1'):    #ת��           
                    AfaLoggerFunc.tradeInfo("<<<<<ת��������")
                    TradeContext.HostCode = '8813' 
                    TradeContext.ACUR     = '1'
                    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                    TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYWZ    #�跽�˺�
                    TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
                    TradeContext.ACNM     = 'ũ��������'
                    TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSWZ #�����˺� 
                    TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                    TradeContext.OTNM     = 'ũ��������������'
                    TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'] + wtrbka_record['CUSCHRG'])
                    TradeContext.PKFG     = 'W'
                    TradeContext.CTFG     = '9'
                    
                else:    #����
                    AfaLoggerFunc.tradeInfo("<<<<<���������ѣ�����")
                    TradeContext.HostCode = '8813' 
                    TradeContext.ACUR     = '1'
                    TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                    TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYWZ    #�跽�˺�
                    TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
                    TradeContext.ACNM     = 'ũ��������'
                    TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSWZ #�����˺� 
                    TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                    TradeContext.OTNM     = 'ũ��������������'
                    TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'])
                    TradeContext.PKFG     = 'W'
                    TradeContext.CTFG     = '9'
                
            else:
                return AfaFlowControl.ExitThisFlow('A099','ԭ���׽��״���Ƿ�')
                
            #=====����ԭ���׵�״̬--��ת====
            if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_TRAS,PL_BDWFLG_WAIT):
                AfaDBFunc.RollbackSql()
                return AfaFlowControl.ExitThisFlow('A099','����ԭ���׵�״̬--��ת��ʧ��')
            else:
                AfaDBFunc.CommitSql()  
                
            #=====������������====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            #=====�ж����������Ƿ�ɹ�====
            if(TradeContext.errorCode != '0000'):
                AfaLoggerFunc.tradeInfo("��������ʧ��")
                #=====����ԭ����״̬====
                state_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCSTAT':PL_BCSTAT_TRAS,'BDWFLG':PL_BDWFLG_FAIL}
                state_dict['STRINFO'] = TradeContext.errorMsg
                if not rccpsState.setTransState(state_dict):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099','����ԭ����״̬ʧ��')
                else:
                    AfaDBFunc.CommitSql()   
                    
                return AfaFlowControl.ExitThisFlow('A099','��������ʧ��')
                
            else:
                AfaLoggerFunc.tradeInfo('�������˳ɹ�')
                #=====����ԭ����״̬====
                state_dict = {}
                state_dict['BJEDTE'] = TradeContext.BJEDTE
                state_dict['BSPSQN'] = TradeContext.BSPSQN
                state_dict['BCSTAT'] = PL_BCSTAT_TRAS
                state_dict['BDWFLG'] = PL_BDWFLG_SUCC
                if(TradeContext.existVariable("SBAC")):
                    state_dict['SBAC'] = TradeContext.SBAC
                if(TradeContext.existVariable("RBAC")):
                    state_dict['RBAC'] = TradeContext.RBAC
                state_dict['STRINFO'] = '�����ɹ�'
                if(TradeContext.existVariable('TRDT')):
                    state_dict['TRDT'] = TradeContext.TRDT
                if(TradeContext.existVariable('TLSQ')):
                    state_dict['TLSQ'] = TradeContext.TLSQ
                if not rccpsState.setTransState(state_dict):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099','����ԭ����״̬ʧ��')
                else:
                    AfaDBFunc.CommitSql()   
                     
        else:
            return AfaFlowControl.ExitThisFlow('A009','ԭ���ײ��ܽ����������')
        
    else:
        AfaLoggerFunc.tradeInfo('<<<<<<ҵ��Ϊ����')
        autopay = 0    
        auto    = 0
        hcac    = 0   
        canc    = 0
        cancel  = 0
        #=====��ѯ�Ƿ��м��˳ɹ���״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_AUTO,PL_BDWFLG_SUCC,sstlog_list):
            auto = len(sstlog_list)
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_AUTOPAY,PL_BDWFLG_SUCC,sstlog_list):
            autopay = len(sstlog_list)      
        #=====��ѯ�Ƿ���Ĩ�˵�״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_SUCC,sstlog_list):
            hcac = len(sstlog_list)
        #=====��ѯ�Ƿ��г�����״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CANC,PL_BDWFLG_SUCC,sstlog_list):
            canc = len(sstlog_list)
        #=====��ѯ�Ƿ��г�����״̬====
        ssltog_list = []
        if rccpsState.getTransStateSetm(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC,sstlog_list):
            cancel = len(sstlog_list)
            
        #=====�ж�ԭҵ���Ƿ���Ҫ��������״̬����====
        AfaLoggerFunc.tradeInfo("�ж�ԭҵ���Ƿ���Ҫ��������״̬����")
        if((auto + autopay) - (hcac + canc + cancel) >= 0):
            AfaLoggerFunc.tradeInfo("ԭҵ����Ҫ��������״̬����")
            
            TradeContext.BETELR   = PL_BETELR_AUTO
            TradeContext.BRSFLG   = wtrbka_record['BRSFLG']    
            TradeContext.CHRGTYP  = wtrbka_record['CHRGTYP']
            TradeContext.BESBNO   = wtrbka_record['BESBNO']  
            #=====���۴���/��ת���====
            if(wtrbka_record['TRCCO'] in ('3000002','3000003','3000004','3000005')):
                AfaLoggerFunc.tradeInfo('���۴���/��ת���')
                TradeContext.HostCode = '8813' 
                TradeContext.ACUR     = '1'
                TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYLZ
                TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
                TradeContext.ACNM     = 'ũ��������'
                TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSLZ 
                TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM     = 'ũ��������������'
                TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'])
                TradeContext.PKFG     = 'W'
                TradeContext.CTFG     = '7'
            
            #=====����ȡ��/���ת����====    
            elif(wtrbka_record['TRCCO'] in ('3000102','3000103','3000104','3000105')):
                AfaLoggerFunc.tradeInfo('���۴���/��ת���')
                TradeContext.HostCode = '8813'
                TradeContext.ACUR     = '1'
                TradeContext.RCCSMCD  = PL_RCCSMCD_DZBJ
                TradeContext.SBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYDQSLZ 
                TradeContext.SBAC     = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25) 
                TradeContext.ACNM     = 'ũ��������������'
                TradeContext.RBAC     = wtrbka_record['BESBNO'] + PL_ACC_NXYLZ 
                TradeContext.RBAC     = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
                TradeContext.OTNM     = 'ũ��������'
                TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'] + wtrbka_record['CUSCHRG'])
                TradeContext.PKFG     = 'W'
                TradeContext.CTFG     = '9'
                
            else:
                return AfaFlowControl.ExitThisFlow('A099','ԭ���׽��״���Ƿ�')
                
            #=====����ԭ���׵�״̬--��ת====
            if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_TRAS,PL_BDWFLG_WAIT):
                AfaDBFunc.RollbackSql()
                return AfaFlowControl.ExitThisFlow('A099','����ԭ���׵�״̬--��ת��ʧ��')
            else:
                AfaDBFunc.CommitSql()  
                
            #=====������������====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            #=====�ж����������Ƿ�ɹ�====
            if(TradeContext.errorCode != '0000'):
                AfaLoggerFunc.tradeInfo("��������ʧ��")
                #=====����ԭ����״̬====
                state_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCSTAT':PL_BCSTAT_TRAS,'BDWFLG':PL_BDWFLG_FAIL}
                state_dict['STRINFO'] = TradeContext.errorMsg
                if not rccpsState.setTransState(state_dict):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099','����ԭ����״̬ʧ��')
                else:
                    AfaDBFunc.CommitSql()   
                    
                return AfaFlowControl.ExitThisFlow('A099','��������ʧ��')
                
            else:
                AfaLoggerFunc.tradeInfo('�������˳ɹ�')
                #=====����ԭ����״̬====
                state_dict = {}
                state_dict['BJEDTE'] = TradeContext.BJEDTE
                state_dict['BSPSQN'] = TradeContext.BSPSQN
                state_dict['BCSTAT'] = PL_BCSTAT_TRAS
                state_dict['BDWFLG'] = PL_BDWFLG_SUCC
                state_dict['STRINFO'] = '�����ɹ�'
                if(TradeContext.existVariable("SBAC")):
                    state_dict['SBAC'] = TradeContext.SBAC
                if(TradeContext.existVariable("RBAC")):
                    state_dict['RBAC'] = TradeContext.RBAC
                if(TradeContext.existVariable('TRDT')):
                    state_dict['TRDT'] = TradeContext.TRDT
                if(TradeContext.existVariable('TLSQ')):
                    state_dict['TLSQ'] = TradeContext.TLSQ
                if not rccpsState.setTransState(state_dict):
                    AfaDBFunc.RollbackSql()
                    return AfaFlowControl.ExitThisFlow('A099','����ԭ����״̬ʧ��')
                else:
                    AfaDBFunc.CommitSql()   
            
        else:
            return AfaFlowControl.ExitThisFlow('A009','ԭ���ײ��ܽ����������')
       
    #=====���޸��ֵ丳ֵ====
    update_dict = {}
    update_dict = {'ISDEAL':'1','NOTE3':'�˱ʴ����ѽ�ת'}
    where_dict = {}               
    where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,\
                  'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}                                               

    #=====�޸����ݿ��е�����====
    AfaLoggerFunc.tradeInfo("ͨ��ͨ�Ҵ��ʴ����ʶ�޸�")
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A099','�޸�ͨ��ͨ�Ҵ��ʴ����ʶʧ��')
    elif( res == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','���׼�¼������')
        
    #=====���·���֪ͨ���в�������====
    AfaLoggerFunc.tradeInfo("<<<<<<��֪ͨ���в�������")
    insert_dict = {}
    insert_dict['NOTDAT']  = AfaUtilTools.GetHostDate( )
    insert_dict['BESBNO']  = wtrbka_record['BESBNO']
    if(wtrbka_record['BRSFLG'] == PL_BRSFLG_RCV):
        insert_dict['STRINFO'] = "�˱ʴ���["+wtrbka_record['BSPSQN']+"]["+wtrbka_record['BJEDTE']+"]�����ֹ���ת����"
    else:
        insert_dict['STRINFO'] = "�˱ʴ���["+wtrbka_record['BSPSQN']+"]["+wtrbka_record['BJEDTE']+"]�����ֹ���ת���� ����8522��������ƾ֤"
    if not rccpsDBTrcc_notbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','���·���֪ͨ���в�������ʧ��')
    AfaLoggerFunc.tradeInfo("<<<<<<��֪ͨ���в������ݳɹ�")
    
    #=====������ӿڸ�ֵ====
    TradeContext.errorCode = "0000"
    TradeContext.errorMsg  = "�޸�ͨ��ͨ�Ҵ��ʴ����ʶ�ɹ�"
    TradeContext.ISDEAL    = '1'
#    TradeContext.TLSQ      = TradeContext.TLSQ
#    TradeContext.RBSQ      = TradeContext.RBSQ
#    TradeContext.TRDT      = TradeContext.TRDT

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8591]ͨ��ͨ�Ҵ��ʴ����ʶά���˳�***' )
    
    return True      