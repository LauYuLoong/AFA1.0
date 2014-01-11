# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ����ѯ����Э��
#===============================================================================
#   �����ļ�:   T001000_8405.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,AbdtFunc
from types import *


#=====================��ѯ������Ϣ==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********��ѯ������Ϣ(8405)��ʼ**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��



    #�жϵ�λЭ���Ƿ���Ч
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    try:
        sql = "SELECT * FROM ABDT_CUSTINFO WHERE "
        
        sql = sql + "STATUS="                 + "'" + "1"                          + "'"            #״̬(0:�쳣,1:����)

        #Э����
        if ( len(TradeContext.I1PROTOCOLNO) > 0 ):
            sql = sql + " AND PROTOCOLNO="    + "'" + TradeContext.I1PROTOCOLNO    + "'"            #Э����

        #ҵ����
        if ( len(TradeContext.I1APPNO) > 0 ):
            sql = sql + " AND APPNO="         + "'" + TradeContext.I1APPNO         + "'"            #ҵ����

        #��λ���
        if ( len(TradeContext.I1BUSINO) > 0 ):
            sql = sql + " AND BUSINO="        + "'" + TradeContext.I1BUSINO        + "'"            #��λ���

        #�̻��ͻ����
        if ( len(TradeContext.I1BUSIUSERNO) > 0 ):
            sql = sql + " AND BUSIUSERNO="    + "'" + TradeContext.I1BUSIUSERNO    + "'"            #�̻��ͻ����

#       #�̻��ͻ�Ӧ�ñ��
#       if ( len(TradeContext.I1BUSIUSERAPPNO) > 0 ):
#           sql = sql + " AND BUSIUSERAPPNO=" + "'" + TradeContext.I1BUSIUSERAPPNO + "'"            #�̻��ͻ�Ӧ�ñ��

        #���пͻ����
        if ( len(TradeContext.I1BANKUSERNO) > 0 ):
            sql = sql + " AND BANKUSERNO="    + "'" + TradeContext.I1BANKUSERNO    + "'"            #���пͻ����

#       #ƾ֤����
#       if ( len(TradeContext.I1VOUHTYPE) > 0 ):
#           sql = sql + " AND VOUHTYPE="      + "'" + TradeContext.I1VOUHTYPE      + "'"            #ƾ֤����
#
#       #ƾ֤��
#       if ( len(TradeContext.I1VOUHNO) > 0 ):
#           sql = sql + " AND VOUHNO="        + "'" + TradeContext.I1VOUHNO        + "'"            #ƾ֤����

        #�����ʺ�
        if ( len(TradeContext.I1ACCNO) > 0 ):
            sql = sql + " AND ACCNO="         + "'" + TradeContext.I1ACCNO         + "'"            #�����ʺ�

#       #���ʺ�
#       if ( len(TradeContext.I1SUBACCNO) > 0 ):
#           sql = sql + " AND SUBACCNO="      + "'" + TradeContext.I1SUBACCNO      + "'"            #���ʺ�
#
#       #����
#       if ( len(TradeContext.I1CURRTYPE) > 0 ):
#           sql = sql + " AND CURRTYPE="      + "'" + TradeContext.I1CURRTYPE      + "'"            #����
#
#       #֤������
#       if ( len(TradeContext.I1IDCODE) > 0 ):
#           sql = sql + " AND IDCODE="        + "'" + TradeContext.I1IDCODE        + "'"            #֤������
#
#       #�ͻ�����
#       if ( len(TradeContext.I1USERNAME) > 0 ):
#           sql = sql + " AND USERNAME="      + "'" + TradeContext.I1USERNAME      + "'"            #�ͻ�����

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ����Э����Ϣ�쳣' )
    
        if ( len(records) == 0 ):
            return ExitSubTrade( '9000', 'û����صĸ���Э����Ϣ')


        AfaLoggerFunc.tradeInfo(">>>�ܹ���ѯ[" + str(len(records)) + "]����¼")


        #�����¼��
        TradeContext.tradeResponse.append(['RECNUM',  str(len(records))])

        #����None
        AfaUtilTools.ListFilterNone( records )
            
        i = 0
        while ( i  < len(records) ):
            TradeContext.tradeResponse.append(['O1APPNO',           str(records[i][0])])    #ҵ����
            TradeContext.tradeResponse.append(['O1BUSINO',          str(records[i][1])])    #��λ���
            TradeContext.tradeResponse.append(['O1BUSIUSERNO',      str(records[i][2])])    #�̻��ͻ����
            TradeContext.tradeResponse.append(['O1BUSIUSERAPPNO',   str(records[i][3])])    #�̻��ͻ�Ӧ�ñ��
            TradeContext.tradeResponse.append(['O1BANKUSERNO',      str(records[i][4])])    #���пͻ����
            TradeContext.tradeResponse.append(['O1VOUHTYPE',        str(records[i][5])])    #ƾ֤����
            TradeContext.tradeResponse.append(['O1VOUHNO',          str(records[i][6])])    #ƾ֤��
            TradeContext.tradeResponse.append(['O1ACCNO',           str(records[i][7])])    #���ڴ���ʺ�
            TradeContext.tradeResponse.append(['O1SUBACCNO',        str(records[i][8])])    #���ʺ�
            TradeContext.tradeResponse.append(['O1CURRTYPE',        str(records[i][9])])    #����
            TradeContext.tradeResponse.append(['O1LIMITAMT',        str(records[i][10])])   #�����޶�
            TradeContext.tradeResponse.append(['O1PARTFLAG',        str(records[i][11])])   #���ֿۿ��־
            TradeContext.tradeResponse.append(['O1PROTOCOLNO',      str(records[i][12])])   #Э����
            TradeContext.tradeResponse.append(['O1CONTRACTDATE',    str(records[i][13])])   #ǩԼ����(��ͬ����)
            TradeContext.tradeResponse.append(['O1STARTDATE',       str(records[i][14])])   #��Ч����
            TradeContext.tradeResponse.append(['O1ENDDATE',         str(records[i][15])])   #ʧЧ����
            TradeContext.tradeResponse.append(['O1PASSCHKFLAG',     str(records[i][16])])   #������֤��־
            TradeContext.tradeResponse.append(['O1PASSWD',          str(records[i][17])])   #����
            TradeContext.tradeResponse.append(['O1IDCHKFLAG',       str(records[i][18])])   #֤����֤��־
            TradeContext.tradeResponse.append(['O1IDTYPE',          str(records[i][19])])   #֤������
            TradeContext.tradeResponse.append(['O1IDCODE',          str(records[i][20])])   #֤������
            TradeContext.tradeResponse.append(['O1NAMECHKFLAG',     str(records[i][21])])   #������֤��־
            TradeContext.tradeResponse.append(['O1USERNAME',        str(records[i][22])])   #�ͻ�����
            TradeContext.tradeResponse.append(['O1TEL',             str(records[i][23])])   #��ϵ�绰
            TradeContext.tradeResponse.append(['O1ADDRESS',         str(records[i][24])])   #��ϵ��ַ
            TradeContext.tradeResponse.append(['O1ZIPCODE',         str(records[i][25])])   #�ʱ�
            TradeContext.tradeResponse.append(['O1EMAIL',           str(records[i][26])])   #��������
            TradeContext.tradeResponse.append(['O1STATUS',          str(records[i][27])])   #״̬
            TradeContext.tradeResponse.append(['O1ZONENO',          str(records[i][28])])   #������
            TradeContext.tradeResponse.append(['O1BRNO',            str(records[i][29])])   #�����(��������)
            TradeContext.tradeResponse.append(['O1TELLERNO',        str(records[i][30])])   #��Ա��
            TradeContext.tradeResponse.append(['O1INDATE',          str(records[i][31])])   #¼������
            TradeContext.tradeResponse.append(['O1INTIME',          str(records[i][32])])   #¼��ʱ��
            TradeContext.tradeResponse.append(['O1NOTE1',           str(records[i][33])])   #��ע1
            TradeContext.tradeResponse.append(['O1NOTE2',           str(records[i][34])])   #��ע2
            TradeContext.tradeResponse.append(['O1NOTE3',           str(records[i][35])])   #��ע3
            TradeContext.tradeResponse.append(['O1NOTE4',           str(records[i][36])])   #��ע4
            TradeContext.tradeResponse.append(['O1NOTE5',           str(records[i][37])])   #��ע5
            i = i + 1


        AfaLoggerFunc.tradeInfo('**********��ѯ������Ϣ(8405)����**********')


        #����
        TradeContext.tradeResponse.append(['errorCode', '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '��ѯ����Э����Ϣ�쳣')




def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        