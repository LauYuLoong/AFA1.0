# -*- coding: gbk -*-
##################################################################
#   中间业务平台.财税库行横向联网.状态变更通知
#   
#=================================================================
#   程序文件:   TTPS001_845008.py
#   修改时间:   2008-5-4 10:56
##################################################################
import TradeContext, AfaLoggerFunc,TipsFunc
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('状态变更通知交易前处理[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        if( not TradeContext.existVariable( "nextWorkDate" ) ):
            return TipsFunc.ExitThisFlow( '93002', 'TIPS工作日期[nextWorkDate]值不存在!' )
        if(  len(TradeContext.nextWorkDate)!=8 ):
            return TipsFunc.ExitThisFlow( '93001', 'TIPS工作日期[nextWorkDate]值不合法!' )
        if( not TradeContext.existVariable( "SysStat" ) ):
            return TipsFunc.ExitThisFlow( '93002', 'TIPS[SysStat]值不存在!' )
        
        if TradeContext.SysStat=='0':#日间
            #应用运行状态为：运行
            if(not TipsFunc.UpdAppStatus('1')):                                  
                return TipsFunc.ExitThisFlow( 'A0001', '修改应用运行状态失败!' )
            #修改应用工作日期
            if(not TipsFunc.UpdAppWorkDate(TradeContext.nextWorkDate)):
                return TipsFunc.ExitThisFlow( 'A0001', '修改应用工作日期失败!' )
        if TradeContext.SysStat=='1':#日切窗口
            #修改应用工作日期
            if(not TipsFunc.UpdAppWorkDate(TradeContext.nextWorkDate)):
                return TipsFunc.ExitThisFlow( 'A0001', '修改应用工作日期失败!' )
        if TradeContext.SysStat=='2':#系统维护状态
            #应用运行状态为：暂停
            if(not TipsFunc.UpdAppStatus('2')):                                  
                return TipsFunc.ExitThisFlow( 'A0001', '修改应用运行状态失败!' )

        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '交易成功' 
        #=============自动打包====================
        AfaLoggerFunc.tradeInfo('状态变更通知前处理结束[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))
