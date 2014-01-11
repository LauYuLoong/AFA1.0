# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��Ҷ��˴��˴���
#===============================================================================
#   �����ļ�:   rccpsHDDZCZModify.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-27
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc,time
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc,rccpsHostFunc,rccpsFunc,rccpsGetFunc,miya
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_hddzcz,rccpsDBTrcc_hddzmx,rccpsDBTrcc_trcbka,rccpsDBFunc
import rccpsMap0000Dhddzmx2CTradeContext,rccpsMap0000Dtrcbka2CTradeContext,rccpsMap1101CTradeContext2Dtrcbka_dict

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ҷ��˴��˴���[rccpsHDDZCZModify]����***")
        
        #==========��ʼ��δ��ɱ�ʶΪFalse=====================================
        uncomplate_flag = False
        
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
        
        #================����������,������=====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '01' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������������������,��ϵͳ����״̬Ϊ����,�޸Ĵ��˴����ʶΪ�Ѵ���")
            for i in xrange(len(hddzcz_list)):
                #========����״̬Ϊ����========================================
                AfaLoggerFunc.tradeInfo("��ʼ�޸�ԭ����״̬Ϊ����")
                
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========���ý���״̬Ϊ����ɹ�================================
                if not rccpsState.newTransState(hddzcz_list[i]['BJEDTE'],hddzcz_list[i]['BSPSQN'],PL_BCSTAT_LONG,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '���ó���ɹ�״̬�쳣')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                AfaLoggerFunc.tradeInfo("�����޸�ԭ����״̬Ϊ����")
                
                #========�޸Ĵ��˴����ʶΪ�Ѵ���==============================
                AfaLoggerFunc.tradeInfo("��ʼ�޸Ĵ��˴����ʶΪ�Ѵ���")
                
                hddzcz_update_dict = {}
                hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hddzcz_where_dict = {} 
                hddzcz_where_dict['BJEDTE'] = hddzcz_list[i]['BJEDTE']
                hddzcz_where_dict['BSPSQN'] = hddzcz_list[i]['BSPSQN']
                
                ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
                    
                AfaLoggerFunc.tradeInfo("�����޸Ĵ��˴����ʶΪ�Ѵ���")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        #================����������,������=====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '02' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������Ϊϵͳ�쳣,��Ƽ���Ա��ʵ����")
            #for i in xrange(len(hddzcz_list)):
            #    hddzcz_update_dict = {}
            #    hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hddzcz_where_dict = {}
            #    hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
            #    hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
            #    hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
            #    
            #    ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        #================���������Ѽ���,����δ����===============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�������������Ѽ���,����δ��������")
        
        hddzcz_where_sql = "nccwkdat = '" + NCCWKDAT + "' and eactyp = '03' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������������������,��ϵͳ����״̬Ϊ����,�޸Ĵ��˴����ʶΪ�Ѵ���")
            for i in xrange(len(hddzcz_list)):
                #========����״̬Ϊ����========================================
                AfaLoggerFunc.tradeInfo("��ʼ�޸�ԭ����״̬Ϊ����")
                
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========���ý���״̬Ϊ����ɹ�================================
                if not rccpsState.newTransState(hddzcz_list[i]['BJEDTE'],hddzcz_list[i]['BSPSQN'],PL_BCSTAT_LONG,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '���ó���ɹ�״̬�쳣')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                AfaLoggerFunc.tradeInfo("�����޸�ԭ����״̬Ϊ����")
                
                #========�޸Ĵ��˴����ʶΪ�Ѵ���==============================
                AfaLoggerFunc.tradeInfo("��ʼ�޸Ĵ��˴����ʶΪ�Ѵ���")
                
                hddzcz_update_dict = {}
                hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hddzcz_where_dict = {} 
                hddzcz_where_dict['BJEDTE'] = hddzcz_list[i]['BJEDTE']
                hddzcz_where_dict['BSPSQN'] = hddzcz_list[i]['BSPSQN']
                
                ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
                    
                AfaLoggerFunc.tradeInfo("�����޸Ĵ��˴����ʶΪ�Ѵ���")
        
        AfaLoggerFunc.tradeInfo(">>>�����������������Ѽ���,����δ��������")
        #================��������δ����,��������===============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������δ����,������������")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '04' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������������������������,�޸�ԭ����״̬Ϊ����ɹ�,�ɹ����޸Ĵ��˴����ʶΪ�Ѵ���")
            for i in xrange(len(hddzcz_list)):
                #========������================================================
                TradeContext.BESBNO = PL_BESBNO_BCLRSB
                TradeContext.BETELR = PL_BETELR_AUTO
                
                #========���ý���״̬Ϊ����ɹ�=================================
                if not rccpsState.newTransState(hddzcz_list[i]['BJEDTE'],hddzcz_list[i]['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_SUCC):
                    rccpsCronFunc.cronExit('S999', '��������ɹ�״̬�쳣')
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    rccCronFunc.cronExit("S999","Commit�쳣")
                AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
                
                #========�޸Ĵ��˴����ʶΪ�Ѵ���==============================
                hddzcz_update_dict = {}
                hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                
                hddzcz_where_dict = {}
                hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                
                ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����������������δ����,������������")
        #================����������,������=====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '05' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������Ϊϵͳ�쳣,��Ƽ���Ա��ʵ����")
            #for i in xrange(len(hddzcz_list)):
            #    hddzcz_update_dict = {}
            #    hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hddzcz_where_dict = {}
            #    hddzcz_where_dict['BJEDTE'] = hddzcz_list[i]['BJEDTE']
            #    hddzcz_where_dict['BSPSQN'] = hddzcz_list[i]['BSPSQN']
            #    
            #    ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        #================����������,������=====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '06' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴��������貹����,�ɹ����޸Ĵ��˴����ʶΪ�Ѵ���")
            for i in xrange(len(hddzcz_list)):
                #========������================================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ������")
                
                #========��ʼ������������======================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ��ʼ��������")
                TradeContext.tradeResponse=[]
                
                hddzmx_where_dict = {}
                hddzmx_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                hddzmx_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                hddzmx_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                
                hddzmx_dict = rccpsDBTrcc_hddzmx.selectu(hddzmx_where_dict)
                
                if hddzmx_dict == None:
                    rccpsCronFunc.cronExit("S999","��ѯ������ϸ�����쳣")
                    
                if len(hddzmx_dict) <= 0:
                    rccpsCronFunc.cronExit("S999","�Ǽǲ����޴�������ϸ����")
                
                rccpsMap0000Dhddzmx2CTradeContext.map(hddzmx_dict)
                
                TradeContext.OCCAMT = str(TradeContext.OCCAMT)
                TradeContext.TemplateCode  = 'RCC005'
                TradeContext.BRSFLG        = PL_BRSFLG_RCV
                TradeContext.CUR           = '01'
                
                if TradeContext.TRCCO == '2000001':
                    TradeContext.TransCode = '1101'
                    TradeContext.OPRNO     = '00'
                elif TradeContext.TRCCO == '2000002':
                    TradeContext.TransCode = '1102'
                    TradeContext.OPRNO     = '01'
                elif TradeContext.TRCCO == '2000003':
                    TradeContext.TransCode = '1103'
                    TradeContext.OPRNO     = '02'
                elif TradeContext.TRCCO == '2000004':
                    TradeContext.TransCode = '1104'
                    TradeContext.OPRNO     = '09'
                elif TradeContext.TRCCO == '2000009':
                    TradeContext.TransCode = '1105'
                    TradeContext.OPRNO     = '04'
                
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
                trcbka_dict = {}
                if not rccpsMap1101CTradeContext2Dtrcbka_dict.map(trcbka_dict):
                    rccpsCronFunc.cronExit('M999', '�ֵ丳ֵ����')
                
                trcbka_dict['DCFLG'] = PL_DCFLG_CRE                  #�����ʶ
                trcbka_dict['OPRNO'] = TradeContext.OPRNO            #ҵ������
                
                #=====================��ʼ�������ݿ�===========================
                if not rccpsDBFunc.insTransTrc(trcbka_dict):
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
                
                #========���»�Ҷ�����ϸ�Ǽǲ�================================
                AfaLoggerFunc.tradeInfo(">>>��ʼ���»����ϸ�Ǽǲ�")
                
                hddzmx_where_dict = {}
                hddzmx_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                hddzmx_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                hddzmx_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                
                stat_dict = {}
                if not rccpsState.getTransStateCur(TradeContext.BJEDTE,TradeContext.BSPSQN,stat_dict):
                    rccpsCronFunc.cronExit(TradeContext.errorCode,TradeContext.errorMsg)
                
                hddzmx_update_dict = {}
                hddzmx_update_dict['BJEDTE'] = TradeContext.BJEDTE
                hddzmx_update_dict['BSPSQN'] = TradeContext.BSPSQN
                hddzmx_update_dict['BCSTAT'] = stat_dict['BCSTAT']
                hddzmx_update_dict['BDWFLG'] = stat_dict['BDWFLG']
                
                ret = rccpsDBTrcc_hddzmx.updateCmt(hddzmx_update_dict,hddzmx_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�Ǽǻ�Ҷ�����ϸ�Ǽǲ�����������Ϣ�쳣")
                
                AfaLoggerFunc.tradeInfo(">>>�������»����ϸ�Ǽǲ�")
                
                #========�޸Ĵ�������Ϊ����δ����,��������=====================
                hddzcz_update_dict = {}
                hddzcz_update_dict['EACTYP'] = '08'
                hddzcz_update_dict['EACINF'] = '��������δ����,��������'
                hddzcz_update_dict['BJEDTE'] = TradeContext.BJEDTE
                hddzcz_update_dict['BSPSQN'] = TradeContext.BSPSQN
                
                hddzcz_where_dict = {}
                hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                
                ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�޸Ļ�Ҷ��˴��˵Ǽǲ������ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        #================�������ڼ���,����δ����===============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�����������ڼ���,����δ��������")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '07' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴�������Ϊϵͳ�쳣,��Ƽ���Ա��ʵ����")
            #for i in xrange(len(hddzcz_list)):
            #    hddzcz_update_dict = {}
            #    hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
            #    
            #    hddzcz_where_dict = {}
            #    hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
            #    hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
            #    hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
            #    
            #    ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
            #    
            #    if ret <= 0:
            #        AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
            #        rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
        
        AfaLoggerFunc.tradeInfo(">>>���������������ڼ���,����δ��������")
        #================��������δ����,��������===============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������δ����,������������")
        
        hddzcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and eactyp = '08' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        hddzcz_list = rccpsDBTrcc_hddzcz.selectm(1,0,hddzcz_where_sql,"")
        
        if hddzcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(hddzcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
        
        else:
            AfaLoggerFunc.tradeInfo("�˴��������貹����,�ɹ����޸Ĵ��˴����ʶΪ�Ѵ���")
            for i in xrange(len(hddzcz_list)):
                #============��������ಹ����==================================
                
                j = 0     #��������ʼ��
                
                while 1 == 1:
                    
                    j = j + 1   #��������1
                        
                    #========��ʼ������========================================
                    AfaLoggerFunc.tradeInfo(">>>��ʼ��ʼ����������")
                    
                    trc_dict = {}
                    if not rccpsDBFunc.getTransTrc(hddzcz_list[i]['BJEDTE'],hddzcz_list[i]['BSPSQN'],trc_dict):
                        rccpsCronFunc.cronExit("S999","��ѯ�˽��������Ϣ�쳣")
                        
                    if not rccpsMap0000Dtrcbka2CTradeContext.map(trc_dict):
                        rccpsCronFunc.cronExit("S999","��������Ϣ��ֵ��TradeContext�쳣")
                    
                    TradeContext.NCCworkDate = TradeContext.NCCWKDAT 
                    TradeContext.BJETIM = AfaUtilTools.GetSysTime( )
                    TradeContext.BEAUUS = ""
                    TradeContext.BEAUPS = ""
                    TradeContext.OCCAMT = str(TradeContext.OCCAMT)
                    
                    AfaLoggerFunc.tradeInfo(">>>������ʼ����������")
                    #========����,����=========================================
                    AfaLoggerFunc.tradeInfo('>>>��������δ����,��������,�Զ�����')
                    
                    if TradeContext.TRCCO != '2000004':
                        AfaLoggerFunc.tradeInfo("���˻�����,��ʼУ����Ѻ")
                        
                        #=====��ʼ������Ѻ���������к�Ѻ====
                        TRCDAT = TradeContext.TRCDAT
                        TRCNO = TradeContext.TRCNO
                        SEAL = TradeContext.SEAL
                        SNDBANKCO  = TradeContext.SNDBNKCO
                        RCVBANKCO  = TradeContext.RCVBNKCO
                        SNDBANKCO = SNDBANKCO.rjust(12,'0')
                        RCVBANKCO = RCVBANKCO.rjust(12,'0')
                        AMOUNT = TradeContext.OCCAMT.split('.')[0] + TradeContext.OCCAMT.split('.')[1]
                        AMOUNT = AMOUNT.rjust(15,'0')
                        INFO   = "".rjust(60,' ')
                        
                        AfaLoggerFunc.tradeDebug('��������(0-��Ѻ 1-��Ѻ):' + str(PL_SEAL_DEC) )
                        AfaLoggerFunc.tradeDebug('ҵ������(1-�ֽ��Ʊ 2-ת�˻�Ʊ 3-���ӻ��ҵ��):' +str(PL_TYPE_DZHD) )
                        AfaLoggerFunc.tradeDebug('ί������:' + TradeContext.TRCDAT )
                        AfaLoggerFunc.tradeDebug('������ˮ��:' + TradeContext.TRCNO )
                        AfaLoggerFunc.tradeDebug('AMOUNT=' + str(AMOUNT) )
                        AfaLoggerFunc.tradeDebug('SNDBANKCO=' + str(SNDBANKCO) )
                        AfaLoggerFunc.tradeDebug('RCVBANKCO=' + str(RCVBANKCO) )
                        AfaLoggerFunc.tradeDebug('��Ѻ:' + TradeContext.SEAL )
                        AfaLoggerFunc.tradeDebug('OTHERINFO[' + str(INFO) + ']')
                        
                        ret = miya.DraftEncrypt(PL_SEAL_DEC,PL_TYPE_DZHD,TRCDAT,TRCNO,AMOUNT,SNDBANKCO,RCVBANKCO,INFO,SEAL)
                        AfaLoggerFunc.tradeInfo('>>>У����Ѻ,����ֵret=['+ str(ret) + ']')
                        
                        if ret != 0:
                            if ret == 9005:
                                #====��Ѻ���Զ�����==============================
                                AfaLoggerFunc.tradeInfo("��Ѻ��,�Զ�����")
                                NOTE3 = "��Ѻ��,�Զ�����"
                            else:
                                #====У����Ѻ�쳣,�Զ�����=========================
                                AfaLoggerFunc.tradeInfo("У����Ѻ�쳣,�Զ�����")
                                NOTE3 = "У����Ѻ�쳣,�Զ�����"
                            
                            TradeContext.HostCode = '8813'            #����8813�����ӿ�
                            
                            TradeContext.NOTE3   = NOTE3            #����ԭ��
                            TradeContext.BCSTAT  = PL_BCSTAT_HANG   #�Զ�����
                            TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #������
                        
                            #====ƴ������˻�====
                            TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #�跽�˻�
                            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                            
                            TradeContext.RBAC = TradeContext.BESBNO + "".rjust(15,'0')
                            
                            TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ      #�����˻�
                            TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                            
                            AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
                            AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
                            AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.REAC )
                        else:
                            #======��ѺУ��ͨ��,�Զ�����===========================
                            AfaLoggerFunc.tradeInfo("��ѺУ��ͨ��,�Զ�����")
                            
                            TradeContext.HostCode = '8813'            #����8813�����ӿ�
                            
                            TradeContext.BCSTAT  = PL_BCSTAT_AUTO   #�Զ�����
                            TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #������
                            
                            #====ƴ������˻�====
                            TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #�跽�˻�
                            TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                            
                            TradeContext.RBAC = TradeContext.PYEACC                      #�տ����˺�
                            
                            TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ      #�����˻�
                            TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                            
                            AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
                            AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
                            AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.REAC )
                        
                        AfaLoggerFunc.tradeInfo(">>>����У����Ѻ")
                    else:
                        AfaLoggerFunc.tradeInfo("�˻�����,�Զ�����")
                        
                        TradeContext.HostCode = '8813'            #����8813�����ӿ�
                        
                        TradeContext.BCSTAT  = PL_BCSTAT_AUTO   #�Զ�����
                        TradeContext.BDWFLG  = PL_BDWFLG_WAIT   #������
                        
                        #====ƴ������˻�====
                        TradeContext.SBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ    #�跽�˻�
                        TradeContext.SBAC = rccpsHostFunc.CrtAcc(TradeContext.SBAC, 25)
                        
                        TradeContext.RBAC = TradeContext.PYEACC                      #�����˻�
                        
                        TradeContext.REAC = TradeContext.BESBNO + PL_ACC_NXYDXZ      #�����˻�
                        TradeContext.REAC = rccpsHostFunc.CrtAcc(TradeContext.REAC, 25)
                        
                        AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
                        AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
                        AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.REAC )
                    
                    
                    #======================�޸ĵǼǲ��н��׻�����Ϊ��ǰ������======
                    
                    AfaLoggerFunc.tradeInfo(">>>��ʼ���»��ҵ��Ǽǲ����׻�����")
                    
                    trcbka_update_dict = {}
                    trcbka_update_dict['BESBNO'] = TradeContext.BESBNO
                    
                    trcbka_where_dict = {}
                    trcbka_where_dict['BJEDTE'] = TradeContext.BJEDTE
                    trcbka_where_dict['BSPSQN'] = TradeContext.BSPSQN
                    
                    ret = rccpsDBTrcc_trcbka.update(trcbka_update_dict,trcbka_where_dict)
                    
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
                        
                        hddzcz_update_dict = {}
                        hddzcz_update_dict['ISDEAL'] = PL_ISDEAL_ISDO
                        
                        hddzcz_where_dict = {}
                        hddzcz_where_dict['SNDBNKCO'] = hddzcz_list[i]['SNDBNKCO']
                        hddzcz_where_dict['TRCDAT']   = hddzcz_list[i]['TRCDAT']
                        hddzcz_where_dict['TRCNO']    = hddzcz_list[i]['TRCNO']
                        
                        ret = rccpsDBTrcc_hddzcz.updateCmt(hddzcz_update_dict,hddzcz_where_dict)
                        
                        if ret <= 0:
                            AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                            rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
                        
                        AfaLoggerFunc.tradeInfo(">>>�����޸Ĵ��˴����ʶΪ�Ѵ���")
                        
                        break
                
        AfaLoggerFunc.tradeInfo(">>>����������������δ����,������������")
        
        #================�رջ�Ҷ��˻�Ҷ��˴��˴���ϵͳ����,�򿪻�Ҷ�����ϸ�ļ����ɼ����͵�����ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ҷ��˻�Ҷ��˴��˴���ϵͳ����,�򿪻�Ҷ�����ϸ�ļ����ɼ����͵�����ϵͳ����")
        if not rccpsCronFunc.closeCron("00030"):
            rccpsCronFunc.cronExit("S999","�رջ�Ҷ��˴��˴���ϵͳ�����쳣")
        
        if not uncomplate_flag:
            if not rccpsCronFunc.openCron("00035"):
                rccpsCronFunc.cronExit("S999","�򿪻�Ҷ�����ϸ�ļ����ɼ����͵�����ϵͳ�����쳣")
        else:
            AfaLoggerFunc.tradeInfo(">>>����δ��ɱ�ʶΪTrue,���򿪻�Ҷ�����ϸ�ļ����ɼ����͵�����ϵͳ�����쳣")
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ҷ��˻�Ҷ��˴��˴���ϵͳ����,�򿪻�Ҷ�����ϸ�ļ����ɼ����͵�����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ҷ��˴��˴���[rccpsHDDZCZModify]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHDDZCZModify]�����ж�***')

        sys.exit(-1)
