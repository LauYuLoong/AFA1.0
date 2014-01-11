# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.汇兑对账错账处理
#===============================================================================
#   交易文件:   rccpsHDDZCZModify.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-27
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc,time
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc,rccpsHostFunc,rccpsFunc,rccpsGetFunc,miya
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hddzcz,rccpsDBTrcc_hddzmx,rccpsDBTrcc_trcbka,rccpsDBFunc
import rccpsMap0000Dhddzmx2CTradeContext,rccpsMap0000Dtrcbka2CTradeContext,rccpsMap1101CTradeContext2Dtrcbka_dict

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇兑对账错账处理[rccpsHDDZCZModify]进入***")
        
        #==========初始化未完成标识为False=====================================
        uncomplate_flag = False
        
        #==========获取中心日期================================================
        AfaLoggerFunc.tradeInfo(">>>开始获取前中心工作日期")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","查询当前中心日期异常")
        
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #对账日期
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>结束获取前中心工作日期")
        
        #================往账行内有,中心无=====================================
        AfaLoggerFunc.tradeInfo(">>>开始处理往账行内有,中心无类型")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '01' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型由主机方调账,本系统设置状态为长款,修改错账处理标识为已处理")
            for i in xrange(len(hddzcz_list)):
                #========设置状态为长款========================================
                AfaLoggerFunc.tradeInfo("开始修改原交易状态为长款")
                
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========设置交易状态为长款成功================================
                if not rccpsState.newTransState(hddzcz_list[i]['BJEDTE'],hddzcz_list[i]['BSPSQN'],PL_BCSTAT_LONG,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '设置长款成功状态异常')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                AfaLoggerFunc.tradeInfo("结束修改原交易状态为长款")
                
                #========修改错账处理标识为已处理==============================
                AfaLoggerFunc.tradeInfo("开始修改错账处理标识为已处理")
                
                hddzcz_update_dict = {}
                hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hddzcz_where_dict = {} 
                hddzcz_where_dict['BJEDTE'] = hddzcz_list[i]['BJEDTE']
                hddzcz_where_dict['BSPSQN'] = hddzcz_list[i]['BSPSQN']
                
                ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
                    
                AfaLoggerFunc.tradeInfo("结束修改错账处理标识为已处理")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理往账行内有,中心无类型")
        #================往账行内无,中心有=====================================
        AfaLoggerFunc.tradeInfo(">>>开始处理往账行内无,中心有类型")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '02' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型为系统异常,需科技人员查实后处理")
            #for i in xrange(len(hddzcz_list)):
            #    hddzcz_update_dict = {}
            #    hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hddzcz_where_dict = {}
            #    hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
            #    hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
            #    hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
            #    
            #    ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理往账行内无,中心有类型")
        #================往账行内已记账,中心未清算===============================
        AfaLoggerFunc.tradeInfo(">>>开始处理往账行内已记账,中心未清算类型")
        
        hddzcz_where_sql = "nccwkdat = '" + NCCWKDAT + "' and eactyp = '03' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型由主机方调账,本系统设置状态为长款,修改错账处理标识为已处理")
            for i in xrange(len(hddzcz_list)):
                #========设置状态为长款========================================
                AfaLoggerFunc.tradeInfo("开始修改原交易状态为长款")
                
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========设置交易状态为长款成功================================
                if not rccpsState.newTransState(hddzcz_list[i]['BJEDTE'],hddzcz_list[i]['BSPSQN'],PL_BCSTAT_LONG,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '设置长款成功状态异常')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                AfaLoggerFunc.tradeInfo("结束修改原交易状态为长款")
                
                #========修改错账处理标识为已处理==============================
                AfaLoggerFunc.tradeInfo("开始修改错账处理标识为已处理")
                
                hddzcz_update_dict = {}
                hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hddzcz_where_dict = {} 
                hddzcz_where_dict['BJEDTE'] = hddzcz_list[i]['BJEDTE']
                hddzcz_where_dict['BSPSQN'] = hddzcz_list[i]['BSPSQN']
                
                ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
                    
                AfaLoggerFunc.tradeInfo("结束修改错账处理标识为已处理")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理往账行内已记账,中心未清算类型")
        #================往账行内未清算,中心清算===============================
        AfaLoggerFunc.tradeInfo(">>>开始处理往账行内未清算,中心清算类型")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '04' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型账务处理由主机方处理,修改原交易状态为清算成功,成功后修改错账处理标识为已处理")
            for i in xrange(len(hddzcz_list)):
                #========补清算================================================
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========设置交易状态为清算成功=================================
                if not rccpsState.newTransState(hddzcz_list[i]['BJEDTE'],hddzcz_list[i]['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '设置清算成功状态异常')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit异常")
                AfaLoggerFunc.tradeInfo(">>>Commit成功")
                
                #========修改错账处理标识为已处理==============================
                hddzcz_update_dict = {}
                hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hddzcz_where_dict = {}
                hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                
                ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理往账行内未清算,中心清算类型")
        #================来账行内有,中心无=====================================
        AfaLoggerFunc.tradeInfo(">>>开始处理来账行内有,中心无类型")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '05' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型为系统异常,需科技人员查实后处理")
            #for i in xrange(len(hddzcz_list)):
            #    hddzcz_update_dict = {}
            #    hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hddzcz_where_dict = {}
            #    hddzcz_where_dict['BJEDTE'] = hddzcz_list[i]['BJEDTE']
            #    hddzcz_where_dict['BSPSQN'] = hddzcz_list[i]['BSPSQN']
            #    
            #    ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理来账行内有,中心无类型")
        #================来账行内无,中心有=====================================
        AfaLoggerFunc.tradeInfo(">>>开始处理来账行内无,中心有类型")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '06' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("查询此错账类型相关记录异常")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型需补来账,成功后修改错账处理标识为已处理")
            for i in xrange(len(hddzcz_list)):
                #========补来账================================================
                AfaLoggerFunc.tradeInfo(">>>开始补来账")
                
                #========初始化来账上下文======================================
                AfaLoggerFunc.tradeInfo(">>>开始初始化上下文")
                TradeContext.tradeResponse=[]
                
                hddzmx_where_dict = {}
                hddzmx_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                hddzmx_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                hddzmx_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                
                hddzmx_dict = rccpsDBTrcc_hddzmx.selectu(hddzmx_where_dict)
                
                if hddzmx_dict == None:
                    rccpsCronFunc.cronExit("S999","查询来账明细数据异常")
                    
                if len(hddzmx_dict) <= 0:
                    rccpsCronFunc.cronExit("S999","登记簿中无此来账明细数据")
                
                rccpsMap0000Dhddzmx2CTradeContext.map(hddzmx_dict)
                
                TradeContext.OCCAMT = str(TradeContext.OCCAMT)
                TradeContext.TemplateCode  = 'RCC005'
                TradeContext.BRSFLG        = PL_BRSFLG_RCV
                TradeContext.CUR           = '01'
                
                if TradeContext.TRCCO == '2000001':
                    TradeContext.TransCode = '1101'
                    TradeContext.OPRNO     = '00'
                elif TradeContext.TRCCO == '2000002':
                    TradeContext.TransCode = '1102'
                    TradeContext.OPRNO     = '01'
                elif TradeContext.TRCCO == '2000003':
                    TradeContext.TransCode = '1103'
                    TradeContext.OPRNO     = '02'
                elif TradeContext.TRCCO == '2000004':
                    TradeContext.TransCode = '1104'
                    TradeContext.OPRNO     = '09'
                elif TradeContext.TRCCO == '2000009':
                    TradeContext.TransCode = '1105'
                    TradeContext.OPRNO     = '04'
                
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
                trcbka_dict = {}
                if not rccpsMap1101CTradeContext2Dtrcbka_dict.map(trcbka_dict):
                    rccpsCronFunc.cronExit('M999', '字典赋值出错')
                
                trcbka_dict['DCFLG'] = PL_DCFLG_CRE                  #借贷标识
                trcbka_dict['OPRNO'] = TradeContext.OPRNO            #业务属性
                
                #=====================开始插入数据库===========================
                if not rccpsDBFunc.insTransTrc(trcbka_dict):
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
                
                #========更新汇兑对账明细登记簿================================
                AfaLoggerFunc.tradeInfo(">>>开始更新汇兑明细登记簿")
                
                hddzmx_where_dict = {}
                hddzmx_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                hddzmx_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                hddzmx_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                
                stat_dict = {}
                if not rccpsState.getTransStateCur(TradeContext.BJEDTE,TradeContext.BSPSQN,stat_dict):
                    rccpsCronFunc.cronExit(TradeContext.errorCode,TradeContext.errorMsg)
                
                hddzmx_update_dict = {}
                hddzmx_update_dict['BJEDTE'] = TradeContext.BJEDTE
                hddzmx_update_dict['BSPSQN'] = TradeContext.BSPSQN
                hddzmx_update_dict['BCSTAT'] = stat_dict['BCSTAT']
                hddzmx_update_dict['BDWFLG'] = stat_dict['BDWFLG']
                
                ret = rccpsDBTrcc_hddzmx.updateCmt(hddzmx_update_dict,hddzmx_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","登记汇兑对账明细登记簿交易行内信息异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束更新汇兑明细登记簿")
                
                #========修改错账类型为行内未记账,中心清算=====================
                hddzcz_update_dict = {}
                hddzcz_update_dict['EACTYP'] = '08'
                hddzcz_update_dict['EACINF'] = '来账行内未记账,中心清算'
                hddzcz_update_dict['BJEDTE'] = TradeContext.BJEDTE
                hddzcz_update_dict['BSPSQN'] = TradeContext.BSPSQN
                
                hddzcz_where_dict = {}
                hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                
                ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","修改汇兑对账错账登记簿处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理来账行内无,中心有类型")
        #================来账行内记账,中心未清算===============================
        AfaLoggerFunc.tradeInfo(">>>开始处理来账行内记账,中心未清算类型")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '07' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型为系统异常,需科技人员查实后处理")
            #for i in xrange(len(hddzcz_list)):
            #    hddzcz_update_dict = {}
            #    hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hddzcz_where_dict = {}
            #    hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
            #    hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
            #    hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
            #    
            #    ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束处理来账行内记账,中心未清算类型")
        #================来账行内未记账,中心清算===============================
        AfaLoggerFunc.tradeInfo(">>>开始处理来账行内未记账,中心清算类型")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '08' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","查询此错账类型相关记录异常")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("无此错账类型相关记录")
        
        else:
            AfaLoggerFunc.tradeInfo("此错账类型需补挂账,成功后修改错账处理标识为已处理")
            for i in xrange(len(hddzcz_list)):
                #============补记账最多补三次==================================
                
                j = 0     #计数器初始化
                
                while 1 == 1:
                    
                    j = j + 1   #计数器加1
                        
                    #========初始化数据========================================
                    AfaLoggerFunc.tradeInfo(">>>开始初始化挂账数据")
                    
                    trc_dict = {}
                    if not rccpsDBFunc.getTransTrc(hddzcz_list[i]['BJEDTE'],hddzcz_list[i]['BSPSQN'],trc_dict):
                        rccpsCronFunc.cronExit("S999","查询此交易相关信息异常")
                        
                    if not rccpsMap0000Dtrcbka2CTradeContext.map(trc_dict):
                        rccpsCronFunc.cronExit("S999","将交易信息赋值到TradeContext异常")
                    
                    TradeContext.NCCworkDate = TradeContext.NCCWKDAT 
                    TradeContext.BJETIM = AfaUtilTools.GetSysTime( )
                    TradeContext.BEAUUS = ""
                    TradeContext.BEAUPS = ""
                    TradeContext.OCCAMT = str(TradeContext.OCCAMT)
                    
                    AfaLoggerFunc.tradeInfo(">>>结束初始化挂账数据")
                    #========来账,补账=========================================
                    AfaLoggerFunc.tradeInfo('>>>来账行内未清算,中心清算,自动挂账')
                    
                    if TradeContext.TRCCO != '2000004':
                        AfaLoggerFunc.tradeInfo("非退汇来账,开始校验密押")
                        
                        #=====开始调用密押服务器进行核押====
                        TRCDAT = TradeContext.TRCDAT
                        TRCNO = TradeContext.TRCNO
                        SEAL = TradeContext.SEAL
                        SNDBANKCO  = TradeContext.SNDBNKCO
                        RCVBANKCO  = TradeContext.RCVBNKCO
                        SNDBANKCO = SNDBANKCO.rjust(12,'0')
                        RCVBANKCO = RCVBANKCO.rjust(12,'0')
                        AMOUNT = TradeContext.OCCAMT.split('.')[0] + TradeContext.OCCAMT.split('.')[1]
                        AMOUNT = AMOUNT.rjust(15,'0')
                        INFO   = "".rjust(60,' ')
                        
                        AfaLoggerFunc.tradeDebug('处理类型(0-编押 1-核押):' + str(PL_SEAL_DEC) )
                        AfaLoggerFunc.tradeDebug('业务种类(1-现金汇票 2-转账汇票 3-电子汇兑业务):' +str(PL_TYPE_DZHD) )
                        AfaLoggerFunc.tradeDebug('委托日期:' + TradeContext.TRCDAT )
                        AfaLoggerFunc.tradeDebug('交易流水号:' + TradeContext.TRCNO )
                        AfaLoggerFunc.tradeDebug('AMOUNT=' + str(AMOUNT) )
                        AfaLoggerFunc.tradeDebug('SNDBANKCO=' + str(SNDBANKCO) )
                        AfaLoggerFunc.tradeDebug('RCVBANKCO=' + str(RCVBANKCO) )
                        AfaLoggerFunc.tradeDebug('密押:' + TradeContext.SEAL )
                        AfaLoggerFunc.tradeDebug('OTHERINFO[' + str(INFO) + ']')
                        
                        ret = miya.DraftEncrypt(PL_SEAL_DEC,PL_TYPE_DZHD,TRCDAT,TRCNO,AMOUNT,SNDBANKCO,RCVBANKCO,INFO,SEAL)
                        AfaLoggerFunc.tradeInfo('>>>校验密押,返回值ret=['+ str(ret) + ']')
                        
                        if ret != 0:
                            if ret == 9005:
                                #====密押错，自动挂账==============================
                                AfaLoggerFunc.tradeInfo("密押错,自动挂账")
                                NOTE3 = "密押错,自动挂账"
                            else:
                                #====校验密押异常,自动挂账=========================
                                AfaLoggerFunc.tradeInfo("校验密押异常,自动挂账")
                                NOTE3 = "校验密押异常,自动挂账"
                            
                            TradeContext.HostCode = '8813'            #调用8813主机接口
                            
                            TradeContext.NOTE3   = NOTE3            #挂账原因
                            TradeContext.BCSTAT  = PL_BCSTAT_HANG   #自动挂账
                            TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #处理中
                        
                            #====拼借贷方账户====
                            TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #借方账户
                            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                            
                            TradeContext.RBAC = TradeContext.BESBNO + "".rjust(15,'0')
                            
                            TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ      #挂账账户
                            TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                            
                            AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
                            AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
                            AfaLoggerFunc.tradeInfo( '挂账账号:' + TradeContext.REAC )
                        else:
                            #======密押校验通过,自动入账===========================
                            AfaLoggerFunc.tradeInfo("密押校验通过,自动入账")
                            
                            TradeContext.HostCode = '8813'            #调用8813主机接口
                            
                            TradeContext.BCSTAT  = PL_BCSTAT_AUTO   #自动入账
                            TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #处理中
                            
                            #====拼借贷方账户====
                            TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #借方账户
                            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                            
                            TradeContext.RBAC = TradeContext.PYEACC                      #收款人账号
                            
                            TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ      #挂账账户
                            TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                            
                            AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
                            AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
                            AfaLoggerFunc.tradeInfo( '挂账账号:' + TradeContext.REAC )
                        
                        AfaLoggerFunc.tradeInfo(">>>结束校验密押")
                    else:
                        AfaLoggerFunc.tradeInfo("退汇来账,自动入账")
                        
                        TradeContext.HostCode = '8813'            #调用8813主机接口
                        
                        TradeContext.BCSTAT  = PL_BCSTAT_AUTO   #自动入账
                        TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #处理中
                        
                        #====拼借贷方账户====
                        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #借方账户
                        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                        
                        TradeContext.RBAC = TradeContext.PYEACC                      #贷方账户
                        
                        TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ      #挂账账户
                        TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                        
                        AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
                        AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
                        AfaLoggerFunc.tradeInfo( '挂账账号:' + TradeContext.REAC )
                    
                    
                    #======================修改登记簿中交易机构号为当前机构号======
                    
                    AfaLoggerFunc.tradeInfo(">>>开始更新汇兑业务登记簿交易机构号")
                    
                    trcbka_update_dict = {}
                    trcbka_update_dict['BESBNO'] = TradeContext.BESBNO
                    
                    trcbka_where_dict = {}
                    trcbka_where_dict['BJEDTE'] = TradeContext.BJEDTE
                    trcbka_where_dict['BSPSQN'] = TradeContext.BSPSQN
                    
                    ret = rccpsDBTrcc_trcbka.update(trcbka_update_dict,trcbka_where_dict)
                    
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
                        
                        hddzcz_update_dict = {}
                        hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                        
                        hddzcz_where_dict = {}
                        hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                        hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                        hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                        
                        ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                        
                        if ret <= 0:
                            AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                            rccpsCronFunc.cronExit("S999","修改此错账处理标识异常")
                        
                        AfaLoggerFunc.tradeInfo(">>>结束修改错账处理标识为已处理")
                        
                        break
                
        AfaLoggerFunc.tradeInfo(">>>结束处理来账行内未清算,中心清算类型")
        
        #================关闭汇兑对账汇兑对账错账处理系统调度,打开汇兑对账明细文件生成及发送到主机系统调度==
        AfaLoggerFunc.tradeInfo(">>>开始关闭汇兑对账汇兑对账错账处理系统调度,打开汇兑对账明细文件生成及发送到主机系统调度")
        if not rccpsCronFunc.closeCron("00030"):
            rccpsCronFunc.cronExit("S999","关闭汇兑对账错账处理系统调度异常")
        
        if not uncomplate_flag:
            if not rccpsCronFunc.openCron("00035"):
                rccpsCronFunc.cronExit("S999","打开汇兑对账明细文件生成及发送到主机系统调度异常")
        else:
            AfaLoggerFunc.tradeInfo(">>>对账未完成标识为True,不打开汇兑对账明细文件生成及发送到主机系统调度异常")
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>结束关闭汇兑对账汇兑对账错账处理系统调度,打开汇兑对账明细文件生成及发送到主机系统调度")
        
        AfaLoggerFunc.tradeInfo("***农信银系统: 系统调度类.汇兑对账错账处理[rccpsHDDZCZModify]退出***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHDDZCZModify]交易中断***')

        sys.exit(-1)
