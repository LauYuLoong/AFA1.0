# -*- coding: gbk -*-
##################################################################
#   ũ����.���ڼ���
#=================================================================
#   �����ļ�:   TRCC001_8569.py
#   �޸�ʱ��:   2008-06-05
##################################################################

import rccpsDBFunc,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc
from types import *
from rccpsConst import *
import rccpsState,rccpsFtpFunc,os,rccpsCronFunc,rccpsHostFunc

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8569]����***' )

    #=====�ж�����ӿ�ֵ�Ƿ����====
    if(not TradeContext.existVariable("STRDAT")):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
    if(not TradeContext.existVariable("ENDDAT")):
        return AfaFlowControl.ExitThisFlow('A099', '��������[ENDDAT]������')
        
    if TradeContext.ENDDAT > AfaUtilTools.GetHostDate():
        return AfaFlowControl.ExitThisFlow('S999', '�������ڱ����ڵ�ǰ����֮ǰ')
        
    #=====��ȡ��������==================
    TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )

    #===========�������ڼ����ļ�====================
    #===========�ļ���ʽ===========================
    #��������|��ʼ����|��ֹ����|���׻�����|������־|�շ��ܽ��|��������|������ܽ��|��Ʊ�����|��Ʊ���ܽ��|
    #ͨ��ͨ�������|ͨ��ͨ�����ܽ��|��Ϣ�����|��Ϣ���ܽ��|��¼״̬|�����ֶ� 1|�����ֶ� 2|�����ֶ� 3|�����ֶ� 4
    
    file_path = os.environ['AFAP_HOME'] + "/data/rccps/host/"
    file_name = 'rccsxfile' + TradeContext.BJEDTE
    TradeContext.OCCAMT = 0     #�ܽ��
    TradeContext.CONT   = 0     #�ܱ���
    rb = open(file_path + file_name,'w')
    
    sqlStr = "select distinct NCCWKDAT,BESBNO from rcc_trcsta "
    sqlStr = sqlStr + "where NCCWKDAT >= '" + TradeContext.STRDAT + "' and NCCWKDAT <= '" + TradeContext.ENDDAT + "'"
    sqlStr = sqlStr + "and BRSFLG = '" + PL_BRSFLG_SND + "' order by NCCWKDAT,BESBNO"
    AfaLoggerFunc.tradeInfo(sqlStr)
    records = AfaDBFunc.SelectSql(sqlStr)
    if (records == None):
        return AfaFlowControl.ExitThisFlow('A099', '��ѯ[RCC_NCCWKDAT]���쳣')
    else:

        for i in range(len(records)):
            sqlStr_1 = "select t.TRCCO,t.ts,t.ts*double(t1.BPADAT) from("
            sqlStr_1 = sqlStr_1 + "select TRCCO,sum(TCNT) ts from rcc_trcsta"
            sqlStr_1 = sqlStr_1 + " where NCCWKDAT = '" + records[i][0] + "' and BESBNO = '" + records[i][1] + "'"
            sqlStr_1 = sqlStr_1 + " group by TRCCO" 
            sqlStr_1 = sqlStr_1 + ") t,RCC_PAMTBL t1 where t.TRCCO = t1.BPARAD and double(t1.BPADAT) > 0"

            AfaLoggerFunc.tradeDebug(sqlStr_1)
            res = AfaDBFunc.SelectSql(sqlStr_1)
            if (res == None):
                return AfaFlowControl.ExitThisFlow('A099', '��ѯ[RCC_NCCWKDAT]���쳣')
                
            amount20 = 0
            sum20 = 0
            amount21 = 0
            sum21 = 0
            amount30 = 0
            sum30 = 0
            amount99 = 0
            sum99 = 0 
            AfaLoggerFunc.tradeInfo(res)
            for j in range(len(res)):
                if(len(res[j][0]) < 7):
                    return AfaFlowControl.ExitThisFlow('A099', '[RCC_PAMTBL]���״���[' + res[j][0] + ']�쳣')
                elif((res[j][0])[:2] == '20'):
                    amount20 = amount20 + float(res[j][2])
                    sum20 = sum20 + int(res[j][1])
                elif((res[j][0])[:2] == '21'):
                    amount21 = amount21 + float(res[j][2])
                    sum21 = sum21 + int(res[j][1])
                elif((res[j][0])[:2] == '30'):
                    amount30 = amount30 + float(res[j][2])
                    sum30 = sum30 + int(res[j][1])
                elif((res[j][0])[:2] == '99'):
                    amount99 = amount99 + float(res[j][2])
                    sum99 = sum99 + int(res[j][1])
               
            Amount = amount20 + amount21 + amount30 + amount99
            #=====����ܽ������㣬������´�ѭ��=================
            if(Amount <= 0):
                continue
                
            TradeContext.OCCAMT = TradeContext.OCCAMT + Amount
            TradeContext.CONT   = TradeContext.CONT + 1
            lines = ""
            lines = lines + str(records[i][0]).strip().ljust(8, ' ') + "|"
            lines = lines + str(TradeContext.STRDAT).strip().ljust(8, ' ') + "|"
            lines = lines + str(TradeContext.ENDDAT).strip().ljust(8, ' ') + "|"
            lines = lines + str(records[i][1]).strip().ljust(10,' ') + "|"
            lines = lines + str(Amount).strip().ljust(15,' ') + "|"
            lines = lines + str(sum20).strip().ljust(8,' ') + "|"
            lines = lines + str(amount20).strip().ljust(15,' ') + "|"
            lines = lines + str(sum21).strip().ljust(8,' ') + "|"
            lines = lines + str(amount21).strip().ljust(15,' ') + "|"
            lines = lines + str(sum30).strip().ljust(8,' ') + "|"
            lines = lines + str(amount30).strip().ljust(15,' ') + "|"
            lines = lines + str(sum99).strip().ljust(8,' ') + "|"
            lines = lines + str(amount99).strip().ljust(15,' ') + "|"
            lines = lines + str('0').ljust(1,' ') + "|"
            lines = lines + str('').ljust(62,' ') + "|"
            lines = lines + str('').ljust(62,' ') + "|"
            lines = lines + str('').ljust(62,' ') + "|"
            lines = lines + str('').ljust(62,' ') + "|"
            
            rb.write(lines + "\n")
    
    
    rb.close()

    #===========�ļ�ת��============================
    AfaLoggerFunc.tradeInfo('>>>�ļ�ת��')
    sFileName = file_name
    dFileName = 'RCCSXFILE.SX'+ TradeContext.BJEDTE
    fldName = 'nxsxa.fld'
    if( not rccpsCronFunc.FormatFile('1', fldName, sFileName, dFileName)):
        return AfaFlowControl.ExitThisFlow('A099', 'ת�����������ļ������쳣')
    
    
    #===========�ϴ������ļ�========================
    AfaLoggerFunc.tradeInfo('>>>�ϴ������ļ�')
    if( not rccpsFtpFunc.putHost(dFileName)):
        return AfaFlowControl.ExitThisFlow('A099', '�ϴ������ļ��쳣')

    AfaLoggerFunc.tradeInfo('>>>���������ӿ�')
    #===========������������===========================
    TradeContext.HostCode = '8823'                       #������
    TradeContext.OCCAMT = str(TradeContext.OCCAMT)
    AfaLoggerFunc.tradeInfo('>>>���ս��'+ str(TradeContext.OCCAMT))
    TradeContext.fileName = 'SX' + TradeContext.BJEDTE   #�ļ���
    
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("����������[" + TradeContext.errorCode + "],����������Ϣ[" + TradeContext.errorMsg +"]")
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
            
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '�ɹ�'
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8569]�˳�***' )

    return True