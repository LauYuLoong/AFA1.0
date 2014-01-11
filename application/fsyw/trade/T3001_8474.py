###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��15��
###############################################################################

#���е�״̬λ 0 ��������  1�Ƿ�˰
import TradeContext, AfaDBFunc, AfaLoggerFunc, os, sys
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #�ӱ��־



    #-----------------------���ݵ�λ�������û�ȡ������Ϣ----------------------------
    sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
    sqlstr      =   sqlstr + " and bankno ='" + TradeContext.bankbm + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        return False

    elif len(records) > 1:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ��Ϣ���쳣:һ����λ��Ŷ�Ӧ�˶��������Ϣ"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        return False

    TradeContext.AAA010     =   records[0][0].strip()
    TradeContext.AFA101     =   records[0][1].strip()
    #TradeContext.AAA010 =   '0000000000'
    #TradeContext.AFA101 =   '011'

    try:
        #��ѯδ��ֹ���
        if TradeContext.opType  ==   '0':

            if( not TradeContext.existVariable( "FileName" ) ):
                TradeContext.errorCode,TradeContext.errorMsg    =   '0001','�ļ�����Ϊ��'
                return False

            fileName = os.environ['AFAP_HOME'] + "/data/ahfs/" + TradeContext.FileName

            AfaLoggerFunc.tradeInfo( '�ļ����ƣ�' + fileName )
            if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
                AfaLoggerFunc.tradeInfo( '�����ѯδ���' )
                fp      =   open(fileName,"r")
                sLine   =   fp.readline()
                while ( sLine ):
                    AfaLoggerFunc.tradeInfo( "********************��̨��ֲ�ѯ��ʼ***************" )


                    LineItem    =   sLine.split("<fld>")

                    dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]
                    sqlstr      =   ""
                    sqlstr      =   "select * from fs_fc74 where afc401='" + LineItem[0].strip() + "' and afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "'"
                    sqlstr      =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                    #===�����������б����ֶ�,�ź��޸�===
                    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                    AfaLoggerFunc.tradeInfo( sqlstr )
                    records = AfaDBFunc.SelectSql( sqlstr )
                    if( records == None  ):
                        TradeContext.errorCode  =   "0001"
                        TradeContext.errorMsg   =   "������ˮ��ϸ���쳣"
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        return False

                    #���û�в鵽��ˮ���룬�����һ����¼
                    if ( len( records)==0 ):
                        #=====������ ���������տ����˺Ŵ���ȡbusinoinfo�����˺�====
                        sql2 = "select accno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
                        sql2 = sql2 + " and bankno = '" + TradeContext.bankbm + "'"
                        red = AfaDBFunc.SelectSql( sql2 )
                        if red == None or len(red)==0 :
                            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
                            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                            AfaLoggerFunc.tradeInfo( sql2 )
                            #=====û���򸳿�====
                            TradeContext.accno1 = ''

                        #=====��ֵ====
                        TradeContext.accno1 = red[0][0]

                        AfaLoggerFunc.tradeInfo( '������ˮ����%s' %LineItem[0] )
                        sqlstr      =   ""          #��ˮ��               �ɿ�������         �ɿ����˺�  �շѽ��        �����տ�ʱ��
                        sqlstr      =   "insert into fs_fc74 (AFC401,AAA010,AFA101,AFC004,AFC006,AFC007,AFC008,AFC011,AFC015,PAYTIME,AFC016,TELLER,BUSINO,FZPH,AFA091,AFC001,NOFEE,FLAG,DATE,TIME) values ( "

                        dateTmp     =   LineItem[5].strip()
                        dateTmp     =   dateTmp[0:4] + '-' + dateTmp[4:6] + '-' + dateTmp[6:8]

                        sqlstr      =   sqlstr  + "'" +  LineItem[0].strip()         + "',"         #��ˮ��
                        sqlstr      =   sqlstr  + "'" +  TradeContext.AAA010         + "',"         #������������
                        sqlstr      =   sqlstr  + "'" +  TradeContext.AFA101         + "',"         #��������

                        #=====������ 20080825 �޸Ĺ����տ����˺ŵĴ���====
                        #sqlstr      =   sqlstr  + "'" +  ''                         + "',"         #�տ����ʺ�
                        sqlstr      =   sqlstr  + "'" +  TradeContext.accno1           + "',"         #�տ����ʺ�

                        sqlstr      =   sqlstr  + "'" +  LineItem[1].strip()         + "',"         #��������
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #�ɿ��˿�����
                        sqlstr      =   sqlstr  + "'" +  LineItem[2].strip()         + "',"         #�ɿ����ʺ�
                        sqlstr      =   sqlstr  + "'" +  LineItem[3].strip()         + "',"         #�շѽ��
                        sqlstr      =   sqlstr  + "'" +  dateTmp                     + "',"         #�տ�����
                        sqlstr      =   sqlstr  + "'" +  LineItem[4].strip()         + "',"         #�տ�ʱ��
                        sqlstr      =   sqlstr  + "'" +  TradeContext.brno           + "',"         #��������

                        sqlstr      =   sqlstr  + "'" +  TradeContext.teller         + "',"         #��Ա��
                        sqlstr      =   sqlstr  + "'" +  TradeContext.busiNo         + "',"         #��λ���
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #֧Ʊ��
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #��������
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #�ɿ�����
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #�ɿ�����
                        sqlstr      =   sqlstr  + "'" +  '*'                         + "',"         #��־λ,��ʼ��Ϊδ����״̬
                        sqlstr      =   sqlstr  + "'" +  '00000000'                  + "',"         #����
                        sqlstr      =   sqlstr  + "'" +  TradeContext.workTime       + "')"         #ʱ��


                        if( AfaDBFunc.InsertSql( sqlstr ) < 1 ):
                            AfaDBFunc.RollbackSql( )
                            AfaLoggerFunc.tradeInfo( "�������ݿ�ʧ��" )
                            AfaLoggerFunc.tradeInfo(sqlstr)
                            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                            TradeContext.errorCode  =   "0001"
                            TradeContext.errorMsg   =   "������ˮ��ʧ��"
                            return False

                        AfaDBFunc.CommitSql( )
                    #else:
                    #    AfaLoggerFunc.tradeInfo('������ˮ����%s����' %LineItem[0])
                    #    sqlstr      =   "update fs_fc74 set date='" + TradeContext.workDate + "' where afc401='" + LineItem[0].strip() + "'"
                    #    if( AfaDBFunc.UpdateSql( sqlstr ) < 1 ) :
                    #        AfaDBFunc.RollbackSql()
                    #        TradeContext.errorCode, TradeContext.errorMsg='0001', '���´������ݱ�ʧ��'
                    #        AfaLoggerFunc.tradeInfo( sqlstr )
                    #        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    #        return False
                    #
                    #    AfaDBFunc.CommitSql( )

                    sLine   =   fp.readline()

                #�����ݿ��в�ѯ�������ݣ�д���ļ���ȥ
                sqlstr  =   ""
                #sqlstr  =   "select FLAG,SERNO,PAYAMOUNT,PAYACCNO,PAYER,PAYDATE,PAYTIME from fs_detail where date='" + TradeContext.workDate + "' and busino='" + TradeContext.busiNo + "' and flag = '1'"

                dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]

                #��ǰ״̬����ˮ�š��շѽ��ɿ����˺š��ɿ������ơ��տ����ڡ������տ�ʱ��
                sqlstr  =   "select flag,afc401,afc011,afc008,afc006,afc015,paytime from fs_fc74 where afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag='*'  and date='00000000' "

                #===�����������б����ֶ�,�ź��޸�===
                sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                AfaLoggerFunc.tradeInfo( sqlstr )
                records = AfaDBFunc.SelectSql( sqlstr )
                if( records == None  ):
                    TradeContext.errorCode  =   "0001"
                    TradeContext.errorMsg   =   "������ˮ��Ϣʧ��"
                    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                    AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
                    return False

                else:
                    #������д���ļ���ȥ
                    lDir        =   os.environ['AFAP_HOME'] + "/data/ahfs/"             #����Ŀ¼
                    fName       =   "DOWN_8474_" + TradeContext.busiNo + ".txt"         #�ļ�����

                    try:
                        hp      =   open(lDir+fName,"w")

                        hp.write( str(len(records)) + "\n" )
                        i       =   0
                        while( i < len(records) ):
                            lineList    =   list(records[i])

                            if lineList[0]   ==  '*':
                                lineList[0]  =   '1'

                            #ת�����ڸ�ʽ��0000-00-00ת��Ϊ00000000
                            lineList[5]  =   lineList[5].replace('-','')

                            hp.write( "|".join( lineList ) )
                            if i != len(records) -1 :
                                hp.write( "\n" )

                            i = i + 1
                        else:
                            hp.close()
                            TradeContext.downFileName   =   fName

                    except Exception, e:
                        AfaLoggerFunc.tradeInfo( str(e) )
                        TradeContext.errorCode  =   "0001"
                        TradeContext.errorMsg   =   "д�ļ��쳣"
                        return False

            else:
                AfaLoggerFunc.tradeInfo( "�ļ�" + fileName + "������" )
                TradeContext.errorCode  =   "0002"
                TradeContext.errorMsg   =   "û���ҵ��ϴ��ļ�"
                return False

        #��ѯ�Ѿ���ֵ�
        else:
            AfaLoggerFunc.tradeInfo( '�����ѯ���' )
            sqlstr  =   ""
            dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]
            sqlstr  =   "select flag,afc401,afc011,afc008,afc006,afc015,paytime from fs_fc74 where afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag='1' "

            #===�����������б����ֶ�,�ź��޸�===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            #�ж���ˮ�����Ƿ�Ϊ��,���򷵻ص������м�¼�����գ�ֻ�Ƿ�����ˮ�ŵļ�¼
            if  TradeContext.serNo :
                sqlstr  =   sqlstr + " and afc401='" + TradeContext.serNo + "'"

            AfaLoggerFunc.tradeInfo( '�����ѯ���1' )
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "������ˮ��Ϣʧ��"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
                return False

            else:
                #������д���ļ���ȥ
                lDir        =   os.environ['AFAP_HOME'] + "/data/ahfs/"         #����Ŀ¼
                fName       =   "DOWN_8474_" + TradeContext.busiNo + "_" + TradeContext.teller + ".txt"  #�ļ�����

                try:
                    hp      =   open(lDir+fName,"w")
                    hp.write(str( len(records) ) + "\n" )
                    i       =   0
                    while( i < len(records) ):
                        tmpList =   list(records[i])
                        if  tmpList[0]   ==  '1':
                            tmpList[0]  =   '0'
                        elif tmpList[0]   ==  '*':
                            tmpList[0]  =   '1'

                        #ת�����ڸ�ʽ��0000-00-00ת��Ϊ00000000
                        tmpList[5]  =   tmpList[5].replace('-','')

                        hp.write( "|".join( tmpList) )
                        if i != len(records) -1 :
                            hp.write( "\n" )

                        i = i + 1
                    else:
                        hp.close()
                        TradeContext.downFileName   =   fName

                except Exception, e:
                    AfaLoggerFunc.tradeInfo( str(e) )
                    TradeContext.errorCode  =   "0001"
                    TradeContext.errorMsg   =   "д�ļ��쳣"
                    return False

        AfaLoggerFunc.tradeInfo( "********************��̨��ֲ�ѯ����***************" )
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "��ֲ�ѯ�ɹ�"
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode  =   "0003"
        TradeContext.errorMsg   =   "��ֲ�ѯ�쳣"
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode  =   "0003"
        TradeContext.errorMsg   =   "��ֲ�ѯ�쳣"
        return False

