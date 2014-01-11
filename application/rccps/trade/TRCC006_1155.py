# -*- coding: gbk -*-
###############################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).折本转异应答报文接收
#==============================================================================
#   交易文件:   TRCC006_1155.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷 
#   修改时间:   2008-10-21
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsGetFunc,rccpsHostFunc,rccpsEntries
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_atcbka,rccpsDBTrcc_mpcbka


#=====================交易前处理(登记流水,中心前处理)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo(" 农信银系统：来账.中心类操作(1.本地操作).折本转异应答报文接收[TRCC006_1155]进入 ")

    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)

    #=================必要性检查===============================================
    AfaLoggerFunc.tradeInfo(">>>开始必要性检查")
    #=================若交易已被冲正或冲销,则停止处理================================
    
    AfaLoggerFunc.tradeInfo(">>>开始检查此交易是否已被冲正")
    
    where_sql = "ORMFN = '" + TradeContext.ORMFN + "'"
    
    ret = rccpsDBTrcc_atcbka.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","查询冲正登记簿异常,退出主流程")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","冲正登记簿中存在对此交易的冲正,退出主流程")
        
    AfaLoggerFunc.tradeInfo(">>>结束检查此交易是否已被冲正")
    
    AfaLoggerFunc.tradeInfo(">>>开始检查此交易是否已被冲销")
    
    ret = rccpsDBTrcc_mpcbka.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","查询冲销登记簿异常,退出主流程")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","冲销登记簿中存在对此交易的冲销,退出主流程")
        
    AfaLoggerFunc.tradeInfo(">>>结束检查此交易是否已被冲销")
        
    AfaLoggerFunc.tradeInfo(">>>结束必要性检查")
    
    #=================匹配原交易信息===========================================
    AfaLoggerFunc.tradeInfo(">>>开始匹配原交易")
    
    wtr_dict = {}
    
    if not rccpsDBFunc.getTransWtrAK(TradeContext.SNDBNKCO,TradeContext.TRCDAT,TradeContext.TRCNO,wtr_dict):
        return AfaFlowControl.ExitThisFlow('S999', "未找到原存款请求交易,停止处理")
    
    TradeContext.BJEDTE  = wtr_dict['BJEDTE']
    TradeContext.BSPSQN  = wtr_dict['BSPSQN']
    TradeContext.TRCCO   = wtr_dict['TRCCO']
    TradeContext.BESBNO  = wtr_dict['BESBNO']
    TradeContext.BETELR  = wtr_dict['BETELR']
    TradeContext.OCCAMT  = str(wtr_dict['OCCAMT'])
    TradeContext.CHRGTYP = wtr_dict['CHRGTYP']
    TradeContext.LOCCUSCHRG = str(wtr_dict['CUSCHRG'])
    TradeContext.PYRTYP  = wtr_dict['PYRTYP']
    TradeContext.PYRACC  = wtr_dict['PYRACC']
    TradeContext.PYRNAM  = wtr_dict['PYRNAM']
    TradeContext.CERTTYPE = wtr_dict['CERTTYPE']
    TradeContext.CERTNO  = wtr_dict['CERTNO']
    TradeContext.TERMID  = wtr_dict['TERMID']
    TradeContext.WARNTNO = wtr_dict['BNKBKNO']
    
    AfaLoggerFunc.tradeInfo(">>>结束匹配原交易")
    
    #=================若应答报文回复拒绝,则设置状态为拒绝,停止处理=============
    if TradeContext.PRCCO != 'RCCI0000':
        AfaLoggerFunc.tradeInfo(">>>对方返回拒绝应答")
        #=============设置业务状态为拒绝处理中=================================
        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为拒绝处理中异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRCCO']   = TradeContext.PRCCO
        stat_dict['STRINFO'] = TradeContext.STRINFO
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为拒绝成功异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
        #=============发起主机抹账=============================================
        AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为抹账处理中")
        
        
        #=====特殊处理  关彬捷 20081127 调8813抹账,需产生新的前置流水号进行记账====
        if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
            return AfaFlowControl.ExisThisFlow('S999',"产生新的前置流水号异常")
              
        
        #为抹账赋值会计分录
        entries_dict = {}
        entries_dict['FEDT']     = wtr_dict['BJEDTE']
        entries_dict['RBSQ']     = wtr_dict['BSPSQN']
        entries_dict['PYRACC']   = wtr_dict['PYRACC']
        entries_dict['PYRNAM']   = wtr_dict['PYRNAM']
        entries_dict['PYEACC']   = wtr_dict['PYEACC']
        entries_dict['PYENAM']   = wtr_dict['PYENAM']
        entries_dict['OCCAMT']   = wtr_dict['OCCAMT']
        entries_dict['CHRGTYP']  = wtr_dict['CHRGTYP']
        entries_dict['CUSCHRG']  = wtr_dict['CUSCHRG']
        entries_dict['RCCSMCD']  = PL_RCCSMCD_CZ
        TradeContext.BRSFLG      = PL_BRSFLG_SND
        
        rccpsEntries.KZBZYWZMZ(entries_dict)
          
        #====设置业务状态为抹账处理中====        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为抹账处理中异常')
        
        AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为抹账处理中")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
        #====自动抹账====
        AfaLoggerFunc.tradeInfo(">>>开始发起主机抹账")
        
        #=====调起抹账主机接口====
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo(">>>结束发起主机抹账")
        
        stat_dict = {}
        
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['MGID']    = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        if TradeContext.errorCode == '0000':
            AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为抹账成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            stat_dict['TRDT']   = TradeContext.TRDT
            stat_dict['TLSQ']   = TradeContext.TLSQ
            stat_dict['PRTCNT'] = 1
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态抹账成功异常')
            
            AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为抹账成功")
            
        else:
            AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为抹账失败")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态抹账成功异常')
            
            AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为抹账失败")
            
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
        return AfaFlowControl.ExitThisFlow("S999","对方拒绝,停止处理")
    
    else:
        AfaLoggerFunc.tradeInfo(">>>对方返回成功应答")

    #=================设置业务状态为确认付款处理中=============================
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为确认付款处理中")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CONFPAY,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为确认付款处理中异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为确认付款处理中")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    #=================更新存款确认委托日期和交易流水号=========================
    AfaLoggerFunc.tradeInfo(">>>开始更新存款确认委托日期和交易流水号")
    
    wtrbka_update_dict = {}
    wtrbka_update_dict['COTRCDAT'] = TradeContext.TRCDAT
    wtrbka_update_dict['COTRCNO']  = TradeContext.SerialNo
    wtrbka_update_dict['COMSGFLGNO'] = TradeContext.RCVMBRCO + TradeContext.TRCDAT + TradeContext.SerialNo
    
    wtrbka_where_dict = {}
    wtrbka_where_dict['BJEDTE'] = TradeContext.BJEDTE
    wtrbka_where_dict['BSPSQN'] = TradeContext.BSPSQN
    
    ret = rccpsDBTrcc_wtrbka.update(wtrbka_update_dict,wtrbka_where_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999', "更新存款确认委托日期和交易流水号异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束更新存款确认委托日期和交易流水号")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    #=================为存款确认请求报文做准备=================================
    AfaLoggerFunc.tradeInfo(">>>开始为存款确认请求报文做准备")
    
    TradeContext.MSGTYPCO = 'SET009'
    TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO
    TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    #TradeContext.SNDTRDAT = TradeContext.BJEDTE
    #TradeContext.SNDTRTIM = TradeContext.BJETIM
    #TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = TradeContext.ORMFN
    TradeContext.OPRTYPNO = '30'
    TradeContext.ROPRTPNO = '30'
    TradeContext.TRANTYP  = '0'
    
    TradeContext.ORTRCCO  = TradeContext.TRCCO
    TradeContext.ORTRCNO  = TradeContext.TRCNO
    TradeContext.TRCCO    = '3000503'
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.CURPIN   = ""
    TradeContext.STRINFO  = '收到存款应答,自动发送存款确认'
    
    AfaLoggerFunc.tradeInfo(">>>结束为存款确认请求报文做准备")
    
    AfaLoggerFunc.tradeInfo(" 农信银系统：来账.中心类操作(1.本地操作).卡本转异应答报文接收[TRCC006_1155]退出 ")
    return True


#=====================交易后处理===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo(" 农信银系统：来账.中心类操作(2.中心回执).卡本转异应答报文接收[TRCC006_1155]进入 ")

    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['BCSTAT']  = PL_BCSTAT_CONFPAY
    stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
    stat_dict['PRCCO']   = TradeContext.errorCode
    stat_dict['STRINFO'] = TradeContext.errorMsg
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        #=====发送农信银成功,设置状态为确认付款成功====
        stat_dict['BCSTAT']  = PL_BCSTAT_CONFPAY
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为确认付款成功异常")
        
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为确认付款成功")
    else:
        #=====发送农信银失败,设置状态为确认付款失败====       
        stat_dict['BCSTAT']  = PL_BCSTAT_CONFPAY
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为确认付款失败异常")
        
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为确认付款失败")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    AfaLoggerFunc.tradeInfo(" 农信银系统：来账.中心类操作(2.中心回执).卡本转异应答报文接收[TRCC006_1155]退出 ")
    
    return True
        
