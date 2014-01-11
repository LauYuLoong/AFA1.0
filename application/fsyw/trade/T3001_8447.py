# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.�����ӡ
#=================================================================
#   �����ļ�:   T3001_8447.py
#   �޸�ʱ��:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc, sys, os
from types import *

def printZhou_yuebiao():

    if TradeContext.qryType     ==   '1' :
        fileName    =   TradeContext.busiNo + "_zhoubaobiao.txt"

    elif TradeContext.qryType   ==   '2':
        fileName    =   TradeContext.busiNo + "_yuebaobiao.txt"


    sqlstr  =   "select date from fs_remain where busino='" + TradeContext.busiNo + "' order by date desc"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len(records) == 0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "�������һ�ζ�������ʧ��"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if TradeContext.edDate > records[0][0].strip():
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "%sû�ж��ˣ����ȶ���" %TradeContext.edDate
        return False

    sqlstr  =   "select * from fs_remain where busino='" + TradeContext.busiNo + "' and date<'" + TradeContext.bgDate + "' order by date desc"
    records = AfaDBFunc.SelectSql( sqlstr )
    if (records==None or len(records) == 0):
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��ȡ�������ʧ��,���ݿ��쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

    TradeContext.lastBanlance   =   records[0][2].strip()       #�������
    fileDirName     =   os.environ['AFAP_HOME'] + "/data/ahfs/" + fileName

    #ͳ����������
    #sqlStr  = "select date,sum(cast(afc157 as decimal(17,2))),count(date) from fs_fc76 where flag='0' and busino='" + TradeContext.busiNo + "'"
    #sqlStr  = sqlStr + " and date between '" + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by date"

    sqlStr  = "select workdate,sum(cast(amount as decimal(17,2))),count(workdate) from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"
    sqlStr  = sqlStr + " AND NOTE2='1' AND BANKSTATUS='0' and REVTRANF='0'"
    sqlStr  = sqlStr + " and workdate between '" + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by workdate"

    AfaLoggerFunc.tradeInfo(sqlStr)
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None  ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "��ѯ��������ʧ��"
        AfaLoggerFunc.tradeInfo( "��ѯ��������ʧ��"+sqlStr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeInfo( "***************��̨�����ӡ����*******************" )
        fOutRpt.close()
        return False

    normal_map  =   {}          #��������ͳ�Ʊ�
    for i in range(len(records)):
        normal_map[records[i][0]]   =   [str(records[i][1]),str(records[i][2])]

    AfaLoggerFunc.tradeInfo( '�������ݣ�' )
    AfaLoggerFunc.tradeInfo( normal_map )

    #ͳ���˸�֧��
    #sqlStr  = "select date,sum(cast(afc064 as decimal(17,2))),count(date) from fs_fc75 where flag='0' and busino='" + TradeContext.busiNo + "'"
    #sqlStr  = sqlStr + " and date between '" + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by date"

    sqlStr = "SELECT workdate,sum(cast(amount as decimal(17,2))),count(workdate) FROM fs_maintransdtl WHERE APPNO='"    + TradeContext.appNo    + "'  AND BUSINO='"   + TradeContext.busiNo   + "'"
    sqlStr = sqlStr + " and NOTE2='2' AND BANKSTATUS='0' and REVTRANF='0' and chkflag='0' "
    sqlStr  = sqlStr + " and workdate between '" + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by workdate"

    AfaLoggerFunc.tradeInfo( sqlStr )
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None  ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "��ѯ�˸����ݿ�ʧ��"
        AfaLoggerFunc.tradeInfo( "��ѯ�˸����ݿ�ʧ��"+sqlStr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeInfo( "***************��̨�����ӡ����*******************" )
        fOutRpt.close()
        return False

    tuifu_map   =   {}
    for i in range(len(records)):
        tuifu_map[records[i][0]]   =   [str(records[i][1]).replace('-',''),str(records[i][2])]

    AfaLoggerFunc.tradeInfo( '�˸����ݣ�' )
    AfaLoggerFunc.tradeInfo( tuifu_map )

    #ͳ�ƴ�������
    sqlStr  =   ""
    sqlStr  = "select date,sum(cast(afc011 as decimal(17,2))),count(date) from fs_fc74 where flag!='*' and busino='" + TradeContext.busiNo + "'  "

    #===�����������б����ֶ�,�ź��޸�===
    sqlStr = sqlStr + " and afa101 = '" + TradeContext.bankbm + "'"

    sqlStr  = sqlStr + "  and date between '"    + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by date"
    AfaLoggerFunc.tradeInfo( "��������:" + sqlStr )
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None  ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "��ѯ�������ݿ�ʧ��"
        AfaLoggerFunc.tradeInfo( "��ѯ�������ݿ�ʧ��"+sqlStr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeInfo( "***************��̨�����ӡ����*******************" )
        fOutRpt.close()
        return False

    daicha_map  =   {}
    for i in range(len(records)):
        daicha_map[records[i][0]]   =   [str(records[i][1]),str(records[i][2])]

    AfaLoggerFunc.tradeInfo( '�������ݣ�' )
    AfaLoggerFunc.tradeInfo( daicha_map )
    AfaLoggerFunc.tradeInfo( "********************��ʼ������***************" )

    #�����������е����ںϳɣ������ӡ
    tmpList =   []                      #�����б�
    for item in normal_map.keys():
        if not item in tmpList:
            tmpList.append(item)

    for item in tuifu_map.keys():
        if not item in tmpList:
            tmpList.append(item)

    for item in daicha_map.keys():
        if not item in tmpList:
            tmpList.append(item)

    fOutRpt         =   open(fileDirName,"w")

    lineWidth       =   144             #�����б���
    WidthList       =   [8,14,6,14,6,14,6,14,6,14,6,14]

    #----------------------------------������--------------------------------
    fOutRpt.write('\n')
    fOutRpt.write('\n')
    fOutRpt.write('\n')

    if TradeContext.qryType     ==   '1' :
        fOutRpt.write('��˰�ܱ���'.center(lineWidth))
    elif TradeContext.qryType   ==   '2':
        fOutRpt.write('��˰�±���'.center(lineWidth))

    #----------------------------------������---------------------------------------
    fOutRpt.write('\n')
    fOutRpt.write('\n')

    fOutRpt.write( '     �Ʊ����ڣ�' + TradeContext.workDate + '\t\t\t' ) #busiAccno
    fOutRpt.write('      ������'  + str(TradeContext.lastBanlance) + '\t\t\t' )
    fOutRpt.write('�տ����ʺţ�' + TradeContext.busiAccno )
    fOutRpt.write('\n')
    fOutRpt.write('     �����������Щ����������������������Щ����������������������Щ����������������������Щ����������������������Щ����������������������Щ���������������'+'\n')
    fOutRpt.write('     ��        ��       ��������       ��       ��������       ��       �˸�����       ��       �Ͻɹ���       ��       �Ͻ�ר��       ��              ��'+'\n')
    fOutRpt.write('     ��  ����  �����������������Щ������੤�������������Щ������੤�������������Щ������੤�������������Щ������੤�������������Щ�������    �ϼ�      ��'+'\n')
    fOutRpt.write('     ��        ��    ���      �� ���� ��    ���      �� ���� ��    ���      �� ���� ��    ���      �� ���� ��    ���      �� ���� ��              ��'+'\n')
    fOutRpt.write('     �����������੤�������������੤�����੤�������������੤�����੤�������������੤�����੤�������������੤�����੤�������������੤�����੤��������������'+'\n')

    tmpList.sort()
    banlance    =   float(TradeContext.lastBanlance)
    AfaLoggerFunc.tradeInfo( tmpList )
    for date in tmpList:
        fOutRpt.write( '     ��' )
        fOutRpt.write( date.ljust(8) )                      #��������
        fOutRpt.write( '��' )


        #�������������û�е����������ͣ���ֵ��
        if  not normal_map.has_key(date):
            fOutRpt.write( ''.ljust(14) )
            fOutRpt.write( '��' )
            fOutRpt.write( ''.ljust(6) )
            fOutRpt.write( '��' )
        else:
            fOutRpt.write( normal_map[date][0].ljust(14) )
            fOutRpt.write( '��' )
            fOutRpt.write( normal_map[date][1].ljust(6) )
            fOutRpt.write( '��' )

            banlance    =   banlance + float( normal_map[date][0] )         #�ۼӽ��

        #�������������û�е����������ͣ���ֵ��
        if not daicha_map.has_key(date):
            fOutRpt.write( ''.ljust(14) )
            fOutRpt.write( '��' )
            fOutRpt.write( ''.ljust(6) )
            fOutRpt.write( '��' )
        else:
            fOutRpt.write( daicha_map[date][0].ljust(14) )
            fOutRpt.write( '��' )
            fOutRpt.write( daicha_map[date][1].ljust(6) )
            fOutRpt.write( '��' )

            banlance    =   banlance + float( daicha_map[date][0] )         #�ۼӽ��

        #����˸�������û�е����������ͣ���ֵ��
        if not tuifu_map.has_key(date):
            fOutRpt.write( ''.ljust(14) )
            fOutRpt.write( '��' )
            fOutRpt.write( ''.ljust(6) )
            fOutRpt.write( '��' )
        else:
            fOutRpt.write( tuifu_map[date][0].ljust(14) )
            fOutRpt.write( '��' )
            fOutRpt.write( tuifu_map[date][1].ljust(6) )
            fOutRpt.write( '��' )

            banlance    =   banlance - float( tuifu_map[date][0] )         #�ۼӽ��

        #�Ͻɹ���
        fOutRpt.write( ''.ljust(14) )
        fOutRpt.write( '��' )
        fOutRpt.write( ''.ljust(6) )
        fOutRpt.write( '��' )

        #�Ͻ�ר��
        fOutRpt.write( ''.ljust(14) )
        fOutRpt.write( '��' )
        fOutRpt.write( ''.ljust(6) )
        fOutRpt.write( '��' )

        #��������ȡ�����
        sqlstr  =   "select this from fs_remain where busino='" + TradeContext.busiNo + "' and date='" + date + "'"

        #begin 20100701 �������������б���
        sqlstr  =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"
        #end

        AfaLoggerFunc.tradeInfo( sqlstr )
        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None or len( records)==0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "û�в��ҵ�%s�����" %date
            return False

        #fOutRpt.write( str(banlance).ljust(14) )
        fOutRpt.write( records[0][0].rjust(14) )
        fOutRpt.write( '��' )
        fOutRpt.write( '\n' )

        if date != tmpList[len(tmpList)-1] :
            fOutRpt.write('     �����������੤�������������੤�����੤�������������੤�����੤�������������੤�����੤�������������੤�����੤�������������੤�����੤��������������'+'\n')

    fOutRpt.write('     �����������ة��������������ة������ة��������������ة������ة��������������ة������ة��������������ة������ة��������������ة������ة���������������'+'\n')
    fOutRpt.write('     ��ӡ��' + TradeContext.teller + '\t\t\t' + '���ˣ�' + '' + '\n')
    fOutRpt.close()
    TradeContext.FileName       =   fileName
    return True

#����ɷѱ�
def printPaybiao():
    fileName        =   "JK" + "_" + TradeContext.busiNo + ".txt"

    #�����������
    if TradeContext.isMainBank  :

        #��ѯ��������,��ѯ�������
        if TradeContext.fdBrno :
            sqlstr          =   "select bankserno, accno, username,amount,userno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.fdBrno + "' and note2='1' and bankstatus='0' and revtranf='0'  "
            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"
        else:
            sqlstr          =   "select bankserno, accno, username,amount,userno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and note2='1' and bankstatus='0' and revtranf='0' "
            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #�������������,ֻ�ܲ�ѯ��ǰ��������
    else:
        sqlstr          =   "select bankserno, accno, username,amount,userno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.brno + "' and note2='1' and bankstatus='0' and revtranf='0' "
        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    AfaLoggerFunc.tradeInfo( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���ҵ��ɿ���Ϣ�쳣"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False


    #������д���ļ���ȥ
    if len( records)>=0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        try:
            fileHead    =   ['ҵ����ˮ��','�ɿ����˺�','�ɿ�������','�ɷѽ��','�ɿ�����']
            fileWidth   =   [15,25,40,17,13]
            nWidth      =   130                         #�����ļ����
            nPageRow    =   50                          #ÿ���ļ���ӡ������
            needPage    =   len(records)/nWidth         #��Ҫ��ӡ��ҳ��  ��ʵ������һ
            hp          =   open(lDir+fileName,"w")

            #------------------������--------------------------
            hp.write('\n')
            hp.write('\n')
            hp.write('\n')
            hp.write( '��˰����ɷ���ˮ��ϸ��'.center(nWidth) + '\n' )

            #------------------������--------------------------
            hp.write('\n')
            hp.write('\n')

            hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
            hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
            hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )


            #��ӡ��ͷ
            for i in range( len(fileHead) ) :
                hp.write(fileHead[i].ljust( fileWidth[i]) )
            else:
                hp.write('\n')

            #��ӡ����
            for i in range(nWidth/2):
                hp.write('��')
            else:
                hp.write('\n')

            for i in range( len(records) ):

                tmpList =   list(records[i])
                #�������Ҫ��ҳ
                if not needPage :
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].ljust(fileWidth[j]))
                    else:
                        hp.write('\n')

                #�����Ҫ��ҳ
                else:

                    #�����ǰ��¼����50������������뻻ҳ��
                    if not i % nPageRow :
                        #���Ȼ�����ҳ���һ������
                        for j in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                        #�����µ�һҳ�����濪ʼ���µ�һҳ������Ҳ�ǹ̶��ı�ͷ
                        hp.write( chr(12) )

                        #------------------������--------------------------
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '��˰����ɷ���ˮ��ϸ��'.center(nWidth) + '\n' )

                        #------------------������--------------------------
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
                        hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )


                        #��ӡ��ͷ
                        for j in range( len(fileHead) ) :
                            hp.write(fileHead[j].ljust( fileWidth[j]) )
                        else:
                            hp.write('\n')

                        #��ӡ����
                        for j in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].center(fileWidth[j]))
                    else:
                        hp.write('\n')

            else:
                #��ӡ����
                for j in range(nWidth/2):
                    hp.write('��')
                else:
                    hp.write('\n')

                hp.write('��ӡ��' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('���ˣ�' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "��ѯ����ɷ���Ϣ�ɹ�"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "д�ļ��쳣"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

#�����
def printDaichabiao():
    fileName        =   "DC" + "_" + TradeContext.busiNo + ".txt"

    #�����������
    if TradeContext.isMainBank  :

        #��ѯ��������,��ѯ�������
        if TradeContext.fdBrno :
            sqlstr          =   "select  afc401,afc008,afc006,afc011 from fs_fc74 where flag !='*' and afc016='" + TradeContext.fdBrno + "' and busino='" + TradeContext.busiNo + "'"

            #===�����������б����ֶ�,�ź��޸�===
            sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and date=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

        #��ѯ����Ϊ�գ�
        else:
            sqlstr          =   "select  afc401,afc008,afc006,afc011 from fs_fc74 where flag !='*' and busino='" + TradeContext.busiNo + "'"

            #===�����������б����ֶ�,�ź��޸�===
            sqlstr          =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and date=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + " and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #�������������,ֻ�ܲ�ѯ��ǰ��������
    else:
        sqlstr              =   "select  afc401,afc008,afc006,afc011 from fs_fc74 where flag !='*' and afc016='" + TradeContext.brno + "' and busino='" + TradeContext.busiNo + "'"

        #===�����������б����ֶ�,�ź��޸�===
        sqlstr              =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        if TradeContext.edDate  ==  '00000000':
            sqlstr          =   sqlstr + " and date=" + TradeContext.bgDate + "'"
        else:
            sqlstr          =   sqlstr + "and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���Ҵ�����Ϣ�쳣"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if len( records)>=0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        try:
            fileHead    =   ['��ˮ��','�ɿ����˺�','�ɿ�������','�ɷѽ��']
            fileWidth   =   [15,25,25,40,20]
            nWidth      =   130                         #�����ļ����
            nPageRow    =   50                          #ÿ���ļ���ӡ������
            needPage    =   len(records)/nWidth         #��Ҫ��ӡ��ҳ��  ��ʵ������һ
            hp          =   open(lDir+fileName,"w")
            #----------------������---------------
            hp.write('\n')
            hp.write('\n')
            hp.write('\n')
            hp.write( '��˰������ˮ��ϸ��'.center(nWidth) + '\n' )
            hp.write('\n')
            hp.write('\n')

            hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
            hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
            hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )


            #��ӡ��ͷ
            for i in range( len(fileHead) ) :
                hp.write(fileHead[i].ljust( fileWidth[i]) )
            else:
                hp.write('\n')

            for i in range(nWidth/2):
                hp.write('��')
            else:
                hp.write('\n')


            for i in range(len(records)):
                tmpList =   list(records[i])

                #�������Ҫ��ҳ
                if not needPage :
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].ljust(fileWidth[j]))
                    else:
                        hp.write('\n')
                #�����Ҫ��ҳ
                else:

                    #�����ǰ��¼����50������������뻻ҳ��
                    if not i % nPageRow :

                        #���Ȼ�һ������
                        for i in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                        #�����µ�һҳ�����濪ʼ���µ�һҳ������Ҳ�ǹ̶��ı�ͷ
                        hp.write( chr(12) )

                        #----------------������
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '��˰������ˮ��ϸ��'.center(nWidth) + '\n' )
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
                        hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )


                        #��ӡ��ͷ
                        for i in range( len(fileHead) ) :
                            hp.write(fileHead[i].ljust( fileWidth[i]) )
                        else:
                            hp.write('\n')

                        for i in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                    #��һ������
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].center(fileWidth[j]))
                    else:
                        hp.write('\n')

            else:
                #��ӡ����ĺ���
                for j in range(nWidth/2):
                    hp.write('��')
                else:
                    hp.write('\n')

                hp.write('��ӡ��' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('���ˣ�' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "��ѯ������Ϣ�ɹ�"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "д�ļ��쳣"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

#�˸���
def printTuifubiao():
    fileName        =   "TF" + "_" + TradeContext.busiNo + ".txt"

    #��ѯ��������,��ѯ�������
    if TradeContext.fdBrno :
        sqlstr          =   "select bankserno, userno,username,accno,amount from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' brno='" + TradeContext.fdBrno + "' and note2='2' and bankstatus='0' and revtranf='0'  "
        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"
    else:
        sqlstr          =   "select bankserno, userno,username,accno,amount from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and note2='2' and bankstatus='0' and revtranf='0'  "
        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���ҵ��ɿ���Ϣ�쳣"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if len( records)>=0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        try:
            fileHead    =   ['ҵ����ˮ��','�˸�֪ͨ����','���������','������ʺ�','�˸����']
            fileWidth   =   [15,25,40,25,20]
            nWidth      =   130                         #�����ļ����
            nPageRow    =   50                          #ÿ���ļ���ӡ������
            needPage    =   len(records)/nWidth         #��Ҫ��ӡ��ҳ��  ��ʵ������һ
            hp          =   open(lDir+fileName,"w")

            #----------------������
            hp.write('\n')
            hp.write('\n')
            hp.write('\n')
            hp.write( '��˰�˸���ˮ��ϸ��'.center(nWidth) + '\n' )
            hp.write('\n')
            hp.write('\n')

            hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
            hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
            hp.write( '�������ʺţ�' + TradeContext.busiAccno  + '\n' )


            #��ӡ��ͷ
            for i in range( len(fileHead) ) :
                hp.write(fileHead[i].ljust( fileWidth[i]) )
            else:
                hp.write('\n')

            for i in range(nWidth/2):
                hp.write('��')
            else:
                hp.write('\n')


            for i in range(len(records)):
                tmpList =   list(records[i])
                #�������Ҫ��ҳ
                if not needPage :
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].ljust(fileWidth[j]))
                    else:
                        hp.write('\n')
                #�����Ҫ��ҳ
                else:

                    #�����ǰ��¼����50������������뻻ҳ��
                    if not i % nPageRow :

                        #���Ȼ�����ҳ���һ������
                        for i in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                        #�����µ�һҳ�����濪ʼ���µ�һҳ������Ҳ�ǹ̶��ı�ͷ
                        hp.write( chr(12) )

                        #----------------������
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '��˰������ˮ��ϸ��'.center(nWidth) + '\n' )
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
                        hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )


                        #��ӡ��ͷ
                        for i in range( len(fileHead) ) :
                            hp.write(fileHead[i].ljust( fileWidth[i]) )
                        else:
                            hp.write('\n')

                        for i in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                    #��һ������
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].center(fileWidth[j]))
                    else:
                        hp.write('\n')

            else:
                #��ӡ����ĺ���
                for j in range(nWidth/2):
                    hp.write('��')
                else:
                    hp.write('\n')

                hp.write('��ӡ��' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('���ˣ�' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "��ѯ�����˸���Ϣ�ɹ�"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "д�ļ��쳣"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

#��¼��
def printBulubiao():
    #��ѯ��������,��ѯ�������
    if TradeContext.fdBrno :
        sqlstr          =   "select distinct afc001,afc401,afc008,afc006,amount  from fs_fc84 where busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.fdBrno + "' and flag = '0' "

        #===�����������б����ֶ�,�ź��޸�===
        sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and date=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #��ѯ���л�������
    else:
        sqlstr          =   "select distinct afc001,afc401,afc008,afc006,amount from fs_fc84 where busino='" + TradeContext.busiNo + "' and flag='0' "

        #===�����������б����ֶ�,�ź��޸�===
        sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and date=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���Ҳ�¼��Ϣ�쳣"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    fileName    =   "BL_" + TradeContext.busiNo + ".txt"
    if len( records) >= 0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        fileHead    =   ['�ɿ�����','ҵ����ˮ��','�ɿ����ʺ�','�ɿ�������','�ɷѽ��']
        fileWidth   =   [15,15,25,40,20]
        nWidth      =   130                         #�����ļ����
        nPageRow    =   50                          #ÿ���ļ���ӡ������,�����ݶ�Ϊ50�оͻ�ҳ
        needPage    =   len(records)/nWidth         #��Ҫ��ӡ��ҳ��  ��ʵ������һ
        try:
            hp          =   open(lDir+fileName,"w")
            #----------------������
            #hp.write('\n')
            #hp.write('\n')
            #hp.write('\n')
            #hp.write( '��˰��¼��ˮ��ϸ��'.center(nWidth) + '\n' )
            #hp.write('\n')
            #hp.write('\n')
            #
            #hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
            #hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
            #hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )

            i       =   0                           #��¼��
            LineNum =   0                           #����
            for i in range ( len(records) ):
                tmpList     =   list(records[i])

                #���Ƚ����������б�dataList��
                serNoNum    =   len( tmpList[1].strip().split(':') )      #������ˮ�����Ӧһ���ɿ�����
                dataList    =   [[]]
                for j in range( serNoNum):
                    tmp     =   tmpList[:]          #�б���
                    tmp[1]  =   (tmpList[1].split(':'))[j]

                    if j != 0:
                        tmp[0]  =   ''
                        tmp[2]  =   ''
                        tmp[3]  =   ''
                        tmp[4]  =   ''

                    dataList.insert(j,tmp)
                else:
                    dataList.pop()

                AfaLoggerFunc.tradeInfo( dataList )

                for j in range( len(dataList) ):
                    if not LineNum % nPageRow :
                        if LineNum != 0:
                            #���Ȼ�����ҳ���һ������
                            for i in range(nWidth/2):
                                hp.write('��')
                            else:
                                hp.write('\n')
                            hp.write( chr(12) )


                        #�����µ�һҳ�����濪ʼ���µ�һҳ������Ҳ�ǹ̶��ı�ͷ

                        #----------------������
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '��˰��¼��ˮ��ϸ��'.center(nWidth) + '\n' )
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
                        hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )


                        #��ӡ��ͷ
                        for i in range( len(fileHead) ) :
                            hp.write(fileHead[i].ljust( fileWidth[i]) )
                        else:
                            hp.write('\n')

                        for i in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                    #��һ������
                    for k in range( len(fileHead) ):
                        hp.write(dataList[j][k].ljust(fileWidth[k]))

                    else:
                        hp.write('\n')
                    LineNum =   LineNum + 1
            else:
                #��ӡ����ĺ���
                for j in range(nWidth/2):
                    hp.write('��')
                else:
                    hp.write('\n')

                hp.write('��ӡ��' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('���ˣ�' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "��ѯ��¼��Ϣ�ɹ�"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "д�ļ��쳣"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

#������
def printCZbiao():
    fileName        =   "CZ" + "_" + TradeContext.busiNo + ".txt"

    #�����������
    if TradeContext.isMainBank  :

        #��ѯ��������,��ѯ�������
        if TradeContext.fdBrno :
            sqlstr          =   "select revagentserno, userno,accno,username,amount,serialno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'and brno='" + TradeContext.fdBrno + "' and bankstatus='0' and revtranf='1' "
            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"
        else:
            sqlstr          =   "select revagentserno, userno,accno,username,amount,serialno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and bankstatus='0' and revtranf='1' "
            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #�������������,ֻ�ܲ�ѯ��ǰ��������
    else:
        sqlstr          =   "select revagentserno, userno,accno,username,amount,serialno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'and brno='" + TradeContext.brno + "' and bankstatus='0' and revtranf='1' "
        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #sqlstr          =   "select revagentserno, accno, userno,amount,worktime,userno,serialno,note3 from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and note2='2'"
    #if TradeContext.edDate  ==  '00000000':
    #    sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
    #else:
    #    sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"
    #    fileName    =   fileName + "_" + TradeContext.edDate

    AfaLoggerFunc.tradeInfo( sqlstr )

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���ҳ�����Ϣ�쳣"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if len( records)>=0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        try:
            fileHead    =   ['ҵ����ˮ��','�ɿ�˸������','�ɿ�����ʺ�','�ɿ��������','�ɷѽ��','������ˮ��']
            fileWidth   =   [15,20,25,40,17,8]
            nWidth      =   130                         #�����ļ����
            nPageRow    =   50                          #ÿ���ļ���ӡ������
            needPage    =   len(records)/nWidth         #��Ҫ��ӡ��ҳ��  ��ʵ������һ
            hp          =   open(lDir+fileName,"w")

            #----------------������
            hp.write('\n')
            hp.write('\n')
            hp.write('\n')
            hp.write( '��˰������ˮ��ϸ��'.center(nWidth) + '\n' )
            hp.write('\n')
            hp.write('\n')

            hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
            hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
            hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )

            #��ӡ��ͷ
            for i in range( len(fileHead) ) :
                hp.write(fileHead[i].ljust( fileWidth[i]) )
            else:
                hp.write('\n')

            for i in range(nWidth/2):
                hp.write('��')
            else:
                hp.write('\n')


            for i in range(len(records)):
                tmpList =   list(records[i])

                #�������Ҫ��ҳ
                if not needPage :
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].ljust(fileWidth[j]))
                    else:
                        hp.write('\n')
                #�����Ҫ��ҳ
                else:

                    #�����ǰ��¼����50������������뻻ҳ��
                    if not i % nPageRow :
                        #���Ȼ�����ҳ���һ������
                        for i in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                        #�����µ�һҳ�����濪ʼ���µ�һҳ������Ҳ�ǹ̶��ı�ͷ
                        hp.write( chr(12) )

                        #----------------������-----------------------
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '��˰������ˮ��ϸ��'.center(nWidth) + '\n' )
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '�������ƣ�'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '�Ʊ����ڣ�'   + TradeContext.workDate + '\t' )
                        hp.write( '�տ����ʺţ�' + TradeContext.busiAccno  + '\n' )


                        #��ӡ��ͷ
                        for i in range( len(fileHead) ) :
                            hp.write(fileHead[i].ljust( fileWidth[i]) )
                        else:
                            hp.write('\n')

                        for i in range(nWidth/2):
                            hp.write('��')
                        else:
                            hp.write('\n')

                    #��һ������
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].center(fileWidth[j]))
                    else:
                        hp.write('\n')
            else:
                #��ӡ����ĺ���
                for j in range(nWidth/2):
                    hp.write('��')
                else:
                    hp.write('\n')

                hp.write('��ӡ��' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('���ˣ�' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "��ѯ������Ϣ�ɹ�"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "д�ļ��쳣"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

def SubModuleMainFst( ):
    TradeContext.__agentEigen__  = '0'   #�ӱ��־
    TradeContext.errorCode, TradeContext.errorMsg='0000', '�����ѯ�ɹ�'
    AfaLoggerFunc.tradeInfo( "********************��̨�����ӡ��ʼ***************" )

    #--------------ת�����ڸ�ʽ---------------------
    #TradeContext.bgDate =   TradeContext.bgDate[0:4] + '-' + TradeContext.bgDate[4:6] + '-' + TradeContext.bgDate[6:]
    #TradeContext.edDate =   TradeContext.edDate[0:4] + '-' + TradeContext.edDate[4:6] + '-' + TradeContext.edDate[6:]

    #��ѯ���ڲ�������ǩԼ���ڣ������������һ�ζ��˵�����

    #===�޸����Ϊ����������appnoΪAG2012,�ź��޸�===
    #if TradeContext.bankbm == '012' :
    #    sqlstr  =   "select startdate from abdt_unitinfo where appno='AG2008' and busino='" + TradeContext.busiNo + "'"
    #else:
    #    sqlstr  =   "select startdate from abdt_unitinfo where appno='AG2012' and busino='" + TradeContext.busiNo + "'"
    sqlstr  =   "select startdate from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len(records) == 0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "������Ч����ʧ��"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if TradeContext.bgDate < records[0][0].strip():
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "��ѯ��ʼ��������ǩԼ��ʼ����"
        return False



    #��ѯ�Թ����˻�
    sqlstr          =   "select accno from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len(records) == 0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���ҵ��Թ��˻��쳣"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    TradeContext.busiAccno      =   records[0][0]

    AfaLoggerFunc.tradeInfo( "��ѯ��ǰ�����Ƿ��ǿ����л���" )
    #���Ȳ�ѯ��ǰ�����Ƿ��ǿ����л���
    sqlstr  =   "select brno from abdt_unitinfo where appno='" + TradeContext.appNo + "' and  busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.brno + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records  == None :
        TradeContext.errorCode,TradeContext.errorMsg    =   '0001','��ѯ���ݿ��쳣���ͻ���Ϣ��'
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

    if len(records) == 0 :
        TradeContext.isMainBank =   False       #�Ƿ��ǿ����л���
        AfaLoggerFunc.tradeInfo( '���ǿ����л���' )
    else:
        TradeContext.isMainBank =   True
        AfaLoggerFunc.tradeInfo( '�����л���' )

    if TradeContext.qryType == '1' or TradeContext.qryType == '2':
        if TradeContext.isMainBank  :
            return printZhou_yuebiao()
        else:
            TradeContext.errorCode, TradeContext.errorMsg   =   '0001', '���������У����ܰ����ҵ��'
            return False

    elif TradeContext.qryType == '3':
        return printPaybiao()
    elif TradeContext.qryType == '4':
        return printDaichabiao()
    elif TradeContext.qryType == '5':
        if TradeContext.isMainBank  :
            return printTuifubiao()
        else:
            TradeContext.errorCode, TradeContext.errorMsg   =   '0001', '���������У����ܰ����ҵ��'
            return False
    elif TradeContext.qryType == '6':
        if TradeContext.isMainBank  :
            return printBulubiao()
        else:
            TradeContext.errorCode, TradeContext.errorMsg   =   '0001', '���������У����ܰ����ҵ��'
            return False
    elif TradeContext.qryType == '7':
        return printCZbiao()
    else:
        TradeContext.errorCode,TradeContext.errorMsg  =   '0001','ѡ����Ŵ���'
        return False
