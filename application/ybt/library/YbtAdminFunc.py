# -*- coding: gbk -*-
################################################################################
# �ļ����ƣ�YbtAdminFunc.py
# �ļ���ʶ��
# ժ    Ҫ���м�ҵ��ͨ�ù����
#
# ��ǰ�汾��1.0
# ��    �ߣ�CYG
# ������ڣ�2010-09-06
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
################################################################################
import TradeContext, LoggerHandler, sys, os, time, AfaDBFunc, AfaUtilTools, ConfigParser, HostContext, HostComm
from types import *

cronLogger = LoggerHandler.getLogger( 'cron' )

#����λ������������
def getTimeFromNow( offsetDays, format = "%Y%m%d" ):
    secs = time.time( ) + offsetDays * 3600 * 24
    return time.strftime( format, time.localtime( secs ) )


#��ȡ���������ļ�����Ϣ
def GetCronConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.CRON_TRACE   = config.get('CRON', 'TRACE')
        TradeContext.CRON_CYCTIME = config.get('CRON', 'CYCTIME')

        return True

    except Exception, e:
        print '��ȡ�����ļ��쳣:' + str(e)
        return False


#=========================��־==================================================
def WrtLog(logstr):

    if ( TradeContext.existVariable('CRON_TRACE') ):

        if ( TradeContext.CRON_TRACE   == 'off' ):
            #�������־
            return True
        
        #elif ( TradeContext.CRON_TRACE == 'dsdf' ):
        #    #����־����
        #    return True
        #    
        #elif ( TradeContext.CRON_TRACE == 'aix'  ):
        #    #���ļ����
        #    return True

        elif ( TradeContext.CRON_TRACE == 'file' ):
            #���ļ����
            cronLogger.info(logstr)

        elif ( TradeContext.CRON_TRACE == 'all' ):
            #���ļ�����Ļͬʱ���
            cronLogger.info(logstr)
            print logstr

        elif ( TradeContext.CRON_TRACE == 'stdout' ):
            #����Ļ���
            print logstr

    else:
        #Ĭ�����ļ�����Ļͬʱ���
        cronLogger.info(logstr)
        print logstr

    return True



#=========================��ȡ���������ļ�����Ϣ=========================
def GetLappConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOST_HOSTIP   = config.get('HOST_DZ', 'HOSTIP')
        TradeContext.HOST_USERNO   = config.get('HOST_DZ', 'USERNO')
        TradeContext.HOST_PASSWD   = config.get('HOST_DZ', 'PASSWD')
        TradeContext.HOST_LDIR     = config.get('HOST_DZ', 'LDIR')
        TradeContext.HOST_RDIR     = config.get('HOST_DZ', 'RDIR')
        TradeContext.HOST_CDIR     = config.get('HOST_DZ', 'CDIR')
        TradeContext.HOST_BDIR     = config.get('HOST_DZ', 'BDIR')
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return True

    except Exception, e:
        print str(e)
        return False


#=========================��ȡ���������ļ�����Ϣ=========================
def GetCorpConfig(sysId, CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.CORP_HOSTIP   = config.get(sysId + '_DZ', 'HOSTIP')
        TradeContext.CORP_HOSTPORT = config.get(sysId + '_DZ', 'HOSTPORT')
        TradeContext.CORP_USERNO   = config.get(sysId + '_DZ', 'USERNO')
        TradeContext.CORP_PASSWD   = config.get(sysId + '_DZ', 'PASSWD')
        TradeContext.CORP_LDIR     = config.get(sysId + '_DZ', 'LDIR')
        TradeContext.CORP_RDIR     = config.get(sysId + '_DZ', 'RDIR')

        return True

    except Exception, e:
        print str(e)
        return False
        
#=========================��ȡ�����ļ�=========================
def GetAdminConfig(sysId=''):
    
    if not GetCronConfig():
        return False

    
    if not GetLappConfig():
        return False
    

    if len(sysId) > 0 :
        if not GetCorpConfig(sysId):
            return False

    return True


#=========================���ض����ļ�=========================
def GetDzFile(sysId, rfilename, lfilename):

    WrtLog('>>>���ض����ļ�')

    try:
        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/tmp/ftphost_' + sysId + '.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.HOST_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.HOST_USERNO + ' ' + TradeContext.HOST_PASSWD + '\n')

        #�����ļ�
        ftpFp.write('cd '  + TradeContext.HOST_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.HOST_LDIR + '\n')
        ftpFp.write('bin ' + '\n')
        ftpFp.write('get ' + rfilename + ' ' + lfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return False
        else:

            #�ж��ļ��Ƿ����
            sFileName = TradeContext.HOST_LDIR + "/" + lfilename
            if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
                return True
            else:
                WrtLog('>>>FTP���������ļ�ʧ��')
                return False

    except Exception, e:
        WrtLog(e)
        WrtLog('>>>FTP�����쳣')
        return False


#=========================�ϴ������ļ�=========================
def PutDzFile(sysId, lfilename, rfilename):

    WrtLog('>>>�ϴ������ļ�')
        
    try:
    
        #�ж��ļ��Ƿ����
        sFileName = TradeContext.CORP_LDIR + '/' + lfilename
        if ( not (os.path.exists(sFileName) and os.path.isfile(sFileName)) ):
            WrtLog('>>>�����ļ�������')
            return False

        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/tmp/ftpcorp_' + sysId + '.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.CORP_HOSTIP + ' ' + TradeContext.CORP_HOSTPORT + '\n')
        ftpFp.write('user ' + TradeContext.CORP_USERNO + ' ' + TradeContext.CORP_PASSWD   + '\n')

        #�ϴ��ļ�
        ftpFp.write('cd '  + TradeContext.CORP_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.CORP_LDIR + '\n')
        ftpFp.write('asc ' + '\n')
        ftpFp.write('put ' + lfilename + ' ' + rfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '
        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return False
        else:
            return True

    except Exception, e:
        WrtLog(e)
        WrtLog('>>>FTP�����쳣')
        return False
        
        
#=========================��ʽ���ļ�=========================
def FormatFile(sFileName, dFileName):

    try:
        srcFileName    = TradeContext.HOST_LDIR + '/' + sFileName
        dstFileName    = TradeContext.HOST_LDIR + '/' + dFileName

        #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D �����] [-S] [-R]
        CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
        fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/agent03.fld'
        cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName

        WrtLog( cmdstr )

        ret = os.system(cmdstr)
        if ( ret != 0 ):
            return False
        else:

            #�ж��ļ��Ƿ����
            if ( os.path.exists(dstFileName) and os.path.isfile(dstFileName) ):
                return True
            else:
                WrtLog('>>>��ʽ���ļ�ʧ��')
                return False

    except Exception, e:
        WrtLog(e)
        WrtLog('��ʽ���ļ��쳣')
        return False


######################################��ʵ������ˮ��Ϣ#####################################
def PrtRecInfo( prtbuf ):
    WrtLog('************************************************')
    WrtLog('����ҵ���       = ' + prtbuf[0])
   #WrtLog('����ί������     = ' + prtbuf[1])
   #WrtLog('����ί�к�       = ' + prtbuf[2])
    WrtLog('ǰ������         = ' + prtbuf[3])
    WrtLog('ǰ����ˮ��       = ' + prtbuf[4])
    WrtLog('��ϵͳ��������   = ' + prtbuf[5])
   #WrtLog('��������         = ' + prtbuf[6])
   #WrtLog('������ˮ��       = ' + prtbuf[7])
   #WrtLog('�����ֱ�־       = ' + prtbuf[8])
    WrtLog('���׻���         = ' + prtbuf[9])
    WrtLog('���׹�Ա         = ' + prtbuf[10])
   #WrtLog('���             = ' + prtbuf[11])
   #WrtLog('�������         = ' + prtbuf[12])
   #WrtLog('�跽�ʺ�         = ' + prtbuf[13])
   #WrtLog('�跽�ʻ�����     = ' + prtbuf[14])
   #WrtLog('�������         = ' + prtbuf[15])
   #WrtLog('����У�鷽ʽ     = ' + prtbuf[16])
   #WrtLog('����             = ' + prtbuf[17])
   #WrtLog('֧������         = ' + prtbuf[18])
   #WrtLog('֤������         = ' + prtbuf[19])
   #WrtLog('֤������         = ' + prtbuf[20])
   #WrtLog('֤��У���־     = ' + prtbuf[21])
    WrtLog('ƾ֤����         = ' + prtbuf[22])
    WrtLog('ƾ֤��           = ' + prtbuf[23])
   #WrtLog('����֧Ʊ��־     = ' + prtbuf[24])
   #WrtLog('ƾ֤�����־     = ' + prtbuf[25])
   #WrtLog('�����ʺ�         = ' + prtbuf[26])
   #WrtLog('�����ʻ�����     = ' + prtbuf[27])
   #WrtLog('����             = ' + prtbuf[28])
   #WrtLog('�����־         = ' + prtbuf[29])
    WrtLog('��ת��־         = ' + prtbuf[30])
   #WrtLog('�����ʱ�־       = ' + prtbuf[31])
    WrtLog('������           = ' + prtbuf[32])
   #WrtLog('ժҪ����         = ' + prtbuf[33])
   #WrtLog('ժҪ˵��         = ' + prtbuf[34])
   #WrtLog('����У���־     = ' + prtbuf[35])
   #WrtLog('������         = ' + prtbuf[36])
   #WrtLog('�ŵ� 2 ��Ϣ      = ' + prtbuf[37])
   #WrtLog('�ŵ� 3 ��Ϣ      = ' + prtbuf[38])
    WrtLog('������Ϣ 1       = ' + prtbuf[39])
   #WrtLog('������Ϣ 2       = ' + prtbuf[40])
   #WrtLog('�����ʺ�         = ' + prtbuf[41])
   #WrtLog('�����������     = ' + prtbuf[42])
   #WrtLog('��������         = ' + prtbuf[43])
   #WrtLog('����ʱ��         = ' + prtbuf[44])
   #WrtLog('���ʻ���         = ' + prtbuf[45])
   #WrtLog('���ʹ�Ա         = ' + prtbuf[46])
    WrtLog('������ˮ��       = ' + prtbuf[47])
   #WrtLog('��Ϣ��ʶ         = ' + prtbuf[48])
   #WrtLog('����/���ʱ�־    = ' + prtbuf[49])
    WrtLog('Ĩ�ʱ�־         = ' + prtbuf[50])
   #WrtLog('Ĩ������         = ' + prtbuf[51])
    WrtLog('Ĩ��������ˮ��   = ' + prtbuf[52])
   #WrtLog('��¼״̬         = ' + prtbuf[53])
    WrtLog('************************************************')





######################################�޸�ϵͳ########################################
def UpdSysStatus(sysId, sysStatus):

    WrtLog('>>>�޸�ϵͳ״̬')

    updSql = "UPDATE AFA_SYSTEM SET STATUS='" + sysStatus + "' WHERE SYSID='" + sysId + "'"

    WrtLog(updSql)

    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result <= 0 ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('>>>������:�޸�ϵͳ״̬,���ݿ��쳣')
        return False

    WrtLog('>>>�޸�ϵͳ״̬ ---> �ɹ�')

    return True



######################################�޸ĵ�λ########################################
def UpdUnitStatus(procType, sysId, unitNo, subUnitno=''):

    WrtLog('>>>�޸ĵ�λ״̬')

    if ( len(subUnitno)!=8 ):
        sTableName = "AFA_UNITADM"
    else:
        sTableName = "AFA_SUBUNITADM"

    #loginstatus            is 'ǩ��״̬(0-ǩ�� 1-ǩ��)';
    #dayendstatus           is '����״̬(0-δ�� 1-����)';
    #dayendtime             is '����ʱ��';
    #trxchkstatus           is '����״̬(0-δ�� 1-�Ѷ������� 2-���������ʳɹ� 3-����������ʧ��)';
    #trxchktime             is '����ʱ��';


    #��ȡʱ��
    sysTime = AfaUtilTools.GetSysTime( )

    updSql = ""

    if ( procType == 1 ):
        #����
        updSql = "UPDATE " + "%s" + " SET LOGINSTATUS='1',"
        updSql = updSql + "DAYENDSTATUS='0',"
        updSql = updSql + "DAYENDTIME='"   + sysTime + "',"
        updSql = updSql + "TRXCHKSTATUS='0',"
        updSql = updSql + "TRXCHKTIME='"   + sysTime + "' "

    else:
        #�ر�
        updSql = "UPDATE " + "%s" + " SET LOGINSTATUS='0',"
        updSql = updSql + "DAYENDSTATUS='1',"
        updSql = updSql + "DAYENDTIME='"   + sysTime + "',"
        updSql = updSql + "TRXCHKSTATUS='1',"
        updSql = updSql + "TRXCHKTIME='"   + sysTime + "' "

    updSql = updSql + "WHERE SYSID='" + sysId + "' AND UNITNO='" + unitNo + "'"

    updSql1 = updSql %(sTableName)

    WrtLog(updSql1)

    result = AfaDBFunc.UpdateSqlCmt( updSql1 )
    if ( result <= 0 ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('>>>������:�޸ĵ�λ״̬1,���ݿ��쳣')
        return False

    if sTableName=="AFA_SUBUNITADM":
        updSql2 = updSql %('AFA_UNITADM')
        WrtLog(updSql2)
        result = AfaDBFunc.UpdateSqlCmt( updSql1 )
        if ( result <= 0 ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            WrtLog('>>>������:�޸ĵ�λ״̬2,���ݿ��쳣')
            return False
    
    WrtLog('>>>�޸ĵ�λ״̬ ---> �ɹ�')

    return True
    

######################################���������ļ�#####################################
def DownLoadFile(sysId, trxDate):

    WrtLog('>>>���������ļ�')

    try:

        #ͨѶ�����
        HostContext.I1TRCD = '8818'                         #����������
        HostContext.I1SBNO = "3400008889"                   #�ý��׵ķ������(��������)
        HostContext.I1USID = '999986'                       #���׹�Ա��
        HostContext.I1AUUS = ""                             #��Ȩ��Ա
        HostContext.I1AUPS = ""                             #��Ȩ��Ա����
        HostContext.I1WSNO = ""                             #�ն˺�
        HostContext.I1CLDT = "00000000"                     #����ί������
        HostContext.I1UNSQ = '000000000000'                 #����ί�к�
        HostContext.I1NBBH = sysId                          #����ҵ���(AG2???)
        HostContext.I1DATE = trxDate                        #��ϵͳ����
        HostContext.I1FINA = sysId + trxDate[4:]            #�´��ļ�����

        HostTradeCode = "8818".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8818.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            WrtLog('>>>������=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return False

        else:
            if ( HostContext.O1MGID != 'AAAAAAA' ):
                WrtLog('>>>������=[' + str(HostContext.O1MGID) + ']:' +  HostContext.O1INFO)
                return False

            else:
                WrtLog('���ؽ��:�ظ�����=' + HostContext.O1ACUR)                          #�ظ�����
                WrtLog('���ؽ��:��������=' + HostContext.O1TRDT)                          #��������
                WrtLog('���ؽ��:����ʱ��=' + HostContext.O1TRTM)                          #����ʱ��
                WrtLog('���ؽ��:��Ա��ˮ=' + HostContext.O1TLSQ)                          #��Ա��ˮ
                WrtLog('���ؽ��:�ɹ���־=' + HostContext.O1OPFG)                          #�Ƿ��ύ�ɹ�(0-�ɹ�,1-ʧ��)

                #�������������ļ�
                rFileName = sysId + trxDate[4:]
                lFileName = sysId + '_' + trxDate + '_1'
                if not GetDzFile(sysId, rFileName, lFileName):
                    WrtLog('>>>������:�������������ļ�ʧ��')
                    return False

                dFileName = sysId + '_' + trxDate + '_2'
                if not FormatFile(lFileName, dFileName):
                    WrtLog('>>>������:ת�����������ļ�ʧ��')
                    return False

                WrtLog('>>>���������ļ� ---> �ɹ�')

        return True

    except Exception, e:
        WrtLog(str(e))
        WrtLog('>>>���������ļ� ---> �쳣')
        return False




######################################��ʼ����ˮ��־###################################
def InitData(sysId,unitNo,trxDate):

    WrtLog('>>>��ʼ����ˮ��־')
    TradeContext.serialFlag = '0'

    updSql =  "UPDATE AFA_MAINTRANSDTL SET CHKFLAG='*' WHERE SYSID='" + sysId + "' AND WORKDATE='" + trxDate + "' AND UNITNO='" + unitNo + "'"

    WrtLog(updSql)

    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result < 0 ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('>>>������:��ʼ����ˮ��־,���ݿ��쳣')
        TradeContext.serialFlag = '0'
        return False

    if ( result == 0 ):
        WrtLog('>>>������:��ϵͳû���κ���ˮ��Ϣ')
        TradeContext.serialFlag = '0'
        return False

    WrtLog('>>>��ʼ����ˮ��־ ---> �ɹ�')

    return True



######################################��ʹ�����ˮ#####################################
def MatchData(sysId,unitNo,trxDate):

    WrtLog('>>>��ʹ�����ˮ')

    try:
        #���������ļ�
        if not DownLoadFile(sysId, trxDate):
            return False

        #��ʼ����ˮ��־
        if not InitData(sysId,unitNo,trxDate):
            return False

        totalnum = 0
        totalamt = 0

        #�����������ļ�
        sFileName = TradeContext.HOST_LDIR + '/' + sysId + '_' + trxDate + '_2'


        hFp = open(sFileName, "r")


        #��ȡһ��
        linebuf = hFp.readline()


        while ( len(linebuf) > 0 ):


            #�ж϶�����ˮ�ĺϷ���
            if ( len(linebuf) < 996 ):
                WrtLog('�����������ļ���ʽ����(����),����')
                hFp.close()
                return False


            #��ֶ�����ˮ
            swapbuf = linebuf[0:996].split('<fld>')


            #��ȡһ��
            linebuf = hFp.readline()


            #���˷Ǳ�Ӧ�ö�����ˮ
            if ( swapbuf[0].strip()!=sysId or swapbuf[3].strip()!=trxDate or swapbuf[5].strip()!=trxDate ):
                WrtLog("===������===")
                PrtRecInfo( swapbuf )
                continue


            #�Ȳ�ѯ���ݿ��м�¼�Ƿ����
            sqlstr = "SELECT BRNO,TELLERNO,REVTRANF,AMOUNT,BANKSTATUS,CORPSTATUS,AGENTSERIALNO,WORKDATE,ERRORMSG FROM AFA_MAINTRANSDTL WHERE"
            sqlstr = sqlstr + "     SYSID         = '"  + sysId              + "'"
            sqlstr = sqlstr + " AND WORKDATE      = '"  + trxDate            + "'"
            sqlstr = sqlstr + " AND AGENTSERIALNO = '"  + swapbuf[4].strip() + "'"
            sqlstr = sqlstr + " AND UNITNO        = '"  + unitNo             + "'"

            WrtLog(sqlstr)

            ChkFlag = '*'
            statusFlag = '0'            #������ʶ��¼�е�BANKSTATUS��״̬�����BANKSTATUS��״̬��Ϊ0����ñ�־��ֵΪ1
            
            records = AfaDBFunc.SelectSql( sqlstr )

            if ( records==None ):
                WrtLog( AfaDBFunc.sqlErrMsg )
                WrtLog('��ѯ��ˮ��Ϣ�쳣,����')
                hFp.close()
                return False


            if ( len(records) == 0 ):
                WrtLog('���ݿ��м�¼ƥ��ʧ��(�����޼�¼)')
                continue

            else:
                h_tradeamt = long(float(swapbuf[32].strip())  *100 + 0.1)
                m_tradeamt = long(float(records[0][3].strip())*100 + 0.1)

                if ( swapbuf[9].strip() != records[0][0].strip() ):
                    WrtLog('���ݿ��м�¼ƥ��ʧ��(�����Ų���):' + swapbuf[9].strip()  + '|' + records[0][0] + '|')
                    PrtRecInfo( swapbuf )
                    ChkFlag = '2'

                elif ( swapbuf[10].strip() != records[0][1] ):
                    WrtLog('���ݿ��м�¼ƥ��ʧ��(��Ա�Ų���):' + swapbuf[10].strip() + '|' + records[0][1] + '|')
                    PrtRecInfo( swapbuf )
                    ChkFlag = '3'

                elif ( h_tradeamt != m_tradeamt ):
                    WrtLog('���ݿ��м�¼ƥ��ʧ��(�������):' + str(h_tradeamt) + '|' + str(m_tradeamt) + '|')
                    PrtRecInfo( swapbuf )
                    ChkFlag = '4'

                elif ( swapbuf[50].strip() == '1' ):
                    ChkFlag = '1'

                else:
                    if records[0][4] != '0':
                        WrtLog( '���ݿ��м�¼״̬������������������̨�����Ա��ֺ�����һ��' )
                        statusFlag = 1
                        
                        #�Ѵ��ڸ���������Ϣ��¼����AFA_DZERROR��
                        WrtLog( '��¼��̨��������һ�µ���ˮ��Ϣ' )
                        occurTime = time.strftime('%Y%m%d%H%M%S',time.localtime())
                        insertSql = "insert into afa_dzerror(OCCURTIME,SERIALNO,WORKDATE,AMOUNT,BANKSTATUS,ERROEMSG) values("
                        insertSql = insertSql + "'" + occurTime     +"',"
                        insertSql = insertSql + "'" + records[0][6] + "',"
                        insertSql = insertSql + "'" + records[0][7] + "',"
                        insertSql = insertSql + "'" + records[0][3] + "',"
                        insertSql = insertSql + "'" + records[0][4] + "',"
                        insertSql = insertSql + "'" + records[0][8] + "')"
                        WrtLog( '��¼�����¼sql��' + insertSql )
                        
                        result = AfaDBFunc.InsertSqlCmt( insertSql )
                        if ( result < 0 ):
                            WrtLog( AfaDBFunc.sqlErrMsg )
                            WrtLog( '��¼����������������̨���ݲ�һ��ʧ��' )
                            return False
                            
                    ChkFlag = '0'

            #�޸������ݿ����ƥ��
            updSql = "UPDATE AFA_MAINTRANSDTL SET CHKFLAG='" + ChkFlag + "'"
            if statusFlag == 1 :
                updSql = updSql + " ,BANKSTATUS = '0'"
            updSql = updSql + " WHERE SYSID         = '" + sysId              + "'"
            updSql = updSql + " AND   WORKDATE      = '" + trxDate            + "'"
            updSql = updSql + " AND   AGENTSERIALNO = '" + swapbuf[4].strip() + "'"
            updSql = updSql + " AND   UNITNO        = '" + unitNo             + "'"

            WrtLog(updSql)

            result = AfaDBFunc.UpdateSqlCmt( updSql )
            if ( result <= 0 ):
                WrtLog( AfaDBFunc.sqlErrMsg )
                WrtLog('>>>������:�޸���ƥ����ˮ״̬,���ݿ��쳣')
                return False

            totalnum = totalnum + 1
            totalamt = totalamt + m_tradeamt

        hFp.close()

        WrtLog( 'ƥ���¼��=' + str(totalnum) + ",ƥ���ܽ��=" + str(totalamt) )

        WrtLog( '>>>��ʹ�����ˮ ---> �ɹ�' )

        return True

    except Exception, e:
        hFp.close()
        WrtLog(str(e))
        WrtLog('>>>��ʹ�����ˮ ---> �쳣')
        return False





######################################���ɱ����ļ�#####################################
def CrtReportFile(sysId,unitNo,trxDate):

    WrtLog('>>>���ɱ����ļ�')

    colName = "agentserialno,workdate,worktime,sysid,unitno,subunitno,agentflag,trxcode,zoneno,brno,tellerno,"
    colName = colName + "cashtelno,authtellerno,channelcode,channelserno,termid,customerid,userno,subuserno,username,acctype,"
    colName = colName + "draccno,craccno,vouhtype,vouhno,vouhdate,currType,currFlag,amount,subamount,revtranf,preagentserno,"
    colName = colName + "bankstatus,bankcode,bankserno,corpstatus,corpcode,corpserno,corptime,errormsg,chkflag,corpchkflag,appendflag,"
    colName = colName + "note1,note2,note3,note4,note5,note6,note7,note8,note9,note10"

    selSql = "SELECT " + colName + "FROM AFA_MAINTRANSDTL WHERE SYSID='" + sysId + "' AND UNITNO='" + unitNo + "' AND WORKDATE='" + trxDate + "' AND CHKFLAG='0' ORDER BY WORKTIME ASC"

    WrtLog(selSql)

    records = AfaDBFunc.SelectSql( sqlstr, 10000 )

    if ( records==None ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('���ɱ����ļ��쳣,����')
        return False

    if ( len(records) == 0 ):
        WrtLog('���ݿ���û����ˮ��Ϣ')
        return False

    records=AfaUtilTools.ListFilterNone( records )

    #�����ļ�
    bankRpt1 = TradeContext.HOST_BDIR + "/" + sysId + "_" + unitNo + "_" + trxDate + ".SUC"
    bankRpt2 = TradeContext.HOST_BDIR + "/" + sysID + "_" + unitNo + "_" + trxDate + ".ERR"
    sfp= open(bankRpt1,  "w")
    efp= open(bankRpt2,  "w")

    iRecNum=0
    for i in range(0, len(records)):
        prtBuffer = ""
        prtBuffer = prtBuffer + str(records[i][0]).strip() + "|"  #agentserialno
        prtBuffer = prtBuffer + str(records[i][1]).strip() + "|"  #workdate
        prtBuffer = prtBuffer + str(records[i][2]).strip() + "|"  #worktime
        prtBuffer = prtBuffer + str(records[i][3]).strip() + "|"  #sysid
        prtBuffer = prtBuffer + str(records[i][4]).strip() + "|"  #unitno
        prtBuffer = prtBuffer + str(records[i][5]).strip() + "|"  #subunitno
        prtBuffer = prtBuffer + str(records[i][6]).strip() + "|"  #agentflag
        prtBuffer = prtBuffer + str(records[i][7]).strip() + "|"  #trxcode
        prtBuffer = prtBuffer + str(records[i][8]).strip() + "|"  #zoneno
        prtBuffer = prtBuffer + str(records[i][9]).strip() + "|"  #brno
        prtBuffer = prtBuffer + str(records[i][10]).strip()+ "|"  #tellerno
        prtBuffer = prtBuffer + str(records[i][11]).strip()+ "|"  #cashtelno
        prtBuffer = prtBuffer + str(records[i][12]).strip()+ "|"  #authtellerno
        prtBuffer = prtBuffer + str(records[i][13]).strip()+ "|"  #channelcode
        prtBuffer = prtBuffer + str(records[i][14]).strip()+ "|"  #channelserno
        prtBuffer = prtBuffer + str(records[i][15]).strip()+ "|"  #termid
        prtBuffer = prtBuffer + str(records[i][16]).strip()+ "|"  #customerid
        prtBuffer = prtBuffer + str(records[i][17]).strip()+ "|"  #userno
        prtBuffer = prtBuffer + str(records[i][18]).strip()+ "|"  #subuserno
        prtBuffer = prtBuffer + str(records[i][19]).strip()+ "|"  #username
        prtBuffer = prtBuffer + str(records[i][20]).strip()+ "|"  #acctype
        prtBuffer = prtBuffer + str(records[i][21]).strip()+ "|"  #draccno
        prtBuffer = prtBuffer + str(records[i][22]).strip()+ "|"  #craccno
        prtBuffer = prtBuffer + str(records[i][23]).strip()+ "|"  #vouhtype
        prtBuffer = prtBuffer + str(records[i][24]).strip()+ "|"  #vouhno
        prtBuffer = prtBuffer + str(records[i][25]).strip()+ "|"  #vouhdate
        prtBuffer = prtBuffer + str(records[i][26]).strip()+ "|"  #currType
        prtBuffer = prtBuffer + str(records[i][27]).strip()+ "|"  #currFlag
        prtBuffer = prtBuffer + str(records[i][28]).strip()+ "|"  #amount
        prtBuffer = prtBuffer + str(records[i][29]).strip()+ "|"  #subamount
        prtBuffer = prtBuffer + str(records[i][30]).strip()+ "|"  #revtranf
        prtBuffer = prtBuffer + str(records[i][31]).strip()+ "|"  #preagentserno
        prtBuffer = prtBuffer + str(records[i][32]).strip()+ "|"  #bankstatus
        prtBuffer = prtBuffer + str(records[i][33]).strip()+ "|"  #bankcode
        prtBuffer = prtBuffer + str(records[i][34]).strip()+ "|"  #bankserno
        prtBuffer = prtBuffer + str(records[i][35]).strip()+ "|"  #corpstatus
        prtBuffer = prtBuffer + str(records[i][36]).strip()+ "|"  #corpcode
        prtBuffer = prtBuffer + str(records[i][37]).strip()+ "|"  #corpserno
        prtBuffer = prtBuffer + str(records[i][38]).strip()+ "|"  #corptime
        prtBuffer = prtBuffer + str(records[i][39]).strip()+ "|"  #errormsg
        prtBuffer = prtBuffer + str(records[i][40]).strip()+ "|"  #chkflag
        prtBuffer = prtBuffer + str(records[i][41]).strip()+ "|"  #corpchkflag
        prtBuffer = prtBuffer + str(records[i][42]).strip()+ "|"  #appendflag
        prtBuffer = prtBuffer + str(records[i][43]).strip()+ "|"  #note1
        prtBuffer = prtBuffer + str(records[i][44]).strip()+ "|"  #note2
        prtBuffer = prtBuffer + str(records[i][45]).strip()+ "|"  #note3
        prtBuffer = prtBuffer + str(records[i][46]).strip()+ "|"  #note4
        prtBuffer = prtBuffer + str(records[i][47]).strip()+ "|"  #note5
        prtBuffer = prtBuffer + str(records[i][48]).strip()+ "|"  #note6
        prtBuffer = prtBuffer + str(records[i][49]).strip()+ "|"  #note7
        prtBuffer = prtBuffer + str(records[i][50]).strip()+ "|"  #note8
        prtBuffer = prtBuffer + str(records[i][51]).strip()+ "|"  #note9
        prtBuffer = prtBuffer + str(records[i][52]).strip()+ "|"  #note10
        iRecNum = iRecNum + 1

        if str(records[i][40]).strip() == "0" :
            sfp.write(prtBuffer + '\n')

        elif (str(records[i][40]).strip()=="2" or str(records[i][40]).strip()=="3" or str(records[i][40]).strip()=="3"):
            efp.write(prtBuffer + '\n')

    sfp.close()
    cfp.close()
    efp.close()
    WrtLog('>>>��¼��=' + str(iRecNum))
        
    WrtLog('>>>���ɱ����ļ� ---> �ɹ�')

    return True
