# -*- coding: gbk -*-
##################################################################
#   财税库行.交易状态查询
#=================================================================
#   程序文件:   T3001_8460.py
#   修改时间:   2007-7-2 15:03
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,AfaFlowControl
import TipsFunc,AfaAfeFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '进入交易状态查询[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============获取平台流水号====================
        if TipsFunc.GetSerialno( ) == -1 :
            WrtLog('>>>处理结果:获取平台流水号异常' )
            sys.exit()
        
        #=============与第三方通讯====================
        AfaAfeFunc.CommAfe()
        if( TradeContext.errorCode != '0000' ):
            return False
        AfaLoggerFunc.tradeInfo( '退出交易状态查询['+TradeContext.TemplateCode+']\n' )
        return True
    except AfaFlowControl.flowException, e:
        return False
