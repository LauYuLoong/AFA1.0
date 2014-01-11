  # -*- coding: gbk -*-
################################################################################
#   银保通.查询模板.不去第三方,不去主机
#===============================================================================
#   模板文件:   TTJYW004.py
#   修改时间:   2012-08-20
#   作   者：   陈浩
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaAfeFunc,AfaFlowControl
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******统缴业务行内查询模板[' + TradeContext.TemplateCode + ']进入******')
    try:
        
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]
        
        #获取当前系统时间
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
            
                                                                                  
        #=====================外调接口(前处理)==================================  
        subModuleExistFlag = 0                                                    
        subModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode  
        try:                                                                      
            subModuleHandle=__import__( subModuleName )                           
        except Exception, e:                                                      
            AfaLoggerFunc.tradeInfo( e)                                           
        else:                                                                     
            AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )              
            subModuleExistFlag=1                                                  
            if not subModuleHandle.SubModuleDoFst( ) :                            
                raise AfaFlowControl.flowException( )                             
                                                                                  
       
        #===============================================================
        TradeContext.errorCode='0000'   
            
        #=====================自动打包==========================================
        AfaFunc.autoPackData()
        
        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******统缴业务行内查询模板[' + TradeContext.TemplateCode + ']退出******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )       
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
