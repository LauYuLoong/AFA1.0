# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.通存通兑业务量统计
#===============================================================================
#   交易文件:   rccpsTDProStat.py
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
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑业务量统计[rccpsTDProStat]进入***")
        
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
        
        #==================通存通兑往账统计=========================================
        AfaLoggerFunc.tradeInfo(">>>开始通存通兑往账业务量统计")
        
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,a.besbno,a.trcco,a.brsflg,'','',count(occamt),sum(occamt),'0','','','','',''"
        tmp_sql = tmp_sql + " from rcc_wtrbka as a,rcc_spbsta as b where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn"
        tmp_sql = tmp_sql + " and b.bcstat = '42' and b.bdwflg = '1' and a.brsflg = '" + PL_BRSFLG_SND + "' and a.nccwkdat in " + LNCCWKDAT
        tmp_sql = tmp_sql + " group by a.nccwkdat,a.besbno,a.trcco,a.brsflg)"
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","通存通兑往账业务量统计异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束通存通兑往账业务量统计")
        
        #==================通存通兑来账统计=========================================
        AfaLoggerFunc.tradeInfo(">>>开始通存通兑来账业务量统计")
        
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,a.besbno,a.trcco,a.brsflg,'','',count(occamt),sum(occamt),'0','','','','',''"
        tmp_sql = tmp_sql + " from rcc_wtrbka as a,rcc_spbsta as b where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn"
        tmp_sql = tmp_sql + " and b.bcstat in ('70','72') and b.bdwflg = '1' and a.brsflg = '" + PL_BRSFLG_RCV + "' and a.nccwkdat in " + LNCCWKDAT
        tmp_sql = tmp_sql + " group by a.nccwkdat,a.besbno,a.trcco,a.brsflg)"
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","通存通兑来账业务量统计异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束通存通兑来账业务量统计")
        
        #================关闭通存通兑业务量统计系统调度===========
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑业务量统计系统调度")
        if not rccpsCronFunc.closeCron("00066"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭通存通兑业务量统计调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑业务量统计系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑业务量统计[rccpsTDProStat]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDProStat]交易中断***')

        sys.exit(-1)
