# -*- coding: gbk -*-
################################################################################
#   批量业务系统：维护个人信息
#===============================================================================
#   交易文件:   T001000_8406.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,AbdtFunc,AfaAfeFunc
from types import *


#=====================维护个人信息==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********维护个人信息(8406)开始**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间


    #判断单位协议是否有效
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    #判断个人协议是否有效
    if ( not ChkCustInfo( ) ):
        return False


    if ( TradeContext.I1PROCTYPE == '0' ):
        
        AfaLoggerFunc.tradeInfo('>>修改个人协议信息')


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

       #签约方式
        if (TradeContext.SIGNUPMODE=="1"):
            return ExitSubTrade( '9000', '三方签约方式,不能修改协议' )

        
        #修改个人协议信息(本地)
        if ( not UpdateCustInfo( ) ):
            return False

    else:

        AfaLoggerFunc.tradeInfo('>>注销个人协议信息')

       #签约方式
        if (TradeContext.SIGNUPMODE=="1"):
            
            AfaLoggerFunc.tradeInfo('>>>签约方式：三方：需要与企业进行交互')

            #系统标识
            TradeContext.sysId = TradeContext.I1APPNO
            
            #不使用转换返回码
            TradeContext.__respFlag__='0'
    
            AfaAfeFunc.CommAfe()

            if TradeContext.errorCode!='0000' :
                return ExitSubTrade( TradeContext.errorCode, TradeContext.errorMsg )

        #注销个人协议信息(本地)
        if ( not DeleteCustInfo( ) ):
            return False

        
    AfaLoggerFunc.tradeInfo('**********维护个人信息(8406)结束**********')


    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True



#判断个人协议是否有效
def ChkCustInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>判断个人协议是否有效')

    try:
        sql = "SELECT USERNAME,IDTYPE,IDCODE,PROTOCOLNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "       #业务编号
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND ("      #单位编号
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.I1BUSIUSERNO + "'" + " OR "        #商户客户编号
        sql = sql + "BANKUSERNO=" + "'" + TradeContext.I1BANKUSERNO + "'" + " OR "        #银行客户编号
        sql = sql + "ACCNO="      + "'" + TradeContext.I1ACCNO      + "'" + ") AND "      #银行账号
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                 #状态


        AfaLoggerFunc.tradeInfo( sql )


        records = AfaDBFunc.SelectSql( sql )
        if ( len(records) == 0 ):
            return ExitSubTrade('9000','没有该客户信息,不能进行相关的操作')


        #过滤None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.USERNAME  = str(records[0][0])
        TradeContext.IDTYPE    = str(records[0][1])
        TradeContext.IDCODE    = str(records[0][2])
        rPROTOCOLNO            = str(records[0][3])
        TradeContext.ACCSTATUS = "0"

        if ( rPROTOCOLNO != TradeContext.I1PROTOCOLNO ):
            return ExitSubTrade( '9000', '不能修改个人协议编码')

        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断个人协议信息是否存在异常')


#修改个人协议信息(本地)
def UpdateCustInfo( ):


    AfaLoggerFunc.tradeInfo(">>>修改个人协议信息(本地)")


    try:
        sql = "UPDATE ABDT_CUSTINFO SET "
#       sql = sql + "APPNO='"           + TradeContext.I1APPNO                           + "',"        #业务编号
#       sql = sql + "BUSINO='"          + TradeContext.I1BUSINO                          + "',"        #单位编号
        sql = sql + "BUSIUSERNO='"      + TradeContext.I1BUSIUSERNO                      + "',"        #商户客户编号
        sql = sql + "BUSIUSERAPPNO='"   + TradeContext.I1BUSIUSERAPPNO                   + "',"        #商户客户应用编号
        sql = sql + "BANKUSERNO='"      + TradeContext.I1BANKUSERNO                      + "',"        #银行客户编号
        sql = sql + "VOUHTYPE='"        + TradeContext.I1VOUHTYPE                        + "',"        #凭证类型
        sql = sql + "VOUHNO='"          + TradeContext.I1VOUHNO                          + "',"        #凭证号
        sql = sql + "ACCNO='"           + TradeContext.I1ACCNO                           + "',"        #活期存款帐号
        sql = sql + "SUBACCNO='"        + TradeContext.I1SUBACCNO                        + "',"        #子帐号
        sql = sql + "CURRTYPE='"        + TradeContext.I1CURRTYPE                        + "',"        #币种
        sql = sql + "LIMITAMT='"        + TradeContext.I1LIMITAMT                        + "',"        #交易限额
        sql = sql + "PARTFLAG='"        + TradeContext.I1PARTFLAG                        + "',"        #部分扣款标志
#       sql = sql + "PROTOCOLNO='"      + TradeContext.I1PROTOCOLNO                      + "',"        #协议编号
        sql = sql + "CONTRACTDATE='"    + TradeContext.I1CONTRACTDATE                    + "',"        #签约日期(合同日期)
        sql = sql + "STARTDATE='"       + TradeContext.I1STARTDATE                       + "',"        #生效日期
        sql = sql + "ENDDATE='"         + TradeContext.I1ENDDATE                         + "',"        #失效日期
        sql = sql + "PASSCHKFLAG='"     + TradeContext.I1PASSCHKFLAG                     + "',"        #密码验证标志
        sql = sql + "PASSWD='"          + TradeContext.I1PASSWD                          + "',"        #密码
        sql = sql + "IDCHKFLAG='"       + TradeContext.I1IDCHKFLAG                       + "',"        #证件验证标志
        sql = sql + "IDTYPE='"          + TradeContext.IDTYPE                            + "',"        #证件类型
        sql = sql + "IDCODE='"          + TradeContext.IDCODE                            + "',"        #证件号码
        sql = sql + "NAMECHKFLAG='"     + TradeContext.I1NAMECHKFLAG                     + "',"        #姓名验证标志
        sql = sql + "USERNAME='"        + TradeContext.USERNAME                          + "',"        #客户姓名
        sql = sql + "TEL='"             + TradeContext.I1TEL                             + "',"        #联系电话
        sql = sql + "ADDRESS='"         + TradeContext.I1ADDRESS                         + "',"        #联系地址
        sql = sql + "ZIPCODE='"         + TradeContext.I1ZIPCODE                         + "',"        #邮编
        sql = sql + "EMAIL='"           + TradeContext.I1EMAIL                           + "',"        #电子邮箱
        sql = sql + "STATUS='"          + TradeContext.I1STATUS                          + "',"        #状态
#       sql = sql + "ZONENO='"          + TradeContext.I1ZONENO                          + "',"        #地区号
#       sql = sql + "BRNO='"            + TradeContext.I1BRNO                            + "',"        #网点号(机构代码)
#       sql = sql + "TELLERNO='"        + TradeContext.I1TELLERNO                        + "',"        #柜员号
#       sql = sql + "INDATE='"          + TradeContext.I1INDATE                          + "',"        #录入日期
#       sql = sql + "INTIME='"          + TradeContext.I1INTIME                          + "',"        #录入时间
        sql = sql + "NOTE1='"           + TradeContext.I1USID                            + "',"        #备注1
        sql = sql + "NOTE2='"           + TradeContext.TranDate+TradeContext.TranTime    + "',"        #备注2
        sql = sql + "NOTE3='"           + TradeContext.I1NOTE3                           + "',"        #备注3
        sql = sql + "NOTE4='"           + TradeContext.I1NOTE4                           + "',"        #备注4
        sql = sql + "NOTE5='"           + TradeContext.I1NOTE5                           + "'"         #备注5

        sql = sql + " WHERE "

        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "            #业务编码
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND "            #单位编码
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND "            #单位编码
        sql = sql + "ZONENO="     + "'" + TradeContext.I1ZONENO     + "'" + " AND "            #地区代码
        sql = sql + "PROTOCOLNO=" + "'" + TradeContext.I1PROTOCOLNO + "'"                      #协议编码

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '修改个人协议信息失败')


        AfaLoggerFunc.tradeInfo(">>>总共修改[" + str(result) + "]条记录")


        TradeContext.tradeResponse.append(['O1USERNAME',     TradeContext.USERNAME])        #用户名称
        TradeContext.tradeResponse.append(['O1IDTYPE',       TradeContext.IDTYPE])          #证件类型
        TradeContext.tradeResponse.append(['O1IDCODE',       TradeContext.IDCODE])          #证件号码

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '修改个人协议信息异常')

    
    
#注销个人协议信息(本地)
def DeleteCustInfo( ):

    AfaLoggerFunc.tradeInfo(">>>注销客户信息(本地)")

    try:

        AfaLoggerFunc.tradeInfo(">>>修改注销日期和时间")

        sql = "UPDATE ABDT_CUSTINFO SET NOTE3='" + TradeContext.TranDate+TradeContext.TranTime + "'"

        sql = sql + " WHERE "

        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "        #业务编码
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND "        #单位编码
        sql = sql + "PROTOCOLNO=" + "'" + TradeContext.I1PROTOCOLNO + "'"                  #协议编码

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.UpdateSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '修改注销日期和时间失败')
        
        AfaLoggerFunc.tradeInfo(">>>把需要个人信息记录移到个人信息历史表中")

        sql = ""
        sql = "INSERT INTO ABDT_HIS_CUSTINFO SELECT * FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="       + "'" + TradeContext.I1APPNO      + "'" + " AND "        #业务编码
        sql = sql + "BUSINO="      + "'" + TradeContext.I1BUSINO     + "'" + " AND "        #单位编码
        sql = sql + "PROTOCOLNO="  + "'" + TradeContext.I1PROTOCOLNO + "'"                  #协议编码

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '注销个人协议信息失败(移动)')

        AfaLoggerFunc.tradeInfo(">>>总共移动[" + str(result) + "]条记录")


        AfaLoggerFunc.tradeInfo(">>>删除在个人信息表中被注销个人信息记录")
        sql = ""
        sql = "DELETE FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.I1APPNO      + "'" + " AND "        #业务编码
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO     + "'" + " AND "        #单位编码
        sql = sql + "PROTOCOLNO=" + "'" + TradeContext.I1PROTOCOLNO + "'"                  #协议编码

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.DeleteSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '注销个人协议信息失败(删除)')


        AfaLoggerFunc.tradeInfo(">>>总共删除[" + str(result) + "]条记录")


        TradeContext.tradeResponse.append(['O1USERNAME',     TradeContext.USERNAME])       #用户名称
        TradeContext.tradeResponse.append(['O1IDTYPE',       TradeContext.IDTYPE])         #证件类型
        TradeContext.tradeResponse.append(['O1IDCODE',       TradeContext.IDCODE])         #证件号码

        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '注销个人协议信息异常')



def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
