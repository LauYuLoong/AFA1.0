# -*- coding: gbk -*-
##################################################################
#   ũ����.����.���������(1.���ز���).���������ļ�֪ͨ��ѯ
#=================================================================
#   �����ļ�:   TRCC001_8550.py
#   �޸�ʱ��:   2008-06-07
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_pbdata,rccpsDBFunc,AfaUtilTools,os,rccpsFtpFunc
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8550]����***' )

    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[ENDDAT]������')
    if( not TradeContext.existVariable( "PBDATYP" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[PBDATYP]������')
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    #=====��֯sql���====
    wheresql=""
    wheresql=wheresql+"NCCWKDAT>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND NCCWKDAT<='"+TradeContext.ENDDAT+"'"
    wheresql=wheresql+" AND PbDaTyp='"+TradeContext.PBDATYP+"'"
    
    start_no=TradeContext.RECSTRNO      #��ʼ����
    sel_size=10                         #��ѯ����
    
    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_pbdata.count(wheresql)
    if(allcount == -1):
        return AfaFlowControl.ExitThisFlow('S999', '��ѯ�ܼ�¼���쳣')
    
    #=====��ѯ����====
    records=rccpsDBTrcc_pbdata.selectm(start_no,sel_size,wheresql,"")
    if(records == None):
        return AfaFlowControl.ExitThisFlow('S999', '��ѯ�������ݵǼǲ��쳣')
    if(len(records) <= 0):
        return AfaFlowControl.ExitThisFlow('S999', '�������ݵǼǲ����޶�Ӧ��Ϣ')
    else:
        AfaLoggerFunc.tradeInfo( "�����ļ�")
        #=====�����ļ�====
        filename="rccps_"+TradeContext.BESBNO+"_"+AfaUtilTools.GetSysDate()+"_"+TradeContext.TransCode
        try:
            pub_path = os.environ["AFAP_HOME"]
            pub_path = pub_path + "/tmp/"
            f=open(pub_path+filename,"w")
        except IOError:
            return AfaFlowControl.ExitThisFlow('A099','���ļ�ʧ��')
            
        filecontext=""
        #=====д�ļ�����====
        for i in range(0,len(records)):
            #=====�����ļ�����====
            pub_list=str(records[i]['PBDAFILE']).split('/')
            AfaLoggerFunc.tradeInfo( pub_list)
            mfilename=""
            mfilename=pub_list[len(pub_list)-1]

            filecontext = records[i]['EFCTDAT'] + "|" + records[i]['PBDATYP'] + "|" + os.environ["AFAP_HOME"] + "/data/rccps/filein/" + mfilename + "|"

            f.write(filecontext+"\n")
        f.close()
        #=====����ӿڸ�ֵ====
        AfaLoggerFunc.tradeInfo( ">>>������ӿ�ֵ")
        TradeContext.PBDAFILE=filename                  #�ļ���
        TradeContext.RECCOUNT=str(len(records))         #��ѯ����
        TradeContext.RECALLCOUNT=str(len(records))      #�ܱ���
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����[TRC001_8550]�˳�***' )
    return True
