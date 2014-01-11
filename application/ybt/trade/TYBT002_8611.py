# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT002_8611.py
#   ����˵��:   �±��ɷ�
#   �޸�ʱ��:   2010��07-29
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,HostContext,AfaYbtdb,YbtFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    
    #У�鱣�չ�˾�����ƾ֤�����Ƿ�Ϸ�
    if not AfaYbtdb.ADBCheckCert( ):
        return False
   
    
    try:
        AfaLoggerFunc.tradeInfo( '��ʼ���±��ɷѽ��ױ���' )
        
        #���״��루8611��
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
        if not( TradeContext.existVariable( "applno" ) and len(TradeContext.applno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ�����Ų�����"
            raise AfaFlowControl.flowException( )   
        
        #����ӡˢ��
        if not( TradeContext.existVariable( "userno" ) and len(TradeContext.userno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "����ӡˢ�Ų�����"
            raise AfaFlowControl.flowException( )  
        
        #�±�Ͷ�����˱�����ˮ��
        if not( TradeContext.existVariable( "PreSerialno"  ) and len(TradeContext.PreSerialno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�±�Ͷ�����˱�����ˮ�Ų�����"
            raise AfaFlowControl.flowException( )  
        
        #������
        if not( TradeContext.existVariable( "productid" ) and len(TradeContext.productid.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "���ֲ�����"
            raise AfaFlowControl.flowException( )
        
        #�ɷѷ�ʽ
        if not( TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷѷ�ʽ������"
            raise AfaFlowControl.flowException( )   
        
        #�ɷ�����
        if not( TradeContext.existVariable( "paydatelimit" ) and len(TradeContext.paydatelimit.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷ����޲�����"
            raise AfaFlowControl.flowException( )  
        
        #Ͷ��������
        if not( TradeContext.existVariable( "tbr_name" ) and len(TradeContext.tbr_name.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ��������������"
            raise AfaFlowControl.flowException( )
        
        #Ͷ����֤������
        if not( TradeContext.existVariable( "tbr_idno" ) and len(TradeContext.tbr_idno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ����֤�����벻����"
            raise AfaFlowControl.flowException( )
        
        #������������
        if not( TradeContext.existVariable( "bbr_name" ) and len(TradeContext.bbr_name.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "������������������"
            raise AfaFlowControl.flowException( )  
        
        #��������֤������
        if not( TradeContext.existVariable( "bbr_idno" ) and len(TradeContext.bbr_idno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�������˺���֤��������"
            raise AfaFlowControl.flowException( )  
        
        #��Ͷ���˹�ϵ
        if not( TradeContext.existVariable( "tbr_bbr_rela" ) and len(TradeContext.tbr_bbr_rela.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��Ͷ���˹�ϵ������"
            raise AfaFlowControl.flowException( )  
       
        #����Ӫ����Ա����
        if not( TradeContext.existVariable( "salerno" ) and len(TradeContext.salerno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "����Ӫ����Ա���Ų�����"
            raise AfaFlowControl.flowException( )  
        
        #paymethod1���ѷ�ʽ(0�ֽ�1ת��)  accType�ɷѽ��ʴ��루000:�ֽ�001����˽�˺ţ�002����ǿ���
        #003�����ǿ���004���Թ��˺ţ�005�����񿨣�  payacc�˺�  paycard����
        TradeContext.accType = ''
        
        if TradeContext.paymethod1=="0":
            TradeContext.accType="000"
       
        else:
            if TradeContext.vouchtype == "49":                                 #vouchtype 49���洢����
                TradeContext.accType="001"
                TradeContext.accno = TradeContext.payacc                       #�˺�
            
            elif TradeContext.vouchtype == "81":                               #vouchtype 81����ũ��ǿ�
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
            AfaLoggerFunc.tradeInfo("TradeContext.vouhNo:"+TradeContext.vouhNo)
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
    
    #����ɷѽ��ʴ���
    AfaLoggerFunc.tradeDebug("TradeContext.accType = [" + TradeContext.accType + "]")
    return True

def SubModuleDoSnd( ):
    return True

def SubModuleDoTrd( ):
    
    AfaLoggerFunc.tradeInfo('����ɷѽ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    
    names = Party3Context.getNames( )
   
    for name in names:
        value = getattr( Party3Context, name )
        #AfaLoggerFunc.tradeInfo(str(name) + ":" + str(value))
        if ( not name.startswith( '__' ) and type(value) is StringType or type(value) is ListType) :
            setattr( TradeContext,name, value )
        #    AfaLoggerFunc.tradeInfo(name + ":" + value)
    
    if( TradeContext.errorCode == '0000' ):
        TradeContext.errorMsg = '���׳ɹ�'
        
        #���������سɹ��������ֽ��ֵ�ļ�
        if not YbtFunc.createFile( ):
            return False
          
        #���������سɹ����������ˮ���note�ֶ�
        if not AfaYbtdb.ADBUpdateTransdtl( ):
            return False
        
    else:
        AfaLoggerFunc.tradeInfo('�����������ʧ��')
        return False

    AfaLoggerFunc.tradeInfo('�˳��ɷѽ����������ͨѶ����' )
    
    return True


