# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).票据查询接收
#===============================================================================
#   模板文件:   TRCC006.py
#   修改时间:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_pjcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1125CTradeContext2Dpjcbka_dict,rccpsDBFunc

#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
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
        AfaLoggerFunc.tradeInfo("票据查询查复登记簿中存在相同查询交易,此报文为重复报文,直接进入下一流程,发送表示成功的通讯回执")
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
        out_context_dict['STRINFO']  = '重复报文'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>结束检查是否重复报文")
    
    #==========为票据查询查复登记簿字典赋值================================
    AfaLoggerFunc.tradeInfo(">>>开始为票据查询查复登记簿字典赋值")
    
    TradeContext.ISDEAL = PL_ISDEAL_UNDO
    
    pjcbka_insert_dict = {}
    if not rccpsMap1125CTradeContext2Dpjcbka_dict.map(pjcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","为票据查询查复登记簿字典赋值异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束为票据查询查复登记簿字典赋值")
    
    #==========登记票据查询查复登记簿======================================
    AfaLoggerFunc.tradeInfo(">>>开始登记票据查询查复登记簿")
    AfaLoggerFunc.tradeInfo(">>>" + str(TradeContext.SNDBNKNM))
    
    ret = rccpsDBTrcc_pjcbka.insertCmt(pjcbka_insert_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","登记票据查询查复登记簿异常") 
    
    AfaLoggerFunc.tradeInfo(">>>结束登记票据查询查复登记簿")
    
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
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow("S999","发送通讯回执报文异常")
        
    return True
