# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TTJYW002_8496.py
#   程序说明:   当日撤销
#   修改时间:   2011-01-05
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaAfeFunc,AfaFlowControl
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    
    AfaLoggerFunc.tradeInfo( '反交易数据预查询，查询是否有此缴费记录' )
    try:
        sql = "select workdate,worktime,userno,tellerno,brno,unitno,amount,trxcode from afa_maintransdtl"
        sql = sql + " where agentserialno = '"+TradeContext.preAgentSerno+"' and workdate = '"+TradeContext.workDate+"' and trxcode='8495'"
        sql = sql + " and revtranf = '0' and bankstatus = '0'and chkflag = '9'"
        
        #20120718陈浩添加
        sql = sql + " and  sysid = '" + TradeContext.sysId.strip()   + "' "
        sql = sql + " and  note2 = '" + TradeContext.busino.strip()  + "' "
        
        
        AfaLoggerFunc.tradeInfo('反交易查询语句：'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        AfaLoggerFunc.tradeInfo('反交易查询的结果：'+ str(records))
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001","反交易查询数据失败"
            raise AfaFlowControl.flowException( )
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此交易"
            return False
        else:
            if(records[0][3] != TradeContext.tellerno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本柜员所做，不能做此交易"
                return False
            if(records[0][4] != TradeContext.brno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本网点所做，不能做此交易"
                return False
            if(records[0][5] != TradeContext.unitno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易公司不符，不能做此交易"
                return False
            if(records[0][6].strip() != TradeContext.amount.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易金额不符，不能做此交易"
                return False
           
            TradeContext.PreWorkDate = records[0][0]                  #原交易日期
            TradeContext.PreWorktime = records[0][1]                  #原交易时间
            TradeContext.PreTrxCode  = records[0][7]                  #原交易码
            TradeContext.amount = records[0][6]                       #金额
            TradeContext.preAgentSerno = TradeContext.preAgentSerno   #原交易流水号
        return True     
    except  Exception, e:                       
        AfaLoggerFunc.tradeInfo( str(e) )     
        AfaFlowControl.flowException( )       
                             