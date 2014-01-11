###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰���ؽɿ�����Ϣ
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��15��
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import ConfigParser, sys, AfaDBFunc, Party3Context, AfaUtilTools
import os, HostContext, AfaAfeFunc, AfaLoggerFunc, time
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
        WrtErrLog(e)
        return False

#FTP������
def ftpfile( sfilename, rfilename):

    try:
        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/AhfsFtpJks' + '.sh'
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
        WrtErrLog(e)
        AfaLoggerFunc.tradeInfo('FTP�����쳣')
        return -1

def ChkAppStatus():
    sqlstr  =   "select status from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino ='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
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
    AfaLoggerFunc.tradeInfo('**********���շ�˰�ɿ�����Ϣ���ؿ�ʼ**********')

    #��ʼ��TradeContext
    TradeContext.workDate       =   AfaUtilTools.GetSysDate( )
    TradeContext.workTime       =   AfaUtilTools.GetSysTime( )
    TradeContext.zoneno         =   ""
    TradeContext.brno           =   ""
    TradeContext.teller         =   ""
    TradeContext.authPwd        =   ""
    TradeContext.termId         =   ""
    TradeContext.TransCode      =   "8440"

    #begin 20100525 �������޸� ���Ӵ�������ҵ������ѯ����
    #sqlstr  = "select distinct busino from abdt_unitinfo where appno='AG2008'"
    #sqlstr  = "select distinct busino, appno from abdt_unitinfo where appno in ('AG2008','AG2012')"
    sqlstr  = " select busino,bankno from fs_businoinfo "
    #end

    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None:
        AfaLoggerFunc.tradeInfo("���ҵ�λ��Ϣ���쳣" + AfaDBFunc.sqlErrMsg)
        sys.exit(1)

    elif len(records)==0 :
        AfaLoggerFunc.tradeInfo("û���κε�λ��Ϣ")
        sys.exit(1)


    for i in range( len(records) ):

        #begin 20100525 �������޸�
        #TradeContext.appNo        = 'AG2008'
        TradeContext.bankbm        = records[i][1].strip()
        if( TradeContext.bankbm == '012' ):
            TradeContext.appNo = 'AG2008';
        else:
            TradeContext.appNo = 'AG2012';
        #end

        TradeContext.busiNo       = records[i][0].strip()

        AfaLoggerFunc.tradeInfo("ҵ�����:" + TradeContext.appNo)
        AfaLoggerFunc.tradeInfo("��λ����:" + TradeContext.busiNo)

        #=============�ж�Ӧ��״̬========================
        if not ChkAppStatus( ) :
            AfaLoggerFunc.tradeInfo('**********���շ�˰Ӧ��״̬������**********')
            continue

        #----------------�ɿ�����Ϣͨ��socket�����ȡ�ýɿ������afe�ϣ�afaȥafeȥ�ɿ�����Ϣ�ļ�
        if not GetConfig() :
            AfaLoggerFunc.tradeInfo('��ȡftp�����ļ�ʧ��')
            sys.exit(1)

        #ƴ�ɵ���������
        TradeContext.TemplateCode   =   "3001"

        #begin 20100525 �������޸�
        #TradeContext.sysId          =   "AG2008"
        TradeContext.sysId          =   TradeContext.appNo
        #end

        #=============�������ͨѶͨѶ====================
        TradeContext.__respFlag__='0'
        AfaAfeFunc.CommAfe()

        if( TradeContext.errorCode != '0000' ):
            AfaLoggerFunc.tradeInfo("���������ش��󣬳����˳�")
            continue

        else :
            if (  ftpfile ( Party3Context.FileName ,Party3Context.FileName ) <0 ):
                AfaLoggerFunc.tradeInfo("û�����ص��ļ�")
                continue

            #��ʼ��ȡ�ļ�
            try:
                fp          =   open(TradeContext.BATCH_LDIR+Party3Context.FileName,"rb")
                recs        =   fp.read()

                if not recs :
                    AfaLoggerFunc.tradeInfo( "�ļ�Ϊ��" )
                    continue

            except Exception, e:
                AfaLoggerFunc.tradeInfo( "û�������ļ������ļ�Ϊ��" )
                continue


            #����¼��д�����ݿ���

            #begin 20100526 �������޸ģ����������bankno�ֶ�
            #fields  =   "AFC001,AFA031,AFC163,AFC187,AFC183,AFC157,AFC181,AFA040,AFC180,AFA051,AFC166,AFC155,AFC153,AFC154,AFA183,AFA184,AFA185,AFA091, AAA010,DATE,TIME"
            fields  =   "AFC001,AFA031,AFC163,AFC187,AFC183,AFC157,AFC181,AFA040,AFC180,AFA051,AFC166,AFC155,AFC153,AFC154,AFA183,AFA184,AFA185,AFA091, AAA010,DATE,TIME,BANKNO"
            #end

            sqlstr  =   "INSERT INTO FS_FC70(" + fields + ") VALUES("

            #��һ�����ݲ��Ǽ�¼������������
            rec     =   recs.split( chr(12) )

            #print rec,"��¼������",len(rec)

            sep         =   chr(31)
            itemCnt     =   len( rec[1].split( sep ) )

            for i in range( 1,len(rec) ):
                sqlstr1 =   sqlstr

                #���ڶ�����¼�Ƿ�Ϊ��
                if not rec[i]:
                    AfaLoggerFunc.tradeInfo ( "��ǰ�ֶ��Ѿ�Ϊ��" )
                    break

                for item in rec[i].split( sep ):
                    sqlstr1  =  sqlstr1   +  "'" + item + "',"

                sqlstr1         =   sqlstr1 + "'" + TradeContext.workDate + "',"

                #begin 20100526 �������޸�
                #sqlstr1         =   sqlstr1 + "'" + TradeContext.workTime + "')"
                sqlstr1         =   sqlstr1 + "'" + TradeContext.workTime + "',"
                sqlstr1         =   sqlstr1 + "'" + TradeContext.bankbm   + "')"
                #end

                AfaLoggerFunc.tradeInfo( sqlstr1 )

                if( AfaDBFunc.InsertSqlCmt( sqlstr1 ) < 1 ):
                    AfaLoggerFunc.tradeInfo ( "�������ݿ�ʧ��:"  + AfaDBFunc.sqlErrMsg )

    AfaLoggerFunc.tradeInfo('**********���շ�˰�ɿ�����Ϣ���ؽ���**********')
    sys.exit(0)

