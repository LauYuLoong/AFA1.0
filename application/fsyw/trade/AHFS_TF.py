###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：安徽非税下载退付信息
#
# 当前版本：1.0
# 作    者：WJJ
# 完成日期：2007年10月15日
###############################################################################
import TradeContext

TradeContext.sysType = 'cron'

import ConfigParser, AfaUtilTools, sys, AfaDBFunc, Party3Context
import os, HostContext, HostComm, AfaAfeFunc, AfaLoggerFunc, time
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
        AfaLoggerFunc.tradeInfo(e)
        return False


#FTP处理函数
def ftpfile( sfilename, rfilename):

    try:
        #创建文件
        ftpShell = os.environ['AFAP_HOME'] + '/data/ahfs/shell/AhfsFtpTf' + '.sh'
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
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('FTP处理异常')
        return -1

def ChkAppStatus():
    sqlstr  =   "select status from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino ='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    AfaLoggerFunc.tradeInfo( sqlstr )
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
    #初始化TradeContext
    TradeContext.workDate       =   AfaUtilTools.GetSysDate( )
    TradeContext.workTime       =   AfaUtilTools.GetSysTime( )
    TradeContext.zoneno         =   ""
    TradeContext.brno           =   ""
    TradeContext.teller         =   ""
    TradeContext.authPwd        =   ""
    TradeContext.termId         =   ""
    TradeContext.TransCode      =   "8448"                  #退付表下载


    AfaLoggerFunc.tradeInfo('**********安徽非税退付信息下载开始**********')

    #sqlstr  = "select distinct busino from abdt_unitinfo where appno='AG2008'"

    #begin 20100528 蔡永贵修改
    #sqlstr  = "select distinct busino from fs_businoconf"
    #sqlstr  = "select distinct busino,appno from abdt_unitinfo where appno in ('AG2008','AG2012')"
    sqlstr  = " select busino,bankno from fs_businoinfo "
    #end


    AfaLoggerFunc.tradeInfo( sqlstr )

    fsrecords = AfaDBFunc.SelectSql( sqlstr )
    if fsrecords == None or len(fsrecords)==0 :
        AfaLoggerFunc.tradeInfo("查找单位信息表异常")
        sys.exit(1)

    i=0
    for i in range( len(fsrecords) ):
        #bgein 20100528 蔡永贵修改
        #TradeContext.appNo        = 'AG2008'
        TradeContext.bankbm        = fsrecords[i][1].strip()
        if( TradeContext.bankbm == '012' ):
            TradeContext.appNo = 'AG2008';
        else:
            TradeContext.appNo = 'AG2012';
        #end


        TradeContext.busiNo       = fsrecords[i][0].strip()

        AfaLoggerFunc.tradeInfo("单位编码:" + TradeContext.busiNo)

        #=============判断应用状态========================
        if not ChkAppStatus( ) :
            AfaLoggerFunc.tradeInfo('**********安徽非税应用状态不正常**********')
            continue

        #----------------退付信息通过socket向财政取得缴款书放在afe上，afa去afe去缴款书信息文件
        if not GetConfig() :
            AfaLoggerFunc.tradeInfo('获取ftp配置文件失败')
            sys.exit(1)

        #拼成第三方报文
        TradeContext.TemplateCode   =   "3001"
        #TradeContext.sysId          =   "AG2008"
        TradeContext.sysId          =   TradeContext.appNo
        TradeContext.__respFlag__   =   "0"

        #=============与第三方通讯通讯====================
        AfaAfeFunc.CommAfe()
        if( TradeContext.errorCode != '0000' ):
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            continue
            #sys.exit(0)
        else :
            if (  ftpfile ( TradeContext.bankbm + Party3Context.FileName ,Party3Context.FileName ) <0 ):
                AfaLoggerFunc.tradeInfo("没有下载到文件")
                continue

            #开始读取文件
            try:
                fp          =   open(TradeContext.BATCH_LDIR + TradeContext.bankbm + Party3Context.FileName,"rb")
                recs        =   fp.read()

                if not recs :
                    AfaLoggerFunc.tradeInfo( "文件为空" )
                    continue

            except Exception, e:
                AfaLoggerFunc.tradeInfo( "没有生成文件或者文件为空" )
                continue

            #第一个数据不是记录而是数据种类
            rec     =   recs.split( chr(12) )
            sep     =   chr(31)

            for i in range( 1,len(rec) ):

                #检测第二条记录是否为空
                if not rec[i]:
                    AfaLoggerFunc.tradeInfo ( "当前字段已经为空" )
                    continue

                AfaLoggerFunc.tradeInfo( "rec=" + rec[i] )
                AfaLoggerFunc.tradeInfo( "recl=" + str(rec[i].split(sep)) )


                #首先检测退付信息是否下载过，如果下载了则更新退付状态，反之则插入一条记录
                sqlstr = "select * from fs_fc06 where afc060='" + (rec[i].split(sep))[9] + "'"
                sqlstr = sqlstr + " AND AFC306='" + (rec[i].split( sep ))[0] + "'"
                sqlstr = sqlstr + " AND AAA010='" + (rec[i].split( sep ))[1] + "'"

                AfaLoggerFunc.tradeInfo( sqlstr )
                records = AfaDBFunc.SelectSql( sqlstr )
                if( records == None ):
                    TradeContext.errorCode  =   "0001"
                    TradeContext.errorMsg   =   "查找退付信息异常"
                    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                    continue

                #如果没有查找到退付编号
                if len( records )==0:

                    #将记录集写到数据库中
                    fields  =   "AFC306,AAA010,AFC041,AFA050,AFC061,AFC062,AFC063,AFC064,AAZ016,AFC060,AAZ015,DATE,TIME"
                    sqlstr  =   "INSERT INTO FS_FC06(" + fields + ") VALUES("
                    for item in rec[i].split( sep ):
                        sqlstr  =  sqlstr   +  "'" + item + "',"

                    sqlstr      =  sqlstr +  "'" + TradeContext.workDate  + "',"
                    sqlstr      =  sqlstr +  "'" + TradeContext.workTime  + "')"

                    AfaLoggerFunc.tradeInfo( sqlstr )

                    if( AfaDBFunc.InsertSqlCmt( sqlstr ) < 1 ):
                        AfaLoggerFunc.tradeInfo ( "插入数据库失败"  + AfaDBFunc.sqlErrMsg )

                #如果查找到了退付编号，则更新状态位
                else:

                    AfaLoggerFunc.tradeInfo( '更新操作' )

                    sqlstr  =   "update fs_fc06 set aaz015='" + (rec[i].split( sep ))[10] + "' where afc060='" + (rec[i].split( sep ))[9] + "'"
                    sqlstr  =   sqlstr + " AND AFC306='" + (rec[i].split( sep ))[0] + "'"
                    sqlstr  =   sqlstr + " AND AAA010='" + (rec[i].split( sep ))[1] + "'"

                    AfaLoggerFunc.tradeInfo( sqlstr )

                    if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
                        TradeContext.errorCode, TradeContext.errorMsg='0001', '更新退付状态失败'
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                        continue

    AfaLoggerFunc.tradeInfo('**********安徽非税退付信息下载结束**********')
    sys.exit(0)
