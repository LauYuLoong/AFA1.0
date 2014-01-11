# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ������ά��
#===============================================================================
#   �����ļ�:   T001000_8802.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AbdtManager
from types import *


#=====================������Ϣά��==============================================
def TrxMain():
    
    AfaLoggerFunc.tradeInfo('**********������Ϣά��(8802)_��ʼ**********')


    if (TradeContext.PROCTYPE   == '00'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ')
        if not QueryBatchInfo():
            return False

    elif (TradeContext.PROCTYPE == '01'):
        AfaLoggerFunc.tradeInfo('>>>����')
        
        if TradeContext.STATUS=='11':
            if not AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '20', '��������(����Ա)-->����������'):
                return False

        elif TradeContext.STATUS=='20':
            if not AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '21', '��������(����Ա)-->���ύ'):
                return False

        else:
            return ExitSubTrade( '9999', '����״̬�Ƿ�' )


    elif (TradeContext.PROCTYPE == '02'):
        AfaLoggerFunc.tradeInfo('>>>����')

        if TradeContext.STATUS=='11':
            if not AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '40', '��������(����Ա)-->�ֹ�����'):
                return False
                
        elif TradeContext.STATUS=='20':
            if not AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '40', '��������(����Ա)-->�ֹ�����'):
                return False

        else:
            return ExitSubTrade( '9999', '����״̬�Ƿ�' )
                
    AfaLoggerFunc.tradeInfo('**********������Ϣά��(8802)_����**********')

    #����
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '���׳ɹ�'
    return True


#=====================��ѯ������Ϣ==============================================
def QueryBatchInfo():

    sqlwhere = "WHERE BATCHNO > '" + TradeContext.batchNo + "'"

    if TradeContext.ZONENO == "0000":
        #����
        if (len(TradeContext.brno)==6):
            #��ѯ��������
            sqlwhere = sqlwhere + " AND SUBSTR(BRNO,1,6) = '" + TradeContext.brno + "'"

        elif (len(TradeContext.brno)==0):
            #��ѯȫ������
            pass

        else:
            #��ѯ��������
            sqlwhere = sqlwhere + " AND BRNO = '" + TradeContext.brno + "'"

    else:
        #����
        if(len(TradeContext.brno)==6):
            #��ѯ��������
            sqlwhere = sqlwhere + " AND SUBSTR(BRNO,1,6) = '" + TradeContext.brno + "'"
        else:
            #��ѯ��������
            sqlwhere = sqlwhere + " AND BRNO = '" + TradeContext.brno     + "'"


    if(len(TradeContext.trxDate)!=0):
        sqlwhere = sqlwhere + " AND INDATE = '" + TradeContext.trxDate + "'"

    if(len(TradeContext.trxState)==0 or TradeContext.trxState=='00' ):
        sqlwhere = sqlwhere + " AND STATUS IN ('10','11','20','21','22','30','31','32','40','88')"

    else:
        sqlwhere = sqlwhere + " AND STATUS = '" + TradeContext.trxState + "'"

    sqlwhere = sqlwhere + " ORDER BY BATCHNO"

    sql = "SELECT BATCHNO,APPNO,BUSINO,BRNO,USERNO,TERMTYPE,FILENAME,INDATE,INTIME,BATCHDATE,BATCHTIME,TOTALNUM"
    sql = sql + ",TOTALAMT,SUCCNUM,SUCCAMT,FAILNUM,FAILAMT,STATUS,BEGINDATE,ENDDATE,PROCMSG FROM ABDT_BATCHINFO " + sqlwhere

    AfaLoggerFunc.tradeInfo(sql)

    records =  AfaDBFunc.SelectSql( sql )
    if (records == None):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9999', '��ѯ������Ϣ�쳣' )

    if (len(records)==0) :
        return ExitSubTrade( '9000', 'û���κ�������Ϣ' )


    #############################################################################################################
    TradeContext.retData = ""

    TradeContext.retTotalNum = len(records)

    if(len(records)>3):
        TradeContext.retQueryNum = 3

    else:
        TradeContext.retQueryNum = len(records)

    for i in range(0,TradeContext.retQueryNum):
        TradeContext.retData = TradeContext.retData + records[i][0]                                      #���κ�
        TradeContext.retData = TradeContext.retData +"|"

        sql = "SELECT APPNAME,BUSINAME FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + records[i][1]  + "'" + " AND "         #ҵ����
        sql = sql + "BUSINO=" + "'" + records[i][2]  + "'" + " AND "         #��λ���
        sql = sql + "STATUS=" + "'" + "1"                   + "'"            #״̬(0:ע��,1:����)

        name_records = AfaDBFunc.SelectSql( sql )
        if ( len(name_records) != 0 ):
            TradeContext.retData = TradeContext.retData + records[i][1] + ' - ' + name_records[0][0]     #ҵ����
            TradeContext.retData = TradeContext.retData +"|"

            TradeContext.retData = TradeContext.retData + records[i][2] + ' - ' + name_records[0][1]     #��λ���
            TradeContext.retData = TradeContext.retData +"|"
        else:
            TradeContext.retData = TradeContext.retData + records[i][1]                                  #ҵ����
            TradeContext.retData = TradeContext.retData +"|"

            TradeContext.retData = TradeContext.retData + records[i][2]                                  #��λ���
            TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][3]    #������
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][4]    #����Ա
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][5]    #�ϴ���ʽ
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][6]    #�ϴ��ļ���
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][7]    #ί������
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][8]    #ί��ʱ��
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][9]    #�ύ����
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][10]   #�ύʱ��
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][11]   #�ܱ���
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][12]   #�ܽ��
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][13]   #�ɹ�����
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][14]   #�ɹ����
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][15]   #ʧ�ܱ���
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][16]   #ʧ�ܽ��
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][17]   #״̬
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][18]   #��Ч����
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][19]   #ʧЧ����
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][20]   #������Ϣ
        TradeContext.retData = TradeContext.retData +"|"

        AfaLoggerFunc.tradeInfo(records[i][0] + '|' + records[i][1] + "|" + records[i][2] + "|" + records[i][3] + "|")

    TradeContext.RETDATA      = TradeContext.retData
    
    TradeContext.RETTOTALNUM  = str(TradeContext.retTotalNum)

    TradeContext.RETQUERYNUM  = str(TradeContext.retQueryNum)
    
    return True




def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
