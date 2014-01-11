# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������ģ��(1.���ز��� 2.���Ĳ���).��Ʊ��ʧ/���
#===============================================================================
#   �����ļ�:   TRCC003_8505.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-08-04
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
import rccpsDBFunc,rccpsState,rccpsMap8505CTradeContext2Dbilbka_dict

from types import *
from rccpsConst import *

#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():

    AfaLoggerFunc.tradeInfo('>>>�����Ʊ��ʧ/��Ҳ���')
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
 
    #=====��ʼ��ѯ��Ʊ��Ϣ====
    AfaLoggerFunc.tradeDebug('>>>��ʼ��ѯ��Ʊ��Ϣ')
    bil_dict = {}
    if not rccpsDBFunc.getInfoBil(TradeContext.BILVER,TradeContext.BILNO,TradeContext.BILRS,bil_dict):
        return AfaFlowControl.ExitThisFlow('S999','��ѯ��Ʊ��Ϣ����')

    AfaLoggerFunc.tradeDebug('>>>������ѯ��Ʊ��Ϣ')

    #=====�ж��ֽ����ת�˻�Ʊ��ֻ���ֽ��Ʊ���Խ��й�ʧ====
    #if bil_dict['PAYWAY'] != '0':
    #    return AfaFlowControl.ExitThisFlow('S999','ת�˻�Ʊ�������ʧ/���')
        
    AfaLoggerFunc.tradeDebug('>>>�жϻ�Ʊ�Ƿ������ʧ')
    
    if bil_dict['REMBNKCO'] != TradeContext.SNDBNKCO:
        return AfaFlowControl.ExitThisFlow('S999','ֻ����ǩ���н��й�ʧ����')
    
    AfaLoggerFunc.tradeDebug('>>>�ж�ǩ���к͹�ʧ���Ƿ�һ��')

    if bil_dict['SEAL'] == '':
        return AfaFlowControl.ExitThisFlow('S999','��Ѻ�մ���')
    else:
        TradeContext.SEAL = bil_dict['SEAL']

    AfaLoggerFunc.tradeDebug('>>>������Ѻ�ж�')
    
    #=====��ѯ���ݿ�====
    records = {}
    ret = rccpsDBFunc.getTransBil(bil_dict['NOTE1'],bil_dict['NOTE2'],records)
    if( ret == False):
        return AfaFlowControl.ExitThisFlow('A099', '�޴�����')

    if str(bil_dict['BILAMT']) == '':
        return AfaFlowControl.ExitThisFlow('S999','���մ���')
    else:
        TradeContext.OCCAMT = str(bil_dict['BILAMT'])

    TradeContext.PYRACC  =  bil_dict['PYRACC']
    TradeContext.PYRNAM  =  bil_dict['PYRNAM']
    TradeContext.PYRADDR =  bil_dict['PYRADDR']
    TradeContext.PYEACC  =  bil_dict['PYEACC']
    TradeContext.PYENAM  =  bil_dict['PYENAM']
    TradeContext.PYEADDR =  bil_dict['PYEADDR']
    TradeContext.BILDAT  =  bil_dict['BILDAT']
    TradeContext.RCVBNKCO  =  bil_dict['PAYBNKCO']
    TradeContext.RCVBNKNM  =  bil_dict['PAYBNKNM']
    
    TradeContext.BBSSRC  =  records['BBSSRC']
    TradeContext.OPRNO   =  records['OPRNO']
    
        
    AfaLoggerFunc.tradeDebug('>>>��ʼ�жϻ�Ʊ��������')

    #=====�ж�TRCCO��Ʊ��������====
    if TradeContext.TRCCO == '2100102':
        #=====��Ʊ��ʧ====
        if TradeContext.SNDBNKCO != bil_dict['REMBNKCO']:
            return AfaFlowControl.ExitThisFlow('S999','��Ʊ������ǩ���н��й�ʧ')
        #=====�жϻ�Ʊ״̬�Ƿ� ǩ�� ���� ��� ״̬====
        if not (bil_dict['HPSTAT'] == PL_HPSTAT_SIGN or bil_dict['HPSTAT'] == PL_HPSTAT_DEHG):
            return AfaFlowControl.ExitThisFlow('S999','��Ʊ��ǰ״̬[' + bil_dict['HPSTAT'] + ']��������й�ʧ')
        
        #=====���OPRNO  PL_HPOPRNO_GS ��ʧ====
        TradeContext.OPRNO   =  PL_HPOPRNO_GS
    elif TradeContext.TRCCO == '2100104':
        #=====��Ʊ���====
        if TradeContext.SNDBNKCO != bil_dict['REMBNKCO']:
            return AfaFlowControl.ExitThisFlow('S999','��Ʊ�����ɹ�ʧ�н��н��')
        #=====�жϻ�Ʊ״̬�Ƿ� ��ʧ ״̬====
        if not bil_dict['HPSTAT'] == PL_HPSTAT_HANG:
            return AfaFlowControl.ExitThisFlow('S999','��Ʊ��ǰ״̬[' + bil_dict['HPSTAT'] + ']��������н��')
            
        #=====���OPRNO  PL_HPOPRNO_JG ���====
        TradeContext.OPRNO   =  PL_HPOPRNO_JG
    else:
        return AfaFlowControl.ExitThisFlow('S999','��Ʊ�������ʹ���')

    AfaLoggerFunc.tradeDebug('>>>�����жϻ�Ʊ��������')

    #=====PL_BILTYP_CASH  0  �ֽ�====
    if bil_dict['BILTYP'] == PL_BILTYP_CASH:
        #=====�ֽ��Ʊ====
        TradeContext.ROPRTPNO  =  ''
    else:
        #=====ת�˻�Ʊ====
        TradeContext.ROPRTPNO  =  '21'

    AfaLoggerFunc.tradeDebug('>>>�����жϻ�Ʊ����')
    
    #=====�ֵ丳ֵ====
    TradeContext.DCFLG = PL_DCFLG_DEB

    bilbka_dict = {}
    if not rccpsMap8505CTradeContext2Dbilbka_dict.map(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�ֵ丳ֵ����')

    AfaLoggerFunc.tradeDebug('>>>�����ֵ丳ֵ')
    AfaLoggerFunc.tradeDebug('>>>��ʼ�Ǽǻ�Ʊҵ����Ϣ�Ǽǲ�')

    #=====�Ǽǻ�Ʊҵ����Ϣ�Ǽǲ�====
    if not rccpsDBFunc.insTransBil(bilbka_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǻ�Ʊҵ����Ϣ�Ǽǲ�����')

    AfaDBFunc.CommitSql()
    
    AfaLoggerFunc.tradeDebug('>>>�����Ǽǻ�Ʊҵ����Ϣ�Ǽǲ�')
    AfaLoggerFunc.tradeDebug('>>>��ʼ����ũ��������')

    TradeContext.TRANTYP   = '0'                #��������
    TradeContext.OPRTYPNO  = PL_TRCCO_HP        #ҵ������ PL_TRCCO_HP 21 ��Ʊ
    
    #begin 20110614 ����̩ �޸� ����ũ�������ĵ�Ʊ��Ϊ8λ
    TradeContext.BILNO = TradeContext.BILNO[-8:]
    #end
    
    return True


#=====================���׺���================================================
def SubModuleDoSnd():

    AfaLoggerFunc.tradeDebug('>>>��������ũ��������')
    AfaLoggerFunc.tradeDebug('>>>��ʼ״̬���')

    sstlog = {}

    sstlog['BJEDTE'] = TradeContext.BJEDTE
    sstlog['BSPSQN'] = TradeContext.BSPSQN
    sstlog['BCSTAT'] = PL_BCSTAT_SND
    sstlog['NOTE3']  = TradeContext.errorMsg

    if TradeContext.errorCode == '0000':
        sstlog['BDWFLG'] = PL_BDWFLG_SUCC
    else:
        sstlog['BDWFLG'] = PL_BDWFLG_FAIL

    #=====�޸�sstlog��������====
    if not rccpsState.setTransState(sstlog):
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()

    AfaLoggerFunc.tradeDebug('>>>����״̬���')

    
    return True
    
