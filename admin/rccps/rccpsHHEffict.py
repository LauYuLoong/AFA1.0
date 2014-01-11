# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.行号生效处理
#===============================================================================
#   交易文件:   rccpsHHEffict.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-09-15
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc,rccpsHostFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_paybnk

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.行名行号生效处理[rccpsHHEffict]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NWWKDAT'][:8]                           #当前中心工作日期
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #========行号生效处理==================================================
        AfaLoggerFunc.tradeInfo("开始生效行号")
        
        bank_sql = ""
        bank_sql = bank_sql + "update rcc_paybnk set note1 = '1' "
        bank_sql = bank_sql + "where alttype in ('1','2') and bankbin in ("
        bank_sql = bank_sql + "select bankbin from rcc_paybnk "
        bank_sql = bank_sql + "where '" + NCCWKDAT +  "' >= efctdat)"
        
        AfaLoggerFunc.tradeInfo(bank_sql)
        
        ret = AfaDBFunc.executeUpdateCmt(bank_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","修改已生效的行号生效失效标识为(1-生效)异常")
            
        AfaLoggerFunc.tradeInfo("结束生效行号")
        
        #========行号失效处理==================================================
        AfaLoggerFunc.tradeInfo("开始失效行号")
        
        bank_sql = ""
        bank_sql = bank_sql + "update rcc_paybnk set note1 = '2' "
        bank_sql = bank_sql + "where alttype in ('3') and bankbin in ("
        bank_sql = bank_sql + "select bankbin from rcc_paybnk "
        bank_sql = bank_sql + "where '" + NCCWKDAT + "' >= efctdat)"
        
        AfaLoggerFunc.tradeInfo(bank_sql)
        
        ret = AfaDBFunc.executeUpdateCmt(bank_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","修改已失效的行号生效失效标识为(2-失效)异常")
        
        AfaLoggerFunc.tradeInfo("结束失效行号")
        
        #========删除已加入NCS系统的特约汇兑系统行号===========================
        AfaLoggerFunc.tradeInfo("开始删除已加入NCS系统的特约汇兑系统行号")
        
        bank_sql = ""
        bank_sql = bank_sql + "delete from rcc_paybnk "
        bank_sql = bank_sql + "where note1 = '2' and newoflg = '2' "
        bank_sql = bank_sql + "and bankbin in ("
        bank_sql = bank_sql + "select bankbin from rcc_paybnk "
        bank_sql = bank_sql + "where '" + NCCWKDAT + "' >= efctdat)"
        
        AfaLoggerFunc.tradeInfo(bank_sql)
        
        ret = AfaDBFunc.executeUpdateCmt(bank_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","删除已加入NCS系统的特约汇兑系统行号异常")
        
        AfaLoggerFunc.tradeInfo("结束删除已加入NCS系统的特约汇兑系统行号")
        #================关闭行名行号生效处理系统调度==========================
        AfaLoggerFunc.tradeInfo(">>>开始关闭行名行号生效处理系统调度")
        if not rccpsCronFunc.closeCron("00050"):
            rccpsCronFunc.cronExit("S999","关闭行名行号生效处理系统调度异常")
            
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭行名行号生效处理系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.行名行号生效处理[rccpsHHEffict]退出***")
        
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
            AfaLoggerFunc.tradeInfo("***[rccpsHHEffict]交易中断***")

        sys.exit(-1)
