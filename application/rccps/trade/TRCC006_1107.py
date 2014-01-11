# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).ҵ��״̬��ѯ���Ľ���
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-11
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsFunc,rccpsGetFunc
import rccpsDBTrcc_ztcbka,rccpsMap0000Dout_context2CTradeContext,rccpsMap1107CTradeContext2Dztcbka

#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ҵ��״̬��ѯ���Ľ���[RCC006_1107]����***' )
    
    #==========�ж��Ƿ��ظ�����,������ظ�����,ֱ�ӽ�����һ����================
    AfaLoggerFunc.tradeInfo(">>>��ʼ����Ƿ��ظ�����")
    ztcbka_where_dict = {}
    ztcbka_where_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
    ztcbka_where_dict['TRCDAT']   = TradeContext.TRCDAT
    ztcbka_where_dict['TRCNO']    = TradeContext.TRCNO
    
    ztcbka_dict = rccpsDBTrcc_ztcbka.selectu(ztcbka_where_dict)
    
    if ztcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","У���ظ������쳣") 
    
    if len(ztcbka_dict) > 0:
        AfaLoggerFunc.tradeInfo("ҵ��״̬�Ǽǲ��д�����ͬ��ѯ����,�˱���Ϊ�ظ�����,ֱ�ӽ�����һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
        out_context_dict['STRINFO']  = '�ظ�����'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
        
    AfaLoggerFunc.tradeInfo(">>>��������Ƿ��ظ�����")
    
    #==========Ϊҵ��״̬��ѯ�鸴�Ǽǲ��ֵ丳ֵ================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪҵ��״̬��ѯ�鸴�Ǽǲ��ֵ丳ֵ")
    
    
    AfaLoggerFunc.tradeInfo("ҵ������[" + TradeContext.ROPRTPNO + "]")
    AfaLoggerFunc.tradeInfo("ԭ�����к�[" + TradeContext.ORSNDBNK + "]")
    AfaLoggerFunc.tradeInfo("ԭί������[" + TradeContext.ORTRCDAT + "]")
    AfaLoggerFunc.tradeInfo("ԭ������ˮ��[" + TradeContext.ORTRCNO + "]")
    
    tran_dict = {}
    if TradeContext.ROPRTPNO == '20':
        if not rccpsDBFunc.getTransTrcAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
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
            out_context_dict['STRINFO']  = 'ԭ���ײ�����'
            
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
            
            return True
    elif TradeContext.ROPRTPNO == '21':
        if not rccpsDBFunc.getTransBilAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
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
            out_context_dict['STRINFO']  = 'ԭ���ײ�����'
            
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
            
            return True
    elif TradeContext.ROPRTPNO == '30':
        if not rccpsDBFunc.getTransWtrAK(TradeContext.ORSNDBNK,TradeContext.ORTRCDAT,TradeContext.ORTRCNO,tran_dict):
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
            out_context_dict['STRINFO']  = 'ԭ���ײ�����'
            
            rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
            
            return True
                   
    else:
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
        out_context_dict['STRINFO']  = 'ԭҵ�����ͷǷ�'
        
        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)
        
        return True
    
    if tran_dict.has_key('BJEDTE'):
        TradeContext.BOJEDT = tran_dict['BJEDTE']
    
    if tran_dict.has_key('BSPSQN'):
        TradeContext.BOSPSQ = tran_dict['BSPSQN']

    TradeContext.ISDEAL = PL_ISDEAL_ISDO
    
    ztcbka_insert_dict = {}
    if not rccpsMap1107CTradeContext2Dztcbka.map(ztcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999","Ϊҵ��״̬��ѯ�鸴�Ǽǲ��ֵ丳ֵ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊҵ��״̬��ѯ�鸴�Ǽǲ��ֵ丳ֵ")
    #==========�Ǽ�ҵ��״̬��ѯ�鸴�Ǽǲ�======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�ҵ��״̬��ѯ�鸴�Ǽǲ�")
    
    ztcbka_insert_dict['BRSFLG']   =   PL_BRSFLG_RCV         #����
    if TradeContext.ORCUR == 'CNY':
        ztcbka_insert_dict['CUR']  =   '01'                  #ԭ����
    else:
        ztcbka_insert_dict['CUR']  =   TradeContext.ORCUR    #ԭ����

    ztcbka_insert_dict['OCCAMT']   =   TradeContext.OROCCAMT #ԭ���
    
    ret = rccpsDBTrcc_ztcbka.insertCmt(ztcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�Ǽ�ҵ��״̬��ѯ�鸴�Ǽǲ��쳣")   
        
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ�ҵ��״̬��ѯ�鸴�Ǽǲ�")
    
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
    
    #==��BJEDTE��BSPSQN����TradeContext�е�BOJEDT��BOSPSQ��,Ϊ���׺�����׼��==
    TradeContext.BOJEDT    = TradeContext.BJEDTE
    TradeContext.BOSPSQ    = TradeContext.BSPSQN
    TradeContext.OQTSBNK   = TradeContext.SNDBNKCO
    TradeContext.OQTDAT    = TradeContext.BJEDTE
    TradeContext.OQTNO     = TradeContext.TRCNO
    TradeContext.ORSNDBNK  = TradeContext.SNDBNKCO
    TradeContext.ORRCVBNK  = TradeContext.RCVBNKCO
    TradeContext.ORTRCDAT  = TradeContext.TRCDAT
    TradeContext.ORTRCNO   = TradeContext.TRCNO
    TradeContext.OQTDAT    = TradeContext.TRCDAT
    TradeContext.OQTSBNK   = TradeContext.SNDBNKCO
    TradeContext.OQTNO     = TradeContext.TRCNO
    TradeContext.ORMFN     = TradeContext.MSGFLGNO
    TradeContext.ROPRTPNO  = TradeContext.OPRTYPNO
    TradeContext.RCVBNKCO  = TradeContext.SNDBNKCO
    TradeContext.RCVBNKNM  = TradeContext.SNDBNKNM
    
    if tran_dict.has_key('BCSTAT'):
        TradeContext.ORBCSTAT = tran_dict['BCSTAT']
    if tran_dict.has_key('BDWFLG'):
        TradeContext.ORBDWFLG = tran_dict['BDWFLG']
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ҵ��״̬��ѯ���Ľ���[RCC006_1107]�˳�***' )
    
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).ҵ��״̬��ѯ���Ľ���[RCC006_1107]����***' )
    
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow("S999","����ͨѶ��ִ�����쳣")
    
    if TradeContext.existVariable('ISDEAL'):
        AfaLoggerFunc.tradeInfo(">>>״̬��ѯҵ������,�ɹ�����,��ʼ�Զ�ҵ��״̬�鸴����")
        
        AfaLoggerFunc.tradeInfo(">>>��ʼ���˳�ʼ��")
        
        #=====================���˳�ʼ��============================================
        TradeContext.sysType = "rccpst"
        TradeContext.BRSFLG = PL_BRSFLG_SND
        TradeContext.TRCCO  = '9900507'
        
        TradeContext.BJEDTE=AfaUtilTools.GetSysDate( )
        TradeContext.BJETIM=AfaUtilTools.GetSysTime( )
        TradeContext.TRCDAT=AfaUtilTools.GetSysDate( )
        
        #=====================�����Ϸ���У��========================================
        if not rccpsFunc.ChkUnitInfo( PL_BRSFLG_SND ) :
            return AfaFlowControl.ExitThisFlow("S999","�����Ϸ���У���쳣")
                
        #=====================��ȡƽ̨��ˮ��========================================
        if rccpsGetFunc.GetSerialno(PL_BRSFLG_SND) == -1 :
            return AfaFlowControl.ExitThisFlow("S999","��ȡƽ̨��ˮ���쳣")
            
        #=====================��ȡ������ˮ��========================================
        if rccpsGetFunc.GetRccSerialno( ) == -1 :
            return AfaFlowControl.ExitThisFlow("S999","��ȡ������ˮ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�������˳�ʼ��")
        
        #=====================Ϊ״̬�鸴ҵ���ֵ丳ֵ================================
        AfaLoggerFunc.tradeInfo(">>>��ʼΪ״̬�鸴ҵ���ֵ丳ֵ")
        
        TradeContext.TRCNO = TradeContext.SerialNo
        TradeContext.NCCTRCST = ""
        
        if not TradeContext.existVariable('ORBCSTAT'):
            TradeContext.MBRTRCST = PL_MBRTRCST_UNRCV
        else:
            if TradeContext.ORBCSTAT == PL_BCSTAT_BNKRCV:
                TradeContext.MBRTRCST = PL_MBRTRCST_RCV
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTO or TradeContext.ORBCSTAT == PL_BCSTAT_HANG) and TradeContext.ORBDWFLG ==PL_BDWFLG_SUCC:
                TradeContext.MBRTRCST = PL_MBRTRCST_ACSUC
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTO or TradeContext.ORBCSTAT == PL_BCSTAT_HANG) and TradeContext.ORBDWFLG ==PL_BDWFLG_FAIL:
                TradeContext.MBRTRCST = PL_MBRTRCST_ACFAL
            elif(TradeContext.ORBCSTAT == PL_BCSTAT_CONFACC and TradeContext.ORBDWFLG == PL_BDWFLG_SUCC):
                TradeContext.MBRTRCST = PL_MBRTRCST_CNF
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTOPAY and TradeContext.ORBDWFLG == PL_BDWFLG_SUCC):
                TradeContext.MBRTRCST = PL_MBRTRCST_ACSUC
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTOPAY and TradeContext.ORBDWFLG == PL_BDWFLG_FAIL):
                TradeContext.MBRTRCST = PL_MBRTRCST_ACFAL
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_AUTOPAY and TradeContext.ORBDWFLG == PL_BDWFLG_WAIT):
                TradeContext.MBRTRCTS = PL_MBRTRCST_RCV
            elif (TradeContext.ORBCSTAT == PL_BCSTAT_CANC and TradeContext.ORBDWFLG == PL_BDWFLG_SUCC):
                TradeContext.MBRTRCTS = PL_MBRTRCST_RUSH
            else:
                TradeContext.MBRTRCTS = PL_MBRTRCST_RCV
        
        TradeContext.CONT     = "ϵͳ�Զ��鸴ҵ��״̬��ѯ"
        
        TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
        TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
        
        ztcbka_insert_dict = {}
        if not rccpsMap1107CTradeContext2Dztcbka.map(ztcbka_insert_dict):
            return AfaFlowControl.ExitThisFlow("S999","Ϊ�鸴ҵ���ֵ丳ֵ�쳣")
            
        AfaLoggerFunc.tradeInfo(">>>����Ϊ״̬�鸴ҵ���ֵ丳ֵ")
        #=====================�Ǽ�״̬�鸴ҵ��======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�״̬��ѯ�鸴�Ǽǲ�")
        
        ret = rccpsDBTrcc_ztcbka.insert(ztcbka_insert_dict)
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","�Ǽ�״̬��ѯ�鸴�Ǽǲ��쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�����Ǽ�״̬��ѯ�鸴�Ǽǲ�")
        
        #=====================�޸�ԭ��ѯҵ���ѯ�鸴��ʶ============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�޸�ԭ��ѯҵ���ѯ�鸴��ʶ")
        
        orztcbka_update_dict = {'ISDEAL':PL_ISDEAL_ISDO,'NCCTRCST':TradeContext.NCCTRCST,'MBRTRCST':TradeContext.MBRTRCST}
        orztcbka_where_dict  = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}

        ret = rccpsDBTrcc_ztcbka.update(orztcbka_update_dict,orztcbka_where_dict)
        
        if ret <= 0:
            return AfaFlowControl.ExitThisFlow("S999","�޸�ԭ��ѯҵ���ѯ�鸴��ʶ�쳣")
            
        AfaLoggerFunc.tradeInfo(">>>�����޸�ԭ��ѯҵ���ѯ�鸴��ʶ")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        #=====================Ϊҵ��״̬�鸴���ĸ�ֵ================================
        AfaLoggerFunc.tradeInfo(">>>��ʼΪҵ��״̬�鸴���ĸ�ֵ")
        
        TradeContext.sysType  = 'rccpst'
        TradeContext.TRCCO    = '9900507'
        TradeContext.MSGTYPCO = 'SET008'
        TradeContext.SNDBRHCO = TradeContext.BESBNO
        TradeContext.SNDCLKNO = TradeContext.BETELR
        TradeContext.SNDTRDAT = TradeContext.BJEDTE
        TradeContext.SNDTRTIM = TradeContext.BJETIM
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
        TradeContext.OPRTYPNO = '99'
        TradeContext.TRANTYP  = '0'
        
        AfaLoggerFunc.tradeInfo(">>>����Ϊҵ��״̬�鸴���ĸ�ֵ")
        #=====================����ҵ��״̬�鸴����==================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬�鸴����")
        
        AfaAfeFunc.CommAfe()
        
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow("S999","����ҵ��״̬�鸴�����쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬�鸴����")
        
        AfaLoggerFunc.tradeInfo(">>>�����Զ�ҵ��״̬�鸴����")
    
    else:
        AfaLoggerFunc.tradeInfo(">>>״̬��ѯҵ�������,�������Զ�ҵ��״̬�鸴����")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).ҵ��״̬��ѯ���Ľ���[RCC006_1107]�˳�***' )
    
    return True

