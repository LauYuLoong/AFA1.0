# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TYBT004_8619.py
#   程序说明:   [银保通明细查询]
#   修改时间:   2010-08-12
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc,YbtFunc,LoggerHandler
from types import *

def SubModuleDoFst( ):
    
    AfaLoggerFunc.tradeInfo( '初始化交易变量' )
    
    if( not (TradeContext.existVariable( "startdate" ) and TradeContext.startdate != '00000000') ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '起始日期[startdate]值不存在!' )
    
    if( not (TradeContext.existVariable( "enddate" ) and TradeContext.enddate != '00000000' ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '截止日期[enddate]值不存在!' )
   
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
    
    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[tellerno]值不存在!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '网点号[brno]值不存在!' )
        if( not TradeContext.existVariable( "termid" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '终端号[termid]值不存在!' )
        
    return True

def SubModuleDoSnd():
    
    AfaLoggerFunc.tradeInfo('进入银保通明细查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
   
    tradelogger = LoggerHandler.getLogger( "ybt" )
    
    res = YbtFunc.CreatDetailReport(tradelogger)
    if(res != 0):
        #return AfaFlowControl.ExitThisFlow("A999","生成银保通明细报表失败")
        return False
    else:
        TradeContext.errorCode = '0000'
        return True
