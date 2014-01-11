# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��ά����λ��Ϣ
#===============================================================================
#   �����ļ�:   T001000_8403.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AfaFunc
from types import *


#=====================ά����λ��Ϣ==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********ά����λ��Ϣ(8403)��ʼ**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��


    #�жϵ�λ�Ƿ���ҵ��
    sql = "SELECT BATCHNO FROM ABDT_BATCHINFO WHERE "
    sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO   + "'" + " AND "                   #ҵ�����
    sql = sql + "BUSINO=" + "'" + TradeContext.I1BUSINO  + "'" + " AND "                   #��λ����
    sql = sql + "ZONENO=" + "'" + TradeContext.I1ZONENO  + "'" + " AND "                   #��������
    sql = sql + "BRNO="   + "'" + TradeContext.I1SBNO    + "'" + " AND "                   #��������
    sql = sql + "STATUS NOT IN ('40','88','**')"                                           #״̬(����)


    AfaLoggerFunc.tradeInfo( sql )


    records = AfaDBFunc.SelectSql( sql )
    if ( records==None ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '�жϵ�λ�Ƿ���ҵ���쳣' )

    if ( len(records) > 0 ):
        return ExitSubTrade( '9000', '�õ�λ�Ѿ�����ҵ��,�����κβ���')


    #�Ե�λ��Ϣ����ά������
    if (TradeContext.I1PROCTYPE == '0'):
        #�޸�
        if ( TradeContext.I1OLDACCNO != TradeContext.I1ACCNO ):
            return ExitSubTrade( '9000', '���˺Ų�����ԭ���˺���ͬ')
                
        else:

            sql = "UPDATE ABDT_UNITINFO SET "
#           sql = sql + "APPNO='"         + TradeContext.I1APPNO         + "',"                    #ҵ����
#           sql = sql + "BUSINO='"        + TradeContext.I1BUSINO        + "',"                    #��λ���
            sql = sql + "AGENTTYPE='"     + TradeContext.I1AGENTTYPE     + "',"                    #ί�з�ʽ
            sql = sql + "AGENTMODE='"     + TradeContext.I1AGENTMODE     + "',"                    #����Χ
            sql = sql + "VOUHTYPE='"      + TradeContext.I1VOUHTYPE      + "',"                    #ƾ֤����
            sql = sql + "VOUHNO='"        + TradeContext.I1VOUHNO        + "',"                    #ƾ֤����
            sql = sql + "ACCNO='"         + TradeContext.I1ACCNO         + "',"                    #�����˻�(�Թ��ʻ�)
            sql = sql + "SUBACCNO='"      + TradeContext.I1SUBACCNO      + "',"                    #���ʻ�����
            sql = sql + "SIGNUPMODE='"    + TradeContext.I1SIGNUPMODE    + "',"                    #ǩԼ��ʽ
            sql = sql + "GETUSERNOMODE='" + TradeContext.I1GETUSERNOMODE + "',"                    #��λ�ͻ���Ż�ȡ��ʽ
            sql = sql + "PROTNO='"        + TradeContext.I1PROTNO        + "',"                    #Э���
#           sql = sql + "APPNAME='"       + TradeContext.I1APPNAME       + "',"                    #ҵ������
            sql = sql + "BUSINAME='"      + TradeContext.I1BUSINAME      + "',"                    #��λ����
            sql = sql + "ADDRESS='"       + TradeContext.I1ADDRESS       + "',"                    #��ϵ��ַ
            sql = sql + "TEL='"           + TradeContext.I1TEL           + "',"                    #��ϵ�绰
            sql = sql + "USERNAME='"      + TradeContext.I1USERNAME      + "',"                    #��ϵ��Ա
#           sql = sql + "WORKDATE='"      + TradeContext.I1WORKDATE      + "',"                    #��������
#           sql = sql + "BATCHNO='"       + TradeContext.I1BATCHNO       + "',"                    #���κ�
            sql = sql + "STARTDATE='"     + TradeContext.I1STARTDATE     + "',"                    #��Ч����
            sql = sql + "ENDDATE='"       + TradeContext.I1ENDDATE       + "',"                    #ʧЧ����
            sql = sql + "STARTTIME='"     + TradeContext.I1STARTTIME     + "',"                    #����ʼʱ��
            sql = sql + "ENDTIME='"       + TradeContext.I1ENDTIME       + "',"                    #������ֹʱ��
#           sql = sql + "ZONENO='"        + TradeContext.I1ZONENO        + "',"                    #��������
#           sql = sql + "BRNO='"          + TradeContext.I1BRNO          + "',"                    #��������
#           sql = sql + "TELLERNO='"      + TradeContext.I1TELLERNO      + "',"                    #��Ա����
#           sql = sql + "REGDATE='"       + TradeContext.I1REGDATE       + "',"                    #ע������
#           sql = sql + "REGTIME='"       + TradeContext.I1REGTIME       + "',"                    #ע��ʱ��
#           sql = sql + "STATUS='"        + TradeContext.I1STATUS        + "',"                    #״̬
#           sql = sql + "CHKDATE='"       + TradeContext.I1CHKDATE       + "',"                    #��������
#           sql = sql + "CHKTIME='"       + TradeContext.I1CHKTIME       + "',"                    #����ʱ��
#           sql = sql + "CHKFLAG='"       + TradeContext.I1CHKFLAG       + "',"                    #���˱�־
            sql = sql + "NOTE1='"         + TradeContext.I1USID          + "',"                    #��ע1(�޸Ĺ�Ա��)
            sql = sql + "NOTE2='"         + TradeContext.TranDate+TradeContext.TranTime + "',"     #��ע2(�޸�����ʱ��)
            sql = sql + "NOTE3='"         + TradeContext.I1NOTE3         + "',"                    #��ע3
            sql = sql + "NOTE4='"         + TradeContext.I1NOTE4         + "',"                    #��ע4
            sql = sql + "NOTE5='"         + TradeContext.I1NOTE5         + "'"                     #��ע5

            sql = sql + " WHERE "

            sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO   + "'" + " AND "                   #ҵ�����
            sql = sql + "BUSINO=" + "'" + TradeContext.I1BUSINO  + "'" + " AND "                   #��λ����
            sql = sql + "ZONENO=" + "'" + TradeContext.I1ZONENO  + "'" + " AND "                   #��������
            sql = sql + "BRNO="   + "'" + TradeContext.I1SBNO    + "'"                             #��������
#           sql = sql + "STATUS='1'"                                                               #״̬(0-ע�� 1-����)

            AfaLoggerFunc.tradeInfo( sql )

            result = AfaDBFunc.UpdateSqlCmt( sql )
                
            if( result <= 0 ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return ExitSubTrade( '9000', '�޸ĵ�λ��Ϣʧ��')
    else:
        #ע��

        AfaLoggerFunc.tradeInfo(">>>����Ҫ��λ��Ϣ��¼�Ƶ���λ��Ϣ��ʷ����")

        sql = ""
        sql = "INSERT INTO ABDT_HIS_UNITINFO SELECT * FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO   + "'" + " AND "        #ҵ�����
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO  + "'" + " AND "        #��λ����
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO  + "'" + " AND "        #��������
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO    + "'"                  #��������
#       sql = sql + "STATUS='1'"                                                      #״̬(0-ע�� 1-����)

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.InsertSqlCmt( sql )
        if (result <= 0):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', 'ע����λ��Ϣʧ��')


        AfaLoggerFunc.tradeInfo(">>>ɾ���ڵ�λ��Ϣ���б�ע����λ��Ϣ��¼")

        sql = ""
        sql = "DELETE FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO   + "'" + " AND "        #ҵ�����
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO  + "'" + " AND "        #��λ����
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO  + "'" + " AND "        #��������
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO    + "'"                  #��������
#       sql = sql + "STATUS='1'"                                                      #״̬(0-ע�� 1-����)

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.DeleteSqlCmt( sql )
        if (result <= 0):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', 'ע���ͻ���Ϣʧ��')


        AfaLoggerFunc.tradeInfo(">>>�ܹ�ע��[" + str(result) + "]����¼")


    AfaLoggerFunc.tradeInfo('**********ά����λ��Ϣ(8403)����**********')


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
