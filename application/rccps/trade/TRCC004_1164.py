# -*- coding: gbk -*-
##################################################################
#   农信银.通存通兑来账交易.错帐控制/解控应答报文接收    #我方主动请求错帐控制和解控第三方返回报文 我行作为受理行发送错帐控制解控请求报文
#=================================================================
#   程序文件:   TRCC004_1164.py
#   修改时间:   2011—05-16
#   作者：      曾照泰
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc
import rccpsDBTrcc_acckj
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
    AfaLoggerFunc.tradeInfo("检查是否有对应的请求报文")  #
    acckj_where_dict = {'TRCDAT':TradeContext.ORMFN[10:18],'TRCNO':TradeContext.ORMFN[18:],'SNDMBRCO':TradeContext.ORMFN[:10]} #从参考报文标识号中取数据
    res = rccpsDBTrcc_acckj.selectu(acckj_where_dict)
    if( res == None ):
        return AfaFlowControl.ExitThisFlow('A099','检查对应的请求报文失败')
        
    if( len(res) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','没有对应的请求报文')   
        
             
    #=====组织更新字典====
    AfaLoggerFunc.tradeInfo("开始组织更新字典")
    update_dict = {}
    
    if(TradeContext.TRCCO=='3000508'):   #更新错帐控制返回结果
        if (TradeContext.PRCCO=='RCCI0000'):
            update_dict['CONSTS']  = '0'
        else:
            update_dict['CONSTS']  = '1'  
            update_dict['STRINFO']   = "错帐控制失败，" + TradeContext.STRINFO 
        update_dict['PRCCO']     = TradeContext.PRCCO                                #交易码    
        update_dict['BALANCE']   = TradeContext.BALANCE                              #账户实际金额
        update_dict['STRINFO']   = TradeContext.STRINFO                              #响应信息（附言）   
    
    if(TradeContext.TRCCO=='3000509'):  #更新错帐解控返回结果
        if (TradeContext.PRCCO=='RCCI0000'):
            update_dict['UNCONRST']  = '0'
        else:
            update_dict['UNCONRST']  = '1'    
            update_dict['STRINFO']   = "错帐解控失败，"+ TradeContext.STRINFO 
        update_dict['PRCCO']     = TradeContext.PRCCO                                #交易码     
        update_dict['STRINFO']   = TradeContext.STRINFO                              #响应信息（附言）   
   
    where_dict = {}
    where_dict['TRCDAT']     = TradeContext.TRCDAT                   #委托日期
    where_dict['TRCNO']      = TradeContext.TRCNO                    #交易流水号
    where_dict['SNDBNKCO']   = TradeContext.SNDBNKCO                 #发送行行号
    
    #=====更新错帐控制解控登记簿====
    AfaLoggerFunc.tradeInfo("更新错帐控制解控登记簿")
    res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','更新错帐控制解控登记簿')

    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '交易成功'
    
    AfaLoggerFunc.tradeInfo("回执个性化处理(本地操作)  退出")
    
    return True