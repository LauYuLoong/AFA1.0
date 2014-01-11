# -*- coding: gbk -*-
################################################################################
#  凤台财政-待查询账户维护.查询模板
#===============================================================================
#   模板文件:   TFTCZ001.py
#   修改时间:   2012-09-17
#   作    者:   陈浩
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******凤台财政-待查询账户维护模板['+TradeContext.TemplateCode+']进入******')
    
    try:
    
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]
                
        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

       # #=====================判断应用系统状态==================================
       # if not AfaFunc.ChkSysStatus( ) :
       #     raise AfaFlowControl.flowException( )             
       #         
        #=====================外调接口(前处理)==================================
        subModuleExistFlag=0
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
       
        
        #=====================自动打包==========================================
        AfaFunc.autoPackData()
        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('************凤台财政-待查询账户维护模板['+TradeContext.TemplateCode+']退出******')


    except AfaFlowControl.flowException, e:
        #AfaFlowControl.exitMainFlow( str(e) )
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        #AfaFlowControl.exitMainFlow( str(e) )
        AfaFlowControl.exitMainFlow( )        
