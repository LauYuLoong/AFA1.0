# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8476.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):
    
    TradeContext.__agentEigen__  = '0'   #�ӱ��־
    
    AfaLoggerFunc.tradeInfo( "***********��̨���ұ������ƿ�ʼ**********" )
    
    #��ѯִ�յ�λ����
    if TradeContext.unitNo :
        sql   =   "select aaa010 from fs_businoinfo where  busino='" + TradeContext.busiNo + "'"
        ret   =   AfaDBFunc.SelectSql(sql)
        if ret == None or len(ret) == 0:
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "û�в��ҵ�ִ�յ�λ����"
            return False

        #sqlstr  =   "select afa052 from fs_fa15 where afa051='" + TradeContext.unitNo + "'"    
        sqlstr  =   "select afa052 from fs_fa15 where afa051='" + TradeContext.unitNo + "'"
        sqlstr  = sqlstr + " and aaa010='" + ret[0][0] + "' order by aaz002 desc"
        
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "û�в��ҵ�ִ�յ�λ����"
            return False
        
        TradeContext.unitName       =   records[0][0]               #ִ�յ�λ����
    else:
        TradeContext.unitName       =   ''
    AfaLoggerFunc.tradeInfo( ">>>ִ�յ�λ����[" + TradeContext.unitName + "]")
    
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯִ����Ŀ����" )
    #��ѯִ����Ŀ����
    if TradeContext.itemNo :
        sqlstr  =   "select afa032,afa030 from fs_fa13 where afa031='" + TradeContext.itemNo  + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"
        
        records = AfaDBFunc.SelectSql( sqlstr )
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( records )
        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "û�в��ҵ�ִ����Ŀ����"
            return False
        TradeContext.itemName       =   records[0][0]     #ִ����Ŀ����
    else:
        TradeContext.itemName       =   ''     
    AfaLoggerFunc.tradeInfo( ">>>ִ����Ŀ����[" + TradeContext.itemName + "]")
    
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ������������" )
    
    #��ѯ������������
    if TradeContext.bankNo :
        sqlstr  =   "select afa102 from fs_fa22 where afa101='" + TradeContext.bankNo + "'"
            
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "û�в��ҵ�������������"
            return False
            
        TradeContext.bankName       =   records[0][0]               #������������
    else:
        TradeContext.bankName       =   ''
     
    AfaLoggerFunc.tradeInfo( ">>>������������[" + TradeContext.bankName + "]")
          
    TradeContext.errorCode  =   "0000"
    TradeContext.errorMsg   =   "���ұ������Ƴɹ�"