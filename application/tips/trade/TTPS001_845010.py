# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.ǿ���˳������з���
#=================================================================
#   �����ļ�:   TTPS001_845010.py
#   �޸�ʱ��:   2007-5-28 10:28
##################################################################
import TradeContext, AfaLoggerFunc,TipsFunc
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('ǿ���˳�����ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #ǩ��
        if (not TipsFunc.UpdAppStatus('0')):
            raise TipsFunc.flowException( )
        
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '���׳ɹ�' 
        AfaLoggerFunc.tradeInfo('ǿ���˳�ǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        return TipsFunc.exitMainFlow(str(e))
