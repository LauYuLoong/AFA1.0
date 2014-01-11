# -*- coding: gbk -*-
###############################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).折通存请求报文接收
#==============================================================================
#   交易文件:   TRCC006_1136.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷  
#   修改时间:   2008-10-29
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc  
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_atcbka
import rccpsMap1136CTradeContext2Dwtrbka_dict


#=====================交易前处理(登记流水,中心前处理)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).折通存请求报文接收[TRCC006_1136]进入***' )
    
    #判断是否重复交易
    AfaLoggerFunc.tradeInfo(">>>开始判断是否重复报文")
    
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_wtrbka.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','判断是否重复报文，查询通存通兑业务登记簿相同报文异常')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('通存通兑业务登记簿中存在相同数据,重复报文,返回拒绝应答报文')
        #=====为应答报文赋值====
        TradeContext.sysType  = 'rccpst'
        TradeContext.MSGTYPCO = 'SET006'
        TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO
        TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO
        TradeContext.SNDBRHCO = TradeContext.BESBNO
        TradeContext.SNDCLKNO = TradeContext.BETELR
        #TradeContext.SNDTRDAT = TradeContext.BJEDTE
        #TradeContext.SNDTRTIM = TradeContext.BJETIM
        TradeContext.ORMFN    = TradeContext.MSGFLGNO
        #TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.SerialNo
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.OPRTYPNO = '30'
        TradeContext.ROPRTPNO = TradeContext.OPRTYPNO
        TradeContext.TRANTYP  = '0'
    
        TradeContext.CUR      = 'CNY'
        TradeContext.PRCCO    = 'NN1IM101'
        TradeContext.STRINFO  = "重复报文"

        #=====发送afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','重复报文，退出处理流程')

    AfaLoggerFunc.tradeInfo(">>>结束判断是否重复报文")
    
    #登记通存通兑登记簿
    AfaLoggerFunc.tradeInfo(">>>开始登记通存通兑业务登记簿")
    
    #=====币种转换====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'
        
    #=====手续费收取方式=====
    if float(TradeContext.CUSCHRG) > 0.001:
        TradeContext.CHRGTYP = '1'
    else:
        TradeContext.CHRGTYP = '0'
        
    #====开始向字典赋值====
    wtrbka_dict = {}
    if not rccpsMap1136CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('M999', '字典赋值出错')
    
    wtrbka_dict['DCFLG'] = PL_DCFLG_CRE                  #借贷标识
    wtrbka_dict['OPRNO'] = PL_TDOPRNO_TC                 #业务种类
    
    #=====开始插入数据库====
    if not rccpsDBFunc.insTransWtr(wtrbka_dict):
        return False
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束登记通存通兑业务登记簿")
    
    #设置业务状态为行内收妥成功
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为收妥成功")
    
    stat_dict   = {}
    stat_dict['BSPSQN']   = TradeContext.BSPSQN
    stat_dict['BJEDTE']   = TradeContext.BJEDTE
    stat_dict['BCSTAT']   = PL_BCSTAT_BNKRCV
    stat_dict['BDWFLG']   = PL_BDWFLG_SUCC
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','设置业务状态收妥成功异常')
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为收妥成功")
    
    #设置业务状态为确认入账处理中
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为确认入账处理中")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_CONFACC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为确认入账处理中异常')
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为确认入账处理中")
    
    #初始化返回码
    TradeContext.PRCCO = 'RCCI0000'
    TradeContext.STRINFO = "成功"
    TradeContext.BCSTAT = PL_BCSTAT_CONFACC #状态:确认付款
    TradeContext.BCSTATNM = "确认付款"
    #进行必要性检查,若校验通过,则返回成功应答报文,若校验未通过,则返回拒绝应答报文
    AfaLoggerFunc.tradeInfo(">>>开始必要性检查")
    AfaLoggerFunc.tradeInfo(">>>查询主机账户成功")

    #检查冲正登记簿中是否有此笔业务的冲正业务,存在则返回拒绝应答报文,并设置业务状态为冲正处理中
    if TradeContext.PRCCO == 'RCCI0000':
        atcbka_where_dict = {}
        atcbka_where_dict['ORMFN'] = TradeContext.MSGFLGNO

        atcbka_dict = rccpsDBTrcc_atcbka.selectu(atcbka_where_dict)
        
        if atcbka_dict == None:
            #return AfaFlowControl.ExitThisFlow('S999', "查询冲正登记簿异常")
            AfaLoggerFunc.tradeInfo(">>>查询冲正登记簿异常")
            TradeContext.PRCCO = 'NN1ID003'
            TradeContext.STRINFO = "系统错误,查询冲正登记簿异常"
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
        
        else:
            if len(atcbka_dict) <= 0:
                AfaLoggerFunc.tradeInfo(">>>此交易未被冲正,继续校验")

            else:
                AfaLoggerFunc.tradeInfo(">>>此交易已被冲正,返回拒绝应答报文")
                TradeContext.PRCCO = 'NN1IO307'
                TradeContext.STRINFO = "此交易已被冲正"
                TradeContext.BCSTAT = PL_BCSTAT_CANC

    #唐斌新增#
    sql = "SELECT ischkactname,ischklate FROM rcc_chlabt where transcode='"+TradeContext.TransCode+"' and channelno= '"+(TradeContext.SNDCLKNO)[6:8]+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql( sql)
    if (records == None):
        return False
    elif (len(records) == 0):
        AfaLoggerFunc.tradeDebug("查询结果为空,查询条件[" + sql + "]")
        return False
    AfaLoggerFunc.tradeDebug(str(records))
        
    #校验账户状态是否正常和账号户名是否相符
    if TradeContext.PRCCO == 'RCCI0000':
    
        #调用主机接口查询账户信息
        TradeContext.HostCode = '8810'

        TradeContext.ACCNO = TradeContext.PYEACC
        #TradeContext.WARNTNO = TradeContext.BNKBKNO

        AfaLoggerFunc.tradeDebug("ACCNO :" + TradeContext.ACCNO)
        #AfaLoggerFunc.tradeDebug("WARNTNO :" + TradeContext.WARNTNO)

        rccpsHostFunc.CommHost( TradeContext.HostCode )

        if TradeContext.errorCode != '0000':
            #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
            AfaLoggerFunc.tradeInfo("查询账户信息异常,主机返回码[" + TradeContext.errorCode + "],主机返回信息[" + TradeContext.errorMsg +"]")
            TradeContext.PRCCO = rccpsDBFunc.HostErr2RccErr(TradeContext.errorCode)
            TradeContext.STRINFO = "查询主机账户信息失败 " + TradeContext.errorMsg
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
        else:
            AfaLoggerFunc.tradeInfo(">>>查询主机账户成功")
            
            #if TradeContext.BESBNO != PL_BESBNO_BCLRSB:
            #    AfaLoggerFunc.tradeInfo(">>>" + TradeContext.BESBNO + ">>>" + TradeContext.ACCSO)
            #    if( TradeContext.BESBNO[:6] != TradeContext.ACCSO[:6] ):
            #        AfaLoggerFunc.tradeInfo(">>>不许跨法人做此交易")
            #        TradeContext.PRCCO = 'NN1IO999'
            #        TradeContext.STRINFO = "接收行与账户开户行不属于同一法人"
            #        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            #        TradeContext.BCSTATNM = "拒绝"
            
            #检查本机构是否有通存通兑业务权限
            if not rccpsDBFunc.chkTDBESAuth(TradeContext.ACCSO):
                TradeContext.PRCCO = 'NN1IO999'
                TradeContext.STRINFO = "本账户开户机构无通存通兑业务权限"
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "拒绝"
            
            if TradeContext.PRCCO == 'RCCI0000':
                AfaLoggerFunc.tradeInfo(">>>开始更新机构号为开户机构")
                TradeContext.BESBNO = TradeContext.ACCSO
                wtrbka_update_dict = {'BESBNO':TradeContext.ACCSO}
                wtrbka_where_dict  = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
                ret = rccpsDBTrcc_wtrbka.updateCmt(wtrbka_update_dict,wtrbka_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo(">>>更新机构号为开户机构异常")
                    TradeContext.PRCCO = 'RCCI1000'
                    TradeContext.STRINFO = "系统错误,更新账务机构号异常"
                    TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "拒绝"
                
                else:
                    AfaLoggerFunc.tradeInfo(">>>更新机构号为开户机构成功")
                    AfaLoggerFunc.tradeDebug("主机返回户名ACCNM :[" + TradeContext.ACCNM + "]")
                    AfaLoggerFunc.tradeDebug("报文接收户名PYENAM:[" + TradeContext.PYENAM + "]")
                    AfaLoggerFunc.tradeDebug("主机返回账户状态ACCST:[" + TradeContext.ACCST + "]")
                    
                    
                    if TradeContext.ACCNM != TradeContext.PYENAM:
                        #唐斌新增#
                        if(records[0][0]=='1'):
                            AfaLoggerFunc.tradeInfo(">>>账号户名不符")
                            TradeContext.PRCCO = 'NN1IA102'
                            TradeContext.STRINFO = '账号户名不符'
                            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                            TradeContext.BCSTATNM  = "拒绝"
                    
                    elif TradeContext.ACCST != '0' and TradeContext.ACCST != '2':
                        AfaLoggerFunc.tradeInfo(">>>账户状态不正常")
                        TradeContext.PRCCO = 'NN1IA999'
                        TradeContext.STRINFO = '账户状态不正常'
                        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM  = "拒绝"
                        
                    elif not (TradeContext.ACCCD == '0428' and TradeContext.ACCEM == '21111'):
                        AfaLoggerFunc.tradeInfo(">>>此账户非个人结算户")
                        TradeContext.PRCCO   = 'NN1IA999'
                        TradeContext.STRINFO = '此账户非个人结算户'
                        TradeContext.BCSTAT  = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM  = "拒绝"
                    
    #校验凭证状态是否正常
    #if TradeContext.PRCCO == 'RCCI0000':
    #    #调用主机接口查询凭证信息
    #    TradeContext.HostCode = '8811'
    #
    #    TradeContext.ACCNO = TradeContext.PYEACC
    #    TradeContext.WARNTNO = TradeContext.BNKBKNO
    #
    #    AfaLoggerFunc.tradeDebug("ACCNO :" + TradeContext.ACCNO)
    #    AfaLoggerFunc.tradeDebug("WARNTNO :" + TradeContext.WARNTNO)
    #
    #    rccpsHostFunc.CommHost( TradeContext.HostCode )
    #
    #    if TradeContext.errorCode != '0000':
    #        #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    #        AfaLoggerFunc.tradeInfo("查询凭证信息异常,主机返回码[" + TradeContext.errorCode + "],主机返回信息[" + TradeContext.errorMsg +"]")
    #        TradeContext.PRCCO = 'RCCI1000'
    #        TradeContext.STRINFO = "查询主机凭证信息失败 " + TradeContext.errorMsg
    #        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
    #        TradeContext.BCSTATNM = "拒绝"
    #
    #    else:
    #        #查询成功
    #        AfaLoggerFunc.tradeInfo(">>>查询主机凭证信息成功")
    #        AfaLoggerFunc.tradeInfo(">>>凭证信息ACCSTCD:[" + TradeContext.ACCSTCD + "]")
    #        
    #        if TradeContext.ACCSTCD != '0':
    #            TradeContext.PRCCO    = 'RCCI1000'
    #            TradeContext.STRINFO  = '账户凭证状态不正常'
    #            TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
    #            TradeContext.BCSTATNM = "拒绝"

    AfaLoggerFunc.tradeInfo(">>>结束必要性检查")
    
    #为应答报文赋值
    TradeContext.sysType  = 'rccpst'
    TradeContext.MSGTYPCO = 'SET006'
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
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).折通存请求报文接收[TRCC006_1136]退出***' )
    return True


#=====================交易后处理===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).折通存请求报文接收[TRCC006_1136]进入***' )
    
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['PRCCO']   = TradeContext.PRCCO
    stat_dict['STRINFO'] = TradeContext.STRINFO
    
    #根据afe返回码判断应答报文是否发送成功,并设置相应业务状态
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        #=====发送农信银成功,设置状态为确认入账\拒绝\冲正成功====
        stat_dict['BCSTAT']  = TradeContext.BCSTAT
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为发送异常")
        
        AfaLoggerFunc.tradeInfo(">>>成功设置业务状态为" + TradeContext.BCSTATNM + "成功")
    else:
        #=====发送农信银失败,设置状态为确认入账\拒绝\冲正失败====       
        stat_dict['BCSTAT']  = TradeContext.BCSTAT
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为发送失败异常")
        
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为发送失败")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).折通存请求报文接收[TRCC006_1136]退出***' )
    return True
        
