# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.�����кŲ�ѯ
#=================================================================
#   �����ļ�:   TRCC001_8523.py
#   �޸�ʱ��:   2008-06-05
#   ���ߣ�      �˹�ͨ
##################################################################

import rccpsDBTrcc_paybnk,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *
import os

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8523]����***' )
    
    #=====�жϽӿ��Ƿ����====
    if( (not TradeContext.existVariable("BANKBIN")) and (not TradeContext.existVariable("LNAME")) ):
        return AfaFlowControl.ExitThisFlow('A099','����[LNAME]�к�[BANKBIN]����ͬʱΪ��' )
        
    if int(TradeContext.RECSTRNO) == 0:
        return AfaFlowControl.ExitThisFlow('A009','��ʼ����[RECSTRNO]����Ϊ��')
    
    #=====��ʼ��������ѯ������ֵ====    
    start_no = TradeContext.RECSTRNO
    sel_size = 10 
    
    #=====��֯sql���====
    wheresql=""
    if(TradeContext.BANKBIN!=""):
        wheresql1=TradeContext.BANKBIN.split( )
        
        wheresql="BANKBIN like '%"
        j=0
        
        #=====���ֻ��һ����¼ʱ��������ѭ������====
        for i in range(0,len(wheresql1)-1):
            wheresql=wheresql+wheresql1[i]+"%' and BANKBIN like '%"
            j=j+1
        
        wheresql=wheresql+wheresql1[j]+"%'"
        
    if(TradeContext.LNAME!=""):
        wheresql2=TradeContext.LNAME.split()
        
        #=====�ж��к��Ƿ�Ϊ��====
        if(TradeContext.BANKBIN!=""):
            wheresql=wheresql+" and BANKNAM like '%"        
        else:
            wheresql=wheresql+" BANKNAM like '%"
            
        j=0
        #=====���ֻ��һ����¼ʱ��������ѭ������====
        for i in range(0,len(wheresql2)-1):
            wheresql=wheresql+wheresql2[i]+"%' and BANKNAM like '%"
            j=j+1
            
        wheresql=wheresql+wheresql2[j]+"%'"
        
    AfaLoggerFunc.tradeInfo("��ѯ����Ϊ��"+wheresql)
    
    #=====��ѯ�ܱ���====
    allcount=rccpsDBTrcc_paybnk.count(wheresql)
    if(allcount<0):
        return AfaFlowControl.ExitThisFlow('A099','�����ܼ�¼��ʧ��' )
    
    AfaLoggerFunc.tradeInfo("�ܼ�¼��Ϊ��"+str(allcount))
    
    #=====��ʼ�������ݿ�====
    ordersql = " order by BANKBIN "
    records=rccpsDBTrcc_paybnk.selectm(start_no,sel_size,wheresql,ordersql)
    
    if(records==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ���ݿ�ʧ��' )        
    elif(len(records)==0):
        return AfaFlowControl.ExitThisFlow('A099','û�в�ѯ������' )        
    else:
        #=====���ļ�====
        filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
        fpath=os.environ["AFAP_HOME"]+"/tmp/"
        f=open(fpath+filename,"w")
        
        if(f==None):
            return AfaFlowControl.ExitThisFlow('A099','���ļ�ʧ��' )
            
        #=====д�ļ�����====
        AfaLoggerFunc.tradeInfo( '>>>��ʼ��֯�ļ�' )       
        for i in xrange(0,len(records)):
            filecontext = records[i]['BANKBIN']    + "|" \
                        + records[i]['BANKNAM']    + "|" \
                        + records[i]['BANKSTATUS'] + "|" \
                        + records[i]['BANKATTR']   + "|" \
                        + records[i]['STLBANKBIN'] + "|" \
                        + records[i]['BANKADDR']   + "|" \
                        + records[i]['BANKPC']     + "|" \
                        + records[i]['BANKTEL']    + "|" \
                        + records[i]['EFCTDAT']    + "|" \
                        + records[i]['INVDAT']     + "|" \
                        + records[i]['ALTTYPE']    + "|" \
                        + records[i]['PRIVILEGE']  + "|"
            f.write(filecontext+"\n")
        f.close()
        
        #=====���ؽӿڸ�ֵ====
        TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
        TradeContext.RECCOUNT=str(len(records))     #��ѯ����
        TradeContext.PBDAFILE=filename              #�ļ�����
        TradeContext.errorMsg="��ѯ�ɹ�"
        TradeContext.errorCode="0000"

        AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8523]�˳�***' )

        return True
