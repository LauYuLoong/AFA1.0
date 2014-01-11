# -*- coding: gbk -*-
##################################################################

#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TTJYW003_8497.py
#   ����˵��:   [���ܲ�ѯ]
#   �޸�ʱ��:   2011-01-05
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    try:
        AfaLoggerFunc.tradeInfo('>>>>>>>>>>>>ǰһ�����ݻ��ܲ�ѯ��俪ʼ') 
        sql = "select sum(cast(amount as decimal(15,2))),count(*) from afa_maintransdtl"
        sql = sql + " where  workdate    = '" + TradeContext.workdate.strip()  + "'"
        sql = sql + " and    bankstatus  = '0'  and revtranf = '0' and chkflag = '0'"
        sql = sql + " and    sysid       = '" + TradeContext.sysId.strip()     +"'"
        sql = sql + " and    unitno      = '" + TradeContext.unitno.strip()    + "'"
        
        #20120709�º���� note2 ---busino��λ����
        sql = sql + " and    note2       = '" + TradeContext.busino            +"'"     #��λ���
        
        AfaLoggerFunc.tradeInfo('������Ϣ��ѯ���'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ�ʧ��"
            raise AfaFlowControl.flowException( )
        
        if records[0][1] == 0:
            TradeContext.errorCode,TradeContext.errorMsg = "0001","û�в�ѯ�����ܼ�¼��Ϣ"
            raise AfaFlowControl.flowException( )
        
        else:
            TradeContext.totalamt = str(records[0][0])             #�ܽ��
            TradeContext.totalnum = str(records[0][1])             #�ܱ��� 

     #20120706 �º��޸�ע�ͣ����
     #begin
     #   sql = "select accno1 from afa_unitadm"
     #   sql = sql + " where sysid     = '" + TradeContext.sysId.strip() + "'"           
     #   sql = sql + " and   unitno    = '" + TradeContext.unitno.strip() + "'"          
     #                                                                                   
     #   AfaLoggerFunc.tradeInfo('�տ����˺���Ϣ��ѯ���'+ sql)                          
     #                                                                                   
     #   records = AfaDBFunc.SelectSql( sql )                                            
     #                                                                                   
     #   if records == None:                                                             
     #       TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ�ʧ��"     
     #       raise AfaFlowControl.flowException( )                                       
     #                                                                                   
     #   if(len(records) < 1):                                                             
     #       TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴���Ϣ"              
     #       raise AfaFlowControl.flowException( )                                                                 
     #                                                                                     
     #   else:                                                                             
     #       TradeContext.accno = records[0][0]             #�տ���   
            
            
        sql = ""
        sql = sql + " select accno from abdt_unitinfo "
        sql = sql + " where appno = '" + TradeContext.sysId.strip()  + "' "
        sql = sql + " and  busino = '" + TradeContext.busino.strip() + "' "
        
        AfaLoggerFunc.tradeInfo('��ѯ��� �� '+ sql)                          
                                                                                    
        record = AfaDBFunc.SelectSql( sql )                                        
        if record == None:                                                         
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ�ʧ��" 
            raise AfaFlowControl.flowException( )                                   
                                                                                    
        if(len(record) < 1):                                                       
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�õ�λû��ǩԼ����������ҵ��"        
            raise AfaFlowControl.flowException( )                                                             
                                                                                    
        else:                                                                       
            TradeContext.accno       = record[0][0]             #�տ����ʻ� 
            
            #AfaLoggerFunc.tradeInfo('�տ����ʻ�accno��'+ TradeContext.accno) 
        
     #end    
            
            
                              
        AfaLoggerFunc.tradeInfo('>>>>>>>>>>>>>>>ǰһ�����ݻ��ܲ�ѯ������') 
        return True 
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
    
    
     