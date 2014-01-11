# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.����ũ����ϵͳ���Ǽǲ�
#===============================================================================
#   �����ļ�:   rccpsDBBackup.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2009-09-15
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc

def backupdb(tbName,clName,backupDate):
    
    AfaLoggerFunc.tradeInfo(">>>>��ʼͳ�Ʊ�[" + tbName + "]" + backupDate + "]�豸������")
    sql = "select count(*) from " + tbName + " where " + clName + " < '" + backupDate + "'"
    AfaLoggerFunc.tradeInfo(sql)
    
    rec = AfaDBFunc.SelectSql(sql)
    
    if rec == None:
        AfaLoggerFunc.tradeInfo(">>>>ͳ�Ʊ�[" + tbName + "][" + backupDate + "]�豸�������쳣")
        rccpsCronFunc.cronExit("S999","ͳ�Ʊ�[" + tbName + "][" + backupDate + "]�豸�������쳣")
    if len(rec) <= 0:
        AfaLoggerFunc.tradeInfo(">>>>ͳ�Ʊ�[" + tbName + "][" + backupDate + "]�豸�������쳣")
        rccpsCronFunc.cronExit("S999","ͳ�Ʊ�[" + tbName + "][" + backupDate + "]�豸�������쳣")
        
    if rec[0][0] <= 0:
        AfaLoggerFunc.tradeInfo(">>>>��[" + tbName + "][" + backupDate + "]���豸������")
        #rccpsCronFunc.cronExit("S999","ʵʱ��ҵǼǲ�[" + backupDate + "]���豸������")
    else:
        #�������������ļ�
        file = path + "/" + tbName + ".del"
        
        if not os.path.exists(file):
            AfaLoggerFunc.tradeInfo(">>>>��ʼ������[" + tbName + "][" + backupDate + "]�������ļ�")
            
            cmd = "db2 \"export to '" + file + "' of del select * from " + tbName + " where " + clName + " < '" + backupDate + "'\""
            AfaLoggerFunc.tradeInfo(cmd)
            os.system(cmd)
            
            AfaLoggerFunc.tradeInfo(">>>>����������[" + tbName + "][" + backupDate + "]�������ļ�")
        else:
            AfaLoggerFunc.tradeInfo(">>>>��[" + tbName + "][" + backupDate + "]�����ļ��Ѵ���")
        
        #��������������ʷ��
        AfaLoggerFunc.tradeInfo(">>>>��ʼ������[" + tbName + "][" + backupDate + "]��������ʷ��")
        
        sql = ""
        sql = sql + "insert into " + tbName + "_his "
        sql = sql + "(select * from " + tbName + " where " + clName + " < '" + backupDate + "')"
        AfaLoggerFunc.tradeInfo(sql)
        
        rec = AfaDBFunc.InsertSql(sql)
        
        if (rec < 0):
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","������[" + tbName + "][" + backupDate + "]��������ʷ���쳣")
            
        AfaLoggerFunc.tradeInfo(">>>>����������[" + tbName + "][" + backupDate + "]��������ʷ��")
        
        #ɾ��������
        AfaLoggerFunc.tradeInfo(">>>>��ʼɾ����[" + tbName + "][" + backupDate + "]����")
        
        sql = ""
        sql = sql + "delete from " + tbName + " where " + clName + " < '" + backupDate + "'"
        AfaLoggerFunc.tradeInfo(sql)
        
        rec = AfaDBFunc.DeleteSql(sql)
        
        if (rec < 0):
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","ɾ����[" + tbName + "][" + backupDate + "]�����쳣")
            
        AfaLoggerFunc.tradeInfo(">>>>����ɾ����[" + tbName + "][" + backupDate + "]����")
        
        #�ύ����
        if not AfaDBFunc.CommitSql():
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","�ύ�����쳣")
            
        #������
        AfaLoggerFunc.tradeInfo(">>>>��ʼ������[" + tbName + "]")
        
        cmd = "db2 \"reorg table " + tbName + "\" "
        AfaLoggerFunc.tradeInfo(cmd)
        os.system(cmd)
        
        AfaLoggerFunc.tradeInfo(">>>>����������[" + tbName + "]")

if __name__ == '__main__':
    
    try:
        rccpsCronFunc.WrtLog("***ũ����ϵͳ: ϵͳ������.����ũ�������Ǽǲ�[rccpsDBBackup]����***")
 
        #��ȡ��ǰ��������
        workDate=AfaUtilTools.GetSysDate()
        #AfaLoggerFunc.tradeInfo("��ǰ����[" + workDate + "]")
        #backupDate=str(long(workDate) - 100)
        #AfaLoggerFunc.tradeInfo("��������[" + backupDate + "]")

        AfaLoggerFunc.tradeInfo("��ǰ����[" + workDate + "]")

        #=====START �ź�������20091229 ��Կ��겢�ҵ�ǰ����01�����豸����һ��12�·ݵ�����===
        if workDate[4:6] == '01' :
            backupDate = str(long(workDate) - 8900)
        else:
            backupDate=str(long(workDate) - 100)
        #=====END============================================================================
        AfaLoggerFunc.tradeInfo("��������[" + backupDate + "]")

        #���������ļ����Ŀ¼
        AfaLoggerFunc.tradeInfo(">>>>��ʼ����[" + backupDate + "]Ŀ¼")
        
        path = os.environ['AFAP_HOME'] + "/data/rccps/dbbackup/" + backupDate
        AfaLoggerFunc.tradeInfo(path)
        
        if not os.path.exists(path):
            cmd = "mkdir -p " + path
            AfaLoggerFunc.tradeInfo(cmd)
            os.system(cmd)
            
        AfaLoggerFunc.tradeInfo(">>>>��������[" + backupDate + "]Ŀ¼")
        #rccpsCronFunc.cronExit("S999","�˳�")

        #�������ݿ�
        AfaLoggerFunc.tradeInfo(">>>>��ʼ�������ݿ�")
        
        cmd = "db2 connect to maps"
        os.system(cmd)
        
        AfaLoggerFunc.tradeInfo(">>>>�����������ݿ�")

        #ʵʱ��ҵǼǲ���ز���
        backupdb("rcc_trcbka","bjedte",backupDate)
        
        #ȫ����Ʊ�Ǽǲ���ز���
        backupdb("rcc_bilbka","bjedte",backupDate)
        
        #ͨ��ͨ�ҵǼǲ���ز���
        backupdb("rcc_wtrbka","bjedte",backupDate)
                
        #��ǰ״̬�Ǽǲ���ز���
        backupdb("rcc_spbsta","bjedte",backupDate)
        
        #��ʷ״̬�Ǽǲ���ز���
        backupdb("rcc_sstlog","bjedte",backupDate)
        
        #ʵʱ��Ҷ�����ϸ�Ǽǲ���ز���
        backupdb("rcc_hddzmx","nccwkdat",backupDate)
        
        #ȫ����Ʊ������ϸ�Ǽǲ���ز���
        backupdb("rcc_hpdzmx","nccwkdat",backupDate)
        
        #ͨ��ͨ�Ҷ�����ϸ�Ǽǲ���ز���
        backupdb("rcc_tddzmx","nccwkdat",backupDate)
        
        #�Ͽ����ݿ�
        AfaLoggerFunc.tradeInfo(">>>>��ʼ�Ͽ����ݿ�")
        
        cmd = "db2 disconnect maps"
        os.system(cmd)
        
        AfaLoggerFunc.tradeInfo(">>>>�����Ͽ����ݿ�")
        
        rccpsCronFunc.WrtLog("***ũ����ϵͳ: ϵͳ������.����ũ�������Ǽǲ�[rccpsDBBackup]�˳�***")
    
    except Exception, e:
        #�����쳣

        if not AfaDBFunc.RollbackSql( ):
            rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.WrtLog(">>>Rollback�쳣")
        rccpsCronFunc.WrtLog(">>>Rollback�ɹ�")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = 'ϵͳ����['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            rccpsCronFunc.WrtLog( 'errorCode=['+TradeContext.errorCode+']' )
            rccpsCronFunc.WrtLog( 'errorMsg=['+TradeContext.errorMsg+']' )
            rccpsCronFunc.WrtLog('[rccpsDBBackup]�����ж�')

        sys.exit(-1)

