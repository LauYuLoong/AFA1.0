# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).特约汇兑查复接收
#===============================================================================
#   模板文件:   TRCC006.py
#   修改时间:   2008-06-11
################################################################################
#   修改者  :   刘雨龙
#   修改时间:   2008-07-21
#   功    能:   修改本交易流程
################################################################################
#   修改者  :   关彬捷
#   修改时间:   2008-07-26
#   功    能:   修改登记登记簿数据
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1128CTradeContext2Dhdcbka_dict

#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    #==========判断是否重复报文,如果是重复报文,直接进入下一流程================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    hdcbka_where_dict = {}
    hdcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    hdcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    hdcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    #hdcbka_where_dict['TRCDAT']   = TradeContext.ORQYDAT
    #hdcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    
    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常")
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
        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #发起成员行号
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>结束检查是否重复报文")
    
    #==========判断是否存在原查询交易===========================================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否存在原查询交易")
    hdcbka_where_dict = {}
    hdcbka_where_dict['SNDBNKCO'] = TradeContext.RCVBNKCO
    hdcbka_where_dict['TRCDAT']   = TradeContext.OQTDAT
    hdcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    #or_hdcbka_where_dict['TRCNO']    = TradeContext.ORTRCNO
    #or_hdcbka_where_dict['TRCDAT']   = TradeContext.ORTRCDAT
    
    or_hdcbka_dict = {}
    or_hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    
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
        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #发起成员行号
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>结束检查是否存在原查询交易")
    
    #==========为汇兑查询查复自由格式登记簿字典赋值================================
    AfaLoggerFunc.tradeInfo(">>>开始为汇兑查询查复自由格式登记簿字典赋值")
    
    TradeContext.BOJEDT  = or_hdcbka_dict['BJEDTE']
    TradeContext.BOSPSQ  = or_hdcbka_dict['BSPSQN']
    #TradeContext.CUR     = or_hdcbka_dict['CUR']
    #TradeContext.OCCAMT  = str(or_hdcbka_dict['OCCAMT'])
    TradeContext.ORTRCCO = or_hdcbka_dict['TRCCO']
    #=========关彬捷 修改 币种,金额,付款人账号,收款人账号,发送行名,接收行名
    #TradeContext.PYRACC  = or_hdcbka_dict['PYRACC']
    #TradeContext.PYEACC  = or_hdcbka_dict['PYEACC'] 
    TradeContext.ISDEAL  = PL_ISDEAL_ISDO
    
    if TradeContext.ORCUR == 'CNY':
        TradeContext.CUR  =   '01'                     #原币种
    else:
        TradeContext.CUR  =   TradeContext.ORCUR       #原币种

    TradeContext.OCCAMT   =   TradeContext.OROCCAMT    #原金额
    
    #=====张恒 20091010 新增 将机构落到原交易机构 ====
    TradeContext.BESBNO = or_hdcbka_dict['BESBNO']     #接收机构号
    
    rccpsGetFunc.GetSndBnkCo(TradeContext.SNDBNKCO)
    rccpsGetFunc.GetRcvBnkCo(TradeContext.RCVBNKCO)
    
    hdcbka_insert_dict = {}
    if not rccpsMap1128CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","为汇兑查询查复自由格式登记簿字典赋值异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束为汇兑查询查复自由格式登记簿字典赋值")
    #==========登记会对查询查复自由格式登记簿=======================================
    AfaLoggerFunc.tradeInfo(">>>开始登记此查复业务")
    
    ret = rccpsDBTrcc_hdcbka.insert(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","登记汇兑查询查复自由格式登记簿异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束登记此查复业务")
    
    #======更新原查询交易信息===================================================
    AfaLoggerFunc.tradeInfo(">>>开始更新原查询业务信息")
    
    or_hdcbka_update_dict = {}
    or_hdcbka_update_dict['ISDEAL']   = PL_ISDEAL_ISDO
    
    
    orhdcbka_where_dict = {}
    orhdcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    orhdcbka_where_dict['TRCDAT']   = TradeContext.OQTDAT
    orhdcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    ret = rccpsDBTrcc_hdcbka.update(or_hdcbka_update_dict,orhdcbka_where_dict)
    if (ret <= 0):
        return AfaFlowControl.ExitThisFlow("S999","更新原查询业务信息异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束更新原查询业务信息")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
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
    TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #发起成员行号
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    return True 
    
#=====================交易后处理================================================
def SubModuleDoSnd():

    #=====判断afe返回结果
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True 
