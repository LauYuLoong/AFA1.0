# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑往账交易.通存通兑差错补记抹账
#=================================================================
#   程序文件:   TRCC001_8573.py
#   修改时间:   2008-12-11
#   作者：      潘广通
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,rccpsState,AfaDBFunc,rccpsEntriesErr,rccpsHostFunc,rccpsFunc,rccpsGetFunc,rccpsDBFunc
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_sstlog
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.差错补记抹账[8573] 进入")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<个性化处理(本地操作) 进入")
    
    #=====校验变量的合法性====
    AfaLoggerFunc.tradeInfo("<<<<<<<开始校验变量的合法性")
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','没有原发送行号')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A099','没有交易流水号')
        
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A099','没有委托日期')
        
    AfaLoggerFunc.tradeInfo("<<<<<<<结束校验变量的合法性")
    
    #=====产生RBSQ,NCCWKDAT,FEDT====
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
        return AfaFlowControl.ExitThisFlow('A099','产生前置流水号失败')
        
    if not rccpsFunc.GetNCCDate( ) :            #NCCworkDate
        raise AfaFlowControl.flowException( )

    TradeContext.FEDT = AfaUtilTools.GetHostDate( )
    
    #=====查询错账登记簿====
    where_dict = {}
    where_dict={'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT}
    tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
    if(tddzcz_record_dict == None):
        return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿异常')
        
    elif(len(tddzcz_record_dict) == 0):
        return AfaFlowControl.ExitThisFlow('A099','查询错账登记簿结果为空')
        
    else:
        AfaLoggerFunc.tradeInfo("查询错账登记簿成功")
        
    #=======判断原交易是否已被补记==
    AfaLoggerFunc.tradeInfo("<<<<<<判断原交易是否已被补记")
    if(tddzcz_record_dict['ISDEAL'] == PL_ISDEAL_UNDO):
        return AfaFlowControl.ExitThisFlow('A099','原交易尚未被补记')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<原交易已被补记")
        
    #=====查询原交易信息====
    AfaLoggerFunc.tradeInfo("<<<<<<查询通存通兑业务登记簿")
    wtrbka_record_dict = {}
    if not rccpsDBFunc.getTransWtr(tddzcz_record_dict['BJEDTE'],tddzcz_record_dict['BSPSQN'],wtrbka_record_dict):
        return AfaFlowControl.ExitThisFlow('A099','查询原交易信息失败')
        
    #=====判断被抹账务的日期是否是当日====
    if(wtrbka_record_dict['FEDT'] != AfaUtilTools.GetHostDate( )):
        return AfaFlowControl.ExitThisFlow('A099','要抹掉的交易非当日记账')
        
    #=====开始行内抹账====
    AfaLoggerFunc.tradeInfo("<<<<<<开始行内抹账")
    #=====给主机函数参数赋值====
    TradeContext.BOSPSQ   = wtrbka_record_dict['RBSQ']
    TradeContext.BOJEDT   = wtrbka_record_dict['FEDT']
    TradeContext.HostCode = '8820'   
        
    #=====设置原交易状态为抹账处理中====
    AfaLoggerFunc.tradeInfo("<<<<<<设置原交易状态为抹账处理中")
    if not rccpsState.newTransState(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
        AfaDBFunc.RollBackSql()
        return AfaFlowControl.ExitThisFlow('S999','设置业务状态为抹账处理中异常')
    else:
        AfaDBFunc.CommitSql()
        
    #=====开始调用主机交易====
    AfaLoggerFunc.tradeInfo("<<<<<<开始调用主机交易")
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("<<<<<<结束调用主机交易")
    
    AfaLoggerFunc.tradeInfo("<<<<<<结束行内抹账")
    
    #=====给状态字典赋值====
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
    
    #=====判断主机抹账是否成功====
    AfaLoggerFunc.tradeInfo("<<<<<<判断主机抹账是否成功")
    AfaLoggerFunc.tradeDebug("<<<<<<errorCode=" + TradeContext.errorCode)
    if(TradeContext.errorCode != '0000'):
        AfaLoggerFunc.tradeDebug("主机抹账失败")
        #=====更改原交易状态为抹账失败====
        AfaLoggerFunc.tradeInfo("<<<<<<更改原交易状态为抹账失败")
        state_dict['BDWFLG'] = PL_BDWFLG_FAIL
        state_dict['STRINFO'] = TradeContext.errorMsg
        if not rccpsState.setTransState(state_dict):
            AfaDBFunc.RollBackSql()
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为抹账成功异常')
        else:
            AfaDBFunc.CommitSql()
       
        return AfaFlowControl.ExitThisFlow('S999','主机抹账失败')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<主机抹账成功")
        
    #=====更改原交易状态=====
    AfaLoggerFunc.tradeInfo("<<<<<<更改原交易状态为抹账成功")
    state_dict['BDWFLG'] = PL_BDWFLG_SUCC
    state_dict['STRINFO'] = '主机成功'
    if not rccpsState.setTransState(state_dict):
        AfaDBFunc.RollBackSql()
        return AfaFlowControl.ExitThisFlow('S999','设置业务状态为抹账成功异常')
    else:
        AfaDBFunc.CommitSql()
        
    #=====更改错账登记簿中的处理标示====
    AfaLoggerFunc.tradeInfo("<<<<<<更改错账登记簿中的处理标示")
    where_dict = {}
    where_dict = {'BJEDTE':tddzcz_record_dict['BJEDTE'],'BSPSQN':tddzcz_record_dict['BSPSQN']}
    update_dict = {}
    update_dict['ISDEAL'] = PL_ISDEAL_UNDO
    update_dict['NOTE3']  = '此笔补记已经被抹账'
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if(res == -1):
        return AfaFlowControl.ExitThisFlow('S999','更新处理标示失败')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<更改错账登记簿中的处理标示成功")
    
    #=====给输出接口赋值=====
    AfaLoggerFunc.tradeInfo("<<<<<<开始给输出接口赋值")
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
    AfaLoggerFunc.tradeInfo("<<<<<<结束给输出接口赋值")    
        
    AfaLoggerFunc.tradeInfo("<<<<<<<个性化处理(本地操作) 退出")
    
    AfaLoggerFunc.tradeInfo("'***农信银系统：通存通兑往账交易.差错补记抹账[8573] 退出")
    
    return True