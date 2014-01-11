# -*- coding: gbk -*-
################################################################################
#   �м�ҵ��ƽ̨.FTP������
#===============================================================================
#   �����ļ�:   AfaFtpFunc.py
#   ��    ��:   �ر��
#   �޸�ʱ��:   2009-07-24
################################################################################
import os,ftplib,ConfigParser,AfaLoggerFunc

################################################################################
#����:�ϴ������ļ���Զ��FTP������
#����:ConfigNode:�ڵ���(���������Զ����ݽڵ����Ƶ�conf/lapp.conf�ж�ȡFTP����);
#     LocalFileName:�����ļ�����;
#     RemoteFileName:Զ���ļ�����
#����:True:�ɹ�;False:ʧ��
#ʹ�÷�������:
#import AfaFtpFunc
#    ret = AfaFtpFunc.getFile("NODE","localfile.txt","remotefile.txt")
#    if not ret:
#        return AfaFlowControl.ExitThisFlow("A999","�����ļ�remotefile.txt��localfile.txtʧ��")
#    AfaLoggerFunc.tradeInfo(">>>�����ļ�remotefile.txt������localfile.txt�ɹ�")
################################################################################
def getFile(ConfigNode,LocalFileName,RemoteFileName):
    
    AfaLoggerFunc.tradeInfo( '>>>FTP�����ļ�' )
    
    try:
        #��ȡFTP�����ļ�
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        
        config.readfp( open( configFileName ) )
        
        HOSTIP    = config.get(ConfigNode,'HOSTIP')
        HOSTPORT  = config.get(ConfigNode,'HOSTPORT')
        USERNO    = config.get(ConfigNode,'USERNO')
        PASSWD    = config.get(ConfigNode,'PASSWD')
        LDIR      = config.get(ConfigNode,'LDIR')
        RDIR      = config.get(ConfigNode,'RDIR')
        
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
            raise Exception,"�ļ�[" + LDIR + "/" + LocalFileName + "]����ʧ��"
            
        AfaLoggerFunc.tradeInfo("�ļ�[" + LDIR + "/" + LocalFileName + "]���سɹ�")
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False

################################################################################
#����:����Զ��FTP�������ļ�������
#����:ConfigNode:�ڵ���;(���������Զ����ݽڵ����Ƶ�conf/lapp.conf�ж�ȡFTP����)
#     LocalFileName:�����ļ�����;
#     RemoteFileName:Զ���ļ�����
#����:True:�ɹ�;False:ʧ��
#ʹ�÷�������:
#import AfaFtpFunc
#    ret = AfaFtpFunc.putFile("NODE","localfile.txt","remotefile.txt")
#    if not ret:
#        return AfaFlowControl.ExitThisFlow("A999","�ϴ��ļ�localefile.txt��������remotefile.txtʧ��")
#    AfaLoggerFunc.tradeInfo(">>>�ϴ��ļ�localfile.txt��������remotefile.txt�ɹ�")
################################################################################
def putFile(ConfigNode,LocalFileName,RemoteFileName):
    
    AfaLoggerFunc.tradeInfo( '>>>FTP�ϴ��ļ�' )
    
    try:
        #��ȡFTP�����ļ�
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        
        config.readfp( open( configFileName ) )
        
        HOSTIP    = config.get(ConfigNode,'HOSTIP')
        HOSTPORT  = config.get(ConfigNode,'HOSTPORT')
        USERNO    = config.get(ConfigNode,'USERNO')
        PASSWD    = config.get(ConfigNode,'PASSWD')
        LDIR      = config.get(ConfigNode,'LDIR')
        RDIR      = config.get(ConfigNode,'RDIR')
        
        if not os.path.exists(LDIR + "/" + LocalFileName):
            raise Exception,"�ϴ��ļ�[" + LDIR + "/" + LocalFileName + "]������"
        
        #����FTPʵ��
        ftp_p = ftplib.FTP()
        #����FTP
        ftp_p.connect(HOSTIP,HOSTPORT)
        #��½FTP
        ftp_p.login(USERNO,PASSWD)
        #�ƶ���Զ��FTP������ָ��Ŀ¼��
        ftp_p.cwd(RDIR)
        #�Զ�ȡ��ʽ�򿪱����ļ�
        file_handler = open(LDIR + "/" + LocalFileName,'rb')
        #��ȡ�����ļ�����,��д�뵽Զ��FTP������ָ���ļ�
        ftp_p.storbinary("STOR " + RDIR + "/" + RemoteFileName,file_handler)
        #�رձ����ļ�
        file_handler.close()
        #�˳�FTP
        ftp_p.quit()
        
        AfaLoggerFunc.tradeInfo("�ļ�[" + LDIR + "/" + LocalFileName + "]�ϴ��ɹ�")
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
