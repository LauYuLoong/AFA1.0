# -*- coding: gbk -*-
import os
import logging, socket, cPickle, struct, time

#################################################################################
#                    Unix Domain Socket日志处理类
#################################################################################
class DomainHandler( logging.Handler ):
    """
    A handler class which writes logging records, in pickle format, to
    a streaming unix domain socket. The socket is kept open across logging calls.
    If the peer resets it, an attempt is made to reconnect on the next call.
    The pickle which is sent is that of the LogRecord's attribute dictionary
    (__dict__), so that the receiver does not need to have the logging module
    installed in order to process the logging event.

    To unpickle the record at the receiving end into a LogRecord, use the
    makeLogRecord function.
    """

    def __init__( self, domainAddr ):
        """
        Initializes the handler with a specific unix domain address.

        The attribute 'closeOnError' is set to 1 - which means that if
        a socket error occurs, the socket is silently closed and then
        reopened on the next logging call.
        """
        logging.Handler.__init__( self )
        self.domainAddr = domainAddr
        self.sock = None
        self.closeOnError = 0
        self.retryTime = None
        #
        # Exponential backoff parameters.
        #
        self.retryStart = 1.0
        self.retryMax = 30.0
        self.retryFactor = 2.0

    def makeSocket( self ):
        """
        A factory method which allows subclasses to define the precise
        type of socket they want.
        """
        s = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
        s.connect( ( self.domainAddr ) )
        return s

    def createSocket( self ):
        """
        Try to create a socket, using an exponential backoff with
        a max retry time. Thanks to Robert Olson for the original patch
        (SF #815911) which has been slightly refactored.
        """
        now = time.time( )
        # Either retryTime is None, in which case this
        # is the first time back after a disconnect, or
        # we've waited long enough.
        if self.retryTime is None:
            attempt = 1
        else:
            attempt = ( now >= self.retryTime )
        if attempt:
            try:
                self.sock = self.makeSocket( )
                self.retryTime = None # next time, no delay before trying
            except:
                #Creation failed, so set the retry time and return.
                if self.retryTime is None:
                    self.retryPeriod = self.retryStart
                else:
                    self.retryPeriod = self.retryPeriod * self.retryFactor
                    if self.retryPeriod > self.retryMax:
                        self.retryPeriod = self.retryMax
                self.retryTime = now + self.retryPeriod

    def send( self, s ):
        """
        Send a pickled string to the socket.

        This function allows for partial sends which can happen when the
        network is busy.
        """
        if self.sock is None:
            self.createSocket( )
        #self.sock can be None either because we haven't reached the retry
        #time yet, or because we have reached the retry time and retried,
        #but are still unable to connect.
        if self.sock:
            try:
                if hasattr( self.sock, "sendall" ):
                    self.sock.sendall( s )
                else:
                    sentsofar = 0
                    left = len( s )
                    while left > 0:
                        sent = self.sock.send( s[sentsofar:] )
                        sentsofar = sentsofar + sent
                        left = left - sent
            except socket.error:
                self.sock.close( )
                self.sock = None  # so we can call createSocket next time

    def makePickle( self, record ):
        """
        Pickles the record in binary format with a length prefix, and
        returns it ready for transmission across the socket.
        """
        ei = record.exc_info
        if ei:
            dummy = self.format( record ) # just to get traceback text into record.exc_text
            record.exc_info = None  # to avoid Unpickleable error
        s = cPickle.dumps( record.__dict__, 1 )
        if ei:
            record.exc_info = ei  # for next handler
        slen = struct.pack( ">L", len( s ) )
        return slen + s

    def handleError( self, record ):
        """
        Handle an error during logging.

        An error has occurred during logging. Most likely cause -
        connection lost. Close the socket so that we can retry on the
        next event.
        """
        print 'Error occured in logging!'
        if self.closeOnError and self.sock:
            self.sock.close( )
            self.sock = None        #try to reconnect next time
        else:
            logging.Handler.handleError( self, record )

    def emit( self, record ):
        """
        Emit a record.

        Pickles the record and writes it to the socket in binary format.
        If there is an error with the socket, silently drop the packet.
        If there was a problem with the socket, re-establishes the
        socket.
        """
        try:
            s = self.makePickle( record )
            self.send( s )
        except:
            self.handleError( record )

    def close( self ):
        """
        Closes the socket.
        """
        if self.sock:
            self.sock.close( )
            self.sock = None
        logging.Handler.close( self )

#################################################################################
#          取得应用或者交易对应的日志，用以向Unix Domain Socket发送日志请求
#################################################################################
#print
#print 'Initializing logger......', os.getpid( )
rootLogger = logging.getLogger( '' )
rootLogger.setLevel( logging.DEBUG )

# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
domainHandler = DomainHandler( os.environ['AFAP_HOME']+'/bin/afaipc/domainLog' )
rootLogger.addHandler( domainHandler )
#print 'Logger Initializd successfully(', os.getpid( ), "):\t", rootLogger
#print rootLogger
#print

def getLogger( loggerName ): 
    return logging.getLogger( loggerName )

def setLevel( level ):
    rootLogger = logging.getLogger( '' )
    rootLogger.setLevel( level )

#################################################################################
#                          业务进程的日志处理
#################################################################################
serviceLogger = logging.getLogger( "service" )

def serviceDebug( msg ):
    serviceLogger.debug( msg )

def serviceInfo( msg ):
    serviceLogger.info( msg )

def serviceWarn( msg ):
    serviceLogger.warn( msg )

def serviceError( msg ):
    serviceLogger.error( msg )

def serviceFatal( msg ):
    serviceLogger.fatal( msg )
