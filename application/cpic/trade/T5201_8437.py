# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   004201_8430.py
#   程序说明:   [8430--6000112]新保保费试算
#   修改时间:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    try:
        if( TradeContext.errorCode == '0000' ):
            TradeContext.errorMsg = '交易成功'
        else:
            if( long(TradeContext.errorCode) < 0 ):
                TradeContext.errorMsg = '与第三方通讯失败'
                return False
            else:
                #响应码转换
                #return (AfaFunc.GetRespMsg( TradeContext.errorCode,TradeContext.sysId ))
                return True
        AfaLoggerFunc.tradeInfo('退出查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))