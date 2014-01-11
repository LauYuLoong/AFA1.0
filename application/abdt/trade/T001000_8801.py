# -*- coding: gbk -*-
################################################################################
#   批量业务系统：用户维护
#===============================================================================
#   交易文件:   T001000_8801.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os
from types import *


#=====================用户登陆==================================================
def TrxMain():
    

    AfaLoggerFunc.tradeInfo('**********用户维护(8801)开始**********')

    if (TradeContext.PROCTYPE   == '00'):
        AfaLoggerFunc.tradeInfo('>>>查询')
        if not QueryUserInfo():
            return False

    elif (TradeContext.PROCTYPE == '01'):
        AfaLoggerFunc.tradeInfo('>>>新增')
        if not AddUserInfo():
            return False

    elif (TradeContext.PROCTYPE == '02'):
        AfaLoggerFunc.tradeInfo('>>>修改')
        if not UpdateUserInfo():
            return False

    elif (TradeContext.PROCTYPE == '03'):
        AfaLoggerFunc.tradeInfo('>>>删除')
        if not DeleteUserInfo():
            return False

    elif (TradeContext.PROCTYPE == '04'):
        AfaLoggerFunc.tradeInfo('>>>修改密码')
        if not UpdateUserPass():
            return False

    AfaLoggerFunc.tradeInfo('**********用户维护(8801)结束**********')

    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True


#=====================查询用户信息==============================================
def QueryUserInfo():

    sql = "SELECT ZONENO,BRNO,USERNO,USERNAME,DUTYNO,TEL,ADDRESS FROM ABDT_USERINFO WHERE STATUS='1'"

    if( TradeContext.existVariable( "USERNO" ) and len(TradeContext.USERNO)>0 ):
        sql = sql + " AND USERNO = '" + TradeContext.USERNO + "' ORDER BY USERNO"

    AfaLoggerFunc.tradeInfo(sql)

    records =  AfaDBFunc.SelectSql( sql )
    if (records == None):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9999', '查询用户信息异常' )

    if (len(records)==0) :
        return ExitSubTrade( '9000', '不存在用户信息' )

    else:
        TradeContext.RETDATA = ""

        if(len(records)>5):
            TradeContext.RETFINDNUM = 5

        else:
            TradeContext.RETFINDNUM = len(records)

        for i in range(0,TradeContext.RETFINDNUM):

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][0]    #ZONENO
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][1]    #BRNO
            TradeContext.RETDATA = TradeContext.RETDATA +"|"
            
            TradeContext.RETDATA = TradeContext.RETDATA + records[i][2]    #USERNO
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][3]    #USERNAME
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][4]    #DUTYNO
            TradeContext.RETDATA = TradeContext.RETDATA +"|"
            
            TradeContext.RETDATA = TradeContext.RETDATA + records[i][5]    #TEL
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            TradeContext.RETDATA = TradeContext.RETDATA + records[i][6]    #ADDRESS
            TradeContext.RETDATA = TradeContext.RETDATA +"|"

            AfaLoggerFunc.tradeInfo( records[i][0] + '|' + records[i][1] + "|" + records[i][2] + "|" + records[i][3] + "|")

        TradeContext.tradeResponse.append(['RETDATA',TradeContext.RETDATA])

        TradeContext.tradeResponse.append(['RETFINDNUM',str(TradeContext.RETFINDNUM)])

        return True



#=====================新增用户信息==============================================
def AddUserInfo():
    
    sql = "SELECT * FROM ABDT_USERINFO WHERE STATUS='1'"
    sql = sql + " AND ZONENO = '" + TradeContext.ZONENO + "'"
    sql = sql + " AND BRNO = '"   + TradeContext.BRNO   + "'"
    sql = sql + " AND USERNO = '" + TradeContext.USERNO + "'"
    
    records =  AfaDBFunc.SelectSql( sql )
        
    if( records == None ) :
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9999', '查询用户信息异常' )

    if( len(records) > 0 ) :
        return ExitSubTrade( '9000', '该用户已经被注册,不能再次注册' )

    sql = "INSERT INTO ABDT_USERINFO("
    sql = sql + "ZONENO,"
    sql = sql + "BRNO,"
    sql = sql + "USERNO,"
    sql = sql + "USERNAME,"
    sql = sql + "ADDRESS,"
    sql = sql + "TEL,"
    sql = sql + "REGDATE,"
    sql = sql + "REGTIME,"
    sql = sql + "PASSWORD,"
    sql = sql + "DUTYNO,"
    sql = sql + "STATUS,"
    sql = sql + "NOTE1,"
    sql = sql + "NOTE2,"
    sql = sql + "NOTE3,"
    sql = sql + "NOTE4,"
    sql = sql + "NOTE5)"

    sql = sql + " VALUES ("

    sql = sql + "'" + TradeContext.ZONENO   + "',"            #地区代码
    sql = sql + "'" + TradeContext.BRNO     + "',"            #机构代码
    sql = sql + "'" + TradeContext.USERNO   + "',"            #用户号
    sql = sql + "'" + TradeContext.USERNAME + "',"            #用户名
    sql = sql + "'" + TradeContext.ADDRESS  + "',"            #地址
    sql = sql + "'" + TradeContext.TEL      + "',"            #电话
    sql = sql + "'" + TradeContext.TranDate + "',"            #日期
    sql = sql + "'" + TradeContext.TranTime + "',"            #时间
    sql = sql + "'" + TradeContext.PASSWD   + "',"            #密码
    sql = sql + "'" + TradeContext.DUTYNO   + "',"            #岗位编码
    sql = sql + "'" + '1'                   + "',"            #状态
    sql = sql + "'" + ''                    + "',"            #备用
    sql = sql + "'" + ''                    + "',"            #备用
    sql = sql + "'" + ''                    + "',"            #备用
    sql = sql + "'" + ''                    + "',"            #备用
    sql = sql + "'" + ''                    + "')"            #备用

    AfaLoggerFunc.tradeInfo(sql)

    ret = AfaDBFunc.InsertSqlCmt( sql )
    if (ret <= 0):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '用户注册失败' )

    return True



#=====================修改用户信息==============================================
def UpdateUserInfo():

    sql = "UPDATE ABDT_USERINFO SET "
    sql = sql + "ZONENO='"   + TradeContext.ZONENO      + "',"                    #地区号
    sql = sql + "BRNO='"     + TradeContext.BRNO        + "',"                    #网点
    sql = sql + "USERNAME='" + TradeContext.USERNAME    + "',"                    #用户名
    sql = sql + "DUTYNO='"   + TradeContext.DUTYNO      + "',"                    #岗位编码
    sql = sql + "ADDRESS='"  + TradeContext.ADDRESS     + "',"                    #地址
    sql = sql + "TEL='"      + TradeContext.TEL         + "'"                     #电话
    sql = sql + " WHERE "

    sql = sql + "USERNO="  + "'" + TradeContext.USERNO  + "'"                     #用户号

    AfaLoggerFunc.tradeInfo(sql)

    ret = AfaDBFunc.UpdateSqlCmt( sql )
    if (ret <= 0):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9000', '修改用户信息失败' )

    return True


#=====================删除用户信息==============================================
def DeleteUserInfo():
    
    sql = "DELETE FROM ABDT_USERINFO WHERE USERNO=" + "'" + TradeContext.USERNO + "'"

    AfaLoggerFunc.tradeInfo(sql)

    ret = AfaDBFunc.UpdateSqlCmt( sql )
    if (ret <= 0):
        return ExitSubTrade( '9000', '删除用户信息失败' )
        
    return True


#=====================修改用户密码==============================================
def UpdateUserPass():

    sql = "SELECT PASSWORD FROM ABDT_USERINFO WHERE STATUS='1' AND USERNO = '" + TradeContext.USERNO + "'"

    AfaLoggerFunc.tradeInfo(sql)
        
    records =  AfaDBFunc.SelectSql( sql )

    if (records == None or len(records)==0) :
        return ExitSubTrade( '9000', '不存在用户信息' )

    if (records[0][0] != TradeContext.OLDPASSWD):
        return ExitSubTrade( '9000', '旧密码不符' )

    sql = "UPDATE ABDT_USERINFO SET PASSWORD='" + TradeContext.NEWPASSWD + "'"

    sql = sql + " WHERE "

    sql = sql + "USERNO="  + "'" + TradeContext.USERNO  + "'"              #用户号

    AfaLoggerFunc.tradeInfo(sql)

    ret = AfaDBFunc.UpdateSqlCmt( sql )
    if (ret < 0):
        return ExitSubTrade('9000', '修改用户密码失败')

    return True



def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False