# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TAHJF001_8625.py
#   ����˵��:   ���ս�����ѯ����
#
#   �޸�ʱ��:   2011-01-20
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '��ʼ�������������ѯ���ױ���' )
    
    #���״��루8625��
    TradeContext.tradeCode = TradeContext.TransCode
    
    #������������
    if not( TradeContext.existVariable( "punishNo" ) and len(TradeContext.punishNo.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����������Ų�����"
        raise AfaFlowControl.flowException( ) 
   
    return True

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('���밲�ս�����ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    
    try:
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
          
        if(TradeContext.errorCode=='0000'):
            TradeContext.errorMsg="���ս�����ѯ�ɹ�"
        
        AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
        AfaLoggerFunc.tradeInfo('�˳����ս�����ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )    
        return True
        
    except Exception, e:
        AfaFlowControl.ExitThisFlow( "E0001", str(e) )
