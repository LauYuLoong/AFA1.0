# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�BatchDeamon.py
# �ļ���ʶ��
# ժ    Ҫ�����������ػ�����
#
# ��ǰ�汾��1.0
# ��    �ߣ�XZH
# ������ڣ�2006��9��8��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import time,AfaDBFunc,TradeContext,os,AfaUtilTools,AbdtManager,HostContext,HostComm
from types import *


#=========================�ж������ļ��Ƿ����==================================
def delDataFile(fname):
    if ( os.path.exists(fname) and os.path.isfile(fname) ):
        AbdtManager.WrtLog('ɾ���ļ�:[' + fname + ']')
        cmdstr = "rm " + fname
        os.system(cmdstr)
        return 0
    else:
        return -1




#=========================��ȡƫ������������====================================
def getTimeFromNow( offsetDays, format = "%Y%m%d" ):
    secs = time.time( ) + offsetDays * 3600 * 24
    return time.strftime( format, time.localtime( secs ) )
    
    
    
    
#=========================ɾ�������ļ�==========================================
def DelHostFile(curBatchNo, HostFileName, Flag):

    AbdtManager.WrtLog('ɾ�������ļ�:[' + HostFileName + ']')

    try:
        HostBatchNo  = curBatchNo[4:16]

        #ͨѶ�����
        HostContext.I1TRCD = '8819'                     #������
        HostContext.I1SBNO = TradeContext.BRNO          #���׻�����
        HostContext.I1USID = '999986'                   #���׹�Ա��
        HostContext.I1AUUS = ""                         #��Ȩ��Ա
        HostContext.I1AUPS = ""                         #��Ȩ��Ա����
        HostContext.I1WSNO = ""                         #�ն˺�
        HostContext.I1NBBH = TradeContext.APPNO         #����ҵ���ʶ
        HostContext.I1CLDT = TradeContext.BATCHDATE     #ԭ��������
        HostContext.I1UNSQ = HostBatchNo                #ԭ����ί�к�
        HostContext.I1FILE = HostFileName               #ɾ���ļ���
        HostContext.I1OPFG = Flag                       #������־(0-��ѯ 1-ɾ���ϴ��ļ� 2-ɾ���´��ļ�)

        HostTradeCode = "8819".ljust(10,' ')
        HostComm.callHostTrade( os.environ['AFAP_HOME'] + '/conf/hostconf/AH8819.map', HostTradeCode, "0002" )
        if( HostContext.host_Error ):
            AbdtManager.WrtLog('>>>������=[' + str(HostContext.host_ErrorType) + ']:' +  HostContext.host_ErrorMsg)
            return -1

        if ( HostContext.O1MGID == "AAAAAAA" ):
            AbdtManager.WrtLog('>>>������=[' + HostContext.O1MGID + ']���׳ɹ�')

        else:
            AbdtManager.WrtLog('>>>������=[' + HostContext.O1MGID + ']' + HostContext.O1INFO)

        #ɾ���������е�����
        sql = ""
        sql = sql + "UPDATE ABDT_BATCHINFO SET STATUS='**' WHERE "
        sql = sql + "APPNO='"   + TradeContext.APPNO     + "'" + " AND "
        sql = sql + "BUSINO='"  + TradeContext.BUSINO    + "'" + " AND "
        sql = sql + "BATCHNO='" + TradeContext.BATCHNO   + "'"

        retcode = AfaDBFunc.UpdateSqlCmt( sql )
        if (retcode==None or retcode <= 0):
            return -1
        else:
            return 0

    except Exception, e:
        AbdtManager.WrtLog( str(e) )
        AbdtManager.WrtLog('ɾ�������ļ��쳣')
        return -1


#��ʷ���������ļ�����
def ClearHisDataFile():

    #��ѯ������Ϣ��
    try:
        sql = ""
        #88-�Ѿ�������� 40-�Ѿ���������
        sql = "SELECT BATCHNO,APPNO,BUSINO,INDATE,BATCHDATE,STATUS,BRNO FROM ABDT_BATCHINFO WHERE STATUS IN ('40','88') AND NOTE2<" + "'" + TradeContext.WorkDate  + "'"
        records = AfaDBFunc.SelectSql( sql )
        if ( len(records) == 0 ):
            AbdtManager.WrtLog('û����Ҫ�������������ļ�')
            return 0

        else:
            AbdtManager.WrtLog('�ܹ���[' + str(len(records)) + ']���������¼')

    except Exception, e:
        AbdtManager.WrtLog(e)
        AbdtManager.WrtLog('�������������ļ��쳣')
        return -1

    i = 0
    while ( i  < len(records) ):
        TradeContext.BATCHNO   = str(records[i][0]).strip()         #ί�к�(���κ�)
        TradeContext.APPNO     = str(records[i][1]).strip()         #ҵ����
        TradeContext.BUSINO    = str(records[i][2]).strip()         #��λ���
        TradeContext.INDATE    = str(records[i][3]).strip()         #��������
        TradeContext.BATCHDATE = str(records[i][4]).strip()         #�ύ����
        TradeContext.STATUS    = str(records[i][5]).strip()         #��ҵ״̬
        TradeContext.BRNO      = str(records[i][6]).strip()         #��������


        #�����ļ�������(������ļ��ƶ�����Ŀ¼��)
        AbdtManager.WrtLog('��������:['+TradeContext.BUSINO+']['+TradeContext.BATCHNO+']['+TradeContext.BATCHDATE+']')

        #���inĿ¼�ļ�
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.APPNO + TradeContext.BUSINO + '_' + TradeContext.INDATE
        delDataFile(dFileName)

        #���hostĿ¼�ļ�
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_1'
        delDataFile(dFileName)

        dFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_2'
        delDataFile(dFileName)

        dFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_3'
        delDataFile(dFileName)

        dFileName = os.environ['AFAP_HOME'] + '/data/batch/host/' + TradeContext.BATCHNO + '_4'
        delDataFile(dFileName)

        #���downĿ¼�ļ�
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.APPNO + TradeContext.BUSINO + '_' + TradeContext.INDATE + '.RET'
        delDataFile(dFileName)

        dFileName = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.APPNO + TradeContext.BUSINO + '_' + TradeContext.INDATE + '.RPT'
        delDataFile(dFileName)

        if ( TradeContext.STATUS == '88' ):
            #���������ļ�

            #�ϴ�
            upHFileName = 'A' + TradeContext.BATCHNO[8:16] + '1'
            DelHostFile(TradeContext.BATCHNO, upHFileName, '1')

            #����
            dwHFileName = 'A' + TradeContext.BATCHNO[8:16] + '2'
            DelHostFile(TradeContext.BATCHNO, dwHFileName, '2')

        i=i+1

    return 0










###########################################������###########################################
if __name__=='__main__':

    AbdtManager.WrtLog('********************�������ݴ���ʼ********************')

    #��ȡ�����ļ�
    BatchConfig = AbdtManager.GetBatchConfig()


    #����ƫ���������������
    TradeContext.WorkDate = getTimeFromNow(long(TradeContext.BATCH_CLEARDAY))
    
    #��ȡ��ǰ����
    TradeContext.CurDate  = AfaUtilTools.GetSysTime( )


    if ( TradeContext.WorkDate >= TradeContext.CurDate ):
        AbdtManager.WrtLog('>>>������ڲ��ܴ��ڵ�ǰ����:[' + TradeContext.WorkDate + ']')

    else:
        AbdtManager.WrtLog('>>>���:[ʧЧ���� < '+ TradeContext.WorkDate + ']���������ļ�')

        ClearHisDataFile()

    AbdtManager.WrtLog('********************�������ݴ������********************')

