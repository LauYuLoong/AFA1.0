# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.汇票业务量统计
#===============================================================================
#   交易文件:   rccpsHPProStat.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-07-03
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,AfaDBFunc,rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇票业务量统计[rccpsHPProStat]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        LNCCWKDAT = "('" + mbrifa_dict['NOTE4'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #==================汇票往账统计=========================================
        AfaLoggerFunc.tradeInfo(">>>开始汇票往账业务量统计")
        
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_SND + "',b.btopsb,b.beacsb,count(a.occamt),sum(a.occamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hpdzmx a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","汇票往账业务量统计异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束汇票往账业务量统计")
        
        #==================汇票来账统计=========================================
        AfaLoggerFunc.tradeInfo(">>>开始汇票来账业务量统计")
        
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,case when b.besbno is null then '3400008889' else b.besbno end,a.trcco,'" + PL_BRSFLG_RCV + "',case when b.btopsb is null then '3400008889' else b.btopsb end,case when b.beacsb is null then '3400008889' else b.beacsb end,count(a.occamt),sum(a.occamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hpdzmx a left join rcc_subbra b on a.rcvbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.rcvmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","汇票来账业务量统计异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束汇票来账业务量统计")
        
        #================关闭汇票业务量统计系统调度===========
        AfaLoggerFunc.tradeInfo(">>>开始关闭汇票业务量统计系统调度")
        if not rccpsCronFunc.closeCron("00046"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭汇票业务量统计调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭汇票业务量统计系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇票业务量统计[rccpsHPProStat]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHPProStat]交易中断***')

        sys.exit(-1)
