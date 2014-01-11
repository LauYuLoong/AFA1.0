# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ��ϵͳ������.ũ������Ʊ�����ļ����ɼ����͵�����
#==============================================================================
#   �����ļ�:   rccpsHPDZMXPutFile.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-28
###############################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc,rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsUtilTools
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hpdzmx

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ũ������Ʊ�����ļ����ɼ����͵�����[rccpsHPDZMXPutFile]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE4'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #================���ݻ�Ʊ������ϸ�Ǽǲ�,���ɻ�Ʊ���������ļ�===========
        AfaLoggerFunc.tradeInfo(">>>��ʼ���ɻ�Ʊ���������ļ�")
        
        hpdzmx_where_sql = "NCCWKDAT in " + LNCCWKDAT
        
        hpdzmx_list = rccpsDBTrcc_hpdzmx.selectm(1,0,hpdzmx_where_sql,"")
        
        if hpdzmx_list == None:
            rccpsCronFunc.cronExit("S999","��ѯ��Ʊ������ϸ�Ǽǲ��쳣")
            
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/RCCPSHPDZMX" + NCCWKDAT
        
        fp = open(file_path,"w")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","�򿪻�Ʊ����(����)��ϸ�ļ��쳣")
            
        file_line = ""
        
        if len(hpdzmx_list) <= 0:
            AfaLoggerFunc.tradeInfo(">>>��Ʊ������ϸ�Ǽǲ����޶�Ӧ��¼")
        else:
            for i in xrange(len(hpdzmx_list)):
                
                file_line = file_line + "RCC".ljust(8,' ')                     + '|' #����ҵ���
                file_line = file_line + hpdzmx_list[i]['BJEDTE'].ljust(8,' ')  + '|' #ǰ������
                file_line = file_line + hpdzmx_list[i]['BSPSQN'].ljust(12,' ') + '|' #ǰ����ˮ��
                
                trc_dict = {}
                if not rccpsDBFunc.getTransBil(hpdzmx_list[i]['BJEDTE'],hpdzmx_list[i]['BSPSQN'],trc_dict):
                    rccpsCronFunc.cronExit("S999","��ѯ��Ʊҵ����Ϣ�쳣")
                    
                if not rccpsDBFunc.getInfoBil(trc_dict['BILVER'],trc_dict['BILNO'],trc_dict['BILRS'],trc_dict):
                    rccpsCronFunc.cronExit("S999","��ѯ��Ʊ��ϸ��Ϣ�쳣")
                
                file_line = file_line + hpdzmx_list[i]['SNDBNKCO'].ljust(12,' ') + '|' #�����к�
                file_line = file_line + hpdzmx_list[i]['SNDBNKNM'].ljust(62,' ') + '|' #��������
                file_line = file_line + trc_dict['BRSFLG'].ljust(1,' ')        + '|' #������ʶ
                file_line = file_line + "".ljust(5,' ')                        + '|' #ҵ������
                
                
                #=======����������ʶȥ�������Ϣ===============================
                if trc_dict['BRSFLG'] == PL_BRSFLG_SND:
                    #===���˲�ѯ����/�̿�ɹ�״̬��Ϣ�еĽ�����˺���Ϣ========
                    
                    if trc_dict['TRCCO'] == '2100101':
                        tmpBCSTAT = PL_BCSTAT_HCAC
                        tmpstr = 'Ĩ��'
                    else:
                        tmpBCSTAT = PL_BCSTAT_ACC
                        tmpstr = '����'
                        
                    stat_dict = {}
                    if not rccpsState.getTransStateSet(hpdzmx_list[i]['BJEDTE'],hpdzmx_list[i]['BSPSQN'],tmpBCSTAT,PL_BDWFLG_SUCC,stat_dict):
                        AfaLoggerFunc.tradeInfo("��ˮ״̬�Ǽǲ�����" + tmpstr + "״̬,��ʼ��ѯ�̿�״̬")
                        if not rccpsState.getTransStateSet(hpdzmx_list[i]['BJEDTE'],hpdzmx_list[i]['BSPSQN'],PL_BCSTAT_SHORT,PL_BDWFLG_SUCC,stat_dict):
                            rccpsCronFunc.cronExit("S999","��ѯ�̿�״̬�쳣")
                        
                    file_line = file_line + stat_dict['SBAC'].ljust(32,' ')    + '|' #�跽�˺�
                    file_line = file_line + stat_dict['ACNM'].ljust(62,' ')    + '|' #�跽����
                    file_line = file_line + "".ljust(62,' ')                   + '|' #�跽��ַ
                    file_line = file_line + hpdzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #�����к�
                    file_line = file_line + hpdzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #��������
                    file_line = file_line + stat_dict['RBAC'].ljust(32,' ')    + '|' #�����˺�
                    file_line = file_line + stat_dict['OTNM'].ljust(62,' ')    + '|' #��������
                    file_line = file_line + "".ljust(62,' ')                   + '|' #������ַ
                else:
                    #===����ֱ��ȡ�Ǽǲ���ѯ������ѯ���Ľ�����˺���Ϣ=========
                    file_line = file_line + trc_dict['SBAC'].ljust(32,' ')     + '|' #�跽�˺�
                    file_line = file_line + trc_dict['ACNM'].ljust(62,' ')     + '|' #�跽����
                    file_line = file_line + "".ljust(62,' ')                   + '|' #�跽��ַ
                    file_line = file_line + hpdzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #�����к�
                    file_line = file_line + hpdzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #��������
                    file_line = file_line + trc_dict['RBAC'].ljust(32,' ')     + '|' #�����˺�
                    file_line = file_line + trc_dict['OTNM'].ljust(62,' ')     + '|' #��������
                    file_line = file_line + "".ljust(62,' ')                   + '|' #������ַ
                    
                if hpdzmx_list[i]['TRCCO'] == '2100100':
                    file_line = file_line + str(hpdzmx_list[i]['OCCAMT'])      + '|' #���׽��(�⸶ҵ��,���׽��ȡʵ�ʽ�����)
                elif hpdzmx_list[i]['TRCCO'] == '2100101' and trc_dict['BBSSRC'] != '3':
                    file_line = file_line + "-" + str(hpdzmx_list[i]['BILAMT'])+ '|' #���׽��(����ҵ�����ʽ���Դ�Ǵ�����,���׽��ȡ����Ʊ���)
                else:
                    file_line = file_line + str(hpdzmx_list[i]['BILAMT'])      + '|' #���׽��(�ǳ����ͽ⸶ҵ��,���׽��ȡ��Ʊ���)
                    
                file_line = file_line + "".ljust(1,' ')                        + '|' #��¼״̬
                if hpdzmx_list[i]['TRCCO'] == '2100100':
                    file_line = file_line + "1".ljust(62,' ')                  + '|' #�����ֶ�1(�⸶ҵ��,��Ҫ��ת,��1)
                else:
                    file_line = file_line + "0".ljust(62,' ')                  + '|' #�����ֶ�1(�ǽ⸶ҵ��,����Ҫ��ת,��0)
                file_line = file_line + "".ljust(62,' ')                       + '|' #�����ֶ�2
                file_line = file_line + "".ljust(62,' ')                       + '|' #�����ֶ�3
                file_line = file_line + "".ljust(62,' ')                       + '|' #�����ֶ�4
                file_line = file_line + "\n"
                
        fp.write(file_line)
        
        fp.close()
        
        #====================ת�����������ļ�����==============================
        sFileName = "RCCPSHPDZMX" + NCCWKDAT
        dFileName = "RCCPSFILE.HP"  + NCCWKDAT
        
        if not rccpsCronFunc.FormatFile("1","rccps01.fld",sFileName,dFileName):
            rccpsCronFunc.cronExit("S999","ת�����������ļ������쳣")
            
        AfaLoggerFunc.tradeInfo(">>>�������ɻ�Ʊ���������ļ�")
        
        #================FTP�ļ�������=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼFTP�ļ�������")
        if not rccpsFtpFunc.putHost(dFileName):
            rccpsCronFunc.cronExit("S999","FTP�ļ��������쳣")
            
        AfaLoggerFunc.tradeInfo(">>>����FTP�ļ�������")
        
        #================��ʼע����������======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼע����������")
        
        #================��ȡ�ܱ������ܽ��====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡ�ܱ������ܽ��")
        
        #��Ʊ�⸶ҵ��,���ȡʵ�ʽ�����
        sql = "select count(*),sum(OCCAMT) from rcc_hpdzmx where NCCWKDAT in " + LNCCWKDAT
        sql = sql + " and TRCCO in ('2100100') "
        
        records1 = AfaDBFunc.SelectSql(sql)
        
        if records1 == None:
            rccpsCronFunc.cronExit("S999","��ȡ�ܱ������ܽ���쳣")
            
        else:
            AfaLoggerFunc.tradeInfo("count:[" + str(records1[0][0]) + "],sum:[" + str(records1[0][1]) + "]")
            rec_count1 = 0
            rec_sum1   = 0.00
            
            if records1[0][0] > 0:
                rec_count1 = records1[0][0]
                rec_sum1   = records1[0][1]
        
        #�ǻ�Ʊ�⸶ҵ��,���ȡ��Ʊ���
        sql = "select count(*),sum(BILAMT) from rcc_hpdzmx where NCCWKDAT in " + LNCCWKDAT
        sql = sql + " and TRCCO not in ('2100100') "
        
        records2 = AfaDBFunc.SelectSql(sql)
        
        if records2 == None:
            rccpsCronFunc.cronExit("S999","��ȡ�ܱ������ܽ���쳣")
            
        else:
            AfaLoggerFunc.tradeInfo("count:[" + str(records2[0][0]) + "],sum:[" + str(records2[0][1]) + "]")
            rec_count2 = 0
            rec_sum2   = 0.00
            
            if records2[0][0] > 0:
                rec_count2 = records2[0][0]
                rec_sum2   = records2[0][1]
                
        rec_count = rec_count1 + rec_count2
        rec_sum   = rec_sum1   + rec_sum2
            
        AfaLoggerFunc.tradeInfo("���˵Ǽǲ�����������" + LNCCWKDAT + "���ױ���[" + str(rec_count) + "]���׽��[" + str(rec_sum) + "]")
        
        AfaLoggerFunc.tradeInfo(">>>������ȡ�ܱ������ܽ��")
        
        TradeContext.HostCode = '8826'
        TradeContext.BESBNO   = PL_BESBNO_BCLRSB
        TradeContext.BETELR   = PL_BETELR_AUTO
        TradeContext.NBBH     = 'RCC'
        TradeContext.COUT     = rec_count
        TradeContext.TOAM     = rec_sum
        TradeContext.FINA     = 'HP' + NCCWKDAT
        
        #================����ע����������======================================
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo("errorCode = [" + TradeContext.errorCode + "]")
        AfaLoggerFunc.tradeInfo("errorMsg  = [" + TradeContext.errorMsg + "]")
        
        #================�ж�ע���������˷�����Ϣ==============================
        
        if TradeContext.errorCode != '0000':
            rccpsCronFunc.cronExit("S999","ע�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ע����������")
        
        #================�رջ�Ʊ���˴����ļ����ɼ����͵�����ϵͳ����==========
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ʊ���˴����ļ����ɼ����͵�����ϵͳ����")
        if not rccpsCronFunc.closeCron("00045"):
            rccpsCronFunc.cronExit("S999","�رջ�Ʊ���˴����ļ����ɼ����͵����������쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ʊ���˴����ļ����ɼ����͵�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ũ������Ʊ�����ļ����ɼ����͵�����[rccpsHPDZMXPutFile]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHPDZMXPutFile]�����ж�***')

        sys.exit(-1)
