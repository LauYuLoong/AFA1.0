# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TYBT005_8617.py
#   程序说明:   单方撤销
#   修改时间:   2010-7-30
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaYbtdb
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    
    try:
        AfaLoggerFunc.tradeInfo( '---->查询原缴费记录' )
       
        sql = "select workdate,tellerno,brno,unitno,amount,note9,bankstatus ,userno from afa_maintransdtl"
        sql = sql + " where agentserialno = '" + TradeContext.preAgentSerno + "'"
        sql = sql + " and   workdate      = '" + TradeContext.workDate      + "'"
        
        AfaLoggerFunc.tradeInfo('---->查询原始缴费记录：'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records ==  None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询银保通数据库异常"
            AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
            raise False
        
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","没有找到原缴费交易，请检查录入项"
            return False
        else:
            #bankstatus 0:正常 1：失败 2：异常 3：已冲正
            if (records[0][6] != '0'):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原始缴费交易异常或已冲正，不能再做撤销交易"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
                
            if (records[0][0] !=TradeContext.workDate ):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","不是当日交易，不能做此交易"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
                
            if(records[0][1] != TradeContext.tellerno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本柜员所做，不能做此交易"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
            
            if(records[0][2] != TradeContext.brno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本网点所做，不能做此交易"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
            
            if(records[0][3] != TradeContext.unitno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易保险公司不符，不能做此交易"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
           
            if(records[0][4].strip() != TradeContext.amount.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易金额不符，不能做此交易"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
            
            if(records[0][5].split('|')[2] != TradeContext.policy):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易保险单号不符，不能做此交易"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
            
            TradeContext.userno = records[0][7]
            TradeContext.amount = records[0][4]
            
        AfaLoggerFunc.tradeInfo( '---->查询原始撤销记录是否成功，失败则进行单方撤销' )                                                             
        
        sql = "select bankstatus from afa_maintransdtl"
        sql = sql + " where preagentserno = '" + TradeContext.preAgentSerno + "'"
        sql = sql + " and   workdate      = '" + TradeContext.workDate      + "'"
        sql = sql + " and   revtranf      <> '0'"
        sql = sql + " and   trxcode in ('8615','8616')"
        
        AfaLoggerFunc.tradeInfo('---->查询原始撤销记录是否成功：'+ sql)
                                                                                                                              
        results = AfaDBFunc.SelectSql( sql )
                                                                                                                              
        if results == None:                                                                                                     
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询数据库异常" 
            AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
            return False
        elif(len(results) < 1):                                                                                                 
            TradeContext.errorCode,TradeContext.errorMsg = "0001","没有做过撤销交易，不能做单方撤销" 
            AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
            return False
        else:
            for result in results:
                #bankstatus 0:正常 1：失败 2：异常 3：已冲正 
                if ( result[0] == '0' ):
                    TradeContext.errorCode = "0001"
                    TradeContext.errorMsg  = "该交易已成功撤销，无需再撤销"
                    AfaLoggerFunc.tradeInfo ( '---->' + TradeContext.errorMsg )
                    return False
            AfaLoggerFunc.tradeInfo( '---->该交易撤销失败，可以做单方撤销' )
        return True

    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e)) 
