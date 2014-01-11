# -*- coding: gbk -*-
###################################################################
#    大前置系统.主机日期与时间同步
#==================================================================
#    程序文件：  get_date.py
#    修改时间：  2008-7-7
#    作    者：  刘雨龙
#==================================================================
#    修改时间：
#    修改者  ：
#==================================================================
#    功    能：  向主机发起同步操作
###################################################################
import TradeContext,HostContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
import AfaHostFunc
import sys, time

from types import *

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***大前置系统: 同步主机日期与时间 进入***")

        #=====开始拼主机接口====
        TradeContext.TransCode   = '9999'             #交易码
        HostContext.I1TRCD      = '8808'             #主机交易码
        HostContext.I1SBNO      = '3401018889'       #机构号
        HostContext.I1USID      = '999986'           #柜员号
        HostContext.I1WSNO      = '1234567890'       #终端号
        HostContext.I1PYNO      = '9999'             #系统标识
        HostContext.I1AUUS = ''
        HostContext.I1AUPS = ''

        #====与主机进行通讯====
        AfaHostFunc.CommHost('8808')
      
        #=====判断主机返回结果====
        if TradeContext.errorCode == '0000':
            #=====同步数据库表AFA_DATE====
            sql = "UPDATE AFA_DATE SET WORKDATE='" + HostContext.O1TRDT + "'"
            sql = sql + ", WORKTIME = '" + HostContext.O1TRTM + "'"
            sql = sql + ", HOSTDATE = '" + HostContext.O1DATE + "'"

        ret = AfaDBFunc.UpdateSqlCmt(sql)
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
        else:
            AfaLoggerFunc.tradeInfo('主机日期['+HostContext.O1TRDT +']')
            AfaLoggerFunc.tradeInfo('主机时间['+HostContext.O1TRTM +']')

        AfaLoggerFunc.tradeInfo("***大前置系统: 同步主机日期与时间 退出***")

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        sys.exit(-1)
