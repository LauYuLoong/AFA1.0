# -*- coding: gbk -*-
################################################################################
#   批量业务系统：录入单位信息
#===============================================================================
#   交易文件:   T001000_8401.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AfaFunc
from types import *


#=====================录入单位信息==============================================
def TrxMain():

    AfaLoggerFunc.tradeInfo('**********录入单位信息(8401)开始**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间

    #begin 20100709 蔡永贵 由于非税业务中把单位编号作为唯一标识，为了保证非税业务中不同业务编号时不产生相同的单位编号，修改查询条件
    #判断单位信息是否存在
    #sqlStr = "SELECT BUSINAME FROM ABDT_UNITINFO WHERE "
    #sqlStr = sqlStr + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "        #业务编号
    #sqlStr = sqlStr + "BUSINO=" + "'" + TradeContext.I1BUSINO + "'" + " AND "        #单位编号
    #sqlStr = sqlStr + "STATUS=" + "'" + "1"                   + "'"                  #状态(0:注销,1:正常)
    
    sqlStr = "SELECT BUSINAME FROM ABDT_UNITINFO WHERE "
    if TradeContext.I1APPNO == 'AG2008' or TradeContext.I1APPNO == 'AG2012':
        sqlStr = sqlStr + "APPNO in ('AG2008','AG2012')" + " AND "                   #业务编号
    else:
        sqlStr = sqlStr + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "    #业务编号
    sqlStr = sqlStr + "BUSINO=" + "'" + TradeContext.I1BUSINO + "'" + " AND "        #单位编号
    sqlStr = sqlStr + "STATUS=" + "'" + "1"                   + "'"                  #状态(0:注销,1:正常)
    #end


    AfaLoggerFunc.tradeInfo( sqlStr )


    records = AfaDBFunc.SelectSql( sqlStr )
    if ( records == None ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '录入单位信息异常' )

    if ( len(records) > 0 ):
        return ExitSubTrade( '9000', '该单位信息已经被注册,不能再次进行注册')


    #如果该单位没有进行注册，则对该单位信息进行注册(新增)
    sql = "INSERT INTO ABDT_UNITINFO("
    sql = sql + "APPNO,"             #业务编号:AG + 顺序号(4)
    sql = sql + "BUSINO,"            #单位编号:机构代码(10) + 顺序号(4)
    sql = sql + "AGENTTYPE,"         #委托方式
    sql = sql + "AGENTMODE,"         #委托范围
    sql = sql + "VOUHTYPE,"          #凭证类型
    sql = sql + "VOUHNO,"            #凭证号码
    sql = sql + "ACCNO,"             #银行账户(对公账户)
    sql = sql + "SUBACCNO,"          #子账户代码
    sql = sql + "SIGNUPMODE,"        #签约方式(0-双方, 1-三方)
    sql = sql + "GETUSERNOMODE,"     #单位客户编号获取方式(0-本地, 1-企业)
    sql = sql + "PROTNO,"            #协议号
    sql = sql + "APPNAME,"           #业务名称
    sql = sql + "BUSINAME,"          #单位名称
    sql = sql + "ADDRESS,"           #联系地址
    sql = sql + "TEL,"               #联系电话
    sql = sql + "USERNAME,"          #联系人员
    sql = sql + "WORKDATE,"          #工作日期
    sql = sql + "BATCHNO,"           #批次号
    sql = sql + "STARTDATE,"         #生效日期
    sql = sql + "ENDDATE,"           #失效日期
    sql = sql + "STARTTIME,"         #服务开始时间
    sql = sql + "ENDTIME,"           #服务终止时间
    sql = sql + "ZONENO,"            #地区代码
    sql = sql + "BRNO,"              #机构代码
    sql = sql + "TELLERNO,"          #柜员代码
    sql = sql + "REGDATE,"           #注册日期
    sql = sql + "REGTIME,"           #注册时间
    sql = sql + "STATUS,"            #状态(0-未启用, 1-开启, 2-关闭, 3-停用)
    sql = sql + "CHKDATE,"           #对账日期
    sql = sql + "CHKTIME,"           #对账时间
    sql = sql + "CHKFLAG,"           #对帐标志(0-未对账, 1-已对账)
    sql = sql + "NOTE1,"             #备注1
    sql = sql + "NOTE2,"             #备注2
    sql = sql + "NOTE3,"             #备注3
    sql = sql + "NOTE4,"             #备注4
    sql = sql + "NOTE5) "            #备注5

    sql = sql + " VALUES ("

    sql = sql + "'" + TradeContext.I1APPNO          + "',"            #业务编号
    sql = sql + "'" + TradeContext.I1BUSINO         + "',"            #单位编号
    sql = sql + "'" + TradeContext.I1AGENTTYPE      + "',"            #委托方式
    sql = sql + "'" + TradeContext.I1AGENTMODE      + "',"            #代理范围
    sql = sql + "'" + TradeContext.I1VOUHTYPE       + "',"            #凭证类型
    sql = sql + "'" + TradeContext.I1VOUHNO         + "',"            #凭证号码
    sql = sql + "'" + TradeContext.I1ACCNO          + "',"            #银行账户(对公帐户)
    sql = sql + "'" + TradeContext.I1SUBACCNO       + "',"            #子帐户代码
    sql = sql + "'" + TradeContext.I1SIGNUPMODE     + "',"            #签约方式(0-双方, 1-三方)
    sql = sql + "'" + TradeContext.I1GETUSERNOMODE  + "',"            #单位客户编号获取方式(0-本地, 1-企业)
    sql = sql + "'" + TradeContext.I1PROTNO         + "',"            #协议号
    sql = sql + "'" + TradeContext.I1APPNAME        + "',"            #业务名称
    sql = sql + "'" + TradeContext.I1BUSINAME       + "',"            #单位名称
    sql = sql + "'" + TradeContext.I1ADDRESS        + "',"            #联系地址
    sql = sql + "'" + TradeContext.I1TEL            + "',"            #联系电话
    sql = sql + "'" + TradeContext.I1USERNAME       + "',"            #联系人员
    sql = sql + "'" + TradeContext.TranDate         + "',"            #工作日期
    sql = sql + "'" + "000"                         + "',"            #批次号
    sql = sql + "'" + TradeContext.I1STARTDATE      + "',"            #生效日期
    sql = sql + "'" + TradeContext.I1ENDDATE        + "',"            #失效日期
    sql = sql + "'" + TradeContext.I1STARTTIME      + "',"            #服务开始时间
    sql = sql + "'" + TradeContext.I1ENDTIME        + "',"            #服务终止时间
    sql = sql + "'" + TradeContext.I1ZONENO         + "',"            #地区代码
    sql = sql + "'" + TradeContext.I1SBNO           + "',"            #机构代码
    sql = sql + "'" + TradeContext.I1USID           + "',"            #柜员代码
    sql = sql + "'" + TradeContext.TranDate         + "',"            #注册日期
    sql = sql + "'" + TradeContext.TranTime         + "',"            #注册时间
    sql = sql + "'" + "1"                           + "',"            #状态((0-未启用, 1-开启, 2-关闭, 3-停用)
    sql = sql + "'" + ""                            + "',"            #对账日期
    sql = sql + "'" + ""                            + "',"            #对账时间
    sql = sql + "'" + "0"                           + "',"            #对帐标志(0-未对账, 1-已对账)
    sql = sql + "'" + TradeContext.I1NOTE1          + "',"            #备注1
    sql = sql + "'" + TradeContext.I1NOTE2          + "',"            #备注2
    sql = sql + "'" + TradeContext.I1NOTE3          + "',"            #备注3
    sql = sql + "'" + TradeContext.I1NOTE4          + "',"            #备注4
    sql = sql + "'" + TradeContext.I1NOTE5          + "')"            #备注5

    AfaLoggerFunc.tradeInfo( sql )

    result = AfaDBFunc.InsertSqlCmt( sql )
    if( result <= 0 ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '增加单位信息失败')

    AfaLoggerFunc.tradeInfo('**********录入单位信息(8401)结束**********')

    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True



def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False