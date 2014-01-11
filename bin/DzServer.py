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


#根据位移量计算日期
def getTimeFromNow( offsetDays, format = "%Y%m%d" ):
    secs = time.time( ) + offsetDays * 3600 * 24
    return time.strftime( format, time.localtime( secs ) )


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


def runStatus(sysID, sysStatus):
    
    WrtLog('>>>修改企业对账状态')

    updSql = "UPDATE AFA_SYSTEM SET STATUS='" + sysStatus + "' WHERE SYSID='" + sysID + "'"
    
    WrtLog(updSql)
            
    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result <= 0 ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('>>>处理结果:修改企业对账状态,数据库异常')
        return False

    WrtLog('>>>修改企业对账状态 ---> 成功')

    return True

        
###########################################主函数###########################################
if __name__=='__main__':

    WrtLog ( ':::进入对账入口程序程序(DzServer.py)' )

    #读取定时调度程序的配置参数
    if ( not GetCronConfig() ) :
        sys.exit(-1)

    try:
        
        iParamNum = len(sys.argv)


        WrtLog( '>>>参数个数=' +  str(iParamNum))


        if iParamNum == 3:
            #第一个参数：应用代码
            sSysID = sys.argv[1].strip()
            WrtLog( '>>>第一个参数：应用代码=' +  sSysID)
    
    
            #第二个参数：开关标志
            sStatus = sys.argv[2].strip()
            WrtLog( '>>>第二个参数：开关标志=' +  sStatus)

            #修改系统状态
            if not runStatus(sSysID, sStatus):
                sys.exit(-1)
                
        else:
            WrtLog ( '调用参数非法' )
            sys.exit(-1)


#        if iParamNum < 4:
#            WrtLog ( '调用参数非法' )
#            sys.exit(-1)
#
#        else:
#        
#            #第一个参数：应用代码
#            sSysID = sys.argv[1].strip()
#            WrtLog( '>>>第一个参数：应用代码=' +  sSysID)
#    
#    
#            #第二个参数：时间位移量
#            iDateOffSet = int(sys.argv[2].strip())
#            sDzDate     =  getTimeFromNow(iDateOffSet)
#            WrtLog( '>>>第二个参数：对账日期=' +  sDzDate)
#    
#    
#            #第三个参数：对账程序
#            sDzProc = sys.argv[3].strip()
#            WrtLog( '>>>第三个参数：对账程序=' +  sDzProc)
#    
#    
#            #第四个参数以后全部为对账程序的参数
#            sParamStr = ""
#            for i in range(4, iParamNum):
#                sParamStr =  sParamStr + ' ' + sys.argv[i].strip()
#    
#    
#            sCommandStr = 'python ' + os.environ['AFAP_HOME'] + sDzProc + sParamStr % (sDzDate)
#            WrtLog( '运行对账程序名称=' +  sCommandStr )
#    
#            
#            #修改系统状态(关闭)
#            if not runStatus(sSysID, '0'):
#                sys.exit(-1)
#
#                
#            #os.system(sCommandStr + ' &')
#    
#    
#            #修改系统状态(启动)
#            if not runStatus(sSysID, '1'):
#                sys.exit(-1)

    except Exception, e:
        WrtLog( ">>>对账程序严重错误:" + str(e) )
        sys.exit(-1)
