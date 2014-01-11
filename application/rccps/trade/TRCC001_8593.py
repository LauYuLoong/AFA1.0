# -*- coding: gbk -*-                                             
##################################################################
#   ũ����.ͨ��ͨ�����˽���.�������˲���                    
#=================================================================
#   �����ļ�:   TRCC001_8593.py                                   
#   �޸�ʱ��:   20089-01-04                                        
#   ���ߣ�      �˹�ͨ                                            
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,rccpsState,AfaDBFunc,rccpsEntriesErr,rccpsHostFunc,rccpsFunc,rccpsGetFunc,rccpsState,rccpsEntriesErr
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_paybnk,rccpsDBTrcc_notbka,rccpsDBTrcc_spbsta,rccpsDBTrcc_subbra
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.�������˲���[8593] ����")
    
    #=====�жϱ�������Ƿ����====
    if not TradeContext.existVariable("BESBNO"):
        return AfaFlowControl.ExitThisFlow('A099','û�л�����')
        
    if not TradeContext.existVariable("TRCCO"):
        return AfaFlowControl.ExitThisFlow('A099','û�н��״���')
        
    if not TradeContext.existVariable("CUSCHRG"):
        return AfaFlowControl.ExitThisFlow('A099','û�������ѽ��')
        
    if not TradeContext.existVariable("OCCAMT"):
        return AfaFlowControl.ExitThisFlow('A099','û�н��׽��')
        
    #=====�õ��˻��Ŀ�������====
    AfaLoggerFunc.tradeInfo("<<<<<<��ѯ�˻���������")
    
    TradeContext.HostCode = '8810'
    TradeContext.BETELR   = PL_BETELR_AUTO
    
    if(TradeContext.TRCCO in ('3000102','3000103','3000104','3000105')):
        TradeContext.ACCNO = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug("ACCNO<<<<<<" + TradeContext.ACCNO)
    else:
        TradeContext.ACCNO = TradeContext.PYEACC
        AfaLoggerFunc.tradeDebug("ACCNO<<<<<<" + TradeContext.ACCNO)
        
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    
    AfaLoggerFunc.tradeDebug("errorCode<<<<<<" + TradeContext.errorCode)
    AfaLoggerFunc.tradeDebug("errorMsg<<<<<<" + TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo("<<<<<<�ж�����8810�����Ƿ�ɹ�")
    if(TradeContext.errorCode != '0000'):
        return AfaFlowControl.ExitThisFlow('S999',TradeContext.errorMsg)
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<8810���׳ɹ�")
        TradeContext.BESBNO = TradeContext.ACCSO
        
    AfaLoggerFunc.tradeInfo("<<<<<<������ѯ�˻���������")
    
    #=====���ɱ������,��Ա�кţ������кţ���������,ǰ�����ڣ�ǰ����ˮ��====
#    if not rccpsFunc.GetNCCDate( ) :                      #NCCWKDAT
#        raise AfaFlowControl.flowException( )
#    TradeContext.NCCWKDAT = TradeContext.NCCworkDate

    TradeContext.NCCworkDate = TradeContext.NCCWKDAT
   
    where_dict = {}                                       #���ͳ�Ա�к�
    where_dict['BANKBIN'] = TradeContext.SNDBNKCO
    record = rccpsDBTrcc_paybnk.selectu(where_dict)
    if(record == None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ�����кű�ʧ��')
    elif(len(record) == 0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ�����кű���Ϊ��')
    else:
        TradeContext.STLBANKBIN = record['STLBANKBIN']    
    
#    where_dict = {}                                       #�����кţ���������
#    where_dict['BESBNO'] = TradeContext.BESBNO
#    record_tmp = rccpsDBTrcc_subbra.selectu(where_dict)
#    if(record_tmp == None):
#        return AfaFlowControl.ExitThisFlow('A099','��ѯ������ʧ��')
#    elif(len(record_tmp) == 0):
#        return AfaFlowControl.ExitThisFlow('A099','��ѯ��������Ϊ��')
#    else:
#        TradeContext.BANKBIN = record_tmp['BANKBIN']
#        where_dict = {}
#        where_dict['BANKBIN'] = TradeContext.BANKBIN
#        record = None
#        record = rccpsDBTrcc_paybnk.selectu(where_dict)
#        if(record == None):
#            return AfaFlowControl.ExitThisFlow('A099','��ѯ�����кű�ʧ��')
#        elif(len(record) == 0):
#            AfaLoggerFunc.tradeInfo("�˻������к�")
#            TradeContext.RCVBNKNM = ""
#            TradeContext.RCVBNKCO = ""
#        else:
#            TradeContext.RCVBNKNM = record['BANKNAM']
#            TradeContext.RCVBNKCO = record['BANKBIN']
    
    TradeContext.BJEDTE = AfaUtilTools.GetHostDate( )  #BJEDTE
    
    TradeContext.FEDT = AfaUtilTools.GetHostDate( )      #FEDT
    
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_RCV) == -1 :     #RBSQ
        return AfaFlowControl.ExitThisFlow('S999','��������ǰ����ˮ��ʧ��,��������')
        
    TradeContext.BSPSQN = TradeContext.RBSQ
       
    #=====��ͨ��ͨ��ҵ��Ǽǲ���������====
    AfaLoggerFunc.tradeInfo("<<<<<<�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
    insert_dict = {}
    insert_dict['BJEDTE']     = TradeContext.BJEDTE
    insert_dict['BSPSQN']     = TradeContext.BSPSQN
    insert_dict['BRSFLG']     = "1"
    insert_dict['BEACSB']     = ""
    insert_dict['BETELR']     = TradeContext.BETELR
    insert_dict['BEAUUS']     = TradeContext.BEAUUS
    insert_dict['BEAUPS']     = TradeContext.BEAUPS
    insert_dict['TERMID']     = TradeContext.TERMID
    insert_dict['BESBNO']     = TradeContext.BESBNO
    insert_dict['BBSSRC']     = ""
    insert_dict['DASQ']       = ""
    if(TradeContext.TRCCO in ('3000002','3000003','3000004','3000005')):
        insert_dict['DCFLG']  = PL_DCFLG_DEB
    else:
        insert_dict['DCFLG']  = PL_DCFLG_CRE
        
    if(TradeContext.TRCCO in ('3000002','3000004')):
        insert_dict['OPRNO']  = PL_TDOPRNO_TC
    elif(TradeContext.TRCCO in ('3000003','3000005')):
        insert_dict['OPRNO']  = PL_TDOPRNO_BZY
    elif(TradeContext.TRCCO in ('3000102','3000104')):
        insert_dict['OPRNO']  = PL_TDOPRNO_TD
    else:
        insert_dict['OPRNO']  = PL_TDOPRNO_YZB
    insert_dict['OPRATTNO']   = ""
    insert_dict['NCCWKDAT']   = TradeContext.NCCWKDAT
    insert_dict['TRCCO']      = TradeContext.TRCCO
    insert_dict['TRCDAT']     = TradeContext.TRCDAT
    insert_dict['TRCNO']      = TradeContext.TRCNO
    insert_dict['MSGFLGNO']   = ""
    insert_dict['COTRCDAT']   = ""
    insert_dict['COTRCNO']    = ""
    insert_dict['COMSGFLGNO'] = ""
    insert_dict['SNDMBRCO']   = TradeContext.STLBANKBIN
    insert_dict['RCVMBRCO']   = "1340000008"
    insert_dict['SNDBNKCO']   = TradeContext.SNDBNKCO
    insert_dict['SNDBNKNM']   = TradeContext.SNDBNKNM
    insert_dict['RCVBNKCO']   = TradeContext.RCVBNKCO
    insert_dict['RCVBNKNM']   = TradeContext.RCVBNKNM
    insert_dict['CUR']        = "01"
    insert_dict['OCCAMT']     = TradeContext.OCCAMT
    if(float(TradeContext.CUSCHRG) != 0.00 and TradeContext.CUSCHRG != ""):
        insert_dict['CHRGTYP']= PL_CHRG_TYPE 
        chrgtyp = 1
    else:
        insert_dict['CHRGTYP']= PL_CHRG_CASH
        chrgtyp = 0
    insert_dict['LOCCUSCHRG'] = ""
    insert_dict['CUSCHRG']    = TradeContext.CUSCHRG
    insert_dict['PYRTYP']     = ""
    insert_dict['PYRACC']     = TradeContext.PYRACC 
    insert_dict['PYRNAM']     = TradeContext.PYRNAM  
    insert_dict['PYRADDR']    = "" 
    insert_dict['PYETYP']     = ""
    insert_dict['PYEACC']     = TradeContext.PYEACC
    insert_dict['PYENAM']     = TradeContext.PYENAM 
    insert_dict['PYEADDR']    = "" 
    insert_dict['STRINFO']    = TradeContext.STRINFO
    insert_dict['CERTTYPE']   = ""
    insert_dict['CERTNO']     = ""
    insert_dict['BNKBKNO']    = "" 
    insert_dict['BNKBKBAL']   = ""
    insert_dict['NOTE1']      = "" 
    insert_dict['NOTE2']      = "" 
    insert_dict['NOTE3']      = "" 
    insert_dict['NOTE4']      = "" 
    
    if not rccpsDBTrcc_wtrbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('A099','�Ǽ�ͨ��ͨ�ҵǼǲ�ʧ��')
    
    AfaLoggerFunc.tradeInfo("<<<<<<�����Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")    
    
    #=====��ѯ�ող��뵽ҵ��Ǽǲ��е�����====
    where_dict = {}
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
    wtrbka_record = rccpsDBTrcc_wtrbka.selectu(where_dict)
    if(wtrbka_record == None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ��ҵ��Ǽǲ�ʧ��')
    elif(len(wtrbka_record) == 0):
        return AfaFlowControl.ExitThisFlow('A099','�Ǽ�ͨ��ͨ��ҵ��Ǽǲ����Ϊ��')
    else:
        AfaLoggerFunc.tradeInfo("��ѯͨ��ͨ��ҵ��Ǽǲ��ɹ�")
    
    
    #=====����˵Ǽǲ���������====
    AfaLoggerFunc.tradeInfo("<<<<<<�ǼǴ��˵Ǽǲ�")
    insert_dict = {}
    insert_dict['NCCWKDAT']   = TradeContext.NCCWKDAT 
    insert_dict['SNDBNKCO']   = TradeContext.SNDBNKCO
    insert_dict['TRCDAT']     = TradeContext.TRCDAT
    insert_dict['TRCNO']      = TradeContext.TRCNO
    insert_dict['RCVBNKCO']   = TradeContext.RCVBNKCO
    insert_dict['SNDMBRCO']   = TradeContext.STLBANKBIN
    insert_dict['RCVMBRCO']   = "1340000008"
    insert_dict['TRCCO']      = TradeContext.TRCCO
    if(TradeContext.TRCCO in ('3000002','3000003','3000004','3000005')):
        insert_dict['DCFLG']  = PL_DCFLG_DEB
    else:
        insert_dict['DCFLG']  = PL_DCFLG_CRE
    insert_dict['PYRACC']     = TradeContext.PYRACC
    insert_dict['PYEACC']     = TradeContext.PYEACC
    insert_dict['CUR']        = "01"
    insert_dict['OCCAMT']     = TradeContext.OCCAMT
    insert_dict['LOCOCCAMT']  = TradeContext.OCCAMT
    if(TradeContext.TRCCO in ('3000102','3000103','3000104','3000105') and wtrbka_record['CHRGTYP'] == PL_CHRG_TYPE ):
        insert_dict['CUSCHRG']    = TradeContext.CUSCHRG
        insert_dict['LOCCUSCHRG'] = TradeContext.CUSCHRG
    else:
        insert_dict['CUSCHRG']    = 0.00
        insert_dict['LOCCUSCHRG'] = 0.00
    insert_dict['ORTRCNO']    = ""
    insert_dict['BJEDTE']     = AfaUtilTools.GetHostDate( )
    insert_dict['BSPSQN']     = TradeContext.BSPSQN
    insert_dict['EACTYP']     = "11"
    insert_dict['EACINF']     = "�����ޣ�������"
    insert_dict['LOCEACTYP']  = "11"
    insert_dict['LOCEACINF']  = "�����ޣ�������"
    insert_dict['ISDEAL']     = PL_ISDEAL_UNDO
    insert_dict['NOTE1']      = ""
    insert_dict['NOTE2']      = ""
    insert_dict['NOTE3']      = ""
    insert_dict['NOTE4']      = ""
    
    if not rccpsDBTrcc_tddzcz.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('A099','�Ǽ�ͨ��ͨ�ҵǼǲ�ʧ��')

    AfaLoggerFunc.tradeInfo("<<<<<<�����ǼǴ��˵Ǽǲ�")
    
    #=====��ѯ�ող��뵽ҵ��Ǽǲ��е�����====
    where_dict = {}
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
    tddzcz_record = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if(tddzcz_record == None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ�ʧ��')
    elif(len(tddzcz_record) == 0):
        return AfaFlowControl.ExitThisFlow('A099','�ǼǴ��˵Ǽǲ����Ϊ��')
    else:
        AfaLoggerFunc.tradeInfo("��ѯ���˵Ǽǲ��ɹ�")
    
    #=====��ʼ����Ʒ�¼��ֵ====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ����Ʒ�¼��ֵ")
    TradeContext.BRSFLG   = PL_BRSFLG_RCV
    TradeContext.BETELR   = PL_BETELR_AUTO
    AfaLoggerFunc.tradeInfo("<<<<<<BETELR==" + TradeContext.BETELR)
    input_dict = {}
    input_dict['FEDT']    = TradeContext.FEDT
    input_dict['RBSQ']    = TradeContext.RBSQ
    input_dict['PYRACC']  = wtrbka_record['PYRACC']
    input_dict['PYRNAM']  = wtrbka_record['PYRNAM']
    input_dict['PYEACC']  = wtrbka_record['PYEACC']
    input_dict['PYENAM']  = wtrbka_record['PYENAM']
    input_dict['CHRGTYP'] = wtrbka_record['CHRGTYP']
    input_dict['OCCAMT']  = wtrbka_record['OCCAMT']
    input_dict['CUSCHRG'] = wtrbka_record['CUSCHRG']
    
    if(wtrbka_record['TRCCO'] in ('3000002','3000004')):  
        AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ�����˼���")
        input_dict['RCCSMCD'] = PL_RCCSMCD_XJTCLZ
        rccpsEntriesErr.KZTCLZJZ(input_dict)
        
    elif(wtrbka_record['TRCCO'] in ('3000003','3000005')):
        AfaLoggerFunc.tradeDebug("<<<<<<���۱�ת�����˼���")
        input_dict['RCCSMCD'] = PL_RCCSMCD_BZYLZ
        rccpsEntriesErr.KZBZYLZJZ(input_dict)
        
    elif(wtrbka_record['TRCCO'] in ('3000102','3000104')):
        AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ�����˼���")
        input_dict['RCCSMCD'] = PL_RCCSMCD_XJTDLZ
        rccpsEntriesErr.KZTDLZJZ(input_dict)
        
    elif(wtrbka_record['TRCCO'] in ('3000103','3000105')):
        AfaLoggerFunc.tradeDebug("<<<<<<������ת�����˼���")
        input_dict['RCCSMCD'] = PL_RCCSMCD_YZBLZ
        rccpsEntriesErr.KZYZBLZJZ(input_dict)
    
    else:
        return AfaFlowControl.ExitThisFlow('A099','���״���Ƿ�')
        
    AfaLoggerFunc.tradeInfo("<<<<<<����Ʒ�¼��ֵ����") 
    
    #=====����ǰ����ԭ����״̬====  
    AfaLoggerFunc.tradeInfo("<<<<<<����ǰ����ԭ����״̬")  
    if not rccpsState.newTransState(wtrbka_record['BJEDTE'],wtrbka_record['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ���˴������쳣')
    else:
        AfaDBFunc.CommitSql()
        
    #=====������������====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������������")
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("<<<<<<����������������") 
    
    AfaLoggerFunc.tradeDebug("errorCode<<<<<<" + TradeContext.errorCode)
    AfaLoggerFunc.tradeDebug("errorMsg<<<<<<" + TradeContext.errorMsg)
    
    #=====��״̬�ֵ丳ֵ====
    state_dict = {}
    state_dict['BJEDTE'] = wtrbka_record['BJEDTE']
    state_dict['BSPSQN'] = wtrbka_record['BSPSQN']
    state_dict['MGID']   = TradeContext.errorCode
    if TradeContext.existVariable('TRDT'):
        state_dict['TRDT']   = TradeContext.TRDT
    if TradeContext.existVariable('TLSQ'):
        state_dict['TLSQ']   = TradeContext.TLSQ
    if TradeContext.existVariable('RBSQ'): 
        state_dict['RBSQ'] = TradeContext.RBSQ
    if TradeContext.existVariable('FEDT'):
        state_dict['FEDT'] = TradeContext.FEDT
    
    #=====�ж����������Ƿ�ɹ�====
    AfaLoggerFunc.tradeInfo("<<<<<<�ж����������Ƿ�ɹ�")
    AfaLoggerFunc.tradeDebug("<<<<<<errorCode=" + TradeContext.errorCode)
    if(TradeContext.errorCode != '0000'):
        AfaLoggerFunc.tradeInfo("������������ʧ��")
        #=====���������ԭ����״̬Ϊʧ��====
        state_dict['BDWFLG'] = PL_BDWFLG_FAIL
        state_dict['STRINFO'] = TradeContext.errorMsg
        state_dict['NOTE3'] = "�������˲���ʧ��"
        state_dict['BCSTAT'] = PL_BCSTAT_ACC
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊʧ���쳣')
        else:
            AfaDBFunc.CommitSql()
       
        return AfaFlowControl.ExitThisFlow('S999',TradeContext.errorMsg)
        
    else:
        #=====���������ԭ����״̬Ϊ�ɹ�====
        state_dict['BDWFLG'] = PL_BDWFLG_SUCC
        state_dict['STRINFO'] = '�����ɹ�'
        state_dict['NOTE3'] = "�������˲��ǳɹ�"
        if(TradeContext.TRCCO in('3000002','3000004','3000005','3000003')):    #ͨ��
            state_dict['BCSTAT'] = PL_BCSTAT_AUTO 
        else:
            state_dict['BCSTAT'] = PL_BCSTAT_AUTOPAY
        if(TradeContext.existVariable("SBAC")):
            state_dict['SBAC'] = TradeContext.SBAC
        if(TradeContext.existVariable("RBAC")):
            state_dict['RBAC'] = TradeContext.RBAC
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ʧ��')
        else:
            AfaDBFunc.CommitSql()
            
#        bcsata = ""    #״̬��ʶ
#        if(TradeContext.TRCCO in('3000002','3000004','3000005','3000003')):    #ͨ��
#            bcstat = PL_BCSTAT_AUTO 
#        else:
#            bcstat = PL_BCSTAT_AUTOPAY       
#        if not rccpsState.newTransState(wtrbka_record['BJEDTE'],wtrbka_record['BSPSQN'],bcstat,PL_BDWFLG_SUCC):
#            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬�쳣')
#        else:
#            AfaDBFunc.CommitSql()
        
    #=====���Ĵ��˵Ǽǲ��еĴ����ʾ====
    AfaLoggerFunc.tradeInfo("<<<<<<���Ĵ��˵Ǽǲ��еĴ����ʾ")
    where_dict = {}
    where_dict = {'BJEDTE':tddzcz_record['BJEDTE'],'BSPSQN':tddzcz_record['BSPSQN']}
    update_dict = {}
    update_dict['ISDEAL'] = PL_ISDEAL_ISDO
    update_dict['NOTE3']  = '�˱ʴ����Ѳ���'
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if(res == -1):
        return AfaFlowControl.ExitThisFlow('S999','���������ѳɹ��������´����ʾʧ�ܣ����ֶ����Ĵ����ʾ')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<���Ĵ��˵Ǽǲ��еĴ����ʾ�ɹ�")

    #=====���·���֪ͨ���в�������====
    AfaLoggerFunc.tradeInfo("<<<<<<��֪ͨ���в�������")
    insert_dict = {}
    insert_dict['NOTDAT']  = AfaUtilTools.GetHostDate( )
    insert_dict['BESBNO']  = wtrbka_record['BESBNO']
    if(wtrbka_record['BRSFLG'] == PL_BRSFLG_RCV):
        insert_dict['STRINFO'] = "�˱ʴ���["+wtrbka_record['BSPSQN']+"]["+wtrbka_record['BJEDTE']+"]�Ѵ���"
    else:
        insert_dict['STRINFO'] = "�˱ʴ���["+wtrbka_record['BSPSQN']+"]["+wtrbka_record['BJEDTE']+"]�Ѵ��� ����8522��������ƾ֤"
    if not rccpsDBTrcc_notbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','���·���֪ͨ���в�������ʧ��')
    AfaLoggerFunc.tradeInfo("<<<<<<��֪ͨ���в������ݳɹ�")
    
    
    #=====������ӿڸ�ֵ====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������ӿڸ�ֵ")
    TradeContext.TRCCO      = wtrbka_record['TRCCO']
    TradeContext.BRSFLG     = wtrbka_record['BRSFLG']
    TradeContext.BEACSB     = wtrbka_record['BESBNO']
    TradeContext.OCCAMT     = str(wtrbka_record['OCCAMT'])
    TradeContext.BSPSQN     = state_dict['TLSQ']
    TradeContext.BJEDTE     = wtrbka_record['BJEDTE']
    
    AfaLoggerFunc.tradeInfo("<<<<<<����������ӿڸ�ֵ")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<���Ի�����(���ز���) �˳�")
    
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.�������˲���[8593] �˳�")
    return True
    
    