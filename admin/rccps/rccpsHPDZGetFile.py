# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��Ʊ�����ļ�����
#===============================================================================
#   �����ļ�:   rccpsHPDZGetFile.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-24
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc
import rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊ�����ļ�����[rccpsHPDZGetFile]����***")
        
        local_home = os.environ['AFAP_HOME'] + "/data/rccps/"
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #================�ж�ǰ�û���Ʊ�����ļ��Ƿ������=========================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ж�ǰ�û���Ʊ�����ļ��Ƿ������")
        
        file_path = "settlefile/hpsendend1340000008"
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","�����ļ�[" + file_path + "]�쳣")
            
        local_file_path = local_home + file_path
        
        fp = open(local_file_path,"rb")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","�򿪻�Ҷ����ļ����ͱ�ʶ�ļ��쳣")
        
        file_line = fp.readline()
        file_line = AfaUtilTools.trim(file_line)
        
        fp.close()
        
        if file_line[:8] != NCCWKDAT:
            rccpsCronFunc.cronExit("S999","��Ʊ�����ļ���δ�������")
        
        AfaLoggerFunc.tradeInfo(">>>��Ʊ�����ļ��������")
        
        AfaLoggerFunc.tradeInfo(">>>�����ж�ǰ�û���Ʊ�����ļ��Ƿ������")
        
        #================���ػ�Ʊ�����ļ�����=======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ���ػ�Ʊ�����ļ�")
        
        file_path = "settlefile/HPHZCNY1340000008" + NCCWKDAT
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","���ػ�Ʊ���˻����ļ�[" + file_path + "]�쳣")
        
        file_path = "settlefile/HPMXCNY1340000008" + NCCWKDAT
        
        if not rccpsFtpFunc.getRccps(file_path):
            rccpsCronFunc.cronExit("S999","���ػ�Ʊ������ϸ�ļ�[" + file_path + "]�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�������ػ�Ʊ�����ļ�")
        
        #================�رջ�Ʊ�����ļ�����ϵͳ����,�򿪵����Ʊ�����ļ�ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ʊ�����ļ�����ϵͳ����,�򿪵����Ʊ�����ļ�ϵͳ����")
        if not rccpsCronFunc.closeCron("00041"):
            rccpsCronFunc.cronExit("S999","�رջ�Ʊ�����ļ�����ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00044"):
            rccpsCronFunc.cronExit("S999","�򿪻�Ʊ������ϸ�ļ�����ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ʊ�����ļ�����ϵͳ����,�򿪵����Ʊ�����ļ�ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊ�����ļ�����[rccpsHPDZGetFile]�˳�***")
        
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
            AfaLoggerFunc.tradeInfo('***[rccpsHPDZGetFile]�����ж�***')

        sys.exit(-1)
