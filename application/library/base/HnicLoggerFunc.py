# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��־ά����
#=================================================================
#   �����ļ�:   AfaLoggerFunc.py
#   �޸�ʱ��:   2006��11��27�� ����һ
##################################################################
import logging, logging.handlers

#Initializing root logger......
rootLogger = logging.getLogger( '' )
rootLogger.setLevel( logging.DEBUG )
#=====================������־����=============================
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
