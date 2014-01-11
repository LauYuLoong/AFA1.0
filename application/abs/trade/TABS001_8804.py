# -*- coding: gbk -*-
################################################################################
#   批量业务系统：批量处理结果查询
#===============================================================================
#   交易文件:   Tabs001_8804.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  ghh
#   修改时间:   2012-09-20
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AbdtFunc
from types import *


#=====================查询==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********查询(8804)开始**********')

    try:
        sql = ""
        sql = "SELECT * FROM ABDT_BATCHINFO WHERE "
        sql = sql + "INDATE="    + "'" + TradeContext.indate  + "'" + " AND "      #申请日期
        sql = sql + "BATCHNO="   + "'" + TradeContext.batchno + "'"                #委托号




        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询批量信息表异常' )

        if ( len(records) == 0 ):
            return ExitSubTrade( '9000', '没有该委托号的批次信息' )

        #过滤None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.tradeResponse.append(['appno',           str(records[0][1])])         #业务编号
        TradeContext.tradeResponse.append(['busino',          str(records[0][2])])         #单位编号
        TradeContext.tradeResponse.append(['brno',            str(records[0][4])])         #网点号
        TradeContext.tradeResponse.append(['status',          str(records[0][19])])        #状态
        TradeContext.tradeResponse.append(['procmsg',         str(records[0][22])])        #错误描述



        #处理结果信息
        BatchResultMsg = str(records[0][22])

        AfaLoggerFunc.tradeInfo('**********查询(8804)结束**********')


        #返回
        TradeContext.tradeResponse.append(['errorCode', '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  BatchResultMsg])
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '查询,数据库异常' )


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        