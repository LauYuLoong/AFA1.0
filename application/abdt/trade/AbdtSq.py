# -*- coding: gbk -*-
###############################################################################
# 文件名称：AbdtSq.py
# 文件标识：
# 摘    要：批量文件申请
#
# 当前版本：2.0
# 作    者：XZH
# 完成日期：2008年06月10日
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import time,AfaDBFunc,TradeContext,os,AfaUtilTools,AbdtManager
from types import *



#=========================处理函数==============================================
def MainSQ_Proc( ):
    
    #获取当前系统时间
    TradeContext.WorkDate=AfaUtilTools.GetSysDate( )
    TradeContext.WorkTime=AfaUtilTools.GetSysTime( )

    AbdtManager.WrtLog('>>>日期=' + TradeContext.WorkDate + ' 时间=' + TradeContext.WorkTime)

    #查询批量待处理信息
    try:
        sql = ""

        #10-申请 11-待分行审批 20-待中心审批 21-待提交 22-已提交 30-待提回 31-正在提回 32-已提回 40-撤销 88-处理完毕
        sql = "SELECT * FROM ABDT_BATCHINFO WHERE STATUS IN ('10')"
        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AbdtManager.WrtLog( AfaDBFunc.sqlErrMsg )
            return AbdtManager.ExitThisFlow( '9000', '查询需要处理的批次信息异常')


        if ( len(records) == 0 ):
            return AbdtManager.ExitThisFlow( '9000', '没有需要处理的批次信息')


        AbdtManager.WrtLog('>>>总共有[' + str(len(records)) + ']条待处理批次记录')

        i = 0
        while ( i  < len(records) ):
            TradeContext.BATCHNO     = str(records[i][0]).strip()          #委托号(批次号)
            TradeContext.APPNO       = str(records[i][1]).strip()          #业务编号
            TradeContext.BUSINO      = str(records[i][2]).strip()          #单位编号
            TradeContext.ZONENO      = str(records[i][3]).strip()          #地区号
            TradeContext.BRNO        = str(records[i][4]).strip()          #网点号
            TradeContext.USERNO      = str(records[i][5]).strip()          #操作员
            TradeContext.ADMINNO     = str(records[i][6]).strip()          #管理员
            TradeContext.TERMTYPE    = str(records[i][7]).strip()          #终端类型
            TradeContext.FILENAME    = str(records[i][8]).strip()          #上传文件名
            TradeContext.INDATE      = str(records[i][9]).strip()          #申请日期
            TradeContext.INTIME      = str(records[i][10]).strip()         #申请时间
            TradeContext.BATCHDATE   = str(records[i][11]).strip()         #提交日期
            TradeContext.BATCHTIME   = str(records[i][12]).strip()         #提交时间
            TradeContext.TOTALNUM    = str(records[i][13]).strip()         #总笔数
            TradeContext.TOTALAMT    = str(records[i][14]).strip()         #总金额
            TradeContext.SUCCNUM     = str(records[i][15]).strip()         #成功笔数
            TradeContext.SUCCAMT     = str(records[i][16]).strip()         #成功金额
            TradeContext.FAILNUM     = str(records[i][17]).strip()         #失败笔数
            TradeContext.FAILAMT     = str(records[i][18]).strip()         #失败金额
            TradeContext.STATUS      = str(records[i][19]).strip()         #状态
            TradeContext.STARTDATE   = str(records[i][20]).strip()         #生效日期
            TradeContext.ENDDATE     = str(records[i][21]).strip()         #失效日期
            TradeContext.PROCMSG     = str(records[i][22]).strip()         #处理信息
            TradeContext.NOTE1       = str(records[i][23]).strip()         #备注1
            TradeContext.NOTE2       = str(records[i][24]).strip()         #备注3
            TradeContext.NOTE3       = str(records[i][25]).strip()         #备注3
            TradeContext.NOTE4       = str(records[i][26]).strip()         #备注4
            TradeContext.NOTE5       = str(records[i][27]).strip()         #备注5
            i=i+1


            AbdtManager.WrtLog('#################################')


            AbdtManager.WrtLog('申请:APPNO=[' + TradeContext.APPNO + '],BATCHNO=[' + TradeContext.BATCHNO + ']')


            #查询单位信息
            if not AbdtManager.QueryBusiInfo() :
                AbdtManager.WrtLog( '自动撤消,没有发现单位信息' )
                AbdtManager.UpdateBatchInfo(TradeContext.BATCHNO, '40', '自动撤消,没有发现单位信息')
                continue

    
            if ( TradeContext.TERMTYPE == '0' ):
                #(柜面上传文件)
                AbdtManager.SQ_VMENU_Proc(TradeContext.BATCHNO)

            else:
                #转换(外围上传文件)
                AbdtManager.SQ_OTHER_Proc(TradeContext.BATCHNO)

            AbdtManager.WrtLog('#################################')


    except Exception, e:
        AbdtManager.WrtLog( str(e) )
        return AbdtManager.ExitThisFlow( '9000', '查询批量信息(申请)异常')


###########################################主函数###########################################
if __name__=='__main__':

    AbdtManager.WrtLog('********************批量申请处理开始********************')

    #读取配置文件
    BatchConfig = AbdtManager.GetBatchConfig()

    #申请处理
    MainSQ_Proc( )
        

    AbdtManager.WrtLog('********************批量申请处理结束********************')
