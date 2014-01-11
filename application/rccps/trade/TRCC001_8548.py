# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).省中心机构维护
#===============================================================================
#   交易文件:   TRCC001_8548.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷 
#   修改时间:   2008-06-16
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_subbra,rccpsMap8548Dsubbra2CTradeContext,rccpsMap8548CTradeContext2Dsubbra

#=====================个性化处理(本地操作)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***往账.本地类操作(1.本地操作).省中心机构维护[TRC001_8548]进入***' )
    
    #=================判断是否省清算中心========================================
    AfaLoggerFunc.tradeDebug(">>>开始校验机构权限,只有省清算中心才能做此交易")
    
    if TradeContext.BESBNO != PL_BESBNO_BCLRSB:
        return AfaFlowControl.ExitThisFlow("S999","本机构非清算中心,无此交易权限")
    
    AfaLoggerFunc.tradeDebug(">>>结束校验机构权限")
    
    #=================必要性校验================================================
    AfaLoggerFunc.tradeInfo(">>>开始必要性校验")
    
    #=====0 增加====
    if TradeContext.OPRNO == '0':
        #=================校验此机构是否已存在==================================
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        subbra_dict = rccpsDBTrcc_subbra.selectu(subbra_where_dict)
        
        if subbra_dict == None:
            return AfaFlowControl.ExitThisFlow("S999","校验机构是否已存在异常")
        if len(subbra_dict) > 0:
            return AfaFlowControl.ExitThisFlow("S999","机构登记簿中存在此机构")
    #=====0 增加或 1 修改====   
    if TradeContext.OPRNO == '0' or TradeContext.OPRNO == '1':
        #=================校验农信银系统行号是否已被分配========================
        subbra_where_sql = "BANKBIN = '" + TradeContext.BANKBIN + "' and BESBNO != '" + TradeContext.BRNO + "'"
        subbra_count = rccpsDBTrcc_subbra.count(subbra_where_sql)
        
        if subbra_count < 0:
            return AfaFlowControl.ExitThisFlow("S999","校验农信银系统行号是否已被分配异常")        
        if subbra_count > 0:
            return AfaFlowControl.ExitThisFlow("S999","农信银系统行号已被分配给其他机构,禁止提交")
        
    AfaLoggerFunc.tradeInfo(">>>结束必要性校验")
    
    #=================判断操作类型  3  查询====
    if TradeContext.OPRNO == '3':
        AfaLoggerFunc.tradeInfo(">>>开始查询机构信息")
        
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        subbra_dict = {}
        subbra_dict = rccpsDBTrcc_subbra.selectu(subbra_where_dict)
        
        if subbra_dict == None:
            return AfaFlowControl.ExitThisFlow("S999","查询机构登记簿异常")
        if len(subbra_dict) <= 0:
            return AfaFlowControl.ExitThisFlow("S999","机构登记簿中不存在此机构")
        else:
            rccpsMap8548Dsubbra2CTradeContext.map(subbra_dict)
            
        AfaLoggerFunc.tradeInfo(">>>结束查询机构信息")
    #=================操作类型为 0  增加====    
    elif TradeContext.OPRNO == '0':
        AfaLoggerFunc.tradeInfo(">>>开始新增机构信息")
        
        subbra_insert_dict = {}
        rccpsMap8548CTradeContext2Dsubbra.map(subbra_insert_dict)
        
        ret = rccpsDBTrcc_subbra.insertCmt(subbra_insert_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","新增机构信息异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束新增机构信息")
    #=================操作类型为 1  修改====    
    elif TradeContext.OPRNO == '1':
        
        AfaLoggerFunc.tradeInfo(">>>开始修改机构信息")
        
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        subbra_update_dict = {}
        rccpsMap8548CTradeContext2Dsubbra.map(subbra_update_dict)
        
        ret = rccpsDBTrcc_subbra.updateCmt(subbra_update_dict,subbra_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","修改机构信息异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束修改机构信息")
    #=================操作类型为 2  删除====
    elif TradeContext.OPRNO == '2':       
        AfaLoggerFunc.tradeInfo(">>>开始删除机构信息")
        
        subbra_where_dict = {}
        subbra_where_dict['BESBNO'] = TradeContext.BRNO
        
        ret = rccpsDBTrcc_subbra.deleteCmt(subbra_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","删除机构信息异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束删除机构信息")
    
    else:
        #=================操作类型非法==========================================
        return AfaFlowControl.ExitThisFlow("S999","操作类型非法")
        
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '处理成功'
    
    AfaLoggerFunc.tradeInfo( '***往账.本地类操作(1.本地操作).省中心机构维护[TRC001_8548]退出***' )
    
    return True
