# -*- coding: gbk -*-
################################################################################
#   批量业务系统：用户登陆
#===============================================================================
#   交易文件:   T001000_8800.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os
from types import *


#=====================用户登陆==================================================
def TrxMain():
    

    AfaLoggerFunc.tradeInfo('**********用户登陆(8800)开始**********')


    sqlStr = "SELECT ZONENO,BRNO,USERNAME,TEL,ADDRESS,PASSWORD FROM ABDT_USERINFO WHERE STATUS='1'"
    sqlStr = sqlStr + " AND USERNO = '" + TradeContext.USERNO + "'"

    AfaLoggerFunc.tradeInfo(sqlStr)

    records =  AfaDBFunc.SelectSql( sqlStr )
        
    if (records == None):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9999', '查询用户信息异常' )

    if (len(records)==0) :
        return ExitSubTrade( '9000', '该用户号不存在' )

    else:
        if ( records[0][5] == TradeContext.PASSWD ):
            TradeContext.tradeResponse.append(['ZONENO',    records[0][0]])
            TradeContext.tradeResponse.append(['BRNO',      records[0][1]])
            TradeContext.tradeResponse.append(['USERNAME',  records[0][2]])
        else:
            return ExitSubTrade( '9999', '密码错误,请重试!')

    AfaLoggerFunc.tradeInfo('**********用户登陆(8800)结束**********')

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