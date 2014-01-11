# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑来账交易.卡余额查询应答报文接收
#=================================================================
#   程序文件:   TRCC004_1150.py
#   修改时间:   2008-10-21
#   作者：      潘广通
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc
import rccpsDBTrcc_balbka
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("回执个性化处理(本地操作)  进入")
    
    #=====校验变量的有效性====
    AfaLoggerFunc.tradeInfo("校验变量的有效性")
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A099','没有委托日期')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A099','没有交易流水号')
        
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','没有发起行行号')
        
    #=====检查是否有对应的请求报文====
    AfaLoggerFunc.tradeInfo("检查是否有对应的请求报文")
    balbka_where_dict = {'TRCDAT':TradeContext.ORMFN[10:18],'TRCNO':TradeContext.ORMFN[18:],'SNDMBRCO':TradeContext.ORMFN[:10]}
    res = rccpsDBTrcc_balbka.selectu(balbka_where_dict)
    if( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','检查对应的请求报文失败')
        
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','没有对应的请求报文')   
        
             
    #=====组织更新字典====
    AfaLoggerFunc.tradeInfo("开始组织更新字典")
    update_dict = {}
    update_dict['AVLBAL']  = TradeContext.AVLBAL
    update_dict['ACCBAL']  = TradeContext.ACCBAL
    update_dict['PRCCO']   = TradeContext.PRCCO
    #update_dict['PRCINFO'] = "AFE发送成功，已收到应答报文"
    update_dict['STRINFO'] = TradeContext.STRINFO
    where_dict = {}
    where_dict['TRCDAT']   = TradeContext.TRCDAT
    where_dict['TRCNO']    = TradeContext.TRCNO
    where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    
    #=====更新余额查询登记簿====
    AfaLoggerFunc.tradeInfo("更新余额查询登记簿")
    res = rccpsDBTrcc_balbka.updateCmt(update_dict,where_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','更新余额查询登记簿失败')

    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '交易成功'
    
    AfaLoggerFunc.tradeInfo("回执个性化处理(本地操作)  退出")
    
    return True