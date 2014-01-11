# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).业务状态查复报文接收
#===============================================================================
#   模板文件:   TRCC006.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_ztcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1108CTradeContext2Dztcbka

#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).业务状态查复报文接收[RCC00R6_1108]进入***' )
    
    #==========判断是否重复报文,如果是重复报文,直接进入下一流程=================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    ztcbka_where_dict = {}
    ztcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    ztcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    ztcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    ztcbka_dict = rccpsDBTrcc_ztcbka.selectu(ztcbka_where_dict)
    
    if ztcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文失败")
    
    if len(ztcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("业务状态登记簿中存在相同查复交易,此报文为重复报文,进入下一流程,发送表示成功的通讯回执")
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
    or_ztcbka_where_dict = {}
    or_ztcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    or_ztcbka_where_dict['TRCDAT']   = TradeContext.OQTDAT
    or_ztcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    or_ztcbka_dict = {}
    or_ztcbka_dict = rccpsDBTrcc_ztcbka.selectu(or_ztcbka_where_dict)
    
    if or_ztcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验原查询交易失败") 
    
    if len(or_ztcbka_dict) <= 0:
        AfaLoggerFunc.tradeInfo("业务状态登记簿中不存在原查询交易,进入下一流程,发送表示成功的通讯回执")
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
        
    
    #==========为业务状态查复查复登记簿字典赋值=================================
    AfaLoggerFunc.tradeInfo(">>>开始为此业务状态登记簿字典赋值")
    
    if or_ztcbka_dict.has_key('BJEDTE'):
        TradeContext.BOJEDT = or_ztcbka_dict['BJEDTE']
    
    if or_ztcbka_dict.has_key('BSPSQN'):
        TradeContext.BOSPSQ = or_ztcbka_dict['BSPSQN']
    
    if TradeContext.existVariable('TRCCO'):
        TradeContext.ORTRCCO = TradeContext.TRCCO
        
    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    
    ztcbka_insert_dict = {}
    if not rccpsMap1108CTradeContext2Dztcbka.map(ztcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","为查复业务字典赋值异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束为此业务状态登记簿字典赋值")
    #==========登记业务状态查复查复登记簿=======================================
    AfaLoggerFunc.tradeInfo(">>>开始登记此查复业务")
    
    ret = rccpsDBTrcc_ztcbka.insert(ztcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","登记状态查复登记簿异常") 
    
    AfaLoggerFunc.tradeInfo(">>>结束登记此查复业务")
    
    #======更新原查询交易信息===================================================
    AfaLoggerFunc.tradeInfo(">>>开始更新原查询业务信息")
    
    or_ztcbka_update_dict = {}
    or_ztcbka_update_dict['NCCTRCST'] = TradeContext.NCCTRCST
    or_ztcbka_update_dict['MBRTRCST'] = TradeContext.MBRTRCST
    or_ztcbka_update_dict['ISDEAL']   = PL_ISDEAL_ISDO
    
    ret = rccpsDBTrcc_ztcbka.update(or_ztcbka_update_dict,or_ztcbka_where_dict)
    if (ret <= 0):
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
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).业务状态查复报文接收[RCC00R6_1108]退出***' )
    
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).业务状态查复报文接收[RCC00R6_1108]进入***' )
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).业务状态查复报文接收[RCC00R6_1108]退出***' )
    return True
        
