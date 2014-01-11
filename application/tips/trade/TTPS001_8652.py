# -*- coding: gbk -*-
###############################################################################
# Copyright (c) 2011,北京赞同科技发展有限公司.第三事业部
# All rights reserved.
# 文件名称：TPS001_8652.py
# 文件标识：
# 摘    要：财税库行.变更开户行行号
# 当前版本：1.0
# 作    者：
# 完成日期：2012 年 7 月
# 取代版本：
# 原 作 者：LLJ
###############################################################################
import TradeContext
TradeContext.sysType = 'tips'
import TipsFunc, AfaDBFunc,AfaLoggerFunc,AfaFlowControl
#,ConfigParser,os,LoggerHandler, UtilTools, 
#import TipsHostFunc,HostContext,TradeContext, 

def SubModuleMainFst( ):
    try:
        
        AfaLoggerFunc.tradeInfo( '进入变更开户行行号[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        
        #检查原开户行行号是否与数据库中登记的开户行行号一致
        sqlStr = ""
        sqlStr = sqlStr + "SELECT PAYOPBKCODE FROM TIPS_CUSTINFO WHERE TAXORGCODE = '" + TradeContext.taxOrgCode + "'" 
        sqlStr = sqlStr + " AND PAYACCT ='" + TradeContext.payAcct + "'"
        #sqlStr = sqlStr + " AND PAYOPBKCODE ='" + TradeContext.payBkCode+ "'"
        sqlStr = sqlStr + " AND PROTOCOLNO ='" +TradeContext.protocolNo+"'"
        
        AfaLoggerFunc.tradeInfo(sqlStr)
        
        records = AfaDBFunc.SelectSql( sqlStr )
        
        if( records == None ):
            
            return TipsFunc.ExitThisFlow( 'A0027', '表操作异常:'+AfaDBFunc.sqlErrMsg )
                
        elif( len( records )==0 ):
                
            return TipsFunc.ExitThisFlow( 'A0027', '没有满足条件的数据记录！' )
            
        else: 
            AfaLoggerFunc.tradeDebug("原开户行行号为：" +records[0][0])
                
        if(records[0][0] !=TradeContext.payBkCode):
            TradeContext.errorCode,TradeContext.errorMsg = "A0001","原开户行行号不正确！"
            return False
                
        
        #====================更新开户行行号====================
        AfaLoggerFunc.tradeInfo(">>>更改开户行行号")
        update_sql = ""
        update_sql = "UPDATE TIPS_CUSTINFO SET PAYOPBKCODE = '" + TradeContext.payBkCode1 + "'"
        update_sql = update_sql + "WHERE TAXORGCODE = '" + TradeContext.taxOrgCode + "'"
        update_sql = update_sql + " AND PAYACCT ='" + TradeContext.payAcct + "'"
        update_sql = update_sql + " AND PAYOPBKCODE ='" + TradeContext.payBkCode+ "'"
        update_sql = update_sql + " AND PROTOCOLNO ='" +TradeContext.protocolNo+"'" 
        
        AfaLoggerFunc.tradeInfo(update_sql)
        
        if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                return AfaFlowControl.ExitThisFlow("A0027","更新开户行行号失败！")
        
        TradeContext.errorCode,TradeContext.errorMsg = "0000","交易成功"

        AfaLoggerFunc.tradeInfo( '退出变更开户行行号[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
        return True 
    
    except Exception, e:             

        AfaFlowControl.exitMainFlow(str(e))    
