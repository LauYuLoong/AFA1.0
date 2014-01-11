###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰
#
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2009��8��5��
###############################################################################

#���е�״̬λ 0 ��������  1�Ƿ�˰
import TradeContext

TradeContext.sysType = 'cron'

import AfaDBFunc, AfaLoggerFunc, os, sys, HostContext, ConfigParser, HostComm, AfaUtilTools,AfaAdminFunc
from types import *



def GetLappConfig( CfgFileName = None ):
    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOST_HOSTIP   = config.get('HOST_DZ', 'HOSTIP')
        TradeContext.HOST_USERNO   = config.get('HOST_DZ', 'USERNO')
        TradeContext.HOST_PASSWD   = config.get('HOST_DZ', 'PASSWD')

        TradeContext.HOST_LDIR     = os.environ['AFAP_HOME'] + "/data/ahfs/"        #����·��
        TradeContext.HOST_RDIR     = 'FTAXLIB'            #config.get('HOST_DZ', 'RDIR')  #Զ��·��
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return 0

    except Exception, e:
        print str(e)
        return -1

#�����ʺ���ˮ��ϸ�ļ�
def GetDetailFile(rfilename, lfilename):
    AfaLoggerFunc.tradeInfo( '--->��ʼ�����ļ�' )
    try:
        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/ahfs_ahfs.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.HOST_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.HOST_USERNO + ' ' + TradeContext.HOST_PASSWD + '\n')

        #�����ļ�
        ftpFp.write('cd '  + TradeContext.HOST_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.HOST_LDIR + '\n')
        ftpFp.write('quote type c 1381 ' + '\n')
        ftpFp.write('get ' + rfilename + ' ' + lfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return -1
        else:
            return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('FTP�����쳣')
        return -1


#20111102 �º����
#begin
#------------------------------------------------------------------
#����һ��4λ�����
#------------------------------------------------------------------     
def CrtSequence( ):
    
    try:
        sqlStr = "SELECT NEXTVAL FOR FSYW_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :        
            TradeContext.errorCode,TradeContext.errorMsg    =   "9999","�������к��쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlStr )
            return False
        
        AfaLoggerFunc.tradeInfo( "���кţ�" + str(records[0][0]) )
        
        #���к�
        TradeContext.sequenceNo = str(records[0][0]).rjust(4,'0')
        
        return 0

    except Exception, e:
        print str(e)
        return -1
        
#end        

###########################################������###########################################
if __name__=='__main__':

    if ( len(sys.argv) != 2 ):
        TradeContext.serDate = AfaAdminFunc.getTimeFromNow(int(-1))
    else:
        sOffSet                =   sys.argv[1]
        TradeContext.serDate   = AfaAdminFunc.getTimeFromNow(int(sOffSet))

    TradeContext.workDate  =   AfaUtilTools.GetSysDate( )
    TradeContext.workTime =   AfaUtilTools.GetSysTime( )
    #TradeContext.serDate  =   AfaAdminFunc.getTimeFromNow(int(-1))
    #TradeContext.serDate  =   '20090910'
    #TradeContext.serDate  =   '20110601'
    AfaLoggerFunc.tradeInfo( TradeContext.serDate )
    TradeContext.opType   =   '0'
    #TradeContext.appNo    =   'AG2008'
    TradeContext.teller   =   '999986'

    #begin 20100609 �������޸�
    #sqlstr_bus  =  "select busino from fs_businoconf"
    sqlstr_bus = "select busino,bankno from fs_businoconf"
    #end

    records_bus = AfaDBFunc.SelectSql( sqlstr_bus )
    if records_bus == None or len(records_bus)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr_bus )
        sys.exit(1)
    for i in range( len(records_bus) ):
        TradeContext.busiNo  = records_bus[i][0].strip()

        #begin 20100609 ����������
        TradeContext.bankbm  = records_bus[i][1].strip()
        if ( TradeContext.bankbm == '012' ):
            TradeContext.appNo = "AG2008"
            
        else:
            TradeContext.appNo = "AG2012"
        #end

        TradeContext.brno    = TradeContext.busiNo[0:10]
        AfaLoggerFunc.tradeInfo( TradeContext.brno )

        #begin 20100609 �������޸�
        #sqlstr_acc   =   "select accno from abdt_unitinfo  where appno='AG2008' and busino='" +  TradeContext.busiNo + "'"
        sqlstr_acc   =   "select accno from abdt_unitinfo  where busino='" +  TradeContext.busiNo + "'"
        sqlstr_acc   =   sqlstr_acc + " and appno = '" + TradeContext.appNo + "'"
        #end

        records_acc = AfaDBFunc.SelectSql( sqlstr_acc )
        if records_bus == None or len(records_bus)==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr_bus )
            continue
            #sys.exit(1)

        else:
            TradeContext.accno   =   records_acc[0][0]

        #ͨѶ�����
        HostContext.I1TRCD = '8847'                        #������
        HostContext.I1SBNO = TradeContext.brno             #���׻�����
        HostContext.I1USID = '999986'                      #���׹�Ա��
        HostContext.I1AUUS = ""                            #��Ȩ��Ա
        HostContext.I1AUPS = ""                            #��Ȩ��Ա����
        HostContext.I1WSNO = '10.12.2.199'                 #�ն˺�
        
        
        #20111102 �º��޸� �ļ��������к� ȷ��Ψһ��
        #begin    
        #��ȡһ��4λ�����кţ�����ƴ���ͺ��ĵĿ����ļ��� ȷ��Ψһ��
        
        if CrtSequence() < 0 :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "�����ļ����к�ʧ��"
            continue

        #HostContext.I1FINA = 'AG12345678'                             #�ļ�����
        HostContext.I1FINA = 'AG1234'+ TradeContext.sequenceNo         #�ļ�����(10λ)  
        #end
        
        HostContext.I1STDT = TradeContext.serDate          #��ʼ����
        HostContext.I1EDDT = TradeContext.serDate          #��ֹ����
        HostContext.I1ACCN = TradeContext.accno            #�Թ������ʺ�
        AfaLoggerFunc.tradeInfo('���ؽ��:�����ʺ�     = ' + HostContext.I1ACCN)

        HostTradeCode = "8847".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8847.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   HostContext.host_ErrorMsg
            continue
            #sys.exit(1)
        else:
            if ( HostContext.O1MGID == "AAAAAAA" ):
                AfaLoggerFunc.tradeInfo('>>>��ѯ������=[' + HostContext.O1MGID + ']���׳ɹ�')
                AfaLoggerFunc.tradeInfo('���ؽ��:�ļ�����     = ' + HostContext.O1FINA)        #�ļ�����
                AfaLoggerFunc.tradeInfo('���ؽ��:��������     = ' + HostContext.O1TRDT)        #��������
                AfaLoggerFunc.tradeInfo('���ؽ��:����ʱ��     = ' + HostContext.O1TRTM)        #����ʱ��

            else:
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   HostContext.O1INFO
                AfaLoggerFunc.tradeInfo('�������ؽ��:' + TradeContext.errorMsg)
                continue
                #sys.exit(1)

        AfaLoggerFunc.tradeInfo( "********************��̨�ʺ���ˮ��ϸ��ѯ��ʼ***************" )
        if GetLappConfig() < 0 :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "��ȡ�����ļ�����"
            continue
            #sys.exit(1)

        AfaLoggerFunc.tradeInfo(TradeContext.HOST_HOSTIP)
        AfaLoggerFunc.tradeInfo(TradeContext.HOST_USERNO)
        AfaLoggerFunc.tradeInfo(TradeContext.HOST_PASSWD)
        AfaLoggerFunc.tradeInfo(TradeContext.TRACE      )
        AfaLoggerFunc.tradeInfo(TradeContext.HOST_LDIR  )
        AfaLoggerFunc.tradeInfo(TradeContext.HOST_RDIR  )

        #fileName    =   os.environ['AFAP_HOME'] + "/data/ahfs/" + TradeContext.FileName
        #=====�ź��޸��ļ��������б���======
        lFileName    =   'DOWN_8477_' + TradeContext.bankbm+TradeContext.busiNo + '.txt'
        AfaLoggerFunc.tradeInfo( '�����ļ����ơ�' + lFileName + "��" )
        if GetDetailFile( HostContext.O1FINA,lFileName ) != 0 :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "ftp��ˮ��ϸ�ļ�ʧ��"
            continue
            #sys.exit(1)

        AfaLoggerFunc.tradeInfo( "********************��̨�ʺ���ˮ��ϸ��ѯ����***************" )
        TradeContext.errorCode      =   "0000"
        TradeContext.errorMsg       =   "��̨�ʺ���ˮ��ϸ��ѯ�ɹ�"
        TradeContext.downFileName   =   lFileName

        TradeContext.FileName   =   TradeContext.downFileName


        #-----------------------���ݵ�λ�������û�ȡ������Ϣ----------------------------
        #begin 20100609 �������޸�
        #sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        sqlstr      =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"
        #end


        records = AfaDBFunc.SelectSql( sqlstr )
        if records == None or len(records)==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr )
            continue
            #sys.exit(1)

        elif len(records) > 1:
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��λ��Ϣ���쳣:һ����λ��Ŷ�Ӧ�˶��������Ϣ"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr )
            continue
            #sys.exit(1)

        TradeContext.AAA010     =   records[0][0].strip()
        TradeContext.AFA101     =   records[0][1].strip()

        try:
            #��ѯδ��ֹ���
            if TradeContext.opType  ==   '0':

                if( not TradeContext.existVariable( "FileName" ) ):
                    TradeContext.errorCode,TradeContext.errorMsg    =   '0001','�ļ�����Ϊ��'
                    continue
                    #sys.exit(1)

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
                        #begin 20100609 �������޸�
                        #sqlstr      =   "select * from fs_fc74 where afc401='" + LineItem[0].strip() + "' and afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "'"
                        sqlstr      =   sqlstr + "select * from fs_fc74 where afc401='" + LineItem[0].strip() + "' and afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "'"
                        sqlstr      =   sqlstr + " and afa101 = '" + TradeContext.AFA101 + "'"
                        #end

                        AfaLoggerFunc.tradeInfo( sqlstr )
                        records = AfaDBFunc.SelectSql( sqlstr )
                        if( records == None  ):
                            TradeContext.errorCode  =   "0001"
                            TradeContext.errorMsg   =   "������ˮ��ϸ���쳣"
                            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                            continue
                            #sys.exit(1)

                        #���û�в鵽��ˮ���룬�����һ����¼
                        if ( len( records)==0 ):

                            #begin 20100609 �������޸�
                            sql2 = ""
                            #sql2 = "select accno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
                            sql2 = sql2 + "select accno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
                            sql2 = sql2 + " and bankno = '" + TradeContext.bankbm + "'"
                            #end

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
                                continue
                                #sys.exit(1)

                            AfaDBFunc.CommitSql( )

                        sLine   =   fp.readline()

                    #�����ݿ��в�ѯ�������ݣ�д���ļ���ȥ
                    sqlstr  =   ""

                    dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]

                    #begin 20100609 �������޸�
                    #��ǰ״̬����ˮ�š��շѽ��ɿ����˺š��ɿ������ơ��տ����ڡ������տ�ʱ��
                    sqlstr  = ""
                    #sqlstr  =   "select flag,afc401,afc011,afc008,afc006,afc015,paytime from fs_fc74 where afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag='*'  and date='00000000' "
                    sqlstr  =   sqlstr + "select flag,afc401,afc011,afc008,afc006,afc015,paytime from fs_fc74 where afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag='*'  and date='00000000' "
                    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.AFA101 + "'"
                    #end

                    AfaLoggerFunc.tradeInfo( sqlstr )
                    records = AfaDBFunc.SelectSql( sqlstr )
                    if( records == None  ):
                        TradeContext.errorCode  =   "0001"
                        TradeContext.errorMsg   =   "������ˮ��Ϣʧ��"
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
                        continue
                        #sys.exit(1)

                    else:
                        #������д���ļ���ȥ
                        lDir        =   os.environ['AFAP_HOME'] + "/data/ahfs/"             #����Ŀ¼
                        #====�ź��޸ļ������б���
                        fName       =   "DOWN_8474_" + TradeContext.bankbm+TradeContext.busiNo + ".txt"         #�ļ�����

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
                            continue
                            #sys.exit(1)

                else:
                    AfaLoggerFunc.tradeInfo( "�ļ�" + fileName + "������" )
                    TradeContext.errorCode  =   "0002"
                    TradeContext.errorMsg   =   "û���ҵ��ϴ��ļ�"
                    continue
                    #sys.exit(1)

            AfaLoggerFunc.tradeInfo( "********************��̨��ֲ�ѯ����***************" )
            TradeContext.errorCode  =   "0000"
            TradeContext.errorMsg   =   "��ֲ�ѯ�ɹ�"
            continue
            #sys.exit(0)

        except Exception, e:
            AfaLoggerFunc.tradeInfo( str(e) )
            TradeContext.errorCode  =   "0003"
            TradeContext.errorMsg   =   "��ֲ�ѯ�쳣"
            sys.exit(1)

        except Exception, e:
            AfaLoggerFunc.tradeInfo( str(e) )
            TradeContext.errorCode  =   "0003"
            TradeContext.errorMsg   =   "��ֲ�ѯ�쳣"
            sys.exit(1)


