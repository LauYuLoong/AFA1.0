  # -*- coding: gbk -*-
################################################################################
#   银保通.查询模板.不去第三方,不去主机
#===============================================================================
#   模板文件:   YBT004.py
#   修改时间:   2010-08-18
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaAfeFunc,AfaFlowControl
from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******银保通行内查询模板[' + TradeContext.TemplateCode + ']进入******')
    try:
        
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]
        
        #获取当前系统时间
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )
        
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
        if( not AfaFunc.Query_ChkVariableExist( ) ):
            raise AfaFlowControl.flowException( )
        
        #=====================判断商户状态======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================判断渠道状态======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================获取平台流水号====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
        
        #=====================与第三方系统交互==================================
        #AfaAfeFunc.CommAfe()
        
        #=====================外调接口(后处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd( ) :
                raise AfaFlowControl.flowException( )
        
        #=====================自动打包==========================================
        AfaFunc.autoPackData()
        
        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******银保通行内查询模板[' + TradeContext.TemplateCode + ']退出******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )       
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
