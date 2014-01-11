# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8473.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #从表标志

    AfaLoggerFunc.tradeInfo( "********************中台勾兑查找开始***************" )

    #考虑缴款书编号是空的时候
    if not TradeContext.AFC001 :
        TradeContext.errorCode,TradeContext.errorMsg        =   "0002","缴款书编号为空"
        return False

    sqlstr          =   "select AFC401,AFC015 from fs_fc74 where AFC001 like '%" + TradeContext.AFC001 + "%' and afc016='" +TradeContext.brno + "' and busino='" + TradeContext.busiNo + "' and flag!='*'"

    #===条件增加银行编码字段,张恒修改===
    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "没有查到勾对信息"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
    else:
        recCnt                  =   len(records)            #记录条数
        TradeContext.RECCNT     =   str ( recCnt )

        TradeContext.AFC015     =   records[0][1]

        value                   =   []
        for i in range(recCnt):
            value.append(records[i][0])

        AfaLoggerFunc.tradeInfo( value )
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( TradeContext.AFC015 )
        TradeContext.serialNo   =   ":".join(value)
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "勾兑查找成功"

    AfaLoggerFunc.tradeInfo( "********************中台勾兑查找结束***************" )
    return True
