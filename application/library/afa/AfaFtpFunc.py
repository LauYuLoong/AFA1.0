# -*- coding: gbk -*-
################################################################################
#   中间业务平台.FTP方法类
#===============================================================================
#   程序文件:   AfaFtpFunc.py
#   作    者:   关彬捷
#   修改时间:   2009-07-24
################################################################################
import os,ftplib,ConfigParser,AfaLoggerFunc

################################################################################
#功能:上传本地文件至远程FTP服务器
#参数:ConfigNode:节点名(本方法将自动根据节点名称到conf/lapp.conf中读取FTP配置);
#     LocalFileName:本地文件名称;
#     RemoteFileName:远程文件名称
#返回:True:成功;False:失败
#使用方法举例:
#import AfaFtpFunc
#    ret = AfaFtpFunc.getFile("NODE","localfile.txt","remotefile.txt")
#    if not ret:
#        return AfaFlowControl.ExitThisFlow("A999","下载文件remotefile.txt至localfile.txt失败")
#    AfaLoggerFunc.tradeInfo(">>>下载文件remotefile.txt至本地localfile.txt成功")
################################################################################
def getFile(ConfigNode,LocalFileName,RemoteFileName):
    
    AfaLoggerFunc.tradeInfo( '>>>FTP下载文件' )
    
    try:
        #读取FTP配置文件
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        
        config.readfp( open( configFileName ) )
        
        HOSTIP    = config.get(ConfigNode,'HOSTIP')
        HOSTPORT  = config.get(ConfigNode,'HOSTPORT')
        USERNO    = config.get(ConfigNode,'USERNO')
        PASSWD    = config.get(ConfigNode,'PASSWD')
        LDIR      = config.get(ConfigNode,'LDIR')
        RDIR      = config.get(ConfigNode,'RDIR')
        
        #建立FTP实例
        ftp_p = ftplib.FTP()
        #连接FTP
        ftp_p.connect(HOSTIP,HOSTPORT)
        #登陆FTP
        ftp_p.login(USERNO,PASSWD)
        #移动到远程FTP服务器指定目录
        ftp_p.cwd(RDIR)
        #以写入方式打开本地文件
        file_handler = open(LDIR + "/" + LocalFileName,'wb')
        #获取指定下载文件内容,并写入到本地文件
        ftp_p.retrbinary("RETR " + RDIR + "/" + RemoteFileName,file_handler.write)
        #关闭本地文件
        file_handler.close()
        #退出FTP
        ftp_p.quit()
        
        #判断本地文件是否生成,若未生成,则抛出异常
        if not os.path.exists(LDIR + "/" + LocalFileName):
            raise Exception,"文件[" + LDIR + "/" + LocalFileName + "]下载失败"
            
        AfaLoggerFunc.tradeInfo("文件[" + LDIR + "/" + LocalFileName + "]下载成功")
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False

################################################################################
#功能:下载远程FTP服务器文件至本地
#参数:ConfigNode:节点名;(本方法将自动根据节点名称到conf/lapp.conf中读取FTP配置)
#     LocalFileName:本地文件名称;
#     RemoteFileName:远程文件名称
#返回:True:成功;False:失败
#使用方法举例:
#import AfaFtpFunc
#    ret = AfaFtpFunc.putFile("NODE","localfile.txt","remotefile.txt")
#    if not ret:
#        return AfaFlowControl.ExitThisFlow("A999","上传文件localefile.txt至服务器remotefile.txt失败")
#    AfaLoggerFunc.tradeInfo(">>>上传文件localfile.txt至服务器remotefile.txt成功")
################################################################################
def putFile(ConfigNode,LocalFileName,RemoteFileName):
    
    AfaLoggerFunc.tradeInfo( '>>>FTP上传文件' )
    
    try:
        #读取FTP配置文件
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
            raise Exception,"上传文件[" + LDIR + "/" + LocalFileName + "]不存在"
        
        #建立FTP实例
        ftp_p = ftplib.FTP()
        #连接FTP
        ftp_p.connect(HOSTIP,HOSTPORT)
        #登陆FTP
        ftp_p.login(USERNO,PASSWD)
        #移动到远程FTP服务器指定目录下
        ftp_p.cwd(RDIR)
        #以读取方式打开本地文件
        file_handler = open(LDIR + "/" + LocalFileName,'rb')
        #读取本地文件内容,并写入到远程FTP服务器指定文件
        ftp_p.storbinary("STOR " + RDIR + "/" + RemoteFileName,file_handler)
        #关闭本地文件
        file_handler.close()
        #退出FTP
        ftp_p.quit()
        
        AfaLoggerFunc.tradeInfo("文件[" + LDIR + "/" + LocalFileName + "]上传成功")
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
