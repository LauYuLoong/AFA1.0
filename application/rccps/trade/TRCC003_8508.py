# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作模板(1.本地操作 2.中心操作).紧急止付申请
#===============================================================================
#   交易文件:   TRCC003_8508.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsMap8508CTradeContext2Dexistp_dict,rccpsDBTrcc_existp,rccpsGetFunc
from types import *
from rccpsConst import *

#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('>>>开始进入紧急止付申请操作')
    #=====开始取交易流水信息====
    trcbka = {}
    ret = rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka)   
    if ret == False:
        return AfaFlowControl.ExitThisFlow('M999','取交易信息失败')

    AfaLoggerFunc.tradeInfo('trckba=' + str(trcbka))
    TRCCO  =  trcbka['TRCCO']

    #=====是否需要判断状态，何种状态允许此业务发送====
    if trcbka['BJEDTE'] != TradeContext.BJEDTE:
        return AfaFlowControl.ExitThisFlow('M999','当前交易日['+TradeContext.BJEDTE+']不允许发送紧急止付报文')
    if not (trcbka['BCSTAT'] == PL_BCSTAT_MFESTL and trcbka['BDWFLG'] == PL_BDWFLG_SUCC): 
        return AfaFlowControl.ExitThisFlow('M999','当前状态['+str(trcbka['BCSTAT'])+']不允许发送紧急止付报文')
    if TRCCO[0:2]  != '20': 
        return AfaFlowControl.ExitThisFlow('M999','当前业务交易码['+str(trcbka['TRCCO'])+']不允许发送紧急止付报文')
    if trcbka['BRSFLG'] != PL_BRSFLG_SND:
        return AfaFlowControl.ExitThisFlow('M999','当前往来标识['+str(trcbka['BRSFLG'])+']不允许发送紧急止付报文')

    #=====开始向字典赋值====
    TradeContext.ORTRCCO   = trcbka['TRCCO']
    TradeContext.CUR       = trcbka['CUR']
    TradeContext.OCCAMT    = trcbka['OCCAMT']
    TradeContext.RCVBNKCO  = trcbka['RCVBNKCO']
    TradeContext.RCVBNKNM  = trcbka['RCVBNKNM']
    existp_dict = {}
    if not rccpsMap8508CTradeContext2Dexistp_dict.map(existp_dict):
        return AfaFlowControl.ExitThisFlow('M999', '字典赋值出错')

    #=====开始插入撤销止付登记簿====
    if not rccpsDBTrcc_existp.insertCmt(existp_dict):
        return AfaFlowControl.ExitThisFlow('D002', '插入数据库出错,RollBack成功')
    else:
        AfaLoggerFunc.tradeInfo('COMMIT成功')

    #=====通过接收行号取成员行号和行名====
    TradeContext.RCVBNKCO = trcbka['RCVBNKCO']
    TradeContext.RCVBNKNM = trcbka['RCVBNKNM']
    rccpsGetFunc.GetRcvBnkCo(trcbka['RCVBNKCO'])
   
    #=====赋值取中心====
    TradeContext.ORTRCDAT = trcbka['TRCDAT']
    TradeContext.ORTRCNO  = trcbka['TRCNO']
    TradeContext.ORSNDBNK = trcbka['SNDBNKCO']
    TradeContext.ORRCVBNK = trcbka['RCVBNKCO']
    TradeContext.ORCUR    = trcbka['CUR']
    TradeContext.OROCCAMT = str(trcbka['OCCAMT'])
    TradeContext.ORTRCCO  = trcbka['TRCCO']
    TradeContext.OPRTYPNO = '99'
    TradeContext.ROPRTYPNO =TradeContext.ORTRCCO[0:2] 
    return True

#=====================交易后处理================================================
def SubModuleDoSnd():
    #=====判断afe返回====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)

    TradeContext.errorMsg  =  '报文发送成功' 
    
    return True
    
