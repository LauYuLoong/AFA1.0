# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AbdtManager.py
# �ļ���ʶ��
# ժ    Ҫ������������
#
# ��ǰ�汾��2.0
# ��    �ߣ�XZH
# ������ڣ�2008��06��10��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext,UtilTools,AfaFunc,AfaDBFunc,ConfigParser,sys,os,time,LoggerHandler,HostComm,HostContext
from types import *

abdtLogger = LoggerHandler.getLogger( 'abdt' )

#=========================��־==================================================
def WrtLog(logstr):

    if ( TradeContext.existVariable('BATCH_TRACE') ):

        if ( TradeContext.BATCH_TRACE   == 'off' ):
            #�������־
            return True

        elif ( TradeContext.BATCH_TRACE == 'file' ):
            #���ļ����
            abdtLogger.info(logstr)

        elif ( TradeContext.BATCH_TRACE == 'all' ):
            #���ļ�����Ļͬʱ���
            abdtLogger.info(logstr)
            print logstr

        elif ( TradeContext.BATCH_TRACE == 'stdout' ):
            #����Ļ���
            print logstr

    else:
        #Ĭ�����ļ�����Ļͬʱ���
        abdtLogger.info(logstr)
        print logstr

    return True


#=========================�����쳣ʱ�˳�����������==============================
def ExitThisFlow( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode= errorCode
        TradeContext.errorMsg = errorMsg

        WrtLog( '>>>[' + errorCode + ']' + errorMsg )

    if( TradeContext.errorCode.isdigit( )==True and long( TradeContext.errorCode )==0 ):
        return True

    else:
        return False




#=========================��ȡ���������ļ�����Ϣ=================================
def GetBatchConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.BATCH_HOSTIP   = config.get('BATCH', 'HOSTIP')
        TradeContext.BATCH_USERNO   = config.get('BATCH', 'USERNO')
        TradeContext.BATCH_PASSWD   = config.get('BATCH', 'PASSWD')
        TradeContext.BATCH_LDIR     = config.get('BATCH', 'LDIR')
        TradeContext.BATCH_RDIR     = config.get('BATCH', 'RDIR')
        TradeContext.BATCH_CLEARDAY = config.get('BATCH', 'CLEARDAY')
        TradeContext.BATCH_CYCTIME  = config.get('BATCH', 'CYCTIME')
        TradeContext.BATCH_TRACE    = config.get('BATCH', 'TRACE')
        TradeContext.BATCH_MAXNUM   = config.get('BATCH', 'MAXNUM')

        WrtLog(':::BATCH_HOSTIP   = ' + TradeContext.BATCH_HOSTIP)
        WrtLog(':::BATCH_USERNO   = ' + TradeContext.BATCH_USERNO)
        WrtLog(':::BATCH_PASSWD   = ' + TradeContext.BATCH_PASSWD)
        WrtLog(':::BATCH_LDIR     = ' + TradeContext.BATCH_LDIR)
        WrtLog(':::BATCH_RDIR     = ' + TradeContext.BATCH_RDIR)
        WrtLog(':::BATCH_CLEARDAY = ' + TradeContext.BATCH_CLEARDAY)
        WrtLog(':::BATCH_CYCTIME  = ' + TradeContext.BATCH_CYCTIME)
        WrtLog(':::BATCH_TRACE    = ' + TradeContext.BATCH_TRACE)
        WrtLog(':::BATCH_MAXNUM   = ' + TradeContext.BATCH_MAXNUM)

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9000', '��ȡ���������ļ��쳣')



#=========================��ѯ��λ��Ϣ==========================================
def QueryBusiInfo():

    try:
        sql = "SELECT APPNAME,BUSINAME,ACCNO,AGENTTYPE,VOUHNO FROM ABDT_UNITINFO WHERE "
        sql = sql +       "APPNO="    + "'" + TradeContext.APPNO  + "'"        #ҵ����
        sql = sql + " AND BUSINO="    + "'" + TradeContext.BUSINO + "'"        #��λ���
        sql = sql + " AND STATUS="    + "'" + "1"                 + "'"        #״̬(0:ע��,1:����)

        WrtLog(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '��ѯ��λ��Ϣ�쳣')

        if ( len(records) == 0 ):
            return ExitThisFlow( '9000', 'û�в�ѯ��λ��Ϣ')


        TradeContext.APPNAME   = str(records[0][0]).strip()        #ҵ������
        TradeContext.BUSINAME  = str(records[0][1]).strip()        #��λ����
        TradeContext.ACCNO     = str(records[0][2]).strip()        #�����˻�(��λ�ʻ�)
        TradeContext.AGENTTYPE = str(records[0][3]).strip()        #ί�з�ʽ
        TradeContext.VOUHNO    = str(records[0][4]).strip()        #ƾ֤��(�ڲ��ʻ�)

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '��ѯ��λ��Ϣ�쳣')



#=========================�޸������ύ���ڻ��������============================
def UpdateBatchDate(pBatchNo, pDate, pTime):

    WrtLog('>>>�޸������ύʱ��=' + TradeContext.WorkDate + ' ' + TradeContext.WorkTime)

    try:

        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET "
        sql = sql + "BATCHDATE=" +  "'" + TradeContext.WorkDate    + "',"        #����
        sql = sql + "BATCHTIME=" +  "'" + TradeContext.WorkTime    + "'"         #ʱ��

        sql = sql + " WHERE "

        sql = sql + "BATCHNO=" + "'" + pBatchNo    + "'"                         #ί�к�

        WrtLog(sql)

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if (result <= 0):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '�޸������ύ���ڻ��������ʧ��')

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '�޸������ύ���ڻ���������쳣')


#=========================�������ļ��Ƶ�Ŀ¼DUST��==============================
def MoveFileToDust():

    WrtLog('>>>�������ļ��Ƶ�Ŀ¼DUST��')

    try:
        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        sFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/dust/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + TradeContext.WorkTime + '_' + 'X'
        #end

        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            cmdstr = "mv " + sFileName + " " + dFileName
            WrtLog('>>>ת������:' + cmdstr)
            os.system(cmdstr)
            return True
            
        else:
            return ExitThisFlow( '9000', '�������������ļ�������,���ѯԭ��')

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '�����ļ��Ƶ�Ŀ¼DUST�쳣')



#=========================�޸����ε�״̬========================================
def UpdateBatchInfo(pBatchNo, pStatus, pMessage,pInfo=0):

    WrtLog('>>>�޸�����״̬:[' + pStatus + ']' + pMessage)

    try:
        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET "
        sql = sql + "STATUS="   +  "'" + pStatus     + "',"     #״̬
        sql = sql + "PROCMSG="  +  "'" + pMessage    + "',"     #ԭ��
        
        #begin
        #�ر��  20090330  ������ϸ������Ϣ�ļ���(NOTE4)
        if pInfo:
            sql = sql + "NOTE4=" + "'abdt_procmsg" + pBatchNo + ".txt'"  #��ϸ������Ϣ�ļ���
        else:
            sql = sql + "NOTE4=''"                                       #��ϸ������Ϣ�ļ���
        #end

        sql = sql + " WHERE "

        sql = sql + "BATCHNO=" + "'" + pBatchNo    + "'"        #ί�к�

        WrtLog(sql)

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if ( result <= 0 ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '�޸����ε�״̬ʧ��')

        #begin
        #�ر��  20090330  ������ڲ���pInfo(��ϸ������Ϣ),����ϸ��Ϣд�뵽��ϸ��Ϣ�ļ���
        if pInfo:
            path_procmsg = os.environ['AFAP_HOME'] + '/data/batch/procmsg/abdt_procmsg' + pBatchNo + '.txt'
            
            fp_procmsg = open(path_procmsg,"a")
            
            fp_procmsg.write(pInfo + "\n")
            
            fp_procmsg.close()
        #end

        #�������Ϊ�ѳ���״̬,��������ļ��Ƶ�Ŀ¼DUST��
        if ( pStatus == '40' ):
            MoveFileToDust()

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '�޸����ε�״̬�쳣')




#==�޸������ύ״̬,��ʼ�ύ������NOTE1Ϊ1,������������쳣�˳���NOTE1Ϊ0=======
def UpdateBatchInfoTJ(pBatchNo, pStatus):

    WrtLog('>>>�޸��ύ״̬:'+pBatchNo+'[' + pStatus + ']' )

    try:
        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET"
        sql = sql + " NOTE1=" +  "'" + pStatus    + "'"         #�ύ״̬
        sql = sql + " WHERE "

        sql = sql + "BATCHNO=" + "'" + pBatchNo    + "'"        #ί�к�

        WrtLog(sql)

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if ( result <= 0 ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '�޸������ύ״̬ʧ��')

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '�޸������ύ״̬�쳣')



#=========================У��ͻ���Ϣ��========================================
def ChkCustInfo(pAppNo, pBusiNo, pAccNo):

    WrtLog('>>>У��ͻ���Ϣ:'+ pAppNo+'|'+pBusiNo+'|'+pAccNo)

    try:
        sql = ""
        sql = "SELECT * FROM ABDT_CUSTINFO WHERE"
        sql = sql + " APPNO='"          + pAppNo  + "'"
        sql = sql + " AND BUSINO='"     + pBusiNo + "'"
        sql = sql + " AND ACCNO='"      + pAccNo  + "'"
        sql = sql + " AND STARTDATE<='" + TradeContext.WorkDate + "'"
        sql = sql + " AND ENDDATE>='"   + TradeContext.WorkDate + "'"

        WrtLog(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', 'У��ͻ���Ϣʧ��')

        if ( len(records) == 0 ):
            return ExitThisFlow( '9000', 'û�пͻ���Ϣ')
       
        #20110620  ����̩�޸� ȡ��ȫ��򲿷ֿۿ��ʶ
        TradeContext.PartFlag = records[0][11]
        #end
        
        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '��ѯ�ͻ���Ϣ�쳣')



#=========================����AS400������ʽ�ļ�=================================
def CrtBatchFile(curBatchNo):

    WrtLog('>>>����AS400������ʽ�ļ�')

    summary_code = '258'
    
    #begin 20100107 ���������� ժҪ����
    summary_name = ' '
    #end

    ret = 0
    try:
        #У����Ч��
        if ( TradeContext.WorkDate > TradeContext.ENDDATE ):
            UpdateBatchInfo(curBatchNo, "40", "�Զ�����,���ι���")
            return ExitThisFlow( "9000", "�Զ�����,���ι���" )


        #��ѯժҪ����
        sqlstr = "SELECT SUMNO,SUMNAME FROM AFA_SUMMARY WHERE SYSID='" + TradeContext.APPNO + "'"
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records == None or len(records) == 0 ):
            WrtLog('>>>û�з���ժҪ����')
            summary_code = '258'
        else:
            summary_code = records[0][0].strip()
            
            #begin 20100107 ���������� ժҪ����
            summary_name = records[0][1].strip()
            #end


        #�ж��ļ��Ƿ����
        m_totalnum = 0
        m_totalamt = 0
        iCount     = 0

        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        bFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        sFileName = os.environ['AFAP_HOME'] + '/data/batch/swap/SWAP_' + TradeContext.BUSINO + TradeContext.NOTE2 + '.TXT'
        #end

        #begin
        #�ر��  20090330  ɾ����ϸ������Ϣ�ļ�
        DelProcmsgFile(curBatchNo)
        
        #�ر��  20090330  ��ʼ����ϸ�����ʶ��  procFlag(0-����,1-�쳣)
        procFlag = 0
        #end

        if ( os.path.exists(bFileName) ):
            #���ļ�
            bfp = open(bFileName, "r")

            #���������ļ�
            sfp= open(sFileName,  "w")

            #��ȡһ��
            linebuf = bfp.readline()
            iline=0
            while ( len(linebuf) > 0 ):
                iline=iline+1
                
                #�������⴦��(�޸��ˣ����Һͣ��޸����ڣ�20080402)
                if ( (len(linebuf) != 100) and (len(linebuf) != 101) and  (len(linebuf) != 118) and (len(linebuf) != 119)):
                    
                    #begin  �ر��  20090330 
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݸ�ʽ��:��" + str(iline) + "��")
                    #return ExitThisFlow( "9000", "�Զ�����,�������ݸ�ʽ��:��" + str(iline)+  "��")
                    
                    UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݸ�ʽ��:��" + str(iline) + "��")
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end

                #������Ϣ
                if ( linebuf[0] == "1" ):
                    s_rectype    = linebuf[0:1].lstrip().rstrip()          #��¼����
                    s_appno      = linebuf[1:7].lstrip().rstrip()          #ҵ����
                    s_busino     = linebuf[7:21].lstrip().rstrip()         #��λ���
                    s_agenttype  = linebuf[21:22].lstrip().rstrip()        #ί�з�ʽ
                    s_accno      = linebuf[22:45].lstrip().rstrip()        #�Թ��ʺ�
                    s_remark     = linebuf[45:65].lstrip().rstrip()        #����
                    s_status     = linebuf[65:66].lstrip().rstrip()        #״̬
                    s_totalnum   = linebuf[66:76].lstrip().rstrip()        #�ܱ���
                    s_totalamt   = linebuf[76:93].lstrip().rstrip()        #�ܽ��
                    s_retcode    = linebuf[93:100].lstrip().rstrip()       #������

                    #У�����ݺϷ���
                    if ( not (s_agenttype.isdigit() and (len(s_accno)==0 or len(s_accno)==19 or len(s_accno)==23) and s_status.isdigit() and s_totalnum.isdigit()) ):
                        
                        #begin  �ر��  20090330 
                        
                        #bfp.close()
                        #sfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(����):��" + str(iline) + "��")
                        #return ExitThisFlow( "9000", "�Զ�����,�������ݷǷ�(����):��" + str(iline) + "��")
                        
                        UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(����):��" + str(iline) + "��")
                        procFlag = 1
                        linebuf = bfp.readline()
                        continue
                        #end

                #��ϸ��Ϣ
                elif ( linebuf[0] == '2' ):
                    m_rectype    = linebuf[0:1].lstrip().rstrip()               #��¼����
                    
                    #20120409 �º��޸����--AG07
                    #if ( TradeContext.APPNO[0:4] == 'AG08' ):
                    if ( TradeContext.APPNO[0:4] == 'AG08' or TradeContext.APPNO[0:4] == 'AG07'):
                        #�������⴦��(�޸��ˣ����Һͣ��޸����ڣ�20080402),����ʽΪ����6λ�ʽ����ӿͻ���ʶ�в���
                        m_custid     = linebuf[1:26].lstrip().rstrip()          #�ͻ���ʶ(��������(15λ)+���(4λ)+��Ŀ����(3λ)+�������α���(3λ)+�ʽ����(6λ)
                        m_agenttype  = linebuf[39:40].lstrip().rstrip()         #ί�з�ʽ
                        m_accno      = linebuf[40:63].lstrip().rstrip()         #�����ʺ�
                        m_remark     = linebuf[63:83].lstrip().rstrip()         #����
                        m_status     = linebuf[83:84].lstrip().rstrip()         #״̬
                        m_tradenum   = linebuf[84:94].lstrip().rstrip()         #����
                        m_tradeamt   = linebuf[94:111].lstrip().rstrip()        #���
                        m_retcode    = linebuf[111:118].lstrip().rstrip()       #������
                    else:
                        m_custid     = linebuf[1:21].lstrip().rstrip()          #�ͻ���ʶ
                        m_agenttype  = linebuf[21:22].lstrip().rstrip()         #ί�з�ʽ
                        m_accno      = linebuf[22:45].lstrip().rstrip()         #�����ʺ�
                        m_remark     = linebuf[45:65].lstrip().rstrip()         #����
                        m_status     = linebuf[65:66].lstrip().rstrip()         #״̬
                        m_tradenum   = linebuf[66:76].lstrip().rstrip()         #����
                        m_tradeamt   = linebuf[76:93].lstrip().rstrip()         #���
                        m_retcode    = linebuf[93:100].lstrip().rstrip()        #������

                    #У�����ݺϷ���
                    if ( not (m_agenttype.isdigit() and m_accno.isdigit() and m_status.isdigit() and m_tradenum.isdigit()) ):
                        
                        #begin  �ر��  20090330 
                        
                        #bfp.close()
                        #sfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(��ϸ��):��" + str(iline) + "��")
                        #return ExitThisFlow( "9000", "�Զ�����,�������ݷǷ�(��ϸ��):��" + str(iline) + "��")
                        
                        UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(��ϸ��):��" + str(iline) + "��")
                        procFlag = 1
                        linebuf = bfp.readline()
                        continue
                        #end

                    #ɸѡ״̬Ϊ�����ļ�¼
                    if ( m_status == '1' ):

                        #ͳ�ƽ��ͱ���
                        m_totalnum = m_totalnum + 1
                        m_totalamt = m_totalamt + (long)((float)(m_tradeamt)*100 + 0.1)

                        if ( s_agenttype == '3' ):

                            #У��ͻ���Ϣ�ǺϷ�
                            if not ChkCustInfo(TradeContext.APPNO, TradeContext.BUSINO, m_accno):
                                
                                #begin  �ر��  20090330 
                                
                                #bfp.close()
                                #sfp.close()
                                #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(�ͻ�δǩԼ):��" + str(iline) + "��")
                                #return ExitThisFlow( "9000", "�Զ�����,�������ݷǷ�(�ͻ�δǩԼ):��" + str(iline) + "��")
                                
                                UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(�ͻ�δǩԼ):��" + str(iline) + "��")
                                procFlag = 1
                                linebuf = bfp.readline()
                                continue
                                #end

                        #��¼�ļ�
                        onelinebuf = ''
                        onelinebuf = onelinebuf + TradeContext.APPNO            + "|"        #����ҵ��� 
                        onelinebuf = onelinebuf + TradeContext.WorkDate         + "|"        #����ί������
                        onelinebuf = onelinebuf + TradeContext.BATCHNO[4:16]    + "|"        #����ί�к�
                        onelinebuf = onelinebuf + TradeContext.WorkDate         + "|"        #ǰ������
                        onelinebuf = onelinebuf + "000000000000"                + "|"        #ǰ����ˮ��
                        onelinebuf = onelinebuf + TradeContext.WorkDate         + "|"        #��ϵͳ��������
                        onelinebuf = onelinebuf + TradeContext.WorkDate         + "|"        #��������             
                        onelinebuf = onelinebuf + "000000000000"                + "|"        #������ˮ��
                        onelinebuf = onelinebuf + " "                           + "|"        #�����ֱ�־(0-����,1-����)
                        onelinebuf = onelinebuf + TradeContext.BRNO             + "|"        #���׻���
                        
                        #begin 20100107 �������޸� 999990Ϊ�����������ύ�Ĺ�Ա��
                        if(TradeContext.USERNO == '999990'):
                            onelinebuf = onelinebuf + TradeContext.USERNO       + "|"         #���׹�Ա��
                        else:
                            onelinebuf = onelinebuf + '999986'                      + "|"     #���׹�Ա
                        #end
                        
                        
                        iCount = iCount+1
                        onelinebuf = onelinebuf + str(iCount)                   + "|"        #���
                        onelinebuf = onelinebuf + "1 "                          + "|"        #�������

                        if ( s_agenttype == '3' ):
                            #����(��˽)
                            onelinebuf = onelinebuf + m_accno                   + "|"        #�跽�˺�
                            onelinebuf = onelinebuf + m_remark                  + "|"        #�跽�˻�����
                        else:
                            #����(�Թ�)
                            onelinebuf = onelinebuf + TradeContext.VOUHNO       + "|"        #�跽�˺�
                            onelinebuf = onelinebuf + s_remark                  + "|"        #�跽�˻�����

                        onelinebuf = onelinebuf + " "                           + "|"        #�������
                        onelinebuf = onelinebuf + "N"                           + "|"        #����У�鷽ʽ('N' ��ʾ��У�� ����ֵ����ʾ��ҪУ��)
                        onelinebuf = onelinebuf + " "                           + "|"        #����
                        onelinebuf = onelinebuf + " "                           + "|"        #֧������
                       
                        #20110620 ����̩�޸� ֤��������ȫ��򲿷ֿۿ��ʶ
                        if ( s_agenttype == '3' ):
                            onelinebuf = onelinebuf + TradeContext.PartFlag         + "|"        #֤������
                        else:
                            onelinebuf = onelinebuf + " "                           + "|"         #֤������  
                        #end
                        
                        onelinebuf = onelinebuf + " "                           + "|"        #֤������
                        onelinebuf = onelinebuf + "0"                           + "|"        #֤��У���־(0-��У��,1-У��)
                        onelinebuf = onelinebuf + ""                            + "|"        #ƾ֤����
                        onelinebuf = onelinebuf + " "                           + "|"        #ƾ֤��
                        onelinebuf = onelinebuf + "0"                           + "|"        #����֧Ʊ��־
                        onelinebuf = onelinebuf + "1"                           + "|"        #ƾ֤�����־

                        if ( s_agenttype == '3' ):
                            #����(�Թ�)
                            onelinebuf = onelinebuf + TradeContext.VOUHNO       + "|"        #�����˺�
                            onelinebuf = onelinebuf + s_remark                  + "|"        #�����˻�����
                        else:
                            #����(��˽)
                            onelinebuf = onelinebuf + m_accno                   + "|"        #�����˺�
                            onelinebuf = onelinebuf + m_remark                  + "|"        #�����˻�����

                        onelinebuf = onelinebuf + "01"                          + "|"        #����
                        onelinebuf = onelinebuf + "0"                           + "|"        #�����־
                        onelinebuf = onelinebuf + "1"                           + "|"        #��ת��־(0-�ֽ�,1-ת��)
                        onelinebuf = onelinebuf + " "                           + "|"        #�����ʱ�־(0-����,1-����)
                        onelinebuf = onelinebuf + m_tradeamt.rjust(15,'0')      + "|"        #������
                        onelinebuf = onelinebuf + summary_code                  + "|"        #ժҪ����
                        
                        #begin 20100107 ������ �޸�ժҪ˵��
                        #onelinebuf = onelinebuf + " "                           + "|"        #ժҪ˵��
                        onelinebuf = onelinebuf + summary_name                  + "|"        #ժҪ˵��
                        #end
                        
                        onelinebuf = onelinebuf + "0"                           + "|"        #����Ч���־
                        onelinebuf = onelinebuf + " "                           + "|"        #������
                        onelinebuf = onelinebuf + " "                           + "|"        #�ŵ�2��Ϣ
                        onelinebuf = onelinebuf + " "                           + "|"        #�ŵ�3��Ϣ
                        onelinebuf = onelinebuf + TradeContext.BUSINO           + "|"        #������Ϣ1(������ʶ)
                        onelinebuf = onelinebuf + s_accno                       + "|"        #������Ϣ2
                        onelinebuf = onelinebuf + m_custid                      + "|"        #�����˺�(�ͻ���ʶ)

                        sfp.write(onelinebuf + '\n')
                else:
                    
                    #begin  �ر��  20090330 
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݸ�ʽ��(������):��" + str(iline) + "��")
                    #return ExitThisFlow( "9000", "�Զ�����,�������ݸ�ʽ��(������):��" + str(iline) + "��")
                    
                    UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݸ�ʽ��(������):��" + str(iline) + "��")
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end

                #���ļ��ж�ȡһ��
                linebuf = bfp.readline()

            #�ر��ļ�
            bfp.close()
            sfp.close()
            
            #begin  �ر��  20090330 
            if (procFlag == 1):
                return ExitThisFlow( "9000", "�Զ�����,ԭ����д����ϸ�����ļ�")
            #end

            #�ж��ܱ���,�ܽ��
            ls_totalnum = (long)(s_totalnum)
            lm_totalnum = (long)(m_totalnum)

            ls_totalamt = (long)(((float)(s_totalamt)) * 100 + 0.1)
            lm_totalamt = m_totalamt

            WrtLog('>>>�������=%d ������=%d ��ϸ����=%d ��ϸ���=%d' % (ls_totalnum, ls_totalamt, lm_totalnum, lm_totalamt))

            if ( (ls_totalnum!=lm_totalnum) or (ls_totalamt!=lm_totalamt) ):
                UpdateBatchInfo(curBatchNo, "40", "�Զ�����:�����ļ��ܱ������ܽ��������Ĳ���")
                return ExitThisFlow( "9000", "�Զ�����,�����ļ��ܱ������ܽ��������Ĳ���")

            #�ϴ������ļ�(����)
            hFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_1'

            mv_cmdstr="mv " + sFileName + " " + hFileName
            os.system(mv_cmdstr)

            return True

        else:
            UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������������ļ�������")
            return ExitThisFlow( "9000", "�Զ�����,�������������ļ�������")


    except Exception, e:
        bfp.close()
        sfp.close()
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '����AS400������ʽ�ļ��쳣')


#=========================FTP������===========================================
def ftpfile(ftptype, sfilename, rfilename):

    try:
        #�����ļ�
        
        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        ftpShell = os.environ['AFAP_HOME'] + '/data/batch/shell/ftphost_' + TradeContext.BUSINO + TradeContext.NOTE2 + '.sh'
        #end
        
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.BATCH_HOSTIP + '\n')
        WrtLog('>>>>ip=' + TradeContext.BATCH_HOSTIP)
        ftpFp.write('user ' + TradeContext.BATCH_USERNO + ' ' + TradeContext.BATCH_PASSWD + '\n')

        if (ftptype==0):
            #�ϴ��ļ�
            ftpFp.write('cd '  + TradeContext.BATCH_RDIR + '\n')
            ftpFp.write('lcd ' + TradeContext.BATCH_LDIR + '\n')
            ftpFp.write('bin ' + '\n')
            ftpFp.write('put ' + sfilename + ' AGENT.' + rfilename + '\n')
        else:
            #�����ļ�
            ftpFp.write('cd '  + TradeContext.BATCH_RDIR + '\n')
            ftpFp.write('lcd ' + TradeContext.BATCH_LDIR + '\n')
            ftpFp.write('bin ' + '\n')
            ftpFp.write('get ' +  rfilename + ' ' + sfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        os.system(ftpcmd)

        return True

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>FTP�����쳣')
        return False


#=========================���ͼ���֪ͨ==========================================
def SendToHost(curBatchNo):

    WrtLog('>>>���ͼ���֪ͨ(SendToHost)')

    try:
        HostFileName = 'A' + curBatchNo[8:16] + '1'

        #ͨѶ�����
        HostContext.I1TRCD = '8814'                        #����������
        HostContext.I1SBNO = TradeContext.BRNO             #�ý��׵ķ������
        HostContext.I1USID = '999986'                      #���׹�Ա��
        HostContext.I1AUUS = ""                            #��Ȩ��Ա
        HostContext.I1AUPS = ""                            #��Ȩ��Ա����
        HostContext.I1WSNO = "AFAP_BATCH"                  #�ն˺�
        HostContext.I1CLDT = TradeContext.WorkDate         #����ί������
        HostContext.I1UNSQ = TradeContext.BATCHNO[4:16]    #����ί�к�
        HostContext.I1NBBH = TradeContext.APPNO            #����ҵ���
        
        #begin 20100107 ���������� 999990Ϊ�����������ύ�Ĺ�Ա��
        if(TradeContext.USERNO == '999990'):
            HostContext.I1USID = TradeContext.USERNO       #���׹�Ա��
        #end
        
        #begin 20091110 ������ �޸������־
        #HostContext.I1OPFG = "2"                           #�����־(1-�������� 2-��������)
        #������ռ䴦����1�������ڴ����ռ�ʱ��3��״̬(0-����ʧ�ܣ�1-���ڴ���2-����ɹ���������0��1״̬ʱ������ʧ��)
        #������������ʱ��2��״̬(0-����ʧ�ܣ�1-����ɹ�)��Ϊ�˱��⵱״̬Ϊ1��ʱ������յ�Ҳ���ʧ�ܣ��ʴ�����
        if (TradeContext.NOTE3 == "0"):
            HostContext.I1OPFG = "1"
        else:
            HostContext.I1OPFG = "2"
        #end
        
        ########################################################################################
        #20090922 ������ �޸�ԭ�����Ӵ����־
        ########################################################################################
        #HostContext.I1TRFG = "1"                           #�����־(0-��ʱ���� 1-���մ���)
        HostContext.I1TRFG = TradeContext.NOTE3            #�����־(0-��ʱ���� 1-���մ���)
        ########################################################################################
        HostContext.I1RPTF = "0"                           #�ظ���־(0-���δ��� 1-��δ���)
        HostContext.I1STDT = TradeContext.STARTDATE        #������ʼ����
        HostContext.I1ENDT = TradeContext.ENDDATE          #������ֹ����
        HostContext.I1COUT = TradeContext.TOTALNUM         #ί���ܱ���
        HostContext.I1TOAM = TradeContext.TOTALAMT         #ί���ܽ��
        HostContext.I1FINA = HostFileName                  #�����ļ�����

        HostTradeCode = "8814".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8814.map', HostTradeCode, "0002" )
        if ( HostContext.host_Error ):
            WrtLog('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)

            if ( HostContext.host_ErrorType == 5 ):
                #��ʱ
                return 0
            else:
                return -1

        else:
            #JSY0065����¼�Ѵ���
            if ( HostContext.O1MGID == "AAAAAAA" ):
                WrtLog('>>>֪ͨ���ʽ��=[' + HostContext.O1MGID + ']���׳ɹ�')
#                WrtLog('���ؽ��:' + HostContext.O1ACUR)                          #�ظ�����
#                WrtLog('���ؽ��:' + HostContext.O1TRDT)                          #��������
#                WrtLog('���ؽ��:' + HostContext.O1TRTM)                          #����ʱ��
#                WrtLog('���ؽ��:' + HostContext.O1TLSQ)                          #��Ա��ˮ��
#                WrtLog('���ؽ��:' + HostContext.O1CLDT)                          #����ί������
#                WrtLog('���ؽ��:' + HostContext.O1UNSQ)                          #����ί�к�
#                WrtLog('���ؽ��:' + HostContext.O1NBBH)                          #����ҵ���
                return 0

            elif ( HostContext.O1MGID == "FILE001" ):
                #�ļ�������
                WrtLog('>>>֪ͨ���ʽ��=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

            elif ( HostContext.O1MGID == "JSY0065" ):
                #��¼�Ѵ���
                WrtLog('>>>֪ͨ���ʽ��=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return 0

            else:
                WrtLog('>>>֪ͨ���ʽ��=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>���ͼ���֪ͨ�쳣')
        return -1

#20091103  ������  ���ӷ���CallHost����������8877���ռ���������
#=========================�����ռ������������֪ͨ==========================================
def CallHost(curBatchNo):

    WrtLog('>>>�����ռ������������֪ͨ(CallHost)')

    try:
        HostFileName = 'A' + curBatchNo[8:16] + '1'

        #ͨѶ�����
        HostContext.I1TRCD = '8877'                        #����������
        HostContext.I1SBNO = TradeContext.BRNO             #�ý��׵ķ������
        HostContext.I1USID = '999986'                      #���׹�Ա��
        HostContext.I1AUUS = ""                            #��Ȩ��Ա
        HostContext.I1AUPS = ""                            #��Ȩ��Ա����
        HostContext.I1WSNO = "AFAP_BATCH"                  #�ն˺�
        HostContext.I1CLDT = TradeContext.WorkDate         #����ί������
        HostContext.I1UNSQ = TradeContext.BATCHNO[4:16]    #����ί�к�
        HostContext.I1FINA = HostFileName                  #�����ļ�����

        HostTradeCode = "8877".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8877.map', HostTradeCode, "0002" )
        if ( HostContext.host_Error ):
            WrtLog('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)

            if ( HostContext.host_ErrorType == 5 ):
                #��ʱ
                return 0
            else:
                return -1

        else:
            #JSY0065����¼�Ѵ���
            if ( HostContext.O1MGID == "AAAAAAA" ):
                WrtLog('>>>֪ͨ���ʽ��=[' + HostContext.O1MGID + ']���׳ɹ�')
#                WrtLog('���ؽ��:' + HostContext.O1ACUR)                          #�ظ�����
#                WrtLog('���ؽ��:' + HostContext.O1TRDT)                          #��������
#                WrtLog('���ؽ��:' + HostContext.O1TRTM)                          #����ʱ��
#                WrtLog('���ؽ��:' + HostContext.O1TLSQ)                          #��Ա��ˮ��
#                WrtLog('���ؽ��:' + HostContext.O1CLDT)                          #����ί������
#                WrtLog('���ؽ��:' + HostContext.O1UNSQ)                          #����ί�к�
#                WrtLog('���ؽ��:' + HostContext.O1NBBH)                          #����ҵ���
                return 0

            elif ( HostContext.O1MGID == "FILE001" ):
                #�ļ�������
                WrtLog('>>>֪ͨ���ʽ��=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

            elif ( HostContext.O1MGID == "JSY0065" ):
                #��¼�Ѵ���
                WrtLog('>>>֪ͨ���ʽ��=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return 0

            else:
                WrtLog('>>>֪ͨ���ʽ��=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>���ͼ���֪ͨ�쳣')
        return -1


#=========================���������������ļ�==================================
def RecvResultFile(curBatchNo):

    WrtLog('>>>���������������ļ�(RecvResultFile)')

    try:
    
        HostFileName = 'A' + curBatchNo[8:16] + '2'
        HostBatchNo  = curBatchNo[4:16]

        #ͨѶ�����
        HostContext.I1TRCD = '8815'                        #����������
        HostContext.I1SBNO = TradeContext.BRNO             #�ý��׵ķ������
        HostContext.I1USID = '999986'                      #���׹�Ա��
        HostContext.I1AUUS = ""                            #��Ȩ��Ա
        HostContext.I1AUPS = ""                            #��Ȩ��Ա����
        HostContext.I1WSNO = ""                            #�ն˺�
        HostContext.I1NBBH = TradeContext.APPNO            #����ҵ���
        HostContext.I1CLDT = TradeContext.BATCHDATE        #����ί������
        HostContext.I1UNSQ = HostBatchNo                   #����ί�к�
        HostContext.I1FINA = HostFileName                  #�´��ļ���
        HostContext.I1DWFG = "2"                           #�´���־(0-���سɹ���ϸ,1-����ʧ����ϸ,2-ȫ������)

        HostTradeCode = "8815".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8815.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            WrtLog('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)

            #��ʱ
            if ( HostContext.host_ErrorType == 5 ):
                return 1
            else:
                return -1

        else:
            #XCR0001:��¼������ AGR0005:����δ����
            if ( HostContext.O1MGID == "AAAAAAA" ):
                WrtLog('>>>���ɴ�����=[' + HostContext.O1MGID + ']���׳ɹ�')
                WrtLog('���ؽ��:������ˮ��  = ' + HostContext.O1TLSQ)        #������ˮ��
                WrtLog('���ؽ��:����ҵ���  = ' + HostContext.O1NBBH)        #����ҵ���
                WrtLog('���ؽ��:����ί�к�  = ' + HostContext.O1CLDT)        #����ί������
                WrtLog('���ؽ��:����ί�к�  = ' + HostContext.O1UNSQ)        #����ί�к�
                WrtLog('���ؽ��:������ˮ��  = ' + HostContext.O1AMTL)        #����������ˮ��
                WrtLog('���ؽ��:��������    = ' + HostContext.O1DATE)        #��������
                WrtLog('���ؽ��:����ʱ��    = ' + HostContext.O1TIME)        #����ʱ��
                WrtLog('���ؽ��:������Ϣ��ʶ= ' + HostContext.O1MSSG)        #������Ϣ��ʶ
                WrtLog('���ؽ��:�����־    = ' + HostContext.O1OPFG)        #�����־(1-�������� 2-��������)
                WrtLog('���ؽ��:�����־    = ' + HostContext.O1TRFG)        #�����־(0-��ʱ���� 1-���մ���)
                WrtLog('���ؽ��:�ظ���־    = ' + HostContext.O1RPTF)        #�ظ���־(0-���δ��� 1-��δ���)
                WrtLog('���ؽ��:������ʼ����= ' + HostContext.O1STDT)        #������ʼ����
                WrtLog('���ؽ��:������ֹ����= ' + HostContext.O1ENDT)        #������ֹ����
                WrtLog('���ؽ��:ί���ܱ���  = ' + HostContext.O1COUT)        #ί���ܱ���
                WrtLog('���ؽ��:ί���ܽ��  = ' + HostContext.O1TOAM)        #ί���ܽ��
                WrtLog('���ؽ��:�ɹ��ܱ���  = ' + HostContext.O1SUCN)        #�ɹ��ܱ���
                WrtLog('���ؽ��:�ɹ��ܽ��  = ' + HostContext.O1AMAO)        #�ɹ��ܽ��
                WrtLog('���ؽ��:ʧ���ܱ���  = ' + HostContext.O1FACN)        #ʧ���ܱ���
                WrtLog('���ؽ��:ʧ���ܽ��  = ' + HostContext.O1AMOT)        #ʧ���ܽ��
                WrtLog('���ؽ��:�´��ļ�����= ' + HostContext.O1FINA)        #�´��ļ�����

                #ת��
                HostTotalNum = (long)(HostContext.O1COUT)
                HostTotalAmT = (float)(HostContext.O1TOAM)
                HostSuccNum  = (long)(HostContext.O1SUCN)
                HostSuccAmT  = (float)(HostContext.O1AMAO)
                HostFailNum  = (long)(HostContext.O1FACN)
                HostFailAmT  = (float)(HostContext.O1AMOT)

                HostContext.O1COUT = str(HostTotalNum)
                HostContext.O1TOAM = str(HostTotalAmT)
                HostContext.O1SUCN = str(HostSuccNum)
                HostContext.O1AMAO = str(HostSuccAmT)
                HostContext.O1FACN = str(HostFailNum)
                HostContext.O1AMOT = str(HostFailAmT)

                UpdateBatchDate(curBatchNo,HostContext.O1DATE, HostContext.O1TIME)
                WrtLog('>>>�޸Ľ���ʱ��['+ HostContext.O1DATE + ':' + HostContext.O1TIME +']')
                return 0

            elif ( HostContext.O1MGID == "ACR8803" ):
                WrtLog('>>>��������������=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return 1

            else:
                WrtLog('>>>��������������=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>���������������쳣')
        return -1


#=========================��ѯ��������ļ��Ƿ�����==============================
def ChkHostFile(curBatchNo):

    WrtLog('>>>��ѯ��������ļ��Ƿ�����(ChkHostFile)')

    try:
    
        HostFileName = 'A' + curBatchNo[8:16] + '2'
        HostBatchNo  = curBatchNo[4:16]

        #ͨѶ�����
        HostContext.I1TRCD = '8819'                        #������
        HostContext.I1SBNO = TradeContext.BRNO             #���׻�����
        HostContext.I1USID = '999986'                      #���׹�Ա��
        HostContext.I1AUUS = ""                            #��Ȩ��Ա
        HostContext.I1AUPS = ""                            #��Ȩ��Ա����
        HostContext.I1WSNO = ""                            #�ն˺�
        HostContext.I1NBBH = TradeContext.APPNO            #����ҵ���ʶ
        HostContext.I1CLDT = TradeContext.BATCHDATE        #ԭ��������
        HostContext.I1UNSQ = HostBatchNo                   #ԭ����ί�к�
        HostContext.I1FILE = HostFileName                  #ɾ���ļ���
        HostContext.I1OPFG = '0'                           #������־(0-��ѯ 1-ɾ���ϴ��ļ� 2-ɾ���´��ļ�)

        HostTradeCode = "8819".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8819.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            WrtLog('>>>��������ʧ��=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return -1

        else:
            #XCR0001:��¼������ AGR0005:����δ����
            if ( HostContext.O1MGID == "AAAAAAA" ):
                WrtLog('>>>��ѯ������=[' + HostContext.O1MGID + ']���׳ɹ�')
                WrtLog('���ؽ��:�ظ�����     = ' + HostContext.O1ACUR)        #�ظ�����
                WrtLog('���ؽ��:��������     = ' + HostContext.O1TRDT)        #��������
                WrtLog('���ؽ��:����ʱ��     = ' + HostContext.O1TRTM)        #����ʱ��
                WrtLog('���ؽ��:��Ա��ˮ     = ' + HostContext.O1TLSQ)        #��Ա��ˮ
                WrtLog('���ؽ��:����ҵ���ʶ = ' + HostContext.O1NBBH)        #����ҵ���ʶ
                WrtLog('���ؽ��:����ί������ = ' + HostContext.O1CLDT)        #����ί������
                WrtLog('���ؽ��:����ί�к�   = ' + HostContext.O1UNSQ)        #����ί�к�
                WrtLog('���ؽ��:�´��ļ���   = ' + HostContext.O1FILE)        #�´��ļ���
                WrtLog('���ؽ��:�ļ�״̬     = ' + HostContext.O1STCD)        #�ļ�״̬(0-δ���� 1-������ 2-��ɾ��)
                WrtLog('���ؽ��:ί���ܱ���   = ' + HostContext.O1COUT)        #ί���ܱ���
                WrtLog('���ؽ��:ί���ܽ��   = ' + HostContext.O1TOAM)        #ί���ܽ��
                WrtLog('���ؽ��:�ɹ��ܱ���   = ' + HostContext.O1SUCN)        #�ɹ��ܱ���
                WrtLog('���ؽ��:�ɹ��ܽ��   = ' + HostContext.O1AMAO)        #�ɹ��ܽ��
                WrtLog('���ؽ��:ʧ���ܱ���   = ' + HostContext.O1FACN)        #ʧ���ܱ���
                WrtLog('���ؽ��:ʧ���ܽ��   = ' + HostContext.O1AMOT)        #ʧ���ܽ��

                WrtLog('O1STCD='+HostContext.O1STCD)

                if (HostContext.O1STCD == '1'):
                    #ת��
                    HostTotalNum = (long)(HostContext.O1COUT)
                    HostTotalAmT = (float)(HostContext.O1TOAM)
                    HostSuccNum  = (long)(HostContext.O1SUCN)
                    HostSuccAmT  = (float)(HostContext.O1AMAO)
                    HostFailNum  = (long)(HostContext.O1FACN)
                    HostFailAmT  = (float)(HostContext.O1AMOT)

                    HostContext.O1COUT = str(HostTotalNum)
                    HostContext.O1TOAM = str(HostTotalAmT)
                    HostContext.O1SUCN = str(HostSuccNum)
                    HostContext.O1AMAO = str(HostSuccAmT)
                    HostContext.O1FACN = str(HostFailNum)
                    HostContext.O1AMOT = str(HostFailAmT)

                    #UpdateBatchDate(curBatchNo,HostContext.O1TRDT, HostContext.O1TRTM)
                    #WrtLog('>>>�޸Ľ���ʱ��['+ HostContext.O1TRDT + ':' + HostContext.O1TRTM +']')

                    return 0
                else:
                    return -1

            elif ( HostContext.O1MGID == "XCR0001" ):
                #��¼������
                WrtLog('>>>��ѯ������=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return 1

            else:
                WrtLog('>>>��ѯ������=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)
                return -1

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>��ѯ�����������쳣')
        return -1


#=========================��ʽ���ļ�============================================
def FormatFile(ProcType, sFileName, dFileName):

    WrtLog('>>>��ʽ���ļ�:' + ProcType + ' ' + sFileName + ' ' + dFileName)

    try:

        srcFileName    = os.environ['AFAP_HOME'] + '/data/batch/host/' + sFileName
        dstFileName    = os.environ['AFAP_HOME'] + '/data/batch/host/' + dFileName

        if (ProcType == "1"):
            #ascii->ebcd
            #���ø�ʽ:cvt2ebcdic -T Դ�ı��ļ� -P Ŀ�������ļ� -F fld��ʽ�ļ� [ -D ����� ]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ebcdic'
            fldFileName = os.environ['AFAP_HOME'] + '/data/cvt/agent01.fld'
            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName 

        else:
            #ebcd->ascii
            #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D �����] [-S] [-R]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
            fldFileName = os.environ['AFAP_HOME'] + '/data/cvt/agent02.fld'
            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName 
        #WrtLog('>>>ת�룺' + cmdstr)

        ret = os.system(cmdstr)                      
        if ( ret != 0 ):                             
            ret = False
        else:                                        
            ret = True

        return ret

    except Exception, e:
        WrtLog( str(e) )
        WrtLog('>>>��ʽ���ļ��쳣')
        return False


#=========================������λ�����ļ�======================================
def CrtBusiFile(curBatchNo):

    WrtLog('>>>������λ�����ļ�(CrtBusiFile)')

    try:
        rHostFile= os.environ['AFAP_HOME'] + '/data/batch/host/' +  curBatchNo + '_4'
        
        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        rBusiFile= os.environ['AFAP_HOME'] + '/data/batch/down/' +  TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + '.RET'
        #end

        #������ҵ�����ļ�
        bFp = open(rBusiFile, "w")

        #д��������
        wbuffer = '1'                                                  + '|'          #��¼����(1-���� 2-��ϸ)
        wbuffer = wbuffer + TradeContext.APPNO.ljust(6, ' ')           + '|'          #ҵ����
        wbuffer = wbuffer + TradeContext.BUSINO.ljust(14, ' ')         + '|'          #��λ���
        wbuffer = wbuffer + TradeContext.AGENTTYPE                     + '|'          #ί�з�ʽ(3-���ۣ� 4-����)
        wbuffer = wbuffer + TradeContext.ACCNO.ljust(23, ' ')          + '|'          #�Թ��ʺ�
                                                                  
        if ( len(TradeContext.BUSINAME)> 20 ):                                   
            wbuffer = wbuffer + TradeContext.BUSINAME[0:20]            + '|'          #����(��λ����)
        else:                                                                    
            wbuffer = wbuffer + TradeContext.BUSINAME.ljust(20, ' ')   + '|'          #����(��λ����)
                                                                                 
        wbuffer = wbuffer + '1'                                        + '|'          #״̬
        wbuffer = wbuffer + TradeContext.TOTALNUM.rjust(10, ' ')       + '|'          #�ܱ���
        wbuffer = wbuffer + TradeContext.TOTALAMT.rjust(17, ' ')       + '|'          #�ܽ��
        wbuffer = wbuffer + ' '.rjust(8,  ' ')                         + '|'          #������
        wbuffer = wbuffer + TradeContext.SUCCNUM.rjust(10, ' ')        + '|'          #�ɹ�����
        wbuffer = wbuffer + TradeContext.SUCCAMT.rjust(17, ' ')        + '|'          #�ɹ����
        wbuffer = wbuffer + TradeContext.FAILNUM.rjust(10, ' ')        + '|'          #ʧ�ܱ���
        wbuffer = wbuffer + TradeContext.FAILAMT.rjust(17, ' ')        + '|'          #ʧ�ܽ��
        wbuffer = wbuffer + ' '.ljust(7,  ' ')                         + '|'          #����
        wbuffer = wbuffer + '\n'                                                 
                                                                                 
        bFp.write(wbuffer)                                                       
        #�����������ļ�                                                        
        hFp = open(rHostFile, "r")                                               
                                                                                 
        #��ȡһ��                                                                
        linebuf = hFp.readline()                                                 
        while ( len(linebuf) > 0 ):

            if ( len(linebuf) < 994 ):
                hFp.close()
                bFp.close()
                return ExitThisFlow( '9000', '�����������ļ���ʽ����,����')

            swapbuf = linebuf[0:994].split('<fld>')

            #д����ϸ��Ϣ
            
            #begin 20100413 ������   �����ļ���û�зָ�����ʹ�ò��㣬�޸�ΪΪÿ���ֶκ����'|'�ָ���
            wbuffer = '2'                                              + '|'       #��¼����(1-����,2-��ϸ)
            wbuffer = wbuffer + swapbuf[25].strip().ljust(21, ' ')     + '|'       #�ͻ���ʶ

            if ( TradeContext.AGENTTYPE == '3' ):
                wbuffer = wbuffer + '4'                                + '|'       #ί�з�ʽ(3-����,4-����)
                wbuffer = wbuffer + swapbuf[14].strip().ljust(23, ' ') + '|'       #�����ʺ�
                wbuffer = wbuffer + swapbuf[15].strip().ljust(20, ' ') + '|'       #�ͻ�����
            else:
                wbuffer = wbuffer + '3'                                + '|'       #ί�з�ʽ(3-����,4-����)
                wbuffer = wbuffer + swapbuf[20].strip().ljust(23, ' ') + '|'       #�����ʺ�
                wbuffer = wbuffer + swapbuf[21].strip().ljust(20, ' ') + '|'       #�ͻ�����

            wbuffer = wbuffer + '1'                                    + '|'       #״̬
            wbuffer = wbuffer + '1'.rjust(10, ' ')                     + '|'       #����
            wbuffer = wbuffer + swapbuf[28].strip().rjust(17, ' ')     + '|'       #���
            
            tmp_retcode = swapbuf[5].strip()

            retstr = ''
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                if ( TradeContext.AGENTTYPE == '3' ):
                    retstr = "���۳ɹ�"
                else:
                    retstr = "�����ɹ�"
            else:
                if ( TradeContext.AGENTTYPE == '3' ):
                    retstr = "����ʧ��"
                else:
                    retstr = "����ʧ��"
             
            #begin 20110616 ����̩�޸�   ����ȫ��򲿷ֿۿ�ı�ʶλ ��Ӧ�۽���ֶ�   ����ȫ��򲿷ֿۿ��ʶλ����ڻᳮ��ʶ�ֶ���
            #Ӧ�۽������ڴ�����Ϣ������
            #wbuffer = wbuffer +swapbuf[30].strip().ljust(1, ' ')         + '|'    #�ᳮ��ʶ�ڴ���ʱ��ŵ�Ϊȫ��򲿷ֿۿ��ʶ 
            cashflag = swapbuf[30].strip()                                         #ȡ���ᳮ��ʶ��ֵ ����ʱΪABCD����ʱΪ0
            if(cashflag.replace('.','')).isdigit():                                #��������ֱ�ʾ����
                wbuffer =wbuffer +' '.strip().rjust(1,' ')                + '|'    #����ʱΪ��
            else:
                wbuffer =wbuffer +cashflag.strip().rjust(1,' ')            + '|'   #����ʱ���ABCD��ʶ
            
            amount  =  swapbuf[6].strip()
            if (amount.replace('.','')).isdigit():                                 #��������� ˵�����۳ɹ����ֶδ�ŵ���Ӧ�۽��
                wbuffer =wbuffer + amount.strip().rjust(17,' ')         + '|'      #���۳ɹ�ʱ���Ӧ�۽��
                errormsg = ' '
            elif (len(amount)==0):                                                 #���Ϊ�� ˵���Ǵ���  
                wbuffer =wbuffer +' '.strip().rjust(17,' ')          + '|'         #�����ɹ�ʱΪӦ�۽���ֵ 
                errormsg = ' '
                
            else:                                                                  #�����Ϊ��Ҳ��Ϊ���� ˵���Ǵ�������ʧ��   
                wbuffer =wbuffer +' '.strip().rjust(17,' ')          + '|'         #��������ʧ��ʱӦ�۽��ҲΪ��
                errormsg = swapbuf[6].strip()               
            wbuffer = wbuffer + retstr.rjust(8, ' ')                  + '|'       #�ɹ�ʧ��˵��

            
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                tmp_retcode = "AAAAAAA"
            
            wbuffer = wbuffer + tmp_retcode.ljust(7,  ' ')             + '|'       #������
            
            wbuffer = wbuffer + errormsg.strip().ljust(62,' ')         + '|'       #������Ϣ
            wbuffer = wbuffer + '\n'
            #end 20110616 ����̩ �޸�

            bFp.write(wbuffer)

            linebuf = hFp.readline()

        hFp.close()
        bFp.close()
        return True

    except Exception, e:
        hFp.close()
        bFp.close()
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '������λ�����ļ��쳣')


#=========================�������б����ļ�======================================
def CrtBankFile(curBatchNo):

    WrtLog('>>>�������б����ļ�(CrtBankFile)')

    try:

        rHostFile= os.environ['AFAP_HOME'] + '/data/batch/host/' +  curBatchNo + '_4'
        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        rBankFile= os.environ['AFAP_HOME'] + '/data/batch/down/' +  TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + '.RPT'
        #end

        #����ҵ�񱨱��ļ�
        bFp = open(rBankFile, "w")

        #д�����
        bFp.write('\n\n\n                      ********** ��������ҵ�񱨱�(ί�к�:' + curBatchNo + ') **********\n\n\n')

        #д��������
        bFp.write('ҵ�����=' + TradeContext.APPNO.ljust(23,' ')    + ' ҵ������=' +    TradeContext.APPNAME   + '\n')
        bFp.write('��λ����=' + TradeContext.BUSINO.ljust(23,' ')   + ' ��λ����=' +    TradeContext.BUSINAME  + '\n')
        bFp.write('��λ�ʺ�=' + TradeContext.ACCNO.ljust(23,' ')    + ' �ڲ��ʺ�=' +    TradeContext.VOUHNO    + '\n')
        bFp.write('��������=' + TradeContext.BATCHDATE + '\n')
        bFp.write('�� �� ��=' + TradeContext.TOTALNUM.ljust(23,' ') + ' �� �� ��=' +    TradeContext.TOTALAMT  + '\n')
        bFp.write('�ɹ�����=' + TradeContext.SUCCNUM.ljust(23,' ')  + ' �ɹ����=' +    TradeContext.SUCCAMT   + '\n')
        bFp.write('ʧ�ܱ���=' + TradeContext.FAILNUM.ljust(23,' ')  + ' ʧ�ܽ��=' +    TradeContext.FAILAMT   + '\n')

        bFp.write('----------------------------------------------------------------------------------------------------------\n')
        bFp.write('���   �ͻ���ʶ                  ������/����             �ͻ�����                          ���    ���(1:�ɹ� 0-ʧ��) \n')
        bFp.write('----------------------------------------------------------------------------------------------------------\n')

        #�����������ļ�
        hFp = open(rHostFile, "r")

        ireccount=0

        #��ȡһ��
        linebuf = hFp.readline()
        while ( len(linebuf) > 0 ):

            if ( len(linebuf) < 994 ):
                hFp.close()
                bFp.close()
                return ExitThisFlow( '9999', '�����������ļ���ʽ����,����')

            ireccount=ireccount+1

            swapbuf = linebuf[0:994].split('<fld>')

            #д����ϸ��Ϣ
            wbuffer = ''
            wbuffer = wbuffer + str(ireccount).ljust(7, ' ')                  #���(20080402,XZH,��10�޸�Ϊ7)
            wbuffer = wbuffer + swapbuf[25].strip().ljust(26, ' ')            #�ͻ���ʶ(20080402,XZH,��21�޸�Ϊ25)

            if ( TradeContext.AGENTTYPE == '3' ):
                wbuffer = wbuffer + swapbuf[14].strip().ljust(24, ' ')        #�����ʺ�
                wbuffer = wbuffer + swapbuf[15].strip().ljust(21, ' ')        #�ͻ�����
            else:
                wbuffer = wbuffer + swapbuf[20].strip().ljust(24, ' ')        #�����ʺ�
                wbuffer = wbuffer + swapbuf[21].strip().ljust(21, ' ')        #�ͻ�����

            wbuffer = wbuffer + swapbuf[28].strip().rjust(17, ' ')            #���

            tmp_retcode = swapbuf[5].strip()
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                wbuffer = wbuffer + '1'.rjust(5,  ' ')                        #������(1-�ɹ�)
            else:
                wbuffer = wbuffer + '0'.rjust(5,  ' ')                        #������(0-ʧ��)

            wbuffer = wbuffer + '\n'
            bFp.write(wbuffer)

            linebuf = hFp.readline()

        hFp.close()
        bFp.close()

        return True

    except Exception, e:
        hFp.close()
        bFp.close()
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '������λ�����ļ��쳣')





































######################################################################################################################
#�����������ļ�ת����У��(��Χ)
######################################################################################################################
def SQ_OTHER_Proc(curBatchNo):


    WrtLog('>>>���봦��(SQ_OTHER_Proc)')


    ret = 0
    try:
        #У����Ч��
        iline=0
        if ( TradeContext.WorkDate > TradeContext.ENDDATE ):
            UpdateBatchInfo(curBatchNo, "40", "�Զ�����,���ι���")
            return ExitThisFlow( "9000", "�Զ�����,���ι���")

        #�ж��ļ��Ƿ����
        m_totalnum = 0
        m_totalamt = 0
        
        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        bFileName = os.environ['AFAP_HOME'] + '/data/batch/swap/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        sFileName = os.environ['AFAP_HOME'] + '/data/batch/swap/OTHER_SWAP_AFA.TXT'
        iFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        #end
        
        swapbuf   = ''

        #begin
        #�ر��  20090330  ɾ����ϸ������Ϣ�ļ�
        DelProcmsgFile(curBatchNo)
        
        #�ر��  20090330  ��ʼ����ϸ�����ʶ��  procFlag(0-����,1-�쳣)
        procFlag = 0
        #end
        
        if ( os.path.exists(bFileName) ):

            #���ļ�
            bfp = open(bFileName, "r")

             #�����ļ�
            sfp= open(sFileName,  "w")

            #��������������Ϣ
            recinfo = "1"                                                     #��¼����(1-���� 2-��ϸ)
            recinfo = recinfo + TradeContext.APPNO.ljust(6, ' ')              #ҵ����
            recinfo = recinfo + TradeContext.BUSINO.ljust(14, ' ')            #��λ���
            recinfo = recinfo + TradeContext.AGENTTYPE.ljust(1, ' ')          #ί�з�ʽ(3-���� 4-����)
            recinfo = recinfo + TradeContext.ACCNO.ljust(23, ' ')             #�Թ��ʺ�

            if ( len(TradeContext.BUSINAME) > 20 ):
                recinfo = recinfo + TradeContext.BUSINAME[0:20]               #����(��λ����)
            else:
                recinfo = recinfo + TradeContext.BUSINAME.ljust(20, ' ')      #����(��λ����)

            recinfo = recinfo + '1'                                           #״̬(0-���� 1-����)
            recinfo = recinfo + TradeContext.TOTALNUM.rjust(10, ' ')          #�ܱ���
            recinfo = recinfo + TradeContext.TOTALAMT.rjust(17, ' ')          #�ܽ��
            recinfo = recinfo + ' '.ljust(7, ' ')                             #������

            sfp.write(recinfo + '\n')

            #��ȡһ��
            linebuf = bfp.readline()
            iline=0
            while ( len(linebuf) > 20 ):
                iline=iline+1
                swapbuf = UtilTools.rStripChar(linebuf, '\n')
                databuf = swapbuf.split('|')
                WrtLog("=============line" + str(iline) + "==============")

                if ( len(databuf) != 4 and len(databuf) != 5 ):
                    
                    #begin  �ر��  20090330
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,���ݸ�ʽ����(�����������):��" + str(iline) + "��")
                    #return ExitThisFlow( "9000", "�Զ�����,���ݸ�ʽ����(�����������):��" + str(iline) + "��" )
                    
                    UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","���ݸ�ʽ����(�����������):��" + str(iline) + "��")
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end

                m_custid   = databuf[0].lstrip().rstrip()
                m_accno    = databuf[1].lstrip().rstrip()
                m_custname = databuf[2].lstrip().rstrip()
                m_tradeamt = databuf[3].lstrip().rstrip()

                chkFlag = 0
                #У�������Ƿ�Ϸ�
                if ( not (m_accno.isdigit() and (len(m_accno)==19 or len(m_accno)==23)) ):
                    
                    #begin  �ر��  20090330
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(�ʺŷǷ�):��" + str(iline) + "��")
                    #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(�ʺŷǷ�):��" + str(iline) + "��")
                    
                    UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(�ʺŷǷ�):��" + str(iline) + "��" + ",�˺�Ϊ:" + m_accno )
                    procFlag = 1
                    chkFlag  = 1
                    #linebuf = bfp.readline()
                    #continue
                    ##end

                if  not (m_tradeamt.replace('.','')).isdigit() :
                    
                    #begin  �ر��  20090330
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(���Ƿ�):��" + str(iline) + "��")
                    #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(���Ƿ�):��" + str(iline) + "��")
                    
                    UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(���Ƿ�):��" + str(iline) + "��" + ",�˺�Ϊ:" + m_accno)
                    procFlag = 1
                    chkFlag  = 1
                    #linebuf = bfp.readline()
                    #continue
                    ##end

                if chkFlag == 1:
                    linebuf = bfp.readline()
                    continue

                if ( TradeContext.AGENTTYPE == '3' ):           #��������
                    #��ҪУ��ÿ�����������Ƿ��Ѿ�ע��
                    if not  ChkCustInfo(TradeContext.APPNO, TradeContext.BUSINO, m_accno):
                        
                        #begin  �ر��  20090330
                        
                        #bfp.close()
                        #sfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(�ͻ�δǩԼ):��"+str(iline) + "��")
                        #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(�ͻ�δǩԼ):��" + str(iline) + "��")
                        
                        UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(�ͻ�δǩԼ):��"+str(iline) + "��" + ",�˺�Ϊ:" + m_accno)
                        procFlag = 1
                        linebuf = bfp.readline()
                        continue
                        #end

                    m_agenttype = '4'

                elif ( TradeContext.AGENTTYPE == '4' ):         #��������
                     m_agenttype = '3'

                else:
                    #���ʹ���
                    
                    #begin  �ر��  20090330
                    
                    #bfp.close()
                    #sfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ί�з�ʽ����:��" + str(iline) + "��")
                    #return ExitThisFlow("9000", "�Զ�����,ί�з�ʽ����:��" + str(iline) + "��")
                    
                    UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","ί�з�ʽ����:��" + str(iline) + "��" + ",�˺�Ϊ:" + m_accno)
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end


                #����������ϸ��Ϣ
                recinfo = "2"                                             #��¼����(1-���� 2-��ϸ)



                #20120409 �º��޸����--AG07
                #if ( TradeContext.APPNO[0:4] == 'AG08' ):
                if ( TradeContext.APPNO[0:4] == 'AG08' or TradeContext.APPNO[0:4] == 'AG07'):
                    #�������⴦��(�޸��ˣ����Һͣ��޸����ڣ�20080402)
                    recinfo = recinfo + m_custid.ljust(38, ' ')           #�ͻ���ʶ(��ʵ�����31λ)
                else:
                    recinfo = recinfo + m_custid.ljust(20, ' ')           #�ͻ���ʶ


                recinfo = recinfo + m_agenttype                           #ί�з�ʽ(3-���� 4-����)

                recinfo = recinfo + m_accno.ljust(23, ' ')                #�����ʺ�

                if ( len(m_custname)> 20 ):
                    recinfo = recinfo + m_custname[0:20]                  #�ͻ�����
                else:
                    recinfo = recinfo + m_custname.ljust(20, ' ')         #�ͻ�����

                recinfo = recinfo + '1'                                   #״̬(0-���� 1-����)
                recinfo = recinfo + '1'.rjust(10, ' ')                    #�ܱ���
                recinfo = recinfo + m_tradeamt.rjust(17, ' ')             #�ܽ��
                recinfo = recinfo + ' '.ljust(7, ' ')                     #������

                sfp.write(recinfo + '\n')

                m_totalnum = m_totalnum + 1
                m_totalamt = m_totalamt + (long)((float)(m_tradeamt)*100 + 0.1)

                #���ļ��ж�ȡһ��
                linebuf = bfp.readline()

            bfp.close()
            sfp.close()
            
            #begin  �ر��  20090330 
            if (procFlag == 1):
                return ExitThisFlow( "9000", "�Զ�����,ԭ����д����ϸ�����ļ�")
            #end

            #ת��
            ls_totalnum = (long)(TradeContext.TOTALNUM)
            lm_totalnum = (long)(m_totalnum)
            ls_totalamt = (long)((float)(TradeContext.TOTALAMT)*100 + 0.1)
            lm_totalamt = m_totalamt

            WrtLog('>>>�������=%d ������=%d ��ϸ����=%d ��ϸ���=%d' % (ls_totalnum, ls_totalamt, lm_totalnum, lm_totalamt))


            #�ж��ܱ���,�ܽ��
            if ( (ls_totalnum!=lm_totalnum) or (ls_totalamt!=lm_totalamt) ):
                UpdateBatchInfo(curBatchNo, "40", "�Զ�����:�����ļ��ܱ������ܽ��������Ĳ���")
                return ExitThisFlow("9000", "�Զ�����,�����ļ��ܱ������ܽ��������Ĳ���")


            #�������ڲ���ʽ���������ļ��Ƶ��ڲ�Ŀ¼��
            cmdstr = "mv " + sFileName + " " + iFileName
            os.system(cmdstr)

            #ɾ��ԭʼ�ļ�
            cmdstr = "rm " + bFileName
            os.system(cmdstr)

            UpdateBatchInfo(curBatchNo, "11", "����ת��-У��ɹ�->����������")
            
            #################################################################
            #20090927 ����������  ��ʱ������Ҫ���������������
            #----------------------------------------------------------------
            if ( TradeContext.NOTE3 == '0' ):
                UpdateBatchInfo( curBatchNo, "21", "��ʱ����->���ύ" )
                return ExitThisFlow( "0000", "��ʱ����->���ύ" )
            #################################################################
            
            return ExitThisFlow("0000", "����ת��-У��ɹ�->����������")

        else:
            UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������������ļ�������")
            return ExitThisFlow("9000", "�Զ�����,�������������ļ�������")

    except Exception, e:
        bfp.close()
        sfp.close()
        WrtLog( str(e) )
        UpdateBatchInfo(curBatchNo, "40", "���봦��(��Χ)�쳣(���������ļ�)")
        return ExitThisFlow( '9999', '���봦��(��Χ)�쳣')





######################################################################################################################
#�������������봦��(VMENU)
######################################################################################################################
def SQ_VMENU_Proc(curBatchNo):


    WrtLog('>>>���봦��(SQ_VMENU_Proc)')


    ret = 0
    try:
        #У����Ч��
        if ( TradeContext.WorkDate > TradeContext.ENDDATE ):
            UpdateBatchInfo(curBatchNo, '40', '�Զ�����,���ι���')
            return ExitThisFlow( '9000', '�Զ�����,���ι���')


        #�ж��ļ��Ƿ����
        m_totalnum = 0
        m_totalamt = 0
        
        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        bFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE
        #end

        WrtLog(bFileName)
        
        #begin
        #�ر��  20090330  ɾ����ϸ������Ϣ�ļ�
        DelProcmsgFile(curBatchNo)
        
        #�ر��  20090330  ��ʼ����ϸ�����ʶ��  procFlag(0-����,1-�쳣)
        procFlag = 0
        #end

        if ( os.path.exists(bFileName) ):

            #���ļ�
            bfp = open(bFileName, "r")

            #��ȡһ��
            linebuf = bfp.readline()
            iline=0
            while ( len(linebuf) > 0 ):
                iline=iline+1
                if ( (len(linebuf) != 100) and (len(linebuf) != 101) ):
                    
                    #begin  �ر��  20090330
                    
                    #bfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݸ�ʽ��:��" + str(iline) + "��")
                    #return ExitThisFlow( "9000", "�Զ�����,�������ݸ�ʽ��:��" + str(iline) + "��")
                    
                    UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݸ�ʽ��:��" + str(iline) + "��")
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end

                #������Ϣ
                if ( linebuf[0] == '1' ):
                    s_rectype    = linebuf[0:1].lstrip().rstrip()          #��¼����
                    s_appno      = linebuf[1:7].lstrip().rstrip()          #ҵ����
                    s_busino     = linebuf[7:21].lstrip().rstrip()         #��λ���
                    s_agenttype  = linebuf[21:22].lstrip().rstrip()        #ί�з�ʽ
                    s_accno      = linebuf[22:45].lstrip().rstrip()        #�Թ��ʺ�
                    s_remark     = linebuf[45:65].lstrip().rstrip()        #����
                    s_status     = linebuf[65:66].lstrip().rstrip()        #״̬
                    s_totalnum   = linebuf[66:76].lstrip().rstrip()        #�ܱ���
                    s_totalamt   = linebuf[76:93].lstrip().rstrip()        #�ܽ��
                    s_retcode    = linebuf[93:100].lstrip().rstrip()       #������

                    chkFlag = 0
                    #У�����ݺϷ���
                    if ( not (s_agenttype.isdigit() and (len(s_accno)==0 or len(s_accno)==23) and s_status.isdigit() and s_totalnum.isdigit()) ):
                        
                        #begin  �ر��  20090330
                        
                        #bfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(����):��" + str(iline) + "��")
                        #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(����):��" + str(iline) + "��")
                        
                        UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(����):��" + str(iline) + "��"+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                        procFlag = 1
                        chkFlag = 1
                        #linebuf = bfp.readline()
                        #continue
                        ##end
                        
                    if not (s_totalamt.replace('.','')).isdigit():
                        
                        #begin  �ر��  20090330
                        
                        #bfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(����):��" + str(iline) + "��")
                        #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(����):��" + str(iline) + "��")
                        
                        UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(����):��" + str(iline) + "��"+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                        procFlag = 1
                        chkFlag = 1
                        #linebuf = bfp.readline()
                        #continue
                        ##end
                        
                    #begin  �ر��  20090330
                    if chkFlag == 1:
                        linebuf = bfp.readline()
                        continue
                    #end

                #��ϸ��Ϣ
                elif ( linebuf[0] == '2' ):
                    m_rectype    = linebuf[0:1].lstrip().rstrip()          #��¼����
                    m_custid     = linebuf[1:21].lstrip().rstrip()         #�ͻ���ʶ
                    m_agenttype  = linebuf[21:22].lstrip().rstrip()        #ί�з�ʽ
                    m_accno      = linebuf[22:45].lstrip().rstrip()        #�����ʺ�
                    m_remark     = linebuf[45:65].lstrip().rstrip()        #����
                    m_status     = linebuf[65:66].lstrip().rstrip()        #״̬
                    m_tradenum   = linebuf[66:76].lstrip().rstrip()        #����
                    m_tradeamt   = linebuf[76:93].lstrip().rstrip()        #���
                    m_retcode    = linebuf[93:100].lstrip().rstrip()       #������

                    chkFlag = 0
                    #У�����ݺϷ���
                    if ( not (m_agenttype.isdigit() and m_accno.isdigit() and m_status.isdigit() and m_tradenum.isdigit()) ):
                        
                        #begin  �ر��  20090330
                        
                        #bfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(��ϸ):��"+str(iline) + "��")
                        #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(��ϸ):��" + str(iline) + "��")
                        
                        UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(��ϸ):��"+str(iline) + "��"+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                        procFlag = 1
                        chkFlag = 1
                        #linebuf = bfp.readline()
                        #continue
                        ##end
                        
                    if not (m_tradeamt.replace('.','')).isdigit():
                        
                        #begin  �ر��  20090330
                        
                        #bfp.close()
                        #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(��ϸ):��"+str(iline) + "��")
                        #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(��ϸ):��" + str(iline) + "��")
                        
                        UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(��ϸ):��"+str(iline) + "��"+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                        procFlag = 1
                        chkFlag = 1
                        #linebuf = bfp.readline()
                        #continue
                        ##end
                        
                    #begin  �ر��  20090330
                    if chkFlag == 1:
                        linebuf = bfp.readline()
                        continue
                    #end

                    #ɸѡ״̬Ϊ�����ļ�¼
                    if ( m_status == '1' ):

                        #ͳ�ƽ��ͱ���
                        m_totalnum = m_totalnum + 1
                        m_totalamt = m_totalamt + (long)((float)(m_tradeamt) * 100 + 0.1)

                        if ( s_agenttype == '3' ):
                            if ( m_agenttype != '4' ):
                                
                                #begin  �ر��  20090330
                                
                                #bfp.close()
                                #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(ί�з�ʽ��ƥ��):��" + str(iline) + "��")
                                #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(ί�з�ʽ��ƥ��):��" + str(iline) + "��")
                                
                                UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(ί�з�ʽ��ƥ��):��" + str(iline) + "��"+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                                procFlag = 1
                                linebuf = bfp.readline()
                                continue
                                #end


                            #У��ͻ���Ϣ�ǺϷ�
                            if not ChkCustInfo(TradeContext.APPNO, TradeContext.BUSINO, m_accno):
                                
                                #begin  �ر��  20090330
                                
                                #bfp.close()
                                #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(�ͻ�δǩԼ):��" + str(iline) + "��")
                                #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(�ͻ�δǩԼ):��" + str(iline) + "��")
                                
                                UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(�ͻ�δǩԼ):��" + str(iline) + "��"+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                                procFlag = 1
                                linebuf = bfp.readline()
                                continue
                                #end

                        elif ( s_agenttype == '4' ):
                            if ( m_agenttype != '3' ):
                                
                                #begin  �ر��  20090330
                                
                                #bfp.close()
                                #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(ί�з�ʽ��ƥ��):��" + str(iline) + "��")
                                #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(ί�з�ʽ��ƥ��):��" + str(iline) + "��")
                                
                                UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(ί�з�ʽ��ƥ��):��" + str(iline) + "��"+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                                procFlag = 1
                                linebuf = bfp.readline()
                                continue
                                #end

                        else:
                            
                            #begin  �ر��  20090330
                            
                            #bfp.close()
                            #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������ݷǷ�(ί�з�ʽ��):��" + str(iline) + "��")
                            #return ExitThisFlow("9000", "�Զ�����,�������ݷǷ�(ί�з�ʽ��):��" + str(iline) + "��")
                            
                            UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","�������ݷǷ�(ί�з�ʽ��):��" + str(iline) + "��"+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                            procFlag = 1
                            linebuf = bfp.readline()
                            continue
                            #end

                else:
                    
                    #begin  �ر��  20090330
                    
                    #bfp.close()
                    #UpdateBatchInfo(curBatchNo, "40", "�Զ�����,��¼��־��,��" + str(iline) + '��')
                    #return ExitThisFlow("9000", "�Զ�����,��¼��־��:��" + str(iline) + "��")
                    
                    UpdateBatchInfo(curBatchNo, "40", "�Զ�����,ԭ�����ϸ��Ϣ","��¼��־��,��" + str(iline) + '��'+",�˺�Ϊ:"+linebuf[22:45].lstrip().rstrip())
                    procFlag = 1
                    linebuf = bfp.readline()
                    continue
                    #end


                #���ļ��ж�ȡһ��
                linebuf = bfp.readline()

            #�ر��ļ�
            bfp.close()
            
            #begin  �ر��  20090330 
            if (procFlag == 1):
                return ExitThisFlow( "9000", "�Զ�����,ԭ����д����ϸ�����ļ�")
            #end

            #ת��
            ls_totalnum = (long)(s_totalnum)
            lm_totalnum = (long)(m_totalnum)

            ls_totalamt = (long)(((float)(s_totalamt)) * 100 + 0.1)
            lm_totalamt = m_totalamt

            WrtLog('>>>�������=%d ������=%d ��ϸ����=%d ��ϸ���=%d' % (ls_totalnum, ls_totalamt, lm_totalnum, lm_totalamt))

            #�ж��ܱ���,�ܽ��
            if ( (ls_totalnum!=lm_totalnum) or (ls_totalamt!=lm_totalamt) ):
                UpdateBatchInfo(curBatchNo, "40", "�Զ�����:�����ļ��ܱ������ܽ��������Ĳ���")
                return ExitThisFlow("9000", "�Զ�����,�����ļ��ܱ������ܽ��������Ĳ���")


            UpdateBatchInfo(curBatchNo, "11", "����У��ɹ�->����������")
            
            #################################################################
            #20090927 ����������  ��ʱ������Ҫ���������������
            #----------------------------------------------------------------
            if ( TradeContext.NOTE3 == '0' ):
                UpdateBatchInfo( curBatchNo, "21", "��ʱ����->���ύ" )
                return ExitThisFlow( "0000", "��ʱ����->���ύ" )
            #################################################################
                
            return ExitThisFlow("0000", "����У��ɹ�->����������")


        else:
            UpdateBatchInfo(curBatchNo, "40", "�Զ�����,�������������ļ�������:�ļ���=" + bFileName)
            return ExitThisFlow("9000", "�Զ�����,�������������ļ�������:�ļ���=" + bFileName)


    except Exception, e:
        bfp.close()
        WrtLog( str(e) )
        UpdateBatchInfo(curBatchNo, "40", "���봦��(VMENU)�쳣(���������ļ�)")
        return ExitThisFlow( '9999', '���봦��(VMENU)�쳣')





######################################################################################################################
#�����������ύ����
######################################################################################################################
def TJ_Proc(curBatchNo):


    WrtLog('>>>�ύ����(TJ_Proc)')


    try:
        if TradeContext.existVariable('NOTE1'):
            if TradeContext.NOTE1=='1':
                return ExitThisFlow( '9000', '�������ɱ�Ľ������������ύ,�����ύ������')


        #�޸�����״̬Ϊ�����ύ
        UpdateBatchInfoTJ(curBatchNo, "1")

        sFileName   = curBatchNo + '_1'
        dFileName   = curBatchNo + '_2'
        lFileName   = curBatchNo + '_2'
        rFileName   = 'A' + curBatchNo[8:16] + '1'


        #�������������ļ�
        if not CrtBatchFile(curBatchNo) :
            UpdateBatchInfoTJ(curBatchNo, "0")
            return ExitThisFlow( '9000', '�����ύ�ļ�ʧ��')


        WrtLog('>>>�����ύ�ļ�['+ sFileName  +']')


        #ASC->BCD
        if not FormatFile("1", sFileName, dFileName):
            UpdateBatchInfoTJ(curBatchNo, "0")
            UpdateBatchInfo(curBatchNo, "40", "�Զ�����,��ʽ���ļ�ʧ��")
            return ExitThisFlow( '9000', '�Զ�����,��ʽ���ļ�ʧ��')


        WrtLog('>>>���������ļ�['+ dFileName  +']')


        if not ftpfile(0, lFileName, rFileName):
            UpdateBatchInfoTJ(curBatchNo, "0")
            return ExitThisFlow( '9000', '�ύ����FTPʧ��')


        WrtLog('>>>�ϴ������ļ�['+ rFileName  +']')


        #�޸��ύʱ��
        if not UpdateBatchDate(curBatchNo,TradeContext.WorkDate,TradeContext.WorkTime) :
            UpdateBatchInfoTJ(curBatchNo, "0")
            return ExitThisFlow( '9000', '�޸��ύʱ��ʧ��')


        WrtLog('>>>�޸��ύʱ��['+ TradeContext.WorkDate + ':' + TradeContext.WorkTime  +']')


        #֪ͨ��������������ҵ
        ret = SendToHost(curBatchNo)
        if ( ret < 0 ):
            UpdateBatchInfoTJ(curBatchNo, "0")
            return ExitThisFlow( '9000', '�ύ����֪ͨʧ��')
        
        #20091103  ������  ���ӵ����ռ���������
        if( TradeContext.NOTE3 == '0'):
            #֪ͨ���������ռ�����������ҵ    
            ret = CallHost(curBatchNo)
            #if ( ret < 0 ):
            #    UpdateBatchInfoTJ(curBatchNo, "0")
            #    return ExitThisFlow( '9000', '�ռ���������ʧ��')


        UpdateBatchInfoTJ(curBatchNo, "0")


        UpdateBatchInfo(curBatchNo, "22", "�ύ����ɹ�->���ύ")


        WrtLog('>>>״̬���ύ����ɹ�->���ύ[״̬:21->22]')

        return True


    except Exception, e:
        WrtLog( str(e) )
        UpdateBatchInfoTJ(curBatchNo, "0")
        return ExitThisFlow( '9999', '�ύ�����쳣')


######################################################################################################################
#�����������������ɽ���ļ�
######################################################################################################################
def SC_Proc(curBatchNo):


    WrtLog('>>>�������ɽ���ļ�(SC_Proc)')


    try:
        ret = RecvResultFile(curBatchNo)
        if ( ret < 0 ):
            return ExitThisFlow( '9000', '���������������ļ�ʧ��')


        if ( ret == 0 ):
            sql = ""
            sql = "UPDATE ABDT_BATCHINFO SET "
#           sql = sql + "TOTALNUM=" +  "'" + HostContext.O1SUCN    + "',"         #ί���ܱ���
#           sql = sql + "TOTALAMT=" +  "'" + HostContext.O1SUCN    + "',"         #ί���ܽ��
            sql = sql + "SUCCNUM="  +  "'" + HostContext.O1SUCN    + "',"         #�ɹ��ܱ���
            sql = sql + "SUCCAMT="  +  "'" + HostContext.O1AMAO    + "',"         #�ɹ��ܽ��
            sql = sql + "FAILNUM="  +  "'" + HostContext.O1FACN    + "',"         #ʧ���ܱ���
            sql = sql + "FAILAMT="  +  "'" + HostContext.O1AMOT    + "'"          #ʧ���ܽ��

            sql = sql + " WHERE "

            sql = sql + "BATCHNO=" + "'" + curBatchNo    + "'"        #ί�к�

            WrtLog(sql)

            retcode = AfaDBFunc.UpdateSqlCmt( sql )
            if (retcode <= 0):
                return ExitThisFlow( '9000', '�޸����εĴ�������Ϣʧ��')


            UpdateBatchInfo(curBatchNo, "31", "�����Ѿ������ļ�->�������")

            WrtLog('>>>�����Ѿ������ļ�->�������')
                
            return True

        else:
            UpdateBatchInfo(curBatchNo, "30", "��������ɹ�->�����")

            WrtLog('>>>״̬����������ɹ�->�����')

            return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '������������ļ��쳣')




######################################################################################################################
#������������ѯ��������ļ��Ƿ��Ѿ�����
######################################################################################################################
def CX_Proc(curBatchNo):

    WrtLog('>>>��ѯ��������ļ��Ƿ��Ѿ�����(CX_Proc)')

    try:
        ret = ChkHostFile(curBatchNo)
        if ( ret < 0 ):
            return ExitThisFlow( '9000', '��ѯ��������ļ��Ƿ��Ѿ�����,ʧ��')

        if ( ret == 1):
            UpdateBatchInfo(curBatchNo, "22", "�ύ����ɹ�->���ύ(�ȴ���������...)")
            return ExitThisFlow( '9000', '�ύ����ɹ�->���ύ(�ȴ���������...)')


        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET "
#       sql = sql + "TOTALNUM=" +  "'" + HostContext.O1SUCN    + "',"         #ί���ܱ���
#       sql = sql + "TOTALAMT=" +  "'" + HostContext.O1SUCN    + "',"         #ί���ܽ��
        sql = sql + "SUCCNUM="  +  "'" + HostContext.O1SUCN    + "',"         #�ɹ��ܱ���
        sql = sql + "SUCCAMT="  +  "'" + HostContext.O1AMAO    + "',"         #�ɹ��ܽ��
        sql = sql + "FAILNUM="  +  "'" + HostContext.O1FACN    + "',"         #ʧ���ܱ���
        sql = sql + "FAILAMT="  +  "'" + HostContext.O1AMOT    + "'"          #ʧ���ܽ��

        sql = sql + " WHERE "

        sql = sql + "BATCHNO=" + "'" + curBatchNo    + "'"        #ί�к�

        WrtLog(sql)

        retcode = AfaDBFunc.UpdateSqlCmt( sql )
        if (retcode <= 0):
            return ExitThisFlow( '9000', '�޸����εĴ�������Ϣʧ��')

        UpdateBatchInfo(curBatchNo, "31", "�����Ѿ������ļ�->�������")

        WrtLog('>>>״̬�������Ѿ������ļ�->�������')

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '��ѯ����״̬�쳣')


######################################################################################################################
#������������ش���
######################################################################################################################
def TH_Proc(curBatchNo):


    WrtLog('>>>��ش���(TH_Proc)')


    try:
        #����(��������)
        lFileName = curBatchNo + '_3'

        #����
        rFileName = 'A' + curBatchNo[8:16] + '2'

        sFileName = curBatchNo + '_3'
        dFileName = curBatchNo + '_4'

        if not ftpfile(1, lFileName, rFileName) :
            return ExitThisFlow( '9000', '��ش���FTP(��ȡ)ʧ��[�����ļ�:'+ rFileName +']')


        WrtLog('>>>���������ļ�['+ sFileName  +']')


        #BCD->ASC
        if not FormatFile("2", sFileName, dFileName):
            return ExitThisFlow( '9000', '��ʽ�����������ļ�ʧ��[�����ļ�:'+ lFileName +']')


        WrtLog('>>>��������ļ�['+ dFileName  +']')

        UpdateBatchInfo(curBatchNo, "32", "��ش���ɹ�->�����")

        WrtLog('>>>״̬����ش���ɹ�->�����')

        return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '��ش����쳣')



######################################################################################################################
#�������������̴���
######################################################################################################################
def HP_Proc(curBatchNo):

    WrtLog('>>>���̴���(HP_Proc)')

    try:
        #���ɻ����ļ�
        
        #20120409 �º��޸����--AG07
        #if ( TradeContext.APPNO[0:4] == 'AG08' ):
        if ( TradeContext.APPNO[0:4] == 'AG08' or TradeContext.APPNO[0:4] == 'AG07'):
            #�������⴦��(�޸��ˣ����Һͣ��޸����ڣ�20080402)
            #��ѯ�ʽ����
            if not QueryZJDM() :
                return False

            if not CrtBusiFileCZ(curBatchNo):
                return False

        else:
            if not CrtBusiFile(curBatchNo):
                return False

        WrtLog('>>>���ɻ����ļ��ɹ�')

        #���ɱ����ļ�
        if not CrtBankFile(curBatchNo) :
            return False

        WrtLog('>>>����ҵ�񱨱�ɹ�')

        UpdateBatchInfo(curBatchNo, "88", "�����δ����Ѿ�����")
            
        return True


    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '���̴����쳣')



















#############################################################################################################
#  �����������⴦�������޸���:XZH   �޸�����:20080402
#############################################################################################################

#��ѯ�ʽ����
def QueryZJDM():

    WrtLog('>>>��ѯ�ʽ����(QueryZJDM)')

    try:
        sql = "SELECT CZZJDM,ZJDMMC,NOTE1,NOTE2 FROM ABDT_CZDZB WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.APPNO  + "'"        #ҵ����

        WrtLog(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            return ExitThisFlow( '9000', '�ʽ������Ϣʧ��')

        if ( len(records) == 0 ):
            return ExitThisFlow( '9000', 'û���ʽ������Ϣ')

        else:
            TradeContext.CZZJDM  = str(records[0][0]).strip()           #�ʽ����
            TradeContext.CZZJDMMC= str(records[0][1]).strip()           #��λ����
            TradeContext.CZNOTE1 = str(records[0][2]).strip()           #��ע1
            TradeContext.CZNOTE2 = str(records[0][3]).strip()           #��ע2
            return True

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', '��ѯ�ʽ�����쳣')



#������λ�����ļ�
def CrtBusiFileCZ(curBatchNo):

    WrtLog('>>>������λ�����ļ�(CrtBusiFileCZ)')

    try:
        #���������ļ�
        rHostFile= os.environ['AFAP_HOME'] + '/data/batch/host/' +  curBatchNo + '_4'
        WrtLog(rHostFile)

        #�缶�����ļ�
        
        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        rBusiFile= os.environ['AFAP_HOME'] + '/data/batch/down/' +  TradeContext.CZZJDM + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + '.RET'
        #end
        
        WrtLog(rBusiFile)

        #ʡ�������ļ�
        
        #begin
        #20091102  ������  ����ͬһ����һ����Դ���ʣ�Ϊ�����ļ������ǣ��޸��ļ��������ڻ����ź���������κţ�NOTE2��
        qBusiFile= os.environ['AFAP_HOME'] + '/data/batch/down/' +  TradeContext.CZZJDM + TradeContext.BUSINO + TradeContext.NOTE2 + '_' + TradeContext.INDATE + '.TXT'
        #end
        
        WrtLog(qBusiFile)

        #�����������ļ�
        chFp = open(rHostFile, "r")
            
        #������ҵ�����ļ�
        cbFp = open(rBusiFile, "w")
        cqFp = open(qBusiFile, "w")

        #д��������
        wbuffer = ''
        wbuffer = wbuffer + TradeContext.TOTALNUM + '|'                   #�ܱ���
        wbuffer = wbuffer + TradeContext.TOTALAMT + '|'                   #�ܽ��
        wbuffer = wbuffer + TradeContext.SUCCNUM  + '|'                   #�ɹ�����
        wbuffer = wbuffer + TradeContext.SUCCAMT  + '|'                   #�ɹ����
        wbuffer = wbuffer + TradeContext.FAILNUM  + '|'                   #ʧ�ܱ���
        wbuffer = wbuffer + TradeContext.FAILAMT  + '|'                   #ʧ�ܽ��
        wbuffer = wbuffer + '\n'

        WrtLog("================0=====================")
        
        cbFp.write(wbuffer)
        
        WrtLog("================1=====================")
        
        cqFp.write(wbuffer)
        
        WrtLog("================2=====================")
            
        #WrtLog(wbuffer)
        
        WrtLog("================3=====================")

        #��ȡһ��
        linebuf = chFp.readline()

        WrtLog("================5=====================")

        while ( len(linebuf) > 0 ):

            if ( len(linebuf) < 994 ):
                chFp.close()
                cbFp.close()
                cqFp.close()
                return ExitThisFlow( '9000', '�����������ļ���ʽ����,����')

            swapbuf = linebuf[0:994].split('<fld>')
            #WrtLog(linebuf)
            #д����ϸ��Ϣ
            wbuffer = ''
            wbuffer = swapbuf[25].strip() + TradeContext.CZZJDM + '|'       #�ͻ���ʶ            
            if ( TradeContext.AGENTTYPE == '3' ):
                wbuffer = wbuffer + swapbuf[14].strip() + '|'               #�����ʺ�
                wbuffer = wbuffer + swapbuf[15].strip() + '|'               #�ͻ�����
            else:
                wbuffer = wbuffer + swapbuf[20].strip() + '|'               #�����ʺ�
                wbuffer = wbuffer + swapbuf[21].strip() + '|'               #�ͻ�����

            wbuffer = wbuffer + swapbuf[28].strip()     + '|'               #���
            tmp_retcode = swapbuf[5].strip()
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                #�ɹ�
                wbuffer = wbuffer + swapbuf[3].strip()      + '|'           #��������
                tmp_retcode = '0'
            else:
                #ʧ��
                wbuffer = wbuffer +                          '|'           #��������(ʧ��,��Ϊ��)
                tmp_retcode = '1'

            #WrtLog("================6=====================")

            #ʡ�������ļ�
            cqFp.write(wbuffer + '\n')

            #WrtLog("================7=====================")

            wbuffer = wbuffer + tmp_retcode             + '|'               #��־(������)
            tmp_retcode = swapbuf[5].strip()
            if ( (len(tmp_retcode)==0) or (tmp_retcode=="AAAAAAA") ):
                #�ɹ�
                tmp_retcode = '�����ɹ�'
            wbuffer = wbuffer + tmp_retcode             + '|'               #������Ϣ
            wbuffer = wbuffer + '\n'

            #WrtLog("================8=====================")
                
            #�缶�����ļ�
            cbFp.write(wbuffer)
            
            #WrtLog("================9=====================")
            
            #��ȡ���������ļ�����һ��
            linebuf = chFp.readline()

            #WrtLog("================A=====================")
                
        chFp.close()

        WrtLog("================B=====================")

        cbFp.close()

        WrtLog("================C=====================")

        cqFp.close()
            
        WrtLog("================D=====================")
            
        return True

    except Exception, e:
        WrtLog( str(e) )

        WrtLog("================E=====================")
            
        chFp.close()
        
        WrtLog("================F=====================")
        
        cbFp.close()
        
        WrtLog("================G=====================")
        
        cqFp.close()
            
        WrtLog("================H=====================")
            
        return ExitThisFlow( '9999', '������λ�����ļ��쳣')
        

#�ر��  20090330  ɾ����ϸ������Ϣ�ļ�
def DelProcmsgFile(pBatchNo):
    
    WrtLog('>>>ɾ����ϸ������Ϣ�ļ�')

    try:
        procmsgFile = os.environ['AFAP_HOME'] + '/data/batch/procmsg/abdt_procmsg' + pBatchNo + ".txt"

        if ( os.path.exists(procmsgFile) and os.path.isfile(procmsgFile) ):
            cmdstr = "rm " + procmsgFile
            WrtLog('>>>ɾ������:' + cmdstr)
            os.system(cmdstr)
            return True
            
        else:
            WrtLog('��ϸ������Ϣ�ļ�[abdt_procmsg' + pBatchNo + '.txt]������')

    except Exception, e:
        WrtLog( str(e) )
        return ExitThisFlow( '9999', 'ɾ����ϸ������Ϣ�ļ��쳣')
