# -*- coding: gbk -*-
##################################################################
#   代收代付平台.财税库行.连接测试
#=================================================================
#   程序文件:   T3001_8462.py
#   修改时间:   2007-10-18 
##################################################################

import TradeContext, AfaLoggerFunc
import AfaAfeFunc,TipsFunc
#LoggerHandler, UtilTools, os, 

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('==========开始财税库行.连接测试[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']==========')
    #=============获取平台流水号====================
    if TipsFunc.GetSerialno( ) == -1 :
        raise TipsFunc.flowException( )
    
    #=============与第三方通讯====================
    AfaAfeFunc.CommAfe()
    AfaLoggerFunc.tradeInfo('>>>连接测试结果:['+TradeContext.errorCode+']'+TradeContext.errorMsg )
    if( TradeContext.errorCode != '0000' ):
        return False
        
    AfaLoggerFunc.tradeInfo('==========退出财税库行.连接测试[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']==========')
    return True
 
def SubModuleMainSnd ():
    return True