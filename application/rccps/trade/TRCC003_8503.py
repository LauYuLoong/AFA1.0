# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).汇票撤销
#===============================================================================
#   交易文件:   TRCC003_8503.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-08-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsMap8503Dbilinf2CTradeContext,rccpsMap8503CTradeContext2Dbilbka
import rccpsDBTrcc_bilbka

#=====================交易前处理(本地操作,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).汇票撤销[TRCC003_8503]进入***' )
    
    #====begin 蔡永贵 20110215 增加====
    #新票据号是16位，需要取后8位，版本号为02，同时要兼容老票据号8位，版本号为01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #校验当前汇票状态是否为签发或解挂
    AfaLoggerFunc.tradeInfo(">>>开始校验当前汇票状态是否为签发或解挂")
    
    bilinf_dict = {}
    if not rccpsDBFunc.getInfoBil(TradeContext.BILVER,TradeContext.BILNO,PL_BILRS_INN,bilinf_dict):
        return AfaFlowControl.ExitThisFlow("S999","查询汇票信息异常")
        
    if bilinf_dict['REMBNKCO'] != TradeContext.SNDBNKCO:
        return AfaFlowControl.ExitThisFlow("S999","本行非此汇票出票行,禁止提交")
        
    if bilinf_dict['BILDAT'] != TradeContext.BJEDTE:
        return AfaFlowControl.ExitThisFlow("S999","非今日签发的汇票,禁止提交")
        
    if bilinf_dict['HPSTAT'] != PL_HPSTAT_SIGN and bilinf_dict['HPSTAT'] != PL_HPSTAT_DEHG and bilinf_dict['HPSTAT'] != PL_HPSTAT_HANG:
        return AfaFlowControl.ExitThisFlow("S999","此汇票当前状态非[签发,挂失,解挂],禁止提交")
    
        
    #=====通过日期＋报单序号查询汇票业务登记簿rcc_bilbka，取“资金来源”====
    #=====潘广通来负责完成====
    bilbka_where_dict = {'BJEDTE':bilinf_dict['NOTE1'],'BSPSQN':bilinf_dict['NOTE2']}
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    if( bilbka_dict == None ):
        return AfaFlowControl.ExitThisFlow("S999","查询汇票业务登记簿异常")
        
    if( len(bilbka_dict) <= 0 ):
        return AfaFlowControl.ExitThisFlow("S999","查询汇票业务登记簿为空")
        
    #=====潘广通 0916 判断柜员和机构是否为签发柜员和机构====
    if( bilbka_dict['BETELR'] != TradeContext.BETELR ):
        return AfaFlowControl.ExitThisFlow("S999","此柜员不是录入柜员")
        
    #if( bilbka_dict['BESBNO'] != TradeContext.BESBNO):
    #    return AfaFlowControl.ExitThisFlow("S999","此机构不是录入机构")
        
    #将签发交易的资金来源赋值到上下文
    TradeContext.BBSSRC = bilbka_dict['BBSSRC']
    
    #将汇票信息映射到TradeContext中
    if not rccpsMap8503Dbilinf2CTradeContext.map(bilinf_dict):
        return False
    
    AfaLoggerFunc.tradeInfo(">>>结束校验当前汇票状态是否为签发或解挂")
    
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
    TradeContext.OPRNO    = PL_HPOPRNO_CX               #业务种类:撤销
    TradeContext.DCFLG    = PL_DCFLG_DEB                #借贷标识:借记
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #往来标识:往账
    TradeContext.TRCCO    = '2100101'                   #交易代码:2100101汇票撤销
    
    bilbka_dict = {}
    if not rccpsMap8503CTradeContext2Dbilbka.map(bilbka_dict):
        return False
    
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记汇票业务登记簿异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇票业务登记簿")
    
    #设置业务状态为发送处理中
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
    
    #为发送农信银中心做准备
    AfaLoggerFunc.tradeInfo(">>>开始为发送农信银中心做准备")
    
    TradeContext.MSGTYPCO = 'SET001'
    TradeContext.TRCCO    = '2100101'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.TRCNO
    TradeContext.ORMFN    = ""
    TradeContext.OPRTYPNO = '21'
    TradeContext.ROPRTPNO = ''
    TradeContext.TRANTYP  = '0'
    TradeContext.OCCAMT   = str(TradeContext.BILAMT)
    TradeContext.BILAMT   = str(TradeContext.BILAMT)
    
    #begin 20110614 曾照泰 修改 送往农信银中心的票号为8位
    TradeContext.BILNO = TradeContext.BILNO[-8:]
    #end
    
    AfaLoggerFunc.tradeInfo(">>>结束为发送农信银中心做准备")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).汇票撤销[TRCC003_8503]退出***' )
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).汇票撤销[TRCC003_8503]进入***' )
    
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
        AfaLoggerFunc.tradeInfo(">>>发送农信银总中心成功")
        AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为发送成功")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为发送成功异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为发送成功")
        
    else:
        #发送农信银失败,设置业务状态为发送失败
        AfaLoggerFunc.tradeInfo(">>>发送农信银总中心失败")
        AfaLoggerFunc.tradeInfo(">>>开始设置业务状态为发送失败")
        
        stat_dict['BCSTAT']  = PL_BCSTAT_SND
        stat_dict['BDWFLG']  = PL_BDWFLG_FAIL
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "设置业务状态为发送失败异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束设置业务状态为发送失败")
    
    #COMMIT
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
    AfaLoggerFunc.tradeInfo(">>>Commit成功")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).汇票撤销[TRCC003_8503]退出***' )
    
    return True
    
