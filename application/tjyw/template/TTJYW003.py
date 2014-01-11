  # -*- coding: gbk -*-
################################################################################
#   银保通.查询模板.不去第三方,不去主机
#===============================================================================
#   模板文件:   YBT004.py
#   修改时间:   2011-01-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaAfeFunc,AfaFlowControl,AfaTjFunc
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******统缴业务行内查询模板[' + TradeContext.TemplateCode + ']进入******')
    try:
        
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]
        
        #获取当前系统时间
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================判断应用系统状态==================================  
            
        if not AfaFunc.ChkSysStatus( ) :                                          
            raise AfaFlowControl.flowException( ) 
        
     #20120711注释 修改
     #begin
        #=====================判断单位状态======================================
        if not AfaTjFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )
            
     #end                                    
                                                                                  
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
                                                                                  
        #=====================校验公共节点的有效性==============================
        #if( not AfaFunc.Query_ChkVariableExist( ) ):
        #    raise AfaFlowControl.flowException( )
        
        #=====================判断商户状态======================================
        #if not AfaFunc.ChkUnitStatus( ) :
        #    raise AfaFlowControl.flowException( )
        
        #=====================判断渠道状态======================================
        #if not AfaFunc.ChkChannelStatus( ) :
        #    raise AfaFlowControl.flowException( )
        
        #=====================获取平台流水号====================================
        #if AfaFunc.GetSerialno( ) == -1 :
        #    raise AfaFlowControl.flowException( )
        
        TradeContext.errorCode='0000'       
        #=====================自动打包==========================================
        AfaFunc.autoPackData()
        
        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******统缴业务行内查询模板[' + TradeContext.TemplateCode + ']退出******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )       
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
