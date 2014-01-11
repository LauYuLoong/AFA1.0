# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作模板(1.本地操作).清算账户余额查询交易
#===============================================================================
#   交易文件:   TRCC001_8558.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-07-25
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_rekbal

#=====================个性化处理(本地操作)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8558]进入***' )
    
    #=====判断对账日期是否存在====
    if not TradeContext.existVariable('CHKDAT'):
       return AfaFlowControl.ExitThisFlow('S999','对账日期[CHKDAT]不存在')

    #=====进入查询rekbal====
    rek_sel = {}
    rek_sel['NCCWKDAT']  =  TradeContext.CHKDAT

    record = rccpsDBTrcc_rekbal.selectu(rek_sel)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','查询清算账户余额通知登记簿异常')
    elif len(record) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','查询清算账户余额通知登记簿无记录')
    else:
        TradeContext.CHKRST = record['CHKRST']              #对账结果
        TradeContext.OCCAMT = str(record['TODAYBAL'])       #行内余额

    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '成功'
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8558]退出***' )
    return True
