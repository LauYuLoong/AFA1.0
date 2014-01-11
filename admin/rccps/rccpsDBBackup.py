# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.备份农信银系统各登记簿
#===============================================================================
#   交易文件:   rccpsDBBackup.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2009-09-15
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc

def backupdb(tbName,clName,backupDate):
    
    AfaLoggerFunc.tradeInfo(">>>>开始统计表[" + tbName + "]" + backupDate + "]需备份数据")
    sql = "select count(*) from " + tbName + " where " + clName + " < '" + backupDate + "'"
    AfaLoggerFunc.tradeInfo(sql)
    
    rec = AfaDBFunc.SelectSql(sql)
    
    if rec == None:
        AfaLoggerFunc.tradeInfo(">>>>统计表[" + tbName + "][" + backupDate + "]需备份数据异常")
        rccpsCronFunc.cronExit("S999","统计表[" + tbName + "][" + backupDate + "]需备份数据异常")
    if len(rec) <= 0:
        AfaLoggerFunc.tradeInfo(">>>>统计表[" + tbName + "][" + backupDate + "]需备份数据异常")
        rccpsCronFunc.cronExit("S999","统计表[" + tbName + "][" + backupDate + "]需备份数据异常")
        
    if rec[0][0] <= 0:
        AfaLoggerFunc.tradeInfo(">>>>表[" + tbName + "][" + backupDate + "]无需备份数据")
        #rccpsCronFunc.cronExit("S999","实时汇兑登记簿[" + backupDate + "]无需备份数据")
    else:
        #导出表数据至文件
        file = path + "/" + tbName + ".del"
        
        if not os.path.exists(file):
            AfaLoggerFunc.tradeInfo(">>>>开始导出表[" + tbName + "][" + backupDate + "]数据至文件")
            
            cmd = "db2 \"export to '" + file + "' of del select * from " + tbName + " where " + clName + " < '" + backupDate + "'\""
            AfaLoggerFunc.tradeInfo(cmd)
            os.system(cmd)
            
            AfaLoggerFunc.tradeInfo(">>>>结束导出表[" + tbName + "][" + backupDate + "]数据至文件")
        else:
            AfaLoggerFunc.tradeInfo(">>>>表[" + tbName + "][" + backupDate + "]数据文件已存在")
        
        #导出表数据至历史表
        AfaLoggerFunc.tradeInfo(">>>>开始导出表[" + tbName + "][" + backupDate + "]数据至历史表")
        
        sql = ""
        sql = sql + "insert into " + tbName + "_his "
        sql = sql + "(select * from " + tbName + " where " + clName + " < '" + backupDate + "')"
        AfaLoggerFunc.tradeInfo(sql)
        
        rec = AfaDBFunc.InsertSql(sql)
        
        if (rec < 0):
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","导出表[" + tbName + "][" + backupDate + "]数据至历史表异常")
            
        AfaLoggerFunc.tradeInfo(">>>>结束导出表[" + tbName + "][" + backupDate + "]数据至历史表")
        
        #删除表数据
        AfaLoggerFunc.tradeInfo(">>>>开始删除表[" + tbName + "][" + backupDate + "]数据")
        
        sql = ""
        sql = sql + "delete from " + tbName + " where " + clName + " < '" + backupDate + "'"
        AfaLoggerFunc.tradeInfo(sql)
        
        rec = AfaDBFunc.DeleteSql(sql)
        
        if (rec < 0):
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","删除表[" + tbName + "][" + backupDate + "]数据异常")
            
        AfaLoggerFunc.tradeInfo(">>>>结束删除表[" + tbName + "][" + backupDate + "]数据")
        
        #提交事务
        if not AfaDBFunc.CommitSql():
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","提交事务异常")
            
        #重整表
        AfaLoggerFunc.tradeInfo(">>>>开始重整表[" + tbName + "]")
        
        cmd = "db2 \"reorg table " + tbName + "\" "
        AfaLoggerFunc.tradeInfo(cmd)
        os.system(cmd)
        
        AfaLoggerFunc.tradeInfo(">>>>结束重整表[" + tbName + "]")

if __name__ == '__main__':
    
    try:
        rccpsCronFunc.WrtLog("***农信银系统: 系统调度类.备份农信银各登记簿[rccpsDBBackup]进入***")
 
        #获取当前工作日期
        workDate=AfaUtilTools.GetSysDate()
        #AfaLoggerFunc.tradeInfo("当前日期[" + workDate + "]")
        #backupDate=str(long(workDate) - 100)
        #AfaLoggerFunc.tradeInfo("备份日期[" + backupDate + "]")

        AfaLoggerFunc.tradeInfo("当前日期[" + workDate + "]")

        #=====START 张恒增加于20091229 针对跨年并且当前月是01月则需备份上一年12月份的数据===
        if workDate[4:6] == '01' :
            backupDate = str(long(workDate) - 8900)
        else:
            backupDate=str(long(workDate) - 100)
        #=====END============================================================================
        AfaLoggerFunc.tradeInfo("备份日期[" + backupDate + "]")

        #创建备份文件存放目录
        AfaLoggerFunc.tradeInfo(">>>>开始创建[" + backupDate + "]目录")
        
        path = os.environ['AFAP_HOME'] + "/data/rccps/dbbackup/" + backupDate
        AfaLoggerFunc.tradeInfo(path)
        
        if not os.path.exists(path):
            cmd = "mkdir -p " + path
            AfaLoggerFunc.tradeInfo(cmd)
            os.system(cmd)
            
        AfaLoggerFunc.tradeInfo(">>>>结束创建[" + backupDate + "]目录")
        #rccpsCronFunc.cronExit("S999","退出")

        #连接数据库
        AfaLoggerFunc.tradeInfo(">>>>开始连接数据库")
        
        cmd = "db2 connect to maps"
        os.system(cmd)
        
        AfaLoggerFunc.tradeInfo(">>>>结束连接数据库")

        #实时汇兑登记簿相关操作
        backupdb("rcc_trcbka","bjedte",backupDate)
        
        #全国汇票登记簿相关操作
        backupdb("rcc_bilbka","bjedte",backupDate)
        
        #通存通兑登记簿相关操作
        backupdb("rcc_wtrbka","bjedte",backupDate)
                
        #当前状态登记簿相关操作
        backupdb("rcc_spbsta","bjedte",backupDate)
        
        #历史状态登记簿相关操作
        backupdb("rcc_sstlog","bjedte",backupDate)
        
        #实时汇兑对账明细登记簿相关操作
        backupdb("rcc_hddzmx","nccwkdat",backupDate)
        
        #全国汇票对账明细登记簿相关操作
        backupdb("rcc_hpdzmx","nccwkdat",backupDate)
        
        #通存通兑对账明细登记簿相关操作
        backupdb("rcc_tddzmx","nccwkdat",backupDate)
        
        #断开数据库
        AfaLoggerFunc.tradeInfo(">>>>开始断开数据库")
        
        cmd = "db2 disconnect maps"
        os.system(cmd)
        
        AfaLoggerFunc.tradeInfo(">>>>结束断开数据库")
        
        rccpsCronFunc.WrtLog("***农信银系统: 系统调度类.备份农信银各登记簿[rccpsDBBackup]退出***")
    
    except Exception, e:
        #所有异常

        if not AfaDBFunc.RollbackSql( ):
            rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.WrtLog(">>>Rollback异常")
        rccpsCronFunc.WrtLog(">>>Rollback成功")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = '系统错误['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            rccpsCronFunc.WrtLog( 'errorCode=['+TradeContext.errorCode+']' )
            rccpsCronFunc.WrtLog( 'errorMsg=['+TradeContext.errorMsg+']' )
            rccpsCronFunc.WrtLog('[rccpsDBBackup]交易中断')

        sys.exit(-1)

