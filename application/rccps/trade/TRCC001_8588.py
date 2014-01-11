# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡ.ͨ��ͨ���������ʲ�ѯ
#=================================================================
#   �����ļ�:   TRCC001_8588.py
#   �޸�ʱ��:   2008-12-15
#   ���ߣ�      ����
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_tdzjcz 

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ͨ��ͨ���������ʲ�ѯ[TRCC001_8588]����***' )
    
    #=====��Ҫ�Լ��====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    AfaLoggerFunc.tradeInfo(">>>��Ҫ�Լ�����")
    
    #=====��֯sql���====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯsql���")
    
    wheresql = ""
    wheresql = wheresql + "NCCWKDAT='" + TradeContext.NCCWKDAT + "' " 
    
    ordersql = " order by NCCWKDAT DESC "
    
    start_no = TradeContext.RECSTRNO        #��ʼ����
    sel_size = 10                           #��ѯ����
    
    ##=====�жϱ�������Ƿ�Ϊ��====
    #if(TradeContext.BSPSQN != ""):
    #    wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "' "
    
    #=====�жϴ����ʶ�Ƿ�Ϊ��====
    if(TradeContext.ISDEAL == "0"):
        wheresql = wheresql + "AND ISDEAL='0'" 
    elif(TradeContext.ISDEAL == "1"):
        wheresql = wheresql + "AND ISDEAL='1'" 
    else:
        pass
        
    AfaLoggerFunc.tradeDebug(">>>������֯��ѯsql���")   
    
    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_tdzjcz.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ�ܱ���ʧ��' )
        
    #=====��ѯ���ݿ�====
    
    AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
    records = rccpsDBTrcc_tdzjcz.selectm(start_no,sel_size,wheresql,ordersql)
    
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
                filecontext= records[i]['NCCWKDAT']        + "|" \
                           + records[i]['SCFEDT']          + "|" \
                           + records[i]['SCRBSQ']          + "|" \
                           + records[i]['RCFEDT']          + "|" \
                           + records[i]['RCRBSQ']          + "|" \
                           + str(records[i]['SCTRAM'])     + "|" \
                           + str(records[i]['RCTRAM'])     + "|" \
                           + records[i]['SCTRDT']          + "|" \
                           + records[i]['SCTLSQ']          + "|" \
                           + records[i]['ERRTYP']          + "|" \
                           + records[i]['ERRINF']          + "|" \
                           + records[i]['ISDEAL']          + "|" 
                           
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
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).ͨ��ͨ���������ʲ�ѯ[TRCC001_8588]�˳�***' )
    return True 	
           