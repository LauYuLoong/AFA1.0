###############################################################################
# -*- coding: gbk -*-
# 摘    要：批量处理信息查询
# 当前版本：1.0
# 作    者：胡友
# 完成日期：2011年12月1日
###############################################################################
import AfaDBFunc,AfaLoggerFunc,TradeContext,AfaFlowControl
from types import *

def TrxMain( ):
    AfaLoggerFunc.tradeInfo('---------新农保柜面业务进入------------')
    
    #业务编号
    if ( not (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno.strip()) > 0) ):
        TradeContext.errorCode,TradeContext.errorMsg = 'NB001', "不存在业务编号"
        raise AfaFlowControl.flowException( )
    #单位编号
    if ( not (TradeContext.existVariable( "Busino" ) and len(TradeContext.Busino.strip()) > 0) ):
        TradeContext.errorCode,TradeContext.errorMsg = 'NB001', "不存在单位编号"
        raise AfaFlowControl.flowException( )
    #上传文件名
    if ( not (TradeContext.existVariable( "FileName" ) and len(TradeContext.FileName.strip()) > 0) ):
        TradeContext.errorCode,TradeContext.errorMsg = 'NB001', "不存在上传文件名"
        raise AfaFlowControl.flowException( )
    #申请日期
    if ( not (TradeContext.existVariable( "ApplyDate" ) and len(TradeContext.ApplyDate.strip()) > 0) ):
        TradeContext.errorCode,TradeContext.errorMsg = 'NB001', "不存在申请日期"
        raise AfaFlowControl.flowException( )
    
    sql = ""
    sql = sql + "select BATCHNO,FILENAME,SWAPFILENAME,WORKDATE,STATUS,"
    sql = sql + "PROCMSG,APPLYDATE,APPNO,BUSINO,TOTALNUM,TOTALAMT,FILETYPE,"
    sql = sql + "BRNO,TELLERNO,BEGINDATE,ENDDATE,WORKTIME,NOTE1,NOTE2,NOTE3,NOTE4"
    sql = sql + " from ahnx_file where"
    sql = sql + " FileName = '"+ TradeContext.FileName +"'"            #上传文件名
    sql = sql + " and ApplyDate = '"+ TradeContext.ApplyDate +"'"      #申请日期
    sql = sql + " and status <>"  + "'2'"                              #文件状态
    
    sql = sql + " and Appno = '"+ TradeContext.Appno +"'"              #业务编号
    sql = sql + " and Busino = '"+ TradeContext.Busino +"'"            #单位编号
    
    AfaLoggerFunc.tradeInfo("批量处理信息查询sql="+sql)
    records = AfaDBFunc.SelectSql( sql )
    
    if(records == None):
        AfaLoggerFunc.tradeInfo("批量处理信息查询数据库异常")
        return ExitSubTrade('NB000', '批量处理信息查询数据库异常')
    elif(len(records)==0):
        AfaLoggerFunc.tradeInfo("没有查询到相关的批量处理信息")
        return ExitSubTrade('NB002', '没有查询到相关的批量处理信息')
    elif(len(records)>1):
        AfaLoggerFunc.tradeInfo("该批量处理信息不唯一")
        return ExitSubTrade('NB003', '该批量处理信息不唯一')
    else:
        TradeContext.SwapFileName = records[0][2].strip()
        TradeContext.ProcMsg      = records[0][5].strip()
        TradeContext.FileType     = records[0][11].strip()
        TradeContext.batchNo      = records[0][0].strip()
        
    TradeContext.errorCode  = "0000"
    TradeContext.errorMsg   = "交易成功"
    AfaLoggerFunc.tradeInfo('---------新农保柜面业务退出------------')
    
    return ExitSubTrade('0000', '交易成功')


#------------------------------------------------------------------
#抛出并打印提示信息
#------------------------------------------------------------------
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg
        AfaLoggerFunc.tradeInfo( errorMsg )

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False