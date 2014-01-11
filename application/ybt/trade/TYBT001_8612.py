# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYB001_8610.py
#   ����˵��:   [8610--8000112]���ڲ�ѯ
#
#   �޸�ʱ��:   2010-07-28
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '��ʼ�����ڲ�ѯ���ױ���' )
    
    #���״��루8612��
    TradeContext.tradeCode = TradeContext.TransCode
    
    #���չ�˾����
    if not( TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ڱ��չ�˾����"
        raise AfaFlowControl.flowException( ) 
   
    #���յ���
    if not( TradeContext.existVariable( "policy" ) and len(TradeContext.policy.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ڱ��յ���"
        raise AfaFlowControl.flowException( )
   
    return True

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('�������ڲ�ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    
    try:
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
          
        if(TradeContext.errorCode=='0000'):
            TradeContext.errorMsg="���ڲ�ѯ�ɹ�"
        
        
        #TradeContext.syr_name1 = ''
        #syr_name = []
        #if TradeContext.existVariable('syr_name1'):
        #    syr_name.append('xiaozhang')
        #    syr_name.append('xig')
        TradeContext.O1ACUR = '1'
        #    TradeContext.syr_name = syr_name 
     
        AfaLoggerFunc.tradeInfo('�˳����ڲ�ѯ�����������ͨѶ����' )    
        return True
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
