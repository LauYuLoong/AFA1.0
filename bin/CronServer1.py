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



#=========================��ȡ��ʱ����������Ϣ==================================
def GetCronInfo( CfgFileName = None ):

    try:
        TradeContext.TASKLIST = []

        sqlStr = "SELECT TASKID,YEAR,MONTH,DAY,HOUR,MINUTE,WDAY,PROCNAME,RUNTIME,NOTE1,NOTE2,TASKNAME FROM AFA_CRONADM WHERE STATUS='1' ORDER BY TASKID ASC"
        records = AfaDBFunc.SelectSql( sqlStr )
        if ( records == None ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            WrtLog('>>>������:��ȡ��ʱ����������Ϣʧ��,���ݿ��쳣')
            return False

        if ( len(records)==0 ):
            WrtLog('>>>������:û���κζ�ʱ��������')
            return True

        AfaUtilTools.ListFilterNone( records )

        WrtLog("============================================================")
        for i in range(0, len(records)) :
            TradeContext.TASKLIST.append([])
            TradeContext.TASKLIST[i].append(records[i][0].strip())     #����ID
            TradeContext.TASKLIST[i].append(records[i][1].strip())     #��
            TradeContext.TASKLIST[i].append(records[i][2].strip())     #��
            TradeContext.TASKLIST[i].append(records[i][3].strip())     #��
            TradeContext.TASKLIST[i].append(records[i][4].strip())     #ʱ
            TradeContext.TASKLIST[i].append(records[i][5].strip())     #��
            TradeContext.TASKLIST[i].append(records[i][6].strip())     #����
            TradeContext.TASKLIST[i].append(records[i][7].strip())     #��������
            TradeContext.TASKLIST[i].append(records[i][8].strip())     #�ϴ�����ʱ��
            TradeContext.TASKLIST[i].append(records[i][9].strip())     #��ע1
            TradeContext.TASKLIST[i].append(records[i][10].strip())    #��ע2
            TradeContext.TASKLIST[i].append(records[i][11].strip())    #��������

            WrtLog("�������=" + records[i][0] + " ��������=" + records[i][11] + " ִ��ʱ��=" + records[i][1] + " " + records[i][2] + " " + records[i][3] + " " + records[i][4] + " " + records[i][5] + " " + records[i][6])
            WrtLog("��������=" + records[i][7])
            WrtLog("============================================================")

        return True

    except Exception, e:
        WrtLog( ">>>��ȡ��ʱ����������Ϣ�쳣:" + str(e) )
        return False


#=========================�жϸó����Ƿ��������================================
def ChkRunStatus(st, stime):

    #WrtLog(st[1] + " " + st[2] + " " + st[3] + " " + st[4] + " " + st[5] + " " + st[6] + " [" + st[7] + "]")

    #�ϴ�����ʱ��
    preRunTime = st[8]
    if len(preRunTime)==0 or len(preRunTime)!=13 or preRunTime=='0000000000000' :
        return True

    #��-��-��-ʱ-��(ĳ��)
    if st[1]!='*' and st[2]!='*' and st[3]!='*' and st[4]!='*' and st[5]!='*':
        WrtLog('>>>��-��-��-ʱ-��(ĳ��):')
        return True

    #��-��-ʱ-��(ÿ��)
    if st[2]!='*' and st[3]!='*' and st[4]!='*' and st[5]!='*':
        WrtLog('>>>��-��-ʱ-��(ÿ��)')
        if long(preRunTime[0:4]) != long(stime.tm_year):
            return True

    #��-ʱ-��(ÿ��)
    if st[3]!='*' and st[4]!='*' and st[5]!='*':
        WrtLog('>>>��-ʱ-��(ÿ��)')
        if long(preRunTime[4:6]) != long(stime.tm_mon):
            return True

    #ʱ-��(ÿ��)
    if st[4]!='*' and st[5]!='*':
        WrtLog('>>>ʱ-��(ÿ��)')
        if long(preRunTime[6:8]) != long(stime.tm_mday):
            return True

    #��(ÿСʱ)
    if st[5]!='*':
        WrtLog('>>>��(ÿСʱ)')
        if long(preRunTime[8:10]) != long(stime.tm_hour):
            return True

    #����-ʱ-��(ÿ��)
    if st[6]!='*' and st[4]!='*' and st[5]!='*':
        WrtLog('>>>����-ʱ-��(ÿ��)')
        if long(preRunTime[12:13]) != long(stime.tm_wday):
            return True

    #��
    if st[1]=='*' and st[2]=='*' and st[3]=='*' and st[4]=='*' and st[5]=='*':
        WrtLog('>>>ÿ����')
        return True

    WrtLog('>>>����ҵִ��ʱ�䲻����Ҫ��,����')

    return False
    
    
###########################################������###########################################
if __name__=='__main__':

    print ''
    print ':::������ʱ���ȳ���(CronServer.py)'
    print ''


    #��ȡ��ʱ���ȳ�������ò���
    if ( not GetCronConfig() ) :
        sys.exit(-1)
            
    try:

        WrtLog('**********������ʱ���ȿ�ʼ**********')

        #�б��ʼ��
        TradeContext.TASKLIST = []


        #��ȡ��ʱ����������Ϣ(��һ��)
        if ( not GetCronInfo() ) :
            sys.exit(-1)


        iNum = 1
        while ( 1==1 ):
    
            #ˢ�¶�ʱ���ȵ������б�
            if ( iNum == (long)(TradeContext.CRON_CYCTIME) ) :

                #��ȡϵͳʱ��
                stime  = time.localtime( time.time( ) )

                #��ȡ��ʱ����������Ϣ
                if ( not GetCronInfo() ) :
                    break

                #��������ʼ��
                iNum = 0

            #��ȡ��ʱ����������Ϣ
            for i in range(0, len(TradeContext.TASKLIST)):
    
                #��ȡϵͳʱ��
                #stime  = time.localtime( time.time( ) )
                sYEAR  = str(stime.tm_year)
                sMONTH = str(stime.tm_mon)
                sDAY   = str(stime.tm_mday)
                sHOUR  = str(stime.tm_hour)
                sMIN   = str(stime.tm_min)
                sWDAY  = str(stime.tm_wday)
    
                lTask = TradeContext.TASKLIST[i]
                if (lTask[1] != '*') and (long(sYEAR)  != long(lTask[1])) :         #��
                    continue
    
                if (lTask[2] != '*') and (long(sMONTH) != long(lTask[2])) :         #��
                    continue
    
                if (lTask[3] != '*') and (long(sDAY)   != long(lTask[3])) :         #��
                    continue
    
                if (lTask[4] != '*') and (long(sHOUR)  != long(lTask[4])) :         #ʱ
                    continue
    
                if (lTask[5] != '*') and (long(sMIN)   != long(lTask[5])) :         #��
                    continue
    
                if (lTask[6] != '*') and (long(sWDAY)  != long(lTask[6])) :         #����
                    continue

                #�жϸó����Ƿ��������
                if not ChkRunStatus(lTask, stime) :
                    continue

                
                #add by guanbj 20080628 start

                cmd = "ps -ef | grep '" + lTask[7] + "' | grep -v grep"
                handler = os.popen(cmd,'r')
                handler_line = handler.readline()
                handler.close()

                if len(handler_line) > 0:
                    WrtLog( '>>>����:[ ' + lTask[7] + ' ]����������' )
                    continue

                #add by guanbj 20080628 end
                
                sRunTime = ""
                sRunTime = sYEAR.rjust(4,'0')                   #��
                sRunTime = sRunTime + sMONTH.rjust(2,'0')       #��
                sRunTime = sRunTime + sDAY.rjust(2,  '0')       #��
                sRunTime = sRunTime + sHOUR.rjust(2, '0')       #ʱ
                sRunTime = sRunTime + sMIN.rjust(2,  '0')       #��
                sRunTime = sRunTime + sWDAY.rjust(1, '0')       #����
                    
                #�жϸó����Ƿ��������
                WrtLog( ':::[' + sRunTime + ']:���г���=[ ' + lTask[7] + ' ]' )
                os.system(lTask[7] + ' &')


                #�޸�����ʱ��
                sqlStr = "UPDATE AFA_CRONADM SET RUNTIME='" + sRunTime + "'" + " WHERE TASKID='" + lTask[0] + "'"
                result = AfaDBFunc.UpdateSqlCmt( sqlStr )
                if ( result < 0 ):
                    WrtLog( AfaDBFunc.sqlErrMsg )
                    WrtLog('>>>������:�޸Ķ�ʱ��������ʱ��,���ݿ��쳣')
                    sys.exit(-1)

            #˯��(һ����)
            time.sleep(60)

            WrtLog( ':::' + str(time.localtime(time.time())) )

            #ʱ�������
            iNum = iNum + 1

        WrtLog('**********������ʱ���Ƚ���**********')

        sys.exit(0)

    except Exception, e:
        WrtLog( ">>>��ʱ���ȷ���������ش���:" + str(e) )
        sys.exit(-1)
