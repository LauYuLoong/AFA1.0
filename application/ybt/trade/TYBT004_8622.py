# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT004_8622.py
#   ����˵��:   �����Ӳ�ѯ
#   �޸�ʱ��:   2010-8-10
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaAhAdb
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
     
    AfaLoggerFunc.tradeInfo( '�����ױ���ֵ����Ч��У��' )
   
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    
    if( not TradeContext.existVariable( "PreSerialno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ԭ������ˮ��[PreSerialno]ֵ������!' )
   
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    
    if( TradeContext.channelCode == '005' ):
        
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������!' )
        
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '�����[brno]ֵ������!' )
        
        if( not TradeContext.existVariable( "termid" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[termid]ֵ������!' )
    
    return True
    
   
def SubModuleDoSnd( ):
   
    AfaLoggerFunc.tradeInfo('���뷴��ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' ) 
    
    try:
        sql = "select note1,note2,note3,note4,note5,note7,note8,note9,draccno,brno,tellerno,note6,unitno,amount,note9 from afa_maintransdtl "
        sql = sql + " where agentserialno = '"+TradeContext.PreSerialno+"' and workdate = '"+TradeContext.workDate+"'"
        sql = sql + " and revtranf = '0' and bankstatus = '0'  and chkflag = '9'"
        
        AfaLoggerFunc.tradeInfo('�����Ӳ�ѯ���'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        AfaLoggerFunc.tradeInfo('�����Ӳ�ѯ����¼'+str(records))
        
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ����ͨ���ݿ�ʧ��"
            raise AfaFlowControl.flowException( )
        
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽���"
            return False
      
        else:
        
            if(records[0][10] != TradeContext.tellerno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ���Ա�������������˽���"
                return False
        
            if(records[0][9] != TradeContext.brno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ������������������˽���"
                return False
            
            if(records[0][12].strip() != TradeContext.insuid):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","���չ�˾ѡ������"
                return False
            
            if(records[0][13].strip() != TradeContext.amount.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��������ԭ������������¼����"
                return False
            
            if(records[0][14].split('|')[2] != TradeContext.policy.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ�����Ų��������鱣����¼����"
                return False
            
            #Ͷ��������
            TradeContext.tbr_name=records[0][3].split('|')[0]
            
            #Ͷ����֤����
            TradeContext.tbr_idno=records[0][3].split('|')[1]
            
            #������������
            TradeContext.bbr_name=records[0][4].split('|')[0]
            
            #��������֤����
            TradeContext.bbr_idno=records[0][4].split('|')[1]
            
            #��������
            TradeContext.productid=records[0][6].split('|')[0]
            
            #����������
            TradeContext.productid1=records[0][6].split('|')[2]
            
            #Ͷ������
            TradeContext.amt_unit =records[0][7].split('|')[0]
            
            #�˺�
            TradeContext.payacc=records[0][8]
            
            #�˿ʽ
            TradeContext.paymethod1=records[0][11].split('|')[1]
            
            #�ɷ�����
            TradeContext.paytimelimit=records[0][5].split('|')[2]
            
            #�ɷѷ�ʽ
            TradeContext.paymethod=records[0][5].split('|')[0]
            
            #�ɷ��ڴ�
            TradeContext.rev_frequ=records[0][5].split('|')[1]
            
            #������1��Ϣ
            TradeContext.syr_1=""
            #������2��Ϣ
            TradeContext.syr_2=""
            #������3��Ϣ
            TradeContext.syr_3=""
            #������4��Ϣ
            TradeContext.syr_4=""
            #������5��Ϣ
            TradeContext.syr_5=""
            
            TradeContext.errorCode= "0000" 
            
            AfaLoggerFunc.tradeInfo('�˳�����ѯ����' )
            return True                               
    except Exception, e:                          
        AfaFlowControl.exitMainFlow(str(e))       
