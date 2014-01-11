# -*- coding: gbk -*-
################################################################################
#   代收代付.参数下载模板
#===============================================================================
#   模板文件:   003108.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******代收代付.参数下载模板[' + TradeContext.TemplateCode + ']进入******')

    try:
    
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]


        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
        
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

        if ( not TradeContext.existVariable( "procType" ) ) :
            return AfaFlowControl.ExitThisFlow( 'A0001', '操作类型[procType]值不存在,交易失败' )


        if TradeContext.procType == '1' :
            #下载数据字典
            if not DownLoadBaseParam( ) :
                return AfaFlowControl.ExitThisFlow( 'A0001', '下载数据字典失败' )

        if TradeContext.procType == '2' :
            #下载业务参数
            if not DownLoadAppParam( )  :
                return AfaFlowControl.ExitThisFlow( 'A0001', '下载业务参数失败' )

        if TradeContext.procType == '3' :
            #下载交易列表
            if not DownLoadTradeList( ) :
                return AfaFlowControl.ExitThisFlow( 'A0001', '下载交易列表失败' )

            
        #=====================外调接口(后处理)==================================
        if subModuleExistFlag==1 :
            if not subModuleHandle.SubModuleDoSnd():
                raise AfaFlowControl.flowException( )
                
                
        #=====================自动打包==========================================
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '交易成功'
        AfaFunc.autoPackData()


        #=====================程序退出==========================================
        AfaLoggerFunc.tradeInfo('******代收代付.参数下载模板[' + TradeContext.TemplateCode + ']退出******')
        
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )

################################################################################
def DownLoadBaseParam( ):
    AfaLoggerFunc.tradeInfo('>>>下载数据字典')
    return True


def DownLoadAppParam( ):
    AfaLoggerFunc.tradeInfo('>>>下载业务参数')
    return True


def DownLoadTradeList( ):
    AfaLoggerFunc.tradeInfo('>>>下载交易列表')
    return True
