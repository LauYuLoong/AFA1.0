# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.֧��ҵ��״̬�Ǽǲ���ѯ
#=================================================================
#   �����ļ�:   TRCC001_8530.py
#   �޸�ʱ��:   2008-06-09
#   ��    �ߣ�  ������
##################################################################
import rccpsDBTrcc_ztcbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,os
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8530]����***' )

    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
    
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ֹ����[ENDDAT]������')
    
    if( not TradeContext.existVariable( "BRSFLG" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '������־[BRSFLG]������')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    start_no = TradeContext.RECSTRNO        #��ʼ����
    sel_size = 10                           #��ѯ����
        
    #=====���ɲ�ѯ���====
    wheresql = ""
    wheresql = wheresql + "BESBNO='" + TradeContext.BESBNO + "' " 
    wheresql = wheresql + " AND BJEDTE>='" + TradeContext.STRDAT + "'"
    wheresql = wheresql + " AND BJEDTE<='" + TradeContext.ENDDAT + "'"

    #=====�ж�������־�Ƿ�Ϊ��====
    if(TradeContext.BRSFLG != ""):
        wheresql = wheresql +" AND BRSFLG='" + TradeContext.BRSFLG + "'"

    #=====�жϱ�������Ƿ�Ϊ��====
    if(TradeContext.BSPSQN != ""):
        wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "'"
    
    #=====�ж�ԭ���������Ƿ�Ϊ��====    
    if(TradeContext.BOJEDT != "00000000"):
        wheresql = wheresql + " AND BOJEDT='" + TradeContext.BOJEDT + "'"
    
    #=====�ж�ԭ������Ƿ�Ϊ��====    
    if(TradeContext.BOSPSQ != ""):
        wheresql = wheresql + " AND BOSPSQ='" + TradeContext.BOSPSQ + "'"
    
    #=====�жϸ����־�Ƿ�Ϊ��====    
    if(TradeContext.ISDEAL != ""):
        wheresql = wheresql + " AND ISDEAL='" + TradeContext.ISDEAL + "'"
        
    AfaLoggerFunc.tradeInfo( "��ѯ����: "+wheresql)
    
    #=====��ѯ�ܼ�¼��====
    allcount = rccpsDBTrcc_ztcbka.count(wheresql)
    if(allcount < 0):
        return AfaFlowControl.ExitThisFlow('A099', '��ѯ�ܼ�¼��ʧ��')
        
    AfaLoggerFunc.tradeDebug("��ѯ�ܼ�¼�����")
    
    #=====��ѯ���ݿ�====
    ordersql = " order by BJEDTE DESC,BSPSQN DESC"
    
    records = rccpsDBTrcc_ztcbka.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records == None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )    
    if len(records) <= 0:
        return AfaFlowControl.ExitThisFlow('A099','δ���ҵ�����' )
    else:
        #=====�����ļ�====
        filename = "rccps_" + TradeContext.BETELR+"_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode
        fpath = os.environ["AFAP_HOME"] + "/tmp/"
        
        f = open(fpath + filename,"w")
        
        if f == None:
            return AfaLoggerFunc.tradeInfo("S999","���ļ��쳣")
        filecontext = ""
        
        #=====д�ļ�����====
        for i in range(0,len(records)):
            filecontext = records[i]['BJEDTE']      + "|" \
                        + records[i]['BSPSQN']      + "|" \
                        + records[i]['BRSFLG']      + "|" \
                        + records[i]['TRCDAT']      + "|" \
                        + records[i]['TRCNO']       + "|" \
                        + records[i]['SNDBNKCO']    + "|" \
                        + records[i]['SNDBNKNM']    + "|" \
                        + records[i]['RCVBNKCO']    + "|" \
                        + records[i]['RCVBNKNM']    + "|" \
                        + records[i]['BOJEDT']      + "|" \
                        + records[i]['BOSPSQ']      + "|" \
                        + records[i]['ORTRCCO']     + "|" \
                        + records[i]['CUR']         + "|" \
                        + str(records[i]['OCCAMT']) + "|" \
                        + records[i]['CONT']        + "|" \
                        + records[i]['NCCTRCST']    + "|" \
                        + records[i]['MBRTRCST']    + "|" \
                        + records[i]['PRCCO']       + "|" \
                        + records[i]['STRINFO']     + "|"
                        
            f.write(filecontext+"\n")
        
        f.close()        
        AfaLoggerFunc.tradeInfo("�����ļ�����")
        
    #=====����ӿڸ�ֵ====
    TradeContext.RECSTRNO=start_no              #��ʼ����
    TradeContext.RECCOUNT=str(len(records))     #��ѯ����
    TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
    TradeContext.PBDAFILE=filename              #�ļ���
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8530]�˳�***' )
    return True