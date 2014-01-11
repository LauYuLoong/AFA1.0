# -*- coding: gbk -*-
################################################################################
#   批量业务系统：批量维护
#===============================================================================
#   交易文件:   T001000_8802.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os,AbdtManager
from types import *


#=====================批量信息维护==============================================
def TrxMain():
    
    AfaLoggerFunc.tradeInfo('**********批量信息维护(8802)_开始**********')


    if (TradeContext.PROCTYPE   == '00'):
        AfaLoggerFunc.tradeInfo('>>>查询')
        if not QueryBatchInfo():
            return False

    elif (TradeContext.PROCTYPE == '01'):
        AfaLoggerFunc.tradeInfo('>>>审批')
        
        if TradeContext.STATUS=='11':
            if not AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '20', '分行审批(管理员)-->待中心审批'):
                return False

        elif TradeContext.STATUS=='20':
            if not AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '21', '中心审批(管理员)-->待提交'):
                return False

        else:
            return ExitSubTrade( '9999', '批次状态非法' )


    elif (TradeContext.PROCTYPE == '02'):
        AfaLoggerFunc.tradeInfo('>>>撤销')

        if TradeContext.STATUS=='11':
            if not AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '40', '分行审批(管理员)-->手工撤消'):
                return False
                
        elif TradeContext.STATUS=='20':
            if not AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '40', '中心审批(管理员)-->手工撤消'):
                return False

        else:
            return ExitSubTrade( '9999', '批次状态非法' )
                
    AfaLoggerFunc.tradeInfo('**********批量信息维护(8802)_结束**********')

    #返回
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '交易成功'
    return True


#=====================查询批量信息==============================================
def QueryBatchInfo():

    sqlwhere = "WHERE BATCHNO > '" + TradeContext.batchNo + "'"

    if TradeContext.ZONENO == "0000":
        #总行
        if (len(TradeContext.brno)==6):
            #查询联社批次
            sqlwhere = sqlwhere + " AND SUBSTR(BRNO,1,6) = '" + TradeContext.brno + "'"

        elif (len(TradeContext.brno)==0):
            #查询全部批次
            pass

        else:
            #查询机构批次
            sqlwhere = sqlwhere + " AND BRNO = '" + TradeContext.brno + "'"

    else:
        #分行
        if(len(TradeContext.brno)==6):
            #查询联社批次
            sqlwhere = sqlwhere + " AND SUBSTR(BRNO,1,6) = '" + TradeContext.brno + "'"
        else:
            #查询机构批次
            sqlwhere = sqlwhere + " AND BRNO = '" + TradeContext.brno     + "'"


    if(len(TradeContext.trxDate)!=0):
        sqlwhere = sqlwhere + " AND INDATE = '" + TradeContext.trxDate + "'"

    if(len(TradeContext.trxState)==0 or TradeContext.trxState=='00' ):
        sqlwhere = sqlwhere + " AND STATUS IN ('10','11','20','21','22','30','31','32','40','88')"

    else:
        sqlwhere = sqlwhere + " AND STATUS = '" + TradeContext.trxState + "'"

    sqlwhere = sqlwhere + " ORDER BY BATCHNO"

    sql = "SELECT BATCHNO,APPNO,BUSINO,BRNO,USERNO,TERMTYPE,FILENAME,INDATE,INTIME,BATCHDATE,BATCHTIME,TOTALNUM"
    sql = sql + ",TOTALAMT,SUCCNUM,SUCCAMT,FAILNUM,FAILAMT,STATUS,BEGINDATE,ENDDATE,PROCMSG FROM ABDT_BATCHINFO " + sqlwhere

    AfaLoggerFunc.tradeInfo(sql)

    records =  AfaDBFunc.SelectSql( sql )
    if (records == None):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return ExitSubTrade( '9999', '查询批次信息异常' )

    if (len(records)==0) :
        return ExitSubTrade( '9000', '没有任何批次信息' )


    #############################################################################################################
    TradeContext.retData = ""

    TradeContext.retTotalNum = len(records)

    if(len(records)>3):
        TradeContext.retQueryNum = 3

    else:
        TradeContext.retQueryNum = len(records)

    for i in range(0,TradeContext.retQueryNum):
        TradeContext.retData = TradeContext.retData + records[i][0]                                      #批次号
        TradeContext.retData = TradeContext.retData +"|"

        sql = "SELECT APPNAME,BUSINAME FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + records[i][1]  + "'" + " AND "         #业务编号
        sql = sql + "BUSINO=" + "'" + records[i][2]  + "'" + " AND "         #单位编号
        sql = sql + "STATUS=" + "'" + "1"                   + "'"            #状态(0:注销,1:正常)

        name_records = AfaDBFunc.SelectSql( sql )
        if ( len(name_records) != 0 ):
            TradeContext.retData = TradeContext.retData + records[i][1] + ' - ' + name_records[0][0]     #业务编号
            TradeContext.retData = TradeContext.retData +"|"

            TradeContext.retData = TradeContext.retData + records[i][2] + ' - ' + name_records[0][1]     #单位编号
            TradeContext.retData = TradeContext.retData +"|"
        else:
            TradeContext.retData = TradeContext.retData + records[i][1]                                  #业务编号
            TradeContext.retData = TradeContext.retData +"|"

            TradeContext.retData = TradeContext.retData + records[i][2]                                  #单位编号
            TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][3]    #机构号
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][4]    #操作员
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][5]    #上传方式
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][6]    #上传文件名
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][7]    #委托日期
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][8]    #委托时间
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][9]    #提交日期
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][10]   #提交时间
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][11]   #总笔数
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][12]   #总金额
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][13]   #成功笔数
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][14]   #成功金额
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][15]   #失败笔数
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][16]   #失败金额
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][17]   #状态
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][18]   #生效日期
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][19]   #失效日期
        TradeContext.retData = TradeContext.retData +"|"

        TradeContext.retData = TradeContext.retData + records[i][20]   #处理信息
        TradeContext.retData = TradeContext.retData +"|"

        AfaLoggerFunc.tradeInfo(records[i][0] + '|' + records[i][1] + "|" + records[i][2] + "|" + records[i][3] + "|")

    TradeContext.RETDATA      = TradeContext.retData
    
    TradeContext.RETTOTALNUM  = str(TradeContext.retTotalNum)

    TradeContext.RETQUERYNUM  = str(TradeContext.retQueryNum)
    
    return True




def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
