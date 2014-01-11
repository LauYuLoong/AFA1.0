# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TTJYW001_8495.py
#   ����˵��:   ͳ��ҵ��ɷѽ���
#   �޸�ʱ��:   2011-01-05
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaFlowControl,HostContext,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    try:
        AfaLoggerFunc.tradeInfo( '>>>>>>>>>>>>>>��ʼ��ͳ��ҵ��Ľ��ױ�����ʼ' )
        
        #�ɷ�������
        if not( TradeContext.existVariable( "userName" ) and len(TradeContext.userName.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷ�������������"
            raise AfaFlowControl.flowException( )
       
        #��ϵ�绰
        if not( TradeContext.existVariable( "note1" ) and len(TradeContext.note1.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��ϵ�绰������"
            raise AfaFlowControl.flowException( )   
        
        #���׻�������                                                                                 
        if not( TradeContext.existVariable( "note3" ) and len(TradeContext.note3.strip()) > 0 ):   
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "���׻������Ʋ�����"               
            raise AfaFlowControl.flowException( )                                                 
            
        #�ɷѷ�ʽ
        if not( TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷѷ�ʽ������"
            raise AfaFlowControl.flowException( )   
            
        #20120709�º���� ��λ���� busino    
        #��λ����
        if not( TradeContext.existVariable( "busino" ) and len(TradeContext.busino.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��λ���벻����"
            raise AfaFlowControl.flowException( )               
            
        TradeContext.note2   =   TradeContext.busino      #��busino����note2 ��
            
        
        #paymethod1���ѷ�ʽ(0�ֽ�1ת��)  accType�ɷѽ��ʴ��루000:�ֽ�001����˽�˺ţ�002����ǿ���
        #003�����ǿ���004���Թ��˺ţ�005�����񿨣�  paycard����
        TradeContext.accType = ''
        
        if TradeContext.paymethod=="0":
            TradeContext.accType="000"
        else:
            TradeContext.vouhType = "81"                            #vouhType 81����ũ��ǿ�
            TradeContext.accType="002"
            TradeContext.accno = TradeContext.paycard               #����
            TradeContext.accPwd = TradeContext.password
            TradeContext.vouhNo=TradeContext.paycard[8:18]
        
        #20120706�º��޸ģ������տ����޸�Ϊ�ʻ�����
        #begin   
        #sql = "select unitname from afa_unitadm"              
        #sql = sql + " where sysid     = '" + TradeContext.sysId.strip() + "'"
        #sql = sql + " and   unitno    = '" + TradeContext.unitno.strip() + "'"     
        #                                                                            
        #AfaLoggerFunc.tradeInfo('�տ�����Ϣ��ѯ���'+ sql)                          
        #                                                                            
        #records = AfaDBFunc.SelectSql( sql )                                        
        #if records == None:                                                         
        #    TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ�ʧ��" 
        #    raise AfaFlowControl.flowException( )                                   
        #                                                                            
        #if(len(records) < 1):                                                       
        #    TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴���Ϣ"        
        #    raise AfaFlowControl.flowException( )                                                             
        #                                                                            
        #else:                                                                       
        #    TradeContext.unitname = records[0][0]             #�տ���  
        
        sql = ""
        sql = sql + " select businame,accno from abdt_unitinfo "
        sql = sql + " where appno = '" + TradeContext.sysId.strip()  + "' "
        sql = sql + " and  busino = '" + TradeContext.busino.strip() + "' "
        
        AfaLoggerFunc.tradeInfo('�տ����ʻ�������Ϣ��ѯ���'+ sql)                          
                                                                                    
        records = AfaDBFunc.SelectSql( sql )                                        
        if records == None:                                                         
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ�ʧ��" 
            raise AfaFlowControl.flowException( )                                   
                                                                                    
        if(len(records) < 1):                                                       
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�õ�λû��ǩԼ����������ҵ��"        
            raise AfaFlowControl.flowException( )                                                             
                                                                                    
        else:                                                                       
            TradeContext.businame       = records[0][0]             #�տ����ʻ����� 
            TradeContext.ACCNO          = records[0][1]             #�տ����ʺ�
                       
            TradeContext.__agentAccno__ = records[0][1]             #�ʺ�
            AfaLoggerFunc.tradeInfo('�տ����ʻ�__agentAccno__ AA����'+ TradeContext.__agentAccno__) 
        
        #end
                    
        AfaLoggerFunc.tradeInfo( '>>>>>>>>>>>��ʼ��ͳ��ҵ��Ľ��ױ�������' )
        return True
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
    
    

