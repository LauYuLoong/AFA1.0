# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.汇票对账错账处理
#===============================================================================
#   交易文件:   rccpsHPDZCZModify.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-27
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc,time
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc,rccpsHostFunc,rccpsFunc,rccpsGetFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hpdzcz,rccpsDBTrcc_sstlog,rccpsDBTrcc_bilbka,rccpsDBTrcc_hpdzmx
import rccpsMap0000Dhpdzmx2CTradeContext,rccpsMap0000Dbilbka2CTradeContext,rccpsMap0000Dbilinf2CTradeContext,rccpsMap1113CTradeContext2Dbilbka


if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇票对账错账处理[rccpsHPDZCZModify]进入***")
        
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
        
        #================往账行内有,中心无======================================
        AfaLoggerFunc.tradeInfo(">>>开始处理往账行内有,中心无类型")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '01' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型账务处理由主机方调账,本系统设置交易状态为抹账成功,成功后修改错账处理标识为已处理")
            
            for i in xrange(len(hpdzcz_list)):
                #========设置状态为长款=========================================
                AfaLoggerFunc.tradeInfo("开始修改原交易状态为长款")
                
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========设置交易状态为长款成功=================================
                if not rccpsState.newTransState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_LONG,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '设置长款成功状态异常')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                AfaLoggerFunc.tradeInfo("结束修改原交易状态为长款")
                
                #========修改错账处理标识为已处理===============================
                hpdzcz_update_dict = {}
                hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hpdzcz_where_dict = {}
                hpdzcz_where_dict['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                hpdzcz_where_dict['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                
                ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理往账行内有,中心无类型")
        
        #================往账行内无,中心有======================================
        AfaLoggerFunc.tradeInfo(">>>开始处理往账行内无,中心有类型")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '02' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型为系统异常,需科技人员查实后处理")
            #for i in xrange(len(hpdzcz_list)):
            #    hpdzcz_update_dict = {}
            #    hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hpdzcz_where_dict = {}
            #    hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
            #    hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
            #    hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
            #    
            #    ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理往账行内无,中心有类型")
        
        #================往账行内清算,中心未清算================================
        AfaLoggerFunc.tradeInfo(">>>开始处理往账行内清算,中心未清算类型")
        
        hpdzcz_where_sql = "nccwkdat = '" + NCCWKDAT + "' and eactyp = '03' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型为系统异常,需科技人员查实后处理")
            for i in xrange(len(hpdzcz_list)):
                #========设置状态为长款=========================================
                AfaLoggerFunc.tradeInfo("开始修改原交易状态为长款")
                
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========设置交易状态为长款成功=================================
                if not rccpsState.newTransState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_LONG,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '设置长款成功状态异常')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                AfaLoggerFunc.tradeInfo("结束修改原交易状态为长款")
                
                #========修改错账处理标识为已处理===============================
                hpdzcz_update_dict = {}
                hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hpdzcz_where_dict = {}
                hpdzcz_where_dict['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                hpdzcz_where_dict['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                
                ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理往账行内清算,中心未清算类型")
        
        #================往账行内未清算,中心清算================================
        AfaLoggerFunc.tradeInfo(">>>开始处理往账行内未清算,中心清算类型")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '04' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型账务处理由主机方处理,本系统设置交易状态为清算\短款成功,成功后修改错账处理标识为已处理")
            
            for i in xrange(len(hpdzcz_list)):
                tmp_stat_where_dict = {}
                tmp_stat_where_dict['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                tmp_stat_where_dict['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                tmp_stat_where_dict['BCSTAT'] = PL_BCSTAT_ACC
                tmp_stat_where_dict['BDWFLG'] = PL_BDWFLG_SUCC
                
                tmp_stat_dict = {}
                tmp_stat_dict = rccpsDBTrcc_sstlog.selectu(tmp_stat_where_dict)
                
                if tmp_stat_dict == None:
                    AfaCronFunc.cronExit('S999','查询交易记账状态异常')
                #if not rccpsState.getTransStateSet(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,tmp_stat_dict):
                HPSTAT = ''
                if hpdzcz_list[i]['TRCCO'] == '2100001':
                    #汇票签发
                    HPSTAT = PL_HPSTAT_SIGN
                elif hpdzcz_list[i]['TRCCO'] == '2100100':
                    #汇票解付
                    HPSTAT = PL_HPSTAT_PAYC
                elif hpdzcz_list[i]['TRCCO'] == '2100101':
                    #汇票撤销
                    HPSTAT = PL_HPSTAT_CANC
                elif hpdzcz_list[i]['TRCCO'] == '2100102':
                    #汇票挂失
                    HPSTAT = PL_HPSTAT_HANG
                elif hpdzcz_list[i]['TRCCO'] == '2100103':
                    #汇票退票
                    HPSTAT = PL_HPSTAT_RETN
                elif hpdzcz_list[i]['TRCCO'] == '2100104':
                    #汇票解挂
                    HPSTAT = PL_HPSTAT_DEHG
                
                #业务状态无记账状态而且非汇票挂失和汇票解挂交易
                if len(tmp_stat_dict) <= 0 and hpdzcz_list[i]['TRCCO'] != '2100102' and hpdzcz_list[i]['TRCCO'] != '2100104':
                    AfaLoggerFunc.tradeInfo("此交易非汇票挂失\解挂交易,且未记账成功")
                    AfaLoggerFunc.tradeInfo("设短款")
                    #========设短款============================================
                    TradeContext.BESBNO = PL_BESBNO_BCLRSB
                    TradeContext.BETELR = PL_BETELR_AUTO
                    
                    AfaLoggerFunc.tradeInfo(">>>开始设置短款处理中状态")
                    
                    #========设置交易状态为短款处理中==========================
                    if not rccpsState.newTransState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_SHORT,PL_BDWFLG_WAIT):
                        rccpsCronFunc.cronExit('S999', '设置短款处理中状态异常')
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置短款处理中状态")
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                        rccCronFunc.cronExit("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态")
                    
                    if not rccpsState.newBilState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],HPSTAT):
                        rccpsCronFunc.cronExit('S999', '设置汇票状态异常')
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态")
                    
                    AfaLoggerFunc.tradeInfo(">>>开始设置短款成功状态")
                    
                    tmp_stat = {}
                    tmp_stat['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                    tmp_stat['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                    
                    tmptrc_dict = {}
                    if not rccpsDBFunc.getTransBil(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],tmptrc_dict):
                        rccpsCronFunc.cronExit('S999', '查询汇票交易业务信息异常')
                    
                    if not rccpsDBFunc.getInfoBil(tmptrc_dict['BILVER'],tmptrc_dict['BILNO'],tmptrc_dict['BILRS'],tmptrc_dict):
                        rccpsCronFunc.cronExit('S999', '查询汇票信息异常')
                        
                    TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_NXYDQSWZ  #借农信银待清算往账
                    TradeContext.ACNM     = "农信银待清算往账"
                    TradeContext.RBAC     = tmptrc_dict['PYHACC']                     #贷持票人账号
                    TradeContext.OTNM     = tmptrc_dict['PYHNAM']
                    
                    #=====开始调函数拼贷方账号第25位校验位====
                    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                    
                    tmp_stat['BCSTAT'] = PL_BCSTAT_SHORT
                    tmp_stat['BDWFLG'] = PL_BDWFLG_SUCC
                    
                    if not rccpsState.setTransState(tmp_stat):
                        rccpsCronFunc.cronExit('S999', '设置短款成功状态异常')
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置短款成功状态")
                    
                else:
                    AfaLoggerFunc.tradeInfo("补清算")
                    #========补清算============================================
                    TradeContext.BESBNO = PL_BESBNO_BCLRSB
                    TradeContext.BETELR = PL_BETELR_AUTO
                    
                    #========设置交易状态为清算处理中==========================
                    AfaLoggerFunc.tradeInfo("开始设置清算处理中状态")
                    
                    if not rccpsState.newTransState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_SUCC):
                        rccpsCronFunc.cronExit('S999', '设置清算处理中状态异常')
                    
                    AfaLoggerFunc.tradeInfo("结束设置清算处理中状态")
                    
                    #COMMIT
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                        rccCronFunc.cronExit("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    AfaLoggerFunc.tradeInfo(">>>开始设置汇票状态")
                    
                    if not rccpsState.newBilState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],HPSTAT):
                        rccpsCronFunc.cronExit('S999', '设置汇票状态异常')
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置汇票状态")
                    
                    AfaLoggerFunc.tradeInfo(">>>开始设置清算成功状态")
                    
                    tmp_stat = {}
                    tmp_stat['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                    tmp_stat['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                    tmp_stat['BCSTAT'] = PL_BCSTAT_MFESTL
                    tmp_stat['BDWFLG'] = PL_BDWFLG_SUCC
                    
                    if not rccpsState.setTransState(tmp_stat):
                        rccpsCronFunc.cronExit('S999', '设置清算成功状态异常')
                    
                    AfaLoggerFunc.tradeInfo(">>>结束设置清算成功状态")
                    
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                #========修改错账处理标识为已处理==============================
                hpdzcz_update_dict = {}
                hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hpdzcz_where_dict = {}
                hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                
                ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理往账行内未清算,中心清算类型")
        
        #================来账行内有,中心无=====================================
        AfaLoggerFunc.tradeInfo(">>>开始处理来账行内有,中心无类型")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '05' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型为系统异常,需科技人员查实后处理")
            #for i in xrange(len(hpdzcz_list)):
            #    hpdzcz_update_dict = {}
            #    hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hpdzcz_where_dict = {}
            #    hpdzcz_where_dict['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
            #    hpdzcz_where_dict['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
            #    
            #    ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理来账行内有,中心无类型")
        #================来账行内无,中心有=====================================
        AfaLoggerFunc.tradeInfo(">>>开始处理来账行内无,中心有类型")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '06' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("查询此错账类型相关记录异常")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型需补来账,成功后修改错账处理标识为已处理")
            for i in xrange(len(hpdzcz_list)):
                #========补来账================================================
                AfaLoggerFunc.tradeInfo(">>>开始补来账")
                
                #========初始化来账上下文======================================
                AfaLoggerFunc.tradeInfo(">>>开始初始化上下文")
                TradeContext.tradeResponse=[]
                
                hpdzmx_where_dict = {}
                hpdzmx_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                hpdzmx_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                hpdzmx_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                
                hpdzmx_dict = rccpsDBTrcc_hpdzmx.selectu(hpdzmx_where_dict)
                
                if hpdzmx_dict == None:
                    rccpsCronFunc.cronExit("S999","查询来账明细数据异常")
                    
                if len(hpdzmx_dict) <= 0:
                    rccpsCronFunc.cronExit("S999","登记簿中无此来账明细数据")
                
                rccpsMap0000Dhpdzmx2CTradeContext.map(hpdzmx_dict)
                
                TradeContext.OCCAMT = str(TradeContext.OCCAMT)
                TradeContext.TemplateCode  = 'RCC005'
                TradeContext.BRSFLG        = PL_BRSFLG_RCV
                TradeContext.CUR           = '01'
                TradeContext.BILRS         = '0' 
                TradeContext.TransCode = '1113'
                TradeContext.OPRNO     = PL_HPOPRNO_JF
                
                #=====================获取系统日期时间=========================
                TradeContext.BJEDTE = AfaUtilTools.GetHostDate( )
                #TradeContext.TRCDAT = AfaUtilTools.GetHostDate( )
                TradeContext.BJETIM = AfaUtilTools.GetSysTime( )
                #TradeContext.BJEDTE = PL_BJEDTE     #测试,暂时使用
                #TradeContext.TRCDAT = PL_BJEDTE     #测试,暂时使用
                
                #=====================系统公共校验=============================
                if not rccpsFunc.ChkPubInfo(PL_BRSFLG_RCV) :
                    raise Exception
                    
                #=====================机构合法性校验===========================
                if not rccpsFunc.ChkUnitInfo( PL_BRSFLG_RCV ) :
                    raise Exception
                
                #=====================获取中心日期=============================
                TradeContext.NCCworkDate = TradeContext.NCCWKDAT
                
                #=====================获取平台流水号===========================
                if rccpsGetFunc.GetSerialno(PL_BRSFLG_RCV) == -1 :
                    raise Exception
                
                #=====================获取中心流水号===========================
                if rccpsGetFunc.GetRccSerialno( ) == -1 :
                    raise Exception
                
                AfaLoggerFunc.tradeInfo(">>>结束初始化上下文")
                
                #=====================登记来账信息=============================
                AfaLoggerFunc.tradeInfo(">>>开始登记来账信息")
                
                #=====================币种转换=================================
                if TradeContext.CUR == 'CNY':
                    TradeContext.CUR  = '01'
                
                #=====================开始向字典赋值===========================
                bilbka_dict = {}
                if not rccpsMap1113CTradeContext2Dbilbka.map(bilbka_dict):
                    rccpsCronFunc.cronExit('M999', '字典赋值出错')
                
                bilbka_dict['DCFLG'] = PL_DCFLG_CRE                  #借贷标识
                bilbka_dict['OPRNO'] = TradeContext.OPRNO            #业务属性
                
                #=====================开始插入数据库===========================
                if not rccpsDBFunc.insTransBil(bilbka_dict):
                    rccpsCronFunc.cronExit('D002', '插入数据库异常')
                    
                #=====================commit操作===============================
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    rccpsCronFunc.cronExit("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                AfaLoggerFunc.tradeInfo('插入汇兑业务登记簿成功')
                
                #=====================设置状态为收妥===========================
                sstlog   = {}
                sstlog['BSPSQN']   = TradeContext.BSPSQN
                sstlog['BJEDTE']   = TradeContext.BJEDTE
                sstlog['BCSTAT']   = PL_BCSTAT_BNKRCV
                sstlog['BDWFLG']   = PL_BDWFLG_SUCC
                
                #=====================设置状态为 收妥-成功=====================
                if not rccpsState.setTransState(sstlog):
                    rccpsCronFunc.cronExit(TradeContext.errorCode, TradeContext.errorMsg)
                    
                #=====================commit操作===============================
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    rccpsCronFunc.cronExit("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                AfaLoggerFunc.tradeInfo(">>>结束登记来账信息")
                
                AfaLoggerFunc.tradeInfo(">>>结束补来账")
                
                #========更新汇票对账明细登记簿================================
                AfaLoggerFunc.tradeInfo(">>>开始更新汇兑明细登记簿")
                
                hpdzmx_where_dict = {}
                hpdzmx_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                hpdzmx_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                hpdzmx_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                
                stat_dict = {}
                if not rccpsState.getTransStateCur(TradeContext.BJEDTE,TradeContext.BSPSQN,stat_dict):
                    rccpsCronFunc.cronExit(TradeContext.errorCode,TradeContext.errorMsg)
                
                hpdzmx_update_dict = {}
                hpdzmx_update_dict['BJEDTE'] = TradeContext.BJEDTE
                hpdzmx_update_dict['BSPSQN'] = TradeContext.BSPSQN
                hpdzmx_update_dict['BCSTAT'] = stat_dict['BCSTAT']
                hpdzmx_update_dict['BDWFLG'] = stat_dict['BDWFLG']
                
                ret = rccpsDBTrcc_hpdzmx.updateCmt(hpdzmx_update_dict,hpdzmx_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","登记汇兑对账明细登记簿交易行内信息异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束更新汇兑明细登记簿")
                
                #========修改错账类型为行内未记账,中心清算=====================
                hpdzcz_update_dict = {}
                hpdzcz_update_dict['EACTYP'] = '08'
                hpdzcz_update_dict['EACINF'] = '来账行内未记账,中心清算'
                hpdzcz_update_dict['BJEDTE'] = TradeContext.BJEDTE
                hpdzcz_update_dict['BSPSQN'] = TradeContext.BSPSQN
                
                hpdzcz_where_dict = {}
                hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                
                ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","修改汇兑对账错账登记簿处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理来账行内无,中心有类型")
        #================来账行内记账,中心未清算===============================
        AfaLoggerFunc.tradeInfo(">>>开始处理来账行内记账,中心未清算类型")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '07' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型为系统异常,需科技人员查实后处理")
            #for i in xrange(len(hpdzcz_list)):
            #    hpdzcz_update_dict = {}
            #    hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hpdzcz_where_dict = {}
            #    hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
            #    hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
            #    hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
            #    
            #    ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理来账行内记账,中心未清算类型")
        #================来账行内未记账,中心清算===============================
        AfaLoggerFunc.tradeInfo(">>>开始处理来账行内未记账,中心清算类型")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '08' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型需补挂账,成功后修改错账处理标识为已处理")
            for i in xrange(len(hpdzcz_list)):
                #============补记账最多补三次==================================
                
                j = 0     #计数器初始化
                
                while 1 == 1:
                    
                    j = j + 1   #计数器加1
                    
                    #========初始化数据========================================
                    AfaLoggerFunc.tradeInfo(">>>开始初始化挂账数据")
                    
                    trc_dict = {}
                    if not rccpsDBFunc.getTransBil(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],trc_dict):
                        rccpsCronFunc.cronExit("S999","查询此交易相关信息异常")
                        
                    if not rccpsMap0000Dbilbka2CTradeContext.map(trc_dict):
                        rccpsCronFunc.cronExit("S999","将交易信息赋值到TradeContext异常")
                        
                    if not rccpsDBFunc.getInfoBil(TradeContext.BILVER,TradeContext.BILNO,TradeContext.BILRS,trc_dict):
                        rccpsCronFunc.cronExit("S999","查询此交易相关汇票信息异常")
                        
                    if not rccpsMap0000Dbilinf2CTradeContext.map(trc_dict):
                        rccpsCronFunc.cronExit("S999","将汇票信息赋值到TradeContext异常")
                    
                    TradeContext.BJETIM = AfaUtilTools.GetSysTime( )
                    TradeContext.BEAUUS = TradeContext.BEAUUS
                    TradeContext.BEAUPS = TradeContext.BEAUPS
                    TradeContext.OCCAMT = str(TradeContext.OCCAMT)
                    TradeContext.NCCworkDate = TradeContext.NCCWKDAT
                    
                    AfaLoggerFunc.tradeInfo(">>>结束初始化挂账数据")
                    #========来账,补账=========================================
                    AfaLoggerFunc.tradeInfo('>>>来账行内未清算,中心清算,自动挂账')
                    
                    AfaLoggerFunc.tradeInfo("汇票解付来账,自动入账")
                    
                    TradeContext.HostCode = '8813'            #调用8813主机接口
                    
                    TradeContext.BCSTAT  = PL_BCSTAT_AUTO   #自动入账
                    TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #处理中
                    
                    #====拼借贷方账户====
                    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_HCHK        #借方账户
                    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                    
                    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #贷方账号
                    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                    
                    TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ      #挂账账户
                    TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                    
                    AfaLoggerFunc.tradeInfo( '借方账号1:' + TradeContext.SBAC )
                    AfaLoggerFunc.tradeInfo( '贷方账号1:' + TradeContext.RBAC )
                    AfaLoggerFunc.tradeInfo( '挂账账号1:' + TradeContext.REAC )
                    
                    AfaLoggerFunc.tradeInfo(">>>开始判断是否存在多余款操作")
                    #=====判断记账次数====
                    #关彬捷 20080913 增加实际结算金额摘要代码
                    TradeContext.RCCSMCD = PL_RCCSMCD_HPJF       #摘要代码
                    if float(TradeContext.RMNAMT) != 0.00:
                        AfaLoggerFunc.tradeInfo(">>>第二次记账赋值操作")
                        
                        TradeContext.ACUR   = '2'   #记账循环次数
                        TradeContext.TRFG   = '9'   #凭证处理标识'
                        TradeContext.I2CETY = ''    #凭证种类
                        TradeContext.I2TRAM = str(TradeContext.RMNAMT)             #结余金额
                        TradeContext.I2SMCD = PL_RCCSMCD_HPJF                      #摘要代码
                        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_DYKJQ   #贷方账号
                        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_HCHK    #借方账号
                        TradeContext.I2REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ  #挂账账号
                        
                        #=====生成账号校验位====
                        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
                        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
                        TradeContext.I2REAC = rccpsHostFunc.CrtAcc(TradeContext.I2REAC,25)
                        
                        AfaLoggerFunc.tradeInfo( '借方账号2:' + TradeContext.I2SBAC )
                        AfaLoggerFunc.tradeInfo( '贷方账号2:' + TradeContext.I2RBAC )
                        AfaLoggerFunc.tradeInfo( '挂账账号2:' + TradeContext.I2REAC )
                        
                    AfaLoggerFunc.tradeInfo(">>>结束判断是否存在多余款操作")
                    
                    #======================修改登记簿中交易机构号为当前机构号======
                    
                    AfaLoggerFunc.tradeInfo(">>>开始更新汇兑业务登记簿交易机构号")
                    
                    bilbka_update_dict = {}
                    bilbka_update_dict['BESBNO'] = TradeContext.BESBNO
                    
                    bilbka_where_dict = {}
                    bilbka_where_dict['BJEDTE'] = TradeContext.BJEDTE
                    bilbka_where_dict['BSPSQN'] = TradeContext.BSPSQN
                    
                    ret = rccpsDBTrcc_bilbka.update(bilbka_update_dict,bilbka_where_dict)
                    
                    if ret <= 0:
                        rccpsCronFunc.cronExit('S999','更新汇兑业务登记簿中机构号异常')
                        
                    AfaLoggerFunc.tradeInfo(">>>结束更新汇兑业务登记簿交易机构号")
                    
                    #======================新增sstlog表状态记录====================
                    AfaLoggerFunc.tradeInfo(">>>开始新增交易状态")
                    
                    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
                        rccpsCronFunc.cronExit(TradeContext.errorCode, TradeContext.errorMsg)
                    
                    AfaLoggerFunc.tradeInfo(">>>结束新增交易状态")
                    
                    #======================commit操作==============================
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        rccpsCronFunc.cronExit("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    #=====================与主机通讯===============================
                    rccpsHostFunc.CommHost(TradeContext.HostCode)
                    
                    #=========开始向状态字典赋值===================================
                    stat_dict = {}
                    stat_dict['BJEDTE']  = TradeContext.BJEDTE            #交易日期
                    stat_dict['BSPSQN']  = TradeContext.BSPSQN            #报单序号
                    stat_dict['BJETIM']  = TradeContext.BJETIM            #交易时间
                    stat_dict['BESBNO']  = TradeContext.BESBNO            #机构号
                    stat_dict['BETELR']  = TradeContext.BETELR            #柜员号
                    stat_dict['SBAC']    = TradeContext.SBAC              #借方账号
                    stat_dict['RBAC']    = TradeContext.REAC              #贷方账号
                    stat_dict['MGID']    = TradeContext.errorCode         #主机返回代码
                    stat_dict['STRINFO'] = TradeContext.errorMsg          #主机返回信息
                    stat_dict['NOTE3']   = ""
                    
                    #=========判断主机返回结果=================================
                    if TradeContext.errorCode == '0000':
                        AfaLoggerFunc.tradeInfo("来账补记账成功,设置状态为自动入账\自动挂账成功")
                        
                        stat_dict['BCSTAT'] = TradeContext.BCSTAT          #流水状态
                        stat_dict['BDWFLG'] = PL_BDWFLG_SUCC               #流转处理标识
                        stat_dict['TRDT']   = TradeContext.TRDT            #主机日期
                        stat_dict['TLSQ']   = TradeContext.TLSQ            #主机流水
                        
                        #====若主机记账成功,但返回代销账序号不为空,则设置业务状态为挂账===
                        if TradeContext.existVariable('DASQ'):
                            if TradeContext.DASQ != '':
                                AfaLoggerFunc.tradeInfo("主机记账成功,但返回代销账序号非空,设置业务状态为挂账成功")
                                TradeContext.BCSTAT = PL_BCSTAT_HANG
                                stat_dict['DASQ']   = TradeContext.DASQ              #销账序号
                                stat_dict['NOTE3']  = "主机方挂账"
                    else:
                        AfaLoggerFunc.tradeInfo("来账补记账失败,设置状态为自动入账\自动挂账失败")
                        
                        stat_dict['BCSTAT'] = TradeContext.BCSTAT          #流水状态
                        stat_dict['BDWFLG'] = PL_BDWFLG_FAIL               #流转处理标识
                    
                    #=========设置状态=========================================
                    if not rccpsState.setTransState(stat_dict):
                        rccpsCronFunc.cronExit('S999', '设置状态异常')
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                        rccCronFunc.cronExit("S999","Commit异常")
                    AfaLoggerFunc.tradeInfo(">>>Commit成功")
                    
                    #========若主机返回失败,睡眠五分钟,进入下一次补记账========
                    if TradeContext.errorCode != '0000':
                        if j < 3:
                            AfaLoggerFunc.tradeInfo("第[" + str(j) + "]次来账补记账失败,睡眠五分钟,进入下一次补记账")
                            time.sleep(300)
                            continue
                        else:
                            AfaLoggerFunc.tradeInfo("第[" + str(j) + "]次来账补记账失败,停止此来账业务补记账,进入下一来账业务补记账")
                            #======置未完成标识为True==========================
                            uncomplate_flag = True
                            break
                    else:
                        AfaLoggerFunc.tradeInfo("补记账成功")
                
                        #========修改错账处理标识为已处理==============================
                        AfaLoggerFunc.tradeInfo(">>>开始修改错账处理标识为已处理")
                        
                        hpdzcz_update_dict = {}
                        hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                        
                        hpdzcz_where_dict = {}
                        hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                        hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                        hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                        
                        ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                        
                        if ret <= 0:
                            AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                            rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
                        
                        AfaLoggerFunc.tradeInfo(">>>结束修改错账处理标识为已处理")
                        
                        break
                
        AfaLoggerFunc.tradeInfo(">>>结束处理来账行内未清算,中心清算类型")
        
        #================关闭汇票对账汇票对账错账处理系统调度,打开汇票对账明细文件生成及发送到主机系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭汇票对账汇票对账错账处理系统调度,打开汇票对账明细文件生成及发送到主机系统调度")
        if not rccpsCronFunc.closeCron("00040"):
            rccpsCronFunc.cronExit("S999","关闭汇票对账错账处理系统调度异常")
        
        if not rccpsCronFunc.openCron("00045"):
            rccpsCronFunc.cronExit("S999","打开汇票对账明细文件生成及发送到主机系统调度异常")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭汇票对账汇票对账错账处理系统调度,打开汇票对账明细文件生成及发送到主机系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇票对账错账处理[rccpsHPDZCZModify]退出***")
        
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
            AfaLoggerFunc.tradeInfo("***[rccpsHPDZCZModify]交易中断***")

        sys.exit(-1)
