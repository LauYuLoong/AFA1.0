# -*- coding: gbk -*-
##################################################################
#   代收代付平台.空模板.
#=================================================================
#   程序文件:   3001.py
#   修改时间:   2007-10-15 
##################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc
from types import *

def main( ):
    
    AfaLoggerFunc.tradeInfo('=======非税自由模板开始=======')

    try:
        #=============初始化返回报文变量====================
        TradeContext.tradeResponse=[]
        
        #=============获取当前系统时间====================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #begin 20100625 蔡永贵修改
        #TradeContext.sysId       = "AG2008"
        TradeContext.sysId       = TradeContext.appNo
        #end

        TradeContext.agentFlag   = "01"
        TradeContext.__respFlag__='0'

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
                raise AfaFlowControl.flowException( )
        
        #=============自动打包====================
        AfaFunc.autoPackData()

        AfaLoggerFunc.tradeInfo('=======非税自由模板结束=======')
        
    except AfaFlowControl.flowException, e:
        #流程异常
        AfaFlowControl.exitMainFlow( )

    except AfaFlowControl.accException:
        #账务异常
        AfaFlowControl.exitMainFlow( )
            
    except Exception, e:
        #默认异常
        AfaFlowControl.exitMainFlow( str( e ) )
