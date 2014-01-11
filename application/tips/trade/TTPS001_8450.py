# -*- coding: gbk -*-
##################################################################
#   代收代付平台.财税库行横向联网.前台发起登陆退出
#=================================================================
#   程序文件:   TTPS001_8450.py
#   修改时间:   2008-10-23
##################################################################

import TradeContext, TipsFunc
#LoggerHandler, UtilTools,, os
import AfaAfeFunc,AfaLoggerFunc

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('==========开始财税库行.前台发起登陆退出[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']==========')
    
    #=============获取平台流水号====================
    if TipsFunc.GetSerialno( ) == -1 :
        raise TipsFunc.flowException( )
        
    if TradeContext.OperFlag=='1':  #登陆
        #查询应用运行状态
        TipsFunc.SelAppStatus()
        if(TradeContext.flag == '1'):
            AfaLoggerFunc.tradeInfo('>>>应用运行状态为登陆，不能重复登陆')
            TradeContext.errorCode = '0001'
            TradeContext.errorMsg = '已登陆'
            return True
        
    elif TradeContext.OperFlag=='2': #退出
        #查询应用运行状态
        TipsFunc.SelAppStatus()
        if(TradeContext.flag == '2'):
            AfaLoggerFunc.tradeInfo('>>>应用运行状态为退出，不能重复退出')
            TradeContext.errorCode = '0001'
            TradeContext.errorMsg = '已退出'
            return True

    #=============与第三方通讯====================
    AfaAfeFunc.CommAfe()
    if( TradeContext.errorCode != '0000' ):
        return False
    else:
        if TradeContext.OperFlag=='1':  #登陆
            #查询应用运行状态
            #TipsFunc.SelAppStatus()
            #if(TradeContext.flag == '1'):
            #    TradeContext.errorMsg = '已登陆'
            #    return True
            AfaLoggerFunc.tradeInfo('>>>修改运行状态为登陆状态(1-登陆,0-退出)')
            if (not TipsFunc.UpdAppStatus('1')):
                raise TipsFunc.flowException( )
        elif TradeContext.OperFlag=='2': #退出
            AfaLoggerFunc.tradeInfo('>>>修改运行状态为退出状态(1-登陆,0-退出)')
            if (not TipsFunc.UpdAppStatus('0')):
                raise TipsFunc.flowException( )
        
        #TradeContext.errorMsg = '交易成功'
        
    AfaLoggerFunc.tradeInfo('==========退出财税库行.前台发起登陆退出[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']==========')
    return True
 
def SubModuleMainSnd ():
    return True
