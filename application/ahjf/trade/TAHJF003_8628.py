# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TTJYW003_8628.py
#   程序说明:   处罚决定书缴费冲正交易
#   修改时间:   2011-01-21
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaAfeFunc,AfaFlowControl,Party3Context,AhjfFunc
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    
    AfaLoggerFunc.tradeInfo( '反交易数据预查询，查询是否有此缴费记录' )
    try:
        sql = "select workdate,userno,tellerno,brno,amount from afa_maintransdtl"
        sql = sql + " where agentserialno = '"+TradeContext.preAgentSerno+"' and workdate = '"+TradeContext.workDate+"' and trxcode='8627'"
        sql = sql + " and revtranf = '0' and bankstatus = '0'and chkflag = '9'"
        
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
            if(records[0][1] != TradeContext.punishNo):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易的处罚交款书编号不一致，不能做此交易"
                return False
            
            if(records[0][2] != TradeContext.tellerno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本柜员所做，不能做此交易"
                return False
            if(records[0][3] != TradeContext.brno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本网点所做，不能做此交易"
                return False
            if(records[0][4].strip() != TradeContext.amount.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","与原交易金额不符，不能做此交易"
                return False
           
            TradeContext.orgDate       = records[0][0]                #原交易日期
            TradeContext.punishNo      = records[0][1]                #处罚交款书编号 
            TradeContext.userno        = records[0][1]                #初始化userno的值，取消变量检查时需要
            TradeContext.amount        = records[0][4]                #金额 
            TradeContext.preAgentSerno = TradeContext.preAgentSerno   #原交易流水号
        TradeContext.note2             = TradeContext.busino          #签约单位编号
            
        return True     
    except  Exception, e:                     
        AfaLoggerFunc.tradeInfo( str(e) )     
        AfaFlowControl.flowException( )   
            
def SubModuleDoSnd( ):
    AfaLoggerFunc.tradeInfo('进入撤销冲正[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    
    try:
        names = Party3Context.getNames( )
        
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
            

        if( TradeContext.errorCode != '0000' ):
            
            AfaLoggerFunc.tradeInfo("返回错误代码 ["+TradeContext.errorCode+"]")
            AfaLoggerFunc.tradeInfo("返回错误信息 ["+TradeContext.errorMsg+"]")
            
            #第三方交易失败后记录错误码和错误信息
            if not AhjfFunc.ADBUpdateTransdtlRev( ):
                raise AfaFlowControl.accException()
        
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))

def SubModuleDoTrd( ):
    return True
                            