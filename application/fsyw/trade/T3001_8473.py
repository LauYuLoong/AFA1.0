# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8473.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ��־

    AfaLoggerFunc.tradeInfo( "********************��̨���Ҳ��ҿ�ʼ***************" )

    #���ǽɿ������ǿյ�ʱ��
    if not TradeContext.AFC001 :
        TradeContext.errorCode,TradeContext.errorMsg        =   "0002","�ɿ�����Ϊ��"
        return False

    sqlstr          =   "select AFC401,AFC015 from fs_fc74 where AFC001 like '%" + TradeContext.AFC001 + "%' and afc016='" +TradeContext.brno + "' and busino='" + TradeContext.busiNo + "' and flag!='*'"

    #===�����������б����ֶ�,�ź��޸�===
    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "û�в鵽������Ϣ"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
    else:
        recCnt                  =   len(records)            #��¼����
        TradeContext.RECCNT     =   str ( recCnt )

        TradeContext.AFC015     =   records[0][1]

        value                   =   []
        for i in range(recCnt):
            value.append(records[i][0])

        AfaLoggerFunc.tradeInfo( value )
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( TradeContext.AFC015 )
        TradeContext.serialNo   =   ":".join(value)
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "���Ҳ��ҳɹ�"

    AfaLoggerFunc.tradeInfo( "********************��̨���Ҳ��ҽ���***************" )
    return True
