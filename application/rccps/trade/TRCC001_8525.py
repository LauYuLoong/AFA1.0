# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).��Ʊҵ����ϸ��ѯ
#===============================================================================
#   �����ļ�:   TRCC001_8525.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-07-09
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_bilbka


#=====================���Ի�����(���ز���)======================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊҵ����ϸ��ѯ[TRC001_8525]����***' )
    
    #=================��Ҫ�Լ��================================================
    AfaLoggerFunc.tradeDebug(">>>��ʼ��Ҫ�Լ��")
    
    if not TradeContext.existVariable('STRDAT'):
        return AfaFlowControl.ExitThisFlow('S999','��ʼ����[STRDAT]������' )
    elif len(TradeContext.STRDAT) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','��ʼ����[STRDAT]����Ϊ��' )
        
    if not TradeContext.existVariable('ENDDAT'):
        return AfaFlowControl.ExitThisFlow('S999','��ֹ����[ENDDAT]������' )
    elif len(TradeContext.ENDDAT) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','��ֹ����[ENDDAT]����Ϊ��' )
        
    AfaLoggerFunc.tradeDebug(">>>������Ҫ�Լ��")
    
    #=================��֯��ѯsql���===========================================
    AfaLoggerFunc.tradeDebug(">>>��ʼ��֯��ѯsql���")
    
    bilbka_where_sql = ""
    bilbka_where_sql = bilbka_where_sql + "BESBNO='" + TradeContext.BESBNO + "' "
    bilbka_where_sql = bilbka_where_sql + "and BJEDTE >= '" + TradeContext.STRDAT + "' and BJEDTE <= '" + TradeContext.ENDDAT + "'"
    
    #=====�ж�������־�Ƿ����====
    if TradeContext.existVariable('BRSFLG'):
        if len(TradeContext.BRSFLG) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BRSFLG = '" + TradeContext.BRSFLG + "'"
    
    #=====�жϽ��״����Ƿ����====
    if TradeContext.existVariable('TRCCO'):
        if len(TradeContext.TRCCO) > 0:
            bilbka_where_sql = bilbka_where_sql + " and TRCCO = '" + TradeContext.TRCCO + "'"
    
    #=====�жϱ�������Ƿ����====        
    if TradeContext.existVariable('BSPSQN'):
        if len(TradeContext.BSPSQN) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BSPSQN = '" + TradeContext.BSPSQN + "'"
    
    #=====�жϻ�Ʊ�������б�ʶ�Ƿ����====
    if TradeContext.existVariable('BILRS'):
        if len(TradeContext.BILRS) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BILRS = '" + TradeContext.BILRS + "'"
    
    #=====�жϻ�Ʊ�汾���Ƿ����====        
    if TradeContext.existVariable('BILVER'):
        if len(TradeContext.BILVER) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BILVER = '" + TradeContext.BILVER + "'"
    
    #=====�жϻ�Ʊ�����Ƿ����====
    if TradeContext.existVariable('BILNO'):
        if len(TradeContext.BILNO) > 0:
            bilbka_where_sql = bilbka_where_sql + " and BILNO = '" + TradeContext.BILNO + "'"
    
    #=====�жϽ����к��Ƿ����====        
    if TradeContext.existVariable('RCVBNKCO'):
        if len(TradeContext.RCVBNKCO) > 0:
            bilbka_where_sql = bilbka_where_sql + " and RCVBNKCO = '" + TradeContext.RCVBNKCO + "'"
            
    AfaLoggerFunc.tradeDebug(">>>������֯��ѯsql���")
            
    #================��ѯ�ܱ���==================================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ܱ���")
    
    all_count = rccpsDBTrcc_bilbka.count(bilbka_where_sql)
    
    AfaLoggerFunc.tradeInfo(">>>������֯��ѯ�ܱ���")
    
    if all_count < 0:
        return AfaFlowControl.ExitThisFlow('S999','��ѯ�ܱ����쳣')        
    if all_count == 0:
        return AfaFlowControl.ExitThisFlow('S999','�޲�ѯ��Ӧ��¼')        
    if all_count > 0:
        TradeContext.RECALLCOUNT = str(all_count)                #�ܱ���
        #============��ѯ��ϸ��¼================================================
        AfaLoggerFunc.tradeDebug(">>>��ʼ��ѯ��ϸ��¼")
        
        bilbka_order_sql = " order by BJEDTE DESC,BSPSQN DESC "
        
        bilbka_dict = rccpsDBTrcc_bilbka.selectm(TradeContext.RECSTRNO,10,bilbka_where_sql,bilbka_order_sql)
        
        AfaLoggerFunc.tradeDebug(">>>������ѯ��ϸ��¼")
        
        if bilbka_dict == None:
            return AfaFlowControl.ExitThisFlow('S999','��ѯ��ϸ��¼�쳣')        
        if len(bilbka_dict) <= 0:
            return AfaFlowControl.ExitThisFlow('S999','��ѯ��ϸ�޼�¼')
        else:
            TradeContext.RECCOUNT = str(len(bilbka_dict))         #���β�ѯ����
            #========�������form�ļ�============================================
            AfaLoggerFunc.tradeInfo(">>>��ʼ�����ļ�")
            
            file_name = "rccps_" + TradeContext.BETELR + "_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode
            
            try:
            	fpath=os.environ["AFAP_HOME"]+"/tmp/"
            	fp=open(fpath+file_name,"w") 
            except IOError:
                return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��')
            
            for i in xrange(len(bilbka_dict)):
                #====��ѯ�˽���״̬��Ϣ==========================================
                stat_dict = {}
                ret = rccpsState.getTransStateCur(bilbka_dict[i]['BJEDTE'],bilbka_dict[i]['BSPSQN'],stat_dict)
                
                if not ret:
                    AfaLoggerFunc.tradeDebug("��ѯ����״̬��Ϣ�쳣")
                    return AfaFlowControl.ExitThisFlow('S999','�����ļ��쳣')
                
                file_line = bilbka_dict[i]['BJEDTE']   + "|" \
                          + bilbka_dict[i]['BSPSQN']   + "|" \
                          + bilbka_dict[i]['BRSFLG']   + "|" \
                          + bilbka_dict[i]['OPRNO']    + "|" \
                          + bilbka_dict[i]['BESBNO']   + "|" \
                          + bilbka_dict[i]['BEACSB']   + "|" \
                          + bilbka_dict[i]['BETELR']   + "|" \
                          + bilbka_dict[i]['BEAUUS']   + "|" \
                          + bilbka_dict[i]['BBSSRC']   + "|" \
                          + bilbka_dict[i]['DASQ']     + "|" \
                          + bilbka_dict[i]['DCFLG']    + "|" \
                          + bilbka_dict[i]['NCCWKDAT'] + "|" \
                          + bilbka_dict[i]['TRCCO']    + "|" \
                          + bilbka_dict[i]['TRCDAT']   + "|" \
                          + bilbka_dict[i]['TRCNO']    + "|" \
                          + bilbka_dict[i]['SNDBNKCO'] + "|" \
                          + bilbka_dict[i]['SNDBNKNM'] + "|" \
                          + bilbka_dict[i]['RCVBNKCO'] + "|" \
                          + bilbka_dict[i]['RCVBNKNM'] + "|" \
                          + bilbka_dict[i]['BILVER']   + "|" \
                          + bilbka_dict[i]['BILNO']    + "|" \
                          + bilbka_dict[i]['BILRS']    + "|" \
                          + bilbka_dict[i]['HPSTAT']   + "|" \
                          + stat_dict['BCSTAT']        + "|" \
                          + stat_dict['BDWFLG']        + "|" 
                fp.write(file_line + "\n")
                
            fp.close()
            AfaLoggerFunc.tradeInfo(">>>���������ļ�")
        
        TradeContext.PBDAFILE = file_name       #�ļ���
        TradeContext.errorCode = "0000"
        TradeContext.errorMsg  = "�ɹ�"
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ʊҵ����ϸ��ѯ[TRC001_8525]�˳�***' )
    return True
