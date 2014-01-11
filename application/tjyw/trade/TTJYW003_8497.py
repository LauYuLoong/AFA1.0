# -*- coding: gbk -*-
##################################################################

#   中间业务平台.
#=================================================================
#   程序文件:   TTJYW003_8497.py
#   程序说明:   [汇总查询]
#   修改时间:   2011-01-05
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    try:
        AfaLoggerFunc.tradeInfo('>>>>>>>>>>>>前一天数据汇总查询语句开始') 
        sql = "select sum(cast(amount as decimal(15,2))),count(*) from afa_maintransdtl"
        sql = sql + " where  workdate    = '" + TradeContext.workdate.strip()  + "'"
        sql = sql + " and    bankstatus  = '0'  and revtranf = '0' and chkflag = '0'"
        sql = sql + " and    sysid       = '" + TradeContext.sysId.strip()     +"'"
        sql = sql + " and    unitno      = '" + TradeContext.unitno.strip()    + "'"
        
        #20120709陈浩添加 note2 ---busino单位编码
        sql = sql + " and    note2       = '" + TradeContext.busino            +"'"     #单位编号
        
        AfaLoggerFunc.tradeInfo('汇总信息查询语句'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询数据库失败"
            raise AfaFlowControl.flowException( )
        
        if records[0][1] == 0:
            TradeContext.errorCode,TradeContext.errorMsg = "0001","没有查询到汇总记录信息"
            raise AfaFlowControl.flowException( )
        
        else:
            TradeContext.totalamt = str(records[0][0])             #总金额
            TradeContext.totalnum = str(records[0][1])             #总笔数 

     #20120706 陈浩修改注释，添加
     #begin
     #   sql = "select accno1 from afa_unitadm"
     #   sql = sql + " where sysid     = '" + TradeContext.sysId.strip() + "'"           
     #   sql = sql + " and   unitno    = '" + TradeContext.unitno.strip() + "'"          
     #                                                                                   
     #   AfaLoggerFunc.tradeInfo('收款人账号信息查询语句'+ sql)                          
     #                                                                                   
     #   records = AfaDBFunc.SelectSql( sql )                                            
     #                                                                                   
     #   if records == None:                                                             
     #       TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询数据库失败"     
     #       raise AfaFlowControl.flowException( )                                       
     #                                                                                   
     #   if(len(records) < 1):                                                             
     #       TradeContext.errorCode,TradeContext.errorMsg = "0001","无此信息"              
     #       raise AfaFlowControl.flowException( )                                                                 
     #                                                                                     
     #   else:                                                                             
     #       TradeContext.accno = records[0][0]             #收款人   
            
            
        sql = ""
        sql = sql + " select accno from abdt_unitinfo "
        sql = sql + " where appno = '" + TradeContext.sysId.strip()  + "' "
        sql = sql + " and  busino = '" + TradeContext.busino.strip() + "' "
        
        AfaLoggerFunc.tradeInfo('查询语句 ： '+ sql)                          
                                                                                    
        record = AfaDBFunc.SelectSql( sql )                                        
        if record == None:                                                         
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询数据库失败" 
            raise AfaFlowControl.flowException( )                                   
                                                                                    
        if(len(record) < 1):                                                       
            TradeContext.errorCode,TradeContext.errorMsg = "0001","该单位没有签约，不能做次业务！"        
            raise AfaFlowControl.flowException( )                                                             
                                                                                    
        else:                                                                       
            TradeContext.accno       = record[0][0]             #收款人帐户 
            
            #AfaLoggerFunc.tradeInfo('收款人帐户accno：'+ TradeContext.accno) 
        
     #end    
            
            
                              
        AfaLoggerFunc.tradeInfo('>>>>>>>>>>>>>>>前一天数据汇总查询语句结束') 
        return True 
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
    
    
     