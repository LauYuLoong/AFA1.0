# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��������������ѯ
#===============================================================================
#   �����ļ�:   T001000_8490.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  CYG
#   �޸�ʱ��:   2009-10-29
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os
from types import *


#=====================������������ѯ==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********���������ʲ�ѯ(8490)��ʼ**********')

    TradeContext.O1AFAPDATE                =           TradeContext.TranDate    #��������
    TradeContext.O1AFAPTIME                =           TradeContext.TranTime    #��������

    #��ѯ��λ��Ϣ����õ�λ���
    try:
        sql = ""
        sql = "SELECT BUSINO FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "        #ҵ����
        sql = sql + "ACCNO="  + "'" + TradeContext.I1ACCNO  + "'"                  #�Թ��˻�
        
        AfaLoggerFunc.tradeInfo( sql )
        
        results = AfaDBFunc.SelectSql( sql )
        
        if ( results == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ��λ��Ϣ�쳣' )
        
        if ( len(results) <= 0 ):
            return ExitSubTrade( '9000', 'û�е�λ��Ϣ,���ܽ��д������')
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '��ѯ��λ��Ϣʧ��')

    busResult = []
    for i in range( 0, len(results) ):
        TradeContext.I1BUSINO = results[i][0]                               #��λ���
        #�жϵ�λЭ���Ƿ���Ч
        if ( ChkUnitInfo( ) ):
            #��У��ͨ���ĵ�λ��ű�������
            busResult.append(results[i][0])
            AfaLoggerFunc.tradeInfo( "[" + results[i][0] + "]��λЭ����Ч��У��ͨ��" )
        else:
            AfaLoggerFunc.tradeInfo( "[" + results[i][0] + "]��λЭ����Ч")

    #begin 20091130 ���������� 
    if( len(busResult) == 0 ):
        return ExitSubTrade( '9999', '��λЭ�鲻���ڣ��������˽���')
    #end

    try:
        sql = ""
        sql = "SELECT * FROM (select abdt_batchinfo.*,rownumber() over(order by batchno) as rn from ABDT_BATCHINFO WHERE "
        sql = sql + "APPNO="       + "'" + TradeContext.I1APPNO    + "'"    + " AND "          #ҵ����
        sql = sql + "BUSINO in ("
        for busino in busResult:
            sql = sql +  "'" + busino + "',"                                                   #��λ���
        sql = sql[0:-1] + ") AND "
        sql = sql + "BEGINDATE>="   + "'" + TradeContext.I1WORKDATE + "'"    + " AND "         #��ʼ����
        sql = sql + "ENDDATE<="     + "'" + TradeContext.I1ENDDATE + "') "                     #��������
        sql = sql + "as a1 where a1.rn >= " + TradeContext.I1STARTNO

        AfaLoggerFunc.tradeInfo( "��ѯ������Ϣsql:" + sql )
        
        #��ѯ����
        count = int(TradeContext.I1COUNT)

        records = AfaDBFunc.SelectSql( sql, count )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ������Ϣ���쳣' )

        if ( len(records) == 0 ):
            return ExitSubTrade( '9000', 'û�и�ί�кŵ�������Ϣ' )

        #����None
        AfaUtilTools.ListFilterNone( records )
        TradeContext.O2BATCHNO    = []
        TradeContext.O2APPNO      = []
        TradeContext.O2BUSINO     = []
        TradeContext.O2ZONENO     = []
        TradeContext.O2BRNO       = []
        TradeContext.O2USERNO     = []
        TradeContext.O2ADMINNO    = []
        TradeContext.O2TERMTYPE   = []
        TradeContext.O2FILENAME   = []
        TradeContext.O2INDATE     = []
        TradeContext.O2INTIME     = []
        TradeContext.O2BATCHDATE  = []
        TradeContext.O2BATCHTIME  = []
        TradeContext.O2TOTALNUM   = []
        TradeContext.O2TOTALAMT   = []
        TradeContext.O2SUCCAMT    = []
        TradeContext.O2FAILNUM    = []
        TradeContext.O2FAILAMT    = []
        TradeContext.O2SUCCNUM    = []
        TradeContext.O2UNSETNUM   = []
        TradeContext.O2UNSETAMT   = []
        TradeContext.O2STATUS     = []
        TradeContext.O2BEGINDATE  = []
        TradeContext.O2ENDDATE    = []
        TradeContext.O2PROCMSG    = []
        TradeContext.O2NOTE1      = []
        TradeContext.O2NOTE2      = []
        TradeContext.O2NOTE3      = []
        TradeContext.O2NOTE4      = []
        TradeContext.O2NOTE5      = []
        for i in range(0, len(records)):
            TradeContext.O2BATCHNO.append(         str(records[i][0])  )         #ί�к�(���κ�)
            TradeContext.O2APPNO.append(           str(records[i][1])  )         #ҵ����
            TradeContext.O2BUSINO.append(          str(records[i][2])  )         #��λ���
            TradeContext.O2ZONENO.append(          str(records[i][3])  )         #������
            TradeContext.O2BRNO.append(            str(records[i][4])  )         #�����
            TradeContext.O2USERNO.append(          str(records[i][5])  )         #����Ա
            TradeContext.O2ADMINNO.append(         str(records[i][6])  )         #����Ա
            TradeContext.O2TERMTYPE.append(        str(records[i][7])  )         #�ն�����
            TradeContext.O2FILENAME.append(        str(records[i][8])  )         #�ϴ��ļ���
            TradeContext.O2INDATE.append(          str(records[i][9])  )         #ί������
            TradeContext.O2INTIME.append(          str(records[i][10]) )         #ί��ʱ��
            TradeContext.O2BATCHDATE.append(       str(records[i][11]) )         #�ύ����
            TradeContext.O2BATCHTIME.append(       str(records[i][12]) )         #�ύʱ��
            TradeContext.O2TOTALNUM.append(        str(records[i][13]) )         #�ܱ���
            TradeContext.O2TOTALAMT.append(        str(records[i][14]) )         #�ܽ��
            TradeContext.O2SUCCNUM.append(         str(records[i][15]) )         #�ɹ�����
            TradeContext.O2SUCCAMT.append(         str(records[i][16]) )         #�ɹ����
            TradeContext.O2FAILNUM.append(         str(records[i][17]) )         #ʧ�ܱ���
            TradeContext.O2FAILAMT.append(         str(records[i][18]) )         #ʧ�ܽ��
            TradeContext.O2UNSETNUM.append(        '0')                          #δ�������
            TradeContext.O2UNSETAMT.append(        '0.00')                       #δ������
            TradeContext.O2STATUS.append(          str(records[i][19]) )         #״̬
            TradeContext.O2BEGINDATE.append(       str(records[i][20]) )         #��Ч����
            TradeContext.O2ENDDATE.append(         str(records[i][21]) )         #ʧЧ����
            TradeContext.O2PROCMSG.append(         str(records[i][22]) )         #������Ϣ
            TradeContext.O2NOTE1.append(           str(records[i][23]) )         #��ע1
            TradeContext.O2NOTE2.append(           str(records[i][24]) )         #��ע2
            TradeContext.O2NOTE3.append(           str(records[i][25]) )         #��ע3
            TradeContext.O2NOTE4.append(           str(records[i][26]) )        #��ע4
            TradeContext.O2NOTE5.append(           str(records[i][27]) )        #��ע5

        TradeContext.O1STARTNO =  TradeContext.I1STARTNO                                  #���β�ѯ��ʼ����
        TradeContext.O1COUNT   =   str(len(records))                                      #���β�ѯ����
        
        #��ѯ���������ı���
        sql = ""
        sql = sql + "select count(*) from abdt_batchinfo where "
        sql = sql + "APPNO="        + "'" + TradeContext.I1APPNO  + "'"    + " AND "         #ҵ����
        sql = sql + "BUSINO in ("
        for busino in busResult:
            sql = sql +  "'" + busino + "',"                                                 #��λ���
        sql = sql[0:-1] + ") AND "
        sql = sql + "BEGINDATE>="   + "'" + TradeContext.I1WORKDATE + "'"  + " AND "         #��ʼ����
        sql = sql + "ENDDATE<="     + "'" + TradeContext.I1ENDDATE + "' "                    #��������
        
        AfaLoggerFunc.tradeInfo( sql )
        
        rcount = AfaDBFunc.SelectSql( sql )
        if ( rcount == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ������Ϣ���쳣' )
        
        if ( rcount[0][0] == None ):
            return ExitSubTrade( '9000', 'û�и�ί�кŵ�������Ϣ' )
        
        TradeContext.O1TOTALCO = str(rcount[0][0])                                     #������������
        

        AfaLoggerFunc.tradeInfo('**********���������ʲ�ѯ(8490)����**********')


        #����
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '��ѯ�ɹ�'
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '������������ѯ,���ݿ��쳣' )
        
        
#�жϵ�λЭ���Ƿ���Ч
def ChkUnitInfo( ):


    AfaLoggerFunc.tradeInfo('>>>�жϵ�λЭ���Ƿ���Ч')


    try:
        sql = ""
        sql = "SELECT SIGNUPMODE,GETUSERNOMODE,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO,AGENTTYPE,VOUHNO FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "        #ҵ����
        sql = sql + "BUSINO=" + "'" + TradeContext.I1BUSINO + "'" + " AND "        #��λ���
        sql = sql + "STATUS=" + "'" + "1"                   + "'"                  #״̬

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ��λЭ����Ϣ�쳣' )
    
        if ( len(records) <= 0 ):
            return ExitSubTrade( '9000', 'û�е�λЭ����Ϣ,���ܽ��д������')

        #����None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.SIGNUPMODE    = str(records[0][0])                             #ǩԼ��ʽ
        TradeContext.GETUSERNOMODE = str(records[0][1])                             #�̻��ͻ���Ż�ȡ��ʽ
        TradeContext.STARTDATE     = str(records[0][2])                             #��Ч����
        TradeContext.ENDDATE       = str(records[0][3])                             #ʧЧ����
        TradeContext.STARTTIME     = str(records[0][4])                             #����ʼʱ��
        TradeContext.ENDTIME       = str(records[0][5])                             #������ֹʱ��
        TradeContext.ACCNO         = str(records[0][6])                             #�Թ��˻�
        TradeContext.AGENTTYPE     = str(records[0][7])                             #ί�з�ʽ
        TradeContext.VOUHNO        = str(records[0][8])                             #ƾ֤��(�ڲ��ʻ�)

        AfaLoggerFunc.tradeInfo( "TranDate=[" + TradeContext.TranDate + "]" )

        if ( (TradeContext.STARTDATE > TradeContext.TranDate) or (TradeContext.TranDate > TradeContext.ENDDATE) ):
            return ExitSubTrade( '9000', '�õ�λί��Э�黹û����Ч���ѹ���Ч��')

        if ( (TradeContext.STARTTIME > TradeContext.TranTime) or (TradeContext.TranTime > TradeContext.ENDTIME) ):
            return ExitSubTrade( '9000', '�Ѿ�������ϵͳ�ķ���ʱ��,��ҵ�������[' + s_StartDate + ']-[' + s_EndDate + ']ʱ�������')

        if ((TradeContext.SIGNUPMODE=="1") and (TradeContext.GETUSERNOMODE=="1")):
            #���͵�ͨѶǰ�ò��ӵ�������ȡЭ��
            return True

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�жϵ�λЭ����Ϣ�Ƿ����ʧ��')


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        
