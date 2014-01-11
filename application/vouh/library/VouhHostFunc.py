# -*- coding: gbk -*-
##################################################################
#   代收代付平台.与主机通讯函数
#=================================================================
#   程序文件:   VouhHostFunc.py
#   修改时间:   2008-06-13
#               李亚杰
#
##################################################################
import TradeContext,UtilTools,HostComm,HostContext,AfaLoggerFunc,os
#,AfaFunc,AfaFlowControl,AfaHostFunc,HostDataHandler
from types import *

def VouhCommHost():
    if( TradeContext.existVariable( "sOperSty" ) ):
        HostContext.I1OPTY = TradeContext.sOperSty
    else:
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '交易模式[sOperSty]值不存在!'
        return False
        
    #################################################
    #交易模式：      0、借方 		如入库;
	#				1、贷方 		如出库、作废、手工销号;
	#				2、双方帐务 如上缴、领用、调配;
	#################################################
	
    if( TradeContext.existVariable("sInTellerNo")):
        HostContext.I1SJUS = TradeContext.sInTellerNo
    elif( TradeContext.sOperSty =='2'):
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '对方柜员[sInTellerNo]值不存在!'
        return False
        
    if( TradeContext.existVariable("sInBesbNo")):
        HostContext.I1OPNT = TradeContext.sInBesbNo
    elif( TradeContext.sOperSty =='2'):
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '对方机构代号[sInBesbNo]值不存在!'
        return False
        
    AfaLoggerFunc.tradeInfo( '=======================1' )
    if( TradeContext.existVariable("sPassWD")):
        HostContext.I1PSWD = TradeContext.sPassWD
    elif( TradeContext.sOperSty =='2'):
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '密码[sPassWD]值不存在!'
        return False
    
    AfaLoggerFunc.tradeInfo( '=======================2' )
    if( TradeContext.existVariable( "sBesbNo" )):
        HostContext.I1SBNO = TradeContext.sBesbNo
    else:
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '机构代号[sBesbNo]值不存在!'
        return False
    
    
    AfaLoggerFunc.tradeInfo( '=======================3' )
    if( TradeContext.existVariable( "sTellerNo" )):
        HostContext.I1USID = TradeContext.sTellerNo      
    else:
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '交易柜员[I1USID]值不存在!'
        return False
     
    AfaLoggerFunc.tradeInfo( '=======================4' )   
    if( TradeContext.existVariable( "sWSNO" )):
        HostContext.I1WSNO = TradeContext.sWSNO
    else:
        TradeContext.errorCode = 'A005060'
        TradeContext.errorMsg = '终端号[sWSNO]值不存在!'
        return False    
                
    AfaLoggerFunc.tradeInfo( '=======================5' )
    if( TradeContext.existVariable( "sCur" )):
        HostContext.I1CYNO = TradeContext.sCur
        
    if( TradeContext.existVariable("sNum")):
        HostContext.I1ACUR = TradeContext.sNum
    
    AfaLoggerFunc.tradeInfo( '=======================6,'+str(TradeContext.sNum) )
    HostContext.I2CETY = []
    HostContext.I2NUBZ = []
    
    HostContext.I1DATE = TradeContext.sLstTrxDay           #中台日期
    HostContext.I1AGNO = TradeContext.sVouhSerial          #中台流水号
        
    for i in range(TradeContext.sNum):
        HostContext.I2CETY.append(TradeContext.sVouhType[i])
        HostContext.I2NUBZ.append(TradeContext.sVouhNum[i])
        
    AfaLoggerFunc.tradeInfo( '=======================7' )
        
    #与主机数据交换
    CommHost()
    
        

#====================与主机数据交换=============================
def CommHost( result = '8827' ):

    AfaLoggerFunc.tradeInfo('>>>主机通讯函数[CommHost]')

    #根据正反交易标志TradeContext.revTranF判断具体选择哪个map文件和主机接口方式

    if (result == '8827'):
        AfaLoggerFunc.tradeInfo('>>>凭证记帐')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8827.map'
        TradeContext.HostCode = '8827'

    elif(result == '8828'):
        AfaLoggerFunc.tradeInfo('>>>凭证对帐')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8828.map'
        TradeContext.HostCode = '8828'
    
    elif(result == '2001'):
        AfaLoggerFunc.tradeInfo('>>>获取机构类型')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH2001.map'
        TradeContext.HostCode = '2001'
    
    elif(result == '8809'):
        AfaLoggerFunc.tradeInfo('>>>获取机构类型')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8809.map'
        TradeContext.HostCode = '8809' 
    
    #begin凭证优化更改201109  
    elif(result == '0104'):
        AfaLoggerFunc.tradeInfo('>>>查询柜员尾箱号')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH0104.map'
        TradeContext.HostCode = '0104'
    #end
    
    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '主机代码错误'
        return False

    AfaLoggerFunc.tradeInfo( '=======================8' )
    #此处交易代码要求10位,右补空格
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )
    AfaLoggerFunc.tradeInfo( '=======================9' )
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
    AfaLoggerFunc.tradeInfo( '=======================10' )
    #================分析主机返回包====================
    return HostParseRet(result )


#================分析主机返回包====================
def HostParseRet( hostType ):
    HostContext.O1TLSQ=''
    AfaLoggerFunc.tradeInfo( '=======================11' )
    if (HostContext.host_Error == True):    #主机通讯错误
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '主机通讯错误'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #通讯错误代码
        return False
    AfaLoggerFunc.tradeInfo( '=======================12'+HostContext.O1MGID )
    if( HostContext.O1MGID == 'AAAAAAA' ): #成功
        
        AfaLoggerFunc.tradeInfo('>>>凭证记账====' + HostContext.O1MGID)

        
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '主机成功'
        TradeContext.HostSerno = HostContext.O1TLSQ                               #柜员流水号
        TradeContext.HostDate = HostContext.O1TRDT                                #主机时间
        TradeContext.bankCode  = HostContext.O1MGID                               #主机返回代码
        return True

    else:                                  #失败
        TradeContext.__status__='1'
        
        #安徽农信-主机自动返回错误信息，不需要转换
        #result = AfapFunc.RespCodeMsg(HostContext.O1MGID,'0000','100000')
        #if not result :
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
