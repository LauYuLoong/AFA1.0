# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��¼����ҵ��Ϣ
#===============================================================================
#   �����ļ�:   T001000_8423.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,NGSFAbdtFunc,AfaAfeFunc
from types import *

#=====================¼����ҵ��Ϣ==============================================
def TrxMain( ):
    AfaLoggerFunc.tradeInfo('**********¼����ҵ��Ϣ(8423)��ʼ**********')

    #TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    #TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��
    
    #�жϵ�λЭ���Ƿ���Ч
    if ( not NGSFAbdtFunc.ChkUnitInfo( ) ):
        return False

    #�ж���ҵЭ���Ƿ����
    if ( not ChkCustInfo( ) ):
        return False

    #��ѯ�˻���Ϣ(����)
    if ( not NGSFAbdtFunc.QueryAccInfo( ) ):
        return False
        
    #�Ϸ���У��
    AfaLoggerFunc.tradeInfo('>>>�ж������˻�״̬')
    if ( TradeContext.ACCSTATUS != "0"):
        return ExitSubTrade( '9000', '�ͻ������˻�״̬�쳣,���ܽ���ע��' )

    #AfaLoggerFunc.tradeInfo('>>>�ж��Ƿ���ҪУ��֤������')
    #if ( TradeContext.I1IDCHKFLAG == "1" ):
    #    if (TradeContext.IDCODE != TradeContext.I1IDCODE):
    #        return ExitSubTrade( '9000', '�ͻ�֤�����벻��ȷ,���ܽ���ע��' )

    AfaLoggerFunc.tradeInfo('>>>�ж��Ƿ���ҪУ��ͻ�����')
    if (TradeContext.USERNAME != TradeContext.PayerName):
        return ExitSubTrade( '9000', '�ͻ����Ʋ���ȷ,���ܽ���ע��' )

    #�Զ�������ҵЭ����
    if ( AfaFunc.GetSerialno() < 0 ):
        return ExitSubTrade( '9000', '������ҵЭ����ʧ��' )

    #��֯��ҵЭ�����(�������� + �м�ҵ����ˮ��)
    TradeContext.Protocolno = TradeContext.TranDate + TradeContext.agentSerialno

    #ǩԼ��ʽ  ����ǩԼ
    #if (TradeContext.SIGNUPMODE=="1"):
    #    #ϵͳ��ʶ
    #    TradeContext.sysId = TradeContext.Appno + TradeContext.PayeeUnitno
    #
    #    #��ʹ��ת��������
    #    TradeContext.__respFlag__="0"
    #  
    #    AfaAfeFunc.CommAfe()
    #
    #    if TradeContext.errorCode!='0000' :
    #        return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )

    #������ҵЭ����Ϣ
    if ( not InsertCustInfo( ) ):
        return False

    AfaLoggerFunc.tradeInfo('**********¼����ҵ��Ϣ(8423)����**********')

    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True

#�ж���ҵЭ���Ƿ����
def ChkCustInfo( ):
    AfaLoggerFunc.tradeInfo('>>>�ж���ҵЭ���Ƿ����')

    try:
        sql = ""
        sql = "SELECT PROTOCOLNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.Appno        + "'" + " AND "       #ҵ����
        sql = sql + "BUSINO="     + "'" + TradeContext.PayeeUnitno  + "'" + " AND ("      #��λ���
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.PayerUnitno  + "'" + " OR "        #�̻��ͻ����
        sql = sql + "BANKUSERNO=" + "'" + TradeContext.PayerAccno[0:12] + "'" + " OR "        #���пͻ����
        sql = sql + "ACCNO="      + "'" + TradeContext.PayerAccno   + "'" + ") AND "      #�����˺�
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                 #״̬

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ��ҵЭ����Ϣ�쳣' )
    
        if ( len(records) > 0 ):
            return ExitSubTrade( '9000', '����ҵЭ���Ѿ���ע��,�����ٴν���ע��')

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�ж���ҵЭ����Ϣ�Ƿ�����쳣')

#������ҵЭ����Ϣ
def InsertCustInfo( ):
    AfaLoggerFunc.tradeInfo('>>>������ҵЭ����Ϣ')

    try:

        sql = ""
        sql = "INSERT INTO ABDT_CUSTINFO("
        sql = sql + "APPNO,"
        sql = sql + "BUSINO,"
        sql = sql + "BUSIUSERNO,"
        sql = sql + "BUSIUSERAPPNO,"
        sql = sql + "BANKUSERNO,"
        sql = sql + "VOUHTYPE,"
        sql = sql + "VOUHNO,"
        sql = sql + "ACCNO,"
        sql = sql + "SUBACCNO,"
        sql = sql + "CURRTYPE,"
        sql = sql + "LIMITAMT,"
        sql = sql + "PARTFLAG,"
        sql = sql + "PROTOCOLNO,"
        sql = sql + "CONTRACTDATE,"
        sql = sql + "STARTDATE,"
        sql = sql + "ENDDATE,"
        sql = sql + "PASSCHKFLAG,"
        sql = sql + "PASSWD,"
        sql = sql + "IDCHKFLAG,"
        sql = sql + "IDTYPE,"
        sql = sql + "IDCODE,"
        sql = sql + "NAMECHKFLAG,"
        sql = sql + "USERNAME,"
        sql = sql + "TEL,"
        sql = sql + "ADDRESS,"
        sql = sql + "ZIPCODE,"
        sql = sql + "EMAIL,"
        sql = sql + "STATUS,"
        sql = sql + "ZONENO,"
        sql = sql + "BRNO,"
        sql = sql + "TELLERNO,"
        sql = sql + "INDATE,"
        sql = sql + "INTIME,"
        sql = sql + "NOTE1,"
        sql = sql + "NOTE2,"
        sql = sql + "NOTE3,"
        sql = sql + "NOTE4,"
        sql = sql + "NOTE5)"

        sql = sql + " VALUES ("

        sql = sql + "'" + TradeContext.Appno           + "',"        #ҵ����
        sql = sql + "'" + TradeContext.PayeeUnitno     + "',"        #��λ���
        sql = sql + "'" + TradeContext.PayerUnitno     + "',"        #�̻��ͻ����
        sql = sql + "'" + TradeContext.PayerUnitno     + "',"        #�̻��ͻ�Ӧ�ñ��
        sql = sql + "'" + TradeContext.PayerAccno[0:12]    + "',"    #���пͻ����
        sql = sql + "'" + '49'                         + "',"        #ƾ֤����
        sql = sql + "'" + TradeContext.PayerAccno[0:12]+ "',"        #ƾ֤��
        sql = sql + "'" + TradeContext.PayerAccno      + "',"        #���ڴ���ʺ�
        sql = sql + "'" + ' '                          + "',"        #���ʺ�
        sql = sql + "'" + '01'                         + "',"        #����
        sql = sql + "'" + '0'                          + "',"        #�����޶�
        sql = sql + "'" + TradeContext.PartFlag        + "',"        #���ֿۿ��־
        sql = sql + "'" + TradeContext.Protocolno      + "',"        #Э����
        sql = sql + "'" + TradeContext.ContractDate    + "',"        #ǩԼ����(��ͬ����)
        sql = sql + "'" + TradeContext.StartDate       + "',"        #��Ч����
        sql = sql + "'" + TradeContext.EndDate         + "',"        #ʧЧ����
        sql = sql + "'" + '0'                          + "',"        #������֤��־
        sql = sql + "'" + "****************"           + "',"        #����
        sql = sql + "'" + '0'                          + "',"        #֤����֤��־
        sql = sql + "'" + '01'                         + "',"        #֤������
        sql = sql + "'" + ' '                          + "',"        #֤������
        sql = sql + "'" + '0'                          + "',"        #������֤��־
        sql = sql + "'" + TradeContext.PayerName       + "',"        #�ͻ�����
        sql = sql + "'" + TradeContext.Tel             + "',"        #��ϵ�绰
        sql = sql + "'" + TradeContext.Address         + "',"        #��ϵ��ַ
        sql = sql + "'" + ' '                          + "',"        #�ʱ�
        sql = sql + "'" + ' '                          + "',"        #��������
        sql = sql + "'" + '1'                          + "',"        #״̬
        sql = sql + "'" + TradeContext.zoneno          + "',"        #������
        sql = sql + "'" + TradeContext.brno            + "',"        #�����(��������)
        sql = sql + "'" + TradeContext.tellerno        + "',"        #��Ա��
        sql = sql + "'" + TradeContext.TranDate        + "',"        #¼������
        sql = sql + "'" + TradeContext.TranTime        + "',"        #¼��ʱ��
        sql = sql + "'" + ' '                          + "',"        #��ע1
        sql = sql + "'" + TradeContext.UserName        + "',"        #���λ����
        sql = sql + "'" + TradeContext.PayeeAccno      + "',"        #�տλ�˺�
        sql = sql + "'" + ' '                          + "',"        #��ע4
        sql = sql + "'" + TradeContext.PayeeName       + "')"        #�տλ����
        

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '������ҵЭ����Ϣʧ��')

        #TradeContext.tradeResponse.append(['O1USERNAME',     TradeContext.USERNAME])        #�û�����
        #TradeContext.tradeResponse.append(['O1IDTYPE',       TradeContext.IDTYPE])          #֤������
        #TradeContext.tradeResponse.append(['O1IDCODE',       TradeContext.IDCODE])          #֤������
        #TradeContext.tradeResponse.append(['O1PROTOCOLNO',   TradeContext.PROTOCOLNO])      #Э���
        #TradeContext.tradeResponse.append(['O1WORKDATE',     TradeContext.TranDate])        #ע������
        #TradeContext.tradeResponse.append(['O1WORKTIME',     TradeContext.TranTime])        #ע������

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '������ҵЭ����Ϣ�쳣')

def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False