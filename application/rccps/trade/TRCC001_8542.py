# -*- coding: gbk -*-
##################################################################
#   ũ����.����.���������(1.���ز���).���˲��Ǽǲ���ѯ
#=================================================================
#   �����ļ�:   TRCC001_8542.py
#   �޸�ʱ��:   2008-06-07
#   �޸���  ��  ������
#   �޸�ʱ�䣺  2008-07-02
##################################################################
#   �޸���  ��  ����
#   �޸�ʱ�䣺  2008-10-27
#   �޸�����:   ��� 30 ͨ��ͨ�� ����ز�ѯ
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_hddzcz,rccpsDBTrcc_trcbka,rccpsDBTrcc_bilbka
import rccpsDBTrcc_hpdzcz,rccpsDBTrcc_tddzcz,rccpsDBFunc,os
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)���˲��Ǽǲ���ѯ[TRC001_8542]����***' )
    
    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ֹ����[ENDDAT]������')
    if( not TradeContext.existVariable( "OPRTYPNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[OPRTYPNO]������')
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
    
    #=====��֯sql���====
    wheresql=""
    wheresql=wheresql+"BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    
    ordersql = " order by NCCWKDAT DESC"
    
    start_no=TradeContext.RECSTRNO          #��ʼ����
    sel_size=10                             #��ѯ����
    
    #=====20 ���====
    if TradeContext.OPRTYPNO == '20':
        #=====��ѯ�ܱ���====
        allcount=rccpsDBTrcc_hddzcz.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ�ܼ�¼���쳣')
        
        #=====��ѯ��ϸ====
        records=rccpsDBTrcc_hddzcz.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��Ҵ��˵Ǽǲ��쳣')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '��Ҵ��˵Ǽǲ����޶�Ӧ��Ϣ') 
    
    #=====21 ��Ʊ====        
    if TradeContext.OPRTYPNO == '21':
        #=====��ѯ�ܱ���====
        allcount=rccpsDBTrcc_hpdzcz.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ�ܼ�¼���쳣')
        
        #=====��ѯ��ϸ====
        records=rccpsDBTrcc_hpdzcz.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��Ʊ���˵Ǽǲ��쳣')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '��Ʊ���˵Ǽǲ����޶�Ӧ��Ϣ')
    
    #=====30 ͨ��ͨ��(���� 20081024 ���)====        
    if TradeContext.OPRTYPNO == '30':
        #=====��ѯ�ܱ���====
        allcount=rccpsDBTrcc_tddzcz.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ�ܼ�¼���쳣')
        
        #=====��ѯ��ϸ====
        records=rccpsDBTrcc_tddzcz.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��Ʊ���˵Ǽǲ��쳣')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '��Ʊ���˵Ǽǲ����޶�Ӧ��Ϣ')
    
    #=====�����ļ�====
    AfaLoggerFunc.tradeInfo( "�����ļ�")
    filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
    try:
        pub_path = os.environ["AFAP_HOME"]
        pub_path = pub_path + "/tmp/"
        f=open(pub_path+filename,"w")
    except IOError:
        return AfaLoggerFunc.ExitThisFlow('S099','���ļ�ʧ��')
        
    #=====д�ļ�����====
    try:
        filecontext=""
        for i in range(0,len(records)):
            #=====�����ļ�����====
            filecontext=records[i]['NCCWKDAT'] + "|" \
                       +records[i]['BJEDTE']   + "|" \
                       +records[i]['BSPSQN']   + "|" \
                       +records[i]['SNDBNKCO'] + "|" \
                       +records[i]['TRCDAT']   + "|" \
                       +records[i]['TRCNO']    + "|" \
                       +records[i]['EACTYP']   + "|" \
                       +records[i]['EACINF']   + "|" \
                       +records[i]['ISDEAL']   + "|" \
            
            #����̩20120614�����ϸ�ļ������ӽ����к�
            filecontext1=""
            #=====20 ���====
            if(TradeContext.OPRTYPNO == '20'): 
                trcbka_sql = {}
                trcbka_sql = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
                result=rccpsDBTrcc_trcbka.selectu(trcbka_sql)
                if(result == None):
                    return AfaFlowControl.ExitThisFlow('S999', '��ѯ���ҵ��Ǽǲ��쳣')
                
                if(len(result) <= 0):
                    filecontext1=" " + "|" 
                else:
                    filecontext1= result['RCVBNKCO']+ "|" 
            #=====21 ��Ʊ====        
            elif TradeContext.OPRTYPNO == '21': 
                bilbka_sql = {}
                bilbka_sql = {'BJEDTE':records[i]['BJEDTE'],'BSPSQN':records[i]['BSPSQN']}
                result=rccpsDBTrcc_bilbka.selectu(bilbka_sql)
                AfaLoggerFunc.tradeInfo(result)
                if(result == None):
                    return AfaFlowControl.ExitThisFlow('S999', '��ѯ��Ʊҵ��Ǽǲ��쳣')
                
                if(len(result) <= 0):
                    filecontext1=" " + "|" 
                else:
                    filecontext1= result['RCVBNKCO']+ "|"              
            
            else:
                filecontext1= records[i]['RCVBNKCO'] + "|" 
            filecontext=filecontext+filecontext1 
            #end  
            f.write(filecontext+"\n")
    except Exception,e:     
        f.close()
        return AfaFlowControl.ExitThisFlow('S099','д�ļ�ʧ��')
    
    #=====����ӿڸ�ֵ====
    TradeContext.PBDAFILE=filename              #�ļ���
    TradeContext.RECCOUNT=str(len(records))     #��ѯ����
    TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)���˲��Ǽǲ���ѯ[TRC001_8542]�˳�***' )
    return True
