# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TZJYW0001_8650.py
#   程序说明:   [查询中间业务流水号]
#   原 作 者：  LLJ
#   修改时间:   2012年6月
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *
        
def TrxMain():
    AfaLoggerFunc.tradeInfo('查询中间业务流水号[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']进入' )
    
    try:
        
        #只查询当天未对账的已成功正交易
        sql = ""
        sql = sql + "select AGENTSERIALNO from afa_maintransdtl where "
        sql = sql + " workdate = '" + TradeContext.workdate + "'"
        sql = sql + " and  bankstatus    = '0' and corpstatus = '0' and revtranf = '0' and chkflag='9'and corpchkflag='9'"
        
        #安贷保、银保通业务
        if((TradeContext.sysId =='AG2011' or TradeContext.sysId =='AG2013') and  TradeContext.existVariable( "printNo" ) and len(TradeContext.printNo.strip()) > 0  ):
            if ( not (TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno.strip()) > 0) ):
                TradeContext.errorCode,TradeContext.errorMsg = '0001', "查询条件不足，请输入正确的单位编号"
                raise AfaFlowControl.flowException( )
                
            sql = sql + " and sysid = '" + TradeContext.sysId+ "'"           
            sql = sql + " and  unitno  = '" + TradeContext.unitno + "'"  
            sql = sql + " and  userno  = '" + TradeContext.printNo.strip() + "'"        #保单印刷号
            
            
        #安徽交罚业务    
        if(TradeContext.sysId =='AG2017' and TradeContext.existVariable( "punishNo" ) and len(TradeContext.punishNo.strip()) > 0):
            sql = sql + " and sysid = '" + TradeContext.sysId+ "'"
            sql = sql + " and  unitno  = '0001'"                                        #0001
            sql = sql + " and  userno  = '" + TradeContext.punishNo.strip() + "'"       #处罚决定书编号
            
        #银电联网
        if(TradeContext.sysId =='AG2018'and TradeContext.existVariable( "userno" ) and len(TradeContext.userno.strip()) > 0):
            
            sql = sql + " and sysid = '" + TradeContext.sysId + "'"
            sql = sql + " and  unitno  = '00000001'"                                    #00000001
            sql = sql + " and  userno  = '" + TradeContext.userno.strip() + "'"         #用户编号
            
        if(TradeContext.existVariable( "bankserno" ) and len(TradeContext.bankserno.strip()) > 0):
            
            sql = sql + " and  bankserno  = '" + TradeContext.bankserno.strip() + "'"    #核心流水号            
        
        AfaLoggerFunc.tradeInfo('查询中间业务流水号：'+ sql)
        
        results = AfaDBFunc.SelectSql( sql )
        
        if results == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询中间业务流水号异常"
            return False
        
        if(len(results) == 0):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此交易,查询中间业务流水号失败"
            return False
            
        else:
            TradeContext.agentSerialno  = results[0][0]                        #中间业务流水号
            AfaLoggerFunc.tradeInfo(TradeContext.agentSerialno)       
            
        TradeContext.errorCode,TradeContext.errorMsg = '0000', "交易成功"
        AfaLoggerFunc.tradeInfo('中间业务流水号查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']退出' )
        return True
    
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
