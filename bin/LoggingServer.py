# -*- coding: gbk -*-
import os, sys
import cPickle, struct
import logging, logging.config
import SocketServer, socket
#import thread, threading

#=====刘雨龙 20081028 新增import字库操作====
from encodings import *


#listenConfigCommand = True
abort = False
configNum = 0

#configFileName = "../conf/service.conf"
configFileName = "../conf/serviceLog.conf"
unixDomainAddr = "./afaipc/domainLog"

#
#   The following code implements a socket listener for on-the-fly
#   reconfiguration of logging.
#
#   _listener holds the server object doing the listening
_listener = None
_server = None

DEFAULT_LOGGING_CONFIG_PORT = 9031
if sys.platform == "win32":
    RESET_ERROR = 10054   #WSAECONNRESET
else:
    RESET_ERROR = 104     #ECONNRESET

class LogRecordStreamHandler( SocketServer.StreamRequestHandler ):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle( self ):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while 1:
            chunk = self.connection.recv( 4 )
            if len( chunk ) < 4:
                break
            slen = struct.unpack( ">L", chunk )[0]
            chunk = self.connection.recv( slen )
            while len( chunk ) < slen:
                chunk = chunk + self.connection.recv( slen - len( chunk ) )
            obj = self.unPickle( chunk )
            record = logging.makeLogRecord( obj )
            self.handleLogRecord( record )

    def unPickle( self, data ):
        return cPickle.loads( data )

    def handleLogRecord( self, record ):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger( name )
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle( record )

class LogRecordDomainReceiver( SocketServer.ThreadingUnixStreamServer ):
    """simple Unix Domain socket-based logging receiver suitable for testing.
    """

    #allow_reuse_address = True
    #request_queue_size = 35
        
    def __init__( self, domainAddr=unixDomainAddr, handler=LogRecordStreamHandler ):
        #    change these attributes before bind(TCPServer.server_bind) and listen(TCPServer.server_activate)
        #self.allow_reuse_address = True    #    default:    False
        #self.request_queue_size = 35       #    default:    5
        SocketServer.ThreadingUnixStreamServer.__init__( self, ( domainAddr ), handler )
        self.abort = 0
        self.timeout = 1
        self.logname = None
    
    def serve_until_stopped( self ):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select( [self.socket.fileno( )], 
                                       [], [], 
                                       self.timeout )
            if rd:
                self.handle_request( )
            abort = self.abort

class ConfigStreamHandler( SocketServer.StreamRequestHandler ):
    """
    Handler for a logging configuration request.

    It expects a completely new logging configuration and uses fileConfig
    to install it.
    """
    def handle( self ):
        """
        Handle a request.

        Each request is expected to be a 4-byte length,
        followed by the config command. Uses fileConfig() to do the
        grunt work.
        """
        try:
            conn = self.connection
            chunk = conn.recv( 4 )
            if len( chunk ) == 4:
                slen = struct.unpack( ">L", chunk )[0]
                chunk = self.connection.recv( slen )
                while len( chunk ) < slen:
                    chunk = chunk + conn.recv( slen - len( chunk ) )
                if( chunk == 'reconfig' ):
                    global configNum
                    configNum = configNum + 1
                    print 'Reconfiguring logging server (', configNum, ')......'
                    #logging._acquireLock( )
                    #logging.shutdown( )
                    #logging._releaseLock( )
                    logging.config.fileConfig( configFileName )
                elif( chunk == 'stopserver' ):
                    print 'Shutting down logging server......'
                    stopServer( )
                else:
                    print 'Error config command from client!'
        except socket.error, e:
            if type( e.args ) != types.TupleType:
                raise
            else:
                errcode = e.args[0]
                if errcode != RESET_ERROR:
                    raise

class ConfigSocketReceiver( SocketServer.ThreadingTCPServer ):
    """
    A simple TCP socket-based logging config receiver.
    """

    allow_reuse_address = 1

    def __init__( self, host='localhost', port=DEFAULT_LOGGING_CONFIG_PORT, 
                 handler=ConfigStreamHandler ):
        SocketServer.ThreadingTCPServer.__init__( self, ( host, port ), handler )
        #logging._acquireLock( )
        self.abort = 0
        #logging._releaseLock( )
        self.timeout = 1

    def serve_until_stopped( self ):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select( [self.socket.fileno( )], 
                                       [], [], 
                                       self.timeout )
            if rd:
                self.handle_request( )
            #logging._acquireLock( )
            abort = self.abort
            #logging._releaseLock( )
            
def startServer( ):
    global _listener, _server
    timeout = 1
    try:
        os.unlink( unixDomainAddr )
    except:
        pass
    
    _listener = ConfigSocketReceiver( )
    _server = LogRecordDomainReceiver( )    
    listenFilno = _listener.socket.fileno( )
    serverFilno = _server.socket.fileno( )
   
    import select
    while not abort:
        rd, wr, ex = select.select( [listenFilno, serverFilno], [], [], timeout )
        if rd:
            for fileNo in rd:
                if( fileNo == serverFilno ):
                    _server.handle_request( )
                elif( fileNo == listenFilno ):
                    _listener.handle_request( )
    
def stopServer( ):
    """
    Stop the listening server which was created with a call to listen().
    """
    global _listener, _server, abort
    
    logging._acquireLock( )
    abort = True
    if _listener: 
        _listener = None                
    if _server:
        _server = None
        try:
            os.unlink( unixDomainAddr ) 
        except:
            pass       
    logging._releaseLock( )

if __name__ == "__main__":
    logging.config.fileConfig( configFileName )  
    logging.info( "Starting logging server..." ) 
    startServer( )
    logging.info( 'Logging server stoped successfuly!' ) 
