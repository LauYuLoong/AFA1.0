# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.���ղ�ѯ����
#=================================================================
#   �����ļ�:   T3001_8479.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext
TradeContext.sysType = 'fsyw'
import AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ��־

    AfaLoggerFunc.tradeInfo( "��λ������Ϣ��ѯ��ʼ" )

    #����̨���ݿ��в�ѯ
    sqlstr =   "select ACCNO,NAME,AAA010 ,AAA012,BANKNO,BANKNAME  from fs_businoinfo where busino='" + TradeContext.busiNo + "' and bankno = '" + TradeContext.bankbm  + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "9999"
        TradeContext.errorMsg   =   "���ҵ�λ������Ϣ�쳣"
        return False

    elif ( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "û�в��ҵ���λ������Ϣ"
        return False

    else:
        TradeContext.O1ACCN     =   records[0][0]           #�տ����ʺ�
        TradeContext.O1NAME     =   records[0][1]           #�տ�������
        TradeContext.O1AAA010   =   records[0][2]           #������������
        TradeContext.O1AAA012   =   records[0][3]           #��������
        TradeContext.O1BANKNO   =   records[0][4]           #�տ��˿����б���
        TradeContext.O1BANKNAME =   records[0][5]           #�տ��˿���������

    TradeContext.errorCode  =   "0000"
    TradeContext.errorMsg   =   "���ҵ�λ������Ϣ�ɹ�"
    AfaLoggerFunc.tradeInfo( "********************��̨��λ������Ϣ��ѯ����***************" )
    return True
