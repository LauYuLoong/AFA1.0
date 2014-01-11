# -*- coding: gbk -*-
################################################################################
# �ļ����ƣ�CronServer.py
# �ļ���ʶ��
# ժ    Ҫ����ʱ���ȷ������
#
# ��ǰ�汾��1.0
# ��    �ߣ�XZH
# ������ڣ�2006��9��8��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
################################################################################
import TradeContext, LoggerHandler, sys, os, time, AfaDBFunc, AfaUtilTools, ConfigParser
from types import *

cronLogger = LoggerHandler.getLogger( 'cron' )


#����λ������������
def getTimeFromNow( offsetDays, format = "%Y%m%d" ):
    secs = time.time( ) + offsetDays * 3600 * 24
    return time.strftime( format, time.localtime( secs ) )


#��ȡ���������ļ�����Ϣ
def GetCronConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.CRON_TRACE   = config.get('CRON', 'TRACE')
        TradeContext.CRON_CYCTIME = config.get('CRON', 'CYCTIME')

        #print ':::CRON_TRACE   =' + TradeContext.CRON_TRACE
        #print ':::CRON_CYCTIME =' + TradeContext.CRON_CYCTIME

        return True

    except Exception, e:
        print '��ȡ�����ļ��쳣:' + str(e)
        return False

#=========================��־==================================================
def WrtLog(logstr):

    if ( TradeContext.existVariable('CRON_TRACE') ):
        
        if ( TradeContext.CRON_TRACE   == 'off' ):
            #�������־
            return True

        elif ( TradeContext.CRON_TRACE == 'file' ):
            #���ļ����
            cronLogger.info(logstr)

        elif ( TradeContext.CRON_TRACE == 'all' ):
            #���ļ�����Ļͬʱ���
            cronLogger.info(logstr)
            print logstr

        elif ( TradeContext.CRON_TRACE == 'stdout' ):
            #����Ļ���
            print logstr

    else:
        #Ĭ�����ļ�����Ļͬʱ���
        cronLogger.info(logstr)
        print logstr

    return True


def runStatus(sysID, sysStatus):
    
    WrtLog('>>>�޸���ҵ����״̬')

    updSql = "UPDATE AFA_SYSTEM SET STATUS='" + sysStatus + "' WHERE SYSID='" + sysID + "'"
    
    WrtLog(updSql)
            
    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result <= 0 ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('>>>������:�޸���ҵ����״̬,���ݿ��쳣')
        return False

    WrtLog('>>>�޸���ҵ����״̬ ---> �ɹ�')

    return True

        
###########################################������###########################################
if __name__=='__main__':

    WrtLog ( ':::���������ڳ������(DzServer.py)' )

    #��ȡ��ʱ���ȳ�������ò���
    if ( not GetCronConfig() ) :
        sys.exit(-1)

    try:
        
        iParamNum = len(sys.argv)


        WrtLog( '>>>��������=' +  str(iParamNum))


        if iParamNum == 3:
            #��һ��������Ӧ�ô���
            sSysID = sys.argv[1].strip()
            WrtLog( '>>>��һ��������Ӧ�ô���=' +  sSysID)
    
    
            #�ڶ������������ر�־
            sStatus = sys.argv[2].strip()
            WrtLog( '>>>�ڶ������������ر�־=' +  sStatus)

            #�޸�ϵͳ״̬
            if not runStatus(sSysID, sStatus):
                sys.exit(-1)
                
        else:
            WrtLog ( '���ò����Ƿ�' )
            sys.exit(-1)


#        if iParamNum < 4:
#            WrtLog ( '���ò����Ƿ�' )
#            sys.exit(-1)
#
#        else:
#        
#            #��һ��������Ӧ�ô���
#            sSysID = sys.argv[1].strip()
#            WrtLog( '>>>��һ��������Ӧ�ô���=' +  sSysID)
#    
#    
#            #�ڶ���������ʱ��λ����
#            iDateOffSet = int(sys.argv[2].strip())
#            sDzDate     =  getTimeFromNow(iDateOffSet)
#            WrtLog( '>>>�ڶ�����������������=' +  sDzDate)
#    
#    
#            #���������������˳���
#            sDzProc = sys.argv[3].strip()
#            WrtLog( '>>>���������������˳���=' +  sDzProc)
#    
#    
#            #���ĸ������Ժ�ȫ��Ϊ���˳���Ĳ���
#            sParamStr = ""
#            for i in range(4, iParamNum):
#                sParamStr =  sParamStr + ' ' + sys.argv[i].strip()
#    
#    
#            sCommandStr = 'python ' + os.environ['AFAP_HOME'] + sDzProc + sParamStr % (sDzDate)
#            WrtLog( '���ж��˳�������=' +  sCommandStr )
#    
#            
#            #�޸�ϵͳ״̬(�ر�)
#            if not runStatus(sSysID, '0'):
#                sys.exit(-1)
#
#                
#            #os.system(sCommandStr + ' &')
#    
#    
#            #�޸�ϵͳ״̬(����)
#            if not runStatus(sSysID, '1'):
#                sys.exit(-1)

    except Exception, e:
        WrtLog( ">>>���˳������ش���:" + str(e) )
        sys.exit(-1)
