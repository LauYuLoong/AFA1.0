# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.中心类操作模板(1.本地操作 2.中心记帐).个人现金通兑
#==============================================================================
#   交易文件:   TRCC002_8562.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-10-30
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,jiami
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_pamtbl,rccpsMap8562CTradeContext2Dwtrbka_dict


#=====================交易前处理(登记流水,主机前处理)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 通存通兑.本地类操作交易[RCC003_8562]进入***' )

    #检查本机构是否有通存通兑业务权限
    if not rccpsDBFunc.chkTDBESAuth(TradeContext.BESBNO):
        return AfaFlowControl.ExitThisFlow("S999","本机构无通存通兑业务权限")
    
    #=====接收行判断====
    if TradeContext.SNDSTLBIN == TradeContext.RCVSTLBIN:
        return AfaFlowControl.ExitThisFlow('S999','同一清算行不允许做此业务')

    #=====账户类型判断====
    if not TradeContext.existVariable('PYRTYP'):
        return AfaFlowControl.ExitThisFlow('S999','账户类型不存在[PYRTYP]')

    if TradeContext.PYRTYP == '0':
        #=====银行卡====        
        if len(TradeContext.PYRNAM)   == 0:
            return AfaFlowControl.ExitThisFlow('S999','付款人名称[PYRNAM]不允许为空')
        if len(TradeContext.SCTRKINF) == 0:
            return AfaFlowControl.ExitThisFlow('S999','二磁道[SCTRKINF]信息不允许为空')
        #if len(TradeContext.THTRKINF) == 0:
        #    return AfaFlowControl.ExitThisFlow('S999','三磁道[THTRKINF]信息不允许为空')
            
        if len(TradeContext.SCTRKINF) > 37:
            return AfaFlowControl.ExitThisFlow('S999','磁道信息非法')
            
        #if len(TradeContext.THTRKINF) > 104:
        #    return AfaFlowControl.ExitThisFlow('S999','磁道信息非法')
    elif TradeContext.PYRTYP == '1':
        #=====存折====
        if len(TradeContext.BNKBKNO)  == 0:
            return AfaFlowControl.ExitThisFlow('S999','存折号码[BNKBKNO]不允许为空')
        if float(TradeContext.BNKBKBAL) == 0.0:
            return AfaFlowControl.ExitThisFlow('S999','存折余额[BNKBKBAL]不允许为空')
            
        TradeContext.SCTRKINF = ''.rjust(37,'0')
        TradeContext.THTRKINF = ''.rjust(37,'0')
    else:
        return AfaFlowControl.ExitThisFlow('S999','账户类型错误')
    
    #=====交易金额判断====
    sel_dict = {}
    sel_dict['BPARAD'] = 'TD001'    #通存通兑凭证金额校验
    
    dict = rccpsDBTrcc_pamtbl.selectu(sel_dict) 
    AfaLoggerFunc.tradeInfo('dict='+str(dict))

    if dict == None:
        return AfaFlowControl.ExitThisFlow('S999','校验交易金额失败')
    if len(dict) == 0:
        return AfaFlowControl.ExitThisFlow('S999','查询PAMTBL校验交易金额表记录错误')
    
    #=====判断农信银中心规定校验凭证上线====
    if float(TradeContext.OCCAMT) >= float(dict['BPADAT']):
         #=====交易金额大于农信银中心规定金额，需要输入证件====
         if TradeContext.existVariable('CERTTYPE') and len(TradeContext.CERTTYPE) == 0:
             return AfaFlowControl.ExitThisFlow('S999','请选择证件类型!')
         if TradeContext.existVariable('CERTNO')   and len(TradeContext.CERTNO)   == 0:
             return AfaFlowControl.ExitThisFlow('S999','请输入证件号码!')

    #加密客户密码
    MIMA = '                '
    #PIN = '888888'
    #ACC = '12311111111111111111111111111111'
    PIN  = TradeContext.CURPIN
    ACC  = TradeContext.PYRACC
    AfaLoggerFunc.tradeDebug('密码[' + PIN + ']')
    AfaLoggerFunc.tradeDebug('账号[' + ACC + ']')
    ret = jiami.secEncryptPin(PIN,ACC,MIMA)
    if ret != 0:
        AfaLoggerFunc.tradeDebug("ret=[" + str(ret) + "]")
        return AfaFlowControl.ExitThisFlow('M9999','调用加密服务器失败')
    else:
        TradeContext.CURPIN = MIMA
        AfaLoggerFunc.tradeDebug('密码new[' + TradeContext.CURPIN + ']')

    #=====字段赋值====
    TradeContext.OPRNO   =  PL_TDOPRNO_TD          #业务种类
    TradeContext.DCFLG   =  PL_DCFLG_DEB           #借贷标识

    #=====字典赋值，插入数据库====
    wtrbka_dict = {}
    if not rccpsMap8562CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','字典赋值错误!')
        
    wtrbka_dict['MSGFLGNO'] = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo       #报文标识号

    #=====插入数据库表====
    if not rccpsDBFunc.insTransWtr(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记通存通兑业务登记簿异常')
    AfaDBFunc.CommitSql( )

    #=====设置业务状态为发送处理中====
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为发送处理中")
    
    stat_dict = {}
    stat_dict['BJEDTE'] = TradeContext.BJEDTE       #交易日期
    stat_dict['BSPSQN'] = TradeContext.BSPSQN       #报单序号
    stat_dict['BCSTAT'] = PL_BCSTAT_SND             #PL_BCSTAT_SND  发送
    stat_dict['BDWFLG'] = PL_BDWFLG_WAIT            #PL_BDWFLG_WAIT 处理中
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','设置状态为发送处理中异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为发送处理中")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为发送处理中")
    
    #=====发送农信银中心====
    AfaLoggerFunc.tradeInfo(">>>开始发送农信银中心处理")
    
    TradeContext.MSGTYPCO   =   'SET004'              #报文类代码
    TradeContext.OPRTYPNO   =   '30'                  #通存通兑
    
    #=====根据手续费收取方式判断是否发送农信银中心====
    TradeContext.sCuschrg = TradeContext.CUSCHRG
    if TradeContext.CHRGTYP != PL_CHRG_TYPE:          #PL_CHRG_TYPE 1 转账
        #=====转账收取手续费====
        TradeContext.CUSCHRG = '0.0'
    
    AfaLoggerFunc.tradeDebug(">>>结束发送农信银中心处理")

    AfaLoggerFunc.tradeInfo( '***农信银系统: 通存通兑.本地类操作交易[RCC003_8562]退出***' )
    return True
#=====================交易后处理===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统: 通存通兑.中心类操作交易[RCC003_8562]进入***' )
    
    #=====判断中心返回是否成功====
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['BCSTAT']  = PL_BCSTAT_SND             #PL_BCSTAT_SND  发送
    
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为发送成功")    
    
    if TradeContext.errorCode != '0000':
        stat_dict['BDWFLG'] = PL_BDWFLG_FAIL         #PL_BDWFLG_FAIL 失败
    else:
        stat_dict['BDWFLG'] = PL_BDWFLG_SUCC         #PL_BDWFLG_SUCC 成功
        stat_dict['PRTCNT'] = 1
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','设置状态为发送成功异常')
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为发送成功")
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    TradeContext.CUSCHRG = TradeContext.sCuschrg
    
    AfaLoggerFunc.tradeInfo( '***农信银系统: 通存通兑.中心类操作交易[RCC003_8562]退出***' )
    
    return True
