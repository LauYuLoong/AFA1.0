# -*- coding: gbk -*-
##################################################################
#                 交易公用函数定义模块
#＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
#                作    者：    陈 显 明 
#                修改时间：    20051111
##################################################################

from types import * 
import TradeException, TradeContext, Party3Context
import os, ConfigParser, time, sys, traceback

#    自定义的异常函数，用于交易异常时退出主执行流程
def exitOnError( errorCode , errorMsg ):
    TradeContext.tradeResponse = [[ 'errorCode', errorCode ], [ 'errorMsg', errorMsg ]]
    raise TradeException.TradeException( errorMsg )

#    取得当前系统时间，默认格式为YYYYmmdd
def getCurrentTime( format = "%Y%m%d" ):
    return time.strftime( format, time.localtime( ) )

#    异常发生时获取异常信息，包括异常类型、异常值和异常堆栈信息
def getExceptInfo( ):
    exceptionInfo = sys.exc_info( )
    return [str( exceptionInfo[0] ), str( exceptionInfo[1] ), str( traceback.format_tb( exceptionInfo[2] ) )]

#    通过配置文件方式读取去第三方的AFE服务器地址、端口和网络通讯超时时间
def getAfeConfig( configFileName = None ):
    config = ConfigParser.ConfigParser( )
    if( configFileName == None ):
        configFileName = os.environ['AFAP_HOME'] + '/conf/afeconf/afe.conf'    
    config.readfp( open( configFileName ) )
     
    result = [config.get( 'AFECONFIG', 'IP' ), config.getint( 'AFECONFIG', 'PORT' ), config.getint( 'AFECONFIG', 'TIMEOUT' )]
    return result

#    自动把第三方返回的所有结果拼装到返回给前台的结果集
def sendParty3Response( appendFlag = True ):
    #    初始化TradeContext.tradeResponse
    if( appendFlag ):    #    在原来TradeContext.tradeResponse基础上添加
        if( not hasattr( TradeContext, "tradeResponse" ) ):
            TradeContext.tradeResponse = []
    else:    #    清除原来的TradeContext.tradeResponse返回，并只添加第三方返回结果到结果集
        TradeContext.tradeResponse = []
    
    #    拼装第三方返回数据到TradeContext.tradeResponse
    names = Party3Context.getNames( )
    for name in names:
        value = getattr( Party3Context, name )
        if ( not name.startswith( '__' ) ) :
            if( type( value ) is StringType ) :
                TradeContext.tradeResponse.append( [name, value] )
            elif( type( value ) is ListType ) :
                for elem in value:
                    TradeContext.tradeResponse.append( [name, elem] )

#    清空第三方通讯的上下文，消除前次通讯的影响，以便在一个交易中进行多次和第三方的通讯
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
