# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.回执类操作(1.回执操作).通存通兑业务回执报文接收
#==============================================================================
#   交易文件:   TRCC004_1147.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-10-22
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsGetFunc,rccpsEntries
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_balbka,rccpsDBTrcc_atcbka,rccpsDBTrcc_mpcbka


#=====================回执个性化处理(本地操作)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.回执类操作(1.回执操作).通存通兑业务回执报文接收[TRC004_1147]进入***' )
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #=================匹配原交易信息===========================================
    wtrbka_where_dict = {}
    wtrbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
    
    wtrbka_dict = {}
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
    if wtrbka_dict == None:
        return AfaFlowControl.ExitThisFlow('S999', "查询通存通兑业务信息登记簿异常")
    
    if len(wtrbka_dict) > 0:
        TradeContext.BJEDTE  = wtrbka_dict['BJEDTE']
        TradeContext.BSPSQN  = wtrbka_dict['BSPSQN']
        TradeContext.TRCCO   = wtrbka_dict['TRCCO']
        TradeContext.BESBNO  = wtrbka_dict['BESBNO']
        TradeContext.BETELR  = wtrbka_dict['BETELR']
        TradeContext.OCCAMT  = str(wtrbka_dict['OCCAMT'])
        TradeContext.CHRGTYP = wtrbka_dict['CHRGTYP']
        TradeContext.LOCCUSCHRG = str(wtrbka_dict['CUSCHRG'])
        TradeContext.PYETYP  = wtrbka_dict['PYETYP']
        TradeContext.PYEACC  = wtrbka_dict['PYEACC']
        TradeContext.PYENAM  = wtrbka_dict['PYENAM']
        TradeContext.PYRTYP  = wtrbka_dict['PYRTYP']
        TradeContext.PYRACC  = wtrbka_dict['PYRACC']
        TradeContext.PYRNAM  = wtrbka_dict['PYRNAM']
        TradeContext.CERTTYPE = wtrbka_dict['CERTTYPE']
        TradeContext.CERTNO  = wtrbka_dict['CERTNO']
        TradeContext.TERMID  = wtrbka_dict['TERMID']
        TradeContext.WARNTNO = wtrbka_dict['BNKBKNO']
        
        #============设置原交易状态为拒绝======================================
        AfaLoggerFunc.tradeInfo(">>>开始设置原交易业务状态为拒绝处理中")
        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为拒绝处理中异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束设置原交易业务状态为拒绝处理中")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        AfaLoggerFunc.tradeInfo(">>>开始设置原交易业务状态为拒绝成功")
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRCCO']   = TradeContext.PRCCO
        stat_dict['STRINFO'] = TradeContext.STRINFO
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为拒绝成功异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束设置原交易业务状态为拒绝成功")
        
    else:
        AfaLoggerFunc.tradeInfo(">>>通存通兑业务登记簿中未找到原请求交易信息,开始查询原存款确认信息")
        wtrbka_where_dict = {}
        wtrbka_where_dict['COMSGFLGNO'] = TradeContext.ORMFN
        
        wtrbka_dict = {}
        wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
        
        if wtrbka_dict == None:
            return AfaFlowControl.ExitThisFlow('S999', "查询通存通兑业务信息登记簿异常")
        
        if len(wtrbka_dict) > 0:
            TradeContext.BJEDTE  = wtrbka_dict['BJEDTE']
            TradeContext.BSPSQN  = wtrbka_dict['BSPSQN']
            TradeContext.TRCCO   = wtrbka_dict['TRCCO']
            TradeContext.BESBNO  = wtrbka_dict['BESBNO']
            TradeContext.BETELR  = wtrbka_dict['BETELR']
            TradeContext.OCCAMT  = str(wtrbka_dict['OCCAMT'])
            TradeContext.CHRGTYP = wtrbka_dict['CHRGTYP']
            TradeContext.LOCCUSCHRG = str(wtrbka_dict['CUSCHRG'])
            TradeContext.PYETYP  = wtrbka_dict['PYETYP']
            TradeContext.PYEACC  = wtrbka_dict['PYEACC']
            TradeContext.PYENAM  = wtrbka_dict['PYENAM']
            TradeContext.PYRTYP  = wtrbka_dict['PYRTYP']
            TradeContext.PYRACC  = wtrbka_dict['PYRACC']
            TradeContext.PYRNAM  = wtrbka_dict['PYRNAM']
            TradeContext.CERTTYPE = wtrbka_dict['CERTTYPE']
            TradeContext.CERTNO  = wtrbka_dict['CERTNO']
            TradeContext.TERMID  = wtrbka_dict['TERMID']
            TradeContext.WARNTNO = wtrbka_dict['BNKBKNO']
            
            #============设置原交易状态为拒绝======================================
            AfaLoggerFunc.tradeInfo(">>>开始设置原交易业务状态为拒绝处理中")
            
            if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为拒绝处理中异常")
            
            AfaLoggerFunc.tradeInfo(">>>结束设置原交易业务状态为拒绝处理中")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            AfaLoggerFunc.tradeInfo(">>>Commit成功")
            
            AfaLoggerFunc.tradeInfo(">>>开始设置原交易业务状态为拒绝成功")
            
            stat_dict = {}
            stat_dict['BJEDTE']  = TradeContext.BJEDTE
            stat_dict['BSPSQN']  = TradeContext.BSPSQN
            stat_dict['BESBNO']  = TradeContext.BESBNO
            stat_dict['BETELR']  = TradeContext.BETELR
            stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            stat_dict['PRCCO']   = TradeContext.PRCCO
            stat_dict['STRINFO'] = TradeContext.STRINFO
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为拒绝成功异常")
            
            AfaLoggerFunc.tradeInfo(">>>结束设置原交易业务状态为拒绝成功")
            
        else:
            AfaLoggerFunc.tradeInfo(">>>通存通兑业务登记簿中未找到原存款确认信息,开始查询余额查询登记簿")
            balbka_where_dict = {}
            balbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
            
            balbka_dict = {}
            balbka_dict = rccpsDBTrcc_balbka.selectu(balbka_where_dict)
            
            if balbka_dict == None:
                return AfaFlowControl.ExitThisFlow('S999', "查询余额查询登记簿异常")
                
            if len(balbka_dict) > 0:
                TradeContext.TRCCO = balbka_dict['TRCCO']
                
                #=====更新原余额查询交易返回码=================================
                AfaLoggerFunc.tradeInfo(">>>开始更新原余额查询交易返回码")
                
                balbka_update_dict = {}
                balbka_update_dict['PRCCO']   = TradeContext.PRCCO
                balbka_update_dict['STRINFO'] = TradeContext.STRINFO
                
                ret = rccpsDBTrcc_balbka.update(balbka_update_dict,balbka_where_dict)
                
                if ret <= 0:
                    return AfaFlowControl.ExitThisFlow('S999', "更新原余额查询交易返回码异常")
                
                AfaLoggerFunc.tradeInfo(">>>结束更新原余额查询交易返回码")
            else:
                AfaLoggerFunc.tradeInfo(">>>余额查询登记簿中未找到原交易信息,开始查询自动冲正登记簿")
                atcbka_where_dict = {}
                atcbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
                
                atcbka_dict = {}
                atcbka_dict = rccpsDBTrcc_atcbka.selectu(atcbka_where_dict)
                
                if atcbka_dict == None:
                    return AfaFlowControl.ExitThisFlow('S999', "查询自动冲正登记簿异常")
                    
                if len(atcbka_dict) > 0:
                    TradeContext.BOJEDT = atcbka_dict['BOJEDT']
                    TradeContext.BOSPSQ = atcbka_dict['BOSPSQ']
                    TradeContext.TRCCO  = atcbka_dict['TRCCO']
                    
                    #====更新自动冲正交易返回码================================
                    AfaLoggerFunc.tradeInfo(">>>开始更新原自动冲正交易返回码")
                    
                    atcbka_update_dict = {}
                    atcbka_update_dict['PRCCO']   = TradeContext.PRCCO
                    atcbka_update_dict['STRINFO'] = TradeContext.STRINFO
                    
                    ret = rccpsDBTrcc_atcbka.update(atcbka_update_dict,atcbka_where_dict)
                    
                    if ret<= 0:
                        return AfaFlowControl.ExitThisFlow('S999', "更新原冲正交易返回码异常")
                    
                    AfaLoggerFunc.tradeInfo(">>>结束更新原自动冲正交易返回码")
                    
                    #====设置原被冲正交易业务状态为冲正失败================
                    #AfaLoggerFunc.tradeInfo(">>>开始设置原被冲正交易业务状态为冲正失败")
                    #
                    #stat_dict = {}
                    #stat_dict['BJEDTE']  = TradeContext.BOJEDT
                    #stat_dict['BSPSQN']  = TradeContext.BOSPSQ
                    #stat_dict['BCSTAT']  = PL_BCSTAT_CANC
                    #stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
                    #stat_dict['PRCCO']   = TradeContext.PRCCO
                    #stat_dict['STRINFO'] = TradeContext.STRINFO
                    #
                    #if not rccpsState.setTransState(stat_dict):
                    #    return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为冲正失败异常")
                    #
                    #AfaLoggerFunc.tradeInfo(">>>结束设置原被冲正交易业务状态为冲正失败")
                else:
                    AfaLoggerFunc.tradeInfo(">>>自动冲正登记簿中未找到原交易信息,开始查询柜面冲销登记簿")
                    mpcbka_where_dict = {}
                    mpcbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
                    
                    mpcbka_dict = {}
                    mpcbka_dict = rccpsDBTrcc_mpcbka.selectu(mpcbka_where_dict)
                    
                    if mpcbka_dict == None:
                        return AfaFlowControl.ExitThisFlow('S999', "查询柜面冲销登记簿异常")
                        
                    if len(mpcbka_dict) > 0:
                        TradeContext.BOJEDT  = mpcbka_dict['BOJEDT']
                        TradeContext.BOSPSQ  = mpcbka_dict['BOSPSQ']
                        TradeContext.TRCCO   = mpcbka_dict['TRCCO']
                        TradeContext.ORTRCCO = mpcbka_dict['ORTRCCO']
                        TradeContext.BESBNO  = mpcbka_dict['BESBNO']
                        TradeContext.BETELR  = mpcbka_dict['BETELR']
                        TradeContext.TERMID  = mpcbka_dict['TERMID']
                        
                        #====更新柜台冲销交易返回码================================
                        AfaLoggerFunc.tradeInfo(">>>开始更新原柜台冲销交易返回码")
                        
                        mpcbka_update_dict = {}
                        mpcbka_update_dict['PRCCO']   = TradeContext.PRCCO
                        mpcbka_update_dict['STRINFO'] = TradeContext.STRINFO
                        
                        ret = rccpsDBTrcc_mpcbka.update(mpcbka_update_dict,mpcbka_where_dict)
                        
                        if ret <=0:
                            return AfaFlowControl.ExitThisFlow('S999', "更新原柜面冲销交易返回码异常")
                            
                        AfaLoggerFunc.tradeInfo(">>>结束更新原柜面冲销交易返回码")
                        
                        #====设置原被冲销交易业务状态为冲销失败================
                        #AfaLoggerFunc.tradeInfo(">>>开始设置原被冲销交易业务状态为冲销处理中")
                        #
                        #if not rccpsState.newTransState(TradeContext.BOJEDT,TradeContext.BOSPSQ,PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
                        #    return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为冲销失败异常")
                        #
                        #AfaLoggerFunc.tradeInfo(">>>结束设置原被冲销交易业务状态为冲销处理中")
                        #
                        #if not AfaDBFunc.CommitSql( ):
                        #    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        #    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                        #AfaLoggerFunc.tradeInfo(">>>Commit成功")
                        #
                        #AfaLoggerFunc.tradeInfo(">>>开始设置原被冲销交易业务状态为冲销失败")
                        #
                        #stat_dict = {}
                        #
                        #stat_dict['BJEDTE']  = TradeContext.BJEDTE
                        #stat_dict['BSPSQN']  = TradeContext.BSPSQN
                        #stat_dict['PRCCO']   = TradeContext.PRCCO
                        #stat_dict['STRINFO'] = TradeContext.STRINFO
                        #stat_dict['BCSTAT']  = PL_BCSTAT_CANC
                        #stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
                        #
                        #AfaLoggerFunc.tradeInfo(">>>结束设置原被冲销交易业务状态为冲销失败")
                    
                    else:
                        return AfaFlowControl.ExitThisFlow('S999', "未找到原交易信息,丢弃报文")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    #=================若原交易为通存交易,开始自动抹账==========================
    if TradeContext.TRCCO == '3000002' or TradeContext.TRCCO == '3000003' or TradeContext.TRCCO == '3000004' or TradeContext.TRCCO == '3000005':
        
        #=====特殊处理  关彬捷 20081127 调8813抹账,需产生新的前置流水号进行记账====
        if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
            return AfaFlowControl.ExisThisFlow('S999',"产生新的前置流水号异常")
        else:
            AfaLoggerFunc.tradeInfo(">>>成功产生新的前置流水号")
        
        #为抹账赋值会计分录
        entries_dict = {}
        entries_dict['FEDT']     = TradeContext.BJEDTE
        entries_dict['RBSQ']     = TradeContext.BSPSQN
        entries_dict['PYRACC']   = TradeContext.PYRACC
        entries_dict['PYRNAM']   = TradeContext.PYRNAM
        entries_dict['PYEACC']   = TradeContext.PYEACC
        entries_dict['PYENAM']   = TradeContext.PYENAM
        entries_dict['OCCAMT']   = TradeContext.OCCAMT
        entries_dict['CHRGTYP']  = TradeContext.CHRGTYP
        entries_dict['CUSCHRG']  = TradeContext.LOCCUSCHRG
        entries_dict['RCCSMCD']  = PL_RCCSMCD_CX
        TradeContext.BRSFLG      = PL_BRSFLG_SND
        
        if TradeContext.TRCCO == '3000002' or TradeContext.TRCCO == '3000004':
            rccpsEntries.KZTCWZMZ(entries_dict)
        
        if TradeContext.TRCCO == '3000003' or TradeContext.TRCCO == '3000005':
            rccpsEntries.KZBZYWZMZ(entries_dict)
        
        #=============设置原交易业务状态为抹账处理中===========================
        AfaLoggerFunc.tradeInfo(">>>开始设置原交易业务状态为抹账处理中")
        
        #====设置业务状态为抹账处理中====
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为抹账处理中异常')
        
        AfaLoggerFunc.tradeInfo(">>>结束设置原交易业务状态为抹账处理中")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
        #=============开始发起主机抹账=========================================
        AfaLoggerFunc.tradeInfo(">>>开始主机抹账")
        
        #=====调起抹账主机接口====
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo(">>>结束主机抹账")
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        
        stat_dict = {}
        
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['MGID']    = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        if TradeContext.errorCode == '0000':
            #=========设置原交易业务状态为抹账成功=============================
            AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为抹账成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            stat_dict['TRDT']   = TradeContext.TRDT
            stat_dict['TLSQ']   = TradeContext.TLSQ
            stat_dict['PRTCNT'] = 1
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态抹账成功异常')
            
            AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为抹账成功")
        
        else:
            #=========设置原交易业务状态为抹账失败=============================
            AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为抹账失败")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态抹账成功异常')
            
            AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为抹账失败")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.回执类操作(1.回执操作).通存通兑业务回执报文接收[TRC004_1147]退出***' )
    
    return True
