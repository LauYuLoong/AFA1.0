# -*- coding: gbk -*-
################################################################################
#   安徽交罚.查询模板.去第三方
#===============================================================================
#   模板文件:   TAHJF001.py
#   修改时间:   2011-01-20
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,Party3Context,AfaAfeFunc,AfaFlowControl,AhjfAdminFunc

from types import *

def main( ):
    AfaLoggerFunc.tradeInfo('******安徽交罚查询模板[' + TradeContext.TemplateCode + ']进入******')
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
        if not AhjfAdminFunc.ChkUnitInfo( ):
            raise AfaFlowControl.flowException( )
        
        #=====================与第三方系统交互==================================
        TradeContext.__respFlag__='0'
        
        AfaAfeFunc.CommAfe()
       
        #=====================外调接口(后处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd( ) :
                raise AfaFlowControl.flowException( )
        
        #=====================自动打包==========================================
        AfaFunc.autoPackData()
        
        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('******安徽交罚查询模板[' + TradeContext.TemplateCode + ']退出******')
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
