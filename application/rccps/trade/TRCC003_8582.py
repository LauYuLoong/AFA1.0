# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).自动冲正
#==============================================================================
#   交易文件:   TRCC003_8582.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-12-03
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_atcbka
import rccpsMap8582CTradeContext2Datcbka_dict


#=====================交易前处理(本地操作,中心前处理)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).自动冲正[TRCC003_8582]进入***' )
    
    #=====校验变量的合法性====
    if not TradeContext.existVariable("BOJEDT"):
        return AfaFlowControl.ExitThisFlow('A099','原交易日期不能为空')  
        
    if not TradeContext.existVariable("BOSPSQ"):
        return AfaFlowControl.ExitThisFlow('A099','原报单序号不能为空')
        
    #if not TradeContext.existVariable("RESNNM"):
    #    return AfaFlowControl.ExitThisFlow('A099','冲正原因不能为空')
    
    #查询原交易信息
    trc_dict = {}
    
    if rccpsDBFunc.getTransWtr(TradeContext.BOJEDT,TradeContext.BOSPSQ,trc_dict):
        AfaLoggerFunc.tradeInfo(">>>通存通兑登记簿中找到原交易")
        
    elif rccpsDBFunc.getTransMpc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trc_dict):
        AfaLoggerFunc.tradeInfo(">>>冲销登记簿中找到原交易")
        
    else:
        return AfaFlowControl.ExitThisFlow("S999","无此交易")
        
    #判断原交易是否为往账
    if( trc_dict['BRSFLG'] != PL_BRSFLG_SND):
        return AfaFlowControl.ExitThisFlow('A099','此交易非往账,禁止冲正')
        
    #判断被冲销交易的日期是否为当日
    if( trc_dict['NCCWKDAT'] != TradeContext.NCCworkDate ):
        return AfaFlowControl.ExitThisFlow('A099','此交易非当日交易,禁止冲正')
        
    #判断当前机构是否为原交易机构
    if( trc_dict['BESBNO'] != TradeContext.BESBNO ):
        return AfaFlowControl.ExitThisFlow('A099','当前机构非原交易机构,禁止冲正')
    
    #判断当前柜员是否为原交易柜员
    if( trc_dict['BETELR'] != TradeContext.BETELR ):
        return AfaFlowControl.ExitThisFlow('A099','当前柜员非原交易柜员,禁止冲正')
        
    if trc_dict['TRCCO'] in('3000002','3000003','3000004','3000005','3000102','3000103','3000104','3000105','3000505'):
        AfaLoggerFunc.tradeInfo(">>>原交易为通存或通兑账务类交易")
        
        #判断原交易当前状态是否可以冲正
        #原交易当前状态为:发送处理中,发送成功,记账失败,允许冲正
        if not ((trc_dict['BCSTAT'] == PL_BCSTAT_SND and (trc_dict['BDWFLG'] == PL_BDWFLG_WAIT or trc_dict['BDWFLG'] == PL_BDWFLG_SUCC)) or (trc_dict['BCSTAT'] == PL_BCSTAT_ACC) and trc_dict['BDWFLG'] == PL_BDWFLG_FAIL):
            return AfaFlowControl.ExitThisFlow("S999","此交易当前状态为[" + trc_dict['BCSTAT'] + "][" + trc_dict['BDWFLG'] + "],禁止冲正")
        
        #登记冲正登记簿
        AfaLoggerFunc.tradeInfo(">>>开始登记冲正登记簿")
        
        TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
        TradeContext.RCVMBRCO = trc_dict['RCVMBRCO']
        TradeContext.ORTRCDAT = trc_dict['TRCDAT']
        TradeContext.OPRNO    = PL_TDOPRNO_CZ
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.NCCworkDate + TradeContext.SerialNo
        TradeContext.ORMFN    = trc_dict['MSGFLGNO']
        TradeContext.TRCCO    = "3000506" 
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.ORTRCCO  = trc_dict['TRCCO']
        TradeContext.ORTRCNO  = trc_dict['TRCNO']
        TradeContext.SNDBNKCO = trc_dict['SNDBNKCO']
        TradeContext.SNDBNKNM = trc_dict['SNDBNKNM']
        TradeContext.RCVBNKCO = trc_dict['RCVBNKCO']
        TradeContext.RCVBNKNM = trc_dict['RCVBNKNM']
        
        insert_dict = {}
        
        rccpsMap8582CTradeContext2Datcbka_dict.map(insert_dict)
        
        ret = rccpsDBTrcc_atcbka.insertCmt(insert_dict)
        
        if( ret <= 0 ):
            return AfaFlowControl.ExitThisFlow('S999','登记自动冲正登记簿失败')
        
        AfaLoggerFunc.tradeInfo(">>>结束登记冲正登记簿")
        
        #若原交易当前状态非冲正处理中,则设置原交易状态为冲正处理中
        #if not (trc_dict['BCSTAT'] == PL_BCSTAT_CANCEL and trc_dict['BDWFLG'] == PL_BDWFLG_WAIT):
        #    AfaLoggerFunc.tradeInfo(">>>开始设置原交易状态为冲正处理中")
        #    
        #    if not rccpsState.newTransState(trc_dict['BJEDTE'],trc_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_WAIT):
        #        return AfaFlowControl.ExitThisFlow("S999","设置原交易当前状态为冲正处理中异常")
        #
        #    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为冲正处理中")
        #    
        #if not AfaDBFunc.CommitSql( ):
        #    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        #    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
        #为冲正报文做准备
        #=====报文头====
        TradeContext.MSGTYPCO = 'SET009'
        TradeContext.RCVSTLBIN= trc_dict['RCVMBRCO']
        #TradeContext.SNDBRHCO = TradeContext.BESBNO
        #TradeContext.SNDCLKNO = TradeContext.BETELR
        #TradeContext.SNDTRDAT = TradeContext.BJEDTE
        #TradeContext.SNDTRTIM = TradeContext.BJETIM
        #TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
        #TradeContext.ORMFN    = wtr_dict['MSGFLGNO']
        #TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.OPRTYPNO = "30"
        TradeContext.ROPRTPNO = "30"
        TradeContext.TRANTYP  = "0"
        #=====业务要素集====
        TradeContext.CUR      = trc_dict['CUR']
        TradeContext.OCCAMT   = str(trc_dict['OCCAMT'])
        
        #手续费处理
        if trc_dict['TRCCO'] == '3000002' or trc_dict['TRCCO'] == '3000003' or trc_dict['TRCCO'] == '3000004' or trc_dict['TRCCO'] == '3000005':
            TradeContext.CUSCHRG  = "0.00"
        elif trc_dict['TRCCO'] == '3000102' or trc_dict['TRCCO'] == '3000103' or trc_dict['TRCCO'] == '3000104' or trc_dict['TRCCO'] == '3000105':
            if trc_dict['CHRGTYP'] == '1':
                TradeContext.CUSCHRG = str(trc_dict['CUSCHRG'])
            else:
                TradeContext.CUSCHRG = '0.00'
                
        TradeContext.PYRACC   = trc_dict['PYRACC']
        TradeContext.PYRNAM   = trc_dict['PYRNAM']
        TradeContext.PYEACC   = trc_dict['PYEACC']
        TradeContext.PYENAM   = trc_dict['PYENAM']
        TradeContext.CURPIN   = ""
        TradeContext.STRINFO  = ""
        TradeContext.PRCCO    = ""
        #=====扩展要素集====
        TradeContext.RESNCO = TradeContext.RESNNM  
        
        
    elif trc_dict['TRCCO'] == '3000504':
        AfaLoggerFunc.tradeInfo(">>>原交易为冲销交易")
        
        if trc_dict['PRCCO'].lstrip() != "":
            return AfaFlowControl.ExitThisFlow("S999","已收到冲销应答,禁止冲正此冲销交易")
        
        wtr_dict = {}
        
        if not rccpsDBFunc.getTransWtr(trc_dict['BOJEDT'],trc_dict['BOSPSQ'],wtr_dict):
            return AfaFlowControl.ExitThisFlow("S999","通存通兑登记簿中未找到原被冲销交易")
            
        #若原被冲销交易当前状态为冲销,禁止冲正此冲销交易
        if wtr_dict['BCSTAT'] == PL_BCSTAT_CANC:
            return AfaFlowControl.ExitThisFlow("S999","原被冲销交易已被冲销成功或失败,禁止冲正此冲销交易")
            
        #登记冲正登记簿
        AfaLoggerFunc.tradeInfo(">>>开始登记冲正登记簿")
        
        TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
        TradeContext.RCVMBRCO = trc_dict['RCVMBRCO']
        TradeContext.ORTRCDAT = trc_dict['TRCDAT']
        TradeContext.OPRNO    = PL_TDOPRNO_CZ
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.NCCworkDate + TradeContext.SerialNo
        TradeContext.ORMFN    = trc_dict['MSGFLGNO']
        TradeContext.TRCCO    = "3000506"
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.ORTRCCO  = trc_dict['TRCCO']
        TradeContext.ORTRCNO  = trc_dict['TRCNO']
        TradeContext.SNDBNKCO = trc_dict['SNDBNKCO']
        TradeContext.SNDBNKNM = trc_dict['SNDBNKNM']
        TradeContext.RCVBNKCO = trc_dict['RCVBNKCO']
        TradeContext.RCVBNKNM = trc_dict['RCVBNKNM']
        
        insert_dict = {}
        
        rccpsMap8582CTradeContext2Datcbka_dict.map(insert_dict)
        
        ret = rccpsDBTrcc_atcbka.insertCmt(insert_dict)
        
        if( ret <= 0 ):
            return AfaFlowControl.ExitThisFlow('S999','登记自动冲正登记簿失败')
        
        AfaLoggerFunc.tradeInfo(">>>结束登记冲正登记簿")
        
        #为冲正报文做准备
        #=====报文头====
        TradeContext.MSGTYPCO = 'SET009'
        TradeContext.RCVSTLBIN= trc_dict['RCVMBRCO']
        #TradeContext.SNDBRHCO = TradeContext.BESBNO
        #TradeContext.SNDCLKNO = TradeContext.BETELR
        #TradeContext.SNDTRDAT = TradeContext.BJEDTE
        #TradeContext.SNDTRTIM = TradeContext.BJETIM
        #TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
        #TradeContext.ORMFN    = wtr_dict['MSGFLGNO']
        #TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.OPRTYPNO = "30"
        TradeContext.ROPRTPNO = "30"
        TradeContext.TRANTYP  = "0"
        #=====业务要素集====
        TradeContext.CUR      = wtr_dict['CUR']
        TradeContext.OCCAMT   = str(wtr_dict['OCCAMT'])
        
        #手续费处理
        if wtr_dict['TRCCO'] == '3000002' or wtr_dict['TRCCO'] == '3000003' or wtr_dict['TRCCO'] == '3000004' or wtr_dict['TRCCO'] == '3000005':
            TradeContext.CUSCHRG  = "0.00"
        elif wtr_dict['TRCCO'] == '3000102' or wtr_dict['TRCCO'] == '3000103' or wtr_dict['TRCCO'] == '3000104' or wtr_dict['TRCCO'] == '3000105':
            if wtr_dict['CHRGTYP'] == '1':
                TradeContext.CUSCHRG = str(wtr_dict['CUSCHRG'])
            else:
                TradeContext.CUSCHRG = '0.00'
                
        TradeContext.PYRACC   = wtr_dict['PYRACC']
        TradeContext.PYRNAM   = wtr_dict['PYRNAM']
        TradeContext.PYEACC   = wtr_dict['PYEACC']
        TradeContext.PYENAM   = wtr_dict['PYENAM']
        TradeContext.CURPIN   = ""
        TradeContext.STRINFO  = ""
        TradeContext.PRCCO    = ""
        #=====扩展要素集====
        TradeContext.RESNCO = TradeContext.RESNNM  
        
    else:
        return AfaFlowControl.ExitThisFlow("S999","原交易非通存或通兑账务类交易或冲销交易,禁止冲正")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).自动冲正[TRCC003_8582]进入***' )
    
    return True


#=====================交易后处理===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).自动冲正[TRCC003_8582]进入***' )
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    #判断是否发送成功
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo(">>>冲正报文发送成功")
        
    else:
        AfaLoggerFunc.tradeInfo(">>>冲正报文发送失败")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).自动冲正[TRCC003_8582]进入***' )
    
    return True
    
