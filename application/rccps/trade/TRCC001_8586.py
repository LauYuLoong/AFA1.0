# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作模板(1.本地操作).网银专用往账联动查询
#===============================================================================
#   交易文件:   TRCC001_8586.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  张恒
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsMap8554Dtrcbka2CTradeContext,rccpsDBTrcc_trcbka
from types import *

#=====================个性化处理(本地操作)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8554]进入***' )
    
    ##===张恒增加于20091230==== 
    trcbka_where_dict1={}
    trcbka_where_dict1 = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}            
 
    #==========查询汇兑登记簿相关业务信息=======================================
    trcbka_dict = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict1)  
    
    if trcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '查询汇兑业务登记簿交易信息异常' )
        
    if len(trcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '汇兑业务登记簿中无此交易信息' )
    if trcbka_dict['BESBNO'] != TradeContext.BESBNO :
        return AfaFlowControl.ExitThisFlow( 'S999', '非本机构业务!' )
    ##====end=================
    
    #=====查询汇兑单笔信息====
    trcbka = {}
    bka = rccpsDBFunc.getTransTrc(TradeContext.BJEDTE,TradeContext.BSPSQN,trcbka)
    if bka == False:
        return  AfaFlowControl.ExitThisFlow('M999','查询单笔信息失败') 
    else:
        AfaLoggerFunc.tradeInfo( '>>>查询成功' )
        #=====字典赋值到TradeContext====
        rccpsMap8554Dtrcbka2CTradeContext.map(trcbka)
        
    TradeContext.OCCAMT    = str(trcbka['OCCAMT'])              #金额
    TradeContext.LOCCUSCHRG    = str(trcbka['LOCCUSCHRG'])      #手续费金额 增加于20091228  张恒
    
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '查询成功'

    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8554]退出***' )
    return True
