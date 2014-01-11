# -*- coding: gbk -*-
##################################################################
#   中间业务平台.对账回执处理
#   功能描述：发起对账回执交易到人行
#=================================================================
#   程序文件:   003001_032111.py
#   修改时间:   2007-5-28 10:28
##################################################################
import TradeContext, AfaLoggerFunc, TipsFunc,AfaAfeFunc
from types import *

def SubModuleMainFst( ):
    TradeContext.TransCode='2111'
    AfaLoggerFunc.tradeInfo('财税库行_对账回执处理_前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:

        #=============获取平台流水号====================
        if TipsFunc.GetSerialno( ) == -1 :
            AfaLoggerFunc.tradeInfo('>>>处理结果:获取平台流水号异常' )
            return TipsFunc.ExitThisFlow( 'A0027', '获取流水号失败' )

        #=============与第三方通讯====================
        AfaAfeFunc.CommAfe()
                
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='交易成功'
        AfaLoggerFunc.tradeInfo('财税库行_对账回执处理_前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
