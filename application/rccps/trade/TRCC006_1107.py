# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).业务状态查询报文接收
#===============================================================================
#   模板文件:   TRCC006.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsFunc,rccpsGetFunc
import rccpsDBTrcc_ztcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1107CTradeContext2Dztcbka

#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).业务状态查询报文接收[RCC006_1107]进入***' )
    
    #==========判断是否重复报文,如果是重复报文,直接进入下一流程================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    ztcbka_where_dict = {}
    ztcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    ztcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    ztcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    ztcbka_dict = rccpsDBTrcc_ztcbka.selectu(ztcbka_where_dict)
    
    if ztcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常") 
    
    if len(ztcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("业务状态登记簿中存在相同查询交易,此报文为重复报文,直接进入下一流程,发送表示成功的通讯回执")
        #======为通讯回执报文赋值===================================================
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
        out_context_dict['STRINFO']  = '重复报文'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>结束检查是否重复报文")
    
    #==========为业务状态查询查复登记簿字典赋值================================
    AfaLoggerFunc.tradeInfo(">>>开始为业务状态查询查复登记簿字典赋值")
    
    
    AfaLoggerFunc.tradeInfo("业务类型[" + TradeContext.ROPRTPNO + "]")
    AfaLoggerFunc.tradeInfo("原发送行号[" + TradeContext.ORSNDBNK + "]")
    AfaLoggerFunc.tradeInfo("原委托日期[" + TradeContext.ORTRCDAT + "]")
    AfaLoggerFunc.tradeInfo("原交易流水号[" + TradeContext.ORTRCNO + "]")
    
    tran_dict = {}
    if TradeContext.ROPRTPNO == '20':
        if not rccpsDBFunc.getTransTrcAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
            #======为通讯回执报文赋值===================================================
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
            out_context_dict['STRINFO']  = '原交易不存在'
            
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
            
            return True
    elif TradeContext.ROPRTPNO == '21':
        if not rccpsDBFunc.getTransBilAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
            #======为通讯回执报文赋值===================================================
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
            out_context_dict['STRINFO']  = '原交易不存在'
            
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
            
            return True
    elif TradeContext.ROPRTPNO == '30':
        if not rccpsDBFunc.getTransWtrAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
            #======为通讯回执报文赋值===================================================
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
            out_context_dict['STRINFO']  = '原交易不存在'
            
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
            
            return True
                   
    else:
        #======为通讯回执报文赋值===================================================
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
        out_context_dict['STRINFO']  = '原业务类型非法'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    if tran_dict.has_key('BJEDTE'):
        TradeContext.BOJEDT = tran_dict['BJEDTE']
    
    if tran_dict.has_key('BSPSQN'):
        TradeContext.BOSPSQ = tran_dict['BSPSQN']

    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    
    ztcbka_insert_dict = {}
    if not rccpsMap1107CTradeContext2Dztcbka.map(ztcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","为业务状态查询查复登记簿字典赋值异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束为业务状态查询查复登记簿字典赋值")
    #==========登记业务状态查询查复登记簿======================================
    AfaLoggerFunc.tradeInfo(">>>开始登记业务状态查询查复登记簿")
    
    ztcbka_insert_dict['BRSFLG']   =   PL_BRSFLG_RCV         #来账
    if TradeContext.ORCUR == 'CNY':
        ztcbka_insert_dict['CUR']  =   '01'                  #原币种
    else:
        ztcbka_insert_dict['CUR']  =   TradeContext.ORCUR    #原币种

    ztcbka_insert_dict['OCCAMT']   =   TradeContext.OROCCAMT #原金额
    
    ret = rccpsDBTrcc_ztcbka.insertCmt(ztcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","登记业务状态查询查复登记簿异常")   
        
    
    AfaLoggerFunc.tradeInfo(">>>结束登记业务状态查询查复登记簿")
    
    #======为通讯回执报文赋值===================================================
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
    
    #==将BJEDTE和BSPSQN赋到TradeContext中的BOJEDT和BOSPSQ中,为交易后处理做准备==
    TradeContext.BOJEDT    = TradeContext.BJEDTE
    TradeContext.BOSPSQ    = TradeContext.BSPSQN
    TradeContext.OQTSBNK   = TradeContext.SNDBNKCO
    TradeContext.OQTDAT    = TradeContext.BJEDTE
    TradeContext.OQTNO     = TradeContext.TRCNO
    TradeContext.ORSNDBNK  = TradeContext.SNDBNKCO
    TradeContext.ORRCVBNK  = TradeContext.RCVBNKCO
    TradeContext.ORTRCDAT  = TradeContext.TRCDAT
    TradeContext.ORTRCNO   = TradeContext.TRCNO
    TradeContext.OQTDAT    = TradeContext.TRCDAT
    TradeContext.OQTSBNK   = TradeContext.SNDBNKCO
    TradeContext.OQTNO     = TradeContext.TRCNO
    TradeContext.ORMFN     = TradeContext.MSGFLGNO
    TradeContext.ROPRTPNO  = TradeContext.OPRTYPNO
    TradeContext.RCVBNKCO  = TradeContext.SNDBNKCO
    TradeContext.RCVBNKNM  = TradeContext.SNDBNKNM
    
    if tran_dict.has_key('BCSTAT'):
        TradeContext.ORBCSTAT = tran_dict['BCSTAT']
    if tran_dict.has_key('BDWFLG'):
        TradeContext.ORBDWFLG = tran_dict['BDWFLG']
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(1.本地操作).业务状态查询报文接收[RCC006_1107]退出***' )
    
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).业务状态查询报文接收[RCC006_1107]进入***' )
    
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow("S999","发送通讯回执报文异常")
    
    if TradeContext.existVariable('ISDEAL'):
        AfaLoggerFunc.tradeInfo(">>>状态查询业务正常,成功接收,开始自动业务状态查复处理")
        
        AfaLoggerFunc.tradeInfo(">>>开始往账初始化")
        
        #=====================往账初始化============================================
        TradeContext.sysType = "rccpst"
        TradeContext.BRSFLG = PL_BRSFLG_SND
        TradeContext.TRCCO  = '9900507'
        
        TradeContext.BJEDTE=AfaUtilTools.GetSysDate( )
        TradeContext.BJETIM=AfaUtilTools.GetSysTime( )
        TradeContext.TRCDAT=AfaUtilTools.GetSysDate( )
        
        #=====================机构合法性校验========================================
        if not rccpsFunc.ChkUnitInfo( PL_BRSFLG_SND ) :
            return AfaFlowControl.ExitThisFlow("S999","机构合法性校验异常")
                
        #=====================获取平台流水号========================================
        if rccpsGetFunc.GetSerialno(PL_BRSFLG_SND) == -1 :
            return AfaFlowControl.ExitThisFlow("S999","获取平台流水号异常")
            
        #=====================获取中心流水号========================================
        if rccpsGetFunc.GetRccSerialno( ) == -1 :
            return AfaFlowControl.ExitThisFlow("S999","获取中心流水号异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束往账初始化")
        
        #=====================为状态查复业务字典赋值================================
        AfaLoggerFunc.tradeInfo(">>>开始为状态查复业务字典赋值")
        
        TradeContext.TRCNO = TradeContext.SerialNo
        TradeContext.NCCTRCST = ""
        
        if not TradeContext.existVariable('ORBCSTAT'):
            TradeContext.MBRTRCST = PL_MBRTRCST_UNRCV
        else:
            if TradeContext.ORBCSTAT == PL_BCSTAT_BNKRCV:
                TradeContext.MBRTRCST = PL_MBRTRCST_RCV
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTO or TradeContext.ORBCSTAT == PL_BCSTAT_HANG) and TradeContext.ORBDWFLG ==PL_BDWFLG_SUCC:
                TradeContext.MBRTRCST = PL_MBRTRCST_ACSUC
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTO or TradeContext.ORBCSTAT == PL_BCSTAT_HANG) and TradeContext.ORBDWFLG ==PL_BDWFLG_FAIL:
                TradeContext.MBRTRCST = PL_MBRTRCST_ACFAL
            elif(TradeContext.ORBCSTAT == PL_BCSTAT_CONFACC and TradeContext.ORBDWFLG == PL_BDWFLG_SUCC):
                TradeContext.MBRTRCST = PL_MBRTRCST_CNF
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTOPAY and TradeContext.ORBDWFLG == PL_BDWFLG_SUCC):
                TradeContext.MBRTRCST = PL_MBRTRCST_ACSUC
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTOPAY and TradeContext.ORBDWFLG == PL_BDWFLG_FAIL):
                TradeContext.MBRTRCST = PL_MBRTRCST_ACFAL
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTOPAY and TradeContext.ORBDWFLG == PL_BDWFLG_WAIT):
                TradeContext.MBRTRCTS = PL_MBRTRCST_RCV
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_CANC and TradeContext.ORBDWFLG == PL_BDWFLG_SUCC):
                TradeContext.MBRTRCTS = PL_MBRTRCST_RUSH
            else:
                TradeContext.MBRTRCTS = PL_MBRTRCST_RCV
        
        TradeContext.CONT     = "系统自动查复业务状态查询"
        
        TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
        TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
        
        ztcbka_insert_dict = {}
        if not rccpsMap1107CTradeContext2Dztcbka.map(ztcbka_insert_dict):
            return AfaFlowControl.ExitThisFlow("S999","为查复业务字典赋值异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束为状态查复业务字典赋值")
        #=====================登记状态查复业务======================================
        AfaLoggerFunc.tradeInfo(">>>开始登记状态查询查复登记簿")
        
        ret = rccpsDBTrcc_ztcbka.insert(ztcbka_insert_dict)
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","登记状态查询查复登记簿异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束登记状态查询查复登记簿")
        
        #=====================修改原查询业务查询查复标识============================
        AfaLoggerFunc.tradeInfo(">>>开始修改原查询业务查询查复标识")
        
        orztcbka_update_dict = {'ISDEAL':PL_ISDEAL_ISDO,'NCCTRCST':TradeContext.NCCTRCST,'MBRTRCST':TradeContext.MBRTRCST}
        orztcbka_where_dict  = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}

        ret = rccpsDBTrcc_ztcbka.update(orztcbka_update_dict,orztcbka_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","修改原查询业务查询查复标识异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束修改原查询业务查询查复标识")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit异常")
        AfaLoggerFunc.tradeInfo(">>>Commit成功")
        
        #=====================为业务状态查复报文赋值================================
        AfaLoggerFunc.tradeInfo(">>>开始为业务状态查复报文赋值")
        
        TradeContext.sysType  = 'rccpst'
        TradeContext.TRCCO    = '9900507'
        TradeContext.MSGTYPCO = 'SET008'
        TradeContext.SNDBRHCO = TradeContext.BESBNO
        TradeContext.SNDCLKNO = TradeContext.BETELR
        TradeContext.SNDTRDAT = TradeContext.BJEDTE
        TradeContext.SNDTRTIM = TradeContext.BJETIM
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
        TradeContext.OPRTYPNO = '99'
        TradeContext.TRANTYP  = '0'
        
        AfaLoggerFunc.tradeInfo(">>>结束为业务状态查复报文赋值")
        #=====================发送业务状态查复报文==================================
        AfaLoggerFunc.tradeInfo(">>>开始发送业务状态查复报文")
        
        AfaAfeFunc.CommAfe()
        
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow("S999","发送业务状态查复报文异常")
        
        AfaLoggerFunc.tradeInfo(">>>结束发送业务状态查复报文")
        
        AfaLoggerFunc.tradeInfo(">>>结束自动业务状态查复处理")
    
    else:
        AfaLoggerFunc.tradeInfo(">>>状态查询业务非正常,不进行自动业务状态查复处理")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：来账.中心类操作(2.中心回执).业务状态查询报文接收[RCC006_1107]退出***' )
    
    return True

