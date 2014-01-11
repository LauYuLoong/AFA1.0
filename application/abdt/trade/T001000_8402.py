# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ����ѯ��λ��Ϣ
#===============================================================================
#   �����ļ�:   T001000_8402.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AfaFunc
from types import *


#=====================��ѯ��λ��Ϣ==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********��ѯ��λ��Ϣ(8402)��ʼ**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��


    #�жϵ�λ��Ϣ�Ƿ����
    sqlStr = "SELECT * FROM ABDT_UNITINFO WHERE "
    sqlStr = sqlStr +       "APPNO=" + "'" + TradeContext.I1APPNO   + "'"        #ҵ����
    sqlStr = sqlStr + " AND BUSINO=" + "'" + TradeContext.I1BUSINO  + "'"        #��λ���
#   sqlStr = sqlStr + " AND STATUS=" + "'" + "1"                    + "'"        #״̬(0:ע��,1:����)

    AfaLoggerFunc.tradeInfo( sqlStr )

    records = AfaDBFunc.SelectSql( sqlStr )
    if ( records == None ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '��ѯ��λ��Ϣ�쳣' )

    if ( len(records) <= 0 ):
        return ExitSubTrade( '9000', 'û���κε�λ��Ϣ')


    AfaLoggerFunc.tradeInfo("�ܹ���ѯ[" + str(len(records)) + "]����¼")

    #����None
    AfaUtilTools.ListFilterNone( records )
    
    #��¼����
    TradeContext.tradeResponse.append(['RECNUM',  str(len(records))])

    i=0
    while ( i  < len(records) ):
        TradeContext.tradeResponse.append(['O1APPNO',           str(records[i][0])])         #ҵ����
        TradeContext.tradeResponse.append(['O1BUSINO',          str(records[i][1])])         #��λ���
        TradeContext.tradeResponse.append(['O1AGENTTYPE',       str(records[i][2])])         #ί�з�ʽ
        TradeContext.tradeResponse.append(['O1AGENTMODE',       str(records[i][3])])         #����Χ
        TradeContext.tradeResponse.append(['O1VOUHTYPE',        str(records[i][4])])         #ƾ֤����
        TradeContext.tradeResponse.append(['O1VOUHNO',          str(records[i][5])])         #ƾ֤����
        TradeContext.tradeResponse.append(['O1ACCNO',           str(records[i][6])])         #�����˻�(�Թ��ʻ�)
        TradeContext.tradeResponse.append(['O1SUBACCNO',        str(records[i][7])])         #���ʻ�����
        TradeContext.tradeResponse.append(['O1SIGNUPMODE',      str(records[i][8])])         #ǩԼ��ʽ
        TradeContext.tradeResponse.append(['O1GETUSERNOMODE',   str(records[i][9])])         #��λ�ͻ���Ż�ȡ��ʽ
        TradeContext.tradeResponse.append(['O1PROTNO',          str(records[i][10])])        #Э���
        TradeContext.tradeResponse.append(['O1APPNAME',         str(records[i][11])])        #ҵ������
        TradeContext.tradeResponse.append(['O1BUSINAME',        str(records[i][12])])        #��λ����
        TradeContext.tradeResponse.append(['O1ADDRESS',         str(records[i][13])])        #��ϵ��ַ
        TradeContext.tradeResponse.append(['O1TEL',             str(records[i][14])])        #��ϵ�绰
        TradeContext.tradeResponse.append(['O1USERNAME',        str(records[i][15])])        #��ϵ��Ա
        TradeContext.tradeResponse.append(['O1WORKDATE',        str(records[i][16])])        #��������
        TradeContext.tradeResponse.append(['O1BATCHNO',         str(records[i][17])])        #���κ�
        TradeContext.tradeResponse.append(['O1STARTDATE',       str(records[i][18])])        #��Ч����
        TradeContext.tradeResponse.append(['O1ENDDATE',         str(records[i][19])])        #ʧЧ����
        TradeContext.tradeResponse.append(['O1STARTTIME',       str(records[i][20])])        #����ʼʱ��
        TradeContext.tradeResponse.append(['O1ENDTIME',         str(records[i][21])])        #������ֹʱ��
        TradeContext.tradeResponse.append(['O1ZONENO',          str(records[i][22])])        #��������
        TradeContext.tradeResponse.append(['O1BRNO',            str(records[i][23])])        #��������
        TradeContext.tradeResponse.append(['O1TELLERNO',        str(records[i][24])])        #��Ա����
        TradeContext.tradeResponse.append(['O1REGDATE',         str(records[i][25])])        #ע������
        TradeContext.tradeResponse.append(['O1REGTIME',         str(records[i][26])])        #ע��ʱ��
        TradeContext.tradeResponse.append(['O1STATUS',          str(records[i][27])])        #״̬
        TradeContext.tradeResponse.append(['O1CHKDATE',         str(records[i][28])])        #��������                      
        TradeContext.tradeResponse.append(['O1CHKTIME',         str(records[i][29])])        #����ʱ��                      
        TradeContext.tradeResponse.append(['O1CHKFLAG',         str(records[i][30])])        #���ʱ�־(0-δ����, 1-�Ѷ���)  
        TradeContext.tradeResponse.append(['O1NOTE1',           str(records[i][31])])        #��ע1
        TradeContext.tradeResponse.append(['O1NOTE2',           str(records[i][32])])        #��ע2
        TradeContext.tradeResponse.append(['O1NOTE3',           str(records[i][33])])        #��ע3
        TradeContext.tradeResponse.append(['O1NOTE4',           str(records[i][34])])        #��ע4
        TradeContext.tradeResponse.append(['O1NOTE5',           str(records[i][35])])        #��ע5
        i=i+1

    AfaLoggerFunc.tradeInfo('**********��ѯ��λ��Ϣ(8402)����**********')


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
        