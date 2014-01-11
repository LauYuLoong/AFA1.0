# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收水费查询交易
#=================================================================
#   程序文件:   T4201_8422.py
#   修改时间:   2007-06-12
##################################################################

import TradeContext, AfaDBFunc

#需要上送第三方接口的前台没办法产生的,再此进行拼接.比如有的第三方查询也需要流水号等
def SubModuleMainFst( ):
    TradeContext.__agentEigen__  = '0'   #从表标志
    return True
 
def SubModuleMainSnd ():
    if TradeContext.errorCode   ==    "0000":
        TradeContext.errorMsg   =     "登陆成功"
    return True