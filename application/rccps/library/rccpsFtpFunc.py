# -*- coding: gbk -*-
##################################################################
#   农信银系统.FTP操作模块
#=================================================================
#   程序文件:   rccpsFtpFunc.py
#   作    者:   关彬捷
#   修改时间:   2008-06-11
##################################################################

import os,ftplib,ConfigParser,AfaLoggerFunc

def getRccps(file_path):
    try:
        rccps_home = "run/ftr"
        local_home = os.environ['AFAP_HOME'] + "/data/rccps/"
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/ftpconnect.conf'
        config.readfp( open( configFileName ) )
        
        ftp_p = ftplib.FTP(config.get('rccps','ip'),config.get('rccps','username'),config.get('rccps','password' ))
        ftp_p.cwd(rccps_home)
        file_handler = open(local_home + file_path,'wb')
        ftp_p.retrbinary("RETR " + file_path,file_handler.write)
        file_handler.close()
        ftp_p.quit()
        
        if not os.path.exists(local_home + file_path):
            raise Exception,"文件[" + local_home + file_path + "]下载失败"
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
    
def putHost(file_path):
    try:
        host_home  = "textlib"
        local_home = os.environ['AFAP_HOME'] + "/data/rccps/host/"
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/ftpconnect.conf'
        config.readfp( open( configFileName ) )
        
        if not os.path.exists(local_home + file_path):
            raise Exception,"上传文件[" + local_home + file_path + "]不存在"
            
        ftp_p = ftplib.FTP(config.get('host','ip'),config.get('host','username'),config.get('host','password' ))
        ftp_p.cwd(host_home)
        file_handler = open(local_home + file_path,'rb')
        ftp_p.storbinary("STOR " + file_path,file_handler)
        file_handler.close()
        ftp_p.quit()
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
        
def putERRSYS(file_path):
    try:
        errsys_home  = "./"
        local_home = os.environ['AFAP_HOME'] + "/data/rccps/errorfile/"
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/ftpconnect.conf'
        config.readfp( open( configFileName ) )
        
        if not os.path.exists(local_home + file_path):
            raise Exception,"上传文件[" + local_home + file_path + "]不存在"
            
        ftp_p = ftplib.FTP(config.get('errsys','ip'),config.get('errsys','username'),config.get('errsys','password' ))
        ftp_p.cwd(errsys_home)
        file_handler = open(local_home + file_path,'rb')
        ftp_p.storbinary("STOR " + file_path,file_handler)
        file_handler.close()
        ftp_p.quit()
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False

def getHost(file_path,host_home):
    try:
        #host_home = "BANKMDS"
        local_home = os.environ['AFAP_HOME'] + "/data/rccps/host/"
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/ftpconnect.conf'
        config.readfp( open( configFileName ) )
        
        ftp_p = ftplib.FTP(config.get('host','ip'),config.get('host','username'),config.get('host','password' ))
        ftp_p.cwd(host_home)
        file_handler = open(local_home + file_path,'wb')
        ftp_p.retrbinary("RETR " + file_path,file_handler.write)
        file_handler.close()
        ftp_p.quit()
        
        if not os.path.exists(local_home + file_path):
            raise Exception,"文件[" + local_home + file_path + "]下载失败"
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
