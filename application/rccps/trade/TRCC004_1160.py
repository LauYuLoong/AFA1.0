# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.回执类操作模板(1.回执操作).存款确认应答报文接收
#==============================================================================
#   交易文件:   TRCC004_0000.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-10-22
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_mpcbka,rccpsDBTrcc_atcbka


#=====================回执个性化处理(本地操作)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo(" 农信银系统：来账.中心类操作(1.回执操作).存款确认应答报文接收[TRCC004_1160]进入 ")
    
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #=================匹配原交易信息===========================================
    AfaLoggerFunc.tradeInfo(">>>开始匹配原请求交易信息")
    
    wtr_dict = {}
    if not rccpsDBFunc.getTransWtrCK(TradeContext.SNDBNKCO,TradeContext.TRCDAT,TradeContext.TRCNO,wtr_dict):
        return AfaFlowControl.ExitThisFlow('S999', "匹配原请求交易信息异常")
    
    TradeContext.BJEDTE = wtr_dict['BJEDTE']
    TradeContext.BSPSQN = wtr_dict['BSPSQN']
    
    AfaLoggerFunc.tradeInfo(">>>结束匹配原请求交易信息")
    
    #=================必要性检查===============================================
    AfaLoggerFunc.tradeInfo(">>>开始进行必要性检查")
    
    #=================如果此交易已被冲正或冲销,则停止处理============================
    
    where_sql = "ORMFN = '" + wtr_dict['MSGFLGNO'] + "'"
    
    AfaLoggerFunc.tradeInfo(">>>开始检查此交易是否已被冲正")
    
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
    
    AfaLoggerFunc.tradeInfo(">>>结束进行必要性检查")
    
    #=================设置业务状态为清算=======================================
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为清算处理中")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFESTL,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为清算处理中异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为清算处理中")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为清算成功")
    
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['BCSTAT']  = PL_BCSTAT_MFESTL
    stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
    stat_dict['PRCCO']   = TradeContext.PRCCO
    stat_dict['STRINFO'] = TradeContext.STRINFO
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为清算成功异常")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为清算成功")
    
    AfaLoggerFunc.tradeInfo(" 农信银系统：来账.中心类操作(1.回执操作).存款确认应答报文接收[TRCC004_1160]退出 ")
    
    return True
