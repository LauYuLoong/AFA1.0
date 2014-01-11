# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.通存通兑对账明细账勾兑
#===============================================================================
#   交易文件:   rccpsTDDZMXCompare.py
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
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑对账明细账勾兑[rccpsTDDZMXCompare]进入***")
        
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
        
        #===================往账,行内已记账且未抹账,中心无==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账,行内已记账且未抹账,中心无")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,case a.dcflg when '1' then '0' else '1' end,a.pyracc,a.pyeacc,'CNY',a.occamt,a.occamt,case when a.chrgtyp='1' and a.trcco in ('3000102','3000103','3000104','3000105') then a.cuschrg else 0.00 end case,case when a.chrgtyp='1' and a.trcco in ('3000102','3000103','3000104','3000105') then a.cuschrg else 0.00 end case,'',a.bjedte,a.bspsqn,'01','中心无成员行有','01','往账,行内已记账且未抹账,中心无','0','','','',''"
        temp_sql = temp_sql + " from rcc_wtrbka as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.brsflg = '0'"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select * from rcc_tddzmx as b"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno)"
        temp_sql = temp_sql + " and exists"
        temp_sql = temp_sql + " (select * "
        temp_sql = temp_sql + " from rcc_sstlog as c"
        temp_sql = temp_sql + " where a.bjedte = c.bjedte and a.bspsqn = c.bspsqn and c.bcstat = '20' and c.bdwflg = '1')"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select *"
        temp_sql = temp_sql + " from rcc_sstlog as d"
        temp_sql = temp_sql + " where a.bjedte = d.bjedte and a.bspsqn = d.bspsqn and d.bcstat in ('21','81','82') and d.bdwflg = '1'))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账,行内已记账且未抹账,中心无异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账往账,行内已记账且未抹账,中心无")
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #===================往账,中心有,行内无==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账,中心有,行内无")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,a.occamt,a.cuschrg,a.cuschrg,a.ortrcno,'','','02','中心有成员行无','02','往账,中心有,行内无','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.sndmbrco = '1340000008' and not exists" 
        temp_sql = temp_sql + " (select * from rcc_wtrbka as b"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账,中心有,行内无异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账往账,中心有,行内无")
        
        #===================往账,中心清算,行内未清算==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账,中心清算,行内未清算")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'02','中心有成员行无','03','往账中心清算,行内未清算','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.sndmbrco = '1340000008' and (c.bcstat != '42' or c.bdwflg != '1')"
        temp_sql = temp_sql + " and ((a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '1') or (a.trcco in ('3000102','3000103','3000104','3000105') and a.confflg = '0')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账,中心清算,行内未清算异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账往账,中心清算,行内未清算")
        
        #===================往账,中心冲销,行内未冲销==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账,中心冲销,行内未冲销")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'01','中心无成员行有','04','往账中心冲销,行内未冲销','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '1' and a.sndmbrco = '1340000008' and not (c.bcstat = '81' and c.bdwflg = '1')"
        temp_sql = temp_sql + " and ((a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '1') or (a.trcco in ('3000102','3000103','3000104','3000105') and a.confflg = '0')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账,中心冲销,行内未冲销异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账往账,中心冲销,行内未冲销")
        
        
        #===================往账,通存业务,行内已记账且未抹账,中心未确认==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账往账,通存业务,行内已记账且未抹账,中心未确认")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'03','补确认','05','往账,通存,行内已记账且未抹账,中心未确认','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.sndmbrco = '1340000008'"
        temp_sql = temp_sql + " and a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '0'"

        ##########################################################################
        #guanbj 20091012 补确认错账只包含记账且未抹账的交易
        temp_sql = temp_sql + " and exists"
        temp_sql = temp_sql + " (select * "
        temp_sql = temp_sql + " from rcc_sstlog as d"
        temp_sql = temp_sql + " where c.bjedte = d.bjedte and c.bspsqn = d.bspsqn and d.bcstat = '20' and d.bdwflg = '1')"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select *"
        temp_sql = temp_sql + " from rcc_sstlog as e"
        temp_sql = temp_sql + " where c.bjedte = e.bjedte and c.bspsqn = e.bspsqn and e.bcstat in ('21','81','82') and e.bdwflg = '1'))"
        ##########################################################################
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账,通存业务,行内已记账且未抹账,中心未确认异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束往账,通存业务,行内已记账且未抹账,中心未确认")
        
        #===================往账,通存,行内未记账,中心有但未确认=========================
        #关彬捷 20091014 将中心未确认,行内未记账的错账归为中心有行内无错账类型
        AfaLoggerFunc.tradeInfo(">>>开始往账,通存,行内未记账,中心有但未确认")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'02','中心有成员行无','11','往账,通存,行内未记账,中心有但未确认','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.sndmbrco = '1340000008'"
        temp_sql = temp_sql + " and a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '0'"
        temp_sql = temp_sql + " and not (exists"
        temp_sql = temp_sql + " (select * "
        temp_sql = temp_sql + " from rcc_sstlog as d"
        temp_sql = temp_sql + " where c.bjedte = d.bjedte and c.bspsqn = d.bspsqn and d.bcstat = '20' and d.bdwflg = '1')"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select *"
        temp_sql = temp_sql + " from rcc_sstlog as e"
        temp_sql = temp_sql + " where c.bjedte = e.bjedte and c.bspsqn = e.bspsqn and e.bcstat in ('21','81','82') and e.bdwflg = '1')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账往账,通存业务,行内未记账,中心有但未确认")
        
        AfaLoggerFunc.tradeInfo(">>>结束往账,通存,行内未记账,中心有但未确认")
        
        #===================来账,行内已记账且未抹账,中心无==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账,行内已记账且未抹账,中心无")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,case a.dcflg when '1' then '0' else '1' end,a.pyracc,a.pyeacc,'CNY',a.occamt,a.occamt,case when a.chrgtyp='1'and a.trcco in ('3000102','3000103','3000104','3000105') then a.cuschrg else 0.00 end case,case when a.chrgtyp='1'and a.trcco in ('3000102','3000103','3000104','3000105') then a.cuschrg else 0.00 end case,'',a.bjedte,a.bspsqn,'01','中心无成员行有','06','来账,行内已记账且未抹账,中心无','0','','','',''"
        temp_sql = temp_sql + " from rcc_wtrbka as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.brsflg = '1'"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select * from rcc_tddzmx as b"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno)"
        temp_sql = temp_sql + " and exists"
        temp_sql = temp_sql + " (select * from rcc_sstlog as c"
        temp_sql = temp_sql + " where a.bjedte = c.bjedte and a.bspsqn = c.bspsqn and c.bcstat in ('70','72') and c.bdwflg = '1')"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select * from rcc_sstlog as d"
        temp_sql = temp_sql + " where a.bjedte = d.bjedte and a.bspsqn = d.bspsqn and d.bcstat in ('21','81','82') and d.bdwflg = '1'))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账,行内已记账且未抹账,中心无异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账,行内已记账且未抹账,中心无")
        
        #===================来账,中心有,行内无==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账,中心有,行内无")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,a.occamt,a.cuschrg,a.cuschrg,a.ortrcno,'','','02','中心有成员行无','07','来账,中心有,行内无','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.sndmbrco != '1340000008' and not exists"
        temp_sql = temp_sql + " (select * from rcc_wtrbka as b"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账,中心有,行内无异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账,中心有,行内无")
        
        #===================来账,中心清算,行内未清算==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账,中心清算,行内未清算")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'02','中心有成员行无','08','来账中心清算,行内未清算','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"                                                                        
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.rcvmbrco = '1340000008' and not ((c.bcstat in ('70','72')) and c.bdwflg = '1')"
        temp_sql = temp_sql + " and ((a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '1') or (a.trcco in ('3000102','3000103','3000104','3000105') and a.confflg = '0')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账,中心清算,行内未清算异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账,中心清算,行内未清算")
        
        #===================来账,中心冲销,行内未冲销==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账,中心冲销,行内未冲销")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'01','中心无成员行有','09','来账中心冲销,行内未冲销','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '1' and a.rcvmbrco = '1340000008' and not (c.bcstat = '81' and c.bdwflg = '1')"
        temp_sql = temp_sql + " and ((a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '1') or (a.trcco in ('3000102','3000103','3000104','3000105') and a.confflg = '0')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账,中心冲销,行内未冲销异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账,中心冲销,行内未冲销")
        
        #===================来账,通存业务,中心未确认==============================
        AfaLoggerFunc.tradeInfo(">>>开始对账来账,通存业务,中心未确认")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'04','查确认','10','来账,通存,中心未确认','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.rcvmbrco = '1340000008'"
        temp_sql = temp_sql + " and a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '0')"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","对账来账,通存业务,中心未确认异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束对账来账,通存业务,中心未确认")
        
        
        
        #================关闭通存通兑对账明细账勾兑系统调度,打开通存通兑对账差错文件上传系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑对账明细账勾兑系统调度,打开通存通兑对账错账处理系统调度")
        if not rccpsCronFunc.closeCron("00063"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","关闭通存通兑对账明细账勾兑系统调度异常")
            
        if not rccpsCronFunc.openCron("00060"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","打开通存通兑对账差错文件上传系统调度异常")
            
        if not rccpsCronFunc.openCron("00065"):
            rccpsCronFunc.cronExit("S999","打开通存通兑结转文件生成及发送到主机调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑对账明细账勾兑系统调度,打开通存通兑对账差错文件上传系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.通存通兑对账明细账勾兑[rccpsTDDZMXCompare]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDDZMXCompare]交易中断***')

        sys.exit(-1)
