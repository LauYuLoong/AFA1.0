# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.通存通兑对账错账处理
#===============================================================================
#   交易文件:   rccpsTDZJDZModify.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-12-12
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc,time
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_tdzjcz

if __name__ == '__main__':
    
    try:
        rccpsCronFunc.WrtLog("***农信银系统: 系统调度类.通存通兑对账错账处理[rccpstdzjczModify]进入***")
        
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
        
        #对前置少账类型中,前置存在此状态但流转处理标识非成功的,更新流转处理标识为成功,并更新主机日期,主机流水号
        tdzjcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and errtyp = '51' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        tdzjcz_list = rccpsDBTrcc_tdzjcz.selectm(1,0,tdzjcz_where_sql,"")
        
        if tdzjcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(tdzjcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
            
        else:
            AfaLoggerFunc.tradeInfo("更新流转处理标识为成功,并更新主机日期,主机流水号")
            for i in xrange(len(tdzjcz_list)):
                AfaLoggerFunc.tradeInfo("开始更新流转处理标识为成功")
                
                #========更新交易状态流转处理标识为成功========================
                #关彬捷 20090223  增加记账超时,返回拒绝,但实际主机记账成功的处理
                
                where_sql = "select a.bjedte,a.bspsqn,a.bcstat,a.bdwflg from rcc_spbsta as a,rcc_sstlog as b,rcc_tdzjcz as c "
                where_sql = where_sql + " where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.bcursq = b.bcursq"
                where_sql = where_sql + " and ((b.bcstat in ('20','21','70','72','81','82') and b.bdwflg != '1') or (b.bcstat = '40'))"
                where_sql = where_sql + " and b.fedt = c.scfedt and b.rbsq = c.scrbsq"
                where_sql = where_sql + " and b.fedt = '" + tdzjcz_list[i]['SCFEDT'] + "' and b.rbsq = '" + tdzjcz_list[i]['SCRBSQ'] + "'"
                
                tmp_list = AfaDBFunc.SelectSql(where_sql)
                
                if tmp_list == None:
                    AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","查询可以更新流转处理标识的交易报单日期和报单序号异常")
                
                elif len(tmp_list) <= 0:
                    AfaLoggerFunc.tradeInfo("无可以更新流转处理标识的交易")
                    continue
                
                else:
                    stat_dict = {}
                    stat_dict['BJEDTE'] = tmp_list[0][0]
                    stat_dict['BSPSQN'] = tmp_list[0][1]
                    if tmp_list[0][2] == '40':
                        stat_dict['BCSTAT'] = '72'
                    else:
                        stat_dict['BCSTAT'] = tmp_list[0][2]
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    stat_dict['TRDT']   = tdzjcz_list[i]['SCTRDT']
                    stat_dict['TLSQ']   = tdzjcz_list[i]['SCTLSQ']
                    
                    if not rccpsState.setTransState(stat_dict):
                        rccpsCronFunc.cronExit('S999', '设置状态异常')
                
                AfaLoggerFunc.tradeInfo("结束更新流转处理标识为成功")
                
                #========修改错账处理标识为已处理==============================
                AfaLoggerFunc.tradeInfo("开始修改错账处理标识为已处理")
                
                tdzjcz_update_sql = "update rcc_tdzjcz set isdeal = '1'"
                tdzjcz_update_sql = tdzjcz_update_sql + " where errtyp = '51' and scfedt = '" + tdzjcz_list[i]['SCFEDT'] + "' and scrbsq = '" + tdzjcz_list[i]['SCRBSQ'] + "'"
                
                ret = AfaDBFunc.UpdateSqlCmt(tdzjcz_update_sql)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
                    
                AfaLoggerFunc.tradeInfo("结束修改错账处理标识为已处理")
        
        #================关闭通存通兑对账汇兑对账错账处理系统调度,打开通存通兑对账明细账勾兑系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭通存通兑对账汇兑对账错账处理系统调度,打开通存通兑对账明细账勾兑系统调度")
        if not rccpsCronFunc.closeCron("00071"):
            rccpsCronFunc.cronExit("S999","关闭通存通兑对账错账处理系统调度异常")
        
        if not rccpsCronFunc.openCron("00063"):
            rccpsCronFunc.cronExit("S999","打开通存通兑对账明细账勾兑系统调度异常")
                
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭通存通兑对账汇兑对账错账处理系统调度,打开通存通兑对账明细账勾兑系统调度")
        
        rccpsCronFunc.WrtLog("***农信银系统: 系统调度类.通存通兑对账错账处理[rccpstdzjczModify]退出***")
    
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
            rccpsCronFunc.WrtLog('***[rccpstdzjczModify]交易中断***')

        sys.exit(-1)
