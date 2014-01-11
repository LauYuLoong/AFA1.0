# -*- coding: gbk -*-
##################################################################
#   中间业务平台.止付请求
#=================================================================
#   程序文件:   003001_031123.py
#   修改时间:   2007-5-28 10:28
##################################################################
import TradeContext, LoggerFunc, UtilTools,AfaFlowControl,AfaAfeFunc,AfapFunc,DBFunc

#import datetime,TradeException,ConfigParser,os,TipsFunc
from types import *

def SubModuleMainFst( ):
    LoggerFunc.tradeInfo('财税库行_止付请求交易_前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============获取当前系统时间====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        ##============校验公共节点的有效性==================
        #if( not AfapFunc.Query_ChkVariableExist( ) ):
        #    raise AfaFlowControl.flowException( )
        ##===============判断应用系统状态======================
        #if not AfapFunc.ChkSysStatus( ) :
        #    raise AfaFlowControl.flowException( )
        ##===============判断商户状态======================
        #if not AfapFunc.ChkUnitStatus( ) :
        #    raise AfaFlowControl.flowException( )
        ##=============判断应用状态====================
        #if not AfapFunc.ChkAppStatus( ) :
        #    raise AfaFlowControl.flowException( )
        #
                    
        #============变量值的有效性校验============
        if( not TradeContext.existVariable( "TaxOrgCode" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[TaxOrgCode]值不存在!' )
        if( not TradeContext.existVariable( "OriPackNo" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[OriPackNo]值不存在!' )
        if( not TradeContext.existVariable( "EntrustDate" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[EntrustDate]值不存在!' )
        if( not TradeContext.existVariable( "OriEntrustDate" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[OriEntrustDate]值不存在!' )
        if( not TradeContext.existVariable( "StopReason" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[StopReason]值不存在!' )
        if( not TradeContext.existVariable( "StopType" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[StopType]值不存在!' )
        
        if (TradeContext.StopType=='0'):
            if( not TradeContext.existVariable( "OriTraNo" ) ):
                return AfaFlowControl.ExitThisFlow( 'A0001', '[OriTraNo]值不存在!' )
            #查询批量流水处理状态
            sqlStr = "SELECT STATUS FROM BATCH_TRANSDTL WHERE "
            sqlStr =sqlStr +" sysid             = '" + TradeContext.appNo           + "'"
            sqlStr =sqlStr +"and unitno         = '" + TradeContext.unitno          + "'"
            #sqlStr =sqlStr +"and subUnitno      = '" + TradeContext.subUnitno       + "'"
            sqlStr =sqlStr +"and workDate       = '" + TradeContext.OriEntrustDate  + "'"
            sqlStr =sqlStr +"and Batchno        = '" + TradeContext.PackNo          + "'"
            sqlStr =sqlStr +"and CORPSERIALNO   = '" + TradeContext.OriTraNo        + "'"
            sqlStr =sqlStr +"and NOTE1          = '" + TradeContext.TaxOrgCode      + "'"
            Records = DBFunc.SelectSql( sqlStr )
            LoggerFunc.tradeInfo(sqlStr)
            if( Records == None ):
                LoggerFunc.tradeFatal('批量管理表操作异常:'+DBFunc.sqlErrMsg)
                return AfaFlowControl.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
            elif(len(Records)>0):
                if Records[0][0]=='9': #流水尚未处理
                    sqlStr = "UPDATE BATCH_TRANSDTL SET STATUS='1',ERRORMSG='已止付' WHERE "
                    sqlStr =sqlStr +" sysid             = '" + TradeContext.appNo           + "'"
                    sqlStr =sqlStr +"and unitno         = '" + TradeContext.unitno          + "'"
                    #sqlStr =sqlStr +"and subUnitno      = '" + TradeContext.subUnitno       + "'"
                    sqlStr =sqlStr +"and workDate       = '" + TradeContext.OriEntrustDate  + "'"
                    sqlStr =sqlStr +"and Batchno        = '" + TradeContext.OriPackNo          + "'"
                    sqlStr =sqlStr +"and CORPSERIALNO   = '" + TradeContext.OriTraNo        + "'"
                    sqlStr =sqlStr +"and NOTE1          = '" + TradeContext.TaxOrgCode      + "'"
                    LoggerFunc.tradeInfo(sqlStr )
                    records=DBFunc.UpdateSqlCmt( sqlStr )
                    if( records <0 ):
                        TradeContext.errorCode='A0027'
                        TradeContext.StopAnswer='3'
                        TradeContext.errorMsg='止付失败,数据库异常'
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='1'
                    TradeContext.errorMsg='止付成功'
                elif Records[0][0]=='1': #原流水处理失败，则止付成功
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='1'
                    TradeContext.errorMsg='止付成功'
                elif Records[0][0]=='0': #原流水处理成功，则止付成功
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='2'
                    TradeContext.errorMsg='止付成功'
                else:
                    TradeContext.errorCode='A0027'
                    TradeContext.StopAnswer='3'
                    TradeContext.errorMsg='止付失败,交易已处理'
        else:
            #查询批量处理状态
            sqlStr = "SELECT DEALSTATUS FROM BATCH_ADM WHERE "
            sqlStr =sqlStr +" sysid     = '" + TradeContext.appNo       + "'"
            sqlStr =sqlStr +"and unitno    = '" + TradeContext.unitno      + "'"
            #sqlStr =sqlStr +"and subUnitno = '" + TradeContext.subUnitno   + "'"
            sqlStr =sqlStr +"and workDate  = '" + TradeContext.OriEntrustDate + "'"
            sqlStr =sqlStr +"and Batchno   = '" + TradeContext.OriPackNo      + "'"
            sqlStr =sqlStr +"and note1     = '" + TradeContext.TaxOrgCode  + "'"
            Records = DBFunc.SelectSql( sqlStr )
            LoggerFunc.tradeInfo(sqlStr)
            if( Records == None ):
                LoggerFunc.tradeFatal('批量管理表操作异常:'+DBFunc.sqlErrMsg)
                return AfaFlowControl.ExitThisFlow( 'A0027', '数据库错，批量管理表操作异常' )
            elif(len(Records)>0):
                if Records[0][0]=='9': #原批次尚未处理
                    sqlStr = "UPDATE  BATCH_ADM SET DEALSTATUS='1',ERRORCODE='24020',ERRORMSG='已止付' WHERE "
                    sqlStr =sqlStr +" sysid             = '" + TradeContext.appNo           + "'"
                    sqlStr =sqlStr +"and unitno         = '" + TradeContext.unitno          + "'"
                    #sqlStr =sqlStr +"and subUnitno      = '" + TradeContext.subUnitno       + "'"
                    sqlStr =sqlStr +"and workDate       = '" + TradeContext.OriEntrustDate  + "'"
                    sqlStr =sqlStr +"and Batchno        = '" + TradeContext.OriPackNo          + "'"
                    sqlStr =sqlStr +"and NOTE1          = '" + TradeContext.TaxOrgCode      + "'"
                    LoggerFunc.tradeInfo(sqlStr )
                    records=DBFunc.UpdateSqlCmt( sqlStr )
                    if( records <0 ):
                        TradeContext.errorCode='A0027'
                        TradeContext.StopAnswer='3'
                        TradeContext.errorMsg='止付失败,数据库异常'
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='1'
                    TradeContext.errorMsg='止付成功'
                elif Records[0][0]=='1': #原批次处理失败，则止付成功
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='1'
                    TradeContext.errorMsg='止付成功'
                elif Records[0][0]=='0': #原批次处理成功，则止付成功
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='2'
                    TradeContext.errorMsg='止付成功'
                else:
                    TradeContext.errorCode='A0027'
                    TradeContext.StopAnswer='3'
                    TradeContext.errorMsg='止付失败,交易已处理'
        
        #=============获取平台流水号====================
        if AfapFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
        #=============与第三方通讯，发送止付应答====================
        TradeContext.TransCode='2123' #止付应答
        AfaAfeFunc.CommAfe()
        
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='交易成功'
        LoggerFunc.tradeInfo('处理结果:')
        LoggerFunc.tradeInfo('财税库行_止付请求交易_前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
