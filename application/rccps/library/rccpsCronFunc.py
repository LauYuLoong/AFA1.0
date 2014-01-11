# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ.ϵͳ���Ȳ���ģ��
#===============================================================================
#   �����ļ�:   rccpsCronFunc.py
#   ��    ��:   �ر��
#   �޸�ʱ��:   2008-06-14
################################################################################

import AfaLoggerFunc,AfaDBFunc,TradeContext, LoggerHandler, sys, os, time, AfaUtilTools, ConfigParser
from types import *

cronLogger = LoggerHandler.getLogger( 'cron' )

#��ȡ���������ļ�����Ϣ
def GetCronConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.CRON_TRACE   = config.get('CRON', 'TRACE')
        TradeContext.CRON_CYCTIME = config.get('CRON', 'CYCTIME')

        #print ':::CRON_TRACE   =' + TradeContext.CRON_TRACE
        #print ':::CRON_CYCTIME =' + TradeContext.CRON_CYCTIME

        return True

    except Exception, e:
        print '��ȡ�����ļ��쳣:' + str(e)
        return False

#д��־
def WrtLog(logstr):

    if ( TradeContext.existVariable('CRON_TRACE') ):
        
        if ( TradeContext.CRON_TRACE   == 'off' ):
            #�������־
            return True

        elif ( TradeContext.CRON_TRACE == 'file' ):
            #���ļ����
            cronLogger.info(logstr)

        elif ( TradeContext.CRON_TRACE == 'all' ):
            #���ļ�����Ļͬʱ���
            cronLogger.info(logstr)
            print logstr

        elif ( TradeContext.CRON_TRACE == 'stdout' ):
            #����Ļ���
            print logstr

    else:
        #Ĭ�����ļ�����Ļͬʱ���
        cronLogger.info(logstr)
        print logstr

    return True


#��ϵͳ����
def openCron(taskid):
    #======================��ѯϵͳ������Ϣ================================
    sql = "SELECT * FROM AFA_CRONADM WHERE TASKID = '" + taskid + "'"
    
    records = AfaDBFunc.SelectSql(sql)
    
    if records == None:
        rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog("��ȡϵͳ����[" + taskid + "]��Ϣ�쳣")
        return False
    
    if len(records) <= 0:
        WrtLog("ϵͳ���ȱ����޴˵�����Ϣ[" + taskid + "]")
        return False
    
    #======================�޸�ϵͳ����״̬Ϊ0=============================
    sql = "UPDATE AFA_CRONADM SET STATUS = '1' WHERE TASKID = '" + taskid + "'"
    
    if not AfaDBFunc.UpdateSql(sql):
        rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog("��ϵͳ����[" + taskid + "]�쳣")
        return False
        
    WrtLog("��ϵͳ����[" + taskid + "]�ɹ�")
    return True
    
#�ر�ϵͳ����
def closeCron(taskid):
    #======================��ѯϵͳ������Ϣ================================
    sql = "SELECT * FROM AFA_CRONADM WHERE TASKID = '" + taskid + "'"
    
    records = AfaDBFunc.SelectSql(sql)
    
    if records == None:
        rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog("��ȡϵͳ����[" + taskid + "]��Ϣ�쳣")
        return False
    
    if len(records) <= 0:
        WrtLog("ϵͳ���ȱ����޴˵�����Ϣ[" + taskid + "]")
        return False
    
    #======================�޸�ϵͳ����״̬Ϊ0=============================
    sql = "UPDATE AFA_CRONADM SET STATUS = '0' WHERE TASKID = '" + taskid + "'"
    
    if not AfaDBFunc.UpdateSql(sql):
        rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
        WrtLog("�ر�ϵͳ����[" + taskid + "]�쳣")
        return False
        
    WrtLog("�ر�ϵͳ����[" + taskid + "]�ɹ�")
    return True
    
#�˳�ϵͳ��������
def cronExit(code,msg):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    raise Exception,msg
    

#��ʽ���ļ�
def FormatFile(ProcType, FLDName, sFileName, dFileName):

#    WrtLog('>>>��ʽ���ļ�:' + ProcType + ' ' + sFileName + ' ' + dFileName)

    try:

        srcFileName    = os.environ['AFAP_HOME'] + '/data/rccps/host/' + sFileName
        dstFileName    = os.environ['AFAP_HOME'] + '/data/rccps/host/' + dFileName

        if (ProcType == "1"):
            #ascii->ebcd
            #���ø�ʽ:cvt2ebcdic -T Դ�ı��ļ� -P Ŀ�������ļ� -F fld��ʽ�ļ� [-D ����� ]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/rccps/cvt/cvt2ebcdic'
            #�ر��  20081126  ����������fld�ļ�
            #fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/rccps01.fld'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/' + FLDName
            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName + " -D '|' "

        else:
            #ebcd->ascii
            #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D ���-��] [-S] [-R]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/rccps/cvt/cvt2ascii'
            #�ر��  20081126  ����������fld�ļ�
            #fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/rccps02.fld'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/' + FLDName
            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName + " -D '|' "

        #WrtLog('>>>' + cmdstr)
        #ret = -1
        WrtLog('>>>�����ʽת������ʼ============')   #2007824
        WrtLog(cmdstr)
        ret = os.system(cmdstr)                         #2007824
        if ( ret != 0 ):                                #2007824
            ret = False                                 #2007824
        else:                                           #2007824
            ret = True                                  #2007824
        #return 0                                       #2007824
        WrtLog('>>>�����ʽת���������============')   #2007824

        return ret
        
    except Exception, e:
        WrtLog(e)
        WrtLog('��ʽ���ļ��쳣')
        return False
