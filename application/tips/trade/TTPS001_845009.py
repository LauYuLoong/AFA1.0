# -*- coding: gbk -*-
##################################################################
#   中间业务平台.故障通知（人行发起）
#=================================================================
#   程序文件:   TTPS001_845009.py
#   修改时间:   2007-5-28 10:28
##################################################################
import TradeContext, AfaLoggerFunc, TipsFunc,AfaFlowControl
import AfaDBFunc
#UtilTools,
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('故障通知交易前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        
        AfaLoggerFunc.tradeInfo('节点故障通知' )
        sql="UPDATE TIPS_NODECODE SET RUNSTATUS='"+TradeContext.NodeState+\
            "',NOTE2='"+ TradeContext.TroubleReason+\
            "' where NODECODE='"+ TradeContext.TroubleNode+"'"
        AfaLoggerFunc.tradeInfo(sql )
        records=AfaDBFunc.UpdateSqlCmt( sql )
        if( records <0 ):
            AfaLoggerFunc.tradeFatal( sql )
            return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，节点信息表操作异常:'+AfaDBFunc.sqlErrMsg )
        if( records ==0 ):
            AfaLoggerFunc.tradeFatal( sql )
            return AfaFlowControl.ExitThisFlow( 'A0027', '数据库错误，无此节点信息:'+AfaDBFunc.sqlErrMsg )

        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '交易成功' 
        #=============自动打包====================
        AfaLoggerFunc.tradeInfo('故障通知前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))
