# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   004201_8430.py
#   ����˵��:   [8430--6000112]�±���������
#   �޸�ʱ��:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('�����ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    try:
        if( TradeContext.errorCode == '0000' ):
            TradeContext.errorMsg = '���׳ɹ�'
        else:
            if( long(TradeContext.errorCode) < 0 ):
                TradeContext.errorMsg = '�������ͨѶʧ��'
                return False
            else:
                #��Ӧ��ת��
                #return (AfaFunc.GetRespMsg( TradeContext.errorCode,TradeContext.sysId ))
                return True
        AfaLoggerFunc.tradeInfo('�˳���ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))