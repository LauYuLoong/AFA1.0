# -*- coding: gbk -*-
##################################################################

#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT010_8621.py
#   ����˵��:   [��֤�ش������Ӳ�ѯ]
#   �޸�ʱ��:   2010-08-11
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    
    
    AfaLoggerFunc.tradeInfo( '��֤�ش��ѯ����ֵ����Ч��У��' )
    
    if( not TradeContext.existVariable( "unitno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��λ���[unitno]ֵ������!' )
    
    if( not TradeContext.existVariable( "policy" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'Ͷ������[policy]ֵ������!' )
    
    if( not TradeContext.existVariable( "userno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ԭ����ӡˢ��[userno]ֵ������!' )
    
    if( not TradeContext.existVariable( "userno1" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�±���ӡˢ��[userno1]ֵ������!' )    
    
    if( not TradeContext.existVariable( "transrno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ԭ������ˮ��[transrno]ֵ������!' ) 
    
    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ԭ���׽��[amount]ֵ������!' )  
   
    if( not TradeContext.existVariable( "I1CETY" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ԭ����ƾ֤[I1CETY]ֵ������!' )  
           
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    
    if( TradeContext.channelCode == '005' ):
        
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������!' )
        
        if( not TradeContext.existVariable( "brno" ) ): 
            return AfaFlowControl.ExitThisFlow( 'A0001', '�����[brno]ֵ������!' )
        
        if( not TradeContext.existVariable( "termId" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '�ն˺�[termId]ֵ������!' )
   
    return True

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('��֤�ش��Ӳ�ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']����' )
    
    try:
        sql = "select unitno,amount,userno,note4,note5,note8,note9,note10,craccno,note7 from afa_maintransdtl"
        sql = sql + " where agentserialno = '" + TradeContext.transrno.strip() + "'"
        sql = sql + " and   workdate      = '" + TradeContext.workDate.strip() + "'"
        sql = sql + " and   bankstatus    = '0' and corpstatus = '0' and revtranf = '0'"
        
        AfaLoggerFunc.tradeInfo('��֤�ش���Ϣ��ѯ���'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ����ͨ���ݿ�ʧ��"
            raise AfaFlowControl.flowException( )
        
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽ɷ���Ϣ"
            return False
        
        else:
            if(records[0][0]!=TradeContext.unitno):
                TradeContext.errorCode,TradeContext.errorMsg='E9999',"��λ��Ų���"
                return False
            
            if(records[0][1].split()!=TradeContext.amount.split()):
                TradeContext.errorCode,TradeContext.errorMsg='E9999',"��ԭ���׽���"
                return False
            
            if(records[0][2]!=TradeContext.userno):
                TradeContext.errorCode,TradeContext.errorMsg='E9999',"��ԭ����ӡˢ�Ų���"
                return False
           
            note9=records[0][6].split('|')
            AfaLoggerFunc.tradeInfo(note9[2] + "||"+TradeContext.policy)
            if(note9[2]!=TradeContext.policy):
                TradeContext.errorCode,TradeContext.errorMsg='E9999',"��ԭ���յ��Ų���"  
                return False
            
            #note9���յ���
            TradeContext.policy=note9[2]
            
            #note8�������ֺ͸�������      
            note8= records[0][5].split('|') 
            TradeContext.productid=note8[0]
            TradeContext.productid1=note8[2] 
            
            #note4:Ͷ��������|Ͷ����֤������|��Ͷ���˹�ϵ        
            note4= records[0][3].split('|') 
            TradeContext.tbr_name=note4[0]
            TradeContext.tbr_idno=note4[1]
            TradeContext.tbr_bbr_rela=note4[2] 
          
            #note5:����������|������֤������|�뱻�����˹�ϵ 
            note5= records[0][4].split('|') 
            TradeContext.bbr_name=note5[0]
            TradeContext.bbr_idno=note5[1]
            TradeContext.syr_bbr_rela=note5[2] 
            TradeContext.payacc=records[0][8] 

            #note7:���ѷ�ʽ|�ɷ��ڴ�|�����ڼ�
            TradeContext.paymethod = records[0][9].split('|')[0]
            
        #��ѯ��������Ϣ
        sql = "select syr_info1,syr_info2,syr_info3,syr_info4,syr_info5 from ybt_info"
        sql = sql + " where submino  = '" + note9[1]                    + "'"            #Ͷ������
        sql = sql + " and   cpicno   = '" + TradeContext.unitno         + "'"            #���չ�˾����
        sql = sql + " and   workdate = '" + TradeContext.workDate       + "'"            #��������
        sql = sql + " and   tellerno = '" + TradeContext.tellerno       + "'"            #���׹�Ա
        
        AfaLoggerFunc.tradeInfo('��ѯ��������Ϣ��'+ sql)
        
        results = AfaDBFunc.SelectSql( sql )
        
        if results == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ��������Ϣ�쳣"
            return False
        
        if(len(results) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","û���ҵ���ص���������Ϣ"
            return False
            
        else:
            TradeContext.syr_1 = results[0][0]                        #������1��Ϣ
            TradeContext.syr_2 = results[0][1]                        #������2��Ϣ
            TradeContext.syr_3 = results[0][2]                        #������3��Ϣ
            TradeContext.syr_4 = results[0][3]                        #������4��Ϣ
            TradeContext.syr_5 = results[0][4]                        #������5��Ϣ
            
        TradeContext.errorCode = '0000'
        AfaLoggerFunc.tradeInfo('��֤�ش��Ӳ�ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�˳�' )
        return True
    
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
