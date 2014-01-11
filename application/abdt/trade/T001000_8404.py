# -*- coding: gbk -*-
################################################################################
#   批量业务系统：录入个人信息
#===============================================================================
#   交易文件:   T001000_8404.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,AbdtFunc,AfaAfeFunc
from types import *


#=====================录入个人信息==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********录入个人信息(8404)开始**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间


    #判断单位协议是否有效
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    #判断个人协议是否存在
    if ( not ChkCustInfo( ) ):
        return False


    #查询账户信息(主机)
    if ( not AbdtFunc.QueryAccInfo( ) ):
        return False
        

    #合法性校验
    AfaLoggerFunc.tradeInfo('>>>判断银行账户状态')
    if ( TradeContext.ACCSTATUS != "0"):
        return ExitSubTrade( '9000', '客户银行账户状态异常,不能进行注册' )


    AfaLoggerFunc.tradeInfo('>>>判断是否需要校验证件号码')
    if ( TradeContext.I1IDCHKFLAG == "1" ):
        if (TradeContext.IDCODE != TradeContext.I1IDCODE):
            return ExitSubTrade( '9000', '客户证件号码不正确,不能进行注册' )


    AfaLoggerFunc.tradeInfo('>>>判断是否需要校验客户姓名')
    if ( TradeContext.I1NAMECHKFLAG == "1"):
        if (TradeContext.USERNAME != TradeContext.I1USERNAME):
            return ExitSubTrade( '9000', '客户名称不正确,不能进行注册' )


    #自动生成个人协议编号
    if ( AfaFunc.GetSerialno() < 0 ):
        return ExitSubTrade( '9000', '生成个人协议编号失败' )


    #组织个人协议编码(交易日期 + 中间业务流水号)
    TradeContext.PROTOCOLNO = TradeContext.TranDate + TradeContext.agentSerialno


    #签约方式
    if (TradeContext.SIGNUPMODE=="1"):
        
        #系统标识
        TradeContext.sysId = TradeContext.I1APPNO + TradeContext.I1BUSINO

        #不使用转换返回码
        TradeContext.__respFlag__="0"
      
        AfaAfeFunc.CommAfe()

        if TradeContext.errorCode!='0000' :
            return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )

    #增加个人协议信息
    if ( not InsertCustInfo( ) ):
        return False

           
    AfaLoggerFunc.tradeInfo('**********录入个人信息(8404)结束**********')


    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True



#判断个人协议是否存在
def ChkCustInfo( ):

    AfaLoggerFunc.tradeInfo('>>>判断个人协议是否存在')

    try:
        sql = ""
        sql = "SELECT PROTOCOLNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "       #业务编号
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND ("      #单位编号
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.I1BUSIUSERNO + "'" + " OR "        #商户客户编号
        sql = sql + "BANKUSERNO=" + "'" + TradeContext.I1BANKUSERNO + "'" + " OR "        #银行客户编号
        sql = sql + "ACCNO="      + "'" + TradeContext.I1ACCNO      + "'" + ") AND "      #银行账号
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                 #状态

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询个人协议信息异常' )
    
        if ( len(records) > 0 ):
            return ExitSubTrade( '9000', '该个人协议已经被注册,不能再次进行注册')

        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断个人协议信息是否存在异常')


#增加个人协议信息
def InsertCustInfo( ):

    AfaLoggerFunc.tradeInfo('>>>增加个人协议信息')

    try:

        sql = ""

        sql = "INSERT INTO ABDT_CUSTINFO("
        sql = sql + "APPNO,"
        sql = sql + "BUSINO,"
        sql = sql + "BUSIUSERNO,"
        sql = sql + "BUSIUSERAPPNO,"
        sql = sql + "BANKUSERNO,"
        sql = sql + "VOUHTYPE,"
        sql = sql + "VOUHNO,"
        sql = sql + "ACCNO,"
        sql = sql + "SUBACCNO,"
        sql = sql + "CURRTYPE,"
        sql = sql + "LIMITAMT,"
        sql = sql + "PARTFLAG,"
        sql = sql + "PROTOCOLNO,"
        sql = sql + "CONTRACTDATE,"
        sql = sql + "STARTDATE,"
        sql = sql + "ENDDATE,"
        sql = sql + "PASSCHKFLAG,"
        sql = sql + "PASSWD,"
        sql = sql + "IDCHKFLAG,"
        sql = sql + "IDTYPE,"
        sql = sql + "IDCODE,"
        sql = sql + "NAMECHKFLAG,"
        sql = sql + "USERNAME,"
        sql = sql + "TEL,"
        sql = sql + "ADDRESS,"
        sql = sql + "ZIPCODE,"
        sql = sql + "EMAIL,"
        sql = sql + "STATUS,"
        sql = sql + "ZONENO,"
        sql = sql + "BRNO,"
        sql = sql + "TELLERNO,"
        sql = sql + "INDATE,"
        sql = sql + "INTIME,"
        sql = sql + "NOTE1,"
        sql = sql + "NOTE2,"
        sql = sql + "NOTE3,"
        sql = sql + "NOTE4,"
        sql = sql + "NOTE5)"

        sql = sql + " VALUES ("

        sql = sql + "'" + TradeContext.I1APPNO         + "',"        #业务编号
        sql = sql + "'" + TradeContext.I1BUSINO        + "',"        #单位编号
        sql = sql + "'" + TradeContext.I1BUSIUSERNO    + "',"        #商户客户编号
        sql = sql + "'" + TradeContext.I1BUSIUSERAPPNO + "',"       #商户客户应用编号
        sql = sql + "'" + TradeContext.I1BANKUSERNO    + "',"        #银行客户编号
        sql = sql + "'" + TradeContext.I1VOUHTYPE      + "',"        #凭证类型
        sql = sql + "'" + TradeContext.I1VOUHNO        + "',"        #凭证号
        sql = sql + "'" + TradeContext.I1ACCNO         + "',"        #活期存款帐号
        sql = sql + "'" + TradeContext.I1SUBACCNO      + "',"        #子帐号
        sql = sql + "'" + TradeContext.I1CURRTYPE      + "',"        #币种
        sql = sql + "'" + TradeContext.I1LIMITAMT      + "',"        #交易限额
        sql = sql + "'" + TradeContext.I1PARTFLAG      + "',"        #部分扣款标志
        sql = sql + "'" + TradeContext.PROTOCOLNO      + "',"        #协议编号
        sql = sql + "'" + TradeContext.I1CONTRACTDATE  + "',"        #签约日期(合同日期)
        sql = sql + "'" + TradeContext.I1STARTDATE     + "',"        #生效日期
        sql = sql + "'" + TradeContext.I1ENDDATE       + "',"        #失效日期
        sql = sql + "'" + TradeContext.I1PASSCHKFLAG   + "',"        #密码验证标志
        sql = sql + "'" + "****************"           + "',"        #密码
        sql = sql + "'" + TradeContext.I1IDCHKFLAG     + "',"        #证件验证标志
        sql = sql + "'" + TradeContext.IDTYPE          + "',"        #证件类型
        sql = sql + "'" + TradeContext.IDCODE          + "',"        #证件号码
        sql = sql + "'" + TradeContext.I1NAMECHKFLAG   + "',"        #姓名验证标志
        sql = sql + "'" + TradeContext.USERNAME        + "',"        #客户姓名
        sql = sql + "'" + TradeContext.I1TEL           + "',"        #联系电话
        sql = sql + "'" + TradeContext.I1ADDRESS       + "',"        #联系地址
        sql = sql + "'" + TradeContext.I1ZIPCODE       + "',"        #邮编
        sql = sql + "'" + TradeContext.I1EMAIL         + "',"        #电子邮箱
        sql = sql + "'" + TradeContext.I1STATUS        + "',"        #状态
        sql = sql + "'" + TradeContext.I1ZONENO        + "',"        #地区号
        sql = sql + "'" + TradeContext.I1SBNO          + "',"        #网点号(机构代码)
        sql = sql + "'" + TradeContext.I1USID          + "',"        #柜员号
        sql = sql + "'" + TradeContext.TranDate        + "',"        #录入日期
        sql = sql + "'" + TradeContext.TranTime        + "',"        #录入时间
        sql = sql + "'" + TradeContext.I1NOTE1         + "',"        #备注1
        sql = sql + "'" + TradeContext.I1NOTE2         + "',"        #备注2
        sql = sql + "'" + TradeContext.I1NOTE3         + "',"        #备注3
        sql = sql + "'" + TradeContext.I1NOTE4         + "',"        #备注4
        sql = sql + "'" + TradeContext.I1NOTE5         + "')"        #备注5

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '增加个人协议信息失败')


        TradeContext.tradeResponse.append(['O1USERNAME',     TradeContext.USERNAME])        #用户名称
        TradeContext.tradeResponse.append(['O1IDTYPE',       TradeContext.IDTYPE])          #证件类型
        TradeContext.tradeResponse.append(['O1IDCODE',       TradeContext.IDCODE])          #证件号码
        TradeContext.tradeResponse.append(['O1PROTOCOLNO',   TradeContext.PROTOCOLNO])      #协议号
        TradeContext.tradeResponse.append(['O1WORKDATE',     TradeContext.TranDate])        #注册日期
        TradeContext.tradeResponse.append(['O1WORKTIME',     TradeContext.TranTime])        #注册日期

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '增加个人协议信息异常')


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        