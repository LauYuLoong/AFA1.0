################################################################################
# �� �� ��: ADBUpdateTransdtlRev
# ����˵��: �����ɷѽ��׵��������سɹ�����·��ؽ����Ϣ
# �޸ļ�¼: 
# ��    ע: ֻ���ڳ���ʧ�ܵ�����²ż�¼ʧ����Ϣ
# ��    ��: 
###############################################################################
import TradeContext, sys, os, time, AfaDBFunc, AfaUtilTools, ConfigParser,AfaLoggerFunc,ftplib
from types import *

def ADBUpdateTransdtlRev( ):
    sqlupdate = ""
   
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ����ԭ�������׽����Ϣ<<<<<<<')
   
    sqlupdate = sqlupdate + "update afa_maintransdtl set "
    sqlupdate = sqlupdate + " corpcode = '"+TradeContext.errorCode.strip()+"' "
    sqlupdate = sqlupdate + ", errorMsg = '"+TradeContext.errorMsg.strip()+"' "
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
   
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
   
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
   
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣ�ɹ�<<<<<<<')
        return True
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣʧ��<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','δ����ԭʼ����'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣʧ��<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '����ԭ����״̬ʧ��' + AfaDBFunc.sqlErrMsg
        return False
        
def putFile(LocalFileName,RemoteFileName):
    
    AfaLoggerFunc.tradeInfo( '>>>FTP�ϴ��ļ�' )
    
    try:
        if not os.path.exists(TradeContext.CORP_LDIR + "/" + LocalFileName):
            raise Exception,"�ϴ��ļ�[" + TradeContext.CORP_LDIR + "/" + LocalFileName + "]������"
        
        #����FTPʵ��
        ftp_p = ftplib.FTP()
        #����FTP
        ftp_p.connect(TradeContext.CORP_HOSTPORT,TradeContext.CORP_HOSTIP)
        #��½FTP
        ftp_p.login(TradeContext.CORP_USERNO,TradeContext.CORP_PASSWD)
        #�ƶ���Զ��FTP������ָ��Ŀ¼��
        ftp_p.cwd(CORP_RDIR)
        #�Զ�ȡ��ʽ�򿪱����ļ�
        file_handler = open(TradeContext.CORP_LDIR + "/" + LocalFileName,'rb')
        #��ȡ�����ļ�����,��д�뵽Զ��FTP������ָ���ļ�
        ftp_p.storbinary("STOR " + TradeContext.CORP_RDIR + "/" + RemoteFileName,file_handler)
        #�رձ����ļ�
        file_handler.close()
        #�˳�FTP
        ftp_p.quit()
        
        AfaLoggerFunc.tradeInfo("�ļ�[" + TradeContext.CORP_LDIR + "/" + LocalFileName + "]�ϴ��ɹ�")
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False