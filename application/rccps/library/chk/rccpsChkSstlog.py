# -*- coding: gbk -*-
##################################################################
#   农信银系统.函数检查类
#=================================================================
#   程序文件:   rccpsChkSstlog.py
#   修改时间:   2008-06-07
##################################################################
import TradeContext,AfaLoggerFunc
from types import *
import exceptions,os,time

################################################################################
# 函数名:    ChkSstlog()
# 参数:      无 
# 返回值：    True  设置状态成功    False 设置状态失败
# 函数说明：  检查表中的字段是否存在 
# 编写时间：   2008-6-5
# 作者：       刘雨龙
################################################################################
def ChkSstlog():
    #=====开始字段检查====
    AfaLoggerFunc.tradeInfo( '>>>开始Sstlog表字段检查' )
    #=====判断交易日期是否存在====
    if  TradeContext.existVariable( "BEJDTE" ):
        sstlog["BJEDTE"] = TradeContext.BJEDTE
    else:
        TradeContext.errorCode = 'O201'
        TradeContext.errorMsg  = '交易日期不存在'
        return False
    #=====判断报单序号是否存在====
    if  TradeContext.existVariable( "BSPSQN" ):
        sstlog["BSPSQN"] = TradeContext.BSPSQN
    else:
        TradeContext.errorCode = 'M006'
        TradeContext.errorMsg  = '报单序号不存在'
        return False
    #====判断状态是否存在====
    if TradeContext.existVariable( "BCSTAT" ):
        sstlog["BCSTAT"] = TradeContext.BCSTAT
    else:
        sstlog["BCSTAT"] = ''
    #=====判断流转处理标志是否存在====
    if TradeContext.existVariable( "BDWFLG" ):
        sstlog["BDWFLG"] = TradeContext.BDWFLG
    else:
        sstlog["BDWFLG"] = ''
    #=====判断备注1是否存在====
    if TradeContext.existVariable( 'NOTE1' ):
        sstlog['NOTE1'] = TradeContext.NOTE1
    else:
        sstlog['NOTE1'] = ''
    #=====判断备注2是否存在====
    if TradeContext.existVariable( 'NOTE2' ):
        sstlog['NOTE2'] = TradeContext.NOTE2
    else:
        sstlog['NOTE2'] = ''
    #=====判断备注3是否存在====
    if TradeContext.existVariable( 'NOTE3' ):
        sstlog['NOTE3'] = TradeContext.NOTE3
    else:
        sstlog['NOTE3'] = ''
    #=====判断备注4是否存在====
    if TradeContext.existVariable( 'NOTE4' ):
        sstlog['NOTE4'] = TradeContext.NOTE4
    else:
        sstlog['NOTE4'] = ''
    return sstlog
