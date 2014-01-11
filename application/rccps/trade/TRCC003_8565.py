# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��̨����
#==============================================================================
#   �����ļ�:   TRCC003_8565.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-11-29
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,HostContext
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsEntries,rccpsHostFunc,rccpsGetFunc
import rccpsDBTrcc_mpcbka
import rccpsMap8565CTradeContext2Dmpcbka


#=====================����ǰ����(���ز���,����ǰ����)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��̨����[TRCC003_8565]����***' )
    
    #=====У������ĺϷ���====
    if not TradeContext.existVariable("BOJEDT"):
        return AfaFlowControl.ExitThisFlow('A099','ԭ�������ڲ���Ϊ��')  
        
    if not TradeContext.existVariable("BOSPSQ"):
        return AfaFlowControl.ExitThisFlow('A099','ԭ������Ų���Ϊ��')
        
    if not TradeContext.existVariable("RESNNM"):
        return AfaFlowControl.ExitThisFlow('A099','����ԭ����Ϊ��')
    
    #��ѯԭ������Ϣ
    wtr_dict = {}
    
    if not rccpsDBFunc.getTransWtr(TradeContext.BOJEDT,TradeContext.BOSPSQ,wtr_dict):
        return AfaFlowControl.ExitThisFlow("S999","�޴˽���")
       
    #�ж�ԭ�����Ƿ�Ϊ����
    if( wtr_dict['BRSFLG'] != PL_BRSFLG_SND):
        return AfaFlowControl.ExitThisFlow('A099','�˽��׷�����,��ֹ����')
        
    #�жϱ��������׵������Ƿ�Ϊ����
    if( wtr_dict['NCCWKDAT'] != TradeContext.NCCworkDate ):
        return AfaFlowControl.ExitThisFlow('A099','�˽��׷ǵ��ս���,��ֹ����')
        
    #�жϵ�ǰ�����Ƿ�Ϊԭ���׻���
    if( wtr_dict['BESBNO'] != TradeContext.BESBNO ):
        return AfaFlowControl.ExitThisFlow('A099','��ǰ������ԭ���׻���,��ֹ����')
    
    #�жϵ�ǰ��Ա�Ƿ�Ϊԭ���׹�Ա
    if( wtr_dict['BETELR'] != TradeContext.BETELR ):
        return AfaFlowControl.ExitThisFlow('A099','��ǰ��Ա��ԭ���׹�Ա,��ֹ����')
    
    #�ж�ԭ����״̬�Ƿ��������
    AfaLoggerFunc.tradeInfo("��ʼ�ж�ԭ������Ϣ�Ƿ��������")
    
    #=====add by pgt 12-9=====
    #able_to_cancel = 1    #��������ı�ʾ��1Ϊ������0Ϊ����
    #
    #if wtr_dict['TRCCO'] in ('3000002','3000003','3000004','3000005'):    #ͨ����߱�ת��
    #    #״̬Ϊ:ȷ�ϸ���,����,���ʹ�����,���ͳɹ�,�������
    #    if(wtr_dict['BCSTAT'] == PL_BCSTAT_CONFPAY or wtr_dict['BCSTAT'] == PL_BCSTAT_MFESTL or (wtr_dict['BCSTAT'] == PL_BCSTAT_SND and (wtr_dict['BDWFLG'] == PL_BDWFLG_WAIT or wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC))):
    #        able_to_cancel = 0
    #        
    #elif wtr_dict['TRCCO'] in ('3000102','3000103','3000104','3000105'):    #ͨ�һ�����ת��
    #    #״̬Ϊ:����,����,���ʹ�����,���ͳɹ�,�������
    #    if(wtr_dict['BCSTAT'] == PL_BCSTAT_ACC or wtr_dict['BCSTAT'] == PL_BCSTAT_MFESTL or (wtr_dict['BCSTAT'] == PL_BCSTAT_SND and (wtr_dict['BDWFLG'] == PL_BDWFLG_WAIT or wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC))):
    #        able_to_cancel = 0
    #        
    #else:
    #    return AfaFlowControl.ExitThisFlow("S999","�����׷�ͨ���ͨ�������ཻ��,��ֹ����")
    #
    ##����ʧ���������
    #if(wtr_dict['BCSTAT'] == PL_BCSTAT_CANC and wtr_dict['BDWFLG'] == PL_BDWFLG_FAIL):   
    #    able_to_cancel = 0
    #     
    #if(able_to_cancel == 1):
    #    return AfaFlowControl.ExitThisFlow("S999","�˽��׵�ǰ״̬Ϊ[" + wtr_dict['BCSTAT'] + "][" + wtr_dict['BDWFLG'] + "],��ֹ����")
    #    
    #else:
    #    AfaLoggerFunc.tradeDebug('>>>>>>�˽��׵�ǰ״̬�������')
        
    if wtr_dict['TRCCO'] in ('3000002','3000003','3000004','3000005'):    #ͨ����߱�ת��
        #״̬Ϊ:ȷ�ϸ���,����,���ʹ�����,���ͳɹ�,�������
    	if not (wtr_dict['BCSTAT'] == PL_BCSTAT_CONFPAY or wtr_dict['BCSTAT'] == PL_BCSTAT_MFESTL or (wtr_dict['BCSTAT'] == PL_BCSTAT_SND and (wtr_dict['BDWFLG'] == PL_BDWFLG_WAIT or wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC))):
    	    return AfaFlowControl.ExitThisFlow("S999","�˽��׵�ǰ״̬Ϊ[" + wtr_dict['BCSTAT'] + "[" + wtr_dict['BDWFLG'] + "],��ֹ����")
    
    elif wtr_dict['TRCCO'] in ('3000102','3000103','3000104','3000105'):    #ͨ�һ�����ת��
        #״̬Ϊ:����,����,���ʹ�����,���ͳɹ�,�������
    	if not (wtr_dict['BCSTAT'] == PL_BCSTAT_ACC or wtr_dict['BCSTAT'] == PL_BCSTAT_MFESTL or (wtr_dict['BCSTAT'] == PL_BCSTAT_SND and (wtr_dict['BDWFLG'] == PL_BDWFLG_WAIT or wtr_dict['BDWFLG'] == PL_BDWFLG_SUCC))):
    		return AfaFlowControl.ExitThisFlow("S999","�˽��׵�ǰ״̬Ϊ[" + wtr_dict['BCSTAT'] + "][" + wtr_dict['BDWFLG'] + "],��ֹ����")
    else:
        return AfaFlowControl.ExitThisFlow("S999","�����׷�ͨ���ͨ�������ཻ��,��ֹ����")
        
    if wtr_dict['BCSTAT'] == PL_BCSTAT_ACC and wtr_dict['BDWFLG'] != PL_BDWFLG_SUCC:
        #ԭ���׵�ǰ״̬Ϊ����,����ת�����ʶ�ǳɹ�,�����8816��ѯ�˱�ҵ����������״̬
        
        AfaLoggerFunc.tradeDebug('>>>����8816���Ҹ�ҵ��[' + wtr_dict['BSPSQN'] + '״̬')

        TradeContext.HostCode = '8816'                   #����������
        TradeContext.OPFG     = '1'                      #��ѯ����
        TradeContext.NBBH     = 'RCC'                    #����ҵ���ʶ
        TradeContext.FEDT     = wtr_dict['FEDT']         #ԭǰ������
        TradeContext.RBSQ     = wtr_dict['RBSQ']         #ԭǰ����ˮ��
        TradeContext.DAFG     = '1'                      #Ĩ/���˱�־  1:��  2:Ĩ
        TradeContext.BESBNO   = wtr_dict['BESBNO']       #������
        TradeContext.BETELR   = wtr_dict['BETELR']       #��Ա��

        rccpsHostFunc.CommHost( TradeContext.HostCode )

        #=====������������====
        if TradeContext.errorCode == '0000':
            if HostContext.O1STCD == '0':
                #�������ѳɹ���������,�޸�ԭ����״̬Ϊ���˳ɹ�
                stat_dict = {}
                stat_dict['BJEDTE'] = TradeContext.BOJEDT
                stat_dict['BOSPSQ'] = tradeContext.BOSPSQ
                stat_dict['BCSTAT'] = PL_BCSTAT_ACC
                stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                stat_dict['TRDT']   = HostContext.O1DADT           #��������
                stat_dict['TLSQ']   = HostContext.O1AMTL           #������ˮ
                stat_dict['MGID']   = '0000'
                stat_dict['STRINFO']= '�����ɹ�'
                
                if not rccpsState.setTransState(stat_dict):
                    return AfaFlowControl.ExitThisFlow('S999','����ԭ����ҵ��״̬Ϊ���˳ɹ��쳣') 
                
                if not AfaDBFunc.CommitSql( ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            else:
                return AfaFlowControl.ExitThisFlow('S999','ԭ������������״̬����̨����,��ֹ�ύ')
        
        elif TradeContext.errorCode == 'XCR0001':
            AfaLoggerFunc.tradeInfo(">>>��������ԭ���׼���ʧ��,��������")
            
        else:
            return AfaFlowControl.ExitThisFlow('S999','��ѯ���������쳣,���Ժ��ٳ���')
            
    
    AfaLoggerFunc.tradeInfo("�����ж�ԭ������Ϣ�Ƿ��������")
    		
    #�Ǽǹ�̨�����Ǽǲ�
    AfaLoggerFunc.tradeInfo("��ʼ�Ǽǹ�̨�����Ǽǲ�")
    
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = wtr_dict['RCVMBRCO']
    TradeContext.ORTRCDAT = wtr_dict['TRCDAT']
    TradeContext.OPRNO    = PL_TDOPRNO_CX
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.NCCworkDate + TradeContext.SerialNo
    TradeContext.ORMFN    = wtr_dict['MSGFLGNO']
    TradeContext.TRCCO    = "3000504" 
    TradeContext.TRCNO    = TradeContext.SerialNo
    TradeContext.ORTRCCO  = wtr_dict['TRCCO']
    TradeContext.ORTRCNO  = wtr_dict['TRCNO']
    TradeContext.SNDBNKCO = wtr_dict['SNDBNKCO']
    TradeContext.SNDBNKNM = wtr_dict['SNDBNKNM']
    TradeContext.RCVBNKCO = wtr_dict['RCVBNKCO']
    TradeContext.RCVBNKNM = wtr_dict['RCVBNKNM']
    
    insert_dict = {}
    
    if not rccpsMap8565CTradeContext2Dmpcbka.map(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǹ�̨�����Ǽǲ�ʧ��')
    
    AfaLoggerFunc.tradeInfo('>>>��ʼ�Ǽǹ�̨�����Ǽǲ�')
    res = rccpsDBTrcc_mpcbka.insertCmt(insert_dict)
    if( res <= 0 ):
        return AfaFlowControl.ExitThisFlow('S999','�Ǽǹ�̨�����Ǽǲ�ʧ��')
        
    AfaLoggerFunc.tradeInfo('>>>�����Ǽǹ�̨�����Ǽǲ�')
    
    #Ϊ���͹������������׼��
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET009'
    TradeContext.RCVSTLBIN= wtr_dict['RCVMBRCO']
    #TradeContext.SNDBRHCO = TradeContext.BESBNO
    #TradeContext.SNDCLKNO = TradeContext.BETELR
    #TradeContext.SNDTRDAT = TradeContext.BJEDTE
    #TradeContext.SNDTRTIM = TradeContext.BJETIM
    #TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    #TradeContext.ORMFN    = wtr_dict['MSGFLGNO']
    #TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "30"
    TradeContext.ROPRTPNO = "30"
    TradeContext.TRANTYP  = "0"
    #=====ҵ��Ҫ�ؼ�====
    TradeContext.CUR      = wtr_dict['CUR']
    TradeContext.OCCAMT   = str(wtr_dict['OCCAMT'])
    
    #�����Ѵ���
    if wtr_dict['TRCCO'] == '3000002' or wtr_dict['TRCCO'] == '3000003' or wtr_dict['TRCCO'] == '3000004' or wtr_dict['TRCCO'] == '3000005':
        TradeContext.CUSCHRG  = "0.00"
    elif wtr_dict['TRCCO'] == '3000102' or wtr_dict['TRCCO'] == '3000103' or wtr_dict['TRCCO'] == '3000104' or wtr_dict['TRCCO'] == '3000105':
        if wtr_dict['CHRGTYP'] == '1':
            TradeContext.CUSCHRG = str(wtr_dict['CUSCHRG'])
        else:
            TradeContext.CUSCHRG = '0.00'
            
    TradeContext.PYRACC   = wtr_dict['PYRACC']
    TradeContext.PYRNAM   = wtr_dict['PYRNAM']
    TradeContext.PYEACC   = wtr_dict['PYEACC']
    TradeContext.PYENAM   = wtr_dict['PYENAM']
    TradeContext.CURPIN   = ""
    TradeContext.STRINFO  = ""
    TradeContext.PRCCO    = ""
    #=====��չҪ�ؼ�====
    TradeContext.RESNCO = TradeContext.RESNNM  
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��̨����[TRCC003_8565]�˳�***' )
    return True

#=====================���׺���===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).��̨����[TRCC003_8565]����***' )
    
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    #�ж��Ƿ��ͳɹ�
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo(">>>�������ķ��ͳɹ�")
        
    else:
        AfaLoggerFunc.tradeInfo(">>>�������ķ���ʧ��")
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ĳ���).��̨����[TRCC003_8565]�˳�***' )
    return True
    
