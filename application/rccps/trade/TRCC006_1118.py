# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).查询书接收
#===============================================================================
#   模板文件:   TRCC006.py
#   修改时间:   2008-06-11
################################################################################
#   修改者  ：  刘雨龙
#   修改时间：  2008-07-07
#   功    能：  修改交易中workDate为BJEDTE
################################################################################
#   修改者  ：  潘广通
#   修改时间：  2008-10-29
#   功    能：  增加通存通兑部分
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc,rccpsDBFunc
import rccpsDBTrcc_hdcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1118CTradeContext2Dhdcbka_dict

from types import *
from rccpsConst import *
#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    #=====得到来账查询书的参考业务类型====
    ROPRTPNO = TradeContext.ROPRTPNO
    
    #==========判断是否重复报文,如果是重复报文,直接进入下一流程================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    hdcbka_where_dict = {}
    hdcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    hdcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    hdcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    #hdcbka_where_dict['TRCNO']    = TradeContext.ORTRCNO 
    
    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    
    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常")
        
        return True
        
    if len(hdcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("汇兑查询查复自由格式登记簿中存在相同查询交易,此报文为重复报文,直接进入下一流程,发送表示成功的通讯回执")
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
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '重复报文'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        AfaAfeFunc.CommAfe()
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>结束检查是否重复报文")
    
    #=====判断交易类型====
    if( TradeContext.ROPRTPNO == '20' ):    #汇兑
        AfaLoggerFunc.tradeInfo("进入汇兑处理")
        #==========为汇兑查询查复自由格式登记簿字典赋值================================
        AfaLoggerFunc.tradeInfo(">>>开始为汇兑查询查复自由格式登记簿字典赋值")
        
        tran_dict = {}
        #if not rccpsDBFunc.getTransTrcPK(TradeContext.ORMFN[:10],TradeContext.ORMFN[10:18],TradeContext.ORMFN[18:26],tran_dict):
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
            out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
            out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
            out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
            out_context_dict['OPRTYPNO'] = '99'
            out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
            out_context_dict['TRANTYP']  = '0'
            out_context_dict['ORTRCCO']  = TradeContext.TRCCO
            out_context_dict['PRCCO']    = 'RCCI0000'
            out_context_dict['STRINFO']  = '无原汇兑交易'
        
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
            AfaAfeFunc.CommAfe()
        
            return AfaFlowControl.ExitThisFlow('S999','无原交易，丢弃此报文') 
        
        if tran_dict.has_key('BJEDTE'):
            TradeContext.BOJEDT = tran_dict['BJEDTE']
        
        if tran_dict.has_key('BSPSQN'):
            TradeContext.BOSPSQ = tran_dict['BSPSQN']
        
        TradeContext.ISDEAL = PL_ISDEAL_UNDO
        TradeContext.PYRACC = tran_dict['PYRACC']     #付款人账号
        TradeContext.PYEACC = tran_dict['PYEACC']     #收款人账号
        
        #=====张恒 20091010 新增 将机构落到原交易机构 ====
        TradeContext.BESBNO = tran_dict['BESBNO']     #接收机构号
        
        hdcbka_insert_dict = {}
        if not rccpsMap1118CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
            return AfaFlowControl.ExitThisFlow("S999","为汇兑查询查复自由格式登记簿字典赋值异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束为汇兑查询查复自由格式登记簿字典赋值")
        
    elif( TradeContext.ROPRTPNO == '30' ):    #通存通兑
        AfaLoggerFunc.tradeInfo("进入通存通兑处理")
        #==========为汇兑查询查复自由格式登记簿字典赋值================================
        AfaLoggerFunc.tradeInfo(">>>开始为汇兑查询查复自由格式登记簿字典赋值")
        
        wtrbka_dict = {}
        if not rccpsDBFunc.getTransWtrAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,wtrbka_dict):
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
            out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
            out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
            out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
            out_context_dict['OPRTYPNO'] = '99'
            out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
            out_context_dict['TRANTYP']  = '0'
            out_context_dict['ORTRCCO']  = TradeContext.TRCCO
            out_context_dict['PRCCO']    = 'RCCI0000'
            out_context_dict['STRINFO']  = '无原通存通兑交易'
        
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
            AfaAfeFunc.CommAfe()
        
            return AfaFlowControl.ExitThisFlow('S999','无原交易，丢弃此报文') 
        
        if wtrbka_dict.has_key('BJEDTE'):
            TradeContext.BOJEDT = wtrbka_dict['BJEDTE']
        
        if wtrbka_dict.has_key('BSPSQN'):
            TradeContext.BOSPSQ = wtrbka_dict['BSPSQN']
        
        TradeContext.ISDEAL = PL_ISDEAL_UNDO
        TradeContext.PYRACC = wtrbka_dict['PYRACC']     #付款人账号
        TradeContext.PYEACC = wtrbka_dict['PYEACC']     #收款人账号
        
        
        hdcbka_insert_dict = {}
        if not rccpsMap1118CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
            return AfaFlowControl.ExitThisFlow("S999","为汇兑查询查复自由格式登记簿字典赋值异常")
            
        AfaLoggerFunc.tradeInfo(">>>结束为汇兑查询查复自由格式登记簿字典赋值")
        
    else:
        return AfaFlowControl.ExitThisFlow("S999","没有此交易类型")
          
    #==========登记汇兑查询查复自由格式登记簿======================================
    AfaLoggerFunc.tradeInfo(">>>开始登记汇兑查询查复自由格式登记簿")

    hdcbka_insert_dict['BRSFLG']   =   PL_BRSFLG_RCV        #来账
    if TradeContext.ORCUR == 'CNY':
        hdcbka_insert_dict['CUR']      =   '01'   #原币种
    else:
        hdcbka_insert_dict['CUR']      =   TradeContext.ORCUR   #原币种

    hdcbka_insert_dict['OCCAMT']   =   TradeContext.OROCCAMT #原金额
    
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","登记汇兑查询查复自由格式登记簿异常") 
    
    
    AfaLoggerFunc.tradeInfo(">>>结束登记汇兑查询查复自由格式登记簿")
    
    #======为通讯回执报文赋值===================================================回执前置里只要三个字段.1.2.末
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
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow("S999","发送通讯回执报文异常")
        
    return True
