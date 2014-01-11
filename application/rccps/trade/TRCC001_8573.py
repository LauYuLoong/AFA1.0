# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�����˽���.ͨ��ͨ�Ҳ����Ĩ��
#=================================================================
#   �����ļ�:   TRCC001_8573.py
#   �޸�ʱ��:   2008-12-11
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,rccpsState,AfaDBFunc,rccpsEntriesErr,rccpsHostFunc,rccpsFunc,rccpsGetFunc,rccpsDBFunc
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_sstlog
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.�����Ĩ��[8573] ����")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<���Ի�����(���ز���) ����")
    
    #=====У������ĺϷ���====
    AfaLoggerFunc.tradeInfo("<<<<<<<��ʼУ������ĺϷ���")
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','û��ԭ�����к�')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A099','û�н�����ˮ��')
        
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A099','û��ί������')
        
    AfaLoggerFunc.tradeInfo("<<<<<<<����У������ĺϷ���")
    
    #=====����RBSQ,NCCWKDAT,FEDT====
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
        return AfaFlowControl.ExitThisFlow('A099','����ǰ����ˮ��ʧ��')
        
    if not rccpsFunc.GetNCCDate( ) :            #NCCworkDate
        raise AfaFlowControl.flowException( )

    TradeContext.FEDT = AfaUtilTools.GetHostDate( )
    
    #=====��ѯ���˵Ǽǲ�====
    where_dict = {}
    where_dict={'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT}
    tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if(tddzcz_record_dict == None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ��쳣')
        
    elif(len(tddzcz_record_dict) == 0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ����Ϊ��')
        
    else:
        AfaLoggerFunc.tradeInfo("��ѯ���˵Ǽǲ��ɹ�")
        
    #=======�ж�ԭ�����Ƿ��ѱ�����==
    AfaLoggerFunc.tradeInfo("<<<<<<�ж�ԭ�����Ƿ��ѱ�����")
    if(tddzcz_record_dict['ISDEAL'] == PL_ISDEAL_UNDO):
        return AfaFlowControl.ExitThisFlow('A099','ԭ������δ������')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<ԭ�����ѱ�����")
        
    #=====��ѯԭ������Ϣ====
    AfaLoggerFunc.tradeInfo("<<<<<<��ѯͨ��ͨ��ҵ��Ǽǲ�")
    wtrbka_record_dict = {}
    if not rccpsDBFunc.getTransWtr(tddzcz_record_dict['BJEDTE'],tddzcz_record_dict['BSPSQN'],wtrbka_record_dict):
        return AfaFlowControl.ExitThisFlow('A099','��ѯԭ������Ϣʧ��')
        
    #=====�жϱ�Ĩ����������Ƿ��ǵ���====
    if(wtrbka_record_dict['FEDT'] != AfaUtilTools.GetHostDate( )):
        return AfaFlowControl.ExitThisFlow('A099','ҪĨ���Ľ��׷ǵ��ռ���')
        
    #=====��ʼ����Ĩ��====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ����Ĩ��")
    #=====����������������ֵ====
    TradeContext.BOSPSQ   = wtrbka_record_dict['RBSQ']
    TradeContext.BOJEDT   = wtrbka_record_dict['FEDT']
    TradeContext.HostCode = '8820'   
        
    #=====����ԭ����״̬ΪĨ�˴�����====
    AfaLoggerFunc.tradeInfo("<<<<<<����ԭ����״̬ΪĨ�˴�����")
    if not rccpsState.newTransState(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
        AfaDBFunc.RollBackSql()
        return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ΪĨ�˴������쳣')
    else:
        AfaDBFunc.CommitSql()
        
    #=====��ʼ������������====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������������")
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("<<<<<<����������������")
    
    AfaLoggerFunc.tradeInfo("<<<<<<��������Ĩ��")
    
    #=====��״̬�ֵ丳ֵ====
    state_dict = {}
    state_dict['BJEDTE'] = wtrbka_record_dict['BJEDTE']
    state_dict['BSPSQN'] = wtrbka_record_dict['BSPSQN']
    state_dict['BCSTAT'] = PL_BCSTAT_HCAC
    state_dict['MGID']   = TradeContext.errorCode
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
        #=====����ԭ����״̬ΪĨ��ʧ��====
        AfaLoggerFunc.tradeInfo("<<<<<<����ԭ����״̬ΪĨ��ʧ��")
        state_dict['BDWFLG'] = PL_BDWFLG_FAIL
        state_dict['STRINFO'] = TradeContext.errorMsg
        if not rccpsState.setTransState(state_dict):
            AfaDBFunc.RollBackSql()
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ΪĨ�˳ɹ��쳣')
        else:
            AfaDBFunc.CommitSql()
       
        return AfaFlowControl.ExitThisFlow('S999','����Ĩ��ʧ��')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<����Ĩ�˳ɹ�")
        
    #=====����ԭ����״̬=====
    AfaLoggerFunc.tradeInfo("<<<<<<����ԭ����״̬ΪĨ�˳ɹ�")
    state_dict['BDWFLG'] = PL_BDWFLG_SUCC
    state_dict['STRINFO'] = '�����ɹ�'
    if not rccpsState.setTransState(state_dict):
        AfaDBFunc.RollBackSql()
        return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬ΪĨ�˳ɹ��쳣')
    else:
        AfaDBFunc.CommitSql()
        
    #=====���Ĵ��˵Ǽǲ��еĴ����ʾ====
    AfaLoggerFunc.tradeInfo("<<<<<<���Ĵ��˵Ǽǲ��еĴ����ʾ")
    where_dict = {}
    where_dict = {'BJEDTE':tddzcz_record_dict['BJEDTE'],'BSPSQN':tddzcz_record_dict['BSPSQN']}
    update_dict = {}
    update_dict['ISDEAL'] = PL_ISDEAL_UNDO
    update_dict['NOTE3']  = '�˱ʲ����Ѿ���Ĩ��'
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if(res == -1):
        return AfaFlowControl.ExitThisFlow('S999','���´����ʾʧ��')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<���Ĵ��˵Ǽǲ��еĴ����ʾ�ɹ�")
    
    #=====������ӿڸ�ֵ=====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������ӿڸ�ֵ")
    TradeContext.BOSPSQ     = wtrbka_record_dict['BSPSQN']
    TradeContext.BOJEDT     = wtrbka_record_dict['BJEDTE']
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
    
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.�����Ĩ��[8573] �˳�")
    
    return True