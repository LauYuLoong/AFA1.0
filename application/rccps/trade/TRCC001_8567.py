# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).ͨ��ͨ��ҵ��Ǽǲ���ѯ
#===============================================================================
#   ģ���ļ�:   TRCC001_8567.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-10-24
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka 

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������(1.���ز���).ͨ��ͨ��ҵ��Ǽǲ���ѯ[TRCC001_8567]����***' )
    
    #=====��Ҫ�Լ��====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")
    
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
        
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ֹ����[ENDDAT]������')
    
    if( not TradeContext.existVariable( "BRSFLG" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '������־[BRSFLG]������')

    if( not TradeContext.existVariable( "PYITYP" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '���۱�־[PYITYP]������')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    #=====��֯sql���====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯsql���")
    
    wheresql = ""
    wheresql = wheresql + "BJEDTE>='" + TradeContext.STRDAT + "' AND BJEDTE<='" + TradeContext.ENDDAT + "' "
    
    ordersql = " order by BJEDTE DESC,BSPSQN DESC,NCCWKDAT DESC "
    
    start_no = TradeContext.RECSTRNO        #��ʼ����
    sel_size = 10                           #��ѯ����
    
    #====add by pgt 0106 �����µĻ����ŵ��ж�====
    if(TradeContext.BESBNO1 != ""):
        wheresql = wheresql + " and BESBNO='" + TradeContext.BESBNO1 + "' " 
        
    else:
        if(TradeContext.BESBNO != PL_BESBNO_BCLRSB):
            wheresql = wheresql + " and BESBNO='" + TradeContext.BESBNO + "' " 
    
    #=====�ж�������־�Ƿ�Ϊ��====
    if(TradeContext.BRSFLG != ""):
        wheresql = wheresql + " AND BRSFLG='" + TradeContext.BRSFLG + "' "
        
#    #=====�жϽ��������Ƿ�Ϊ��====
#    if(TradeContext.OPRTPNO != ""):
#        wheresql = wheresql + " AND OPRTPNO='" + TradeContext.OPRTPNO + "' "
   
    #=====�жϱ�������Ƿ�Ϊ��====
    if(TradeContext.BSPSQN != ""):
        wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "' "
        
    #=====�ж�ҵ��״̬�Ƿ�Ϊ��====
    if(TradeContext.BCSTAT != ""):
        wheresql = wheresql + " AND OPRATTNO='" + TradeContext.BCSTAT + "' "	
        
    #=====�жϿ��۱�־�Ƿ�Ϊ��====
    if(TradeContext.PYITYP != ""):
        #wheresql = wheresql + " AND BBSSRC='" + TradeContext.PYITYP + "' "
        wheresql = wheresql + " AND ((PYETYP = '" + TradeContext.PYITYP + "' AND TRCCO in ('3000002','3000003','3000004','3000005')) OR (PYRTYP = '" + TradeContext.PYITYP + "' AND TRCCO in ('3000102','3000103','3000104','3000105')))"
    
    #=====�жϷ������к��Ƿ�Ϊ��====
    if(TradeContext.SNDBNKCO != ""):
        wheresql = wheresql + " AND SNDBNKCO='" + TradeContext.SNDBNKCO + "' "
    
    #=====�жϽ������к��Ƿ�Ϊ��====
    if(TradeContext.RCVBNKCO != ""):
        wheresql = wheresql + " AND RCVBNKCO='" + TradeContext.RCVBNKCO + "' "
    
    AfaLoggerFunc.tradeDebug(">>>������֯��ѯsql���")    
    
    #=====��ѯ�ܼ�¼��====
    allcount=rccpsDBTrcc_wtrbka.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ�ܱ���ʧ��' )
        
    #=====��ѯ���ݿ�====
    
    AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
    records = rccpsDBTrcc_wtrbka.selectm(start_no,sel_size,wheresql,ordersql)
    
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
                
                #=====�õ�ҵ��״̬BCSTAT==== 
                stat_dict = {}
                if not rccpsState.getTransStateCur(records[i]['BJEDTE'],records[i]['BSPSQN'],stat_dict):
                    return AfaFlowControl.ExitThisFlow( 'S999', '��ǰҵ��Ǽǲ�û�����������ļ�¼' )
                    
                filecontext= records[i]['BJEDTE']          + "|" \
                           + records[i]['BSPSQN']          + "|" \
                           + records[i]['BRSFLG']          + "|" \
                           + stat_dict['BCSTAT']           + "|" \
                           + stat_dict['BDWFLG']           + "|" \
                           + records[i]['BESBNO']          + "|" \
                           + records[i]['BETELR']          + "|" \
                           + records[i]['BEAUUS']          + "|" \
                           + records[i]['DCFLG']           + "|" \
                           + records[i]['OPRNO']           + "|" \
                           + records[i]['NCCWKDAT']        + "|" \
                           + records[i]['TRCCO']           + "|" \
                           + records[i]['TRCDAT']          + "|" \
                           + records[i]['TRCNO']           + "|" \
                           + records[i]['COTRCNO']         + "|" \
                           + records[i]['SNDMBRCO']        + "|" \
                           + records[i]['RCVMBRCO']        + "|" \
                           + records[i]['SNDBNKCO']        + "|" \
                           + records[i]['SNDBNKNM']        + "|" \
                           + records[i]['RCVBNKCO']        + "|" \
                           + records[i]['RCVBNKNM']        + "|" \
                           + records[i]['CUR']             + "|" \
                           + str(records[i]['OCCAMT'])     + "|" \
                           + records[i]['CHRGTYP']         + "|" \
                           + str(records[i]['CUSCHRG'])    + "|" \
                           + records[i]['PYRACC']          + "|" \
                           + records[i]['PYRNAM']          + "|" \
                           + records[i]['PYEACC']          + "|" \
                           + records[i]['PYENAM']          + "|" \
                           + records[i]['STRINFO']         + "|" \
                           + records[i]['CERTTYPE']        + "|" \
                           + records[i]['CERTNO']          + "|" \
                           + records[i]['BNKBKNO']         + "|" \
                           + str(records[i]['BNKBKBAL'])   + "|" 
                           
                f.write(filecontext+"\n")      
        except Exception,e:                                        
            f.close()                                              
            return AfaFlowControl.ExitThisFlow('S099','д�ļ�ʧ��')
            
    #=====����ӿڸ�ֵ====
    TradeContext.RECSTRNO=start_no              #��ʼ����
    TradeContext.RECCOUNT=str(len(records))     #���β�ѯ����
    TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
#    TradeContext.PRTDAT= TradeContext.BJEDTE    #��ӡ����
    TradeContext.PBDAFILE=filename              #�ļ���
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������(1.���ز���).ͨ��ͨ��ҵ��Ǽǲ���ѯ[TRCC001_8567]�˳�***' )
    return True 	
