# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TYBT005_8617.py
#   ����˵��:   ��������
#   �޸�ʱ��:   2010-7-30
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaYbtdb
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    
    try:
        AfaLoggerFunc.tradeInfo( '---->��ѯԭ�ɷѼ�¼' )
       
        sql = "select workdate,tellerno,brno,unitno,amount,note9,bankstatus ,userno from afa_maintransdtl"
        sql = sql + " where agentserialno = '" + TradeContext.preAgentSerno + "'"
        sql = sql + " and   workdate      = '" + TradeContext.workDate      + "'"
        
        AfaLoggerFunc.tradeInfo('---->��ѯԭʼ�ɷѼ�¼��'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records ==  None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ����ͨ���ݿ��쳣"
            AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
            raise False
        
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","û���ҵ�ԭ�ɷѽ��ף�����¼����"
            return False
        else:
            #bankstatus 0:���� 1��ʧ�� 2���쳣 3���ѳ���
            if (records[0][6] != '0'):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭʼ�ɷѽ����쳣���ѳ���������������������"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
                
            if (records[0][0] !=TradeContext.workDate ):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","���ǵ��ս��ף��������˽���"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
                
            if(records[0][1] != TradeContext.tellerno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ���Ա�������������˽���"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
            
            if(records[0][2] != TradeContext.brno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ������������������˽���"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
            
            if(records[0][3] != TradeContext.unitno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���ױ��չ�˾�������������˽���"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
           
            if(records[0][4].strip() != TradeContext.amount.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���׽������������˽���"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
            
            if(records[0][5].split('|')[2] != TradeContext.policy):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���ױ��յ��Ų������������˽���"
                AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
                return False
            
            TradeContext.userno = records[0][7]
            TradeContext.amount = records[0][4]
            
        AfaLoggerFunc.tradeInfo( '---->��ѯԭʼ������¼�Ƿ�ɹ���ʧ������е�������' )                                                             
        
        sql = "select bankstatus from afa_maintransdtl"
        sql = sql + " where preagentserno = '" + TradeContext.preAgentSerno + "'"
        sql = sql + " and   workdate      = '" + TradeContext.workDate      + "'"
        sql = sql + " and   revtranf      <> '0'"
        sql = sql + " and   trxcode in ('8615','8616')"
        
        AfaLoggerFunc.tradeInfo('---->��ѯԭʼ������¼�Ƿ�ɹ���'+ sql)
                                                                                                                              
        results = AfaDBFunc.SelectSql( sql )
                                                                                                                              
        if results == None:                                                                                                     
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"��ѯ���ݿ��쳣" 
            AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
            return False
        elif(len(results) < 1):                                                                                                 
            TradeContext.errorCode,TradeContext.errorMsg = "0001","û�������������ף���������������" 
            AfaLoggerFunc.tradeInfo('---->' + TradeContext.errorMsg)
            return False
        else:
            for result in results:
                #bankstatus 0:���� 1��ʧ�� 2���쳣 3���ѳ��� 
                if ( result[0] == '0' ):
                    TradeContext.errorCode = "0001"
                    TradeContext.errorMsg  = "�ý����ѳɹ������������ٳ���"
                    AfaLoggerFunc.tradeInfo ( '---->' + TradeContext.errorMsg )
                    return False
            AfaLoggerFunc.tradeInfo( '---->�ý��׳���ʧ�ܣ���������������' )
        return True

    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e)) 
