# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ũ������Ҵ����ļ����ɼ����͵�����
#===============================================================================
#   �����ļ�:   rccpsHDDZMXPutFile.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-28
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsFtpFunc,rccpsDBFunc,rccpsState,rccpsHostFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hddzmx

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ũ������Ҵ����ļ����ɼ����͵�����[rccpsHDDZMXPutFile]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #================���ݻ�Ҷ�����ϸ�Ǽǲ�,���ɻ�����������ļ�============
        AfaLoggerFunc.tradeInfo(">>>��ʼ���ɻ�����������ļ�")
        
        hddzmx_where_sql = "NCCWKDAT in " + LNCCWKDAT
        
        hddzmx_list = rccpsDBTrcc_hddzmx.selectm(1,0,hddzmx_where_sql,"")
        
        if hddzmx_list == None:
            rccpsCronFunc.cronExit("S999","��ѯ��Ҷ�����ϸ�Ǽǲ��쳣")
            
        file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/RCCPSHDDZMX" + NCCWKDAT
        
        fp = open(file_path,"wb")
        
        if fp == None:
            rccpsCronFunc.cronExit("S999","�򿪻�Ҷ���(����)��ϸ�ļ��쳣")
            
        file_line = ""
        
        if len(hddzmx_list) <= 0:
            AfaLoggerFunc.tradeInfo(">>>��Ҷ�����ϸ�Ǽǲ����޶�Ӧ��¼")
        else:
            for i in xrange(len(hddzmx_list)):
                
                file_line = file_line + "RCC".ljust(8,' ')                     + '|' #����ҵ���
                file_line = file_line + hddzmx_list[i]['BJEDTE'].ljust(8,' ')  + '|' #ǰ������
                file_line = file_line + hddzmx_list[i]['BSPSQN'].ljust(12,' ') + '|' #ǰ����ˮ��
                
                trc_dict = {}
                if not rccpsDBFunc.getTransTrc(hddzmx_list[i]['BJEDTE'],hddzmx_list[i]['BSPSQN'],trc_dict):
                    rccpsCronFunc.cronExit("S999","��ѯ������Ϣ�쳣")
                
                file_line = file_line + hddzmx_list[i]['SNDBNKCO'].ljust(12,' ') + '|'     #�����к�
                file_line = file_line + hddzmx_list[i]['SNDBNKNM'].ljust(62,' ') + '|'     #��������
                file_line = file_line + trc_dict['BRSFLG'].ljust(1,' ')    + '|'     #������ʶ
                file_line = file_line + "".ljust(5,' ')                    + '|'     #ҵ������
                
                
                #=======����������ʶ��ȡ�������Ϣ================================
                if trc_dict['BRSFLG'] == PL_BRSFLG_SND:
                    #===���˲�ѯ����״̬��Ϣ�еĽ�����˺���Ϣ==================
                    stat_dict = {}
                    if not rccpsState.getTransStateSet(hddzmx_list[i]['BJEDTE'],hddzmx_list[i]['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,stat_dict):
                        rccosCronFunc.cronExit("S999","��ѯ����״̬�쳣")
                        
                    file_line = file_line + stat_dict['SBAC'].ljust(32,' ')    + '|' #�跽�˺�
                    file_line = file_line + stat_dict['ACNM'].ljust(62,' ')    + '|' #�跽����
                    file_line = file_line + "".ljust(62,' ')                   + '|' #�跽��ַ
                    file_line = file_line + hddzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #�����к�
                    file_line = file_line + hddzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #��������
                    file_line = file_line + stat_dict['RBAC'].ljust(32,' ')    + '|' #�����˺�
                    file_line = file_line + stat_dict['OTNM'].ljust(62,' ')    + '|' #��������
                    file_line = file_line + "".ljust(62,' ')                   + '|' #������ַ
                else:
                    #===���˲�ѯ�Զ�����/�Զ�����״̬��Ϣ�еĽ�����˺���Ϣ==========
                    stat_dict = {}
                    if not rccpsState.getTransStateSet(hddzmx_list[i]['BJEDTE'],hddzmx_list[i]['BSPSQN'],PL_BCSTAT_AUTO,PL_BDWFLG_SUCC,stat_dict):
                        AfaLoggerFunc.tradeInfo("��ˮ״̬�Ǽǲ������Զ�����״̬,��ѯ�Զ�����״̬")
                        if not rccpsState.getTransStateSet(hddzmx_list[i]['BJEDTE'],hddzmx_list[i]['BSPSQN'],PL_BCSTAT_HANG,PL_BDWFLG_SUCC,stat_dict):
                            rccpsCronFunc.cronExit("S999","��ѯ�Զ�����״̬�쳣")
                            
                    file_line = file_line + stat_dict['SBAC'].ljust(32,' ')    + '|' #�跽�˺�
                    file_line = file_line + stat_dict['ACNM'].ljust(62,' ')    + '|' #�跽����
                    file_line = file_line + "".ljust(62,' ')                   + '|' #�跽��ַ
                    file_line = file_line + hddzmx_list[i]['RCVBNKCO'].ljust(12,' ') + '|' #�����к�
                    file_line = file_line + hddzmx_list[i]['RCVBNKNM'].ljust(62,' ') + '|' #��������
                    file_line = file_line + stat_dict['RBAC'].ljust(32,' ')    + '|' #�����˺�
                    file_line = file_line + stat_dict['OTNM'].ljust(62,' ')    + '|' #��������
                    file_line = file_line + "".ljust(62,' ')                   + '|' #������ַ
                    
                file_line = file_line + str(hddzmx_list[i]['OCCAMT'])      + '|'     #���׽��
                file_line = file_line + "".ljust(1,' ')                    + '|'     #��¼״̬
                file_line = file_line + "1".ljust(62,' ')                  + '|'     #�����ֶ�1(��Ҫ��ת,��1)
                file_line = file_line + "".ljust(62,' ')                   + '|'     #�����ֶ�2
                file_line = file_line + "".ljust(62,' ')                   + '|'     #�����ֶ�3
                file_line = file_line + "".ljust(62,' ')                   + '|'     #�����ֶ�4
                file_line = file_line + "\n"
                
        fp.write(file_line)
        
        fp.close()
        
        #================ת�����������ļ�����==================================
        sFileName = "RCCPSHDDZMX" + NCCWKDAT
        dFileName = "RCCPSFILE.HD"  + NCCWKDAT
        
        if not rccpsCronFunc.FormatFile("1","rccps01.fld",sFileName,dFileName):
            rccpsCronFunc.cronExit("S999","ת�����������ļ������쳣")
            
        AfaLoggerFunc.tradeInfo(">>>�������ɻ�����������ļ�")
        
        #================FTP�ļ�������=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼFTP�ļ�������")
        if not rccpsFtpFunc.putHost(dFileName):
            rccpsCronFunc.cronExit("S999","FTP�ļ��������쳣")
            
        AfaLoggerFunc.tradeInfo(">>>����FTP�ļ�������")
        
        #================��ʼע����������======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼע����������")
        
        #================��ȡ�ܱ������ܽ��====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡ�ܱ������ܽ��")
        
        sql = "select count(*),sum(OCCAMT) from rcc_hddzmx where NCCWKDAT in " + LNCCWKDAT
        
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
        TradeContext.FINA     = 'HD' + NCCWKDAT
        
        #================����ע����������======================================
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo("errorCode = [" + TradeContext.errorCode + "]")
        AfaLoggerFunc.tradeInfo("errorMsg  = [" + TradeContext.errorMsg + "]")
        
        #================�ж�ע���������˷�����Ϣ==============================
        
        if TradeContext.errorCode != '0000':
            rccpsCronFunc.cronExit("S999","ע�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ע����������")
        
        #================�رջ�Ҷ��˴����ļ����ɼ����͵�����ϵͳ����==========
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ҷ��˴����ļ����ɼ����͵�����ϵͳ����")
        if not rccpsCronFunc.closeCron("00035"):
            rccpsCronFunc.cronExit("S999","�رջ�Ҷ��˴����ļ����ɼ����͵����������쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ҷ��˴����ļ����ɼ����͵�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ũ������Ҵ����ļ����ɼ����͵�����[rccpsHDDZMXPutFile]�˳�***")
    
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
