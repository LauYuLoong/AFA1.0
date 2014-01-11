# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).ϵͳ״̬������Ľ���
#===============================================================================
#   ģ���ļ�:   TRCC006.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-02
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBTrcc_mbrifa,rccpsMap0000Dout_context2CTradeContext,rccpsCronFunc


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ϵͳ״̬������Ľ���[RCC00R6_1121]����***' )
    
    #=================��ѯ�������ҵ��״̬��ϵͳ״̬============================
    mbrifa_where_dict = {}
    mbrifa_where_dict['OPRTYPNO'] = TradeContext.RELOPRTYPNO
    
    mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
    if mbrifa_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","��ѯ����ϵͳ״̬��Ϣ�쳣")
        
    if  len(mbrifa_dict) <= 0:
        return AfaFlowControl.ExitThisFlow("S999","�����ҵ�����ͱ���ϵͳ״̬��Ϣ")
    
    #=================У�鱨���¹�������============================================
    if int(TradeContext.NWWKDAT) < int(mbrifa_dict['NWWKDAT']):
        AfaLoggerFunc.tradeInfo("�����¹�������[" + TradeContext.NWWKDAT + "]�ڱ����¹�������[" + mbrifa_dict['NWWKDAT'] + "]֮ǰ,�����˱���,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
        #======ΪͨѶ��ִ���ĸ�ֵ===================================================
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        #out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        #out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        #out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
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
        
    elif int(TradeContext.NWWKDAT) == int(mbrifa_dict['NWWKDAT']):
        #============�����¹��������뱾���¹���������ͬ,У�鱨���¹���״̬======
        if int(TradeContext.NWSYSST) <= int(mbrifa_dict['NWSYSST']):
            AfaLoggerFunc.tradeInfo("�����¹���״̬[" + TradeContext.NWSYSST + "]���ڱ����¹���״̬[" + mbrifa_dict['NWSYSST'] + "]֮��,�����˱���,������һ����,���ͱ�ʾ�ɹ���ͨѶ��ִ")
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
    
    #�������б��ĺ���������Ĵ���
    #ͨ��ͨ��˳��10-20-30-10
    if TradeContext.RELOPRTYPNO == "30":
        if mbrifa_dict['NWSYSST'] == '10' and TradeContext.NWSYSST != '20':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]ҵ��ǰҵ��״̬Ϊ�ռ俪ʼ[10],�����б����б��״̬��ҵ���ֹ׼��[20],ֹͣ����")
            
        if mbrifa_dict['NWSYSST'] == '20' and TradeContext.NWSYSST != '30':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]ҵ��ǰҵ��״̬Ϊҵ���ֹ׼��[20],�����б����б��״̬��ҵ���ֹ[30],ֹͣ����")
            
        if mbrifa_dict['NWSYSST'] == '30' and TradeContext.NWSYSST != '10':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]ҵ��ǰҵ��״̬Ϊҵ���ֹ[30],�����б����б��״̬���ռ俪ʼ[10],ֹͣ����")
    #��һ�Ʊ˳��10-30-10
    else:
        if mbrifa_dict['NWSYSST'] == '10' and TradeContext.NWSYSST != '30':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]ҵ��ǰҵ��״̬Ϊ�ռ俪ʼ[10],�����б����б��״̬��ҵ���ֹ[30],ֹͣ����")
            
        if mbrifa_dict['NWSYSST'] == '30' and TradeContext.NWSYSST != '10':
            return AfaFlowControl.ExitThisFlow("S999","[" + TradeContext.RELOPRTYPNO + "]ҵ��ǰҵ��״̬Ϊҵ���ֹ[30],�����б����б��״̬���ռ俪ʼ[10],ֹͣ����")
    
    mbrifa_update_dict = {}
    mbrifa_update_dict['ORWKDAT'] = mbrifa_dict['NWWKDAT']
    mbrifa_update_dict['ORSYSST'] = mbrifa_dict['NWSYSST']
    mbrifa_update_dict['NWWKDAT'] = TradeContext.NWWKDAT
    mbrifa_update_dict['NWSYSST'] = TradeContext.NWSYSST
    mbrifa_update_dict['HOLFLG']  = TradeContext.HOLFLG
    mbrifa_update_dict['NOTE1']   = mbrifa_dict['NWWKDAT']
    
    ret = rccpsDBTrcc_mbrifa.update(mbrifa_update_dict,mbrifa_where_dict)
    if ret <= 0:
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
        return AfaFlowControl.ExitThisFlow("S999","����ϵͳ״̬�쳣")
    
    #======����ϵͳ״̬Ϊҵ���ֹ,��򿪶���ϵͳ����============================
    if TradeContext.NWSYSST == '30' and TradeContext.HOLFLG == '2':
        if TradeContext.RELOPRTYPNO == '20':
            #====�򿪻�Ҷ���ϵͳ����=======================================
            AfaLoggerFunc.tradeInfo(">>>��ʼ�򿪻�Ҷ���ϵͳ����")
            
            if not rccpsCronFunc.openCron("00031"):
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                return AfaFlowControl.ExitThisFlow("S999","�򿪻�Ҷ���ϵͳ�����쳣")
                
            AfaLoggerFunc.tradeInfo(">>>�����򿪻�Ҷ���ϵͳ����")
            
            #====�򿪻�Ʊ����ϵͳ����=======================================
            AfaLoggerFunc.tradeInfo(">>>��ʼ�򿪻�Ʊ����ϵͳ����")
            
            if not rccpsCronFunc.openCron("00041"):
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                return AfaFlowControl.ExitThisFlow("S999","�򿪻�Ʊ����ϵͳ�����쳣")
            
            AfaLoggerFunc.tradeInfo(">>>�����򿪻�Ʊ����ϵͳ����")
            
        elif TradeContext.RELOPRTYPNO == '30':
            #====��ͨ��ͨ�Ҷ���ϵͳ����===================================
            AfaLoggerFunc.tradeInfo(">>>��ʼ��ͨ��ͨ�Ҷ���ϵͳ����")
            
            if not rccpsCronFunc.openCron("00061"):
                if not AfaDBFunc.RollbackSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    AfaLoggerFunc.tradeError(">>>Rollback�쳣")
                AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
                return AfaFlowControl.ExitThisFlow("S999","��ͨ��ͨ�Ҷ���ϵͳ�����쳣")
                
            AfaLoggerFunc.tradeInfo(">>>������ͨ��ͨ�Ҷ���ϵͳ����")
            
            #====����Ϣ��ҵ����ͳ��ϵͳ����======================
            AfaLoggerFunc.tradeInfo(">>>��ʼ����Ϣ��ҵ����ͳ��ϵͳ����")
            
#            if not rccpsCronFunc.openCron("00067"):
#                if not AfaDBFunc.RollbackSql( ):
#                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
#                    AfaLoggerFunc.tradeError(">>>Rollback�쳣")
#                AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
#                return AfaFlowControl.ExitThisFlow("S999","����Ϣ��ҵ����ͳ��ϵͳ�����쳣")
            
#            AfaLoggerFunc.tradeInfo(">>>��������Ϣ��ҵ����ͳ��ϵͳ����")
            
            
            
    #======��ͨ��ͨ����ϵͳ״̬Ϊ�ռ俪ʼ,��������к���Чϵͳ����===================
    if TradeContext.NWSYSST == '10' and TradeContext.RELOPRTYPNO == '30':
        #====��ʼ�������к���Чϵͳ����=======================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�������к���Чϵͳ����")
        
        if not rccpsCronFunc.openCron("00050"):
            if not AfaDBFunc.RollbackSql( ):
                AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeError(">>>Rollback�쳣")
            AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")
            return AfaFlowControl.ExitThisFlow("S999","�������к���Чϵͳ�����쳣")
            
        AfaLoggerFunc.tradeInfo(">>>�����������к���Чϵͳ����")
            
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
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ϵͳ״̬������Ľ���[RCC00R6_1121]�˳�***' )
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).ϵͳ״̬������Ľ���[RCC00R6_1121]����***' )
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).ϵͳ״̬������Ľ���[RCC00R6_1121]�˳�***' )
    return True
        
