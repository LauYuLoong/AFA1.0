
# -*- coding: gbk -*-
##################################################################
#   ��˰����.�����ӡ
#=================================================================
#   �����ļ�:   TTPS001_8491.py
#   �޸�ʱ��:   2007-7-2 15:03
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,AfaFlowControl
#import TipsFunc,AfaAfeFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '���뱨���ӡ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    TradeContext.appNo      ='AG2010'
    TradeContext.busiNo  ='00000000000001'
    sbrno=TradeContext.brno
    try:
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        TradeContext.errorCode = '0000'
        TradeContext.errorCode = '����Ӧ�Ĵ�ӡ��ϸ'

        AfaLoggerFunc.tradeInfo( '�˳������ӡ['+TradeContext.TemplateCode+']\n' )
        return True
    except AfaFlowControl.flowException, e:
        return False
