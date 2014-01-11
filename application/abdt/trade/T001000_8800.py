# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ���û���½
#===============================================================================
#   �����ļ�:   T001000_8800.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os
from types import *


#=====================�û���½==================================================
def TrxMain():
    

    AfaLoggerFunc.tradeInfo('**********�û���½(8800)��ʼ**********')


    sqlStr = "SELECT ZONENO,BRNO,USERNAME,TEL,ADDRESS,PASSWORD FROM ABDT_USERINFO WHERE STATUS='1'"
    sqlStr = sqlStr + " AND USERNO = '" + TradeContext.USERNO + "'"

    AfaLoggerFunc.tradeInfo(sqlStr)

    records =  AfaDBFunc.SelectSql( sqlStr )
        
    if (records == None):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9999', '��ѯ�û���Ϣ�쳣' )

    if (len(records)==0) :
        return ExitSubTrade( '9000', '���û��Ų�����' )

    else:
        if ( records[0][5] == TradeContext.PASSWD ):
            TradeContext.tradeResponse.append(['ZONENO',    records[0][0]])
            TradeContext.tradeResponse.append(['BRNO',      records[0][1]])
            TradeContext.tradeResponse.append(['USERNAME',  records[0][2]])
        else:
            return ExitSubTrade( '9999', '�������,������!')

    AfaLoggerFunc.tradeInfo('**********�û���½(8800)����**********')

    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False