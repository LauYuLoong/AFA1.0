# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).柜台补正
#==============================================================================
#   交易文件:   TRCC003_8587.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘振东
#   修改时间:   2008-12-3
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsEntries,rccpsHostFunc,rccpsGetFunc
import rccpsDBTrcc_jstbka
import rccpsMap8563CTradeContext2Dwtrbka_dict

#==========交易前处理(本地操作,中心前处理)==========
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).柜台补正[TRCC003_8587]进入***' )

    #=====检验变量合法性====
    if not TradeContext.existVariable("BOJEDT"):
        return AfaFlowControl.ExitThisFlow('A099','原报单日期不能为空')  
        
    if not TradeContext.existVariable("BOSPSQ"):
        return AfaFlowControl.ExitThisFlow('A099','原报单序号不能为空')

    #=====查询原交易信息====
    wtr_dict = {}
    
    if rccpsDBFunc.getTransWtr(TradeContext.BOJEDT,TradeContext.BOSPSQ,wtr_dict):
        AfaLoggerFunc.tradeInfo(">>>通存通兑登记簿中找到原交易")
    else:
        return AfaFlowControl.ExitThisFlow('S0999','查找原交易信息失败')
    
    swtr_dict = wtr_dict
    
    #=====判断原交易是否为往账====
    if( wtr_dict['BRSFLG'] != PL_BRSFLG_SND):
        return AfaFlowControl.ExitThisFlow('A099','此交易非往账,禁止补正')
    
    #====判断账户卡折类型====
    if TradeContext.DCFLG == '0':
        TradeContext.CBFLG = TradeContext.PYITYP
    else:
        TradeContext.CBFLG = TradeContext.PYOTYP
        
    #====判断原交易状态====
    AfaLoggerFunc.tradeInfo("开始判断原交易信息是否允许补正")
    
    if (wtr_dict['BCSTAT'] != PL_BCSTAT_CANC and wtr_dict['BDWFLG'] != PL_BDWFLG_SUCC):
        return AfaFlowControl.ExitThisFlow("S999","交易状态["+str(wtr_dict['BCSTAT'])+"],禁止补正")
        
    AfaLoggerFunc.tradeInfo("结束判断原交易信息是否允许补正")
    
    #=================登记通存通兑业务登记簿===================================
    AfaLoggerFunc.tradeInfo(">>>开始登记通存通兑业务登记簿")

    #=====================获取中心流水号====================================
    if rccpsGetFunc.GetRccSerialno( ) == -1 :
        raise AfaFlowControl.flowException( )
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN      #发送成员行号
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN      #接收成员行号
    TradeContext.TRCNO    = TradeContext.SerialNo       #交易流水号
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate    #中心工作日期
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.TRCDAT + TradeContext.SerialNo  #报文标识号
    TradeContext.OPRNO    = PL_TDOPRNO_BZ               #业务种类:个人现金通存
    TradeContext.BRSFLG   = PL_BRSFLG_SND               #往来标识:往账
    TradeContext.PYRMBRCO = TradeContext.SNDSTLBIN
    TradeContext.PYEMBRCO = TradeContext.RCVSTLBIN
    TradeContext.NOTE1    = TradeContext.BOJEDT
    TradeContext.NOTE2    = TradeContext.BOSPSQ
    TradeContext.TRCCO    = '3000505'
    
    wtrbka_dict = {}
    if not rccpsMap8563CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
        return AfaFlowContorl.ExitThisFlow("S999","为通存通兑业务登记簿赋值异常")
        
    if(TradeContext.DCFLG == '0'):
        wtrbka_dict['DCFLG'] = '1'
    elif(TradeContext.DCFLG == '1'):
        wtrbka_dict['DCFLG'] = '2'
    else:
        return AfaFlowControl.ExitThisFlow('S999','非法借贷标示')
        
    if not rccpsDBFunc.insTransWtr(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记通存通兑业务登记簿异常')
    
    AfaLoggerFunc.tradeInfo(">>>结束登记通存通兑业务登记簿")
    
    #=====判断原交易是否为异转本或通兑====
    if swtr_dict['TRCCO'] in ('3000102','3000103','3000104','3000105') and swtr_dict['CHRGTYP'] == '1':
        TradeContext.CUSCHRG = str(swtr_dict['CUSCHRG'])
    else:
        TradeContext.CUSCHRG = "0.00"
        
    #=====发送农信银中心，为发送柜面报文做准备====
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET009'   
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN    = swtr_dict['MSGFLGNO']
    TradeContext.TRCCO    = "3000505"
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "30"
    TradeContext.ROPRTPNO = "30"
    TradeContext.TRANTYP  = "0"
    #=====业务要素集====
    TradeContext.CUR      = "CNY"
    TradeContext.OCCAMT   = str(TradeContext.OCCAMT)
    #TradeContext.OCCAMT   = str(wtr_dict['OCCAMT'])
    TradeContext.CUSCHRG  = str(TradeContext.CUSCHRG)
    TradeContext.ORTRCCO  = str(swtr_dict['TRCCO'])
    TradeContext.ORTRCNO  = str(swtr_dict['TRCNO'])

    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_SND,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow("S999","设置原交易当前状态为发送-处理中异常")
        
    AfaLoggerFunc.tradeInfo(">>>结束设置原交易状态为发送-处理中")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        
    return True

#==========交易后处理(本地操作,中心后处理)==========
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('>>>中心后处理')
    
    if TradeContext.errorCode == '0000':
        TradeContext.BDWFLG = PL_BDWFLG_SUCC
    else:
        TradeContext.BDWFLG = PL_BDWFLG_FAIL
        
    sstlog_dict={}
    sstlog_dict['BSPSQN']  = TradeContext.BSPSQN
    sstlog_dict['BJEDTE']  = TradeContext.BJEDTE
    sstlog_dict['BCSTAT']  = PL_BCSTAT_SND
    sstlog_dict['BDWFLG']  = TradeContext.BDWFLG
    
    if not rccpsState.setTransState(sstlog_dict):
        AfaDBFunc.RollBackSql()
        return AfaFlowControl.ExitThisFlow("S999","修改原交易当前状态为发送-成功异常")
    else:
        AfaDBFunc.CommitSql( )
        AfaLoggerFunc.tradeInfo(">>>结束修改原交易状态为发送-成功")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).柜台补正[TRCC003_8587]退出***' )
    return True
    
