# -*- coding: gbk -*-
##################################################################
#   农信银.农信银.查询打印业务.卡BIN行号查询
#=================================================================
#   程序文件:   TRCC001_8551.py
#   修改时间:   2008-11-12
#   作者：      刘振东
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc
import rccpsDBTrcc_cadbnk,rccpsDBTrcc_paybnk
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo('***农信银系统：往账.本地类操作(1.本地操作)卡BIN行号查询[TRCC001_8551]进入***')
    
    start_no = 1                            #起始笔数
    sel_size = 10                           #查询笔数
    
    #=====校验变量的有效性====
    AfaLoggerFunc.tradeInfo("校验变量的有效性")
    
    if not (TradeContext.existVariable( "CARDBIN" ) and TradeContext.CARDBIN != "" ):
        return AfaFlowControl.ExitThisFlow('A099','卡BIN[CARDBIN]不存在' )
    
    #===== 检查卡BIN位数====     
    AfaLoggerFunc.tradeInfo(">>>开始组织查询语句")
    i = 12
    bankcode = ""
    while( i >=6 ):
        cardbin = TradeContext.CARDBIN[:i]
        wheresql = "CARDBIN like '" + cardbin + "%'"
        ordersql = " order by CARDBIN DESC"
        
        AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
        record = rccpsDBTrcc_cadbnk.selectm(start_no,sel_size,wheresql,ordersql)
        if( record == None ):
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )  
            
        elif( len(record) == 0 ):
            i = i-1 
            
        else:
            bankcode = record[0]['BANKBIN']
            break
    
    if( i < 6 ):
        return AfaFlowControl.ExitThisFlow('A099','无此卡BIN' )
   
    TradeContext.BANKBIN = bankcode
        
    #=====生成查询条件====
    wheresql_dic={}
    wheresql_dic['BANKBIN']=TradeContext.BANKBIN
    AfaLoggerFunc.tradeInfo( "wheresql_dic="+TradeContext.BANKBIN)
                
    #=====开始查询数据库====
    records=rccpsDBTrcc_paybnk.selectu(wheresql_dic)
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('A099','没有查找到数据')
    else:    
        #=====输出接口====
        TradeContext.BANKNAM=records['BANKNAM']
    
    #=====输出接口赋值====
    AfaLoggerFunc.tradeInfo(">>>输出接口赋值")
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '成功'
    TradeContext.BANKBIN = bankcode
    
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)卡BIN行号查询[TRCC001_8551]退出***')
    return True
    