# -*- coding: gbk -*-
################################################################################
#   农信银系统.系统调度操作模块
#===============================================================================
#   程序文件:   rccpsCronFunc.py
#   作    者:   关彬捷
#   修改时间:   2008-06-14
################################################################################

import AfaLoggerFunc,AfaDBFunc,TradeContext, LoggerHandler, sys, os, time, AfaUtilTools, ConfigParser
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

#写日志
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


#打开系统调度
def openCron(taskid):
    #======================查询系统调度信息================================
    sql = "SELECT * FROM AFA_CRONADM WHERE TASKID = '" + taskid + "'"
    
    records = AfaDBFunc.SelectSql(sql)
    
    if records == None:
        rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog("获取系统调度[" + taskid + "]信息异常")
        return False
    
    if len(records) <= 0:
        WrtLog("系统调度表中无此调度信息[" + taskid + "]")
        return False
    
    #======================修改系统调度状态为0=============================
    sql = "UPDATE AFA_CRONADM SET STATUS = '1' WHERE TASKID = '" + taskid + "'"
    
    if not AfaDBFunc.UpdateSql(sql):
        rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog("打开系统调度[" + taskid + "]异常")
        return False
        
    WrtLog("打开系统调度[" + taskid + "]成功")
    return True
    
#关闭系统调度
def closeCron(taskid):
    #======================查询系统调度信息================================
    sql = "SELECT * FROM AFA_CRONADM WHERE TASKID = '" + taskid + "'"
    
    records = AfaDBFunc.SelectSql(sql)
    
    if records == None:
        rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog("获取系统调度[" + taskid + "]信息异常")
        return False
    
    if len(records) <= 0:
        WrtLog("系统调度表中无此调度信息[" + taskid + "]")
        return False
    
    #======================修改系统调度状态为0=============================
    sql = "UPDATE AFA_CRONADM SET STATUS = '0' WHERE TASKID = '" + taskid + "'"
    
    if not AfaDBFunc.UpdateSql(sql):
        rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog("关闭系统调度[" + taskid + "]异常")
        return False
        
    WrtLog("关闭系统调度[" + taskid + "]成功")
    return True
    
#退出系统调度流程
def cronExit(code,msg):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    raise Exception,msg
    

#格式化文件
def FormatFile(ProcType, FLDName, sFileName, dFileName):

#    WrtLog('>>>格式化文件:' + ProcType + ' ' + sFileName + ' ' + dFileName)

    try:

        srcFileName    = os.environ['AFAP_HOME'] + '/data/rccps/host/' + sFileName
        dstFileName    = os.environ['AFAP_HOME'] + '/data/rccps/host/' + dFileName

        if (ProcType == "1"):
            #ascii->ebcd
            #调用格式:cvt2ebcdic -T 源文本文件 -P 目标物理文件 -F fld格式文件 [-D 间隔符 ]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/rccps/cvt/cvt2ebcdic'
            #关彬捷  20081126  参数化设置fld文件
            #fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/rccps01.fld'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/' + FLDName
            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName + " -D '|' "

        else:
            #ebcd->ascii
            #调用格式:cvt2ascii -T 生成文本文件 -P 物理文件 -F fld文件 [-D 间隔-符] [-S] [-R]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/rccps/cvt/cvt2ascii'
            #关彬捷  20081126  参数化设置fld文件
            #fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/rccps02.fld'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/' + FLDName
            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName + " -D '|' "

        #WrtLog('>>>' + cmdstr)
        #ret = -1
        WrtLog('>>>外调格式转换程序开始============')   #2007824
        WrtLog(cmdstr)
        ret = os.system(cmdstr)                         #2007824
        if ( ret != 0 ):                                #2007824
            ret = False                                 #2007824
        else:                                           #2007824
            ret = True                                  #2007824
        #return 0                                       #2007824
        WrtLog('>>>外调格式转换程序结束============')   #2007824

        return ret
        
    except Exception, e:
        WrtLog(e)
        WrtLog('格式化文件异常')
        return False
