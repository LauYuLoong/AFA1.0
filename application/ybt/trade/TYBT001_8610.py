# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT001_8610.py
#   ����˵��:   �±�Ͷ��
#
#   �޸�ʱ��:   2010-07-28
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaYbtdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #У�鱣�չ�˾�����ƾ֤�����Ƿ�Ϸ�
    if not AfaYbtdb.ADBCheckCert( ):
        return False
        
    try:
        AfaLoggerFunc.tradeInfo( '��ʼ���±�Ͷ�����ױ���' )
        
        #���״��루8610��
        TradeContext.tradeCode = TradeContext.TransCode
        
        #���չ�˾����
        if not( TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ڱ��չ�˾����"
            raise AfaFlowControl.flowException( )
            
        #����
        if not( TradeContext.existVariable( "productid" ) and len(TradeContext.productid.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "���ֲ�����"
            raise AfaFlowControl.flowException( )
            
        #Ͷ��������
        if not( TradeContext.existVariable( "tbr_name" ) and len(TradeContext.tbr_name.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ��������������"
            raise AfaFlowControl.flowException( )
            
        #Ͷ����֤������
        if not( TradeContext.existVariable( "tbr_idtype" ) and len(TradeContext.tbr_idtype.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ����֤�����Ͳ�����"
            raise AfaFlowControl.flowException( )
            
        #Ͷ����֤������
        if not( TradeContext.existVariable( "tbr_idno" ) and len(TradeContext.tbr_idno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ����֤�����벻����"
            raise AfaFlowControl.flowException( )
            
        #Ͷ�����Ա�
        if not( TradeContext.existVariable( "tbr_sex" ) and len(TradeContext.tbr_sex.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ�����Ա𲻴���"
            raise AfaFlowControl.flowException( )
            
        #Ͷ���˳�������
        if not( TradeContext.existVariable( "tbr_birth" ) and len(TradeContext.tbr_birth.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ���˳������ڲ�����"
            raise AfaFlowControl.flowException( )
            
        #Ͷ���˼�ͥ��ַ    
        if not( TradeContext.existVariable( "tbr_addr" ) and len(TradeContext.tbr_addr.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ���˼�ͥ��ַ������"
            raise AfaFlowControl.flowException( )
            
        #Ͷ���˼�ͥ���� Ͷ�����ƶ�����
        if not( TradeContext.existVariable( "tbr_tel" )  or TradeContext.existVariable( "tbr_mobile" ) ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ���˵绰������"
            raise AfaFlowControl.flowException( )
            
        #Ͷ������������
        if not( TradeContext.existVariable( "tbr_postcode" ) and len(TradeContext.tbr_postcode.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ�����������벻����"
            raise AfaFlowControl.flowException( )
              
        #Ͷ������
        if not( TradeContext.existVariable( "applno" ) and len(TradeContext.applno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ�����Ų�����"
            raise AfaFlowControl.flowException( ) 
             
        #����ӡˢ��
        if not( TradeContext.existVariable( "userno" ) and len(TradeContext.userno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "����ӡˢ�Ų�����"
            raise AfaFlowControl.flowException( )
              
        #Ͷ������
        if not( TradeContext.existVariable( "tb_date" ) and len(TradeContext.tb_date.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ͷ�����ڲ�����"
            raise AfaFlowControl.flowException( )  
       
        #Ӧ�ɱ���
        if not( TradeContext.existVariable( "amount" ) and len(TradeContext.amount.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "Ӧ�ɱ��Ѳ�����"
            raise AfaFlowControl.flowException( ) 
             
        #�����ڼ�����
        if not( TradeContext.existVariable( "tormtype" ) and len(TradeContext.tormtype.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ڼ����Ͳ�����"
            raise AfaFlowControl.flowException( )
              
        #�����ڼ�
        if not( TradeContext.existVariable( "coverage_year" ) and len(TradeContext.coverage_year.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ڼ䲻����"
            raise AfaFlowControl.flowException( )  
       
        #�ɷѷ�ʽ
        if ( TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
            if(TradeContext.paymethod=='1'):
                #���ɷѷ�ʽΪ1���ڽɣ�ʱ�ɷ���������Ϊ2�������޽������й����������ֶΣ�
                TradeContext.charge_period='2'                                         
            else:
                #���ɷѷ�ʽΪ5��������ʱ�ɷ���������Ϊ1��������
                TradeContext.charge_period='1'  
        
        #�ɷ�����
        if not( TradeContext.existVariable( "paydatelimit" ) and len(TradeContext.paydatelimit.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ɷ����޲�����"
            raise AfaFlowControl.flowException( )  
       
        #������������
        if not( TradeContext.existVariable( "bbr_name" ) and len(TradeContext.bbr_name.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "������������������"
            raise AfaFlowControl.flowException( )
              
        #��������֤������
        if not( TradeContext.existVariable( "bbr_idtype" ) and len(TradeContext.bbr_idtype.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��������֤�����Ͳ�����"
            raise AfaFlowControl.flowException( )  
            
        #��������֤������
        if not( TradeContext.existVariable( "bbr_idno" ) and len(TradeContext.bbr_idno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�������˺���֤��������"
            raise AfaFlowControl.flowException( ) 
             
        #���������Ա�
        if not( TradeContext.existVariable( "bbr_sex" ) and len(TradeContext.bbr_sex.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "���������Ա𲻴���"
            raise AfaFlowControl.flowException( )
              
        #�������˳�������
        if not( TradeContext.existVariable( "bbr_birth" ) and len(TradeContext.bbr_birth.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�������˳������ڲ�����"
            raise AfaFlowControl.flowException( )
            
        #��������ְҵ
        if not( TradeContext.existVariable( "bbr_worktype" ) and len(TradeContext.bbr_worktype.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��������ְҵ������"
            raise AfaFlowControl.flowException( ) 
             
        #��Ͷ���˹�ϵ
        if not( TradeContext.existVariable( "tbr_bbr_rela" ) and len(TradeContext.tbr_bbr_rela.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��Ͷ���˹�ϵ������"
            raise AfaFlowControl.flowException( )  
        
        #��Ա����
        if not( TradeContext.existVariable( "tellers" ) and len(TradeContext.tellers.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��Ա���Ų�����"
            raise AfaFlowControl.flowException( )
              
        #����Ӫ����Ա����
        if not( TradeContext.existVariable( "salerno" ) and len(TradeContext.salerno.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "����Ӫ����Ա���Ų�����"
            raise AfaFlowControl.flowException( ) 
             
        #ƾ֤����
        if not( TradeContext.existVariable( "I1CETY" ) and len(TradeContext.I1CETY.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "ƾ֤���಻����"
            raise AfaFlowControl.flowException( )  
        if(TradeContext.syr_type=='1'):      
            #��ʼ����������Ϣ ,���������   
            syr_name = []
            syr_idtype = []
            syr_idno = []
            syr_sex = []
            syr_order = []
            syr_bbr_rela = []
            syr_bent_profit_pcent = []
            syr_bent_profit_base = []
            
             
            #������1��Ϣ
            if TradeContext.existVariable( "syr_1" ) :  
                if not (len(TradeContext.syr_1.strip())>0 ):
                    syr_name.append("")
                    syr_idtype.append("")
                    syr_idno.append("")
                    syr_sex.append("")
                    syr_order.append("")
                    syr_bbr_rela.append("")
                    syr_bent_profit_pcent.append("")
                    syr_bent_profit_base.append("")
                else:
                    syr1=TradeContext.syr_1.split('|')
                    #����������
                    syr_name.append(syr1[0])
                    #������֤������
                    syr_idtype.append(syr1[1])
                    #������֤������
                    syr_idno.append(syr1[2])
                    #�������Ա�
                    syr_sex.append(syr1[3])
                    #����˳��
                    syr_order.append(syr1[5])
                    #�������˹�ϵ
                    syr_bbr_rela.append(syr1[6])
                    #����ݶ���Ӳ��֣�
                    syr_bent_profit_pcent.append(syr1[7])
                    #����ݶ��ĸ���֣�
                    syr_bent_profit_base.append(syr1[8])
            
            
       
            #������2��Ϣ
            if  TradeContext.existVariable( "syr_2" ) :  
                if not (len(TradeContext.syr_2.strip())>0 ):
                    syr_name.append("")
                    syr_idtype.append("")
                    syr_idno.append("")
                    syr_sex.append("")
                    syr_order.append("")
                    syr_bbr_rela.append("")
                    syr_bent_profit_pcent.append("")
                    syr_bent_profit_base.append("")
                else:
                    syr2=TradeContext.syr_2.split('|')
                    #����������
                    syr_name.append(syr2[0])
                    #������֤������
                    syr_idtype.append(syr2[1])
                    #������֤������
                    syr_idno.append(syr2[2])
                    #�������Ա�
                    syr_sex.append(syr2[3])
                    #����˳��
                    syr_order.append(syr2[5])
                    #�������˹�ϵ
                    syr_bbr_rela.append(syr2[6])
                    #����ݶ���Ӳ��֣�
                    syr_bent_profit_pcent.append(syr2[7])
                    #����ݶ��ĸ���֣�
                    syr_bent_profit_base.append(syr2[8])
                
                
            #������3��Ϣ
            if  TradeContext.existVariable( "syr_3" ):  
                if not (len(TradeContext.syr_3.strip())>0 ): 
                    syr_name.append("")   
                    syr_idtype.append("") 
                    syr_idno.append("")  
                    syr_sex.append("")      
                    syr_order.append("")    
                    syr_bbr_rela.append("") 
                    syr_bent_profit_pcent.append("")    
                    syr_bent_profit_base.append("")     
                else:
                    syr3=TradeContext.syr_3.split('|')
                    #����������
                    syr_name.append(syr3[0])
                    #������֤������
                    syr_idtype.append(syr3[1])
                    #������֤������
                    syr_idno.append(syr3[2])
                    #�������Ա�
                    syr_sex.append(syr3[3])
                    #����˳��
                    syr_order.append(syr3[5])
                    #�������˹�ϵ
                    syr_bbr_rela.append(syr3[6])
                    #����ݶ���Ӳ��֣�
                    syr_bent_profit_pcent.append(syr3[7])
                    #����ݶ��ĸ���֣�
                    syr_bent_profit_base.append(syr3[8])
                
                
            #������4��Ϣ
            if  TradeContext.existVariable( "syr_4" ):  
                if not (len(TradeContext.syr_4.strip())>0 ):   
                    syr_name.append("")                        
                    syr_idtype.append("")                      
                    syr_idno.append("")                        
                    syr_sex.append("")                         
                    syr_order.append("")                       
                    syr_bbr_rela.append("")                    
                    syr_bent_profit_pcent.append("")           
                    syr_bent_profit_base.append("")            
                else:
                    syr4=TradeContext.syr_4.split('|')
                    #����������
                    syr_name.append(syr4[0])
                    #������֤������
                    syr_idtype.append(syr4[1])
                    #������֤������
                    syr_idno.append(syr4[2])
                    #�������Ա�
                    syr_sex.append(syr4[3])
                    #����˳��
                    syr_order.append(syr4[5])
                    #�������˹�ϵ
                    syr_bbr_rela.append(syr4[6])
                    #����ݶ���Ӳ��֣�
                    syr_bent_profit_pcent.append(syr4[7])
                    #����ݶ��ĸ���֣�
                    syr_bent_profit_base.append(syr4[8]) 
                    
        
            #������5��Ϣ
            if  TradeContext.existVariable( "syr_5" ) :  
                
                if not (len(TradeContext.syr_5.strip())>0 ):   
                    syr_name.append("")                        
                    syr_idtype.append("")                      
                    syr_idno.append("")                        
                    syr_sex.append("")                         
                    syr_order.append("")                       
                    syr_bbr_rela.append("")                    
                    syr_bent_profit_pcent.append("")           
                    syr_bent_profit_base.append("")            
                else:
                    syr5=TradeContext.syr_5.split('|')
                    #����������
                    syr_name.append(syr5[0])
                    #������֤������
                    syr_idtype.append(syr5[1])
                    #������֤������
                    syr_idno.append(syr5[2])
                    #�������Ա�
                    syr_sex.append(syr5[3])
                    #����˳��
                    syr_order.append(syr5[5])
                    #�������˹�ϵ
                    syr_bbr_rela.append(syr5[6])
                    #����ݶ���Ӳ��֣�
                    syr_bent_profit_pcent.append(syr5[7])
                    #����ݶ��ĸ���֣�
                    syr_bent_profit_base.append(syr5[8])    
       
            
            TradeContext.syr_name = syr_name
            TradeContext.syr_idtype = syr_idtype
            TradeContext.syr_idno = syr_idno
            TradeContext.syr_sex = syr_sex
            TradeContext.syr_order = syr_order
            TradeContext.syr_bbr_rela = syr_bbr_rela
            TradeContext.syr_bent_profit_pcent = syr_bent_profit_pcent
            TradeContext.syr_bent_profit_base = syr_bent_profit_base
            
        
        return True 
                
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )       
   
   
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('�����ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    try:
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType) :
                setattr( TradeContext, name, value )
                #AfaLoggerFunc.tradeInfo("name:" + str(name) + "     value:" + str(value))
            
        if( TradeContext.errorCode == '0000' ):
            if not AfaYbtdb.AdbSelectQueDtl( ):                             #����Ͷ�����ź����ڲ�ѯYBT_INFO���м�¼���£��޼�¼����
                raise AfaFlowControl.flowException()
        
        AfaLoggerFunc.tradeInfo('�˳���ѯ�����������ͨѶ����' )
        return True
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
