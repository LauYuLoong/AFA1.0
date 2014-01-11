# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).��������֪ͨ���Ľ���
#===============================================================================
#   ģ���ļ�:   TRCC006_1122.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-18
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsFtpFunc,rccpsUtilTools
import rccpsDBTrcc_pbdata,rccpsDBTrcc_paybnk,rccpsDBTrcc_cadbnk
import rccpsMap0000Dout_context2CTradeContext,rccpsMap1122CTradeContext2Dpbdata


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***����.���������(1.���ز���).��������֪ͨ���Ľ���[TRCC006_1122]����***' )
    
    #=================�ж��Ƿ��ظ�����==========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�ж��Ƿ��ظ�����")
    
    pbdata_where_dict = {}
    pbdata_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    pbdata_where_dict['TRCDAT']   = TradeContext.TRCDAT
    pbdata_where_dict['TRCNO']    = TradeContext.TRCNO
    
    pbdata_dict = rccpsDBTrcc_pbdata.selectu(pbdata_where_dict)
    
    if pbdata_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","�ж��Ƿ��ظ�����,��ѯ�������ݵǼǲ���ͬ�����쳣")
        
    if len(pbdata_dict) > 0:
        AfaLoggerFunc.tradeInfo("�������ݵǼǲ��д�����ͬ����,�ظ�����,������һ����")
        #======ΪͨѶ��ִ���ĸ�ֵ===================================================
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '���ڱ���'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        return True
    
    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ��ظ�����")
    
    #=================���ع��������ļ�==========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ���ع��������ļ�")
    
    rccps_path_list = TradeContext.PBDAFILE.split('/')
    
    file_path = AfaUtilTools.trim(rccps_path_list[len(rccps_path_list)-2] + "/" + rccps_path_list[len(rccps_path_list)-1])
    
    if not rccpsFtpFunc.getRccps(file_path):
        return AfaFlowControl.ExitThisFlow("S999","���ع��������ļ�" + file_path + "�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�������ع��������ļ�")
    
    #=================�Ǽǹ�������֪ͨ�Ǽǲ�====================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǹ�������֪ͨ�Ǽǲ�")
    
    pbdata_insert_dict = {}
    if not rccpsMap1122CTradeContext2Dpbdata.map(pbdata_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","Ϊ��������֪ͨ�Ǽǲ���ֵ�쳣")
    
    ret = rccpsDBTrcc_pbdata.insert(pbdata_insert_dict)
    
    if ret <= 0:
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǹ�������֪ͨ�Ǽǲ��쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǹ�������֪ͨ�Ǽǲ�")
    
    #=================������յ�������==========================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ������յ�������")
    
    local_file_home = os.environ['AFAP_HOME'] + "/data/rccps/"
    #AfaLoggerFunc.tradeInfo(local_file_home + file_path)
    
    #=================ũ�����ʽ�����ϵͳ�����к�================================
    if TradeContext.PBDATYP == '001':
        AfaLoggerFunc.tradeInfo(">>>��ʼ���������кű�ũ�����ʽ�����ϵͳ�����к�")
        
        pfile = open(local_file_home + file_path,"rb")
        file_line = " "
        
        while file_line:
            file_line = AfaUtilTools.trim(pfile.readline())   
            file_line = rccpsUtilTools.replaceRet(file_line)
            
            if file_line == "":
                continue
                
            line_list = file_line.split('|')
            
            paybnk_where_dict = {}
            paybnk_where_dict['BANKBIN'] = line_list[0]
            tmp_paybnk_dict = rccpsDBTrcc_paybnk.selectu(paybnk_where_dict)
            if tmp_paybnk_dict == None:
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                return AfaFlowControl.ExitThisFlow("S999","��ѯ���Ǽ��к��Ƿ�����쳣")
            
            paybnk_dict = {}
            paybnk_dict['BANKBIN']      = line_list[0][:10]
            paybnk_dict['BANKSTATUS']   = line_list[1][:1]
            paybnk_dict['BANKATTR']     = line_list[2][:2]
            paybnk_dict['STLBANKBIN']   = line_list[3][:10]
            paybnk_dict['BANKNAM']      = line_list[4][:60]
            paybnk_dict['BANKADDR']     = line_list[5][:60]
            paybnk_dict['BANKPC']       = line_list[6][:6]
            paybnk_dict['BANKTEL']      = line_list[7][:30]
            paybnk_dict['EFCTDAT']      = line_list[8][:8]
            paybnk_dict['INVDAT']       = line_list[9][:8]
            paybnk_dict['ALTTYPE']      = line_list[10][:1]
            paybnk_dict['PRIVILEGE']    = line_list[11][:20]
            paybnk_dict['STRINFO']      = line_list[12][:60]
            
            if len(tmp_paybnk_dict) <= 0:
                #=====�����кű��в����ڴ��к�,�������к�=======================
                ret = rccpsDBTrcc_paybnk.insert(paybnk_dict)
                AfaLoggerFunc.tradeInfo("�������к�")
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                    return AfaFlowControl.ExitThisFlow("S999","�������к��쳣")
                    
            else:
                #=====�����кű��д��ڴ��к�,�����к���Ϣ=======================
                ret = rccpsDBTrcc_paybnk.update(paybnk_dict,paybnk_where_dict)
                AfaLoggerFunc.tradeInfo("���¾��к�")
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                    return AfaFlowControl.ExitThisFlow("S999","���¾��к��쳣")
            
        
        AfaLoggerFunc.tradeInfo(">>>�������������кű�ũ�����ʽ�����ϵͳ�����к�")
        
    #=================��Լ���ϵͳ�����к�======================================
    elif TradeContext.PBDATYP == '011':
        AfaLoggerFunc.tradeInfo(">>>��ʼ���������кű���Լ���ϵͳ�����к�")
        
        pfile = open(local_file_home + file_path,"rb")
        file_line = " "
        
        while file_line:
            file_line = AfaUtilTools.trim(pfile.readline())
            file_line = rccpsUtilTools.replaceRet(file_line)
            
            if file_line == "":
                continue
            
            line_list = file_line.split('|')
            
            paybnk_where_dict = {}
            paybnk_where_dict['BANKBIN'] = line_list[0]
            
            tmp_paybnk_dict = rccpsDBTrcc_paybnk.selectu(paybnk_where_dict)
            
            if tmp_paybnk_dict == None:
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                return AfaFlowControl.ExitThisFlow("S999","��ѯ���Ǽ��к��Ƿ�����쳣")
            
            paybnk_dict = {}
            paybnk_dict['BANKBIN']      = line_list[0][:10]
            paybnk_dict['BANKNAM']      = line_list[1][:60]
            paybnk_dict['BANKADDR']     = line_list[2][:60]
            paybnk_dict['BANKPC']       = line_list[3][:6]
            paybnk_dict['BANKTEL']      = line_list[4][:30]
            paybnk_dict['EFCTDAT']      = line_list[5][:8]
            paybnk_dict['INVDAT']       = line_list[6][:8]
            paybnk_dict['ALTTYPE']      = line_list[7][:1]
            paybnk_dict['NEWOFLG']      = line_list[8][:1]
            paybnk_dict['STRINFO']      = line_list[9][:60]
            
            if len(tmp_paybnk_dict) <= 0:
                #=====�����кű��в����ڴ��к�,�������к�=========
                ret = rccpsDBTrcc_paybnk.insert(paybnk_dict)
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                    return AfaFlowControl.ExitThisFlow("S999","�������к��쳣")
                    
            else:
                #=====�����кű��д��ڴ��к�,�����к���Ϣ=========
                ret = rccpsDBTrcc_paybnk.update(paybnk_dict,paybnk_where_dict)
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                    return AfaFlowControl.ExitThisFlow("S999","�������к��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�������������кű���Լ���ϵͳ�����к�")
        
    #=================�����·�֪ͨ==============================================
    elif TradeContext.PBDATYP == '002':
        AfaLoggerFunc.tradeInfo(">>>��ʼ���������·�֪ͨ")
        
        AfaLoggerFunc.tradeInfo(">>>�����·�֪ͨ�ļ�,��������")
        
        AfaLoggerFunc.tradeInfo(">>>�������������·�֪ͨ")
        
    #=================�����Ϣ�嵥==============================================
    elif TradeContext.PBDATYP == '003':
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������Ϣ�嵥")
        
        #=============Ϊ�����Ϣ�嵥�ļ���̧ͷ==================================
        file = ""
        file = file + "\n"
        file = file + "                    �ϴ�ũ�����ʽ��������Ĵ����Ϣ��                    " + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "    ��Ա�кţ�1340000008  ��Ա����������ʡ������������    " + "\n"
        file = file + "\n"
        file = file + "".ljust(145,"-")
        file = file + "\n"
        file = file + "�˺�".ljust(18," ")     + "|"
        file = file + "����".ljust(60," ")     + "|"
        file = file + "����".ljust(20," ")     + "|"
        file = file + "����".ljust(10," ")     + "|"
        file = file + "��Ϣ��".ljust(8," ")    + "|"
        file = file + "��Ϣ��".ljust(8," ")    + "|"
        file = file + "��Ϣ���".ljust(14," ") + "\n"
        file = file + "".ljust(145,"-")
        file = file + "\n"
        
        pfile = open(local_file_home + file_path,"rb")
        file = file + pfile.read()
        
        pfile.close
        
        file = file + "".ljust(145,"-")
        file = file + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "��ӡ����:                ����:                 ����:                " + "\n"
        
        pfile = open(local_file_home + file_path,"wb")
        pfile.write(file)
        
        pfile.close()
        
        AfaLoggerFunc.tradeInfo(">>>������������Ϣ�嵥")
        
    #=================͸֧��Ϣ�嵥==============================================
    elif TradeContext.PBDATYP == '004':
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������Ϣ�嵥")
        
        #=============Ϊ͸֧��Ϣ�嵥�ļ���̧ͷ==================================
        file = ""
        file = file + "\n"
        file = file + "                    �ϴ�ũ�����ʽ��������Ĵ��͸֧��Ϣ��                    " + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "    ��Ա�кţ�1340000008  ��Ա����������ʡ������������    " + "\n"
        file = file + "\n"
        file = file + "".ljust(145,"-")
        file = file + "\n"
        file = file + "�˺�".ljust(18," ")     + "|"
        file = file + "����".ljust(60," ")     + "|"
        file = file + "͸֧����".ljust(20," ") + "|"
        file = file + "͸֧����".ljust(10," ") + "|"
        file = file + "��Ϣ��".ljust(8," ")    + "|"
        file = file + "��Ϣ��".ljust(8," ")    + "|"
        file = file + "��Ϣ���".ljust(14," ") + "\n"
        file = file + "".ljust(145,"-")
        file = file + "\n"
        
        pfile = open(local_file_home + file_path,"rb")
        file = file + pfile.read()
        
        pfile.close
        
        file = file + "".ljust(145,"-")
        file = file + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "��ӡ����:                ����:                 ����:                " + "\n"
        
        pfile = open(local_file_home + file_path,"wb")
        pfile.write(file)
        
        pfile.close()
        
        AfaLoggerFunc.tradeInfo(">>>������������Ϣ�嵥")
        
    #=================�����ѿ����嵥============================================
    elif TradeContext.PBDATYP == '005':
        AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ������ѿ����嵥")
        
        #=============Ϊ�����ѿ����嵥�ļ���̧ͷ==================================
        file = ""
        file = file + "\n"
        file = file + "                    ũ�����ʽ���������ҵ�������ѿۻ���                    " + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "    ��Ա�кţ�1340000008  ��Ա����������ʡ������������    " + "\n"
        file = file + "\n"
        file = file + "".ljust(268,"-")
        file = file + "\n"
        file = file + "�˺�".ljust(18," ")              + "|"
        file = file + "����".ljust(60," ")              + "|"
        file = file + "��ʼ����".ljust(8," ")           + "|"
        file = file + "��ֹ����".ljust(8," ")           + "|"
        file = file + "�Ʒ��ܽ��".ljust(15," ")        + "|"
        file = file + "�ۿ���".ljust(11," ")             + "|"
        file = file + "�۷��ܽ��".ljust(15," ")        + "|"
        file = file + "����ۼƱ���".ljust(10," ")      + "|"
        file = file + "���������/��".ljust(13," ")     + "|"
        file = file + "��ҼƷѽ��".ljust(16," ")      + "|"
        file = file + "��Ʊ�ۼƱ���".ljust(10," ")      + "|"
        file = file + "��Ʊ������/��".ljust(13," ")     + "|"
        file = file + "��Ʊ�Ʒѽ��".ljust(16, " ")     + "|"
        file = file + "ͨ��ͨ���ۼƱ���".ljust(10," ")  + "|"
        file = file + "ͨ��ͨ��������/��".ljust(13," ") + "|"
        file = file + "ͨ��ͨ�ҼƷѽ��".ljust(16," ")  + "\n"
        file = file + "".ljust(268,"-")
        file = file + "\n"
        
        pfile = open(local_file_home + file_path,"rb")
        file = file + pfile.read()
        
        pfile.close
        
        file = file + "".ljust(268,"-")
        file = file + "\n"
        file = file + "\n"
        file = file + "\n"
        file = file + "��ӡ����:                ����:                 ����:                " + "\n"
        
        pfile = open(local_file_home + file_path,"wb")
        pfile.write(file)
        
        pfile.close()
        
        AfaLoggerFunc.tradeInfo(">>>�����Ǽ������ѿ����嵥")
        
    #=================��BIN���кŶ���===========================================
    elif TradeContext.PBDATYP == '006':
        AfaLoggerFunc.tradeInfo(">>>��ʼ���¿�BIN���кŶ��ձ�")
        
        pfile = open(local_file_home + file_path,"r")
        file_line = " "
        
        while file_line:
            file_line = AfaUtilTools.trim(pfile.readline())
            file_line = rccpsUtilTools.replaceRet(file_line)
            #AfaLoggerFunc.tradeInfo("file_line = [" + file_line + "]")
            
            if file_line == "":
                continue
                
            line_list = file_line.split('|')
            
            cadbnk_where_dict = {}
            cadbnk_where_dict['CARDBIN'] = line_list[0][:12]
            
            tmp_cadbnk_dict = rccpsDBTrcc_cadbnk.selectu(cadbnk_where_dict)
            
            if tmp_cadbnk_dict == None:
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                return AfaFlowControl.ExitThisFlow("S999","��ѯ���Ǽǿ�BIN�Ƿ�����쳣")
            
            cadbnk_dict = {}
            cadbnk_dict['CARDBIN']      = line_list[0][:12]
            cadbnk_dict['BANKBIN']      = line_list[1][:10]
            
            if len(tmp_cadbnk_dict) <= 0:
                #=====�����кű��в����ڴ˿�BIN,�����¿�BIN===================
                ret = rccpsDBTrcc_cadbnk.insert(cadbnk_dict)
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                    return AfaFlowControl.ExitThisFlow("S999","�����¿�BIN�쳣")
                    
            else:
                #=====�����кű��д��ڴ˿�BIN,���¿�BIN========================
                ret = rccpsDBTrcc_cadbnk.update(cadbnk_dict,cadbnk_where_dict)
                if ret <= 0:
                    if not AfaDBFunc.RollbackSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                    return AfaFlowControl.ExitThisFlow("S999","�����¿�BIN�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�������¿�BIN���кŶ��ձ�")
        
        
    AfaLoggerFunc.tradeInfo(">>>����������յ�������")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    #======ΪͨѶ��ִ���ĸ�ֵ===================================================
    out_context_dict = {}
    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO
    out_context_dict['PRCCO']    = 'RCCI0000'
    out_context_dict['STRINFO']  = '�ɹ�'
    
    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
    
    AfaLoggerFunc.tradeInfo( '***����.���������(1.���ز���).��������֪ͨ���Ľ���[TRCC006_1122]�˳�***' )
    
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***����.���������(2.���Ļ�ִ).��������֪ͨ���Ľ���[TRCC006_1122]����***' )
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo( '***����.���������(2.���Ļ�ִ).��������֪ͨ���Ľ���[TRCC006_1122]�˳�***' )
    return True
        
