# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8475.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):
    TradeContext.__agentEigen__  = '0'   #�ӱ��־

    AfaLoggerFunc.tradeInfo( "��̨������ˮ������ݿ⿪ʼ" )

    #����̨���ݿ��в�ѯ
    sqlstr = "select afc011 from fs_fc74 where afc401='" + TradeContext.serNo + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and afc015='" + TradeContext.AFC015 + "'"

    #===�����������б����ֶ�,�ź��޸�===
    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        AfaLoggerFunc.tradeInfo( sqlstr )
        TradeContext.errorCode  =   "9999"
        TradeContext.errorMsg   =   "������ˮ���ʧ��"
        return False

    elif ( len(records)==0 ):
        AfaLoggerFunc.tradeInfo( sqlstr )
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "û�в��ҵ���ˮ���"
        return False

    else:
        TradeContext.totalAmt   =   records[0][0]

    TradeContext.errorCode  =   "0000"
    TradeContext.errorMsg   =   "������ˮ���ɹ�"
    AfaLoggerFunc.tradeInfo( "********************��̨������ˮ������ݿ⿪ʼ***************" )
    return True