# -*- coding: gbk -*-
##################################################################
#              ����ũ������������ͨѶʵ��ģ��
#=================================================================
#                ��    �ߣ�    �� �� ��
#                �޸�ʱ�䣺    20060907
##################################################################
import LoggerHandler, HostDataHandler, HostContext, SockUtil
import os, sys, types, traceback, struct, socket, ConfigParser

isDebug = False
logger = LoggerHandler.getLogger( 'hostComm' )

#ͨѶ����������־���,��16����������ݵľ�������
def dump( src, length = 16 ):
    FILTER=''.join( [( len( repr( chr( x ) ) )==3 ) and chr( x ) or '.' for x in range( 256 )] )
    N=0; result=''
    while src:
        s, src = src[:length], src[length:]
        hexa = ' '.join( ["%02X"%ord( x ) for x in s] )
        s = s.translate( FILTER )
        result += "%04X   %-*s   %s\n" % ( N, length*3, hexa, s )
        N+=length
    return result

#�������ͨѶ�����Ļ���
def clearHostContext( ):
    names = HostContext.getNames( )
    delList = []
    for name in names:
        if ( not name.startswith( '__' ) ) :
            value = getattr( HostContext, name )
            if( ( type( value ) is types.StringType )  or ( type( value ) is types.ListType ) ):
                delList.append( name )
                
    for name in delList:
        delattr( HostContext, name )

#����ͨѶ���ýӿ�
def callHostTrade( mapping, serviceName, sysId ):
    global isDebug
    HostContext.host_Error = False
    HostContext.host_ErrorType = 0
    HostContext.host_ErrorMsg = '������ͨѶ�ɹ�'
    
    #��ȡ����ͨѶ������Ϣ
    try:
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/hostconf/host.ini'
        hostSection = 'HOST'
        config.readfp( open( configFileName ) )    
        isDebug = config.getboolean( hostSection, 'DEBUG' )
        ip = config.get( hostSection, 'IP' )
        port = config.getint( hostSection, 'PORT' )
        timeout = config.getint( hostSection, 'TIMEOUT' )
        HostDataHandler.isDebug = isDebug
        logger.debug( '������ַ:[' + ip +']['+str(port)+']' )
    except:
        HostContext.host_Error = True
        HostContext.host_ErrorType = 1
        HostContext.host_ErrorMsg = '��ȡ����������Ϣʧ��'
        
        if isDebug:
            logger.error( '��ȡ����������Ϣʧ��' )
            
        return
    
    #����ͨѶ�����ı�����ƴװ���͸�����������
    try:
        reqMsg = HostDataHandler.hostPack( mapping, sysId, serviceName )
        
    except ( Exception ), e:      
        HostContext.host_Error = True
        HostContext.host_ErrorType = 2
        HostContext.host_ErrorMsg = str( e )
        
        if isDebug: 
            logger.error( str( sys.exc_type ) )
            logger.error( str( sys.exc_value ) )
            logger.error( str( traceback.format_tb( sys.exc_traceback ) ) )
            
        return

    #������������
    sockobj = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sockobj.settimeout( timeout )
    
    try:
        sockobj.connect( ( ip, port ) )
        
    except ( Exception ), e:
        HostContext.host_Error = True
        HostContext.host_ErrorType = 3
        HostContext.host_ErrorMsg = '������������ʧ��'
        
        if isDebug:
            logger.error( '������������ʧ��' )
            
        return

    #�����������ݵ�����
    if isDebug:
        logger.debug( '��������:\n' + dump( reqMsg ) )
        
    try:
        SockUtil.sendAllData( sockobj, reqMsg )
        
    except:
        HostContext.host_Error = True
        HostContext.host_ErrorType = 4
        HostContext.host_ErrorMsg = '������������ʧ��'
        
        if isDebug:
            logger.error( '������������ʧ��' )
            
        sockobj.close( )
        
        return

    #����������Ӧ����
    try:
        chuckLen = SockUtil.receiveNumBytes( sockobj, 4 )
        chuckData = SockUtil.receiveNumBytes( sockobj, struct.unpack( "!L", chuckLen )[0] - 4 )
        respData = chuckLen + chuckData
        
        if isDebug:
            logger.debug( '��������:\n' + dump( respData ) )
            
        sockobj.close( )
        
    except:
        sockobj.close( )
        HostContext.host_Error = True
        HostContext.host_ErrorType = 5
        HostContext.host_ErrorMsg = '����������Ӧ����ʧ��'
        
        if isDebug:
            logger.error( '����������Ӧ����ʧ��' )
            
        return

    #����������ص���Ϣ��HostContext��
    try:
        clearHostContext( )
        HostContext.host_Error = False
        HostContext.host_ErrorType = 0
        HostContext.host_ErrorMsg = '������ͨѶ�ɹ�'
        HostDataHandler.hostUnpack( respData )
        
    except:
        HostContext.host_Error = True
        HostContext.host_ErrorType = 6
        HostContext.host_ErrorMsg = '���������Ӧ����ʧ��'
        
        if isDebug: 
            logger.error( '���������Ӧ����ʧ��' )
            logger.error( str( sys.exc_type ) )
            logger.error( str( sys.exc_value ) )
            logger.error( str( traceback.format_tb( sys.exc_traceback ) ) )
