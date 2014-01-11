# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��Ʊ���˴��˴���
#===============================================================================
#   �����ļ�:   rccpsHPDZCZModify.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-27
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc,time
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc,rccpsHostFunc,rccpsFunc,rccpsGetFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hpdzcz,rccpsDBTrcc_sstlog,rccpsDBTrcc_bilbka,rccpsDBTrcc_hpdzmx
import rccpsMap0000Dhpdzmx2CTradeContext,rccpsMap0000Dbilbka2CTradeContext,rccpsMap0000Dbilinf2CTradeContext,rccpsMap1113CTradeContext2Dbilbka


if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊ���˴��˴���[rccpsHPDZCZModify]����***")
        
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
        
        #================����������,������======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '01' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������������������������,��ϵͳ���ý���״̬ΪĨ�˳ɹ�,�ɹ����޸Ĵ��˴����ʶΪ�Ѵ���")
            
            for i in xrange(len(hpdzcz_list)):
                #========����״̬Ϊ����=========================================
                AfaLoggerFunc.tradeInfo("��ʼ�޸�ԭ����״̬Ϊ����")
                
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========���ý���״̬Ϊ����ɹ�=================================
                if not rccpsState.newTransState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_LONG,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '���ó���ɹ�״̬�쳣')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                AfaLoggerFunc.tradeInfo("�����޸�ԭ����״̬Ϊ����")
                
                #========�޸Ĵ��˴����ʶΪ�Ѵ���===============================
                hpdzcz_update_dict = {}
                hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hpdzcz_where_dict = {}
                hpdzcz_where_dict['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                hpdzcz_where_dict['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                
                ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #================����������,������======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '02' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������Ϊϵͳ�쳣,��Ƽ���Ա��ʵ����")
            #for i in xrange(len(hpdzcz_list)):
            #    hpdzcz_update_dict = {}
            #    hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hpdzcz_where_dict = {}
            #    hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
            #    hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
            #    hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
            #    
            #    ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #================������������,����δ����================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����������������,����δ��������")
        
        hpdzcz_where_sql = "nccwkdat = '" + NCCWKDAT + "' and eactyp = '03' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������Ϊϵͳ�쳣,��Ƽ���Ա��ʵ����")
            for i in xrange(len(hpdzcz_list)):
                #========����״̬Ϊ����=========================================
                AfaLoggerFunc.tradeInfo("��ʼ�޸�ԭ����״̬Ϊ����")
                
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========���ý���״̬Ϊ����ɹ�=================================
                if not rccpsState.newTransState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_LONG,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '���ó���ɹ�״̬�쳣')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                AfaLoggerFunc.tradeInfo("�����޸�ԭ����״̬Ϊ����")
                
                #========�޸Ĵ��˴����ʶΪ�Ѵ���===============================
                hpdzcz_update_dict = {}
                hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hpdzcz_where_dict = {}
                hpdzcz_where_dict['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                hpdzcz_where_dict['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                
                ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������������������,����δ��������")
        
        #================��������δ����,��������================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������δ����,������������")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '04' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������������������������,��ϵͳ���ý���״̬Ϊ����\�̿�ɹ�,�ɹ����޸Ĵ��˴����ʶΪ�Ѵ���")
            
            for i in xrange(len(hpdzcz_list)):
                tmp_stat_where_dict = {}
                tmp_stat_where_dict['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                tmp_stat_where_dict['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                tmp_stat_where_dict['BCSTAT'] = PL_BCSTAT_ACC
                tmp_stat_where_dict['BDWFLG'] = PL_BDWFLG_SUCC
                
                tmp_stat_dict = {}
                tmp_stat_dict = rccpsDBTrcc_sstlog.selectu(tmp_stat_where_dict)
                
                if tmp_stat_dict == None:
                    AfaCronFunc.cronExit('S999','��ѯ���׼���״̬�쳣')
                #if not rccpsState.getTransStateSet(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,tmp_stat_dict):
                HPSTAT = ''
                if hpdzcz_list[i]['TRCCO'] == '2100001':
                    #��Ʊǩ��
                    HPSTAT = PL_HPSTAT_SIGN
                elif hpdzcz_list[i]['TRCCO'] == '2100100':
                    #��Ʊ�⸶
                    HPSTAT = PL_HPSTAT_PAYC
                elif hpdzcz_list[i]['TRCCO'] == '2100101':
                    #��Ʊ����
                    HPSTAT = PL_HPSTAT_CANC
                elif hpdzcz_list[i]['TRCCO'] == '2100102':
                    #��Ʊ��ʧ
                    HPSTAT = PL_HPSTAT_HANG
                elif hpdzcz_list[i]['TRCCO'] == '2100103':
                    #��Ʊ��Ʊ
                    HPSTAT = PL_HPSTAT_RETN
                elif hpdzcz_list[i]['TRCCO'] == '2100104':
                    #��Ʊ���
                    HPSTAT = PL_HPSTAT_DEHG
                
                #ҵ��״̬�޼���״̬���ҷǻ�Ʊ��ʧ�ͻ�Ʊ��ҽ���
                if len(tmp_stat_dict) <= 0 and hpdzcz_list[i]['TRCCO'] != '2100102' and hpdzcz_list[i]['TRCCO'] != '2100104':
                    AfaLoggerFunc.tradeInfo("�˽��׷ǻ�Ʊ��ʧ\��ҽ���,��δ���˳ɹ�")
                    AfaLoggerFunc.tradeInfo("��̿�")
                    #========��̿�============================================
                    TradeContext.BESBNO = PL_BESBNO_BCLRSB
                    TradeContext.BETELR = PL_BETELR_AUTO
                    
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���ö̿����״̬")
                    
                    #========���ý���״̬Ϊ�̿����==========================
                    if not rccpsState.newTransState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_SHORT,PL_BDWFLG_WAIT):
                        rccpsCronFunc.cronExit('S999', '���ö̿����״̬�쳣')
                    
                    AfaLoggerFunc.tradeInfo(">>>�������ö̿����״̬")
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                        rccCronFunc.cronExit("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬")
                    
                    if not rccpsState.newBilState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],HPSTAT):
                        rccpsCronFunc.cronExit('S999', '���û�Ʊ״̬�쳣')
                    
                    AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬")
                    
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���ö̿�ɹ�״̬")
                    
                    tmp_stat = {}
                    tmp_stat['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                    tmp_stat['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                    
                    tmptrc_dict = {}
                    if not rccpsDBFunc.getTransBil(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],tmptrc_dict):
                        rccpsCronFunc.cronExit('S999', '��ѯ��Ʊ����ҵ����Ϣ�쳣')
                    
                    if not rccpsDBFunc.getInfoBil(tmptrc_dict['BILVER'],tmptrc_dict['BILNO'],tmptrc_dict['BILRS'],tmptrc_dict):
                        rccpsCronFunc.cronExit('S999', '��ѯ��Ʊ��Ϣ�쳣')
                        
                    TradeContext.SBAC     = TradeContext.BESBNO + PL_ACC_NXYDQSWZ  #��ũ��������������
                    TradeContext.ACNM     = "ũ��������������"
                    TradeContext.RBAC     = tmptrc_dict['PYHACC']                     #����Ʊ���˺�
                    TradeContext.OTNM     = tmptrc_dict['PYHNAM']
                    
                    #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
                    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                    
                    tmp_stat['BCSTAT'] = PL_BCSTAT_SHORT
                    tmp_stat['BDWFLG'] = PL_BDWFLG_SUCC
                    
                    if not rccpsState.setTransState(tmp_stat):
                        rccpsCronFunc.cronExit('S999', '���ö̿�ɹ�״̬�쳣')
                    
                    AfaLoggerFunc.tradeInfo(">>>�������ö̿�ɹ�״̬")
                    
                else:
                    AfaLoggerFunc.tradeInfo("������")
                    #========������============================================
                    TradeContext.BESBNO = PL_BESBNO_BCLRSB
                    TradeContext.BETELR = PL_BETELR_AUTO
                    
                    #========���ý���״̬Ϊ���㴦����==========================
                    AfaLoggerFunc.tradeInfo("��ʼ�������㴦����״̬")
                    
                    if not rccpsState.newTransState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_SUCC):
                        rccpsCronFunc.cronExit('S999', '�������㴦����״̬�쳣')
                    
                    AfaLoggerFunc.tradeInfo("�����������㴦����״̬")
                    
                    #COMMIT
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                        rccCronFunc.cronExit("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���û�Ʊ״̬")
                    
                    if not rccpsState.newBilState(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],HPSTAT):
                        rccpsCronFunc.cronExit('S999', '���û�Ʊ״̬�쳣')
                    
                    AfaLoggerFunc.tradeInfo(">>>�������û�Ʊ״̬")
                    
                    AfaLoggerFunc.tradeInfo(">>>��ʼ��������ɹ�״̬")
                    
                    tmp_stat = {}
                    tmp_stat['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
                    tmp_stat['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
                    tmp_stat['BCSTAT'] = PL_BCSTAT_MFESTL
                    tmp_stat['BDWFLG'] = PL_BDWFLG_SUCC
                    
                    if not rccpsState.setTransState(tmp_stat):
                        rccpsCronFunc.cronExit('S999', '��������ɹ�״̬�쳣')
                    
                    AfaLoggerFunc.tradeInfo(">>>������������ɹ�״̬")
                    
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                #========�޸Ĵ��˴����ʶΪ�Ѵ���==============================
                hpdzcz_update_dict = {}
                hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hpdzcz_where_dict = {}
                hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                
                ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����������������δ����,������������")
        
        #================����������,������=====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '05' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������Ϊϵͳ�쳣,��Ƽ���Ա��ʵ����")
            #for i in xrange(len(hpdzcz_list)):
            #    hpdzcz_update_dict = {}
            #    hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hpdzcz_where_dict = {}
            #    hpdzcz_where_dict['BJEDTE'] = hpdzcz_list[i]['BJEDTE']
            #    hpdzcz_where_dict['BSPSQN'] = hpdzcz_list[i]['BSPSQN']
            #    
            #    ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        #================����������,������=====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '06' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴��������貹����,�ɹ����޸Ĵ��˴����ʶΪ�Ѵ���")
            for i in xrange(len(hpdzcz_list)):
                #========������================================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ������")
                
                #========��ʼ������������======================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ��ʼ��������")
                TradeContext.tradeResponse=[]
                
                hpdzmx_where_dict = {}
                hpdzmx_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                hpdzmx_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                hpdzmx_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                
                hpdzmx_dict = rccpsDBTrcc_hpdzmx.selectu(hpdzmx_where_dict)
                
                if hpdzmx_dict == None:
                    rccpsCronFunc.cronExit("S999","��ѯ������ϸ�����쳣")
                    
                if len(hpdzmx_dict) <= 0:
                    rccpsCronFunc.cronExit("S999","�Ǽǲ����޴�������ϸ����")
                
                rccpsMap0000Dhpdzmx2CTradeContext.map(hpdzmx_dict)
                
                TradeContext.OCCAMT = str(TradeContext.OCCAMT)
                TradeContext.TemplateCode  = 'RCC005'
                TradeContext.BRSFLG        = PL_BRSFLG_RCV
                TradeContext.CUR           = '01'
                TradeContext.BILRS         = '0' 
                TradeContext.TransCode = '1113'
                TradeContext.OPRNO     = PL_HPOPRNO_JF
                
                #=====================��ȡϵͳ����ʱ��=========================
                TradeContext.BJEDTE = AfaUtilTools.GetHostDate( )
                #TradeContext.TRCDAT = AfaUtilTools.GetHostDate( )
                TradeContext.BJETIM = AfaUtilTools.GetSysTime( )
                #TradeContext.BJEDTE = PL_BJEDTE     #����,��ʱʹ��
                #TradeContext.TRCDAT = PL_BJEDTE     #����,��ʱʹ��
                
                #=====================ϵͳ����У��=============================
                if not rccpsFunc.ChkPubInfo(PL_BRSFLG_RCV) :
                    raise Exception
                    
                #=====================�����Ϸ���У��===========================
                if not rccpsFunc.ChkUnitInfo( PL_BRSFLG_RCV ) :
                    raise Exception
                
                #=====================��ȡ��������=============================
                TradeContext.NCCworkDate = TradeContext.NCCWKDAT
                
                #=====================��ȡƽ̨��ˮ��===========================
                if rccpsGetFunc.GetSerialno(PL_BRSFLG_RCV) == -1 :
                    raise Exception
                
                #=====================��ȡ������ˮ��===========================
                if rccpsGetFunc.GetRccSerialno( ) == -1 :
                    raise Exception
                
                AfaLoggerFunc.tradeInfo(">>>������ʼ��������")
                
                #=====================�Ǽ�������Ϣ=============================
                AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�������Ϣ")
                
                #=====================����ת��=================================
                if TradeContext.CUR == 'CNY':
                    TradeContext.CUR  = '01'
                
                #=====================��ʼ���ֵ丳ֵ===========================
                bilbka_dict = {}
                if not rccpsMap1113CTradeContext2Dbilbka.map(bilbka_dict):
                    rccpsCronFunc.cronExit('M999', '�ֵ丳ֵ����')
                
                bilbka_dict['DCFLG'] = PL_DCFLG_CRE                  #�����ʶ
                bilbka_dict['OPRNO'] = TradeContext.OPRNO            #ҵ������
                
                #=====================��ʼ�������ݿ�===========================
                if not rccpsDBFunc.insTransBil(bilbka_dict):
                    rccpsCronFunc.cronExit('D002', '�������ݿ��쳣')
                    
                #=====================commit����===============================
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    rccpsCronFunc.cronExit("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                AfaLoggerFunc.tradeInfo('������ҵ��Ǽǲ��ɹ�')
                
                #=====================����״̬Ϊ����===========================
                sstlog   = {}
                sstlog['BSPSQN']   = TradeContext.BSPSQN
                sstlog['BJEDTE']   = TradeContext.BJEDTE
                sstlog['BCSTAT']   = PL_BCSTAT_BNKRCV
                sstlog['BDWFLG']   = PL_BDWFLG_SUCC
                
                #=====================����״̬Ϊ ����-�ɹ�=====================
                if not rccpsState.setTransState(sstlog):
                    rccpsCronFunc.cronExit(TradeContext.errorCode, TradeContext.errorMsg)
                    
                #=====================commit����===============================
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    rccpsCronFunc.cronExit("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                AfaLoggerFunc.tradeInfo(">>>�����Ǽ�������Ϣ")
                
                AfaLoggerFunc.tradeInfo(">>>����������")
                
                #========���»�Ʊ������ϸ�Ǽǲ�================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ���»����ϸ�Ǽǲ�")
                
                hpdzmx_where_dict = {}
                hpdzmx_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                hpdzmx_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                hpdzmx_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                
                stat_dict = {}
                if not rccpsState.getTransStateCur(TradeContext.BJEDTE,TradeContext.BSPSQN,stat_dict):
                    rccpsCronFunc.cronExit(TradeContext.errorCode,TradeContext.errorMsg)
                
                hpdzmx_update_dict = {}
                hpdzmx_update_dict['BJEDTE'] = TradeContext.BJEDTE
                hpdzmx_update_dict['BSPSQN'] = TradeContext.BSPSQN
                hpdzmx_update_dict['BCSTAT'] = stat_dict['BCSTAT']
                hpdzmx_update_dict['BDWFLG'] = stat_dict['BDWFLG']
                
                ret = rccpsDBTrcc_hpdzmx.updateCmt(hpdzmx_update_dict,hpdzmx_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�Ǽǻ�Ҷ�����ϸ�Ǽǲ�����������Ϣ�쳣")
                
                AfaLoggerFunc.tradeInfo(">>>�������»����ϸ�Ǽǲ�")
                
                #========�޸Ĵ�������Ϊ����δ����,��������=====================
                hpdzcz_update_dict = {}
                hpdzcz_update_dict['EACTYP'] = '08'
                hpdzcz_update_dict['EACINF'] = '��������δ����,��������'
                hpdzcz_update_dict['BJEDTE'] = TradeContext.BJEDTE
                hpdzcz_update_dict['BSPSQN'] = TradeContext.BSPSQN
                
                hpdzcz_where_dict = {}
                hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                
                ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�޸Ļ�Ҷ��˴��˵Ǽǲ������ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        #================�������ڼ���,����δ����===============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�����������ڼ���,����δ��������")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '07' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������Ϊϵͳ�쳣,��Ƽ���Ա��ʵ����")
            #for i in xrange(len(hpdzcz_list)):
            #    hpdzcz_update_dict = {}
            #    hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hpdzcz_where_dict = {}
            #    hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
            #    hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
            #    hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
            #    
            #    ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>���������������ڼ���,����δ��������")
        #================��������δ����,��������===============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������δ����,������������")
        
        hpdzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '08' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hpdzcz_list = rccpsDBTrcc_hpdzcz.selectm(1,0,hpdzcz_where_sql,"")
        
        if hpdzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hpdzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴��������貹����,�ɹ����޸Ĵ��˴����ʶΪ�Ѵ���")
            for i in xrange(len(hpdzcz_list)):
                #============��������ಹ����==================================
                
                j = 0     #��������ʼ��
                
                while 1 == 1:
                    
                    j = j + 1   #��������1
                    
                    #========��ʼ������========================================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ��ʼ����������")
                    
                    trc_dict = {}
                    if not rccpsDBFunc.getTransBil(hpdzcz_list[i]['BJEDTE'],hpdzcz_list[i]['BSPSQN'],trc_dict):
                        rccpsCronFunc.cronExit("S999","��ѯ�˽��������Ϣ�쳣")
                        
                    if not rccpsMap0000Dbilbka2CTradeContext.map(trc_dict):
                        rccpsCronFunc.cronExit("S999","��������Ϣ��ֵ��TradeContext�쳣")
                        
                    if not rccpsDBFunc.getInfoBil(TradeContext.BILVER,TradeContext.BILNO,TradeContext.BILRS,trc_dict):
                        rccpsCronFunc.cronExit("S999","��ѯ�˽�����ػ�Ʊ��Ϣ�쳣")
                        
                    if not rccpsMap0000Dbilinf2CTradeContext.map(trc_dict):
                        rccpsCronFunc.cronExit("S999","����Ʊ��Ϣ��ֵ��TradeContext�쳣")
                    
                    TradeContext.BJETIM = AfaUtilTools.GetSysTime( )
                    TradeContext.BEAUUS = TradeContext.BEAUUS
                    TradeContext.BEAUPS = TradeContext.BEAUPS
                    TradeContext.OCCAMT = str(TradeContext.OCCAMT)
                    TradeContext.NCCworkDate = TradeContext.NCCWKDAT
                    
                    AfaLoggerFunc.tradeInfo(">>>������ʼ����������")
                    #========����,����=========================================
                    AfaLoggerFunc.tradeInfo('>>>��������δ����,��������,�Զ�����')
                    
                    AfaLoggerFunc.tradeInfo("��Ʊ�⸶����,�Զ�����")
                    
                    TradeContext.HostCode = '8813'            #����8813�����ӿ�
                    
                    TradeContext.BCSTAT  = PL_BCSTAT_AUTO   #�Զ�����
                    TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #������
                    
                    #====ƴ������˻�====
                    TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_HCHK        #�跽�˻�
                    TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                    
                    TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #�����˺�
                    TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
                    
                    TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ      #�����˻�
                    TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                    
                    AfaLoggerFunc.tradeInfo( '�跽�˺�1:' + TradeContext.SBAC )
                    AfaLoggerFunc.tradeInfo( '�����˺�1:' + TradeContext.RBAC )
                    AfaLoggerFunc.tradeInfo( '�����˺�1:' + TradeContext.REAC )
                    
                    AfaLoggerFunc.tradeInfo(">>>��ʼ�ж��Ƿ���ڶ�������")
                    #=====�жϼ��˴���====
                    #�ر�� 20080913 ����ʵ�ʽ�����ժҪ����
                    TradeContext.RCCSMCD = PL_RCCSMCD_HPJF       #ժҪ����
                    if float(TradeContext.RMNAMT) != 0.00:
                        AfaLoggerFunc.tradeInfo(">>>�ڶ��μ��˸�ֵ����")
                        
                        TradeContext.ACUR   = '2'   #����ѭ������
                        TradeContext.TRFG   = '9'   #ƾ֤�����ʶ'
                        TradeContext.I2CETY = ''    #ƾ֤����
                        TradeContext.I2TRAM = str(TradeContext.RMNAMT)             #������
                        TradeContext.I2SMCD = PL_RCCSMCD_HPJF                      #ժҪ����
                        TradeContext.I2RBAC = TradeContext.BESBNO + PL_ACC_DYKJQ   #�����˺�
                        TradeContext.I2SBAC = TradeContext.BESBNO + PL_ACC_HCHK    #�跽�˺�
                        TradeContext.I2REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ  #�����˺�
                        
                        #=====�����˺�У��λ====
                        TradeContext.I2SBAC = rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
                        TradeContext.I2RBAC = rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
                        TradeContext.I2REAC = rccpsHostFunc.CrtAcc(TradeContext.I2REAC,25)
                        
                        AfaLoggerFunc.tradeInfo( '�跽�˺�2:' + TradeContext.I2SBAC )
                        AfaLoggerFunc.tradeInfo( '�����˺�2:' + TradeContext.I2RBAC )
                        AfaLoggerFunc.tradeInfo( '�����˺�2:' + TradeContext.I2REAC )
                        
                    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ���ڶ�������")
                    
                    #======================�޸ĵǼǲ��н��׻�����Ϊ��ǰ������======
                    
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���»��ҵ��Ǽǲ����׻�����")
                    
                    bilbka_update_dict = {}
                    bilbka_update_dict['BESBNO'] = TradeContext.BESBNO
                    
                    bilbka_where_dict = {}
                    bilbka_where_dict['BJEDTE'] = TradeContext.BJEDTE
                    bilbka_where_dict['BSPSQN'] = TradeContext.BSPSQN
                    
                    ret = rccpsDBTrcc_bilbka.update(bilbka_update_dict,bilbka_where_dict)
                    
                    if ret <= 0:
                        rccpsCronFunc.cronExit('S999','���»��ҵ��Ǽǲ��л������쳣')
                        
                    AfaLoggerFunc.tradeInfo(">>>�������»��ҵ��Ǽǲ����׻�����")
                    
                    #======================����sstlog��״̬��¼====================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ��������״̬")
                    
                    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
                        rccpsCronFunc.cronExit(TradeContext.errorCode, TradeContext.errorMsg)
                    
                    AfaLoggerFunc.tradeInfo(">>>������������״̬")
                    
                    #======================commit����==============================
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                        rccpsCronFunc.cronExit("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    #=====================������ͨѶ===============================
                    rccpsHostFunc.CommHost(TradeContext.HostCode)
                    
                    #=========��ʼ��״̬�ֵ丳ֵ===================================
                    stat_dict = {}
                    stat_dict['BJEDTE']  = TradeContext.BJEDTE            #��������
                    stat_dict['BSPSQN']  = TradeContext.BSPSQN            #�������
                    stat_dict['BJETIM']  = TradeContext.BJETIM            #����ʱ��
                    stat_dict['BESBNO']  = TradeContext.BESBNO            #������
                    stat_dict['BETELR']  = TradeContext.BETELR            #��Ա��
                    stat_dict['SBAC']    = TradeContext.SBAC              #�跽�˺�
                    stat_dict['RBAC']    = TradeContext.REAC              #�����˺�
                    stat_dict['MGID']    = TradeContext.errorCode         #�������ش���
                    stat_dict['STRINFO'] = TradeContext.errorMsg          #����������Ϣ
                    stat_dict['NOTE3']   = ""
                    
                    #=========�ж��������ؽ��=================================
                    if TradeContext.errorCode == '0000':
                        AfaLoggerFunc.tradeInfo("���˲����˳ɹ�,����״̬Ϊ�Զ�����\�Զ����˳ɹ�")
                        
                        stat_dict['BCSTAT'] = TradeContext.BCSTAT          #��ˮ״̬
                        stat_dict['BDWFLG'] = PL_BDWFLG_SUCC               #��ת�����ʶ
                        stat_dict['TRDT']   = TradeContext.TRDT            #��������
                        stat_dict['TLSQ']   = TradeContext.TLSQ            #������ˮ
                        
                        #====���������˳ɹ�,�����ش�������Ų�Ϊ��,������ҵ��״̬Ϊ����===
                        if TradeContext.existVariable('DASQ'):
                            if TradeContext.DASQ != '':
                                AfaLoggerFunc.tradeInfo("�������˳ɹ�,�����ش�������ŷǿ�,����ҵ��״̬Ϊ���˳ɹ�")
                                TradeContext.BCSTAT = PL_BCSTAT_HANG
                                stat_dict['DASQ']   = TradeContext.DASQ              #�������
                                stat_dict['NOTE3']  = "����������"
                    else:
                        AfaLoggerFunc.tradeInfo("���˲�����ʧ��,����״̬Ϊ�Զ�����\�Զ�����ʧ��")
                        
                        stat_dict['BCSTAT'] = TradeContext.BCSTAT          #��ˮ״̬
                        stat_dict['BDWFLG'] = PL_BDWFLG_FAIL               #��ת�����ʶ
                    
                    #=========����״̬=========================================
                    if not rccpsState.setTransState(stat_dict):
                        rccpsCronFunc.cronExit('S999', '����״̬�쳣')
                    
                    if not AfaDBFunc.CommitSql( ):
                        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                        rccCronFunc.cronExit("S999","Commit�쳣")
                    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                    
                    #========����������ʧ��,˯�������,������һ�β�����========
                    if TradeContext.errorCode != '0000':
                        if j < 3:
                            AfaLoggerFunc.tradeInfo("��[" + str(j) + "]�����˲�����ʧ��,˯�������,������һ�β�����")
                            time.sleep(300)
                            continue
                        else:
                            AfaLoggerFunc.tradeInfo("��[" + str(j) + "]�����˲�����ʧ��,ֹͣ������ҵ�񲹼���,������һ����ҵ�񲹼���")
                            #======��δ��ɱ�ʶΪTrue==========================
                            uncomplate_flag = True
                            break
                    else:
                        AfaLoggerFunc.tradeInfo("�����˳ɹ�")
                
                        #========�޸Ĵ��˴����ʶΪ�Ѵ���==============================
                        AfaLoggerFunc.tradeInfo(">>>��ʼ�޸Ĵ��˴����ʶΪ�Ѵ���")
                        
                        hpdzcz_update_dict = {}
                        hpdzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                        
                        hpdzcz_where_dict = {}
                        hpdzcz_where_dict['SNDBNKCO'] = hpdzcz_list[i]['SNDBNKCO']
                        hpdzcz_where_dict['TRCDAT']   = hpdzcz_list[i]['TRCDAT']
                        hpdzcz_where_dict['TRCNO']    = hpdzcz_list[i]['TRCNO']
                        
                        ret = rccpsDBTrcc_hpdzcz.updateCmt(hpdzcz_update_dict,hpdzcz_where_dict)
                        
                        if ret <= 0:
                            AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                            rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
                        
                        AfaLoggerFunc.tradeInfo(">>>�����޸Ĵ��˴����ʶΪ�Ѵ���")
                        
                        break
                
        AfaLoggerFunc.tradeInfo(">>>����������������δ����,������������")
        
        #================�رջ�Ʊ���˻�Ʊ���˴��˴���ϵͳ����,�򿪻�Ʊ������ϸ�ļ����ɼ����͵�����ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ʊ���˻�Ʊ���˴��˴���ϵͳ����,�򿪻�Ʊ������ϸ�ļ����ɼ����͵�����ϵͳ����")
        if not rccpsCronFunc.closeCron("00040"):
            rccpsCronFunc.cronExit("S999","�رջ�Ʊ���˴��˴���ϵͳ�����쳣")
        
        if not rccpsCronFunc.openCron("00045"):
            rccpsCronFunc.cronExit("S999","�򿪻�Ʊ������ϸ�ļ����ɼ����͵�����ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ʊ���˻�Ʊ���˴��˴���ϵͳ����,�򿪻�Ʊ������ϸ�ļ����ɼ����͵�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊ���˴��˴���[rccpsHPDZCZModify]�˳�***")
        
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
            AfaLoggerFunc.tradeInfo("***[rccpsHPDZCZModify]�����ж�***")

        sys.exit(-1)
