# -*- coding: gbk -*-
##################################################################
#   中间业务平台.停运启用通知（人行发起）
#=================================================================
#   程序文件:   TTPS001_845011.py
#   公司名称：  北京赞同科技有限公司
#   修改时间:   2008-9-9 
#   作    者：  阴晓亮
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,TipsFunc, AfaFlowControl,AfaDBFunc
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('停运启用通知前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    #============校验公共节点的有效性==================
    if( not TradeContext.existVariable( "RunSign" ) ):
        return TipsFunc.ExitThisFlow( 'A0001', '[RunSign]值不存在!' )
            
    #============RunSign=0 停运时======================
    if( TradeContext.RunSign=='0'):
        if not stop():
            return False
        if not start():
            return False

    #============RunSign=1 启用时======================
    if( TradeContext.RunSign=='1'):                
        if not start():
            return False
           
    TradeContext.errorCode='0000'
    TradeContext.errorMsg='交易处理成功'
    return True
    
    
#停运
def stop():
    try:
        AfaLoggerFunc.tradeInfo('RunSign='+TradeContext.RunSign+' 停运调度')
        
        if( TradeContext.existVariable( "StopRunTime" ) and len(TradeContext.StopRunTime)<=0 ):
            return TipsFunc.ExitThisFlow( 'A0001', '[StopRunTime]值不存在!' )
            
        year=(TradeContext.StopRunTime)[0:4]
        month=(TradeContext.StopRunTime)[4:6]
        day=(TradeContext.StopRunTime)[6:8]
        hour=(TradeContext.StopRunTime)[8:10]
        minute=(TradeContext.StopRunTime)[10:12]
          
        sql="UPDATE AFA_CRONADM               "
        sql=sql+" SET YEAR = '"+year+"',      "
        sql=sql+"     MONTH = '"+month+"',    "
        sql=sql+"     DAY = '"+day+"',        "
        sql=sql+"     HOUR = '"+hour+"',      "
        sql=sql+"     MINUTE = '"+minute+"',  "
        sql=sql+"     STATUS = '1'            "
        sql=sql+" WHERE TASKID = '00051'      "
            
        AfaLoggerFunc.tradeDebug(sql)
        
        records = AfaDBFunc.UpdateSqlCmt(sql)
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', '未发现调度信息:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
            
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e)) 
        
#启用
def start():
    try:
        AfaLoggerFunc.tradeInfo('RunSign='+TradeContext.RunSign+' 启用调度')
        if( TradeContext.existVariable( "BackRunTime" ) and len(TradeContext.BackRunTime)<=0 ):
            return TipsFunc.ExitThisFlow( 'A0001', '[BackRunTime]值不存在!' )
        
        year=(TradeContext.BackRunTime)[0:4]
        month=(TradeContext.BackRunTime)[4:6]
        day=(TradeContext.BackRunTime)[6:8]
        hour=(TradeContext.BackRunTime)[8:10]
        minute=(TradeContext.BackRunTime)[10:12]
            
        sql="UPDATE AFA_CRONADM              "
        sql=sql+" SET YEAR = '"+year+"',     "
        sql=sql+"     MONTH = '"+month+"',   "
        sql=sql+"     DAY = '"+day+"',       "
        sql=sql+"     HOUR = '"+hour+"',     "
        sql=sql+"     MINUTE = '"+minute+"', "
        sql=sql+"     STATUS = '1'           "
        sql=sql+" WHERE TASKID = '00050'     "
            
        AfaLoggerFunc.tradeInfo(sql)
        
        records = AfaDBFunc.UpdateSqlCmt(sql)
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', '未发现调度信息:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
      
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))         