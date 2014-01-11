# -*- coding: gbk -*-
###############################################################################
# 文件名称：AbdtQyIn.py
# 文件标识：
# 作    者：陈浩  
# 修改时间：2011-07-27
# 摘    要：批量签约 定时调度 导入
#
###############################################################################   
 
import TradeContext                
                                   
TradeContext.sysType = 'abdt' 
                                   
import time ,TradeContext ,AfaDBFunc,os,sys,TradeContext,AfaUtilTools,AbdtManager,AfaLoggerFunc,AfaFlowControl,AfaAdminFunc,sys,AfaFunc
from types import *

def AbdtQyIn():

    AfaLoggerFunc.tradeInfo('**********批量签约定时调度 进入**********')
                 
    try: 
     
        AfaLoggerFunc.tradeInfo('>>>判断批量文件是否存在')    
        sql = ""       
        sql = "SELECT FILENAME,APPNO,BUSINO,WORKDATE,TELLERNO FROM AHNX_FILE WHERE "
        sql = sql + "FILETYPE="    + "'7'" + " AND "        #7-批量签约
        sql = sql + "STATUS="   + "'0'"                     #未处理
       
        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql(sql)
        if records == None:
            return ExitSubTrade("E9999" ,"查询AHNX_FILE数据库异常")
             
        elif(len(records)==0):
            return ExitSubTrade("E9999" ,"数据库AHNX_FILE中没有要读取的文件！")
            
        else:            
            for i in range(0,len(records)):
                TradeContext.prefileName = records[i][0]
                TradeContext.sysId       = records[i][1]
                TradeContext.busiNo      = records[i][2]  
                TradeContext.workDate    = records[i][3]
                TradeContext.tellerno    = records[i][4]
              
                FileName = '/home/maps/afa/data/batch/batch_qy/' + TradeContext.prefileName
                               
                if (os.path.exists(FileName)): 
                    AfaLoggerFunc.tradeInfo( '>>>批文件名 fileName ：' + TradeContext.prefileName ) 
                                                                        
                    AfaLoggerFunc.tradeInfo('**********导入批量文件**********')                                                             
                    sfp = open(FileName,'r')            
                    AfaLoggerFunc.tradeInfo("读取批量文件:" + FileName)
                                    
                    #生成创建导出错误文件
                    serrorFile = '/home/maps/afa/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + TradeContext.prefileName[-7:-4] + "_WF.TXT"           
                    #errorFile = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + "_WF.TXT"
                    AfaLoggerFunc.tradeInfo('errorFile文件名=' + serrorFile)
                    if os.path.exists(serrorFile):
                        os.system("rm -f " + serrorFile)
                        
                        
                    errorFile = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + TradeContext.prefileName[-7:-4]+ "_WF.TXT"    
                    
                               
                    #读取一行 读取的文件格式为：学生学号|身份证|姓名|存折号或卡号|凭证号|
                    linebuff = sfp.readline( )            
                    lineCount = 0            
                    while( len(linebuff)>0 ):
                        swapbuff = linebuff.split("|")              
                        
                        if len(swapbuff) != 6:
                            TradeContext.errorCode, TradeContext.errorMsg='E7777', "第[" + str(lineCount+1) + "]行数据格式不合法,该行数据有" + str(len(swapbuff)) + "列"                        
                            AfaLoggerFunc.tradeInfo("第" + str(lineCount+1) + "行数据格式不合法,该行数据有" + str(len(swapbuff)) + "列")   
                            
                            #记录签约失败 信息
                            FalseMsg( )
                                
                                            
                            linebuff = sfp.readline( )
                            lineCount = lineCount + 1
                            continue
                            
                        TradeContext.USERNO      = swapbuff[0].lstrip().rstrip()          #学生学号
                        if len(TradeContext.USERNO) != 9:
                            TradeContext.errorCode, TradeContext.errorMsg='E7777', "第[" + str(lineCount+1) + "]行数据格式不合法,学生学号位数不正确！"                        
                            AfaLoggerFunc.tradeInfo("第" + str(lineCount+1) + "行数据格式不合法,学生学号位数不正确！")
                            
                            #记录签约失败 信息
                            FalseMsg( ) 
                            
                            linebuff = sfp.readline( )
                            lineCount = lineCount + 1
                            continue  
                        
                        TradeContext.IDENTITYNO  = swapbuff[1].lstrip().rstrip()          #身份证
                        if ((len(TradeContext.IDENTITYNO) != 18) and (len(TradeContext.IDENTITYNO) != 15) ):
                            TradeContext.errorCode, TradeContext.errorMsg='E7777', "第[" + str(lineCount+1) + "]行数据格式不合法,身份证位数不正确！"                        
                            AfaLoggerFunc.tradeInfo("第" + str(lineCount+1) + "行数据格式不合法,身份证位数不正确！")
                            
                            #记录签约失败 信息
                            FalseMsg( )  
                            
                            linebuff = sfp.readline( )
                            lineCount = lineCount + 1
                            continue 
                        
                        TradeContext.USERNAME    = swapbuff[2].lstrip().rstrip()          #姓名(持卡人姓名)
                                                                            
                        if ((len(swapbuff[3].lstrip().rstrip()) != 23) and (len(swapbuff[3].lstrip().rstrip()) != 19)):
                             TradeContext.errorCode, TradeContext.errorMsg='E7777', "第[" + str(lineCount+1) + "]行数据格式不合法,帐号或卡号位数不正确！"                        
                             AfaLoggerFunc.tradeInfo("第" + str(lineCount+1) + "行数据格式不合法,帐号或卡号位数不正确！")  
                             
                             #记录签约失败 信息
                             FalseMsg( )  
                            
                             linebuff = sfp.readline( )
                             lineCount = lineCount + 1
                             continue    
                            
                        
                        if len(swapbuff[3].lstrip().rstrip()) == 23:                      #折为23位
                            #折                                                         
                            TradeContext.ACCNO     = swapbuff[3].lstrip().rstrip()
                            TradeContext.VOUHNO    = swapbuff[4].lstrip().rstrip()        #凭证号
                            TradeContext.VOUHTYPE  = '49'                                 #凭证种类
                                                                                                                                                    
                        if len(swapbuff[3].lstrip().rstrip()) == 19:                      #卡为19位
                            #卡                                                        
                            TradeContext.ACCNO     = swapbuff[3].lstrip().rstrip()
                            TradeContext.VOUHNO    = TradeContext.ACCNO[8:18]             #凭证号
                            TradeContext.VOUHTYPE  = TradeContext.ACCNO[6:8]              #凭证种类
                            
                        if ( not CrtCustInfo( ) ):
                        
                            #记录签约失败 信息
                            FalseMsg( )
                                
                                
                            linebuff = sfp.readline( )
                            lineCount = lineCount + 1
                            continue
                            
                        lineCount = lineCount + 1
                        linebuff = sfp.readline( )
                        continue            
                     
                        mfp.close( )     
                        sfp.close( )
                    
                    #更新 AHNX_FILE 中的 STATUS = 1
                    sql = ""
                    sql = " update AHNX_FILE set"
                    sql = sql + " STATUS   = '1',"  
                    sql = sql + " PROCMSG  = '批量处理已完成，可以下载回盘文件'"
                    sql = sql + " where filename = '" + records[i][0] + "'" 
                    AfaLoggerFunc.tradeInfo('查询结果 sql: ' +sql)
                    
                    if AfaDBFunc.UpdateSqlCmt( sql ) == -1:
                        TradeContext.errorCode,TradeContext.errorMsg = "E9999","更新 AHNX_FILE 数据库 STATUS 失败!"
                        raise AfaFlowControl.flowException( )                                                           
                    
                else:
                    TradeContext.errorCode,TradeContext.errorMsg = "E9999","批量文件不存在!"
                    continue 
                                    
            AfaLoggerFunc.tradeInfo('**********批量签约定时调度 退出**********' )       
            
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
    
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
    TradeContext.PROTOCOLNO = TradeContext.workDate + TradeContext.agentSerialno
        
    #个人协议不存在，登记个人协议信息
    if ( not InsertCustInfo( ) ):
        return False
        
    return True
    
        
#------------------------------------------------------------------
#判断个人协议是否存在
#------------------------------------------------------------------
def ChkCustInfo( ):

    AfaLoggerFunc.tradeInfo('>>>判断个人协议是否存在')

    try:
        sql = ""
        sql = "SELECT PROTOCOLNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.sysId        + "'" + " AND "        #业务编号
        sql = sql + "BUSINO="     + "'" + TradeContext.busiNo       + "'" + " AND ("       #单位编号
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.USERNO       + "'" + " OR "         #商户客户编号
        sql = sql + "ACCNO="      + "'" + TradeContext.ACCNO        + "'" + " )AND "       #银行账号
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                  #状态

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询个人协议信息异常' )
    
        if ( len(records) > 0 ):
            return ExitSubTrade( '9000', '学号' +TradeContext.USERNO+ '该个人协议已经被注册,不能再次进行注册')

        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断个人协议信息是否存在异常')

#------------------------------------------------------------------
#增加个人协议信息
#------------------------------------------------------------------
def InsertCustInfo( ):

    AfaLoggerFunc.tradeInfo('>>>增加个人协议信息')

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

        sql = sql + "'" + TradeContext.sysId           + "',"        #业务编号
        sql = sql + "'" + TradeContext.busiNo          + "',"        #单位编号
        sql = sql + "'" + TradeContext.USERNO          + "',"        #商户客户编号
        sql = sql + "'" + TradeContext.USERNO          + "',"        #商户客户应用编号
        sql = sql + "'" + TradeContext.VOUHNO          + "',"        #银行客户编号（前台提供的开户文件中没有此项，使用凭证号代替）
        sql = sql + "'" + TradeContext.VOUHTYPE        + "',"        #凭证类型
        sql = sql + "'" + TradeContext.VOUHNO          + "',"        #凭证号
        sql = sql + "'" + TradeContext.ACCNO           + "',"        #活期存款帐号
        sql = sql + "'',"                                            #子帐号
        sql = sql + "'01',"                                          #币种
        sql = sql + "'0',"                                           #交易限额
        sql = sql + "'A',"                                           #部分扣款标志  改为A 表示全额扣款 扣到1余额
        sql = sql + "'" + TradeContext.PROTOCOLNO      + "',"        #协议编号
        sql = sql + "'" + TradeContext.workDate        + "',"        #签约日期(合同日期)
        sql = sql + "'" + TradeContext.workDate        + "',"        #生效日期
        sql = sql + "'20990101',"                                    #失效日期
        sql = sql + "'0',"                                           #密码验证标志
        sql = sql + "'" + "****************"           + "',"        #密码
        sql = sql + "'0',"                                           #证件验证标志
        sql = sql + "'01',"                                          #证件类型
        sql = sql + "'" + TradeContext.IDENTITYNO      + "',"        #证件号码
        sql = sql + "'0',"                                           #姓名验证标志
        sql = sql + "'" + TradeContext.USERNAME        + "',"        #客户姓名
        sql = sql + "'',"                                            #联系电话
        sql = sql + "'',"                                            #联系地址
        sql = sql + "'',"                                            #邮编
        sql = sql + "'',"                                            #电子邮箱
        sql = sql + "'1',"                                           #状态
        sql = sql + "'" + TradeContext.busiNo[0:4]     + "',"        #地区号
        sql = sql + "'" + TradeContext.busiNo[0:10]    + "',"        #网点号(机构代码)
        sql = sql + "'" + TradeContext.tellerno        + "',"        #柜员号
        sql = sql + "'" + TradeContext.workDate        + "',"        #录入日期
        sql = sql + "'" + TradeContext.workTime        + "',"        #录入时间
        sql = sql + "'',"                                            #备注1
        sql = sql + "'',"                                            #备注2
        sql = sql + "'',"                                            #备注3
        sql = sql + "'',"                                            #备注4
        sql = sql + "'')"                                            #备注5

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '学号为' +TradeContext.USERNO+ '增加个人协议信息插入失败')
            
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '增加个人协议信息异常')
        
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
#导出签约失败 客户信息
#------------------------------------------------------------------
def FalseMsg():

    AfaLoggerFunc.tradeInfo('>>>存放导入错误信息...') 
    
    try:
        
        errorFile = '/home/maps/afa/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + TradeContext.prefileName[-7:-4]+ "_WF.TXT"
        
        mfp = open( errorFile, 'a' ) 
        AfaLoggerFunc.tradeInfo("错误信息的文件为："  + errorFile) 
        TradeContext.errorFile = TradeContext.errorMsg                                                           
        mfp = open( errorFile, 'a' )                
        mfp.write( TradeContext.errorFile + "\n")
        mfp.close()  
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )                                  
      
              
#######################################主函数###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('***************批量签约定时调度开始********************')
    
    TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
    if ( len(sys.argv) in (1,2)):
    
        if ( len(sys.argv) == 1 ):
            sTrxDate = AfaUtilTools.GetSysDate( ) 
        else:
            sTrxDate = sys.argv[1]         #定时调度日期
            
        AbdtQyIn()
        
    else:
        print( '用法1: jtfk_Proc sysid1  date')
        sys.exit(-1)    
    
    AfaLoggerFunc.tradeInfo('****************批量签约定时调度结束********************')
            
     