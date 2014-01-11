###############################################################################
# -*- coding: gbk -*-
# 摘    要：新农保批量业务
# 当前版本：1.0
# 作    者：蔡永贵
# 完成日期：2010年12月15日
###############################################################################
import AfaDBFunc,AfaLoggerFunc,AhXnbFunc,TradeContext
import os
from types import *

#=====================安徽省新农保批量作业申请==============================================
def TrxMain( ):

    AfaLoggerFunc.tradeInfo('---------安徽省批量申请进入------------')
    
    #----1，批次申请校验
    if TradeContext.I1FTPTYPE in ("0","1"):
        #判断单位协议是否有效（只有批量代发代扣才校验单位协议）
        if ( not AhXnbFunc.ChkUnitInfo( ) ):
            return False
    
    #转换批量开户后的文件时不需要此校验
    if TradeContext.I1FTPTYPE != "3":
        #判断批量申请是否已存在
        if (  not ChkBatchInfo( ) ):
            return False
    
    #----2，批次申请处理
    #读取配置文件信息
    if ( not AhXnbFunc.getBatchFile( "AHXNB" ) ):
        return False
    
    #----A，批量代发代扣-校验上传文件是否已上传
    if TradeContext.I1FTPTYPE in ("0","1"):
        TradeContext.swapFile=" "
        filePath = TradeContext.XNB_BSDIR + "/" + TradeContext.I1FILENAME
        if not os.path.exists(filePath):
            return ExitSubTrade( "E0001","批量文件不存在，请确认文件是否上传" ) 
        pass
        
    #----B，批量开户-上传文件转转BC文件
    elif TradeContext.I1FTPTYPE == "2":
        if ( not CrtXnbFile( ) ):
            return False
    
    #----XX 开户后文件转换特殊处理-只需更改批次状态
    elif TradeContext.I1FTPTYPE == "3":
        if ( not AhXnbFunc.UpdateFileStatus( TradeContext.I1BATCHNO,'4', '正在处理开户后的批量文件，请等待...', TradeContext.WorkTime) ):
            return False
        #转换成功后应该直接返回，不再走后续流程
        TradeContext.O1AFAPDATE = TradeContext.WorkDate
        TradeContext.O1AFAPTIME = TradeContext.WorkTime
        return ExitSubTrade('0000', '交易成功')
    
    #20110601曾照泰修改 前台添加操作类型为4 表示已经开过户，只需批量签约即可
    #begin
    elif TradeContext.I1FTPTYPE == "4":
        if ( not CrtBatchNo( ) ): 
            return False          
        
        if ( not inserXnbFile_for_4() ):
            return False
        #插入ahnx_file表成功后应该直接返回，不再走后续流程
        TradeContext.O1AFAPDATE = TradeContext.WorkDate
        TradeContext.O1AFAPTIME = TradeContext.WorkTime
        return ExitSubTrade('0000', '交易成功')
    else:
        return ExitSubTrade( "E0001","没有该操作类型" )
    
    #end
            
    #生成委托号
    if ( not CrtBatchNo( ) ):
        return False
    
    #登记批量文件登记表AHNX_FILE
    if ( not inserXnbFile( ) ):
        return False
    TradeContext.O1BATCHNO  = TradeContext.BATCHNO
    TradeContext.O1AFAPDATE = TradeContext.WorkDate
    TradeContext.O1AFAPTIME = TradeContext.WorkTime
    TradeContext.O1FILENAME = TradeContext.swapFile
    TradeContext.errorCode  = "0000"
    TradeContext.errorMsg   = "交易成功"
    AfaLoggerFunc.tradeInfo('---------安徽省批量申请退出------------')
    
    return ExitSubTrade('0000', '交易成功')

#------------------------------------------------------------------
#批量开户文件格式转换
#------------------------------------------------------------------
def CrtXnbFile( ):
    #获取一个3位的序列号，用于拼上送核心的开户文件名
    CrtSequence( )
    
    try:
        #----2，开户文件转换BC文件
        TradeContext.sFileName = TradeContext.XNB_BSDIR + "/" + TradeContext.I1FILENAME
        #上送核心批量开户文件：BC+10机构号+8日期+3序号.TXT
        TradeContext.swapFile  = "BC" + TradeContext.I1SBNO + TradeContext.WorkDate + TradeContext.sequenceNo + ".TXT"
        TradeContext.dFileName = TradeContext.XNB_BDDIR + "/" + TradeContext.swapFile
        
        AfaLoggerFunc.tradeInfo(TradeContext.sFileName)
        if not os.path.exists(TradeContext.sFileName):
            return ExitSubTrade( "E0001", "批量文件不存在" )
            
        sfp = open(TradeContext.sFileName,"r")
        dfp = open(TradeContext.dFileName,"w")
        
        line = sfp.readline()
        fileCount = 0
        while( len(line) > 0 ):
            line = sfp.readline()
            fileCount = fileCount + 1
        AfaLoggerFunc.tradeInfo("批量开户笔数" + str(fileCount))
        sfp.close( )
        
        #----2.1，核心对于单次批量开户笔数不能超过500笔
        if fileCount > 500:
            return ExitSubTrade("E0001","单次批量开户笔数不能超过500笔")
            
        sfp = open(TradeContext.sFileName,"r")
        #写入汇总:总笔数|金额|现转标志 0-现金|开户类型 0428-对私开户|||币种01|是否通存通兑1-通存|
        lineinfo = str(fileCount) + "|0.00|0|0428|||01|1|"
        dfp.write(lineinfo + "\n")
        
        #读取一行
        linebuff = sfp.readline( )
        #写入文件的序号
        sequenceNO = 0
        
        #begin 20120209 胡友增加 删除详细处理信息文件
        AhXnbFunc.DelProcmsgFile(TradeContext.I1FILENAME[:-4])
        flag = 0           #处理标识
        #end
        
        AfaLoggerFunc.tradeInfo('开户文件转换BC文件开始。。。。。。')
        
        while( len(linebuff)>0 ):
            sequenceNO = sequenceNO + 1
            swapbuff = linebuff.split("|")
            
            if len(swapbuff) !=5:
                #----2.2，开户文件格式校验
                #begin 20120209 胡友增加 如上传文件格式错误,将详细信息写入文件
                AhXnbFunc.WriteInfo(TradeContext.I1FILENAME[:-4] ,"上传文件第" + str(sequenceNO) + "行格式[字段]不正确，请检查")
                flag = 1
                #end
                
                linebuff = sfp.readline( )
                continue
                
            TradeContext.SBNO        = swapbuff[0].lstrip().rstrip()          #社保编号
            TradeContext.NAME        = swapbuff[1].lstrip().rstrip()          #姓名
            TradeContext.IDENTITYNO  = swapbuff[2].lstrip().rstrip()          #身份证
            TradeContext.XZQHNO      = swapbuff[3].lstrip().rstrip()          #行政区划代码
            TradeContext.XZQHNAME    = swapbuff[4].lstrip().rstrip()          #行政区划名称
            
            #begin 20120209 胡友增加 若格式失败，不生成目标批量文件，继续查看格式
            if (flag == 1):
                linebuff = sfp.readline( )
                continue
            #end
            
            #----2.3，上传文件信息写入BC文件
            #前台提供的批量开户文件格式:序号|证件种类(01-身份证)|身份证|姓名|金额|2| | | |||
            lineinfo =            str(sequenceNO)          + "|"
            lineinfo = lineinfo + "01"                     + "|"
            lineinfo = lineinfo + TradeContext.IDENTITYNO  + "|"
            lineinfo = lineinfo + TradeContext.NAME        + "|"
            lineinfo = lineinfo + "0.00"                   + "|"
            lieninfo = lineinfo + "2"                      + "|"
            lineinfo = lineinfo + ""                       + "|"
            lineinfo = lineinfo + ""                       + "|"
            lineinfo = lineinfo + ""                       + "|"
            lineinfo = lineinfo + ""                       + "|"
            lineinfo = lineinfo + ""                       + "|"
            
            dfp.write(lineinfo + "\n")
            
            #----2.4，登记明细信息
            if not insertXnbMac( ):
                return False
            
            linebuff = sfp.readline( )
            
        sfp.close( )
        dfp.close( )
        AfaLoggerFunc.tradeInfo('开户文件转换BC文件结束。。。。。。')
        
        #begin 20120209 胡友增加处理标识为失败时，处理下一批次
        if (flag == 1):
            AfaLoggerFunc.tradeInfo( "批次"+TradeContext.I1FILENAME[:-4]+"上传文件格式错误,原因已写入详细处理文件")
            TradeContext.errorCode,TradeContext.errorMsg = '9000','上传文件格式错误,原因已写入详细处理文件'
            
            if ( os.path.exists(TradeContext.dFileName) and os.path.isfile(TradeContext.dFileName) ):
                cmdstr = "rm " + TradeContext.dFileName
                AfaLoggerFunc.tradeInfo('>>>删除命令:' + cmdstr)
                os.system(cmdstr)
            
            return False
        #end
        
        return True
    except Exception, e:
        sfp.close()
        dfp.close()
        return ExitSubTrade('E0001', str(e))
        
#------------------------------------------------------------------
#批量文件登记表AHNX_FILE 
#------------------------------------------------------------------
def inserXnbFile( ):
    
    sql = ""
    sql = sql + "insert into AHNX_FILE("
    sql = sql + "BATCHNO,"
    sql = sql + "FILENAME,"
    sql = sql + "SWAPFILENAME,"
    sql = sql + "WORKDATE,"
    sql = sql + "STATUS,"
    sql = sql + "PROCMSG,"
    sql = sql + "APPLYDATE,"
    sql = sql + "APPNO,"
    sql = sql + "BUSINO,"
    sql = sql + "TOTALNUM,"
    sql = sql + "TOTALAMT,"
    sql = sql + "FILETYPE,"
    sql = sql + "BRNO,"
    sql = sql + "TELLERNO,"
    sql = sql + "BEGINDATE,"
    sql = sql + "ENDDATE,"
    sql = sql + "WORKTIME,"
    sql = sql + "NOTE1,"
    sql = sql + "NOTE2,"
    sql = sql + "NOTE3,"
    sql = sql + "NOTE4)"
    sql = sql + " values("
    sql = sql + "'" + TradeContext.BATCHNO     + "',"             #登记流水号
    sql = sql + "'" + TradeContext.I1FILENAME  + "',"             #文件名
    sql = sql + "'" + TradeContext.swapFile    + "',"             #转换后的文件名
    sql = sql + "'" + TradeContext.WorkDate    + "',"             #登记日期
    sql = sql + "'0',"                                            #状态(0-待处理，1-处理成功)
    sql = sql + "'上传成功，批量文件等待处理中...',"              #处理信息描述
    sql = sql + "'" + TradeContext.WorkDate    + "',"             #申请日期
    sql = sql + "'" + TradeContext.I1APPNO     + "',"             #业务编号
    sql = sql + "'" + TradeContext.I1BUSINO    + "',"             #单位编号
    sql = sql + "'" + TradeContext.I1TOTALNUM  + "',"             #总笔数
    sql = sql + "'" + TradeContext.I1TOTALAMT  + "',"             #总金额
    sql = sql + "'" + TradeContext.I1FTPTYPE   + "',"             #文件类型（0-批量代发，1-批量代扣，2-批量开户)
    sql = sql + "'" + TradeContext.I1SBNO      + "',"             #机构号
    sql = sql + "'" + TradeContext.I1USID      + "',"             #柜员号
    sql = sql + "'" + TradeContext.I1STARTDATE + "',"             #生效日期
    sql = sql + "'" + TradeContext.I1ENDDATE   + "',"             #失效日期
    sql = sql + "'" + TradeContext.WorkTime    + "',"             #申请时间
    sql = sql + "'',"                                             #备用1
    sql = sql + "'',"                                             #备用2
    sql = sql + "'',"                                             #备用3
    sql = sql + "'')"                                             #备用4
    
    AfaLoggerFunc.tradeInfo( "批量文件登记：" + sql )
    
    ret = AfaDBFunc.InsertSqlCmt(sql)
    
    if ret < 0:
        return ExitSubTrade('D0001', "插入数据失败")
        
    return True
    
#------------------------------------------------------------------
#往新农保开户表AHXNB_MAC中登记数据
#------------------------------------------------------------------
def insertXnbMac( ):

    sql = ""
    sql = sql + " select SBNO,NAME,IDENTITYNO,XZQHNAME,XZQHNO,ACCNO"
    sql = sql + " from AHXNB_MAC "
    sql = sql + " where SBNO = '" + TradeContext.SBNO  + "'" #社保编号
    
    #AfaLoggerFunc.tradeInfo( '批量开户校验sql：' + sql )
    result = AfaDBFunc.SelectSql( sql )
    
    if result == None:
        return ExitSubTrade('D0001', "校验批量开户失败，数据库异常")
    elif len(result) > 0:
        
        #胡友 20111116 start   先判断查询结果再处理
        #20110620 曾照泰 修改  如果该客户已经在ahxnb_mac表中登记直接返回True
        #return True
        #return ExitSubTrade('D0001', "该客户已经登记过，跳过此条记录")
        
        flag = ( len(result[0][5].strip()) == 0 )
        
        #账号为空，删除原记录，插入新纪录
        if( flag ):
            sql2 = ""
            sql2 = sql2 + "delete"
            sql2 = sql2 + " from ahxnb_mac"
            sql2 = sql2 + " where sbno = '" + TradeContext.SBNO + "'"
            
            #AfaLoggerFunc.tradeInfo( '删除系统占用社保编号sql2：' + sql2 )
            result2 = AfaDBFunc.DeleteSqlCmt( sql2 )
            
            if( result2 <= 0 ):
                #AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return ExitSubTrade( '9000', '删除系统占用社保编号失败')
            
        #账号不为空跳出
        else:
            return True
        #end
        
        
    sql = ""
    sql = sql + "insert into AHXNB_MAC("
    sql = sql + "SBNO,"
    sql = sql + "NAME,"
    sql = sql + "IDENTITYNO,"
    sql = sql + "XZQHNO,"
    sql = sql + "XZQHNAME,"
    sql = sql + "ACCNO,"
    sql = sql + "STATUS,"
    sql = sql + "WORKDATE,"
    sql = sql + "BRNO,"
    sql = sql + "NOTE1,"
    sql = sql + "NOTE2,"
    sql = sql + "NOTE3,"
    sql = sql + "NOTE4)"
    sql = sql + " values("
    sql = sql + "'" + TradeContext.SBNO       + "',"             #社保编号
    sql = sql + "'" + TradeContext.NAME       + "',"             #姓名
    sql = sql + "'" + TradeContext.IDENTITYNO + "',"             #身份证
    sql = sql + "'" + TradeContext.XZQHNO     + "',"             #行政区划代码
    sql = sql + "'" + TradeContext.XZQHNAME   + "',"             #行政区划名称
    sql = sql + "'',"                                            #银行账号
    sql = sql + "'1',"                                           #状态(0-已开户，1-未开户，2-已注销)
    sql = sql + "'',"                                            #开户日期
    sql = sql + "'',"                                            #开户机构
    sql = sql + "'',"                                            #备用1
    sql = sql + "'',"                                            #备用2
    sql = sql + "'',"                                            #备用3
    sql = sql + "'')"                                            #备用4
    
    #AfaLoggerFunc.tradeInfo( "批量开户登记：" + sql )
    
    ret = AfaDBFunc.InsertSqlCmt(sql)
    
    if ret < 0:
        
        return ExitSubTrade('D0001', "插入数据失败")
        
    return True
    

#------------------------------------------------------------------
#判断批量申请是否已存在
#------------------------------------------------------------------
def ChkBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>判断批量申请是否已存在')

    try:
        sql = "SELECT BATCHNO,STATUS FROM AHNX_FILE WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO     + "'" + " AND "        #业务编号
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO    + "'" + " AND "        #单位编号
        sql = sql + "WORKDATE=" + "'" + TradeContext.WorkDate    + "'" + " AND "        #委托日期
        sql = sql + "FILENAME=" + "'" + TradeContext.I1FILENAME  + "'" + " AND "        #申请文件
        sql = sql + "STATUS<>"  + "'" + "2"                      + "'"                  #状态(撤销)

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql(sql)
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询批量信息表异常' )

        if ( len(records) > 0 ):
            #判断状态
            if ( str(records[0][1]) in ('0','3','4')  ):
                return ExitSubTrade( '9000', '该机构该单位今天的批量数据文件正在处理中,不能进行申请操作' )

            elif ( str(records[0][1]) == "1" ):
                return ExitSubTrade( '9000', '该机构该单位今天的批量数据文件已经处理完成,不能再次申请' )

        else:
            AfaLoggerFunc.tradeInfo('>>>没有发现该机构今天申请批量数据文件,可以申请')
            return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断批量申请是否已存在,数据库异常' )
        
#------------------------------------------------------------------
#生成委托号
#------------------------------------------------------------------
def CrtBatchNo( ):

    AfaLoggerFunc.tradeInfo('>>>生成批次委托号')

    try:
        sqlStr = "SELECT NEXTVAL FOR ABDT_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '生成委托号异常' )

        #批次号
        TradeContext.BATCHNO = TradeContext.WorkDate + str(records[0][0]).rjust(8, '0')

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '生成委托号异常' )
        
        
#------------------------------------------------------------------
#生成一个3位的序号
#------------------------------------------------------------------
def CrtSequence( ):
    
    try:
        sqlStr = "SELECT NEXTVAL FOR AHXNB_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '生成序列号异常' )
        AfaLoggerFunc.tradeInfo( "序列号：" + str(records[0][0]) )
        
        #序列号
        TradeContext.sequenceNo = str(records[0][0]).rjust(3,'0')
        
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '生成委托号异常' )

#------------------------------------------------------------------
#20110601曾照泰修改添加
#登记表AHNX_FILE，只登记操作类型为4的记录，即只做批量签约的记录 
#------------------------------------------------------------------
#begin
def inserXnbFile_for_4( ):
    
    sql = ""
    sql = sql + "insert into AHNX_FILE("
    sql = sql + "BATCHNO,"
    sql = sql + "FILENAME,"
    sql = sql + "SWAPFILENAME,"
    sql = sql + "WORKDATE,"
    sql = sql + "STATUS,"
    sql = sql + "PROCMSG,"
    sql = sql + "APPLYDATE,"
    sql = sql + "APPNO,"
    sql = sql + "BUSINO,"
    sql = sql + "TOTALNUM,"
    sql = sql + "TOTALAMT,"
    sql = sql + "FILETYPE,"
    sql = sql + "BRNO,"
    sql = sql + "TELLERNO,"
    sql = sql + "BEGINDATE,"
    sql = sql + "ENDDATE,"
    sql = sql + "WORKTIME,"
    sql = sql + "NOTE1,"
    sql = sql + "NOTE2,"
    sql = sql + "NOTE3,"
    sql = sql + "NOTE4)"
    sql = sql + " values("
    sql = sql + "'" + TradeContext.BATCHNO     + "',"             #登记流水号
    sql = sql + "'" + TradeContext.I1FILENAME  + "',"             #文件名
    sql = sql + "'',"                                             #转换后的文件名
    sql = sql + "'" + TradeContext.WorkDate    + "',"             #登记日期
    sql = sql + "'0',"                                            #状态(0-待处理，1-处理成功)
    sql = sql + "'上传成功,等待批量签约...',"                     #处理信息描述
    sql = sql + "'" + TradeContext.WorkDate    + "',"             #申请日期
    sql = sql + "'" + TradeContext.I1APPNO     + "',"             #业务编号
    sql = sql + "'" + TradeContext.I1BUSINO    + "',"             #单位编号
    sql = sql + "'" + TradeContext.I1TOTALNUM  + "',"             #总笔数
    sql = sql + "'" + TradeContext.I1TOTALAMT  + "',"             #总金额
    sql = sql + "'" + TradeContext.I1FTPTYPE   + "',"             #文件类型（0-批量代发，1-批量代扣，2-批量开户，3-开户后文件转换，4-批量签约)
    sql = sql + "'" + TradeContext.I1SBNO      + "',"             #机构号
    sql = sql + "'" + TradeContext.I1USID      + "',"             #柜员号
    sql = sql + "'" + TradeContext.I1STARTDATE + "',"             #生效日期
    sql = sql + "'" + TradeContext.I1ENDDATE   + "',"             #失效日期
    sql = sql + "'" + TradeContext.WorkTime    + "',"             #申请时间
    sql = sql + "'',"                                             #备用1
    sql = sql + "'',"                                             #备用2
    sql = sql + "'',"                                             #备用3
    sql = sql + "'')"                                             #备用4
    
    AfaLoggerFunc.tradeInfo( "批量文件登记：" + sql )
    
    ret = AfaDBFunc.InsertSqlCmt(sql)
    
    if ret < 0:
        return ExitSubTrade('D0001', "插入数据失败")
        
    return True
#end

        
#------------------------------------------------------------------
#抛出并打印提示信息
#------------------------------------------------------------------
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg
        AfaLoggerFunc.tradeInfo( errorMsg )

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
