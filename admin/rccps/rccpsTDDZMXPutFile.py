# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ũ����ͨ��ͨ���ļ����ɼ����͵�����
#===============================================================================
#   �����ļ�:   rccpsTDDZMXPutFile.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-12-10
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc,rccpsDBFunc,rccpsState,rccpsHostFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_tddzmx

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ũ����ͨ��ͨ�Ҵ����ļ����ɼ����͵�����[rccpsHDDZMXPutFile]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #================����ͨ��ͨ�Ҷ�����ϸ�Ǽǲ�,����ͨ��ͨ�����������ļ�============
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ͨ��ͨ�����������ļ�")
        
        tddzmx_where_sql = "NCCWKDAT in " + LNCCWKDAT
        tddzmx_where_sql = tddzmx_where_sql + " and ((trcco in ('3000002','3000003','3000004','3000005') and confflg = '1') or (trcco in ('3000102','3000103','3000104','3000105') and confflg = '0')) and cancflg = '0'"
        tddzmx_where_sql = tddzmx_where_sql + " and not exists (select * from rcc_tddzcz where rcc_tddzmx.sndbnkco = rcc_tddzcz.sndbnkco and rcc_tddzmx.trcdat = rcc_tddzcz.trcdat and rcc_tddzmx.trcno = rcc_tddzcz.trcno )"
        
        tddzmx_list = rccpsDBTrcc_tddzmx.selectm(1,0,tddzmx_where_sql,"")
        
        if tddzmx_list == None:
            rccpsCronFunc.cronExit("S999","��ѯͨ��ͨ�Ҷ�����ϸ�Ǽǲ��쳣")
            
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/RCCPSTDDZMX" + NCCWKDAT
        
        fp = open(file_path,"wb")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ���(����)��ϸ�ļ��쳣")
            
        file_line = ""
        
        if len(tddzmx_list) <= 0:
            AfaLoggerFunc.tradeInfo(">>>ͨ��ͨ�Ҷ�����ϸ�Ǽǲ����޶�Ӧ��¼")
        else:
            for i in xrange(len(tddzmx_list)):
                
                
                trc_dict = {}
                if not rccpsDBFunc.getTransWtr(tddzmx_list[i]['BJEDTE'],tddzmx_list[i]['BSPSQN'],trc_dict):
                    rccpsCronFunc.cronExit("S999","��ѯ������Ϣ�쳣")
                
                
                
                #=======����������ʶ��ȡ�������Ϣ================================
                if trc_dict['BRSFLG'] == PL_BRSFLG_SND:
                    #===���˲�ѯ����״̬��Ϣ�еĽ�����˺���Ϣ==================
                    stat_dict = {}
                    if not rccpsState.getTransStateSet(tddzmx_list[i]['BJEDTE'],tddzmx_list[i]['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,stat_dict):
                        rccpsCronFunc.cronExit("S999","��ѯ����״̬�쳣")
                        
                    file_line = file_line + "RCC".ljust(8,' ')                 + '|' #����ҵ���
                    file_line = file_line + stat_dict['FEDT'].ljust(8,' ')     + '|' #ǰ������
                    file_line = file_line + stat_dict['RBSQ'].ljust(12,' ')    + '|' #ǰ����ˮ��
                    file_line = file_line + tddzmx_list[i]['SNDBNKCO'].ljust(12,' ') + '|' #�����к�
                    file_line = file_line + tddzmx_list[i]['SNDBNKNM'].ljust(62,' ') + '|' #��������
                    file_line = file_line + trc_dict['BRSFLG'].ljust(1,' ')    + '|' #������ʶ
                    file_line = file_line + "".ljust(5,' ')                    + '|' #ҵ������
                    file_line = file_line + stat_dict['SBAC'].ljust(32,' ')    + '|' #�跽�˺�
                    file_line = file_line + stat_dict['ACNM'].ljust(62,' ')    + '|' #�跽����
                    file_line = file_line + "".ljust(62,' ')                   + '|' #�跽��ַ
                    file_line = file_line + tddzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #�����к�
                    file_line = file_line + tddzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #��������
                    file_line = file_line + stat_dict['RBAC'].ljust(32,' ')    + '|' #�����˺�
                    file_line = file_line + stat_dict['OTNM'].ljust(62,' ')    + '|' #��������
                    file_line = file_line + "".ljust(62,' ')                   + '|' #������ַ
                else:
                    #===���˲�ѯ�Զ�����/�Զ��ۿ�״̬��Ϣ�еĽ�����˺���Ϣ==========
                    stat_dict = {}
                    if rccpsState.getTransStateCur(tddzmx_list[i]['BJEDTE'],tddzmx_list[i]['BSPSQN'],stat_dict):
                        AfaLoggerFunc.tradeInfo("��ѯ��ˮ״̬�Ǽǲ��е�ǰ״̬�ɹ�")
                        if not (stat_dict['BCSTAT'] in (PL_BCSTAT_AUTO,PL_BCSTAT_AUTOPAY) and stat_dict['BDWFLG']):
                            rccpsCronFunc.cronExit("S999","���׵�ǰ״̬���Զ����˻��Զ��ۿ�")
                    else:
                        rccpsCronFunc.cronExit("S999","��ˮ״̬�Ǽǲ��е�ǰ״̬�쳣")
                            
                    file_line = file_line + "RCC".ljust(8,' ')                 + '|' #����ҵ���
                    file_line = file_line + stat_dict['FEDT'].ljust(8,' ')     + '|' #ǰ������
                    file_line = file_line + stat_dict['RBSQ'].ljust(12,' ')    + '|' #ǰ����ˮ��
                    file_line = file_line + tddzmx_list[i]['SNDBNKCO'].ljust(12,' ') + '|' #�����к�
                    file_line = file_line + tddzmx_list[i]['SNDBNKNM'].ljust(62,' ') + '|' #��������
                    file_line = file_line + trc_dict['BRSFLG'].ljust(1,' ')    + '|' #������ʶ
                    file_line = file_line + "".ljust(5,' ')                    + '|' #ҵ������
                    file_line = file_line + stat_dict['SBAC'].ljust(32,' ')    + '|' #�跽�˺�
                    file_line = file_line + stat_dict['ACNM'].ljust(62,' ')    + '|' #�跽����
                    file_line = file_line + "".ljust(62,' ')                   + '|' #�跽��ַ
                    file_line = file_line + tddzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #�����к�
                    file_line = file_line + tddzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #��������
                    file_line = file_line + stat_dict['RBAC'].ljust(32,' ')    + '|' #�����˺�
                    file_line = file_line + stat_dict['OTNM'].ljust(62,' ')    + '|' #��������
                    file_line = file_line + "".ljust(62,' ')                   + '|' #������ַ
                    
                file_line = file_line + str(tddzmx_list[i]['OCCAMT'])      + '|'     #���׽��
                file_line = file_line + str(tddzmx_list[i]['CUSCHRG'])      + '|'    #�����ѽ��
                file_line = file_line + "0".ljust(1,' ')                    + '|'    #��¼״̬
                file_line = file_line + "".ljust(62,' ')                  + '|'      #�����ֶ�1
                file_line = file_line + "".ljust(62,' ')                   + '|'     #�����ֶ�2
                file_line = file_line + "".ljust(62,' ')                   + '|'     #�����ֶ�3
                file_line = file_line + "".ljust(62,' ')                   + '|'     #�����ֶ�4
                file_line = file_line + "\n"
                
        fp.write(file_line)
        
        fp.close()
        
        #================ת�����������ļ�����==================================
        sFileName = "RCCPSTDDZMX" + NCCWKDAT
        dFileName = "RCCTDFILE.TD"  + NCCWKDAT
        
        if not rccpsCronFunc.FormatFile("1","tdlsa.fld",sFileName,dFileName):
            rccpsCronFunc.cronExit("S999","ת�����������ļ������쳣")
            
        AfaLoggerFunc.tradeInfo(">>>��������ͨ��ͨ�����������ļ�")
        
        #================FTP�ļ�������=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼFTP�ļ�������")
        if not rccpsFtpFunc.putHost(dFileName):
            rccpsCronFunc.cronExit("S999","FTP�ļ��������쳣")
            
        AfaLoggerFunc.tradeInfo(">>>����FTP�ļ�������")
        
        #================��ʼע����������======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼע����������")
        
        #================��ȡ�ܱ������ܽ��====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡ�ܱ������ܽ��")
        
        sql = "select count(*),sum(OCCAMT),sum(CUSCHRG) from rcc_tddzmx as tab1 where NCCWKDAT in " + LNCCWKDAT
        sql = sql + " and ((trcco in ('3000002','3000003','3000004','3000005') and confflg = '1') or (trcco in ('3000102','3000103','3000104','3000105') and confflg = '0')) and cancflg = '0'"
        sql = sql + " and not exists (select * from rcc_tddzcz as tab2 where tab1.sndbnkco = tab2.sndbnkco and tab1.trcdat = tab2.trcdat and tab1.trcno = tab2.trcno )"
        
        records = AfaDBFunc.SelectSql(sql)
        
        if records == None:
            rccpsCronFunc.cronExit("S999","��ȡ�ܱ������ܽ���쳣")
            
        else:
            rec_count = records[0][0]
            rec_sum   = records[0][1]
            
            if rec_count <= 0:
                rec_count = 0
                rec_sum   = 0.00
            
        AfaLoggerFunc.tradeInfo("���˵Ǽǲ�����������" + LNCCWKDAT + "���ױ���[" + str(rec_count) + "]���׽��[" + str(rec_sum) + "]")
        
        AfaLoggerFunc.tradeInfo(">>>������ȡ�ܱ������ܽ��")
        
        TradeContext.HostCode = '8826'
        TradeContext.BESBNO   = PL_BESBNO_BCLRSB
        TradeContext.BETELR   = PL_BETELR_AUTO
        TradeContext.NBBH     = 'RCC'
        TradeContext.COUT     = rec_count
        TradeContext.TOAM     = rec_sum
        TradeContext.FINA     = 'TD' + NCCWKDAT
        
        #================����ע����������======================================
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo("errorCode = [" + TradeContext.errorCode + "]")
        AfaLoggerFunc.tradeInfo("errorMsg  = [" + TradeContext.errorMsg + "]")
        
        #================�ж�ע���������˷�����Ϣ==============================
        
        if TradeContext.errorCode != '0000':
            rccpsCronFunc.cronExit("S999","ע�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ע����������")
        
        #================�ر�ͨ��ͨ�Ҷ��˴����ļ����ɼ����͵�����ϵͳ����==========
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ�Ҷ��˴����ļ����ɼ����͵�����ϵͳ����")
        if not rccpsCronFunc.closeCron("00065"):
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ�Ҷ��˴����ļ����ɼ����͵����������쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ�Ҷ��˴����ļ����ɼ����͵�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ũ����ͨ��ͨ�Ҵ����ļ����ɼ����͵�����[rccpsHDDZMXPutFile]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHDDZMXPutFile]�����ж�***')

        sys.exit(-1)
