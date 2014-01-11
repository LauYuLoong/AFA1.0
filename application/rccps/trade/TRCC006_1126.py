# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).票据查复接收
#===============================================================================
#   模板文件:   TRCC006.py
#   修改时间:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_pjcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1126CTradeContext2Dpjcbka_dict

#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).票据查复接收[RCC00R6_1126]进入***' )
    
    #==========判断是否重复报文,如果是重复报文,直接进入下一流程================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    pjcbka_where_dict = {}
    pjcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    pjcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    pjcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    pjcbka_dict = rccpsDBTrcc_pjcbka.selectu(pjcbka_where_dict)
    
    if pjcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常")
        
        return True
        
    if len(pjcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("票据查复查复登记簿中存在相同查复交易,此报文为重复报文,进入下一流程,发送表示成功的通讯回执")
        #======为通讯回执报文赋值===============================================
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '重复报文'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>结束检查是否重复报文")
    
    #==========判断是否存在原查询交易===========================================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否存在原查询交易")
    or_pjcbka_where_dict = {}
    or_pjcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    or_pjcbka_where_dict['TRCDAT']   = TradeContext.OQTDAT
    or_pjcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    or_pjcbka_dict = {}
    or_pjcbka_dict = rccpsDBTrcc_pjcbka.selectu(or_pjcbka_where_dict)
    
    if or_pjcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验原查询交易失败") 
    
    if len(or_pjcbka_dict) <= 0:
        AfaLoggerFunc.tradeInfo("票据查复查复登记簿中不存在原查询交易,进入下一流程,发送表示成功的通讯回执")
        #======为通讯回执报文赋值===============================================
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '业务状态登记簿中不存在原查询交易'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>结束检查是否存在原查询交易")
    
    #==========为票据查复查复登记簿字典赋值================================
    AfaLoggerFunc.tradeInfo(">>>开始为票据查复查复登记簿字典赋值")
    
    TradeContext.BRSFLG = '1'
    
    if or_pjcbka_dict.has_key('BJEDTE'):
        TradeContext.BOJEDT = or_pjcbka_dict['BJEDTE']
    
    if or_pjcbka_dict.has_key('BSPSQN'):
        TradeContext.BOSPSQ = or_pjcbka_dict['BSPSQN']
    
    #关彬捷 20080728 删除
    #if TradeContext.existVariable('TRCCO'):
    #    TradeContext.ORTRCCO = TradeContext.TRCCO
    TradeContext.ORTRCCO = or_pjcbka_dict['TRCCO']
    
    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    AfaLoggerFunc.tradeDebug(">>>SNDBNKNM" + str(TradeContext.SNDBNKNM) )
    
    pjcbka_insert_dict = {}
    if not rccpsMap1126CTradeContext2Dpjcbka_dict.map(pjcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","为票据查复查复登记簿字典赋值异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束为票据查复查复登记簿字典赋值")
    
    #==========登记会对查询查复自由格式登记簿=======================================
    AfaLoggerFunc.tradeInfo(">>>开始登记此查复业务")
    
    ret = rccpsDBTrcc_pjcbka.insert(pjcbka_insert_dict)
    
    if ret <= 0:
        if not AfaDBFunc.RollbackSql():
            AfaFlowControl.ExitThisFlow("S999","Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        
        return AfaFlowControl.ExitThisFlow("S999","登记票据查复查复登记簿异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束登记此查复业务")
    
    #======更新原查询交易信息===================================================
    AfaLoggerFunc.tradeInfo(">>>开始更新原查询业务信息")
    
    or_pjcbka_update_dict = {}
    or_pjcbka_update_dict['ISDEAL']   = PL_ISDEAL_ISDO
    
    ret = rccpsDBTrcc_pjcbka.update(or_pjcbka_update_dict,or_pjcbka_where_dict)
    if (ret <= 0):
        if not AfaDBFunc.RollbackSql():
            AfaFlowControl.ExitThisFlow("S999","Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        
        return AfaFlowControl.ExitThisFlow("S999","更新原查询业务信息异常")
        
    if not AfaDBFunc.CommitSql():
        AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    AfaLoggerFunc.tradeInfo(">>>结束更新原查询业务信息")
    
    #======为通讯回执报文赋值===================================================
    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '成功'
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    return True 
#=====================交易后处理================================================
def SubModuleDoSnd():
    
    return True 
