# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.汇兑对账文件下载
#===============================================================================
#   交易文件:   rccpsHDDZGetFile.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-24
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc
import rccpsDBTrcc_mbrifa


if __name__ == "__main__":
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇兑对账文件下载[rccpsHDDZGetFile]进入***")

        local_home = os.environ['AFAP_HOME'] + "/data/rccps/"
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #================判断前置机汇兑对账文件是否传送完毕=========================
        AfaLoggerFunc.tradeInfo(">>>开始判断前置机汇兑对账文件是否传送完毕")
        
        file_path = "settlefile/hdsendend1340000008"
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","下载文件[" + file_path + "]异常")
        
        local_file_path = local_home + file_path
        
        fp = open(local_file_path,"rb")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","打开汇兑对账文件传送标识文件异常")
        
        file_line = fp.readline()
        file_line = AfaUtilTools.trim(file_line)
        
        fp.close()
        
        if file_line[:8] != NCCWKDAT:
            rccpsCronFunc.cronExit("S999","汇兑对账文件尚未传送完毕")
        
        AfaLoggerFunc.tradeInfo(">>>汇兑对账文件传送完毕")
        
        AfaLoggerFunc.tradeInfo(">>>结束判断前置机汇兑对账文件是否传送完毕")
        
        #================下载汇兑对账文件下载=======================================
        AfaLoggerFunc.tradeInfo(">>>开始下载汇兑对账文件")
        
        file_path = "settlefile/HDHZCNY1340000008" + NCCWKDAT
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","下载汇兑对账汇总文件[" + file_path + "]异常")
        
        file_path = "settlefile/HDMXCNY1340000008" + NCCWKDAT
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","下载汇兑对账明细文件[" + file_path + "]异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束下载汇兑对账文件")
        
        #================关闭汇兑对账文件下载系统调度,打开导入汇兑对账文件系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭汇兑对账文件下载系统调度,打开导入汇兑对账文件系统调度")
        if not rccpsCronFunc.closeCron("00031"):
            rccpsCronFunc.cronExit("S999","关闭汇兑对账文件下载系统调度异常")
            
        if not rccpsCronFunc.openCron("00034"):
            rccpsCronFunc.cronExit("S999","打开汇兑对账明细文件导入系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭汇兑对账文件下载系统调度,打开导入汇兑对账文件系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇兑对账文件下载[rccpsHDDZGetFile]退出***")
        

    except Exception, e:
        #所有异常

        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = '系统错误['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            AfaLoggerFunc.tradeInfo( 'errorCode=['+TradeContext.errorCode+']' )
            AfaLoggerFunc.tradeInfo( 'errorMsg=['+TradeContext.errorMsg+']' )
            AfaLoggerFunc.tradeInfo('***[rccpsHDDZGetFile]交易中断***')

        sys.exit(-1)
