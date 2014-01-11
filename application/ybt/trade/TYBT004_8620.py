# -*- coding: gbk -*-
##################################################################

#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT004_8620.py
#   ����˵��:   [���ݱ����Ų�ѯ�ɷ���Ϣ,�±��ɷ���������]
#   �޸�ʱ��:   2010-08-11
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    
   
    AfaLoggerFunc.tradeInfo( '�ɷ���Ϣ��ѯ����ֵ����Ч��У��' )
    
    if( not TradeContext.existVariable( "unitno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��λ���[unitno]ֵ������!' )
       
    if( not TradeContext.existVariable( "applno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'Ͷ������[applno]ֵ������!' )
   
    if( not TradeContext.existVariable( "userno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '����ӡˢ��[userno]ֵ������!' )   
    
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
    AfaLoggerFunc.tradeInfo('�±��ɷ���Ϣ��ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
   
    try:
        sql = "select agentserialno,amount,payouttype,payoutdur,tbr_name,tbr_idno,bbr_name,bbr_idno,tbr_bbr_rela,"
        sql = sql + " tellerno,xzinfo,syr_info1,syr_info2,syr_info3,syr_info4,syr_info5 from ybt_info"
        sql = sql + " where printno  = '" + TradeContext.userno.strip() + "'"
        sql = sql + " and   submino  = '" + TradeContext.applno.strip() + "'"
        sql = sql + " and   cpicno   = '" + TradeContext.unitno         + "'"
        sql = sql + " and   workdate = '" + TradeContext.workDate       + "'"
        sql = sql + " and   tellerno = '" + TradeContext.tellerno       + "'"
        
        AfaLoggerFunc.tradeInfo('�ɷ���Ϣ��ѯ���'+ sql)
       
        records = AfaDBFunc.SelectSql( sql )
       
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯYBT_INFO ��ʧ��"
            raise AfaFlowControl.flowException( )
            
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴�Ͷ����Ϣ"
            return False
        
        else:
            #������ˮ��
            TradeContext.transrno = records[0][0]
           
            #Ӧ�ɱ���
            TradeContext.amount = records[0][1]
            
            #�ɷѷ�ʽ
            TradeContext.paymethod = records[0][2]
            
            #�ɷ�����
            TradeContext.paydatelimit = records[0][3]
            
            # Ͷ��������
            TradeContext.tbr_name = records[0][4]
           
            #Ͷ�������֤����
            TradeContext.tbr_idno= records[0][5]
            
            #����������
            TradeContext.bbr_name = records[0][6]
            
            #���������֤����
            TradeContext.bbr_idno = records[0][7]
           
            #��Ͷ���˹�ϵ
            TradeContext.tbr_bbr_rela = records[0][8]
            
            #����Ӫ����Ա����
            TradeContext.salerno = records[0][9]
            
            #�������ֺ͸�������
            list=records[0][10].split('|')        
            TradeContext.productid=list[0]
            TradeContext.productid1=list[1]
            
            #��������Ϣ
            TradeContext.syr_1 = records[0][11]
            TradeContext.syr_2 = records[0][12]
            TradeContext.syr_3 = records[0][13]
            TradeContext.syr_4 = records[0][14]
            TradeContext.syr_5 = records[0][15]
            
            TradeContext.errorCode = '0000'
        
        AfaLoggerFunc.tradeInfo('�˳��±��ɷ���Ϣ��ѯ����' )
        return True
   
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
