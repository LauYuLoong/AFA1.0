# -*- coding: gbk -*-
##################################################################
#   农信银系统：往账.回执类操作(1.回执操作).通存通兑冲销应答报文接收
#=================================================================
#   程序文件:   TRCC004_1162.py
#   修改时间:   2008-12-01
#   作者：      潘广通
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,AfaDBFunc
from types import *
from rccpsConst import *
import rccpsState,rccpsGetFunc,rccpsHostFunc,rccpsDBFunc,rccpsEntries
import rccpsDBTrcc_mpcbka,rccpsDBTrcc_atcbka

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.回执类操作(1.回执操作).通存通兑冲销应答报文接收[TRC004_1162]进入***' )
    
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #=================初始化返回信息============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)
    
    #查询冲正登记簿中是否有对此冲销交易的冲正
    AfaLoggerFunc.tradeInfo(">>>开始检查此冲销交易是否已被冲正")
    
    where_sql = "ORMFN = '" + TradeContext.ORMFN + "'"
    
    ret = rccpsDBTrcc_atcbka.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","查询冲正登记簿异常,退出主流程")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","冲正登记簿中存在对此冲销交易的冲正,退出主流程")
        
    AfaLoggerFunc.tradeInfo(">>>结束检查此冲销交易是否已被冲正")
    
    #=====更改柜员号和机构号为发起柜员号、发起机构号====
    AfaLoggerFunc.tradeInfo("<<<<<<开始更改柜员号，机构号")
    
    #=====查找冲销交易的信息=====
    mpcbka_where_dict = {}
    mpcbka_where_dict['MSGFLGNO'] = TradeContext.ORMFN
    
    mpcbka_record = rccpsDBTrcc_mpcbka.selectu(mpcbka_where_dict)
    
    if(mpcbka_record == None):
        return AfaFlowControl.ExitThisFlow("S999","查询原冲销交易信息异常")
        
    if(len(mpcbka_record) <= 0):
        return AfaFlowControl.ExitThisFlow("S999","未找到原冲销交易信息,丢弃报文")
        
    #=====给机构号和柜员号赋值====
    TradeContext.BETELR = mpcbka_record['BETELR']
    TradeContext.BESBNO = mpcbka_record['BESBNO']
    
    AfaLoggerFunc.tradeInfo("<<<<<<更改柜员号，机构号结束")
    
        
    #更新冲销登记簿中心返回信息
    AfaLoggerFunc.tradeInfo(">>>开始更新冲销登记簿中心返回信息")
    
    mpcbka_update_dict = {}
    mpcbka_update_dict['PRCCO'] = TradeContext.PRCCO
    mpcbka_update_dict['STRINFO'] = TradeContext.STRINFO
    
    ret = rccpsDBTrcc_mpcbka.update(mpcbka_update_dict,mpcbka_where_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","更新冲销登记簿异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束更新冲销登记簿中心返回信息")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    #=====查询被冲销交易信息====
    AfaLoggerFunc.tradeInfo("<<<<<<开始查询被冲销的交易的信息")
    
    wtrbka_record = {}
    
    if not rccpsDBFunc.getTransWtr(mpcbka_record['BOJEDT'],mpcbka_record['BOSPSQ'],wtrbka_record):
        return AfaFlowControl.ExitThisFlow("S999","查询被冲销原交易详细信息异常")
        
    AfaLoggerFunc.tradeInfo("<<<<<<结束查询被冲销的交易的信息")
    
    #====为终端号和往来标识赋值====
    TradeContext.TERMID = wtrbka_record['TERMID']
    TradeContext.BRSFLG = wtrbka_record['BRSFLG']
    
    #=====判断对方行冲销是否成功=====
    AfaLoggerFunc.tradeInfo("<<<<<<判断对方行冲销是否成功PRCCO=[" + TradeContext.PRCCO + "]")
    if(TradeContext.PRCCO == 'RCCI0000' or TradeContext.PRCCO == 'RCCO1106'):
        AfaLoggerFunc.tradeInfo("<<<<<<对方行冲销成功")
        
        #=====发起主机记账====
        AfaLoggerFunc.tradeInfo("<<<<<<开始发起主机记账")
        
        #=====取最后一个记账成功状态的前置日期和前置流水号====
        stat_list = []
        
        if rccpsState.getTransStateSetm(wtrbka_record['BJEDTE'],wtrbka_record['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,stat_list):
            
            entries_dict = {}
            entries_dict['FEDT']     = stat_list[0]['FEDT']
            entries_dict['RBSQ']     = stat_list[0]['RBSQ']
            entries_dict['PYRACC']   = wtrbka_record['PYRACC']
            entries_dict['PYRNAM']   = wtrbka_record['PYRNAM']
            entries_dict['PYEACC']   = wtrbka_record['PYEACC']
            entries_dict['PYENAM']   = wtrbka_record['PYENAM']
            entries_dict['OCCAMT']   = wtrbka_record['OCCAMT']
            entries_dict['CHRGTYP']  = wtrbka_record['CHRGTYP']
            entries_dict['CUSCHRG']  = wtrbka_record['CUSCHRG']
            entries_dict['RCCSMCD']  = PL_RCCSMCD_CX
            TradeContext.BRSFLG      = wtrbka_record['BRSFLG']
            
            #卡折通存往账抹账会计分录赋值
            if wtrbka_record['TRCCO'] == '3000002' or wtrbka_record['TRCCO'] == '3000004':
                rccpsEntries.KZTCWZMZ(entries_dict)
            
            #卡折本转异往账抹账会计分录赋值
            if wtrbka_record['TRCCO'] == '3000003' or wtrbka_record['TRCCO'] == '3000005':
                rccpsEntries.KZBZYWZMZ(entries_dict)
                
            #卡折通兑往账抹账会计分录赋值
            if wtrbka_record['TRCCO'] == '3000102' or wtrbka_record['TRCCO'] == '3000104':
                rccpsEntries.KZTDWZMZ(entries_dict)
            
            #卡折异转本往账抹账会计分录赋值
            if wtrbka_record['TRCCO'] == '3000103' or wtrbka_record['TRCCO'] == '3000105':
                rccpsEntries.KZYZBWZMZ(entries_dict)
            
            
            #=====生成新的前置日期和前置流水号,并且更新到数据库中====
            if rccpsGetFunc.GetRBSQ(PL_BRSFLG_SND) == -1 :
                return AfaFlowControl.ExisThisFlow('S999',"产生新的前置流水号异常")
            
            #设置原交易状态为冲销处理中
            AfaLoggerFunc.tradeInfo('>>>开始设置原交易状态为冲销处理中')
            if not rccpsState.newTransState(mpcbka_record['BOJEDT'],mpcbka_record['BOSPSQ'],PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为冲销处理中异常")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                
            AfaLoggerFunc.tradeInfo('>>>结束设置原交易状态为冲销处理中')
            
            #=====调用主机接口函数=====
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            AfaLoggerFunc.tradeInfo("<<<<<<发起主机抹账结束")
            
        else:
            AfaLoggerFunc.tradeInfo(">>>原交易未记账,冲销不抹账")
            
            #设置原交易状态为冲销处理中
            AfaLoggerFunc.tradeInfo('>>>开始设置原交易状态为冲销处理中')
            if not rccpsState.newTransState(mpcbka_record['BOJEDT'],mpcbka_record['BOSPSQ'],PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为冲销处理中异常")
            
            if not AfaDBFunc.CommitSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return AfaFlowControl.ExitThisFlow("S999","Commit异常")
                
            AfaLoggerFunc.tradeInfo('>>>结束设置原交易状态为冲销处理中')
            
            TradeContext.errorCode = '0000'
            TradeContext.errorMsg  = '原交易未记账,冲销不抹账'
            
            
        #根据主机返回信息,设置交易状态
        
        stat_dict = {}
        stat_dict['BJEDTE'] = wtrbka_record['BJEDTE']
        stat_dict['BSPSQN'] = wtrbka_record['BSPSQN']
        stat_dict['MGID']   = TradeContext.errorCode
        stat_dict['STRINFO']= TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        if(TradeContext.errorCode == '0000'):
            #=====设置原交易状态为冲销成功====
            AfaLoggerFunc.tradeInfo("<<<<<<<开始更改原交易状态为冲销成功")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_CANC
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            if TradeContext.existVariable('TRDT'):
                stat_dict['TRDT']   = TradeContext.TRDT
            if TradeContext.existVariable('TLSQ'):
                stat_dict['TLSQ']   = TradeContext.TLSQ
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态冲销成功异常')
            
            AfaLoggerFunc.tradeInfo("<<<<<<<结束更改原交易状态为冲销成功")
            
        else:
            #=====设置原交易状态为冲销失败====
            AfaLoggerFunc.tradeInfo("<<<<<<<开始更改原交易状态为冲销失败")
            
            stat_dict['BCSTAT'] = PL_BCSTAT_CANC
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态冲销失败异常')
                
            AfaLoggerFunc.tradeInfo("<<<<<<<结束更改原交易状态为冲销失败")
            
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<对方行冲销拒绝应答,不设置原交易状态")
        
        ##设置原交易状态为冲销处理中
        #AfaLoggerFunc.tradeInfo('>>>开始设置原交易状态为冲销处理中')
        #
        #if not rccpsState.newTransState(wtrbka_record['BJEDTE'],wtrbka_record['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_WAIT):
        #    return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为冲销处理中异常")
        #
        #AfaLoggerFunc.tradeInfo('>>>结束设置原交易状态为冲销处理中')
        #
        #if not AfaDBFunc.CommitSql( ):
        #    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        #    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        #    
        ##=====设置原交易状态为冲销失败====
        #AfaLoggerFunc.tradeInfo("<<<<<<<开始更改原交易状态为冲销失败")
        #
        #stat_dict = {}
        #stat_dict['BJEDTE'] = wtrbka_record['BJEDTE']
        #stat_dict['BSPSQN'] = wtrbka_record['BSPSQN']
        #stat_dict['PRCCO']  = TradeContext.PRCCO
        #stat_dict['STRINFO']= TradeContext.STRINFO
        #stat_dict['BCSTAT'] = PL_BCSTAT_CANC
        #stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
        #
        #if not rccpsState.setTransState(stat_dict):
        #    return AfaFlowControl.ExitThisFlow('S999','设置业务状态冲销失败异常')
        #    
        #AfaLoggerFunc.tradeInfo("<<<<<<<结束更改原交易状态为冲销失败")
        
    
                
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.回执类操作(1.回执操作).通存通兑冲销应答报文接收[TRC004_1162]退出***' )
    
    return True
