# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).撤销申请应答报文接收
#===============================================================================
#   模板文件:   TRCC006.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-24
#   功    能：  接收撤销申请的应答，修改登记簿中原记录状态
################################################################################
#   修改人  :   关彬捷
#   修改内容:   修改登记数据库
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_ztcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1107CTradeContext2Dztcbka
import rccpsMap1106CTradeContext2Dtrccan_dict,rccpsDBTrcc_trccan,rccpsDBFunc,rccpsState,time
import rccpsDBTrcc_trcbka,rccpsHostFunc
#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    time.sleep(10)
    AfaLoggerFunc.tradeInfo('>>>进入撤销应答接收')
    #==========判断是否重复报文,如果是重复报文,直接进入下一流程================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    trccan_where_dict = {}
    trccan_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    trccan_where_dict['TRCDAT']   = TradeContext.TRCDAT
    trccan_where_dict['TRCNO']    = TradeContext.TRCNO

    trc_dict = rccpsDBTrcc_trccan.selectu(trccan_where_dict)

    if trc_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常")

    if len(trc_dict) > 0:
        AfaLoggerFunc.tradeInfo("汇兑查询查复自由格式登记簿中存在相同查复交易,此报文为重复报文,进入下一流程,发送表示成功的通讯回执")
        #======为通讯回执报文赋值===============================================
        out_context_dict = {}
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
        out_context_dict['STRINFO']  = '重复报文'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        TradeContext.SNDSTLBIN       = TradeContext.RCVMBRCO     #发起成员行号

        return True

    AfaLoggerFunc.tradeInfo(">>>结束检查是否重复报文")

    #==========根据发送行号,委托日期,交易流水号查询原交易信息===========
    AfaLoggerFunc.tradeInfo(">>>开始根据发送行号,委托日期,交易流水号查询交易信息")
    dict_where = {}
    dict_where['SNDBNKCO']  = TradeContext.OQTSBNK
    dict_where['TRCDAT']    = TradeContext.OCADAT
    dict_where['TRCNO']     = TradeContext.OCATNO

    dict = rccpsDBTrcc_trccan.selectu(dict_where)
    if dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常")

    tran_dict_where = {}
    tran_dict_where['BJEDTE']  =  dict['BOJEDT']
    tran_dict_where['BSPSQN']  =  dict['BOSPSQ']

    tran_dict = rccpsDBTrcc_trcbka.selectu(tran_dict_where)
    if tran_dict <= 0:
        return AfaFlowControl.ExitThisFlow("S999","未找到原交易")

    AfaLoggerFunc.tradeInfo(">>>结束根据发送行号,委托日期,交易流水号查询交易信息")

    #=====从TradeContext向字典trccan_dict赋值====
    TradeContext.BBSSRC  =  tran_dict['BBSSRC']
    TradeContext.BOJEDT  =  dict['BJEDTE']
    TradeContext.BOSPSQ  =  dict['BSPSQN']
    TradeContext.ORTRCCO =  dict['TRCCO']
    TradeContext.CUR     =  '01'
    TradeContext.OCCAMT  =  str(dict['OCCAMT'])

    AfaLoggerFunc.tradeDebug('>>>资金来源['+TradeContext.BBSSRC+']')

    trccan_dict = {}
    if not rccpsMap1106CTradeContext2Dtrccan_dict.map(trccan_dict):
        return AfaFlowControl.ExitThisFlow('S999','赋值错误')

    #=====插入登记簿rcc_trccan====
    AfaLoggerFunc.tradeDebug('>>>开始插入数据库')
    ret = rccpsDBTrcc_trccan.insertCmt(trccan_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999','插入数据库撤销申请登记簿trccan错误,抛弃报文') 

    #=====更新原撤销申请状态====
    trc_update = {}
    trc_update_where = {}
    trc_update_where['BJEDTE'] = TradeContext.BOJEDT
    trc_update_where['BSPSQN'] = TradeContext.BSPSQN
    trc_update['CLRESPN']= TradeContext.CLRESPN
    ret = rccpsDBTrcc_trccan.updateCmt(trc_update,trc_update_where)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow('S999','修改撤销申请登记簿原记录状态错误,抛弃报文')

    #=====原汇兑交易流水号,8820抹账使用====
    TradeContext.BOJEDT  =  tran_dict['BJEDTE']
    TradeContext.BOSPSQ  =  tran_dict['BSPSQN']

    #=====判断撤销应答标志是否允许撤销  0-允许撤销  1-不允许撤销 ====
    if TradeContext.CLRESPN  ==  '1':
        #=====发送接收正常回执====
        AfaLoggerFunc.tradeDebug('>>>中心不允许撤销,发送成功回执')
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
        return True

    AfaLoggerFunc.tradeDebug('>>>中心允许撤销,向主机发起记账')

    #=====设置sstlog表中原记录状态为：抹账-处理中====
    TradeContext.BCSTAT  = PL_BCSTAT_HCAC
    TradeContext.BDWFLG  = PL_BDWFLG_WAIT

    if not rccpsState.newTransState(dict['BOJEDT'],dict['BOSPSQ'],TradeContext.BCSTAT,TradeContext.BDWFLG):
        return AfaFlowControl.ExitThisFlow('S999','设置状态出错,抛弃此报文')
    
    #=====commit操作====
    AfaDBFunc.CommitSql()


    AfaLoggerFunc.tradeDebug('>>>开始向主机接口赋值')
    #=====设置主机记账/抹账数据====
    if TradeContext.BBSSRC == '3':
        #=====代销账要发起8813红蓝字记账====
        TradeContext.HostCode = '8813'
        TradeContext.RCCSMCD = '614'                                      #往撤销
        TradeContext.DASQ    = ''
        TradeContext.RVFG    = '0'                                        #红蓝字标志 0
        #关彬捷 20080728 修改抹账挂账原因
        #TradeContext.NOTE3   = '向主机发起红蓝字记账冲销'
        TradeContext.NOTE3   = '中心允许撤销,自动抹账'
        TradeContext.RBAC    =  TradeContext.BESBNO  +  PL_ACC_NXYDXZ     #贷方账号
        TradeContext.SBAC    =  TradeContext.BESBNO  +  PL_ACC_NXYDQSWZ   #借方账号
        #=====开始调函数拼贷方账号第25位校验位====
        TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
        AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
    else:
        TradeContext.HostCode = '8820'
        
        #关彬捷 20080728 修改抹账挂账原因
        #TradeContext.NOTE3   = '向主机发起抹账'
        TradeContext.NOTE3   = '中心允许撤销,自动抹账'

    AfaLoggerFunc.tradeDebug('>>>更新sstlog表中原交易状态成功,开始更新交易状态')
    #=====设置sstlog标志状态为:抹账-处理中====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
        return AfaFlowControl.ExitThisFlow('S999','设置状态出错,抛弃此报文')
    else:
        #=====commit操作====
        AfaDBFunc.CommitSql()

    AfaLoggerFunc.tradeDebug('>>>开始调用主机函数')
    AfaLoggerFunc.tradeDebug('>>>主机交易代码['+TradeContext.HostCode+']')
    #=====向主机发起抹账操作====
    rccpsHostFunc.CommHost(TradeContext.HostCode)
   
    #=====判断主机返回结果设置状态====
    sstlog_dict = {}
    sstlog_dict['BJEDTE'] = TradeContext.BJEDTE
    AfaLoggerFunc.tradeDebug('>>>交易日期['+TradeContext.BJEDTE+']')
    sstlog_dict['BSPSQN'] = TradeContext.BSPSQN
    AfaLoggerFunc.tradeDebug('>>>报单序号['+TradeContext.BSPSQN+']')
    sstlog_dict['BCSTAT']  = TradeContext.BCSTAT
    AfaLoggerFunc.tradeDebug('>>>业务状态['+TradeContext.BCSTAT+']')
    sstlog_dict['NOTE4']  = TradeContext.errorMsg
    AfaLoggerFunc.tradeDebug('>>>主机返回信息['+TradeContext.errorMsg+']')
    sstlog_dict['NOTE3']   = TradeContext.NOTE3
    AfaLoggerFunc.tradeDebug('>>>NOTE3['+TradeContext.NOTE3+']')
    AfaLoggerFunc.tradeDebug('>>>errorCode['+TradeContext.errorCode+']')
    if TradeContext.existVariable('TRDT'):
        sstlog_dict['TRDT']   = TradeContext.TRDT
        AfaLoggerFunc.tradeDebug('>>>主机日期['+TradeContext.TRDT+']')
    if TradeContext.existVariable('TLSQ'):
        sstlog_dict['TLSQ']   = TradeContext.TLSQ
        AfaLoggerFunc.tradeDebug('>>>主机流水['+TradeContext.TLSQ+']')

    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeDebug('>>>测试')

        if TradeContext.HostCode == '8813':
            sstlog_dict['DASQ']   = TradeContext.DASQ
            AfaLoggerFunc.tradeDebug('>>>销账序号['+TradeContext.DASQ+']')
            sstlog_dict['SBAC']   = TradeContext.SBAC
            AfaLoggerFunc.tradeDebug('>>>借方账号['+TradeContext.SBAC+']')
            sstlog_dict['RBAC']   = TradeContext.RBAC
            AfaLoggerFunc.tradeDebug('>>>贷方账号['+TradeContext.RBAC+']')

        AfaLoggerFunc.tradeDebug('>>>测试2')
        sstlog_dict['BDWFLG'] = PL_BDWFLG_SUCC
    else:
        AfaLoggerFunc.tradeDebug('>>>测试1')
        sstlog_dict['BDWFLG'] = PL_BDWFLG_FAIL

    AfaLoggerFunc.tradeDebug('>>>主机返回信息')
    #=====设置原交易状态====
    if not rccpsState.setTransState(sstlog_dict):
        return AfaFlowControl.ExitThisFlow('S999','更新主机返回信息出错,抛弃报文')
    
    #=====commit操作====
    AfaDBFunc.CommitSql()

    #=====设置交易状态====
    sstlog_dict['BJEDTE']  = TradeContext.BOJEDT
    sstlog_dict['BSPSQN']  = TradeContext.BOSPSQ

    if not rccpsState.setTransState(sstlog_dict):
        return AfaFlowControl.ExitThisFlow('S999','更新主机返回信息出错,抛弃报文')
    
    #=====commit操作====
    AfaDBFunc.CommitSql()


    #=====发送回执,其它错误====
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
    
    return True
#=====================交易后处理================================================
def SubModuleDoSnd():
    #=====判断afe返回结果====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    return True
