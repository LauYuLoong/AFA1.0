# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).头寸预警报文接收
#===============================================================================
#   模板文件:   TRCC006.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-24
#   功    能：  头寸不足
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
import rccpsDBTrcc_cshalm,rccpsMap0000Dout_context2CTradeContext,rccpsGetFunc

from types import *
from rccpsConst import *

#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    #==========判断是否重复报文,如果是重复报文,直接进入下一流程================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    cshalm_where_dict = {}
    cshalm_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    cshalm_where_dict['TRCDAT']   = TradeContext.TRCDAT
    cshalm_where_dict['TRCNO']    = TradeContext.TRCNO

    cshalm_dict = rccpsDBTrcc_cshalm.selectu(cshalm_where_dict)

    if cshalm_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常")

    if len(cshalm_dict) > 0:
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

    #=====向字典赋值====
    cshalm = {}
    cshalm['BJEDTE']   =  TradeContext.BJEDTE       #交易日期
    cshalm['BSPSQN']   =  TradeContext.BSPSQN       #报单序号
    #cshalm['NCCWKDAT'] =  TradeContext.NCCworkDate  #中心日期
    #关彬捷 20080924 中心日期赋值报文中的中心日期
    cshalm['NCCWKDAT'] =  TradeContext.NCCWKDAT     #中心日期
    cshalm['TRCCO']    =  TradeContext.TRCCO        #交易代码
    cshalm['TRCDAT']   =  TradeContext.TRCDAT       #委托日期
    cshalm['TRCNO']    =  TradeContext.TRCNO        #交易流水号
    cshalm['SNDBNKCO'] =  TradeContext.SNDBNKCO     #发送行号
    cshalm['RCVBNKCO'] =  TradeContext.RCVBNKCO     #接收行号
    #=====币种转换====
    if TradeContext.CUR == 'CNY':
        cshalm['CUR']  =  '01'                      #币种
    cshalm['POSITION'] =  TradeContext.POSITION     #头寸当前金额
    cshalm['POSALAMT'] =  TradeContext.POSALAMT     #头寸预警金额

    #=====登记头寸预警登记簿====
    AfaLoggerFunc.tradeInfo('>>>开始登记头寸预警登记簿')
    AfaLoggerFunc.tradeInfo('>>>字典：' + str(cshalm))
    ret = rccpsDBTrcc_cshalm.insertCmt(cshalm)
    if ret <= 0:
        #=====发送回执字典赋值====
        TradeContext.PRCCO    = 'RCCS1105'
        TradeContext.STRINFO  = '其它错误'
    else:
        TradeContext.PRCCO    = 'RCCI0000'
        TradeContext.STRINFO  = '成功'
 
    #=====发送通存回执====
    TradeContext.sysType  = 'rccpst'
    TradeContext.ORTRCCO  = TradeContext.TRCCO
    TradeContext.TRCCO    = '9900503'
    TradeContext.MSGTYPCO = 'SET008'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.ORMFN    = TradeContext.MSGFLGNO
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ROPRTPNO = TradeContext.OPRTYPNO
    TradeContext.OPRTYPNO = '99'
    TradeContext.TRANTYP  = '0'

    #=====通过接收行号取行名和成员行号====
    rccpsGetFunc.GetRcvBnkCo(TradeContext.RCVBNKCO)
    
    #=====通过发送行号取行名和成员行号====
    rccpsGetFunc.GetSndBnkCo(TradeContext.SNDBNKCO)

    TradeContext.tmp      = TradeContext.SNDSTLBIN
    TradeContext.SNDSTLBIN= TradeContext.RCVSTLBIN
    TradeContext.RCVSTLBIN= TradeContext.tmp

    return True
#=====================交易后处理================================================
def SubModuleDoSnd():
    #=====判断afe返回====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True

