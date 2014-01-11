# -*- coding: gbk -*-
################################################################################
#   批量业务系统：批量作业清单打印
#===============================================================================
#   交易文件:   T001000_8412.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AbdtFunc
from types import *


#=====================批量作业清单打印==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********批量作业清单打印(8412)开始**********')


    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间


    #判断单位协议是否有效
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    #查询批量作业报表信息
    if ( not QueryBatchInfo( ) ):
        return False
        
    AfaLoggerFunc.tradeInfo('**********批量作业清单打印(8412)结束**********')


    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True



#查询批量作业报表信息
def QueryBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>查询批量作业报表信息')

    try:
        sql = "SELECT * FROM ABDT_BATCHINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO   + "'" + " AND "        #业务编号
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO  + "'" + " AND "        #单位编号
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO  + "'" + " AND "        #地区代码
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO    + "'" + " AND "        #机构代码
        sql = sql + "INDATE="   + "'" + TradeContext.I1INDATE  + "'" + " AND "        #委托日期
        sql = sql + "BATCHNO="  + "'" + TradeContext.I1BATCHNO + "'" + " AND "         #委托号
        
        #begin  20091102  蔡永贵  增加查询条件批次号
        sql = sql + "NOTE2="    + "'" + TradeContext.I1BTHNO   + "'"                  #批次号
        #end

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询批量信息表异常' )

        if ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( "没有该委托号的批次信息，不能打印清单" )
            return ExitSubTrade( '9000', '没有该委托号的批次信息,不能打印清单' )

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
        TradeContext.tradeResponse.append(['O1PFILENAME',       str(records[0][8])])         #上传文件名
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
        TradeContext.tradeResponse.append(['O1STATUS',          str(records[0][19])])        #状态
        TradeContext.tradeResponse.append(['O1BEGINDATE',       str(records[0][20])])        #生效日期
        TradeContext.tradeResponse.append(['O1ENDDATE',         str(records[0][21])])        #失效日期
        TradeContext.tradeResponse.append(['O1PROCMSG',         str(records[0][22])])        #处理信息
        TradeContext.tradeResponse.append(['O1NOTE1',           str(records[0][23])])        #备注1
        TradeContext.tradeResponse.append(['O1NOTE2',           str(records[0][24])])        #备注2
        TradeContext.tradeResponse.append(['O1NOTE3',           str(records[0][25])])        #备注3
        TradeContext.tradeResponse.append(['O1NOTE4',           str(records[0][26])])        #备注4
        TradeContext.tradeResponse.append(['O1NOTE5',           str(records[0][27])])        #备注5
        
        #begin  20091102  蔡永贵  增加回盘文件名
        retFileName = TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO + "_" + TradeContext.I1INDATE + ".RET"
        TradeContext.tradeResponse.append(['O1FILENAME',        retFileName])                #回盘文件名
        #end

        #判断状态
        if ( str(records[0][19]) == "00" ):
            AfaLoggerFunc.tradeInfo('>>>上传')
            return ExitSubTrade( '9000', '该批次还没有提交,不能打印清单' )


        elif ( str(records[0][19]) == "10" ):
            AfaLoggerFunc.tradeInfo('>>>申请')
            return ExitSubTrade( '9000', '该批次还没有处理,不能打印清单' )


        elif ( str(records[0][19]) == "11" ):
            AfaLoggerFunc.tradeInfo('>>>待联社审批')
            return ExitSubTrade( '9000', '该批次还没有处理完毕(待联社审批),不能打印清单' )


        elif ( str(records[0][19]) == "20" ):
            AfaLoggerFunc.tradeInfo('>>>待中心审批')
            return ExitSubTrade( '9000', '该批次还没有处理完毕(待中心审批),不能打印清单' )


        elif ( str(records[0][19]) == "21" ):
            AfaLoggerFunc.tradeInfo('>>>正在提交')
            return ExitSubTrade( '9000', '该批次还没有处理完毕(正在提交),不能打印清单' )


        elif ( str(records[0][19]) == "22" ):
            AfaLoggerFunc.tradeInfo('>>>已提交(正在处理...)')
            return ExitSubTrade( '9000', '该批次还没有处理完毕(主机正在处理),不能打印清单' )


        elif ( str(records[0][19]) == "30" ):
            AfaLoggerFunc.tradeInfo('>>>待提回')
            return ExitSubTrade( '9000', '该批次还没有处理完毕(待提回),不能打印清单' )


        elif ( str(records[0][19]) == "31" ):
            AfaLoggerFunc.tradeInfo('>>>正在提回')
            return ExitSubTrade( '9000', '该批次还没有处理完毕(正在提回),不能打印清单' )


        elif ( str(records[0][19]) == "32" ):
            AfaLoggerFunc.tradeInfo('>>>已提回')
            return ExitSubTrade( '9000', '该批次还没有处理完毕(已提回),不能打印清单' )


        elif ( str(records[0][19]) == "88" ):
            AfaLoggerFunc.tradeInfo('>>>处理完成(回盘文件、业务报表), VMENU应该调用FTP功能下载报表文件')
            return True

        elif ( str(records[0][19]) == "40" ):
            AfaLoggerFunc.tradeInfo('>>>撤销')
            return ExitSubTrade( '9000', '该单位该批次数据已被撤消[' + str(records[0][24]) + ']')

        else:
            return ExitSubTrade( '9000', '该批次数据的状态异常,请联系科技人员')

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '打印批量作业清单,数据库异常' )



def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
