# -*- coding: gbk -*-
###############################################################################
# 文件名称：AhXnb_BatchQy.py
# 文件标识：
# 作    者：曾照泰  
# 修改时间：20110601
# 摘    要：批量签约并转换为社保需要的格式
#
###############################################################################
import TradeContext                

TradeContext.sysType = 'ahxnb'

import AfaDBFunc,os,AfaLoggerFunc,sys,AfaFunc,AhXnbFunc,ConfigParser
from types import *

#=========================处理函数==============================================
def file_Pro( ):
    try:
        
        #-----1，查询未处理的批量文件
        sql = ""
        sql = sql + " select batchno,filename,workdate,busino,WorkTime,tellerno,filename"
        sql = sql + " from ahnx_file"
        sql = sql + " where status='0'"        #上传成功
        sql = sql + " and filetype='4'"        #已有账号签约
        
        AfaLoggerFunc.tradeInfo('>>>>>>>开始查询AHNX_FILE原交易：'+ str(sql))
        records = AfaDBFunc.SelectSql( sql )
                  
        if records==None:
            return ExitSubTrade("D0001" ,"查询AHNX_FILE失败")
        elif(len(records) == 0):
            return ExitSubTrade("D0001" ,"无此信息")
            
        else:
            AfaLoggerFunc.tradeInfo("AHNX_FILE表中的记录数：" +str(len(records)))
            for i in range(len(records)):
                #委托号
                TradeContext.batchno      = records[i][0]
                #取得批量签约需转换的文件名
                TradeContext.FileName = records[i][1]
                #开户日期
                TradeContext.WorkDate     = records[i][2]
                #单位编号
                TradeContext.I1BUSINO     = records[i][3]
                #时间
                TradeContext.WorkTime     = records[i][4]
                #柜员号
                TradeContext.I1USID       = records[i][5]
                #原始文件名
                TradeContext.preFilename  = records[i][6]
                #把批量开户成功的数据转换成社保需要的文件格式
                if ( not CrtXnbFile_To_Sb( ) ):
                    continue
                
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return False

#------------------------------------------------------------------
#把批量签约文件转换成社保需要的文件格式
#------------------------------------------------------------------
def CrtXnbFile_To_Sb( ):
    try:
        #-----1，读取上传签约文件
        TradeContext.sFileName = TradeContext.FileName
        TradeContext.dFileName = "NBQYFH_" + TradeContext.sFileName[7:-4] + "_S" + ".TXT"      #签约成功明细文件
        TradeContext.dFileName_fail = "NBQYFH_" + TradeContext.sFileName[7:-4] + "_F" + ".TXT" #签约失败明细文件
        
        AfaLoggerFunc.tradeInfo("待转换前的文件:" + TradeContext.sFileName)
        AfaLoggerFunc.tradeInfo("待转换后(成功)的文件:" + TradeContext.dFileName)
        AfaLoggerFunc.tradeInfo("待转换后(失败)的文件:" + TradeContext.dFileName_fail)
        
        if not os.path.exists(TradeContext.XNB_BDDIR + "/" + TradeContext.sFileName):
            return ExitSubTrade('D0001', "批量文件不存在")
            
        sfp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.sFileName,"r")
        dfp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.dFileName,"w")
        ffp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.dFileName_fail,"w")
        
        #----1.1,胡友-20120210 总比数校验(<=15w)
        line = sfp.readline()
        fileCount = 0
        while( len(line) > 0 ):
            line = sfp.readline()
            fileCount = fileCount + 1
        sfp.close( )
        AfaLoggerFunc.tradeInfo('该批次上传文件总比数为：'+str(fileCount))
        
        if fileCount > 150000:
            AhXnbFunc.UpdateBatchInfo(TradeContext.batchno, "2", "上传文件总比数大于15w笔,请处理后再申请" )
            return False
        
        sfp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.sFileName,"r")
        #end
        
        #读取一行 读取的文件格式为：社保编号|身份证|姓名|存折号或卡号|
        linebuff = sfp.readline( )
        lineCount = 0
        
        #begin 20120209 胡友增加 删除详细处理信息文件
        AhXnbFunc.DelProcmsgFile(TradeContext.batchno)
        flag = 0          #处理标识
        #end
        
        AfaLoggerFunc.tradeInfo( '上传文件批量签约开始。。。。。。' )
        
        while( len(linebuff)>0 ):
            lineCount = lineCount + 1
            swapbuff = linebuff.split("|")
            
            #20120614曾照泰修改凭证号可以不输
            #----1.2,上传文件格式校验
            if len(swapbuff) != 5:
                #begin 20120209 胡友增加 如上传文件格式错误，更新ahxnb_file表，并将详细信息写入文件                                                            
                AhXnbFunc.UpdateBatchInfo(TradeContext.batchno, "2", "上传文件格式错误,原因见详细信息" ,"上传文件第" + str(lineCount) + "行格式[字段数]不正确，请检查")
                flag = 1
                #end
                
                linebuff = sfp.readline( )
                continue
            
            TradeContext.SBNO        = swapbuff[0].lstrip().rstrip()          #社保编号
            TradeContext.IDENTITYNO  = swapbuff[1].lstrip().rstrip()          #身份证
            TradeContext.NAME        = swapbuff[2].lstrip().rstrip()          #姓名
            if len(swapbuff[3].lstrip().rstrip()) == 23:                      #折为23位
                #折
                TradeContext.ACCNO   = swapbuff[3].lstrip().rstrip()
                #TradeContext.VOUHNO  = swapbuff[4].lstrip().rstrip()          #凭证号
                #20120614曾照泰修改如果是折凭证号固定为490123456789，方便柜员操作
                TradeContext.VOUHNO  = "490123456789"                         #凭证号
            else:
                #卡
                TradeContext.ACCNO   = swapbuff[3].lstrip().rstrip()
                TradeContext.VOUHNO  = TradeContext.ACCNO[8:18]               #凭证号
            
            #begin 20120209 胡友增加 若格式失败，不生成目标回盘文件，继续查看格式
            if (flag == 1):
                linebuff = sfp.readline( )
                continue
            #end
            
            #----1.3签约
            #----1.3.1,身份证字段校验
            if len(TradeContext.IDENTITYNO) == 18:
                limitDate = TradeContext.IDENTITYNO[6:14]
            elif len(TradeContext.IDENTITYNO) == 15:
                limitDate = "19" + TradeContext.IDENTITYNO[6:12]
            else:
                failinfo = ""
                failinfo = failinfo + TradeContext.SBNO       + "|"     #社保编号
                failinfo = failinfo + TradeContext.NAME       + "|"     #姓名
                failinfo = failinfo + TradeContext.IDENTITYNO + "|"     #身份证
                failinfo = failinfo + "签约上传文件的"+str(lineCount)+"身份证字段长度不对，请检查"            #返回说明
                ffp.write(failinfo + "\n")
                
                linebuff = sfp.readline( )
                continue
            
            #----1.3.2，客户年龄判断
            #----A，客户<60周岁签约
            if limitDate > "19491231":
                if ( not CrtCustInfo( ) ):
                
                    #----A,签约失败的写入失败明细文件
                    failinfo = ""
                    failinfo = failinfo + TradeContext.SBNO       + "|"     #社保编号
                    failinfo = failinfo + TradeContext.NAME       + "|"     #姓名
                    failinfo = failinfo + TradeContext.IDENTITYNO + "|"     #身份证
                    
                    if( TradeContext.existVariable('errorMsg') ):
                        failinfo = failinfo + TradeContext.errorMsg         #返回说明
                    else:
                        failinfo = failinfo + "该客户代扣协议签订失败"+ ""
                    
                    ffp.write(failinfo + "\n")
                    
                    linebuff = sfp.readline( )
                    continue
                
                #----B，签约成功的写入成功明细文件
                lineinfo = ""
                lineinfo = lineinfo + TradeContext.SBNO       + "|"                 #社保编号
                lineinfo = lineinfo + TradeContext.NAME       + "|"                 #姓名
                lineinfo = lineinfo + TradeContext.IDENTITYNO + "|"                 #身份证
                lineinfo = lineinfo + TradeContext.ACCNO      + ""                  #账号
                dfp.write(lineinfo + "\n")
                
                linebuff = sfp.readline( )
            
            #----B，客户>60周岁不签约，写入签约失败明细文件
            else:
                failinfo = ""
                failinfo = failinfo + TradeContext.SBNO       + "|"     #社保编号
                failinfo = failinfo + TradeContext.NAME       + "|"     #姓名
                failinfo = failinfo + TradeContext.IDENTITYNO + "|"     #身份证
                failinfo = failinfo + "该客户年龄大于60周岁，无需签订代扣协议"  + ""      #返回说明
                ffp.write(failinfo + "\n")
                
                linebuff = sfp.readline( )
            
        sfp.close( )
        dfp.close( )
        ffp.close( )
        AfaLoggerFunc.tradeInfo( '上传文件批量签约结束。。。。。。' )
        
        #begin 20120209 胡友增加处理标识为失败时，处理下一批次
        if (flag == 1):
            AfaLoggerFunc.tradeInfo("批次"+TradeContext.batchno+"上传文件格式错误,原因已写入详细处理文件")
            fileName1 = os.environ['AFAP_HOME'] + '/data/ahxnb/' + TradeContext.dFileName
            fileName2 = os.environ['AFAP_HOME'] + '/data/ahxnb/' + TradeContext.dFileName_fail
                    
            if ( os.path.exists(fileName1) and os.path.isfile(fileName1) ):
                cmdstr = "rm " + fileName1
                AfaLoggerFunc.tradeInfo('>>>删除命令:' + cmdstr)
                os.system(cmdstr)
                
            if ( os.path.exists(fileName2) and os.path.isfile(fileName2) ):
                cmdstr = "rm " + fileName2
                AfaLoggerFunc.tradeInfo('>>>删除命令:' + cmdstr)
                os.system(cmdstr)
                
            return False
        #end
        
        #----3,更新ahxnb_file表
        if ( not AhXnbFunc.UpdateFileStatus(TradeContext.batchno,'1','批量签约成功，并转换成功，可以下载',TradeContext.WorkTime) ):
            return False
        
        return True
    except Exception, e:
        sfp.close()
        dfp.close()
        ffp.close()
        return ExitSubTrade('D0001', str(e))

#------------------------------------------------------------------
#签订个人协议
#------------------------------------------------------------------
def CrtCustInfo( ):
    #检查个人协议是否存在
    if ( not ChkCustInfo( ) ):
        return False
        
    #自动生成个人协议编号
    if ( AfaFunc.GetSerialno() < 0 ):
        return ExitSubTrade( '9000', '生成个人协议编号失败' )


    #组织个人协议编码(交易日期 + 中间业务流水号)
    TradeContext.PROTOCOLNO = TradeContext.WorkDate + TradeContext.agentSerialno
        
    #个人协议不存在，登记个人协议信息
    if ( not InsertCustInfo( ) ):
        return False
        
    return True
    
        
#------------------------------------------------------------------
#判断个人协议是否存在
#------------------------------------------------------------------
def ChkCustInfo( ):

    #AfaLoggerFunc.tradeInfo('>>>判断个人协议是否存在')

    try:
        sql = ""
        sql = "SELECT PROTOCOLNO,BUSIUSERNO,ACCNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO='AG1014' AND "                                                  #业务编号
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO    + "'" + " AND ("        #单位编号
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.SBNO         + "'" + " OR "         #商户客户编号
        sql = sql + "ACCNO="      + "'" + TradeContext.ACCNO        + "'" + " )AND "       #银行账号
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                  #状态

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询个人协议信息异常' )
    
        if ( len(records) > 0 ):
            if records[0][1]== TradeContext.SBNO:
                return ExitSubTrade( '9000', '该个人协议的社保编号已经被注册,不能再次进行注册')
            if records[0][2]== TradeContext.ACCNO: 
                return ExitSubTrade( '9000', '该个人协议的账号已经被注册,不能再次进行注册')  
            else:
                return ExitSubTrade( '9000', '该个人协议已经被注册,不能再次进行注册')    
        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断个人协议信息是否存在异常')

#------------------------------------------------------------------
#增加个人协议信息
#------------------------------------------------------------------
def InsertCustInfo( ):

    #AfaLoggerFunc.tradeInfo('>>>增加个人协议信息')

    try:

        sql = ""

        sql = "INSERT INTO ABDT_CUSTINFO("
        sql = sql + "APPNO,"
        sql = sql + "BUSINO,"
        sql = sql + "BUSIUSERNO,"
        sql = sql + "BUSIUSERAPPNO,"
        sql = sql + "BANKUSERNO,"
        sql = sql + "VOUHTYPE,"
        sql = sql + "VOUHNO,"
        sql = sql + "ACCNO,"
        sql = sql + "SUBACCNO,"
        sql = sql + "CURRTYPE,"
        sql = sql + "LIMITAMT,"
        sql = sql + "PARTFLAG,"
        sql = sql + "PROTOCOLNO,"
        sql = sql + "CONTRACTDATE,"
        sql = sql + "STARTDATE,"
        sql = sql + "ENDDATE,"
        sql = sql + "PASSCHKFLAG,"
        sql = sql + "PASSWD,"
        sql = sql + "IDCHKFLAG,"
        sql = sql + "IDTYPE,"
        sql = sql + "IDCODE,"
        sql = sql + "NAMECHKFLAG,"
        sql = sql + "USERNAME,"
        sql = sql + "TEL,"
        sql = sql + "ADDRESS,"
        sql = sql + "ZIPCODE,"
        sql = sql + "EMAIL,"
        sql = sql + "STATUS,"
        sql = sql + "ZONENO,"
        sql = sql + "BRNO,"
        sql = sql + "TELLERNO,"
        sql = sql + "INDATE,"
        sql = sql + "INTIME,"
        sql = sql + "NOTE1,"
        sql = sql + "NOTE2,"
        sql = sql + "NOTE3,"
        sql = sql + "NOTE4,"
        sql = sql + "NOTE5)"

        sql = sql + " VALUES ("

        sql = sql + "'AG1014',"                                      #业务编号
        sql = sql + "'" + TradeContext.I1BUSINO        + "',"        #单位编号
        sql = sql + "'" + TradeContext.SBNO            + "',"        #商户客户编号
        sql = sql + "'" + TradeContext.SBNO            + "',"        #商户客户应用编号
        #20120614曾照泰修改，单位客户编号不能用凭证号，批量签约的凭证号是固定的490123456789业务编号+单位编号+银行客户编号为索引不能重复
        sql = sql + "'" + TradeContext.SBNO            + "',"        #银行客户编号
        sql = sql + "'49',"                                          #凭证类型
        sql = sql + "'" + TradeContext.VOUHNO          + "',"        #凭证号
        sql = sql + "'" + TradeContext.ACCNO           + "',"        #活期存款帐号
        sql = sql + "'',"                                            #子帐号
        sql = sql + "'01',"                                          #币种
        sql = sql + "'0',"                                           #交易限额
        
        #begin 20111010--胡友--修改 部分扣款标志为改为B 表示全额扣款 扣到0余额
        sql = sql + "'B',"                                           #部分扣款标志
        #end
        
        sql = sql + "'" + TradeContext.PROTOCOLNO      + "',"        #协议编号
        sql = sql + "'" + TradeContext.WorkDate        + "',"        #签约日期(合同日期)
        sql = sql + "'" + TradeContext.WorkDate        + "',"        #生效日期
        sql = sql + "'20990101',"                                    #失效日期
        sql = sql + "'0',"                                           #密码验证标志
        sql = sql + "'" + "****************"           + "',"        #密码
        sql = sql + "'0',"                                           #证件验证标志
        sql = sql + "'01',"                                          #证件类型
        sql = sql + "'" + TradeContext.IDENTITYNO      + "',"        #证件号码
        sql = sql + "'0',"                                           #姓名验证标志
        sql = sql + "'" + TradeContext.NAME            + "',"        #客户姓名
        sql = sql + "'',"                                            #联系电话
        sql = sql + "'',"                                            #联系地址
        sql = sql + "'',"                                            #邮编
        sql = sql + "'',"                                            #电子邮箱
        sql = sql + "'1',"                                           #状态
        sql = sql + "'" + TradeContext.I1BUSINO[0:4]   + "',"        #地区号
        sql = sql + "'" + TradeContext.I1BUSINO[0:10]  + "',"        #网点号(机构代码)
        sql = sql + "'" + TradeContext.I1USID          + "',"        #柜员号
        sql = sql + "'" + TradeContext.WorkDate        + "',"        #录入日期
        sql = sql + "'" + TradeContext.WorkTime        + "',"        #录入时间
        sql = sql + "'',"                                            #备注1
        sql = sql + "'',"                                            #备注2
        sql = sql + "'',"                                            #备注3
        sql = sql + "'AHXNB',"                                       #备注4（AHXNB表示该协议是通过新农保开户时批量导入）
        sql = sql + "'')"                                            #备注5

        #AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            #AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '增加个人协议信息失败')
            
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '增加个人协议信息异常')
        
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
        #AfaLoggerFunc.tradeInfo( errorMsg )

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
               
#######################################主函数###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************批量转换格式开始********************')
    
    #读取配置文件信息
    if ( not getBatchFile( "AHXNB" ) ):
        sys.exit(-1)
    
    #转换处理
    file_Pro( )
    
    AfaLoggerFunc.tradeInfo('********************批量转换格式结束********************')
