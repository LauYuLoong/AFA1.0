###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：余额信息查询
#
# 作    者：pgt
# 完成日期：2009年05月12日
#
###############################################################################
import TradeContext

TradeContext.sysType =  'cron'

import AfaUtilTools,AfaDBFunc,os,LoggerHandler,HostContext,HostComm,sys,datetime,UtilTools,AfaAdminFunc
from types import *

def SerachDB():
    #=====查询FS_BUSINOINFO表，得到账号等信息====
    tradeLogger.info("进入SearchDB,查询FS_BUSINOINFO表")
    sqlstr = "select BUSINO,ACCNO,TELLER,BANKNO from FS_BUSINOINFO"
    records = AfaDBFunc.SelectSql(sqlstr)
    if(records == None):
        tradeLogger.info( "查找数据库异常" )
        return False

    elif(len(records) == 0):
        tradeLogger.info( "查找数据库为空" )
        return False

    else:
        return records

def ZJJY(record):
    #=====调用主机8810交易====
    tradeLogger.info("调用主机8810交易")
    HostContext.I1TRCD = '8810'
    HostContext.I1ACNO = record[1]
    HostContext.I1SBNO = record[0][0:10]
    HostContext.I1USID = "999986"
    HostContext.I1WSNO = "10.12.5.187"
#    HostContext.I1CFFG = "1"
    HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8810.map', \
                            UtilTools.Rfill('8810',10,' ') ,'0002' )
    if HostContext.host_Error:
        tradeLogger.info( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )

        if HostContext.host_ErrorType != 5 :
            TradeContext.__status__='1'
            TradeContext.errorCode='A0101'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        else :
            TradeContext.__status__='2'
            TradeContext.errorCode='A0102'
            TradeContext.errorMsg=HostContext.host_ErrorMsg

        return False

    #=====分析主机返回文件====
    if (HostContext.host_Error == True):    #主机通讯错误
        tradeLogger.info("主机通讯错")
        return False

    if( HostContext.O1MGID != 'AAAAAAA' ): #失败
        tradeLogger.info('I1ACNO>>>>' + record[1])
        tradeLogger.info('I1SBNO>>>>' + record[0][0:10])
        tradeLogger.info(HostContext.O1MGID+"  "+HostContext.O1INFO)
        return False

    else:                                  #成功
        TradeContext.__status__='0'
        tradeLogger.info("主机成功")
        return True


def InsertDB(record):
    tradeLogger.info(HostContext.O1ACBL)
    #=====向8446表中插入数据====
    tradeLogger.info("进入InsertDB，向8446表中插入数据")
    #TradeContext.serDate  =   AfaAdminFunc.getTimeFromNow(int(-1))
    #TradeContext.serDate  ='20091231'
    insertsql = "insert into FS_8446_REMAIN(BUSINO,DATE,THIS,ACCNO,BANKNO) VALUES('"+ \
                 record[0] + "','" + TradeContext.serDate + "','" + str(float(HostContext.O1ACBL)) + "','" + record[1] + "','" + record[3] + "')"
    tradeLogger.info(insertsql)
    res = AfaDBFunc.InsertSql(insertsql)
    if(res < -1):
        AfaDBFunc.RollbackSql( )
        tradeLogger.info('BUSINO>>>'+record[0])
        tradeLogger.info("插入8446余额表失败")
        return False

    AfaDBFunc.CommitSql( )
    return True


if __name__ == "__main__":

    tradeLogger = LoggerHandler.getLogger( "cron" )
    tradeLogger.info("======开始执行AHFS_YECX，查询余额======")

    if ( len(sys.argv) != 2 ):
        TradeContext.serDate = AfaAdminFunc.getTimeFromNow(int(-1))
    else:
        sOffSet                =   sys.argv[1]
        TradeContext.serDate   = AfaAdminFunc.getTimeFromNow(int(sOffSet))

    records = SerachDB()
    if(records == False):
        sys.exit(1)
    for i in range(0,len(records)):
        res = ZJJY(records[i])
        if(res == False):
            continue

        InsertDB(records[i])

    tradeLogger.info("======结束执行AHFS_YECX，查询余额======")


