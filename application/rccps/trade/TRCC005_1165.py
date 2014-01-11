# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�Ҵ��ʿ��ƽ�ؽ��ս���.���ʿ��ƽ�ؽ���   #���з���Ĵ��ʿ��ƽ�ؽ���,������Ϊ�����ж�������п��ƽ�ش���
#=================================================================
#   �����ļ�:   TRCC005_1165.py
#   �޸�ʱ��:   2011��05-17
#   ���ߣ�      ����̩
##################################################################

import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaAfeFunc,HostContext,AfaUtilTools,HostContext,rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx
import AfaFunc,rccpsDBFunc
import AfaDBFunc,rccpsState,rccpsGetFunc,rccpsHostFunc
import rccpsDBTrcc_acckj
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�Ҵ��ʿ��ƽ�ؽ��ս���.���ʿ��ƽ�ز�ѯ[1165] ����")
    
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)  #������Ϣ
    
    AfaLoggerFunc.tradeInfo("����ǰ����(�Ǽ���ˮ,����ǰ����)")
    
    #=====�ж��Ƿ�����ظ�����====
    AfaLoggerFunc.tradeInfo("�ж��Ƿ�����ظ�����")
    acckj_dict = {'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO,'SNDBNKCO':TradeContext.SNDBNKCO}#ί�����ڣ�������ˮ�ţ������к�
    record_acckj = rccpsDBTrcc_acckj.selectu(acckj_dict)
    if( record_acckj == None ):
        return AfaFlowControl.ExitThisFlow('A009','�ж��ظ�����ʱ��ѯ���ʿ��ƽ�صǼǲ�ʧ��')
        
    if( len(record_acckj) > 0 ):    #�����ظ�����
        AfaLoggerFunc.tradeInfo("�����ظ�����")
        
        #====��֯Ӧ����====
        if (TradeContext.TRCCO=='3000508'):
            Rcvmbrco = TradeContext.ORSNDSUBBNK     #���ͷ���Ա�к�  
        if (TradeContext.TRCCO=='3000509'):  
            Rcvmbrco = TradeContext.SNDMBRCO      
        Sndmbrco = TradeContext.RCVMBRCO        #���շ���Ա�к�
        Ormfn    = TradeContext.ORRCVSUBBNK     #���ı�ʶ��
        #=====����ͷ====
        TradeContext.MSGTYPCO = 'SET010'                    #���������
        TradeContext.RCVSTLBIN = Rcvmbrco                    #���ܷ���Ա�к�
        TradeContext.SNDSTLBIN = Sndmbrco                    #���ͷ���Ա�к�
        TradeContext.SNDBRHCO = TradeContext.BESBNO         #�����������
        TradeContext.SNDCLKNO = TradeContext.BETELR         #�����й�Ա��
        TradeContext.SNDTRDAT = TradeContext.TRCDAT         #�����н�������
        TradeContext.SNDTRTIM = TradeContext.BJETIM         #�����н���ʱ��
        TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.TRCDAT + TradeContext.SerialNo  #���ı�ʶ��
        TradeContext.ORMFN    = Ormfn                                                 #�ο����ı�ʾ��
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate    #���Ĺ�������
        TradeContext.OPRTYPNO = '30'                        #ҵ������
        TradeContext.ROPRTPNO = '30'                        #�ο�ҵ������
        TradeContext.TRANTYP  = '0'                         #��������
        #=====ҵ��Ҫ�ؼ�====
        TradeContext.OCCAMT   =  record_acckj['OCCAMT']     #���׽��
        TradeContext.CHRG     =  record_acckj['CHRG']       #������
        TradeContext.ERRCONBAL=  record_acckj['ERRCONBAL']  #���ʿ��ƽ��
        TradeContext.BALANCE  =  record_acckj['BALANCE']    #�˺�ʵ�ʽ�
        TradeContext.UNCONRST =  record_acckj['UNCONRST']   #��ش�����
        TradeContext.UNCONRST =  record_acckj['UNCONRST']   #����״̬
        TradeContext.PRCCO    = "RCCS1105"                  #������
        TradeContext.STRINFO  = "�ظ�����"                  #����
        
        #=====ֱ����AFE����ͨѶ��ִ====
        AfaLoggerFunc.tradeInfo("ֱ����AFE����ͨѶ��ִ")
        AfaAfeFunc.CommAfe()
        
        AfaLoggerFunc.tradeInfo("�ظ����ģ�����������")
        
        return AfaFlowControl.ExitThisFlow('A009','�ظ���������������')
##############���ظ�����#################################################################
    AfaLoggerFunc.tradeInfo("���ظ�����") 
    #=====��֯�ǼǴ��ʿ��ƽ�صǼǲ��Ĳ����ֵ�====
    AfaLoggerFunc.tradeInfo("��֯�ǼǴ��ʿ��ƽ�صǼǲ��Ĳ����ֵ�")
    insert_dict = {}
     
    insert_dict['TRCDAT']      = TradeContext.TRCDAT         #ί������ 
    insert_dict['BSPSQN']      = TradeContext.BSPSQN         #�������
    insert_dict['MSGFLGNO']    = TradeContext.MSGFLGNO       #���ı�ʶ��
    insert_dict['ORMFN']       = TradeContext.ORMFN          #�ο����ı�ʶ��
    insert_dict['TRCCO']       = TradeContext.TRCCO          #������
    insert_dict['BRSFLG']      = TradeContext.BRSFLG         #������ʶ  
    insert_dict['BESBNO']      = TradeContext.BESBNO         #������ 
    insert_dict['BEACSB']      = ""                          #���������
    insert_dict['BETELR']      = TradeContext.BETELR         #������Ա��
    insert_dict['BEAUUS']      = ""                          #��Ȩ��Ա��
    insert_dict['BEAUPS']      = ""                          #��Ȩ��Ա����
    insert_dict['TERMID']      = ""                          #�ն˺�
    insert_dict['OPTYPE']       = TradeContext.OPTYPE        #ҵ������
    insert_dict['NCCWKDAT']    = TradeContext.NCCWKDAT       #ũ������������
    insert_dict['TRCNO']       = TradeContext.TRCNO          #������ˮ��
    insert_dict['SNDMBRCO']    = TradeContext.SNDMBRCO       #���ͷ���Ա�к�
    insert_dict['RCVMBRCO']    = TradeContext.RCVMBRCO       #���ܳ�Ա���к�
    insert_dict['SNDBNKCO']    = TradeContext.SNDBNKCO       #���ͷ��к�
    insert_dict['SNDBNKNM']    = TradeContext.SNDBNKNM       #���ͷ�����
    insert_dict['RCVBNKCO']    = TradeContext.RCVBNKCO       #�����к�
    insert_dict['RCVBNKNM']    = TradeContext.RCVBNKNM       #��������
    insert_dict['ORTRCDAT']    = TradeContext.ORTRCDAT       #ԭί������
    insert_dict['ORTRCCO']     = TradeContext.ORTRCCO        #ԭ���״���
    insert_dict['ORTRCNO']     = TradeContext.ORTRCNO        #������ˮ��
    insert_dict['ORSNDSUBBNK'] = TradeContext.ORSNDSUBBNK    #ԭ�����Ա�к�
    insert_dict['ORSNDBNK']    = TradeContext.ORSNDBNK       #ԭ�����к�
    insert_dict['ORRCVSUBBNK'] = TradeContext.ORRCVSUBBNK    #ԭ���ܳ�Ա���к�
    insert_dict['ORRCVBNK']    = TradeContext.ORRCVBNK       #ԭ��������
    insert_dict['ORPYRACC']    = TradeContext.ORPYRACC       #ԭ�������˺�
    insert_dict['ORPYRNAM']    = TradeContext.ORPYRNAM       #ԭ����������
    insert_dict['ORPYEACC']    = TradeContext.ORPYEACC       #ԭ�տ����˺�
    insert_dict['ORPYENAM']    = TradeContext.ORPYENAM       #ԭ�տ�������
    insert_dict['CUR']         = '01'                        #����
    insert_dict['OCCAMT']      = TradeContext.OCCAMT         #ԭ���׽��
    insert_dict['CHRG']        = TradeContext.CHRG           #������
    insert_dict['ERRCONBAL']   = TradeContext.ERRCONBAL      #���ʿ��ƽ��
    if( TradeContext.existVariable( "BALANCE" ) ):
        insert_dict['BALANCE']     = TradeContext.BALANCE        #�˺�ʵ�ʽ��
    else:
        insert_dict['BALANCE'] = ""   
    if( TradeContext.existVariable( "UNCONRST" ) ):
        insert_dict['UNCONRST']    = TradeContext.UNCONRST       #��ش�����
    else:
        insert_dict['UNCONRST']= ""   
    if( TradeContext.existVariable( "CONSTS" ) ):
        insert_dict['CONSTS']      = TradeContext.CONSTS         #����״̬
    else:
        insert_dict['CONSTS']  = ""    
    
    if( TradeContext.existVariable( "PRCCO" ) ):
        insert_dict['PRCCO']       = TradeContext.PRCCO          #���ķ�����
    else:
        insert_dict['PRCCO']  =""   
    insert_dict['STRINFO']     = TradeContext.STRINFO           #����
    insert_dict['NOTE1']       = TradeContext.BJETIM            #ʱ��
    insert_dict['NOTE2']       = ""
    insert_dict['NOTE3']       = ""
    insert_dict['NOTE4']       = ""
    insert_dict['NOTE5']       = ""
    
    #=====�ǼǴ��ʿ��ƽ�صǼǲ�====
    AfaLoggerFunc.tradeInfo("��ʼ�ǼǴ��ʿ��ƽ�صǼǲ�")
    AfaLoggerFunc.tradeInfo(insert_dict)
    res = rccpsDBTrcc_acckj.insertCmt(insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','�ǼǴ��ʿ��ƽ�صǼǲ�ʧ��')
   
    #���˴��ʿ��ƴ���    
    if(TradeContext.TRCCO=='3000508'):     #��������˴��ʿ��ƿش��� �Ȳ�ѯԭ��Ҫ���ƵĴ����Ƿ���ڣ�����ҵ��Ҫ���Ƿ���ȷ
        #=====��֯��ѯ�ֵ�====                            
        AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ䣬�ж�ԭ��Ҫ���ʿ��Ƶļ�¼�Ƿ����")    
       
        wheresql_dic={}
        wheresql_dic['TRCDAT'] =TradeContext.ORTRCDAT   #ԭ��������
        wheresql_dic['SNDBNKCO']=TradeContext.ORSNDBNK  #ԭ�����к�
        wheresql_dic['TRCNO']=TradeContext.ORTRCNO      #ԭ������ˮ��
        
        #=====��ʼ��ѯ���ݿ�====
        records=rccpsDBTrcc_wtrbka.selectu(wheresql_dic)          #��ѯ���ʿ��ƽ�صǼǲ� 
        AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
        if(records==None):                                        
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
        elif(len(records)==0):
            records=rccpsDBTrcc_tddzmx.selectu(wheresql_dic)      #��ѯ���ʿ��ƽ�ض�����ϸ��Ϣ�Ǽǲ�
            AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
            if(records==None):
                return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
            elif(len(records)==0): 
                TradeContext.CONSTS  ='1' 
                TradeContext.STRINFO ='���ʿ���ʧ�ܣ��޴���ԭʼ��¼,�����������ݵ�Ҫ��'  
                hzAfe()                                                                   
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ��޴���ԭʼ��¼,�����������ݵ�Ҫ��")  
            else:
                
                ORTRCCO           = records['TRCCO']         #ԭ���״���         
                ORSNDSUBBNK       = records['SNDMBRCO']      #ԭ�����Ա�к�     
                ORRCVSUBBNK       = records['RCVMBRCO']      #ԭ���ճ�Ա�к�      
                ORRCVBNK          = records['RCVBNKCO']      #ԭ�����к�    
                ORPYRACC          = records['PYRACC']        #ԭ�������˺�  
                ORPYEACC          = records['PYEACC']        #ԭ�տ����˺�  
                OCCAMT            = str(records['OCCAMT'])   #ԭ���׽��
                OCCAMT            = str((long)(((float)(OCCAMT)) * 100 + 0.1))   #ȥ�����С���㣬���ڱȽ�ԭ���׽���Ƿ����
                CHRG              = str(records['CUSCHRG'])    #ԭ������
                CHRG              = str((long)(((float)(CHRG)) * 100 + 0.1))     #ȥ�����С���㣬���ڱȽ�ԭ�������Ƿ���� 
                PYRNAM            = records['PYRNAM'].strip()           #����������
                PYENAM            = records['PYENAM'].strip()           #�տ�������
                 
            
                if (ORTRCCO!=TradeContext.ORTRCCO): 
                    TradeContext.CONSTS  ='1'
                    TradeContext.STRINFO ='���ʿ���ʧ�ܣ�ԭ�����벻��'   
                    hzAfe()                                                                 
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�����벻��")
                         
                if (ORSNDSUBBNK!=TradeContext.ORSNDSUBBNK):     
                    TradeContext.CONSTS  ='1'    
                    TradeContext.STRINFO = '���ʿ���ʧ�ܣ�ԭ�����Ա�кŲ���'  
                    hzAfe()                                                                   
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�����Ա�кŲ���")  
                                                                                 
                if (ORRCVSUBBNK!=TradeContext.ORRCVSUBBNK):                       
                    TradeContext.CONSTS  ='1'    
                    TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ���ܳ�Ա�кŲ���'  
                    hzAfe()                                                                        
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ���ܳ�Ա�кŲ���") 
                    
                if (ORRCVBNK!=TradeContext.ORRCVBNK):                         
                    TradeContext.CONSTS  ='1'
                    TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ�����кŲ���'  
                    hzAfe()                                                                        
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�����кŲ���") 
                    
                if (ORPYRACC!=TradeContext.ORPYRACC):           
                    TradeContext.CONSTS  ='1' 
                    TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ�������˺Ų���'   
                    hzAfe()                                                                      
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�������˺Ų���") 
                
                if (PYRNAM!=TradeContext.ORPYRNAM.strip()):                            
                    TradeContext.CONSTS  ='1'                                    
                    TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ���������Ʋ���'                   
                    hzAfe()
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ���������Ʋ���")
                                                                          
                if (ORPYEACC!=TradeContext.ORPYEACC):             
                    TradeContext.CONSTS  ='1'                     
                    TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ�տ�����˺Ų���' 
                    hzAfe()                                                                     
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�տ�����˺Ų���")   
                
                if (PYENAM!=TradeContext.ORPYENAM.strip()):                            
                    TradeContext.CONSTS  ='1'                                    
                    TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ�տ������Ʋ���'                   
                    hzAfe()
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�տ������Ʋ���")
               
                if (OCCAMT!=TradeContext.OCCAMT):              
                    TradeContext.CONSTS  ='1'                      
                    TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ���׽���'  
                    hzAfe()                                                                          
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ���׽���")
                       
                if (CHRG!=TradeContext.CHRG):              
                    TradeContext.CONSTS  ='1'                  
                    TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ���������Ѳ���' 
                    hzAfe()                                                                     
                    return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ���������Ѳ���")  
        else:
            
            ORTRCCO           = records['TRCCO']           #ԭ���״���         
            ORSNDSUBBNK       = records['SNDMBRCO']        #ԭ�����Ա�к�     
            ORRCVSUBBNK       = records['RCVMBRCO']        #ԭ���ճ�Ա�к�      
            ORRCVBNK          = records['RCVBNKCO']        #ԭ�����к�    
            ORPYRACC          = records['PYRACC'].strip()  #ԭ�������˺�  
            ORPYEACC          = records['PYEACC'].strip()  #ԭ�տ����˺�  
            OCCAMT            = str(records['OCCAMT'])     #ԭ���׽��
            OCCAMT            = str((long)(((float)(OCCAMT)) * 100 + 0.1))   #ȥ�����С���㣬���ڱȽ�ԭ���׽���Ƿ����
            CHRG              = str(records['CUSCHRG'])    #ԭ������
            CHRG              = str((long)(((float)(CHRG)) * 100 + 0.1))     #ȥ�����С���㣬���ڱȽ�ԭ�������Ƿ����
            PYRNAM            = records['PYRNAM'].strip()           #����������
            PYENAM            = records['PYENAM'].strip()           #�տ�������
            
            AfaLoggerFunc.tradeInfo(CHRG)
            AfaLoggerFunc.tradeInfo(type(CHRG))
            AfaLoggerFunc.tradeInfo(type(TradeContext.CHRG))
            AfaLoggerFunc.tradeInfo("TradeContext.CHRG:" + TradeContext.CHRG) 
            
            if (ORTRCCO!=TradeContext.ORTRCCO):                              
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO ='���ʿ���ʧ�ܣ�ԭ�����벻��'  
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�����벻��")                       
                                                                        
            if (ORSNDSUBBNK!=TradeContext.ORSNDSUBBNK):                      
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO = '���ʿ���ʧ�ܣ�ԭ�����Ա�кŲ���'
                hzAfe()                
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�����Ա�кŲ���") 
                                                                            
            if (ORRCVSUBBNK!=TradeContext.ORRCVSUBBNK):                      
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ���ܳ�Ա�кŲ���'                 
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ���ܳ�Ա�кŲ���") 
                                                                             
            if (ORRCVBNK!=TradeContext.ORRCVBNK):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ�����кŲ���'    
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�����кŲ���")               
                                                                             
            if (ORPYRACC!=TradeContext.ORPYRACC.strip()):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ�������˺Ų���'                   
                AfaLoggerFunc.tradeInfo(ORPYRACC)
                AfaLoggerFunc.tradeInfo(TradeContext.ORPYRACC)
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�������˺Ų���")
            
            if (PYRNAM!=TradeContext.ORPYRNAM.strip()):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ���������Ʋ���'                   
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ���������Ʋ���")
                                                                             
            if (ORPYEACC!=TradeContext.ORPYEACC.strip()):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ�տ�����˺Ų���'                 
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�տ�����˺Ų���")
            
            if (PYENAM!=TradeContext.ORPYENAM.strip()):                            
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ�տ������Ʋ���'                   
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ�տ������Ʋ���")
            
            if (OCCAMT!=TradeContext.OCCAMT): 
                                              
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ���׽���'
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ���׽���")
                                                                             
            if (CHRG!=TradeContext.CHRG):                                    
                TradeContext.CONSTS  ='1'                                    
                TradeContext.STRINFO  = '���ʿ���ʧ�ܣ�ԭ���������Ѳ���' 
                hzAfe()
                return AfaFlowControl.ExitThisFlow('S999', "���ʿ���ʧ�ܣ�ԭ���������Ѳ���")  
                  
        #=====��֯��ѯ�ֵ�====                            
        AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ䣬�ж��Ƿ����ظ�����")    
       
        wheresql_dic={}
        wheresql_dic['ORTRCDAT'] =TradeContext.ORTRCDAT     #ԭ��������
        wheresql_dic['ORSNDBNK'] =TradeContext.ORSNDBNK     #ԭ�����к�
        wheresql_dic['ORTRCNO']  =TradeContext.ORTRCNO      #ԭ������ˮ��
        if (TradeContext.TRCCO=='3000508'):
            wheresql_dic['TRCCO']    ='3000508'
            wheresql_dic['CONSTS']   ='0'                       #���ʿ��Ƴɹ���ʶ             
        if (TradeContext.TRCCO=='3000509'):
            wheresql_dic['TRCCO']    ='3000509'
            wheresql_dic['UNCONRST'] ='0' 
            
        #=====��ʼ��ѯ���ݿ�====
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #��ѯ���ʿ��ƽ�صǼǲ� 
        AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')
        if(records==None):                                        
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
        if(len(records)>0):
            TradeContext.STRINFO  = '�ô����Ѿ����ƻ��Ѿ���أ������ظ�����' 
            hzAfe()
            return AfaFlowControl.ExitThisFlow('S999', "�ô����Ѿ����ƻ��أ������ظ�����")
        
        #=====================������ͨѶ��ѯ���======================================== 
        TradeContext.HostCode = '8810'
        if(len(TradeContext.ORPYEACC.strip())!=0):
            TradeContext.ACCNO    = TradeContext.ORPYEACC
        else:
            TradeContext.ACCNO    = TradeContext.ORPYRACC
        
        #tiger����
        if((TradeContext.ORTRCCO=='3000103')or(TradeContext.ORTRCCO=='3000105' )):
            AfaLoggerFunc.tradeInfo('tiger1111')
            TradeContext.ACCNO    = TradeContext.ORPYRACC
        
        AfaLoggerFunc.tradeInfo("test3" + TradeContext.ACCNO)
        
        rccpsHostFunc.CommHost('8810')
        
        #=====�ж����������Ƿ�ɹ�====   
        if( TradeContext.errorCode != '0000' ):  
            AfaLoggerFunc.tradeInfo("��������ʧ��")                                        
            TradeContext.CONSTS  ='1'                                                                               
            TradeContext.STRINFO  = "������ѯ���ʧ�� "+TradeContext.errorMsg[7:]+" "  #����
            hzAfe()                                                                      
            return AfaFlowControl.ExitThisFlow('S999', "������ѯ���ʧ��") 
        else:
            TradeContext.ACCBAL = HostContext.O1ACBL           #�ʻ����
            TradeContext.AVLBAL = HostContext.O1CUBL           #�������
            TradeContext.BALANCE  = TradeContext.AVLBAL        #ʵ�ʿ��ý��     
            AfaLoggerFunc.tradeInfo(HostContext.O1CUBL)
            
            if((float(TradeContext.AVLBAL)) < (float(TradeContext.ERRCONBAL))):    #�˺ſ��ý�����ʿ��ƽ�� 
                TradeContext.CONSTS  ='1'                 
                TradeContext.STRINFO  = '�˺ſ��ý�����ʿ��ƽ��' 
                TradeContext.BALANCE  = TradeContext.AVLBAL    #ʵ�ʿ��ý�� 
                hzAfe()                                                         
                return AfaFlowControl.ExitThisFlow('S999', "�˺ſ��ý�����ʿ��ƽ��")  
        
        #����0061�������ʿ��ƽ���
        TradeContext.HostCode = '0061'
        TradeContext.kjflag='0'                                 #���ʿ��Ʊ�ʶλ
        
    #���˴��ʽ�ش���                                                                                            
    if(TradeContext.TRCCO=='3000509'):     #��������˴��ʽ�� �Ȳ�ѯԭ��Ҫ��صĴ����Ƿ���ڣ��Ƿ��Ѿ����
        #=====��֯��ѯ�ֵ�====                                                                                       
        AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ�,��ԭ���ʿ��Ƽ�¼�Ƿ����")                                                               
                                                                                                                     
        wheresql_dic={}                                                                                              
        wheresql_dic['MSGFLGNO'] =TradeContext.ORMFN        #���ʿ��Ƶı��ı�ʶ��                                                 
        wheresql_dic['TRCCO']    ='3000508'                 #������  
        wheresql_dic['TRCDAT'] =TradeContext.ORTRCDAT       #ԭ��������
        wheresql_dic['SNDBNKCO'] =TradeContext.ORSNDBNK      #ԭ�����к�
        wheresql_dic['TRCNO']  =TradeContext.ORTRCNO        #ԭ������ˮ��
        wheresql_dic['CONSTS']   ='0'                                                                   
                                                                                                                     
        #=====��ʼ��ѯ���ݿ�====                                                                                     
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #��ѯ���ʿ��ƽ�صǼǲ�                             
        AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')                                                        
        if(records==None):                                                                                           
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )                                                   
        elif(len(records)==0):                                                                                       
            TradeContext.UNCONRST   ='1'                  
            TradeContext.STRINFO  = '���ʽ��ʧ�ܣ�ԭ���ʿ��Ƽ�¼������' 
            hzAfe()                                                                   
            return AfaFlowControl.ExitThisFlow('S999', "���ʽ��ʧ�ܣ�ԭ���ʿ��Ƽ�¼������")
        else:
            AfaLoggerFunc.tradeInfo("kkkkk"+records['ORTRCCO'] )
            if((records['ORTRCCO']=='3000103')or(records['ORTRCCO']=='3000105' )or(records['ORTRCCO']=='3000102')or(records['ORTRCCO']=='3000104')):
                AfaLoggerFunc.tradeInfo("yyyyyyyyyyyyyyyy")
                TradeContext.ACCNO     =   records['ORPYRACC']      #����˺�
            else: 
                AfaLoggerFunc.tradeInfo("XXXXXXXXXXXXXXXX")   
                TradeContext.ACCNO     =   records['ORPYEACC']      #����˺�
            AfaLoggerFunc.tradeInfo("fffffffff"+TradeContext.ACCNO )  
            TradeContext.ERRCONBAL    =   records['ERRCONBAL']     #��ؽ�� 
            
        AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ䣬���Ƿ����ظ����")  
        wheresql_dic={}                                                                                              
        wheresql_dic['TRCCO']      ='3000509'                 #������                                                 
        wheresql_dic['ORTRCDAT']   =TradeContext.ORTRCDAT     #ԭ��������
        wheresql_dic['ORSNDBNK']   =TradeContext.ORSNDBNK     #ԭ�����к�
        wheresql_dic['ORTRCNO']    =TradeContext.ORTRCNO      #ԭ������ˮ��
        wheresql_dic['UNCONRST']   ='0'  
        
        #=====��ʼ��ѯ���ݿ�====                                                                                     
        records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #��ѯ���ʿ��ƽ�صǼǲ�                             
        AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')                                                        
        if(records==None):                                                                                           
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )  
        if(len(records)>0):
            if (records['UNCONRST'] == '0'):           #���״̬
                TradeContext.UNCONSTS  ='0'                                   
                TradeContext.STRINFO  = '���ʽ��ʧ�ܣ�ԭ�����Ѿ����'
                hzAfe()                                                                            
                return AfaFlowControl.ExitThisFlow('S999', "���ʽ��ʧ�ܣ�ԭ�����Ѿ����")
        
        #TradeContext.ACCNO    = TradeContext.ORPYEACC              
        #����0061�������ʽ�ؽ���
        TradeContext.HostCode = '0061'
        TradeContext.kjflag='1'                                 #���ʿ��Ʊ�ʶλ

    AfaLoggerFunc.tradeInfo("����ǰ����(�Ǽ���ˮ,����ǰ����)  ����")
        
    return True    
 
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("�����д���(�޸���ˮ,��������,����ǰ����)")
    
    AfaLoggerFunc.tradeInfo("errorCode<<<<<<<<<<<"+TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo("errorMsg<<<<<<<<<<"+TradeContext.errorMsg)
    
    #=====�ж����������Ƿ�ɹ�====
    if( TradeContext.errorCode != '0000' ):
        AfaLoggerFunc.tradeInfo("��������ʧ��")
        
        TradeContext.PRCCO    = "NN1CA999"  #������
        TradeContext.STRINFO  = "����ʧ�� "+TradeContext.errorMsg[7:]+" "  #���� 
        
        #=====���´��ʿ��ƽ�صǼǲ�====
        AfaLoggerFunc.tradeInfo("��֯�����ֵ�")
        where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN}   #���ں�ƽ̨��ˮ��
        if (TradeContext.TRCCO=='3000508'):
            TradeContext.CONSTS='1'
            update_dict = {'CONSTS':TradeContext.CONSTS,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #������Ϣ�����ͷ�����  
        if (TradeContext.TRCCO=='3000509'):
            TradeContext.UNCONRST='1'   
            update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #������Ϣ�����ͷ�����  
        AfaLoggerFunc.tradeInfo("��ʼ���´��ʿ��ƽ�صǼǲ�")
        
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','���´��ʿ��ƽ�صǼǲ�ʧ��')
    else:
        AfaLoggerFunc.tradeInfo("�������׳ɹ�")
        #=====���´��ʿ��ƽ�صǼǲ�====
        AfaLoggerFunc.tradeInfo("��֯�����ֵ�")
        TradeContext.PRCCO = "RCCI0000"              #������
        
        if(TradeContext.TRCCO=='3000508'):
            TradeContext.CONSTS='0'
            TradeContext.STRINFO = "���ʿ��Ƴɹ�"  #����
            update_dict = {'BALANCE':TradeContext.BALANCE,'CONSTS':TradeContext.CONSTS,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO} 
        
        if(TradeContext.TRCCO=='3000509'):
            TradeContext.UNCONRST='0'
            TradeContext.STRINFO = "���ʽ�سɹ�"  #����
            update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}
        
        where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN}    #���ں���̨��ˮ��
                          
        AfaLoggerFunc.tradeInfo("��ʼ���´��ʿ��ƽ�صǼǲ�")
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','���´��ʿ��ƽ�صǼǲ�ʧ��')
            
    #=====��ʼ���ʿ��ƽ��Ӧ���ĸ�ֵ====
    AfaLoggerFunc.tradeInfo("��ʼ�������ʿ��ƽ��Ӧ���ĸ�ֵ")
    
    Rcvmbrco = TradeContext.SNDMBRCO    #�������к�
    Sndmbrco = TradeContext.RCVMBRCO    #�������к�
    Ormfn    = TradeContext.MSGFLGNO    #�ο����ı�ʶ��
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET010'  #���������
    TradeContext.RCVSTLBIN = Rcvmbrco #���ܷ���Ա�к�
    TradeContext.SNDSTLBIN = Sndmbrco #���ͷ���Ա�к�
    TradeContext.SNDBRHCO = TradeContext.BESBNO         #�����������
    TradeContext.SNDCLKNO = TradeContext.BETELR         #�����й�Ա��
    TradeContext.SNDTRDAT = TradeContext.TRCDAT         #�����н�������
    TradeContext.SNDTRTIM = TradeContext.BJETIM         #�����н���ʱ��
    TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.TRCDAT + TradeContext.SerialNo        #���ı�ʾ��
    TradeContext.ORMFN    = Ormfn                             #�ο����ı�ʾ��
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate          #���Ĺ�������
    TradeContext.OPRTYPNO = '30'     #ҵ������
    TradeContext.ROPRTPNO = '30'     #�ο�ҵ������
    TradeContext.TRANTYP  = '0'      #��������
    #=====ҵ��Ҫ�ؼ�====

        
    AfaLoggerFunc.tradeInfo("�����д���(�޸���ˮ,��������,����ǰ����)  ����")
    
    return True    
    
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo("���׺���")
    
    AfaLoggerFunc.tradeInfo("errorCode<<<<<<<<<<<"+TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo("errorMsg<<<<<<<<<<"+TradeContext.errorMsg)
    
    #=====�ж�afe���ؽ��====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>���ͳɹ�')
    else:
        AfaLoggerFunc.tradeInfo('>>>����ʧ��')

    AfaLoggerFunc.tradeInfo("���׺��� ����")
    
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�Ҵ��ʿ��ƽ�ؽ��ս���.���ʿ��ƽ�ز�ѯ[1165] �˳�")

    return True  


#������Ҫ�ز���ʱ��ũ��������ֱ�ӷ��ش�����Ϣ��������ֹ
def hzAfe():
    #=====��ʼ���ʿ��ƽ��Ӧ���ĸ�ֵ====
    AfaLoggerFunc.tradeInfo("��ʼ�������ʿ��ƽ��Ӧ���ĸ�ֵ")
    
    Rcvmbrco = TradeContext.SNDMBRCO    #�������к�
    Sndmbrco = TradeContext.RCVMBRCO    #�������к�
    Ormfn    = TradeContext.MSGFLGNO    #�ο�������ʾ��
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET010'  #���������
    TradeContext.RCVSTLBIN = Rcvmbrco #���ܷ���Ա�к�
    TradeContext.SNDSTLBIN = Sndmbrco #���ͷ���Ա�к�
    TradeContext.SNDBRHCO = TradeContext.BESBNO         #�����������
    TradeContext.SNDCLKNO = TradeContext.BETELR         #�����й�Ա��
    TradeContext.SNDTRDAT = TradeContext.TRCDAT         #�����н�������
    TradeContext.SNDTRTIM = TradeContext.BJETIM         #�����н���ʱ��
    TradeContext.MSGFLGNO = Rcvmbrco+TradeContext.TRCDAT + TradeContext.SerialNo        #���ı�ʾ��
    TradeContext.ORMFN    = Ormfn                             #�ο����ı�ʾ��
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate          #���Ĺ�������
    TradeContext.OPRTYPNO = '30'     #ҵ������
    TradeContext.ROPRTPNO = '30'     #�ο�ҵ������
    TradeContext.TRANTYP  = '0'      #��������        
    TradeContext.PRCCO    = "NN1CA999"  #������                                                                   
    
    #=====���´��ʿ��ƽ�صǼǲ�====
    AfaLoggerFunc.tradeInfo("��֯�����ֵ�")
    where_dict = {'TRCDAT':TradeContext.TRCDAT,'BSPSQN':TradeContext.BSPSQN}   #���ں�ƽ̨��ˮ��
    if (TradeContext.TRCCO=='3000508'):
        TradeContext.CONSTS='1'
        update_dict = {'CONSTS':TradeContext.CONSTS,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #������Ϣ�����ͷ�����  
    if (TradeContext.TRCCO=='3000509'):
        TradeContext.UNCONRST='1'   
        update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #������Ϣ�����ͷ�����  
    AfaLoggerFunc.tradeInfo("��ʼ���´��ʿ��ƽ�صǼǲ�")
    
    res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
    
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A009','���´��ʿ��ƽ�صǼǲ�ʧ��')
    #=====ֱ����AFE����ͨѶ��ִ====
    AfaLoggerFunc.tradeInfo("ֱ����AFE����ͨѶ��ִ")
    AfaAfeFunc.CommAfe()
