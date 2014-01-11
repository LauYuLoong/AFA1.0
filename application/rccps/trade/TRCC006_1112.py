# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作模板(1.本地操作 2.中心回执).汇总核对报文接收
#===============================================================================
#   交易文件:   TRCC006_1112.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-07-07
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_atrchk,rccpsMap1112CTradeContext2Datrchk_dict
import rccpsMap0000Dout_context2CTradeContext


#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('>>>进入汇总核对报文接收')
    #=====判断是否重复交易====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_atrchk.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','判断是否重复报文，查询汇总核对报文登记簿相同报文异常')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('汇兑业务登记簿中存在相同数据,重复报文,进入下一流程')
        #=====为通讯回执报文赋值====
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
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '重复报文'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        #=====发送afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','重复报文，退出处理流程')

    AfaLoggerFunc.tradeInfo(">>>结束判断是否重复报文")

    #=====赋值开始登记登记簿====
    atrchk_dict = { }
    if not rccpsMap1112CTradeContext2Datrchk_dict.map(atrchk_dict):
        return AfaFlowControl.ExitThisFlow('S999','字典赋值出错')

    if TradeContext.existVariable('CUR') and TradeContext.CUR == 'CNY':
        sel_dict['CUR'] = '01'
        
    #=====插入登记簿====
    record = rccpsDBTrcc_atrchk.insert(sel_dict)
    if record <= 0:
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow("S999","登记汇兑核对报文登记簿异常")

    AfaDBFunc.CommitSql()

    #=====为通讯回执报文赋值====
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
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
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

    #=====判断中心返回====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True
