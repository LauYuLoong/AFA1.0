# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   004203_8203.py
#   程序说明:   [8432--6000901]当日投保撤销
#   修改时间:   2006-04-06
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaAhAdb
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    #TradeContext.Amount = ""
    AfaLoggerFunc.tradeInfo( '反交易数据预查询' )
    sql = "select corpserno,workdate,worktime,userno,amount,tellerno,brno,note5 "
    sql = sql + "from afa_maintransdtl where agentserialno = '"+TradeContext.PreSerialno+"'"
    sql = sql + "and workdate = '"+TradeContext.workDate+"'"
    sql = sql + " and revtranf = '0' and bankstatus = '0' and corpstatus = '0' and chkflag = '9'"
    AfaLoggerFunc.tradeInfo('反交易查询语句'+ sql)
    records = AfaDBFunc.SelectSql( sql )
    if(len(records) < 1):
        TradeContext.errorCode,TradeContext.errorMsg = "0001","无此交易"
        return False
    else:
        if(records[0][5] != TradeContext.tellerno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本柜员所做，不能做此交易"
            return False
        if(records[0][6] != TradeContext.brno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本网点所做，不能做此交易"
            return False
        #原交易的太保流水号
        TradeContext.PreCpicno = records[0][0]
        #原交易日期
        TradeContext.PreWorkDate = records[0][1]
        #原交易时间
        TradeContext.PreWorktime = records[0][2]
        #保单号
        TradeContext.userno = records[0][3]
        TradeContext.CpicNo = records[0][3]
        #金额
        TradeContext.amount = records[0][4]
        #保单号(撤销用)与保险单号不同
        TradeContext.PolNumber = records[0][7]
        #流水号
        TradeContext.preAgentSerno = TradeContext.PreSerialno
    return True
def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo('进入缴费反交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    try:
        
        Party3Context.preAgentSerno = TradeContext.preAgentSerno
        Party3Context.Amount        = TradeContext.amount        
        Party3Context.workDate      = TradeContext.workDate      

        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            setattr( TradeContext, name, value )
            #AfaLoggerFunc.tradeInfo("字段名称  ["+str(name)+"] =  "+str(value))

        if( TradeContext.errorCode != '0000' ):
            AfaLoggerFunc.tradeInfo("太保返回错误代码 ["+TradeContext.errorCode+"]")
            AfaLoggerFunc.tradeInfo("太保返回错误信息 ["+TradeContext.errorMsg+"]")
            #第三方交易失败后记录错误码和错误信息
            if not AfaAhAdb.ADBUpdateTransdtlRev( ):
                raise AfaFlowControl.accException()
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

def SubModuleDoTrd( ):
    return True
