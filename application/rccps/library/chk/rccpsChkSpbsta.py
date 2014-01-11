# -*- coding: gbk -*-
##################################################################
#   农信银系统.函数检查类
#=================================================================
#   程序文件:   rccpsChkSpbsta.py
#   修改时间:   2008-06-07
##################################################################
import TradeContext,AfaLoggerFunc
from types import *
import exceptions,os,time

################################################################################
# 函数名:    ChkSpbsta()
# 参数:      无 
# 返回值：    True  设置状态成功    False 设置状态失败
# 函数说明：  检查表中的字段是否存在 
# 编写时间：   2008-6-5
# 作者：       刘雨龙
################################################################################
def ChkSpbsta():
    #=====开始字段检查====
    AfaLoggerFunc.tradeInfo( '>>>开始Spbsta表字段检查' )
    #=====判断交易日期是否存在====
    if  TradeContext.existVariable( "BEJDTE" ):
        spbsta["BJEDTE"] = TradeContext.BJEDTE
    else:
        TradeContext.errorCode = 'O201'
        TradeContext.errorMsg  = '交易日期不存在'
        return False
    #=====判断报单序号是否存在====
    if  TradeContext.existVariable( "BSPSQN" ):
        spbsta["BSPSQN"] = TradeContext.BSPSQN
    else:
        TradeContext.errorCode = 'M006'
        TradeContext.errorMsg  = '报单序号不存在'
        return False
    #====判断状态是否存在====
    if TradeContext.existVariable( "BCSTAT" ):
        spbsta["BCSTAT"] = TradeContext.BCSTAT
    else:
        spbsta["BCSTAT"] = ''
    #=====判断流转处理标志是否存在====
    if TradeContext.existVariable( "BDWFLG" ):
        spbsta["BDWFLG"] = TradeContext.BDWFLG
    else:
        spbsta["BDWFLG"] = ''
    #=====判断备注1是否存在====
    if TradeContext.existVariable( 'NOTE1' ):
        spbsta['NOTE1'] = TradeContext.NOTE1
    else:
        spbsta['NOTE1'] = ''
    #=====判断备注2是否存在====
    if TradeContext.existVariable( 'NOTE2' ):
        spbsta['NOTE2'] = TradeContext.NOTE2
    else:
        spbsta['NOTE2'] = ''
    #=====判断备注3是否存在====
    if TradeContext.existVariable( 'NOTE3' ):
        spbsta['NOTE3'] = TradeContext.NOTE3
    else:
        spbsta['NOTE3'] = ''
    #=====判断备注4是否存在====
    if TradeContext.existVariable( 'NOTE4' ):
        spbsta['NOTE4'] = TradeContext.NOTE4
    else:
        spbsta['NOTE4'] = ''
    return spbsta
