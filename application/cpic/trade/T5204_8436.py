# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   5204_8438.py
#   程序说明:   [代理保险汇总查询]
#   修改时间:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc,CpicFunc,LoggerHandler
from types import *

def SubModuleDoFst( ):
    AfaLoggerFunc.tradeInfo( '初始化交易变量' )
    #AfaLoggerFunc.tradeInfo( '反交易变量值的有效性校验' )
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
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[termid]值不存在!' )
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入代理保险汇总查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    #=====得到ccip日志的handler====
    tradelogger = LoggerHandler.getLogger( "cpic" )
    res = CpicFunc.CreatReport(tradelogger)
    if(res != 0):
        #return AfaFlowControl.ExitThisFlow("A999","生成明细报表失败")
        return False
    else:
        TradeContext.errorCode = '0000'
        return True
