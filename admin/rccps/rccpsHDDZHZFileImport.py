# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��Ҷ��˻����ļ�����
#===============================================================================
#   �����ļ�:   rccpsHDDZHZFileImport.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-25
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hddzhz

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ҷ��˻����ļ�����[rccpsHDDZHZFileImport]����***")
        
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
        
        #====================�����Ҷ��˻����ļ�===================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�����Ҷ��˻����ļ�")
        
        file_path = local_home + "settlefile/HDHZCNY1340000008" + NCCWKDAT
        
        fp = open(file_path,"r")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","�򿪻�Ҷ��˻����ļ��쳣")
            
        file_line = " "
        
        while file_line:
            
            file_line = fp.readline()
            
            #�ر�� 20081028 ���Ӹ�ʽ�������ļ�
            file_line = AfaUtilTools.trim(file_line)
            #�ź� 20091125 ����ɾ�������ļ��зǷ��ַ�
            file_line = AfaUtilTools.trimchn(file_line)
            file_line = rccpsUtilTools.replaceRet(file_line)
            
            if file_line == "":
                continue
                
            line_list = file_line.split('|')
            
            hddzhz_insert_dict = {}
            
            hddzhz_insert_dict['NCCWKDAT'] = NCCWKDAT
            hddzhz_insert_dict['TRCCO']    = line_list[0][:7]
            hddzhz_insert_dict['TRCNAM']   = line_list[1][:12]
            hddzhz_insert_dict['TRCRSNM']  = line_list[2][:8]
            hddzhz_insert_dict['TCNT']     = line_list[3][:10]
            hddzhz_insert_dict['CTAMT']    = line_list[4][:18]
            hddzhz_insert_dict['DTAMT']    = line_list[5][:18]
            hddzhz_insert_dict['OFSTAMT']  = line_list[6][:18]
            hddzhz_insert_dict['NOTE1']    = NCCWKDAT          #��������
            
            if hddzhz_insert_dict['TRCRSNM'][:4] == "����":
                hddzhz_insert_dict['BRSFLG'] = PL_BRSFLG_SND
            elif hddzhz_insert_dict['TRCRSNM'][:4] == "����":
                hddzhz_insert_dict['BRSFLG'] = PL_BRSFLG_RCV
            else:
                hddzhz_insert_dict['BRSFLG'] = '9'
            
            ret = rccpsDBTrcc_hddzhz.insert(hddzhz_insert_dict)
            
            if ret <= 0:
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                rccpsCronFunc.cronExit("S999","�����Ҷ��˻����ļ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>���������Ҷ��˻����ļ�")
        
        #====================�رջ�Ҷ��˻����ļ�����ϵͳ����,�򿪻�Ҷ�����ϸ�˹���====
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ҷ��˻����ļ�����ϵͳ����,�򿪻�Ҷ�����ϸ�˹���")
        if not rccpsCronFunc.closeCron("00032"):
            rccpsCronFunc.cronExit("S999","�رջ�Ҷ����ļ�����ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00033"):
            rccpsCronFunc.cronExit("S999","�򿪻�Ҷ��˻����ļ�����ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ҷ�����ϸ�ļ�����ϵͳ����,�򿪻�Ҷ��˻����ļ�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ҷ��˻����ļ�����[rccpsHDDZHZFileImport]�˳�***")
        
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
            AfaLoggerFunc.tradeInfo('***[rccpsHDDZHZFileImport]�����ж�***')

        sys.exit(-1)
