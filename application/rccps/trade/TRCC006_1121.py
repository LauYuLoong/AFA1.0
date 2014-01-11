# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).系统状态变更报文接收
#===============================================================================
#   模板文件:   TRCC006.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_mbrifa,rccpsMap0000Dout_context2CTradeContext,rccpsCronFunc


#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).系统状态变更报文接收[RCC00R6_1121]进入***' )
    
    #=================查询本地相关业务状态的系统状态============================
    mbrifa_where_dict = {}
    mbrifa_where_dict['OPRTYPNO'] = TradeContext.RELOPRTYPNO
    
    mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
    if mbrifa_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","查询本地系统状态信息异常")
        
    if  len(mbrifa_dict) <= 0:
        return AfaFlowControl.ExitThisFlow("S999","无相关业务类型本地系统状态信息")
    
    #=================校验报文新工作日期============================================
    if int(TradeContext.NWWKDAT) < int(mbrifa_dict['NWWKDAT']):
        AfaLoggerFunc.tradeInfo("报文新工作日期[" + TradeContext.NWWKDAT + "]在本地新工作日期[" + mbrifa_dict['NWWKDAT'] + "]之前,丢弃此报文,进入下一流程,发送表示成功的通讯回执")
        #======为通讯回执报文赋值===================================================
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        #out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        #out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        #out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '过期报文'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
        
    elif int(TradeContext.NWWKDAT) == int(mbrifa_dict['NWWKDAT']):
        #============报文新工作日期与本地新工作日期相同,校验报文新工作状态======
        if int(TradeContext.NWSYSST) <= int(mbrifa_dict['NWSYSST']):
            AfaLoggerFunc.tradeInfo("报文新工作状态[" + TradeContext.NWSYSST + "]不在本地新工作状态[" + mbrifa_dict['NWSYSST'] + "]之后,丢弃此报文,进入下一流程,发送表示成功的通讯回执")
            #======为通讯回执报文赋值===================================================
            out_context_dict = {}
            out_context_dict['sysType']  = 'rccpst'
            out_context_dict['TRCCO']    = '9900503'
            out_context_dict['MSGTYPCO'] = 'SET008'
            out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
            out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
            out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
            out_context_dict['SNDCLKNO'] = TradeContext.BETELR
            out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
            out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
            out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
            out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
            out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
            out_context_dict['OPRTYPNO'] = '99'
            out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
            out_context_dict['TRANTYP']  = '0'
            out_context_dict['ORTRCCO']  = TradeContext.TRCCO
            out_context_dict['PRCCO']    = 'RCCI0000'
            out_context_dict['STRINFO']  = '过期报文'
            
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
            
            return True
    
    #增加日切报文后发先至情况的处理
    #通存通兑顺序10-20-30-10
    if TradeContext.RELOPRTYPNO == "30":
        if mbrifa_dict['NWSYSST'] == '10' and TradeContext.NWSYSST != '20':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]业务当前业务状态为日间开始[10],但日切报文中变更状态非业务截止准备[20],停止处理")
            
        if mbrifa_dict['NWSYSST'] == '20' and TradeContext.NWSYSST != '30':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]业务当前业务状态为业务截止准备[20],但日切报文中变更状态非业务截止[30],停止处理")
            
        if mbrifa_dict['NWSYSST'] == '30' and TradeContext.NWSYSST != '10':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]业务当前业务状态为业务截止[30],但日切报文中变更状态非日间开始[10],停止处理")
    #汇兑汇票顺序10-30-10
    else:
        if mbrifa_dict['NWSYSST'] == '10' and TradeContext.NWSYSST != '30':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]业务当前业务状态为日间开始[10],但日切报文中变更状态非业务截止[30],停止处理")
            
        if mbrifa_dict['NWSYSST'] == '30' and TradeContext.NWSYSST != '10':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]业务当前业务状态为业务截止[30],但日切报文中变更状态非日间开始[10],停止处理")
    
    mbrifa_update_dict = {}
    mbrifa_update_dict['ORWKDAT'] = mbrifa_dict['NWWKDAT']
    mbrifa_update_dict['ORSYSST'] = mbrifa_dict['NWSYSST']
    mbrifa_update_dict['NWWKDAT'] = TradeContext.NWWKDAT
    mbrifa_update_dict['NWSYSST'] = TradeContext.NWSYSST
    mbrifa_update_dict['HOLFLG']  = TradeContext.HOLFLG
    mbrifa_update_dict['NOTE1']   = mbrifa_dict['NWWKDAT']
    
    ret = rccpsDBTrcc_mbrifa.update(mbrifa_update_dict,mbrifa_where_dict)
    if ret <= 0:
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback异常")
        AfaLoggerFunc.tradeInfo(">>>Rollback成功")
        return AfaFlowControl.ExitThisFlow("S999","更新系统状态异常")
    
    #======若新系统状态为业务截止,则打开对账系统调度============================
    if TradeContext.NWSYSST == '30' and TradeContext.HOLFLG == '2':
        if TradeContext.RELOPRTYPNO == '20':
            #====打开汇兑对账系统调度=======================================
            AfaLoggerFunc.tradeInfo(">>>开始打开汇兑对账系统调度")
            
            if not rccpsCronFunc.openCron("00031"):
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback异常")
                AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                return AfaFlowControl.ExitThisFlow("S999","打开汇兑对账系统调度异常")
                
            AfaLoggerFunc.tradeInfo(">>>结束打开汇兑对账系统调度")
            
            #====打开汇票对账系统调度=======================================
            AfaLoggerFunc.tradeInfo(">>>开始打开汇票对账系统调度")
            
            if not rccpsCronFunc.openCron("00041"):
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback异常")
                AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                return AfaFlowControl.ExitThisFlow("S999","打开汇票对账系统调度异常")
            
            AfaLoggerFunc.tradeInfo(">>>结束打开汇票对账系统调度")
            
        elif TradeContext.RELOPRTYPNO == '30':
            #====打开通存通兑对账系统调度===================================
            AfaLoggerFunc.tradeInfo(">>>开始打开通存通兑对账系统调度")
            
            if not rccpsCronFunc.openCron("00061"):
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback异常")
                AfaLoggerFunc.tradeInfo(">>>Rollback成功")
                return AfaFlowControl.ExitThisFlow("S999","打开通存通兑对账系统调度异常")
                
            AfaLoggerFunc.tradeInfo(">>>结束打开通存通兑对账系统调度")
            
            #====打开信息类业务量统计系统调度======================
            AfaLoggerFunc.tradeInfo(">>>开始打开信息类业务量统计系统调度")
            
#            if not rccpsCronFunc.openCron("00067"):
#                if not AfaDBFunc.RollbackSql( ):
#                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
#                    AfaLoggerFunc.tradeError(">>>Rollback异常")
#                AfaLoggerFunc.tradeInfo(">>>Rollback成功")
#                return AfaFlowControl.ExitThisFlow("S999","打开信息类业务量统计系统调度异常")
            
#            AfaLoggerFunc.tradeInfo(">>>结束打开信息类业务量统计系统调度")
            
            
            
    #======若通存通兑新系统状态为日间开始,则打开行名行号生效系统调度===================
    if TradeContext.NWSYSST == '10' and TradeContext.RELOPRTYPNO == '30':
        #====开始打开行名行号生效系统调度=======================================
        AfaLoggerFunc.tradeInfo(">>>开始打开行名行号生效系统调度")
        
        if not rccpsCronFunc.openCron("00050"):
            if not AfaDBFunc.RollbackSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeError(">>>Rollback异常")
            AfaLoggerFunc.tradeInfo(">>>Rollback成功")
            return AfaFlowControl.ExitThisFlow("S999","打开行名行号生效系统调度异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束打开行名行号生效系统调度")
            
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
    #======为通讯回执报文赋值===================================================
    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '成功'
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).系统状态变更报文接收[RCC00R6_1121]退出***' )
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).系统状态变更报文接收[RCC00R6_1121]进入***' )
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).系统状态变更报文接收[RCC00R6_1121]退出***' )
    return True
        
