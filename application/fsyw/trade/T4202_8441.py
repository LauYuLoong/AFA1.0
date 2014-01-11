# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.�ɷѽ���
#=================================================================
#   �����ļ�:   4202_8441.py
#   �޸�ʱ��:   2006-09-11
##################################################################
import TradeContext
TradeContext.sysType = 'fsyw'
import AfaLoggerFunc,AfaDBFunc,AfaFlowControl
import AfaHostFunc,datetime

from types import *

#�ӱ�table��ȡ��field����item��ֵΪvalue
def GetDataFromDB(item,value,table,field):
    sql = "select " + field + " from " + "FS_" + table + " where " + item + "='" + value +"'"

    #afc163��Ʊ����
    records = AfaDBFunc.SelectSql( sql )
    if ( records == None or len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( sql )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False
    else:
        if not records[0][0]:
            return "null"
        else:
            return records[0][0]

def SubModuleDoFst():

    #=====add by pgt 20090423 ��֤ʵ�ʽɷѽ���Ƿ�Ϊ0���߿գ�����ǣ���ֱ���˳�====
    if(TradeContext.amount == "0" or TradeContext.amount == "0.00" or TradeContext.amount == "0.0" ):
        AfaLoggerFunc.tradeInfo("ʵ�ʽɷѽ��Ϊ0Ԫ")
        TradeContext.errorCode = "A9999"
        TradeContext.errorMsg = "ʵ�ʽɷѽ��Ϊ0Ԫ"
        return False

    if(TradeContext.amount == ""):
        AfaLoggerFunc.tradeInfo("ʵ�ʽɷѽ��Ϊ��")
        TradeContext.errorCode = "A9999"
        TradeContext.errorMsg = "ʵ�ʽɷѽ��Ϊ��"
        return False


    TradeContext.__agentEigen__ = '0'                     #�ӱ���־

    TradeContext.accno          =   TradeContext.AFA185   #�������ʺ�
    if len(TradeContext.accno) == 0:
        #TradeContext.accno = '0'
        TradeContext.accno = ''


    #����ǿ�����Ҫ�ӿ����л�ȡƾ֤����
    if TradeContext.opkd    == '1':                       #�˻�����
        TradeContext.vouhNo =   TradeContext.cardno[6:18]
        TradeContext.AFA185 =   TradeContext.cardno
        TradeContext.accno  =   TradeContext.cardno

    #��ȡƾ֤�š�ƾ֤����
    if TradeContext.catrFlag == '1':                      #��ת��־
        TradeContext.vouhType   =   TradeContext.vouhNo[0:2]
        TradeContext.vouhNo     =   TradeContext.vouhNo[2:]
        if TradeContext.wdtp=='2': #ƾ֤��
            TradeContext.accPwd=''

    #�ж����б����Ƿ�Ϊ��ֵ,�ź��޸�
    AfaLoggerFunc.tradeInfo("=====���б��� "+TradeContext.bankbm)
    if  len(TradeContext.bankbm) == 0:
            TradeContext.errorCode,TradeContext.errorMsg  =   '0001','���б���Ϊ��ֵ,����������'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

    #���ȴӿ���в�ѯ�ɿ����ţ�������ҵ��򷵻��Ѿ��ɷѵĴ���
    sqlstr  =   "select flag from fs_fc76 where afc001='" + TradeContext.userNo + "'"

    #===�ź����Ӳ�ѯ������Ŀ�����ֶ�,���б����ֶ�,��֤���Ψһһ����¼===
    sqlstr  =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )

    if ( len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( "û�в��ҵ��ɿ����ſ��Խɷ�\n"+sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
    else:
        if records[0][0]   ==  '0':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0001','�Ѿ����ҵ��˽ɿ����ţ������ٽɷ�'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        elif records[0][0]   ==  '1':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0002',"�ɿ����ѳ������ɽɷ�"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        else:
            TradeContext.errorCode,TradeContext.errorMsg  =   '0003',"�ɿ���״̬λ�쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
    #���ɷ���afap��Ҫ���ֶ�ת��Ϊ�ɿ�����Ϣ�����ֶ���
    TradeContext.AFC001         =   TradeContext.userNo
    TradeContext.AFC157         =   TradeContext.amount
    TradeContext.AFA183         =   TradeContext.userName
    TradeContext.AFA185         =   TradeContext.accno
    TradeContext.AFA051         =   TradeContext.note1


    TradeContext.AFA031List     =   []

    #TradeContext.AFA032List     =   []

    TradeContext.AFC181List     =   []
    TradeContext.AFA040List     =   []
    TradeContext.AFC180List     =   []

    #�𿪼�¼
    itemCnt                     =   len( TradeContext.AFA031.split('^') )

    TradeContext.recLen         =   str( itemCnt )

    AfaLoggerFunc.tradeInfo( "AAAAAA[" + TradeContext.recLen + "]AAAA" )

    for i in range(itemCnt):
        TradeContext.AFA031List.append( (TradeContext.AFA031.split('^'))[i] )
        TradeContext.AFC181List.append( (TradeContext.AFC181.split('^'))[i] )
        TradeContext.AFA040List.append( (TradeContext.AFA040.split('^'))[i] )
        TradeContext.AFC180List.append( (TradeContext.AFC180.split('^'))[i] )


    #�Ƿ�Ʊ��У��
    piaoNo          =   TradeContext.AFC001[0:9]
    aaz010      =   TradeContext.AAA010

    sqlstr      =   "select * from fs_dpz_gl where fczqhnm='" + aaz010 + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )

    records     =   AfaDBFunc.SelectSql(sqlstr)

    #=====�����Ƿ��Ѿ������Ѻ�ǰ̨��������У���ʶ�������Ƿ���д�ƱУ�� pgt 20090414====
    if (len(records) > 0  and (TradeContext.CKMD == "1")):    #CKMDУ���ʾ��1У�飬0��У��
        AfaLoggerFunc.tradeInfo( "��ƱУ��" )

        #�����������Ϊ�գ�����Ǵ���ģʽ
        if ( not TradeContext.existVariable('AFA091' ) or len(TradeContext.AFA091)==0 ):
            sqlstr  =   "select count(*) from (select distinct b.AFA051 from FS_DPZ_GL a,fs_fa15 b where a.fdwdm=b.AFA050 and a.FQSHM<='" + piaoNo + "' and a.FQZHM>='" + piaoNo +  "'" + \
            " union all select distinct c.AFA051 from FS_DPZ_GL a,fs_fa21 b,fs_fa15 c where a.FQSHM<='" + piaoNo + "' and a.FQZHM>='" + piaoNo + "' and a.fdwdm=b.AFA050 and b.AFA050=c.AFA050) a where locate(a.afa051, '" + TradeContext.AFA051 + "')=1"

            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )

            if( records == None  ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "��ƱУ��ʧ��"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            if  int(records[0][0]) == 0 :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "�Ǳ�ִ�յ�λƱ��,����Ʊ��"
                return False

            AfaLoggerFunc.tradeInfo('>>>��ƱУ�����')

        #����Ǵ������벻�գ���������ģʽ
        if (TradeContext.existVariable('AFA091' ) and len(TradeContext.AFA091)>0):

            #���ȸ��ݴ�������ת��Ϊ��������
            sqlstr  =   "select afa090 from fs_fa20 where afa091='" + TradeContext.AFA091 + "' and aaa010='" + TradeContext.AAA010 + "' and BUSINO='" + TradeContext.busiNo + "'"


            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "��������ת�����������쳣"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            if  ( len(records) == 0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "û���ҵ�%s�Ĵ�������" %TradeContext.AFA091
                return False

            afa090  =   records[0][0].strip()           #��������
            #���ݴ��������Ʊ����ʼ����ֹ�����ѯ�Ƿ���Ʊ���칺��Ϣ
            sqlstr  =   "select count(*) from fs_dpz_gl where FDWDM='" + afa090 + "' and FQSHM<='" + piaoNo + "' and FQZHM>='" + piaoNo + "'"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if  int(records[0][0]) > 0 :
                pass
            else:
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "�Ǳ�ִ�յ�λƱ��,����Ʊ��--����ģʽ"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

    AfaLoggerFunc.tradeInfo("��λ�ڴ˿�Ʊ�������Ƿ���Ȩ��ȡ����Ŀ")

    #��λ�Ƿ�Ϸ�
    sql         =   "select aaz006,aaz007,afa050,AAZ002 from fs_fa15 where afa051='" + TradeContext.AFA051 + "' and BUSINO='" + TradeContext.busiNo + "'"
    sql         =   sql + " and aaa010='" + TradeContext.AAA010 + "'"
    sql         =   sql + " and busino='" + TradeContext.busiNo + "'"


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
        for i in range( len(records) ) :
            if (records[0][3]!='1'):
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ����ĩ��"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            if  (records[i][0] <= TradeContext.AFC163 ) and (len(records[i][1])==0 or records[i][1] >= TradeContext.AFC163)  :
                iFlag=1
        if iFlag==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ�Ѿ���Ч"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        #���浥λ����
        afa050  =   records[0][2]

    for afa031 in TradeContext.AFA031.split( "^" ):
        #��Ŀ�����Ƿ�Ϸ�
        sql         =   "select aaz006,aaz007,AFA030,AAZ002 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"
        AfaLoggerFunc.tradeInfo(sql)
        records     =   AfaDBFunc.SelectSql( sql )

        AfaLoggerFunc.tradeInfo(records)
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
            if  (records[0][0] <= TradeContext.AFC163 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC163)  :
                iFlag=1
            if iFlag==0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��Ŀ%s�Ѿ���Ч" %afa031
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            #�����շ�����
            afa030  =   records[0][2]
            AfaLoggerFunc.tradeInfo('>>>�շ�����['+afa030+']')

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
                if  (records[0][0] <= TradeContext.AFC163 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC163) :
                    iFlag=1
            AfaLoggerFunc.tradeInfo('-->��¼����' + records[0][0] + '   -->У������' + TradeContext.AFC163)
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
                AfaLoggerFunc.tradeInfo(records)
                AfaLoggerFunc.tradeInfo(TradeContext.AFC163)
                for i in range( len(records) ) :
                    if  (records[0][0] <= TradeContext.AFC163 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC163) :
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

            sqlstr   =  "select afa038,afa039,AFA041 from fs_fa13 where afa031='" + afa031 + "' order by aaz006 desc"
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
                    inputAmt    =   float( (TradeContext.AFC181.split("^"))[i] )    #������
                    maxAmt      =   float( records[0][0] ) * float( (TradeContext.AFC180.split("^"))[i] )    #�����
                    minAmt      =   float( records[0][1] ) * float( (TradeContext.AFC180.split("^"))[i] )    #��С���

                    AfaLoggerFunc.tradeInfo("��ǰ��Ŀ���ޣ�" + str(maxAmt))
                    AfaLoggerFunc.tradeInfo("��ǰ��Ŀ���ޣ�" + str(minAmt))
                    AfaLoggerFunc.tradeInfo("�����" + str(inputAmt))

                    #=====����ǰ̨������У���ʾ�ж��Ƿ���н���ж�pgt 20090414====
                    if TradeContext.CKMD == '1':
                        if minAmt <= inputAmt :
                            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','��Ŀ%s���������' %afa031
                            return False
                #2 ���������С�ڵ��ڱ����ֳɽ��
                #3 �ɿ���ɷ�ʱ��
                d1 = datetime.datetime(int(TradeContext.workDate[0:4]),int( TradeContext.workDate[4:6]), int(TradeContext.workDate[6:8]))
                d2 = datetime.datetime(int(TradeContext.AFC163[0:4]), int(TradeContext.AFC163[5:7]), int(TradeContext.AFC163[8:10]))
                AfaLoggerFunc.tradeInfo(str((d1 - d2).days))
                if (d1 - d2).days >5 or (d1 - d2).days >records[0][2]: #�ɿ��鱾���ɷ�ʱ��Ϊ5��
                    TradeContext.errorCode,TradeContext.errorMsg    =   '0001','�Ѿ������ɷ�ʱ�ޣ���Ŀ%s' %afa031
                    return False
                #4 ����Ŀ����FA13�����ж�����Ŀ��Ϣʱ������ݽɿ���Ŀ�Ʊ��������Ŀ�������ڿ�Ʊ������Ч��������Ŀ��Ϣ

    #���л��:���л��200
    #��Ϊ�޷�ȷ�������������Բ�У�����
    #���Ϊ����ģʽ����Ӧ����������¼�뵽ϵͳ�У���У�鵱ǰ��Ʊ�����ڣ��˵�λ��Ŀ�Ƿ����ڴ˴�����
    elif (TradeContext.AFC187=="200"):
        AfaLoggerFunc.tradeInfo("���л��")

    #ֱ�ӽɿ�Ĭ��300
    else:
        for afa031 in TradeContext.AFA031.split( "^" ):
            i        =   TradeContext.AFA031.split( "^" ).index(afa031)

            AfaLoggerFunc.tradeInfo( TradeContext.AFA031.split( "^" ) )

            sqlstr   =  "select afa038,afa039 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"

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
                    AfaLoggerFunc.tradeInfo('>>>��У��������������')
                    pass
                else:
                    inputAmt    =   float( (TradeContext.AFC181.split("^"))[i] )    #������

                    AfaLoggerFunc.tradeInfo( '>>>��Ա�������ͽ��[' + (TradeContext.AFC181.split("^"))[i] + ']')

                    maxAmt      =   float( records[0][0] ) * float( (TradeContext.AFC180.split("^"))[i] )    #�����
                    minAmt      =   float( records[0][1] ) * float( (TradeContext.AFC180.split("^"))[i] )    #��С���

                    AfaLoggerFunc.tradeInfo("��ǰ��Ŀ���ޣ�" + str(maxAmt))
                    AfaLoggerFunc.tradeInfo("��ǰ��Ŀ���ޣ�" + str(minAmt))
                    AfaLoggerFunc.tradeInfo("�����" + str(inputAmt))

                    AfaLoggerFunc.tradeInfo(records[0][0])
                    AfaLoggerFunc.tradeInfo(records[0][1])
                    AfaLoggerFunc.tradeInfo((TradeContext.AFC181.split("^"))[i])


                    #=====����ǰ̨��������У���־�ж��Ƿ���н��У�� pgt 20090414====
                    if TradeContext.CKMD == '1':
                        if minAmt > inputAmt or inputAmt  >  maxAmt :
                            AfaLoggerFunc.tradeInfo(minAmt)
                            AfaLoggerFunc.tradeInfo(inputAmt)
                            AfaLoggerFunc.tradeInfo(maxAmt)
                            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','��Ŀ%s���������' %afa031
                            return False

        AfaLoggerFunc.tradeInfo("������:"  + TradeContext.AFC157 )
        AfaLoggerFunc.tradeInfo("*************--------*****************  "+str(TradeContext.recLen))
    return True


def SubModuledoSnd():
    TradeContext.mima   =   "011"
    TradeContext.user   =   "011"
    return True

def SubModuledoTrd():

    #��ģ����Ҫ��Ϊ����д��Ʊ����

    if (TradeContext.channelCode =='001' ): #���潻�ײ��Ʒ�Ʊ
        TradeContext.__billSaveCtl__  = '0'

    else:
        TradeContext.__billSaveCtl__  = '1'

    bill    =   []
    bill.append('1')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    AfaLoggerFunc.tradeInfo("*************�ɷѽ��׿�ʼ*****************")

    try:
        sqlstr      =   ""
        sqlstr      =   "select * from fs_fc76 where afc001='" + TradeContext.userNo + "'"
        #===�ź����Ӳ�ѯ���������б����ֶ�,��֤���Ψһһ����¼===
        sqlstr      =   sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"
        records     =   AfaDBFunc.SelectSql(sqlstr)
        #���ҵ��˽ɿ�����,ֻ��Ҫ����״̬λ
        if ( len(records) > 0 ):
            AfaLoggerFunc.tradeInfo("=====>>>��FS_FC76����"+TradeContext.userNo+"��Ӧ����Ϣ,ֻ��Ҫ����״̬λ")
            sqlstr      =   ""
            sqlstr      =   "update fs_fc76 set flag='0',afc187='" + TradeContext.AFC187 + "' ,serno='" + TradeContext.agentSerialno + "' where afc001='" + TradeContext.userNo + "'"
            if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
                TradeContext.errorCode,TradeContext.errorMsg  =   '0001','���нɿ��¼'
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg +sqlstr)
                return None
            else:
                TradeContext.errorCode,TradeContext.errorMsg    =   "0000",'�ɷѳɹ�'
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo("*************�ɷѽ��׽���*****************")   
                return bill
                
        else:
                AfaLoggerFunc.tradeInfo("=====>>>��FS_FC76����"+TradeContext.userNo+"��Ӧ����Ϣ�������¼")

        #==����ҵ��˽ɿ�����,��Ҫ����ǰ̨�͹����ĵ�ǰ��¼�������ֶ�,�ź��޸���20100524==
        sqlstr1     =   ""
        #�ѽ�����Ϣд���������ݿ�����
        #�������б����ֶ�,�ź��޸�
        sqlstr  =   "insert into FS_FC76(AFC001,AFA031,AFC163,AFC187,AFC183,AFC157,   \
                                      AFC181,AFA040,AFC180,AFA051,AFC166,AFC155,AFC153,  \
                                      AFC154,AFA183,AFA184,AFA185,AFA091,AFC015,AAA010,FLAG,SERNO,BUSINO,TELLER,BRNO,DATE,TIME,BANKNO) values("

        for i in range( len( (TradeContext.AFA031).split("^") ) ) :
            sqlstr1          =   sqlstr

            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC001                      + "',"
            sqlstr1          =   sqlstr1 + "'" + (TradeContext.AFA031.split("^"))[i]      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC163                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC187                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC183                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC157                      + "',"
            sqlstr1          =   sqlstr1 + "'" + (TradeContext.AFC181.split("^"))[i].strip()   + "',"
            sqlstr1          =   sqlstr1 + "'" + (TradeContext.AFA040.split("^"))[i].strip()   + "',"
            sqlstr1          =   sqlstr1 + "'" + (TradeContext.AFC180.split("^"))[i].strip()   + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA051                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC166                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC155                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC153                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC154                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA183                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA184                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA185                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA091                      + "',"

            sqlstr1=sqlstr1+"'"+TradeContext.workDate[:4]+'-'+TradeContext.workDate[4:6]+'-'+TradeContext.workDate[6:]+"',"
            #=====������ 20080821 �޸������տ�ʱ��ΪTradeContext.workDate====
            #sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC015                      + "',"

            sqlstr1          =   sqlstr1 + "'" + TradeContext.AAA010                      + "',"
            sqlstr1          =   sqlstr1 + "'" + '0'                                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.agentSerialno               + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.busiNo                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.teller                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.brno                        + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.workDate                    + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.workTime                    + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.bankbm                      + "')"

            AfaLoggerFunc.tradeInfo( sqlstr1 )
            if( AfaDBFunc.InsertSql( sqlstr1 ) < 1 ):
                AfaDBFunc.RollbackSql( )
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'����ɷ�����Ϣ��ʧ��' + sqlstr1
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return None

            AfaDBFunc.CommitSql( )

        TradeContext.errorCode,TradeContext.errorMsg    =   "0000",'�ɷѳɹ�'
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )

        AfaLoggerFunc.tradeInfo("*************�ɷѽ��׽���*****************")
        return bill

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        return None
