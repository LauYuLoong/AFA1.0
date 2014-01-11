# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡ.ͨ��ͨ�Ҵ���֪ͨ��ѯ
#=================================================================
#   �����ļ�:   TRCC001_8589.py
#   �޸�ʱ��:   2008-12-15
#   ���ߣ�      ����
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_notbka 

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ͨ��ͨ���������ʲ�ѯ[TRCC001_8589]����***' )
    
    #=====��Ҫ�Լ��====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")
    
    if( not TradeContext.existVariable( "TRCCO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '���״���[TRCCO]������')
        
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    AfaLoggerFunc.tradeInfo(">>>��Ҫ�Լ�����")
    
    #=====��֯sql���====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯsql���")
    
    wheresql = ""
    wheresql = wheresql + "NOTDAT='" + TradeContext.NOTDAT + "' " 
    wheresql = wheresql + " AND BESBNO='" + TradeContext.BESBNO + "' "
    
    ordersql = " order by NOTDAT DESC"
    
    start_no = TradeContext.RECSTRNO        #��ʼ����
    sel_size = 10                           #��ѯ����
    
    AfaLoggerFunc.tradeDebug(">>>������֯��ѯsql���")   
    
    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_notbka.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ�ܱ���ʧ��' )
        
    #=====��ѯ���ݿ�====
    
    AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
    records = rccpsDBTrcc_notbka.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )    
    if len(records) <= 0:
        return AfaFlowControl.ExitThisFlow('A099','δ���ҵ�����' )
    else:
        #=====�����ļ�====
        try:
            filename = "rccps_" + TradeContext.BETELR+"_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode
            fpath = os.environ["AFAP_HOME"] + "/tmp/"
            f = open(fpath + filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S099','���ļ�ʧ��')
    
    #=====д�ļ�����====
        try:
            filecontext=""
            AfaLoggerFunc.tradeInfo ("�����ļ����� ")
            for i in range(0,len(records)):
                #AfaLoggerFunc.tradeDebug("д���"+str(i)+"�ʼ�¼��ʼ")
                filecontext= records[i]['NOTDAT']        + "|" \
                           + records[i]['BESBNO']        + "|" \
                           + records[i]['STRINFO']       + "|" 
                           
                f.write(filecontext+"\n") 
                #AfaLoggerFunc.tradeDebug("д���"+str(i)+"�ʼ�¼����")     
        except Exception,e:                                        
            f.close()                                              
            return AfaFlowControl.ExitThisFlow('S099','д�ļ�ʧ��')
            AfaLoggerFunc.tradeInfo ("�����ļ����ݽ��� ")
    
    #=====����ӿڸ�ֵ====
    TradeContext.RECSTRNO=start_no              #��ʼ����
    TradeContext.RECCOUNT=str(len(records))     #���β�ѯ����
    TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
    TradeContext.PBDAFILE=filename              #�ļ���
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ͨ��ͨ�Ҵ���֪ͨ��ѯ[TRCC001_8589]�˳�***' )
    return True 	
           
