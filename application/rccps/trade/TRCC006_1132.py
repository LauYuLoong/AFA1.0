# -*- coding: gbk -*-
################################################################################
#   农信银系统：来账.中心类操作(1.本地操作 2.中心回执).汇票查复书接收
#===============================================================================
#   交易文件:   TRCC006_1132.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  关彬捷
#   修改时间:   2008-06-20
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_hpcbka
import rccpsMap0000Dout_context2CTradeContext,rccpsMap1132CTradeContext2Dhpcbka


#=====================交易前处理(登记流水,中心前处理)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("***农信银系统：来账.中心类操作(1.本地操作).汇票查复书接收[TRC006_1132]进入***")
    
    #================检查是否重复报文===========================================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否重复报文")
    
    hpcbka_where_dict = {}
    hpcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    hpcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    hpcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    hpcbka_dict = rccpsDBTrcc_hpcbka.selectu(hpcbka_where_dict)
    
    if hpcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","校验重复报文异常") 
        
    if len(hpcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("业务状态登记簿中存在相同查复交易,此报文为重复报文,直接进入下一流程,发送表示成功的通讯回执")
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
    
    #================判断是否存在原查询交易=====================================
    AfaLoggerFunc.tradeInfo(">>>开始检查是否存在原查询交易")
    
    or_hpcbka_where_dict = {}
    or_hpcbka_where_dict['SNDBNKCO'] = TradeContext.OQTSBNK
    or_hpcbka_where_dict['TRCDAT']   = TradeContext.ORQYDAT
    or_hpcbka_where_dict['TRCNO']    = TradeContext.OQTNO
    
    or_hpcbka_dict = rccpsDBTrcc_hpcbka.selectu(or_hpcbka_where_dict)
    
    if or_hpcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","查询原查询交易信息异常")
        
    if len(or_hpcbka_dict) <= 0:
        AfaLoggerFunc.tradeInfo("汇票登记簿中不存在原查询交易,进入下一流程,发送表示成功的通讯回执")
        #======为通讯回执报文赋值===============================================
        out_context_dict = {}
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
        out_context_dict['STRINFO']  = '汇票查询查复登记簿中不存在原查询交易'
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    AfaLoggerFunc.tradeInfo(">>>结束检查是否存在原查询交易")
    
    #================为汇票查询查复登记簿字典赋值===============================
    AfaLoggerFunc.tradeInfo(">>>开始为汇票查询查复登记簿赋值")
    
    #=====币种转换====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'
    
    TradeContext.BOJEDT = or_hpcbka_dict['BJEDTE']
    TradeContext.BOSPSQ = or_hpcbka_dict['BSPSQN']
    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    TradeContext.PYEACC = TradeContext.ORPYENAM
    
    hpcbka_dict = {}
    if not rccpsMap1132CTradeContext2Dhpcbka.map(hpcbka_dict):
        return AfaFlowControl.ExitThisFlow("S999","为汇票查询查复登记簿赋值异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束为汇票查询查复登记簿赋值")
    
    #================登记查询查复登记簿=========================================
    AfaLoggerFunc.tradeInfo(">>>开始登记查询查复登记簿")
    
    ret = rccpsDBTrcc_hpcbka.insertCmt(hpcbka_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","登记汇票查询查复登记簿异常")
    
    AfaLoggerFunc.tradeInfo(">>>结束登记查询查复登记簿")
    
    #================为通讯回执报文赋值=========================================
    AfaLoggerFunc.tradeInfo(">>>开始为通讯回执报文赋值")
    
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
    
    AfaLoggerFunc.tradeInfo(">>>结束为通讯回执报文赋值")
    
    #=====pgt 0910 更改原交易的查复状态====
    AfaLoggerFunc.tradeInfo(">>>更改原交易查复标示")
    or_hpcbka_where_dict = {}
    or_hpcbka_where_dict = {'BJEDTE':or_hpcbka_dict['BJEDTE'],'BSPSQN':or_hpcbka_dict['BSPSQN']}
    or_hpcbka_update_dict = {'ISDEAL':'1'}
    ret = rccpsDBTrcc_hpcbka.updateCmt(or_hpcbka_update_dict,or_hpcbka_where_dict)
    if( ret < 0 ):
        return AfaFlowControl.ExitThisFlow("S999", "登记汇票查询查复登记簿异常")
    
    AfaLoggerFunc.tradeInfo("***农信银系统：来账.中心类操作(1.本地操作).汇票查询书接收[TRC006_1132]进入***")
    
    return True


#=====================交易后处理================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("***农信银系统：来账.中心类操作(2.中心回执).汇票查复书接收[TRC006_1132]进入***")
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(errorCode,errorMsg)
    
    AfaLoggerFunc.tradeInfo("***农信银系统：来账.中心类操作(2.中心回执).汇票查复书接收[TRC006_1132]进入***")
    
    return True
        
