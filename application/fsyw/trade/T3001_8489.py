# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8472.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):
    
    AfaLoggerFunc.tradeInfo( '********************查找数据表结束*******************' )
    TradeContext.__agentEigen__  = '0'   #从表标志
    
    sqlstr      =   "select busino,hostip,upuser,uppasswd,upldir,downuser,downpasswd,downldir from fs_businoconf where busino='" + TradeContext.busiNo + "'"
    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )   
    if records == None:
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "操作数据库异常"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
        
    if( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "未找到相应记录"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
    else:    
        TradeContext.APPNO      =   'AG2008'
        TradeContext.BUSINO     =   records[0][0]
        TradeContext.HOSTIP     =   records[0][1]
        TradeContext.RDOWNPATH  =   records[0][7]
        TradeContext.RUPPATH    =   records[0][4]
        TradeContext.DOWNUSER   =   records[0][5]
        TradeContext.DOWNPWD    =   records[0][6]
        TradeContext.UPUSER     =   records[0][2]
        TradeContext.UPPD       =   records[0][3]
    
    sqlstr      =   "select date,this from fs_remain where busino='" + TradeContext.busiNo + "'"
    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )   
    if records == None:
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "操作数据库异常"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
        
    if( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "未找到相应记录"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
    else:    
        AfaLoggerFunc.tradeInfo(records[0][1])
        TradeContext.THIS        =   records[0][1]
        AfaLoggerFunc.tradeInfo(records[0][0])
        TradeContext.ACCDATE     =   records[0][0]
        
    AfaLoggerFunc.tradeInfo( '********************查找数据表结束*******************' )
    TradeContext.errorCode,TradeContext.errorMsg        =   "0000","查找非税数据成功"
    return True
        
