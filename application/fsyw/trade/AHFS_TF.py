###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰�����˸���Ϣ
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��15��
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import ConfigParser, AfaUtilTools, sys, AfaDBFunc, Party3Context
import os, HostContext, HostComm, AfaAfeFunc, AfaLoggerFunc, time
from types import *


#��ȡ�����ļ�����Ϣ
def GetConfig( CfgFileName = None ):
    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )
        TradeContext.BATCH_TRACE    = config.get('FS_AFE', 'TRACE')
        TradeContext.BATCH_ERR_TRACE= config.get('FS_AFE', 'ERR_TRACE')

        TradeContext.BATCH_HOSTIP   =   config.get('FS_AFE', 'HOSTIP')
        TradeContext.BATCH_USERNO   =   config.get('FS_AFE', 'USERNO')
        TradeContext.BATCH_PASSWD   =   config.get('FS_AFE', 'PASSWD')
        TradeContext.BATCH_RDIR     =   config.get('FS_AFE', 'RDIR')
        TradeContext.BATCH_LDIR     =   config.get('FS_AFE', 'LDIR')
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False


#FTP������
def ftpfile( sfilename, rfilename):

    try:
        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/AhfsFtpTf' + '.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.BATCH_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.BATCH_USERNO + ' ' + TradeContext.BATCH_PASSWD + '\n')

        #�����ļ�
        ftpFp.write('cd '  + TradeContext.BATCH_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.BATCH_LDIR + '\n')
        ftpFp.write('bin ' + '\n')
        ftpFp.write('get ' + rfilename + ' ' + sfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        os.system(ftpcmd)

        return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('FTP�����쳣')
        return -1

def ChkAppStatus():
    sqlstr  =   "select status from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino ='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    AfaLoggerFunc.tradeInfo( sqlstr )
    if( records == None or len( records)==0 ):
        AfaLoggerFunc.tradeInfo('����Ӧ��״̬��ʧ��')
        return False
    elif len( records ) == 1:
        if records[0][0].strip() == '1':
            return True
        else:
            AfaLoggerFunc.tradeInfo('Ӧ��״̬û�п���')
            return False
    else:
        AfaLoggerFunc.tradeInfo('Ӧ��ǩԼ�쳣')
        return False

###########################################������###########################################
if __name__=='__main__':
    #��ʼ��TradeContext
    TradeContext.workDate       =   AfaUtilTools.GetSysDate( )
    TradeContext.workTime       =   AfaUtilTools.GetSysTime( )
    TradeContext.zoneno         =   ""
    TradeContext.brno           =   ""
    TradeContext.teller         =   ""
    TradeContext.authPwd        =   ""
    TradeContext.termId         =   ""
    TradeContext.TransCode      =   "8448"                  #�˸�������


    AfaLoggerFunc.tradeInfo('**********���շ�˰�˸���Ϣ���ؿ�ʼ**********')

    #sqlstr  = "select distinct busino from abdt_unitinfo where appno='AG2008'"

    #begin 20100528 �������޸�
    #sqlstr  = "select distinct busino from fs_businoconf"
    #sqlstr  = "select distinct busino,appno from abdt_unitinfo where appno in ('AG2008','AG2012')"
    sqlstr  = " select busino,bankno from fs_businoinfo "
    #end


    AfaLoggerFunc.tradeInfo( sqlstr )

    fsrecords = AfaDBFunc.SelectSql( sqlstr )
    if fsrecords == None or len(fsrecords)==0 :
        AfaLoggerFunc.tradeInfo("���ҵ�λ��Ϣ���쳣")
        sys.exit(1)

    i=0
    for i in range( len(fsrecords) ):
        #bgein 20100528 �������޸�
        #TradeContext.appNo        = 'AG2008'
        TradeContext.bankbm        = fsrecords[i][1].strip()
        if( TradeContext.bankbm == '012' ):
            TradeContext.appNo = 'AG2008';
        else:
            TradeContext.appNo = 'AG2012';
        #end


        TradeContext.busiNo       = fsrecords[i][0].strip()

        AfaLoggerFunc.tradeInfo("��λ����:" + TradeContext.busiNo)

        #=============�ж�Ӧ��״̬========================
        if not ChkAppStatus( ) :
            AfaLoggerFunc.tradeInfo('**********���շ�˰Ӧ��״̬������**********')
            continue

        #----------------�˸���Ϣͨ��socket�����ȡ�ýɿ������afe�ϣ�afaȥafeȥ�ɿ�����Ϣ�ļ�
        if not GetConfig() :
            AfaLoggerFunc.tradeInfo('��ȡftp�����ļ�ʧ��')
            sys.exit(1)

        #ƴ�ɵ���������
        TradeContext.TemplateCode   =   "3001"
        #TradeContext.sysId          =   "AG2008"
        TradeContext.sysId          =   TradeContext.appNo
        TradeContext.__respFlag__   =   "0"

        #=============�������ͨѶͨѶ====================
        AfaAfeFunc.CommAfe()
        if( TradeContext.errorCode != '0000' ):
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            continue
            #sys.exit(0)
        else :
            if (  ftpfile ( TradeContext.bankbm + Party3Context.FileName ,Party3Context.FileName ) <0 ):
                AfaLoggerFunc.tradeInfo("û�����ص��ļ�")
                continue

            #��ʼ��ȡ�ļ�
            try:
                fp          =   open(TradeContext.BATCH_LDIR + TradeContext.bankbm + Party3Context.FileName,"rb")
                recs        =   fp.read()

                if not recs :
                    AfaLoggerFunc.tradeInfo( "�ļ�Ϊ��" )
                    continue

            except Exception, e:
                AfaLoggerFunc.tradeInfo( "û�������ļ������ļ�Ϊ��" )
                continue

            #��һ�����ݲ��Ǽ�¼������������
            rec     =   recs.split( chr(12) )
            sep     =   chr(31)

            for i in range( 1,len(rec) ):

                #���ڶ�����¼�Ƿ�Ϊ��
                if not rec[i]:
                    AfaLoggerFunc.tradeInfo ( "��ǰ�ֶ��Ѿ�Ϊ��" )
                    continue

                AfaLoggerFunc.tradeInfo( "rec=" + rec[i] )
                AfaLoggerFunc.tradeInfo( "recl=" + str(rec[i].split(sep)) )


                #���ȼ���˸���Ϣ�Ƿ����ع������������������˸�״̬����֮�����һ����¼
                sqlstr = "select * from fs_fc06 where afc060='" + (rec[i].split(sep))[9] + "'"
                sqlstr = sqlstr + " AND AFC306='" + (rec[i].split( sep ))[0] + "'"
                sqlstr = sqlstr + " AND AAA010='" + (rec[i].split( sep ))[1] + "'"

                AfaLoggerFunc.tradeInfo( sqlstr )
                records = AfaDBFunc.SelectSql( sqlstr )
                if( records == None ):
                    TradeContext.errorCode  =   "0001"
                    TradeContext.errorMsg   =   "�����˸���Ϣ�쳣"
                    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                    continue

                #���û�в��ҵ��˸����
                if len( records )==0:

                    #����¼��д�����ݿ���
                    fields  =   "AFC306,AAA010,AFC041,AFA050,AFC061,AFC062,AFC063,AFC064,AAZ016,AFC060,AAZ015,DATE,TIME"
                    sqlstr  =   "INSERT INTO FS_FC06(" + fields + ") VALUES("
                    for item in rec[i].split( sep ):
                        sqlstr  =  sqlstr   +  "'" + item + "',"

                    sqlstr      =  sqlstr +  "'" + TradeContext.workDate  + "',"
                    sqlstr      =  sqlstr +  "'" + TradeContext.workTime  + "')"

                    AfaLoggerFunc.tradeInfo( sqlstr )

                    if( AfaDBFunc.InsertSqlCmt( sqlstr ) < 1 ):
                        AfaLoggerFunc.tradeInfo ( "�������ݿ�ʧ��"  + AfaDBFunc.sqlErrMsg )

                #������ҵ����˸���ţ������״̬λ
                else:

                    AfaLoggerFunc.tradeInfo( '���²���' )

                    sqlstr  =   "update fs_fc06 set aaz015='" + (rec[i].split( sep ))[10] + "' where afc060='" + (rec[i].split( sep ))[9] + "'"
                    sqlstr  =   sqlstr + " AND AFC306='" + (rec[i].split( sep ))[0] + "'"
                    sqlstr  =   sqlstr + " AND AAA010='" + (rec[i].split( sep ))[1] + "'"

                    AfaLoggerFunc.tradeInfo( sqlstr )

                    if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
                        TradeContext.errorCode, TradeContext.errorMsg='0001', '�����˸�״̬ʧ��'
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                        continue

    AfaLoggerFunc.tradeInfo('**********���շ�˰�˸���Ϣ���ؽ���**********')
    sys.exit(0)
