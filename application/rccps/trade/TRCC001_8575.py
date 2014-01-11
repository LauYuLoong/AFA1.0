# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).余额查询登记簿查询
#===============================================================================
#   模板文件:   TRCC001_8575.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘振东
#   修改时间:   2008-11-21
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_balbka

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作).余额查询登记簿查询[TRCC001_8575]进入***' )
    
    #=====判断输入接口是否存在====
    if( not TradeContext.existVariable( "BJEDTE" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '报单日期[BJEDTE]不存在')
        
    if( not TradeContext.existVariable( "BSPSQN" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '报单序号[BSPSQN]不存在')
        
    #=====组织查询字典====
    AfaLoggerFunc.tradeInfo(">>>开始组织查询字典")
    
    wheresql_dic={}
    wheresql_dic['BJEDTE']=TradeContext.BJEDTE
    wheresql_dic['BESBNO']=TradeContext.BESBNO
    
    if(len(TradeContext.BSPSQN) != 0):
        wheresql_dic['BSPSQN']=TradeContext.BSPSQN
    
    #=====开始查询数据库====
    records=rccpsDBTrcc_balbka.selectu(wheresql_dic)
    AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('A099','没有查找到数据')
    else: 
        pass
    
#    =====判断返回码====
#    if records['PRCCO']!='RCCI0000':
#        #=====输出接口赋值====
#        AfaLoggerFunc.tradeInfo(">>>输出接口赋值")        
#        TradeContext.errorMsg  = records['PRCCO'] +' '+ records['PRCINFO']
#        if len(TradeContext.errorMsg) != 1:
#            TradeContext.errorCode = 'A099'
#        else:
#            #=====前台判断为此交易码继续轮询====
#            TradeContext.errorCode = '9999'
#            TradeContext.errorMsg  = '回车后再次查询结果,请稍候...'
#        AfaLoggerFunc.tradeDebug(">>>errorMsg["+str(TradeContext.errorMsg)+']')
#        AfaLoggerFunc.tradeDebug(">>>errorCode["+str(TradeContext.errorCode)+']')
#    else:
#        AfaLoggerFunc.tradeInfo(">>>输出接口赋值")
#        TradeContext.errorCode = '0000'
#        TradeContext.errorMsg  = '成功'
#        TradeContext.BJEDTE = records['BJEDTE']
#        TradeContext.BSPSQN = records['BSPSQN']
#        TradeContext.AVLBAL = str(records['AVLBAL'])
#        TradeContext.ACCBAL = str(records['ACCBAL'])
#    
    AfaLoggerFunc.tradeInfo(">>>输出接口赋值")       
    TradeContext.errorCode = '0000'       
    TradeContext.errorMsg  = '成功'    
    TradeContext.PRCCO  = records['PRCCO']
    TradeContext.STRINFO= records['STRINFO']              
    TradeContext.BJEDTE = records['BJEDTE']          
    TradeContext.BSPSQN = records['BSPSQN']          
    TradeContext.AVLBAL = str(records['AVLBAL'])     
    TradeContext.ACCBAL = str(records['ACCBAL'])     

    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)余额查询登记簿查询[TRCC001_8575]退出***')
    return True