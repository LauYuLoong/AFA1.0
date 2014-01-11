# -*- coding: gbk -*-
###############################################################################
# 摘    要：安徽交罚基础数据下载
# 当前版本：1.0
# 作    者：CYG
# 完成日期：2011年01月21日
###############################################################################
import TradeContext
TradeContext.sysType = 'ahjf'
import ConfigParser, AfaUtilTools, AfaLoggerFunc, sys, AfaDBFunc
import os,ftplib,ConfigParser
from types import *

#读取配置文件中信息
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
        
#安徽非税下载基础数据-从财政下载
def GetFile(RemoteFileName,LocalFileName):

    try:
        #设置默认超时时间
        #socket.setdefaulttimeout(15)
        #建立FTP实例
        ftp_p = ftplib.FTP()
        #连接FTP
        ftp_p.connect(TradeContext.HOSTIP,TradeContext.HOSTPORT)
        #登陆FTP
        ftp_p.login(TradeContext.USERNO,TradeContext.PASSWD)
        #移动到远程FTP服务器指定目录
        ftp_p.cwd(TradeContext.RDIR)
        #以写入方式打开本地文件
        file_handler = open(TradeContext.LDIR + "/" + LocalFileName,'wb')
        #获取指定下载文件内容,并写入到本地文件
        ftp_p.retrbinary("RETR " + TradeContext.RDIR + "/" + RemoteFileName,file_handler.write)
        #关闭本地文件
        file_handler.close()
        #退出FTP
        ftp_p.quit()

        #判断本地文件是否生成,若未生成,则抛出异常
        if not os.path.exists(TradeContext.LDIR + "/" + LocalFileName):
            AfaLoggerFunc.tradeInfo("文件[" + TradeContext.LDIR + "/" + LocalFileName + "]下载失败")
            return False
        AfaLoggerFunc.tradeInfo("文件[" + TradeContext.LDIR + "/" + LocalFileName + "]下载成功")

        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo('FTP处理异常:' + str(e))
        return False

def UpdateData( file ):

    AfaLoggerFunc.tradeInfo( '文件操作开始' )
    
    try:
        sfp = open(TradeContext.LDIR + "/" + file,"r")
        #读取一行
        linebuff = sfp.readline( )
        
        if file[0:9] == "JGDATADOC":
            #读取处罚/采集机关代码文件
            while( len(linebuff)>0 ):
                swapbuff = linebuff.split(chr(05))
                TradeContext.OFFICECODE    = swapbuff[0].lstrip().rstrip()          #采集机关代码
                TradeContext.OFFICENAME    = swapbuff[1].lstrip().rstrip()          #采集机关名称
                #登记基础数据
                upDate_ahjf_officecode( )
                
                linebuff = sfp.readline( )
        else:
            #读取交通违法代码文件
            while( len(linebuff)>0 ):
                swapbuff = linebuff.split(chr(05))
                TradeContext.OFFICECODE    = swapbuff[0].lstrip().rstrip()          #采集机关代码
                TradeContext.LAWACTIONCODE = swapbuff[1].lstrip().rstrip()          #违法行为代码
                TradeContext.DESCRIBE      = swapbuff[2].lstrip().rstrip()          #违法行为描述
                TradeContext.MR_AMOUNT     = swapbuff[3].lstrip().rstrip()          #默认罚款金额
                TradeContext.LOWER_AMOUNT  = swapbuff[4].lstrip().rstrip()          #罚款金额下限
                TradeContext.TOP_AMOUNT    = swapbuff[5].lstrip().rstrip()          #罚款金额上限
                #登记基础数据
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
        AfaLoggerFunc.tradeInfo( '基础数据查询sql：' + selectSql)
        selectRecord = AfaDBFunc.SelectSql( selectSql )
        
        if selectRecord == None:
            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
            return False
        if len(selectRecord) > 0:
            AfaLoggerFunc.tradeInfo('>>>数据已存在，做更新操作')
            
            updateSql = "update ahjf_officecode set "
            updateSql = updateSql + "OFFICENAME     ='" + TradeContext.OFFICENAME     + "'"
        
            updateSql = updateSql + whereSql
            AfaLoggerFunc.tradeInfo( '基础数据更新sql：' + updateSql)
            updateRecord = AfaDBFunc.UpdateSqlCmt( updateSql )
            if updateRecord <  0:
                AfaLoggerFunc.tradeInfo( "更新基础数据失败" )
                return False
        else:
            AfaLoggerFunc.tradeInfo('>>>数据不存在，登记新的数据')
            
            insertSql = "insert into ahjf_officecode(OFFICECODE,OFFICENAME,NOTE1,NOTE2) values("
            insertSql = insertSql + "'" + TradeContext.OFFICECODE    + "',"      #采集机关代码
            insertSql = insertSql + "'" + TradeContext.OFFICENAME + "',"         #采集机关名称
            insertSql = insertSql + "'',"                                        #备用1
            insertSql = insertSql + "'')"                                        #备用2
            
            AfaLoggerFunc.tradeInfo( '基础数据登记sql：' + insertSql)
            insertRecord = AfaDBFunc.InsertSqlCmt( insertSql )
            
            if insertRecord < 0:
                AfaLoggerFunc.tradeInfo( '>>>登记基础更新数据失败数据失败' )
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
        AfaLoggerFunc.tradeInfo( '基础数据查询sql：' + selectSql)
        selectRecord = AfaDBFunc.SelectSql( selectSql )
        
        if selectRecord == None:
            AfaLoggerFunc.tradeInfo('>>>查询数据库异常')
            return False
        if len(selectRecord) > 0:
            AfaLoggerFunc.tradeInfo('>>>数据已存在，做更新操作')
            
            updateSql = "update ahjf_lawcode set "
            updateSql = updateSql + "DESCRIBE     ='" + TradeContext.DESCRIBE     + "',"
            updateSql = updateSql + "MR_AMOUNT    ='" + TradeContext.MR_AMOUNT    + "',"
            updateSql = updateSql + "LOWER_AMOUNT ='" + TradeContext.LOWER_AMOUNT + "',"
            updateSql = updateSql + "TOP_AMOUNT   ='" + TradeContext.TOP_AMOUNT   + "'"
            
            updateSql = updateSql + whereSql
            AfaLoggerFunc.tradeInfo( '基础数据更新sql：' + updateSql)
            updateRecord = AfaDBFunc.UpdateSqlCmt( updateSql )
            if updateRecord <  0:
                AfaLoggerFunc.tradeInfo( "更新基础数据失败" )
                return False
        else:
            AfaLoggerFunc.tradeInfo('>>>数据不存在，登记新的数据')
            
            insertSql = "insert into ahjf_lawcode(OFFICECODE,LAWACTIONCODE,DESCRIBE,MR_AMOUNT,LOWER_AMOUNT,TOP_AMOUNT,note1,note2,note3,note4) values("
            insertSql = insertSql + "'" + TradeContext.OFFICECODE    + "',"      #采集机关代码 
            insertSql = insertSql + "'" + TradeContext.LAWACTIONCODE + "',"      #违法行为代码 
            insertSql = insertSql + "'" + TradeContext.DESCRIBE      + "',"      #违法行为描述 
            insertSql = insertSql + "'" + TradeContext.MR_AMOUNT     + "',"      #默认罚款金额 
            insertSql = insertSql + "'" + TradeContext.LOWER_AMOUNT  + "',"      #罚款金额下限 
            insertSql = insertSql + "'" + TradeContext.TOP_AMOUNT    + "',"      #罚款金额上限 
            insertSql = insertSql + "'',"                                        #备用1
            insertSql = insertSql + "'',"                                        #备用2
            insertSql = insertSql + "'',"                                        #备用3
            insertSql = insertSql + "'')"                                        #备用4
            
            AfaLoggerFunc.tradeInfo( '基础数据登记sql：' + insertSql)
            insertRecord = AfaDBFunc.InsertSqlCmt( insertSql )
            
            if insertRecord < 0:
                AfaLoggerFunc.tradeInfo( '>>>登记基础更新数据失败数据失败' )
                return False
            return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return False

if __name__ == '__main__':

    AfaLoggerFunc.tradeInfo('******安徽交罚每日基础数据更新开始******')
    
    TradeContext.workDate = AfaUtilTools.GetSysDate( )
    
    #获取配置文件信息
    GetConfig( 'AG2017_AHJF_DZ' )
    
    files = ["JGDATADOC_012_" + TradeContext.workDate + ".TXT","DATADOC_012_" + TradeContext.workDate + ".TXT"]
    
    #到财政下载基础数据文件
    for file in files:
        if GetFile( file,file ):
            AfaLoggerFunc.tradeInfo( ">>>" + file + '文件有数据需要更新')
            UpdateData( file )
    
    AfaLoggerFunc.tradeInfo('******安徽交罚每日基础数据更新结束******')
