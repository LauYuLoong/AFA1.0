# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).通存通兑交易信息联动查询
#===============================================================================
#   模板文件:   TRCC001_8592.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘振东
#   修改时间:   2008-12-30
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易(1.本地操作).通存通兑交易信息联动查询[TRCC001_8592]进入***' )
    
    #=====必要性检查====
    #=====判断输入接口是否存在====
    if( not TradeContext.existVariable( "TRCDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '委托日期[TRCDAT]不存在')
        
    if( not TradeContext.existVariable( "SNDBNKCO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '发送行号[SNDBNKCO]不存在')
        
    if( not TradeContext.existVariable( "TRCNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '交易流水号[TRCNO]不存在')
        
    #=====组织查询字典====
    AfaLoggerFunc.tradeInfo(">>>开始组织查询字典")
    
    wheresql_dic={}
    wheresql_dic['TRCDAT']=TradeContext.TRCDAT
    wheresql_dic['SNDBNKCO']=TradeContext.SNDBNKCO
    wheresql_dic['TRCNO']=TradeContext.TRCNO
    
    #=====开始查询数据库====
    records=rccpsDBTrcc_wtrbka.selectu(wheresql_dic)
    AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
    if(records==None):                                        
        return AfaFlowControl.ExitThisFlow('A099','查询失败' )
    elif(len(records)==0):
        records=rccpsDBTrcc_tddzmx.selectu(wheresql_dic)
        AfaLoggerFunc.tradeDebug('>>>记录['+str(records)+']')
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','查询失败' )
        elif(len(records)==0):
            return AfaFlowControl.ExitThisFlow('A099','没有查找到数据')
        else:
            #=====输出接口赋值====
            AfaLoggerFunc.tradeInfo(">>>输出接口赋值")       
            TradeContext.errorCode = '0000'                  
            TradeContext.errorMsg  = '成功'                  
            TradeContext.BJEDTE    = records['BJEDTE']       
            TradeContext.BSPSQN    = records['BSPSQN']       
            TradeContext.SNDBNKCO  = records['SNDBNKCO']     
            TradeContext.SNDBNKNM  = records['SNDBNKNM']     
            TradeContext.RCVBNKCO  = records['RCVBNKCO']     
            TradeContext.RCVBNKNM  = records['RCVBNKNM']     
            TradeContext.PYEACC    = records['PYEACC']       
            TradeContext.PYENAM    = ""       
            TradeContext.PYRACC    = records['PYRACC']       
            TradeContext.PYRNAM    = ""      
            TradeContext.OCCAMT    = str(records['OCCAMT'])  
            TradeContext.CUSCHRG   = str(records['CUSCHRG']) 
            TradeContext.CUR       = '01'          
            TradeContext.STRINFO   = records['STRINFO']      
    else:
        #=====输出接口赋值====
        AfaLoggerFunc.tradeInfo(">>>输出接口赋值")       
        TradeContext.errorCode = '0000'       
        TradeContext.errorMsg  = '成功'    
        TradeContext.BJEDTE    = records['BJEDTE']
        TradeContext.BSPSQN    = records['BSPSQN']             
        TradeContext.SNDBNKCO  = records['SNDBNKCO']          
        TradeContext.SNDBNKNM  = records['SNDBNKNM'] 
        TradeContext.RCVBNKCO  = records['RCVBNKCO']
        TradeContext.RCVBNKNM  = records['RCVBNKNM']
        TradeContext.PYEACC    = records['PYEACC']
        TradeContext.PYENAM    = records['PYENAM']
        TradeContext.PYRACC    = records['PYRACC']
        TradeContext.PYRNAM    = records['PYRNAM']
        TradeContext.OCCAMT    = str(records['OCCAMT'])
        TradeContext.CUSCHRG   = str(records['CUSCHRG'])
        TradeContext.CUR       = records['CUR']
        TradeContext.STRINFO   = records['STRINFO']

    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)通存通兑交易信息联动查询[TRCC001_8592]退出***')
    return True
    
     
        
    
    