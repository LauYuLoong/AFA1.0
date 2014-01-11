# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).���ʿ��ƻ��ؽ����Ϣ��ѯ  ���潻��
#===============================================================================
#   ģ���ļ�:   TRCC001_8597.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����̩
#   �޸�ʱ��:   2011-08��22
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������(1.���ز���).���ʿ��ƻ��ؽ����ѯ[TRCC001_8597]����***' )
    
    #=====��Ҫ�Լ��====
    #=====�ж�����ӿ��Ƿ����====
    if( not TradeContext.existVariable( "TRCDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[ORTRCDAT]������')
        
    if( not TradeContext.existVariable( "OPTYPE" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[OPTYPE]������')
    #=====��ʼ��ѯ���ݿ�==== 
    
    if TradeContext.OPTYPE=='0': 
        sql =''   
        sql = sql + "select ORTRCDAT,ORTRCCO,ORSNDBNK,ORRCVBNK,ORPYRACC,ORPYRNAM,ORPYEACC,ORPYENAM,ERRCONBAL,CONSTS,STRINFO,TRCNO "     
        sql = sql + "from rcc_acckj where trcdat ='" + TradeContext.TRCDAT + "' and trcco='3000508' order by note1 desc "    
    if TradeContext.OPTYPE=='1':
        sql =''
        sql = sql + "select ORTRCDAT,TRCCO,ORSNDBNK,ORRCVBNK,ORPYRACC,ORPYRNAM,ORPYEACC,ORPYENAM,ERRCONBAL,UNCONRST,STRINFO,ORTRCNO "     
        sql = sql + "from rcc_acckj where trcdat ='" + TradeContext.TRCDAT + "' and trcco='3000509' order by note1  desc"                                                                                        
    AfaLoggerFunc.tradeDebug("��ѯ���ʿ��ƽ��sql��䣺"+ sql )
    
    records = AfaDBFunc.SelectSql( sql )  
    
    if ( records == None ):                                                                                              
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )                                                                  
        return AfaFlowControl.ExitThisFlow( '9000', '��ѯ����Э����Ϣ�쳣' )                                             
        
    if ( len(records) == 0 ):
        TradeContext.errorMsg    =  "û�н�����ʿ��ƽ�ص�����"
        TradeContext.errorCode   =  '9000'
        return AfaFlowControl.ExitThisFlow( '9000', 'û�н�����ʿ��ƽ�ص�����' )  
      
    else:
        TradeContext.count=str(len(records))  
        if TradeContext.count=='1':
            TradeContext.errorMsg    =  "���׳ɹ�"
            TradeContext.errorCode   =  '0000'    
            TradeContext.ORTRCDAT    =  records[0][0]
            TradeContext.ORTRCCO     =  records[0][1]
            TradeContext.ORSNDBNK    =  records[0][2]
            TradeContext.ORRCVBNK    =  records[0][3]
            TradeContext.ORPYRACC    =  records[0][4]
            TradeContext.ORPYRNAM    =  records[0][5]
            TradeContext.ORPYEACC    =  records[0][6]
            TradeContext.ORPYENAM    =  records[0][7] 
            TradeContext.ERRCONBAL   =  str(records[0][8]) 
            TradeContext.CONSTS      =  records[0][9] 
            TradeContext.STRINFO     =  records[0][10]
            TradeContext.TRCNO       =  records[0][11]
            AfaLoggerFunc.tradeDebug(TradeContext.STRINFO)
            
        else:
            ORTRCDAT    = []
            ORTRCCO     = []
            ORSNDBNK    = []
            ORRCVBNK    = []  
            ORPYRACC    = []  
            ORPYRNAM    = []  
            ORPYEACC    = []  
            ORPYENAM    = []  
            ERRCONBAL   = []  
            CONSTS      = []  
            STRINFO     = []
            TRCNO       = []
            i = 0
            for i in range(0, len(records)):
                ORTRCDAT.append(records[i][0])               #ԭί������
                ORTRCCO.append(records[i][1])                #ԭ���״���
                ORSNDBNK.append(records[i][2])               #ԭ�����к�
                ORRCVBNK.append(records[i][3])               #ԭ�����к�
                ORPYRACC.append(records[i][4])               #ԭ�����˺�
                ORPYRNAM.append(records[i][5])               #ԭ����������
                ORPYEACC.append(records[i][6])               #ԭ�տ��˺�
                ORPYENAM.append(records[i][7])               #ԭ�տ�������
                ERRCONBAL.append(str(records[i][8]))         #���ʿ��ƻ��ؽ��  
                CONSTS.append(records[i][9])                 #���ʿ��ƻ���״̬
                STRINFO.append(records[i][10])               #������
                TRCNO.append(records[i][11])                 #���ʿ�����ˮ��
             
            TradeContext.errorMsg    =  "���׳ɹ�"
            TradeContext.errorCode   =  '0000'
            TradeContext.ORTRCDAT    =   ORTRCDAT 
            TradeContext.ORTRCCO     =   ORTRCCO
            TradeContext.ORSNDBNK    =   ORSNDBNK  
            TradeContext.ORRCVBNK    =   ORRCVBNK   
            TradeContext.ORPYRACC    =   ORPYRACC   
            TradeContext.ORPYRNAM    =   ORPYRNAM   
            TradeContext.ORPYEACC    =   ORPYEACC   
            TradeContext.ORPYENAM    =   ORPYENAM   
            TradeContext.ERRCONBAL   =   ERRCONBAL   
            TradeContext.CONSTS      =   CONSTS  
            TradeContext.STRINFO     =   STRINFO
            TradeContext.TRCNO       =   TRCNO
                                                    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)���ʿ��ƽ�ؽ�����Ϣ������ѯ[TRCC001_8597]�˳�***')
    return True
