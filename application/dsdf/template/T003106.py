# -*- coding: gbk -*-
################################################################################
#   代收代付.自由处理模板
#===============================================================================
#   模板文件:   003106.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaHostFunc,AfaAfeFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******代收代付.自由处理模板[' + TradeContext.TemplateCode + ']进入******')

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

        #=====================判断商户状态======================================
        if not AfaFunc.ChkUnitStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================判断渠道状态======================================
        if not AfaFunc.ChkChannelStatus( ) :
            raise AfaFlowControl.flowException( )
        
        #=====================获取平台流水号====================================
        if AfaFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )


        #本地操作
        if( TradeContext.existVariable( "localFlag" ) ):
            if ( TradeContext.localFlag == '1' ):
                #外调接口(后处理)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoSnd():
                        raise AfaFlowControl.flowException( )

        #主机操作
        if( TradeContext.existVariable( "hostFlag" ) ):
            if ( TradeContext.hostFlag == '1' ):

                #判断主机接口代码是否存在
                if( not TradeContext.existVariable( "hostCode" ) ):
                    return AfaFlowControl.ExitThisFlow( 'A0001', '主机代码[hostCode]值不存在,交易失败' )

                #与主机交换
                AfaHostFunc.CommHost(TradeContext.hostCode)

                #外调接口(后处理)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoTrd():
                        raise AfaFlowControl.flowException( )

        #企业操作
        if( TradeContext.existVariable( "corpFlag" ) ):
            if ( TradeContext.corpFlag == '1' ):

                #与通讯前置交换
                AfaAfeFunc.CommAfe()

                #外调接口(后处理)
                if subModuleExistFlag==1 :
                    if not subModuleHandle.SubModuleDoFth():
                        raise AfaFlowControl.flowException( )


        #=====================外调接口(后处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoFth():
                raise AfaFlowControl.flowException( )
        
        #=====================自动打包==========================================
        AfaFunc.autoPackData()

        #=====================程序退出==========================================
        AfaLoggerFunc.tradeInfo('******代收代付.自由处理模板[' + TradeContext.TemplateCode + ']退出******')

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
