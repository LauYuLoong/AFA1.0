# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TAHJF001_8626.py
#   程序说明:   安徽手工录入处罚决定书查询交易交易
#
#   修改时间:   2011-01-20
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '初始化手工录入处罚决定书查询交易变量' )
    
    #交易代码（8626）
    TradeContext.tradeCode = TradeContext.TransCode
    TradeContext.paymDate = AfaUtilTools.GetSysDate( )
    #处罚决定书编号
    if not( TradeContext.existVariable( "punishNo" ) and len(TradeContext.punishNo.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "处罚决定书编号不存在"
        raise AfaFlowControl.flowException( ) 
   
    #缴费日期
    if not( TradeContext.existVariable( "paymDate" ) and len(TradeContext.paymDate.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费日期不存在"
        raise AfaFlowControl.flowException( ) 
        
    #处罚时间
    if not( TradeContext.existVariable( "punishDate" ) and len(TradeContext.punishDate.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "处罚时间不存在"
        raise AfaFlowControl.flowException( )     
    
    #违法行为代码 
    if not( TradeContext.existVariable( "punishCode" ) and len(TradeContext.punishCode.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "违法行为代码不存在"
        raise AfaFlowControl.flowException( )    
        
    #驾驶证编号
    if not( TradeContext.existVariable( "driversNo" ) and len(TradeContext.driversNo.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "驾驶证编号不存在"
        raise AfaFlowControl.flowException( )  
     
    #当事人
    if not( TradeContext.existVariable( "username" ) and len(TradeContext.username.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "当事人不存在"
        raise AfaFlowControl.flowException( )  
    
    #违法金额    
    if not( TradeContext.existVariable( "punishAmt" ) and len(TradeContext.punishAmt.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "违法金额不存在 "
        raise AfaFlowControl.flowException( )   
                  
    #判断罚款金额是否在罚款的上下限之间
    #try:
    #    sql = "select lower_amount,top_amount  from ahjf_lawcode where lawactioncode = '"+ TradeContext.punishCode +"'" 
    #    
    #    AfaLoggerFunc.tradeInfo( '查询ahjf_lawcode表的sql：'+ sql )
    #    records = AfaDBFunc.SelectSql( sql )
    #    if records == None:
    #        TradeContext.errorCode,TradeContext.errorMsg = "0001","查询数据失败"
    #        raise AfaFlowControl.flowException( )
    #    elif(len(records) < 1):
    #        TradeContext.errorCode,TradeContext.errorMsg = "0001","无此记录"
    #        raise AfaFlowControl.flowException( )
    #    else:
    #        minAmt   = float(records[0][0])
    #        maxAmt   = float(records[0][1])
    #        inputAmt = float(TradeContext.punishAmt)
    #        if minAmt > inputAmt or inputAmt  >  maxAmt :
    #            TradeContext.errorCode,TradeContext.errorMsg = "0001","输入的金额不在罚款的范围之内，请重新输入"
    #            raise AfaFlowControl.flowException( )
    #except  Exception, e:                     
    #    AfaLoggerFunc.tradeInfo( str(e) )     
    #    return AfaFlowControl.ExitThisFlow( "E0001", str(e) )         
    return True

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入安徽手工录入处罚决定书查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    
    try:
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
          
        if(TradeContext.errorCode=='0000'):
            TradeContext.errorMsg="手工录入处罚决定书查询交易成功"
        
        AfaLoggerFunc.tradeInfo('安徽手工录入处罚决定书查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )    
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return AfaFlowControl.exitMainFlow( "E0001",str(e) )
