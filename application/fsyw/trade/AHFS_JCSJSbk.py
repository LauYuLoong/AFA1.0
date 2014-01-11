###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：安徽非税下载基础信息
#
# 当前版本：1.0
# 作    者：WJJ
# 完成日期：2007年10月15日
###############################################################################
import TradeContext
TradeContext.sysType = 'fsyw'
import ConfigParser, AfaUtilTools, AfaLoggerFunc, sys, AfaDBFunc, AfaAfeFunc,Party3Context
import os, HostContext, AfaLoggerFunc,ftplib,ConfigParser,socket

from types import *



#读取财政ftp配置信息
def GetFtpConfig( ):

    #---------------从数据库中提取信息--------------
    sqlstr =   "select hostip,downuser,downpasswd,downldir,downrdir from fs_businoconf where busino='" + TradeContext.busiNo + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        AfaLoggerFunc.tradeInfo( "查找数据库异常：单位编码ftp配置信息表，联系科技人员" )
        return False

    if( len( records)==0 ):
        AfaLoggerFunc.tradeInfo( "没有查找到单位配置信息，联系科技人员" )
        return False

    else:
        TradeContext.CROP_HOSTIP   = records[0][0].strip()
        TradeContext.CROP_USERNO   = records[0][1].strip()
        TradeContext.CROP_PASSWD   = records[0][2].strip()
        TradeContext.CROP_LDIR     = records[0][3].strip()
        TradeContext.CROP_RDIR     = records[0][4].strip()

        AfaLoggerFunc.tradeInfo( "当前单位编码：%s" %TradeContext.busiNo )
        AfaLoggerFunc.tradeInfo( "当前主机地址：%s" %TradeContext.CROP_HOSTIP )
        AfaLoggerFunc.tradeInfo( "账户：%s"         %TradeContext.CROP_USERNO )
        AfaLoggerFunc.tradeInfo( "密码：%s"         %TradeContext.CROP_PASSWD )
        AfaLoggerFunc.tradeInfo( "本地路径：%s"     %TradeContext.CROP_LDIR )
        return True




#读取配置文件中信息
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
        AfaLoggerFunc.tradeInfo("TradeContext.BATCH_HOSTIP::"+TradeContext.BATCH_HOSTIP)
        AfaLoggerFunc.tradeInfo("TradeContext.BATCH_USERNO::"+TradeContext.BATCH_USERNO)



        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False

#发送到afe下载文件
def GetFtpFile(RemoteFileName):

    TradeContext.sysId          = "FTP"
    TradeContext.hostip         = TradeContext.CROP_HOSTIP
    TradeContext.user           = TradeContext.CROP_USERNO
    TradeContext.pwd            = TradeContext.CROP_PASSWD
    TradeContext.localpath      = TradeContext.CROP_LDIR
    #TradeContext.localfilename  = LocalFileName
    TradeContext.remotefilename = RemoteFileName
    TradeContext.remotepath     = TradeContext.CROP_RDIR
    TradeContext.TransCode      = "8889"
    TradeContext.TemplateCode   = "3001"

    #=============与第三方通讯通讯====================
    TradeContext.__respFlag__='0'

    AfaAfeFunc.CommAfe()

    flag  = -1

    if( TradeContext.errorCode != '0000' ):
        AfaLoggerFunc.tradeInfo("文件[" + TradeContext.localpath + "/" + RemoteFileName + "]下载失败")
        flag = -1

    else:
        AfaLoggerFunc.tradeInfo("文件[" + TradeContext.localpath + "/" + RemoteFileName + "]下载成功")
        flag = 0

    #下载完成之后把下载日志记录到数据库中
    sql = ""
    sql = sql + "insert into fs_ftpreturn(busino,hostip,succflag,ftpflag,workdate,worktime,filename,note1,note2) values(  "
    sql = sql + "'" + TradeContext.busiNo         + "',"        #单位编号
    sql = sql + "'" + TradeContext.hostip         + "',"        #主机地址
    sql = sql + "'" + str(flag)                   + "',"        #成功失败标志（0-成功，-1-失败）
    sql = sql + "'" + "1"                         + "',"        #上传下载标志（0-上传，1-下载）
    sql = sql + "'" + TradeContext.WORKDATE       + "',"        #操作日期
    sql = sql + "'" + AfaUtilTools.GetSysTime( )  + "',"        #操作时间
    sql = sql + "'" + RemoteFileName              + "',"        #下载文件名
    sql = sql + "'',"                                           #备注1
    sql = sql + "'')"                                           #备注2

    AfaLoggerFunc.tradeInfo( ">>>>登记下载记录:" + sql )

    AfaDBFunc.UpdateSqlCmt( sql )

    return flag


#安徽非税下载基础数据-从财政下载
def GetData(RemoteFileName,LocalFileName):

    ##======== START 20091110 by zhangheng ===============================================================
    try:
        HOSTIP    =  TradeContext.CROP_HOSTIP
        HOSTPORT  =  '21'
        USERNO    =  TradeContext.CROP_USERNO
        PASSWD    =  TradeContext.CROP_PASSWD
        LDIR      =  TradeContext.CROP_LDIR
        RDIR      =  TradeContext.CROP_RDIR

        #设置默认超时时间
        socket.setdefaulttimeout(15)
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
            AfaLoggerFunc.tradeInfo("文件[" + LDIR + "/" + LocalFileName + "]下载失败")
            return -1
        AfaLoggerFunc.tradeInfo("文件[" + LDIR + "/" + LocalFileName + "]下载成功")

        return 0
    ##========= END ================================================================
    except Exception, e:
        AfaLoggerFunc.tradeInfo('FTP处理异常')
        return -1

#从AFE下载基础信息-文件形式
def ftpfile( rfilename, lfilename):

    try:
        #创建文件
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/AhfsFtpJks' + '.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.BATCH_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.BATCH_USERNO + ' ' + TradeContext.BATCH_PASSWD + '\n')

        #下载文件
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
        AfaLoggerFunc.tradeInfo('FTP处理异常')
        return -1

def DataToDB(file,ibegin):
    AfaLoggerFunc.tradeInfo( 'table:'+file )
    try :

        #首先建立表名和字段的映射,然后在下载的数据中都加入日期和时间字段
        #map =   {"AA11":"AAA010,AAA011,AAA012, AAA014,AAZ001,BUSINO,DATE,TIME",\
        #         "FA15":"AAA010,AFA050,AAZ006,AFA051,AFA052,AAZ007,AFA062,AAZ002,BUSINO,DATE,TIME",\
        #         "FA16":"AFA050,AFA030,AAZ006,AAZ007,BUSINO,DATE,TIME",\
        #         "FA13":"AFA030,AAZ006,AAZ007,AFA031,AFA032,AAZ002,AFA038,AFA039,AFA040,AFA041,AFA042,AFA020,BUSINO,DATE,TIME",\
        #         "FA20":"AAA010,AFA090,AFA091,AFA092,AFA096,BUSINO,DATE,TIME",\
        #         "FA21":"AFA090,AFA050,AFA030,AAZ006,AAZ007,BUSINO,DATE,TIME",\
        #         "DPZ_GL":"FPZDM,FQSHM,FQZHM,FDWDM,FCZQHNM,BUSINO,DATE,TIME",\
        #         "FA22":"AAA010,AFA106,AAZ006,AFA100,AFA101,AFA102,AFA103,BUSINO,DATE,TIME" }

        #begin 20100604 蔡永贵修改 除了FA22外，所有映射中在BUSINO前加上BANKNO字段
        
        map =   {"AA11":"AAA010,AAA011,AAA012, AAA014,AAZ001,BANKNO,BUSINO,DATE,TIME",\
                 "FA15":"AAA010,AFA050,AAZ006,AFA051,AFA052,AAZ007,AFA062,AAZ002,BANKNO,BUSINO,DATE,TIME",\
                 "FA16":"AFA050,AFA030,AAZ006,AAZ007,BANKNO,BUSINO,DATE,TIME",\
                 "FA13":"AFA030,AAZ006,AAZ007,AFA031,AFA032,AAZ002,AFA038,AFA039,AFA040,AFA041,AFA042,AFA020,BANKNO,BUSINO,DATE,TIME",\
                 "FA20":"AAA010,AFA090,AFA091,AFA092,AFA096,BANKNO,BUSINO,DATE,TIME",\
                 "FA21":"AFA090,AFA050,AFA030,AAZ006,AAZ007,BANKNO,BUSINO,DATE,TIME",\
                 "DPZ_GL":"FPZDM,FQSHM,FQZHM,FDWDM,FCZQHNM,BANKNO,BUSINO,DATE,TIME",\
                 "FA22":"AAA010,AFA106,AAZ006,AFA100,AFA101,AFA102,AFA103,BUSINO,DATE,TIME" }
        
        #将文件中的记录加入到数据库中
        #fileName    =   TradeContext.CROP_LDIR + "/" + file + '_' + TradeContext.busiNo + ".txt"


        if file == 'FA22':
            fileName = TradeContext.CROP_LDIR + "/" + TradeContext.bankbm+file+".txt"
        else:
            fileName = TradeContext.CROP_LDIR + "/" + file + ".txt"
        #end



        print '====' + fileName

        if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
            fp      =   open(fileName,"rb")

            #将所有的数据读取到sALl中
            sAll    =   fp.read()
            fp.close()
            #rec是每一条记录
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
                        sqlstr=''
                        sqlstr = "select count(*) from FS_AA11 where AAA010='" + rec.split(chr(31))[0] + "' and BUSINO='" + TradeContext.busiNo + "'"
                        sqlstr = sqlstr + " and bankno ='" + TradeContext.bankbm + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            print '>>>查询数据库异常'
                            AfaLoggerFunc.tradeInfo('>>>查询数据库异常AA11')
                            return -1

                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '重复记录,更新处理' )

                            #如果记录存在,必须先删除,再新增
                            strStr_del = "DELETE FROM FS_AA11 where AAA010='" + rec.split(chr(31))[0] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            strStr_del = strStr_del + " and bankno ='" + TradeContext.bankbm + "'"

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>删除数据失败:' + AfaDBFunc.sqlErrMsg)
                                return -1


                    elif file=='FA15':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_FA15 where AFA050='" + rec.split(chr(31))[1] + "' and AAZ006='" + rec.split(chr(31))[2] + "' and BUSINO='" + TradeContext.busiNo + "'"
                        sqlstr = sqlstr + " and bankno ='" + TradeContext.bankbm + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            print '>>>查询数据库异常'
                            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
                            return -1

                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '重复记录,更新处理' )

                            #如果记录存在,必须先删除,再新增
                            strStr_del = "DELETE FROM FS_FA15 where AFA050='" + rec.split(chr(31))[1] + "' and AAZ006='" + rec.split(chr(31))[2] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            strStr_del = strStr_del + " and bankno ='" + TradeContext.bankbm + "'"

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>删除数据失败:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    elif file=='FA16':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_FA16 where AFA050='" + rec.split(chr(31))[0] + "' and AFA030='" + rec.split(chr(31))[1] + "'and AAZ006='" + rec.split(chr(31))[2] + "' and BUSINO='" + TradeContext.busiNo + "'"
                        sqlstr = sqlstr + " and bankno ='" + TradeContext.bankbm + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
                            return -1

                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '重复记录,更新处理' )

                            #如果记录存在,必须先删除,再新增
                            strStr_del = "DELETE FROM FS_FA16 where AFA050='" + rec.split(chr(31))[0] + "' and AFA030='" + rec.split(chr(31))[1] + "'and AAZ006='" + rec.split(chr(31))[2] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            strStr_del = strStr_del + " and bankno ='" + TradeContext.bankbm + "'"

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>删除数据失败:' + AfaDBFunc.sqlErrMsg)
                                return -1


                    elif file=='FA13':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_FA13 where AFA030='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[1] + "' and BUSINO='" + TradeContext.busiNo + "'"
                        sqlstr = sqlstr + " and bankno ='" + TradeContext.bankbm + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
                            return -1

                        if records[0][0]==1:
                            AfaLoggerFunc.tradeInfo( '重复记录,更新处理' )

                            #如果记录存在,必须先删除,再新增
                            strStr_del = "DELETE FROM FS_FA13 where AFA030='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[1] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            strStr_del = strStr_del + " and bankno ='" + TradeContext.bankbm + "'"

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>删除数据失败:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    elif file=='FA20':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_FA20 where AAA010='" + rec.split(chr(31))[0] + "' and AFA090='" + rec.split(chr(31))[1] + "' and BUSINO='" + TradeContext.busiNo + "'"
                        sqlstr = sqlstr + " and bankno ='" + TradeContext.bankbm + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
                            return -1

                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '重复记录,更新处理' )

                            #如果记录存在,必须先删除,再新增
                            strStr_del = "DELETE FROM FS_FA20 where AAA010='" + rec.split(chr(31))[0] + "' and AFA090='" + rec.split(chr(31))[1] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            strStr_del = strStr_del + " and bankno ='" + TradeContext.bankbm + "'"

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>删除数据失败:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    elif file=='FA21':
                        sqlstr=''
                        #sqlstr = "select count(*) from FS_FA21 where AFA090='" + rec.split(chr(31))[0] + "' and AFA050='" + rec.split(chr(31))[1] + "'and AFA030='" + rec.split(chr(31))[2] + "'and AAZ006='" + rec.split(chr(31))[3] + "' and BUSINO='" + TradeContext.busiNo + "'"

                        sqlstr = "select count(*) from FS_FA21 where AFA090='" + rec.split(chr(31))[0] + "' and AFA050='" + rec.split(chr(31))[1] + "'and AFA030='" + rec.split(chr(31))[2] + "'and BUSINO='" + TradeContext.busiNo + "'"
                        sqlstr = sqlstr + " and bankno ='" + TradeContext.bankbm + "'"
                        
                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
                            return -1

                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '重复记录,更新处理' )

                            #如果记录存在,必须先删除,再新增
                            strStr_del = "DELETE FROM FS_FA21 where AFA090='" + rec.split(chr(31))[0] + "' and AFA050='" + rec.split(chr(31))[1] + "'and AFA030='" + rec.split(chr(31))[2] + "'and BUSINO='" + TradeContext.busiNo + "'"
                            strStr_del = strStr_del + " and bankno ='" + TradeContext.bankbm + "'"

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>删除数据失败:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    elif file=='DPZ_GL':
                        sqlstr=''
                        sqlstr = "select count(*) from FS_DPZ_GL where FPZDM='" + rec.split(chr(31))[0] + "' and FQSHM='" + rec.split(chr(31))[1] + "'and FQZHM='" + rec.split(chr(31))[2] + "'and FDWDM='" + rec.split(chr(31))[3] + "'and FCZQHNM='" + rec.split(chr(31))[4].strip() + "' and BUSINO='" + TradeContext.busiNo + "'"
                        sqlstr = sqlstr + " and bankno ='" + TradeContext.bankbm + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
                            return -1

                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '重复记录,更新处理' )

                            #如果记录存在,必须先删除,再新增
                            strStr_del = "DELETE FROM FS_DPZ_GL where FPZDM='" + rec.split(chr(31))[0] + "' and FQSHM='" + rec.split(chr(31))[1] + "'and FQZHM='" + rec.split(chr(31))[2] + "'and FDWDM='" + rec.split(chr(31))[3] + "'and FCZQHNM='" + rec.split(chr(31))[4].strip() + "' and BUSINO='" + TradeContext.busiNo + "'"
                            strStr_del = strStr_del + " and bankno ='" + TradeContext.bankbm + "'"

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>删除数据失败:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    elif file=='FA22':
                        sqlstr = ''
                        sqlstr = "select count(*) from FS_FA22 where AAA010='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[2] + "'and AFA100='" + rec.split(chr(31))[3] + "' and BUSINO='" + TradeContext.busiNo + "'" + " and AFA101='" + rec.split(chr(31))[4] + "'"

                        AfaLoggerFunc.tradeInfo( sqlstr )

                        records = AfaDBFunc.SelectSql( sqlstr )
                        if (records==None or len(records) <= 0):
                            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
                            return -1

                        if records[0][0]==1:

                            AfaLoggerFunc.tradeInfo( '重复记录,更新处理' )

                            #如果记录存在,必须先删除,再新增

                            #begin 20100527 蔡永贵修改 增加AFA101（单位编码)作为sql的查询条件
                            #strStr_del = "DELETE FROM FS_FA22 where AAA010='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[2] + "'and AFA100='" + rec.split(chr(31))[3] + "' and BUSINO='" + TradeContext.busiNo + "'"
                            strStr_del = "DELETE FROM FS_FA22 where AAA010='" + rec.split(chr(31))[0] + "' and AAZ006='" + rec.split(chr(31))[2] + "'and AFA100='" + rec.split(chr(31))[3] + "' and BUSINO='" + TradeContext.busiNo + "'" + " and AFA101='" + rec.split(chr(31))[4] + "'"
                            #end

                            AfaLoggerFunc.tradeInfo( strStr_del )

                            result = AfaDBFunc.DeleteSqlCmt( strStr_del )
                            if result < 1 :
                                AfaLoggerFunc.tradeInfo('>>>删除数据失败:' + AfaDBFunc.sqlErrMsg)
                                return -1

                    sqlstr  =   ""
                    sqlstr  =   "insert into " + "FS_" + file + " (" + map[file] + " ) " + "  values ("

                    for item in rec.split(chr(31)):
                        sqlstr  =  sqlstr   +   "'"
                        sqlstr  =  sqlstr   +   item.strip() + "',"
                        
                    #begin 20100629 蔡永贵增加银行编码
                    if file != 'FA22':
                        sqlstr      =   sqlstr  + "'" + TradeContext.bankbm   + "',"
                    #end

                    sqlstr      =   sqlstr  + "'" + TradeContext.busiNo   + "',"
                    sqlstr      =   sqlstr  + "'" + TradeContext.WORKDATE + "',"
                    sqlstr      =   sqlstr  + "'" + TradeContext.WORKTIME + "')"

                    AfaLoggerFunc.tradeInfo( sqlstr )

                    ret = AfaDBFunc.InsertSqlCmt( sqlstr )
                    if(  ret< 1 ):
                        AfaLoggerFunc.tradeInfo( "插入记录异常:" + AfaDBFunc.sqlErrMsg )
                        continue

        else:
            AfaLoggerFunc.tradeInfo( "文件" + fileName + "不存在" )

        return 0



    except Exception, e:
        fp.close()
        AfaLoggerFunc.tradeInfo( e )
        return -1


def ChkAppStatus():
    sqlstr  =   "select status from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino ='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        AfaLoggerFunc.tradeInfo('查找应用状态库失败')
        return False

    elif len( records ) == 1:
        if records[0][0].strip() == '1':
            return True
        else:
            AfaLoggerFunc.tradeInfo('应用状态没有开启')
            return False

    else:
        AfaLoggerFunc.tradeInfo('应用签约异常')
        return False






###########################################主函数###########################################
if __name__=='__main__':
    AfaLoggerFunc.tradeInfo('**********安徽非税下载基础信息开始**********')

    #初始化TradeContext
    TradeContext.WORKDATE       =   AfaUtilTools.GetSysDate( )
    TradeContext.WORKTIME       =   AfaUtilTools.GetSysTime( )

    #begin 20100527 蔡永贵修改
    #sqlstr  = "select distinct busino from abdt_unitinfo where appno='AG2008'"
    sqlstr  = "select distinct busino,appno from abdt_unitinfo where appno in ('AG2008','AG2012') and busino= '34146860230001'"
    #sqlstr  = " select busino,bankno from fs_businoinfo "
    #end
    AfaLoggerFunc.tradeInfo("sqlstr ="+sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None:
        AfaLoggerFunc.tradeInfo("查找单位信息表异常" + AfaDBFunc.sqlErrMsg)
        sys.exit(1)

    elif len(records)==0 :
        AfaLoggerFunc.tradeInfo("没有任何单位信息")
        sys.exit(1)


    for i in range( len(records) ):
        TradeContext.appNo        = records[i][1].strip()
        TradeContext.busiNo       = records[i][0].strip()

        #begin 20100527 蔡永贵修改
        if( TradeContext.appNo == 'AG2008' ):
            TradeContext.bankbm = '012';
        else:
            TradeContext.bankbm = '099';
        #end

        AfaLoggerFunc.tradeInfo("单位编码:" + TradeContext.busiNo)
        print "单位编码:" + TradeContext.busiNo

        #=============判断应用状态========================
        if not ChkAppStatus( ) :
            AfaLoggerFunc.tradeInfo('**********安徽非税单位编号%s应用状态不正常**********' %TradeContext.busiNo)
            continue

        #获取财政ftp地址、账户和密码
        if not GetFtpConfig() :
            AfaLoggerFunc.tradeInfo('获取财政配置ftp失败')
            if i == len(records) -1:
                sys.exit(1)
            else:
                continue

        #获取afe配置
        if not GetAfeConfig() :
            AfaLoggerFunc.tradeInfo('获取AFE配置ftp失败')
            if i == len(records) -1:
                sys.exit(1)
            else:
                continue

        AfaLoggerFunc.tradeInfo( "*************************%s_FTP开始********************"  %TradeContext.busiNo)
        fileList    =   ["AA11","FA15","FA16","FA13","FA20","FA21","FA22","DPZ_GL"]

        for file in fileList:

            if file == 'FA22':
                #特殊处理，由于该表为代收银行信息表，文件名为：012FA22.txt(012-农信社)
                #lFileName   =   file + '_' + TradeContext.busiNo + '.txt'
                #直接向财政ftp以便于取得文件

                #begin 20100527 蔡永贵修改
                #GetData("012"+file+".txt")
                rfile = TradeContext.bankbm+file+".txt"
                GetFtpFile(rfile)
                #end

            else:
                #lFileName   =   file + '_' + TradeContext.busiNo + '.txt'
                rfile = file + ".txt"
                #直接向财政ftp以便于取得文件
                GetFtpFile(rfile)

            AfaLoggerFunc.tradeInfo( ">>>>>>>>>>>>>开始登记下载数据" )
            DataToDB(file,0)

            #备份数据文件
            #filename1 = TradeContext.CROP_LDIR + "/" + lileName
            #filename2 = TradeContext.CROP_LDIR + "/" + lFileName + '_pre'

            filename1 = TradeContext.CROP_LDIR + "/" + rfile
            filename2 = TradeContext.CROP_LDIR + "/" + file + '_' + TradeContext.busiNo + '_pre'

            if( os.path.exists(filename1) and os.path.isfile(filename1) ):
                cmdstr = "mv " + filename1 + " " + filename2
                AfaLoggerFunc.tradeInfo( cmdstr )
                os.system(cmdstr)

        AfaLoggerFunc.tradeInfo( "*************************%s_FTP结束********************"  %TradeContext.busiNo)

    AfaLoggerFunc.tradeInfo('**********安徽非税下载基础信息结束**********')
    sys.exit(0)
