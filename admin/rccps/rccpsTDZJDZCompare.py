# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.通存通兑主机明细账勾兑
#===============================================================================
#   交易文件:   rccpsTDZJDZCompare.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-11-20
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc
import rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑主机明细账勾兑[rccpsTDZJDZCompare]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT  = mbrifa_dict['NOTE1'][:8]                           #对账日期
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"  #需要对账的中心日期(包括本清算工作日和之前的非清算工作日)
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #===================前置少账==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账前置少账")
        
        temp_sql = "insert into rcc_tdzjcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.scfedt,a.scrbsq,'','',a.sctram,0.00,a.sceydt,a.sctlsq,'51','前置少账','0','','','',''"
        temp_sql = temp_sql + " from rcc_tdzjmx as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT  
        temp_sql = temp_sql + " and not exists ("  
        temp_sql = temp_sql + " select * from rcc_sstlog as b where b.fedt = a.scfedt and b.rbsq = a.scrbsq"  
        temp_sql = temp_sql + " and ((b.bcstat in ('20','70','72') and b.bdwflg = '1' and a.scrvsb = '')"  
        temp_sql = temp_sql + " or (b.bcstat in ('21','81','82') and b.bdwflg = '1' and a.scrvsb != ''))))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账前置少账异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账前置少账")
        
        #===================前置多账==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账前置多账")
        
        temp_sql = "insert into rcc_tdzjcz"
        temp_sql = temp_sql + " (select a.nccwkdat,'','',b.fedt,b.rbsq,0.00,a.occamt,b.trdt,b.tlsq,'52','前置多账','0','','','',''"
        temp_sql = temp_sql + " from rcc_wtrbka as a,rcc_sstlog as b"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and ("
        temp_sql = temp_sql + " (b.bcstat in ('20','70','72') and b.bdwflg = '1' and b.trdt != '' and b.tlsq != '' and not exists(select * from rcc_tdzjmx as c where b.fedt = c.scfedt and b.rbsq = c.scrbsq and c.scrvsb = ''))"
        temp_sql = temp_sql + " or (b.bcstat in ('21','81','82') and b.bdwflg = '1' and b.trdt != '' and b.tlsq != '' and not exists(select * from rcc_tdzjmx as c where b.fedt = c.scfedt and b.rbsq = c.scrbsq and c.scrvsb != ''))))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账前置多账异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账前置多账")
        
        
#        #===================金额不符==============================
#        AfaLoggerFunc.tradeInfo(">>>开始对账金额不符")
#        
#        temp_sql = "insert into rcc_tdzjcz"
#        temp_sql = temp_sql + " (select a.nccwkdat,a.scfedt,a.scrbsq,b.fedt,b.rbsq,a.sctram,case a.scflag when '7' then c.occamt else c.cuschrg end,a.sceydt,a.sctlsq,'53','金额不符','0','','','',''"
#        temp_sql = temp_sql + " from rcc_tdzjmx as a,rcc_sstlog as b,rcc_wtrbka c"            
#        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.scfedt = b.fedt and a.scrbsq = b.rbsq and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
#        temp_sql = temp_sql + " and ((b.bcstat in ('20','70','72') and b.bdwflg = '1' and a.scrvsb = '') or (b.bcstat in ('21','81','82') and b.bdwflg = '1' and a.scrvsb != ''))"
#        #20090512  修改判断金额是否相等的方式
#        #temp_sql = temp_sql + " and ((a.scflag = '7' and a.sctram != c.occamt) or (a.scflag = '8' and a.sctram != c.cuschrg)))"
#        temp_sql = temp_sql + " and ((a.scflag = '7' and abs(a.sctram - c.occamt) > 0.001) or (a.scflag = '8' and abs(a.sctram - c.cuschrg) > 0.001)))"
#        
#        AfaLoggerFunc.tradeInfo(temp_sql)
#        
#        ret = AfaDBFunc.InsertSql(temp_sql)
#        
#        if ret < 0:
#            rccpsCronFunc.cronExit("S999","对账金额不符异常")
#        
#        AfaLoggerFunc.tradeInfo(">>>结束对账金额不符")
        
        
        #================关闭通存通兑主机明细账勾兑系统调度,打开通存通兑主机错账处理系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑主机明细账勾兑系统调度,打开通存通兑主机错账处理系统调度")
        if not rccpsCronFunc.closeCron("00070"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭通存通兑主机明细账勾兑系统调度异常")
            
        if not rccpsCronFunc.openCron("00071"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","打开通存通兑主机错账处理系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑主机明细账勾兑系统调度,打开通存通兑主机错账处理系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑主机明细账勾兑[rccpsTDZJDZCompare]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDZJDZCompare]交易中断***')

        sys.exit(-1)
