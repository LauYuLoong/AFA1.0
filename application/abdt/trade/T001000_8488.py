# -*- coding: gbk -*-
################################################################################
#   批量业务系统：批量业务公用交易
#===============================================================================
#   交易文件:   T001000_8401.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AbdtFunc
from types import *


#=====================批量业务公用交易==========================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********批量业务公用交易(8488)开始**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间


    if ( TradeContext.I1PROCTYPE == '01' ):

        #查询账户信息
        if ( not AbdtFunc.VMENU_QueryAccInfo( ) ):
            return False

    else:
        return ExitSubTrade( '9000', '无此操作类型' )


    AfaLoggerFunc.tradeInfo('**********批量业务公用交易(8488)结束**********')


    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True
       
    
    

def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False