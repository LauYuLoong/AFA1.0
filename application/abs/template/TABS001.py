# -*- coding: gbk -*-
################################################################################
#   批量业务.通用模板
#===============================================================================
#   模板文件:   ABS001.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFlowControl,AfaFunc

from types import *


def main( ):


    AfaLoggerFunc.tradeInfo('********abs.通用模板进入********')


    try:
    
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]

       
        #=====================获取系统日期时间==================================
        TradeContext.TranDate=AfaUtilTools.GetSysDate( )
        TradeContext.TranTime=AfaUtilTools.GetSysTime( )


        #=====================动态加载交易脚本==================================
        trxModuleName = 'T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode
        try:
            trxModuleHandle=__import__( trxModuleName )


        except Exception, e:
            AfaLoggerFunc.tradeInfo(e)
            raise AfaFlowControl.flowException( 'A0001', '加载交易脚本失败或交易脚本不存在' )


        #=====================批量业务个性化操作================================
        if not trxModuleHandle.TrxMain( ) :
            raise AfaFlowControl.accException( )


        #=====================自动打包==========================================
        AfaFunc.autoPackData()


        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo('********批量业务.通用模板['+TradeContext.TemplateCode+']退出********')


    except AfaFlowControl.flowException, e:
        #流程异常
        AfaFlowControl.exitMainFlow( str(e) )

    except AfaFlowControl.accException:
        #账务异常
        AfaFunc.autoPackData()

    except Exception, e:
        #默认异常
        AfaFlowControl.exitMainFlow( str( e ) )
