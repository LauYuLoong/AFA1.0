# -*- coding: gbk -*-
################################################################################
#   呼叫中心.模板1.转发模板(1.主机)
#===============================================================================
#   模板文件:   0001.py
#   修改时间:   2009-03-13
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaTransDtlFunc,TransBillFunc,AfaHostFunc,AfaFlowControl
from types import *
import ccHostFunc

def main( ):

    AfaLoggerFunc.tradeInfo('******呼叫中心.模板1.转发模板['+TradeContext.TemplateCode+']进入******')
    
    try:
    
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]
                
                
        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
                
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
                
        #=====================与主机交换========================================
        ccHostFunc.CommHost(TradeContext.TransCode) 


        #=====================外调接口(后处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd():
                raise AfaFlowControl.flowException( )


        #=====================自动打包==========================================
        AfaFunc.autoPackData()

        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******呼叫中心.模板1.转发模板['+TradeContext.TemplateCode+']退出******')


    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
