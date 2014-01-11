# -*- coding: gbk -*-
###############################################################################
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰����
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��22��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext,ConfigParser,AfaUtilTools,AfaDBFunc,os,AfaLoggerFunc,HostContext,HostComm,sys,datetime
from types import *


#��ȡ���������ļ�����Ϣ
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
        TradeContext.CORP_CDIR     = config.get('HOST_DZ', 'CDIR')
        TradeContext.BANK_CDIR     = config.get('HOST_DZ', 'BDIR')
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return 0

    except Exception, e:
        print str(e)
        return -1

#���ض����ļ�
def GetDzFile(rfilename, lfilename):

    try:
        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/ftphost.sh'
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

        AfaLoggerFunc.tradeInfo('�����ļ�' + rfilename + lfilename)

        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return -1
        else:
            return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('FTP�����쳣')
        return -1

#��ʽ���ļ�
def FormatFile(sFileName, dFileName):

    try:
        srcFileName    = TradeContext.HOST_LDIR + '/' + sFileName
        dstFileName    = TradeContext.HOST_LDIR + '/' + dFileName

        #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D �����] [-S] [-R]
        CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
        fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/agent03.fld'
        cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName

        AfaLoggerFunc.tradeInfo( cmdstr )


        ret = os.system(cmdstr)
        if ( ret != 0 ):
            return -1
        else:
            return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('��ʽ���ļ��쳣')
        return -1

##########################################ǩ��##########################################
def Ahdx_Login():

    try:
        sqlStr = "SELECT STATUS FROM ABDT_UNITINFO WHERE"
        sqlStr = sqlStr + " APPNO = '"      + TradeContext.appNo  + "'"
        sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busiNo + "'"
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        #AfaLoggerFunc.tradeInfo(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None or len(records) < 0):
            AfaLoggerFunc.tradeInfo('>>>�������:ǩ��ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","ǩ��ʧ��,���ݿ��쳣"
            return False

        elif ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('>>>�������:û�з��ָõ�λ��Ϣ,����ǩ��')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�з��ָõ�λ��Ϣ,����ǩ��"
            return False


        sqlStr = "UPDATE ABDT_UNITINFO SET STATUS='1' WHERE"
        sqlStr = sqlStr + " APPNO = '"      + TradeContext.appNo  + "'"
        sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busiNo + "'"
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        retcode = AfaDBFunc.UpdateSqlCmt( sqlStr )
        if (retcode==None or retcode <= 0):
            AfaLoggerFunc.tradeInfo('>>>�������:ǩ��ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","ǩ��ʧ��,���ݿ��쳣"
            return False

        AfaLoggerFunc.tradeInfo('>>>�������:ǩ���ɹ�')

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001",str(e)
        return False



##########################################ǩ��##########################################
def Ahdx_Logout():
    try:
        sqlStr = "SELECT STATUS FROM ABDT_UNITINFO WHERE"
        sqlStr = sqlStr + " APPNO = '"      + TradeContext.appNo  + "'"
        sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busiNo + "'"
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        #AfaLoggerFunc.tradeInfo(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None or len(records) < 0):
            AfaLoggerFunc.tradeInfo('>>>�������:ǩ��ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","ǩ��ʧ��,���ݿ��쳣"
            return False

        elif ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('>>>�������:û�з��ָõ�λ��Ϣ,����ǩ��')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�з��ָõ�λ��Ϣ,����ǩ��"
            return False

        sqlStr = "UPDATE ABDT_UNITINFO SET STATUS='2' WHERE"
        sqlStr = sqlStr + " APPNO = '"      + TradeContext.appNo  + "'"
        sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busiNo + "'"
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        retcode = AfaDBFunc.UpdateSqlCmt( sqlStr )
        if (retcode==None or retcode <= 0):
            AfaLoggerFunc.tradeInfo('>>>�������:ǩ��ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","ǩ��ʧ��,���ݿ��쳣"
            return False

        AfaLoggerFunc.tradeInfo('>>>�������:ǩ�˳ɹ�')

        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001",str(e)
        return False


##########################################���մ���##########################################
def Ahdx_DayEnd():

    try:
        sqlStr = "SELECT STATUS,BRNO FROM ABDT_UNITINFO WHERE"
        sqlStr = sqlStr + " APPNO = '"      + TradeContext.appNo  + "'"
        sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busiNo + "'"
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None or len(records) < 0):
            AfaLoggerFunc.tradeInfo('>>>�������:���մ���ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���մ���ʧ��,���ݿ��쳣"
            return False

        elif ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('>>>�������:û�з��ָõ�λ��Ϣ,�������մ���')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�з��ָõ�λ��Ϣ,�������մ���"
            return False

        #=====�Էǵ��յ��ˣ�����Ҫǩ��====
        if ( records[0][0] != '2' and (TradeContext.WORKDATE == TradeContext.workDate)):
            AfaLoggerFunc.tradeInfo('>>>�������:������ǩ�˲��ܽ������մ���')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","������ǩ�˲��ܽ������մ���"
            return False

        AfaLoggerFunc.tradeInfo('>>>�������������ļ�')

        #ͨѶ�����
        HostContext.I1TRCD = '8818'                        #����������
        HostContext.I1SBNO = records[0][1]                 #�ý��׵ķ������
        HostContext.I1USID = '999999'                      #���׹�Ա��
        HostContext.I1AUUS = ""                            #��Ȩ��Ա
        HostContext.I1AUPS = ""                            #��Ȩ��Ա����
        HostContext.I1WSNO = ""                            #�ն˺�
        HostContext.I1CLDT = "00000000"                    #����ί������
        HostContext.I1UNSQ = '000000000000'                #����ί�к�
        HostContext.I1NBBH = TradeContext.appNo            #����ҵ���(AG2003)
        HostContext.I1DATE = TradeContext.WORKDATE         #��ϵͳ����
        HostContext.I1FINA = TradeContext.appNo            #�´��ļ�����

        HostTradeCode = "8818".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8818.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AfaLoggerFunc.tradeInfo('>>>�������=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001", '[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg
            return False

        else:
            if ( HostContext.O1MGID != 'AAAAAAA' ):
                AfaLoggerFunc.tradeInfo('>>>�������=[' + str(HostContext.O1MGID) + ']:' +  HostContext.O1INFO)

                #���ɿ��ļ�
                fileName    =   TradeContext.HOST_LDIR + "/" + TradeContext.appNo + '_' + TradeContext.WORKDATE + '_2'
                fpFile      =   open( fileName,"w" )
                fpFile.close()
                AfaLoggerFunc.tradeInfo('>>>�������:û����������(�����˿��ļ�)')
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û����������(�����˿��ļ�)"
                return False

            else:
                #AfaLoggerFunc.tradeInfo('���ؽ��:�ظ�����=' + HostContext.O1ACUR)                          #�ظ�����
                #AfaLoggerFunc.tradeInfo('���ؽ��:��������=' + HostContext.O1TRDT)                          #��������
                #AfaLoggerFunc.tradeInfo('���ؽ��:����ʱ��=' + HostContext.O1TRTM)                          #����ʱ��
                #AfaLoggerFunc.tradeInfo('���ؽ��:��Ա��ˮ=' + HostContext.O1TLSQ)                          #��Ա��ˮ
                #AfaLoggerFunc.tradeInfo('���ؽ��:�ɹ���־=' + HostContext.O1OPFG)                          #�Ƿ��ύ�ɹ�(0-�ɹ�,1-ʧ��)

                #�������������ļ�
                rFileName = TradeContext.appNo
                lFileName = TradeContext.appNo + '_' + TradeContext.WORKDATE + '_1'
                if ( GetDzFile(rFileName, lFileName) < 0 ):
                    AfaLoggerFunc.tradeInfo('>>>�������:���մ���ʧ��(�����ļ�)')
                    TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���մ���ʧ��(�����ļ�)"
                    return False

                AfaLoggerFunc.tradeInfo('>>>ת�����������ļ�')
                dFileName = TradeContext.appNo + '_' + TradeContext.WORKDATE + '_2'
                if ( FormatFile(lFileName, dFileName) < 0 ):
                    AfaLoggerFunc.tradeInfo('>>>�������:���մ���ʧ��(��ʽ��)')
                    TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���մ���ʧ��(��ʽ��)"
                    return False

                AfaLoggerFunc.tradeInfo('>>>�������:���մ����ɹ�')

        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001",str(e)
        return False

def printRow( Contextlist,hp ):

    if ( len(Contextlist)!= 6 ):
        AfaLoggerFunc.tradeInfo( "���г��Ȳ���6" )
        return False

    else:
        lineList    =   []
        lineList.append( Contextlist[0] )
        lineList.append( Contextlist[1] )
        lineList.append( Contextlist[2] )
        lineList.append( Contextlist[3] )

        if   Contextlist[4].strip() == '1':
            lineList.append("��������")
            lineList.append(Contextlist[5].strip())
            lineList.append("")
        elif Contextlist[4].strip() == '2':
            lineList.append("�˸�")
            lineList.append("")
            lineList.append(Contextlist[5].strip())
        elif Contextlist[4].strip() == '3':
            lineList.append("�Ͻɹ���")
        elif Contextlist[4].strip() == '4':
            lineList.append("�Ͻ�ר��")
        elif Contextlist[4].strip() == '5':
            lineList.append("��������")
            lineList.append(Contextlist[5].strip())
            lineList.append("")

        if len(lineList) != 7 :
            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','ͳ����Ŀ��������'
            return False

        else:
            #ͳ�ƺϼƣ����ϴ�����ȥ�跽
            if not lineList[len(lineList)-2] and lineList[len(lineList)-1]:          #����Ϊ��,�跽����
                TradeContext.banlance   =   str( float(TradeContext.banlance)  - float(lineList[len(lineList)-1]) )
                lineList.append( TradeContext.banlance )
            elif not lineList[len(lineList)-1] and lineList[len(lineList)-2]:        #��������,�跽Ϊ��
                TradeContext.banlance   =   str( float(TradeContext.banlance)  + float(lineList[len(lineList)-2]) )
                lineList.append( TradeContext.banlance )
            else:
                TradeContext.errorCode,TradeContext.errorMsg    =   '0001','�����ȫ��Ϊ�ջ���ȫ����Ϊ��'
                return False

        for i in range(len(fieldWidthList)):
            hp.write("��")
            hp.write( lineList[i].center(fieldWidthList[i]) )

        hp.write("��")
        hp.write("\n")

##########################################���ʴ���##########################################
def Ahdx_DzSend():
    totalnum = 0
    totalamt = 0
    try:
        sqlStr = "SELECT STATUS FROM ABDT_UNITINFO WHERE"
        sqlStr = sqlStr + " APPNO = '"      + TradeContext.appNo  + "'"
        sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busiNo + "'"
        sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

        #AfaLoggerFunc.tradeInfo(sqlStr)

        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None or len(records) < 0):
            AfaLoggerFunc.tradeInfo('>>>�������:���ʴ���ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ʴ���ʧ��,���ݿ��쳣"
            return False

        elif ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo('>>>�������:û�з��ָõ�λ��Ϣ,���ܶ��ʴ���')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û�з��ָõ�λ��Ϣ,���ܶ��ʴ���"
            return False

        #=====�Էǵ����˲���Ҫǩ��====
        if ( records[0][0] != '2' and (TradeContext.WORKDATE == TradeContext.workDate)):
            AfaLoggerFunc.tradeInfo('>>>�������:������ǩ�˲��ܽ��ж��ʴ���')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","������ǩ�˲��ܽ��ж��ʴ���"
            return False

        sFileName = TradeContext.HOST_LDIR + '/' + TradeContext.appNo + '_' + TradeContext.WORKDATE + '_2'
        if ( not (os.path.exists(sFileName) and os.path.isfile(sFileName)) ):
            AfaLoggerFunc.tradeInfo("�����ļ�������,���������մ������ܽ��ж��ʴ���")
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","�����ļ�������,���������մ������ܽ��ж��ʴ���"
            return False

        hpTmp   =   open( sFileName,"r" )
        if not hpTmp.read() :
            AfaLoggerFunc.tradeInfo("����û���������뽻��")
            #begin 20100716 �������޸� ���ڴ˴���û���׳��쳣��ֹ���򣬹ʴ˴�errorCode����Ӧ����Ϊ0000
            #TradeContext.errorCode,TradeContext.errorMsg    =   "0001","����û�н���"
            TradeContext.errorCode,TradeContext.errorMsg    =   "0000","����û�н���"
            #end
            #return False

        #���ʳ�ʼ��
        sqlstr = "UPDATE FS_MAINTRANSDTL SET CHKFLAG='" + '*' + "' WHERE "
        sqlstr = sqlstr + " APPNO='"        + TradeContext.appNo    + "'"
        sqlstr = sqlstr + " AND BUSINO='"   + TradeContext.busiNo   + "'"
        sqlstr = sqlstr + " AND WORKDATE='" + TradeContext.WORKDATE + "'"

        AfaLoggerFunc.tradeInfo(sqlstr)

        retcode = AfaDBFunc.UpdateSqlCmt( sqlstr )
        if (retcode==None or retcode <= 0):
            AfaLoggerFunc.tradeInfo('û���κν�������')

        #�����������ļ�
        hFp = open(sFileName, "r")

        #��ȡһ��
        linebuf = hFp.readline()
        while ( len(linebuf) > 0 ):
            if ( len(linebuf) < 996 ):
                AfaLoggerFunc.tradeInfo('�����������ļ���ʽ����(����),����')
                hFp.close()
                return False

            swapbuf = linebuf[0:996].split('<fld>')

#            if ( len(swapbuf) != 55 ):
#                AfaLoggerFunc.tradeInfo('�����������ļ���ʽ����(����),����')
#                hFp.close()
#                return False

            #��ʾ��¼��Ϣ
            #PrtRecInfo(swapbuf)

            linebuf = hFp.readline()

            if ( swapbuf[0].strip()  != TradeContext.appNo or \
                 swapbuf[3].strip()  != TradeContext.WORKDATE or \
                 swapbuf[5].strip()  != TradeContext.WORKDATE ):
                continue

            #�Ȳ�ѯ���ݿ��м�¼�Ƿ����
            sqlstr = "SELECT BRNO,TELLERNO,REVTRANF,AMOUNT,BANKSTATUS,CORPSTATUS FROM FS_MAINTRANSDTL WHERE"
            sqlstr = sqlstr + " APPNO='"        + TradeContext.appNo    + "'"
            sqlstr = sqlstr + " AND BUSINO='"   + TradeContext.busiNo   + "'"
            sqlstr = sqlstr + " AND WORKDATE='" + TradeContext.WORKDATE + "'"
            sqlstr = sqlstr + " AND SERIALNO='" + swapbuf[4].strip()    + "'"

            AfaLoggerFunc.tradeInfo(sqlstr)

            ChkFlag = '*'
            records = AfaDBFunc.SelectSql( sqlstr )
            if ( records==None or len(records) == 0 ):
                AfaLoggerFunc.tradeInfo('���ݿ��м�¼ƥ��ʧ��(�����޼�¼)')
                AfaLoggerFunc.tradeInfo(sqlstr)
                continue

            else:
                h_tradeamt = (long)((float)(swapbuf[32].strip())*100   + 0.1)
                m_tradeamt = (long)((float)(records[0][3].strip())*100 + 0.1)

                if ( swapbuf[9].strip() != records[0][0] ):
                    AfaLoggerFunc.tradeInfo('���ݿ��м�¼ƥ��ʧ��(�����Ų���):' + swapbuf[9].strip()  + '|' + records[0][0] + '|')
                    #PrtRecInfo(swapbuf)
                    ChkFlag = '2'

                elif ( swapbuf[10].strip() != records[0][1] ):
                    AfaLoggerFunc.tradeInfo('���ݿ��м�¼ƥ��ʧ��(��Ա�Ų���):' + swapbuf[10].strip() + '|' + records[0][1] + '|')
                    #PrtRecInfo(swapbuf)
                    ChkFlag = '3'

                elif ( h_tradeamt != m_tradeamt ):
                    AfaLoggerFunc.tradeInfo('���ݿ��м�¼ƥ��ʧ��(�������):' + str(h_tradeamt) + '|' + str(m_tradeamt) + '|')
                    #PrtRecInfo(swapbuf)
                    ChkFlag = '4'

                elif ( swapbuf[50].strip() == '1' ):
                    ChkFlag = '1'

                else:
                    ChkFlag = '0'

            #���޸������ݿ����ƥ��
            sqlstr = "UPDATE FS_MAINTRANSDTL SET CHKFLAG='" + ChkFlag + "' WHERE "
            sqlstr = sqlstr + " APPNO='"        + TradeContext.appNo    + "'"
            sqlstr = sqlstr + " AND BUSINO='"   + TradeContext.busiNo   + "'"
            sqlstr = sqlstr + " AND WORKDATE='" + TradeContext.WORKDATE + "'"
            sqlstr = sqlstr + " AND SERIALNO='" + swapbuf[4].strip()    + "'"

            #AfaLoggerFunc.tradeInfo(sqlstr)

            retcode = AfaDBFunc.UpdateSqlCmt( sqlstr )
            if (retcode==None or retcode <= 0):
                AfaLoggerFunc.tradeInfo('�޸ļ�¼����״̬,���ݿ��쳣')
                hFp.close()
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","�޸ļ�¼����״̬,���ݿ��쳣"
                return False

            totalnum = totalnum + 1
            totalamt = totalamt + m_tradeamt

        hFp.close()

        #ÿ��ֻ����һ�ζ���
        sqlstr  =   "select this,date from fs_remain where busino='" + TradeContext.busiNo + "'"
        sqlstr  =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'" + "order by date desc"

        AfaLoggerFunc.tradeInfo(sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None ):
            TradeContext.errorCode  =   "9999"
            TradeContext.errorMsg   =   "��˰�����쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        if( len(records)==0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "��˰�����쳣(û�е�λ��Ϣ)"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False


        #ȡ����������
        sqlstr = "select this from fs_remain where busino='" + TradeContext.busiNo + "' and date='" + TradeContext.wyesterdate + "'"

        sqlstr = sqlstr + " and bankno = '" + TradeContext.bankbm + "'" + " order by date desc"

        AfaLoggerFunc.tradeInfo( sqlstr )
        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None ):
            TradeContext.errorCode  =   "9999"
            TradeContext.errorMsg   =   "��˰�����쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        if( len(records)==0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "��˰�����쳣(û�ж�������ǰһ�����Ϣ)"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        TradeContext.lastRemain     =   records[0][0]       #�������
        TradeContext.banlance       =   records[0][0]       #ͳ�����仯


        #�������û�������Ϣ�����һ��
        #TradeContext.remain="44676653.13"
        sqlstr  =   "insert into fs_remain(busino,date,this,bankno) values('" + TradeContext.busiNo + "','" + TradeContext.WORKDATE + "','" + TradeContext.remain + "','" + TradeContext.bankbm + "')"
        if( AfaDBFunc.InsertSql( sqlstr ) < 1 ):
            AfaDBFunc.RollbackSql( )
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'���뱾�����ʧ��' + sqlstr
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            return False

        AfaDBFunc.CommitSql( )

        #���ɶ����ļ�,�������ױ���ȡ������
        sqlStr = "SELECT bankserno,USERNO,NOTE1,USERNAME,NOTE2,AMOUNT FROM FS_MAINTRANSDTL WHERE "
        sqlStr = sqlStr + " APPNO='"    + TradeContext.appNo    + "'"
        sqlStr = sqlStr + " AND BUSINO='"   + TradeContext.busiNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='" + TradeContext.WORKDATE + "'"
        sqlStr = sqlStr + " AND CHKFLAG='0' AND NOTE2='1' AND BANKSTATUS='0' and REVTRANF='0' order by userno"


        AfaLoggerFunc.tradeInfo( sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None ):
            AfaLoggerFunc.tradeInfo('��ѯ��Ҫ����ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ɶ��ʴ���ʧ��,���ݿ��쳣"
            return False

        normalNum   = 0           #��������
        tuifuNum    = 0           #�˸�����
        normalAmt   = 0           #�������ϼ�
        tuifuAmt    = 0           #�˸����ϼ�



##############################������������2007��10��16###########################################################
        fileName   = TradeContext.busiNo + "duizhang" +  ".txt"
        dzFileName = os.environ['AFAP_HOME'] + "/data/ahfs/" + fileName
        dzfp= open(dzFileName,  "w")

        lineWidth       =   144             #�����б�����
        WidthList       =   [10,10,20,40,32,14,14,14]
        dzfp.write('���˵�'.center(lineWidth))
        dzfp.write('\n')
        dzfp.write('\n')

        dzfp.write('     �������ƣ�'   + TradeContext.I1SBNM + '\t' )
#        dzfp.write('     �Ʊ����ڣ�' + TradeContext.workDate   + '\t\t\t\t\n' )
        dzfp.write('     �Ʊ����ڣ�' + TradeContext.WORKDATE   + '\t\t\t\t\n' )    #���Ʊ����ڸ�Ϊ�����������������
        dzfp.write('     �Թ��ʻ���' + TradeContext.busiAccno  + '\t\t\t\t' )
        dzfp.write('     ������' + TradeContext.lastRemain + '\n' )
        dzfp.write('     �������������Щ����������Щ��������������������Щ����������������������������������������Щ��������������������������������Щ��������������Щ��������������Щ���������������'+'\n')
        dzfp.write('     ��������ˮ�ũ��ɿ����ũ�    ִ�յ�λ���    ��                  �ɿ���                ������ ���� �˸� �Ͻɹ��� �Ͻ�ר����    ����      ��       �跽   ��    �ϼ�      ��'+'\n')

        banlance    =   float(TradeContext.lastRemain)          #�������
        normalNum   =   0
        tuifuNum    =   0

        AfaLoggerFunc.tradeInfo( '��ǰ��ˮ�ɷ�����' + str( len(records) ) )
        i = 0
        while ( i  < len(records) ):
            rowLine     =   '     ��'
            lineList    =   list(records[i])

            if lineList[4]  ==  '1':                            #��������
                lineList[4] =   '��������'
                lineList.append('')
                banlance    =   banlance + float(lineList[5])
                lineList.append( str(banlance) )
                normalNum   =   normalNum + 1

            elif lineList[4]  ==  '2' :                         #�˸�����
                lineList[4]     =   '�˸�����'
                lineList.insert(len(lineList)-1,'')

                banlance        =   banlance - float(lineList[6])
                lineList.append( str(banlance) )
                tuifuNum        =   tuifuNum + 1
            else:
                AfaLoggerFunc.tradeInfo('�ʽ����ʴ���')
                return False

            dzfp.write('     �������������੤���������੤�������������������੤���������������������������������������੤�������������������������������੤�������������੤�������������੤��������������'+'\n')

            dzfp.write('     ��')
            for j in range( len(WidthList) ):
                if j == 4:
                    dzfp.write( lineList[j].center(WidthList[j]) )
                else:
                    dzfp.write( lineList[j].ljust(WidthList[j]) )
                dzfp.write('��')
            else:
                dzfp.write('\n')

            i=i+1
################################################################################################################

        #ͳ�ƴ�������  ��ˮ�š��ɿ����š������ˡ��շѽ��
        #sqlstr  =   "select afc401,afc001,afc006,afc011 from fs_fc74 where date='" + TradeContext.WORKDATE + "'and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag != '*'"
        dateTmp     =   TradeContext.WORKDATE[0:4] + '-' + TradeContext.WORKDATE[4:6] + '-' + TradeContext.WORKDATE[6:8]
        sqlstr  =   "select afc401,afc001,afc006,afc011 from fs_fc74 where afc015='" + dateTmp + "'and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag != '*' and afa101 = '" + TradeContext.bankbm + "'"
        AfaLoggerFunc.tradeInfo( sqlstr )
        records =   AfaDBFunc.SelectSql( sqlstr )
        if (records==None) :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","��ȡ��������ʧ��,���ݿ��쳣"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
            return False

        i           =   0
        AfaLoggerFunc.tradeInfo( '��ǰ������Ŀ��' + str( len(records) ) )
        daichaNum   =   0           #�������
        while ( i < len(records) ):
            lineList    =   list(records[i])
            lineList[1] =   ''

            lineList.insert(2,'')           #ִ�յ�λ����
            lineList.insert(4,'����')       #�ʽ�����

            banlance    =   banlance + float(lineList[len(lineList)-1])
            lineList.append('')           #����
            lineList.append( str(banlance) )
            daichaNum   =   daichaNum + 1

            dzfp.write('     �������������੤���������੤�������������������੤���������������������������������������੤�������������������������������੤�������������੤�������������੤��������������'+'\n')

            dzfp.write('     ��')
            for j in range( len(WidthList) ):

                if j == 4:
                    dzfp.write( lineList[j].center(WidthList[j]) )
                else:
                    dzfp.write( lineList[j].ljust(WidthList[j]) )
                dzfp.write('��')
            else:
                dzfp.write('\n')

            i=i+1


        #---------------------ͳ���˸�--------------
        sqlStr = "SELECT bankserno,USERNO,NOTE1,USERNAME,NOTE2,AMOUNT FROM FS_MAINTRANSDTL WHERE "
        sqlStr = sqlStr + " APPNO='"    + TradeContext.appNo    + "'"
        sqlStr = sqlStr + " AND BUSINO='"   + TradeContext.busiNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='" + TradeContext.WORKDATE + "'"
        sqlStr = sqlStr + " AND CHKFLAG='0' AND NOTE2='2' AND BANKSTATUS='0' and REVTRANF='0' order by userno"

        AfaLoggerFunc.tradeInfo( sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        if (records==None ):
            AfaLoggerFunc.tradeInfo('��ѯ��Ҫ����ʧ��,���ݿ��쳣')
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ɶ��ʴ���ʧ��,���ݿ��쳣"
            return False

        i = 0
        while ( i  < len(records) ):
            rowLine     =   '     ��'
            lineList    =   list(records[i])

            if lineList[4]  ==  '1':                            #��������
                lineList[4] =   '��������'
                lineList.append('')
                banlance    =   banlance + float(lineList[5])
                lineList.append( str(banlance) )
                normalNum   =   normalNum + 1

            elif lineList[4]  ==  '2' :                         #�˸�����
                lineList[4]     =   '�˸�����'
                lineList.insert(len(lineList)-1,'')             #�ʽ����ʴ���Ϊ��

                banlance        =   banlance - float(lineList[6])
                lineList.append( str(banlance) )
                tuifuNum        =   tuifuNum + 1
            else:
                AfaLoggerFunc.tradeInfo('�ʽ����ʴ���')
                return False

            dzfp.write('     �������������੤���������੤�������������������੤���������������������������������������੤�������������������������������੤�������������੤�������������੤��������������'+'\n')

            dzfp.write('     ��')
            for j in range( len(WidthList) ):
                if j == 4:
                    dzfp.write( lineList[j].center(WidthList[j]) )
                else:
                    dzfp.write( lineList[j].ljust(WidthList[j]) )
                dzfp.write('��')
            else:
                dzfp.write('\n')

            i=i+1
        else:
            dzfp.write('     �������������ة����������ة��������������������ة����������������������������������������ة��������������������������������ة��������������ة��������������ة���������������'+'\n' )


        normalAmt   =   0
        tuifuAmt    =   0
        daichaAmt   =   0

        sqlStr = "SELECT sum(double(AMOUNT)) FROM FS_MAINTRANSDTL WHERE "
        sqlStr = sqlStr + " APPNO='"    + TradeContext.appNo    + "'"
        sqlStr = sqlStr + " AND BUSINO='"   + TradeContext.busiNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='" + TradeContext.WORKDATE + "'"
        sqlStr = sqlStr + " AND CHKFLAG='0' AND NOTE2='1' AND BANKSTATUS='0' and REVTRANF='0'"
        AfaLoggerFunc.tradeInfo( sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        normalAmt = records[0][0]
        if (normalAmt==None) :
            normalAmt = 0


        sqlStr = "SELECT sum(double(AMOUNT)) FROM FS_MAINTRANSDTL WHERE "
        sqlStr = sqlStr + " APPNO='"    + TradeContext.appNo    + "'"
        sqlStr = sqlStr + " AND BUSINO='"   + TradeContext.busiNo   + "'"
        sqlStr = sqlStr + " AND WORKDATE='" + TradeContext.WORKDATE + "'"
        sqlStr = sqlStr + " AND CHKFLAG='0' AND NOTE2='2' AND BANKSTATUS='0' and REVTRANF='0'"
        AfaLoggerFunc.tradeInfo( sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        tuifuAmt = records[0][0]
        if (tuifuAmt==None) :
            tuifuAmt = 0

        dateTmp     =   TradeContext.WORKDATE[0:4] + '-' + TradeContext.WORKDATE[4:6] + '-' + TradeContext.WORKDATE[6:8]
        sqlstr  =   "select sum(double(AFC011)) from fs_fc74 where AFC015='" + dateTmp + "'and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag != '*'"
        AfaLoggerFunc.tradeInfo( sqlstr )
        records = AfaDBFunc.SelectSql( sqlstr )
        daichaAmt = records[0][0]
        if (daichaAmt==None) :
            daichaAmt = 0

        sLastLine   =   "     �ܱ�����" + str(daichaNum+normalNum+tuifuNum)+ "\t\t����������" + str(normalNum) + "\t\t���������" + str(daichaNum) + "\t\t�˸�������" + str(tuifuNum) + "\t\t�Ʊ��ˣ�"
        dzfp.write(sLastLine + "\n")
        sLastLine   =   "     ��������ϼƣ�" + str(normalAmt)+ "\t\t�˸��ϼƣ�" + str(tuifuAmt) + "\t\t����ϼƣ�" + str(daichaAmt)
        dzfp.write(sLastLine + "\n")
        dzfp.write("     ������"+ TradeContext.remain )
        dzfp.close()

        #�ļ�����
        TradeContext.DZFILESIZE = str(os.path.getsize(dzFileName))

        #�����ļ���
        TradeContext.DZFILENAME = fileName


    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        AfaLoggerFunc.tradeInfo('���ʴ����쳣')
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ʴ����쳣"
        dzfp.close()
        return False

#fieldWidthList  =   [14,24,24,40,60,16,16,16]           #�����б�
#fieldHeadList   =   ["������ˮ��","�ɿ����","ִ�յ�λ����","�ɿ���","�ʽ����ʣ��������������롢�˸����Ͻɹ��⡢�Ͻ�ר����","����","�跽","�ϼ�"]
#width           =   14+24+24+40+60+16+16+16+9



###########################################������###########################################
def SubModuleMainFst():

    AfaLoggerFunc.tradeInfo('**********���շ�˰���ʿ�ʼ*********')
#    TradeContext.WORKDATE = AfaUtilTools.GetSysDate( )
    TradeContext.WORKTIME = AfaUtilTools.GetSysTime( )

    #�ź��޸ļ������б�������
    sqlstr = "select this from fs_8446_remain where busino='" + TradeContext.busiNo + "' and date='" + TradeContext.WORKDATE + "' and bankno = '"+TradeContext.bankbm+"' order by date desc"

    AfaLoggerFunc.tradeInfo('ȡǰһ�����')
    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "9999"
        TradeContext.errorMsg   =   "��˰�����쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

    if( len(records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "��˰�����쳣(û�ж���������Ϣ)"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

    TradeContext.remain     =   records[0][0]       #�������

    TradeContext.errorCode,TradeContext.errorMsg    =   "0000","���ʳɹ�"

    #=====�õ����˵�ǰһ������� add by pgt 20090401====
    wyear  = int(TradeContext.WORKDATE[:4])
    wmonth = int(TradeContext.WORKDATE[4:6])
    wday   = int(TradeContext.WORKDATE[6:])
    wdate       = datetime.date(wyear,wmonth,wday)     #���˵�����
    TradeContext.wyesterdate = wdate - datetime.timedelta(days=1)
    TradeContext.wyesterdate = TradeContext.wyesterdate.strftime("%Y%m%d")

    AfaLoggerFunc.tradeInfo('wyesterdate<<<<<<'+TradeContext.wyesterdate)
    AfaLoggerFunc.tradeInfo('workDate<<<<<<'+TradeContext.workDate)

    #ÿ��ֻ����һ�ζ���
    sqlstr  =   "select this from fs_remain where busino='" + TradeContext.busiNo + "' and date='" + TradeContext.WORKDATE + "'"

    #begin 20100701 ����������
    sqlstr  =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"
    #end

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None  ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "��˰�����쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

    #�������û�ж��ˣ���ȡ�����������
    if ( len( records)>0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "ÿ��ֻ����һ�ζ���"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

    #��ѯ�Թ����˻�
    sqlstr          =   "select accno from ABDT_UNITINFO where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len(records) == 0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���ҵ��Թ��˻��쳣"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    TradeContext.busiAccno      =   records[0][0]

    #��ȡλ���ļ�
    GetLappConfig()

    #=====����Էǵ�����ˣ��򲻽���ǩ�˴���====
    AfaLoggerFunc.tradeInfo('WORKDATE=='+str(TradeContext.WORKDATE))
    if(TradeContext.WORKDATE == TradeContext.workDate):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "���ܶԵ����ʣ�����ն���"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False
        #AfaLoggerFunc.tradeInfo('>>>ǩ��')
        #Ahdx_Logout()

    AfaLoggerFunc.tradeInfo('>>>���մ���')
    Ahdx_DayEnd()     #���������ļ����Ҹ�ʽ���ļ�

    AfaLoggerFunc.tradeInfo('>>>���ʴ���')
    Ahdx_DzSend()

    #AfaLoggerFunc.tradeInfo('>>>ǩ��')
    #Ahdx_Login()

    AfaLoggerFunc.tradeInfo('**********���շ�˰���ʽ���**********')
    return True

