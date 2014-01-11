# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8475.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):
    TradeContext.__agentEigen__  = '0'   #从表标志

    AfaLoggerFunc.tradeInfo( "中台查找流水金额数据库开始" )

    #在中台数据库中查询
    sqlstr = "select afc011 from fs_fc74 where afc401='" + TradeContext.serNo + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and afc015='" + TradeContext.AFC015 + "'"

    #===条件增加银行编码字段,张恒修改===
    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        AfaLoggerFunc.tradeInfo( sqlstr )
        TradeContext.errorCode  =   "9999"
        TradeContext.errorMsg   =   "查找流水金额失败"
        return False

    elif ( len(records)==0 ):
        AfaLoggerFunc.tradeInfo( sqlstr )
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "没有查找到流水金额"
        return False

    else:
        TradeContext.totalAmt   =   records[0][0]

    TradeContext.errorCode  =   "0000"
    TradeContext.errorMsg   =   "查找流水金额成功"
    AfaLoggerFunc.tradeInfo( "********************中台查找流水金额数据库开始***************" )
    return True