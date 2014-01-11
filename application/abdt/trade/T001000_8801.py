# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ���û�ά��
#===============================================================================
#   �����ļ�:   T001000_8801.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os
from types import *


#=====================�û���½==================================================
def TrxMain():
    

    AfaLoggerFunc.tradeInfo('**********�û�ά��(8801)��ʼ**********')

    if (TradeContext.PROCTYPE   == '00'):
        AfaLoggerFunc.tradeInfo('>>>��ѯ')
        if not QueryUserInfo():
            return False

    elif (TradeContext.PROCTYPE == '01'):
        AfaLoggerFunc.tradeInfo('>>>����')
        if not AddUserInfo():
            return False

    elif (TradeContext.PROCTYPE == '02'):
        AfaLoggerFunc.tradeInfo('>>>�޸�')
        if not UpdateUserInfo():
            return False

    elif (TradeContext.PROCTYPE == '03'):
        AfaLoggerFunc.tradeInfo('>>>ɾ��')
        if not DeleteUserInfo():
            return False

    elif (TradeContext.PROCTYPE == '04'):
        AfaLoggerFunc.tradeInfo('>>>�޸�����')
        if not UpdateUserPass():
            return False

    AfaLoggerFunc.tradeInfo('**********�û�ά��(8801)����**********')

    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True


#=====================��ѯ�û���Ϣ==============================================
def QueryUserInfo():

    sql = "SELECT ZONENO,BRNO,USERNO,USERNAME,DUTYNO,TEL,ADDRESS FROM ABDT_USERINFO WHERE STATUS='1'"

    if( TradeContext.existVariable( "USERNO" ) and len(TradeContext.USERNO)>0 ):
        sql = sql + " AND USERNO = '" + TradeContext.USERNO + "' ORDER BY USERNO"

    AfaLoggerFunc.tradeInfo(sql)

    records =  AfaDBFunc.SelectSql( sql )
    if (records == None):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9999', '��ѯ�û���Ϣ�쳣' )

    if (len(records)==0) :
        return ExitSubTrade( '9000', '�������û���Ϣ' )

    else:
        TradeContext.RETDATA = ""

        if(len(records)>5):
            TradeContext.RETFINDNUM = 5

        else:
            TradeContext.RETFINDNUM = len(records)

        for i in range(0,TradeContext.RETFINDNUM):

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][0]    #ZONENO
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][1]    #BRNO
            TradeContext.RETDATA = TradeContext.RETDATA +"|"
            
            TradeContext.RETDATA = TradeContext.RETDATA + records[i][2]    #USERNO
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][3]    #USERNAME
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][4]    #DUTYNO
            TradeContext.RETDATA = TradeContext.RETDATA +"|"
            
            TradeContext.RETDATA = TradeContext.RETDATA + records[i][5]    #TEL
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][6]    #ADDRESS
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            AfaLoggerFunc.tradeInfo( records[i][0] + '|' + records[i][1] + "|" + records[i][2] + "|" + records[i][3] + "|")

        TradeContext.tradeResponse.append(['RETDATA',TradeContext.RETDATA])

        TradeContext.tradeResponse.append(['RETFINDNUM',str(TradeContext.RETFINDNUM)])

        return True



#=====================�����û���Ϣ==============================================
def AddUserInfo():
    
    sql = "SELECT * FROM ABDT_USERINFO WHERE STATUS='1'"
    sql = sql + " AND ZONENO = '" + TradeContext.ZONENO + "'"
    sql = sql + " AND BRNO = '"   + TradeContext.BRNO   + "'"
    sql = sql + " AND USERNO = '" + TradeContext.USERNO + "'"
    
    records =  AfaDBFunc.SelectSql( sql )
        
    if( records == None ) :
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9999', '��ѯ�û���Ϣ�쳣' )

    if( len(records) > 0 ) :
        return ExitSubTrade( '9000', '���û��Ѿ���ע��,�����ٴ�ע��' )

    sql = "INSERT INTO ABDT_USERINFO("
    sql = sql + "ZONENO,"
    sql = sql + "BRNO,"
    sql = sql + "USERNO,"
    sql = sql + "USERNAME,"
    sql = sql + "ADDRESS,"
    sql = sql + "TEL,"
    sql = sql + "REGDATE,"
    sql = sql + "REGTIME,"
    sql = sql + "PASSWORD,"
    sql = sql + "DUTYNO,"
    sql = sql + "STATUS,"
    sql = sql + "NOTE1,"
    sql = sql + "NOTE2,"
    sql = sql + "NOTE3,"
    sql = sql + "NOTE4,"
    sql = sql + "NOTE5)"

    sql = sql + " VALUES ("

    sql = sql + "'" + TradeContext.ZONENO   + "',"            #��������
    sql = sql + "'" + TradeContext.BRNO     + "',"            #��������
    sql = sql + "'" + TradeContext.USERNO   + "',"            #�û���
    sql = sql + "'" + TradeContext.USERNAME + "',"            #�û���
    sql = sql + "'" + TradeContext.ADDRESS  + "',"            #��ַ
    sql = sql + "'" + TradeContext.TEL      + "',"            #�绰
    sql = sql + "'" + TradeContext.TranDate + "',"            #����
    sql = sql + "'" + TradeContext.TranTime + "',"            #ʱ��
    sql = sql + "'" + TradeContext.PASSWD   + "',"            #����
    sql = sql + "'" + TradeContext.DUTYNO   + "',"            #��λ����
    sql = sql + "'" + '1'                   + "',"            #״̬
    sql = sql + "'" + ''                    + "',"            #����
    sql = sql + "'" + ''                    + "',"            #����
    sql = sql + "'" + ''                    + "',"            #����
    sql = sql + "'" + ''                    + "',"            #����
    sql = sql + "'" + ''                    + "')"            #����

    AfaLoggerFunc.tradeInfo(sql)

    ret = AfaDBFunc.InsertSqlCmt( sql )
    if (ret <= 0):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '�û�ע��ʧ��' )

    return True



#=====================�޸��û���Ϣ==============================================
def UpdateUserInfo():

    sql = "UPDATE ABDT_USERINFO SET "
    sql = sql + "ZONENO='"   + TradeContext.ZONENO      + "',"                    #������
    sql = sql + "BRNO='"     + TradeContext.BRNO        + "',"                    #����
    sql = sql + "USERNAME='" + TradeContext.USERNAME    + "',"                    #�û���
    sql = sql + "DUTYNO='"   + TradeContext.DUTYNO      + "',"                    #��λ����
    sql = sql + "ADDRESS='"  + TradeContext.ADDRESS     + "',"                    #��ַ
    sql = sql + "TEL='"      + TradeContext.TEL         + "'"                     #�绰
    sql = sql + " WHERE "

    sql = sql + "USERNO="  + "'" + TradeContext.USERNO  + "'"                     #�û���

    AfaLoggerFunc.tradeInfo(sql)

    ret = AfaDBFunc.UpdateSqlCmt( sql )
    if (ret <= 0):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '�޸��û���Ϣʧ��' )

    return True


#=====================ɾ���û���Ϣ==============================================
def DeleteUserInfo():
    
    sql = "DELETE FROM ABDT_USERINFO WHERE USERNO=" + "'" + TradeContext.USERNO + "'"

    AfaLoggerFunc.tradeInfo(sql)

    ret = AfaDBFunc.UpdateSqlCmt( sql )
    if (ret <= 0):
        return ExitSubTrade( '9000', 'ɾ���û���Ϣʧ��' )
        
    return True


#=====================�޸��û�����==============================================
def UpdateUserPass():

    sql = "SELECT PASSWORD FROM ABDT_USERINFO WHERE STATUS='1' AND USERNO = '" + TradeContext.USERNO + "'"

    AfaLoggerFunc.tradeInfo(sql)
        
    records =  AfaDBFunc.SelectSql( sql )

    if (records == None or len(records)==0) :
        return ExitSubTrade( '9000', '�������û���Ϣ' )

    if (records[0][0] != TradeContext.OLDPASSWD):
        return ExitSubTrade( '9000', '�����벻��' )

    sql = "UPDATE ABDT_USERINFO SET PASSWORD='" + TradeContext.NEWPASSWD + "'"

    sql = sql + " WHERE "

    sql = sql + "USERNO="  + "'" + TradeContext.USERNO  + "'"              #�û���

    AfaLoggerFunc.tradeInfo(sql)

    ret = AfaDBFunc.UpdateSqlCmt( sql )
    if (ret < 0):
        return ExitSubTrade('9000', '�޸��û�����ʧ��')

    return True



def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False