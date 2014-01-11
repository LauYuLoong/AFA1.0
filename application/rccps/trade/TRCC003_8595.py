# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�����˽���.���ʿ��ƺͽ������  ���潻��
#=================================================================
#   �����ļ�:   TRCC003_8595.py
#   �޸�ʱ��:   2011-05-11
#   ���ߣ�      ����̩
##################################################################
import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaAdminFunc,rccpsDBTrcc_acckj
import rccpsDBTrcc_balbka,rccpsDBTrcc_paybnk,rccpsDBTrcc_subbra
import rccpsMap8595CTradeContext2Dacckj
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.���ʿ���/���[8595] ����")
    
    AfaLoggerFunc.tradeInfo("����ǰ����(���ز���,����ǰ����)")
    
    #=====У����ʿ��ƽ��ױ����Ƿ����====                                              
    if not TradeContext.existVariable("OPTYPE"):          #��������  ���ʿ���/���ʽ��  
        return AfaFlowControl.ExitThisFlow('A099','�����������Ͳ���Ϊ��')               
    
    #=====�ж��ʻ�����====
    if( TradeContext.OPTYPE == '0' ): #���ʿ���
        AfaLoggerFunc.tradeInfo("������ʿ��Ʋ�������")
        TradeContext.TRCCO = '3000508'            #������
        
        if not TradeContext.existVariable("TRCDAT"):          #ί������
            return AfaFlowControl.ExitThisFlow('A099','ί�����ڲ���Ϊ��')  
        
        if not TradeContext.existVariable("SNDBNKCO"):          #�����к�
            return AfaFlowControl.ExitThisFlow('A099','�����кŲ���Ϊ��')    
        
        if not TradeContext.existVariable("SNDBNKNM"):          #��������
            return AfaFlowControl.ExitThisFlow('A099','������������Ϊ��')    
        
        if not TradeContext.existVariable("RCVBNKCO"):          #�����к�
            return AfaFlowControl.ExitThisFlow('A099','�����кŲ���Ϊ��')    
        
        if not TradeContext.existVariable("RCVBNKNM"):          #��������
            return AfaFlowControl.ExitThisFlow('A099','������������Ϊ��')   
        
        if not TradeContext.existVariable("ORTRCDAT"):          #ԭί������
            return AfaFlowControl.ExitThisFlow('A099','ԭί�����ڲ���Ϊ��')  
            
        if not TradeContext.existVariable("ORTRCCO"):          #ԭ���״���
            return AfaFlowControl.ExitThisFlow('A099','ԭ���״��벻��Ϊ��')  
                 
        if not TradeContext.existVariable("ORTRCNO"):           #ԭ������ˮ��
            return AfaFlowControl.ExitThisFlow('A099','ԭ������ˮ�Ų���Ϊ��') 
            
        if not TradeContext.existVariable("ORSNDSUBBNK"):         #ԭ�����Ա�к�
            return AfaFlowControl.ExitThisFlow('A099','ԭ�����Ա�кŲ���Ϊ��')  
            
        if not TradeContext.existVariable("ORSNDBNK"):         #ԭ�����к�
            return AfaFlowControl.ExitThisFlow('A099','ԭ�����Ա�кŲ���Ϊ��')  
            
        if not TradeContext.existVariable("ORRCVSUBBNK"):          #ԭ���ܳ�Ա�к�
            return AfaFlowControl.ExitThisFlow('A099','ԭ���ܳ�Ա�кŲ���Ϊ��')  
        
        if not TradeContext.existVariable("ORRCVBNK"):          #ԭ�����к�
            return AfaFlowControl.ExitThisFlow('A099','ԭ�����кŲ���Ϊ��')  
        
        if not TradeContext.existVariable("CUR"):              #���ҷ���
            return AfaFlowControl.ExitThisFlow('A099','ԭ���ҷ��Ų���Ϊ��')  
        
        if not TradeContext.existVariable("OCCAMT"):        #ԭ���׽��
            return AfaFlowControl.ExitThisFlow('A099','ԭ���׽���Ϊ��') 
             
        if not TradeContext.existVariable("CHRG"):          #ԭ������
            return AfaFlowControl.ExitThisFlow('A099','ԭ�����Ѳ���Ϊ��') 
                     
        if not TradeContext.existVariable("ERRCONBAL"):          #���ƻ��ؽ��
            return AfaFlowControl.ExitThisFlow('A099','���ƻ��ؽ���Ϊ��') 
        
        OCCAMT    = float(TradeContext.OCCAMT)    #���׽��
        ERRCONBAL = float(TradeContext.ERRCONBAL) #���ʿ��ƽ��
        CHRG      = float(TradeContext.CHRG)      #������ 
        
        #if  ERRCONBAL>(OCCAMT+CHRG):
        #     return AfaFlowControl.ExitThisFlow('A099','���ʿ��ƽ��ܳ���ԭ���׽��')
        
        #���ʿ���ʱ��ҪУ�鷢���кźͽ����кű�����ԭ�����кź�ԭ�����к�һ��
        AfaLoggerFunc.tradeInfo(TradeContext.SNDBNKCO )
        AfaLoggerFunc.tradeInfo(TradeContext.ORSNDBNK )
        
        if (TradeContext.SNDBNKCO != TradeContext.ORSNDBNK):
            return AfaFlowControl.ExitThisFlow('A099','�����кź�ԭ�����кŲ���')
        
        AfaLoggerFunc.tradeInfo(TradeContext.RCVBNKCO )
        AfaLoggerFunc.tradeInfo(TradeContext.ORRCVBNK )
        
        if (TradeContext.RCVBNKCO != TradeContext.ORRCVBNK):
            return AfaFlowControl.ExitThisFlow('A099','�����кź�ԭ�����кŲ���')    
        
        #�ж�ί�����ں�ԭ�������ڵĲ�ֵ�Ƿ����15��������
        sTrxDate   = AfaAdminFunc.getTimeFromNow(-15)   #ȡ����ǰ���ڵ�ǰ15�������
        #if (TradeContext.ORTRCDAT < sTrxDate ):
        #    return AfaFlowControl.ExitThisFlow('A099','���ʿ���������ٲ��ó���ԭ�����պ�15��')   
        #end
       
        #=====��֯��ѯ�ֵ�====                            
        AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ�")    
        
        wheresql_dic={}
        wheresql_dic['ORTRCDAT'] =TradeContext.ORTRCDAT   #ԭ��������
        wheresql_dic['SNDBNKCO'] =TradeContext.ORSNDBNK   #ԭ�����к�
        wheresql_dic['ORTRCNO']  =TradeContext.ORTRCNO    #ԭ������ˮ��
        wheresql_dic['TRCCO']    ="3000508"               #���ʿ��ƽ�����
        wheresql_dic['CONSTS']    ="0"                    #���Ƴɹ�
        
        #=====��ʼ��ѯ���ݿ�====
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #��ѯ���ʿ��ƽ�صǼǲ� 
        AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
        if(records==None):                                        
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
        elif(len(records)>0):
            return AfaFlowControl.ExitThisFlow('A099','�ñʴ����Ѿ����Ƴɹ��������ظ�����')
            
    elif( TradeContext.OPTYPE == '1' ): #���ʽ��
        AfaLoggerFunc.tradeInfo("������ʽ�ز�������")
        TradeContext.TRCCO = '3000509'            #������  
        #=====У����ʿ��ƽ��ױ����Ƿ����====  
        if not TradeContext.existVariable("TRCDAT"):          #ί������      
            return AfaFlowControl.ExitThisFlow('A099','ί�����ڲ���Ϊ��')    
        
        if not TradeContext.existVariable("SNDBNKCO"):          #�����к�     
            return AfaFlowControl.ExitThisFlow('A099','�����кŲ���Ϊ��')     
                                                                               
        if not TradeContext.existVariable("SNDBNKNM"):          #��������     
            return AfaFlowControl.ExitThisFlow('A099','������������Ϊ��')     
        
        if not TradeContext.existVariable("RCVBNKCO"):          #�����к�   
            return AfaFlowControl.ExitThisFlow('A099','�����кŲ���Ϊ��')   
                                                                            
        if not TradeContext.existVariable("RCVBNKNM"):          #��������   
            return AfaFlowControl.ExitThisFlow('A099','������������Ϊ��')   
    
        if not TradeContext.existVariable("ORTRCDAT"):          #ԭί������        
            return AfaFlowControl.ExitThisFlow('A099','ԭί�����ڲ���Ϊ��')        
                                                                                   
        if not TradeContext.existVariable("ORTRCNO"):           #ԭ������ˮ��     
            return AfaFlowControl.ExitThisFlow('A099','ԭ������ˮ�Ų���Ϊ��')     
                                                          
        #=====��֯��ѯ�ֵ�====                            
        AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ�")    
        
        wheresql_dic={}
        wheresql_dic['TRCDAT'] =TradeContext.ORTRCDAT   #ԭ��������
        wheresql_dic['SNDBNKCO'] =TradeContext.ORSNDBNK   #ԭ�����к�
        wheresql_dic['TRCNO']  =TradeContext.ORTRCNO     #ԭ������ˮ��
        wheresql_dic['TRCCO']    ="3000508"               #���ʿ��ƽ�����
        wheresql_dic['CONSTS']    ="0"                    #���Ƴɹ�
        
        #=====��ʼ��ѯ���ݿ�====
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #��ѯ���ʿ��ƽ�صǼǲ� 
        AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
        if(records==None):                                        
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
        
        elif(len(records)==0):
            return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ�ԭ���ʿ��ƽ������ݣ��������������Ƿ�����,����ԭ���׿���ʧ�ܣ����ܽ�ء�')
        
        else:
            TradeContext.ORMFNBAK = records['MSGFLGNO']                 #���ʿ��Ƶı��ı�ʶ�� �ڽ��ʱ��Ҫ���ڲο����ı�ʶ����
            if  ((records['ORTRCCO']=='3000103')or(records['ORTRCCO']=='3000105')or (records['ORTRCCO']=='3000102')or(records['ORTRCCO']=='3000104')):
                TradeContext.ACCNO    = records['ORPYRACC']
                TradeContext.ACCNONAME= records['ORPYRNAM'] 
            else:
                TradeContext.ACCNO    = records['ORPYEACC']             #���ʽ���˺� 
                TradeContext.ACCNONAME= records['ORPYENAM']             #���ʽ���˻��� 
            
            TradeContext.AMOUNT       = str(records['ERRCONBAL'])             #���ʽ�ؽ��
            
    else:
        return AfaFlowControl.ExitThisFlow("S999", "�Ƿ��Ĳ�������")
       
    #=====��֯���ʿ���/���������====
    AfaLoggerFunc.tradeInfo("��ʼ����ʿ���/���������")
    
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET009'                    #ʵʱ��Ϣ����   ��ҵ��Ҫ��  SET000����ECHO����
    #�Ƿ���Ҫ�ѽ��ܳ�Ա�кźͷ��ͳ�Ա�кŸ�ֵ
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN      #���ͳ�Ա�к�
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN      #���ճ�Ա�к�
    #TradeContext.SNDSTLBIN= PL_BESBNO_BCLRSB           #���ͷ���Ա�к�
    #TradeContext.RCVSTLBIN= PL_RCV_CENTER          #���ܷ���Ա�к�
    TradeContext.SNDBRHCO = TradeContext.BESBNO    #���ͻ�����
    TradeContext.SNDCLKNO = TradeContext.BETELR    #���͹�Ա�� 
    TradeContext.SNDTRDAT = TradeContext.TRCDAT    #�������������
    TradeContext.SNDTRTIM = TradeContext.BJETIM    #���������ʱ��
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo  #�����кţ��������ڣ�������ˮ�� ��ͬ��ɱ��ı�ʶ��
    TradeContext.ORMFN     = TradeContext.ORSNDBNK + TradeContext.ORTRCDAT + TradeContext.ORTRCNO  #�ο����ı�ʶ�� ԭ�����кţ�ԭ�������ڣ�ԭ������ˮ��          
    #��Ϊ���ʽ��ʱ ���Ĳο���ʶ��Ϊ���ʿ��Ƶı��ı�ʶ��
    if(TradeContext.TRCCO == '3000509' ):
        TradeContext.ORMFN = TradeContext.ORMFNBAK
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate  #ũ������������
    TradeContext.OPRTYPNO = "30"                   #ҵ������
    TradeContext.ROPRTPNO = "30"                   #�ο�ҵ������
    TradeContext.TRANTYP  = "0"                    #��������
    #=====ҵ��Ҫ�ؼ�==== 
    TradeContext.TRCNO    =  TradeContext.SerialNo #������ˮ��    
    TradeContext.CUR      = "CNY"                  #���ҷ���
    TradeContext.PRCCO    = ""                     #������   
    
    #=====�ǼǴ��ʿ��ƽ�صǼǲ�====
    AfaLoggerFunc.tradeInfo('���Ǽ��ֵ丳ֵ')
    insert_dict = {}
    rccpsMap8595CTradeContext2Dacckj.map(insert_dict)
    insert_dict['CUR']      = '01'                #���� 
    insert_dict['MSGFLGNO'] = TradeContext.MSGFLGNO #���ı�ʶ��
    insert_dict['BRSFLG']   = PL_BRSFLG_SND #���˱�ʶ
    insert_dict['NOTE1']     = TradeContext.BJETIM
    
    AfaLoggerFunc.tradeInfo('��ʼ�ǼǴ��ʿ��ƺͽ�صǼǲ�')
    res = rccpsDBTrcc_acckj.insertCmt(insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','�ǼǴ��ʿ��ƽ�صǼǲ�ʧ��')
        
    AfaLoggerFunc.tradeInfo("����ǰ����(���ز���,����ǰ����) ����")
    
    return True    
        
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('���׺���')
    
    AfaLoggerFunc.tradeInfo('errorCode:' + TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo('errorMsg:' + TradeContext.errorMsg)
    
    #=====�ж�AFE�Ƿ��ͳɹ�====
    if TradeContext.errorCode != '0000':
        #=====�������ķ����룬�͸���====
        AfaLoggerFunc.tradeInfo("��ʼ���´��ʿ��ƽ�صǼǲ�")
        update_dict = {'PRCCO':'RCCS1105','STRINFO':'AFE����ʧ��'}                 #�����룬�������Ӧ����Ϣ����
        where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN}   #ϵͳ���ڣ�ƽ̨��ˮ��(���ı��)
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','���´��ʿ��ƽ�صǼǲ�ʧ��')
           
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,'�����ķ��ʹ��ʿ��ƽ��������ʧ��')
    
    else:
        AfaLoggerFunc.tradeInfo('���ͳɹ�')
        
        update_dict = {'PRCCO':'RCCS1000','STRINFO':'AFE���ͳɹ�'}   #�����룬�������Ӧ����Ϣ����               
        where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN} #ϵͳ���ڣ�ƽ̨��ˮ��(���ı��) 
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)                                                
        if( res == -1 ):                                                                                         
            return AfaFlowControl.ExitThisFlow('A009','���´��ʿ��ƽ�صǼǲ�ʧ��')                              
                                                                                                                 
        AfaLoggerFunc.tradeInfo('���׺��� ����')
    
        AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.���ʿ��ƽ��[8595] �˳�")
    
        return True
    