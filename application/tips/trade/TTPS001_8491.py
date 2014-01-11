
# -*- coding: gbk -*-
##################################################################
#   财税库行.报表打印
#=================================================================
#   程序文件:   TTPS001_8491.py
#   修改时间:   2007-7-2 15:03
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,AfaFlowControl
#import TipsFunc,AfaAfeFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '进入报表打印[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    TradeContext.appNo      ='AG2010'
    TradeContext.busiNo  ='00000000000001'
    sbrno=TradeContext.brno
    try:
        #=============获取当前系统时间====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        TradeContext.errorCode = '0000'
        TradeContext.errorCode = '无相应的打印明细'

        AfaLoggerFunc.tradeInfo( '退出报表打印['+TradeContext.TemplateCode+']\n' )
        return True
    except AfaFlowControl.flowException, e:
        return False
