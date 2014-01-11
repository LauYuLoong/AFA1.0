# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��¼�������Ϣ
#===============================================================================
#   �����ļ�:   T001000_8404.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,AbdtFunc,AfaAfeFunc
from types import *


#=====================¼�������Ϣ==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********¼�������Ϣ(8404)��ʼ**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��


    #�жϵ�λЭ���Ƿ���Ч
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    #�жϸ���Э���Ƿ����
    if ( not ChkCustInfo( ) ):
        return False


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


    #�Զ����ɸ���Э����
    if ( AfaFunc.GetSerialno() < 0 ):
        return ExitSubTrade( '9000', '���ɸ���Э����ʧ��' )


    #��֯����Э�����(�������� + �м�ҵ����ˮ��)
    TradeContext.PROTOCOLNO = TradeContext.TranDate + TradeContext.agentSerialno


    #ǩԼ��ʽ
    if (TradeContext.SIGNUPMODE=="1"):
        
        #ϵͳ��ʶ
        TradeContext.sysId = TradeContext.I1APPNO + TradeContext.I1BUSINO

        #��ʹ��ת��������
        TradeContext.__respFlag__="0"
      
        AfaAfeFunc.CommAfe()

        if TradeContext.errorCode!='0000' :
            return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )

    #���Ӹ���Э����Ϣ
    if ( not InsertCustInfo( ) ):
        return False

           
    AfaLoggerFunc.tradeInfo('**********¼�������Ϣ(8404)����**********')


    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True



#�жϸ���Э���Ƿ����
def ChkCustInfo( ):

    AfaLoggerFunc.tradeInfo('>>>�жϸ���Э���Ƿ����')

    try:
        sql = ""
        sql = "SELECT PROTOCOLNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "       #ҵ����
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND ("      #��λ���
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.I1BUSIUSERNO + "'" + " OR "        #�̻��ͻ����
        sql = sql + "BANKUSERNO=" + "'" + TradeContext.I1BANKUSERNO + "'" + " OR "        #���пͻ����
        sql = sql + "ACCNO="      + "'" + TradeContext.I1ACCNO      + "'" + ") AND "      #�����˺�
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                 #״̬

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ����Э����Ϣ�쳣' )
    
        if ( len(records) > 0 ):
            return ExitSubTrade( '9000', '�ø���Э���Ѿ���ע��,�����ٴν���ע��')

        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�жϸ���Э����Ϣ�Ƿ�����쳣')


#���Ӹ���Э����Ϣ
def InsertCustInfo( ):

    AfaLoggerFunc.tradeInfo('>>>���Ӹ���Э����Ϣ')

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

        sql = sql + "'" + TradeContext.I1APPNO         + "',"        #ҵ����
        sql = sql + "'" + TradeContext.I1BUSINO        + "',"        #��λ���
        sql = sql + "'" + TradeContext.I1BUSIUSERNO    + "',"        #�̻��ͻ����
        sql = sql + "'" + TradeContext.I1BUSIUSERAPPNO + "',"       #�̻��ͻ�Ӧ�ñ��
        sql = sql + "'" + TradeContext.I1BANKUSERNO    + "',"        #���пͻ����
        sql = sql + "'" + TradeContext.I1VOUHTYPE      + "',"        #ƾ֤����
        sql = sql + "'" + TradeContext.I1VOUHNO        + "',"        #ƾ֤��
        sql = sql + "'" + TradeContext.I1ACCNO         + "',"        #���ڴ���ʺ�
        sql = sql + "'" + TradeContext.I1SUBACCNO      + "',"        #���ʺ�
        sql = sql + "'" + TradeContext.I1CURRTYPE      + "',"        #����
        sql = sql + "'" + TradeContext.I1LIMITAMT      + "',"        #�����޶�
        sql = sql + "'" + TradeContext.I1PARTFLAG      + "',"        #���ֿۿ��־
        sql = sql + "'" + TradeContext.PROTOCOLNO      + "',"        #Э����
        sql = sql + "'" + TradeContext.I1CONTRACTDATE  + "',"        #ǩԼ����(��ͬ����)
        sql = sql + "'" + TradeContext.I1STARTDATE     + "',"        #��Ч����
        sql = sql + "'" + TradeContext.I1ENDDATE       + "',"        #ʧЧ����
        sql = sql + "'" + TradeContext.I1PASSCHKFLAG   + "',"        #������֤��־
        sql = sql + "'" + "****************"           + "',"        #����
        sql = sql + "'" + TradeContext.I1IDCHKFLAG     + "',"        #֤����֤��־
        sql = sql + "'" + TradeContext.IDTYPE          + "',"        #֤������
        sql = sql + "'" + TradeContext.IDCODE          + "',"        #֤������
        sql = sql + "'" + TradeContext.I1NAMECHKFLAG   + "',"        #������֤��־
        sql = sql + "'" + TradeContext.USERNAME        + "',"        #�ͻ�����
        sql = sql + "'" + TradeContext.I1TEL           + "',"        #��ϵ�绰
        sql = sql + "'" + TradeContext.I1ADDRESS       + "',"        #��ϵ��ַ
        sql = sql + "'" + TradeContext.I1ZIPCODE       + "',"        #�ʱ�
        sql = sql + "'" + TradeContext.I1EMAIL         + "',"        #��������
        sql = sql + "'" + TradeContext.I1STATUS        + "',"        #״̬
        sql = sql + "'" + TradeContext.I1ZONENO        + "',"        #������
        sql = sql + "'" + TradeContext.I1SBNO          + "',"        #�����(��������)
        sql = sql + "'" + TradeContext.I1USID          + "',"        #��Ա��
        sql = sql + "'" + TradeContext.TranDate        + "',"        #¼������
        sql = sql + "'" + TradeContext.TranTime        + "',"        #¼��ʱ��
        sql = sql + "'" + TradeContext.I1NOTE1         + "',"        #��ע1
        sql = sql + "'" + TradeContext.I1NOTE2         + "',"        #��ע2
        sql = sql + "'" + TradeContext.I1NOTE3         + "',"        #��ע3
        sql = sql + "'" + TradeContext.I1NOTE4         + "',"        #��ע4
        sql = sql + "'" + TradeContext.I1NOTE5         + "')"        #��ע5

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '���Ӹ���Э����Ϣʧ��')


        TradeContext.tradeResponse.append(['O1USERNAME',     TradeContext.USERNAME])        #�û�����
        TradeContext.tradeResponse.append(['O1IDTYPE',       TradeContext.IDTYPE])          #֤������
        TradeContext.tradeResponse.append(['O1IDCODE',       TradeContext.IDCODE])          #֤������
        TradeContext.tradeResponse.append(['O1PROTOCOLNO',   TradeContext.PROTOCOLNO])      #Э���
        TradeContext.tradeResponse.append(['O1WORKDATE',     TradeContext.TranDate])        #ע������
        TradeContext.tradeResponse.append(['O1WORKTIME',     TradeContext.TranTime])        #ע������

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '���Ӹ���Э����Ϣ�쳣')


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        