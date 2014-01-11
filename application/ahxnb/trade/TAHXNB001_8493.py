###############################################################################
# -*- coding: gbk -*-
# 摘    要：新农保批量业务状态查询
# 当前版本：1.0
# 作    者：曾照泰
# 完成日期：2010年12月16日
###############################################################################
import AfaDBFunc,AfaLoggerFunc,TradeContext
#import os,AfaUtilTools, sys,AhXnbFunc,ConfigParser,  
from types import *

#=====================安徽省新农保批量状态查询==============================================
def TrxMain( ):
    
    try:
        AfaLoggerFunc.tradeInfo('---------安徽省批量状态查询进入------------')
       
        #业务编号
        if not( TradeContext.existVariable( "I1APPNO" ) and len(TradeContext.I1APPNO.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在业务编号"
            raise AfaFlowControl.flowException( )
       
        #单位编号
        if not( TradeContext.existVariable( "I1BUSINO" ) and len(TradeContext.I1BUSINO.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在单位编号"
            raise AfaFlowControl.flowException( )   
       
        #申请日期
        if not( TradeContext.existVariable( "I1WORKDATE" ) and len(TradeContext.I1WORKDATE.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在申请日期"
            raise AfaFlowControl.flowException( )   
         
        
        #批次号
        if not( TradeContext.existVariable( "I1BATCHNO" ) and len(TradeContext.I1BATCHNO.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在批次号"
            raise AfaFlowControl.flowException( )
            
        sql = ''
        sql = "select procmsg from ahnx_file"
        sql = sql + " where workdate = '"+ TradeContext.I1WORKDATE + "' "  
        sql = sql + " and   batchno  = '"+ TradeContext.I1BATCHNO  + "' "   
        if TradeContext.I1APPNO != "NBKH":
            sql = sql + " and appno  = '"+ TradeContext.I1APPNO    +"' "  
            sql = sql + " and busino = '"+ TradeContext.I1BUSINO   + "' " 
        
        
        AfaLoggerFunc.tradeInfo('>>>>>>>开始查询原交易：'+ str(sql))
        records = AfaDBFunc.SelectSql( sql ) 
                  
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询AHNX_FILE表失败"
            AfaLoggerFunc.tradeInfo('>>>>>>>：'+ TradeContext.errorMsg)
            return False
            
        if(len(records) == 0):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此信息"
            AfaLoggerFunc.tradeInfo('>>>>>>>：'+ TradeContext.errorMsg)
            return False   
        
        else:
            TradeContext.O1DESCRIBE = records[0][0]
            TradeContext.errorCode='0000'
        AfaLoggerFunc.tradeInfo('---------安徽省批量状态查询退出------------')
        return True
    
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return False
  
