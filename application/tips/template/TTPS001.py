# -*- coding: gbk -*-
##################################################################
#   财税库行横向联网.查询维护类模板.
#=================================================================
#   程序文件:   TPS001.py
#   修改时间:   2008-5-2 10:24 
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, TipsFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('==========进入查询维护类模板['+TradeContext.TemplateCode+']==========')
    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]
        
        #=============获取当前系统时间====================
        AfaLoggerFunc.tradeInfo('>>>获取当前系统时间')
        if not (TradeContext.existVariable( "workDate" ) and len(TradeContext.workDate)>0):
            TradeContext.workDate = UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        TradeContext.sysId      ='AG2010'
        TradeContext.busiNo     ='00000000000001'
        
        #不使用转换返回码
        TradeContext.__respFlag__="0"
    
        #=============外调接口1====================
        subModuleExistFlag=0
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            subModuleHandle=__import__( subModuleName )
        except Exception, e:
            AfaLoggerFunc.tradeInfo( e)
        else:
            AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleMainFst( ) :
                raise TipsFunc.flowException( )

        #=============自动打包====================
        TipsFunc.autoPackData()

        AfaLoggerFunc.tradeInfo('==========退出查询维护类模板['+TradeContext.TemplateCode+']==========')
        
    except TipsFunc.flowException, e:
        TipsFunc.exitMainFlow( )
        
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
