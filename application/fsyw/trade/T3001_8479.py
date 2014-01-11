# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8479.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext
TradeContext.sysType = 'fsyw'
import AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #从表标志

    AfaLoggerFunc.tradeInfo( "单位编码信息查询开始" )

    #在中台数据库中查询
    sqlstr =   "select ACCNO,NAME,AAA010 ,AAA012,BANKNO,BANKNAME  from fs_businoinfo where busino='" + TradeContext.busiNo + "' and bankno = '" + TradeContext.bankbm  + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "9999"
        TradeContext.errorMsg   =   "查找单位编码信息异常"
        return False

    elif ( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "没有查找到单位编码信息"
        return False

    else:
        TradeContext.O1ACCN     =   records[0][0]           #收款人帐号
        TradeContext.O1NAME     =   records[0][1]           #收款人名字
        TradeContext.O1AAA010   =   records[0][2]           #财政区划内码
        TradeContext.O1AAA012   =   records[0][3]           #区划名称
        TradeContext.O1BANKNO   =   records[0][4]           #收款人开户行编码
        TradeContext.O1BANKNAME =   records[0][5]           #收款人开户行名称

    TradeContext.errorCode  =   "0000"
    TradeContext.errorMsg   =   "查找单位编码信息成功"
    AfaLoggerFunc.tradeInfo( "********************中台单位编码信息查询结束***************" )
    return True
