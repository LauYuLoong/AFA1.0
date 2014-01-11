# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�����˽���.����ѯ
#=================================================================
#   �����ļ�:   TRCC003_8560.py
#   �޸�ʱ��:   2008-10-21
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc
import rccpsDBTrcc_balbka,rccpsDBTrcc_paybnk,rccpsDBTrcc_subbra
import rccpsMap8560CTradeContext2Dbalbka
from types import *
from rccpsConst import *
import jiami

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.����ѯ[8560] ����")
    
    AfaLoggerFunc.tradeInfo("����ǰ����(���ز���,����ǰ����)")
    
    #=====У���������Ƿ����====
    if not TradeContext.existVariable("PYITYP"):
        return AfaFlowControl.ExitThisFlow('A099','�ʻ����Ͳ���Ϊ��')
        
    #=====�õ���Ա�к�====
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    
    #���ܿͻ�����
    MIMA = '                '
    #PIN = '888888'
    #ACC = '12311111111111111111111111111111'
    PIN  = TradeContext.CURPIN
    ACC  = TradeContext.PYEACC
    AfaLoggerFunc.tradeDebug('����[' + PIN + ']')
    AfaLoggerFunc.tradeDebug('�˺�[' + ACC + ']')
    ret = jiami.secEncryptPin(PIN,ACC,MIMA)
    if ret != 0:
        AfaLoggerFunc.tradeDebug("ret=[" + str(ret) + "]")
        return AfaFlowControl.ExitThisFlow('M9999','���ü��ܷ�����ʧ��')
    else:
        TradeContext.CURPIN = MIMA
        AfaLoggerFunc.tradeDebug('����new[' + TradeContext.CURPIN + ']')
    
    #=====��֯����ѯ������====
    AfaLoggerFunc.tradeInfo("��ʼ��֯����ѯ������")
    
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET009'
#    TradeContext.RCVMBRCO = 
#    TradeContext.SNDMBRCO = 
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN    = ""
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "30"
    TradeContext.ROPRTPNO = ""
    TradeContext.TRANTYP  = "0"
    #=====ҵ��Ҫ�ؼ�====
#    TradeContext.TRCCO    =  
#    TradeContext.SNDBNKCO =
#    TradeContext.SNDBNKNM =
#    TradeContext.RCVBNKCO =
#    TradeContext.RCVBNKNM =
#    TradeContext.TRCDAT   =  
    TradeContext.TRCNO    =  TradeContext.SerialNo
    TradeContext.ORTRCCO  = ""
    TradeContext.ORTRCNO  = ""
    TradeContext.CUR      = "CNY" 
    TradeContext.OCCAMT   = "0.00"
#    TradeContext.CUSCHRG  = 
    TradeContext.PYRACC   = ""
#    TradeContext.PYEACC   = 
#    TradeContext.CURPIN   =
    TradeContext.STRINFO  = ""
    TradeContext.PRCCO    = ""           
            
    #=====�ж��ʻ�����====
    if( TradeContext.PYITYP == '0' ): #���п�
        AfaLoggerFunc.tradeInfo("�������п���������")
        TradeContext.TRCCO = '3000501'     
        #=====��չ����====
#        TradeContext.PYENAM = 
#        TradeContext.SCTRKINF =
#        TradeContext.THTRKINF =
        
    elif( TradeContext.PYITYP == '1' ): #����
        AfaLoggerFunc.tradeInfo("������۲�������")
        TradeContext.TRCCO = '3000502'    
        #=====��չ����====
#        TradeContext.PYENAM
#        TradeContext.BNKBKNO
        
    else:
        return AfaFlowControl.ExitThisFlow("S999", "�Ƿ��Ĳ�������")
        
    #=====�Ǽ�����ѯ�Ǽǲ�====
    AfaLoggerFunc.tradeInfo('���Ǽ��ֵ丳ֵ')
    insert_dict = {}
    rccpsMap8560CTradeContext2Dbalbka.map(insert_dict)
    insert_dict['OPRNO']    = '30'
    insert_dict['CUR']      = '01'
    insert_dict['MSGFLGNO'] = TradeContext.MSGFLGNO
    insert_dict['BRSFLG']   = PL_BRSFLG_SND
    
    
    AfaLoggerFunc.tradeInfo('��ʼ�Ǽ�����ѯ�Ǽǲ�')
    res = rccpsDBTrcc_balbka.insertCmt(insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','�Ǽ�����ѯ�Ǽǲ�ʧ��')
        
    AfaLoggerFunc.tradeInfo("����ǰ����(���ز���,����ǰ����) ����")
    
    return True    
        
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('���׺���')
    
    AfaLoggerFunc.tradeInfo('errorCode:' + TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo('errorMsg:' + TradeContext.errorMsg)
    
    #=====�ж�AFE�Ƿ��ͳɹ�====
    if TradeContext.errorCode != '0000':
        #=====�������ķ����룬�͸���====
        AfaLoggerFunc.tradeInfo("��ʼ��������ѯ�Ǽǲ�")
        update_dict = {'PRCCO':'RCCS1105','STRINFO':'AFE����ʧ��'}
        where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        res = rccpsDBTrcc_balbka.updateCmt(update_dict,where_dict)
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','��������ѯ�Ǽǲ�ʧ��')
           
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,'�����ķ�������ѯ������ʧ��')
    
    else:
        AfaLoggerFunc.tradeInfo('���ͳɹ�')
        
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg  = '���׳ɹ�'
        
    AfaLoggerFunc.tradeInfo('���׺��� ����')
    
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.����ѯ[8560] �˳�")
    
    return True
    