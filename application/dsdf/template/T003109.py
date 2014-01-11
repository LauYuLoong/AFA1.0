# -*- coding: gbk -*-
################################################################################
#   代收代付.权限检查模板
#===============================================================================
#   模板文件:   003109.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******代收代付.权限检查模板[' + TradeContext.TemplateCode + ']进入******')
    
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
            AfaLoggerFunc.tradeInfo( e )

        else:
            AfaLoggerFunc.tradeInfo( '执行['+subModuleName+']模块' )
            subModuleExistFlag=1
            if not subModuleHandle.SubModuleDoFst( ) :
                raise AfaFlowControl.flowException( )


        #=====================判断商户状态======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
            
            
        #=====================判断渠道状态======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )


        #=====================判断交易状态======================================
        if not AfaFunc.ChkTradeStatus( ) :
            raise AfaFlowControl.flowException( )
 
 
        #=====================外调接口(后处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd():
                raise AfaFlowControl.flowException( )
                
                
        #=====================自动打包==========================================
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '交易成功'
        AfaFunc.autoPackData()

        #=====================程序退出==========================================
        AfaLoggerFunc.tradeInfo('******代收代付.权限检查模板[' + TradeContext.TemplateCode + ']退出******')
        
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
