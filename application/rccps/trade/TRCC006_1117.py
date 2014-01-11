# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).清算账户余额通知接收
#===============================================================================
#   模板文件:   TRCC006_1117.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-24
#   功    能：  清算账户余额通知接收
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
import rccpsDBTrcc_rekbal,rccpsMap0000Dout_context2CTradeContext

from types import *
from rccpsConst import *

#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('>>>进入清算账户余额通知报文接收')
    #=====判断是否重复交易====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_rekbal.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','判断是否重复报文，查询清算账户余额通知登记簿相同报文异常')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('清算账户余额登记簿中存在相同数据,重复报文,进入下一流程')
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

        return True 
    AfaLoggerFunc.tradeInfo(">>>结束判断是否重复报文")

    #=====向字典赋值====
    rekbal = {}
    rekbal['BJEDTE']   =  TradeContext.BJEDTE       #交易日期
    rekbal['BSPSQN']   =  TradeContext.BSPSQN       #报单序号
    #rekbal['NCCWKDAT'] =  TradeContext.NCCworkDate  #中心日期
    #关彬捷 20080924 中心日期赋值报文中的中心日期
    rekbal['NCCWKDAT'] =  TradeContext.NCCWKDAT     #中心日期
    rekbal['TRCCO']    =  TradeContext.TRCCO        #交易代码
    rekbal['TRCDAT']   =  TradeContext.TRCDAT       #委托日期
    rekbal['TRCNO']    =  TradeContext.TRCNO        #交易流水号
    rekbal['SNDBNKCO'] =  TradeContext.SNDBNKCO     #发送行号
    rekbal['RCVBNKCO'] =  TradeContext.RCVBNKCO     #接收行号
    #=====币种转换====
    if TradeContext.CUR == 'CNY':
        rekbal['CUR']  =  '01'                      #币种
    rekbal['LBDCFLG']  =  TradeContext.LBDCFLG      #上日余额借贷标志
    rekbal['LSTDTBAL'] =  TradeContext.LSTDTBAL     #上日余额
    rekbal['NTTDCFLG'] =  TradeContext.NTTDCFLG     #本日扎查额借贷标志
    rekbal['NTTBAL']   =  TradeContext.NTTBAL       #本日扎查额
    rekbal['BALDCFLG'] =  TradeContext.BALDCFLG     #本日余额借贷标志
    rekbal['TODAYBAL'] =  TradeContext.TODAYBAL     #本日余额
    rekbal['AVLBAL']   =  TradeContext.AVLBAL       #可用余额
    rekbal['BRSFLG']   =  PL_BRSFLG_RCV
    rekbal['SNDMBRCO'] =  TradeContext.SNDMBRCO     #发起成员行号
    rekbal['RCVMBRCO'] =  TradeContext.RCVMBRCO     #接收成员行号

    #=====登记清算账户余额通知登记簿====
    out_context_dict = {}
    AfaLoggerFunc.tradeInfo('>>>开始登记清算账户余额通知登记簿')
    ret = rccpsDBTrcc_rekbal.insertCmt(rekbal)
    if ret <= 0:
        #=====发送回执字典赋值====
        out_context_dict['PRCCO']    = 'RCCS1105'
        out_context_dict['STRINFO']  = '其它错误'
    else:
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '成功'
 
    #=====发送通存回执====
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
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo

    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    return True
#=====================交易后处理================================================
def SubModuleDoSnd():
    #=====判断afe返回====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True

