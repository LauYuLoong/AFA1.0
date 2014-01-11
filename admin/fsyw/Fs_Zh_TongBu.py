############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：安徽非税中心单位签约数据导出
#
# 当前版本：1.0
# 作    者：蔡永贵
# 完成日期：2010年06月28日
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import AfaDBFunc,ConfigParser,os, AfaLoggerFunc,ftplib
from types import *

#导出非税单位签约数据
def ExpUnitInfo( filename ):

    AfaLoggerFunc.tradeInfo( '--->开始导出单位协议签约数据' )
    try:
      
      os.system("db2 connect to maps")
      
      #cmd = "db2 \" export to '" + TradeContext.ldir + "/" + filename + "' of del select * from abdt_unitinfo where appno in ('AG2008','AG2012')\" "
      #begin 20110811 修改，因为芜湖扬子银行三县支行非税与当地非税的012相互冲突，所以增加银行编码015，新增AG2104与银行编码015对应
      cmd = "db2 \" export to '" + TradeContext.ldir + "/" + filename + "' of del select * from abdt_unitinfo where appno in ('AG2008','AG2012','AG2104')\" "
      #end 20110811
      os.system( cmd )
      
      os.system("db2 disconnect maps")
      
      return True
    
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('导出单位协议签约数据异常')
        return False
    

#把导出的数据主动ftp到地市的服务器上
def PutFile( ftpInfo,LocalFileName,RemoteFileName ):
    
    for record in ftpInfo:
         HOSTIP   = record[1]
         USERNO   = record[2]
         PASSWD   = record[3]
         RDIR     = record[4]
         LDIR     = record[5]
         
         try:
         
            if not os.path.exists(LDIR + "/" + LocalFileName):
                raise Exception,"上传文件[" + LDIR + "/" + LocalFileName + "]不存在"
            
            AfaLoggerFunc.tradeInfo('--->开始往[' + HOSTIP + ']发送数据')
           
            #建立FTP实例
            ftp_p = ftplib.FTP()
            #连接FTP
            ftp_p.connect(HOSTIP,'21')
            #登陆FTP
            ftp_p.login(USERNO,PASSWD)
            #移动到远程FTP服务器指定目录下
            #ftp_p.cwd(RDIR)
            #以读取方式打开本地文件
            file_handler = open(LDIR + "/" + LocalFileName,'rb')
            #读取本地文件内容,并写入到远程FTP服务器指定文件
            ftp_p.storbinary("STOR " + RDIR + "/" + RemoteFileName,file_handler)
            #关闭本地文件
            file_handler.close()
            #退出FTP
            ftp_p.quit()
           
            AfaLoggerFunc.tradeInfo('--->往[' + HOSTIP + ']发送数据成功')
            
         #如果失败了应该继续往下一个ftp服务器发送数据     
         except Exception, e:
             AfaLoggerFunc.tradeInfo(e)
             AfaLoggerFunc.tradeInfo('--->往[' + HOSTIP + ']发送数据失败')
             continue

#从数据库中获取地市服务器信息
def GetFtpConfig( ):
    
    AfaLoggerFunc.tradeInfo( '--->获取地市ftp配置信息' )

    sql = " select * from fs_dsconf "
  
    records = AfaDBFunc.SelectSql( sql )
    
    if records == None:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找地市ftp配置信息异常"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False
    elif len( records ) == 0:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","没有找到地市ftp配置信息"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False
    else:
        TradeContext.ldir = records[0][5]       #本地路径
        return records
    
    
#########################################主函数#########################################
if __name__ == '__main__':
    
    AfaLoggerFunc.tradeInfo( '*************非税中心单位签约数据导出开始*************' )

    #获取地市ftp服务配置信息
    ftpInfo = GetFtpConfig( )
    
    if ftpInfo:
    
        AfaLoggerFunc.tradeInfo( TradeContext.ldir )
        
        filename  =  "abdt_unitinfo.del"
        
        #导出单位协议签约数据
        ExpUnitInfo( filename )
        
        #往所有地市服务器发送导出的签约数据
        PutFile( ftpInfo ,filename,filename)
    
    AfaLoggerFunc.tradeInfo( '*************非税中心单位签约数据导出结束*************' )
