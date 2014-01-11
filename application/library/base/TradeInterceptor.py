# -*- coding: gbk -*-
############################################################################
#            �м�ҵ��ƽ̨����ǰ���������������Ӽ�ؼ�ͳ����Ϣ
#===========================================================================
#                    ��  �ߣ�    ��  ��  ��
#                    ʱ  �䣺    20070921
############################################################################
import os, socket, time

#    �Ǽ�AFA���ڻ�����ַ��ҵ�������ID�����׿�ʼʱ����Ϣ��ȫ�ֱ�����������Ϊ��Ӧ���ݿ���еĹؼ��ֱ����������׼�¼
gHostAddress, gServicePid, gExecuteBeginTime = '', 0, 0

#    �����Բ��Ե�ģ��ͻ���������������
def analyzeRequest():
    import TradeContext
    TradeContext.TemplateCode = 'TemplateCode'
    TradeContext.TransCode = 'TransCode'
    TradeContext.ReservedCode = 'ReservedCode'

#    �����Բ��Ե�ģ��ִ�н��׺���
def executeTrade():
    time.sleep(1)



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#    ִ�в��뼰�޸����ݿ���䣬��¼����������Ϣ�����ݿ�ָ������
def executeStaticsLogSql(sqlStr):
    #    TODO:    ���Ӷ����ݿ������쳣�����������ݿ����ˣ�����Ĵ�����Ҫ���»�ȡ���ݿ����ӣ�
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

#    �����׵�service����ID����һ������ģ��ʱ��ʼ�������Լ�¼�����ݿ�
def setServicePid():
    #    TODO:    ����ƽ̨ʱ��¼���̿�ʼ����ʱ����Ϣ�����ݿ���
    global gHostAddress, gServicePid
    gHostAddress, gServicePid = '', os.getpid()
    ipaddrlist = socket.gethostbyaddr(socket.gethostname())[2]
    for addr in ipaddrlist:
        gHostAddress = gHostAddress + '[' +  addr + ']'

#    ����ǰ����ƽ̨ά����Ա�����޸��Զ�������Ϊ��һ������½��鲻�޸ģ�������ܴ����������д���
def preTradeProcess():
    global gExecuteBeginTime
    import TradeContext
    gExecuteBeginTime = time.time()
    timeToFormat = time.localtime(gExecuteBeginTime)
    #print time.strftime ("%Y-%m-%d", timeToFormat), time.strftime ("%H:%M:%S", timeToFormat)
    sqlStatement = "insert into AFA_CORE_TRDSTAT(HOSTADDRESS,SERVICEPID,PROCESSNUM,TEMPLATECODE,TRANSCODE,RESERVEDCODE,BEGINDATE,BEGINTIME,BACKUPFLAG) values('%s','%d','%.4f','%s','%s','%s','%s','%s','000')" \
          %(gHostAddress, gServicePid, gExecuteBeginTime, TradeContext.TemplateCode, TradeContext.TransCode, TradeContext.ReservedCode, time.strftime ("%Y-%m-%d", timeToFormat), time.strftime ("%H:%M:%S", timeToFormat))
    executeStaticsLogSql(sqlStatement)

#    ���׺���ƽ̨ά����Ա�����޸��Զ�������Ϊ��һ������½��鲻�޸ģ�������ܴ����������д���
def postTradeProcess():
    executeEndTime = time.time()
    actualExecuteTime = executeEndTime - gExecuteBeginTime
    timeToFormat = time.localtime(executeEndTime)
    #print "���̺ţ�%d\tִ��ʱ�䣺%.4f\t��ʼʱ��: %.4f\t����ʱ��: %.4f"%(gServicePid, actualExecuteTime, gExecuteBeginTime, executeEndTime)
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
