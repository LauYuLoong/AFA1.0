# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TAHJF002_8627.py
#   ����˵��:   ���ս��������
#   �޸�ʱ��:   2011��01-20
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,HostContext
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    AfaLoggerFunc.tradeInfo( '��ʼ�����ս������ױ���,������afa_maintransdel��note�ֶ���' )
    #note1���������������
    TradeContext.note1 = TradeContext.finiceCode
    #�û��ű��洦����������
    TradeContext.userno = TradeContext.punishNo
    #note3����ɿ����
    TradeContext.note3 = TradeContext.posNo
    #note4���淣����
    TradeContext.note4 = TradeContext.punishAmt
    #note5�������ɽ�
    TradeContext.note5 = TradeContext.forfeit
    #note6���渶��������
    TradeContext.note6 = TradeContext.payBank
    #note7����ɷ�����
    TradeContext.note7 = TradeContext.paymDate
    #�ɿ�������
    TradeContext.username = TradeContext.payName
    
    #����̩20110412�޸ģ��ɷѽ���Ϊ0.00
    #����ɷѽ����0.00�����ýɷ�
    if not( TradeContext.existVariable( "amount" ) and len(TradeContext.amount.strip()) > 0):
        TradeContext.errorCode,TradeContext.errorMsg = 'E0001', "�ɷѽ�����"
        raise AfaFlowControl.flowException( )
    else:
        AfaLoggerFunc.tradeInfo("�ɷѽ�" + TradeContext.amount )
        if TradeContext.amount.strip( ) == "0.00":
            TradeContext.errorCode,TradeContext.errorMsg = 'E0001', "�ɷѽ���Ϊ��"
            raise AfaFlowControl.flowException( )
    
    #paymethod1���ѷ�ʽ(0�ֽ�1ת��)  accType�ɷѽ��ʴ��루000:�ֽ�001����˽�˺ţ�002����ǿ���
    #003�����ǿ���004���Թ��˺ţ�005�����񿨣�  payacc�˺�  paycard����
    TradeContext.accType = ''
    
    if TradeContext.paymethod1=="0":
        TradeContext.accType="000"
        AfaLoggerFunc.tradeInfo('�ֽ�ɷ�')
    else:
        TradeContext.accno = TradeContext.payacc                           #�˺�
        AfaLoggerFunc.tradeInfo("�ɷ��˺ţ�" + TradeContext.payacc)
        if TradeContext.falg == "0":                                       #vouchtype 49���洢����
            TradeContext.accType="001"
        elif TradeContext.falg == "1":                                     #vouchtype 81����ũ��ǿ�
            TradeContext.accType="002"
     
        #paytype֧��������0ƾ���룬1ƾ֤����2ƾ���ۣ�vouchnoƾ֤����  tbr_idno���֤����
        if TradeContext.paytype == '0':                                    
            TradeContext.accPwd = TradeContext.password                    #ƾ����
            TradeContext.vouhType = TradeContext.vouchno[:2]               #ƾ֤����
            TradeContext.vouhNo = TradeContext.vouchno[2:]                 #ƾ֤����
        elif TradeContext.paytype == '1':                                  #ƾ֤��
            TradeContext.idType = TradeContext.zjtype                      #֤������
            TradeContext.idno = TradeContext.zjno                          #֤������
            TradeContext.vouhType = TradeContext.vouchno[:2]               #ƾ֤���� 
            TradeContext.vouhNo = TradeContext.vouchno[2:]                 #ƾ֤����
        elif TradeContext.paytype == "2":                                  #ƾ����
            TradeContext.vouhType = TradeContext.vouchno[:2]               #ƾ֤���� 
            TradeContext.vouhNo = TradeContext.vouchno[2:]                 #ƾ֤����
            
    return True

def SubModuleDoSnd( ):
    return True

def SubModuleDoTrd( ):
    
    AfaLoggerFunc.tradeInfo('����ɷѽ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    
    names = Party3Context.getNames( )
   
    for name in names:
        value = getattr( Party3Context, name )
        if ( not name.startswith( '__' ) and type(value) is StringType or type(value) is ListType) :
            setattr( TradeContext,name, value )
    
    if( TradeContext.errorCode == '0000' ):
        TradeContext.errorMsg = '���׳ɹ�'
    else:
        AfaLoggerFunc.tradeInfo('�����������ʧ��')
        return False

    AfaLoggerFunc.tradeInfo('�˳��ɷѽ����������ͨѶ����' )
    
    return True


