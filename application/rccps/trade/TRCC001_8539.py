# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ������.���������(1.���ز���).ͷ��Ԥ���Ǽǲ���ѯ 
#=================================================================
#   �����ļ�:   TRCC001_8539.py
#   �޸�ʱ��:   2008-06-07
#   ��    �ߣ�  �˹�ͨ
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_cshalm,rccpsDBFunc,rccpsState,os
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8539]����***' )

    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[ENDDAT]������')
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    #=====��֯sql���====
    wheresql = ""
    wheresql = wheresql+"BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql = wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    
    start_no=TradeContext.RECSTRNO      #��ʼ����
    sel_size=10                         #��ѯ����
    
    #=====��ѯ�ܼ�¼����====
    allcount=rccpsDBTrcc_cshalm.count(wheresql)
    
    if(allcount == -1):
        return AfaFlowControl.ExitThisFlow('S999', '��ѯ�ܼ�¼���쳣')
    
    #=====��ѯ���ݿ�====
    ordersql = " order by BJEDTE DESC"   
    records=rccpsDBTrcc_cshalm.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('S999', '��ѯͷ��Ԥ���Ǽǲ��쳣')
    if(len(records) <= 0):
    	  return AfaFlowControl.ExitThisFlow('S999', 'ͷ��Ԥ���Ǽǲ����޶�Ӧ��Ϣ')
    else:
        #=====�����ļ�====
        AfaLoggerFunc.tradeInfo( "�����ļ�")
        filename="rccps_"+TradeContext.BESBNO+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            pub_path = os.environ["AFAP_HOME"]
            pub_path = pub_path + "/tmp/"
            f=open(pub_path + filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��')

        filecontext=""
        #=====д�ļ�����====
        for i in range(0,len(records)):
            #=====�����ļ�����====
            filecontext=records[i]['BJEDTE']+"|"+records[i]['BSPSQN']+"|"\
                       +records[i]['NCCWKDAT']+"|"+records[i]['TRCDAT']+"|"\
                       +records[i]['TRCNO']+"|"+records[i]['CUR']+"|"\
                       +str(records[i]['POSITION'])+"|"+str(records[i]['POSALAMT'])+"|"
            AfaLoggerFunc.tradeInfo( filecontext)            
            f.write(filecontext+"\n")
        f.close()
        
        #=====����ӿڸ�ֵ====
        TradeContext.PBDAFILE=filename              #�ļ���
        TradeContext.RECCOUNT=str(len(records))     #��ѯ����
        TradeContext.RECALLCOUNT=str(allcount)  #�ܱ���
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
           
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8539]�˳�***' )
    return True
