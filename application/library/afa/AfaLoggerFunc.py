# -*- coding: gbk -*-
##################################################################
#   中间业务平台.日志维护类
#=================================================================
#   程序文件:   AfaLoggerFunc.py
#   修改时间:   2006-03-20
##################################################################
import LoggerHandler,TradeContext

#=====================交易日志处理=============================
tradeLogger = LoggerHandler.getLogger( "agent" )

if TradeContext.existVariable( 'sysType' ):
    tradeLogger = LoggerHandler.getLogger( TradeContext.sysType )

def tradeDebug( msg ):
    tradeLogger.debug( msg )

def tradeInfo( msg ):
    tradeLogger.info( msg )

def tradeWarn( msg ):
    tradeLogger.warn( msg )

def tradeError( msg ):
    tradeLogger.error( msg )

def tradeFatal( msg ):
    tradeLogger.fatal( msg )
