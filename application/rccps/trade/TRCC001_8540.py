# -*- coding: gbk -*-
##################################################################
#   ũ����.����.���������(1.���ز���).�����˻����֪ͨ��ѯ����
#=================================================================
#   �����ļ�:   TRCC001_8540.py
#   �޸�ʱ��:   2008-06-10
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_rekbal,rccpsDBFunc,os
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8540]����***' )

    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "NCCWKDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[NCCWKDAT]������')
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    #=====��֯sql���====
    wheresql=""
    wheresql=wheresql+"NCCWKDAT='"+TradeContext.NCCWKDAT+"'"
    
    start_no=TradeContext.RECSTRNO      #��ʼ����
    sel_size=10                         #��ѯ����
    
    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_rekbal.count(wheresql)     #�õ��ܼ�¼����
    if(allcount == -1):
        return AfaFlowControl.ExitThisFlow('S999', '��ѯ�ܼ�¼���쳣')
    
    #=====��ѯ��ϸ��¼====
    ordersql=" order by BJEDTE DESC,BSPSQN DESC"
    records=rccpsDBTrcc_rekbal.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('S999', '��ѯ�������֪ͨ�Ǽǲ��쳣')
    if(len(records) <= 0):
    	  return AfaFlowControl.ExitThisFlow('S999', '�������֪ͨ�Ǽǲ����޶�Ӧ��Ϣ')
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
        #=====д�ļ�����====
        for i in range(0,len(records)):
            #=====�����ļ�����====
            filecontext=records[i]['BJEDTE']+"|"+records[i]['BSPSQN']+"|"\
                        +records[i]['TRCCO']+"|"+records[i]['NCCWKDAT']+"|"\
                        +records[i]['TRCDAT']+"|"+records[i]['TRCNO']+"|"\
                        +records[i]['CUR']+"|"+records[i]['LBDCFLG']+"|"\
                        +str(records[i]['LSTDTBAL'])+"|"+records[i]['NTTDCFLG']+"|"\
                        +str(records[i]['NTTBAL'])+"|"+records[i]['BALDCFLG']+"|"\
                        +str(records[i]['TODAYBAL'])+"|"+str(records[i]['AVLBAL'])+"|"\
                        +str(records[i]['NTODAYBAL'])+"|"+records[i]['CHKRST']+"|"
            f.write(filecontext+"\n")
        f.close()

        #=====����ӿڸ�ֵ====
        TradeContext.PBDAFILE=filename              #�ļ���
        TradeContext.RECCOUNT=str(len(records))     #��ѯ����
        TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8540]�˳�***' )
    return True
