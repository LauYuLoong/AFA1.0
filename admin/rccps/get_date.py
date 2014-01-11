# -*- coding: gbk -*-
###################################################################
#    ��ǰ��ϵͳ.����������ʱ��ͬ��
#==================================================================
#    �����ļ���  get_date.py
#    �޸�ʱ�䣺  2008-7-7
#    ��    �ߣ�  ������
#==================================================================
#    �޸�ʱ�䣺
#    �޸���  ��
#==================================================================
#    ��    �ܣ�  ����������ͬ������
###################################################################
import TradeContext,HostContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
import rccpsCronFunc,AfaHostFunc
import sys, time

from types import *
from rccpsConst import *

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***��ǰ��ϵͳ: ͬ������������ʱ�� ����***")

        #=====��ʼƴ�����ӿ�====
        #TradeContext.TransCode   = '9999'             #������
        #TradeContext.HostCode    = '8808'             #����������
        #TradeContext.brno        = PL_BESBNO_BCLRSB   #������
        #TradeContext.tellerno    = PL_BETELR_AUTO     #��Ա��
        #TradeContext.termId      = '1234567890'       #�ն˺�
        #TradeContext.sysId       = '9999'             #ϵͳ��ʶ
        TradeContext.TransCode   = '9999'             #������
        HostContext.I1TRCD      = '8808'             #����������
        HostContext.I1SBNO      = PL_BESBNO_BCLRSB   #������
        HostContext.I1USID      = PL_BETELR_AUTO     #��Ա��
        HostContext.I1WSNO      = '1234567890'       #�ն˺�
        HostContext.I1PYNO      = '9999'             #ϵͳ��ʶ
        HostContext.I1AUUS = ''
        HostContext.I1AUPS = ''

        #====����������ͨѶ====
        AfaHostFunc.CommHost('8808')
      
        #=====�ж��������ؽ��====
        if TradeContext.errorCode == '0000':
            #=====ͬ�����ݿ��AFA_DATE====
            sql = "UPDATE AFA_DATE SET WORKDATE='" + HostContext.O1TRDT + "'"
            sql = sql + ", WORKTIME = '" + HostContext.O1TRTM + "'"
            sql = sql + ", HOSTDATE = '" + HostContext.O1DATE + "'"

            ret = AfaDBFunc.UpdateSqlCmt(sql)
            if ret < 0:
                AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
                rccpsCronFunc.cronExit("S999","����ϵͳʱ���쳣")
            else:
                AfaLoggerFunc.tradeInfo('��������['+HostContext.O1TRDT +']')
                AfaLoggerFunc.tradeInfo('����ʱ��['+HostContext.O1TRTM +']')
        else:
            rccpsCronFunc.cronExit("S999","������ͬ��ϵͳʱ���쳣")

        AfaLoggerFunc.tradeInfo("***��ǰ��ϵͳ: ͬ������������ʱ�� �˳�***")
    except Exception, e:
        AfaDBFunc.RollbackSql()
        AfaFlowControl.exitMainFlow( str(e) )
        sys.exit(-1)
