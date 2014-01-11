# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AhXnbFunc.py
# ժ    Ҫ������ʡ��ũ������ҵ�񹫹���
# ��ǰ�汾��1.0
# ��    �ߣ�������
# ������ڣ�2010��12��15��
###############################################################################
import TradeContext,AfaUtilTools,AfaDBFunc,ConfigParser,os,AfaLoggerFunc
from types import *
#sys,time,

#=====================�жϵ�λЭ���Ƿ���Ч=====================
def ChkUnitInfo( ):

    AfaLoggerFunc.tradeInfo('>>>�жϵ�λЭ���Ƿ���Ч')

    try:
        sql = ""
        sql = "SELECT SIGNUPMODE,GETUSERNOMODE,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO,AGENTTYPE,VOUHNO FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "        #ҵ����
        sql = sql + "BUSINO=" + "'" + TradeContext.I1BUSINO + "'" + " AND "        #��λ���
        sql = sql + "STATUS=" + "'" + "1"                   + "'"                  #״̬

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ��λЭ����Ϣ�쳣' )
        if ( len(records) <= 0 ):
            return ExitSubTrade( '9000', 'û�е�λЭ����Ϣ,���ܽ��д������')

        #����None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.SIGNUPMODE    = str(records[0][0])                             #ǩԼ��ʽ
        TradeContext.GETUSERNOMODE = str(records[0][1])                             #�̻��ͻ���Ż�ȡ��ʽ
        TradeContext.STARTDATE     = str(records[0][2])                             #��Ч����
        TradeContext.ENDDATE       = str(records[0][3])                             #ʧЧ����
        TradeContext.STARTTIME     = str(records[0][4])                             #����ʼʱ��
        TradeContext.ENDTIME       = str(records[0][5])                             #������ֹʱ��
        TradeContext.ACCNO         = str(records[0][6])                             #�Թ��˻�
        TradeContext.AGENTTYPE     = str(records[0][7])                             #ί�з�ʽ
        TradeContext.VOUHNO        = str(records[0][8])                             #ƾ֤��(�ڲ��ʻ�)

        AfaLoggerFunc.tradeInfo( "WorkDate=[" + TradeContext.WorkDate + "]" )

        if ( (TradeContext.STARTDATE > TradeContext.WorkDate) or (TradeContext.WorkDate > TradeContext.ENDDATE) ):
            return ExitSubTrade( '9000', '�õ�λί��Э�黹û����Ч���ѹ���Ч��')

        if ( (TradeContext.STARTTIME > TradeContext.WorkTime) or (TradeContext.WorkTime > TradeContext.ENDTIME) ):
            return ExitSubTrade( '9000', '�Ѿ�������ϵͳ�ķ���ʱ��,��ҵ�������[' + s_StartDate + ']-[' + s_EndDate + ']ʱ�������')

        if ((TradeContext.SIGNUPMODE=="1") and (TradeContext.GETUSERNOMODE=="1")):
            #���͵�ͨѶǰ�ò��ӵ�������ȡЭ��
            return True

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�жϵ�λЭ����Ϣ�Ƿ����ʧ��')
        
        
#=====================�׳�����ӡ��ʾ��Ϣ=====================
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg
        AfaLoggerFunc.tradeInfo( errorMsg )
    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True
    else:
        return False
        
        
#=====================����ahnx_file���е�״̬=====================
def UpdateFileStatus(BatchNo, Status, ProcMsg, workTime):
    
    AfaLoggerFunc.tradeInfo( '����ahnx_file��BATCHNO=' + BatchNo + ' ' + Status + ' ' + workTime)

    try:
        sql = "UPDATE AHNX_FILE SET "
        sql = sql + " STATUS  ='" + Status   + "',"       #״̬
        sql = sql + " PROCMSG ='" + ProcMsg  + "',"       #������Ϣ����
        sql = sql + " WORKTIME='" + workTime + "'"        #����ʱ��
        sql = sql + " WHERE"
        sql = sql + " BATCHNO ='" + BatchNo  + "'"        #ί�к�
        
        AfaLoggerFunc.tradeInfo( '����ahnx_file����״̬sql��' + sql )
        
        result = AfaDBFunc.UpdateSqlCmt( sql )
        if (result <= 0):
            return ExitSubTrade( 'D001', '����ahnx_file��ʧ��')
            
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade( '9999', '����ahnx_file���쳣')
        

#=====================��ȡ������Ϣ=====================
def getBatchFile( ConfigNode ):
    try:
        #��ȡFTP�����ļ�
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        
        config.readfp( open( configFileName ) )
        
        TradeContext.ABDT_PDIR    = config.get(ConfigNode,'ABDT_BDIR')     #�����ϴ��ļ����·��
        TradeContext.ABDT_GDIR    = config.get(ConfigNode,'ABDT_GDIR')     #���������ļ����·��
        TradeContext.XNB_BSDIR    = config.get(ConfigNode,'XNB_BSDIR')     #��ũ��ת��ǰ��·��
        TradeContext.XNB_BDDIR    = config.get(ConfigNode,'XNB_BDDIR')     #��ũ��ת�����·��
        
        
        return True
        
    except Exception, e:
        return ExitSubTrade( 'E0001', "��ȡ�����ļ��쳣��" + str(e))


#====================������Ϣд���ļ�=================
def UpdateBatchInfo(pBatchNo, pStatus, pMessage,pInfo=0):
    AfaLoggerFunc.tradeInfo('>>>�޸�����״̬:[' + pStatus + ']' + pMessage)

    try:
        #-----1,��������Ϣ���µ�ahxnb_file���PROCMSG��
        sql = ""
        sql = "UPDATE AHNX_FILE SET "
        sql = sql + "STATUS="   +  "'" + pStatus     + "',"     #״̬
        sql = sql + "PROCMSG="  +  "'" + pMessage    + "'"      #ԭ��
        sql = sql + " WHERE BATCHNO = '" + pBatchNo  + "'"      #ί�к�"

        AfaLoggerFunc.tradeInfo(sql)
        result = AfaDBFunc.UpdateSqlCmt( sql )
        
        if ( result <= 0 ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '�޸����ε�״̬ʧ��')
            
        #-----1.1,����ǩԼ�Ĵ�����Ϣ�ļ���Ϊ�ϴ��ļ���
        sql = ""
        sql = sql + "select FILETYPE,FILENAME from AHNX_FILE"
        sql = sql + " where BATCHNO = '"+ pBatchNo +"'"
        
        AfaLoggerFunc.tradeInfo(sql)
        record = AfaDBFunc.SelectSql( sql )
        
        if record==None:
            return ExitSubTrade("D0001" ,"��ѯAHNX_FILEʧ��")
        elif(len(record) == 0):
            return ExitSubTrade("D0001" ,"�޴���Ϣ")
        else:
            TradeContext.procFileType = record[0][0].strip()
            TradeContext.procFileName = record[0][1].strip()
        
        if( TradeContext.procFileType == '4' ):     #����ǩԼ
            if pInfo:
                path_procmsg = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + TradeContext.procFileName
                fp_procmsg = open(path_procmsg,"a")
                fp_procmsg.write(pInfo + "\n")
                fp_procmsg.close()
            
        else:
            #-----2,�Ѵ�����Ϣд�뵽�����ļ���
            if pInfo:
                path_procmsg = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + pBatchNo + '.TXT'
                fp_procmsg = open(path_procmsg,"a")
                fp_procmsg.write(pInfo + "\n")
                fp_procmsg.close()

        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade( '9999', '�޸����ε�״̬�쳣')
        

#=========================ɾ����ϸ������Ϣ�ļ�=========================
def DelProcmsgFile(pBatchNo):
    AfaLoggerFunc.tradeInfo('>>>ɾ����ϸ������Ϣ�ļ�')

    try:
        #-----1.1,����ǩԼ�Ĵ�����Ϣ�ļ���Ϊ�ϴ��ļ���
        sql = ""
        sql = sql + "select FILETYPE,FILENAME from AHNX_FILE"
        sql = sql + " where BATCHNO = '"+ pBatchNo +"'"
        
        AfaLoggerFunc.tradeInfo(sql)
        record = AfaDBFunc.SelectSql( sql )
        
        if record==None:
            return ExitSubTrade("D0001" ,"��ѯAHNX_FILEʧ��")
        elif(len(record) == 0):
            if( pBatchNo[0:6] == 'YHKHFS' ):
                procmsgFile = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + pBatchNo + '.TXT'
                if ( os.path.exists(procmsgFile) and os.path.isfile(procmsgFile) ):
                    cmdstr = "rm " + procmsgFile
                    AfaLoggerFunc.tradeInfo('>>>ɾ������:' + cmdstr)
                    os.system(cmdstr)
                    return True
                    
                else:
                    AfaLoggerFunc.tradeInfo('��ϸ������Ϣ�ļ�[AHXNB_PROCMSG' + pBatchNo + '.TXT],������')
                    return True
                    
            return ExitSubTrade("D0001" ,"�޴���Ϣ")
        else:
            TradeContext.procFileType = record[0][0].strip()
            TradeContext.procFileName = record[0][1].strip()
        
        if( TradeContext.procFileType == '4' ):     #����ǩԼ
            procmsgFile = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + TradeContext.procFileName
            
            if ( os.path.exists(procmsgFile) and os.path.isfile(procmsgFile) ):
                cmdstr = "rm " + procmsgFile
                AfaLoggerFunc.tradeInfo('>>>ɾ������:' + cmdstr)
                os.system(cmdstr)
                return True
                
            else:
                AfaLoggerFunc.tradeInfo('��ϸ������Ϣ�ļ�[AHXNB_PROCMSG' + TradeContext.procFileName + '],������')
                return True
        
        else:
            procmsgFile = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + pBatchNo + '.TXT'
            
            if ( os.path.exists(procmsgFile) and os.path.isfile(procmsgFile) ):
                cmdstr = "rm " + procmsgFile
                AfaLoggerFunc.tradeInfo('>>>ɾ������:' + cmdstr)
                os.system(cmdstr)
                return True
                
            else:
                AfaLoggerFunc.tradeInfo('��ϸ������Ϣ�ļ�[AHXNB_PROCMSG' + pBatchNo + '.TXT')
                return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade( '9999', 'ɾ����ϸ������Ϣ�ļ��쳣')

#====================����������Ϣд���ļ�=================
def WriteInfo(FileName,Info):
    try:
        path_procmsg = os.environ['AFAP_HOME'] + '/data/ahxnb/procmsg/AHXNB_PROCMSG' + FileName + '.TXT'
        fp_procmsg = open(path_procmsg,"a")
        fp_procmsg.write(Info + "\n")
        fp_procmsg.close()

        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade( '9999', '����������Ϣд���ļ��쳣')