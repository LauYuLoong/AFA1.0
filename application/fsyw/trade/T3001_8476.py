# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8476.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):
    
    TradeContext.__agentEigen__  = '0'   #从表标志
    
    AfaLoggerFunc.tradeInfo( "***********中台查找编码名称开始**********" )
    
    #查询执收单位名称
    if TradeContext.unitNo :
        sql   =   "select aaa010 from fs_businoinfo where  busino='" + TradeContext.busiNo + "'"
        ret   =   AfaDBFunc.SelectSql(sql)
        if ret == None or len(ret) == 0:
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "没有查找到执收单位名称"
            return False

        #sqlstr  =   "select afa052 from fs_fa15 where afa051='" + TradeContext.unitNo + "'"    
        sqlstr  =   "select afa052 from fs_fa15 where afa051='" + TradeContext.unitNo + "'"
        sqlstr  = sqlstr + " and aaa010='" + ret[0][0] + "' order by aaz002 desc"
        
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "没有查找到执收单位名称"
            return False
        
        TradeContext.unitName       =   records[0][0]               #执收单位名称
    else:
        TradeContext.unitName       =   ''
    AfaLoggerFunc.tradeInfo( ">>>执收单位名称[" + TradeContext.unitName + "]")
    
    AfaLoggerFunc.tradeInfo( ">>>开始查询执收项目名称" )
    #查询执收项目名称
    if TradeContext.itemNo :
        sqlstr  =   "select afa032,afa030 from fs_fa13 where afa031='" + TradeContext.itemNo  + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"
        
        records = AfaDBFunc.SelectSql( sqlstr )
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( records )
        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "没有查找到执收项目名称"
            return False
        TradeContext.itemName       =   records[0][0]     #执收项目名称
    else:
        TradeContext.itemName       =   ''     
    AfaLoggerFunc.tradeInfo( ">>>执收项目名称[" + TradeContext.itemName + "]")
    
    AfaLoggerFunc.tradeInfo( ">>>开始查询代收银行名称" )
    
    #查询代收银行名称
    if TradeContext.bankNo :
        sqlstr  =   "select afa102 from fs_fa22 where afa101='" + TradeContext.bankNo + "'"
            
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "没有查找到代收银行名称"
            return False
            
        TradeContext.bankName       =   records[0][0]               #代收银行名称
    else:
        TradeContext.bankName       =   ''
     
    AfaLoggerFunc.tradeInfo( ">>>代收银行名称[" + TradeContext.bankName + "]")
          
    TradeContext.errorCode  =   "0000"
    TradeContext.errorMsg   =   "查找编码名称成功"