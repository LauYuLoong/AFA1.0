# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.���ҵ����ˮ״̬��ѯ
#=================================================================
#   �����ļ�:   TRCC001_8528.py
#   �޸�ʱ��:   2008-06-08
#   ���ߣ�      �˹�ͨ
##################################################################
import os
import rccpsDBTrcc_sstlog,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8528]����***' )

    #=====�ж�����ӿ�ֵ�Ƿ����====
    #if( not TradeContext.existVariable( "BJEDTE" ) ):
    #    return AfaFlowControl.ExitThisFlow('A099', '��������[BJEDTE]������')
    #    
    #if( not TradeContext.existVariable( "BSPSQN" ) ):
    #    return AfaFlowControl.ExitThisFlow('A099', '�������[BSPSQN]������')
    
    start_no=TradeContext.RECSTRNO      #��ʼ����
    sel_size=10                         #��ѯ����
    
    #=====���ɲ�ѯ���====
    wheresql=""
    
    #�ر��  20090401  ���Ӱ�(ǰ������,ǰ����ˮ��)��(��������,������ˮ��)��ѯ��ˮ״̬��ϸ��Ϣ
    check_flag = 0
    if TradeContext.existVariable('BJEDTE') and TradeContext.BJEDTE != '00000000' and TradeContext.existVariable('BSPSQN') and TradeContext.BSPSQN != '':
        wheresql = wheresql + "BJEDTE='" + TradeContext.BJEDTE + "'"
        wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "' and "
        check_flag = 1
    
    if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '00000000' and TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '':
        wheresql = wheresql + "FEDT='" + TradeContext.FEDT + "'"
        wheresql = wheresql + " AND RBSQ='" + TradeContext.RBSQ + "' and "
        check_flag = 1
    
    if TradeContext.existVariable('TRDT') and TradeContext.TRDT != '00000000' and TradeContext.existVariable('TLSQ') and TradeContext.TLSQ != '':
        wheresql = wheresql + "TRDT='" + TradeContext.TRDT + "'"
        wheresql = wheresql + " AND TLSQ='" + TradeContext.TLSQ + "' and "
        check_flag = 1
        
    if check_flag == 0:
        return AfaFlowControl.ExitThisFlow('A099', '��ѯ�����Ƿ�')
        
    wheresql = wheresql[:-5]    
    
    AfaLoggerFunc.tradeDebug( "���ɲ�ѯ������ ")
    
    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_sstlog.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ�ܱ���ʧ��' )
        
    #=====��ѯ���ݿ�====
    ordersql = " order by BCURSQ DESC "
    
    records=rccpsDBTrcc_sstlog.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )        
    elif(len(records)<=0):
        return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ�����' )        
    else:
    	try:
            #=====�����ļ�====
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
            
            if(f==None):
                return AfaFlowControl.ExitThisFlow('A099','���ļ�ʧ��' )
                   
            #=====д�ļ�����====
            filecontext=""
            for i in range(0,len(records)):
                filecontext= records[i]['BJEDTE']      + "|" \
                           + records[i]['BSPSQN']      + "|" \
                           + records[i]['BCSTAT']      + "|" \
                           + records[i]['BDWFLG']      + "|" \
                           + records[i]['BESBNO']      + "|" \
                           + records[i]['BEACSB']      + "|" \
                           + records[i]['BETELR']      + "|" \
                           + records[i]['BEAUUS']      + "|" \
                           + records[i]['FEDT']        + "|" \
                           + records[i]['RBSQ']        + "|" \
                           + records[i]['TRDT']        + "|" \
                           + records[i]['TLSQ']        + "|" \
                           + records[i]['SBAC']        + "|" \
                           + records[i]['ACNM']        + "|" \
                           + records[i]['RBAC']        + "|" \
                           + records[i]['OTNM']        + "|" \
                           + records[i]['DASQ']        + "|" \
                           + records[i]['MGID']        + "|" \
                           + records[i]['PRCCO']       + "|" \
                           + records[i]['STRINFO']     + "|" \
                           + str(records[i]['PRTCNT']) + "|" \
                           + records[i]['BJETIM']      + "|" \
                           + records[i]['NOTE3']       + "|" \
                           + str(records[i]['BCURSQ']) + "|"
                f.write(filecontext+"\n")      
            f.close()  
            
        except Exception, e:
            #=====�ر��ļ�====
            f.close()
            return AfaFlowControl.ExitThisFlow('A099','д�뷵���ļ�ʧ��' ) 
            
        #=====����ӿ�1====
        TradeContext.RECCOUNT=str(len(records))             #��ѯ����
        TradeContext.RECALLCOUNT=str(allcount)              #�ܱ���
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
        TradeContext.RECSTRNO=str(start_no)                 #��ʼ����
        TradeContext.PBDAFILE=filename                      #�ļ���

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8528]�˳�***' )
    return True
