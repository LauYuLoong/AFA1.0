###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：安徽非税下载缴款书信息
#
# 当前版本：1.0
# 作    者：WJJ
# 完成日期：2007年10月15日
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import ConfigParser, sys, AfaDBFunc, Party3Context, AfaUtilTools
import os, HostContext, AfaAfeFunc, AfaLoggerFunc, time
from types import *

#读取配置文件中信息
def GetConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )
        TradeContext.BATCH_TRACE    = config.get('FS_AFE', 'TRACE')
        TradeContext.BATCH_ERR_TRACE= config.get('FS_AFE', 'ERR_TRACE')

        TradeContext.BATCH_HOSTIP   =   config.get('FS_AFE', 'HOSTIP')
        TradeContext.BATCH_USERNO   =   config.get('FS_AFE', 'USERNO')
        TradeContext.BATCH_PASSWD   =   config.get('FS_AFE', 'PASSWD')
        TradeContext.BATCH_RDIR     =   config.get('FS_AFE', 'RDIR')
        TradeContext.BATCH_LDIR     =   config.get('FS_AFE', 'LDIR')

        return True

    except Exception, e:
        WrtErrLog(e)
        return False

#FTP处理函数
def ftpfile( sfilename, rfilename):

    try:
        #创建文件
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/AhfsFtpJks' + '.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.BATCH_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.BATCH_USERNO + ' ' + TradeContext.BATCH_PASSWD + '\n')

        #下载文件
        ftpFp.write('cd '  + TradeContext.BATCH_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.BATCH_LDIR + '\n')
        ftpFp.write('bin ' + '\n')
        ftpFp.write('get ' + rfilename + ' ' + sfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        os.system(ftpcmd)

        return 0

    except Exception, e:
        WrtErrLog(e)
        AfaLoggerFunc.tradeInfo('FTP处理异常')
        return -1

def ChkAppStatus():
    sqlstr  =   "select status from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino ='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        AfaLoggerFunc.tradeInfo('查找应用状态库失败')
        return False
    elif len( records ) == 1:
        if records[0][0].strip() == '1':
            return True
        else:
            AfaLoggerFunc.tradeInfo('应用状态没有开启')
            return False
    else:
        AfaLoggerFunc.tradeInfo('应用签约异常')
        return False

###########################################主函数###########################################
if __name__=='__main__':
    AfaLoggerFunc.tradeInfo('**********安徽非税缴款书信息下载开始**********')

    #初始化TradeContext
    TradeContext.workDate       =   AfaUtilTools.GetSysDate( )
    TradeContext.workTime       =   AfaUtilTools.GetSysTime( )
    TradeContext.zoneno         =   ""
    TradeContext.brno           =   ""
    TradeContext.teller         =   ""
    TradeContext.authPwd        =   ""
    TradeContext.termId         =   ""
    TradeContext.TransCode      =   "8440"

    #begin 20100525 蔡永贵修改 增加村镇银行业务编码查询条件
    #sqlstr  = "select distinct busino from abdt_unitinfo where appno='AG2008'"
    #sqlstr  = "select distinct busino, appno from abdt_unitinfo where appno in ('AG2008','AG2012')"
    sqlstr  = " select busino,bankno from fs_businoinfo "
    #end

    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None:
        AfaLoggerFunc.tradeInfo("查找单位信息表异常" + AfaDBFunc.sqlErrMsg)
        sys.exit(1)

    elif len(records)==0 :
        AfaLoggerFunc.tradeInfo("没有任何单位信息")
        sys.exit(1)


    for i in range( len(records) ):

        #begin 20100525 蔡永贵修改
        #TradeContext.appNo        = 'AG2008'
        TradeContext.bankbm        = records[i][1].strip()
        if( TradeContext.bankbm == '012' ):
            TradeContext.appNo = 'AG2008';
        else:
            TradeContext.appNo = 'AG2012';
        #end

        TradeContext.busiNo       = records[i][0].strip()

        AfaLoggerFunc.tradeInfo("业务编码:" + TradeContext.appNo)
        AfaLoggerFunc.tradeInfo("单位编码:" + TradeContext.busiNo)

        #=============判断应用状态========================
        if not ChkAppStatus( ) :
            AfaLoggerFunc.tradeInfo('**********安徽非税应用状态不正常**********')
            continue

        #----------------缴款书信息通过socket向财政取得缴款书放在afe上，afa去afe去缴款书信息文件
        if not GetConfig() :
            AfaLoggerFunc.tradeInfo('获取ftp配置文件失败')
            sys.exit(1)

        #拼成第三方报文
        TradeContext.TemplateCode   =   "3001"

        #begin 20100525 蔡永贵修改
        #TradeContext.sysId          =   "AG2008"
        TradeContext.sysId          =   TradeContext.appNo
        #end

        #=============与第三方通讯通讯====================
        TradeContext.__respFlag__='0'
        AfaAfeFunc.CommAfe()

        if( TradeContext.errorCode != '0000' ):
            AfaLoggerFunc.tradeInfo("第三方返回错误，程序退出")
            continue

        else :
            if (  ftpfile ( Party3Context.FileName ,Party3Context.FileName ) <0 ):
                AfaLoggerFunc.tradeInfo("没有下载到文件")
                continue

            #开始读取文件
            try:
                fp          =   open(TradeContext.BATCH_LDIR+Party3Context.FileName,"rb")
                recs        =   fp.read()

                if not recs :
                    AfaLoggerFunc.tradeInfo( "文件为空" )
                    continue

            except Exception, e:
                AfaLoggerFunc.tradeInfo( "没有生成文件或者文件为空" )
                continue


            #将记录集写到数据库中

            #begin 20100526 蔡永贵修改，在最后增加bankno字段
            #fields  =   "AFC001,AFA031,AFC163,AFC187,AFC183,AFC157,AFC181,AFA040,AFC180,AFA051,AFC166,AFC155,AFC153,AFC154,AFA183,AFA184,AFA185,AFA091, AAA010,DATE,TIME"
            fields  =   "AFC001,AFA031,AFC163,AFC187,AFC183,AFC157,AFC181,AFA040,AFC180,AFA051,AFC166,AFC155,AFC153,AFC154,AFA183,AFA184,AFA185,AFA091, AAA010,DATE,TIME,BANKNO"
            #end

            sqlstr  =   "INSERT INTO FS_FC70(" + fields + ") VALUES("

            #第一个数据不是记录而是数据种类
            rec     =   recs.split( chr(12) )

            #print rec,"记录条数：",len(rec)

            sep         =   chr(31)
            itemCnt     =   len( rec[1].split( sep ) )

            for i in range( 1,len(rec) ):
                sqlstr1 =   sqlstr

                #检测第二条记录是否为空
                if not rec[i]:
                    AfaLoggerFunc.tradeInfo ( "当前字段已经为空" )
                    break

                for item in rec[i].split( sep ):
                    sqlstr1  =  sqlstr1   +  "'" + item + "',"

                sqlstr1         =   sqlstr1 + "'" + TradeContext.workDate + "',"

                #begin 20100526 蔡永贵修改
                #sqlstr1         =   sqlstr1 + "'" + TradeContext.workTime + "')"
                sqlstr1         =   sqlstr1 + "'" + TradeContext.workTime + "',"
                sqlstr1         =   sqlstr1 + "'" + TradeContext.bankbm   + "')"
                #end

                AfaLoggerFunc.tradeInfo( sqlstr1 )

                if( AfaDBFunc.InsertSqlCmt( sqlstr1 ) < 1 ):
                    AfaLoggerFunc.tradeInfo ( "插入数据库失败:"  + AfaDBFunc.sqlErrMsg )

    AfaLoggerFunc.tradeInfo('**********安徽非税缴款书信息下载结束**********')
    sys.exit(0)

