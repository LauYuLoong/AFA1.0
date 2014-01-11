# -*- coding: gbk -*-
###################################################################
#    农信银系统.echo报文发送
#==================================================================
#    程序文件：  send_echo.py
#    修改时间：  2008-6-8
#    作    者：  刘雨龙
#==================================================================
#    修改时间：
#    修改者  ：
#==================================================================
#    功    能：  向AFE发送往来echo报文
###################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
import rccpsCronFunc,AfaAfeFunc
import sys, time

from types import *
from rccpsConst import *

if __name__ == '__main__':
    
    try:
        rccpsCronFunc.WrtLog("***农信银系统: 网络echo报文发送 进入***")

        #=====开始拼网络echo报文====
        TradeContext.MSGTYPCO    = 'SET000'
        TradeContext.TransCode   = '9900516'
        TradeContext.TRCCO    = '9900516'
        TradeContext.IPADDR   = '0'
        TradeContext.PORT     = '0'
        TradeContext.LNKNO    = '1'
        TradeContext.ECHINFNO = '1'
        TradeContext.BRSFLG   = '0'
        #====拼模板名称====
        TradeContext.TemplateCode = 'RCC007'
        TradeContext.sysId = 'RCC01'

        #====与afe进行通讯====
        AfaAfeFunc.CommAfe()

        rccpsCronFunc.WrtLog("***农信银系统: 网络echo报文发送 退出***")
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
        sys.exit(-1)
