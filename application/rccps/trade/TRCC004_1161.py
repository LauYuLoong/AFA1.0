# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.回执类操作(1.回执操作).自动冲正应答报文接收
#==============================================================================
#   交易文件:   TRCC004_1161.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-12-04
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsState,rccpsGetFunc,rccpsHostFunc,rccpsDBFunc,rccpsEntries
import rccpsDBTrcc_mpcbka,rccpsDBTrcc_atcbka


#=====================回执个性化处理(本地操作)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.回执类操作(1.回执操作).通存通兑冲正应答报文接收[TRC004_1161]进入***' )
    
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #查询原冲正交易信息
    atcbka_dict = {}
    
    atcbka_where_dict = {}
    atcbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
    
    atcbka_dict = rccpsDBTrcc_atcbka.selectu(atcbka_where_dict)
    
    if atcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","查询原冲正交易信息异常")
        
    if len(atcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow("S999","未找到原冲正交易信息,丢弃报文")
        
    #查询原被冲正交易是否已开始被冲销
    mpcbka_dict = {}
    
    mpcbka_where_dict = {}
    mpcbka_where_dict['ORMFN'] = atcbka_dict['ORMFN']
    
    mpcbka_dict = rccpsDBTrcc_mpcbka.selectu(mpcbka_where_dict)
    
    if mpcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","查询原冲正交易信息异常")
        
    if len(mpcbka_dict) > 0:
        return AfaFlowControl.ExitThisFlow("S999","原交易已开始冲销,停止处理本冲正应答")
        
    #=====给机构号和柜员号赋值====
    TradeContext.BETELR = atcbka_dict['BETELR']
    TradeContext.BESBNO = atcbka_dict['BESBNO']
    
    #更新冲正登记簿中心返回信息
    AfaLoggerFunc.tradeInfo(">>>开始更新冲正登记簿中心返回信息")
    
    atcbka_update_dict = {}
    atcbka_update_dict['PRCCO'] = TradeContext.PRCCO
    atcbka_update_dict['STRINFO'] = TradeContext.STRINFO
    
    ret = rccpsDBTrcc_atcbka.update(atcbka_update_dict,atcbka_where_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","更新冲正登记簿异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束更新冲正登记簿中心返回信息")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    if atcbka_dict['ORTRCCO'] != '3000504':
        AfaLoggerFunc.tradeInfo(">>>原被冲正交易为通存或通兑账务类交易")
        
        #查询原被冲正交易信息
        wtr_dict = {}
        
        if not rccpsDBFunc.getTransWtr(atcbka_dict['BOJEDT'],atcbka_dict['BOSPSQ'],wtr_dict):
            return AfaFlowControl.ExitThisFlow("S999","查询原被冲正交易信息异常")
        
        #如果原被冲正交易当前状态已为冲正,表示已收到冲正应答,停止处理
        if wtr_dict['BCSTAT'] == PL_BCSTAT_CANCEL:
            return AfaFlowControl.ExitThisFlow("S999","已收到冲正应答,丢弃报文")
        
        TradeContext.TERMID = wtr_dict['TERMID']
        TradeContext.BRSFLG = wtr_dict['BRSFLG']
        
        
        
        #若原被冲正交易为通存类交易,应抹账
        if wtr_dict['TRCCO'] in ('3000002','3000003','3000004','3000005'):
            
            AfaLoggerFunc.tradeInfo(">>>开始发起主机抹账")
            
            #为抹账赋值会计分录
            entries_dict = {}
            entries_dict['FEDT']     = wtr_dict['BJEDTE']
            entries_dict['RBSQ']     = wtr_dict['BSPSQN']
            entries_dict['PYRACC']   = wtr_dict['PYRACC']
            entries_dict['PYRNAM']   = wtr_dict['PYRNAM']
            entries_dict['PYEACC']   = wtr_dict['PYEACC']
            entries_dict['PYENAM']   = wtr_dict['PYENAM']
            entries_dict['OCCAMT']   = wtr_dict['OCCAMT']
            entries_dict['CHRGTYP']  = wtr_dict['CHRGTYP']
            entries_dict['CUSCHRG']  = wtr_dict['CUSCHRG']
            entries_dict['RCCSMCD']  = PL_RCCSMCD_CX
            TradeContext.BRSFLG      = wtr_dict['BRSFLG']
            
            if TradeContext.ORTRCCO == '3000002' or TradeContext.ORTRCCO == '3000004':
                rccpsEntries.KZTCWZMZ(entries_dict)
            
            if TradeContext.ORTRCCO == '3000003' or TradeContext.ORTRCCO == '3000005':
                rccpsEntries.KZBZYWZMZ(entries_dict)
                
            #=====生成新的前置日期和前置流水号====
            if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
                return AfaFlowControl.ExisThisFlow('S999',"产生新的前置流水号异常")
            
            #设置原交易状态为冲正处理中
            AfaLoggerFunc.tradeInfo('>>>开始设置原交易状态为冲正处理中')
                
            if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为冲正处理中异常")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
            AfaLoggerFunc.tradeInfo('>>>结束设置原交易状态为冲正处理中')
            
            #=====调起主机接口=====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            AfaLoggerFunc.tradeInfo(">>>结束发起主机记账")
            
        else:
            AfaLoggerFunc.tradeInfo(">>>原交易未记账,冲正不抹账")
            
            #设置原交易状态为冲正处理中
            AfaLoggerFunc.tradeInfo('>>>开始设置原交易状态为冲正处理中')
                
            if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为冲正处理中异常")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
            AfaLoggerFunc.tradeInfo('>>>结束设置原交易状态为冲正处理中')
            
            TradeContext.errorCode = "0000"
            TradeContext.errorMsg  = "冲正前未记账,冲正不抹账"
           
        #根据主机返回信息,设置交易状态 
        stat_dict = {}
        
        stat_dict['BJEDTE']  = wtr_dict['BJEDTE']
        stat_dict['BSPSQN']  = wtr_dict['BSPSQN']
        stat_dict['MGID']    = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        if TradeContext.errorCode == '0000':
            #设置原交易状态为冲正成功
            AfaLoggerFunc.tradeInfo("<<<<<<<开始更改原交易状态为冲正成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_CANCEL
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            if TradeContext.existVariable('TRDT'):
                stat_dict['TRDT']   = TradeContext.TRDT
            if TradeContext.existVariable('TLSQ'):
                stat_dict['TLSQ']   = TradeContext.TLSQ
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态为冲正成功异常')
            
            AfaLoggerFunc.tradeInfo("<<<<<<<结束更改原交易状态为冲正成功")
        else:
            #设置原交易状态为冲正失败
            AfaLoggerFunc.tradeInfo("<<<<<<<开始更改原交易状态为冲正失败")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_CANCEL
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态为冲正失败异常')
            
            AfaLoggerFunc.tradeInfo("<<<<<<<结束更改原交易状态为冲正成功")
            
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
    else:
        AfaLoggerFunc.tradeInfo(">>>原被冲正交易为冲销交易")
        
        #查询原冲销交易详细信息
        AfaLoggerFunc.tradeInfo(">>>冲销交易报单日期[" + atcbka_dict['BOJEDT'] + "]报单序号[" + atcbka_dict['BOSPSQ'] + "]")
        
        AfaLoggerFunc.tradeInfo(">>>开始查询原冲销交易详细信息")
        
        mpc_dict = {}
        
        if not rccpsDBFunc.getTransMpc(atcbka_dict['BOJEDT'],atcbka_dict['BOSPSQ'],mpc_dict):
            return AfaFlowControl.ExitThisFlow("S999","查询原冲销交易详细信息异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束查询原冲销交易详细信息")
        
        #查询原被冲销交易详细信息
        AfaLoggerFunc.tradeInfo(">>>被冲销交易报单日期[" + mpc_dict['BOJEDT'] + "]报单序号[" + mpc_dict['BOSPSQ'] + "]")
        
        AfaLoggerFunc.tradeInfo(">>>开始查询原被冲销交易详细信息")
        
        wtr_dict = {}
        
        if not rccpsDBFunc.getTransWtr(mpc_dict['BOJEDT'],mpc_dict['BOSPSQ'],wtr_dict):
            return AfaFlowControl.ExitThisFlow("S999","查询原被冲销交易详细信息异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束查询原被冲销交易详细信息")
        
        #更新冲销登记簿
        AfaLoggerFunc.tradeInfo(">>>开始更新冲销登记簿")
        
        mpcbka_update_dict = {}
        mpcbka_update_dict['PRCCO'] = "RCCI1000"
        mpcbka_update_dict['STRINFO'] = "冲销交易被成功冲正"
        
        mpcbka_where_dict = {}
        mpcbka_where_dict['BJEDTE'] = mpc_dict['BJEDTE']
        mpcbka_where_dict['BSPSQN'] = mpc_dict['BSPSQN']
        
        ret = rccpsDBTrcc_mpcbka.update(mpcbka_update_dict,mpcbka_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("更新冲销登记簿返回码和返回信息异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束更新冲销登记簿")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.回执类操作(1.回执操作).通存通兑冲正应答报文接收[TRC004_1161]退出***' )
    
    return True
