# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8472.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):
    
    AfaLoggerFunc.tradeInfo( '********************�������ݱ����*******************' )
    TradeContext.__agentEigen__  = '0'   #�ӱ��־
    
    sqlstr      =   "select busino,hostip,upuser,uppasswd,upldir,downuser,downpasswd,downldir from fs_businoconf where busino='" + TradeContext.busiNo + "'"
    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )   
    if records == None:
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "�������ݿ��쳣"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
        
    if( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "δ�ҵ���Ӧ��¼"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
    else:    
        TradeContext.APPNO      =   'AG2008'
        TradeContext.BUSINO     =   records[0][0]
        TradeContext.HOSTIP     =   records[0][1]
        TradeContext.RDOWNPATH  =   records[0][7]
        TradeContext.RUPPATH    =   records[0][4]
        TradeContext.DOWNUSER   =   records[0][5]
        TradeContext.DOWNPWD    =   records[0][6]
        TradeContext.UPUSER     =   records[0][2]
        TradeContext.UPPD       =   records[0][3]
    
    sqlstr      =   "select date,this from fs_remain where busino='" + TradeContext.busiNo + "'"
    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )   
    if records == None:
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "�������ݿ��쳣"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
        
    if( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "δ�ҵ���Ӧ��¼"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
    else:    
        AfaLoggerFunc.tradeInfo(records[0][1])
        TradeContext.THIS        =   records[0][1]
        AfaLoggerFunc.tradeInfo(records[0][0])
        TradeContext.ACCDATE     =   records[0][0]
        
    AfaLoggerFunc.tradeInfo( '********************�������ݱ����*******************' )
    TradeContext.errorCode,TradeContext.errorMsg        =   "0000","���ҷ�˰���ݳɹ�"
    return True
        
