# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��˰����.���Ӳ���
#=================================================================
#   �����ļ�:   T3001_8462.py
#   �޸�ʱ��:   2007-10-18 
##################################################################

import TradeContext, AfaLoggerFunc
import AfaAfeFunc,TipsFunc
#LoggerHandler, UtilTools, os, 

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('==========��ʼ��˰����.���Ӳ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']==========')
    #=============��ȡƽ̨��ˮ��====================
    if TipsFunc.GetSerialno( ) == -1 :
        raise TipsFunc.flowException( )
    
    #=============�������ͨѶ====================
    AfaAfeFunc.CommAfe()
    AfaLoggerFunc.tradeInfo('>>>���Ӳ��Խ��:['+TradeContext.errorCode+']'+TradeContext.errorMsg )
    if( TradeContext.errorCode != '0000' ):
        return False
        
    AfaLoggerFunc.tradeInfo('==========�˳���˰����.���Ӳ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']==========')
    return True
 
def SubModuleMainSnd ():
    return True