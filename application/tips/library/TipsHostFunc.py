# -*- coding: gbk -*-
##################################################################
#   代收代付平台.与主机通讯函数
#=================================================================
#   程序文件:   TipsHostFunc.py
#   修改时间:   2008-06-13
#               李亚杰
#
##################################################################
import TradeContext,UtilTools,HostComm,HostContext,AfaLoggerFunc,os
from types import *

#=================初始化主机通讯接口=======================
def InitHostReq( ):
    #初始化函数返回值变量
    AfaLoggerFunc.tradeInfo('初始化map文件信息[InitHostReq]')
    HostContext.I1SBNO = TradeContext.sBrNo              #交易机构号
    HostContext.I1USID = TradeContext.sTeller            #交易柜员号
    HostContext.I1WSNO = TradeContext.sTermId            #终端号
    if(TradeContext.existVariable('sOpeFlag' ) ): 
        HostContext.I1OPFG = TradeContext.sOpeFlag           #操作标志
    #if(TradeContext.existVariable('entrustDate' ) ): 
    #    HostContext.I1TRDT = TradeContext.entrustDate        #批量委托日期
    if(TradeContext.existVariable('entrustDate' ) ): 
        HostContext.I1CLDT = TradeContext.entrustDate        #批量委托日期
    if(TradeContext.existVariable('packNo' ) ):  
        HostContext.I1UNSQ = TradeContext.packNo             #批量委托号
    if(TradeContext.existVariable('sFileName')):
        HostContext.I1FINA = TradeContext.sFileName          #文件名
    if(TradeContext.existVariable('sTotal' ) ):          #总笔数
        HostContext.I1COUT = TradeContext.sTotal      
    if(TradeContext.existVariable('sAmount' )):       
        HostContext.I1TOAM = TradeContext.sAmount            #总金额
    
    AfaLoggerFunc.tradeInfo('初始化map文件信息[InitHostReq]完成')

    return True

#====================与主机数据交换=============================
def CommHost( result = '8830' ):

    AfaLoggerFunc.tradeInfo('>>>主机通讯函数[CommHost]')
    
    if(not InitHostReq()):
        return False

    #根据正反交易标志TradeContext.revTranF判断具体选择哪个map文件和主机接口方式

    if (result == '8830'):
        AfaLoggerFunc.tradeInfo('>>>批量上传')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8830.map'
        TradeContext.HostCode = '8830'

    elif(result == '8831'):
        AfaLoggerFunc.tradeInfo('>>>批量记账申请')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8831.map'
        TradeContext.HostCode = '8831'
    elif(result == '8833'):
        AfaLoggerFunc.tradeInfo('>>>批量回盘文件生成申请')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8833.map'
        TradeContext.HostCode = '8833'
    elif(result == '8834'):
        AfaLoggerFunc.tradeInfo('>>>查询批量记账结果')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8834.map'
        TradeContext.HostCode = '8834'
    elif(result == '8810'):
        AfaLoggerFunc.tradeInfo('>>>查询单个账户信息')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map'
        TradeContext.HostCode = '8810'    
    elif(result == '8835'):
        AfaLoggerFunc.tradeInfo('>>>凭证消号')
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8835.map'
        TradeContext.HostCode = '8835'    
    else:
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg  = '主机代码错误'
        return False

    #此处交易代码要求10位,右补空格
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )
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
    #================分析主机返回包====================
    return HostParseRet(result )


#================分析主机返回包====================
def HostParseRet( hostType ):
    if (HostContext.host_Error == True):    #主机通讯错误
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '主机通讯错误'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #通讯错误代码
        return False

    if( HostContext.O1MGID == 'AAAAAAA' ): #成功

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
        #    TradeContext.errorCode, TradeContext.errorMsg = 'A9999', '系统错误[主机未知错误]['+HostContext.ERR+']'
        #else:
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False
