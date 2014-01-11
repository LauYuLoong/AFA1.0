# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TYBT003_8615.py
#   程序说明:   当日撤销（新保缴费撤销）
#   修改时间:   2010-7-30
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaYbtdb
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    
    AfaLoggerFunc.tradeInfo( '反交易数据预查询，查询是否有此新保缴费' )
   
    sql = "select workdate,worktime,userno,tellerno,brno,note9,unitno,amount,trxcode from afa_maintransdtl"
    sql = sql + " where agentserialno = '"+TradeContext.PreSerialno+"' and workdate = '"+TradeContext.workDate+"' and trxcode='8611'"
    sql = sql + " and revtranf = '0' and bankstatus = '0' and corpstatus = '0' and chkflag = '9'"
    
    AfaLoggerFunc.tradeInfo('反交易查询语句：'+ sql)
   
    records = AfaDBFunc.SelectSql( sql )
    
    AfaLoggerFunc.tradeInfo('反交易查询的结果：'+ str(records))
    
    if records == None:
        TradeContext.errorCode,TradeContext.errorMsg = "0001","反交易查询银保通数据失败"
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
        
        if(records[0][6] != TradeContext.unitno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易保险公司不符，不能做此交易"
            return False
        
        if(records[0][7].strip() != TradeContext.amount.strip()):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易金额不符，不能做此交易"
            return False
        
        if(records[0][5].split('|')[2] != TradeContext.policy):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易保险单号不符，不能做此交易"
            return False
    
        #原交易日期
        TradeContext.PreWorkDate = records[0][0]
        
        #原交易时间
        TradeContext.PreWorktime = records[0][1]
        
        #原交易码
        TradeContext.PreTrxCode = records[0][8]
        
        #金额
        TradeContext.amount = records[0][7]
        
        #保单印刷号
        TradeContext.userno = records[0][2]
        
        #原交易流水号
        TradeContext.preAgentSerno = TradeContext.PreSerialno
        
        #投保单号
        TradeContext.applno =records[0][5].split('|')[1]
        
        return True

def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo('进入当日撤销[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    
    try:
        names = Party3Context.getNames( )
        
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
            

        if( TradeContext.errorCode != '0000' ):
            
            AfaLoggerFunc.tradeInfo("银保通返回错误代码 ["+TradeContext.errorCode+"]")
            AfaLoggerFunc.tradeInfo("银保通返回错误信息 ["+TradeContext.errorMsg+"]")
            
            #第三方交易失败后记录错误码和错误信息
            if not AfaYbtdb.ADBUpdateTransdtlRev( ):
                raise AfaFlowControl.accException()
        
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

def SubModuleDoTrd( ):
    return True
