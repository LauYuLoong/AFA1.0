# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作模板(1.本地操作 2.中心回执).紧急止付 
#===============================================================================
#   交易文件:   TRCC006_1130.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-26
#   功    能：  紧急止付申请接收，判断是否可以止付，可以止付时主动发起退汇报文
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,AfaAfeFunc,rccpsMap0000Dout_context2CTradeContext,rccpsHostFunc
import rccpsDBTrcc_existp,rccpsMap1130CTradeContext2Dexistp


#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    #=====判断是否重复交易====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_existp.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','判断是否重复报文，查询汇兑业务登记簿相同报文异常')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('紧急止付业务登记簿中存在相同数据,重复报文,进入下一流程')
        #=====为通讯回执报文赋值====
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
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = trc_dict['TRCCO']
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '重复报文'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        #=====发送afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','重复报文，退出处理流程')

    #=====根据发送行号,委托日期,交易流水号查询原交易信息===========
    AfaLoggerFunc.tradeInfo(">>>开始根据发送行号,委托日期,交易流水号查询交易信息")
    trc_dict = {}
    if not rccpsDBFunc.getTransTrcPK(TradeContext.SNDMBRCO,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,trc_dict):
        return AfaFlowControl.ExitThisFlow('S999','汇兑业务登记簿中无此交易,抛弃报文') 

    AfaLoggerFunc.tradeInfo(">>>结束根据发送行号,委托日期,交易流水号查询交易信息")

    #=====需要插入紧急止付业务登记簿existp====
    existp = {}
    if not rccpsMap1130CTradeContext2Dexistp.map(existp):
        return AfaFlowControl.ExitThisFlow('S999','字典赋值出错,抛弃报文')

    existp['BOJEDT']  =  trc_dict['BJEDTE']
    existp['BOSPSQ']  =  trc_dict['BSPSQN']
    existp['CUR']     =  '01'
    
    #=====张恒 20091203 新增 将机构落到原交易机构 ====
    existp['BESBNO']     =  trc_dict['BESBNO']
    
    ret = rccpsDBTrcc_existp.insertCmt(existp)
    if ret < 0:
        return AfaFlowControl.ExitThisflow('S999','插入止付业务登记簿出错,抛弃报文')

    #======检查原业务状态是否为自动挂账－成功====
    #if not (trc_dict['BCSTAT'] != PL_BCSTAT_HANG and trc_dict['BDWFLG'] != PL_BDWFLG_SUCC ):
    if (trc_dict['BCSTAT'] != PL_BCSTAT_HANG or trc_dict['TRCCO'][:2] != '20' or trc_dict['TRCCO'] == '2000009'):
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
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = trc_dict['TRCCO']
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '该笔业务已入账，不允许退汇'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #发起成员行号

        #=====发送afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','重复报文，退出处理流程')

    TradeContext.BOSPSQ   = trc_dict['BSPSQN']
    TradeContext.BOJEDT   = trc_dict['BJEDTE']
    TradeContext.ORPYRACC = trc_dict['PYRACC']
    TradeContext.ORPYRNAM = trc_dict['PYRNAM']
    TradeContext.ORPYEACC = trc_dict['PYEACC']
    TradeContext.ORPYENAM = trc_dict['PYENAM']
    TradeContext.ORTRCCO  = trc_dict['TRCCO']

    #=====汇兑业务登记簿trcbka赋值新增一条记录====
    trc_dict['BOJEDT']  =  trc_dict['BJEDTE']
    trc_dict['BOSPSQ']  =  trc_dict['BSPSQN']
    trc_dict['ORTRCDAT']=  trc_dict['TRCDAT']
    trc_dict['ORTRCNO'] =  trc_dict['TRCNO']
    trc_dict['ORTRCCO'] =  trc_dict['TRCCO']
    trc_dict['TRCCO']   =  '2000004'
    trc_dict['OPRNO']   =  '09'
    trc_dict['DCFLG']   =  PL_DCFLG_CRE
    trc_dict['BJEDTE']  =  TradeContext.BJEDTE
    trc_dict['BSPSQN']  =  TradeContext.BSPSQN
    trc_dict['TRCDAT']  =  TradeContext.TRCDAT
    trc_dict['TRCNO']   =  TradeContext.SerialNo
    trc_dict['BRSFLG']  =  PL_BRSFLG_SND                  #往账
    trc_dict['BBSSRC']  =  '3'                            #待销账
    #=====接收成员行号与发送成员行号互换====
    TradeContext.temp   =  trc_dict['SNDMBRCO']
    trc_dict['SNDMBRCO']=  trc_dict['RCVMBRCO']
    trc_dict['RCVMBRCO']=  TradeContext.temp 

    #=====接收行号与发送行号互换====
    TradeContext.temp   =  trc_dict['SNDBNKCO']
    trc_dict['SNDBNKCO']=  trc_dict['RCVBNKCO']
    trc_dict['RCVBNKCO']=  TradeContext.temp 

    #=====接收行名与发送行名互换====
    TradeContext.temp   =  trc_dict['SNDBNKNM']
    trc_dict['SNDBNKNM']=  trc_dict['RCVBNKNM']
    trc_dict['RCVBNKNM']=  TradeContext.temp 

    #=====开始插入数据库====
    if not rccpsDBFunc.insTransTrc(trc_dict):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D002', '插入数据库出错,RollBack成功')
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('插入汇兑业务登记簿，COMMIT成功')

    #=====设置状态为记账-处理中====
    sstlog   = {}
    sstlog['BSPSQN']   = TradeContext.BSPSQN
    sstlog['BJEDTE']   = TradeContext.BJEDTE
    sstlog['BCSTAT']   = PL_BCSTAT_ACC
    sstlog['BDWFLG']   = PL_BDWFLG_WAIT

    if not rccpsState.setTransState(sstlog):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit成功')

    #=====开始拼借贷方账号====
    TradeContext.DASQ  = trc_dict['DASQ']
    TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ
    TradeContext.OCCAMT= TradeContext.OROCCAMT
    TradeContext.HostCode = '8813'

    #=====开始调函数拼贷方账号第25位校验位====
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
    AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
 
    rccpsHostFunc.CommHost(TradeContext.HostCode)

    AfaLoggerFunc.tradeInfo( '>>>开始判断主机返回结果' )
    status_dict = {}
    status_dict['BSPSQN']  = TradeContext.BSPSQN       #报单序号
    status_dict['BJEDTE']  = TradeContext.BJEDTE       #交易日期
    status_dict['BCSTAT']  = PL_BCSTAT_ACC             #记账

    #=====判断主机返回结果====
    if TradeContext.errorCode != '0000':
        status_dict['BDWFLG']  = PL_BDWFLG_FAIL        #失败
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
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.TRCDAT
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.ORTRCCO 
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '该笔业务已入账，不允许退汇'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #发起成员行号

        #=====发送afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','该笔业务已被主机处理，不允许退汇')

    #=====新增记录的状态为：发送-处理中====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '设置状态失败,系统自动回滚')
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()

    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.TRCDAT
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.ORTRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '成功'

    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

    TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #发起成员行号

    return True
#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeDebug('>>>开始处理AFE返回结果')
    status = {}
    status['BSPSQN']  = TradeContext.BSPSQN       #报单序号
    status['BJEDTE']  = TradeContext.BJEDTE       #交易日期
    status['BCSTAT']  = PL_BCSTAT_SND             #发送
    status['STRINFO'] = TradeContext.errorMsg
    #=====开始判断afe返回结果====
    if TradeContext.errorCode != '0000':
        status['BDWFLG']       = PL_BDWFLG_FAIL       #失败
    else:
        status['BDWFLG']       = PL_BDWFLG_SUCC       #成功

    #=====修改退汇记录的状态====
    if not rccpsState.setTransState(status):
        #=====RollBack操作====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()

    AfaLoggerFunc.tradeDebug('>>>通讯回执处理成功')
    
    #=====发送退汇报文2000004====
    TradeContext.sysType  = 'rccpst'
    TradeContext.TRCCO    = '2000004'
    TradeContext.MSGTYPCO = 'SET005'
    TradeContext.OPRTYPNO =  '20'   #汇兑
    TradeContext.STRINFO  = '收到紧急止付,系统自动退汇' 
   
    #=====接收行号与发送行号互换====
    TradeContext.TEMP     = TradeContext.RCVBNKCO
    TradeContext.RCVBNKCO = TradeContext.SNDBNKCO
    TradeContext.SNDBNKCO = TradeContext.TEMP

    #=====接收行名与发送行名互换====
    TradeContext.NAME     = TradeContext.RCVBNKNM
    TradeContext.RCVBNKNM = TradeContext.SNDBNKNM
    TradeContext.SNDBNKNM = TradeContext.NAME

    #=====发送afe====
    AfaAfeFunc.CommAfe()

    #=====开始判断afe返回结果====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        AfaLoggerFunc.tradeDebug('>>>发送退汇成功')

    return True
