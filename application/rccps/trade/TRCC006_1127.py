# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).特约汇兑查询接收
#===============================================================================
#   模板文件:   TRCC006.py
#   修改时间:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_hdcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1127CTradeContext2Dhdcbka_dict
import rccpsDBFunc,rccpsGetFunc

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
        AfaLoggerFunc.tradeInfo("汇兑查询查复自由格式登记簿中存在相同查询交易,此报文为重复报文,直接进入下一流程,发送表示成功的通讯回执")
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
    
    #关彬捷 20080725 增加查询原交易信息 若未找到原交易信息则返回通讯回执
    #=========查询原特约汇兑交易信息===========================================
    AfaLoggerFunc.tradeInfo(">>>开始查询原交易信息")
    
    tran_dict = {}
    if not rccpsDBFunc.getTransTrcPK(TradeContext.RCVMBRCO,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
        AfaLoggerFunc.tradeInfo("汇兑业务登记簿中不存在此查询书所查询的特约汇兑交易,直接进入下一流程,发送表示成功的通讯回执")
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
        out_context_dict['STRINFO']  = '不存在此查询书所查询的特约汇兑业务'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>结束查询原交易信息")
    
    
    #==========为汇兑查询查复自由格式登记簿字典赋值================================
    AfaLoggerFunc.tradeInfo(">>>开始为汇兑查询查复自由格式登记簿字典赋值")
    
    TradeContext.ISDEAL = PL_ISDEAL_UNDO
    TradeContext.ORTRCCO  = tran_dict['TRCCO']
    TradeContext.BOJEDT = tran_dict['BJEDTE']
    TradeContext.BOSPSQ = tran_dict['BSPSQN']
    
    #=====张恒 20091010 新增 将机构落到原交易机构 ====
    TradeContext.BESBNO = tran_dict['BESBNO']          #接收机构号 
    
    #关彬捷 20070725 修改币种,金额,发送行名,接收行名
    #TradeContext.CUR    = tran_dict['CUR']
    #TradeContext.OCCAMT = str(tran_dict['OCCAMT'])
    #TradeContext.PYRACC = tran_dict['PYRACC']
    #TradeContext.PYEACC = tran_dict['PYEACC']
    #TradeContext.SNDBNKNM = tran_dict['RCVBNKNM']
    #TradeContext.RCVBNKNM = tran_dict['SNDBNKNM']
    
    if TradeContext.ORCUR == 'CNY':
        TradeContext.CUR  =   '01'                     #原币种
    else:
        TradeContext.CUR  =   TradeContext.ORCUR       #原币种

    TradeContext.OCCAMT   =   TradeContext.OROCCAMT    #原金额
    
    rccpsGetFunc.GetSndBnkCo(TradeContext.SNDBNKCO)
    rccpsGetFunc.GetRcvBnkCo(TradeContext.RCVBNKCO)
    
    hdcbka_insert_dict = {}
    if not rccpsMap1127CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","为汇兑查询查复自由格式登记簿字典赋值异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束为汇兑查询查复自由格式登记簿字典赋值")
    #==========登记汇兑查询查复自由格式登记簿======================================
    AfaLoggerFunc.tradeInfo(">>>开始登记汇兑查询查复自由格式登记簿")
    
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","登记汇兑查询查复自由格式登记簿异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇兑查询查复自由格式登记簿")
    
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
