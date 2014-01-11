# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���ļ���).�����ֽ�ͨ��
#==============================================================================
#   �����ļ�:   TRCC002_8562.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-10-30
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,jiami
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_pamtbl,rccpsMap8562CTradeContext2Dwtrbka_dict


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ͨ��ͨ��.�������������[RCC003_8562]����***' )

    #��鱾�����Ƿ���ͨ��ͨ��ҵ��Ȩ��
    if not rccpsDBFunc.chkTDBESAuth(TradeContext.BESBNO):
        return AfaFlowControl.ExitThisFlow("S999","��������ͨ��ͨ��ҵ��Ȩ��")
    
    #=====�������ж�====
    if TradeContext.SNDSTLBIN == TradeContext.RCVSTLBIN:
        return AfaFlowControl.ExitThisFlow('S999','ͬһ�����в���������ҵ��')

    #=====�˻������ж�====
    if not TradeContext.existVariable('PYRTYP'):
        return AfaFlowControl.ExitThisFlow('S999','�˻����Ͳ�����[PYRTYP]')

    if TradeContext.PYRTYP == '0':
        #=====���п�====        
        if len(TradeContext.PYRNAM)   == 0:
            return AfaFlowControl.ExitThisFlow('S999','����������[PYRNAM]������Ϊ��')
        if len(TradeContext.SCTRKINF) == 0:
            return AfaFlowControl.ExitThisFlow('S999','���ŵ�[SCTRKINF]��Ϣ������Ϊ��')
        #if len(TradeContext.THTRKINF) == 0:
        #    return AfaFlowControl.ExitThisFlow('S999','���ŵ�[THTRKINF]��Ϣ������Ϊ��')
            
        if len(TradeContext.SCTRKINF) > 37:
            return AfaFlowControl.ExitThisFlow('S999','�ŵ���Ϣ�Ƿ�')
            
        #if len(TradeContext.THTRKINF) > 104:
        #    return AfaFlowControl.ExitThisFlow('S999','�ŵ���Ϣ�Ƿ�')
    elif TradeContext.PYRTYP == '1':
        #=====����====
        if len(TradeContext.BNKBKNO)  == 0:
            return AfaFlowControl.ExitThisFlow('S999','���ۺ���[BNKBKNO]������Ϊ��')
        if float(TradeContext.BNKBKBAL) == 0.0:
            return AfaFlowControl.ExitThisFlow('S999','�������[BNKBKBAL]������Ϊ��')
            
        TradeContext.SCTRKINF = ''.rjust(37,'0')
        TradeContext.THTRKINF = ''.rjust(37,'0')
    else:
        return AfaFlowControl.ExitThisFlow('S999','�˻����ʹ���')
    
    #=====���׽���ж�====
    sel_dict = {}
    sel_dict['BPARAD'] = 'TD001'    #ͨ��ͨ��ƾ֤���У��
    
    dict = rccpsDBTrcc_pamtbl.selectu(sel_dict) 
    AfaLoggerFunc.tradeInfo('dict='+str(dict))

    if dict == None:
        return AfaFlowControl.ExitThisFlow('S999','У�齻�׽��ʧ��')
    if len(dict) == 0:
        return AfaFlowControl.ExitThisFlow('S999','��ѯPAMTBLУ�齻�׽����¼����')
    
    #=====�ж�ũ�������Ĺ涨У��ƾ֤����====
    if float(TradeContext.OCCAMT) >= float(dict['BPADAT']):
         #=====���׽�����ũ�������Ĺ涨����Ҫ����֤��====
         if TradeContext.existVariable('CERTTYPE') and len(TradeContext.CERTTYPE) == 0:
             return AfaFlowControl.ExitThisFlow('S999','��ѡ��֤������!')
         if TradeContext.existVariable('CERTNO')   and len(TradeContext.CERTNO)   == 0:
             return AfaFlowControl.ExitThisFlow('S999','������֤������!')

    #���ܿͻ�����
    MIMA = '                '
    #PIN = '888888'
    #ACC = '12311111111111111111111111111111'
    PIN  = TradeContext.CURPIN
    ACC  = TradeContext.PYRACC
    AfaLoggerFunc.tradeDebug('����[' + PIN + ']')
    AfaLoggerFunc.tradeDebug('�˺�[' + ACC + ']')
    ret = jiami.secEncryptPin(PIN,ACC,MIMA)
    if ret != 0:
        AfaLoggerFunc.tradeDebug("ret=[" + str(ret) + "]")
        return AfaFlowControl.ExitThisFlow('M9999','���ü��ܷ�����ʧ��')
    else:
        TradeContext.CURPIN = MIMA
        AfaLoggerFunc.tradeDebug('����new[' + TradeContext.CURPIN + ']')

    #=====�ֶθ�ֵ====
    TradeContext.OPRNO   =  PL_TDOPRNO_TD          #ҵ������
    TradeContext.DCFLG   =  PL_DCFLG_DEB           #�����ʶ

    #=====�ֵ丳ֵ���������ݿ�====
    wtrbka_dict = {}
    if not rccpsMap8562CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�ֵ丳ֵ����!')
        
    wtrbka_dict['MSGFLGNO'] = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo       #���ı�ʶ��

    #=====�������ݿ��====
    if not rccpsDBFunc.insTransWtr(wtrbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽ�ͨ��ͨ��ҵ��Ǽǲ��쳣')
    AfaDBFunc.CommitSql( )

    #=====����ҵ��״̬Ϊ���ʹ�����====
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���ʹ�����")
    
    stat_dict = {}
    stat_dict['BJEDTE'] = TradeContext.BJEDTE       #��������
    stat_dict['BSPSQN'] = TradeContext.BSPSQN       #�������
    stat_dict['BCSTAT'] = PL_BCSTAT_SND             #PL_BCSTAT_SND  ����
    stat_dict['BDWFLG'] = PL_BDWFLG_WAIT            #PL_BDWFLG_WAIT ������
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','����״̬Ϊ���ʹ������쳣')
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���ʹ�����")
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���ʹ�����")
    
    #=====����ũ��������====
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ũ�������Ĵ���")
    
    TradeContext.MSGTYPCO   =   'SET004'              #���������
    TradeContext.OPRTYPNO   =   '30'                  #ͨ��ͨ��
    
    #=====������������ȡ��ʽ�ж��Ƿ���ũ��������====
    TradeContext.sCuschrg = TradeContext.CUSCHRG
    if TradeContext.CHRGTYP != PL_CHRG_TYPE:          #PL_CHRG_TYPE 1 ת��
        #=====ת����ȡ������====
        TradeContext.CUSCHRG = '0.0'
    
    AfaLoggerFunc.tradeDebug(">>>��������ũ�������Ĵ���")

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ͨ��ͨ��.�������������[RCC003_8562]�˳�***' )
    return True
#=====================���׺���===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ͨ��ͨ��.�������������[RCC003_8562]����***' )
    
    #=====�ж����ķ����Ƿ�ɹ�====
    stat_dict = {}
    stat_dict['BJEDTE']  = TradeContext.BJEDTE
    stat_dict['BSPSQN']  = TradeContext.BSPSQN
    stat_dict['BESBNO']  = TradeContext.BESBNO
    stat_dict['BETELR']  = TradeContext.BETELR
    stat_dict['BCSTAT']  = PL_BCSTAT_SND             #PL_BCSTAT_SND  ����
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���ͳɹ�")    
    
    if TradeContext.errorCode != '0000':
        stat_dict['BDWFLG'] = PL_BDWFLG_FAIL         #PL_BDWFLG_FAIL ʧ��
    else:
        stat_dict['BDWFLG'] = PL_BDWFLG_SUCC         #PL_BDWFLG_SUCC �ɹ�
        stat_dict['PRTCNT'] = 1
    
    if not rccpsState.setTransState(stat_dict):
        return AfaFlowControl.ExitThisFlow('S999','����״̬Ϊ���ͳɹ��쳣')
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���ͳɹ�")
    
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    TradeContext.CUSCHRG = TradeContext.sCuschrg
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ͨ��ͨ��.�������������[RCC003_8562]�˳�***' )
    
    return True
