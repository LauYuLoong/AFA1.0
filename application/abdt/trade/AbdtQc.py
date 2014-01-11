# -*- coding: gbk -*-
###############################################################################
# 文件名称：BatchDeamon.py
# 文件标识：
# 摘    要：批量处理守护进程
#
# 当前版本：1.0
# 作    者：XZH
# 完成日期：2006年9月8日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import time,AfaDBFunc,TradeContext,os,AfaUtilTools,AbdtManager,HostContext,HostComm
from types import *


#=========================判断数据文件是否存在==================================
def delDataFile(fname):
    if ( os.path.exists(fname) and os.path.isfile(fname) ):
        AbdtManager.WrtLog('删除文件:[' + fname + ']')
        cmdstr = "rm " + fname
        os.system(cmdstr)
        return 0
    else:
        return -1




#=========================获取偏移量计算日期====================================
def getTimeFromNow( offsetDays, format = "%Y%m%d" ):
    secs = time.time( ) + offsetDays * 3600 * 24
    return time.strftime( format, time.localtime( secs ) )
    
    
    
    
#=========================删除批量文件==========================================
def DelHostFile(curBatchNo, HostFileName, Flag):

    AbdtManager.WrtLog('删除主机文件:[' + HostFileName + ']')

    try:
        HostBatchNo  = curBatchNo[4:16]

        #通讯区打包
        HostContext.I1TRCD = '8819'                     #交易码
        HostContext.I1SBNO = TradeContext.BRNO          #交易机构号
        HostContext.I1USID = '999986'                   #交易柜员号
        HostContext.I1AUUS = ""                         #授权柜员
        HostContext.I1AUPS = ""                         #授权柜员密码
        HostContext.I1WSNO = ""                         #终端号
        HostContext.I1NBBH = TradeContext.APPNO         #代理业务标识
        HostContext.I1CLDT = TradeContext.BATCHDATE     #原批量日期
        HostContext.I1UNSQ = HostBatchNo                #原批量委托号
        HostContext.I1FILE = HostFileName               #删除文件名
        HostContext.I1OPFG = Flag                       #操作标志(0-查询 1-删除上传文件 2-删除下传文件)

        HostTradeCode = "8819".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8819.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AbdtManager.WrtLog('>>>处理结果=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return -1

        if ( HostContext.O1MGID == "AAAAAAA" ):
            AbdtManager.WrtLog('>>>处理结果=[' + HostContext.O1MGID + ']交易成功')

        else:
            AbdtManager.WrtLog('>>>处理结果=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)

        #删除批量表中的数据
        sql = ""
        sql = sql + "UPDATE ABDT_BATCHINFO SET STATUS='**' WHERE "
        sql = sql + "APPNO='"   + TradeContext.APPNO     + "'" + " AND "
        sql = sql + "BUSINO='"  + TradeContext.BUSINO    + "'" + " AND "
        sql = sql + "BATCHNO='" + TradeContext.BATCHNO   + "'"

        retcode = AfaDBFunc.UpdateSqlCmt( sql )
        if (retcode==None or retcode <= 0):
            return -1
        else:
            return 0

    except Exception, e:
        AbdtManager.WrtLog( str(e) )
        AbdtManager.WrtLog('删除主机文件异常')
        return -1


#历史批量数据文件清理
def ClearHisDataFile():

    #查询批量信息表
    try:
        sql = ""
        #88-已经处理完成 40-已经撤消批量
        sql = "SELECT BATCHNO,APPNO,BUSINO,INDATE,BATCHDATE,STATUS,BRNO FROM ABDT_BATCHINFO WHERE STATUS IN ('40','88') AND NOTE2<" + "'" + TradeContext.WorkDate  + "'"
        records = AfaDBFunc.SelectSql( sql )
        if ( len(records) == 0 ):
            AbdtManager.WrtLog('没有需要清理批量数据文件')
            return 0

        else:
            AbdtManager.WrtLog('总共有[' + str(len(records)) + ']条待清理记录')

    except Exception, e:
        AbdtManager.WrtLog(e)
        AbdtManager.WrtLog('清理批量数据文件异常')
        return -1

    i = 0
    while ( i  < len(records) ):
        TradeContext.BATCHNO   = str(records[i][0]).strip()         #委托号(批次号)
        TradeContext.APPNO     = str(records[i][1]).strip()         #业务编号
        TradeContext.BUSINO    = str(records[i][2]).strip()         #单位编号
        TradeContext.INDATE    = str(records[i][3]).strip()         #申请日期
        TradeContext.BATCHDATE = str(records[i][4]).strip()         #提交日期
        TradeContext.STATUS    = str(records[i][5]).strip()         #作业状态
        TradeContext.BRNO      = str(records[i][6]).strip()         #机构代码


        #进行文件清理工作(把相关文件移动备份目录中)
        AbdtManager.WrtLog('进行清理:['+TradeContext.BUSINO+']['+TradeContext.BATCHNO+']['+TradeContext.BATCHDATE+']')

        #清除in目录文件
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + '_' + TradeContext.INDATE
        delDataFile(dFileName)

        #清除host目录文件
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_1'
        delDataFile(dFileName)

        dFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_2'
        delDataFile(dFileName)

        dFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_3'
        delDataFile(dFileName)

        dFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_4'
        delDataFile(dFileName)

        #清除down目录文件
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.APPNO + TradeContext.BUSINO + '_' + TradeContext.INDATE + '.RET'
        delDataFile(dFileName)

        dFileName = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.APPNO + TradeContext.BUSINO + '_' + TradeContext.INDATE + '.RPT'
        delDataFile(dFileName)

        if ( TradeContext.STATUS == '88' ):
            #清理主机文件

            #上传
            upHFileName = 'A' + TradeContext.BATCHNO[8:16] + '1'
            DelHostFile(TradeContext.BATCHNO, upHFileName, '1')

            #下载
            dwHFileName = 'A' + TradeContext.BATCHNO[8:16] + '2'
            DelHostFile(TradeContext.BATCHNO, dwHFileName, '2')

        i=i+1

    return 0










###########################################主函数###########################################
if __name__=='__main__':

    AbdtManager.WrtLog('********************清理数据处理开始********************')

    #读取配置文件
    BatchConfig = AbdtManager.GetBatchConfig()


    #根据偏移量计算清除日期
    TradeContext.WorkDate = getTimeFromNow(long(TradeContext.BATCH_CLEARDAY))
    
    #获取当前日期
    TradeContext.CurDate  = AfaUtilTools.GetSysTime( )


    if ( TradeContext.WorkDate >= TradeContext.CurDate ):
        AbdtManager.WrtLog('>>>清除日期不能大于当前日期:[' + TradeContext.WorkDate + ']')

    else:
        AbdtManager.WrtLog('>>>清除:[失效日期 < '+ TradeContext.WorkDate + ']批量数据文件')

        ClearHisDataFile()

    AbdtManager.WrtLog('********************清理数据处理结束********************')

