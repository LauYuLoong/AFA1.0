# -*- coding: gbk -*-
##################################################################
#   中间业务平台.日志维护类
#=================================================================
#   程序文件:   AfaLoggerFunc.py
#   修改时间:   2006年11月27日 星期一
##################################################################
import logging, logging.handlers

#Initializing root logger......
rootLogger = logging.getLogger( '' )
rootLogger.setLevel( logging.DEBUG )
#=====================交易日志处理=============================
tradeLogger = logging.getLogger( "trade" )

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
