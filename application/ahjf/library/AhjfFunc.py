################################################################################
# 函 数 名: ADBUpdateTransdtlRev
# 功能说明: 冲正缴费交易第三方返回成功后更新返回结果信息
# 修改记录: 
# 备    注: 只有在冲正失败的情况下才记录失败信息
# 范    例: 
###############################################################################
import TradeContext, sys, os, time, AfaDBFunc, AfaUtilTools, ConfigParser,AfaLoggerFunc,ftplib
from types import *

def ADBUpdateTransdtlRev( ):
    sqlupdate = ""
   
    AfaLoggerFunc.tradeInfo( '>>>>>>>开始更新原冲正交易结果信息<<<<<<<')
   
    sqlupdate = sqlupdate + "update afa_maintransdtl set "
    sqlupdate = sqlupdate + " corpcode = '"+TradeContext.errorCode.strip()+"' "
    sqlupdate = sqlupdate + ", errorMsg = '"+TradeContext.errorMsg.strip()+"' "
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
   
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
   
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
   
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原冲正交易结果信息成功<<<<<<<')
        return True
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原冲正交易结果信息失败<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','未发现原始交易'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>更新原冲正交易结果信息失败<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新原交易状态失败' + AfaDBFunc.sqlErrMsg
        return False
        
def putFile(LocalFileName,RemoteFileName):
    
    AfaLoggerFunc.tradeInfo( '>>>FTP上传文件' )
    
    try:
        if not os.path.exists(TradeContext.CORP_LDIR + "/" + LocalFileName):
            raise Exception,"上传文件[" + TradeContext.CORP_LDIR + "/" + LocalFileName + "]不存在"
        
        #建立FTP实例
        ftp_p = ftplib.FTP()
        #连接FTP
        ftp_p.connect(TradeContext.CORP_HOSTPORT,TradeContext.CORP_HOSTIP)
        #登陆FTP
        ftp_p.login(TradeContext.CORP_USERNO,TradeContext.CORP_PASSWD)
        #移动到远程FTP服务器指定目录下
        ftp_p.cwd(CORP_RDIR)
        #以读取方式打开本地文件
        file_handler = open(TradeContext.CORP_LDIR + "/" + LocalFileName,'rb')
        #读取本地文件内容,并写入到远程FTP服务器指定文件
        ftp_p.storbinary("STOR " + TradeContext.CORP_RDIR + "/" + RemoteFileName,file_handler)
        #关闭本地文件
        file_handler.close()
        #退出FTP
        ftp_p.quit()
        
        AfaLoggerFunc.tradeInfo("文件[" + TradeContext.CORP_LDIR + "/" + LocalFileName + "]上传成功")
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False