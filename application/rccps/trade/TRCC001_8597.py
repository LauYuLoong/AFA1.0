# -*- coding: gbk -*-
################################################################################
#   农信银系统：往账.本地类操作(1.本地操作).错帐控制或解控结果信息查询  柜面交易
#===============================================================================
#   模板文件:   TRCC001_8597.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  曾照泰
#   修改时间:   2011-08—22
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作交易(1.本地操作).错帐控制或解控结果查询[TRCC001_8597]进入***' )
    
    #=====必要性检查====
    #=====判断输入接口是否存在====
    if( not TradeContext.existVariable( "TRCDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '交易日期[ORTRCDAT]不存在')
        
    if( not TradeContext.existVariable( "OPTYPE" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '操作类型[OPTYPE]不存在')
    #=====开始查询数据库==== 
    
    if TradeContext.OPTYPE=='0': 
        sql =''   
        sql = sql + "select ORTRCDAT,ORTRCCO,ORSNDBNK,ORRCVBNK,ORPYRACC,ORPYRNAM,ORPYEACC,ORPYENAM,ERRCONBAL,CONSTS,STRINFO,TRCNO "     
        sql = sql + "from rcc_acckj where trcdat ='" + TradeContext.TRCDAT + "' and trcco='3000508' order by note1 desc "    
    if TradeContext.OPTYPE=='1':
        sql =''
        sql = sql + "select ORTRCDAT,TRCCO,ORSNDBNK,ORRCVBNK,ORPYRACC,ORPYRNAM,ORPYEACC,ORPYENAM,ERRCONBAL,UNCONRST,STRINFO,ORTRCNO "     
        sql = sql + "from rcc_acckj where trcdat ='" + TradeContext.TRCDAT + "' and trcco='3000509' order by note1  desc"                                                                                        
    AfaLoggerFunc.tradeDebug("查询错帐控制解控sql语句："+ sql )
    
    records = AfaDBFunc.SelectSql( sql )  
    
    if ( records == None ):                                                                                              
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )                                                                  
        return AfaFlowControl.ExitThisFlow( '9000', '查询个人协议信息异常' )                                             
        
    if ( len(records) == 0 ):
        TradeContext.errorMsg    =  "没有今天错帐控制解控的数据"
        TradeContext.errorCode   =  '9000'
        return AfaFlowControl.ExitThisFlow( '9000', '没有今天错帐控制解控的数据' )  
      
    else:
        TradeContext.count=str(len(records))  
        if TradeContext.count=='1':
            TradeContext.errorMsg    =  "交易成功"
            TradeContext.errorCode   =  '0000'    
            TradeContext.ORTRCDAT    =  records[0][0]
            TradeContext.ORTRCCO     =  records[0][1]
            TradeContext.ORSNDBNK    =  records[0][2]
            TradeContext.ORRCVBNK    =  records[0][3]
            TradeContext.ORPYRACC    =  records[0][4]
            TradeContext.ORPYRNAM    =  records[0][5]
            TradeContext.ORPYEACC    =  records[0][6]
            TradeContext.ORPYENAM    =  records[0][7] 
            TradeContext.ERRCONBAL   =  str(records[0][8]) 
            TradeContext.CONSTS      =  records[0][9] 
            TradeContext.STRINFO     =  records[0][10]
            TradeContext.TRCNO       =  records[0][11]
            AfaLoggerFunc.tradeDebug(TradeContext.STRINFO)
            
        else:
            ORTRCDAT    = []
            ORTRCCO     = []
            ORSNDBNK    = []
            ORRCVBNK    = []  
            ORPYRACC    = []  
            ORPYRNAM    = []  
            ORPYEACC    = []  
            ORPYENAM    = []  
            ERRCONBAL   = []  
            CONSTS      = []  
            STRINFO     = []
            TRCNO       = []
            i = 0
            for i in range(0, len(records)):
                ORTRCDAT.append(records[i][0])               #原委托日期
                ORTRCCO.append(records[i][1])                #原交易代码
                ORSNDBNK.append(records[i][2])               #原发起行号
                ORRCVBNK.append(records[i][3])               #原接受行号
                ORPYRACC.append(records[i][4])               #原付款账号
                ORPYRNAM.append(records[i][5])               #原付款人名字
                ORPYEACC.append(records[i][6])               #原收款账号
                ORPYENAM.append(records[i][7])               #原收款人名字
                ERRCONBAL.append(str(records[i][8]))         #错帐控制或解控金额  
                CONSTS.append(records[i][9])                 #错帐控制或解控状态
                STRINFO.append(records[i][10])               #处理结果
                TRCNO.append(records[i][11])                 #错帐控制流水号
             
            TradeContext.errorMsg    =  "交易成功"
            TradeContext.errorCode   =  '0000'
            TradeContext.ORTRCDAT    =   ORTRCDAT 
            TradeContext.ORTRCCO     =   ORTRCCO
            TradeContext.ORSNDBNK    =   ORSNDBNK  
            TradeContext.ORRCVBNK    =   ORRCVBNK   
            TradeContext.ORPYRACC    =   ORPYRACC   
            TradeContext.ORPYRNAM    =   ORPYRNAM   
            TradeContext.ORPYEACC    =   ORPYEACC   
            TradeContext.ORPYENAM    =   ORPYENAM   
            TradeContext.ERRCONBAL   =   ERRCONBAL   
            TradeContext.CONSTS      =   CONSTS  
            TradeContext.STRINFO     =   STRINFO
            TradeContext.TRCNO       =   TRCNO
                                                    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)错帐控制解控交易信息联动查询[TRCC001_8597]退出***')
    return True
