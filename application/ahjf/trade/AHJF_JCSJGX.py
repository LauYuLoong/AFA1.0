# -*- coding: gbk -*-
###############################################################################
# ժ    Ҫ�����ս���������������
# ��ǰ�汾��1.0
# ��    �ߣ�CYG
# ������ڣ�2011��01��21��
###############################################################################
import TradeContext
TradeContext.sysType = 'ahjf'
import ConfigParser, AfaUtilTools, AfaLoggerFunc, sys, AfaDBFunc
import os,ftplib,ConfigParser
from types import *

#��ȡ�����ļ�����Ϣ
def GetConfig( Node,CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOSTIP   =   config.get(Node, 'HOSTIP')
        TradeContext.HOSTPORT =   config.get(Node, 'HOSTPORT')
        TradeContext.USERNO   =   config.get(Node, 'USERNO')
        TradeContext.PASSWD   =   config.get(Node, 'PASSWD')
        TradeContext.RDIR     =   config.get(Node, 'RDIR')
        TradeContext.LDIR     =   config.get(Node, 'LDIR')
        
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
        
#���շ�˰���ػ�������-�Ӳ�������
def GetFile(RemoteFileName,LocalFileName):

    try:
        #����Ĭ�ϳ�ʱʱ��
        #socket.setdefaulttimeout(15)
        #����FTPʵ��
        ftp_p = ftplib.FTP()
        #����FTP
        ftp_p.connect(TradeContext.HOSTIP,TradeContext.HOSTPORT)
        #��½FTP
        ftp_p.login(TradeContext.USERNO,TradeContext.PASSWD)
        #�ƶ���Զ��FTP������ָ��Ŀ¼
        ftp_p.cwd(TradeContext.RDIR)
        #��д�뷽ʽ�򿪱����ļ�
        file_handler = open(TradeContext.LDIR + "/" + LocalFileName,'wb')
        #��ȡָ�������ļ�����,��д�뵽�����ļ�
        ftp_p.retrbinary("RETR " + TradeContext.RDIR + "/" + RemoteFileName,file_handler.write)
        #�رձ����ļ�
        file_handler.close()
        #�˳�FTP
        ftp_p.quit()

        #�жϱ����ļ��Ƿ�����,��δ����,���׳��쳣
        if not os.path.exists(TradeContext.LDIR + "/" + LocalFileName):
            AfaLoggerFunc.tradeInfo("�ļ�[" + TradeContext.LDIR + "/" + LocalFileName + "]����ʧ��")
            return False
        AfaLoggerFunc.tradeInfo("�ļ�[" + TradeContext.LDIR + "/" + LocalFileName + "]���سɹ�")

        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo('FTP�����쳣:' + str(e))
        return False

def UpdateData( file ):

    AfaLoggerFunc.tradeInfo( '�ļ�������ʼ' )
    
    try:
        sfp = open(TradeContext.LDIR + "/" + file,"r")
        #��ȡһ��
        linebuff = sfp.readline( )
        
        if file[0:9] == "JGDATADOC":
            #��ȡ����/�ɼ����ش����ļ�
            while( len(linebuff)>0 ):
                swapbuff = linebuff.split(chr(05))
                TradeContext.OFFICECODE    = swapbuff[0].lstrip().rstrip()          #�ɼ����ش���
                TradeContext.OFFICENAME    = swapbuff[1].lstrip().rstrip()          #�ɼ���������
                #�Ǽǻ�������
                upDate_ahjf_officecode( )
                
                linebuff = sfp.readline( )
        else:
            #��ȡ��ͨΥ�������ļ�
            while( len(linebuff)>0 ):
                swapbuff = linebuff.split(chr(05))
                TradeContext.OFFICECODE    = swapbuff[0].lstrip().rstrip()          #�ɼ����ش���
                TradeContext.LAWACTIONCODE = swapbuff[1].lstrip().rstrip()          #Υ����Ϊ����
                TradeContext.DESCRIBE      = swapbuff[2].lstrip().rstrip()          #Υ����Ϊ����
                TradeContext.MR_AMOUNT     = swapbuff[3].lstrip().rstrip()          #Ĭ�Ϸ�����
                TradeContext.LOWER_AMOUNT  = swapbuff[4].lstrip().rstrip()          #����������
                TradeContext.TOP_AMOUNT    = swapbuff[5].lstrip().rstrip()          #����������
                #�Ǽǻ�������
                upDate_ahjf_lawcode( )
                
                linebuff = sfp.readline( )
            
        sfp.close( )
        return True
    except Exception, e:
        sfp.close()
        return False
        
def upDate_ahjf_officecode( ):
    try:
        selectSql = "select * from ahjf_officecode "
        whereSql  = " where  OFFICECODE='" + TradeContext.OFFICECODE    + "'"
        
        selectSql = selectSql + whereSql
        AfaLoggerFunc.tradeInfo( '�������ݲ�ѯsql��' + selectSql)
        selectRecord = AfaDBFunc.SelectSql( selectSql )
        
        if selectRecord == None:
            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
            return False
        if len(selectRecord) > 0:
            AfaLoggerFunc.tradeInfo('>>>�����Ѵ��ڣ������²���')
            
            updateSql = "update ahjf_officecode set "
            updateSql = updateSql + "OFFICENAME     ='" + TradeContext.OFFICENAME     + "'"
        
            updateSql = updateSql + whereSql
            AfaLoggerFunc.tradeInfo( '�������ݸ���sql��' + updateSql)
            updateRecord = AfaDBFunc.UpdateSqlCmt( updateSql )
            if updateRecord <  0:
                AfaLoggerFunc.tradeInfo( "���»�������ʧ��" )
                return False
        else:
            AfaLoggerFunc.tradeInfo('>>>���ݲ����ڣ��Ǽ��µ�����')
            
            insertSql = "insert into ahjf_officecode(OFFICECODE,OFFICENAME,NOTE1,NOTE2) values("
            insertSql = insertSql + "'" + TradeContext.OFFICECODE    + "',"      #�ɼ����ش���
            insertSql = insertSql + "'" + TradeContext.OFFICENAME + "',"         #�ɼ���������
            insertSql = insertSql + "'',"                                        #����1
            insertSql = insertSql + "'')"                                        #����2
            
            AfaLoggerFunc.tradeInfo( '�������ݵǼ�sql��' + insertSql)
            insertRecord = AfaDBFunc.InsertSqlCmt( insertSql )
            
            if insertRecord < 0:
                AfaLoggerFunc.tradeInfo( '>>>�Ǽǻ�����������ʧ������ʧ��' )
                return False
            return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return False
        
def upDate_ahjf_lawcode( ):
    try:
        selectSql = "select * from ahjf_lawcode "
        whereSql  = " where  OFFICECODE='" + TradeContext.OFFICECODE    + "'"
        whereSql  = whereSql + " and LAWACTIONCODE='" + TradeContext.LAWACTIONCODE + "'"
        
        selectSql = selectSql + whereSql
        AfaLoggerFunc.tradeInfo( '�������ݲ�ѯsql��' + selectSql)
        selectRecord = AfaDBFunc.SelectSql( selectSql )
        
        if selectRecord == None:
            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
            return False
        if len(selectRecord) > 0:
            AfaLoggerFunc.tradeInfo('>>>�����Ѵ��ڣ������²���')
            
            updateSql = "update ahjf_lawcode set "
            updateSql = updateSql + "DESCRIBE     ='" + TradeContext.DESCRIBE     + "',"
            updateSql = updateSql + "MR_AMOUNT    ='" + TradeContext.MR_AMOUNT    + "',"
            updateSql = updateSql + "LOWER_AMOUNT ='" + TradeContext.LOWER_AMOUNT + "',"
            updateSql = updateSql + "TOP_AMOUNT   ='" + TradeContext.TOP_AMOUNT   + "'"
            
            updateSql = updateSql + whereSql
            AfaLoggerFunc.tradeInfo( '�������ݸ���sql��' + updateSql)
            updateRecord = AfaDBFunc.UpdateSqlCmt( updateSql )
            if updateRecord <  0:
                AfaLoggerFunc.tradeInfo( "���»�������ʧ��" )
                return False
        else:
            AfaLoggerFunc.tradeInfo('>>>���ݲ����ڣ��Ǽ��µ�����')
            
            insertSql = "insert into ahjf_lawcode(OFFICECODE,LAWACTIONCODE,DESCRIBE,MR_AMOUNT,LOWER_AMOUNT,TOP_AMOUNT,note1,note2,note3,note4) values("
            insertSql = insertSql + "'" + TradeContext.OFFICECODE    + "',"      #�ɼ����ش��� 
            insertSql = insertSql + "'" + TradeContext.LAWACTIONCODE + "',"      #Υ����Ϊ���� 
            insertSql = insertSql + "'" + TradeContext.DESCRIBE      + "',"      #Υ����Ϊ���� 
            insertSql = insertSql + "'" + TradeContext.MR_AMOUNT     + "',"      #Ĭ�Ϸ����� 
            insertSql = insertSql + "'" + TradeContext.LOWER_AMOUNT  + "',"      #���������� 
            insertSql = insertSql + "'" + TradeContext.TOP_AMOUNT    + "',"      #���������� 
            insertSql = insertSql + "'',"                                        #����1
            insertSql = insertSql + "'',"                                        #����2
            insertSql = insertSql + "'',"                                        #����3
            insertSql = insertSql + "'')"                                        #����4
            
            AfaLoggerFunc.tradeInfo( '�������ݵǼ�sql��' + insertSql)
            insertRecord = AfaDBFunc.InsertSqlCmt( insertSql )
            
            if insertRecord < 0:
                AfaLoggerFunc.tradeInfo( '>>>�Ǽǻ�����������ʧ������ʧ��' )
                return False
            return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return False

if __name__ == '__main__':

    AfaLoggerFunc.tradeInfo('******���ս���ÿ�ջ������ݸ��¿�ʼ******')
    
    TradeContext.workDate = AfaUtilTools.GetSysDate( )
    
    #��ȡ�����ļ���Ϣ
    GetConfig( 'AG2017_AHJF_DZ' )
    
    files = ["JGDATADOC_012_" + TradeContext.workDate + ".TXT","DATADOC_012_" + TradeContext.workDate + ".TXT"]
    
    #���������ػ��������ļ�
    for file in files:
        if GetFile( file,file ):
            AfaLoggerFunc.tradeInfo( ">>>" + file + '�ļ���������Ҫ����')
            UpdateData( file )
    
    AfaLoggerFunc.tradeInfo('******���ս���ÿ�ջ������ݸ��½���******')
