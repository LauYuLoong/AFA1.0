# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.
#=================================================================
#   �����ļ�:   3001_8443.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaLoggerFunc, AfaDBFunc

from types import *

def SubModuleMainFst():

    TradeContext.__agentEigen__ = '0'   #�ӱ��־

    #������������У��������˽���
    AfaLoggerFunc.tradeInfo('�����Ƿ���������')

    sqlstr = "select brno from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.brno + "'"

    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None:
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "�������ݿ��쳣"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False

    if( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���������У��������˽���"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False

    #���ȴӿ���в�ѯ�ɿ����ţ�������ҵ��򷵻��Ѿ��ɷѵĴ���
    AfaLoggerFunc.tradeInfo('�ɿ����Ƿ��Ѿ��ɷ�')

    sqlstr = "select flag from fs_fc76 where afc001='" + TradeContext.AFC001 + "'"

    #===�����������б����ֶ�,�ź��޸�===
    sqlstr = sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if ( len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( "û�в��ҵ��ɿ����ſ��Խɷ�"+sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )

    else:
        if records[0][0]   ==  '0':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0001','�Ѿ����ҵ��˽������ţ������ٽɷ�'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        elif records[0][0]   ==  '1':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0002',"�ɿ����ѳ������ɽɷ�"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        else:
            TradeContext.errorCode,TradeContext.errorMsg  =   '0003',"�ɿ���״̬λ�쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False


    #��ѯ�ɿ�����,���ж�Ӧ��ˮ�Ƿ��Ѿ���¼��
    AfaLoggerFunc.tradeInfo('�Ƿ��Ѿ���¼��')
    for serNo in TradeContext.AFC401.split(':') :
        sqlstr  =   "select * from fs_fc84 where afc001='" + TradeContext.AFC001 + "' and afc401 like '%" + serNo + "%'"

        AfaLoggerFunc.tradeInfo( sqlstr )
        records = AfaDBFunc.SelectSql( sqlstr )
        if( len( records) > 0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "�ýɿ����Ѿ���¼�������ٴβ�¼"
            return False

    AfaLoggerFunc.tradeInfo( '********************���벹¼���ݱ�ʼ*******************' )

    #-----------------------���ݵ�λ�������û�ȡ������Ϣ----------------------------
    sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
    sqlstr      =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        sys.exit(1)

    elif len(records) > 1:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ��Ϣ���쳣:һ����λ��Ŷ�Ӧ�˶��������Ϣ"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        sys.exit(1)

    TradeContext.AAA010     =   records[0][0].strip()
    TradeContext.AFA101     =   records[0][1].strip()

    #TradeContext.AAA010 =   "0000000000"
    TradeContext.AAA011 =   ""
    TradeContext.AFC016 =   TradeContext.brno

    # ----------------------------��ʼƱ����ϢУ��-------------------------------

    #�Ƿ�Ʊ��У��
    piaoNo      =   TradeContext.AFC001[0:9]
    aaz010      =   TradeContext.AAA010             #������������
    sqlstr      =   "select * from fs_dpz_gl where fczqhnm='" + aaz010 + "'"
    AfaLoggerFunc.tradeInfo( sqlstr )
    records     =   AfaDBFunc.SelectSql(sqlstr)

    #=====add by pgt 20090423 ����ǰ̨��������У���־���ж��Ƿ����У��====
    if (len(records) > 0   and  (TradeContext.CKMD == "1")):

        #����ģʽ
        if (TradeContext.existVariable('AFA091' ) and len(TradeContext.AFA091)>0):
            AfaLoggerFunc.tradeInfo( "��ƱУ��--����ģʽ" )
            sqlstr  =   "select afa090 from fs_fa20 where afa091='" + TradeContext.AFA091 + "' and BUSINO='" + TradeContext.busiNo + "'"
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None  or len(records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "���ݿ��쳣,FS_FA20��"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            afa090  =   records[0][0]           #��������

            sqlstr  =   "select count(*) from fs_dpz_gl where fdwdm='" + afa090 + "' and fqshm<='" + piaoNo + "' and fqzhm>='" + piaoNo + "'"

            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None  ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "��ƱУ���쳣"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            if  int(records[0][0]) == 0 :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "�Ǳ�����Ʊ��,����Ʊ��"
                return False

        else:
            #�Ǵ���ģʽ
            AfaLoggerFunc.tradeInfo( "��ƱУ��--�Ǵ���ģʽ" )
            sqlstr  =   "select count(*) from (select distinct b.AFA051 from FS_DPZ_GL a,fs_fa15 b where a.fdwdm=b.AFA050 and a.FQSHM<='" + piaoNo + "' and a.FQZHM>='" + piaoNo +  "'" + \
            " union all select distinct c.AFA051 from FS_DPZ_GL a,fs_fa21 b,fs_fa15 c where a.FQSHM<='" + piaoNo + "' and a.FQZHM>='" + piaoNo + "' and a.fdwdm=b.AFA050 and b.AFA050=c.AFA050) a where locate(a.afa051, '" + TradeContext.AFA051 + "')=1"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None  ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "��ƱУ���쳣"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            if  int(records[0][0]) == 0 :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "�Ǳ�ִ�յ�λƱ��,����Ʊ��"
                return False

    AfaLoggerFunc.tradeInfo("��λ�ڴ˿�Ʊ�������Ƿ���Ȩ��ȡ����Ŀ")


    #��λ�����Ƿ�Ϸ�
    sql         =   "select aaz006,aaz007,afa050,AAZ002 from fs_fa15 where afa051='" + TradeContext.AFA051 + "' and BUSINO='" + TradeContext.busiNo + "'"
    sql  =  sql + " and aaa010='" + TradeContext.AAA010 + "' order by aaz002 desc"

    AfaLoggerFunc.tradeInfo(sql)
    records     =   AfaDBFunc.SelectSql( sql )
    if ( records == None ):
        AfaLoggerFunc.tradeInfo(sql)
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ݿ��쳣:��ѯ��λ��Ϣ��"
        AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
        return False

    if ( len(records) == 0 ):
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�д˵�λ"
        AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
        return False
    else:
        iFlag=0
        if (records[0][3]!='1'):
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ����ĩ��"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        if  (records[0][0] <= TradeContext.AFC005 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC005)  :
            iFlag=1
        if iFlag==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ�Ѿ���Ч"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        #���浥λ����
        afa050  =   records[0][2]
        AfaLoggerFunc.tradeInfo( afa050 )

    for afa031 in TradeContext.AFA031.split( "^" ):
        #��Ŀ�����Ƿ�Ϸ�
        sql         =   "select aaz006,aaz007,AFA030,AAZ002 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo +  "' order by aaz006 desc"
        AfaLoggerFunc.tradeInfo(sql)
        records     =   AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeInfo(sql)
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ݿ��쳣:��ѯ��Ŀ��Ϣ��"
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            return False

        if ( len(records) == 0 ):
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�д���Ŀ%s" %afa031
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            return False
        else:
            iFlag=0
            if  (records[0][0] <= TradeContext.AFC005 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC005)  :
                iFlag=1

            if iFlag==0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��Ŀ%s�Ѿ���Ч" %afa031
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            #�����շ�����
            afa030  =   records[0][2]
            AfaLoggerFunc.tradeInfo( afa030 )

        #��λ�ڴ˿�Ʊ�������Ƿ���Ȩ��ȡ����Ŀ
        sql         =   "select aaz006,aaz007 from fs_fa16 where  afa030='" + afa030 + "' and afa050='" + afa050 + "' and BUSINO='" + TradeContext.busiNo + "'"
        AfaLoggerFunc.tradeInfo(sql)
        records     =   AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeInfo(sql)
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ݿ��쳣:��ѯ��λ��Ŀ��ϵ��Ϣ��"
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            return False

        if ( len(records) == 0 ):
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�д˵�λ��Ŀ%s��ϵ" %afa031
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            return False
        else:
            iFlag=0
            for i in range( len(records) ) :
                if  (records[0][0] <= TradeContext.AFC005 ) and (len(records[0][1])==0 or records[i][1] >= TradeContext.AFC005) :
                    iFlag=1
            if iFlag==0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ��Ŀ%s��ϵ�Ѿ���Ч"  %afa031
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

        #���Ϊ����ģʽ����Ӧ����������¼�뵽ϵͳ�У���У�鵱ǰ��Ʊ�����ڣ��˵�λ��Ŀ�Ƿ����ڴ˴���
        if (TradeContext.existVariable('AFA091' ) and len(TradeContext.AFA091)>0):
            #���մ����뵥λ��Ŀ���ձ�
            sql         =   "select aaz006,aaz007 from fs_fa21,fs_fa20 where  fs_fa21.AFA090=fs_fa20.AFA090 and   fs_fa20.AFA091='" + TradeContext.AFA091 + "' and fs_fa21.afa030='" + afa030 + "' and fs_fa21.afa050='" + afa050 + "'"
            AfaLoggerFunc.tradeInfo(sql)
            records     =   AfaDBFunc.SelectSql( sql )
            if ( records == None ):
                AfaLoggerFunc.tradeInfo(sql)
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ݿ��쳣:��ѯ���մ����뵥λ��Ŀ���ձ�"
                AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
                return False

            if ( len(records) == 0 ):
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�д����մ����뵥λ��Ŀ���չ�ϵ"
                AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
                return False
            else:
                iFlag=0
                for i in range( len(records) ) :
                    if  (records[0][0] <= TradeContext.AFC005 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC005) :
                        iFlag=1
                if iFlag==0 :
                    TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���մ����뵥λ��Ŀ��ϵ�Ѿ���Ч"
                    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                    return False

    #-------------------------������-----------------------------------------------
    AfaLoggerFunc.tradeInfo("������")

    AfaLoggerFunc.tradeInfo("�����־AFC187:"+TradeContext.AFC187)

    #���� :����Ϊ100
    if (TradeContext.AFC187=="100"):
        AfaLoggerFunc.tradeInfo("����")

        for afa031 in TradeContext.AFA031.split( "^" ):
            i        =   TradeContext.AFA031.split( "^" ).index(afa031)

            sqlstr   =  "select afa038,afa039,AFA041 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if ( records == None  ):
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ݿ��쳣�������շ���Ŀ��"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            if len(records) == 0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�д��շ���Ŀ��Ϣ"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:
                #1 ���<����*��׼����
                if records[0][0].strip() == '0' and  records[0][1].strip() == '0' :
                    pass
                else:
                    inputAmt    =   float( (TradeContext.AFC011.split("^"))[i] )    #������
                    maxAmt      =   float( records[0][0] ) * float( (TradeContext.AFC010.split("^"))[i] )    #�����
                    minAmt      =   float( records[0][1] ) * float( (TradeContext.AFC010.split("^"))[i] )    #��С���

                    AfaLoggerFunc.tradeInfo("��ǰ��Ŀ���ޣ�" + str(maxAmt))
                    AfaLoggerFunc.tradeInfo("��ǰ��Ŀ���ޣ�" + str(minAmt))
                    AfaLoggerFunc.tradeInfo("�����" + str(inputAmt))

                    #=====����ǰ̨������У���ʾ�ж��Ƿ���н���ж�pgt 20090423====
                    if TradeContext.CKMD == '1':
                        if minAmt <= inputAmt :
                            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','��Ŀ%s���������' %afa031
                            return False
                #2 ���������С�ڵ��ڱ����ֳɽ��
                #3 �ɿ���ɷ�ʱ��
                d1 = datetime.datetime(int(TradeContext.workDate[0:4]),int( TradeContext.workDate[4:6]), int(TradeContext.workDate[6:8]))
                d2 = datetime.datetime(int(TradeContext.AFC005[0:4]), int(TradeContext.AFC005[5:7]), int(TradeContext.AFC005[8:10]))
                AfaLoggerFunc.tradeInfo(str((d1 - d2).days))
                if (d1 - d2).days >5 or (d1 - d2).days >records[0][2]: #�ɿ��鱾��ɷ�ʱ��Ϊ5��
                    TradeContext.errorCode,TradeContext.errorMsg    =   '0001','�Ѿ������ɷ�ʱ�ޣ���Ŀ%s' %afa031
                    return False
                #4 ����Ŀ��FA13�����ж�����Ŀ��Ϣʱ������ݽɿ���Ŀ�Ʊ��������Ŀ�������ڿ�Ʊ������Ч��������Ŀ��Ϣ

    #���л��:���л��200
    #��Ϊ�޷�ȷ�������������Բ�У�����
    #���Ϊ����ģʽ����Ӧ����������¼�뵽ϵͳ�У���У�鵱ǰ��Ʊ�����ڣ��˵�λ��Ŀ�Ƿ����ڴ˴�����
    elif (TradeContext.AFC187=="200"):
        AfaLoggerFunc.tradeInfo("���л��")

    #ֱ�ӽɿ�Ĭ��300
    else:
        for afa031 in TradeContext.AFA031.split( "^" ):
            i        =   TradeContext.AFA031.split( "^" ).index(afa031)
            sqlstr   =  "select afa038,afa039 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo +  "' order by aaz006 desc"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if ( records == None  ):
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ݿ��쳣�������շ���Ŀ��"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            if len(records) == 0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�д��շ���Ŀ��Ϣ"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:
                if records[0][0].strip() == '0' and  records[0][1].strip() == '0' :
                    pass
                else:
                    inputAmt    =   float( (TradeContext.AFC011.split("^"))[i] )    #������
                    maxAmt      =   float( records[0][0] ) * float( (TradeContext.AFC010.split("^"))[i] )    #�����
                    minAmt      =   float( records[0][1] ) * float( (TradeContext.AFC010.split("^"))[i] )    #��С���

                    AfaLoggerFunc.tradeInfo("��ǰ��Ŀ���ޣ�" + str(maxAmt))
                    AfaLoggerFunc.tradeInfo("��ǰ��Ŀ���ޣ�" + str(minAmt))
                    AfaLoggerFunc.tradeInfo("�����" + str(inputAmt))

                    #=====����ǰ̨��������У���־�ж��Ƿ���н��У�� pgt 20090414====
                    if TradeContext.CKMD == '1':
                        if minAmt > inputAmt or inputAmt  >  maxAmt  :
                            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','��Ŀ%s���������' %afa031
                            return False

        #AfaLoggerFunc.tradeInfo("������:"  + TradeContext.AFC011 )

    #���ܵ��첹¼
    for serno in TradeContext.AFC401.split(":"):
        sqlstr          =   "select date from fs_fc74 where afc401='" + serno + "' and afc015='" + TradeContext.AFC015 + "'"
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "���Ҳ�¼����ʧ��"
            return False

        if  records[0][0] == TradeContext.workDate :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "���ܵ��첹¼,����ղ�¼"
            return False

    #------------------�����ܽ��-----------------
    amount      =   0.0
    for fee in TradeContext.AFC011.split('^'):
        amount  =   amount + float(fee)

    TradeContext.payAmount  =   str( amount )
    AfaLoggerFunc.tradeInfo( '�ܽ�' + TradeContext.payAmount )

    sqlstr  =   "insert into FS_FC84(AFC401,AAA010,AFC001,AFA031,AFA051,AFA101,AAA011,AFC002,AFC003,AFC004,  \
    AFC005,AFC006,AFC007,AFC008,AFC009,AFC010,AFC011,AMOUNT,AFC012,AFC013,AFC015,AFC016,TELLER,BUSINO,AFC187,AFA091,FLAG,DATE,TIME) values("

    for j in range( len( (TradeContext.AFA031).split("^") ) ) :
        sqlstr1     =   sqlstr
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC401               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AAA010               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC001               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFA031.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFA051               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFA101               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AAA011               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC002               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC003               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC004               + "',"
        #=====������ 20080902 �޸����ڸ�ʽ====
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC005[:4] + '-' + TradeContext.AFC005[4:6] + '-' + TradeContext.AFC005[6:]+ "',"
        #sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC005               + "',"

        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC006               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC007               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC008               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC009.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC010.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC011.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.payAmount            + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC012               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC013.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC015               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC016               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.teller               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.busiNo               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC187               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFA091               + "',"
        sqlstr1     =   sqlstr1 + "'" + '0'                               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.workDate             + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.workTime             + "')"

        if( AfaDBFunc.InsertSql( sqlstr1 ) < 0 ):
            AfaDBFunc.RollbackSql( )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo( '���벹¼����ʧ��' + sqlstr1 )
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���벹¼����ʧ��"
            return False

        AfaDBFunc.CommitSql( )

    AfaLoggerFunc.tradeInfo( '********************���벹¼���ݱ����*******************' )
    TradeContext.errorCode,TradeContext.errorMsg        =   "0000","���벹¼���ݳɹ�"
    return True
