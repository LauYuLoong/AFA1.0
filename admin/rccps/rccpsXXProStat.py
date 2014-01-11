# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.查询查复业务量信息统计
#===============================================================================
#   交易文件:   rccpsXXProStat.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  潘广通
#   修改时间:   2008-12-06
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,AfaDBFunc,rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.查询查复业务量信息统计[rccpsXXProStat]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #==================查询查复往账统计=========================================
        AfaLoggerFunc.tradeInfo(">>>开始查询查复往账业务量统计")
        #=====汇兑查询查复往账====
        AfaLoggerFunc.tradeInfo(">>>开始汇兑查询查复往账业务量统计")
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_SND + "',b.btopsb,b.beacsb,count(a.occamt),sum(a.occamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hdcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询查复往账业务量统计异常")
        AfaLoggerFunc.tradeInfo(">>>结束汇兑查询查复往账业务量统计")
        
        #=====汇票查询查复往账====
        AfaLoggerFunc.tradeInfo(">>>开始汇票查询查复往账业务量统计")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_SND + "',b.btopsb,b.beacsb,count(a.bilamt),sum(a.bilamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hpcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询查复往账业务量统计异常")
        AfaLoggerFunc.tradeInfo(">>>结束汇票查询查复往账业务量统计")  
        
        #=====票据查询查复往账====
        AfaLoggerFunc.tradeInfo(">>>开始票据查询查复往账业务量统计")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_SND + "',b.btopsb,b.beacsb,count(a.bilamt),sum(a.bilamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_pjcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询查复往账业务量统计异常")
        AfaLoggerFunc.tradeInfo(">>>结束票据查询查复往账业务量统计")    
        
        AfaLoggerFunc.tradeInfo(">>>结束查询查复往账业务量统计")
        
        #==================查询查复来账统计=========================================
        AfaLoggerFunc.tradeInfo(">>>开始查询查复来账业务量统计")
        
        #=====汇兑查询查复来账====
        AfaLoggerFunc.tradeInfo(">>>开始汇兑查询查复来账业务量统计")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_RCV + "',b.btopsb,b.beacsb,count(a.occamt),sum(a.occamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hdcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询查复来账业务量统计异常")
        AfaLoggerFunc.tradeInfo(">>>结束汇兑查询查复来账业务量统计")    
        
        #=====汇票查询查复来账====
        AfaLoggerFunc.tradeInfo(">>>开始汇票查询查复来账业务量统计")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_RCV + "',b.btopsb,b.beacsb,count(a.bilamt),sum(a.bilamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hpcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询查复来账业务量统计异常")
        AfaLoggerFunc.tradeInfo(">>>结束汇票查询查复来账业务量统计")    
        
        #=====票据查询查复来账====
        AfaLoggerFunc.tradeInfo(">>>开始票据查询查复来账业务量统计")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_RCV + "',b.btopsb,b.beacsb,count(a.bilamt),sum(a.bilamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_pjcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询查复来账业务量统计异常")
        AfaLoggerFunc.tradeInfo(">>>结束票据查询查复来账业务量统计")    
        
        AfaLoggerFunc.tradeInfo(">>>结束查询查复来账业务量统计")
        
        #================关闭查询查复业务量信息统计系统调度===========
        AfaLoggerFunc.tradeInfo(">>>开始关闭查询查复业务量信息统计系统调度")
        if not rccpsCronFunc.closeCron("00067"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭查询查复业务量信息统计调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭查询查复业务量信息统计系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.查询查复业务量信息统计[rccpsXXProStat]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsXXProStat]交易中断***')

        sys.exit(-1)
