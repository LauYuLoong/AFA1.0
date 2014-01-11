###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰���ػ�����Ϣ
#
# ��ǰ�汾��1.0
# ��    �ߣ�WJJ
# ������ڣ�2007��10��15��
###############################################################################
import TradeContext, ConfigParser, AfaUtilTools, AfaLoggerFunc, sys, AfaDBFunc, Party3Context
import os, HostContext, AfaLoggerFunc,ftplib,ConfigParser,socket

from types import *

TradeContext.sysType = 'cron'

#��ȡ����ftp������Ϣ
def GetFtpConfig( ):
    
    #---------------�����ݿ�����ȡ��Ϣ--------------
    sqlstr =   "select hostip,downuser,downpasswd,downldir,downrdir from fs_businoconf where busino='" + TradeContext.busiNo + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
        
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        AfaLoggerFunc.tradeInfo( "�������ݿ��쳣����λ����ftp������Ϣ����ϵ�Ƽ���Ա" )
        return False

    if( len( records)==0 ):
        AfaLoggerFunc.tradeInfo( "û�в��ҵ���λ������Ϣ����ϵ�Ƽ���Ա" )
        return False
        
    else:  
        TradeContext.CROP_HOSTIP   = records[0][0].strip()
        TradeContext.CROP_USERNO   = records[0][1].strip()
        TradeContext.CROP_PASSWD   = records[0][2].strip()
        TradeContext.CROP_LDIR     = records[0][3].strip()
        TradeContext.CROP_RDIR     = records[0][4].strip()
        
        AfaLoggerFunc.tradeInfo( "��ǰ��λ���룺%s" %TradeContext.busiNo )
        AfaLoggerFunc.tradeInfo( "��ǰ������ַ��%s" %TradeContext.CROP_HOSTIP )
        AfaLoggerFunc.tradeInfo( "�˻���%s"         %TradeContext.CROP_USERNO )
        AfaLoggerFunc.tradeInfo( "���룺%s"         %TradeContext.CROP_PASSWD )
        AfaLoggerFunc.tradeInfo( "����·����%s"     %TradeContext.CROP_LDIR )
        return True   




#��ȡ�����ļ�����Ϣ
def GetAfeConfig( CfgFileName = None ):

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

#���շ�˰���ػ�������-�Ӳ�������
def GetData(RemoteFileName,LocalFileName):
    
    ##======== START 20091110 by zhangheng ===============================================================
    try:
        HOSTIP    =  TradeContext.CROP_HOSTIP
        HOSTPORT  =  '21'
        USERNO    =  TradeContext.CROP_USERNO
        PASSWD    =  TradeContext.CROP_PASSWD
        LDIR      =  TradeContext.CROP_LDIR
        RDIR      =  TradeContext.CROP_RDIR
        
        #����Ĭ�ϳ�ʱʱ��
        #socket.setdefaulttimeout(15)
        #����FTPʵ��
        ftp_p = ftplib.FTP()
        #����FTP
        ftp_p.connect(HOSTIP,HOSTPORT)
        #��½FTP
        ftp_p.login(USERNO,PASSWD)
        #�ƶ���Զ��FTP������ָ��Ŀ¼
        ftp_p.cwd(RDIR)
        #��д�뷽ʽ�򿪱����ļ�
        file_handler = open(LDIR + "/" + LocalFileName,'wb')
        #��ȡָ�������ļ�����,��д�뵽�����ļ�
        ftp_p.retrbinary("RETR " + RDIR + "/" + RemoteFileName,file_handler.write)
        #�رձ����ļ�
        file_handler.close()
        #�˳�FTP
        ftp_p.quit()
        
        #�жϱ����ļ��Ƿ�����,��δ����,���׳��쳣
        if not os.path.exists(LDIR + "/" + LocalFileName):
            AfaLoggerFunc.tradeInfo("�ļ�[" + LDIR + "/" + LocalFileName + "]����ʧ��")
            return -1
        AfaLoggerFunc.tradeInfo("�ļ�[" + LDIR + "/" + LocalFileName + "]���سɹ�")
        
        return 0
    ##========= END ================================================================                   
    except Exception, e:
        AfaLoggerFunc.tradeInfo('FTP�����쳣')
        return -1
        
#��AFE���ػ�����Ϣ-�ļ���ʽ
def ftpfile( rfilename, lfilename):

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
        ftpFp.write('get ' + rfilename + ' ' + lfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        os.system(ftpcmd)

        return 0

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('FTP�����쳣')
        return -1          
                
def DataToDB(file,ibegin):
    AfaLoggerFunc.tradeInfo( 'table:'+file )    
    try :
        
        #���Ƚ����������ֶε�ӳ��,Ȼ�������ص������ж��������ں�ʱ���ֶ�
        map =   {"AA11":"AAA010,AAA011,AAA012, AAA014,AAZ001,BUSINO,DATE,TIME",\
                 "FA15":"AAA010,AFA050,AAZ006,AFA051,AFA052,AAZ007,AFA062,AAZ002,BUSINO,DATE,TIME",\
                 "FA16":"AFA050,AFA030,AAZ006,AAZ007,BUSINO,DATE,TIME",\
                 "FA13":"AFA030,AAZ006,AAZ007,AFA031,AFA032,AAZ002,AFA038,AFA039,AFA040,AFA041,AFA042,AFA020,BUSINO,DATE,TIME",\
                 "FA20":"AAA010,AFA090,AFA091,AFA092,AFA096,BUSINO,DATE,TIME",\
                 "FA21":"AFA090,AFA050,AFA030,AAZ006,AAZ007,BUSINO,DATE,TIME",\
                 "DPZ_GL":"FPZDM,FQSHM,FQZHM,FDWDM,FCZQHNM,BUSINO,DATE,TIME",\
                 "FA22":"AAA010,AFA106,AAZ006,AFA100,AFA101,AFA102,AFA103,BUSINO,DATE,TIME" }
                                      
        #���ļ��еļ�¼���뵽���ݿ���
        fileName    =   TradeContext.CROP_LDIR + "/" + file + '_' + TradeContext.busiNo + ".txt"
        
        print '====' + fileName
        
        if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
            fp      =   open(fileName,"rb")
        
            #�����е����ݶ�ȡ��sALl��
            sAll    =   fp.read()
            fp.close()
            #rec��ÿһ����¼
            AfaLoggerFunc.tradeInfo(ibegin)
            AfaLoggerFunc.tradeInfo(len(sAll.split(chr(12))))
            for i in range(ibegin,len(sAll.split(chr(12)))):
                AfaLoggerFunc.tradeInfo(i)
                AfaLoggerFunc.tradeInfo(sAll.split(chr(12))[i])
                rec = sAll.split(chr(12))[i]
                #print   rec + "\n"
                AfaLoggerFunc.tradeInfo(len(rec))
                if len(rec)>0:
                    if file=='AA11':
                        AfaLoggerFunc.tradeInfo('AA11')
                        AfaLoggerFunc.tradeInfo(rec.split(chr(31))[0])
                        AfaLoggerFunc.tradeInfo(rec.split(chr(31))[5])
                        sqlstr=''
                        sqlstr = "select count(*) from FS_AA11 where AAA010='" + rec.split(chr(31))[0] + "' and BUSINO='" + TradeContext.busiNo + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            print '>>>��ѯ���ݿ��쳣'
                            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣AA11')
                            return -1

                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '�ظ���¼,���´���' )

                            #�����¼����,������ɾ��,������
                            strStr_del = "DELETE FROM FS_AA11 where AAA010='" + rec.split(chr(31))[0] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            
                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>ɾ������ʧ��:' + AfaDBFunc.sqlErrMsg)
                                return -1

                            
                    elif file=='FA15':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_FA15 where AFA050='" + rec.split(chr(31))[1] + "' and AAZ006='" + rec.split(chr(31))[2] + "' and BUSINO='" + TradeContext.busiNo + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )
                            
                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            print '>>>��ѯ���ݿ��쳣'
                            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
                            return -1

                        if records[0][0]==1:
                            
                            AfaLoggerFunc.tradeInfo( '�ظ���¼,���´���' )

                            #�����¼����,������ɾ��,������
                            strStr_del = "DELETE FROM FS_FA15 where AFA050='" + rec.split(chr(31))[1] + "' and AAZ006='" + rec.split(chr(31))[2] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            
                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>ɾ������ʧ��:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    elif file=='FA16':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_FA16 where AFA050='" + rec.split(chr(31))[0] + "' and AFA030='" + rec.split(chr(31))[1] + "'and AAZ006='" + rec.split(chr(31))[2] + "' and BUSINO='" + TradeContext.busiNo + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
                            return -1
                            
                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '�ظ���¼,���´���' )

                            #�����¼����,������ɾ��,������
                            strStr_del = "DELETE FROM FS_FA16 where AFA050='" + rec.split(chr(31))[0] + "' and AFA030='" + rec.split(chr(31))[1] + "'and AAZ006='" + rec.split(chr(31))[2] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            
                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>ɾ������ʧ��:' + AfaDBFunc.sqlErrMsg)
                                return -1


                    elif file=='FA13':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_FA13 where AFA030='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[1] + "' and BUSINO='" + TradeContext.busiNo + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
                            return -1
                            
                        if records[0][0]==1:
                            AfaLoggerFunc.tradeInfo( '�ظ���¼,���´���' )

                            #�����¼����,������ɾ��,������
                            strStr_del = "DELETE FROM FS_FA13 where AFA030='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[1] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            
                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>ɾ������ʧ��:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    elif file=='FA20':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_FA20 where AAA010='" + rec.split(chr(31))[0] + "' and AFA090='" + rec.split(chr(31))[1] + "' and BUSINO='" + TradeContext.busiNo + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
                            return -1
                            
                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '�ظ���¼,���´���' )

                            #�����¼����,������ɾ��,������
                            strStr_del = "DELETE FROM FS_FA20 where AAA010='" + rec.split(chr(31))[0] + "' and AFA090='" + rec.split(chr(31))[1] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            
                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>ɾ������ʧ��:' + AfaDBFunc.sqlErrMsg)
                                return -1
                                
                    elif file=='FA21':
                        sqlstr=''
                        #sqlstr = "select count(*) from FS_FA21 where AFA090='" + rec.split(chr(31))[0] + "' and AFA050='" + rec.split(chr(31))[1] + "'and AFA030='" + rec.split(chr(31))[2] + "'and AAZ006='" + rec.split(chr(31))[3] + "' and BUSINO='" + TradeContext.busiNo + "'"

                        sqlstr = "select count(*) from FS_FA21 where AFA090='" + rec.split(chr(31))[0] + "' and AFA050='" + rec.split(chr(31))[1] + "'and AFA030='" + rec.split(chr(31))[2] + "'and BUSINO='" + TradeContext.busiNo + "'"
                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
                            return -1
                            
                        if records[0][0]==1:
                        
                            AfaLoggerFunc.tradeInfo( '�ظ���¼,���´���' )

                            #�����¼����,������ɾ��,������
                            strStr_del = "DELETE FROM FS_FA21 where AFA090='" + rec.split(chr(31))[0] + "' and AFA050='" + rec.split(chr(31))[1] + "'and AFA030='" + rec.split(chr(31))[2] + "'and BUSINO='" + TradeContext.busiNo + "'"
                            
                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>ɾ������ʧ��:' + AfaDBFunc.sqlErrMsg)
                                return -1
                                
                    elif file=='DPZ_GL':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_DPZ_GL where FPZDM='" + rec.split(chr(31))[0] + "' and FQSHM='" + rec.split(chr(31))[1] + "'and FQZHM='" + rec.split(chr(31))[2] + "'and FDWDM='" + rec.split(chr(31))[3] + "'and FCZQHNM='" + rec.split(chr(31))[4].strip() + "' and BUSINO='" + TradeContext.busiNo + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
                            return -1
                        
                        if records[0][0]==1:
                        
                            AfaLoggerFunc.tradeInfo( '�ظ���¼,���´���' )

                            #�����¼����,������ɾ��,������
                            strStr_del = "DELETE FROM FS_DPZ_GL where FPZDM='" + rec.split(chr(31))[0] + "' and FQSHM='" + rec.split(chr(31))[1] + "'and FQZHM='" + rec.split(chr(31))[2] + "'and FDWDM='" + rec.split(chr(31))[3] + "'and FCZQHNM='" + rec.split(chr(31))[4].strip() + "' and BUSINO='" + TradeContext.busiNo + "'"

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>ɾ������ʧ��:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    elif file=='FA22':
                        sqlstr = ''
                        sqlstr = "select count(*) from FS_FA22 where AAA010='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[2] + "'and AFA100='" + rec.split(chr(31))[3] + "' and BUSINO='" + TradeContext.busiNo + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>��ѯ���ݿ��쳣')
                            return -1
                            
                        if records[0][0]==1:
                        
                            AfaLoggerFunc.tradeInfo( '�ظ���¼,���´���' )

                            #�����¼����,������ɾ��,������
                            strStr_del = "DELETE FROM FS_FA22 where AAA010='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[2] + "'and AFA100='" + rec.split(chr(31))[3] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            
                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>ɾ������ʧ��:' + AfaDBFunc.sqlErrMsg)
                                return -1
                    
                    sqlstr  =   ""
                    sqlstr  =   "insert into " + "FS_" + file + " (" + map[file] + " ) " + "  values ("
                    
                    for item in rec.split(chr(31)):
                        sqlstr  =  sqlstr   +   "'"
                        sqlstr  =  sqlstr   +   item.strip() + "',"
                        
                    sqlstr      =   sqlstr  + "'" + TradeContext.busiNo   + "',"
                    sqlstr      =   sqlstr  + "'" + TradeContext.WORKDATE + "',"
                    sqlstr      =   sqlstr  + "'" + TradeContext.WORKTIME + "')"
                    
                    AfaLoggerFunc.tradeInfo( sqlstr )

                    ret = AfaDBFunc.InsertSqlCmt( sqlstr )
                    if(  ret< 1 ):
                        AfaLoggerFunc.tradeInfo( "�����¼�쳣:" + AfaDBFunc.sqlErrMsg )
                        continue
                
        else:
            AfaLoggerFunc.tradeInfo( "�ļ�" + fileName + "������" )
                
        return 0
        
        
        
    except Exception, e:
        fp.close()  
        AfaLoggerFunc.tradeInfo( e )
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
    AfaLoggerFunc.tradeInfo('**********���շ�˰���ػ�����Ϣ��ʼ**********') 
    
    #��ʼ��TradeContext
    TradeContext.WORKDATE       =   AfaUtilTools.GetSysDate( )
    TradeContext.WORKTIME       =   AfaUtilTools.GetSysTime( )

    sqlstr  = "select distinct busino from abdt_unitinfo where appno='AG2008'and busino='34114639310002'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None:
        AfaLoggerFunc.tradeInfo("���ҵ�λ��Ϣ���쳣" + AfaDBFunc.sqlErrMsg)
        sys.exit(1)
    
    elif len(records)==0 :
        AfaLoggerFunc.tradeInfo("û���κε�λ��Ϣ")
        sys.exit(1)


    for i in range( len(records) ):
        TradeContext.appNo        = 'AG2008'
        TradeContext.busiNo       = records[i][0].strip()
        
        AfaLoggerFunc.tradeInfo("��λ����:" + TradeContext.busiNo)
        print "��λ����:" + TradeContext.busiNo
        
        #=============�ж�Ӧ��״̬========================
        if not ChkAppStatus( ) :
            AfaLoggerFunc.tradeInfo('**********���շ�˰��λ���%sӦ��״̬������**********' %TradeContext.busiNo)
            continue
        
        #��ȡ����ftp��ַ���˻�������
        if not GetFtpConfig() :
            AfaLoggerFunc.tradeInfo('��ȡ��������ftpʧ��')        
            if i == len(records) -1:
                sys.exit(1)
            else:
                continue
        
        #��ȡafe����
        if not GetAfeConfig() :
            AfaLoggerFunc.tradeInfo('��ȡAFE����ftpʧ��')        
            if i == len(records) -1:
                sys.exit(1)
            else:
                continue
    
        AfaLoggerFunc.tradeInfo( "*************************%s_FTP��ʼ********************"  %TradeContext.busiNo)
        fileList    =   ["AA11","FA15","FA16","FA13","FA20","FA21","FA22","DPZ_GL"] 

        for file in fileList:

            if file == 'FA22':
                #���⴦�����ڸñ�Ϊ����������Ϣ���ļ���Ϊ��012FA22.txt(012-ũ����)
                lFileName   =   file + '_' + TradeContext.busiNo + '.txt'
                #ֱ�������ftp�Ա���ȡ���ļ�
                GetData("012"+file+".txt",lFileName)  

            else:
                lFileName   =   file + '_' + TradeContext.busiNo + '.txt'
                #ֱ�������ftp�Ա���ȡ���ļ�
                GetData(file+".txt",lFileName)   
                        
            DataToDB(file,0)
            
            #���������ļ�
            filename1 = TradeContext.CROP_LDIR + "/" + lFileName
            filename2 = TradeContext.CROP_LDIR + "/" + lFileName + '_pre'

            cmdstr = "mv " + filename1 + " " + filename2
            AfaLoggerFunc.tradeInfo( cmdstr )
            os.system(cmdstr)

        AfaLoggerFunc.tradeInfo( "*************************%s_FTP����********************"  %TradeContext.busiNo)

    AfaLoggerFunc.tradeInfo('**********���շ�˰���ػ�����Ϣ����**********')
    sys.exit(0)
