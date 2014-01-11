# -*- coding: gbk -*-
###############################################################################
# 摘    要：安徽新农保_签退
#
# 当前版本：1.0
# 作    者：ZZT
# 完成日期：2011年01月25日
###############################################################################
import TradeContext 
TradeContext.sysType = 'ahxnb'

import AfaDBFunc, AfaLoggerFunc, sys
from types import *


##########################################签退##########################################
def xnb_Logout():

    try:
        

        sqlStr = "UPDATE AFA_SYSTEM SET STATUS='2' WHERE"
        
        sqlStr = sqlStr + " SYSID ='AG2015'"
        
        AfaLoggerFunc.tradeInfo('签退sql:'+sqlStr)
       
        retcode = AfaDBFunc.UpdateSqlCmt( sqlStr )
        if (retcode==None or retcode <= 0):
            AfaLoggerFunc.tradeInfo('>>>处理结果:签退失败,数据库异常')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","签退失败,数据库异常"
            sys.exit(1)

        AfaLoggerFunc.tradeInfo('>>>处理结果:签退成功')

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001",str(e)
        sys.exit(1)
        
###########################################主函数###########################################
if __name__=='__main__':
    AfaLoggerFunc.tradeInfo('>>> 安徽新农保签退')
    xnb_Logout()
