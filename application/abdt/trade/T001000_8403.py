# -*- coding: gbk -*-
################################################################################
#   批量业务系统：维护单位信息
#===============================================================================
#   交易文件:   T001000_8403.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AfaFunc
from types import *


#=====================维护单位信息==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********维护单位信息(8403)开始**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间


    #判断单位是否发生业务
    sql = "SELECT BATCHNO FROM ABDT_BATCHINFO WHERE "
    sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO   + "'" + " AND "                   #业务编码
    sql = sql + "BUSINO=" + "'" + TradeContext.I1BUSINO  + "'" + " AND "                   #单位编码
    sql = sql + "ZONENO=" + "'" + TradeContext.I1ZONENO  + "'" + " AND "                   #地区代码
    sql = sql + "BRNO="   + "'" + TradeContext.I1SBNO    + "'" + " AND "                   #机构代码
    sql = sql + "STATUS NOT IN ('40','88','**')"                                           #状态(撤销)


    AfaLoggerFunc.tradeInfo( sql )


    records = AfaDBFunc.SelectSql( sql )
    if ( records==None ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '判断单位是否发生业务异常' )

    if ( len(records) > 0 ):
        return ExitSubTrade( '9000', '该单位已经发生业务,不能任何操作')


    #对单位信息进行维护操作
    if (TradeContext.I1PROCTYPE == '0'):
        #修改
        if ( TradeContext.I1OLDACCNO != TradeContext.I1ACCNO ):
            return ExitSubTrade( '9000', '新账号不能与原来账号相同')
                
        else:

            sql = "UPDATE ABDT_UNITINFO SET "
#           sql = sql + "APPNO='"         + TradeContext.I1APPNO         + "',"                    #业务编号
#           sql = sql + "BUSINO='"        + TradeContext.I1BUSINO        + "',"                    #单位编号
            sql = sql + "AGENTTYPE='"     + TradeContext.I1AGENTTYPE     + "',"                    #委托方式
            sql = sql + "AGENTMODE='"     + TradeContext.I1AGENTMODE     + "',"                    #代理范围
            sql = sql + "VOUHTYPE='"      + TradeContext.I1VOUHTYPE      + "',"                    #凭证类型
            sql = sql + "VOUHNO='"        + TradeContext.I1VOUHNO        + "',"                    #凭证号码
            sql = sql + "ACCNO='"         + TradeContext.I1ACCNO         + "',"                    #银行账户(对公帐户)
            sql = sql + "SUBACCNO='"      + TradeContext.I1SUBACCNO      + "',"                    #子帐户代码
            sql = sql + "SIGNUPMODE='"    + TradeContext.I1SIGNUPMODE    + "',"                    #签约方式
            sql = sql + "GETUSERNOMODE='" + TradeContext.I1GETUSERNOMODE + "',"                    #单位客户编号获取方式
            sql = sql + "PROTNO='"        + TradeContext.I1PROTNO        + "',"                    #协议号
#           sql = sql + "APPNAME='"       + TradeContext.I1APPNAME       + "',"                    #业务名称
            sql = sql + "BUSINAME='"      + TradeContext.I1BUSINAME      + "',"                    #单位名称
            sql = sql + "ADDRESS='"       + TradeContext.I1ADDRESS       + "',"                    #联系地址
            sql = sql + "TEL='"           + TradeContext.I1TEL           + "',"                    #联系电话
            sql = sql + "USERNAME='"      + TradeContext.I1USERNAME      + "',"                    #联系人员
#           sql = sql + "WORKDATE='"      + TradeContext.I1WORKDATE      + "',"                    #工作日期
#           sql = sql + "BATCHNO='"       + TradeContext.I1BATCHNO       + "',"                    #批次号
            sql = sql + "STARTDATE='"     + TradeContext.I1STARTDATE     + "',"                    #生效日期
            sql = sql + "ENDDATE='"       + TradeContext.I1ENDDATE       + "',"                    #失效日期
            sql = sql + "STARTTIME='"     + TradeContext.I1STARTTIME     + "',"                    #服务开始时间
            sql = sql + "ENDTIME='"       + TradeContext.I1ENDTIME       + "',"                    #服务终止时间
#           sql = sql + "ZONENO='"        + TradeContext.I1ZONENO        + "',"                    #地区代码
#           sql = sql + "BRNO='"          + TradeContext.I1BRNO          + "',"                    #机构代码
#           sql = sql + "TELLERNO='"      + TradeContext.I1TELLERNO      + "',"                    #柜员代码
#           sql = sql + "REGDATE='"       + TradeContext.I1REGDATE       + "',"                    #注册日期
#           sql = sql + "REGTIME='"       + TradeContext.I1REGTIME       + "',"                    #注册时间
#           sql = sql + "STATUS='"        + TradeContext.I1STATUS        + "',"                    #状态
#           sql = sql + "CHKDATE='"       + TradeContext.I1CHKDATE       + "',"                    #对账日期
#           sql = sql + "CHKTIME='"       + TradeContext.I1CHKTIME       + "',"                    #对账时间
#           sql = sql + "CHKFLAG='"       + TradeContext.I1CHKFLAG       + "',"                    #对账标志
            sql = sql + "NOTE1='"         + TradeContext.I1USID          + "',"                    #备注1(修改柜员号)
            sql = sql + "NOTE2='"         + TradeContext.TranDate+TradeContext.TranTime + "',"     #备注2(修改日期时间)
            sql = sql + "NOTE3='"         + TradeContext.I1NOTE3         + "',"                    #备注3
            sql = sql + "NOTE4='"         + TradeContext.I1NOTE4         + "',"                    #备注4
            sql = sql + "NOTE5='"         + TradeContext.I1NOTE5         + "'"                     #备注5

            sql = sql + " WHERE "

            sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO   + "'" + " AND "                   #业务编码
            sql = sql + "BUSINO=" + "'" + TradeContext.I1BUSINO  + "'" + " AND "                   #单位编码
            sql = sql + "ZONENO=" + "'" + TradeContext.I1ZONENO  + "'" + " AND "                   #地区代码
            sql = sql + "BRNO="   + "'" + TradeContext.I1SBNO    + "'"                             #机构代码
#           sql = sql + "STATUS='1'"                                                               #状态(0-注销 1-正常)

            AfaLoggerFunc.tradeInfo( sql )

            result = AfaDBFunc.UpdateSqlCmt( sql )
                
            if( result <= 0 ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return ExitSubTrade( '9000', '修改单位信息失败')
    else:
        #注销

        AfaLoggerFunc.tradeInfo(">>>把需要单位信息记录移到单位信息历史表中")

        sql = ""
        sql = "INSERT INTO ABDT_HIS_UNITINFO SELECT * FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO   + "'" + " AND "        #业务编码
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO  + "'" + " AND "        #单位编码
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO  + "'" + " AND "        #地区代码
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO    + "'"                  #机构代码
#       sql = sql + "STATUS='1'"                                                      #状态(0-注销 1-正常)

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.InsertSqlCmt( sql )
        if (result <= 0):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '注销单位信息失败')


        AfaLoggerFunc.tradeInfo(">>>删除在单位信息表中被注销单位信息记录")

        sql = ""
        sql = "DELETE FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO   + "'" + " AND "        #业务编码
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO  + "'" + " AND "        #单位编码
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO  + "'" + " AND "        #地区代码
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO    + "'"                  #机构代码
#       sql = sql + "STATUS='1'"                                                      #状态(0-注销 1-正常)

        AfaLoggerFunc.tradeInfo( sql )

        result = AfaDBFunc.DeleteSqlCmt( sql )
        if (result <= 0):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '注销客户信息失败')


        AfaLoggerFunc.tradeInfo(">>>总共注销[" + str(result) + "]条记录")


    AfaLoggerFunc.tradeInfo('**********维护单位信息(8403)结束**********')


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
