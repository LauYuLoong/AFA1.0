# -*- coding: gbk -*-
################################################################################
#   批量业务系统：批量作业申请
#===============================================================================
#   交易文件:   T001000_8409.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  XZH
#   修改时间:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AbdtFunc
from types import *


#=====================批量作业申请==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********批量作业申请(8409)开始**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #工作日期
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #工作时间

    #判断单位协议是否有效
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False
        
    #######################################################################
    #20090927 蔡永贵 增加对公账户校验
    #----------------------------------------------------------------------
    AfaLoggerFunc.tradeInfo( '>>>校验对公账户' )
    
    if ( TradeContext.I1ACCNO != TradeContext.ACCNO ):
        return ExitSubTrade( "9000", "单位对公账户不一致，不能做此业务")
    #######################################################################

    #判断批量申请是否已存在
    if (  not ChkBatchInfo( ) ):
        return False


    #判断处理数据文件是否存在(0-柜面录入,1-外围上传)
    try:
        if ( TradeContext.I1FTPTYPE == '0' ):
            #柜面系统上传
            sFileName = os.environ['AFAP_HOME'] + '/data/batch/up_vmenu/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO
            dFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO + "_" + TradeContext.TranDate

        elif ( TradeContext.I1FTPTYPE == '1' ):
            #外围系统上传
            
            
            #20120409 陈浩修改添加--AG07
            #if ( TradeContext.I1APPNO[0:4] == 'AG08' ):
            AfaLoggerFunc.tradeInfo('>>>TradeContext.I1APPNO[0:4] =='+TradeContext.I1APPNO[0:4])
            if ( TradeContext.I1APPNO[0:4] == 'AG08' or TradeContext.I1APPNO[0:4] == 'AG07'):
                #财政特殊处理(修改人：徐忠和，修改日期：20080402)

                sCZZJDM  = ''
                sCZZJDMMC= ''
                sCZNOTE1 = ''
                sCZNOTE2 = ''

                #查询资金代码信息
                sql = "SELECT CZZJDM,ZJDMMC,NOTE1,NOTE2 FROM ABDT_CZDZB WHERE "
                sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO  + "'"        #业务编号

                AfaLoggerFunc.tradeInfo( '>>>财政特殊处理结果：' +sql)
                records = AfaDBFunc.SelectSql( sql )
                if ( records == None ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return ExitSubTrade( '9000', '查询资金代码信息异常' )

                if ( len(records) == 0 ):
                    return ExitSubTrade( '9000', '没有资金代码对照信息' )

                else:
                    sCZZJDM  = str(records[0][0]).strip()           #资金代码
                    sCZZJDMMC= str(records[0][1]).strip()           #单位名称
                    sCZNOTE1 = str(records[0][2]).strip()           #备注1
                    sCZNOTE2 = str(records[0][3]).strip()           #备注2

                #生成以资金帐号(6位)+结构代码(14位)的批量文件名
                sFileName = os.environ['AFAP_HOME'] + '/data/batch/up_other/' + sCZZJDM + TradeContext.I1BUSINO + TradeContext.I1BTHNO
            else:
                sFileName = os.environ['AFAP_HOME'] + '/data/batch/up_other/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO

            dFileName = os.environ['AFAP_HOME'] + '/data/batch/swap/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO + "_" + TradeContext.TranDate

        else:
            return ExitSubTrade( '9000', '上传方式错误' )
        
        AfaLoggerFunc.tradeInfo("上传文件是：" + sFileName)


        #源文件名
        TradeContext.S_FILENAME = sFileName
        
        #目标文件名
        TradeContext.D_FILENAME = dFileName

        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            AfaLoggerFunc.tradeInfo("批量处理数据文件存在")

            if ( TradeContext.I1FTPTYPE == '1' ):
                AfaLoggerFunc.tradeInfo("外围系统上传-->只需要登记")

            else:
                AfaLoggerFunc.tradeInfo("柜面系统上传-->需校验文件")

                #打开文件
                bfp = open(sFileName, "r")

                #读取一行
                linebuf = bfp.readline()
                while ( len(linebuf) > 0 ):
                    if ( (len(linebuf) != 100) and (len(linebuf) != 101) ):
                        bfp.close()
                        return ExitSubTrade( '9000', '批量处理数据文件格式错误' )

                    if ( linebuf[0] == "1" ):
                        AfaLoggerFunc.tradeInfo("**********汇总信息**********")
                        s_rectype    = linebuf[0:1].lstrip().rstrip()          #记录类型
                        s_appno      = linebuf[1:7].lstrip().rstrip()          #业务编号
                        s_busino     = linebuf[7:21].lstrip().rstrip()         #单位编号
                        s_agenttype  = linebuf[21:22].lstrip().rstrip()        #委托方式
                        s_accno      = linebuf[22:45].lstrip().rstrip()        #对公帐号
                        s_remark     = linebuf[45:65].lstrip().rstrip()        #备用
                        s_status     = linebuf[65:66].lstrip().rstrip()        #状态
                        s_totalnum   = linebuf[66:76].lstrip().rstrip()        #总笔数
                        s_totalamt   = linebuf[76:93].lstrip().rstrip()        #总金额
                        s_retcode    = linebuf[93:100].lstrip().rstrip()       #返回码

                        AfaLoggerFunc.tradeInfo("记录类型 =" + s_rectype)
                        AfaLoggerFunc.tradeInfo("业务编号 =" + s_appno)
                        AfaLoggerFunc.tradeInfo("单位编号 =" + s_busino)
                        AfaLoggerFunc.tradeInfo("委托方式 =" + s_agenttype)
                        AfaLoggerFunc.tradeInfo("对公帐号 =" + s_accno)
                        AfaLoggerFunc.tradeInfo("备    用 =" + s_remark)
                        AfaLoggerFunc.tradeInfo("状    态 =" + s_status)
                        AfaLoggerFunc.tradeInfo("总 笔 数 =" + s_totalnum)
                        AfaLoggerFunc.tradeInfo("总 金 额 =" + s_totalamt)
                        AfaLoggerFunc.tradeInfo("返 回 码 =" + s_retcode)
                        AfaLoggerFunc.tradeInfo("**********汇总信息**********")

                        break

                    linebuf = bfp.readline()

                #关闭文件
                bfp.close()

                #状态(0:忽略 1:正常)
                if ( s_status == "0" ):
                    return ExitSubTrade('9000', '您申请数据文件中汇总记录状态错误,不能申请')


                #校验业务编码
                if ( TradeContext.I1APPNO != s_appno ):
                    return ExitSubTrade('9000', '您申请的业务编码与数据文件的业务编码不符,不能申请')


                #校验单位编码
                if ( TradeContext.I1BUSINO != s_busino ):
                    return ExitSubTrade('9000', '您申请的单位编码与数据文件的单位编码不符,不能申请')


                #校验对公帐号
                if ( TradeContext.ACCNO != s_accno ):
                    return ExitSubTrade('9000', '批量处理数据文件中的对公帐号和单位信息表中登记不符')


                #校验委托方式是否一致
                if ( TradeContext.AGENTTYPE != s_agenttype ):
                    return ExitSubTrade('9000', '批量处理数据文件中的委托方式和单位信息表中登记不符')


                #校验委托方式合法性
                if ( (s_agenttype!='3') and (s_agenttype!='4') ):
                    return ExitSubTrade('9000', '批量处理数据文件中的委托方式非法')


                #校验总笔数
                if ( TradeContext.I1TOTALNUM != s_totalnum ):
                    return ExitSubTrade('9000', '您申请的批量总笔数与数据文件的总笔数不符,不能申请')


                #校验总金额
                if ( TradeContext.I1TOTALAMT != s_totalamt ):
                    return ExitSubTrade('9000', '您申请的批量总金额与数据文件的总金额不符,不能申请')

        else:
            AfaLoggerFunc.tradeInfo("上传文件名 =" + sFileName)
            return ExitSubTrade('9000', '批量处理数据文件没有上传,请重试')


    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade('9999', '批量处理数据文件操作异常')


    ###############################################################################
    #20090927 蔡永贵 读取配置文件的信息，判断业务处理类型（0-即时处理，1-日终处理）
    #-----------------------------------------------------------------------------
    batchCfg = AbdtFunc.getBatchConfig( )
    
    #拆分出各种业务类型
    APPTRFG = TradeContext.BATCH_APPTRFG.split( '|' )
    
    #判断是日终处理还是即时处理
    if ( TradeContext.I1APPNO[0:6] in APPTRFG and int( TradeContext.I1TOTALNUM ) <= int( TradeContext.BATCH_MAXCOUNT ) ):
        TradeContext.I1TRFG = '0'    #即时处理
        
        AfaLoggerFunc.tradeInfo( '>>>做即时处理' )
        
    else:
        TradeContext.I1TRFG = '1'    #日终处理
        
        AfaLoggerFunc.tradeInfo( '>>>做日终处理' )
        
    ################################################################################
    
    #生成委托号
    if ( not CrtBatchNo( ) ):
        return False


    try:
        #把文件移到批量内部操作目录中(in)
        cp_cmd_str="mv " + sFileName + " " + dFileName
        os.system(cp_cmd_str)
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade('9999', '批量数据文件转移操作异常')


    #登记申请信息
    if ( not InsertBatchInfo( ) ):
        return False

    TradeContext.tradeResponse.append(['O1BATCHNO', TradeContext.BATCHNO])        #委托号
    TradeContext.tradeResponse.append(['O1ACCNO',   TradeContext.ACCNO])          #对公账户
    TradeContext.tradeResponse.append(['O1VOUHNO',  TradeContext.VOUHNO])         #凭证号(内部账户)


    AfaLoggerFunc.tradeInfo('**********批量作业申请(8409)结束**********')


    #返回
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '交易成功'])
    return True




#判断批量申请是否已存在
def ChkBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>判断批量申请是否已存在')

    try:
        sql = "SELECT BATCHNO,STATUS FROM ABDT_BATCHINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO    + "'" + " AND "        #业务编号
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO   + "'" + " AND "        #单位编号
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO   + "'" + " AND "        #地区代码
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO     + "'" + " AND "        #机构代码
        sql = sql + "INDATE="   + "'" + TradeContext.TranDate   + "'" + " AND "        #委托日期
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



#生成委托号
def CrtBatchNo( ):

    AfaLoggerFunc.tradeInfo('>>>生成批次委托号')

    try:
        sqlStr = "SELECT NEXTVAL FOR ABDT_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '生成委托号异常' )

        #批次号
        TradeContext.BATCHNO = TradeContext.TranDate + str(records[0][0]).rjust(8, '0')

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '生成委托号异常' )



#登记批次作业申请信息
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
        sql = sql + "'" + TradeContext.I1ZONENO         + "',"                              #地区号
        sql = sql + "'" + TradeContext.I1SBNO           + "',"                              #网点号
        sql = sql + "'" + TradeContext.I1USID           + "',"                              #操作员
        sql = sql + "'" + TradeContext.I1ADMINNO        + "',"                              #管理员
        sql = sql + "'" + TradeContext.I1FTPTYPE        + "',"                              #终端类型
        sql = sql + "'" + TradeContext.I1FILENAME       + "',"                              #批量文件
        sql = sql + "'" + TradeContext.TranDate         + "',"                              #申请时间
        sql = sql + "'" + TradeContext.TranTime         + "',"                              #申请时间
        sql = sql + "'" + "00000000"                    + "',"                              #提交日期
        sql = sql + "'" + "000000"                      + "',"                              #提交时间
        sql = sql + "'" + TradeContext.I1TOTALNUM       + "',"                              #总笔数
        sql = sql + "'" + TradeContext.I1TOTALAMT       + "',"                              #总金额
        sql = sql + "'" + "0"                           + "',"                              #成功笔数
        sql = sql + "'" + "0"                           + "',"                              #成功金额
        sql = sql + "'" + "0"                           + "',"                              #失败笔数
        sql = sql + "'" + "0"                           + "',"                              #失败金额
        sql = sql + "'" + "10"                          + "',"                              #状态(申请)
        sql = sql + "'" + TradeContext.I1NOTE1          + "',"                              #生效日期
        sql = sql + "'" + TradeContext.I1NOTE2          + "',"                              #失效日期
        sql = sql + "'" + TradeContext.I1NOTE5          + "',"                              #处理信息
        sql = sql + "'" + ""                            + "',"                              #备注1
        
        #begin 20091028 蔡永贵修改 增加批次序号，存放到备注2中
        sql = sql + "'" + TradeContext.I1BTHNO          + "',"                              #备注2
        #end
        
        #begin 20090927 蔡永贵修改 增加处理标志，存放到备注3中
        #sql = sql + "'" + TradeContext.I1NOTE3         + "',"                              #备注3
        sql = sql + "'" + TradeContext.I1TRFG           + "',"                              #备注3
        #end
        
        sql = sql + "'" + TradeContext.I1NOTE4          + "',"                              #备注4
        sql = sql + "'" + ""                            + "')"                              #备注5

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )

            #删除文件
            rm_cmd_str="rm " + TradeContext.D_FILENAME
            os.system(rm_cmd_str)

            return ExitSubTrade( '9000', '登记批次作业申请信息失败')
        
        return True

    except Exception, e:
        #删除文件
        rm_cmd_str="rm " + TradeContext.D_FILENAME
        os.system(rm_cmd_str)

        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '登记批次作业申请信息异常')


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
