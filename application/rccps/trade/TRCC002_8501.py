# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.主机类操作(1.本地操作 2.主机记账 3.中心记帐).汇票签发
#===============================================================================
#   交易文件:   TRCC002_0000.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-07-30
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc,miya
import rccpsDBTrcc_bilbka,rccpsDBTrcc_bilinf
import rccpsMap8501CTradeContext2Dbilbka,rccpsMap8501CTradeContext2Dbilinf


#=====================交易前处理(登记流水,主机前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(1.本地操作).汇票签发[TRCC002_8501]进入***' )
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #=====汇票类交易接收成员行为总中心====
    TradeContext.RCVSTLBIN = PL_RCV_CENTER
    
    #=====出票日期为当前交易日期====
    TradeContext.BILDAT = TradeContext.BJEDTE
    
    #=====出票行为发起行号====
    TradeContext.REMBNKCO = TradeContext.SNDBNKCO
    TradeContext.REMBNKNM = TradeContext.SNDBNKNM
    
    #=====生成汇票密押=====
    AfaLoggerFunc.tradeInfo(">>>开始生成汇票密押")
    
    #=====根据汇票类型赋值编押业务种类和兑付方式====
    #=====PL_BILTYP_CASH  现金  PL_TYPE_XJHP  现金汇票====
    #=====PL_BILTYP_TRAN  转账  PL_TYPE_ZZHP  转账汇票====
    if TradeContext.BILTYP == PL_BILTYP_CASH:
        TYPE = PL_TYPE_XJHP
        TradeContext.PAYWAY = PL_PAYWAY_CASH        
    elif TradeContext.BILTYP == PL_BILTYP_TRAN:
        TYPE = PL_TYPE_ZZHP
        TradeContext.PAYWAY = PL_PAYWAY_TRAN        
    else:
        return AfaFlowControl.ExitThisFlow("S999","汇票类型非法")
    
    #=====资金来源为1-个人结算户时，需要调用8811校验支付条件====
    if TradeContext.BBSSRC == '1':
        TradeContext.HostCode = '8811'
        TradeContext.ACCNO    = TradeContext.PYRACC     #付款人账户

        rccpsHostFunc.CommHost( '8811' )
       
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow('S999','查询凭证信息出错')
        else:
            if TradeContext.PAYTYP != TradeContext.HPAYTYP:
                return AfaFlowControl.ExitThisFlow('S999','支付条件错误')
                
    MIYA      = "".rjust(10,' ')
    TRCDAT    = TradeContext.BILDAT                    #委托日期
    TRCNO     = TradeContext.BILNO                     #汇票号码
    REMBNKCO  = TradeContext.REMBNKCO                  #签发行
    PAYBNKCO  = TradeContext.PAYBNKCO                  #代理付款行
    REMBNKCO  = REMBNKCO.rjust(12,'0')
    PAYBNKCO  = PAYBNKCO.rjust(12,'0')
    AMOUNT    = str(TradeContext.BILAMT).split('.')[0] + str(TradeContext.BILAMT).split('.')[1]
    AMOUNT    = AMOUNT.rjust(15,'0')
    INFO      = ""
    
    AfaLoggerFunc.tradeDebug('处理类型(0-编押 1-核押):' + str(PL_SEAL_ENC) )
    AfaLoggerFunc.tradeDebug('业务种类(1-现金汇票 2-转账汇票 3-电子汇兑业务):' + TYPE )
    AfaLoggerFunc.tradeDebug('出票日期:' + TRCDAT )
    AfaLoggerFunc.tradeDebug('汇票号码:' + TRCNO )
    AfaLoggerFunc.tradeDebug('出票金额:' + str(AMOUNT) )
    AfaLoggerFunc.tradeDebug('出票行号:' + str(REMBNKCO) )
    AfaLoggerFunc.tradeDebug('代理付款行号:' + str(PAYBNKCO) )
    AfaLoggerFunc.tradeDebug('汇票密押:' + MIYA )
    AfaLoggerFunc.tradeDebug('OTHERINFO[' + str(INFO) + ']')
    
    #====begin 蔡永贵 20110215 修改====
    #ret = miya.DraftEncrypt(PL_SEAL_ENC,TYPE,TRCDAT,TRCNO,AMOUNT,REMBNKCO,PAYBNKCO,INFO,MIYA)
    ret = miya.DraftEncrypt(PL_SEAL_ENC,TYPE,TRCDAT,TradeContext.TMP_BILNO,AMOUNT,REMBNKCO,PAYBNKCO,INFO,MIYA)
    #============end============
    
    AfaLoggerFunc.tradeDebug( 'ret=' + str(ret) )
    
    if ret > 0:
        return AfaFlowControl.ExitThisFlow('S999','调用密押服务器生成密押失败')
    
    TradeContext.SEAL = MIYA
    
    AfaLoggerFunc.tradeDebug('TradeContext密押:' + TradeContext.SEAL )
    AfaLoggerFunc.tradeInfo(">>>结束生成汇票密押")
    
    #=====登记汇票业务登记簿====
    AfaLoggerFunc.tradeInfo(">>>开始登记汇票业务登记簿")
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN      #发送成员行号
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN      #接收成员行号
    TradeContext.TRCNO    = TradeContext.SerialNo       #交易流水号
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate    #中心工作日期
    TradeContext.OPRNO    = PL_HPOPRNO_QF               #业务种类:汇票签发
    TradeContext.DCFLG    = PL_DCFLG_CRE                #借贷标识:贷记
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #往来标识:往账
    TradeContext.TRCCO    = '2100001'                   #交易代码:2100001汇票签发
    
    bilbka_dict = {}
    if not rccpsMap8501CTradeContext2Dbilbka.map(bilbka_dict):
        return AfaFlowContorl.ExitThisFlow("S999","为汇票业务登记簿赋值异常")
        
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记汇票业务登记簿异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇票业务登记簿")
    
    #=====登记汇票信息登记簿====
    AfaLoggerFunc.tradeInfo(">>>开始登记汇票信息登记簿")
    
    TradeContext.NOTE1 = TradeContext.BJEDTE
    TradeContext.NOTE2 = TradeContext.BSPSQN
    TradeContext.NOTE3 = TradeContext.BESBNO
    
    bilinf_dict = {}
    if not rccpsMap8501CTradeContext2Dbilinf.map(bilinf_dict):
        return AfaFlowContorl.ExitThisFlow("S999","为汇票信息登记簿赋值异常")
        
    if not rccpsDBFunc.insInfoBil(bilinf_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记汇票信息登记簿异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇票信息登记簿")
    
    #=====设置业务状态为记账处理中====
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为记账处理中")
    
    stat_dict = {}
    stat_dict['BJEDTE'] = TradeContext.BJEDTE       #交易日期
    stat_dict['BSPSQN'] = TradeContext.BSPSQN       #报单序号
    stat_dict['BCSTAT'] = PL_BCSTAT_ACC             #PL_BCSTAT_ACC 记账
    stat_dict['BDWFLG'] = PL_BDWFLG_WAIT            #PL_BDWFLG_WAIT 处理中
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','设置状态为记账处理中异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为记账处理中")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    #=====为主机记账做准备====
    AfaLoggerFunc.tradeInfo(">>>开始为主机记账做准备")
    
    #=====非待销账,借付款人账号,待销账,借方账号赋空====
    if TradeContext.BBSSRC != '3':
        TradeContext.SBAC = TradeContext.PYRACC     #借方账号
        TradeContext.ACNM = TradeContext.PYRNAM
    else:
        TradeContext.SBAC = ''
        TradeContext.ACNM = ''
    
    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_HCHK           #贷方账号
    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
    TradeContext.OTNM = "汇出汇款"
    
    AfaLoggerFunc.tradeInfo("借方账号:[" + TradeContext.SBAC + "]")
    AfaLoggerFunc.tradeInfo("贷方账号:[" + TradeContext.RBAC + "]")
    
    #=====银行卡,凭证号码取账号的7到18位====
    if TradeContext.BBSSRC == '0':
        TradeContext.WARNTNO = TradeContext.SBAC[6:18]
        AfaLoggerFunc.tradeDebug("凭证号码:[" + TradeContext.WARNTNO + "]")
        
    
    TradeContext.HostCode = '8813'    
    TradeContext.OCCAMT = TradeContext.BILAMT                       #出票金额
    TradeContext.RCCSMCD  = PL_RCCSMCD_HPQF                         #主机摘要码:汇票签发    
    TradeContext.ACUR = '2'                                         #重复次数    
    TradeContext.TRFG = '4'                                         #凭证处理标识
    
    AfaLoggerFunc.tradeDebug("TradeContext.TRFG=[" + TradeContext.TRFG + "]")
    AfaLoggerFunc.tradeDebug("TradeContext.PASSWD=[" + TradeContext.PASSWD + "]")
    AfaLoggerFunc.tradeDebug("TradeContext.WARNTNO=[" + TradeContext.WARNTNO + "]")
    
    AfaLoggerFunc.tradeInfo(">>>结束为主机记账做准备")
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(1.本地操作).汇票签发[TRCC002_8501]退出***' )
    return True
#=====================交易中处理(修改流水,主机后处理,中心前处理)================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(2.主机记账).汇票签发[TRCC002_8501]进入***' )
    
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['SBAC']    = TradeContext.SBAC
    stat_dict['ACNM']    = TradeContext.ACNM
    stat_dict['RBAC']    = TradeContext.RBAC
    stat_dict['OTNM']    = TradeContext.OTNM
    if TradeContext.existVariable('TRDT'):
        stat_dict['TRDT'] = TradeContext.TRDT
    if TradeContext.existVariable('TLSQ'):
        stat_dict['TLSQ'] = TradeContext.TLSQ
    stat_dict['MGID']    = TradeContext.errorCode
    stat_dict['STRINFO'] = TradeContext.errorMsg
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        #====主机记账成功,设置状态为记账成功====
        stat_dict['BCSTAT']  = PL_BCSTAT_ACC
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRTCNT']  = 1
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为记账成功异常")
        
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为记账成功")
    else:
        #=====主机记账失败,设置状态为记账失败====
        stat_dict['BCSTAT']  = PL_BCSTAT_ACC
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为记账失败异常")
        
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为记账失败")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    #====设置业务状态为发送处理中====
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为发送处理中")
    
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999',"设置业务状态为发送处理中异常")
    
    AfaLoggerFunc.tradeInfo(">>>设置业务状态为发送处理中")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    #====为发送农信银做准备====    
    TradeContext.MSGTYPCO = 'SET001'
    TradeContext.TRCCO    = '2100001'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = ''
    TradeContext.OPRTYPNO = '21'
    TradeContext.ROPRTPNO = ''
    TradeContext.TRANTYP  = '0'
    
    #begin 20110614 曾照泰 修改 送往农信银中心的票号为8位
    TradeContext.BILNO = TradeContext.BILNO[-8:]
    #end
    
    AfaLoggerFunc.tradeInfo(">>>为发送农信银做准备")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(2.主机记账).汇票签发[TRCC002_8501]退出***' )
    return True   
#=====================交易后处理================================================
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(3.中心记账).汇票签发[TRCC002_8501]进入***' )
    
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['BCSTAT']  = PL_BCSTAT_SND
    stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
    stat_dict['PRCCO']   = TradeContext.errorCode
    stat_dict['STRINFO'] = TradeContext.errorMsg
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        #=====发送农信银成功,设置状态为发送成功====
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为发送成功异常")
        
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为发送成功")
    else:
        #=====发送农信银失败,设置状态为发送失败====       
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为发送失败异常")
        
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为发送失败")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
        #====自动抹账====
        AfaLoggerFunc.tradeInfo(">>>开始自动抹账")
        
        #====设置业务状态为抹账处理中====        
        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_HCAC,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999','设置业务状态为抹账处理中异常')
        
        AfaLoggerFunc.tradeInfo(">>>设置业务状态为抹账处理中")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
        #=====发起主机抹账====
        #=====如果资金来源为代销账，使用8813红字冲销====
        TradeContext.BOJEDT = TradeContext.BJEDTE           #给前置日期赋值
        TradeContext.BOSPSQ = TradeContext.BSPSQN           #给前置流水号赋值
        if TradeContext.BBSSRC  ==  '3':      #待销账
            TradeContext.HostCode= '8813'
            TradeContext.DASQ    = ''
            TradeContext.RVFG    = '0'        #红蓝字标志 0红字
            TradeContext.SBAC    =  TradeContext.BESBNO  +  PL_ACC_HCHK       #借方账号
            TradeContext.RBAC    =  TradeContext.BESBNO  +  PL_ACC_NXYDXZ     #贷方账号
            #=====开始调函数拼贷方账号第25位校验位====
            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
            TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
            AfaLoggerFunc.tradeInfo( '借方账号:' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '贷方账号:' + TradeContext.RBAC )
        else:
            TradeContext.HostCode='8820'

        #=====调起抹账主机接口====
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        if TradeContext.HostCode == '8813':
            stat_dict['SBAC']    = TradeContext.SBAC
            stat_dict['RBAC']    = TradeContext.RBAC
        if TradeContext.existVariable('TRDT'):
            stat_dict['TRDT'] = TradeContext.TRDT
        if TradeContext.existVariable('TLSQ'):
            stat_dict['TLSQ'] = TradeContext.TLSQ
        stat_dict['MGID']    = TradeContext.errorCode
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
        if TradeContext.errorCode == '0000':
            #=====主机抹账成功,设置业务状态为抹账成功====           
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态抹账成功异常')
            
            AfaLoggerFunc.tradeInfo(">>>设置业务状态为抹账成功")
        else:
            #=====主机抹账失败,设置业务状态为抹账失败====
            stat_dict['BCSTAT'] = PL_BCSTAT_HCAC
            stat_dict['BDWFLG'] = PL_BDWFLG_FAIL
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999','设置业务状态抹账成功异常')
            
            AfaLoggerFunc.tradeInfo(">>>设置业务状态为抹账失败")
        
        AfaLoggerFunc.tradeInfo(">>>结束自动抹账")

    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.主机类操作(3.中心记帐).汇票签发[TRCC002_8501]退出***' )
    return True
