# -*- coding: gbk -*-
###############################################################################
# ժ    Ҫ��������ũ��_ǩ��
#
# ��ǰ�汾��1.0
# ��    �ߣ�ZZT
# ������ڣ�2011��01��25��
###############################################################################
import TradeContext
TradeContext.sysType = 'ahxnb'
import AfaDBFunc, AfaLoggerFunc, sys
from types import *

##########################################ǩ��##########################################
def xnb_Login():

    try:

        sqlStr = "UPDATE AFA_SYSTEM SET STATUS='1' WHERE"
        
        sqlStr = sqlStr + " SYSID ='AG2015'"
        
        AfaLoggerFunc.tradeInfo('ǩ��sql:'+sqlStr)
        
        retcode = AfaDBFunc.UpdateSqlCmt( sqlStr )
        if (retcode==None or retcode <= 0):
            AfaLoggerFunc.tradeInfo('>>>������:ǩ��ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","ǩ��ʧ��,���ݿ��쳣"
            sys.exit(1)

        AfaLoggerFunc.tradeInfo('>>>������:ǩ���ɹ�')

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001",str(e)
        sys.exit(1)
        
###########################################������###########################################
if __name__=='__main__':
    AfaLoggerFunc.tradeInfo('>>>����ʡ��ũ��ǩ��')
    xnb_Login()
