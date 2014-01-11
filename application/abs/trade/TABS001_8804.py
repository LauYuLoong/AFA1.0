# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��������������ѯ
#===============================================================================
#   �����ļ�:   Tabs001_8804.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ghh
#   �޸�ʱ��:   2012-09-20
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AbdtFunc
from types import *


#=====================��ѯ==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********��ѯ(8804)��ʼ**********')

    try:
        sql = ""
        sql = "SELECT * FROM ABDT_BATCHINFO WHERE "
        sql = sql + "INDATE="    + "'" + TradeContext.indate  + "'" + " AND "      #��������
        sql = sql + "BATCHNO="   + "'" + TradeContext.batchno + "'"                #ί�к�




        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ������Ϣ���쳣' )

        if ( len(records) == 0 ):
            return ExitSubTrade( '9000', 'û�и�ί�кŵ�������Ϣ' )

        #����None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.tradeResponse.append(['appno',           str(records[0][1])])         #ҵ����
        TradeContext.tradeResponse.append(['busino',          str(records[0][2])])         #��λ���
        TradeContext.tradeResponse.append(['brno',            str(records[0][4])])         #�����
        TradeContext.tradeResponse.append(['status',          str(records[0][19])])        #״̬
        TradeContext.tradeResponse.append(['procmsg',         str(records[0][22])])        #��������



        #��������Ϣ
        BatchResultMsg = str(records[0][22])

        AfaLoggerFunc.tradeInfo('**********��ѯ(8804)����**********')


        #����
        TradeContext.tradeResponse.append(['errorCode', '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  BatchResultMsg])
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '��ѯ,���ݿ��쳣' )


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        