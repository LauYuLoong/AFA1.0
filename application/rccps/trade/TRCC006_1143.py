# -*- coding: gbk -*-
###############################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).存款确认请求报文接收
#==============================================================================
#   交易文件:   TRCC006_1143.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷 
#   修改时间:   2008-11-03
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc
import rccpsDBTrcc_wtrbka


#=====================交易前处理(登记流水,中心前处理)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).存款确认请求报文接收[TRCC006_1143]进入***' )
    
    #判断是否重复报文
    AfaLoggerFunc.tradeInfo(">>>开始判断是否重复报文")
    
    sel_dict = {'COTRCNO':TradeContext.TRCNO,'COTRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_wtrbka.selectu(sel_dict)
    
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','判断是否重复存款确认报文,查询通存通兑业务登记簿相同报文异常')
        
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('通存通兑业务登记簿中存在相同数据,重复报文,返回应答报文')
        TradeContext.STRINFO  = "重复报文"
    else:
        #查询原存款交易信息
        AfaLoggerFunc.tradeInfo(">>>非重复报文,开始查询原存款交易信息")
        
        wtrbka_dict = {}
        
        if not rccpsDBFunc.getTransWtrAK(TradeContext.SNDBNKCO,TradeContext.TRCDAT,TradeContext.ORTRCNO,wtrbka_dict):
            AfaFlowControl.ExitThisFlow('S999',"查询原存款交易信息异常")
            
        TradeContext.BJEDTE = wtrbka_dict['BJEDTE']
        TradeContext.BSPSQN = wtrbka_dict['BSPSQN']
        TradeContext.PYEACC = wtrbka_dict['PYEACC']
        TradeContext.PYENAM = wtrbka_dict['PYENAM']
        TradeContext.OCCAMT = wtrbka_dict['OCCAMT']
        TradeContext.BESBNO = wtrbka_dict['BESBNO']
        
        AfaLoggerFunc.tradeInfo(">>>结束查询原存款交易信息")
        
        
        #检查交易当前状态是否为确认入账成功,非此状态则丢弃报文
        AfaLoggerFunc.tradeInfo(">>>开始判断交易当前状态是否为确认入账成功")
        
        stat_dict = {}
        
        if not rccpsState.getTransStateCur(TradeContext.BJEDTE,TradeContext.BSPSQN,stat_dict):
            return AfaFlowControl.ExitThisFlow('S999',"获取原存款交易当前状态异常")
            
        #if not (stat_dict['BCSTAT'] == PL_BCSTAT_CONFACC and stat_dict['BDWFLG'] == PL_BDWFLG_SUCC):
        #    return AfaFlowControl.ExitThisFlow('S999',"原存款交易当前状态非确认入账成功,丢弃报文")
        
        AfaLoggerFunc.tradeInfo(">>>结束判断交易当前状态是否为确认入账成功")
        
        #更新通存通兑登记簿存款确认相关信息
        AfaLoggerFunc.tradeInfo(">>>开始更新通存通兑登记簿存款确认相关信息")
        
        wtrbka_where_dict = {}
        wtrbka_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
            
        wtrbka_update_dict = {}
        wtrbka_update_dict = {'COTRCDAT':TradeContext.TRCDAT,'COTRCNO':TradeContext.TRCNO,'COMSGFLGNO':TradeContext.MSGFLGNO}
            
        ret = rccpsDBTrcc_wtrbka.update(wtrbka_update_dict,wtrbka_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow('S999',"更新通存通兑登记簿存款确认相关信息异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束更新通存通兑登记簿存款确认相关信息")
        
        
        #设置业务状态为自动入账处理中
        AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为自动入账处理中")
        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CONFACC,PL_BDWFLG_WAIT):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态为自动入账处理中异常')
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            
        AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为自动入账处理中")
        
        #发起主机记账
        AfaLoggerFunc.tradeInfo(">>>开始发起主机记账")
        
        TradeContext.HostCode = '8813'                               #调用8813主机接口
        TradeContext.RCCSMCD  = PL_RCCSMCD_HDLZ                      #主机摘要代码：汇兑来账
        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #借方账户:农信银待清算来账
        TradeContext.SBNM = "农信银待清算来账"
        TradeContext.RBAC = TradeContext.PYEACC                      #贷方账户:收款人账户
        TradeContext.RBNM = TradeContext.PYENAM                      #贷方户名:收款人户名
        TradeContext.OCCAMT = str(TradeContext.OCCAMT)
        
        #=====add by pgt 12-5====
        TradeContext.CTFG = '7'                                      #本金 手续费标识  7 本金 8手续费 9 本金＋手续费 
        TradeContext.PKFG = 'T'                                      #通存通兑标识                                   
        
        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
        
        AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo(">>>结束发起主机记账")
        
        #根据主机返回码,设置业务状态为自动入账成功或失败
        AfaLoggerFunc.tradeInfo(">>>开始根据主机返回码,设置业务状态为自动入账成功或失败")
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BJETIM']  = TradeContext.BJETIM
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['SBAC']    = TradeContext.SBAC
        stat_dict['ACNM']    = TradeContext.SBNM
        stat_dict['RBAC']    = TradeContext.RBAC
        stat_dict['OTNM']    = TradeContext.RBNM
        stat_dict['PRCCO']   = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("主机返回码[" + TradeContext.errorCode + "],主机返回信息[" + TradeContext.errorMsg +"]")
        if TradeContext.errorCode == '0000':
            #=====发送农信银成功,设置状态为自动入账成功====
            stat_dict['TRDT']    = TradeContext.TRDT
            stat_dict['TLSQ']    = TradeContext.TLSQ
            stat_dict['BCSTAT']  = PL_BCSTAT_AUTO
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            TradeContext.STRINFO = '成功'
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为自动入账成功异常")
            
            AfaLoggerFunc.tradeInfo(">>>设置业务状态为自动入账成功完成")
        else:
            #=====发送农信银失败,设置状态为自动入账失败====       
            stat_dict['BCSTAT']  = PL_BCSTAT_AUTO
            stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
            TradeContext.STRINFO = '行内自动入账失败'
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为自动入账失败异常")
            
            AfaLoggerFunc.tradeInfo(">>>设置业务状态为自动入账失败完成")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    #为存款确认应答报文赋值
    TradeContext.sysType  = 'rccpst'
    TradeContext.MSGTYPCO = 'SET010'
    TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO
    TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    #TradeContext.SNDTRDAT = TradeContext.BJEDTE
    #TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.ORMFN    = TradeContext.MSGFLGNO
    #TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.SerialNo
    #TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = '30'
    TradeContext.ROPRTPNO = TradeContext.OPRTYPNO
    TradeContext.TRANTYP  = '0'
    
    TradeContext.CUR      = 'CNY'
    TradeContext.PRCCO    = 'RCCI0000'
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).存款确认请求报文接收[TRCC006_1143]退出***' )
    
    return True


#=====================交易后处理===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).存款确认请求报文接收[TRCC006_1143]进入***' )
    
    #根据afe返回码判断存款确认应答报文是否发送成功,并记录日志
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo(">>>存款确认应答报文发送成功")
    else:
        AfaLoggerFunc.tradeInfo(">>>存款确认应答报文发送失败,等待对方冲正或冲销")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).存款确认请求报文接收[TRCC006_1143]退出***' )
    
    return True
        
