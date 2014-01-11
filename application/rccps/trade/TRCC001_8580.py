# -*- coding: gbk -*-
##################################################################
#   农信银.查询打印.通存通兑往账联动交易
#=================================================================
#   程序文件:   TRCC001_8580.py
#   修改时间:   2008-10-23
#   作者：      潘广通
##################################################################

import rccpsDBTrcc_wtrbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("个性化处理(本地操作)")
    
    #=====校验变量的合法性====
    if( not TradeContext.existVariable( "BJEDTE" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '交易日期不存在')
    
    if( not TradeContext.existVariable( "BSPSQN" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '报单序号不存在')
        
    #=====组织查询字典====
    where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BESBNO':TradeContext.BESBNO}
    
    #=====开始查询通存通兑业务登记簿====
    AfaLoggerFunc.tradeInfo("开始查询通存通兑业务登记簿")
    record = rccpsDBTrcc_wtrbka.selectu(where_dict)
    if( record == None ):
        return AfaFlowControl.ExitThisFlow('A099', '查询通存通兑业务登记簿失败')
        
    elif( len(record) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099', '查询通存通兑业务登记簿为空')
        
    else:
#        #=====判断是否为往账业务====
#        if( record['BRSFLG'] == PL_BRSFLG_RCV ):
#            return AfaFlowControl.ExitThisFlow('A099', '该笔业务不是往账业务')
            
        #=====开始组织输出接口====
        AfaLoggerFunc.tradeInfo("开始组织输出接口")    
          
        TradeContext.BJEDTE     = record['BJEDTE']
        TradeContext.BSPSQN     = record['BSPSQN']
        TradeContext.BRSFLG     = record['BRSFLG']
        TradeContext.BESBNO     = record['BESBNO']   
        TradeContext.BETELR     = record['BETELR']
        TradeContext.BEAUUS     = record['BEAUUS']
        TradeContext.DCFLG      = record['DCFLG']
        TradeContext.OPRNO      = record['OPRNO']
        TradeContext.NCCWKDAT   = record['NCCWKDAT']
        TradeContext.TRCCO      = record['TRCCO']
        TradeContext.TRCDAT     = record['TRCDAT']
        TradeContext.TRCNO      = record['TRCNO']
        TradeContext.COTRCNO    = record['COTRCNO']
        TradeContext.SNDMBRCO   = record['SNDMBRCO']
        TradeContext.RCVMBRCO   = record['RCVMBRCO']
        TradeContext.SNDBNKCO   = record['SNDBNKCO']
        TradeContext.SNDBNKNM   = record['SNDBNKNM']
        TradeContext.RCVBNKCO   = record['RCVBNKCO']
        TradeContext.RCVBNKNM   = record['RCVBNKNM']
        TradeContext.CUR        = record['CUR']
        TradeContext.OCCAMT     = str(record['OCCAMT'])
        TradeContext.CHRGTYP    = record['CHRGTYP']
        TradeContext.CUSCHRG    = str(record['CUSCHRG'])
        TradeContext.PYRACC     = record['PYRACC']
        TradeContext.PYRNAM     = record['PYRNAM']
        TradeContext.PYEACC     = record['PYEACC']
        TradeContext.PYENAM     = record['PYENAM']
        TradeContext.STRINFO    = record['STRINFO']
        TradeContext.CERTTYPE   = record['CERTTYPE']
        TradeContext.CERTNO     = record['CERTNO']
        TradeContext.BNKBKNO    = record['BNKBKNO']
        TradeContext.BNKBKBAL   = str(record['BNKBKBAL'])
        
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '交易成功'
    
    return True
        