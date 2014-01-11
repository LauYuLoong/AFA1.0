# -*- coding: gbk -*-
##################################################################
#   财税库行.请求TIPS重发对账明细
#=================================================================
#   程序文件:   TTPS001_8458.py
#   修改时间:   2007-7-2 15:03
##################################################################
import TradeContext, AfaLoggerFunc
#, UtilTools,TipsFunc
import TipsFunc,AfaAfeFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '进入请求TIPS重发对账明细查询[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    sbrno=TradeContext.brno
    try:
        #====判断机构状态=======
        if not TipsFunc.ChkBranchStatus( ):
            return False
        #====获取清算信息=======
        if not TipsFunc.ChkLiquidStatus( ):
            return False
        if TradeContext.brno != TradeContext.__mainBrno__:
            return TipsFunc.ExitThisFlow( 'A0002', '非清算机构，不允许做此交易')
        #=============获取平台流水号==================== 
        if TipsFunc.GetSerialno( ) == -1 :
            raise TipsFunc.flowException( )
        
        #=============与第三方通讯====================
        AfaAfeFunc.CommAfe()

        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '请求已受理，请稍候查询对账结果'
        
        AfaLoggerFunc.tradeInfo( '退出请求TIPS重发对账明细['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except TipsFunc.flowException, e:
        return False
