# -*- coding: gbk -*-
########################################################################
#    文    件:    VouhFunc.py
#    说    明:    凭证管理系统功能库
#    环    境:    中间业务新平台（AFA）--- UNIX: AIX 5.3 python
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日
#    维护纪录:
########################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools,  AfaFlowControl, AfaDBFunc,os，ConfigParser
import time
from types import *
#AfaFunc,,ftplib,ConfigParser

########################################################################
#    函    数:    VouhModify( )
#    功    能:    登记凭证变更登记簿
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日
#    参    数:    通过内部变量传递
#    返 回 值:    0    成功
#                 -1   运行参数错
########################################################################
def VouhModify( ):
    #判断报文变量是否存在，若存在则赋值到内部变量，用于插入数据库
    if( TradeContext.existVariable( "sLstTrxDay" ) ):
        _sWorkDate_    = TradeContext.sLstTrxDay       #工作日期
    else:
        _sWorkDate_    = ''
    if( TradeContext.existVariable( "sLstTrxTime" ) ):
        _sWorkTime_    = TradeContext.sLstTrxTime      #工作时间
    else:
        _sWorkTime_    = ''
    if( TradeContext.existVariable( "sBesbNo" ) ):
        _sBESBNO_      = TradeContext.sBesbNo          #机构号
    else:
        _sBESBNO_      = ''
    if( TradeContext.existVariable( "sCur" ) ):
        _sCur_      = TradeContext.sCur          #货币代号
    else:
        _sCur_      = ''
    if( TradeContext.existVariable( "sTellerTailNo" ) ):
        _sTellerTailNo_    = TradeContext.sTellerTailNo        #交易柜员尾箱号
    else:
        _sTellerNo_    = ''
    if( TradeContext.existVariable( "sVouhSerial" ) ):
        _sVouhSerial_    = TradeContext.sVouhSerial    #操作流水号
    else:
        _sVouhSerial_    = GetVouhSerial( )
    if( TradeContext.existVariable( "sRivTeller" ) ):
        _sRivTeller_   = TradeContext.sRivTeller       #对方柜员尾箱号
    else:
        _sRivTeller_   = ''
    if( TradeContext.existVariable( "sDepository" ) ):
        _sDepository_  = TradeContext.sDepository      #库箱标志
    else:
        _sDepository_  = ''
    if( TradeContext.existVariable( "sExDepos" ) ):
        _sExDepos_     = TradeContext.sExDepos         #原库箱标志
    else:
        _sExDepos_     = ''
    if( TradeContext.existVariable( "sVouhStatus" ) ):
        _sVouhStatus_  = TradeContext.sVouhStatus      #状态
    else:
        _sVouhStatus_  = ''
    if( TradeContext.existVariable( "sExStatus" ) ):
        _sExStatus_    = TradeContext.sExStatus        #原状态
    else:
        _sExStatus_    = ''
    if( TradeContext.existVariable( "sAuthTeller" ) ):
        _sAuthTeller_     = TradeContext.sAuthTeller         #授权柜员
    else:
        _sAuthTeller_     = ''
    if( TradeContext.existVariable( "sTransType" ) ):
        _sTransType_  = TradeContext.sTransType      #凭证状态
    else:
        _sTransType_  = ''
    if(not TradeContext.existVariable( "sNum" ) ):
        TradeContext.sNum = 1      #重复次数

        
    for i in range(TradeContext.sNum):
        if( TradeContext.existVariable( "sVouhType" ) ):
            _sVouhType_    = TradeContext.sVouhType[i]        #凭证种类
        else:
            _sVouhType_    = ''
        if( TradeContext.existVariable( "sStartNo" ) ):
            _sStartNo_     = TradeContext.sStartNo[i]         #起始号码
        else:
            _sStartNo_     = ''
        if( TradeContext.existVariable( "sEndNo" ) ):
            _sEndNo_       = TradeContext.sEndNo[i]           #终止号码
        else:
            _sEndNo_       = ''
        if( TradeContext.existVariable( "sVouhNum" ) ):
            _sVouhNum_       = TradeContext.sVouhNum[i]           #凭证数量
        else:
            _sVouhNum_       = ''
           
        #用内部变量拼插入数据库SQL
        sqlStrInsert = "insert into VOUH_MODIFY ( VOUHSERIAL, WORKDATE, WORKTIME,VOUHNUM, BESBNO, TELLERNO, CUR ,\
        VOUHTYPE, STARTNO, ENDNO, RIVTELLER, DEPOSITORY, EXDEPOS, VOUHSTATUS, EXSTATUS,TRANSTYPE) \
        VALUES ('" + _sVouhSerial_ + "','" + _sWorkDate_ + "','" + _sWorkTime_ + "','"+ _sVouhNum_ + "','" + _sBESBNO_ +  "','" \
            + _sTellerTailNo_ + "','" + _sCur_+ "','" + _sVouhType_+"','" \
            + _sStartNo_ + "','" + _sEndNo_ + "','" + _sRivTeller_ + "','" + _sDepository_ + "','" \
            + _sExDepos_ + "','" + _sVouhStatus_ + "','" + _sExStatus_ + "','" + _sTransType_  + "')"
        AfaLoggerFunc.tradeInfo( sqlStrInsert )
        records = AfaDBFunc.InsertSql( sqlStrInsert )
        if records == -1 :
            AfaLoggerFunc.tradeInfo( '数据库回滚' )
            record = AfaDBFunc.RollbackSql( )
            tradeExit('A005061', '插入[凭证流水表]操作异常!')
            raise AfaFlowControl.flowException( )
            return -1

    return 0

########################################################################
#    函    数:    ModifyVouhModify( )
#    功    能:    更新凭证变更登记簿
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日
#    参    数:    通过内部变量传递
#    返 回 值:    0    成功
#                 -1   运行参数错
########################################################################
def ModifyVouhModify():
    if(not TradeContext.existVariable( "HostDate" )):
                TradeContext.HostDate = '' 

    #更新流水表
    sqlUpdate = "update VOUH_MODIFY SET TRANSTATUS = '" + TradeContext.sTranStatus + "',\
                HOSTDATE = '" + TradeContext.HostDate + "',\
                HOSTSERIAL = '" + TradeContext.HostSerno + "' where VOUHSERIAL = '" + TradeContext.sVouhSerial + "'"
    record = AfaDBFunc.UpdateSqlCmt( sqlUpdate )
    if record == -1 or record == 0 :
        tradeExit('A005062', '更新流水表失败!')
        raise AfaFlowControl.flowException( )

########################################################################
#    函    数:    GetVouhSerial( )
#    功    能:    取凭证操作序列号
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日
#    参    数:    无
#    返 回 值:    0    成功
#                 -1   运行参数错
########################################################################
def GetVouhSerial( ):
    sqlStr = "SELECT NEXTVAL for VOUH_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1 "
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        TradeContext.errorCode = 'A000001'
        TradeContext.errorMsg = AfaDBFunc.sqlErrMsg
    else:
        TradeContext.sVouhSerial = str( records[0][0] )
    return str( records[0][0] )



######################################################################
#    函    数:    DelSpace( a )
#    功    能:    去掉list中的空字段
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日
#    参    数:    list
#    返 回 值:    0    成功
#                 -1   运行参数错
#####################################################################
def DelSpace( a ):
    b=[]
    for i in range(len(a)):
        if( len(a[i]) <> 0 ):
            b.append(a[i])
    return b
    
######################################################################
#    函    数:    AddSplit( a )
#    功    能:    list装换字符串
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    公    司:    北京赞同科技
#    创建地址:    安徽
#    创建时间:    2008年6月11日
#    参    数:    list
#    返 回 值:    0    成功
#                 -1   运行参数错
#####################################################################
def AddSplit( a ):
    b=''
    for i in range(len(a)):
        if(i==0):
            splitStr=''
        else:
            splitStr='|'
        b = b + splitStr + a[i]
    return b
    
##################################################################
#   凭证管理系统.FTP操作模块
#=================================================================
#   函    数:   getVouh()
#   作    者:   李亚杰
#   修改时间:   2008-06-11
##################################################################

#def getVouh(file_path):
#    try:
#        host_home="run/ftr"
#        local_home = os.environ['AFAP_HOME'] + "/data/vouh/"
#        
#        config = ConfigParser.ConfigParser( )
#        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
#        config.readfp( open( configFileName ) )
#        
#        ftp_p=ftplib.FTP(config.get('host','ip'),config.get('host','username'),config.get('host','password' ))
#        ftp_p.cwd(host_home)
#        file_handler = open(local_home + file_path,'wb')
#        ftp_p.retrbinary("RETR " + file_path,file_handler.write)
#        file_handler.close()
#        ftp_p.quit()
#        
#        if not os.path.exists(local_home + file_path):
#            raise Exception,"文件[" + local_home + file_path + "]下载失败"
#        
#        return True
#        
#    except Exception, e:
#        AfaLoggerFunc.tradeInfo(e)
#        return False
#
    
def putHost(file_path):
    try:
        host_home="textlib"
        local_home = os.environ['AFAP_HOME'] + "/data/vouh/"
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open( configFileName ) )
        
        if not os.path.exists(local_home + file_path):
            raise Exception,"上传文件[" + local_home + file_path + "]不存在"
            
        ftp_p=ftplib.FTP(config.get('HOST_DZ','HOSTIP'),config.get('HOST_DZ','USERNO'),config.get('HOST_DZ','PASSWD' ))
        ftp_p.cwd(host_home)
        file_handler = open(local_home + file_path,'rb')
        ftp_p.storbinary("STOR " + file_path,file_handler)
        file_handler.close()
        ftp_p.quit()
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
        
##################################################################
#   凭证管理系统.格式化文件
#=================================================================
#   函    数:   FormatFile(ProcType, sFileName, dFileName)
#   作    者:   李亚杰
#   修改时间:   2008-06-11
##################################################################
#格式化文件
def FormatFile(ProcType, sFileName, dFileName):

#    WrtLog('>>>格式化文件:' + ProcType + ' ' + sFileName + ' ' + dFileName)

    try:

        srcFileName    = os.environ['AFAP_HOME'] + '/data/vouh/' + sFileName
        dstFileName    = os.environ['AFAP_HOME'] + '/data/vouh/' + dFileName

        if (ProcType == "1"):
            #ascii->ebcd
            #调用格式:cvt2ebcdic -T 源文本文件 -P 目标物理文件 -F fld格式文件 [-D 间隔符 ]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ebcdic'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/vouh/cvt/TPCZA.fld'
            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName + " -D '|'"

        else:
            #ebcd->ascii
            #调用格式:cvt2ascii -T 生成文本文件 -P 物理文件 -F fld文件 [-D 间隔-符] [-S] [-R]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/vouh/cvt/vouh02.fld'
            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName

        AfaLoggerFunc.tradeInfo('>>>' + cmdstr)
        #ret = -1
        AfaLoggerFunc.tradeInfo('>>>外调格式转换程序开始============')   #2007824
        ret = os.system(cmdstr)                         #2007824
        if ( ret != 0 ):                                #2007824
            ret = False                                 #2007824
        else:                                           #2007824
            ret = True                                  #2007824
        #return 0                                       #2007824
        AfaLoggerFunc.tradeInfo('>>>外调格式转换程序结束============')   #2007824

        return ret
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('格式化文件异常')
        return False
        
########################################################################
#    函    数:    SelectBesbSty( sBesbNo)
#    功    能:    查询机构类型
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    参    数:    sBesbNo   - 机构号 
#    创建地址:    安徽
#    创建时间:    2008年6月18日
#    
#    返 回 值:    
#                 
########################################################################
def SelectBesbSty( sBesbNo):
    #=============前台上送数据====================
    #TradeContext.sBESBNO           机构号
    #TradeContext.sBesbSty          机构类型
    
    try:
        
        sqlStr = "SELECT SBSBCH FROM VOUH_FRONT_CRSBA WHERE SBSBNO ='" + sBesbNo + "'"
     
        records = AfaDBFunc.SelectSql( sqlStr)
        if( records == None ):
            tradeExit('A005067', '查询[机构表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '机构不存在!' )
            raise AfaFlowControl.flowException( )

        return str(records[0][0])
            
            
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
        
########################################################################
#    函    数:    SelectSBTPAC( sBesbNo)
#    功    能:    查询清算上级
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    参    数:    sBesbNo   - 机构号 
#    创建地址:    安徽
#    创建时间:    2008年6月18日
#    
#    返 回 值:    
#                 
########################################################################
def SelectSBTPAC( sBesbNo):
    #=============前台上送数据====================
    #TradeContext.sBESBNO           机构号
    #TradeContext.sSBTPAC           清算上级
    
    try:
        
        sqlStr = "SELECT SBTPAC FROM VOUH_FRONT_CRSBA WHERE SBSBNO ='" + sBesbNo + "'"
     
        records = AfaDBFunc.SelectSql( sqlStr)
        if( records == None ):
            tradeExit('A005067', '查询[机构表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '机构不存在!' )
            raise AfaFlowControl.flowException( )

        return str(records[0][0])
            
            
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
        
########################################################################
#    函    数:    SelectBesbName( sBesbNo)
#    功    能:    查询机构名称
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    参    数:    sBesbNo   - 机构号 
#    创建地址:    安徽
#    创建时间:    2008年6月18日
#    
#    返 回 值:    
#                 
########################################################################
def SelectBesbName( sBesbNo):
    #=============前台上送数据====================
    #TradeContext.sBESBNO           机构号
    #TradeContext.sBesbSty          机构类型
    
    try:
        
        sqlStr = "SELECT SBSBNM FROM VOUH_FRONT_CRSBA WHERE SBSBNO ='" + sBesbNo + "'"
     
        records = AfaDBFunc.SelectSql( sqlStr)
        if( records == None ):
            tradeExit('A005067', '查询[机构表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '机构不存在!' )
            raise AfaFlowControl.flowException( )

        return str(records[0][0])
            
            
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
        
#=============返回错误码,错误信息===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True
    
########################################################################
#    函    数:    VouhTrans( )
#    功    能:    交易公共部分
#    环    境:    中间业务平台外 ---  python
#    作    者:    李亚杰
#    参    数:    无 
#    创建地址:    安徽
#    创建时间:    2008年6月18日
#    
#    返 回 值:    
#                 
########################################################################
def VouhTrans( ):
    #===定义变量－输入的凭证号码与库表中状态为‘1’(已出未入)的凭证号码的连续标志======
    #sFlagContinue:continue:前后连续;
    #sFlagContinue:FrontContinue:前连续;
    #sFlagContinue:BackContinue:后连续;
    sFlagContinue = ''
    
    #=============进入凭证出库交易==========================
    
    #1.查询需要出库的凭证起止号码是否在库表中已入未发的凭证号码范围内
    #2.如果需要出库的凭证起止号码在库表中可出库的凭证号码范围内,那么需要
    #  判断库表中满足凭证状态为已发未领,地区号与签到柜员所在地区一致这几个条件的记录
    #与输入的凭证号码是否有连续关系
    #3.如果无连续关系,那么需要判断输入的凭证起止号码与库表中相应的凭证号码区间的关系
    #  1)输入的起始号码与区间的起始号码相同. 2)输入的终止号码与区间的结束号码相同
    #  3)输入的起始号码和终止号码与区间起始和结束号码都相同. 4)输入的起止号码完全在区间之内
    #4.如果有连续关系,那么需要判断输入的凭证起止号码与库表中凭证状态为已发未领的
    #凭证号码之间的关系  1) 前连续 2)后连续  3)前后连续
    
    for i in range(TradeContext.sNum):
        
        #begin凭证优化201202 李利君
        Len=''
        Len = int(len(TradeContext.sStartNo[i]))
        
        #=============计算输入的凭证数量==========================
        sStartNoMulti = str(int( TradeContext.sStartNo[i] ) - 1).rjust(Len,'0')
        sEndNoAdd = str(int( TradeContext.sEndNo[i] ) + 1).rjust(Len,'0')
        #end
        
        #查询数据库[凭证登记表],确认是否输入的凭证起始号码,终止号码在该柜员登陆分行
        #登记未出状态的凭证号码段内
        sqlStr = "select STARTNO,ENDNO,LSTTRXDAY,LSTTRXTIME,RIVTELLER,TELLERNO \
            from VOUH_REGISTER \
            where VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
            and BESBNO = '" + TradeContext.sBesbNo + "'\
            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
            and CUR = '" + TradeContext.sCur + "'\
            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
            and ( ENDNO >= '" + TradeContext.sEndNo[i] + "' and STARTNO <= '" + TradeContext.sStartNo[i] + "' )"
        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if( records == None ):          #查询凭证登记表异常
            if( i > 0 ):
                AfaLoggerFunc.tradeInfo( '数据库回滚' )
                AfaDBFunc.RollbackSql( )
            tradeExit('A005061', '查询[凭证登记表]操作异常!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):    #如果凭证登记表中无对应记录
            if( i > 0 ):
                AfaLoggerFunc.tradeInfo( '数据库回滚' )
                AfaDBFunc.RollbackSql( )
            tradeExit('A005067', '凭证操作失败,凭证库中不存在本次操作的凭证!')
            raise AfaFlowControl.flowException( )
        else :
            records = AfaUtilTools.ListFilterNone( records )
            sTempStartNo = records[0][0]           #保存输入的凭证号码所在的区间起始凭证号码
            sTempEndNo   = records[0][1]           #保存输入的凭证号码所在的区间终止凭证号码
            sTempLstTrxDay   = records[0][2]       #保存输入的凭证号码所在的区间最后交易日期
            sTempLstTrxTime  = records[0][3]       #保存输入的凭证号码所在的区间最后交易时间
            sTempRivTeller   = records[0][4]       #保存输入的凭证号码所在的区间对方柜员
            sTempTellerNo   = records[0][5]        #保存输入的凭证号码所在的区间对方柜员
        
            #当输入的凭证起止号码为合法号码时,查询库表中满足状态为已发未领,
            #柜员号地区号与签到柜员所在地区一致的条件的记录与输入的凭证号码是否有连续关系
            sqlStr = "select STARTNO,ENDNO from VOUH_REGISTER \
                    where VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                    and BESBNO = '" + TradeContext.sInBesbNo + "'\
                    and TELLERNO = '" + TradeContext.sInTellerTailNo + "'\
                    and CUR = '" + TradeContext.sCur + "'\
                    and DEPOSITORY = '" + TradeContext.sDepository + "'\
                    and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                    and ( ENDNO = '" + sStartNoMulti + "' \
                    OR STARTNO = '" + sEndNoAdd + "' )"
    
            AfaLoggerFunc.tradeDebug(sqlStr)
            records = AfaDBFunc.SelectSql( sqlStr )
            records = AfaUtilTools.ListFilterNone( records )
            if( records == None ):          #查询凭证登记表异常
                if( i > 0 ):
                    AfaLoggerFunc.tradeInfo( '数据库回滚' )
                    AfaDBFunc.RollbackSql( )
                tradeExit('A005061', '查询[凭证登记表]操作异常!')
                raise AfaFlowControl.flowException( )
        
            #输入的凭证号码与库中已存在的状态为登记未出的凭证号码无连续关系
            elif( len( records ) == 0 ):
                #输入的起始号码和终止号码与区间起始和结束号码都相同
                if ( int( TradeContext.sEndNo[i] ) == int( sTempEndNo ) \
                    and int( TradeContext.sStartNo[i] ) == int( sTempStartNo ) ):
                    #直接更新对应记录
                    sqlStr = "update VOUH_REGISTER set \
                           DEPOSITORY = '"+TradeContext.sDepository+"',\
                           VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "',\
                           BESBNO = '" + TradeContext.sInBesbNo + "', \
                           TELLERNO = '" + TradeContext.sInTellerTailNo + "', \
                           RIVTELLER = '" + TradeContext.sTellerTailNo + "', \
                           LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                           LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + TradeContext.sStartNo[i] + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR = '"+ TradeContext.sCur+"'"
    
                    AfaLoggerFunc.tradeDebug('1'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
                    else:
                        tradeExit('0000', TradeContext.sTransType+'成功')
        
                #输入的终止号码与区间的结束号码相同
                elif ( int( TradeContext.sEndNo[i] ) == int( sTempEndNo ) ):
                    #更新数据库中已存记录,更新成功后再新增出库记录
                    sqlStr = "update VOUH_REGISTER set \
                      VOUHNUM = '"+ ( str( int( TradeContext.sStartNo[i] ) - int( sTempStartNo ) ) )+ "',\
                      ENDNO = '" + sStartNoMulti + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + sTempStartNo + "' \
                       and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                       and BESBNO = '" + TradeContext.sBesbNo + "'\
                       and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                       and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                       and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                       and CUR ='"+ TradeContext.sCur+"'"
    
                    AfaLoggerFunc.tradeDebug('2'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
                    else:
                        #更新成功后再新增出库记录
                        sqlStr = "insert into VOUH_REGISTER \
                         (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,\
                          VOUHSTATUS,VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                          values \
                          ('" + TradeContext.sInBesbNo + "',\
                           '" + TradeContext.sInTellerTailNo + "','"+TradeContext.sDepository+"','"+ TradeContext.sCur+"',\
                           '"+ TradeContext.sVouhType[i] + "',\
                           '" + TradeContext.sStartNo[i] + "','" + sTempEndNo + "',\
                           '" + TradeContext.sTellerTailNo +"','"+ TradeContext.sVouhStatus+ "',\
                           '" + TradeContext.sVouhNum[i] + "',\
                           '" + TradeContext.sLstTrxDay + "','" + TradeContext.sLstTrxTime + "')"
                        record = AfaDBFunc.InsertSql( sqlStr )
                        if record == -1 or record == 0:
                            AfaLoggerFunc.tradeInfo( '数据库回滚' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'失败!')
                            raise AfaFlowControl.flowException( )
                        else: #调配成功
                            tradeExit('0000', TradeContext.sTransType+'成功')
        
                #输入的起始号码与区间的起始号码相同
                elif ( int( TradeContext.sStartNo[i] ) == int( sTempStartNo ) ):
                    #更新数据库中已存记录,更新成功后再新增出库记录
                    sqlStr = "update VOUH_REGISTER set \
                        VOUHNUM = '" + str( int( sTempEndNo ) - int ( TradeContext.sEndNo[i] ) )+ "',\
                        STARTNO = '" + sEndNoAdd + "'"
                    sqlStr = sqlStr + " where ENDNO = '" + sTempEndNo + "' \
                        and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                        and BESBNO = '" + TradeContext.sBesbNo + "'\
                        and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                        and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                        and CUR ='"+ TradeContext.sCur+"'"
    
                    AfaLoggerFunc.tradeDebug('3'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
                    else:
                        #更新成功后再新增出库记录
                        sqlStr = "insert into VOUH_REGISTER \
                           (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,\
                            VOUHSTATUS,VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                            values \
                            ('" + TradeContext.sInBesbNo + "',\
                             '" + TradeContext.sInTellerTailNo + "','"+TradeContext.sDepository+"',\
                             '" + TradeContext.sCur+"',\
                             '" + TradeContext.sVouhType[i]+"',\
                             '" + sTempStartNo + "',\
                             '" + TradeContext.sEndNo[i] + "','"+TradeContext.sTellerTailNo+"',\
                             '" + TradeContext.sVouhStatus+ "','" + TradeContext.sVouhNum[i] + "',\
                             '" + TradeContext.sLstTrxDay + "',\
                             '" + TradeContext.sLstTrxTime + "')"
                        AfaLoggerFunc.tradeDebug('1'+sqlStr)
                        record = AfaDBFunc.InsertSql( sqlStr )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '数据库回滚' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'失败!')
                            raise AfaFlowControl.flowException( )
                        else: #调配成功
                            tradeExit('0000', TradeContext.sTransType+'成功')
                #输入的起止号码完全包含在区间之内
                else:
                    #1更新数据库中已存记录,更新成功后再新增出库记录和相应登记未出状态记录
                    sqlStr = "update VOUH_REGISTER set \
                       VOUHNUM = '" + str( int( TradeContext.sStartNo[i] ) - int( sTempStartNo ) ) + "',\
                       ENDNO = '" + sStartNoMulti + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + sTempStartNo + "' \
                        and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                        and BESBNO = '" + TradeContext.sBesbNo + "'\
                        and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                        and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                        and CUR ='"+ TradeContext.sCur+"'"
    
                    AfaLoggerFunc.tradeDebug('4'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', '新增[凭证登记表]基本信息失败!')
                        raise AfaFlowControl.flowException( )
    
                    #2##############更新成功后再新增出库记录###########################################
                    sqlStr = "insert into VOUH_REGISTER \
                       (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,\
                        VOUHSTATUS,VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                        values \
                        ('" + TradeContext.sInBesbNo + "',\
                         '" + TradeContext.sInTellerTailNo + "','"+TradeContext.sDepository+"',\
                         '" + TradeContext.sCur+"',\
                         '" + TradeContext.sVouhType[i]+"',\
                         '" + TradeContext.sStartNo[i] + "',\
                         '" + TradeContext.sEndNo[i] + "','"+TradeContext.sTellerTailNo+"',\
                         '" + TradeContext.sVouhStatus+ "','" + TradeContext.sVouhNum[i] + "',\
                         '" + TradeContext.sLstTrxDay + "',\
                         '" + TradeContext.sLstTrxTime + "')"
                    AfaLoggerFunc.tradeDebug('2'+sqlStr)
                    record = AfaDBFunc.InsertSql( sqlStr )
                    if record == -1 or record == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
    
                    #3新增新增出库记录成功后,新增相应登记未出状态记录
                    sqlStr = "insert into VOUH_REGISTER \
                      (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,\
                        VOUHSTATUS,VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                       values \
                       ('" + TradeContext.sBesbNo + "',\
                        '" + sTempTellerNo + "','"+TradeContext.sExDepos+ "','"+TradeContext.sCur+"',\
                        '" + TradeContext.sVouhType[i]+"',\
                        '" + sEndNoAdd + "',\
                        '" + sTempEndNo + "','"+sTempRivTeller+"',\
                        '"+ TradeContext.sExStatus+ "',\
                        '" + str( int( sTempEndNo ) - int ( TradeContext.sEndNo[i] ) )+ "',\
                        '" + sTempLstTrxDay + "',\
                        '" + sTempLstTrxTime + "')"
                    AfaLoggerFunc.tradeDebug('3'+sqlStr)
                    record = AfaDBFunc.InsertSql( sqlStr )
                    if record == -1 or record == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
                    #新增成功
                    tradeExit('0000', '操作成功')
        
            else:      #判断前后连续关系
                #continue:前后连续标识;
                #FrontContinue:前连续标识;
                #BackContinue:后连续标识;
                for x in range( len(records) ):
                    if ( ( int( TradeContext.sStartNo[i] ) - 1 )  == int( records[x][1] ) ): #前连续
                        sTempStart = records[x][0] #records[x][0]:数据库中满足查询条件的凭证起始号码
                        if ( sFlagContinue == 'BackContinue' ):
                            sFlagContinue = 'Continue'
                        else:
                            sFlagContinue = 'FrontContinue'
                    if ( (int( TradeContext.sEndNo[i]) + 1 )  == int( records[x][0] ) ):  #后连续
                        sTempEnd   = records[x][1] #records[x][1]:数据库中满足查询条件的凭证终止号码
                        if ( sFlagContinue == 'FrontContinue' ):
                            sFlagContinue = 'Continue'
                        else:
                            sFlagContinue = 'BackContinue'
        
                #输入的凭证号码与库表中同凭证状态为登记未出的记录存在后连续关系,
                #则与相应的记录进行向后归并
                if (  sFlagContinue == 'BackContinue' ):
                    #1后连续:更新相应数据库中[凭证登记表]相应记录
                    sqlStr = "update VOUH_REGISTER set \
                      VOUHNUM = '" + str( int( sTempEnd ) - int( TradeContext.sStartNo[i] ) + 1 ) + "',\
                      LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                      LSTTRXTIME = '" + TradeContext.sLstTrxTime + "',\
                      STARTNO = '" + TradeContext.sStartNo[i] + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + sEndNoAdd  + "'\
                      and TELLERNO = '" + TradeContext.sInTellerTailNo + "' \
                      and BESBNO = '" + TradeContext.sInBesbNo + "'\
                      and CUR = '" + TradeContext.sCur + "'\
                      and DEPOSITORY = '" + TradeContext.sDepository + "'\
                      and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                      and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'"
                    AfaLoggerFunc.tradeDebug('5'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
    
                        #2更新成功后,删除起始号码为sTempStartNo的原记录,输入凭证数量为1
                    if ( int( sTempStartNo ) == int( TradeContext.sStartNo[i] ) ) :
                        sqlDel = "delete from VOUH_REGISTER \
                            where STARTNO = '" + sTempStartNo + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
                        AfaLoggerFunc.tradeDebug(sqlDel)
                        record = AfaDBFunc.DeleteSql( sqlDel )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '数据库回滚' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'失败!')
                            raise AfaFlowControl.flowException( )
                        else:
                            tradeExit('0000', TradeContext.sTransType+'成功')
                    else:
                        #更新成功后,更新终止号码为TradeContext.sEndNo的原记录,输入凭证数量大于1
                        sqlStr = "update VOUH_REGISTER set \
                          VOUHNUM = '" + str( int( TradeContext.sStartNo[i] ) - int( sTempStartNo ) )+ "',\
                          LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                          LSTTRXTIME = '" + TradeContext.sLstTrxTime + "',\
                          ENDNO = '" +  sStartNoMulti  + "'"
                        sqlStr = sqlStr + " where ENDNO = '" + TradeContext.sEndNo[i] + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
    
                        AfaLoggerFunc.tradeDebug('6'+sqlStr)
                        record = AfaDBFunc.UpdateSql( sqlStr )
                        if record == -1 or record == 0:
                            AfaLoggerFunc.tradeInfo( '数据库回滚' )
                            record = AfaDBFunc.RollbackSql( )  #回滚
                            tradeExit('A005062', TradeContext.sTransType+'失败!')
                            raise AfaFlowControl.flowException( )
                        else:
                            tradeExit('0000', '操作成功')
        
                #输入的凭证号码与库表中同凭证状态为登记未出存在前连续关系,
                #则与相应的记录进行向前归并
                elif ( sFlagContinue == 'FrontContinue' ):
                    #前连续:更新相应数据库中[凭证登记表]相应记录
                    sqlStr = "update VOUH_REGISTER set \
                       VOUHNUM = '" + str( int( TradeContext.sEndNo[i] ) - int( sTempStart ) + 1 ) + "',\
                       LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                       LSTTRXTIME = '" + TradeContext.sLstTrxTime + "',\
                       ENDNO = '" + ( TradeContext.sEndNo[i] ) + "'"
                    sqlStr = sqlStr + " where ENDNO = '" + sStartNoMulti + "'\
                        and TELLERNO = '" + TradeContext.sInTellerTailNo + "' \
                        and BESBNO = '" + TradeContext.sInBesbNo + "'\
                        and CUR = '" + TradeContext.sCur + "'\
                        and DEPOSITORY = '" + TradeContext.sDepository + "'\
                        and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'"
    
                    AfaLoggerFunc.tradeDebug('7'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        AfaDBFunc.RollbackSql( )  #回滚
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
    
                    #2更新成功后,删除起始号码为sTempStartNo的原记录,输入凭证数量为1
                    if ( int( sTempEndNo ) == int( TradeContext.sEndNo[i] ) ) :
                        sqlDel = "delete from VOUH_REGISTER \
                            where STARTNO = '" + sTempStartNo + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
    
                        AfaLoggerFunc.tradeDebug(sqlDel)
                        record = AfaDBFunc.DeleteSql( sqlDel )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '数据库回滚' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'失败!')
                            raise AfaFlowControl.flowException( )
                        else:    #更新成功
                            tradeExit('0000', '操作成功')
                    else:
                        #更新成功后,更新起始号码为TradeContext.sStartNo的原记录,输入凭证数量大于1
                        sqlStr = "update VOUH_REGISTER set \
                           VOUHNUM = '" + str( int( sTempEndNo ) - int( TradeContext.sEndNo[i] ) ) + "',\
                           LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                           LSTTRXTIME = '" + TradeContext.sLstTrxTime + "',\
                           STARTNO = '" + sEndNoAdd  + "'"
                        sqlStr = sqlStr + " where STARTNO = '" + TradeContext.sStartNo[i] + "' \
                           and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
    
                        AfaLoggerFunc.tradeDebug('8'+sqlStr)
                        record = AfaDBFunc.UpdateSql( sqlStr )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '数据库回滚' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'失败!')
                            raise AfaFlowControl.flowException( )
                        else:   #更新成功
                            tradeExit('0000', '操作成功')
        
            #输入的凭证号码与库表中同凭证状态为登记未出存在前后连续关系,
            #则与相应的记录进行前后归并
                elif (  sFlagContinue == 'Continue' ):
                    sTemVouhNum = str( int(sTempEnd) - int(sTempStart) + 1 )
                    #更新数据库表[凭证登记表]内相应记录
                    sqlStr = "update VOUH_REGISTER set \
                       ENDNO = '" + sTempEnd + "', \
                       VOUHNUM = '" + sTemVouhNum + "',\
                       LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                       LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + sTempStart + "' \
                       and TELLERNO = '" + TradeContext.sInTellerTailNo + "' \
                        and BESBNO = '" + TradeContext.sInBesbNo + "'\
                        and CUR = '" + TradeContext.sCur + "'\
                        and DEPOSITORY = '" + TradeContext.sDepository + "'\
                        and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'"
    
                    AfaLoggerFunc.tradeDebug('9'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
    
                    #2归并成功后,删除归并后其余一条
                    sqlDel = "delete from VOUH_REGISTER \
                       where STARTNO = '" + TradeContext.sStartNo[i] + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
                    AfaLoggerFunc.tradeDebug(sqlDel)
                    record = AfaDBFunc.DeleteSql( sqlDel )
                    if record == -1 or record == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
                    # 3
                    sqlDel = "delete from VOUH_REGISTER \
                      where STARTNO = '" + sEndNoAdd + "' \
                        and TELLERNO = '" + TradeContext.sInTellerTailNo + "' \
                        and BESBNO = '" + TradeContext.sInBesbNo + "'\
                        and CUR = '" + TradeContext.sCur + "'\
                        and DEPOSITORY = '" + TradeContext.sDepository + "'\
                        and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'"
                    AfaLoggerFunc.tradeDebug(sqlDel)
                    record = AfaDBFunc.DeleteSql( sqlDel )
                    if record == -1 or record == 0 :
                        AfaLoggerFunc.tradeInfo( '数据库回滚' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'失败!')
                        raise AfaFlowControl.flowException( )
    
                    tradeExit('0000', '操作成功')
                        
    return True
                        
#=========================日志==================================================
def WrtLog(logstr):

    #默认向文件和屏幕同时输出
    AfaLoggerFunc.tradeInfo(logstr)
    print logstr

    return True             
                        
                        

if __name__=='__main__':

#    TradeContext.sLstTrxDay      = '1'   #工作日期
#    TradeContext.sLstTrxTime     = '1'   #工作时间
#    TradeContext.sZoneNo         = '1'   #分行号
#    TradeContext.sBraNo          = '1'   #行所号
#    TradeContext.sTellerNo       = '1'   #柜员号
#    TradeContext.sVouhType       = '1'   #凭证种类
#    TradeContext.sHeadStr        = '1'   #冠字号
#    TradeContext.sStartNo        = '1'   #起始号码
#    TradeContext.sEndNo          = '1'   #终止号码
#    TradeContext.sRivTeller      = '1'   #对方柜员
#    TradeContext.sDepository     = '1'   #库箱标志
#    TradeContext.sExDepos        = '1'   #原库箱标志
#    TradeContext.sVouhStatus     = '1'   #状态
#    TradeContext.sExStatus       = '1'   #原状态
#    TradeContext.sSummary        = '1'   #摘要
#    AfaLoggerFunc.afa_SendStruct()
#    x = VouhModify()
#    print x
    print time.strftime( '%m%d%y%H%M%S', time.localtime( ) )
    sPid = "%08d"%( os.getpid( ))
    print sPid
