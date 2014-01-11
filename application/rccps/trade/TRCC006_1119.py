# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).查复书接收
#===============================================================================
#   模板文件:   TRCC006.py
#   修改时间:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_hdcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1119CTradeContext2Dhdcbka_dict

#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    #==========判断是否重复报文,如果是重复报文,直接进入下一流程================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    hdcbka_where_dict = {}
    hdcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    hdcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    hdcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    
    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常")
        
        return True
    
    if len(hdcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("汇兑查询查复自由格式登记簿中存在相同查复交易,此报文为重复报文,进入下一流程,发送表示成功的通讯回执")
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
    or_hdcbka_where_dict = {}
    or_hdcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    or_hdcbka_where_dict['TRCDAT']   = TradeContext.ORQYDAT
    or_hdcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    AfaLoggerFunc.tradeInfo(">>>" + str(or_hdcbka_where_dict))
    
    or_hdcbka_dict = {}
    or_hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(or_hdcbka_where_dict)
    
    if or_hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验原查询交易失败") 
    
    if len(or_hdcbka_dict) <= 0:
        AfaLoggerFunc.tradeInfo("汇兑查询查复自由格式登记簿中不存在原查询交易,进入下一流程,发送表示成功的通讯回执")
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
        out_context_dict['STRINFO']  = '汇兑查询查复自由格式登记簿中不存在原查询交易'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>结束检查是否存在原查询交易")
    
    #==========为汇兑查询查复自由格式登记簿字典赋值================================
    AfaLoggerFunc.tradeInfo(">>>开始为汇兑查询查复自由格式登记簿字典赋值")
    
    TradeContext.BRSFLG = '1'
    
    if or_hdcbka_dict.has_key('BJEDTE'):
        TradeContext.BOJEDT = or_hdcbka_dict['BJEDTE']
    
    if or_hdcbka_dict.has_key('BSPSQN'):
        TradeContext.BOSPSQ = or_hdcbka_dict['BSPSQN']
    
    if TradeContext.existVariable('TRCCO'):
        TradeContext.ORTRCCO = TradeContext.TRCCO
        
    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    
    #=====张恒 20091010 新增 将机构落到原交易机构 ====
    if or_hdcbka_dict.has_key('BSPSQN'):
        TradeContext.BESBNO = or_hdcbka_dict['BESBNO']     #接收机构号
        
    hdcbka_insert_dict = {}
    if not rccpsMap1119CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","为汇兑查询查复自由格式登记簿字典赋值异常")

    #=====刘雨龙 20080710 ====
    #=====币种转换====
    if TradeContext.ORCUR == 'CNY':
        hdcbka_insert_dict['CUR'] = '01'
    else:
        hdcbka_insert_dict['CUR']    = TradeContext.ORCUR
    hdcbka_insert_dict['OCCAMT'] = TradeContext.OROCCAMT
        
    AfaLoggerFunc.tradeInfo(">>>结束为汇兑查询查复自由格式登记簿字典赋值")
    #==========登记会对查询查复自由格式登记簿=======================================
    AfaLoggerFunc.tradeInfo(">>>开始登记此查复业务")
    
    ret = rccpsDBTrcc_hdcbka.insert(hdcbka_insert_dict)
    
    if ret <= 0:
        if not AfaDBFunc.RollbackSql():
            AfaFlowControl.ExitThisFlow("S999","Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        
        return AfaFlowControl.ExitThisFlow("S999","登记汇兑查询查复自由格式登记簿异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束登记此查复业务")
    #======更新原查询交易信息===================================================
    AfaLoggerFunc.tradeInfo(">>>开始更新原查询业务信息")
    
    or_hdcbka_update_dict = {}
    or_hdcbka_update_dict['ISDEAL']   = PL_ISDEAL_ISDO
    
    ret = rccpsDBTrcc_hdcbka.update(or_hdcbka_update_dict,or_hdcbka_where_dict)
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
