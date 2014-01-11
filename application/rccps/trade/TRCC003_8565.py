# -*- coding: gbk -*-
###############################################################################
#   农信银系统：往账.中心类操作(1.本地操作 2.中心操作).柜台冲销
#==============================================================================
#   交易文件:   TRCC003_8565.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-11-29
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,HostContext
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsEntries,rccpsHostFunc,rccpsGetFunc
import rccpsDBTrcc_mpcbka
import rccpsMap8565CTradeContext2Dmpcbka


#=====================交易前处理(本地操作,中心前处理)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).柜台冲销[TRCC003_8565]进入***' )
    
    #=====校验变量的合法性====
    if not TradeContext.existVariable("BOJEDT"):
        return AfaFlowControl.ExitThisFlow('A099','原交易日期不能为空')  
        
    if not TradeContext.existVariable("BOSPSQ"):
        return AfaFlowControl.ExitThisFlow('A099','原报单序号不能为空')
        
    if not TradeContext.existVariable("RESNNM"):
        return AfaFlowControl.ExitThisFlow('A099','冲销原因不能为空')
    
    #查询原交易信息
    wtr_dict = {}
    
    if not rccpsDBFunc.getTransWtr(TradeContext.BOJEDT,TradeContext.BOSPSQ,wtr_dict):
        return AfaFlowControl.ExitThisFlow("S999","无此交易")
       
    #判断原交易是否为往账
    if( wtr_dict['BRSFLG'] != PL_BRSFLG_SND):
        return AfaFlowControl.ExitThisFlow('A099','此交易非往账,禁止冲销')
        
    #判断被冲销交易的日期是否为当日
    if( wtr_dict['NCCWKDAT'] != TradeContext.NCCworkDate ):
        return AfaFlowControl.ExitThisFlow('A099','此交易非当日交易,禁止冲销')
        
    #判断当前机构是否为原交易机构
    if( wtr_dict['BESBNO'] != TradeContext.BESBNO ):
        return AfaFlowControl.ExitThisFlow('A099','当前机构非原交易机构,禁止冲销')
    
    #判断当前柜员是否为原交易柜员
    if( wtr_dict['BETELR'] != TradeContext.BETELR ):
        return AfaFlowControl.ExitThisFlow('A099','当前柜员非原交易柜员,禁止冲销')
    
    #判断原交易状态是否允许冲销
    AfaLoggerFunc.tradeInfo("开始判断原交易信息是否允许冲销")
    
    #=====add by pgt 12-9=====
    #able_to_cancel = 1    #允许冲销的标示，1为不允许，0为允许
    #
    #if wtr_dict['TRCCO'] in ('3000002','3000003','3000004','3000005'):    #通存或者本转异
    #    #状态为:确认付款,清算,发送处理中,发送成功,允许冲销
    #    if(wtr_dict['BCSTAT'] == PL_BCSTAT_CONFPAY or wtr_dict['BCSTAT'] == PL_BCSTAT_MFESTL or (wtr_dict['BCSTAT'] == PL_BCSTAT_SND and (wtr_dict['BDWFLG'] == PL_BDWFLG_WAIT or wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC))):
    #        able_to_cancel = 0
    #        
    #elif wtr_dict['TRCCO'] in ('3000102','3000103','3000104','3000105'):    #通兑或者异转本
    #    #状态为:记账,清算,发送处理中,发送成功,允许冲销
    #    if(wtr_dict['BCSTAT'] == PL_BCSTAT_ACC or wtr_dict['BCSTAT'] == PL_BCSTAT_MFESTL or (wtr_dict['BCSTAT'] == PL_BCSTAT_SND and (wtr_dict['BDWFLG'] == PL_BDWFLG_WAIT or wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC))):
    #        able_to_cancel = 0
    #        
    #else:
    #    return AfaFlowControl.ExitThisFlow("S999","本交易非通存或通兑账务类交易,禁止冲销")
    #
    ##冲销失败允许冲销
    #if(wtr_dict['BCSTAT'] == PL_BCSTAT_CANC and wtr_dict['BDWFLG'] == PL_BDWFLG_FAIL):   
    #    able_to_cancel = 0
    #     
    #if(able_to_cancel == 1):
    #    return AfaFlowControl.ExitThisFlow("S999","此交易当前状态为[" + wtr_dict['BCSTAT'] + "][" + wtr_dict['BDWFLG'] + "],禁止冲销")
    #    
    #else:
    #    AfaLoggerFunc.tradeDebug('>>>>>>此交易当前状态允许冲销')
        
    if wtr_dict['TRCCO'] in ('3000002','3000003','3000004','3000005'):    #通存或者本转异
        #状态为:确认付款,清算,发送处理中,发送成功,允许冲销
    	if not (wtr_dict['BCSTAT'] == PL_BCSTAT_CONFPAY or wtr_dict['BCSTAT'] == PL_BCSTAT_MFESTL or (wtr_dict['BCSTAT'] == PL_BCSTAT_SND and (wtr_dict['BDWFLG'] == PL_BDWFLG_WAIT or wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC))):
    	    return AfaFlowControl.ExitThisFlow("S999","此交易当前状态为[" + wtr_dict['BCSTAT'] + "[" + wtr_dict['BDWFLG'] + "],禁止冲销")
    
    elif wtr_dict['TRCCO'] in ('3000102','3000103','3000104','3000105'):    #通兑或者异转本
        #状态为:记账,清算,发送处理中,发送成功,允许冲销
    	if not (wtr_dict['BCSTAT'] == PL_BCSTAT_ACC or wtr_dict['BCSTAT'] == PL_BCSTAT_MFESTL or (wtr_dict['BCSTAT'] == PL_BCSTAT_SND and (wtr_dict['BDWFLG'] == PL_BDWFLG_WAIT or wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC))):
    		return AfaFlowControl.ExitThisFlow("S999","此交易当前状态为[" + wtr_dict['BCSTAT'] + "][" + wtr_dict['BDWFLG'] + "],禁止冲销")
    else:
        return AfaFlowControl.ExitThisFlow("S999","本交易非通存或通兑账务类交易,禁止冲销")
        
    if wtr_dict['BCSTAT'] == PL_BCSTAT_ACC and wtr_dict['BDWFLG'] != PL_BDWFLG_SUCC:
        #原交易当前状态为记账,且流转处理标识非成功,则调用8816查询此笔业务主机账务状态
        
        AfaLoggerFunc.tradeDebug('>>>调用8816查找该业务[' + wtr_dict['BSPSQN'] + '状态')

        TradeContext.HostCode = '8816'                   #主机交易码
        TradeContext.OPFG     = '1'                      #查询类型
        TradeContext.NBBH     = 'RCC'                    #代理业务标识
        TradeContext.FEDT     = wtr_dict['FEDT']         #原前置日期
        TradeContext.RBSQ     = wtr_dict['RBSQ']         #原前置流水号
        TradeContext.DAFG     = '1'                      #抹/记账标志  1:记  2:抹
        TradeContext.BESBNO   = wtr_dict['BESBNO']       #机构号
        TradeContext.BETELR   = wtr_dict['BETELR']       #柜员号

        rccpsHostFunc.CommHost( TradeContext.HostCode )

        #=====分析主机返回====
        if TradeContext.errorCode == '0000':
            if HostContext.O1STCD == '0':
                #此账务已成功记主机账,修改原交易状态为记账成功
                stat_dict = {}
                stat_dict['BJEDTE'] = TradeContext.BOJEDT
                stat_dict['BOSPSQ'] = tradeContext.BOSPSQ
                stat_dict['BCSTAT'] = PL_BCSTAT_ACC
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['TRDT']   = HostContext.O1DADT           #主机日期
                stat_dict['TLSQ']   = HostContext.O1AMTL           #主机流水
                stat_dict['MGID']   = '0000'
                stat_dict['STRINFO']= '主机成功'
                
                if not rccpsState.setTransState(stat_dict):
                    return AfaFlowControl.ExitThisFlow('S999','设置原交易业务状态为记账成功异常') 
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit异常")
            else:
                return AfaFlowControl.ExitThisFlow('S999','原交易主机账务状态与中台不符,禁止提交')
        
        elif TradeContext.errorCode == 'XCR0001':
            AfaLoggerFunc.tradeInfo(">>>主机返回原交易记账失败,继续冲销")
            
        else:
            return AfaFlowControl.ExitThisFlow('S999','查询主机账务异常,请稍后再冲销')
            
    
    AfaLoggerFunc.tradeInfo("结束判断原交易信息是否允许冲销")
    		
    #登记柜台冲销登记簿
    AfaLoggerFunc.tradeInfo("开始登记柜台冲销登记簿")
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = wtr_dict['RCVMBRCO']
    TradeContext.ORTRCDAT = wtr_dict['TRCDAT']
    TradeContext.OPRNO    = PL_TDOPRNO_CX
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.NCCworkDate + TradeContext.SerialNo
    TradeContext.ORMFN    = wtr_dict['MSGFLGNO']
    TradeContext.TRCCO    = "3000504" 
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.ORTRCCO  = wtr_dict['TRCCO']
    TradeContext.ORTRCNO  = wtr_dict['TRCNO']
    TradeContext.SNDBNKCO = wtr_dict['SNDBNKCO']
    TradeContext.SNDBNKNM = wtr_dict['SNDBNKNM']
    TradeContext.RCVBNKCO = wtr_dict['RCVBNKCO']
    TradeContext.RCVBNKNM = wtr_dict['RCVBNKNM']
    
    insert_dict = {}
    
    if not rccpsMap8565CTradeContext2Dmpcbka.map(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','登记柜台冲销登记簿失败')
    
    AfaLoggerFunc.tradeInfo('>>>开始登记柜台冲销登记簿')
    res = rccpsDBTrcc_mpcbka.insertCmt(insert_dict)
    if( res <= 0 ):
        return AfaFlowControl.ExitThisFlow('S999','登记柜台冲销登记簿失败')
        
    AfaLoggerFunc.tradeInfo('>>>结束登记柜台冲销登记簿')
    
    #为发送柜面冲销报文做准备
    #=====报文头====
    TradeContext.MSGTYPCO = 'SET009'
    TradeContext.RCVSTLBIN= wtr_dict['RCVMBRCO']
    #TradeContext.SNDBRHCO = TradeContext.BESBNO
    #TradeContext.SNDCLKNO = TradeContext.BETELR
    #TradeContext.SNDTRDAT = TradeContext.BJEDTE
    #TradeContext.SNDTRTIM = TradeContext.BJETIM
    #TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    #TradeContext.ORMFN    = wtr_dict['MSGFLGNO']
    #TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "30"
    TradeContext.ROPRTPNO = "30"
    TradeContext.TRANTYP  = "0"
    #=====业务要素集====
    TradeContext.CUR      = wtr_dict['CUR']
    TradeContext.OCCAMT   = str(wtr_dict['OCCAMT'])
    
    #手续费处理
    if wtr_dict['TRCCO'] == '3000002' or wtr_dict['TRCCO'] == '3000003' or wtr_dict['TRCCO'] == '3000004' or wtr_dict['TRCCO'] == '3000005':
        TradeContext.CUSCHRG  = "0.00"
    elif wtr_dict['TRCCO'] == '3000102' or wtr_dict['TRCCO'] == '3000103' or wtr_dict['TRCCO'] == '3000104' or wtr_dict['TRCCO'] == '3000105':
        if wtr_dict['CHRGTYP'] == '1':
            TradeContext.CUSCHRG = str(wtr_dict['CUSCHRG'])
        else:
            TradeContext.CUSCHRG = '0.00'
            
    TradeContext.PYRACC   = wtr_dict['PYRACC']
    TradeContext.PYRNAM   = wtr_dict['PYRNAM']
    TradeContext.PYEACC   = wtr_dict['PYEACC']
    TradeContext.PYENAM   = wtr_dict['PYENAM']
    TradeContext.CURPIN   = ""
    TradeContext.STRINFO  = ""
    TradeContext.PRCCO    = ""
    #=====扩展要素集====
    TradeContext.RESNCO = TradeContext.RESNNM  
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(1.本地操作).柜台冲销[TRCC003_8565]退出***' )
    return True

#=====================交易后处理===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).柜台冲销[TRCC003_8565]进入***' )
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    #判断是否发送成功
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo(">>>冲销报文发送成功")
        
    else:
        AfaLoggerFunc.tradeInfo(">>>冲销报文发送失败")
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.中心类操作(2.中心操作).柜台冲销[TRCC003_8565]退出***' )
    return True
    
