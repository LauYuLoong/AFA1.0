# -*- coding: gbk -*-
##################################################################
#   代收代付平台.财税库行横向联网.公共交易
#       procType  01 查询账户信息
#       procType  02 查询征收机关信息
#=================================================================
#   程序文件:   TTPS001_8466.py
#   修改时间:   2007-10-23
##################################################################
#UtilTools,AfaDBFunc，TradeFunc,
import TradeContext, AfaLoggerFunc,  AfaFlowControl, os,HostContext
import HostComm,TipsFunc

def SubModuleMainFst( ):
    
    if TradeContext.procType=='01':
        AfaLoggerFunc.tradeInfo('>>>查询账户信息')
        if not QueryAccInfo():
            return False
    elif TradeContext.procType=='02': 
        AfaLoggerFunc.tradeInfo('>>>查询征收机关信息')
        if not TipsFunc.ChkTaxOrg(TradeContext.taxOrgCode):
            return False
    elif TradeContext.procType=='03': #缴费查询清算信息，贷方信息
        if not TipsFunc.ChkTaxOrg(TradeContext.taxOrgCode):
            return False
        #if not TipsFunc.ChkLiquidInfo():
        #    return False
    elif TradeContext.procType=='04': 
        AfaLoggerFunc.tradeInfo('>>>查询清算国库信息')
        if not TipsFunc.ChkTre(TradeContext.treCode,TradeContext.payeeBankNo):
            return False
    else:
        return AfaFlowControl.ExitThisFlow('0001', '未定义该查询类型')    
    TradeContext.errorCode='0000'
    TradeContext.errorMsg='查询信息成功'
    return True
 
def SubModuleMainSnd ():
    return True


def QueryAccInfo():
    try:
        #通讯区打包
        HostContext.I1TRCD = '8810'                        #主机交易码
        HostContext.I1SBNO = TradeContext.brno             #该交易的发起机构
        HostContext.I1USID = TradeContext.teller           #交易柜员号
        HostContext.I1AUUS = TradeContext.authTeller       #授权柜员
        HostContext.I1AUPS = TradeContext.authPwd          #授权柜员密码
        HostContext.I1WSNO = TradeContext.termId           #终端号
        HostContext.I1ACNO = TradeContext.accno            #帐号
        HostContext.I1CYNO = '01'                          #币种
        HostContext.I1CFFG = '1'                           #密码校验标志(0-需要,1-不需要)
        HostContext.I1PSWD = ''                            #密码
        #HostContext.I1CETY = TradeContext.I1VOUTHTYPE      #凭证种类
        #HostContext.I1CCSQ = TradeContext.I1VOUTHNO        #凭证号码
        #HostContext.I1CTFG = TradeContext.I1CHFLAG         #钞汇标志
        HostContext.I1CETY = ''                           #凭证种类
        HostContext.I1CCSQ = ''                           #凭证号码
        HostContext.I1CTFG = ''                           #钞汇标志

        HostTradeCode = "8810".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>主机交易失败=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return AfaFlowControl.ExitThisFlow('9001', HostContext.host_ErrorMsg)
        else:
            if ( HostContext.O1MGID == 'AAAAAAA' ):
                TradeContext.userName         = HostContext.O1CUNM
                TradeContext.accStatus        = HostContext.O1ACST
                TradeContext.idType         = HostContext.O1IDTY
                TradeContext.idCode         = HostContext.O1IDNO
                TradeContext.openBrno        = HostContext.O1OPNT
                
                if ( TradeContext.accStatus != '0'):
                    return AfaFlowControl.ExitThisFlow('9000','客户银行账户状态异常,不能进行注册')
            else:
                return AfaFlowControl.ExitThisFlow(HostContext.O1MGID, HostContext.O1INFO)

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))
    return True