# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ TradeContext �ֵ䵽 acckj �ֵ�ӳ�亯��
#
#   ��    �ߣ�  ����̩
#   �����ļ�:   rccpsMap8595CTradeContext2Dacckj.py
#   �޸�ʱ��:   20110511
##################################################################
import AfaLoggerFunc,TradeContext
from types import *
def map(to_dict):
    if TradeContext.existVariable('TRCDAT'):     #ί������                            
        to_dict['TRCDAT'] = TradeContext.TRCDAT                                       
        AfaLoggerFunc.tradeDebug('acckj[TRCDAT] = ' + str(to_dict['TRCDAT']))         
    else:                                                                             
        AfaLoggerFunc.tradeDebug("TradeContext.OPRATTNO������")                       
                                                                                      
    if TradeContext.existVariable('BSPSQN'):        #ί����ˮ��(���ı�ʶ)
        to_dict['BSPSQN'] = TradeContext.BSPSQN
        AfaLoggerFunc.tradeDebug('acckj[BSPSQN] = ' + str(to_dict['BSPSQN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BSPSQN������")
        
    if TradeContext.existVariable('MSGFLGNO'):  #���ı�ʶ��            
        to_dict['MSGFLGNO'] = TradeContext.MSGFLGNO
        AfaLoggerFunc.tradeDebug('acckj[MSGFLGNO] = ' + str(to_dict['MSGFLGNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.MSGFLGNO������")
        
    if TradeContext.existVariable('ORMFN'):  #�ο����ı�ʶ��            
        to_dict['ORMFN'] = TradeContext.ORMFN
        AfaLoggerFunc.tradeDebug('acckj[ORMFN] = ' + str(to_dict['ORMFN']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORMFN������")

    if TradeContext.existVariable('TRCCO'):        #������  
        to_dict['TRCCO'] = TradeContext.TRCCO
        AfaLoggerFunc.tradeDebug('acckj[TRCCO] = ' + str(to_dict['TRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCCO������")
        
    if TradeContext.existVariable('BRSFLG'):        #�����ʱ�ʶ
        to_dict['BRSFLG'] = TradeContext.BRSFLG
        AfaLoggerFunc.tradeDebug('acckj[BRSFLG] = ' + str(to_dict['BRSFLG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BRSFLG������")

    if TradeContext.existVariable('BESBNO'):        #������
        to_dict['BESBNO'] = TradeContext.BESBNO
        AfaLoggerFunc.tradeDebug('acckj[BESBNO] = ' + str(to_dict['BESBNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BESBNO������")

    if TradeContext.existVariable('BEACSB'):        #���������  
        to_dict['BEACSB'] = TradeContext.BEACSB
        AfaLoggerFunc.tradeDebug('acckj[BEACSB] = ' + str(to_dict['BEACSB']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEACSB������")

    if TradeContext.existVariable('BETELR'):        #��Ա��
        to_dict['BETELR'] = TradeContext.BETELR
        AfaLoggerFunc.tradeDebug('acckj[BETELR] = ' + str(to_dict['BETELR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BETELR������")

    if TradeContext.existVariable('BEAUUS'):        #��Ȩ��Ա
        to_dict['BEAUUS'] = TradeContext.BEAUUS
        AfaLoggerFunc.tradeDebug('acckj[BEAUUS] = ' + str(to_dict['BEAUUS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUUS������")

    if TradeContext.existVariable('BEAUPS'):       #��Ȩ��Ա����  
        to_dict['BEAUPS'] = TradeContext.BEAUPS
        AfaLoggerFunc.tradeDebug('acckj[BEAUPS] = ' + str(to_dict['BEAUPS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BEAUPS������")

    if TradeContext.existVariable('TERMID'):       #�ն˺� 
        to_dict['TERMID'] = TradeContext.TERMID
        AfaLoggerFunc.tradeDebug('acckj[TERMID] = ' + str(to_dict['TERMID']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TERMID������")

    if TradeContext.existVariable('OPTYPE'):        #��������
        to_dict['OPTYPE'] = TradeContext.OPTYPE
        AfaLoggerFunc.tradeDebug('acckj[OPTYPE] = ' + str(to_dict['OPTYPE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OPTYPE������")

    if TradeContext.existVariable('NCCWKDAT'):     #ũ������������   
        to_dict['NCCWKDAT'] = TradeContext.NCCWKDAT
        AfaLoggerFunc.tradeDebug('acckj[NCCWKDAT] = ' + str(to_dict['NCCWKDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NCCWKDAT������")

    if TradeContext.existVariable('TRCNO'):        #������ˮ��
        to_dict['TRCNO'] = TradeContext.TRCNO
        AfaLoggerFunc.tradeDebug('acckj[TRCNO] = ' + str(to_dict['TRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.TRCNO������")

    if TradeContext.existVariable('SNDMBRCO'):      #���ͳ�Ա���к�
        to_dict['SNDMBRCO'] = TradeContext.SNDMBRCO
        AfaLoggerFunc.tradeDebug('acckj[SNDMBRCO] = ' + str(to_dict['SNDMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDMBRCO������")

    if TradeContext.existVariable('RCVMBRCO'):        #���ܳ�Ա���к�
        to_dict['RCVMBRCO'] = TradeContext.RCVMBRCO
        AfaLoggerFunc.tradeDebug('acckj[RCVMBRCO] = ' + str(to_dict['RCVMBRCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVMBRCO������")

    if TradeContext.existVariable('SNDBNKCO'):         #�����к�
        to_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        AfaLoggerFunc.tradeDebug('acckj[SNDBNKCO] = ' + str(to_dict['SNDBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKCO������")

    if TradeContext.existVariable('SNDBNKNM'):         #��������
        to_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        AfaLoggerFunc.tradeDebug('acckj[SNDBNKNM] = ' + str(to_dict['SNDBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.SNDBNKNM������")

    if TradeContext.existVariable('RCVBNKCO'):          #�����к�
        to_dict['RCVBNKCO'] = TradeContext.RCVBNKCO
        AfaLoggerFunc.tradeDebug('acckj[RCVBNKCO] = ' + str(to_dict['RCVBNKCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKCO������")

    if TradeContext.existVariable('RCVBNKNM'):          #��������
        to_dict['RCVBNKNM'] = TradeContext.RCVBNKNM
        AfaLoggerFunc.tradeDebug('acckj[RCVBNKNM] = ' + str(to_dict['RCVBNKNM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.RCVBNKNM������")

    if TradeContext.existVariable('ORTRCDAT'):          #ԭί������
        to_dict['ORTRCDAT'] = TradeContext.ORTRCDAT
        AfaLoggerFunc.tradeDebug('acckj[ORTRCDAT] = ' + str(to_dict['ORTRCDAT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCDAT������")
        
    if TradeContext.existVariable('ORTRCCO'):          #ԭ���״���
        to_dict['ORTRCCO'] = TradeContext.ORTRCCO
        AfaLoggerFunc.tradeDebug('acckj[ORTRCCO] = ' + str(to_dict['ORTRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCCO������")
        
    if TradeContext.existVariable('ORTRCNO'):          #ԭ������ˮ�� 
        to_dict['ORTRCNO'] = TradeContext.ORTRCNO
        AfaLoggerFunc.tradeDebug('acckj[ORTRCNO] = ' + str(to_dict['ORTRCNO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORTRCNO������")
        
    if TradeContext.existVariable('ORSNDSUBBNK'):          #ԭ�����г�Ա�к�
        to_dict['ORSNDSUBBNK'] = TradeContext.ORSNDSUBBNK
        AfaLoggerFunc.tradeDebug('acckj[ORSNDSUBBNK] = ' + str(to_dict['ORSNDSUBBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORSNDSUBBNK������")
        
    if TradeContext.existVariable('ORSNDBNK'):          #ԭ�������к� 
        to_dict['ORSNDBNK'] = TradeContext.ORSNDBNK
        AfaLoggerFunc.tradeDebug('acckj[ORSNDBNK] = ' + str(to_dict['ORSNDBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORSNDBNK������")
        
    if TradeContext.existVariable('ORRCVSUBBNK'):          #ԭ�����г�Ա�к�
        to_dict['ORRCVSUBBNK'] = TradeContext.ORRCVSUBBNK
        AfaLoggerFunc.tradeDebug('acckj[ORRCVSUBBNK] = ' + str(to_dict['ORRCVSUBBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORRCVSUBBNK������")
        
    if TradeContext.existVariable('ORRCVBNK'):          #ԭ�������к� 
        to_dict['ORRCVBNK'] = TradeContext.ORRCVBNK
        AfaLoggerFunc.tradeDebug('acckj[ORRCVBNK] = ' + str(to_dict['ORRCVBNK']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORRCVBNK������")
        
    if TradeContext.existVariable('ORPYRACC'):          #ԭ�������˺� 
        to_dict['ORPYRACC'] = TradeContext.ORPYRACC
        AfaLoggerFunc.tradeDebug('acckj[ORPYRACC] = ' + str(to_dict['ORPYRACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORPYRACC������")
        
    if TradeContext.existVariable('ORPYRNAM'):          #ԭ����������
        to_dict['ORPYRNAM'] = TradeContext.ORPYRNAM
        AfaLoggerFunc.tradeDebug('acckj[ORPYRNAM] = ' + str(to_dict['ORPYRNAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORPYRNAM������")
        
    if TradeContext.existVariable('ORPYEACC'):          #ԭ�տ����˺�
        to_dict['ORPYEACC'] = TradeContext.ORPYEACC
        AfaLoggerFunc.tradeDebug('acckj[ORPYEACC] = ' + str(to_dict['ORPYEACC']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ORPYEACC������")
        
    if TradeContext.existVariable('ORPYENAM'):          #ԭ�տ�������
        to_dict['ORPYENAM'] = TradeContext.ORPYENAM
        AfaLoggerFunc.tradeDebug('acckj[ORPYENAM] = ' + str(to_dict['ORPYENAM']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CERTNO������")
                
    if TradeContext.existVariable('CUR'):               #����
        to_dict['CUR'] = TradeContext.CUR
        AfaLoggerFunc.tradeDebug('acckj[CUR] = ' + str(to_dict['CUR']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CUR������")

    if TradeContext.existVariable('OCCAMT'):          #ԭ���׽��
        to_dict['OCCAMT'] = str((long)(((float)(TradeContext.OCCAMT)) * 100 + 0.1))
        AfaLoggerFunc.tradeDebug('acckj[OCCAMT] = ' + str(to_dict['OCCAMT']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.OCCAMT������") 
        
    if TradeContext.existVariable('CHRG'):          #������
        to_dict['CHRG'] = str((long)(((float)(TradeContext.CHRG)) * 100 + 0.1))
        AfaLoggerFunc.tradeDebug('acckj[CHRG] = ' + str(to_dict['CHRG']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CHRG������")     
    
    if TradeContext.existVariable('ERRCONBAL'):         #���ʿ��ƽ��
        to_dict['ERRCONBAL'] = TradeContext.ERRCONBAL
        AfaLoggerFunc.tradeDebug('acckj[ERRCONBAL] = ' + str(to_dict['ERRCONBAL']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.ERRCONBAL������")
    
    if TradeContext.existVariable('BALANCE'):         #�˻�ʵ�ʽ��
        to_dict['BALANCE'] = TradeContext.BALANCE
        AfaLoggerFunc.tradeDebug('acckj[BALANCE] = ' + str(to_dict['BALANCE']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.BALANCE������")
   
    if TradeContext.existVariable('UNCONRST'):         #��ش�����
        to_dict['UNCONRST'] = TradeContext.UNCONRST
        AfaLoggerFunc.tradeDebug('acckj[UNCONRST] = ' + str(to_dict['UNCONRST']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.UNCONRST������")


    if TradeContext.existVariable('STRINFO'):         #����
        to_dict['STRINFO'] = TradeContext.STRINFO
        AfaLoggerFunc.tradeDebug('acckj[STRINFO] = ' + str(to_dict['STRINFO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.STRINFO������")

    if TradeContext.existVariable('PRCCO'):       #���ķ�����
        to_dict['PRCCO'] = TradeContext.PRCCO
        AfaLoggerFunc.tradeDebug('acckj[PRCCO] = ' + str(to_dict['PRCCO']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.PRCCO������")
    
    if TradeContext.existVariable('CONSTS'):       #����״̬
        to_dict['CONSTS'] = TradeContext.CONSTS
        AfaLoggerFunc.tradeDebug('acckj[CONSTS] = ' + str(to_dict['CONSTS']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.CONSTS������")
    
    if TradeContext.existVariable('NOTE1'):
        to_dict['NOTE1'] = TradeContext.NOTE1
        AfaLoggerFunc.tradeDebug('acckj[NOTE1] = ' + str(to_dict['NOTE1']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE1������")

    if TradeContext.existVariable('NOTE2'):
        to_dict['NOTE2'] = TradeContext.NOTE2
        AfaLoggerFunc.tradeDebug('acckj[NOTE2] = ' + str(to_dict['NOTE2']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE2������")

    if TradeContext.existVariable('NOTE3'):
        to_dict['NOTE3'] = TradeContext.NOTE3
        AfaLoggerFunc.tradeDebug('acckj[NOTE3] = ' + str(to_dict['NOTE3']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE3������")

    if TradeContext.existVariable('NOTE4'):
        to_dict['NOTE4'] = TradeContext.NOTE4
        AfaLoggerFunc.tradeDebug('acckj[NOTE4] = ' + str(to_dict['NOTE4']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE4������")
        
    if TradeContext.existVariable('NOTE5'):
        to_dict['NOTE5'] = TradeContext.NOTE5
        AfaLoggerFunc.tradeDebug('acckj[NOTE5] = ' + str(to_dict['NOTE5']))
    else:
        AfaLoggerFunc.tradeDebug("TradeContext.NOTE5������")

    return True

