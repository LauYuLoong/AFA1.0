# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TAHJF001_8626.py
#   ����˵��:   �����ֹ�¼�봦���������ѯ���׽���
#
#   �޸�ʱ��:   2011-01-20
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '��ʼ���ֹ�¼�봦���������ѯ���ױ���' )
    
    #���״��루8626��
    TradeContext.tradeCode = TradeContext.TransCode
    TradeContext.paymDate = AfaUtilTools.GetSysDate( )
    #������������
    if not( TradeContext.existVariable( "punishNo" ) and len(TradeContext.punishNo.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����������Ų�����"
        raise AfaFlowControl.flowException( ) 
   
    #�ɷ�����
    if not( TradeContext.existVariable( "paymDate" ) and len(TradeContext.paymDate.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷ����ڲ�����"
        raise AfaFlowControl.flowException( ) 
        
    #����ʱ��
    if not( TradeContext.existVariable( "punishDate" ) and len(TradeContext.punishDate.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "����ʱ�䲻����"
        raise AfaFlowControl.flowException( )     
    
    #Υ����Ϊ���� 
    if not( TradeContext.existVariable( "punishCode" ) and len(TradeContext.punishCode.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Υ����Ϊ���벻����"
        raise AfaFlowControl.flowException( )    
        
    #��ʻ֤���
    if not( TradeContext.existVariable( "driversNo" ) and len(TradeContext.driversNo.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��ʻ֤��Ų�����"
        raise AfaFlowControl.flowException( )  
     
    #������
    if not( TradeContext.existVariable( "username" ) and len(TradeContext.username.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����˲�����"
        raise AfaFlowControl.flowException( )  
    
    #Υ�����    
    if not( TradeContext.existVariable( "punishAmt" ) and len(TradeContext.punishAmt.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Υ�������� "
        raise AfaFlowControl.flowException( )   
                  
    #�жϷ������Ƿ��ڷ����������֮��
    #try:
    #    sql = "select lower_amount,top_amount  from ahjf_lawcode where lawactioncode = '"+ TradeContext.punishCode +"'" 
    #    
    #    AfaLoggerFunc.tradeInfo( '��ѯahjf_lawcode���sql��'+ sql )
    #    records = AfaDBFunc.SelectSql( sql )
    #    if records == None:
    #        TradeContext.errorCode,TradeContext.errorMsg = "0001","��ѯ����ʧ��"
    #        raise AfaFlowControl.flowException( )
    #    elif(len(records) < 1):
    #        TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˼�¼"
    #        raise AfaFlowControl.flowException( )
    #    else:
    #        minAmt   = float(records[0][0])
    #        maxAmt   = float(records[0][1])
    #        inputAmt = float(TradeContext.punishAmt)
    #        if minAmt > inputAmt or inputAmt  >  maxAmt :
    #            TradeContext.errorCode,TradeContext.errorMsg = "0001","����Ľ��ڷ���ķ�Χ֮�ڣ�����������"
    #            raise AfaFlowControl.flowException( )
    #except  Exception, e:                     
    #    AfaLoggerFunc.tradeInfo( str(e) )     
    #    return AfaFlowControl.ExitThisFlow( "E0001", str(e) )         
    return True

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('���밲���ֹ�¼�봦���������ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    
    try:
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
          
        if(TradeContext.errorCode=='0000'):
            TradeContext.errorMsg="�ֹ�¼�봦���������ѯ���׳ɹ�"
        
        AfaLoggerFunc.tradeInfo('�����ֹ�¼�봦���������ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )    
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return AfaFlowControl.exitMainFlow( "E0001",str(e) )
