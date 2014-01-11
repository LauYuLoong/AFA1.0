# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑往账交易.通存通兑差错抹账
#=================================================================
#   程序文件:   TRCC001_8571.py
#   修改时间:   2008-12-09
#   作者：      潘广通
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,rccpsState,AfaDBFunc,rccpsEntriesErr,rccpsHostFunc,rccpsFunc,rccpsGetFunc
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_notbka,rccpsDBTrcc_spbsta
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.差错抹账[8571] 进入")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<个性化处理(本地操作) 进入")
    
    #=====校验变量的合法性====
    AfaLoggerFunc.tradeInfo("<<<<<<校验变量的合法性")   
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A099','没有委托日期')
        
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','没有发送行号')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A099','没有交易流水号')
        
    AfaLoggerFunc.tradeInfo("<<<<<<校验变量的合法性结束")
    
    #=====产生FEDT,RBSQ,NCCworkDate,BJEDTE====
    TradeContext.BJEDTE = AfaUtilTools.GetHostDate( )   #BJEDTE
    
    TradeContext.FEDT=AfaUtilTools.GetHostDate( )    #FEDT
    
    if not rccpsFunc.GetNCCDate( ) :                   #NCCworkDate
        raise AfaFlowControl.flowException( )
    
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :   #RBSQ
        return AfaFlowControl.ExitThisFlow('A099','产生前置流水号失败')
    
    #=====查询交易信息====
    AfaLoggerFunc.tradeInfo("<<<<<<开始查询通存通兑业务登记簿")
    where_dict = {}
    where_dict = {'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT}
    wtrbka_record_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
    if(wtrbka_record_dict == None):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑业务登记簿失败')
    
    elif(len(wtrbka_record_dict) == 0):
        return AfaFlowControl.ExitThisFlow('A099','查询通存通兑业务登记簿结果为空')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<查询通存通兑业务登记簿成功")
            
    #=====查询错账登记簿======
    AfaLoggerFunc.tradeInfo("<<<<<<开始查询错账登记簿")
    where_dict = {}
    where_dict = {'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT}
    tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if(tddzcz_record_dict == None):
        return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿失败')
    
    elif(len(tddzcz_record_dict) == 0):
        AfaLoggerFunc.tradeInfo("<<<<<<查询错账登记簿为空，应向其中补记一笔")
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
        
        #=====向错账登记簿中补记此笔交易====
        if not rccpsDBTrcc_tddzcz.insertCmt(insert_dict):
            return AfaFlowControl.ExitThisFlow('A099','向错账登记簿中补记交易失败')
            
        #=====补查错账登记簿，将刚插入的数据查出来====
        AfaLoggerFunc.tradeInfo("<<<<<<补查错账登记簿")
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
        if(tddzcz_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿失败')
        elif(len(tddzcz_record_dict) == 0):
            return AfaFlowControl.ExitThisFlow('A099','查询通错账登记簿结果为空')
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<补查错账登记簿成功")
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<查询错账登记簿成功")
    
    #=====判断此笔业务是否已经处理====
    if(tddzcz_record_dict['ISDEAL'] == PL_ISDEAL_ISDO):
        return AfaFlowControl.ExitThisFlow('A099','此笔账务已经处理过')
        
    #=====开始行内抹账====
    AfaLoggerFunc.tradeInfo("<<<<<<开始行内抹账")
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
        
    #=====判断原交易的往来标示====
    AfaLoggerFunc.tradeInfo("<<<<<<判断原交易是来账还是往账")
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):
        AfaLoggerFunc.tradeInfo("<<<<<原业务为往账")
        
        TradeContext.BRSFLG   = PL_BRSFLG_SND
        
        if(wtrbka_record_dict['TRCCO'] in ('3000002','3000004')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通存往账抹账")
            rccpsEntriesErr.KZTCWZMZ(input_dict)
        
        elif(wtrbka_record_dict['TRCCO'] in ('3000003','3000005')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折本转异往账抹账")
            rccpsEntriesErr.KZBZYWZMZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000102','3000104')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通兑往账抹账")
            rccpsEntriesErr.KZTDWZMZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000103','3000105')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折异转本往账抹账")    
            rccpsEntriesErr.KZYZBWZMZ(input_dict)     
            
        else:
            return AfaFlowControl.ExitThisFlow('S999','非法交易代码')
            
    else:
        AfaLoggerFunc.tradeInfo("<<<<<原业务为来账")      
        
        TradeContext.BRSFLG   = PL_BRSFLG_RCV

        if(wtrbka_record_dict['TRCCO'] in ('3000002','3000004')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通存来账抹账")
            rccpsEntriesErr.KZTCLZMZ(input_dict)
        
        elif(wtrbka_record_dict['TRCCO'] in ('3000003','3000005')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折本转异来账抹账")
            rccpsEntriesErr.KZBZYLZMZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000102','3000104')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折现金通兑来账抹账")
            rccpsEntriesErr.KZTDLZMZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000103','3000105')):
            AfaLoggerFunc.tradeDebug("<<<<<<卡折异转本来账抹账")    
            rccpsEntriesErr.KZYZBLZMZ(input_dict)     
            
        else:
            return AfaFlowControl.ExitThisFlow('S999','非法交易代码')
            
    #=====判断当前状态是否允许抹账====
#    AfaLoggerFunc.tradeInfo("<<<<<<判断交易当前状态是否允许抹账")
#    stat_dict = {}
#    res = rccpsState.getTransStateCur(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],stat_dict)
#    if(res == False):
#        return AfaFlowControl.ExitThisFlow('A099','查询业务的当前状态失败')
#    else:
#        AfaLoggerFunc.tradeInfo("查询业务当前状态成功")
#            
#    if(stat_dict['BCSTAT'] in (PL_BCSTAT_HCAC,PL_BCSTAT_CANC,PL_BCSTAT_CANCEL) and stat_dict['BDWFLG'] == PL_BDWFLG_SUCC):
#        return AfaFlowControl.ExitThisFlow('S999','原业务当前状态不需要抹账，请手工更改处理标识')
    
    
    acc = 0 
    autopay = 0
    auto = 0   
    hcac = 0    
    canc = 0
    cancel = 0
    #=====查询是否有记账成功的状态====
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,sstlog_list):
        acc = len(sstlog_list)
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_AUTOPAY,PL_BDWFLG_SUCC,sstlog_list):
        autopay = len(sstlog_list)
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_AUTO,PL_BDWFLG_SUCC,sstlog_list):
        auto = len(sstlog_list)
    #=====查询是否有抹账的状态====
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_SUCC,sstlog_list):
        hcac = len(sstlog_list)
    #=====查询是否有冲销的状态====
    sstlog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_SUCC,sstlog_list):
        canc = len(sstlog_list)
    #=====查询是否有冲正的状态====
    ssltog_list = []
    if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC,sstlog_list):
        cancel = len(sstlog_list)
    
    if((acc + autopay + auto) - (hcac + canc + cancel) <= 0):
        return AfaFlowControl.ExitThisFlow('S999','此交易未记账或已抹账，禁止提交')
        
    AfaLoggerFunc.tradeInfo("<<<<<<结束判断交易当前状态是否允许抹账")
            
        
    #=====在上主机前设置原交易的状态====
    AfaLoggerFunc.tradeInfo("<<<<<<在上主机前设置原交易的状态")
    if not rccpsState.newTransState(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999','设置业务状态为抹账处理中异常')
    else:
        AfaDBFunc.CommitSql()
        
    #=====开始调用主机交易====
    AfaLoggerFunc.tradeInfo("<<<<<<开始调用主机交易")
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("<<<<<<结束调用主机交易")
    
    AfaLoggerFunc.tradeInfo("<<<<<<行内抹账结束")
    
    #=====给状态字典赋值====
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

    
    #=====判断主机抹账是否成功====
    AfaLoggerFunc.tradeInfo("<<<<<<判断主机抹账是否成功")
    AfaLoggerFunc.tradeDebug("<<<<<<errorCode=" + TradeContext.errorCode)
    if(TradeContext.errorCode != '0000'):
        AfaLoggerFunc.tradeDebug("主机抹账失败")
        #=====主机后更改原交易为失败====
        AfaLoggerFunc.tradeInfo("<<<<<<主机后更改原交易为抹失败")
        state_dict['BDWFLG'] = PL_BDWFLG_FAIL
        state_dict['STRINFO'] = TradeContext.errorMsg
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','设置业务为失败异常')
        else:
            AfaDBFunc.CommitSql()
       
        return AfaFlowControl.ExitThisFlow('S999','主机抹账失败')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<主机抹账成功")
        
    #=====主机后更改原交易状态=====
    AfaLoggerFunc.tradeInfo("<<<<<<主机后更改原交易为成功")
    state_dict['BDWFLG'] = PL_BDWFLG_SUCC
    state_dict['STRINFO'] = '主机成功'
    if not rccpsState.setTransState(state_dict):
        return AfaFlowControl.ExitThisFlow('S999','设置业务为成功异常')
    else:
        AfaDBFunc.CommitSql()
    
    #=====更改错账登记簿中的处理标示====
    AfaLoggerFunc.tradeInfo("<<<<<<更改错账登记簿中的处理标示")
    where_dict = {}
    where_dict = {'BJEDTE':tddzcz_record_dict['BJEDTE'],'BSPSQN':tddzcz_record_dict['BSPSQN']}
    update_dict = {}
    update_dict['ISDEAL'] = PL_ISDEAL_ISDO
    update_dict['NOTE3']  = '此笔错账已抹账'
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if(res == -1):
        return AfaFlowControl.ExitThisFlow('S999','主机抹账成功,但更新错账处理标示失败，请手工更新错账处理标示')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<更改错账登记簿中的处理标示成功")
        
    #=====向下发的通知表中插入数据====
    AfaLoggerFunc.tradeInfo("<<<<<<向通知表中插入数据")
    insert_dict = {}
    insert_dict['NOTDAT']  = TradeContext.BJEDTE
    insert_dict['BESBNO']  = wtrbka_record_dict['BESBNO']
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_RCV):
        insert_dict['STRINFO'] = "此笔错账["+wtrbka_record_dict['BSPSQN']+"]["+wtrbka_record_dict['BJEDTE']+"]已做抹账处理"
    else:
        insert_dict['STRINFO'] = "此笔错账["+wtrbka_record_dict['BSPSQN']+"]["+wtrbka_record_dict['BJEDTE']+"]已做抹账处理 请用8522补打往账凭证"
    if not rccpsDBTrcc_notbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','向下发的通知表中插入数据失败')
    AfaLoggerFunc.tradeInfo("<<<<<<向通知表中插入数据成功")
        
    #=====给输出接口赋值=====
    AfaLoggerFunc.tradeInfo("<<<<<<开始给输出接口赋值")
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
    AfaLoggerFunc.tradeInfo("<<<<<<结束给输出接口赋值")
        
    AfaLoggerFunc.tradeInfo("<<<<<<<个性化处理(本地操作) 退出")
    
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.差错抹账[8571] 退出")
    
    return True
