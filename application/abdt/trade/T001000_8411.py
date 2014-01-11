# -*- coding: gbk -*-
################################################################################
#   批量业务系统：批量处理结果查询
#===============================================================================
#   交易文件:   T001000_8410.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AbdtFunc
from types import *


#=====================批量处理结果查询==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********批量处理结果查询(8411)开始**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间


    #判断单位协议是否有效
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    try:
        sql = ""
        sql = "SELECT * FROM ABDT_BATCHINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO  + "'" + " AND "      #业务编号
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO + "'" + " AND "      #单位编号
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO + "'" + " AND "      #地区代码
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO   + "'" + " AND "      #机构代码

        if ( len(TradeContext.I1BATCHNO) == 0 ):
            sql = sql + "INDATE="  + "'" + TradeContext.I1WORKDATE    + "'" + " AND "     #委托日期
            sql = sql + "STATUS<>" + "'" + '40'  + "'"                                    #状态
        else:
            sql = sql + "INDATE="  + "'" + TradeContext.I1WORKDATE    + "'" + " AND "     #委托日期
            sql = sql + "BATCHNO=" + "'" + TradeContext.I1BATCHNO  + "'"                  #委托号

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询批量信息表异常' )

        if ( len(records) == 0 ):
            return ExitSubTrade( '9000', '没有该委托号的批次信息' )

        #过滤None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.tradeResponse.append(['O1BATCHNO',         str(records[0][0])])         #委托号(批次号)
        TradeContext.tradeResponse.append(['O1APPNO',           str(records[0][1])])         #业务编号
        TradeContext.tradeResponse.append(['O1BUSINO',          str(records[0][2])])         #单位编号
        TradeContext.tradeResponse.append(['O1ZONENO',          str(records[0][3])])         #地区号
        TradeContext.tradeResponse.append(['O1BRNO',            str(records[0][4])])         #网点号
        TradeContext.tradeResponse.append(['O1USERNO',          str(records[0][5])])         #操作员
        TradeContext.tradeResponse.append(['O1ADMINNO',         str(records[0][6])])         #管理员
        TradeContext.tradeResponse.append(['O1TERMTYPE',        str(records[0][7])])         #终端类型
        TradeContext.tradeResponse.append(['O1FILENAME',        str(records[0][8])])         #上传文件名
        TradeContext.tradeResponse.append(['O1INDATE',          str(records[0][9])])         #委托日期
        TradeContext.tradeResponse.append(['O1INTIME',          str(records[0][10])])        #委托时间
        TradeContext.tradeResponse.append(['O1BATCHDATE',       str(records[0][11])])        #提交日期
        TradeContext.tradeResponse.append(['O1BATCHTIME',       str(records[0][12])])        #提交时间
        TradeContext.tradeResponse.append(['O1TOTALNUM',        str(records[0][13])])        #总笔数
        TradeContext.tradeResponse.append(['O1TOTALAMT',        str(records[0][14])])        #总金额
        TradeContext.tradeResponse.append(['O1SUCCNUM',         str(records[0][15])])        #成功笔数
        TradeContext.tradeResponse.append(['O1SUCCAMT',         str(records[0][16])])        #成功金额
        TradeContext.tradeResponse.append(['O1FAILNUM',         str(records[0][17])])        #失败笔数
        TradeContext.tradeResponse.append(['O1FAILAMT',         str(records[0][18])])        #失败金额
        TradeContext.tradeResponse.append(['O1UNSETNUM',        '0'])                        #未处理笔数
        TradeContext.tradeResponse.append(['O1UNSETAMT',        '0.00'])                     #未处理金额
        TradeContext.tradeResponse.append(['O1STATUS',          str(records[0][19])])        #状态
        TradeContext.tradeResponse.append(['O1BEGINDATE',       str(records[0][20])])        #生效日期
        TradeContext.tradeResponse.append(['O1ENDDATE',         str(records[0][21])])        #失效日期
        TradeContext.tradeResponse.append(['O1PROCMSG',         str(records[0][22])])        #处理信息
        TradeContext.tradeResponse.append(['O1NOTE1',           str(records[0][23])])        #备注1
        TradeContext.tradeResponse.append(['O1NOTE2',           str(records[0][24])])        #备注2
        TradeContext.tradeResponse.append(['O1NOTE3',           str(records[0][25])])        #备注3
        TradeContext.tradeResponse.append(['O1NOTE4',           str(records[0][26])])        #备注4
        TradeContext.tradeResponse.append(['O1NOTE5',           str(records[0][27])])        #备注5


        #处理结果信息
        BatchResultMsg = str(records[0][22])

        AfaLoggerFunc.tradeInfo('**********批量处理结果查询(8411)结束**********')


        #返回
        TradeContext.tradeResponse.append(['errorCode', '0000'])
        TradeContext.tradeResponse.append(['errorMsg',  BatchResultMsg])
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '批量处理结果查询,数据库异常' )


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        