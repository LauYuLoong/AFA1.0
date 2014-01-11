# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.�������뼰����ֹ�������ѯ
#=================================================================
#   �����ļ�:   TRCC001_8527.py
#   �޸�ʱ��:   2008-06-07
#   ��    �ߣ�  �˹�ͨ
##################################################################
import rccpsDBTrcc_trccan,rccpsDBTrcc_existp,rccpsDBTrcc_trcbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc
from types import *
import os

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8527]����***' )
    
    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
    
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[ENDDAT]������')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    start_no=TradeContext.RECSTRNO
    sel_size=10                             #��ѯ����
        
    #=====��֯��ѯ��sql���====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ���")
    wheresql=""
    wheresql=wheresql+"BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    wheresql=wheresql+" AND BESBNO ='"+TradeContext.BESBNO+"'"
    
    #=====�жϽ��״����Ƿ�Ϊ��====
    if(TradeContext.TRCCO!=""):
        wheresql=wheresql+" AND TRCCO='"+TradeContext.TRCCO+"'"
    
    #=====�жϱ�������Ƿ�Ϊ��====
    if(TradeContext.BSPSQN!=""):
        wheresql=wheresql+" AND BSPSQN='"+TradeContext.BSPSQN+"'"
    
    AfaLoggerFunc.tradeDebug( "sql=" + wheresql )
    
    #=====����֧��====
    if(TradeContext.TRCCO=="9900519"):
        #=====�õ�existp����ֹ���Ǽǲ��ܼ�¼����====
        allcount=rccpsDBTrcc_existp.count(wheresql)
    #=====����====    
    else:
        #=====�õ�trccan��������Ǽǲ��ܼ�¼����====
        allcount=rccpsDBTrcc_trccan.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ�ܼ�¼��ʧ��')
    
    #=====��������˳��====
    ordersql=" order by BJEDTE DESC,BSPSQN DESC"    

    #=====����֧��====
    if(TradeContext.TRCCO=="9900519"):
        #=====��ѯ����ֹ���Ǽǲ�====
        records=rccpsDBTrcc_existp.selectm(start_no,sel_size,wheresql,ordersql)
    #=====����====
    else:
        #=====��ѯ��������Ǽǲ�====
        records=rccpsDBTrcc_trccan.selectm(start_no,sel_size,wheresql,ordersql)
    
    if records==None:
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )   
    if( len(records)<=0 ):
        return AfaFlowControl.ExitThisFlow('A099','δ���ҵ�����' )    
    else:
        #=====�����ļ�====
        AfaLoggerFunc.tradeInfo(">>>��ʼ�����ļ�")
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
        fpath=os.environ["AFAP_HOME"]+"/tmp/"
        
        f=open(fpath+filename,"w")
        
        if(f==None):
            return AfaFlowControl.ExitThisFlow('A099','���ļ�ʧ��' )
            
        filecontext=""
        #=====д�ļ�����====
        if(TradeContext.TRCCO=="9900501"):  #��������
            AfaLoggerFunc.tradeInfo(">>>��ʼ�������봦��")
            for i in range(0,len(records)):
                #=====�����ļ�����====
                filecontext=records[i]['BJEDTE']       + "|" \
                           +records[i]['BSPSQN']       + "|" \
                           +records[i]['BESBNO']       + "|" \
                           +records[i]['BETELR']       + "|" \
                           +records[i]['BEAUUS']       + "|" \
                           +records[i]['NCCWKDAT']     + "|" \
                           +records[i]['BOJEDT']       + "|" \
                           +records[i]['BOSPSQ']       + "|" \
                           +records[i]['TRCCO']        + "|" \
                           +records[i]['TRCDAT']       + "|" \
                           +records[i]['TRCNO']        + "|" \
                           +records[i]['SNDBNKCO']     + "|" \
                           +records[i]['SNDBNKNM']     + "|" \
                           +records[i]['RCVBNKCO']     + "|" \
                           +records[i]['RCVBNKNM']     + "|" \
                           +records[i]['ORTRCCO']      + "|" \
                           +records[i]['CUR']          + "|" \
                           +str(records[i]['OCCAMT'])  + "|" \
                           +records[i]['CONT']         + "|" \
                           +records[i]['CLRESPN']      + "|"
                AfaLoggerFunc.tradeDebug(">>>�����ļ���Ŀ[" + str(i) + "]")           
                f.write(filecontext+"\n")                
        elif(TradeContext.TRCCO=='9900502'):   #��������Ӧ��
            AfaLoggerFunc.tradeInfo(">>>���볷������Ӧ����")
            for i in range(0,len(records)):
                #=====�����ļ�����====
                filecontext=records[i]['BJEDTE']       + "|" \
                           +records[i]['BSPSQN']       + "|" \
                           +records[i]['BESBNO']       + "|" \
                           +records[i]['BETELR']       + "|" \
                           +records[i]['BEAUUS']       + "|" \
                           +records[i]['NCCWKDAT']     + "|" \
                           +records[i]['BOJEDT']       + "|" \
                           +records[i]['BOSPSQ']       + "|" \
                           +records[i]['TRCCO']        + "|" \
                           +records[i]['TRCDAT']       + "|" \
                           +records[i]['TRCNO']        + "|" \
                           +records[i]['SNDBNKCO']     + "|" \
                           +records[i]['SNDBNKNM']     + "|" \
                           +records[i]['RCVBNKCO']     + "|" \
                           +records[i]['RCVBNKNM']     + "|" \
                           +records[i]['ORTRCCO']       + "|" \
                           +records[i]['CUR']          + "|" \
                           +str(records[i]['OCCAMT'])  + "|" \
                           +records[i]['CONT']         + "|" \
                           +records[i]['CLRESPN']      + "|"
                AfaLoggerFunc.tradeDebug(">>>�����ļ���Ŀ[" + str(i) + "]")           
                f.write(filecontext+"\n")        
        elif(TradeContext.TRCCO=='9900519'):  #����֧��
            AfaLoggerFunc.tradeInfo(">>>�������֧������")
            errors=0
            for i in range(0,len(records)):
                #=====�����ļ�����====
                filecontext=records[i]['BJEDTE']       + "|" \
                           +records[i]['BSPSQN']       + "|" \
                           +records[i]['BESBNO']       + "|" \
                           +records[i]['BETELR']       + "|" \
                           +records[i]['BEAUUS']       + "|" \
                           +records[i]['NCCWKDAT']     + "|" \
                           +records[i]['BOJEDT']       + "|" \
                           +records[i]['BOSPSQ']       + "|" \
                           +records[i]['TRCCO']        + "|" \
                           +records[i]['TRCDAT']       + "|" \
                           +records[i]['TRCNO']        + "|" \
                           +records[i]['SNDBNKCO']     + "|" \
                           +records[i]['SNDBNKNM']     + "|" \
                           +records[i]['RCVBNKCO']     + "|" \
                           +records[i]['RCVBNKNM']     + "|" \
                           +records[i]['ORTRCCO']      + "|" \
                           +records[i]['CUR']          + "|" \
                           +str(records[i]['OCCAMT'])  + "|" \
                           +records[i]['CONT']         + "|" \
                           +""                         + "|"
                AfaLoggerFunc.tradeDebug("�����ļ���Ŀ[" + str(i) + "]")           
                f.write(filecontext+"\n")
                errors=errors+1
        else:
            return AfaFlowControl.ExitThisFlow('M999','ҵ�����ͷǷ�')
                
        #====�ر��ļ�====
        f.close()
        AfaLoggerFunc.tradeInfo( ">>>�����ļ����� ")
        
        #=====����ӿڸ�ֵ====   
        TradeContext.PBDAFILE=filename              #�ļ��� 
        TradeContext.RECSTRNO=start_no              #��ʼ����
#        if(len(records)>10):
#            TradeContext.RECCOUNT=str(sel_size)     #��ѯ����
#        else:
#            TradeContext.RECCOUNT=str(len(records)) #��ѯ����
        TradeContext.RECCOUNT=str(len(records)) #��ѯ����
        TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
        
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8527]�˳�***' )
    return True