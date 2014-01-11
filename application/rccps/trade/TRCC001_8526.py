# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ������.���������(1.���ز���).��Ʊ��Ϣ��ϸ��ѯ
#=================================================================
#   �����ļ�:   TRCC001_8526.py
#   ��    ��:   �˹�ͨ
#   �޸�ʱ��:   2008-07-09
##################################################################
import rccpsDBTrcc_bilinf,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *
import os

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8526]����***' )
        
    #=====�õ���ʼ����====
    start_no=TradeContext.RECSTRNO
        
    #=====��֯sql���====
    wheresql=""
    wheresql = wheresql + "NOTE3='" + TradeContext.BESBNO + "' and "
    
    #=====�ж���ʼʱ���Ƿ�Ϊ��====
    if (TradeContext.STRDAT != "00000000"):
        wheresql = wheresql + "BILDAT>='"+TradeContext.STRDAT+"' and "

    #=====�ж���ֹʱ���Ƿ�Ϊ��====
    if (TradeContext.ENDDAT != "00000000"):
        wheresql=wheresql+" BILDAT<='"+TradeContext.ENDDAT+"' and "
    
    #=====�жϻ�Ʊ����Ƿ�Ϊ��====
    if (TradeContext.BILTYP != ""):
        wheresql=wheresql+" BILTYP='"+TradeContext.BILTYP+"' and "
    
    #=====�жϻ�Ʊ״̬�Ƿ�Ϊ��====
    if (TradeContext.HPSTAT != ""):
        wheresql=wheresql+" HPSTAT='"+TradeContext.HPSTAT+"' and "

    #=====�ж϶Ҹ���ʽ�Ƿ�Ϊ��==== 
    if (TradeContext.PAYWAY != ""):
        wheresql=wheresql+" PAYWAY='"+TradeContext.PAYWAY+"' and "

    #=====�жϻ�Ʊ�������б�ʶ�Ƿ�Ϊ��====
    if(TradeContext.BILRS !="" ):
        wheresql=wheresql+" BILRS='"+TradeContext.BILRS+"' and "

    #=====�жϻ�Ʊ�汾���Ƿ�Ϊ��====        
    if(TradeContext.BILVER!="" ):
        wheresql=wheresql+" BILVER='"+TradeContext.BILVER+"' and "

    #=====�жϻ�Ʊ�����Ƿ�Ϊ��====        
    if(TradeContext.BILNO!="" ):
        wheresql=wheresql+" BILNO='"+TradeContext.BILNO+"' and "

    #=====�жϳ�Ʊ����Ƿ�Ϊ0====        
    if((TradeContext.BILAMT).strip() != '0.00' ):
        wheresql = wheresql + " BILAMT=" + str(TradeContext.BILAMT) + ' and '
    
    #=====ȥ��sql��ѯ������4λ"end "====    
    wheresql = wheresql[:-4]
        
    #=====��ʼ��ѯ�ܱ���====
    allcount=rccpsDBTrcc_bilinf.count(wheresql)
    
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','�����ܼ�¼��ʧ��' )
        
    #=====��ʼ��ѯ��ϸ====
    ordersql = " order by BILNO DESC"
    records=rccpsDBTrcc_bilinf.selectm(start_no,10,wheresql,ordersql)
    
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ�쳣' )
        
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('S999','�޶�Ӧ��¼' )
        
    else:
        #=====�����ļ�====
        filename = "rccps_" + TradeContext.BETELR + "_" + AfaUtilTools.GetHostDate() + "_" + TradeContext.TransCode       
        fpath=os.environ["AFAP_HOME"]+"/tmp/"
        f=open(fpath+filename,"w")
            
        if f == None:
            return AfaFlowControl.ExitThisFlow('S999','���ļ�ʧ��')
        
        for i in range(0,len(records)):            
            #=====�����ļ�����====
            AfaLoggerFunc.tradeDebug ("�����ļ����� ")
            
            filecontext = ""
            filecontext = filecontext + records[i]['BILVER']      + "|"    #��Ʊ�汾��
            filecontext = filecontext + records[i]['BILNO']       + "|"    #��Ʊ����
            filecontext = filecontext + records[i]['BILRS']       + "|"    #��Ʊ�������б�ʶ
            filecontext = filecontext + records[i]['BILTYP']      + "|"    #��Ʊ���
            filecontext = filecontext + records[i]['BILDAT']      + "|"    #��Ʊ����
            filecontext = filecontext + records[i]['PAYWAY']      + "|"    #�Ҹ���ʽ
            filecontext = filecontext + records[i]['REMBNKCO']    + "|"    #��Ʊ���к�
            filecontext = filecontext + records[i]['REMBNKNM']    + "|"    #��Ʊ������
            filecontext = filecontext + records[i]['PAYBNKCO']    + "|"    #���������к�
            filecontext = filecontext + records[i]['PAYBNKNM']    + "|"    #������������
            filecontext = filecontext + records[i]['PYRACC']      + "|"    #��Ʊ���˺�
            filecontext = filecontext + records[i]['PYRNAM']      + "|"    #��Ʊ�˻���
            filecontext = filecontext + records[i]['PYRADDR']     + "|"    #��Ʊ�˵�ַ
            filecontext = filecontext + records[i]['PYEACC']      + "|"    #�տ����˺�
            filecontext = filecontext + records[i]['PYENAM']      + "|"    #�տ��˻���
            filecontext = filecontext + records[i]['PYEADDR']     + "|"    #�տ��˵�ַ
            filecontext = filecontext + records[i]['PYHACC']      + "|"    #��Ʊ���˺�
            filecontext = filecontext + records[i]['PYHNAM']      + "|"    #��Ʊ�˻���
            filecontext = filecontext + records[i]['PYHADDR']     + "|"    #��Ʊ�˵�ַ
            filecontext = filecontext + records[i]['PYITYP']      + "|"    #�����˻�����
            filecontext = filecontext + records[i]['PYIACC']      + "|"    #�����˻��˺�
            filecontext = filecontext + records[i]['PYINAM']      + "|"    #�����˻�����
            filecontext = filecontext + records[i]['CUR']         + "|"    #����
            filecontext = filecontext + str(records[i]['BILAMT']) + "|"    #��Ʊ���
            filecontext = filecontext + str(records[i]['OCCAMT']) + "|"    #ʵ�ʽ�����
            filecontext = filecontext + str(records[i]['RMNAMT']) + "|"    #������
            filecontext = filecontext + records[i]['SEAL']        + "|"    #��Ѻ
            filecontext = filecontext + records[i]['USE']         + "|"    #��;
            filecontext = filecontext + records[i]['REMARK']      + "|"    #��ע
            filecontext = filecontext + records[i]['HPSTAT']      + "|"    #��Ʊ״̬

            f.write(filecontext+"\n")
            
        f.close()
        
    #=====����ӿ�====
    TradeContext.PBDAFILE=filename              #�ļ���
    TradeContext.RECCOUNT=str(len(records))     #��ѯ����
    TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8526]�˳�***' )
        
    return True
