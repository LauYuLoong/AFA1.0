###############################################################################
# -*- coding: gbk -*-
# ժ    Ҫ����ũ������ҵ��״̬��ѯ
# ��ǰ�汾��1.0
# ��    �ߣ�����̩
# ������ڣ�2010��12��16��
###############################################################################
import AfaDBFunc,AfaLoggerFunc,TradeContext
#import os,AfaUtilTools, sys,AhXnbFunc,ConfigParser,  
from types import *

#=====================����ʡ��ũ������״̬��ѯ==============================================
def TrxMain( ):
    
    try:
        AfaLoggerFunc.tradeInfo('---------����ʡ����״̬��ѯ����------------')
       
        #ҵ����
        if not( TradeContext.existVariable( "I1APPNO" ) and len(TradeContext.I1APPNO.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "������ҵ����"
            raise AfaFlowControl.flowException( )
       
        #��λ���
        if not( TradeContext.existVariable( "I1BUSINO" ) and len(TradeContext.I1BUSINO.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ڵ�λ���"
            raise AfaFlowControl.flowException( )   
       
        #��������
        if not( TradeContext.existVariable( "I1WORKDATE" ) and len(TradeContext.I1WORKDATE.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��������������"
            raise AfaFlowControl.flowException( )   
         
        
        #���κ�
        if not( TradeContext.existVariable( "I1BATCHNO" ) and len(TradeContext.I1BATCHNO.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "���������κ�"
            raise AfaFlowControl.flowException( )
            
        sql = ''
        sql = "select procmsg from ahnx_file"
        sql = sql + " where workdate = '"+ TradeContext.I1WORKDATE + "' "  
        sql = sql + " and   batchno  = '"+ TradeContext.I1BATCHNO  + "' "   
        if TradeContext.I1APPNO != "NBKH":
            sql = sql + " and appno  = '"+ TradeContext.I1APPNO    +"' "  
            sql = sql + " and busino = '"+ TradeContext.I1BUSINO   + "' " 
        
        
        AfaLoggerFunc.tradeInfo('>>>>>>>��ʼ��ѯԭ���ף�'+ str(sql))
        records = AfaDBFunc.SelectSql( sql ) 
                  
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯAHNX_FILE��ʧ��"
            AfaLoggerFunc.tradeInfo('>>>>>>>��'+ TradeContext.errorMsg)
            return False
            
        if(len(records) == 0):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴���Ϣ"
            AfaLoggerFunc.tradeInfo('>>>>>>>��'+ TradeContext.errorMsg)
            return False   
        
        else:
            TradeContext.O1DESCRIBE = records[0][0]
            TradeContext.errorCode='0000'
        AfaLoggerFunc.tradeInfo('---------����ʡ����״̬��ѯ�˳�------------')
        return True
    
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return False
  
