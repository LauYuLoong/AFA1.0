# -*- coding: gbk -*-
##################################################################
#   中间业务平台.流程控制类
#=================================================================
#   程序文件:   AfaFlowControl.py
#   修改时间:   2006-09-26
##################################################################
import exceptions, TradeContext,TradeException,AfaLoggerFunc,AfaFunc
import os,time,AfaLoggerFunc
from types import *

#======================流程执行异常类==========================
class flowException ( exceptions.Exception ):

    def __init__( self, errorCode = None , errorMsg = None ):
        if errorCode != None and errorMsg != None :
            TradeContext.errorCode = errorCode
            TradeContext.errorMsg = errorMsg
    def __str__( self ):
        if TradeContext.existVariable("errorCode") and TradeContext.existVariable("errorMsg") and TradeContext.errorCode != None :
            #return 'FlowException' + ': ' + TradeContext.errorMsg
            return TradeContext.errorMsg
        else:
            return 'FlowException'

#======================帐务处理异常类===========================
class accException ( exceptions.Exception ):

    def __init__( self, errorCode = None , errorMsg = None ):
        if errorCode != None and errorMsg != None :
            TradeContext.errorCode = errorCode
            TradeContext.errorMsg = errorMsg
    def __str__( self ):
        if( TradeContext.existVariable("errorCode") and TradeContext.existVariable("errorMsg") and TradeContext.errorCode != None ):
            return 'AccException' + ': ' + TradeContext.errorMsg
        else:
            return 'AccException'

#==================用于交易异常时退出主执行流程=====================
def exitMainFlow( msgStr='' ):

    if( not TradeContext.existVariable( "errorCode" ) or msgStr ):
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg = '系统错误['+msgStr+']'

    if TradeContext.errorCode != '0000' :
        AfaLoggerFunc.tradeFatal( 'errorCode=['+TradeContext.errorCode+']' )
        AfaLoggerFunc.tradeFatal( 'errorMsg=['+TradeContext.errorMsg+']' )
        AfaLoggerFunc.tradeFatal(TradeContext.TransCode+'交易中断')

    if( not AfaFunc.autoPackData() ):
        lenContext=len( TradeContext.tradeResponse )
        chkFlag=0
        for i in range( lenContext ):
            if( type(TradeContext.tradeResponse[i][0]) is str and (TradeContext.tradeResponse[i][0]=='errorCode' or TradeContext.tradeResponse[i][0]=='errorMsg')):
                if(TradeContext.tradeResponse[i][0]=='errorCode'):
                    TradeContext.tradeResponse[i][1]=TradeContext.errorCode
                    chkFlag=chkFlag+1
                if(TradeContext.tradeResponse[i][0]=='errorMsg'):
                    TradeContext.tradeResponse[i][1]=TradeContext.errorMsg
                    chkFlag=chkFlag+1
                if(chkFlag>=2):
                    break
            elif i==lenContext-1 :
                TradeContext.tradeResponse.append( [ 'errorCode', TradeContext.errorCode ] )
                TradeContext.tradeResponse.append( [ 'errorMsg', TradeContext.errorMsg ] )
        
    #raise TradeException.TradeException( TradeContext.errorMsg )

#=======================交易异常时退出本处理流程===========================
def ExitThisFlow( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg = errorMsg
        #AfaFunc.autoPackData()
    if( TradeContext.errorCode.isdigit( )==True and long( TradeContext.errorCode )==0 ):
        return True
    else:
        return False
