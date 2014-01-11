# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.���̿�����
#=================================================================
#   �����ļ�:   AfaFlowControl.py
#   �޸�ʱ��:   2006-09-26
##################################################################
import exceptions, TradeContext,TradeException,AfaLoggerFunc,AfaFunc
import os,time,AfaLoggerFunc
from types import *

#======================����ִ���쳣��==========================
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

#======================�������쳣��===========================
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

#==================���ڽ����쳣ʱ�˳���ִ������=====================
def exitMainFlow( msgStr='' ):

    if( not TradeContext.existVariable( "errorCode" ) or msgStr ):
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg = 'ϵͳ����['+msgStr+']'

    if TradeContext.errorCode != '0000' :
        AfaLoggerFunc.tradeFatal( 'errorCode=['+TradeContext.errorCode+']' )
        AfaLoggerFunc.tradeFatal( 'errorMsg=['+TradeContext.errorMsg+']' )
        AfaLoggerFunc.tradeFatal(TradeContext.TransCode+'�����ж�')

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

#=======================�����쳣ʱ�˳�����������===========================
def ExitThisFlow( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg = errorMsg
        #AfaFunc.autoPackData()
    if( TradeContext.errorCode.isdigit( )==True and long( TradeContext.errorCode )==0 ):
        return True
    else:
        return False
