# -*- coding: gbk -*-
##################################################################
#   中间业务平台.财税库行横向联网.单笔缴费交易
#=================================================================
#   程序文件:   TTPS002_845001.py
#   修改时间:   2008-5-2 16:02
##################################################################
import TradeContext, AfaLoggerFunc,Party3Context,TipsFunc,AfaFlowControl
import HostContext,HostComm,os
from types import *
from tipsConst import *

def SubModuleDoFst( ):
    try:
        AfaLoggerFunc.tradeInfo('进入缴费交易['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']前处理' )
        
        #begin 20101130 蔡永贵增加 缓存收款国库名称，用于后面登记流水
        TradeContext.note10 = TradeContext.payeeName
        #end
        
        #=============判断应用状态====================
        if not TipsFunc.ChkAppStatus( ) :
            return False
        #====获取清算信息=======
        if not TipsFunc.ChkLiquidStatus():
            return False
            
        #TradeContext.tradeType='T' #转账类交易
        if( not TradeContext.existVariable( "corpTime" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '委托日期[corpTime]值不存在!' )
        if( not TradeContext.existVariable( "corpSerno" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '第三方.交易流水号[corpSerno]值不存在!' )
        
        #检查批次是否过期
        AfaLoggerFunc.tradeInfo('>>>检查批次是否过期')
        if (TradeContext.corpTime!=TradeContext.workDate ):
            AfaLoggerFunc.tradeInfo('已过期，交易作废。报文工作日期:'+TradeContext.corpTime+'系统工作日期:'+TradeContext.workDate)
            return TipsFunc.ExitThisFlow( 'A0002', '工作日期不符,作废')

      
        #====检查是否签约户=======
        if not TipsFunc.ChkCustSign():
            return False
        #====查询收款帐号=======
        if not TipsFunc.SelectAcc():
            return False

        #begin 20100721 蔡永贵增加
        AfaLoggerFunc.tradeInfo( '--->原行号[' + TradeContext.brno + ']' )
        #====查询开户行行号======
        if not QueryBrnoInfo( ):
            return False
        #end

        #====获取摘要代码=======
        #if not AfaFlowControl.GetSummaryCode():
        #    return False
        
        #摘要代码
        TradeContext.summary_code = 'TIP'
        TradeContext.teller = TIPS_TELLERNO_AUTO                    #自动柜员
        
        
        #转换金额(以元为单位->以分为单位)
        #AfaLoggerFunc.tradeInfo('转换前金额(以元为单位)=' + TradeContext.amount)
        #TradeContext.amount=str(long((float(TradeContext.amount))*100 + 0.1))
        #AfaLoggerFunc.tradeInfo('转换后金额(以分为单位)=' + TradeContext.amount)
       
        #初始化
        TradeContext.catrFlag = '1'         #现金转账标志
        TradeContext.__agentEigen__ = '0'   #从表标志
        TradeContext.tradeType = '7'        #交易类型
        
       
        AfaLoggerFunc.tradeInfo('退出缴费交易['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']前处理' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e)) 
def SubModuledoSnd():
    try:
        return Party3Context.dn_detail
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))

#20100721 蔡永贵增加，查询开户行行号
def QueryBrnoInfo():
    try:
        AfaLoggerFunc.tradeInfo( '--->付款人账号[' + TradeContext.accno + ']' )
        AfaLoggerFunc.tradeInfo( '--->收款人账号[' + TradeContext.payeeAcct + ']' )
        #通讯区打包
        HostContext.I1TRCD = '8810'                        #主机交易码
        HostContext.I1SBNO = TIPS_SBNO_QS                  #该交易的发起机构
        HostContext.I1USID = TIPS_TELLERNO_AUTO            #交易柜员号
        HostContext.I1AUUS = ''                            #授权柜员
        HostContext.I1AUPS = ''                            #授权柜员密码
        HostContext.I1WSNO = '10.12.5.189'                 #终端号
        HostContext.I1ACNO = TradeContext.accno            #借方帐号
        HostContext.I1CYNO = '01'                          #币种
        HostContext.I1CFFG = '1'                           #密码校验标志(0-需要,1-不需要)
        HostContext.I1PSWD = ''                            #密码
        HostContext.I1CETY = ''                            #凭证种类
        HostContext.I1CCSQ = ''                            #凭证号码
        HostContext.I1CTFG = ''                            #钞汇标志

        HostTradeCode = "8810".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>主机交易失败=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return TipsFunc.ExitThisFlow( '9001', HostContext.host_ErrorMsg )
        else:
            if ( HostContext.O1MGID == 'AAAAAAA' ):
                TradeContext.brno             = HostContext.O1OPNT
                AfaLoggerFunc.tradeInfo( '----->开户机构[' + TradeContext.brno + ']' )

            else:
                return TipsFunc.ExitThisFlow( HostContext.O1MGID, HostContext.O1INFO )

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '程序处理异常'+str(e))
    return True
