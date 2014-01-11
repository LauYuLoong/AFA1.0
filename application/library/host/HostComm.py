# -*- coding: gbk -*-
##################################################################
#              安徽农村信用社主机通讯实现模块
#=================================================================
#                作    者：    陈 显 明
#                修改时间：    20060907
##################################################################
import LoggerHandler, HostDataHandler, HostContext, SockUtil
import os, sys, types, traceback, struct, socket, ConfigParser

isDebug = False
logger = LoggerHandler.getLogger( 'hostComm' )

#通讯缓冲区的日志输出,以16进制输出数据的具体内容
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

#清空主机通讯上下文环境
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

#主机通讯调用接口
def callHostTrade( mapping, serviceName, sysId ):
    global isDebug
    HostContext.host_Error = False
    HostContext.host_ErrorType = 0
    HostContext.host_ErrorMsg = '与主机通讯成功'
    
    #读取主机通讯配置信息
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
        logger.debug( '主机地址:[' + ip +']['+str(port)+']' )
    except:
        HostContext.host_Error = True
        HostContext.host_ErrorType = 1
        HostContext.host_ErrorMsg = '读取主机配置信息失败'
        
        if isDebug:
            logger.error( '读取主机配置信息失败' )
            
        return
    
    #设置通讯上下文变量并拼装发送给主机的数据
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

    #创建网络连接
    sockobj = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sockobj.settimeout( timeout )
    
    try:
        sockobj.connect( ( ip, port ) )
        
    except ( Exception ), e:
        HostContext.host_Error = True
        HostContext.host_ErrorType = 3
        HostContext.host_ErrorMsg = '连接主机网关失败'
        
        if isDebug:
            logger.error( '连接主机网关失败' )
            
        return

    #发送请求数据到主机
    if isDebug:
        logger.debug( '发送数据:\n' + dump( reqMsg ) )
        
    try:
        SockUtil.sendAllData( sockobj, reqMsg )
        
    except:
        HostContext.host_Error = True
        HostContext.host_ErrorType = 4
        HostContext.host_ErrorMsg = '发送请求数据失败'
        
        if isDebug:
            logger.error( '发送请求数据失败' )
            
        sockobj.close( )
        
        return

    #接收主机响应数据
    try:
        chuckLen = SockUtil.receiveNumBytes( sockobj, 4 )
        chuckData = SockUtil.receiveNumBytes( sockobj, struct.unpack( "!L", chuckLen )[0] - 4 )
        respData = chuckLen + chuckData
        
        if isDebug:
            logger.debug( '接收数据:\n' + dump( respData ) )
            
        sockobj.close( )
        
    except:
        sockobj.close( )
        HostContext.host_Error = True
        HostContext.host_ErrorType = 5
        HostContext.host_ErrorMsg = '接收主机响应数据失败'
        
        if isDebug:
            logger.error( '接收主机响应数据失败' )
            
        return

    #拆分主机返回的信息到HostContext中
    try:
        clearHostContext( )
        HostContext.host_Error = False
        HostContext.host_ErrorType = 0
        HostContext.host_ErrorMsg = '与主机通讯成功'
        HostDataHandler.hostUnpack( respData )
        
    except:
        HostContext.host_Error = True
        HostContext.host_ErrorType = 6
        HostContext.host_ErrorMsg = '拆分主机响应数据失败'
        
        if isDebug: 
            logger.error( '拆分主机响应数据失败' )
            logger.error( str( sys.exc_type ) )
            logger.error( str( sys.exc_value ) )
            logger.error( str( traceback.format_tb( sys.exc_traceback ) ) )
