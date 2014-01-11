# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   TTJYW002_8496.py
#   ����˵��:   ���ճ���
#   �޸�ʱ��:   2011-01-05
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaAfeFunc,AfaFlowControl
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
    
    AfaLoggerFunc.tradeInfo( '����������Ԥ��ѯ����ѯ�Ƿ��д˽ɷѼ�¼' )
    try:
        sql = "select workdate,worktime,userno,tellerno,brno,unitno,amount,trxcode from afa_maintransdtl"
        sql = sql + " where agentserialno = '"+TradeContext.preAgentSerno+"' and workdate = '"+TradeContext.workDate+"' and trxcode='8495'"
        sql = sql + " and revtranf = '0' and bankstatus = '0'and chkflag = '9'"
        
        #20120718�º����
        sql = sql + " and  sysid = '" + TradeContext.sysId.strip()   + "' "
        sql = sql + " and  note2 = '" + TradeContext.busino.strip()  + "' "
        
        
        AfaLoggerFunc.tradeInfo('�����ײ�ѯ��䣺'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        AfaLoggerFunc.tradeInfo('�����ײ�ѯ�Ľ����'+ str(records))
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�����ײ�ѯ����ʧ��"
            raise AfaFlowControl.flowException( )
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽���"
            return False
        else:
            if(records[0][3] != TradeContext.tellerno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ���Ա�������������˽���"
                return False
            if(records[0][4] != TradeContext.brno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","ԭ���׷Ǳ������������������˽���"
                return False
            if(records[0][5] != TradeContext.unitno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���׹�˾�������������˽���"
                return False
            if(records[0][6].strip() != TradeContext.amount.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","��ԭ���׽������������˽���"
                return False
           
            TradeContext.PreWorkDate = records[0][0]                  #ԭ��������
            TradeContext.PreWorktime = records[0][1]                  #ԭ����ʱ��
            TradeContext.PreTrxCode  = records[0][7]                  #ԭ������
            TradeContext.amount = records[0][6]                       #���
            TradeContext.preAgentSerno = TradeContext.preAgentSerno   #ԭ������ˮ��
        return True     
    except  Exception, e:                       
        AfaLoggerFunc.tradeInfo( str(e) )     
        AfaFlowControl.flowException( )       
                             