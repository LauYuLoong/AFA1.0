# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��̨����-����ѯ�˻�ά��
#=================================================================
#   �����ļ�:   TFTCZ001_8656.py
#   ����˵��:   ��ѯ�˻�ά��
#   ����:       �º�
#   �޸�ʱ��:   2012��09-17
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    try:
        #�����ʺ�
        if not( TradeContext.existVariable( "CzAccNo" ) and len(TradeContext.CzAccNo.strip()) > 0):     
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ʺŲ�����"                  
            raise AfaFlowControl.flowException( ) 
            
        #�ʺſ�������
        if not( TradeContext.existVariable( "OpBkCode" ) and len(TradeContext.OpBkCode.strip()) > 0):     
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�ʺſ�������������"                  
            raise AfaFlowControl.flowException( )    
            
            
        #�жϴ��ʻ���Ϣ�Ƿ����
        sqlstr = ""
        sqlstr = sqlstr + " select accno,sbno,status from FT_CZZH where "
        sqlstr = sqlstr + " accno = '" + TradeContext.CzAccNo.strip()  + "' and"
        sqlstr = sqlstr + " sbno  = '" + TradeContext.OpBkCode.strip() + "' "
        
        #sqlstr = sqlstr + " sbno  = '" + TradeContext.OpBkCode.strip() + "' and"
        #sqlstr = sqlstr + " status= '1' "
        
        AfaLoggerFunc.tradeInfo("===��ѯ�����"+sqlstr)                                                                                                                         
                                                                                                                                                         
        result = AfaDBFunc.SelectSql(sqlstr)                                                                                                              
                                                                                                                                                         
        if (result == None):                                                                                                                                 
            AfaLoggerFunc.tradeInfo('>>>��������ѯʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg = 'E8888', "��������ѯʧ��,���ݿ��쳣"                  
            raise AfaFlowControl.flowException( )                                      
                                                             
        #�жϲ������� 0--������1--ɾ��
        if TradeContext.OptType == '0':
            AfaLoggerFunc.tradeInfo("===�ʻ��������ͣ�����")
            
            if (len(result) > 0): 
                if result[0][2] == '0':
                    AfaLoggerFunc.tradeInfo( "===�����ʻ�״̬Ϊ0(��ɾ��)���ʻ���Ϣ���ɸ���״̬Ϊ����" )
                    sqld = ""
                    sqld = sqld + " update  FT_CZZH set status = '1', "
                    sqld = sqld + " note1 = '"+ TradeContext.workDate.strip() +"' where "      #��������
                    sqld = sqld + " accno = '"+ TradeContext.CzAccNo.strip()  +"' and "
                    sqld = sqld + " sbno  = '"+ TradeContext.OpBkCode.strip() +"' and "
                    sqld = sqld + " status= '0' "
                
                    AfaLoggerFunc.tradeInfo("==(����)���±���Ϣ��"+sqld)

                    results = AfaDBFunc.UpdateSqlCmt( sqld )
                    if( results <= 0 ):
                        AfaLoggerFunc.tradeFatal( "===(����)���±�ʧ�ܣ�"+AfaDBFunc.sqlErrMsg )
                        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "(����)���±�ʧ�ܣ�"                 
                        raise AfaFlowControl.flowException( ) 
             
                    AfaLoggerFunc.tradeInfo("===�ʻ�����(����)�������̽���")
                    
                else:
                    AfaLoggerFunc.tradeFatal( "===�Ѵ�����Ӧ�ʺ���Ϣ�����ظ�����,��˶���Ϣ" )
                    TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�Ѵ�����Ӧ�ʺ���Ϣ�����ظ�����,��˶���Ϣ"                 
                    raise AfaFlowControl.flowException( )
            
            if (len(result) == 0):                                                                                                                                                                          
                AfaLoggerFunc.tradeInfo( "===���ʻ���Ӧ����,��������Ϣ" )
                sql = ""
                sql = sql + " insert into FT_CZZH values( "
                sql = sql + " '"+ TradeContext.CzAccNo.strip()  +"', "
                sql = sql + " '"+ TradeContext.OpBkCode.strip() +"', "
                sql = sql + " '1', "
                sql = sql + " '"+ TradeContext.workDate.strip() +"', "      #note1 ���ڲ�������
                sql = sql + " '', "
                sql = sql + " '', "
                sql = sql + " '', "
                sql = sql + " '') "
                
                AfaLoggerFunc.tradeInfo("==�������Ϣ��"+sql)

                results = AfaDBFunc.InsertSqlCmt( sql )
                if( results <= 0 ):
                    AfaLoggerFunc.tradeFatal( "===�����ʧ�ܣ�"+AfaDBFunc.sqlErrMsg )
                    TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�����ʧ�ܣ�"                 
                    raise AfaFlowControl.flowException( ) 
        
                AfaLoggerFunc.tradeInfo("===�ʻ������������̽���")
        
        if TradeContext.OptType == '1':
            AfaLoggerFunc.tradeInfo("===�ʻ��������ͣ�ɾ��")
            
            if (len(result) == 0): 
                AfaLoggerFunc.tradeFatal( "===��������Ӧ�ʺ���Ϣ����ɾ��,��˶���Ϣ" )
                TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��������Ӧ�ʺ���Ϣ����ɾ��,��˶���Ϣ"                 
                raise AfaFlowControl.flowException( )
            
            if (len(result) > 0):
                if result[0][2] == '1':                                                                                                                                                                      
                    AfaLoggerFunc.tradeInfo( "===�����ʻ���Ӧ����,��ɾ����Ϣ" )
                    sqld = ""
                    sqld = sqld + " update  FT_CZZH set status = '0', "
                    sqld = sqld + " note1 = '"+ TradeContext.workDate.strip() +"' where "      #��������
                    sqld = sqld + " accno = '"+ TradeContext.CzAccNo.strip()  +"' and "
                    sqld = sqld + " sbno  = '"+ TradeContext.OpBkCode.strip() +"' and "
                    sqld = sqld + " status= '1' "
                    
                    AfaLoggerFunc.tradeInfo("==(ɾ��)���±���Ϣ��"+sqld)
                    
                    results = AfaDBFunc.UpdateSqlCmt( sqld )
                    if( results <= 0 ):
                        AfaLoggerFunc.tradeFatal( "===(ɾ��)���±�ʧ�ܣ�"+AfaDBFunc.sqlErrMsg )
                        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "(ɾ��)���±�ʧ�ܣ�"                 
                        raise AfaFlowControl.flowException( ) 
                    
                    AfaLoggerFunc.tradeInfo("===�ʻ�ɾ���������̽���")
                    
                else:
                    AfaLoggerFunc.tradeFatal( "===��Ӧ�ʺ���Ϣ�ѱ�ɾ���������ظ�ɾ��,��˶���Ϣ" )
                    TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "��Ӧ�ʺ���Ϣ�ѱ�ɾ���������ظ�ɾ��,��˶���Ϣ"                 
                    raise AfaFlowControl.flowException( )
                
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "���׳ɹ�"
        return True
        
    except  Exception, e:                	   
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )  
                        
