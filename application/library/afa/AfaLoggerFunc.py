# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��־ά����
#=================================================================
#   �����ļ�:   AfaLoggerFunc.py
#   �޸�ʱ��:   2006-03-20
##################################################################
import LoggerHandler,TradeContext

#=====================������־����=============================
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
