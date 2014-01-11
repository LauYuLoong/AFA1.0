# -*- coding: gbk -*-
################################################################################
#   农信银系统：ECHO操作模板(中心回执)
#===============================================================================
#   模板文件:   TRCC007.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,TradeFunc,AfaFlowControl,os,AfaAfeFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('***农信银系统: ECHO操作模板['+TradeContext.TemplateCode+']进入***')
    try:
        #=====================初始化返回报文变量================================
        #TradeContext.tradeResponse=[]

        TradeContext.sysId = 'RCC01'
        TradeContext.TRCCO = '9900517'
 
        #=====================与中心通讯(回执)==================================
        AfaAfeFunc.CommAfe()

        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('***农信银系统: ECHO操作模板['+TradeContext.TemplateCode+']退出***')


    except AfaFlowControl.flowException, e:
        #流程异常
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #账务异常
        AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        #默认异常
        AfaFlowControl.exitMainFlow( str(e) )
