# -*- coding: gbk -*-
################################################################################
#   代收代付.报表处理模板
#===============================================================================
#   模板文件:   003105.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaAfeFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******代收代付.报表处理模板['+TradeContext.TemplateCode+']进入******' )

    try:
    
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]


        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )


        #=====================校验公共节点的有效性==============================
        if( not TradeContext.existVariable( "rptType" ) ):
            raise AfaFlowControl.flowException( 'A0001', '报表类型[rptType]值不存在,不能报表打印操作' )

        if( not TradeContext.existVariable( "zoneno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '地区号[zoneno]值不存在,不能报表打印操作' )
            
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '网点号[brno]值不存在,不能报表打印操作' )

        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[tellerno]值不存在,不能报表打印操作' )

        if( not TradeContext.existVariable( "beginDate" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '起始日期[beginDate]值不存在,不能报表打印操作' )

        if( not TradeContext.existVariable( "endDate" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '截至日期[endDate]值不存在,不能报表打印操作' )


        #判断汇总类型(1-按柜员汇总 2-按网点汇总 3-按支行汇总 4-按总行汇总)
        if( int( TradeContext.rptType )<1 or int( TradeContext.rptType )>4 ):           
            return AfaFlowControl.ExitThisFlow( 'A0019', '非法的汇总类型' )


        #=====================按总行汇总========================================
        if (int( TradeContext.rptType )==4):
            AfaLoggerFunc.tradeInfo( '按总行汇总')



        #=====================按支行汇总========================================
        if(int( TradeContext.rptType )==3):
            AfaLoggerFunc.tradeInfo( '按支行汇总')


        #=====================按网点汇总========================================
        if (int( TradeContext.rptType )==2):
            AfaLoggerFunc.tradeInfo( '按网点汇总')


        #=====================按柜员汇总========================================
        if (int( TradeContext.rptType )==1):
            AfaLoggerFunc.tradeInfo( '按柜员汇总')
  
  
        #=====================自动打包==========================================
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='交易成功'
        AfaFunc.autoPackData()

        #=====================程序退出==========================================
        AfaLoggerFunc.tradeInfo('******代收代付.报表处理模板['+TradeContext.TemplateCode+']退出******' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) ) 
