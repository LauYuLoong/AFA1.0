# -*- coding: gbk -*-
################################################################################
# 文件名称：CronServer.py
# 文件标识：
# 摘    要：定时调度服务程序
#
# 当前版本：1.0
# 作    者：XZH
# 完成日期：2006年9月8日
#
# 取代版本：
# 原 作 者：
# 完成日期：
################################################################################
import TradeContext, LoggerHandler, sys, os, time, AfaDBFunc, AfaUtilTools, ConfigParser
from types import *


cronLogger = LoggerHandler.getLogger( 'cron' )


#读取批量配置文件中信息
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
        print '读取配置文件异常:' + str(e)
        return False

#=========================日志==================================================
def WrtLog(logstr):

    if ( TradeContext.existVariable('CRON_TRACE') ):
        
        if ( TradeContext.CRON_TRACE   == 'off' ):
            #不输出日志
            return True

        elif ( TradeContext.CRON_TRACE == 'file' ):
            #向文件输出
            cronLogger.info(logstr)

        elif ( TradeContext.CRON_TRACE == 'all' ):
            #向文件和屏幕同时输出
            cronLogger.info(logstr)
            print logstr

        elif ( TradeContext.CRON_TRACE == 'stdout' ):
            #向屏幕输出
            print logstr

    else:
        #默认向文件和屏幕同时输出
        cronLogger.info(logstr)
        print logstr

    return True



#=========================读取定时调度配置信息==================================
def GetCronInfo( CfgFileName = None ):

    try:
        TradeContext.TASKLIST = []

        sqlStr = "SELECT TASKID,YEAR,MONTH,DAY,HOUR,MINUTE,WDAY,PROCNAME,RUNTIME,NOTE1,NOTE2,TASKNAME FROM AFA_CRONADM WHERE STATUS='1' ORDER BY TASKID ASC"
        records = AfaDBFunc.SelectSql( sqlStr )
        if ( records == None ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            WrtLog('>>>处理结果:读取定时调度配置信息失败,数据库异常')
            return False

        if ( len(records)==0 ):
            WrtLog('>>>处理结果:没有任何定时调度配置')
            return True

        AfaUtilTools.ListFilterNone( records )

        WrtLog("============================================================")
        for i in range(0, len(records)) :
            TradeContext.TASKLIST.append([])
            TradeContext.TASKLIST[i].append(records[i][0].strip())     #任务ID
            TradeContext.TASKLIST[i].append(records[i][1].strip())     #年
            TradeContext.TASKLIST[i].append(records[i][2].strip())     #月
            TradeContext.TASKLIST[i].append(records[i][3].strip())     #日
            TradeContext.TASKLIST[i].append(records[i][4].strip())     #时
            TradeContext.TASKLIST[i].append(records[i][5].strip())     #分
            TradeContext.TASKLIST[i].append(records[i][6].strip())     #星期
            TradeContext.TASKLIST[i].append(records[i][7].strip())     #程序名称
            TradeContext.TASKLIST[i].append(records[i][8].strip())     #上次运行时间
            TradeContext.TASKLIST[i].append(records[i][9].strip())     #备注1
            TradeContext.TASKLIST[i].append(records[i][10].strip())    #备注2
            TradeContext.TASKLIST[i].append(records[i][11].strip())    #任务名称

            WrtLog("任务编码=" + records[i][0] + " 任务名称=" + records[i][11] + " 执行时间=" + records[i][1] + " " + records[i][2] + " " + records[i][3] + " " + records[i][4] + " " + records[i][5] + " " + records[i][6])
            WrtLog("程序名称=" + records[i][7])
            WrtLog("============================================================")

        return True

    except Exception, e:
        WrtLog( ">>>读取定时调度配置信息异常:" + str(e) )
        return False


#=========================判断该程序是否可以运行================================
def ChkRunStatus(st, stime):

    #WrtLog(st[1] + " " + st[2] + " " + st[3] + " " + st[4] + " " + st[5] + " " + st[6] + " [" + st[7] + "]")

    #上次运行时间
    preRunTime = st[8]
    if len(preRunTime)==0 or len(preRunTime)!=13 or preRunTime=='0000000000000' :
        return True

    #年-月-日-时-分(某年)
    if st[1]!='*' and st[2]!='*' and st[3]!='*' and st[4]!='*' and st[5]!='*':
        WrtLog('>>>年-月-日-时-分(某年):')
        return True

    #月-日-时-分(每年)
    if st[2]!='*' and st[3]!='*' and st[4]!='*' and st[5]!='*':
        WrtLog('>>>月-日-时-分(每年)')
        if long(preRunTime[0:4]) != long(stime.tm_year):
            return True

    #日-时-分(每月)
    if st[3]!='*' and st[4]!='*' and st[5]!='*':
        WrtLog('>>>日-时-分(每月)')
        if long(preRunTime[4:6]) != long(stime.tm_mon):
            return True

    #时-分(每天)
    if st[4]!='*' and st[5]!='*':
        WrtLog('>>>时-分(每天)')
        if long(preRunTime[6:8]) != long(stime.tm_mday):
            return True

    #分(每小时)
    if st[5]!='*':
        WrtLog('>>>分(每小时)')
        if long(preRunTime[8:10]) != long(stime.tm_hour):
            return True

    #星期-时-分(每周)
    if st[6]!='*' and st[4]!='*' and st[5]!='*':
        WrtLog('>>>星期-时-分(每周)')
        if long(preRunTime[12:13]) != long(stime.tm_wday):
            return True

    #分
    if st[1]=='*' and st[2]=='*' and st[3]=='*' and st[4]=='*' and st[5]=='*':
        WrtLog('>>>每分钟')
        return True

    WrtLog('>>>该作业执行时间不符合要求,请检查')

    return False
    
    
###########################################主函数###########################################
if __name__=='__main__':

    print ''
    print ':::启动定时调度程序(CronServer.py)'
    print ''


    #读取定时调度程序的配置参数
    if ( not GetCronConfig() ) :
        sys.exit(-1)
            
    try:

        WrtLog('**********启动定时调度开始**********')

        #列表初始化
        TradeContext.TASKLIST = []


        #读取定时调度配置信息(第一次)
        if ( not GetCronInfo() ) :
            sys.exit(-1)


        iNum = 1
        while ( 1==1 ):
    
            #刷新定时调度的任务列表
            if ( iNum == (long)(TradeContext.CRON_CYCTIME) ) :

                #获取系统时间
                stime  = time.localtime( time.time( ) )

                #读取定时调度配置信息
                if ( not GetCronInfo() ) :
                    break

                #计数器初始化
                iNum = 0

            #读取定时调度配置信息
            for i in range(0, len(TradeContext.TASKLIST)):
    
                #获取系统时间
                #stime  = time.localtime( time.time( ) )
                sYEAR  = str(stime.tm_year)
                sMONTH = str(stime.tm_mon)
                sDAY   = str(stime.tm_mday)
                sHOUR  = str(stime.tm_hour)
                sMIN   = str(stime.tm_min)
                sWDAY  = str(stime.tm_wday)
    
                lTask = TradeContext.TASKLIST[i]
                if (lTask[1] != '*') and (long(sYEAR)  != long(lTask[1])) :         #年
                    continue
    
                if (lTask[2] != '*') and (long(sMONTH) != long(lTask[2])) :         #月
                    continue
    
                if (lTask[3] != '*') and (long(sDAY)   != long(lTask[3])) :         #日
                    continue
    
                if (lTask[4] != '*') and (long(sHOUR)  != long(lTask[4])) :         #时
                    continue
    
                if (lTask[5] != '*') and (long(sMIN)   != long(lTask[5])) :         #分
                    continue
    
                if (lTask[6] != '*') and (long(sWDAY)  != long(lTask[6])) :         #星期
                    continue

                #判断该程序是否可以运行
                if not ChkRunStatus(lTask, stime) :
                    continue

                
                #add by guanbj 20080628 start

                cmd = "ps -ef | grep '" + lTask[7] + "' | grep -v grep"
                handler = os.popen(cmd,'r')
                handler_line = handler.readline()
                handler.close()

                if len(handler_line) > 0:
                    WrtLog( '>>>程序:[ ' + lTask[7] + ' ]正在运行中' )
                    continue

                #add by guanbj 20080628 end
                
                sRunTime = ""
                sRunTime = sYEAR.rjust(4,'0')                   #年
                sRunTime = sRunTime + sMONTH.rjust(2,'0')       #月
                sRunTime = sRunTime + sDAY.rjust(2,  '0')       #日
                sRunTime = sRunTime + sHOUR.rjust(2, '0')       #时
                sRunTime = sRunTime + sMIN.rjust(2,  '0')       #分
                sRunTime = sRunTime + sWDAY.rjust(1, '0')       #星期
                    
                #判断该程序是否可以运行
                WrtLog( ':::[' + sRunTime + ']:运行程序=[ ' + lTask[7] + ' ]' )
                os.system(lTask[7] + ' &')


                #修改运行时间
                sqlStr = "UPDATE AFA_CRONADM SET RUNTIME='" + sRunTime + "'" + " WHERE TASKID='" + lTask[0] + "'"
                result = AfaDBFunc.UpdateSqlCmt( sqlStr )
                if ( result < 0 ):
                    WrtLog( AfaDBFunc.sqlErrMsg )
                    WrtLog('>>>处理结果:修改定时调度运行时间,数据库异常')
                    sys.exit(-1)

            #睡眠(一分钟)
            time.sleep(60)

            WrtLog( ':::' + str(time.localtime(time.time())) )

            #时间记数器
            iNum = iNum + 1

        WrtLog('**********启动定时调度结束**********')

        sys.exit(0)

    except Exception, e:
        WrtLog( ">>>定时调度服务程序严重错误:" + str(e) )
        sys.exit(-1)
