# -*- coding: gbk -*-
##################################################################
#   ��˰����.����״̬��ѯ
#=================================================================
#   �����ļ�:   T3001_8460.py
#   �޸�ʱ��:   2007-7-2 15:03
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,AfaFlowControl
import TipsFunc,AfaAfeFunc
from types import *

def SubModuleMainFst( ):

    AfaLoggerFunc.tradeInfo( '���뽻��״̬��ѯ[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============��ȡƽ̨��ˮ��====================
        if TipsFunc.GetSerialno( ) == -1 :
            WrtLog('>>>������:��ȡƽ̨��ˮ���쳣' )
            sys.exit()
        
        #=============�������ͨѶ====================
        AfaAfeFunc.CommAfe()
        if( TradeContext.errorCode != '0000' ):
            return False
        AfaLoggerFunc.tradeInfo( '�˳�����״̬��ѯ['+TradeContext.TemplateCode+']\n' )
        return True
    except AfaFlowControl.flowException, e:
        return False
