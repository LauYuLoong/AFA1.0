# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.汇兑对账明细账勾兑
#===============================================================================
#   交易文件:   rccpsHDDZMXCompare.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-27
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
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇兑对账明细账勾兑[rccpsHDDZMXCompare]进入***")
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
            
        NCCWKDAT  = mbrifa_dict['NOTE1'][:8]                           #对账日期
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"  #需要对账的中心日期(包括本清算工作日和之前的非清算工作日)
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #===================往账行内有,中心无====================================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账行内有,中心无类型")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz (select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'01','往账行内有,中心无','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.nccwkdat in " + LNCCWKDAT + " and b.bcstat = '42' and a.brsflg = '0' and not exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno ))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账行内有,中心无类型异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账往账行内有,中心无类型")
        
        #===================往账行内无,中心有====================================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账行内无,中心有类型")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'02','往账行内无,中心有','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_hddzmx as a where a.sndmbrco = '1340000008' and a.bjedte = '' and a.bspsqn = '' and a.nccwkdat in " + LNCCWKDAT +  ")"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账行内无,中心有类型异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账往账行内无,中心有类型")
        
        #===================往账行内清算,中心未清算==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账行内已记账,中心未清算类型")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'03','往账行内已记账,中心未清算','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and b.bcstat = '21' and b.bdwflg = '2' and a.brsflg = '0' and a.nccwkdat = '" + NCCWKDAT + "' and not exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账行内已记账,中心未清算类型异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账往账行内已记账,中心未清算类型")
        
        #===================往账行内未清算,中心清算==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账行内未清算,中心清算类型")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'04','往账行内未清算,中心清算','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and not (b.bcstat = '42' and b.bdwflg = '1') and a.brsflg = '0' and a.nccwkdat in " + LNCCWKDAT + " and exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账行内未清算,中心清算类型异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账往账行内未清算,中心清算类型")
        
        #===================来账行内有,中心无====================================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账行内有,中心无类型")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'05','来账行内有,中心无','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.brsflg = '1' and b.bcstat in ('70','71','80') and b.bdwflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and not exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账行内有,中心无类型异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账行内有,中心无类型")
        
        #===================来账行内无,中心有====================================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账行内无,中心有类型")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'06','来账行内无,中心有','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_hddzmx as a "
        temp_sql = temp_sql + "where a.sndmbrco != '1340000008' and a.bjedte = '' and a.bspsqn = '' and a.nccwkdat in " + LNCCWKDAT + ")"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账行内无,中心有类型异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账行内无,中心有类型")
        
        #===================来账行内清算,中心未清算==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账行内清算,中心未清算类型")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'07','来账行内清算,中心未清算','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and b.bcstat in ('70','71','80') and b.bdwflg = '1' and a.brsflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and not exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账行内清算,中心未清算类型异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账行内清算,中心未清算类型")
        
        #===================来账行内未清算,中心清算==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账行内未清算,中心清算类型")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'08','来账行内未清算,中心清算','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and not (b.bcstat in ('70','71','80') and b.bdwflg = '1') and a.brsflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账行内未清算,中心清算类型异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账行内未清算,中心清算类型")
        
        #================关闭汇兑对账明细账勾兑系统调度,打开汇兑对账错账处理系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭汇兑对账明细账勾兑系统调度,打开汇兑对账错账处理系统调度")
        if not rccpsCronFunc.closeCron("00033"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭汇兑对账明细账勾兑系统调度异常")
            
        if not rccpsCronFunc.openCron("00030"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","打开汇兑对账错账处理系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭汇兑对账明细账勾兑系统调度,打开汇兑对账错账处理系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇兑对账明细账勾兑[rccpsHDDZMXCompare]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHDDZMXCompare]交易中断***')

        sys.exit(-1)