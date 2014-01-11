# -*- coding: gbk -*-
################################################################################
#   批量业务系统：录入企业信息
#===============================================================================
#   交易文件:   T001000_8423.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  胡友
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,NGSFAbdtFunc,AfaAfeFunc
from types import *

#=====================录入企业信息==============================================
def TrxMain( ):
    AfaLoggerFunc.tradeInfo('**********录入企业信息(8423)开始**********')

    #TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    #TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间
    
    #判断单位协议是否有效
    if ( not NGSFAbdtFunc.ChkUnitInfo( ) ):
        return False

    #判断企业协议是否存在
    if ( not ChkCustInfo( ) ):
        return False

    #查询账户信息(主机)
    if ( not NGSFAbdtFunc.QueryAccInfo( ) ):
        return False
        
    #合法性校验
    AfaLoggerFunc.tradeInfo('>>>判断银行账户状态')
    if ( TradeContext.ACCSTATUS != "0"):
        return ExitSubTrade( '9000', '客户银行账户状态异常,不能进行注册' )

    #AfaLoggerFunc.tradeInfo('>>>判断是否需要校验证件号码')
    #if ( TradeContext.I1IDCHKFLAG == "1" ):
    #    if (TradeContext.IDCODE != TradeContext.I1IDCODE):
    #        return ExitSubTrade( '9000', '客户证件号码不正确,不能进行注册' )

    AfaLoggerFunc.tradeInfo('>>>判断是否需要校验客户姓名')
    if (TradeContext.USERNAME != TradeContext.PayerName):
        return ExitSubTrade( '9000', '客户名称不正确,不能进行注册' )

    #自动生成企业协议编号
    if ( AfaFunc.GetSerialno() < 0 ):
        return ExitSubTrade( '9000', '生成企业协议编号失败' )

    #组织企业协议编码(交易日期 + 中间业务流水号)
    TradeContext.Protocolno = TradeContext.TranDate + TradeContext.agentSerialno

    #签约方式  三方签约
    #if (TradeContext.SIGNUPMODE=="1"):
    #    #系统标识
    #    TradeContext.sysId = TradeContext.Appno + TradeContext.PayeeUnitno
    #
    #    #不使用转换返回码
    #    TradeContext.__respFlag__="0"
    #  
    #    AfaAfeFunc.CommAfe()
    #
    #    if TradeContext.errorCode!='0000' :
    #        return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )

    #增加企业协议信息
    if ( not InsertCustInfo( ) ):
        return False

    AfaLoggerFunc.tradeInfo('**********录入企业信息(8423)结束**********')

    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True

#判断企业协议是否存在
def ChkCustInfo( ):
    AfaLoggerFunc.tradeInfo('>>>判断企业协议是否存在')

    try:
        sql = ""
        sql = "SELECT PROTOCOLNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.Appno        + "'" + " AND "       #业务编号
        sql = sql + "BUSINO="     + "'" + TradeContext.PayeeUnitno  + "'" + " AND ("      #单位编号
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.PayerUnitno  + "'" + " OR "        #商户客户编号
        sql = sql + "BANKUSERNO=" + "'" + TradeContext.PayerAccno[0:12] + "'" + " OR "        #银行客户编号
        sql = sql + "ACCNO="      + "'" + TradeContext.PayerAccno   + "'" + ") AND "      #银行账号
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                 #状态

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询企业协议信息异常' )
    
        if ( len(records) > 0 ):
            return ExitSubTrade( '9000', '该企业协议已经被注册,不能再次进行注册')

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断企业协议信息是否存在异常')

#增加企业协议信息
def InsertCustInfo( ):
    AfaLoggerFunc.tradeInfo('>>>增加企业协议信息')

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

        sql = sql + "'" + TradeContext.Appno           + "',"        #业务编号
        sql = sql + "'" + TradeContext.PayeeUnitno     + "',"        #单位编号
        sql = sql + "'" + TradeContext.PayerUnitno     + "',"        #商户客户编号
        sql = sql + "'" + TradeContext.PayerUnitno     + "',"        #商户客户应用编号
        sql = sql + "'" + TradeContext.PayerAccno[0:12]    + "',"    #银行客户编号
        sql = sql + "'" + '49'                         + "',"        #凭证类型
        sql = sql + "'" + TradeContext.PayerAccno[0:12]+ "',"        #凭证号
        sql = sql + "'" + TradeContext.PayerAccno      + "',"        #活期存款帐号
        sql = sql + "'" + ' '                          + "',"        #子帐号
        sql = sql + "'" + '01'                         + "',"        #币种
        sql = sql + "'" + '0'                          + "',"        #交易限额
        sql = sql + "'" + TradeContext.PartFlag        + "',"        #部分扣款标志
        sql = sql + "'" + TradeContext.Protocolno      + "',"        #协议编号
        sql = sql + "'" + TradeContext.ContractDate    + "',"        #签约日期(合同日期)
        sql = sql + "'" + TradeContext.StartDate       + "',"        #生效日期
        sql = sql + "'" + TradeContext.EndDate         + "',"        #失效日期
        sql = sql + "'" + '0'                          + "',"        #密码验证标志
        sql = sql + "'" + "****************"           + "',"        #密码
        sql = sql + "'" + '0'                          + "',"        #证件验证标志
        sql = sql + "'" + '01'                         + "',"        #证件类型
        sql = sql + "'" + ' '                          + "',"        #证件号码
        sql = sql + "'" + '0'                          + "',"        #姓名验证标志
        sql = sql + "'" + TradeContext.PayerName       + "',"        #客户姓名
        sql = sql + "'" + TradeContext.Tel             + "',"        #联系电话
        sql = sql + "'" + TradeContext.Address         + "',"        #联系地址
        sql = sql + "'" + ' '                          + "',"        #邮编
        sql = sql + "'" + ' '                          + "',"        #电子邮箱
        sql = sql + "'" + '1'                          + "',"        #状态
        sql = sql + "'" + TradeContext.zoneno          + "',"        #地区号
        sql = sql + "'" + TradeContext.brno            + "',"        #网点号(机构代码)
        sql = sql + "'" + TradeContext.tellerno        + "',"        #柜员号
        sql = sql + "'" + TradeContext.TranDate        + "',"        #录入日期
        sql = sql + "'" + TradeContext.TranTime        + "',"        #录入时间
        sql = sql + "'" + ' '                          + "',"        #备注1
        sql = sql + "'" + TradeContext.UserName        + "',"        #付款单位名称
        sql = sql + "'" + TradeContext.PayeeAccno      + "',"        #收款单位账号
        sql = sql + "'" + ' '                          + "',"        #备注4
        sql = sql + "'" + TradeContext.PayeeName       + "')"        #收款单位名称
        

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '增加企业协议信息失败')

        #TradeContext.tradeResponse.append(['O1USERNAME',     TradeContext.USERNAME])        #用户名称
        #TradeContext.tradeResponse.append(['O1IDTYPE',       TradeContext.IDTYPE])          #证件类型
        #TradeContext.tradeResponse.append(['O1IDCODE',       TradeContext.IDCODE])          #证件号码
        #TradeContext.tradeResponse.append(['O1PROTOCOLNO',   TradeContext.PROTOCOLNO])      #协议号
        #TradeContext.tradeResponse.append(['O1WORKDATE',     TradeContext.TranDate])        #注册日期
        #TradeContext.tradeResponse.append(['O1WORKTIME',     TradeContext.TranTime])        #注册日期

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '增加企业协议信息异常')

def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False