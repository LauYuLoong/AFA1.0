# -*- coding: gbk -*-
##################################################################
#   中间业务平台.强制退出（人行发起）
#=================================================================
#   程序文件:   TTPS001_845010.py
#   修改时间:   2007-5-28 10:28
##################################################################
import TradeContext, AfaLoggerFunc,TipsFunc
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('强制退出交易前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #签退
        if (not TipsFunc.UpdAppStatus('0')):
            raise TipsFunc.flowException( )
        
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '交易成功' 
        AfaLoggerFunc.tradeInfo('强制退出前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))
