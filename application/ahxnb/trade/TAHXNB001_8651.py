###############################################################################
# -*- coding: gbk -*-
# 摘    要：新农保签约信息查询
# 当前版本：1.0
# 作    者：LLJ
# 完成日期：2012年7月
###############################################################################
import AfaDBFunc,AfaLoggerFunc,TradeContext,AfaFlowControl,AhXnbFunc
from types import *

def TrxMain( ):
    
    try:
    
        AfaLoggerFunc.tradeInfo('客户签约信息查询[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']进入' )
        
        #业务编号
        if ( not (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno.strip()) > 0) ):
            TradeContext.errorCode,TradeContext.errorMsg = '0001', "不存在业务编号"
            raise AfaFlowControl.flowException( )
            
        #单位编号
        if ( not (TradeContext.existVariable( "Busino" ) and len(TradeContext.Busino.strip()) > 0) ):
            TradeContext.errorCode,TradeContext.errorMsg = '0001', "不存在单位编号"
            raise AfaFlowControl.flowException( )
            
        #社保编号
        if ( not (TradeContext.existVariable( "sbno" ) and len(TradeContext.sbno.strip()) > 0) ):
            TradeContext.errorCode,TradeContext.errorMsg = '0001', "不存在社保编号"
            raise AfaFlowControl.flowException( )
        
        #判断单位协议是否有效
        TradeContext.I1APPNO =TradeContext.Appno
        TradeContext.I1BUSINO=TradeContext.Busino
        if ( not AhXnbFunc.ChkUnitInfo( ) ):
            return False
        
        sql = ""
        sql = sql + "select USERNAME,IDCODE,ACCNO,VOUHTYPE,PROTOCOLNO,BRNO,CONTRACTDATE from abdt_custinfo where "
        sql = sql + " APPNO ='" + TradeContext.Appno + "'"
        sql = sql + " and BUSINO ='" + TradeContext.Busino+ "'"
        sql = sql + " and BUSIUSERNO ='" +TradeContext.sbno+"'" 
        
        AfaLoggerFunc.tradeInfo("客户签约查询sql="+sql)
        records = AfaDBFunc.SelectSql( sql )
        
        if(records == None):
            AfaLoggerFunc.tradeInfo("查询数据库异常")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","查询数据库异常"
            
        elif(len(records)==0):
            AfaLoggerFunc.tradeInfo("没有查询到相关签约信息")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","没有查询到相关签约信息"
            
        elif(len(records)>1):
            AfaLoggerFunc.tradeInfo("客户签约信息不唯一")
            TradeContext.errorCode,TradeContext.errorMsg = "0001","客户签约信息不唯一"
            
        else:
            TradeContext.name        = records[0][0].strip()     #客户姓名
            TradeContext.idcode      = records[0][1].strip()     #证件号码
            TradeContext.accno       = records[0][2].strip()     #账号
            TradeContext.vouhtype    = records[0][3].strip()     #凭证类型
            TradeContext.protocolno  = records[0][4].strip()     #协议编号
            TradeContext.brno        = records[0][5].strip()     #签约机构
            TradeContext.contract_date = records[0][6].strip()   #签约日期
            
            
            TradeContext.errorCode  = "0000"
            TradeContext.errorMsg   = "交易成功"
            return True
        AfaLoggerFunc.tradeInfo('客户签约查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']退出' )
        
    
    except Exception, e:                   
        AfaFlowControl.exitMainFlow(str(e))