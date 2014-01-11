# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�����˽���.ͨ��ͨ�Ҳ��Ĩ��
#=================================================================
#   �����ļ�:   TRCC001_8571.py
#   �޸�ʱ��:   2008-12-09
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,rccpsState,AfaDBFunc,rccpsEntriesErr,rccpsHostFunc,rccpsFunc,rccpsGetFunc
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_notbka,rccpsDBTrcc_spbsta
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.���Ĩ��[8571] ����")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<���Ի�����(���ز���) ����")
    
    #=====У������ĺϷ���====
    AfaLoggerFunc.tradeInfo("<<<<<<У������ĺϷ���")   
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A099','û��ί������')
        
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','û�з����к�')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A099','û�н�����ˮ��')
        
    AfaLoggerFunc.tradeInfo("<<<<<<У������ĺϷ��Խ���")
    
    #=====����FEDT,RBSQ,NCCworkDate,BJEDTE====
    TradeContext.BJEDTE = AfaUtilTools.GetHostDate( )   #BJEDTE
    
    TradeContext.FEDT=AfaUtilTools.GetHostDate( )    #FEDT
    
    if not rccpsFunc.GetNCCDate( ) :                   #NCCworkDate
        raise AfaFlowControl.flowException( )
    
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :   #RBSQ
        return AfaFlowControl.ExitThisFlow('A099','����ǰ����ˮ��ʧ��')
    
    #=====��ѯ������Ϣ====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�")
    where_dict = {}
    where_dict = {'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT}
    wtrbka_record_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
    if(wtrbka_record_dict == None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ��ҵ��Ǽǲ�ʧ��')
    
    elif(len(wtrbka_record_dict) == 0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ��ҵ��Ǽǲ����Ϊ��')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<��ѯͨ��ͨ��ҵ��Ǽǲ��ɹ�")
            
    #=====��ѯ���˵Ǽǲ�======
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ��ѯ���˵Ǽǲ�")
    where_dict = {}
    where_dict = {'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT}
    tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if(tddzcz_record_dict == None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ�ʧ��')
    
    elif(len(tddzcz_record_dict) == 0):
        AfaLoggerFunc.tradeInfo("<<<<<<��ѯ���˵Ǽǲ�Ϊ�գ�Ӧ�����в���һ��")
        insert_dict = {}
        insert_dict['NCCWKDAT']   = wtrbka_record_dict['NCCWKDAT']
        insert_dict['SNDBNKCO']   = wtrbka_record_dict['SNDBNKCO']
        insert_dict['TRCDAT']     = wtrbka_record_dict['TRCDAT']
        insert_dict['TRCNO']      = wtrbka_record_dict['TRCNO']
        insert_dict['RCVBNKCO']   = wtrbka_record_dict['RCVBNKCO']
        insert_dict['SNDMBRCO']   = wtrbka_record_dict['SNDMBRCO']
        insert_dict['RCVMBRCO']   = wtrbka_record_dict['RCVMBRCO']
        insert_dict['TRCCO']      = wtrbka_record_dict['TRCCO']
        insert_dict['DCFLG']      = wtrbka_record_dict['DCFLG']
        insert_dict['PYRACC']     = wtrbka_record_dict['PYRACC']
        insert_dict['PYEACC']     = wtrbka_record_dict['PYEACC']
        insert_dict['CUR']        = 'CNY'
        insert_dict['OCCAMT']     = wtrbka_record_dict['OCCAMT']
        insert_dict['LOCOCCAMT']  = wtrbka_record_dict['OCCAMT'] 
        if(wtrbka_record_dict['TRCCO'] in ('3000102','3000103','3000104','3000105') and wtrbka_record_dict['CHRGTYP'] == '1'):
            insert_dict['CUSCHRG']    = wtrbka_record_dict['CUSCHRG']
            insert_dict['LOCCUSCHRG'] = wtrbka_record_dict['CUSCHRG']
        else:
            insert_dict['CUSCHRG']    = 0.00
            insert_dict['LOCCUSCHRG'] = 0.00
        insert_dict['ORTRCNO']    = ""
        insert_dict['BJEDTE']     = wtrbka_record_dict['BJEDTE']
        insert_dict['BSPSQN']     = wtrbka_record_dict['BSPSQN']
        insert_dict['EACTYP']     = ""
        insert_dict['EACINF']     = ""
        insert_dict['LOCEACTYP']  = ""
        insert_dict['LOCEACINF']  = ""
        insert_dict['ISDEAL']     = "0"
        insert_dict['NOTE1']      = ""
        insert_dict['NOTE2']      = ""
        insert_dict['NOTE3']      = ""
        insert_dict['NOTE4']      = ""
        
        #=====����˵Ǽǲ��в��Ǵ˱ʽ���====
        if not rccpsDBTrcc_tddzcz.insertCmt(insert_dict):
            return AfaFlowControl.ExitThisFlow('A099','����˵Ǽǲ��в��ǽ���ʧ��')
            
        #=====������˵Ǽǲ������ղ�������ݲ����====
        AfaLoggerFunc.tradeInfo("<<<<<<������˵Ǽǲ�")
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
        if(tddzcz_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ�ʧ��')
        elif(len(tddzcz_record_dict) == 0):
            return AfaFlowControl.ExitThisFlow('A099','��ѯͨ���˵Ǽǲ����Ϊ��')
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<������˵Ǽǲ��ɹ�")
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<��ѯ���˵Ǽǲ��ɹ�")
    
    #=====�жϴ˱�ҵ���Ƿ��Ѿ�����====
    if(tddzcz_record_dict['ISDEAL'] == PL_ISDEAL_ISDO):
        return AfaFlowControl.ExitThisFlow('A099','�˱������Ѿ������')
        
    #=====��ʼ����Ĩ��====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ����Ĩ��")
    input_dict = {}   
    input_dict['PYRACC']  = wtrbka_record_dict['PYRACC'] 
    input_dict['PYRNAM']  = wtrbka_record_dict['PYRNAM'] 
    input_dict['PYEACC']  = wtrbka_record_dict['PYEACC'] 
    input_dict['PYENAM']  = wtrbka_record_dict['PYENAM'] 
    input_dict['CHRGTYP'] = wtrbka_record_dict['CHRGTYP']    
    input_dict['OCCAMT']  = wtrbka_record_dict['OCCAMT']
    input_dict['CUSCHRG'] = wtrbka_record_dict['CUSCHRG']
    input_dict['RCCSMCD'] = PL_RCCSMCD_CX
    TradeContext.NCCworkDate = wtrbka_record_dict['NCCWKDAT']
    TradeContext.BESBNO = wtrbka_record_dict['BESBNO']
    TradeContext.BETELR = PL_BETELR_AUTO
    TradeContext.TERMID = wtrbka_record_dict['TERMID']
        
    #=====�ж�ԭ���׵�������ʾ====
    AfaLoggerFunc.tradeInfo("<<<<<<�ж�ԭ���������˻�������")
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):
        AfaLoggerFunc.tradeInfo("<<<<<ԭҵ��Ϊ����")
        
        TradeContext.BRSFLG   = PL_BRSFLG_SND
        
        if(wtrbka_record_dict['TRCCO'] in ('3000002','3000004')):
            AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ������Ĩ��")
            rccpsEntriesErr.KZTCWZMZ(input_dict)
        
        elif(wtrbka_record_dict['TRCCO'] in ('3000003','3000005')):
            AfaLoggerFunc.tradeDebug("<<<<<<���۱�ת������Ĩ��")
            rccpsEntriesErr.KZBZYWZMZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000102','3000104')):
            AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ������Ĩ��")
            rccpsEntriesErr.KZTDWZMZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000103','3000105')):
            AfaLoggerFunc.tradeDebug("<<<<<<������ת������Ĩ��")    
            rccpsEntriesErr.KZYZBWZMZ(input_dict)     
            
        else:
            return AfaFlowControl.ExitThisFlow('S999','�Ƿ����״���')
            
    else:
        AfaLoggerFunc.tradeInfo("<<<<<ԭҵ��Ϊ����")      
        
        TradeContext.BRSFLG   = PL_BRSFLG_RCV

        if(wtrbka_record_dict['TRCCO'] in ('3000002','3000004')):
            AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ������Ĩ��")
            rccpsEntriesErr.KZTCLZMZ(input_dict)
        
        elif(wtrbka_record_dict['TRCCO'] in ('3000003','3000005')):
            AfaLoggerFunc.tradeDebug("<<<<<<���۱�ת������Ĩ��")
            rccpsEntriesErr.KZBZYLZMZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000102','3000104')):
            AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ������Ĩ��")
            rccpsEntriesErr.KZTDLZMZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000103','3000105')):
            AfaLoggerFunc.tradeDebug("<<<<<<������ת������Ĩ��")    
            rccpsEntriesErr.KZYZBLZMZ(input_dict)     
            
        else:
            return AfaFlowControl.ExitThisFlow('S999','�Ƿ����״���')
            
    #=====�жϵ�ǰ״̬�Ƿ�����Ĩ��====
#    AfaLoggerFunc.tradeInfo("<<<<<<�жϽ��׵�ǰ״̬�Ƿ�����Ĩ��")
#    stat_dict = {}
#    res = rccpsState.getTransStateCur(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],stat_dict)
#    if(res == False):
#        return AfaFlowControl.ExitThisFlow('A099','��ѯҵ��ĵ�ǰ״̬ʧ��')
#    else:
#        AfaLoggerFunc.tradeInfo("��ѯҵ��ǰ״̬�ɹ�")
#            
#    if(stat_dict['BCSTAT'] in (PL_BCSTAT_HCAC,PL_BCSTAT_CANC,PL_BCSTAT_CANCEL) and stat_dict['BDWFLG'] == PL_BDWFLG_SUCC):
#        return AfaFlowControl.ExitThisFlow('S999','ԭҵ��ǰ״̬����ҪĨ�ˣ����ֹ����Ĵ����ʶ')
    
    
    acc = 0 
    autopay = 0
    auto = 0   
    hcac = 0    
    canc = 0
    cancel = 0
    #=====��ѯ�Ƿ��м��˳ɹ���״̬====
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,sstlog_list):
        acc = len(sstlog_list)
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_AUTOPAY,PL_BDWFLG_SUCC,sstlog_list):
        autopay = len(sstlog_list)
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_AUTO,PL_BDWFLG_SUCC,sstlog_list):
        auto = len(sstlog_list)
    #=====��ѯ�Ƿ���Ĩ�˵�״̬====
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_SUCC,sstlog_list):
        hcac = len(sstlog_list)
    #=====��ѯ�Ƿ��г�����״̬====
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_SUCC,sstlog_list):
        canc = len(sstlog_list)
    #=====��ѯ�Ƿ��г�����״̬====
    ssltog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC,sstlog_list):
        cancel = len(sstlog_list)
    
    if((acc + autopay + auto) - (hcac + canc + cancel) <= 0):
        return AfaFlowControl.ExitThisFlow('S999','�˽���δ���˻���Ĩ�ˣ���ֹ�ύ')
        
    AfaLoggerFunc.tradeInfo("<<<<<<�����жϽ��׵�ǰ״̬�Ƿ�����Ĩ��")
            
        
    #=====��������ǰ����ԭ���׵�״̬====
    AfaLoggerFunc.tradeInfo("<<<<<<��������ǰ����ԭ���׵�״̬")
    if not rccpsState.newTransState(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ΪĨ�˴������쳣')
    else:
        AfaDBFunc.CommitSql()
        
    #=====��ʼ������������====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������������")
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("<<<<<<����������������")
    
    AfaLoggerFunc.tradeInfo("<<<<<<����Ĩ�˽���")
    
    #=====��״̬�ֵ丳ֵ====
    state_dict = {}
    state_dict['BJEDTE'] = wtrbka_record_dict['BJEDTE']
    state_dict['BSPSQN'] = wtrbka_record_dict['BSPSQN']
    state_dict['BCSTAT'] = PL_BCSTAT_HCAC
    state_dict['MGID']   = TradeContext.errorCode
    state_dict['STRINFO']= TradeContext.errorMsg
    if TradeContext.existVariable('TRDT'):
        state_dict['TRDT']   = TradeContext.TRDT
    if TradeContext.existVariable('TLSQ'):
        state_dict['TLSQ']   = TradeContext.TLSQ
    if TradeContext.existVariable('RBSQ'): 
        state_dict['RBSQ'] = TradeContext.RBSQ
    if TradeContext.existVariable('FEDT'):
        state_dict['FEDT'] = TradeContext.FEDT

    
    #=====�ж�����Ĩ���Ƿ�ɹ�====
    AfaLoggerFunc.tradeInfo("<<<<<<�ж�����Ĩ���Ƿ�ɹ�")
    AfaLoggerFunc.tradeDebug("<<<<<<errorCode=" + TradeContext.errorCode)
    if(TradeContext.errorCode != '0000'):
        AfaLoggerFunc.tradeDebug("����Ĩ��ʧ��")
        #=====���������ԭ����Ϊʧ��====
        AfaLoggerFunc.tradeInfo("<<<<<<���������ԭ����ΪĨʧ��")
        state_dict['BDWFLG'] = PL_BDWFLG_FAIL
        state_dict['STRINFO'] = TradeContext.errorMsg
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��Ϊʧ���쳣')
        else:
            AfaDBFunc.CommitSql()
       
        return AfaFlowControl.ExitThisFlow('S999','����Ĩ��ʧ��')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<����Ĩ�˳ɹ�")
        
    #=====���������ԭ����״̬=====
    AfaLoggerFunc.tradeInfo("<<<<<<���������ԭ����Ϊ�ɹ�")
    state_dict['BDWFLG'] = PL_BDWFLG_SUCC
    state_dict['STRINFO'] = '�����ɹ�'
    if not rccpsState.setTransState(state_dict):
        return AfaFlowControl.ExitThisFlow('S999','����ҵ��Ϊ�ɹ��쳣')
    else:
        AfaDBFunc.CommitSql()
    
    #=====���Ĵ��˵Ǽǲ��еĴ����ʾ====
    AfaLoggerFunc.tradeInfo("<<<<<<���Ĵ��˵Ǽǲ��еĴ����ʾ")
    where_dict = {}
    where_dict = {'BJEDTE':tddzcz_record_dict['BJEDTE'],'BSPSQN':tddzcz_record_dict['BSPSQN']}
    update_dict = {}
    update_dict['ISDEAL'] = PL_ISDEAL_ISDO
    update_dict['NOTE3']  = '�˱ʴ�����Ĩ��'
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if(res == -1):
        return AfaFlowControl.ExitThisFlow('S999','����Ĩ�˳ɹ�,�����´��˴����ʾʧ�ܣ����ֹ����´��˴����ʾ')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<���Ĵ��˵Ǽǲ��еĴ����ʾ�ɹ�")
        
    #=====���·���֪ͨ���в�������====
    AfaLoggerFunc.tradeInfo("<<<<<<��֪ͨ���в�������")
    insert_dict = {}
    insert_dict['NOTDAT']  = TradeContext.BJEDTE
    insert_dict['BESBNO']  = wtrbka_record_dict['BESBNO']
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_RCV):
        insert_dict['STRINFO'] = "�˱ʴ���["+wtrbka_record_dict['BSPSQN']+"]["+wtrbka_record_dict['BJEDTE']+"]����Ĩ�˴���"
    else:
        insert_dict['STRINFO'] = "�˱ʴ���["+wtrbka_record_dict['BSPSQN']+"]["+wtrbka_record_dict['BJEDTE']+"]����Ĩ�˴��� ����8522��������ƾ֤"
    if not rccpsDBTrcc_notbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','���·���֪ͨ���в�������ʧ��')
    AfaLoggerFunc.tradeInfo("<<<<<<��֪ͨ���в������ݳɹ�")
        
    #=====������ӿڸ�ֵ=====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������ӿڸ�ֵ")
    TradeContext.BOSPSQ     = wtrbka_record_dict['BSPSQN']
    TradeContext.BOJEDT     = wtrbka_record_dict['BJEDTE']
    TradeContext.TLSQ       = TradeContext.TLSQ
    TradeContext.BRSFLG     = wtrbka_record_dict['BRSFLG']
    TradeContext.TRCCO      = wtrbka_record_dict['TRCCO']
    TradeContext.BEACSB     = wtrbka_record_dict['BESBNO']
    TradeContext.OROCCAMT   = str(wtrbka_record_dict['OCCAMT'])
    TradeContext.ORCUR      = wtrbka_record_dict['CUR']
    TradeContext.ORSNDBNK   = wtrbka_record_dict['SNDBNKCO']
    TradeContext.ORSNDBNKNM = wtrbka_record_dict['SNDBNKNM']
    TradeContext.ORRCVBNK   = wtrbka_record_dict['RCVBNKCO']
    TradeContext.ORRCVBNKNM = wtrbka_record_dict['RCVBNKNM']
    TradeContext.ORPYRACC   = wtrbka_record_dict['PYRACC']
    TradeContext.ORPYRNAM   = wtrbka_record_dict['PYRNAM']
    TradeContext.ORPYEACC   = wtrbka_record_dict['PYEACC']
    TradeContext.ORPYENAM   = wtrbka_record_dict['PYENAM']
#    TradeContext.SBAC       = 
#    TradeContext.RBAC       = 

    AfaLoggerFunc.tradeDebug("<<<<<<OROCCAMT="+str(TradeContext.OROCCAMT))
    AfaLoggerFunc.tradeInfo("<<<<<<����������ӿڸ�ֵ")
        
    AfaLoggerFunc.tradeInfo("<<<<<<<���Ի�����(���ز���) �˳�")
    
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.���Ĩ��[8571] �˳�")
    
    return True
