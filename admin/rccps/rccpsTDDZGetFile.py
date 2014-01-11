# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ͨ��ͨ�Ҷ����ļ�����
#===============================================================================
#   �����ļ�:   rccpsTDDZGetFile.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-11-20
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc
import rccpsDBTrcc_mbrifa


if __name__ == "__main__":
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ����ļ�����[rccpsTDDZGetFile]����***")

        local_home = os.environ['AFAP_HOME'] + "/data/rccps/"
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #================�ж�ǰ�û�ͨ��ͨ�Ҷ����ļ��Ƿ������=========================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ж�ǰ�û�ͨ��ͨ�Ҷ����ļ��Ƿ������")
        
        file_path = "settlefile/tdsendend1340000008"
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","�����ļ�[" + file_path + "]�쳣")
        
        local_file_path = local_home + file_path
        
        fp = open(local_file_path,"rb")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ����ļ����ͱ�ʶ�ļ��쳣")
        
        file_line = fp.readline()
        file_line = AfaUtilTools.trim(file_line)
        
        fp.close()
        
        if file_line[:8] != NCCWKDAT:
            rccpsCronFunc.cronExit("S999","ͨ��ͨ�Ҷ����ļ���δ�������")
        
        AfaLoggerFunc.tradeInfo(">>>ͨ��ͨ�Ҷ����ļ��������")
        
        AfaLoggerFunc.tradeInfo(">>>�����ж�ǰ�û�ͨ��ͨ�Ҷ����ļ��Ƿ������")
        
        #================����ͨ��ͨ�Ҷ����ļ�����=======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ͨ��ͨ�Ҷ����ļ�")
        
        file_path = "settlefile/TDHZCNY1340000008" + NCCWKDAT
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","����ͨ��ͨ�Ҷ��˻����ļ�[" + file_path + "]�쳣")
        
        file_path = "settlefile/TDMXCNY1340000008" + NCCWKDAT
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","����ͨ��ͨ�Ҷ�����ϸ�ļ�[" + file_path + "]�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ͨ��ͨ�Ҷ����ļ�")
        
        #================�ر�ͨ��ͨ�Ҷ����ļ�����ϵͳ����,�򿪵���ͨ��ͨ�Ҷ����ļ�ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ�Ҷ����ļ�����ϵͳ����,�򿪵���ͨ��ͨ�Ҷ����ļ�ϵͳ����")
        if not rccpsCronFunc.closeCron("00061"):
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ�Ҷ����ļ�����ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00064"):
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ�����ϸ�ļ�����ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ�Ҷ����ļ�����ϵͳ����,�򿪵���ͨ��ͨ�Ҷ����ļ�ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ����ļ�����[rccpsTDDZGetFile]�˳�***")
        

    except Exception, e:
        #�����쳣

        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = 'ϵͳ����['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            AfaLoggerFunc.tradeInfo( 'errorCode=['+TradeContext.errorCode+']' )
            AfaLoggerFunc.tradeInfo( 'errorMsg=['+TradeContext.errorMsg+']' )
            AfaLoggerFunc.tradeInfo('***[rccpsTDDZGetFile]�����ж�***')

        sys.exit(-1)
