# -*- coding: gbk -*-
################################################################################
#   批量业务系统：撤销批量作业
#===============================================================================
#   交易文件:   T001000_8410.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AbdtFunc
from types import *


#=====================撤销批量作业==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********撤销批量作业(8410)开始**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间



    #判断单位协议是否有效
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    #判断批量申请是否已存在
    if (  not ChkBatchInfo( ) ):
        return False


    #修改批次记录为撤销状态
    if ( UpdateBatchInfo() < 0 ):
        return False


    #移动数据文件到撤消目录中
    try:
    
        #begin 20100105 蔡永贵 修改 文件名后加上批次序号（TradeContext.NOTE2）
        sFileName = os.environ['AFAP_HOME'] + '/data/batch/in/'   + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.NOTE2 + "_" + TradeContext.TranDate
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/dust/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.NOTE2 + "_" + TradeContext.TranDate + TradeContext.TranTime
        #end
        
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            AfaLoggerFunc.tradeInfo('>>>批量处理数据文件存在')

            cp_cmd_str="mv " + sFileName + " " + dFileName
            os.system(cp_cmd_str)

        else:
            AfaLoggerFunc.tradeInfo('>>>批量处理数据文件不存在,请查询原因')
            return ExitSubTrade( '9999', '批量处理数据文件不存在(转移),请查询原因' )


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '批量处理数据文件操作异常(转移)' )


    AfaLoggerFunc.tradeInfo('**********撤销批量作业(8410)结束**********')

    
    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True



#判断批量申请是否已存在
def ChkBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>判断批量申请是否已存在')

    try:
    
        #begin 20100105 蔡永贵  修改   查询的时候把NOTE2也查出来
        #sql = "SELECT BATCHNO,STATUS,NOTE5,USERNO FROM ABDT_BATCHINFO WHERE "
        sql = "SELECT BATCHNO,STATUS,NOTE5,USERNO,NOTE2 FROM ABDT_BATCHINFO WHERE "
        #end
        
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO    + "'" + " AND "        #业务编号
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO   + "'" + " AND "        #单位编号
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO   + "'" + " AND "        #地区代码
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO     + "'" + " AND "        #机构代码
        sql = sql + "INDATE="   + "'" + TradeContext.I1WORKDATE + "'" + " AND "        #委托日期
        sql = sql + "BATCHNO="  + "'" + TradeContext.I1BATCHNO  + "'"                  #委托号

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询批量信息表异常' )

        if ( len(records) == 0 ):
                return ExitSubTrade( '9000', '没有该单位批量申请信息,不能撤销' )
                
        #begin 蔡永贵 增加
        TradeContext.NOTE2 = records[0][4]                #NOTE2(批次序号)
        #end

        if ( str(records[0][1]) == "40" ):
            return ExitSubTrade('9000', '该单位的批量数据已经被撤消:['+ str(records[0][2]) +']')

        elif ( str(records[0][1]) == "88" ):
            return ExitSubTrade('9000', '该单位的批量数据文件已经处理完成,不能撤销')

        elif ( str(records[0][1]) == "10" ):
            if ( str(records[0][3]) != TradeContext.I1USID ):
                return ExitSubTrade('9000', '只有申请柜员才能撤消')

            AfaLoggerFunc.tradeInfo('>>>该单位的批量数据文件为申请状态,可以撤销')
            return True

        else:
            return ExitSubTrade( '9000', '该单位批量数据文件已经被提交,不能撤销' )
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断批量申请是否已存在,数据库异常' )




#修改批次记录为撤销状态
def UpdateBatchInfo( ):


    AfaLoggerFunc.tradeInfo('>>>修改批次记录为撤销状态')


    try:
        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET "
        sql = sql + "STATUS='" + "40"       + "',"                                                #状态(撤销)
        sql = sql + "NOTE5='"  + "手工撤消" + "'"                                                 #撤消原因

        sql = sql + " WHERE "

        sql = sql + "APPNO="   + "'" + TradeContext.I1APPNO    + "'" + " AND "                    #业务编码
        sql = sql + "BUSINO="  + "'" + TradeContext.I1BUSINO   + "'" + " AND "                    #单位编码
        sql = sql + "ZONENO="  + "'" + TradeContext.I1ZONENO   + "'" + " AND "                    #地区代码
        sql = sql + "BRNO="    + "'" + TradeContext.I1SBNO     + "'" + " AND "                    #机构代码
        sql = sql + "BATCHNO=" + "'" + TradeContext.I1BATCHNO  + "'" + " AND "                    #委托号
        sql = sql + "INDATE="  + "'" + TradeContext.I1WORKDATE + "'"                              #委托日期
 
 
        AfaLoggerFunc.tradeInfo( sql )


        result = AfaDBFunc.UpdateSqlCmt( sql )
        if (result <= 0):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '撤销批量申请失败' )


        AfaLoggerFunc.tradeInfo(">>>总共修改[" + str(result) + "]条记录")

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '撤销批量申请失败,数据库异常' )


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        
