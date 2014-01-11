###############################################################################
# -*- coding: gbk -*-
# 摘    要：新农保签约账号更改
# 当前版本：1.0
# 作    者：LLJ
# 完成日期：2012年7月
###############################################################################
import AfaDBFunc,AfaLoggerFunc,TradeContext,AfaFlowControl
from types import *

def TrxMain( ):
    
    try:
    
        AfaLoggerFunc.tradeInfo('客户签约账号更改[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']进入' )
        
        sql = ""
        sql = sql + "select USERNAME,ACCNO,VOUHTYPE,BRNO,TELLERNO from abdt_custinfo where "
        sql = sql + "  APPNO ='" + TradeContext.Appno + "'"
        sql = sql + " and BUSINO ='" + TradeContext.Busino+ "'"
        sql = sql + " and BUSIUSERNO ='" +TradeContext.sbno+"'" 
        
        AfaLoggerFunc.tradeInfo("查询原签约信息sql="+sql)
        records = AfaDBFunc.SelectSql( sql )
        
        if(records == None):
            AfaLoggerFunc.tradeInfo("查询数据库异常")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","查询数据库异常"
            
        elif(len(records)==0):
            AfaLoggerFunc.tradeInfo("没有查询到签约信息")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","没有查询到签约信息"
            
        elif(len(records)>1):
            AfaLoggerFunc.tradeInfo("客户签约信息不唯一")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","客户签约信息不唯一"
            
        else:
            #note5字段保存 原账号|原账号类型|
            TradeContext.accno       = records[0][1].strip()
            TradeContext.vouhtype    = records[0][2].strip()
            
            TradeContext.note5 = ''
            TradeContext.note5 = TradeContext.accno + '|'+ TradeContext.vouhtype
            AfaLoggerFunc.tradeInfo(TradeContext.note5) 
            
            #note3字段保存 更改账号日期|更改账号机构|更改账号柜员|
            TradeContext.note3 = ''
            TradeContext.note3 = TradeContext.note3 + TradeContext.WorkDate + '|' + TradeContext.brno +'|'+ TradeContext.tellerno
            AfaLoggerFunc.tradeInfo(TradeContext.note3) 
            
        #更改客户签约账号
        AfaLoggerFunc.tradeInfo(">>>更改客户签约账号")
        update_sql = ""
        update_sql = "UPDATE ABDT_CUSTINFO SET "
        update_sql = update_sql + "ACCNO = '" + TradeContext.accno1 + "',"
        update_sql = update_sql + "VOUHTYPE = '" + TradeContext.vouhtype1 + "',"
        update_sql = update_sql + "NOTE3 = '" + TradeContext.note3 + "',"
        update_sql = update_sql + "NOTE5 = '" + TradeContext.note5 + "'"
        update_sql = update_sql + "WHERE APPNO = '" + TradeContext.Appno + "'" 
        update_sql = update_sql + " and BUSINO ='" + TradeContext.Busino + "'"
        update_sql = update_sql + " and BUSIUSERNO ='" + TradeContext.sbno+ "'"
        
        AfaLoggerFunc.tradeInfo(update_sql)
        
        if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                return AfaFlowControl.ExitThisFlow("0001","更新账号失败！")
        
        TradeContext.errorCode,TradeContext.errorMsg = "0000","交易成功"    	
        
        AfaLoggerFunc.tradeInfo( '客户签约账号更改[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']退出' )
    
        return True 
    
    except Exception, e:                   
        AfaFlowControl.exitMainFlow(str(e))