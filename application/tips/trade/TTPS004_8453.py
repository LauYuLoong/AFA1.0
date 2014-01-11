# -*- coding: gbk -*-
##################################################################
#   中间业务平台.财税库行横向联网.银行端申报缴费交易
#=================================================================
#   程序文件:   TTPS004_8453.py
#   修改时间:   2008-5-2 16:02
##################################################################
import TradeContext, AfaLoggerFunc,Party3Context,TipsFunc
from types import *

def SubModuleDoFst( ):
    try:
        AfaLoggerFunc.tradeInfo('进入缴费交易['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']前处理' )
        #TradeContext.tradeType='T' #转账类交易
        #if( not TradeContext.existVariable( "corpTime" ) ):
        #    return TipsFunc.ExitThisFlow( 'A0001', '委托日期[corpTime]值不存在!' )
        #if( not TradeContext.existVariable( "corpSerno" ) ):
        #    return TipsFunc.ExitThisFlow( 'A0001', '第三方.交易流水号[corpSerno]值不存在!' )
        
        #====判断应用状态=======
        if not TipsFunc.ChkAppStatus():
            return False
            
        TradeContext.payeeBankNo = '011100000003'
        #====获取清算信息=======
        if not TipsFunc.ChkLiquidStatus():
            return False
        #====检查是否签约户=======
        #if not TipsFunc.ChkCustSign():
        #    return False
        #====判断机构状态=======
        if not TipsFunc.ChkBranchStatus():
            return False
        #====获取摘要代码=======
        #if not AfaFlowControl.GetSummaryCode():
        #    return False
        
        #摘要代码
        TradeContext.summary_code = 'TIP'
        
        #转换金额(以元为单位->以分为单位)
        #AfaLoggerFunc.tradeInfo('转换前金额(以元为单位)=' + TradeContext.amount)
        #TradeContext.amount=str(long((float(TradeContext.amount))*100 + 0.1))
        #AfaLoggerFunc.tradeInfo('转换后金额(以分为单位)=' + TradeContext.amount)
       
        #初始化
        #TradeContext.catrFlag = '1'         #现金转账标志
        TradeContext.__agentEigen__ = '0'   #从表标志
        TradeContext.channelCode = '001'
        TradeContext.userno = '12'
        TradeContext.zoneno = '000'
        AfaLoggerFunc.tradeInfo('==========================[' +TradeContext.accno+ ']')
        AfaLoggerFunc.tradeInfo('退出缴费交易['+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']前处理' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e)) 
def SubModuledoSnd():
    try:
        return Party3Context.dn_detail
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
        
        
def SubModuledoTrd():
    return True

