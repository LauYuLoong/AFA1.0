# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作模板(1.本地操作 2.主机操作 3.中心操作).来账退汇
#===============================================================================
#   交易文件:   TRCC003_8509.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsDBTrcc_trcbka,rccpsState,rccpsHostFunc
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
    if trcbka_dict['BRSFLG'] != PL_BRSFLG_RCV:
        return AfaFlowControl.ExitThisFlow('M999','原交易为往帐业务，不允许退汇操作')
    if TradeContext.BESBNO != trcbka_dict["BESBNO"]:
        return AfaFlowControl.ExitThisFlow('M999','不允许跨机构退汇')
    if str(trcbka_dict['TRCCO']) == '2000009':
        return AfaFlowControl.ExitThisFlow('M999','特约汇兑业务不允许退汇')
    if str(trcbka_dict['TRCCO']) == '2000004':
        return AfaFlowControl.ExitThisFlow('M999','退汇业务不允许再次退汇')
    if str(trcbka_dict['TRCCO'])[0:2] != '20':
        return AfaFlowControl.ExitThisFlow('M999','非汇兑业务不允许退汇')
    if trcbka_dict["BCSTAT"] != PL_BCSTAT_HANG:   #自动挂账状态 1 成功
         return AfaFlowControl.ExitThisFlow('M999','当前业务状态为['+str(trcbka_dict["BCSTAT"])+']不允许退汇' )

    TradeContext.ORSNDBNK    = trcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNK    = trcbka_dict['RCVBNKCO']
    TradeContext.ORSNDBNKNM  = trcbka_dict['SNDBNKNM']
    TradeContext.ORRCVBNKNM  = trcbka_dict['RCVBNKNM']

    #=====开始插入数据库====
    trcbka_dict["BRSFLG"]    = TradeContext.BRSFLG
    trcbka_dict["BOJEDT"]    = trcbka_dict["BJEDTE"]
    trcbka_dict["BOSPSQ"]    = trcbka_dict["BSPSQN"]
    trcbka_dict["ORTRCDAT"]  = trcbka_dict["TRCDAT"]
    trcbka_dict["ORTRCCO"]   = trcbka_dict["TRCCO"] 
    trcbka_dict["ORTRCNO"]   = trcbka_dict["TRCNO"] 
    trcbka_dict["ORSNDBNK"]  = trcbka_dict["SNDBNKCO"]
    trcbka_dict["ORRCVBNK"]  = trcbka_dict["RCVBNKCO"]
    trcbka_dict["BJEDTE"]    = TradeContext.BJEDTE
    trcbka_dict["BSPSQN"]    = TradeContext.BSPSQN
    trcbka_dict["BJETIM"]    = TradeContext.BJETIM
    trcbka_dict["TRCDAT"]    = TradeContext.TRCDAT
    trcbka_dict["STRINFO"]   = TradeContext.STRINFO
    trcbka_dict["TRCCO"]     = TradeContext.TRCCO
    trcbka_dict["TRCNO"]     = TradeContext.SerialNo
    trcbka_dict["SNDBNKCO"]  = TradeContext.SNDBNKCO
    trcbka_dict["SNDBNKNM"]  = TradeContext.SNDBNKNM
    trcbka_dict["SNDMBRCO"]  = TradeContext.SNDSTLBIN
    trcbka_dict["RCVBNKCO"]  = TradeContext.RCVBNKCO
    trcbka_dict["RCVBNKNM"]  = TradeContext.RCVBNKNM
    trcbka_dict["RCVMBRCO"]  = TradeContext.RCVSTLBIN
    trcbka_dict["OPRNO"]     = "09"
    trcbka_dict["BBSSRC"]    = "3"
    trcbka_dict["BETELR"]    = TradeContext.BETELR
    trcbka_dict["TERMID"]    = TradeContext.TERMID
    
    #=====刘雨龙 2008-09-17 注释对业务类型的赋空操作====
    #trcbka_dict["OPRATTNO"]  = ""
    
    trcbka_dict["NCCWKDAT"]  = TradeContext.NCCworkDate
    trcbka_dict["SEAL"]      = ""

    #=====为发送退汇报文赋值====
    TradeContext.OPRTYPNO    =  '20'   #汇兑
    TradeContext.ORTRCCO     = trcbka_dict['ORTRCCO']
    TradeContext.ORTRCDAT    = trcbka_dict['ORTRCDAT']
    TradeContext.ORTRCNO     = trcbka_dict['ORTRCNO']
    TradeContext.ORPYRACC    = trcbka_dict['PYRACC']
    TradeContext.ORPYRNAM    = trcbka_dict['PYRNAM']
    TradeContext.ORPYEACC    = trcbka_dict['PYEACC']
    TradeContext.ORPYENAM    = trcbka_dict['PYENAM']
    TradeContext.PYRACC      = trcbka_dict['PYRACC']
    TradeContext.PYRNAM      = trcbka_dict['PYRNAM']
    TradeContext.PYRADDR     = trcbka_dict['PYRADDR']
    TradeContext.PYEACC      = trcbka_dict['PYEACC']
    TradeContext.PYENAM      = trcbka_dict['PYENAM']
    TradeContext.PYEADDR     = trcbka_dict['PYEADDR']
    
    
    
    AfaLoggerFunc.tradeInfo( '字典trccan_dict：' + str(trcbka_dict) )

    #=====开始插入数据库====
    if not rccpsDBFunc.insTransTrc(trcbka_dict):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D002', '插入数据库出错,RollBack成功')

    #=====commit操作====
    if not AfaDBFunc.CommitSql():
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D011', '数据库Commit失败')
    else:
        AfaLoggerFunc.tradeDebug('COMMIT成功')


    #=====设置sstlog表中状态为：记账-处理中====
    status = {}
    status['BJEDTE']     = TradeContext.BJEDTE
    status['BSPSQN']     = TradeContext.BSPSQN
    status['BCSTAT']     = PL_BCSTAT_ACC
    status['BDWFLG']     = PL_BDWFLG_WAIT

    if not rccpsState.setTransState(status):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit成功')

    #=====主机记账8813====
    TradeContext.HostCode  = '8813'
    TradeContext.OCCAMT    = str(trcbka_dict['OCCAMT'])     #金额
    TradeContext.RCCSMCD   = PL_RCCSMCD_LTH                 #主机摘要代码：来账退汇
    TradeContext.DASQ      = trcbka_dict['DASQ']
    #=====开始拼借贷方账号====
    TradeContext.RBAC =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ
    #TradeContext.SBAC =  TradeContext.BESBNO + PL_ACC_NXYDXZ

    #=====开始调函数拼贷方账号第25位校验位====
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
    #TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
    AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
    #AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )

    return True
#=====================中心后处理================================================
def SubModuleDoSnd():

    AfaLoggerFunc.tradeInfo( '>>>开始判断主机返回结果' )
    status_dict = {}
    status_dict['BSPSQN']  = TradeContext.BSPSQN       #报单序号
    status_dict['BJEDTE']  = TradeContext.BJEDTE       #交易日期
    status_dict['BCSTAT']  = PL_BCSTAT_ACC             #记账

    #=====判断主机返回结果====
    if TradeContext.errorCode != '0000':
        status_dict['BDWFLG']  = PL_BDWFLG_FAIL        #失败
        status_dict['STRINFO'] = TradeContext.errorMsg
        #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        status_dict['BDWFLG']  = PL_BDWFLG_SUCC        #成功
        status_dict['TRDT']    = TradeContext.TRDT     #主机日期
        status_dict['TLSQ']    = TradeContext.TLSQ     #主机流水号
        status_dict['MGID']    = TradeContext.MGID     #主机返回信息
        status_dict['DASQ']    = TradeContext.DASQ     #销账序号

    #=====修改退汇记录的状态====
    if not rccpsState.setTransState(status_dict):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit成功')

    #=====判断主机返回结果,是否继续流程====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow('D011', '该笔业务已入账，不允许退汇')
        #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)

    #=====新增记录的状态为：发送-处理中====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '设置状态失败,系统自动回滚')
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()

    #=====发送中心====
    TradeContext.ROPRTPNO  =  '20'

    return True
#=====================交易后处理================================================
def SubModuleDoTrd():
    AfaLoggerFunc.tradeDebug('>>>开始处理AFE返回结果')
    status = {}
    status['BSPSQN']  = TradeContext.BSPSQN       #报单序号
    status['BJEDTE']  = TradeContext.BJEDTE       #交易日期
    status['BCSTAT']  = PL_BCSTAT_SND             #发送
    #=====开始判断afe返回结果====
    if TradeContext.errorCode != '0000':
         status['BDWFLG']  = PL_BDWFLG_FAIL       #失败
         #==== 张恒增于20091216 退汇业务发送MFE失败更新原业务状态=====
         #===========退汇业务,更新原交易挂账代销账序号==============
         AfaLoggerFunc.tradeInfo(">>>开始更新原交易挂账代销账序号(8509)")
        
         orstat_dict = {}
         orstat_dict['BJEDTE'] = TradeContext.BOJEDT
         orstat_dict['BSPSQN'] = TradeContext.BOSPSQ
         orstat_dict['BCSTAT'] = PL_BCSTAT_HANG
         orstat_dict['BDWFLG'] = PL_BDWFLG_FAIL
         if TradeContext.existVariable('DASQ'):
            orstat_dict['DASQ']   = TradeContext.DASQ
        
         if not rccpsState.setTransState(orstat_dict):
            return False
            
         AfaLoggerFunc.tradeInfo(">>>结束更新原交易挂账代销账序号(8509)")
         
    else:
         status['BDWFLG']  = PL_BDWFLG_SUCC       #成功

    #=====修改退汇记录的状态====
    if not rccpsState.setTransState(status):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit成功')

    #关彬捷 2008-07-23
    #此处不更改原交易状态为退汇,在清算回执中修改
    ##=====设置原记录状态为：退汇－成功====
    #if not rccpsState.newTransState(TradeContext.BOJEDT,TradeContext.BOSPSQ,PL_BCSTAT_QTR,PL_BDWFLG_SUCC):
    #    #=====RollBack操作====
    #    AfaDBFunc.RollbackSql()
    #    return AfaFlowControl.ExitThisFlow('M999', '设置状态失败,系统自动回滚')
    #else:
    #    #=====commit操作====
    #    AfaDBFunc.CommitSql()

    
    return True
