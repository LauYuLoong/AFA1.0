# -*- coding: gbk -*-
############################################################################
#            中间业务平台交易前后处理函数，便于增加监控及统计信息
#===========================================================================
#                    作  者：    陈  显  明
#                    时  间：    20070921
############################################################################
import os, socket, time

#    登记AFA所在机器地址、业务处理进程ID及交易开始时间信息的全局变量，可以作为对应数据库表中的关键字便于搜索交易记录
gHostAddress, gServicePid, gExecuteBeginTime = '', 0, 0

#    仅用以测试的模拟客户端请求数据生成
def analyzeRequest():
    import TradeContext
    TradeContext.TemplateCode = 'TemplateCode'
    TradeContext.TransCode = 'TransCode'
    TradeContext.ReservedCode = 'ReservedCode'

#    仅用以测试的模拟执行交易函数
def executeTrade():
    time.sleep(1)



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#    执行插入及修改数据库语句，记录交易运行信息到数据库指定表中
def executeStaticsLogSql(sqlStr):
    #    TODO:    增加对数据库连接异常（如重启数据库服务端）情况的处理（需要重新获取数据库连接）
    #print sqlStr
    import Db2Connection
    conn = Db2Connection.getConnection()
#    import OracleConnection
#    conn = OracleConnection.getConnection()
    curs = None
    try:
        curs = conn.cursor()
        curs.execute(sqlStr)
        curs.execute("commit")
        curs.close()
    except:
        if(curs != None): curs.close()
        import LoggerHandler
        logger = LoggerHandler.getLogger('service')
        logger.error(sqlStr)

#    处理交易的service进程ID，第一次载入模块时初始化，可以记录到数据库
def setServicePid():
    #    TODO:    重启平台时记录进程开始运行时间信息到数据库中
    global gHostAddress, gServicePid
    gHostAddress, gServicePid = '', os.getpid()
    ipaddrlist = socket.gethostbyaddr(socket.gethostname())[2]
    for addr in ipaddrlist:
        gHostAddress = gHostAddress + '[' +  addr + ']'

#    交易前处理（平台维护人员可以修改以定制其行为，一般情况下建议不修改，否则可能带来交易运行错误）
def preTradeProcess():
    global gExecuteBeginTime
    import TradeContext
    gExecuteBeginTime = time.time()
    timeToFormat = time.localtime(gExecuteBeginTime)
    #print time.strftime ("%Y-%m-%d", timeToFormat), time.strftime ("%H:%M:%S", timeToFormat)
    sqlStatement = "insert into AFA_CORE_TRDSTAT(HOSTADDRESS,SERVICEPID,PROCESSNUM,TEMPLATECODE,TRANSCODE,RESERVEDCODE,BEGINDATE,BEGINTIME,BACKUPFLAG) values('%s','%d','%.4f','%s','%s','%s','%s','%s','000')" \
          %(gHostAddress, gServicePid, gExecuteBeginTime, TradeContext.TemplateCode, TradeContext.TransCode, TradeContext.ReservedCode, time.strftime ("%Y-%m-%d", timeToFormat), time.strftime ("%H:%M:%S", timeToFormat))
    executeStaticsLogSql(sqlStatement)

#    交易后处理（平台维护人员可以修改以定制其行为，一般情况下建议不修改，否则可能带来交易运行错误）
def postTradeProcess():
    executeEndTime = time.time()
    actualExecuteTime = executeEndTime - gExecuteBeginTime
    timeToFormat = time.localtime(executeEndTime)
    #print "进程号：%d\t执行时间：%.4f\t开始时间: %.4f\t结束时间: %.4f"%(gServicePid, actualExecuteTime, gExecuteBeginTime, executeEndTime)
    sqlStatement = "update AFA_CORE_TRDSTAT set PROCESSNUM2='%.4f',ENDDATE='%s',ENDTIME='%s',TIMESPAN='%.4f',BACKUPFLAG='100' where HOSTADDRESS='%s' and SERVICEPID='%d' and PROCESSNUM='%.4f'" \
        %(executeEndTime, time.strftime ("%Y-%m-%d", timeToFormat), time.strftime ("%H:%M:%S", timeToFormat), actualExecuteTime, gHostAddress, gServicePid, gExecuteBeginTime)
    executeStaticsLogSql(sqlStatement)
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------



if(__name__ == "__main__"):
    import PythonPathSetter
    analyzeRequest()
    setServicePid()
    preTradeProcess()
    executeTrade()
    postTradeProcess()
