# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ͨ��ͨ�Ҷ�����ϸ�ļ�����
#===============================================================================
#   �����ļ�:   rccpsTDDZMXFileImport.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-11-20
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsDBFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_tddzmx

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ�����ϸ�ļ�����[rccpsTDDZMXFileImport]����***")
        
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
        
        #====================����ͨ��ͨ�Ҷ�����ϸ�ļ�===================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ͨ��ͨ�Ҷ�����ϸ�ļ�")
        
        file_path = local_home + "settlefile/TDMXCNY1340000008" + NCCWKDAT
        
        fp = open(file_path,"r")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ�����ϸ�ļ��쳣")
            
        file_line = " "
        
        #�ر�� 20081028 �޸���Ҫ���˵����ڻ�ȡ��ʽ
        #��ʼ�����ζ�����Ҫ���˵���������
        NCCWKDAT_LIST = []
        NCCWKDAT_LIST.append(NCCWKDAT)
        
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
            
            #��������¼���������ڲ�����Ҫ���˵����������б���,��׷��
            if not NCCWKDAT_LIST.__contains__(line_list[0][:8]):
                NCCWKDAT_LIST.append(line_list[0][:8])
            
            tddzmx_insert_dict = {}
            
            tddzmx_insert_dict['NCCWKDAT'] = line_list[0][:8]
            tddzmx_insert_dict['TRCCO']    = line_list[1][:7]
            tddzmx_insert_dict['MSGTYPCO'] = line_list[2][:6]
            tddzmx_insert_dict['RCVMBRCO'] = line_list[3][:10]
            tddzmx_insert_dict['SNDMBRCO'] = line_list[4][:10]
            tddzmx_insert_dict['SNDBRHCO'] = line_list[5][:6]
            tddzmx_insert_dict['SNDCLKNO'] = line_list[6][:8]
            tddzmx_insert_dict['SNDTRDAT'] = line_list[7][:8]
            tddzmx_insert_dict['SNDTRTIM'] = line_list[8][:6]
            tddzmx_insert_dict['MSGFLGNO'] = line_list[9][:26]
            tddzmx_insert_dict['ORMFN']    = line_list[10][:26]
            tddzmx_insert_dict['OPRTYPNO'] = line_list[11][:2]
            tddzmx_insert_dict['ROPRTPNO'] = line_list[12][:2]
            tddzmx_insert_dict['SNDBNKCO'] = line_list[13][:10]
            tddzmx_insert_dict['SNDBNKNM'] = line_list[14][:60]
            tddzmx_insert_dict['RCVBNKCO'] = line_list[15][:10]
            tddzmx_insert_dict['RCVBNKNM'] = line_list[16][:60]
            tddzmx_insert_dict['TRCDAT']   = line_list[17][:8]
            tddzmx_insert_dict['TRCNO']    = line_list[18][:8]
            tddzmx_insert_dict['CUR']      = line_list[19][:3]
            tddzmx_insert_dict['OCCAMT']   = line_list[20][:18]
            tddzmx_insert_dict['CUSCHRG']  = line_list[21][:18]
            tddzmx_insert_dict['PYRMBRCO'] = line_list[22][:10]
            tddzmx_insert_dict['PYRACC']   = line_list[23][:32]
            tddzmx_insert_dict['PYEMBRCO'] = line_list[24][:10]
            tddzmx_insert_dict['PYEACC']   = line_list[25][:32]
            tddzmx_insert_dict['ORTRCCO']  = line_list[26][:7]
            tddzmx_insert_dict['ORTRCNO']  = line_list[27][:8]
            tddzmx_insert_dict['DCFLG']    = line_list[28][:1]
            tddzmx_insert_dict['CBFLG']    = line_list[29][:1]
            tddzmx_insert_dict['CONFFLG']  = line_list[30][:1]
            tddzmx_insert_dict['CANCFLG']  = line_list[31][:1]
            tddzmx_insert_dict['STRINFO']  = line_list[32][:60]
            tddzmx_insert_dict['NOTE1']    = NCCWKDAT            #���������ڸ�ֵ��������ϸ��NOTE1�ֶ�
            
            #ͨ��ͨ�Ҷ����ļ��д��ȷ�Ϻͳ������ײ����������ϸ����
            if tddzmx_insert_dict['TRCCO'] == '3000503' or tddzmx_insert_dict['TRCCO'] == '3000504':
                continue
            
            wtr_dict = {}
            if not rccpsDBFunc.getTransWtrAK(tddzmx_insert_dict['SNDBNKCO'],tddzmx_insert_dict['TRCDAT'],tddzmx_insert_dict['TRCNO'],wtr_dict):
                if AfaDBFunc.sqlErrMsg != "":
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccpsCronFunc.cronExit("S999","��ѯ������ϸ������Ϣ�쳣")
                else:
                    tddzmx_insert_dict['BJEDTE'] = ""
                    tddzmx_insert_dict['BSPSQN'] = ""
                
            else:
                tddzmx_insert_dict['BJEDTE'] = wtr_dict['BJEDTE']
                tddzmx_insert_dict['BSPSQN'] = wtr_dict['BSPSQN']
            
            ret = rccpsDBTrcc_tddzmx.insert(tddzmx_insert_dict)
            
            if ret <= 0:
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                rccpsCronFunc.cronExit("S999","���������ϸ�ļ��쳣")
        
        fp.close()
        AfaLoggerFunc.tradeInfo(">>>��������ͨ��ͨ�Ҷ�����ϸ�ļ�")
        
        #����ͨ��ͨ��ҵ����Ҫ���˵�����
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ϵͳ״̬����NOTE3�ֶ�(ͨ��ͨ��ҵ����Ҫ���˵�����)")
        
        #�ر�� 20081028 �޸���Ҫ���˵����ڻ�ȡ��ʽ ɾ��ԭ��ʽ
        #rec = AfaDBFunc.SelectSql("select distinct(nccwkdat) from rcc_tddzmx where NOTE1 = '" + NCCWKDAT + "'")
        
        #if ret == None:
        #    rccpsCronFunc.cronExit("S999","��ѯ������ϸ����ͨ��ͨ��ҵ����Ҫ���˵������쳣")
            
        #if len(rec) <= 0:
        #    rccpsCronFunc.cronExit("S999","��ѯ������ϸ����ͨ��ͨ��ҵ����Ҫ���˵������쳣")
        
        LNCCWKDAT = str(NCCWKDAT_LIST).replace('[','').replace(']','').replace('(','').replace(',)','').replace('\'','')
        LNCCWKDAT = AfaUtilTools.trim(LNCCWKDAT)
        
        AfaLoggerFunc.tradeInfo("NOTE3=[" + LNCCWKDAT + "]")
        
        rec = AfaDBFunc.UpdateSqlCmt("update rcc_mbrifa set note3 = '" + LNCCWKDAT + "' " + " where oprtypno = '30' ")
        
        if rec <= 0:
            rccpsCronFunc.cronExit("S999","����ҵ��״̬����NOTE3�ֶ��쳣")
            
        AfaLoggerFunc.tradeInfo(">>>��������ϵͳ״̬����NOTE3�ֶ�(ͨ��ͨ��ҵ����Ҫ���˵�����)")

        
        #====================�ر�ͨ��ͨ�Ҷ�����ϸ�ļ�����ϵͳ����,��ͨ��ͨ�Ҷ��˻����ļ������ͨ��ͨ��ҵ����ͳ��ϵͳ����====
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ�Ҷ�����ϸ�ļ�����ϵͳ����,��ͨ��ͨ�Ҷ��˻����ļ�����ϵͳ����")
        if not rccpsCronFunc.closeCron("00064"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ�Ҷ�����ϸ�ļ�����ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00062"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ��˻����ļ�����ϵͳ�����쳣")
            
#        if not rccpsCronFunc.openCron("00066"):
#            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
#            rccpsCronFunc.cronExit("S999","��ͨ��ͨ��ҵ����ͳ��ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ�Ҷ�����ϸ�ļ�����ϵͳ����,��ͨ��ͨ�Ҷ��˻����ļ�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ�����ϸ�ļ�����[rccpsTDDZMXFileImport]�˳�***")      
        
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDDZMXFileImport]�����ж�***')

        sys.exit(-1)
