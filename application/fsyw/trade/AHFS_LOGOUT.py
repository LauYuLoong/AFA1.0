# -*- coding: gbk -*-
###############################################################################
# ժ    Ҫ�����շ�˰_ǩ��
#
# ��ǰ�汾��1.0
# ��    �ߣ�XZH
# ������ڣ�2008��3��8��
###############################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc, sys, os
from types import *

TradeContext.sysType = 'cron'
##########################################ǩ��##########################################
def Ahdx_Login():

    try:
        sqlStr = "SELECT STATUS FROM ABDT_UNITINFO WHERE"
        
        #begin 20100528 �������޸�
        #sqlStr = sqlStr + " APPNO = '"      + 'AG2008'  + "'"
        sqlStr = sqlStr + " APPNO in ('AG2008','AG2012')"
        #end
        
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        #AfaLoggerFunc.tradeInfo(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None or len(records) < 0):
            AfaLoggerFunc.tradeInfo('>>>������:ǩ��ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","ǩ��ʧ��,���ݿ��쳣"
            sys.exit(1)

        elif ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('>>>������:û�з��ָõ�λ��Ϣ,����ǩ��')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�з��ָõ�λ��Ϣ,����ǩ��"
            sys.exit(1)


        sqlStr = "UPDATE ABDT_UNITINFO SET STATUS='2' WHERE"
        
        #begin 20100528 �������޸�
        #sqlStr = sqlStr + " APPNO = '"      + 'AG2008'  + "'"
        sqlStr = sqlStr + " APPNO in ('AG2008','AG2012')"
        #end
        
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        retcode = AfaDBFunc.UpdateSqlCmt( sqlStr )
        if (retcode==None or retcode <= 0):
            AfaLoggerFunc.tradeInfo('>>>������:ǩ��ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","ǩ��ʧ��,���ݿ��쳣"
            sys.exit(1)

        AfaLoggerFunc.tradeInfo('>>>������:ǩ�˳ɹ�')

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001",str(e)
        sys.exit(1)
        
###########################################������###########################################
if __name__=='__main__':
    AfaLoggerFunc.tradeInfo('>>>��˰ǩ��')
    Ahdx_Login()
