# -*- coding: gbk -*-
##################################################################
#   代收代付平台.与主机通讯函数
#=================================================================
#   程序文件:   VouhHostFunc.py
#   修改时间:   2008-12-18
#               
#
##################################################################
import TradeContext,AfaFunc,UtilTools,HostComm,HostContext,HostDataHandler,AfaLoggerFunc,os,AfaFlowControl
from types import *

#====================与主机数据交换=============================
def CommHost( result = '8844' ):

    AfaLoggerFunc.tradeInfo('>>>主机通讯函数[CommHost]')

    #根据正反交易标志TradeContext.revTranF判断具体选择哪个map文件和主机接口方式

    if (result == '8844'):
        AfaLoggerFunc.tradeInfo('>>>核心记帐')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8844.map'
        TradeContext.HostCode = '8844'

    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '主机代码错误'
        return False

    AfaLoggerFunc.tradeInfo( '=======================7' )
    #此处交易代码要求10位,右补空格
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )
    AfaLoggerFunc.tradeInfo( '=======================8' )
    if HostContext.host_Error:
        AfaLoggerFunc.tradeFatal( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )

        if HostContext.host_ErrorType != 5 :
            TradeContext.__status__='1'
            TradeContext.errorCode='A0101'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        else :
            TradeContext.__status__='2'
            TradeContext.errorCode='A0102'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        return False
    AfaLoggerFunc.tradeInfo( '=======================9' )
    #================分析主机返回包====================
    return HostParseRet(result )


#================分析主机返回包====================
def HostParseRet( hostType ):
    HostContext.O1TLSQ=''
    AfaLoggerFunc.tradeInfo( '=======================10' )
    if (HostContext.host_Error == True):    #主机通讯错误
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '主机通讯错误'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #通讯错误代码
        return False
    AfaLoggerFunc.tradeInfo( '=======================11'+HostContext.O1MGID )
    if( HostContext.O1MGID == 'AAAAAAA' ): #成功
        
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '主机成功'
        TradeContext.PDTLSQ = HostContext.O1TLSQ                               #柜员流水号
        TradeContext.PDTRDT = HostContext.O1TRDT                                #主机时间
        TradeContext.PAMGID = HostContext.O1MGID                               #主机返回代码
        return True

    else:                                  #失败
        TradeContext.__status__='1'
        
        #安徽农信-主机自动返回错误信息，不需要转换
        #result = AfapFunc.RespCodeMsg(HostContext.O1MGID,'0000','100000')
        #if not result :
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
