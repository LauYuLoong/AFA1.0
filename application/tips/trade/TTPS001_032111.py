# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.���˻�ִ����
#   ����������������˻�ִ���׵�����
#=================================================================
#   �����ļ�:   003001_032111.py
#   �޸�ʱ��:   2007-5-28 10:28
##################################################################
import TradeContext, AfaLoggerFunc, TipsFunc,AfaAfeFunc
from types import *

def SubModuleMainFst( ):
    TradeContext.TransCode='2111'
    AfaLoggerFunc.tradeInfo('��˰����_���˻�ִ����_ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:

        #=============��ȡƽ̨��ˮ��====================
        if TipsFunc.GetSerialno( ) == -1 :
            AfaLoggerFunc.tradeInfo('>>>������:��ȡƽ̨��ˮ���쳣' )
            return TipsFunc.ExitThisFlow( 'A0027', '��ȡ��ˮ��ʧ��' )

        #=============�������ͨѶ====================
        AfaAfeFunc.CommAfe()
                
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='���׳ɹ�'
        AfaLoggerFunc.tradeInfo('��˰����_���˻�ִ����_ǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
