# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��Ʊ������ϸ�ļ�����
#===============================================================================
#   �����ļ�:   rccpsHPDZMXFileImport.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-25
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsDBFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hpdzmx


if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊ������ϸ�ļ�����[rccpsHPDZMXFileImport]����***")
        
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
        
        #====================�����Ʊ������ϸ�ļ�===================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�����Ʊ������ϸ�ļ�")
        
        file_path = local_home + "settlefile/HPMXCNY1340000008" + NCCWKDAT
        
        fp = open(file_path,"r")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","�򿪻�Ʊ������ϸ�ļ��쳣")
            
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
            
            hpdzmx_insert_dict = {}
            
            hpdzmx_insert_dict['NCCWKDAT'] = line_list[0][:8]
            hpdzmx_insert_dict['TRCCO']    = line_list[1][:7]
            hpdzmx_insert_dict['MSGTYPCO'] = line_list[2][:6]
            hpdzmx_insert_dict['RCVMBRCO'] = line_list[3][:10]
            hpdzmx_insert_dict['SNDMBRCO'] = line_list[4][:10]
            hpdzmx_insert_dict['SNDBRHCO'] = line_list[5][:6]
            hpdzmx_insert_dict['SNDCLKNO'] = line_list[6][:8]
            hpdzmx_insert_dict['SNDTRDAT'] = line_list[7][:8]
            hpdzmx_insert_dict['SNDTRTIM'] = line_list[8][:6]
            hpdzmx_insert_dict['MSGFLGNO'] = line_list[9][:26]
            hpdzmx_insert_dict['ORMFN']    = line_list[10][:26]
            hpdzmx_insert_dict['OPRTYPNO'] = line_list[11][:2]
            hpdzmx_insert_dict['ROPRTPNO'] = line_list[12][:2]
            hpdzmx_insert_dict['SNDBNKCO'] = line_list[13][:10]
            hpdzmx_insert_dict['SNDBNKNM'] = line_list[14][:60]
            hpdzmx_insert_dict['RCVBNKCO'] = line_list[15][:10]
            hpdzmx_insert_dict['RCVBNKNM'] = line_list[16][:60]
            hpdzmx_insert_dict['TRCDAT']   = line_list[17][:8]
            hpdzmx_insert_dict['TRCNO']    = line_list[18][:8]
            hpdzmx_insert_dict['CUR']      = line_list[19][:3]
            hpdzmx_insert_dict['OCCAMT']   = line_list[20][:18]
            hpdzmx_insert_dict['PYRACC']   = line_list[21][:32]
            hpdzmx_insert_dict['PYRNAM']   = line_list[22][:60]
            hpdzmx_insert_dict['PYRADDR']  = line_list[23][:60]
            hpdzmx_insert_dict['PYEACC']   = line_list[24][:32]
            hpdzmx_insert_dict['PYENAM']   = line_list[25][:60]
            hpdzmx_insert_dict['PYEADDR']  = line_list[26][:60]
            hpdzmx_insert_dict['OPRATTNO'] = line_list[27][:2]
            hpdzmx_insert_dict['SEAL']     = line_list[28][:10]
            hpdzmx_insert_dict['BILDAT']   = line_list[29][:8]
            hpdzmx_insert_dict['BILNO']    = line_list[30][:8]
            hpdzmx_insert_dict['BILVER']   = line_list[31][:2]
            hpdzmx_insert_dict['PAYWAY']   = line_list[32][:1]
            hpdzmx_insert_dict['BILAMT']   = line_list[33][:18]
            hpdzmx_insert_dict['RMNAMT']   = line_list[34][:18]
            hpdzmx_insert_dict['USE']      = line_list[35][:20]
            hpdzmx_insert_dict['REMARK']   = line_list[36][:30]
            hpdzmx_insert_dict['NOTE1']    = NCCWKDAT            #���������ڸ�ֵ��������ϸ��NOTE1�ֶ�
            
            trc_dict = {}
            if not rccpsDBFunc.getTransBilAK(hpdzmx_insert_dict['SNDBNKCO'],hpdzmx_insert_dict['TRCDAT'],hpdzmx_insert_dict['TRCNO'],trc_dict):
                if AfaDBFunc.sqlErrMsg != "":
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccpsCronFunc.cronExit("S999","��ѯ������ϸ������Ϣ�쳣")
                else:
                    hpdzmx_insert_dict['BJEDTE'] = ""
                    hpdzmx_insert_dict['BSPSQN'] = ""
                    hpdzmx_insert_dict['BCSTAT'] = ""
                    hpdzmx_insert_dict['BDWFLG'] = ""
                
            else:
                hpdzmx_insert_dict['BJEDTE'] = trc_dict['BJEDTE']
                hpdzmx_insert_dict['BSPSQN'] = trc_dict['BSPSQN']
                hpdzmx_insert_dict['BCSTAT'] = trc_dict['BCSTAT']
                hpdzmx_insert_dict['BDWFLG'] = trc_dict['BDWFLG']
            
            ret = rccpsDBTrcc_hpdzmx.insert(hpdzmx_insert_dict)
            
            if ret <= 0:
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                rccpsCronFunc.cronExit("S999","���������ϸ�ļ��쳣")
        
        fp.close()
        AfaLoggerFunc.tradeInfo(">>>���������Ʊ������ϸ�ļ�")
        
        #���»�Ʊҵ����Ҫ���˵�����
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ϵͳ״̬����NOTE4�ֶ�(��Ʊҵ����Ҫ���˵�����)")
        
        #�ر�� 20081028 �޸���Ҫ���˵����ڻ�ȡ��ʽ ɾ��ԭ��ʽ
        #rec = AfaDBFunc.SelectSql("select distinct(nccwkdat) from rcc_hpdzmx where NOTE1 = '" + NCCWKDAT + "'")
        
        #if rec == None:
        #    rccpsCronFunc.cronExit("S999","��ѯ������ϸ���л�Ʊҵ����Ҫ���˵������쳣")
            
        #if len(rec) <= 0:
        #    rccpsCronFunc.cronExit("S999","��ѯ������ϸ���л�Ʊҵ����Ҫ���˵������쳣")
        
        LNCCWKDAT = str(NCCWKDAT_LIST).replace('[','').replace(']','').replace('(','').replace(',)','').replace('\'','')
        LNCCWKDAT = AfaUtilTools.trim(LNCCWKDAT)
        
        AfaLoggerFunc.tradeInfo("NOTE4=[" + LNCCWKDAT + "]")
        
        rec = AfaDBFunc.UpdateSqlCmt("update rcc_mbrifa set note4 = '" + LNCCWKDAT + "' " + " where oprtypno = '20' ")
        
        if rec <= 0:
            rccpsCronFunc.cronExit("S999","����ҵ��״̬����NOTE4�ֶ��쳣")
            
        AfaLoggerFunc.tradeInfo(">>>��������ϵͳ״̬����NOTE4�ֶ�(��Ʊҵ����Ҫ���˵�����)")
        
        #====================�رջ�Ʊ������ϸ�ļ�����ϵͳ����,�򿪻�Ʊ���˻����ļ�����ͻ�Ʊҵ����ͳ��ϵͳ����====
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ʊ������ϸ�ļ�����ϵͳ����,�򿪻�Ʊ���˻����ļ�����ϵͳ����")
        if not rccpsCronFunc.closeCron("00044"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�رջ�Ʊ�����ļ�����ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00042"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�򿪻�Ʊ���˻����ļ�����ϵͳ�����쳣")
            
#        if not rccpsCronFunc.openCron("00046"):
#            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
#            rccpsCronFunc.cronExit("S999","�򿪻�Ʊҵ����ͳ��ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ʊ������ϸ�ļ�����ϵͳ����,�򿪻�Ʊ���˻����ļ�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊ������ϸ�ļ�����[rccpsHPDZMXFileImport]�˳�***")
        
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
            AfaLoggerFunc.tradeInfo('***[rccpsHPDZMXFileImport]�����ж�***')

        sys.exit(-1)
