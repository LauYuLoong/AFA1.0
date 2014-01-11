###############################################################################
# -*- coding: gbk -*-
# ժ    Ҫ������������Ϣ��ѯ
# ��ǰ�汾��1.0
# ��    �ߣ�����
# ������ڣ�2011��12��1��
###############################################################################
import AfaDBFunc,AfaLoggerFunc,TradeContext,AfaFlowControl
from types import *

def TrxMain( ):
    AfaLoggerFunc.tradeInfo('---------��ũ������ҵ�����------------')
    
    #ҵ����
    if ( not (TradeContext.existVariable( "Appno" ) and len(TradeContext.Appno.strip()) > 0) ):
        TradeContext.errorCode,TradeContext.errorMsg = 'NB001', "������ҵ����"
        raise AfaFlowControl.flowException( )
    #��λ���
    if ( not (TradeContext.existVariable( "Busino" ) and len(TradeContext.Busino.strip()) > 0) ):
        TradeContext.errorCode,TradeContext.errorMsg = 'NB001', "�����ڵ�λ���"
        raise AfaFlowControl.flowException( )
    #�ϴ��ļ���
    if ( not (TradeContext.existVariable( "FileName" ) and len(TradeContext.FileName.strip()) > 0) ):
        TradeContext.errorCode,TradeContext.errorMsg = 'NB001', "�������ϴ��ļ���"
        raise AfaFlowControl.flowException( )
    #��������
    if ( not (TradeContext.existVariable( "ApplyDate" ) and len(TradeContext.ApplyDate.strip()) > 0) ):
        TradeContext.errorCode,TradeContext.errorMsg = 'NB001', "��������������"
        raise AfaFlowControl.flowException( )
    
    sql = ""
    sql = sql + "select BATCHNO,FILENAME,SWAPFILENAME,WORKDATE,STATUS,"
    sql = sql + "PROCMSG,APPLYDATE,APPNO,BUSINO,TOTALNUM,TOTALAMT,FILETYPE,"
    sql = sql + "BRNO,TELLERNO,BEGINDATE,ENDDATE,WORKTIME,NOTE1,NOTE2,NOTE3,NOTE4"
    sql = sql + " from ahnx_file where"
    sql = sql + " FileName = '"+ TradeContext.FileName +"'"            #�ϴ��ļ���
    sql = sql + " and ApplyDate = '"+ TradeContext.ApplyDate +"'"      #��������
    sql = sql + " and status <>"  + "'2'"                              #�ļ�״̬
    
    sql = sql + " and Appno = '"+ TradeContext.Appno +"'"              #ҵ����
    sql = sql + " and Busino = '"+ TradeContext.Busino +"'"            #��λ���
    
    AfaLoggerFunc.tradeInfo("����������Ϣ��ѯsql="+sql)
    records = AfaDBFunc.SelectSql( sql )
    
    if(records == None):
        AfaLoggerFunc.tradeInfo("����������Ϣ��ѯ���ݿ��쳣")
        return ExitSubTrade('NB000', '����������Ϣ��ѯ���ݿ��쳣')
    elif(len(records)==0):
        AfaLoggerFunc.tradeInfo("û�в�ѯ����ص�����������Ϣ")
        return ExitSubTrade('NB002', 'û�в�ѯ����ص�����������Ϣ')
    elif(len(records)>1):
        AfaLoggerFunc.tradeInfo("������������Ϣ��Ψһ")
        return ExitSubTrade('NB003', '������������Ϣ��Ψһ')
    else:
        TradeContext.SwapFileName = records[0][2].strip()
        TradeContext.ProcMsg      = records[0][5].strip()
        TradeContext.FileType     = records[0][11].strip()
        TradeContext.batchNo      = records[0][0].strip()
        
    TradeContext.errorCode  = "0000"
    TradeContext.errorMsg   = "���׳ɹ�"
    AfaLoggerFunc.tradeInfo('---------��ũ������ҵ���˳�------------')
    
    return ExitSubTrade('0000', '���׳ɹ�')


#------------------------------------------------------------------
#�׳�����ӡ��ʾ��Ϣ
#------------------------------------------------------------------
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg
        AfaLoggerFunc.tradeInfo( errorMsg )

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False