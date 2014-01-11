# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).����\�����Ǽǲ���ѯ
#===============================================================================
#   ģ���ļ�:   TRCC001_8566.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����
#   �޸�ʱ��:   2008-10-20
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_atcbka,rccpsDBTrcc_mpcbka

#=====���Ի��������ز�����====
def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).����\�����Ǽǲ���ѯ[TRC001_8566]����***' )
        
    #=====��Ҫ�Լ��====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")
    
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
    
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ֹ����[ENDDAT]������')
    
    if( not TradeContext.existVariable( "TRCCO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '���״���[TRCCO]������')
    
    if( not TradeContext.existVariable( "BRSFLG" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '������־[BRSFLG]������')
        
    if( not TradeContext.existVariable( "BESBNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '������[BESBNO]������')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
        
    AfaLoggerFunc.tradeInfo(">>>��Ҫ�Լ�����")
    
    #=====��֯sql���====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯsql���")
    
    wheresql=""
    wheresql=wheresql+"BESBNO='"+TradeContext.BESBNO+"'"
    wheresql=wheresql+" AND BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    
    ordersql = " order by BJEDTE DESC,BSPSQN DESC "
    
    start_no=TradeContext.RECSTRNO          #��ʼ����
    sel_size=10                             #��ѯ����
    
    #=====�жϽ��״����Ƿ�Ϊ��====
    if(TradeContext.TRCCO != ""):
        wheresql = wheresql + " AND TRCCO='" + TradeContext.TRCCO + "'"    
    
    #=====�ж�ԭ���״����Ƿ�Ϊ��====
    if(TradeContext.ORTRCCO != ""):
        wheresql = wheresql + " AND ORTRCCO='" + TradeContext.ORTRCCO + "'" 
        
    #=====�жϱ�������Ƿ�Ϊ��====
    if(TradeContext.BSPSQN != ""):
        wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN + "'"
    
    #=====�ж�ԭ��������Ƿ�Ϊ��====
    if(TradeContext.BOSPSQ != ""):
        wheresql = wheresql + " AND BOSPSQ='" + TradeContext.BOSPSQ + "'"
            
    #=====�ж�������־�Ƿ�Ϊ��====
    if(TradeContext.BRSFLG != ""):
        wheresql = wheresql +" AND BRSFLG='" + TradeContext.BRSFLG + "'"
        
    AfaLoggerFunc.tradeDebug(">>>������֯��ѯsql���")
    AfaLoggerFunc.tradeDebug(">>>sql="+str(wheresql) )
    
    #=====3000506 �Զ������Ǽǲ���ѯ====
    if TradeContext.TRCCO == '3000506':
        #=====��ѯ�ܱ���====
        allcount=rccpsDBTrcc_atcbka.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999','��ѯ�ܼ�¼���쳣')
            
        #=====��ѯ��ϸ====
        AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
        records=rccpsDBTrcc_atcbka.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ�����Ǽǲ��쳣')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '�����Ǽǲ����޴˶�Ӧ��Ϣ')
    
    #=====3000504 �ֹ������Ǽǲ���ѯ====
    elif TradeContext.TRCCO == '3000504':
        #=====��ѯ�ܱ���====
        allcount=rccpsDBTrcc_mpcbka.count(wheresql)
        if(allcount == -1):
            return AfaFlowControl.ExitThisFlow('S999','��ѯ�ܼ�¼���쳣')
            
        #=====��ѯ��ϸ====
        AfaLoggerFunc.tradeInfo("wheresql=" + wheresql)
        records=rccpsDBTrcc_mpcbka.selectm(start_no,sel_size,wheresql,ordersql)
        if(records == None):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ�����Ǽǲ��쳣')
        if(len(records) <= 0):
            return AfaFlowControl.ExitThisFlow('S999', '�����Ǽǲ����޴˶�Ӧ��Ϣ')
    else:
        return AfaFlowControl.ExitThisFlow('S999','������Ƿ�' )      
    
    #=====�����ļ�====
    try:
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
        fpath=os.environ["AFAP_HOME"]+"/tmp/"
        f=open(fpath+filename,"w")
    except IOError:
        return AfaFlowControl.ExitThisFlow('S099','���ļ�ʧ��')
              
    #=====д�ļ�����====
    AfaLoggerFunc.tradeInfo("��¼����" + str(len(records)))
    try:
        filecontext=""
        for i in range(0,len(records)):
            #AfaLoggerFunc.tradeDebug("д���"+str(i)+"�ʼ�¼��ʼ")
            filecontext= records[i]['BJEDTE']        + "|" \
                       + records[i]['BSPSQN']        + "|" \
                       + records[i]['BRSFLG']        + "|" \
                       + records[i]['BESBNO']        + "|" \
                       + records[i]['BETELR']        + "|" \
                       + records[i]['BEAUUS']        + "|" \
                       + records[i]['NCCWKDAT']      + "|" \
                       + records[i]['TRCCO']         + "|" \
                       + records[i]['TRCDAT']        + "|" \
                       + records[i]['TRCNO']         + "|" \
                       + records[i]['ORTRCDAT']      + "|" \
                       + records[i]['ORTRCNO']       + "|" \
                       + records[i]['SNDMBRCO']      + "|" \
                       + records[i]['RCVMBRCO']      + "|" \
                       + records[i]['SNDBNKCO']      + "|" \
                       + records[i]['SNDBNKNM']      + "|" \
                       + records[i]['RCVBNKCO']      + "|" \
                       + records[i]['RCVBNKNM']      + "|" \
                       + records[i]['BOJEDT']        + "|" \
                       + records[i]['BOSPSQ']        + "|" \
                       + records[i]['RESNCO']        + "|" \
                       + records[i]['PRCCO']         + "|" \
                       + records[i]['STRINFO']       + "|" 
                           
            f.write(filecontext+"\n")
            #AfaLoggerFunc.tradeDebug("д���"+str(i)+"�ʼ�¼����")
    except Exception,e:     
        f.close()
        return AfaFlowControl.ExitThisFlow('S099','д�ļ�ʧ��')
    
    #=====����ӿڸ�ֵ====
    TradeContext.PBDAFILE=filename              #�ļ���
    TradeContext.RECCOUNT=str(len(records))     #���β�ѯ����
    TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
    
    AfaLoggerFunc.tradeDebug("filename=" + filename)
    
    TradeContext.PBDAFILE=filename              #�ļ���
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)����\�����Ǽǲ���ѯ[TRC001_8566]�˳�***' )
    
    return True
    
    
