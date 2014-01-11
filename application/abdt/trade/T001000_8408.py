# -*- coding: gbk -*-
################################################################################
#   批量业务系统：批量明细维护
#===============================================================================
#   交易文件:   T001000_8408.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AfaFunc,AbdtFunc
from types import *


#=====================批量明细维护==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********批量明细维护(8408)开始**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间


    #判断单位协议是否有效
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    AfaLoggerFunc.tradeInfo('**********批量明细维护(8408)结束**********')


    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True
