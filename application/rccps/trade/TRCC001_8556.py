# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印业务.行名行号联动
#=================================================================
#   程序文件:   TRCC001_8556.py
#   修改时间:   2008-06-05
##################################################################
import rccpsDBTrcc_paybnk,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易.行名行号联动[RCC001_8556]进入***' )
    
    #=====判断接口是否存在====
    if not TradeContext.existVariable("BANKBIN"):
        return AfaFlowControl.ExitThisFlow('S999','行号[BANKBIN]不存在')

    #=====按行号查询====
    sqldic={'BANKBIN':TradeContext.BANKBIN,'NOTE1':'1'}
        
    #=====查询数据库，得到查询结果集====
    records=rccpsDBTrcc_paybnk.selectu(sqldic)
    
    if records == None:
        return AfaFlowControl.ExitThisFlow('S999','查询行名行号数据库失败')
    if len(records) <= 0 :
        return AfaFlowControl.ExitThisFlow('S999','无此行号信息')
        
    TradeContext.BANKNAM = records['BANKNAM']       #行名
    TradeContext.errorMsg="查询成功"
    TradeContext.errorCode="0000"
    
    AfaLoggerFunc.tradeInfo( '***农信银系统: 往账.本地类操作交易.行名行号联动[RCC001_8556]退出***' )
    return True
