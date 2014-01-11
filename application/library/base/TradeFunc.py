# -*- coding: gbk -*-
##################################################################
#                 ���׹��ú�������ģ��
#������������������������������������������������������������������������������
#                ��    �ߣ�    �� �� �� 
#                �޸�ʱ�䣺    20051111
##################################################################

from types import * 
import TradeException, TradeContext, Party3Context
import os, ConfigParser, time, sys, traceback

#    �Զ�����쳣���������ڽ����쳣ʱ�˳���ִ������
def exitOnError( errorCode , errorMsg ):
    TradeContext.tradeResponse = [[ 'errorCode', errorCode ], [ 'errorMsg', errorMsg ]]
    raise TradeException.TradeException( errorMsg )

#    ȡ�õ�ǰϵͳʱ�䣬Ĭ�ϸ�ʽΪYYYYmmdd
def getCurrentTime( format = "%Y%m%d" ):
    return time.strftime( format, time.localtime( ) )

#    �쳣����ʱ��ȡ�쳣��Ϣ�������쳣���͡��쳣ֵ���쳣��ջ��Ϣ
def getExceptInfo( ):
    exceptionInfo = sys.exc_info( )
    return [str( exceptionInfo[0] ), str( exceptionInfo[1] ), str( traceback.format_tb( exceptionInfo[2] ) )]

#    ͨ�������ļ���ʽ��ȡȥ��������AFE��������ַ���˿ں�����ͨѶ��ʱʱ��
def getAfeConfig( configFileName = None ):
    config = ConfigParser.ConfigParser( )
    if( configFileName == None ):
        configFileName = os.environ['AFAP_HOME'] + '/conf/afeconf/afe.conf'    
    config.readfp( open( configFileName ) )
     
    result = [config.get( 'AFECONFIG', 'IP' ), config.getint( 'AFECONFIG', 'PORT' ), config.getint( 'AFECONFIG', 'TIMEOUT' )]
    return result

#    �Զ��ѵ��������ص����н��ƴװ�����ظ�ǰ̨�Ľ����
def sendParty3Response( appendFlag = True ):
    #    ��ʼ��TradeContext.tradeResponse
    if( appendFlag ):    #    ��ԭ��TradeContext.tradeResponse���������
        if( not hasattr( TradeContext, "tradeResponse" ) ):
            TradeContext.tradeResponse = []
    else:    #    ���ԭ����TradeContext.tradeResponse���أ���ֻ��ӵ��������ؽ���������
        TradeContext.tradeResponse = []
    
    #    ƴװ�������������ݵ�TradeContext.tradeResponse
    names = Party3Context.getNames( )
    for name in names:
        value = getattr( Party3Context, name )
        if ( not name.startswith( '__' ) ) :
            if( type( value ) is StringType ) :
                TradeContext.tradeResponse.append( [name, value] )
            elif( type( value ) is ListType ) :
                for elem in value:
                    TradeContext.tradeResponse.append( [name, elem] )

#    ��յ�����ͨѶ�������ģ�����ǰ��ͨѶ��Ӱ�죬�Ա���һ�������н��ж�κ͵�������ͨѶ
def clearParty3Context( ):
    nameList=[]
    names = Party3Context.getNames( )
    for name in names:        
        if ( not name.startswith( '__' ) ) :
            value = getattr( Party3Context, name )
            if( ( type( value ) is StringType ) or ( type( value ) is ListType ) ):
                nameList.append( name )
    for name in nameList:
        delattr( Party3Context, name )
