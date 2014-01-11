# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   004202_8202.py
#   ����˵��:   [8431--8000113]���ڽɷ�
#   �޸�ʱ��:   2010��08-14
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,HostContext,AfaYbtdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '��ʼ�����ڽɷѽ��ױ���' )
    


    
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    
    #����ɷѽ����0.00�����ýɷ�
    if not( TradeContext.existVariable( "amount" ) and len(TradeContext.amount.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷѽ�����"
        raise AfaFlowControl.flowException( )
    else:
        AfaLoggerFunc.tradeInfo("�ɷѽ�" + TradeContext.amount )
        if TradeContext.amount.strip( ) == "0.00":
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷѽ���Ϊ��"
            raise AfaFlowControl.flowException( )

    #���չ�˾����
    if not( TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ڱ��չ�˾����"
        raise AfaFlowControl.flowException( )
       
    #Ͷ������
    if not( TradeContext.existVariable( "policy" ) and len(TradeContext.policy.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "���յ��Ų�����"
        raise AfaFlowControl.flowException( )  
   
    #�ɷѷ�ʽ
    if not( TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷѷ�ʽ������"
        raise AfaFlowControl.flowException( )   
    
    #Ͷ��������
    if not( TradeContext.existVariable( "tbr_name" ) and len(TradeContext.tbr_name.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ��������������"
        raise AfaFlowControl.flowException( )
    
    #�ɷ��ڴ�
    if not( TradeContext.existVariable( "rev_frequ" ) and len(TradeContext.rev_frequ.strip()) > 0):
        TradeContext.rev_frequ = ''
    
    #Ӧ������
    if not( TradeContext.existVariable( "rev_date" ) and len(TradeContext.rev_date.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ӧ�����ڲ�����"
        raise AfaFlowControl.flowException( )   
    
    #paymethod1���ѷ�ʽ(0�ֽ�1ת��)  accType�ɷѽ��ʴ��루000:�ֽ�001����˽�˺ţ�002����ǿ���
    #003�����ǿ���004���Թ��˺ţ�005�����񿨣�  payacc�˺�  paycard����
    TradeContext.accType = ''
    
    if TradeContext.paymethod1=="0":
        TradeContext.accType="000"
    else:
        if TradeContext.vouchtype == "49":                                 #vouchtype 49:�洢�˻�
            TradeContext.accType="001"
            TradeContext.accno = TradeContext.payacc                       #�˺�
        
        elif TradeContext.vouchtype == "81":                               #vouchtype 81:��ũ��ǿ�       
            TradeContext.accType="002"
            TradeContext.accno = TradeContext.paycard                      #����
        
        #paytype֧��������0ƾ���룬1ƾ֤����2ƾ���ۣ�vouchnoƾ֤����  tbr_idnoͶ�������֤����
        if TradeContext.paytype == '0':                                    #ƾ����
            TradeContext.accPwd = TradeContext.password 
            TradeContext.vouhType = TradeContext.vouchtype                 #ƾ֤����
            if(TradeContext.vouchtype == "81"):
                TradeContext.vouhNo=TradeContext.paycard[8:18] 
            else:
                TradeContext.vouhNo = TradeContext.vouchno                 #ƾ֤����
        
        elif TradeContext.paytype == '1':                                  #ƾ֤��
            TradeContext.idType = TradeContext.zjtype                      #֤������
            TradeContext.idno = TradeContext.zjno                          #֤������
            TradeContext.vouhType = TradeContext.vouchtype                 #ƾ֤���� 
            TradeContext.vouhNo = TradeContext.vouchno                     #ƾ֤����
        
        elif TradeContext.paytype == "2":                                  #ƾ����
            TradeContext.vouhType = TradeContext.vouchtype                 #ƾ֤���� 
            TradeContext.vouhNo = TradeContext.vouchno                     #ƾ֤����
   
    return True

def SubModuleDoSnd( ):
    return True

def SubModuleDoTrd( ):
    AfaLoggerFunc.tradeInfo('�������ڽɷѽ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    
    names = Party3Context.getNames( )
    
    for name in names:
        value = getattr( Party3Context, name )
        if ( not name.startswith( '__' ) and type(value) is StringType) :
            setattr( TradeContext, name, value )
    
    if( TradeContext.errorCode == '0000' ):
        TradeContext.errorMsg = '���׳ɹ�'
        
        if not AfaYbtdb.ADBUpdateTransdtl( ):                              #�ɷѳɹ����������ˮ���note�ֶ�ֵ   
           return False
    else:
        AfaLoggerFunc.tradeInfo('�����������ʧ��')
        return False

   
    AfaLoggerFunc.tradeInfo('�˳����ڽɷѽ����������ͨѶ����' )
    return True
        


