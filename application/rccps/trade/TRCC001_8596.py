# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).错帐控制交易信息联动查询  柜面交易
#===============================================================================
#   模板文件:   TRCC001_8596.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  曾照泰
#   修改时间:   2011-05-23
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易(1.本地操作).错帐控制交易信息联动查询[TRCC001_8596]进入***' )
    
    #=====必要性检查====
    #=====判断输入接口是否存在====
    TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )
    if( not TradeContext.existVariable( "ORTRCDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '原委托日期[ORTRCDAT]不存在')
        
    if( not TradeContext.existVariable( "ORSNDBNK" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '原发送行号[ORSNDBNK]不存在')
        
    if( not TradeContext.existVariable( "ORTRCNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '原交易流水号[ORTRCNO]不存在')
        
    #=====组织查询字典====
    AfaLoggerFunc.tradeInfo(">>>开始组织查询字典")
    
    wheresql_dic={}
    wheresql_dic['TRCDAT'] =TradeContext.ORTRCDAT
    wheresql_dic['SNDBNKCO']=TradeContext.ORSNDBNK
    wheresql_dic['TRCNO']=TradeContext.ORTRCNO
    
    #=====开始查询数据库====
    records=rccpsDBTrcc_wtrbka.selectu(wheresql_dic)          #查询错帐控制解控登记簿 
    AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
    if(records==None):                                        
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )
    elif(len(records)==0):
        records=rccpsDBTrcc_tddzmx.selectu(wheresql_dic)      #查询错帐控制解控对账明细信息登记簿
        AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )
        elif(len(records)==0):
            return AfaFlowControl.ExitThisFlow('A099','没有查找到数据')
        else:
            #=====输出接口赋值====
            AfaLoggerFunc.tradeInfo(">>>输出接口赋值")       
            TradeContext.errorCode         = '0000'                  
            TradeContext.errorMsg          = '成功'   
            TradeContext.ORTRCCO           = records['TRCCO']         #原交易代码         
            TradeContext.ORSNDSUBBNK       = records['SNDMBRCO']      #原发起成员行号     
            TradeContext.ORRCVSUBBNK       = records['RCVMBRCO']      #原接收成员行号      
            TradeContext.ORRCVBNK          = records['RCVBNKCO']      #原接受行号    
            TradeContext.ORPYRACC          = records['PYRACC']        #原付款人账号  
            TradeContext.ORPYRNAM          = ''                       #原付款人名字
            TradeContext.ORPYEACC          = records['PYEACC']        #原收款人账号  
            TradeContext.ORPYENAM          = ''                       #原收款人名字      
            TradeContext.CUR               = records['CUR']           #币种
            TradeContext.OCCAMT            = str(records['OCCAMT'])   #原交易金额
            TradeContext.CHRG              = str(records['CUSCHRG'])  #原手续费
              
    else:
        #=====输出接口赋值====
        AfaLoggerFunc.tradeInfo(">>>输出接口赋值")       
        TradeContext.errorCode         = '0000'       
        TradeContext.errorMsg          = '成功'  
        TradeContext.BSPSQN            = records['BSPSQN'] 
        TradeContext.ORTRCCO           = records['TRCCO']         #原交易代码         
        TradeContext.ORSNDSUBBNK       = records['SNDMBRCO']      #原发起成员行号     
        TradeContext.ORRCVSUBBNK       = records['RCVMBRCO']      #原接收成员行号      
        TradeContext.ORRCVBNK          = records['RCVBNKCO']      #原接受行号    
        TradeContext.ORPYRACC          = records['PYRACC']        #原付款人账号  
        TradeContext.ORPYRNAM          = records['PYRNAM']        #原付款人名字
        TradeContext.ORPYEACC          = records['PYEACC']        #原收款人账号  
        TradeContext.ORPYENAM          = records['PYENAM']        #原收款人名字      
        TradeContext.CUR               = records['CUR']           #币种
        TradeContext.OCCAMT            = str(records['OCCAMT'])   #原交易金额
        TradeContext.CHRG              = str(records['CUSCHRG'])  #原手续费

    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)错帐控制解控交易信息联动查询[TRCC001_8596]退出***')
    return True
