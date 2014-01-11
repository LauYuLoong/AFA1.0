# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).汇票退票
#===============================================================================
#   交易文件:   TRCC003_8504.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-08-06
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsHostFunc
import rccpsMap8504CTradeContext2Dbilbka,rccpsMap8504Dbilinf2CTradeContext
import rccpsDBTrcc_bilinf,rccpsDBTrcc_bilbka


#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).汇票退票[TRCC003_8504]进入***' )
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    AfaLoggerFunc.tradeInfo("BJEDTE=[" + TradeContext.BJEDTE + "]")
    
    #检查汇票状态,非签发或解付状态禁止提交
    AfaLoggerFunc.tradeInfo(">>>开始检查汇票状态")
    
    bilinf_dict = {}
    if not rccpsDBFunc.getInfoBil(TradeContext.BILVER,TradeContext.BILNO,PL_BILRS_INN,bilinf_dict):
        return AfaFlowControl.ExitThisFlow("S999","查询汇票信息异常")
        
    AfaLoggerFunc.tradeInfo("----->" + bilinf_dict['REMBNKCO'])
    AfaLoggerFunc.tradeInfo("----->" + TradeContext.SNDBNKCO)
        
    if bilinf_dict['REMBNKCO'] != TradeContext.SNDBNKCO:
        return AfaFlowControl.ExitThisFlow("S999","本行非此汇票出票行,禁止提交")
        
    if bilinf_dict['HPSTAT'] != PL_HPSTAT_SIGN and bilinf_dict['HPSTAT'] != PL_HPSTAT_DEHG and bilinf_dict['HPSTAT'] != PL_HPSTAT_HANG:
        return AfaFlowControl.ExitThisFlow("S999","此汇票当前状态非[签发,挂失,解挂],禁止提交")
    
    #=====增加查询汇票业务登记簿rcc_bilbka信息，查询条件为：汇票信息rcc_bilinf登记簿note1、note2====
    #bilbka_dict = {}
    #bilbka_where_dict = {'BJEDTE':bilinf_dict['NOTE1'],'BSPSQN':bilinf_dict['NOTE2']}
    #bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    #if( bilbka_dict == None ):
    #    return AfaFlowControl.ExitThisFlow("S999","查询汇票业务登记簿异常")
    #    
    #if( len(bilbka_dict) == 0 ):
    #    return AfaFlowControl.ExitThisFlow("S999","查询汇票业务登记为空")
        
    #bilinf_dict['BBSSRC'] = bilbka_dict['BBSSRC']
    #bilinf_dict['DASQ']   = bilbka_dict['DASQ']
    
    
    #=====取签发交易的BBSSRC、DASQ字段，赋值到bilinf_dict字典中====
    #=====例：bilinf_dict['BBSSRC'] = bilbka_dict['BBSSRC']====
    
    
    #将汇票信息映射到TradeContext中
    if not rccpsMap8504Dbilinf2CTradeContext.map(bilinf_dict):
        return False
    
    AfaLoggerFunc.tradeInfo(">>>结束检查汇票状态")
    
    #汇票类交易接收成员行为总中心
    TradeContext.RCVSTLBIN = PL_RCV_CENTER
    
    #接收行为签发时的代理付款行
    TradeContext.RCVBNKCO  = TradeContext.PAYBNKCO
    TradeContext.RCVBNKNM  = TradeContext.PAYBNKNM
    
    #登记汇票业务登记簿
    AfaLoggerFunc.tradeInfo(">>>开始登记汇票业务登记簿")
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    if TradeContext.OPRFLG == '0':
        TradeContext.OPRNO    = PL_HPOPRNO_TP           #业务种类:汇票退票
    else:
        TradeContext.OPRNO    = PL_HPOPRNO_CF           #业务种类:汇票超期付款
    TradeContext.DCFLG    = PL_DCFLG_DEB                #借贷标识:借记
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #往来标识:往账
    TradeContext.TRCCO    = '2100103'                   #交易代码:2100103汇票退票
    
    bilbka_dict = {}
    if not rccpsMap8504CTradeContext2Dbilbka.map(bilbka_dict):
        return False
    
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记汇票业务登记簿异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇票业务登记簿")
    
    #更新汇票信息登记簿
    AfaLoggerFunc.tradeInfo(">>>开始更新汇票信息登记簿")
    
    bilinf_update_dict = {}
    if TradeContext.OPRFLG == '0':
        
        #=================校验入账账号户名======================================
        AfaLoggerFunc.tradeInfo(">>>开始校验入账账号户名")
        
        TradeContext.HostCode = '8810'
        
        TradeContext.ACCNO = bilinf_dict['PYRACC']
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNO)
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNM)
        
        if TradeContext.ACCNM != bilinf_dict['PYRNAM']:
            return AfaFlowControl.ExitThisFlow('S999',"入账账号户名不符")
            
        if TradeContext.ACCST != '0' and TradeContext.ACCST != '2':
            return AfaFlowControl.ExitThisFlow('S999','入账账号状态不正常')
        
        AfaLoggerFunc.tradeInfo(">>>结束校验入账账号户名")
        
        bilinf_update_dict['PYIACC'] = bilinf_dict['PYRACC']
        bilinf_update_dict['PYINAM'] = bilinf_dict['PYRNAM']
        
    elif TradeContext.OPRFLG == '1':
        #bilinf_update_dict['PYIACC'] = TradeContext.PYIACC
        #bilinf_update_dict['PYINAM'] = TradeContext.PYINAM
        #操作类型为超期付款时,入账账号为待销账账号
        bilinf_update_dict['PYIACC'] = TradeContext.BESBNO + PL_ACC_NXYDXZ
        bilinf_update_dict['PYINAM'] = "农信银待销账"
    else:
        return AfaFlowControl.ExitThisFlow('S999','操作类型非法')
    bilinf_update_dict['OCCAMT'] = TradeContext.OCCAMT
    bilinf_update_dict['RMNAMT'] = TradeContext.RMNAMT
    
    bilinf_where_dict = {}
    bilinf_where_dict['BILVER'] = TradeContext.BILVER
    bilinf_where_dict['BILNO']  = TradeContext.BILNO
    
    ret = rccpsDBTrcc_bilinf.update(bilinf_update_dict,bilinf_where_dict)
    
    if ret == None:
        return AfaFlowControl.ExitThisFlow("S999","更新汇票信息登记簿异常")
        
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","无对应的汇票信息")
        
    AfaLoggerFunc.tradeInfo(">>>结束更新汇票信息登记簿")
    
    #设置交易状态为发送处理中
    AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为发送处理中")
    
    stat_dict = {}
    stat_dict['BJEDTE'] = TradeContext.BJEDTE
    stat_dict['BSPSQN'] = TradeContext.BSPSQN
    stat_dict['BCSTAT'] = PL_BCSTAT_SND
    stat_dict['BDWFLG'] = PL_BDWFLG_WAIT
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','设置状态为发送处理中异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为发送处理中")
    
    #COMMIT
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    #为发送农信银做准备
    AfaLoggerFunc.tradeInfo(">>>开始为发送农信银做准备")
    
    TradeContext.MSGTYPCO = 'SET002'
    TradeContext.TRCCO    = '2100103'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = ''
    TradeContext.OPRTYPNO = '21'
    TradeContext.ROPRTPNO = ''
    TradeContext.TRANTYP  = '0'
    TradeContext.OCCAMT   = str(TradeContext.BILAMT)
    TradeContext.BILAMT   = str(TradeContext.BILAMT)
    
    #begin 20110614 曾照泰 修改 送往农信银中心的票号为8位
    TradeContext.BILNO = TradeContext.BILNO[-8:]
    #end
    
    
    AfaLoggerFunc.tradeInfo(">>>结束为发送农信银做准备")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).汇票退票[TRCC003_8504]退出***' )
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).汇票退票[TRCC003_8504]进入***' )
    
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
        #发送农信银成功,设置业务状态为发送成功
        AfaLoggerFunc.tradeInfo("发送农信银成功")
        AfaLoggerFunc.tradeInfo("开始设置业务状态为发送成功")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为发送成功异常")
        
        AfaLoggerFunc.tradeInfo("结束设置业务状态为发送成功")
        
    else:
        #发送农信银失败,设置业务状态为发送失败
        AfaLoggerFunc.tradeInfo("发送农信银失败")
        AfaLoggerFunc.tradeInfo("开始设置业务状态为发送失败")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为发送失败异常")
        
        AfaLoggerFunc.tradeInfo("结束设置业务状态为发送失败")
    
    #COMMIT
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).汇票退票[TRCC003_8504]退出***' )
    return True
    
