# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作模板(1.本地操作 2.中心操作).撤销申请
#===============================================================================
#   交易文件:   TRCC003_8507.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsDBTrcc_trccan,rccpsMap8507Dtrcbka_dict2Dtrccan_dict
import rccpsMap8507Dtrccan_dict2CTradeContext
from types import *
from rccpsConst import *


#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    #====开始取流水号对应信息====
    trcbka_dict = {}
    dict = rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka_dict)
    if dict == False:
        return AfaFlowControl.ExitThisFlow('M999','取交易信息失败')

    #=====判断撤销信息====
    if TradeContext.BESBNO != trcbka_dict["BESBNO"]:
        return AfaFlowControl.ExitThisFlow('M999','不允许跨机构撤销')
    if TradeContext.BETELR != trcbka_dict["BETELR"]:
        return AfaFlowControl.ExitThisFlow('M999','不允许换柜员操作')
    if TradeContext.BJEDTE != trcbka_dict["BJEDTE"]:
        return AfaFlowControl.ExitThisFlow('M999','不允许隔日撤销')
    if trcbka_dict["BCSTAT"] != PL_BCSTAT_MFEQUE:  #41 排队状态 1 成功
         return AfaFlowControl.ExitThisFlow('M999','当前业务状态为['+trcbka_dict["BCSTAT"]+']不允许撤销' )
    if trcbka_dict["BRSFLG"] != PL_BRSFLG_SND:    #往帐
         return AfaFlowControl.ExitThisFlow('M999','当前业务状态为来账业务不允许撤销' )

    #=====开始插入数据库====
    trccan_dict = {}
    if not rccpsMap8507Dtrcbka_dict2Dtrccan_dict.map(trcbka_dict,trccan_dict):
         return AfaFlowControl.ExitThisFlow('M999','字典赋值错误')
    
    trccan_dict["CONT"]   = TradeContext.CONT
    trccan_dict["TRCCO"]  = TradeContext.TRCCO
    trccan_dict["BJEDTE"] = TradeContext.BJEDTE
    trccan_dict["BSPSQN"] = TradeContext.BSPSQN
    trccan_dict['CLRESPN'] = PL_ISDEAL_UNDO
    trccan_dict['RCVBNKCO'] = PL_RCV_CENTER
    trccan_dict['RCVBNKNM'] = PL_RCV_CENNAM 
    trccan_dict['RCVMBRCO'] = PL_RCV_CENTER
    trccan_dict['SNDMBRCO'] = TradeContext.SNDSTLBIN
    trccan_dict['TRCNO']    = TradeContext.SerialNo
    AfaLoggerFunc.tradeInfo( '字典trccan_dict：' + str(trccan_dict) )

    #=====开始插入撤销业务登记簿====
    ret = rccpsDBTrcc_trccan.insert(trccan_dict)
    if ret <= 0:
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D011','数据库ROLLBAKC失败')

    #=====commit操作====
    AfaDBFunc.CommitSql()
    AfaLoggerFunc.tradeInfo('>>>commit succ')

    #=====从字典向TradeContext赋值====
    if not rccpsMap8507Dtrccan_dict2CTradeContext.map(trccan_dict):
         return AfaFlowControl.ExitThisFlow('M999','字典赋值错误')

    #====手工赋值一些字段====
    TradeContext.OROCCAMT = str(TradeContext.OCCAMT)    #原交易金额
    AfaLoggerFunc.tradeDebug('>>>原交易金额' + str(TradeContext.OROCCAMT))
    TradeContext.ROPRTPNO = trcbka_dict['TRCCO'][:2]           #参考业务类型
    AfaLoggerFunc.tradeDebug('>>>参考业务类型' + TradeContext.ROPRTPNO)
    TradeContext.OPRTYPNO = '99'
    AfaLoggerFunc.tradeDebug('>>>业务类型' + TradeContext.OPRTYPNO)
    TradeContext.ORMFN    = str(trcbka_dict['SNDMBRCO']) + str(trcbka_dict['TRCDAT']) + str(trcbka_dict['TRCNO'])     #参考报文标识号
    AfaLoggerFunc.tradeDebug('>>>参考类型' + TradeContext.ORMFN)
    TradeContext.ORRCVBNK = trcbka_dict['RCVBNKCO']
    TradeContext.RCVBNKCO = PL_RCV_CENTER
    TradeContext.RCVBNKNM = PL_RCV_CENNAM 
    TradeContext.RCVSTLBIN = PL_RCV_CENTER
    TradeContext.ORTRCNO   = trcbka_dict['TRCNO']
    
    TradeContext.ORSNDBNKCO=trccan_dict['SNDBNKCO']
    AfaLoggerFunc.tradeInfo("TradeContext.ORSNDBNKCO:"+TradeContext.ORSNDBNKCO)
    AfaLoggerFunc.tradeInfo("TradeContext.BOSPSQ:"+TradeContext.BOSPSQ)

    return True
#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeDebug('>>>开始处理AFE返回结果')
    #=====开始判断afe返回结果====
    if TradeContext.errorCode != '0000':
         return AfaFlowControl.ExitThisFlow('M999','发送农信银中心失败')
    
    return True
    
