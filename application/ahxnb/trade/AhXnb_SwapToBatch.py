# -*- coding: GB18030 -*-
###############################################################################
# 文件名称：AhXnb_SwapToBatch.py
# 文件标识：
# 作    者：曾照泰
# 摘    要：转换批量代扣代发文件为批量系统处理需要的格式
#
###############################################################################
import TradeContext                

TradeContext.sysType = 'ahxnb'

import AfaDBFunc,os,AfaLoggerFunc,sys,ConfigParser,AhXnbFunc,AfaFtpFunc
from types import *

#批量代发代扣文件格式转换
#------------------------------------------------------------------
def file_To_Batch_Pro( ):
    AfaLoggerFunc.tradeInfo( '文件操作开始' )
    
    try:
        #-----1,查询未处理的批量文件
        sql = ''
        sql = sql + "select filename,batchno,appno,busino,workdate,brno,tellerno,begindate,enddate,worktime,totalnum,totalamt,filetype"
        sql = sql + " from ahnx_file"
        sql = sql + " where status='0'"             #上传成功
        sql = sql + " and filetype in ('0','1')"    #代发代扣
        
        AfaLoggerFunc.tradeInfo('>>>>>>>开始查询AHNX_FILE原交易：'+ str(sql))
        records = AfaDBFunc.SelectSql( sql )
        
        if records==None:
            return ExitSubTrade( 'E0001', "操作数据库失败")
            
        elif(len(records) == 0):
            return ExitSubTrade( 'E0001', "无此信息")
            
        else:
            AfaLoggerFunc.tradeInfo("AHNX_FILE表中的记录数：" +str(len(records)))
            
            for i in range(len(records)):
                #用来保存需要转化的文件             
                TradeContext.I1FILENAME = records[i][0]
                #委托号
                TradeContext.BATCHNO    = records[i][1]
                #业务编号
                TradeContext.I1APPNO    = records[i][2]
                #单位编号
                TradeContext.I1BUSINO   = records[i][3]
                #申请日期
                TradeContext.WorkDate   = records[i][4]
                #机构号
                TradeContext.I1SBNO     = records[i][5]
                #柜员号
                TradeContext.I1USID     = records[i][6]
                #生效日期
                TradeContext.I1STARTDATE= records[i][7]
                #失效日期
                TradeContext.I1ENDDATE  = records[i][8]
                #申请时间
                TradeContext.WorkTime   = records[i][9]
                #总笔数
                TradeContext.I1TOTALNUM = records[i][10]
                #总金额
                TradeContext.I1TOTALAMT = records[i][11]
                #代发代扣标志
                TradeContext.FILETYPE   = records[i][12]
                
                #-----2，上传文件转换成批量处理文件(先生成up_other下文件,后上传swap目录)
                TradeContext.sFileName = TradeContext.XNB_BSDIR + "/" + TradeContext.I1FILENAME
                TradeContext.swapFile  = TradeContext.I1APPNO + TradeContext.I1BUSINO + "0000"
                TradeContext.dFileName = TradeContext.XNB_BDDIR + "/" + TradeContext.swapFile
                TradeContext.pFileName = TradeContext.ABDT_PDIR + "/" + TradeContext.I1APPNO + TradeContext.I1BUSINO + "0000_" + TradeContext.WorkDate
                
                #20120916 上传至批量目录文件名
                TradeContext.batchFile = TradeContext.I1APPNO + TradeContext.I1BUSINO + "0000_" + TradeContext.WorkDate
                
                AfaLoggerFunc.tradeInfo("转换成批量处理前的文件为：" +TradeContext.sFileName)
                AfaLoggerFunc.tradeInfo("转换成批量操作的文件为："  +TradeContext.dFileName)
                
                if not os.path.exists(TradeContext.sFileName):
                    AfaLoggerFunc.tradeInfo("待转换文件："  +TradeContext.sFileName + "不存在")
                    AhXnbFunc.UpdateFileStatus(TradeContext.BATCHNO, '2', '待转换的文件不存在', TradeContext.WorkTime)
                    continue
                
                sfp = open(TradeContext.sFileName,"r")
                dfp = open(TradeContext.dFileName,"w")
                
                #----2.1,总比数校验(<=15w)
                line = sfp.readline()
                fileCount = 0
                while( len(line) > 0 ):
                    line = sfp.readline()
                    fileCount = fileCount + 1
                sfp.close( )
                AfaLoggerFunc.tradeInfo('该批次上传文件总比数为：'+str(fileCount))
                
                if fileCount > 150000:
                    AhXnbFunc.UpdateBatchInfo(TradeContext.BATCHNO, "2", "上传文件总比数大于15w笔,请处理后再申请" )
                    continue
                
                sfp = open(TradeContext.sFileName,"r")
                
                linebuff = sfp.readline( )
                lineCount = 0
                
                #begin 20120209 胡友增加 删除详细处理信息文件
                AhXnbFunc.DelProcmsgFile(TradeContext.BATCHNO)
                #end
                
                flag = 0           #处理标识
                AfaLoggerFunc.tradeInfo('批次文件循环校验开始。。。。。。')
                
                while( len(linebuff)>0 ):
                    lineCount = lineCount + 1
                    swapbuff = linebuff.split("|")
                                        
                    #----2.2,格式检验
                    if len(swapbuff) !=7:
                        #begin 20120209 胡友增加 如上传文件格式错误，更新ahxnb_file表，并将详细信息写入文件
                        AhXnbFunc.UpdateBatchInfo(TradeContext.BATCHNO, "2", "上传文件格式错误,原因见详细信息" ,"上传文件第" + str(lineCount) + "行格式[字段数]不正确，请检查")
                        flag = 1
                        #end
                        
                        linebuff = sfp.readline( )
                        continue
                    
                    TradeContext.SBNO        = swapbuff[0].lstrip().rstrip()          #社保编号
                    TradeContext.NAME        = swapbuff[1].lstrip().rstrip()          #姓名
                    TradeContext.IDENTITYNO  = swapbuff[2].lstrip().rstrip()          #身份证
                    TradeContext.AMOUNT      = swapbuff[3].lstrip().rstrip()          #代扣金额
                    TradeContext.SBBILLNO    = swapbuff[4].lstrip().rstrip()          #批次号
                    TradeContext.ACCNO       = swapbuff[5].lstrip().rstrip()          #人员账号
                    TradeContext.AreaCode    = swapbuff[6].lstrip().rstrip()          #行政区划保存到ahxnb_swap的note4中
                    
                    #begin 20120209 胡友增加 若格式失败，不写入目标批量文件，继续查看格式
                    if(flag == 1):
                        linebuff = sfp.readline( )
                        continue
                    #end
                    
                    #----2.4,登记明细信息
                    insertBatch( )
                    
                    #----2.5，转换字段写入文件
                    lineinfo =            TradeContext.SBNO   + "|"
                    lineinfo = lineinfo + TradeContext.ACCNO  + "|"
                    lineinfo = lineinfo + TradeContext.NAME   + "|"
                    lineinfo = lineinfo + TradeContext.AMOUNT + "|"
                    dfp.write(lineinfo + "\n")
                    linebuff = sfp.readline( )
                    
                sfp.close( )
                dfp.close( )
                
                AfaLoggerFunc.tradeInfo('批次文件循环校验结束。。。。。。')
                AfaLoggerFunc.tradeInfo('上传文件总比数为'+str(lineCount))
                
                #----3，上传文件校验后处理
                #----3.1，失败  删除批量文件即可
                if (flag == 1):
                    AfaLoggerFunc.tradeInfo("批次"+TradeContext.BATCHNO+"上传文件格式错误,原因已写入详细处理文件")
                    fileName = os.environ['AFAP_HOME'] + '/data/ahxnb/' + TradeContext.swapFile
                    
                    if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
                        cmdstr = "rm " + fileName
                        AfaLoggerFunc.tradeInfo('>>>删除命令:' + cmdstr)
                        os.system(cmdstr)
                    continue
                #end
                
                #-----3.2,成功  更新ahnx_file表，移走批量文件，登记批量申请
                #-----3.2.1，更新ahnx_file表
                sqlupdate = ""
                sqlupdate = sqlupdate + "update ahnx_file set"
                sqlupdate = sqlupdate + " status='3',"
                sqlupdate = sqlupdate + " procmsg='格式转换完成，等待批量业务系统做批量处理'"
                sqlupdate = sqlupdate + " where batchno = '"+ TradeContext.BATCHNO +"'"
                
                AfaLoggerFunc.tradeInfo("更新数据库语句：" + sqlupdate)
                result   = AfaDBFunc.UpdateSqlCmt( sqlupdate )
                
                if( result <0 ):
                    continue
                
                #-----3.2.2，把文件移到批量内部操作目录中(swap)
                try:
                    #20120916 将本地操作更改为 FTP 操作
                    #begin
                    #cp_cmd_str="mv " + TradeContext.dFileName + " " + TradeContext.pFileName
                    #os.system(cp_cmd_str)
                    
                    if not AfaFtpFunc.putFile('AHXNB_PUT',TradeContext.swapFile,TradeContext.batchFile) :
                        AfaLoggerFunc.tradeInfo('ftp上传文件失败 : '+ TradeContext.swapFile)
                        #GridFunc.WriteInfo('Grid_ToBatch'+ TradeContext.gridIds[i][0].strip() + TradeContext.WorkDate,'ftp上传失败,文件是='+ TradeContext.dFileName)
                        continue
                        
                    #end
                    
                except Exception, e:
                    AfaLoggerFunc.tradeInfo( str(e) )
                    continue
                
                #-----3.2.3，登记批量代发代扣申请信息
                if (  not ChkBatchInfo( ) ):
                    #更新AHXNB_FILE
                    sqlupdate = "update ahnx_file set status='2',procmsg='"+ TradeContext.errorMsg +"'"
                    sqlupdate = sqlupdate + "where batchno = '"+ TradeContext.BATCHNO +"'"
                    AfaLoggerFunc.tradeInfo("更新数据库语句：" + sqlupdate)
                    result   = AfaDBFunc.UpdateSqlCmt( sqlupdate )
                    continue
                    
                if( not InsertBatchInfo( ) ):
                    continue
                    
            return True
    except Exception, e:
        sfp.close()
        dfp.close()

        return ExitSubTrade('E0001', str(e))


#------------------------------------------------------------------
#读取配置信息
#------------------------------------------------------------------
def getBatchFile( ConfigNode ):
    try:
        #读取FTP配置文件
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        
        config.readfp( open( configFileName ) )
        
        TradeContext.ABDT_PDIR    = config.get(ConfigNode,'ABDT_BDIR')     #批量上传文件存放路径
        TradeContext.ABDT_GDIR    = config.get(ConfigNode,'ABDT_GDIR')     #批量回盘文件存放路径
        TradeContext.XNB_BSDIR    = config.get(ConfigNode,'XNB_BSDIR')     #新农保转换前的路径
        TradeContext.XNB_BDDIR    = config.get(ConfigNode,'XNB_BDDIR')     #新农保转换后的路径
        
        
        return True
        
    except Exception, e:
        return ExitSubTrade( 'E0001', "读取配置文件异常：" + str(e))

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
   

#------------------------------------------------------------------
#往批量转换表AHXNB_SWAP中登记临时数据
#------------------------------------------------------------------
def insertBatch( ):    
    #先查询数据是否存在
    sql = ""
    sql = sql + "select IDENTITYNO,SBBILLNO,NAME"
    sql = sql + " from ahxnb_swap"
    sql = sql + " where sbno = '" + TradeContext.SBNO + "'"          #社保编号
    sql = sql + " and workdate = '" + TradeContext.WorkDate + "'"    #申请日期
    AfaLoggerFunc.tradeInfo(sql) 
    ret = AfaDBFunc.SelectSql( sql )
    
    if ret == None:
        return False
        
    elif( len(ret) == 0 ):
        pass
        
    elif len(ret) > 0:
        #先判断该批次是否存在,若存在-不插入，若不存在-插入
        for j in range(0,len(ret)):
            if( TradeContext.SBBILLNO == ret[j][1].strip() ):
                return False
                
        #一个上传文件中同一客户有多个批次时，Name后加标识
        TradeContext.NAME = TradeContext.NAME + ";" + str( len(ret) )
        
    sql = ""
    sql = sql + "insert into AHXNB_SWAP("
    sql = sql + "SBNO,"
    sql = sql + "NAME,"
    sql = sql + "IDENTITYNO,"
    sql = sql + "AMOUNT,"
    sql = sql + "SBBILLNO,"
    sql = sql + "ACCNO,"
    sql = sql + "FILENAME,"
    sql = sql + "WORKDATE,"
    sql = sql + "NOTE1,"
    sql = sql + "NOTE2,"
    sql = sql + "NOTE3,"
    sql = sql + "NOTE4)"
    
    sql = sql + " values("
    sql = sql + "'" + TradeContext.SBNO       + "',"             #社保编号
    sql = sql + "'" + TradeContext.NAME       + "',"             #姓名    
    sql = sql + "'" + TradeContext.IDENTITYNO + "',"             #身份证  
    sql = sql + "'" + TradeContext.AMOUNT     + "',"             #代扣金额
    sql = sql + "'" + TradeContext.SBBILLNO   + "',"             #批次号  
    sql = sql + "'" + TradeContext.ACCNO      + "',"             #人员账号
    sql = sql + "'" + TradeContext.I1FILENAME + "',"             #批量文件名
    sql = sql + "'" + TradeContext.WorkDate   + "',"             #批量登记日期
    
    sql = sql + "'',"
    sql = sql + "'',"
    sql = sql + "'',"
    sql = sql + "'" + TradeContext.AreaCode   + "')"             #行政区划
    AfaLoggerFunc.tradeInfo(sql)    
    ret = AfaDBFunc.InsertSqlCmt(sql)
    
    if ret < 0:
        return ExitSubTrade('D0001', "插入数据失败")
        
    return True
    
#------------------------------------------------------------------
#登记批次作业申请信息
#------------------------------------------------------------------
def InsertBatchInfo( ):
    AfaLoggerFunc.tradeInfo('>>>登记批次作业申请信息')

    try:
        sql = ""
        sql = "INSERT INTO ABDT_BATCHINFO("
        sql = sql + "BATCHNO,"                 #委托号(批次号: 唯一(日期+流水号)
        sql = sql + "APPNO,"                   #业务编号
        sql = sql + "BUSINO,"                  #单位编号
        sql = sql + "ZONENO,"                  #地区号
        sql = sql + "BRNO,"                    #网点号
        sql = sql + "USERNO,"                  #操作员
        sql = sql + "ADMINNO,"                 #管理员
        sql = sql + "TERMTYPE,"                #终端类型
        sql = sql + "FILENAME,"                #上传文件名
        sql = sql + "INDATE,"                  #委托日期
        sql = sql + "INTIME,"                  #委托时间
        sql = sql + "BATCHDATE,"               #提交日期
        sql = sql + "BATCHTIME,"               #提交时间
        sql = sql + "TOTALNUM,"                #总笔数
        sql = sql + "TOTALAMT,"                #总金额
        sql = sql + "SUCCNUM,"                 #成功笔数
        sql = sql + "SUCCAMT,"                 #成功金额
        sql = sql + "FAILNUM,"                 #失败笔数
        sql = sql + "FAILAMT,"                 #失败金额
        sql = sql + "STATUS,"                  #状态
        sql = sql + "BEGINDATE,"               #生效日期
        sql = sql + "ENDDATE,"                 #失效日期
        sql = sql + "PROCMSG,"                 #处理信息
        sql = sql + "NOTE1,"                   #备注1
        sql = sql + "NOTE2,"                   #备注2
        sql = sql + "NOTE3,"                   #备注3
        sql = sql + "NOTE4,"                   #备注4
        sql = sql + "NOTE5)"                   #备注5

        sql = sql + " VALUES ("

        sql = sql + "'" + TradeContext.BATCHNO          + "',"                              #委托号(批次号:唯一(日期+流水号)
        sql = sql + "'" + TradeContext.I1APPNO          + "',"                              #业务编号
        sql = sql + "'" + TradeContext.I1BUSINO         + "',"                              #单位编号
        sql = sql + "'" + TradeContext.I1SBNO[0:4]      + "',"                              #地区号
        sql = sql + "'" + TradeContext.I1SBNO           + "',"                              #网点号
        sql = sql + "'" + TradeContext.I1USID           + "',"                              #操作员
        sql = sql + "'0000000000',"                                                         #管理员
        sql = sql + "'1',"                                                                  #终端类型（0-柜面上传，1-外围上传）
        sql = sql + "'" + TradeContext.I1FILENAME       + "',"                              #批量文件
        sql = sql + "'" + TradeContext.WorkDate         + "',"                              #申请时间
        sql = sql + "'" + TradeContext.WorkTime         + "',"                              #申请时间
        sql = sql + "'" + "00000000"                    + "',"                              #提交日期
        sql = sql + "'" + "000000"                      + "',"                              #提交时间
        sql = sql + "'" + TradeContext.I1TOTALNUM       + "',"                              #总笔数
        sql = sql + "'" + TradeContext.I1TOTALAMT       + "',"                              #总金额
        sql = sql + "'" + "0"                           + "',"                              #成功笔数
        sql = sql + "'" + "0"                           + "',"                              #成功金额
        sql = sql + "'" + "0"                           + "',"                              #失败笔数
        sql = sql + "'" + "0"                           + "',"                              #失败金额
        sql = sql + "'" + "10"                          + "',"                              #状态(申请)
        sql = sql + "'" + TradeContext.I1STARTDATE      + "',"                              #生效日期
        sql = sql + "'" + TradeContext.I1ENDDATE        + "',"                              #失效日期
        sql = sql + "'申请->未处理',"                                                       #处理信息
        sql = sql + "'" + ""                            + "',"                              #备注1
        sql = sql + "'0000',"                                                               #备注2存放批次序号，柜面默认0000
        sql = sql + "'1',"                                                                  #备注3存放操作标志（0-实时处理，1-日终处理）
        sql = sql + "'',"                                                                   #备注4
        sql = sql + "'" + ""                            + "')"                              #备注5

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )

            #移动文件到/data/ahxnb/dust目录下
            TradeContext.Dustdir = os.environ['AFAP_HOME'] + '/data/ahxnb/dust'
            
            #20120917修改，删除新农保本地文件
            #mv_cmd_str="mv " + TradeContext.pFileName + " " + TradeContext.Dustdir
            mv_cmd_str="mv " + TradeContext.dFileName + " " + TradeContext.Dustdir
            os.system(mv_cmd_str)

            return ExitSubTrade( '9000', '登记批次作业申请信息失败')
        
        return True

    except Exception, e: 
        AfaLoggerFunc.tradeFatal( str(e) )
        #移动文件到/data/ahxnb/dust目录下
        TradeContext.Dustdir = os.environ['AFAP_HOME'] + '/data/ahxnb/dust'
        
        #20120917修改，删除新农保本地文件
        #mv_cmd_str="mv " + TradeContext.pFileName + " " + TradeContext.Dustdir
        mv_cmd_str ="mv " + TradeContext.dFileName + " " + TradeContext.Dustdir
        os.system(mv_cmd_str)
        return ExitSubTrade( '9999', '登记批次作业申请信息异常')

#判断批量申请是否已存在
def ChkBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>判断批量申请是否已存在')

    try:
        sql = "SELECT BATCHNO,STATUS FROM ABDT_BATCHINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO    + "'" + " AND "        #业务编号
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO   + "'" + " AND "        #单位编号
        sql = sql + "ZONENO="   + "'" + TradeContext.I1SBNO[0:4]+ "'" + " AND "        #地区代码
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO     + "'" + " AND "        #机构代码
        sql = sql + "INDATE="   + "'" + TradeContext.WorkDate   + "'" + " AND "        #委托日期
        sql = sql + "FILENAME=" + "'" + TradeContext.I1FILENAME + "'" + " AND "        #文件名称
        sql = sql + "STATUS<>"  + "'" + "40"                    + "'"                  #状态(撤销)

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql(sql)
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询批量信息表异常' )

        if ( len(records) > 0 ):
            #判断状态
            if ( str(records[0][1]) == "10" ):
                return ExitSubTrade( '9000', '该机构该单位的批量数据今天已经申请,不能再次申请' )

            elif ( str(records[0][1]) == "88" ):
                return ExitSubTrade( '9000', '该机构该单位的批量数据文件已经处理完成,不能再次申请' )

            else:
                return ExitSubTrade( '9000', '该机构该单位的批量数据文件正在处理,不能进行申请操作' )

        else:
            AfaLoggerFunc.tradeInfo('>>>没有发现该机构今天申请批量数据文件,可以申请')
            return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断批量申请是否已存在,数据库异常' )
        

        
#######################################主函数###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************把代发代扣文件转换成批量处理文件格式开始********************')
    
    #读取配置文件信息
    if ( not getBatchFile( "AHXNB" ) ):
        AfaLoggerFunc.tradeInfo("读取配置文件失败")
        sys.exit(-1)
    
    #转换处理
    if ( not file_To_Batch_Pro( ) ):
        AfaLoggerFunc.tradeInfo("转换处理文件格式失败")    
        sys.exit(-1)           
        
    AfaLoggerFunc.tradeInfo('********************把代发代扣文件转换成批量处理文件格式结束********************')              
