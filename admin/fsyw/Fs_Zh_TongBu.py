############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰���ĵ�λǩԼ���ݵ���
#
# ��ǰ�汾��1.0
# ��    �ߣ�������
# ������ڣ�2010��06��28��
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import AfaDBFunc,ConfigParser,os, AfaLoggerFunc,ftplib
from types import *

#������˰��λǩԼ����
def ExpUnitInfo( filename ):

    AfaLoggerFunc.tradeInfo( '--->��ʼ������λЭ��ǩԼ����' )
    try:
      
      os.system("db2 connect to maps")
      
      #cmd = "db2 \" export to '" + TradeContext.ldir + "/" + filename + "' of del select * from abdt_unitinfo where appno in ('AG2008','AG2012')\" "
      #begin 20110811 �޸ģ���Ϊ�ߺ�������������֧�з�˰�뵱�ط�˰��012�໥��ͻ�������������б���015������AG2104�����б���015��Ӧ
      cmd = "db2 \" export to '" + TradeContext.ldir + "/" + filename + "' of del select * from abdt_unitinfo where appno in ('AG2008','AG2012','AG2104')\" "
      #end 20110811
      os.system( cmd )
      
      os.system("db2 disconnect maps")
      
      return True
    
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('������λЭ��ǩԼ�����쳣')
        return False
    

#�ѵ�������������ftp�����еķ�������
def PutFile( ftpInfo,LocalFileName,RemoteFileName ):
    
    for record in ftpInfo:
         HOSTIP   = record[1]
         USERNO   = record[2]
         PASSWD   = record[3]
         RDIR     = record[4]
         LDIR     = record[5]
         
         try:
         
            if not os.path.exists(LDIR + "/" + LocalFileName):
                raise Exception,"�ϴ��ļ�[" + LDIR + "/" + LocalFileName + "]������"
            
            AfaLoggerFunc.tradeInfo('--->��ʼ��[' + HOSTIP + ']��������')
           
            #����FTPʵ��
            ftp_p = ftplib.FTP()
            #����FTP
            ftp_p.connect(HOSTIP,'21')
            #��½FTP
            ftp_p.login(USERNO,PASSWD)
            #�ƶ���Զ��FTP������ָ��Ŀ¼��
            #ftp_p.cwd(RDIR)
            #�Զ�ȡ��ʽ�򿪱����ļ�
            file_handler = open(LDIR + "/" + LocalFileName,'rb')
            #��ȡ�����ļ�����,��д�뵽Զ��FTP������ָ���ļ�
            ftp_p.storbinary("STOR " + RDIR + "/" + RemoteFileName,file_handler)
            #�رձ����ļ�
            file_handler.close()
            #�˳�FTP
            ftp_p.quit()
           
            AfaLoggerFunc.tradeInfo('--->��[' + HOSTIP + ']�������ݳɹ�')
            
         #���ʧ����Ӧ�ü�������һ��ftp��������������     
         except Exception, e:
             AfaLoggerFunc.tradeInfo(e)
             AfaLoggerFunc.tradeInfo('--->��[' + HOSTIP + ']��������ʧ��')
             continue

#�����ݿ��л�ȡ���з�������Ϣ
def GetFtpConfig( ):
    
    AfaLoggerFunc.tradeInfo( '--->��ȡ����ftp������Ϣ' )

    sql = " select * from fs_dsconf "
  
    records = AfaDBFunc.SelectSql( sql )
    
    if records == None:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ���ftp������Ϣ�쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False
    elif len( records ) == 0:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","û���ҵ�����ftp������Ϣ"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False
    else:
        TradeContext.ldir = records[0][5]       #����·��
        return records
    
    
#########################################������#########################################
if __name__ == '__main__':
    
    AfaLoggerFunc.tradeInfo( '*************��˰���ĵ�λǩԼ���ݵ�����ʼ*************' )

    #��ȡ����ftp����������Ϣ
    ftpInfo = GetFtpConfig( )
    
    if ftpInfo:
    
        AfaLoggerFunc.tradeInfo( TradeContext.ldir )
        
        filename  =  "abdt_unitinfo.del"
        
        #������λЭ��ǩԼ����
        ExpUnitInfo( filename )
        
        #�����е��з��������͵�����ǩԼ����
        PutFile( ftpInfo ,filename,filename)
    
    AfaLoggerFunc.tradeInfo( '*************��˰���ĵ�λǩԼ���ݵ�������*************' )
