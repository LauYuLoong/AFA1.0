# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).资金调拨申请
#===============================================================================
#   交易文件:   TRCC003_8544.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-23
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_mrqtbl
import rccpsMap8544CTradeContext2Dmrqtbl


#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).资金调拨申请[TRCC003_8544]进入***' )
    
    #=================必要性检查================================================
    AfaLoggerFunc.tradeInfo(">>>开始必要性检查")
    
    if TradeContext.BESBNO != PL_BESBNO_BCLRSB:
        return AfaFlowControl.ExitThisFlow('S999','本机构无此交易权限')
        
    AfaLoggerFunc.tradeInfo(">>>结束必要性检查")
    
    #=================登记资金调拨申请登记簿====================================
    AfaLoggerFunc.tradeInfo(">>>开始登记资金调拨申请登记簿")
    
    TradeContext.TRCCO    = "9900525"
    TradeContext.TRCDAT   = TradeContext.BJEDTE
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
    #TradeContext.RCVMBRCO = "1000000000"
    
    mrqtbl_dict = {}
    if not rccpsMap8544CTradeContext2Dmrqtbl.map(mrqtbl_dict):
        return AfaFlowControl.ExitThisFlow('S999','为资金调拨申请登记簿报文赋值异常')
        
    ret = rccpsDBTrcc_mrqtbl.insertCmt(mrqtbl_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999','登记资金调拨申请登记薄异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束登记资金调拨申请登记簿")
    
    #=================为资金调拨申请报文赋值====================================
    AfaLoggerFunc.tradeInfo(">>>开始为资金调拨申请报文赋值")
    
    TradeContext.MSGTYPCO = "SET008"
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.TRCNO
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "99"
    TradeContext.ROPRTPNO = ""
    TradeContext.TRANTYP  = "0"
    TradeContext.ORTRCCO  = ""
    
    AfaLoggerFunc.tradeInfo(">>>结束为资金调拨申请报文赋值")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).资金调拨申请[TRCC003_8544]进入***' )
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).资金调拨申请[TRCC003_8544]进入***' )
    
    #=================判断afe是否发送成功=======================================
    if TradeContext.errorCode != '0000':
        #=============AFE发送失败,设置PRCCO和STRINFO============================
        mrqtbl_where_dict = {}
        mrqtbl_where_dict['BJEDTE'] = TradeContext.BJEDTE
        mrqtbl_where_dict['BSPSQN'] = TradeContext.BSPSQN
        
        mrqtbl_update_dict = {}
        mrqtbl_update_dict['PRCCO']   = "S999"
        mrqtbl_update_dict['STRINFO'] = "发送AFE异常"
        return AfaFlowControl.ExitThisFlow('S999','AFE发送异常')
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).资金调拨申请[TRCC003_8544]退出***' )
    return True
    
