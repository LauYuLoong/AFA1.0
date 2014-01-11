# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   YBT001_8614.py
#   ����˵��:   ���յ�֤�ش�
#   �޸�ʱ��:   2010-08-03
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc,AfaAhAdb,YbtFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #У�鱣�չ�˾�����ƾ֤�����Ƿ�Ϸ�
    if not AfaAhAdb.ADBCheckCert( ):
        return False
    
    AfaLoggerFunc.tradeInfo( '��ʼ����֤�ش��ױ���' )
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    
    try:
        #��ѯԭ�ɷѼ�¼�Ƿ����
        sql = ""
        sql = "select note9,amount,bankserno,agentserialno,tellerno,brno,draccno from afa_maintransdtl where agentserialno = '"+TradeContext.PreSerialno+"'"
        sql = sql + " and userno = '" + TradeContext.userno + "' and workdate = '" + TradeContext.workDate + "'"
        sql = sql + " and bankstatus = '0' and corpstatus = '0' and revtranf = '0'"
        
        AfaLoggerFunc.tradeInfo('���յ�֤�ش��ѯ���'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
         
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ����ͨ���ݿ�ʧ��"
            raise AfaFlowControl.flowException( )
        
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽��ף������ش�ӡ"
            return False
        
        else:
            AfaLoggerFunc.tradeDebug("records=" + str(records))
            
        if(records[0][4] != TradeContext.tellerno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ���Ա�������������˽���"
            return False
        
        if(records[0][5] != TradeContext.brno):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ������������������˽���"
            return False
              
        if (TradeContext.policy!=records[0][0].split('|')[2].strip()):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","���յ��Ų���������������"
            return False
            
        if (TradeContext.premium!=records[0][1].strip()):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","���׽���������������"
            return False
        #Ͷ������
        TradeContext.applno = records[0][0].split('|')[1].strip()    
        #amount : "�ɷѽ��"
        TradeContext.amount  = records[0][1].strip()
        
        #bankserno : "������Ա��ˮ��"
        TradeContext.hostserialno = records[0][2].strip()
        
        #agentSerialno: "�м�ҵ����ˮ��"
        TradeContext.agentserialno = records[0][3].strip()
        
        #draccno : ת���˺�
        TradeContext.payacc = records[0][6].strip()
    
        return True        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
    
   

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('���뵥֤�ش���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨ�ź���' )
    
    try:
        names = Party3Context.getNames( )
       
        for name in names:
            value = getattr( Party3Context, name )
            if ( not name.startswith( '__' ) and type(value) is StringType or type(value) is ListType) :
                setattr( TradeContext, name, value )
            
        if(TradeContext.errorCode=='0000'):
            #���������سɹ������ԭ����ӡˢ��
            update_sql = "update afa_maintransdtl set "                                             
            update_sql = update_sql + " userno            = '" + TradeContext.userno1     + "'"       #user1�±���ӡˢ��
            update_sql = update_sql + " where userno      = '" + TradeContext.userno      + "'"       #userԭ����ӡˢ�� 
            update_sql = update_sql + " and workdate      = '" + TradeContext.workDate    + "'"       #����  
            update_sql = update_sql + " and agentserialno = '" + TradeContext.PreSerialno + "'"       #�ɷѳɹ����м�ҵ����ˮ��
            
            #���²��ύ����
            if  AfaDBFunc.UpdateSqlCmt(update_sql)<0:
                return AfaFlowControl.ExitThisFlow("A999","����Ͷ������ʧ��")
                
            #���������سɹ��������ֽ��ֵ�ļ�
            if not YbtFunc.createFile( ):
                return False

        AfaLoggerFunc.tradeInfo('�˳���֤�ش�[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
        return True
    
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
