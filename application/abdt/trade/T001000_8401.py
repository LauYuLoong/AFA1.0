# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��¼�뵥λ��Ϣ
#===============================================================================
#   �����ļ�:   T001000_8401.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AfaFunc
from types import *


#=====================¼�뵥λ��Ϣ==============================================
def TrxMain():

    AfaLoggerFunc.tradeInfo('**********¼�뵥λ��Ϣ(8401)��ʼ**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��

    #begin 20100709 ������ ���ڷ�˰ҵ���аѵ�λ�����ΪΨһ��ʶ��Ϊ�˱�֤��˰ҵ���в�ͬҵ����ʱ��������ͬ�ĵ�λ��ţ��޸Ĳ�ѯ����
    #�жϵ�λ��Ϣ�Ƿ����
    #sqlStr = "SELECT BUSINAME FROM ABDT_UNITINFO WHERE "
    #sqlStr = sqlStr + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "        #ҵ����
    #sqlStr = sqlStr + "BUSINO=" + "'" + TradeContext.I1BUSINO + "'" + " AND "        #��λ���
    #sqlStr = sqlStr + "STATUS=" + "'" + "1"                   + "'"                  #״̬(0:ע��,1:����)
    
    sqlStr = "SELECT BUSINAME FROM ABDT_UNITINFO WHERE "
    if TradeContext.I1APPNO == 'AG2008' or TradeContext.I1APPNO == 'AG2012':
        sqlStr = sqlStr + "APPNO in ('AG2008','AG2012')" + " AND "                   #ҵ����
    else:
        sqlStr = sqlStr + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "    #ҵ����
    sqlStr = sqlStr + "BUSINO=" + "'" + TradeContext.I1BUSINO + "'" + " AND "        #��λ���
    sqlStr = sqlStr + "STATUS=" + "'" + "1"                   + "'"                  #״̬(0:ע��,1:����)
    #end


    AfaLoggerFunc.tradeInfo( sqlStr )


    records = AfaDBFunc.SelectSql( sqlStr )
    if ( records == None ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '¼�뵥λ��Ϣ�쳣' )

    if ( len(records) > 0 ):
        return ExitSubTrade( '9000', '�õ�λ��Ϣ�Ѿ���ע��,�����ٴν���ע��')


    #����õ�λû�н���ע�ᣬ��Ըõ�λ��Ϣ����ע��(����)
    sql = "INSERT INTO ABDT_UNITINFO("
    sql = sql + "APPNO,"             #ҵ����:AG + ˳���(4)
    sql = sql + "BUSINO,"            #��λ���:��������(10) + ˳���(4)
    sql = sql + "AGENTTYPE,"         #ί�з�ʽ
    sql = sql + "AGENTMODE,"         #ί�з�Χ
    sql = sql + "VOUHTYPE,"          #ƾ֤����
    sql = sql + "VOUHNO,"            #ƾ֤����
    sql = sql + "ACCNO,"             #�����˻�(�Թ��˻�)
    sql = sql + "SUBACCNO,"          #���˻�����
    sql = sql + "SIGNUPMODE,"        #ǩԼ��ʽ(0-˫��, 1-����)
    sql = sql + "GETUSERNOMODE,"     #��λ�ͻ���Ż�ȡ��ʽ(0-����, 1-��ҵ)
    sql = sql + "PROTNO,"            #Э���
    sql = sql + "APPNAME,"           #ҵ������
    sql = sql + "BUSINAME,"          #��λ����
    sql = sql + "ADDRESS,"           #��ϵ��ַ
    sql = sql + "TEL,"               #��ϵ�绰
    sql = sql + "USERNAME,"          #��ϵ��Ա
    sql = sql + "WORKDATE,"          #��������
    sql = sql + "BATCHNO,"           #���κ�
    sql = sql + "STARTDATE,"         #��Ч����
    sql = sql + "ENDDATE,"           #ʧЧ����
    sql = sql + "STARTTIME,"         #����ʼʱ��
    sql = sql + "ENDTIME,"           #������ֹʱ��
    sql = sql + "ZONENO,"            #��������
    sql = sql + "BRNO,"              #��������
    sql = sql + "TELLERNO,"          #��Ա����
    sql = sql + "REGDATE,"           #ע������
    sql = sql + "REGTIME,"           #ע��ʱ��
    sql = sql + "STATUS,"            #״̬(0-δ����, 1-����, 2-�ر�, 3-ͣ��)
    sql = sql + "CHKDATE,"           #��������
    sql = sql + "CHKTIME,"           #����ʱ��
    sql = sql + "CHKFLAG,"           #���ʱ�־(0-δ����, 1-�Ѷ���)
    sql = sql + "NOTE1,"             #��ע1
    sql = sql + "NOTE2,"             #��ע2
    sql = sql + "NOTE3,"             #��ע3
    sql = sql + "NOTE4,"             #��ע4
    sql = sql + "NOTE5) "            #��ע5

    sql = sql + " VALUES ("

    sql = sql + "'" + TradeContext.I1APPNO          + "',"            #ҵ����
    sql = sql + "'" + TradeContext.I1BUSINO         + "',"            #��λ���
    sql = sql + "'" + TradeContext.I1AGENTTYPE      + "',"            #ί�з�ʽ
    sql = sql + "'" + TradeContext.I1AGENTMODE      + "',"            #����Χ
    sql = sql + "'" + TradeContext.I1VOUHTYPE       + "',"            #ƾ֤����
    sql = sql + "'" + TradeContext.I1VOUHNO         + "',"            #ƾ֤����
    sql = sql + "'" + TradeContext.I1ACCNO          + "',"            #�����˻�(�Թ��ʻ�)
    sql = sql + "'" + TradeContext.I1SUBACCNO       + "',"            #���ʻ�����
    sql = sql + "'" + TradeContext.I1SIGNUPMODE     + "',"            #ǩԼ��ʽ(0-˫��, 1-����)
    sql = sql + "'" + TradeContext.I1GETUSERNOMODE  + "',"            #��λ�ͻ���Ż�ȡ��ʽ(0-����, 1-��ҵ)
    sql = sql + "'" + TradeContext.I1PROTNO         + "',"            #Э���
    sql = sql + "'" + TradeContext.I1APPNAME        + "',"            #ҵ������
    sql = sql + "'" + TradeContext.I1BUSINAME       + "',"            #��λ����
    sql = sql + "'" + TradeContext.I1ADDRESS        + "',"            #��ϵ��ַ
    sql = sql + "'" + TradeContext.I1TEL            + "',"            #��ϵ�绰
    sql = sql + "'" + TradeContext.I1USERNAME       + "',"            #��ϵ��Ա
    sql = sql + "'" + TradeContext.TranDate         + "',"            #��������
    sql = sql + "'" + "000"                         + "',"            #���κ�
    sql = sql + "'" + TradeContext.I1STARTDATE      + "',"            #��Ч����
    sql = sql + "'" + TradeContext.I1ENDDATE        + "',"            #ʧЧ����
    sql = sql + "'" + TradeContext.I1STARTTIME      + "',"            #����ʼʱ��
    sql = sql + "'" + TradeContext.I1ENDTIME        + "',"            #������ֹʱ��
    sql = sql + "'" + TradeContext.I1ZONENO         + "',"            #��������
    sql = sql + "'" + TradeContext.I1SBNO           + "',"            #��������
    sql = sql + "'" + TradeContext.I1USID           + "',"            #��Ա����
    sql = sql + "'" + TradeContext.TranDate         + "',"            #ע������
    sql = sql + "'" + TradeContext.TranTime         + "',"            #ע��ʱ��
    sql = sql + "'" + "1"                           + "',"            #״̬((0-δ����, 1-����, 2-�ر�, 3-ͣ��)
    sql = sql + "'" + ""                            + "',"            #��������
    sql = sql + "'" + ""                            + "',"            #����ʱ��
    sql = sql + "'" + "0"                           + "',"            #���ʱ�־(0-δ����, 1-�Ѷ���)
    sql = sql + "'" + TradeContext.I1NOTE1          + "',"            #��ע1
    sql = sql + "'" + TradeContext.I1NOTE2          + "',"            #��ע2
    sql = sql + "'" + TradeContext.I1NOTE3          + "',"            #��ע3
    sql = sql + "'" + TradeContext.I1NOTE4          + "',"            #��ע4
    sql = sql + "'" + TradeContext.I1NOTE5          + "')"            #��ע5

    AfaLoggerFunc.tradeInfo( sql )

    result = AfaDBFunc.InsertSqlCmt( sql )
    if( result <= 0 ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '���ӵ�λ��Ϣʧ��')

    AfaLoggerFunc.tradeInfo('**********¼�뵥λ��Ϣ(8401)����**********')

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