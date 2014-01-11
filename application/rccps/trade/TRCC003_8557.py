# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作模板(1.本地操作 2.中心操作).清算账户余额回执发送
#===============================================================================
#   交易文件:   TRCC003_8557.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-07-25
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_rekbal,rccpsMap8557CTradeContext2Drekbal_dict

#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('>>>开始清算账户余额回执发送交易')

    #=====判断字段值是否存在====
    if not TradeContext.existVariable('CHKDAT'):
        return AfaFlowControl.ExitThisFlow('S999','对账日期不可为空')
    if not TradeContext.existVariable('OCCAMT'):
        return AfaFlowControl.ExitThisFlow('S999','本日余额不可为空')
    if not TradeContext.existVariable('CHKRST'):
        return AfaFlowControl.ExitThisFlow('S999','对账结果不可为空')

    #=====进入查询rekbal====
    rek_sel = {}
    rek_sel['NCCWKDAT']  =  TradeContext.CHKDAT
    rek_sel['BRSFLG']    =  PL_BRSFLG_RCV

    record = rccpsDBTrcc_rekbal.selectu(rek_sel)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','查询清算账户余额通知登记簿异常')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','查询清算账户余额通知登记簿无记录')
    else:
        TradeContext.BOJEDT  =  record['BJEDTE']
        TradeContext.BOSPSQ  =  record['BSPSQN']
        TradeContext.TODAYBAL=  record['TODAYBAL']
        TradeContext.LSTDTBAL=  record['LSTDTBAL']
        TradeContext.LBDCFLG =  record['LBDCFLG']
        TradeContext.NTTDCFLG=  record['NTTDCFLG']
        TradeContext.NTTBAL  =  record['NTTBAL']
        TradeContext.BALDCFLG=  record['BALDCFLG']
        TradeContext.AVLBAL  =  record['AVLBAL']
        

    #=====TradeContext向字典赋值====
    TradeContext.NTODAYBAL   =  TradeContext.OCCAMT
    TradeContext.SNDMBRCO    =  record['RCVMBRCO']
    TradeContext.RCVMBRCO    =  record['SNDMBRCO']

    rekbal_dict = {}
    if not rccpsMap8557CTradeContext2Drekbal_dict.map(rekbal_dict):
        return AfaFlowControl.ExitThisFlow('S999','字典赋值错误')
    
    ret = rccpsDBTrcc_rekbal.insertCmt(rekbal_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999','登记清算账户余额通知登记簿异常')

    #=====赋值发送农信银中心====
    TradeContext.ORTRCDAT  =  record['TRCDAT']
    TradeContext.ORTRCNO   =  record['TRCNO']
    TradeContext.TODAYBAL  =  TradeContext.OCCAMT
    TradeContext.OPRTYPNO  =  '99'
    TradeContext.ROPRTPNO  =  '99'
    TradeContext.ORMFN     =  record['SNDMBRCO'] + TradeContext.ORTRCDAT + TradeContext.ORTRCNO 
    
    return True
#=====================交易后处理================================================
def SubModuleDoSnd():

    #====判断afe返回====
    if TradeContext.errorCode == '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '成功'
    return True
    
