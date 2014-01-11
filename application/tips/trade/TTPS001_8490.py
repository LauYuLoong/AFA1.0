# -*- coding: gbk -*-
##################################################################
#   代收代付平台.财税库行横向联网.人工重发银行端缴款回执
#=================================================================
#   程序文件:   TPS001_8490.py
#   修改时间:   2007-10-23
##################################################################

import TradeContext, AfaFlowControl
#LoggerHandler, UtilTools,  os, AfaLoggerFunc
import AfaAfeFunc,TipsFunc

def SubModuleMainFst( ):

    try:
    
        #=============获取平台流水号====================
        if TipsFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
            
        TradeContext.TaxVouNo = '34234234'
        TradeContext.OriTaxOrgCode = '21100000000'
        TradeContext.OriEntrustDate = '20060623'
        TradeContext.OriTraNo = '00000012'
        TradeContext.TaxDate = '20060623'
        TradeContext.Result = '90000'
        TradeContext.AddWord = '交易成功'
        
        #=============与第三方通讯====================
        AfaAfeFunc.CommAfe()
        if( TradeContext.errorCode != '0000' ):
            return False

        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '交易成功'

    except AfaFlowControl.flowException, e:
        return False
    except Exception, e:
        return AfaFlowControl.ExitThisFlow('A9999','系统异常'+str(e) )
    return True
 
def SubModuleMainSnd ():
    return True
