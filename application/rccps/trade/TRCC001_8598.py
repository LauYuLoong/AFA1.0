# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز���).���ʿ��ƽ�����Ϣ������ѯ  ���潻��
#===============================================================================
#   ģ���ļ�:   TRCC001_8598.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ����̩
#   �޸�ʱ��:   2011-05-23
################################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,TradeFunc,os,AfaFunc,rccpsDBTrcc_acckj,rccpsHostFunc,rccpsGetFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka,rccpsDBTrcc_tddzmx

def SubModuleDoFst():    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������(1.���ز���).���ʿ��ƽ�����Ϣ������ѯ[TRCC001_8596]����***' )
    
    #=====��Ҫ�Լ��====
    #=====�ж�����ӿ��Ƿ����====
    TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )
    TradeContext.TRCDAT=TradeContext.BJEDTE
    #��ȡ��ˮ��
    seqName="RCC_SEQ"
    sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
    TradeContext.TRCNO=str( records[0][0] ).rjust( 8, '0' )
    
    if( not TradeContext.existVariable( "ORTRCDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', 'ԭί������[ORTRCDAT]������')
        
    if( not TradeContext.existVariable( "ORSNDBNK" ) ):
        return AfaFlowControl.ExitThisFlow('A099', 'ԭ�����к�[ORSNDBNK]������')
        
    if( not TradeContext.existVariable( "ORTRCNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', 'ԭ������ˮ��[ORTRCNO]������')
    
   
    #=====��֯��ѯ�ֵ�====                                                                                                                                                       
    AfaLoggerFunc.tradeInfo(">>>��ʼ��֯��ѯ�ֵ�")                                                                                                                               
                                                                                                                                                                                 
    wheresql_dic={}                                                                                                                                                              
    wheresql_dic['TRCDAT']   =TradeContext.ORTRCDAT                                                                                                                                
    wheresql_dic['SNDBNKCO'] =TradeContext.ORSNDBNK                                                                                                                               
    wheresql_dic['TRCNO']    =TradeContext.ORTRCNO                                                                                                                                   
    wheresql_dic['TRCCO']    ='3000508'                 #������                                                                                                                  
    wheresql_dic['CONSTS']   ='0'                                                                                                                                                
                                                                                                                                                                                 
    #=====��ʼ��ѯ���ݿ�====                                                                                                                                                     
    records=rccpsDBTrcc_acckj.selectu(wheresql_dic)          #��ѯ���ʿ��ƽ�صǼǲ�                                                                                             
    AfaLoggerFunc.tradeDebug('>>>��¼['+str(records)+']')                                                                                                                        
    if(records==None):                                                                                                                                                           
        return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )                                                                                                                   
    elif(len(records)==0):                                                                                                                                                       
        TradeContext.UNCONRST   ='1'                                                                                                                                             
        TradeContext.STRINFO  = '���ʽ��ʧ�ܣ�ԭ���ʿ��Ƽ�¼������'                                                                                                             
        return AfaFlowControl.ExitThisFlow('S999', "���ʽ��ʧ�ܣ�ԭ���ʿ��Ƽ�¼������")                                                                                         
    else:                                                                                                                                                                        
        if((records['ORTRCCO']=='3000103')or(records['ORTRCCO']=='3000105' )or(records['ORTRCCO']=='3000102')or(records['ORTRCCO']=='3000104')):                                 
            TradeContext.ACCNO     =   records['ORPYRACC']      #����˺� 
            TradeContext.ACCNONAME =   records['ORPYRNAM']      #����                                                                                             
        else:                                                                                                                                                                    
            TradeContext.ACCNO     =   records['ORPYEACC']      #����˺�
            TradeContext.ACCNONAME =   records['ORPYENAM']      #����                                                                                                   
        TradeContext.ERRCONBAL     =   records['ERRCONBAL']     #��ؽ��
        TradeContext.ORMFN         =   records['MSGFLGNO']      #�ο����ı�ʶ��
        TradeContext.BETELR        =   records['BETELR']        #��Ա��                                                                                        
        TradeContext.BESBNO        =   records['BESBNO']        #������
        #TradeContext.NCCWKDAT      =   records['NCCWKDAT'] 
        TradeContext.SNDMBRCO      =   records['SNDMBRCO']      #���ͷ���Ա�к�
        TradeContext.RCVMBRCO      =   records['RCVMBRCO']      #���ܳ�Ա���к�
        TradeContext.SNDBNKCO      =   records['SNDBNKCO']      
        TradeContext.SNDBNKNM      =   records['SNDBNKNM'] 
        TradeContext.RCVBNKCO      =   records['RCVBNKCO']
        TradeContext.RCVBNKNM      =   records['RCVBNKNM']
        TradeContext.AMOUNT        =   str(records['ERRCONBAL'])
       
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
            return AfaFlowControl.ExitThisFlow('S999', "���ʽ��ʧ�ܣ�ԭ�����Ѿ����")             
                                                                                                   
    #=====��֯�ǼǴ��ʿ��ƽ�صǼǲ��Ĳ����ֵ�====                                                 
    AfaLoggerFunc.tradeInfo("��֯�ǼǴ��ʿ��ƽ�صǼǲ��Ĳ����ֵ�")                                
    insert_dict = {}                                                                               
                                                                                                   
    insert_dict['TRCDAT']      = TradeContext.BJEDTE          #ί������                             
    insert_dict['BSPSQN']      = '0'                          #�������                             
    insert_dict['MSGFLGNO']    = '1'                          #���ı�ʶ��                           
    insert_dict['ORMFN']       = TradeContext.ORMFN           #�ο����ı�ʶ��                       
    insert_dict['TRCCO']       = '3000509'                    #������                               
    insert_dict['BRSFLG']      = '0'                          #������ʶ                             
    insert_dict['BESBNO']      = TradeContext.BESBNO          #������                               
    insert_dict['BEACSB']      = ""                           #���������                           
    insert_dict['BETELR']      = TradeContext.BETELR          #������Ա��                           
    insert_dict['BEAUUS']      = ""                          #��Ȩ��Ա��                           
    insert_dict['BEAUPS']      = ""                          #��Ȩ��Ա����                         
    insert_dict['TERMID']      = ""                          #�ն˺�                               
    insert_dict['OPTYPE']       =''                          #ҵ������                             
    insert_dict['NCCWKDAT']    = TradeContext.BJEDTE         #ũ������������                       
    insert_dict['TRCNO']       = TradeContext.TRCNO          #������ˮ��                           
    insert_dict['SNDMBRCO']    = TradeContext.SNDMBRCO       #���ͷ���Ա�к�                       
    insert_dict['RCVMBRCO']    = TradeContext.RCVMBRCO       #���ܳ�Ա���к�                       
    insert_dict['SNDBNKCO']    = TradeContext.SNDBNKCO       #���ͷ��к�
    insert_dict['SNDBNKNM']    = TradeContext.SNDBNKNM       #���ͷ�����
    insert_dict['RCVBNKCO']    = TradeContext.RCVBNKCO       #�����к�
    insert_dict['RCVBNKNM']    = TradeContext.RCVBNKNM       #��������                          
    insert_dict['ORTRCDAT']    = TradeContext.ORTRCDAT       #ԭί������                           
    insert_dict['ORTRCCO']     = '3000508'                   #ԭ���״���                           
    insert_dict['ORTRCNO']     = TradeContext.ORTRCNO        #������ˮ��                           
    insert_dict['ORSNDSUBBNK'] = ''                          #ԭ�����Ա�к�                       
    insert_dict['ORSNDBNK']    = TradeContext.ORSNDBNK       #ԭ�����к�                           
    insert_dict['ORRCVSUBBNK'] = ''                          #ԭ���ܳ�Ա���к�                     
    insert_dict['ORRCVBNK']    = ''                          #ԭ��������                           
    insert_dict['ORPYRACC']    = ''                          #ԭ�������˺�                         
    insert_dict['ORPYRNAM']    = ''                          #ԭ����������                         
    insert_dict['ORPYEACC']    = ''                          #ԭ�տ����˺�                         
    insert_dict['ORPYENAM']    = ''                          #ԭ�տ�������                         
    insert_dict['CUR']         = '01'                        #����                                 
    insert_dict['OCCAMT']      = '0'                         #ԭ���׽��                           
    insert_dict['CHRG']        = '0'                         #������                               
    insert_dict['ERRCONBAL']   = TradeContext.ERRCONBAL      #���ʿ��ƽ��                         
    insert_dict['BALANCE'] = ""                                                                
    insert_dict['UNCONRST']= ""                                                            
    insert_dict['CONSTS']  = ""                                                            
    insert_dict['PRCCO']  =""                                                              
    insert_dict['STRINFO']     = ''           #����                          
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
        TradeContext.BETELR        =   records['BETELR']        #��Ա��
     
     
     #=====================������ͨѶ���д��ʽ��======================================== 
    #TradeContext.BESBNO='3401010079'
    #TradeContext.BETELR ='007907'
    #TradeContext.TERMID='1234567890'  
    TradeContext.kjflag='1'                                 #���ʿ��Ʊ�ʶλ
    TradeContext.HostCode = '0061'
    rccpsHostFunc.CommHost('0061')   
    
    AfaLoggerFunc.tradeInfo("�����д���(�޸���ˮ,��������)")
    
    AfaLoggerFunc.tradeInfo("errorCode<<<<<<<<<<<"+TradeContext.errorCode)
    AfaLoggerFunc.tradeInfo("errorMsg<<<<<<<<<<"+TradeContext.errorMsg)
    
    #=====�ж����������Ƿ�ɹ�====
    if( TradeContext.errorCode != '0000' ):
        AfaLoggerFunc.tradeInfo("��������ʧ��")
        
        TradeContext.PRCCO    = "NN1CA999"  #������
        TradeContext.STRINFO  = "����ʧ�� "+TradeContext.errorMsg[7:]+" "  #���� 
        TradeContext.UNCONRST='1'
        
        #=====���´��ʿ��ƽ�صǼǲ�====
        AfaLoggerFunc.tradeInfo("��֯�����ֵ�")
        where_dict = {'ORTRCDAT':TradeContext.ORTRCDAT,'ORSNDBNK':TradeContext.ORSNDBNK,'ORTRCNO':TradeContext.ORTRCNO,'TRCCO':'3000509','TRCNO':TradeContext.TRCNO}   #ԭί�����ڣ�ԭ�����кţ�ԭ������ˮ��
        update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #������Ϣ�����ͷ�����  

        AfaLoggerFunc.tradeInfo("��ʼ���´��ʿ��ƽ�صǼǲ�")
        
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','���´��ʿ��ƽ�صǼǲ�ʧ��')
        AfaLoggerFunc.tradeInfo(res)   
    else:
        AfaLoggerFunc.tradeInfo("�������׳ɹ�")
        #=====���´��ʿ��ƽ�صǼǲ�====
        AfaLoggerFunc.tradeInfo("��֯�����ֵ�")
        TradeContext.PRCCO = "RCCI0000"              #������
        TradeContext.UNCONRST='0'
        TradeContext.STRINFO = "���ʽ�سɹ�"  #����
        
        where_dict = {'ORTRCDAT':TradeContext.ORTRCDAT,'ORSNDBNK':TradeContext.ORSNDBNK,'ORTRCNO':TradeContext.ORTRCNO,'TRCCO':'3000509','TRCNO':TradeContext.TRCNO}   #ԭί�����ڣ�ԭ�����кţ�ԭ������ˮ��
        update_dict = {'UNCONRST':TradeContext.UNCONRST,'STRINFO':TradeContext.STRINFO,'PRCCO':TradeContext.PRCCO}  #������Ϣ�����ͷ�����  

        AfaLoggerFunc.tradeInfo("��ʼ���´��ʿ��ƽ�صǼǲ�")
        res = rccpsDBTrcc_acckj.updateCmt(update_dict,where_dict)
        
        if( res == -1 ):
            return AfaFlowControl.ExitThisFlow('A009','���´��ʿ��ƽ�صǼǲ�ʧ��')
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���)���ʿ��ƽ�ؽ�����Ϣ������ѯ[TRCC001_8598]�˳�***')
    return True                                                              