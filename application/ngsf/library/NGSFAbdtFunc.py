# -*- coding: gbk -*-
###############################################################################
# 文件名称：AbdtFunc.py
# 文件标识：
# 摘    要：批量业务公共库
#
# 当前版本：2.0
# 作    者：XZH
# 完成日期：2008年06月10日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import TradeContext,AfaUtilTools,AfaFunc,AfaDBFunc,ConfigParser,sys,os,time,AfaHostFunc,AfaLoggerFunc,HostContext
from types import *

#========================单位协议校验=============================
def ChkUnitInfo( ):
    AfaLoggerFunc.tradeInfo('>>>判断单位协议是否有效')

    try:
        sql = ""
        sql = "SELECT SIGNUPMODE,GETUSERNOMODE,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO,AGENTTYPE,VOUHNO FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + TradeContext.Appno       + "'" + " AND "        #业务编号
        sql = sql + "BUSINO=" + "'" + TradeContext.PayeeUnitno + "'" + " AND "        #单位编号
        sql = sql + "STATUS=" + "'" + "1"                      + "'"                  #状态

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询单位协议信息异常' )
    
        if ( len(records) <= 0 ):
            return ExitSubTrade( '9000', '没有单位协议信息,不能进行此类操作')

        #过滤None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.SIGNUPMODE    = str(records[0][0])                             #签约方式
        TradeContext.GETUSERNOMODE = str(records[0][1])                             #商户客户编号获取方式
        TradeContext.STARTDATE     = str(records[0][2])                             #生效日期
        TradeContext.ENDDATE       = str(records[0][3])                             #失效日期
        TradeContext.STARTTIME     = str(records[0][4])                             #服务开始时间
        TradeContext.ENDTIME       = str(records[0][5])                             #服务终止时间
        TradeContext.ACCNO         = str(records[0][6])                             #对公账户
        TradeContext.AGENTTYPE     = str(records[0][7])                             #委托方式
        TradeContext.VOUHNO        = str(records[0][8])                             #凭证号(内部帐户)

        AfaLoggerFunc.tradeInfo( "TranDate=[" + TradeContext.TranDate + "]" )

        if ( (TradeContext.STARTDATE > TradeContext.TranDate) or (TradeContext.TranDate > TradeContext.ENDDATE) ):
            return ExitSubTrade( '9000', '该单位委托协议还没有生效或已过有效期')

        if ( (TradeContext.STARTTIME > TradeContext.TranTime) or (TradeContext.TranTime > TradeContext.ENDTIME) ):
            return ExitSubTrade( '9000', '已经超过该系统的服务时间,该业务必须在[' + s_StartDate + ']-[' + s_EndDate + ']时间段运行')

        if ((TradeContext.SIGNUPMODE=="1") and (TradeContext.GETUSERNOMODE=="1")):
            #发送到通讯前置并从第三方获取协议
            return True

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断单位协议信息是否存在失败')

#========================账户查询(主机)=============================
def QueryAccInfo( ):
    AfaLoggerFunc.tradeInfo(">>>查询账户信息(主机)")

    try:
        #通讯区打包
        HostContext.I1TRCD = '8810'                        #主机交易码
        HostContext.I1SBNO = TradeContext.brno             #该交易的发起机构
        HostContext.I1USID = TradeContext.tellerno         #交易柜员号
        HostContext.I1AUUS = TradeContext.authteller       #授权柜员
        HostContext.I1AUPS = TradeContext.authtellerpwd    #授权柜员密码
        HostContext.I1WSNO = TradeContext.termId           #终端号
        HostContext.I1ACNO = TradeContext.PayerAccno       #帐号
        HostContext.I1CYNO = '01'                          #币种

        #if ( TradeContext.I1PASSCHKFLAG == "1" ):
        #    HostContext.I1CFFG = "0"                       #密码校验标志(需要)
        #else:
        #    HostContext.I1CFFG = "1"                       #密码校验标志(不需要)
        HostContext.I1CFFG = '1'

        HostContext.I1PSWD = ''                            #密码
        HostContext.I1CETY = ''                            #凭证种类
        HostContext.I1CCSQ = ''                            #凭证号码
        HostContext.I1CTFG = '0'                           #钞汇标志

        #与主机通讯
        if not AfaHostFunc.CommHost('8810'):
            return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )
            
        #缓冲主机返回信息
        TradeContext.USERNAME   = HostContext.O1CUNM        #用户名称
        TradeContext.IDTYPE     = HostContext.O1IDTY        #证件类型
        TradeContext.IDCODE     = HostContext.O1IDNO        #证件号码
        TradeContext.ACCSTATUS  = HostContext.O1ACST        #账户状态

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '查询账户信息(主机)异常')

#========================账户查询(VMENU直接查询)=============================
def VMENU_QueryAccInfo():
    AfaLoggerFunc.tradeInfo('>>>查询账户信息')

    try:
        #通讯区打包
        HostContext.I1TRCD = '8810'                        #主机交易码
        HostContext.I1SBNO = TradeContext.I1SBNO           #该交易的发起机构
        HostContext.I1USID = TradeContext.I1USID           #交易柜员号
        HostContext.I1AUUS = TradeContext.I1AUUS           #授权柜员
        HostContext.I1AUPS = TradeContext.I1AUPS           #授权柜员密码
        HostContext.I1WSNO = TradeContext.I1WSNO           #终端号
        HostContext.I1ACNO = TradeContext.I1ACCNO          #帐号
        HostContext.I1CYNO = '01'                          #币种
        HostContext.I1CFFG = '1'                           #密码校验标志(0-需要,1-不需要)
        HostContext.I1PSWD = ''                            #密码
        HostContext.I1CETY = TradeContext.I1VOUHTYPE       #凭证种类
        HostContext.I1CCSQ = TradeContext.I1VOUHNO         #凭证号码
        HostContext.I1CTFG = TradeContext.I1CHFLAG         #钞汇标志

        #与主机通讯
        if not AfaHostFunc.CommHost('8810'):
            return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )

        if ( HostContext.O1REKD == '900' ):
            return ExitSubTrade( '9000', '非个人结算户,不能操作' )

        TradeContext.tradeResponse.append(['O1USERNAME', HostContext.O1CUNM])   #客户姓名
        TradeContext.tradeResponse.append(['O1IDTYPE',   HostContext.O1IDTY])   #证件种类
        TradeContext.tradeResponse.append(['O1IDCODE',   HostContext.O1IDNO])   #证件号码
        TradeContext.tradeResponse.append(['O1MAFG',     HostContext.O1MAFG])   #公司卡/个人卡标志(0:单位 1:个人)
        TradeContext.tradeResponse.append(['O1REKD',     HostContext.O1REKD])   #账户类型(特殊处理：900-非个人结算户)
        TradeContext.tradeResponse.append(['O1ACBL',     HostContext.O1ACBL])   #账户余额
        TradeContext.tradeResponse.append(['O1CUBL',     HostContext.O1CUBL])   #可用余额
        TradeContext.tradeResponse.append(['O1DATA',     HostContext.O1ITEM])   #附加信息(科目代码)

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '查询账户信息异常(主机)' )

#========================退出模块=============================
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
         
#========================读取批量配置文件=============================      
def getBatchConfig( cfgFileName = None ): 

    try:
        config = ConfigParser.ConfigParser( )
        if ( cfgFileName == None ):
            cfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open( cfgFileName ) )
        TradeContext.BATCH_APPTRFG    = config.get( 'BATCH', 'APPTRFG' )
        TradeContext.BATCH_MAXCOUNT   = config.get( 'BATCH', 'MAXCOUNT' )
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '读取配置文件异常' )