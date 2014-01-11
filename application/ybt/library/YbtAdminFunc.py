# -*- coding: gbk -*-
################################################################################
# 文件名称：YbtAdminFunc.py
# 文件标识：
# 摘    要：中间业务通用管理库
#
# 当前版本：1.0
# 作    者：CYG
# 完成日期：2010-09-06
#
# 取代版本：
# 原 作 者：
# 完成日期：
################################################################################
import TradeContext, LoggerHandler, sys, os, time, AfaDBFunc, AfaUtilTools, ConfigParser, HostContext, HostComm
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
        
        #elif ( TradeContext.CRON_TRACE == 'dsdf' ):
        #    #向日志输入
        #    return True
        #    
        #elif ( TradeContext.CRON_TRACE == 'aix'  ):
        #    #向文件输出
        #    return True

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



#=========================读取对帐配置文件中信息=========================
def GetLappConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOST_HOSTIP   = config.get('HOST_DZ', 'HOSTIP')
        TradeContext.HOST_USERNO   = config.get('HOST_DZ', 'USERNO')
        TradeContext.HOST_PASSWD   = config.get('HOST_DZ', 'PASSWD')
        TradeContext.HOST_LDIR     = config.get('HOST_DZ', 'LDIR')
        TradeContext.HOST_RDIR     = config.get('HOST_DZ', 'RDIR')
        TradeContext.HOST_CDIR     = config.get('HOST_DZ', 'CDIR')
        TradeContext.HOST_BDIR     = config.get('HOST_DZ', 'BDIR')
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return True

    except Exception, e:
        print str(e)
        return False


#=========================读取对帐配置文件中信息=========================
def GetCorpConfig(sysId, CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.CORP_HOSTIP   = config.get(sysId + '_DZ', 'HOSTIP')
        TradeContext.CORP_HOSTPORT = config.get(sysId + '_DZ', 'HOSTPORT')
        TradeContext.CORP_USERNO   = config.get(sysId + '_DZ', 'USERNO')
        TradeContext.CORP_PASSWD   = config.get(sysId + '_DZ', 'PASSWD')
        TradeContext.CORP_LDIR     = config.get(sysId + '_DZ', 'LDIR')
        TradeContext.CORP_RDIR     = config.get(sysId + '_DZ', 'RDIR')

        return True

    except Exception, e:
        print str(e)
        return False
        
#=========================读取配置文件=========================
def GetAdminConfig(sysId=''):
    
    if not GetCronConfig():
        return False

    
    if not GetLappConfig():
        return False
    

    if len(sysId) > 0 :
        if not GetCorpConfig(sysId):
            return False

    return True


#=========================下载对帐文件=========================
def GetDzFile(sysId, rfilename, lfilename):

    WrtLog('>>>下载对帐文件')

    try:
        #创建文件
        ftpShell = os.environ['AFAP_HOME'] + '/tmp/ftphost_' + sysId + '.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.HOST_HOSTIP + '\n')
        ftpFp.write('user ' + TradeContext.HOST_USERNO + ' ' + TradeContext.HOST_PASSWD + '\n')

        #下载文件
        ftpFp.write('cd '  + TradeContext.HOST_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.HOST_LDIR + '\n')
        ftpFp.write('bin ' + '\n')
        ftpFp.write('get ' + rfilename + ' ' + lfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return False
        else:

            #判断文件是否存在
            sFileName = TradeContext.HOST_LDIR + "/" + lfilename
            if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
                return True
            else:
                WrtLog('>>>FTP处理下载文件失败')
                return False

    except Exception, e:
        WrtLog(e)
        WrtLog('>>>FTP处理异常')
        return False


#=========================上传对帐文件=========================
def PutDzFile(sysId, lfilename, rfilename):

    WrtLog('>>>上传对帐文件')
        
    try:
    
        #判断文件是否存在
        sFileName = TradeContext.CORP_LDIR + '/' + lfilename
        if ( not (os.path.exists(sFileName) and os.path.isfile(sFileName)) ):
            WrtLog('>>>对账文件不存在')
            return False

        #创建文件
        ftpShell = os.environ['AFAP_HOME'] + '/tmp/ftpcorp_' + sysId + '.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + TradeContext.CORP_HOSTIP + ' ' + TradeContext.CORP_HOSTPORT + '\n')
        ftpFp.write('user ' + TradeContext.CORP_USERNO + ' ' + TradeContext.CORP_PASSWD   + '\n')

        #上传文件
        ftpFp.write('cd '  + TradeContext.CORP_RDIR + '\n')
        ftpFp.write('lcd ' + TradeContext.CORP_LDIR + '\n')
        ftpFp.write('asc ' + '\n')
        ftpFp.write('put ' + lfilename + ' ' + rfilename + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '
        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return False
        else:
            return True

    except Exception, e:
        WrtLog(e)
        WrtLog('>>>FTP处理异常')
        return False
        
        
#=========================格式化文件=========================
def FormatFile(sFileName, dFileName):

    try:
        srcFileName    = TradeContext.HOST_LDIR + '/' + sFileName
        dstFileName    = TradeContext.HOST_LDIR + '/' + dFileName

        #调用格式:cvt2ascii -T 生成文本文件 -P 物理文件 -F fld文件 [-D 间隔符] [-S] [-R]
        CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
        fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/agent03.fld'
        cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName

        WrtLog( cmdstr )

        ret = os.system(cmdstr)
        if ( ret != 0 ):
            return False
        else:

            #判断文件是否存在
            if ( os.path.exists(dstFileName) and os.path.isfile(dstFileName) ):
                return True
            else:
                WrtLog('>>>格式化文件失败')
                return False

    except Exception, e:
        WrtLog(e)
        WrtLog('格式化文件异常')
        return False


######################################现实对帐流水信息#####################################
def PrtRecInfo( prtbuf ):
    WrtLog('************************************************')
    WrtLog('代理业务号       = ' + prtbuf[0])
   #WrtLog('批量委托日期     = ' + prtbuf[1])
   #WrtLog('批量委托号       = ' + prtbuf[2])
    WrtLog('前置日期         = ' + prtbuf[3])
    WrtLog('前置流水号       = ' + prtbuf[4])
    WrtLog('外系统帐务日期   = ' + prtbuf[5])
   #WrtLog('创建日期         = ' + prtbuf[6])
   #WrtLog('创建流水号       = ' + prtbuf[7])
   #WrtLog('蓝红字标志       = ' + prtbuf[8])
    WrtLog('交易机构         = ' + prtbuf[9])
    WrtLog('交易柜员         = ' + prtbuf[10])
   #WrtLog('组号             = ' + prtbuf[11])
   #WrtLog('组内序号         = ' + prtbuf[12])
   #WrtLog('借方帐号         = ' + prtbuf[13])
   #WrtLog('借方帐户名称     = ' + prtbuf[14])
   #WrtLog('销帐序号         = ' + prtbuf[15])
   #WrtLog('密码校验方式     = ' + prtbuf[16])
   #WrtLog('密码             = ' + prtbuf[17])
   #WrtLog('支付密码         = ' + prtbuf[18])
   #WrtLog('证件种类         = ' + prtbuf[19])
   #WrtLog('证件号码         = ' + prtbuf[20])
   #WrtLog('证件校验标志     = ' + prtbuf[21])
    WrtLog('凭证种类         = ' + prtbuf[22])
    WrtLog('凭证号           = ' + prtbuf[23])
   #WrtLog('存折支票标志     = ' + prtbuf[24])
   #WrtLog('凭证处理标志     = ' + prtbuf[25])
   #WrtLog('贷方帐号         = ' + prtbuf[26])
   #WrtLog('贷方帐户名称     = ' + prtbuf[27])
   #WrtLog('币种             = ' + prtbuf[28])
   #WrtLog('钞汇标志         = ' + prtbuf[29])
    WrtLog('现转标志         = ' + prtbuf[30])
   #WrtLog('往来帐标志       = ' + prtbuf[31])
    WrtLog('发生额           = ' + prtbuf[32])
   #WrtLog('摘要代码         = ' + prtbuf[33])
   #WrtLog('摘要说明         = ' + prtbuf[34])
   #WrtLog('户名校验标志     = ' + prtbuf[35])
   #WrtLog('冻结编号         = ' + prtbuf[36])
   #WrtLog('磁道 2 信息      = ' + prtbuf[37])
   #WrtLog('磁道 3 信息      = ' + prtbuf[38])
    WrtLog('附加信息 1       = ' + prtbuf[39])
   #WrtLog('附加信息 2       = ' + prtbuf[40])
   #WrtLog('挂帐帐号         = ' + prtbuf[41])
   #WrtLog('挂帐销帐序号     = ' + prtbuf[42])
   #WrtLog('记帐日期         = ' + prtbuf[43])
   #WrtLog('记帐时间         = ' + prtbuf[44])
   #WrtLog('记帐机构         = ' + prtbuf[45])
   #WrtLog('记帐柜员         = ' + prtbuf[46])
    WrtLog('主机流水号       = ' + prtbuf[47])
   #WrtLog('信息标识         = ' + prtbuf[48])
   #WrtLog('挂帐/记帐标志    = ' + prtbuf[49])
    WrtLog('抹帐标志         = ' + prtbuf[50])
   #WrtLog('抹帐日期         = ' + prtbuf[51])
    WrtLog('抹帐主机流水号   = ' + prtbuf[52])
   #WrtLog('记录状态         = ' + prtbuf[53])
    WrtLog('************************************************')





######################################修改系统########################################
def UpdSysStatus(sysId, sysStatus):

    WrtLog('>>>修改系统状态')

    updSql = "UPDATE AFA_SYSTEM SET STATUS='" + sysStatus + "' WHERE SYSID='" + sysId + "'"

    WrtLog(updSql)

    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result <= 0 ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('>>>处理结果:修改系统状态,数据库异常')
        return False

    WrtLog('>>>修改系统状态 ---> 成功')

    return True



######################################修改单位########################################
def UpdUnitStatus(procType, sysId, unitNo, subUnitno=''):

    WrtLog('>>>修改单位状态')

    if ( len(subUnitno)!=8 ):
        sTableName = "AFA_UNITADM"
    else:
        sTableName = "AFA_SUBUNITADM"

    #loginstatus            is '签到状态(0-签退 1-签到)';
    #dayendstatus           is '日终状态(0-未做 1-已做)';
    #dayendtime             is '日终时间';
    #trxchkstatus           is '对帐状态(0-未做 1-已对主机帐 2-第三方对帐成功 3-第三方对帐失败)';
    #trxchktime             is '对帐时间';


    #获取时间
    sysTime = AfaUtilTools.GetSysTime( )

    updSql = ""

    if ( procType == 1 ):
        #启动
        updSql = "UPDATE " + "%s" + " SET LOGINSTATUS='1',"
        updSql = updSql + "DAYENDSTATUS='0',"
        updSql = updSql + "DAYENDTIME='"   + sysTime + "',"
        updSql = updSql + "TRXCHKSTATUS='0',"
        updSql = updSql + "TRXCHKTIME='"   + sysTime + "' "

    else:
        #关闭
        updSql = "UPDATE " + "%s" + " SET LOGINSTATUS='0',"
        updSql = updSql + "DAYENDSTATUS='1',"
        updSql = updSql + "DAYENDTIME='"   + sysTime + "',"
        updSql = updSql + "TRXCHKSTATUS='1',"
        updSql = updSql + "TRXCHKTIME='"   + sysTime + "' "

    updSql = updSql + "WHERE SYSID='" + sysId + "' AND UNITNO='" + unitNo + "'"

    updSql1 = updSql %(sTableName)

    WrtLog(updSql1)

    result = AfaDBFunc.UpdateSqlCmt( updSql1 )
    if ( result <= 0 ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('>>>处理结果:修改单位状态1,数据库异常')
        return False

    if sTableName=="AFA_SUBUNITADM":
        updSql2 = updSql %('AFA_UNITADM')
        WrtLog(updSql2)
        result = AfaDBFunc.UpdateSqlCmt( updSql1 )
        if ( result <= 0 ):
            WrtLog( AfaDBFunc.sqlErrMsg )
            WrtLog('>>>处理结果:修改单位状态2,数据库异常')
            return False
    
    WrtLog('>>>修改单位状态 ---> 成功')

    return True
    

######################################下载主机文件#####################################
def DownLoadFile(sysId, trxDate):

    WrtLog('>>>下载主机文件')

    try:

        #通讯区打包
        HostContext.I1TRCD = '8818'                         #主机交易码
        HostContext.I1SBNO = "3400008889"                   #该交易的发起机构(清算中心)
        HostContext.I1USID = '999986'                       #交易柜员号
        HostContext.I1AUUS = ""                             #授权柜员
        HostContext.I1AUPS = ""                             #授权柜员密码
        HostContext.I1WSNO = ""                             #终端号
        HostContext.I1CLDT = "00000000"                     #批量委托日期
        HostContext.I1UNSQ = '000000000000'                 #批量委托号
        HostContext.I1NBBH = sysId                          #代理业务号(AG2???)
        HostContext.I1DATE = trxDate                        #外系统日期
        HostContext.I1FINA = sysId + trxDate[4:]            #下传文件名称

        HostTradeCode = "8818".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8818.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            WrtLog('>>>处理结果=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return False

        else:
            if ( HostContext.O1MGID != 'AAAAAAA' ):
                WrtLog('>>>处理结果=[' + str(HostContext.O1MGID) + ']:' +  HostContext.O1INFO)
                return False

            else:
                WrtLog('返回结果:重复次数=' + HostContext.O1ACUR)                          #重复次数
                WrtLog('返回结果:交易日期=' + HostContext.O1TRDT)                          #交易日期
                WrtLog('返回结果:交易时间=' + HostContext.O1TRTM)                          #交易时间
                WrtLog('返回结果:柜员流水=' + HostContext.O1TLSQ)                          #柜员流水
                WrtLog('返回结果:成功标志=' + HostContext.O1OPFG)                          #是否提交成功(0-成功,1-失败)

                #下载主机对帐文件
                rFileName = sysId + trxDate[4:]
                lFileName = sysId + '_' + trxDate + '_1'
                if not GetDzFile(sysId, rFileName, lFileName):
                    WrtLog('>>>处理结果:下载主机对帐文件失败')
                    return False

                dFileName = sysId + '_' + trxDate + '_2'
                if not FormatFile(lFileName, dFileName):
                    WrtLog('>>>处理结果:转码主机对帐文件失败')
                    return False

                WrtLog('>>>下载主机文件 ---> 成功')

        return True

    except Exception, e:
        WrtLog(str(e))
        WrtLog('>>>下载主机文件 ---> 异常')
        return False




######################################初始化流水标志###################################
def InitData(sysId,unitNo,trxDate):

    WrtLog('>>>初始化流水标志')
    TradeContext.serialFlag = '0'

    updSql =  "UPDATE AFA_MAINTRANSDTL SET CHKFLAG='*' WHERE SYSID='" + sysId + "' AND WORKDATE='" + trxDate + "' AND UNITNO='" + unitNo + "'"

    WrtLog(updSql)

    result = AfaDBFunc.UpdateSqlCmt( updSql )
    if ( result < 0 ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('>>>处理结果:初始化流水标志,数据库异常')
        TradeContext.serialFlag = '0'
        return False

    if ( result == 0 ):
        WrtLog('>>>处理结果:该系统没有任何流水信息')
        TradeContext.serialFlag = '0'
        return False

    WrtLog('>>>初始化流水标志 ---> 成功')

    return True



######################################逐笔勾兑流水#####################################
def MatchData(sysId,unitNo,trxDate):

    WrtLog('>>>逐笔勾兑流水')

    try:
        #下载主机文件
        if not DownLoadFile(sysId, trxDate):
            return False

        #初始化流水标志
        if not InitData(sysId,unitNo,trxDate):
            return False

        totalnum = 0
        totalamt = 0

        #打开主机下载文件
        sFileName = TradeContext.HOST_LDIR + '/' + sysId + '_' + trxDate + '_2'


        hFp = open(sFileName, "r")


        #读取一行
        linebuf = hFp.readline()


        while ( len(linebuf) > 0 ):


            #判断对帐流水的合法性
            if ( len(linebuf) < 996 ):
                WrtLog('该批次下载文件格式错误(长度),请检查')
                hFp.close()
                return False


            #拆分对帐流水
            swapbuf = linebuf[0:996].split('<fld>')


            #读取一行
            linebuf = hFp.readline()


            #过滤非本应用对帐流水
            if ( swapbuf[0].strip()!=sysId or swapbuf[3].strip()!=trxDate or swapbuf[5].strip()!=trxDate ):
                WrtLog("===被忽略===")
                PrtRecInfo( swapbuf )
                continue


            #先查询数据库中记录是否存在
            sqlstr = "SELECT BRNO,TELLERNO,REVTRANF,AMOUNT,BANKSTATUS,CORPSTATUS,AGENTSERIALNO,WORKDATE,ERRORMSG FROM AFA_MAINTRANSDTL WHERE"
            sqlstr = sqlstr + "     SYSID         = '"  + sysId              + "'"
            sqlstr = sqlstr + " AND WORKDATE      = '"  + trxDate            + "'"
            sqlstr = sqlstr + " AND AGENTSERIALNO = '"  + swapbuf[4].strip() + "'"
            sqlstr = sqlstr + " AND UNITNO        = '"  + unitNo             + "'"

            WrtLog(sqlstr)

            ChkFlag = '*'
            statusFlag = '0'            #用来标识记录中的BANKSTATUS的状态，如果BANKSTATUS的状态不为0，则该标志的值为1
            
            records = AfaDBFunc.SelectSql( sqlstr )

            if ( records==None ):
                WrtLog( AfaDBFunc.sqlErrMsg )
                WrtLog('查询流水信息异常,请检查')
                hFp.close()
                return False


            if ( len(records) == 0 ):
                WrtLog('数据库中记录匹配失败(表中无记录)')
                continue

            else:
                h_tradeamt = long(float(swapbuf[32].strip())  *100 + 0.1)
                m_tradeamt = long(float(records[0][3].strip())*100 + 0.1)

                if ( swapbuf[9].strip() != records[0][0].strip() ):
                    WrtLog('数据库中记录匹配失败(机构号不符):' + swapbuf[9].strip()  + '|' + records[0][0] + '|')
                    PrtRecInfo( swapbuf )
                    ChkFlag = '2'

                elif ( swapbuf[10].strip() != records[0][1] ):
                    WrtLog('数据库中记录匹配失败(柜员号不符):' + swapbuf[10].strip() + '|' + records[0][1] + '|')
                    PrtRecInfo( swapbuf )
                    ChkFlag = '3'

                elif ( h_tradeamt != m_tradeamt ):
                    WrtLog('数据库中记录匹配失败(发生额不符):' + str(h_tradeamt) + '|' + str(m_tradeamt) + '|')
                    PrtRecInfo( swapbuf )
                    ChkFlag = '4'

                elif ( swapbuf[50].strip() == '1' ):
                    ChkFlag = '1'

                else:
                    if records[0][4] != '0':
                        WrtLog( '数据库中记录状态与主机不符，更新中台数据以保持和主机一致' )
                        statusFlag = 1
                        
                        #把存在该类错误的信息记录到表AFA_DZERROR中
                        WrtLog( '记录中台和主机不一致的流水信息' )
                        occurTime = time.strftime('%Y%m%d%H%M%S',time.localtime())
                        insertSql = "insert into afa_dzerror(OCCURTIME,SERIALNO,WORKDATE,AMOUNT,BANKSTATUS,ERROEMSG) values("
                        insertSql = insertSql + "'" + occurTime     +"',"
                        insertSql = insertSql + "'" + records[0][6] + "',"
                        insertSql = insertSql + "'" + records[0][7] + "',"
                        insertSql = insertSql + "'" + records[0][3] + "',"
                        insertSql = insertSql + "'" + records[0][4] + "',"
                        insertSql = insertSql + "'" + records[0][8] + "')"
                        WrtLog( '记录错误记录sql：' + insertSql )
                        
                        result = AfaDBFunc.InsertSqlCmt( insertSql )
                        if ( result < 0 ):
                            WrtLog( AfaDBFunc.sqlErrMsg )
                            WrtLog( '记录主机对账主机和中台数据不一致失败' )
                            return False
                            
                    ChkFlag = '0'

            #修改与数据库进行匹配
            updSql = "UPDATE AFA_MAINTRANSDTL SET CHKFLAG='" + ChkFlag + "'"
            if statusFlag == 1 :
                updSql = updSql + " ,BANKSTATUS = '0'"
            updSql = updSql + " WHERE SYSID         = '" + sysId              + "'"
            updSql = updSql + " AND   WORKDATE      = '" + trxDate            + "'"
            updSql = updSql + " AND   AGENTSERIALNO = '" + swapbuf[4].strip() + "'"
            updSql = updSql + " AND   UNITNO        = '" + unitNo             + "'"

            WrtLog(updSql)

            result = AfaDBFunc.UpdateSqlCmt( updSql )
            if ( result <= 0 ):
                WrtLog( AfaDBFunc.sqlErrMsg )
                WrtLog('>>>处理结果:修改与匹配流水状态,数据库异常')
                return False

            totalnum = totalnum + 1
            totalamt = totalamt + m_tradeamt

        hFp.close()

        WrtLog( '匹配记录数=' + str(totalnum) + ",匹配总金额=" + str(totalamt) )

        WrtLog( '>>>逐笔勾兑流水 ---> 成功' )

        return True

    except Exception, e:
        hFp.close()
        WrtLog(str(e))
        WrtLog('>>>逐笔勾兑流水 ---> 异常')
        return False





######################################生成报表文件#####################################
def CrtReportFile(sysId,unitNo,trxDate):

    WrtLog('>>>生成报表文件')

    colName = "agentserialno,workdate,worktime,sysid,unitno,subunitno,agentflag,trxcode,zoneno,brno,tellerno,"
    colName = colName + "cashtelno,authtellerno,channelcode,channelserno,termid,customerid,userno,subuserno,username,acctype,"
    colName = colName + "draccno,craccno,vouhtype,vouhno,vouhdate,currType,currFlag,amount,subamount,revtranf,preagentserno,"
    colName = colName + "bankstatus,bankcode,bankserno,corpstatus,corpcode,corpserno,corptime,errormsg,chkflag,corpchkflag,appendflag,"
    colName = colName + "note1,note2,note3,note4,note5,note6,note7,note8,note9,note10"

    selSql = "SELECT " + colName + "FROM AFA_MAINTRANSDTL WHERE SYSID='" + sysId + "' AND UNITNO='" + unitNo + "' AND WORKDATE='" + trxDate + "' AND CHKFLAG='0' ORDER BY WORKTIME ASC"

    WrtLog(selSql)

    records = AfaDBFunc.SelectSql( sqlstr, 10000 )

    if ( records==None ):
        WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog('生成报表文件异常,请检查')
        return False

    if ( len(records) == 0 ):
        WrtLog('数据库中没有流水信息')
        return False

    records=AfaUtilTools.ListFilterNone( records )

    #创建文件
    bankRpt1 = TradeContext.HOST_BDIR + "/" + sysId + "_" + unitNo + "_" + trxDate + ".SUC"
    bankRpt2 = TradeContext.HOST_BDIR + "/" + sysID + "_" + unitNo + "_" + trxDate + ".ERR"
    sfp= open(bankRpt1,  "w")
    efp= open(bankRpt2,  "w")

    iRecNum=0
    for i in range(0, len(records)):
        prtBuffer = ""
        prtBuffer = prtBuffer + str(records[i][0]).strip() + "|"  #agentserialno
        prtBuffer = prtBuffer + str(records[i][1]).strip() + "|"  #workdate
        prtBuffer = prtBuffer + str(records[i][2]).strip() + "|"  #worktime
        prtBuffer = prtBuffer + str(records[i][3]).strip() + "|"  #sysid
        prtBuffer = prtBuffer + str(records[i][4]).strip() + "|"  #unitno
        prtBuffer = prtBuffer + str(records[i][5]).strip() + "|"  #subunitno
        prtBuffer = prtBuffer + str(records[i][6]).strip() + "|"  #agentflag
        prtBuffer = prtBuffer + str(records[i][7]).strip() + "|"  #trxcode
        prtBuffer = prtBuffer + str(records[i][8]).strip() + "|"  #zoneno
        prtBuffer = prtBuffer + str(records[i][9]).strip() + "|"  #brno
        prtBuffer = prtBuffer + str(records[i][10]).strip()+ "|"  #tellerno
        prtBuffer = prtBuffer + str(records[i][11]).strip()+ "|"  #cashtelno
        prtBuffer = prtBuffer + str(records[i][12]).strip()+ "|"  #authtellerno
        prtBuffer = prtBuffer + str(records[i][13]).strip()+ "|"  #channelcode
        prtBuffer = prtBuffer + str(records[i][14]).strip()+ "|"  #channelserno
        prtBuffer = prtBuffer + str(records[i][15]).strip()+ "|"  #termid
        prtBuffer = prtBuffer + str(records[i][16]).strip()+ "|"  #customerid
        prtBuffer = prtBuffer + str(records[i][17]).strip()+ "|"  #userno
        prtBuffer = prtBuffer + str(records[i][18]).strip()+ "|"  #subuserno
        prtBuffer = prtBuffer + str(records[i][19]).strip()+ "|"  #username
        prtBuffer = prtBuffer + str(records[i][20]).strip()+ "|"  #acctype
        prtBuffer = prtBuffer + str(records[i][21]).strip()+ "|"  #draccno
        prtBuffer = prtBuffer + str(records[i][22]).strip()+ "|"  #craccno
        prtBuffer = prtBuffer + str(records[i][23]).strip()+ "|"  #vouhtype
        prtBuffer = prtBuffer + str(records[i][24]).strip()+ "|"  #vouhno
        prtBuffer = prtBuffer + str(records[i][25]).strip()+ "|"  #vouhdate
        prtBuffer = prtBuffer + str(records[i][26]).strip()+ "|"  #currType
        prtBuffer = prtBuffer + str(records[i][27]).strip()+ "|"  #currFlag
        prtBuffer = prtBuffer + str(records[i][28]).strip()+ "|"  #amount
        prtBuffer = prtBuffer + str(records[i][29]).strip()+ "|"  #subamount
        prtBuffer = prtBuffer + str(records[i][30]).strip()+ "|"  #revtranf
        prtBuffer = prtBuffer + str(records[i][31]).strip()+ "|"  #preagentserno
        prtBuffer = prtBuffer + str(records[i][32]).strip()+ "|"  #bankstatus
        prtBuffer = prtBuffer + str(records[i][33]).strip()+ "|"  #bankcode
        prtBuffer = prtBuffer + str(records[i][34]).strip()+ "|"  #bankserno
        prtBuffer = prtBuffer + str(records[i][35]).strip()+ "|"  #corpstatus
        prtBuffer = prtBuffer + str(records[i][36]).strip()+ "|"  #corpcode
        prtBuffer = prtBuffer + str(records[i][37]).strip()+ "|"  #corpserno
        prtBuffer = prtBuffer + str(records[i][38]).strip()+ "|"  #corptime
        prtBuffer = prtBuffer + str(records[i][39]).strip()+ "|"  #errormsg
        prtBuffer = prtBuffer + str(records[i][40]).strip()+ "|"  #chkflag
        prtBuffer = prtBuffer + str(records[i][41]).strip()+ "|"  #corpchkflag
        prtBuffer = prtBuffer + str(records[i][42]).strip()+ "|"  #appendflag
        prtBuffer = prtBuffer + str(records[i][43]).strip()+ "|"  #note1
        prtBuffer = prtBuffer + str(records[i][44]).strip()+ "|"  #note2
        prtBuffer = prtBuffer + str(records[i][45]).strip()+ "|"  #note3
        prtBuffer = prtBuffer + str(records[i][46]).strip()+ "|"  #note4
        prtBuffer = prtBuffer + str(records[i][47]).strip()+ "|"  #note5
        prtBuffer = prtBuffer + str(records[i][48]).strip()+ "|"  #note6
        prtBuffer = prtBuffer + str(records[i][49]).strip()+ "|"  #note7
        prtBuffer = prtBuffer + str(records[i][50]).strip()+ "|"  #note8
        prtBuffer = prtBuffer + str(records[i][51]).strip()+ "|"  #note9
        prtBuffer = prtBuffer + str(records[i][52]).strip()+ "|"  #note10
        iRecNum = iRecNum + 1

        if str(records[i][40]).strip() == "0" :
            sfp.write(prtBuffer + '\n')

        elif (str(records[i][40]).strip()=="2" or str(records[i][40]).strip()=="3" or str(records[i][40]).strip()=="3"):
            efp.write(prtBuffer + '\n')

    sfp.close()
    cfp.close()
    efp.close()
    WrtLog('>>>记录数=' + str(iRecNum))
        
    WrtLog('>>>生成报表文件 ---> 成功')

    return True
