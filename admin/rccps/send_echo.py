# -*- coding: gbk -*-
###################################################################
#    ũ����ϵͳ.echo���ķ���
#==================================================================
#    �����ļ���  send_echo.py
#    �޸�ʱ�䣺  2008-6-8
#    ��    �ߣ�  ������
#==================================================================
#    �޸�ʱ�䣺
#    �޸���  ��
#==================================================================
#    ��    �ܣ�  ��AFE��������echo����
###################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
import rccpsCronFunc,AfaAfeFunc
import sys, time

from types import *
from rccpsConst import *

if __name__ == '__main__':
    
    try:
        rccpsCronFunc.WrtLog("***ũ����ϵͳ: ����echo���ķ��� ����***")

        #=====��ʼƴ����echo����====
        TradeContext.MSGTYPCO    = 'SET000'
        TradeContext.TransCode   = '9900516'
        TradeContext.TRCCO    = '9900516'
        TradeContext.IPADDR   = '0'
        TradeContext.PORT     = '0'
        TradeContext.LNKNO    = '1'
        TradeContext.ECHINFNO = '1'
        TradeContext.BRSFLG   = '0'
        #====ƴģ������====
        TradeContext.TemplateCode = 'RCC007'
        TradeContext.sysId = 'RCC01'

        #====��afe����ͨѶ====
        AfaAfeFunc.CommAfe()

        rccpsCronFunc.WrtLog("***ũ����ϵͳ: ����echo���ķ��� �˳�***")
    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
        sys.exit(-1)
