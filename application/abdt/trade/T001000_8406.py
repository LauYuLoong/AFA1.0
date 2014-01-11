# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��ά��������Ϣ
#===============================================================================
#   �����ļ�:   T001000_8406.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,AbdtFunc,AfaAfeFunc
from types import *


#=====================ά��������Ϣ==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********ά��������Ϣ(8406)��ʼ**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��


    #�жϵ�λЭ���Ƿ���Ч
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    #�жϸ���Э���Ƿ���Ч
    if ( not ChkCustInfo( ) ):
        return False


    if ( TradeContext.I1PROCTYPE == '0' ):
        
        AfaLoggerFunc.tradeInfo('>>�޸ĸ���Э����Ϣ')


        #��ѯ�˻���Ϣ(����)
        if ( not AbdtFunc.QueryAccInfo( ) ):
            return False

        #�Ϸ���У��
        AfaLoggerFunc.tradeInfo('>>>�ж������˻�״̬')
        if ( TradeContext.ACCSTATUS != "0"):
            return ExitSubTrade( '9000', '�ͻ������˻�״̬�쳣,���ܽ���ע��' )
        
        
        AfaLoggerFunc.tradeInfo('>>>�ж��Ƿ���ҪУ��֤������')
        if ( TradeContext.I1IDCHKFLAG == "1" ):
            if (TradeContext.IDCODE != TradeContext.I1IDCODE):
                return ExitSubTrade( '9000', '�ͻ�֤�����벻��ȷ,���ܽ���ע��' )
        
        
        AfaLoggerFunc.tradeInfo('>>>�ж��Ƿ���ҪУ��ͻ�����')
        if ( TradeContext.I1NAMECHKFLAG == "1"):
            if (TradeContext.USERNAME != TradeContext.I1USERNAME):
                return ExitSubTrade( '9000', '�ͻ����Ʋ���ȷ,���ܽ���ע��' )

       #ǩԼ��ʽ
        if (TradeContext.SIGNUPMODE=="1"):
            return ExitSubTrade( '9000', '����ǩԼ��ʽ,�����޸�Э��' )

        
        #�޸ĸ���Э����Ϣ(����)
        if ( not UpdateCustInfo( ) ):
            return False

    else:

        AfaLoggerFunc.tradeInfo('>>ע������Э����Ϣ')

       #ǩԼ��ʽ
        if (TradeContext.SIGNUPMODE=="1"):
            
            AfaLoggerFunc.tradeInfo('>>>ǩԼ��ʽ����������Ҫ����ҵ���н���')

            #ϵͳ��ʶ
            TradeContext.sysId = TradeContext.I1APPNO
            
            #��ʹ��ת��������
            TradeContext.__respFlag__='0'
    
            AfaAfeFunc.CommAfe()

            if TradeContext.errorCode!='0000' :
                return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )

        #ע������Э����Ϣ(����)
        if ( not DeleteCustInfo( ) ):
            return False

        
    AfaLoggerFunc.tradeInfo('**********ά��������Ϣ(8406)����**********')


    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True



#�жϸ���Э���Ƿ���Ч
def ChkCustInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>�жϸ���Э���Ƿ���Ч')

    try:
        sql = "SELECT USERNAME,IDTYPE,IDCODE,PROTOCOLNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "       #ҵ����
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND ("      #��λ���
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.I1BUSIUSERNO + "'" + " OR "        #�̻��ͻ����
        sql = sql + "BANKUSERNO=" + "'" + TradeContext.I1BANKUSERNO + "'" + " OR "        #���пͻ����
        sql = sql + "ACCNO="      + "'" + TradeContext.I1ACCNO      + "'" + ") AND "      #�����˺�
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                 #״̬


        AfaLoggerFunc.tradeInfo( sql )


        records = AfaDBFunc.SelectSql( sql )
        if ( len(records) == 0 ):
            return ExitSubTrade('9000','û�иÿͻ���Ϣ,���ܽ�����صĲ���')


        #����None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.USERNAME  = str(records[0][0])
        TradeContext.IDTYPE    = str(records[0][1])
        TradeContext.IDCODE    = str(records[0][2])
        rPROTOCOLNO            = str(records[0][3])
        TradeContext.ACCSTATUS = "0"

        if ( rPROTOCOLNO != TradeContext.I1PROTOCOLNO ):
            return ExitSubTrade( '9000', '�����޸ĸ���Э�����')

        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�жϸ���Э����Ϣ�Ƿ�����쳣')


#�޸ĸ���Э����Ϣ(����)
def UpdateCustInfo( ):


    AfaLoggerFunc.tradeInfo(">>>�޸ĸ���Э����Ϣ(����)")


    try:
        sql = "UPDATE ABDT_CUSTINFO SET "
#       sql = sql + "APPNO='"           + TradeContext.I1APPNO                           + "',"        #ҵ����
#       sql = sql + "BUSINO='"          + TradeContext.I1BUSINO                          + "',"        #��λ���
        sql = sql + "BUSIUSERNO='"      + TradeContext.I1BUSIUSERNO                      + "',"        #�̻��ͻ����
        sql = sql + "BUSIUSERAPPNO='"   + TradeContext.I1BUSIUSERAPPNO                   + "',"        #�̻��ͻ�Ӧ�ñ��
        sql = sql + "BANKUSERNO='"      + TradeContext.I1BANKUSERNO                      + "',"        #���пͻ����
        sql = sql + "VOUHTYPE='"        + TradeContext.I1VOUHTYPE                        + "',"        #ƾ֤����
        sql = sql + "VOUHNO='"          + TradeContext.I1VOUHNO                          + "',"        #ƾ֤��
        sql = sql + "ACCNO='"           + TradeContext.I1ACCNO                           + "',"        #���ڴ���ʺ�
        sql = sql + "SUBACCNO='"        + TradeContext.I1SUBACCNO                        + "',"        #���ʺ�
        sql = sql + "CURRTYPE='"        + TradeContext.I1CURRTYPE                        + "',"        #����
        sql = sql + "LIMITAMT='"        + TradeContext.I1LIMITAMT                        + "',"        #�����޶�
        sql = sql + "PARTFLAG='"        + TradeContext.I1PARTFLAG                        + "',"        #���ֿۿ��־
#       sql = sql + "PROTOCOLNO='"      + TradeContext.I1PROTOCOLNO                      + "',"        #Э����
        sql = sql + "CONTRACTDATE='"    + TradeContext.I1CONTRACTDATE                    + "',"        #ǩԼ����(��ͬ����)
        sql = sql + "STARTDATE='"       + TradeContext.I1STARTDATE                       + "',"        #��Ч����
        sql = sql + "ENDDATE='"         + TradeContext.I1ENDDATE                         + "',"        #ʧЧ����
        sql = sql + "PASSCHKFLAG='"     + TradeContext.I1PASSCHKFLAG                     + "',"        #������֤��־
        sql = sql + "PASSWD='"          + TradeContext.I1PASSWD                          + "',"        #����
        sql = sql + "IDCHKFLAG='"       + TradeContext.I1IDCHKFLAG                       + "',"        #֤����֤��־
        sql = sql + "IDTYPE='"          + TradeContext.IDTYPE                            + "',"        #֤������
        sql = sql + "IDCODE='"          + TradeContext.IDCODE                            + "',"        #֤������
        sql = sql + "NAMECHKFLAG='"     + TradeContext.I1NAMECHKFLAG                     + "',"        #������֤��־
        sql = sql + "USERNAME='"        + TradeContext.USERNAME                          + "',"        #�ͻ�����
        sql = sql + "TEL='"             + TradeContext.I1TEL                             + "',"        #��ϵ�绰
        sql = sql + "ADDRESS='"         + TradeContext.I1ADDRESS                         + "',"        #��ϵ��ַ
        sql = sql + "ZIPCODE='"         + TradeContext.I1ZIPCODE                         + "',"        #�ʱ�
        sql = sql + "EMAIL='"           + TradeContext.I1EMAIL                           + "',"        #��������
        sql = sql + "STATUS='"          + TradeContext.I1STATUS                          + "',"        #״̬
#       sql = sql + "ZONENO='"          + TradeContext.I1ZONENO                          + "',"        #������
#       sql = sql + "BRNO='"            + TradeContext.I1BRNO                            + "',"        #�����(��������)
#       sql = sql + "TELLERNO='"        + TradeContext.I1TELLERNO                        + "',"        #��Ա��
#       sql = sql + "INDATE='"          + TradeContext.I1INDATE                          + "',"        #¼������
#       sql = sql + "INTIME='"          + TradeContext.I1INTIME                          + "',"        #¼��ʱ��
        sql = sql + "NOTE1='"           + TradeContext.I1USID                            + "',"        #��ע1
        sql = sql + "NOTE2='"           + TradeContext.TranDate+TradeContext.TranTime    + "',"        #��ע2
        sql = sql + "NOTE3='"           + TradeContext.I1NOTE3                           + "',"        #��ע3
        sql = sql + "NOTE4='"           + TradeContext.I1NOTE4                           + "',"        #��ע4
        sql = sql + "NOTE5='"           + TradeContext.I1NOTE5                           + "'"         #��ע5

        sql = sql + " WHERE "

        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "            #ҵ�����
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND "            #��λ����
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND "            #��λ����
        sql = sql + "ZONENO="     + "'" + TradeContext.I1ZONENO     + "'" + " AND "            #��������
        sql = sql + "PROTOCOLNO=" + "'" + TradeContext.I1PROTOCOLNO + "'"                      #Э�����

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '�޸ĸ���Э����Ϣʧ��')


        AfaLoggerFunc.tradeInfo(">>>�ܹ��޸�[" + str(result) + "]����¼")


        TradeContext.tradeResponse.append(['O1USERNAME',     TradeContext.USERNAME])        #�û�����
        TradeContext.tradeResponse.append(['O1IDTYPE',       TradeContext.IDTYPE])          #֤������
        TradeContext.tradeResponse.append(['O1IDCODE',       TradeContext.IDCODE])          #֤������

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�޸ĸ���Э����Ϣ�쳣')

    
    
#ע������Э����Ϣ(����)
def DeleteCustInfo( ):

    AfaLoggerFunc.tradeInfo(">>>ע���ͻ���Ϣ(����)")

    try:

        AfaLoggerFunc.tradeInfo(">>>�޸�ע�����ں�ʱ��")

        sql = "UPDATE ABDT_CUSTINFO SET NOTE3='" + TradeContext.TranDate+TradeContext.TranTime + "'"

        sql = sql + " WHERE "

        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "        #ҵ�����
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND "        #��λ����
        sql = sql + "PROTOCOLNO=" + "'" + TradeContext.I1PROTOCOLNO + "'"                  #Э�����

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '�޸�ע�����ں�ʱ��ʧ��')
        
        AfaLoggerFunc.tradeInfo(">>>����Ҫ������Ϣ��¼�Ƶ�������Ϣ��ʷ����")

        sql = ""
        sql = "INSERT INTO ABDT_HIS_CUSTINFO SELECT * FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="       + "'" + TradeContext.I1APPNO      + "'" + " AND "        #ҵ�����
        sql = sql + "BUSINO="      + "'" + TradeContext.I1BUSINO     + "'" + " AND "        #��λ����
        sql = sql + "PROTOCOLNO="  + "'" + TradeContext.I1PROTOCOLNO + "'"                  #Э�����

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', 'ע������Э����Ϣʧ��(�ƶ�)')

        AfaLoggerFunc.tradeInfo(">>>�ܹ��ƶ�[" + str(result) + "]����¼")


        AfaLoggerFunc.tradeInfo(">>>ɾ���ڸ�����Ϣ���б�ע��������Ϣ��¼")
        sql = ""
        sql = "DELETE FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "        #ҵ�����
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND "        #��λ����
        sql = sql + "PROTOCOLNO=" + "'" + TradeContext.I1PROTOCOLNO + "'"                  #Э�����

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.DeleteSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', 'ע������Э����Ϣʧ��(ɾ��)')


        AfaLoggerFunc.tradeInfo(">>>�ܹ�ɾ��[" + str(result) + "]����¼")


        TradeContext.tradeResponse.append(['O1USERNAME',     TradeContext.USERNAME])       #�û�����
        TradeContext.tradeResponse.append(['O1IDTYPE',       TradeContext.IDTYPE])         #֤������
        TradeContext.tradeResponse.append(['O1IDCODE',       TradeContext.IDCODE])         #֤������

        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', 'ע������Э����Ϣ�쳣')



def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
