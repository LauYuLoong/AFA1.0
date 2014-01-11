# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.Ʊ�ݲ�ѯ�鸴�Ǽǲ���ѯ
#=================================================================
#   �����ļ�:   TRCC001_8532.py
#   �޸�ʱ��:   2008-06-08
#   ���ߣ�      �˹�ͨ
##################################################################
import os
import rccpsDBTrcc_pjcbka,rccpsDBTrcc_subbra,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8532]����***' )
    
    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
        
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[ENDDAT]������')
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
    
    if(len(TradeContext.PRTTYPE)==0):
        return AfaFlowControl.ExitThisFlow("S999", "��ӡ��־[PRTTYPE]������Ϊ��")  
    
    #=====��֯sql���====
    wheresql=""
    wheresql = wheresql + "BESBNO='" + TradeContext.BESBNO + "' "
    wheresql=wheresql+" and BJEDTE>='"+TradeContext.STRDAT+"'"
    wheresql=wheresql+" AND BJEDTE<='"+TradeContext.ENDDAT+"'"
    
    #=====�жϲ鸴��ʶ�Ƿ�Ϊ�ջ�Ϊ9-ȫ��====
    if(TradeContext.ISDEAL != "" and TradeContext.ISDEAL != "9"):
        wheresql=wheresql+" AND ISDEAL='"+TradeContext.ISDEAL+"'"
    
    #=====�ж�������ʶ�Ƿ�Ϊ��====
    if(TradeContext.BRSFLG!=""):
        wheresql=wheresql+" AND BRSFLG='"+TradeContext.BRSFLG+"'"
    
    #=====�жϽ��״����Ƿ�Ϊ��====
    if(TradeContext.TRCCO !="" ):
        wheresql=wheresql+" AND TRCCO='"+TradeContext.TRCCO+"'" #ҵ�����ͣ����״��룩
    
    start_no=TradeContext.RECSTRNO      #��ʼ����
    sel_size=10
    
    #=====��ѯ������====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ������ʧ��' )
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','��������������������¼' )
    
    #=====�жϴ�ӡ���� 0  ����ӡ====
    if(TradeContext.PRTTYPE=='0'):
        AfaLoggerFunc.tradeInfo(">>>���벻��ӡ����")
        
        #=====�жϲ�ѯ�鸴����Ƿ�Ϊ��====
        if(TradeContext.BSPSQN!="" ):
            wheresql=wheresql+" AND BSPSQN='"+TradeContext.BSPSQN+"'"  
            
        #=====��ѯ�ܼ�¼��====
        allcount=rccpsDBTrcc_pjcbka.count(wheresql)
        if(allcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','�����ܼ�¼��ʧ��' )
            
        #=====��ѯ���ݿ�====
        ordersql=" order by BJEDTE DESC,BSPSQN DESC"
        records=rccpsDBTrcc_pjcbka.selectm(start_no,sel_size,wheresql,ordersql)
        
        if records==None:
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
        if len(records)<=0:
            return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ�����' )        
        else:
            #=====�����ļ�====
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode   
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
                
            try:
                f=open(fpath+filename,"w") 
            except :
                AfaLoggerFunc.tradeInfo(">>>���ļ�ʧ��")
                return AfaFlowControl.ExitThisFlow('A099','���ļ�ʧ��' )
            filecontext=""
            
            #=====д�ļ�����====
            for i in range(0,len(records)):
                #=====�����ļ�����====
                AfaLoggerFunc.tradeDebug( "�����ļ����� ")
                filecontext=records[i]['BJEDTE']     + "|" \
                           +records[i]['BSPSQN']     + "|" \
                           +records[i]['BRSFLG']     + "|" \
                           +records[i]['BESBNO']     + "|" \
                           +records[i]['BETELR']     + "|" \
                           +records[i]['BEAUUS']     + "|" \
                           +records[i]['NCCWKDAT']   + "|" \
                           +records[i]['TRCCO']      + "|" \
                           +records[i]['TRCDAT']     + "|" \
                           +records[i]['TRCNO']      + "|" \
                           +records[i]['SNDBNKCO']   + "|" \
                           +records[i]['SNDBNKNM']   + "|" \
                           +records[i]['RCVBNKCO']   + "|" \
                           +records[i]['RCVBNKNM']   + "|" \
                           +records[i]['BOJEDT']     + "|" \
                           +records[i]['BOSPSQ']     + "|" \
                           +records[i]['ORTRCCO']    + "|" \
                           +records[i]['CONT']       + "|" \
                           +records[i]['ISDEAL']     + "|" \
                           +records[i]['BILDAT']     + "|" \
                           +records[i]['BILNO']      + "|" \
                           +records[i]['BILPNAM']    + "|" \
                           +records[i]['BILENDDT']   + "|" \
                           +str(records[i]['BILAMT'])+ "|" \
                           +records[i]['PYENAM']     + "|" \
                           +records[i]['HONBNKNM']   + "|" \
                           +records[i]['PRCCO']      + "|" \
                           +records[i]['STRINFO']    + "|"
                f.write(filecontext+"\n")
            f.close()
            
            #=====����ӿڸ�ֵ====
            TradeContext.PBDAFILE=filename              #�ļ���
            TradeContext.RECCOUNT=str(len(records))     #��ѯ����
            TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
            
    #=====��ӡ���� 1 ��ӡ====        
    elif(TradeContext.PRTTYPE=='1'):
        AfaLoggerFunc.tradeInfo(">>>�����ӡ����")
        
        #=====�жϲ�ѯ�鸴����Ƿ�Ϊ��====
        if(TradeContext.BSPSQN!="" ):
            wheresql=wheresql+" AND BSPSQN='"+TradeContext.BSPSQN+"'"           
        else:
            return AfaFlowControl.ExitThisFlow('A099','��ѯ�鸴���[BSPSQN]������Ϊ��' )
            
        #=====��ѯ���ݿ�====
        records = rccpsDBTrcc_pjcbka.selectm(TradeContext.RECSTRNO,10,wheresql,"")
        
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )        
        elif( len(records)<=0 ):
            return AfaFlowControl.ExitThisFlow('A099','δ���ҵ�����' )            
        else:
            #=====Ʊ�ݲ�ѯ��====
            if(TradeContext.TRCCO=='9900520'):                
                AfaLoggerFunc.tradeInfo(">>>ҵ������ΪƱ�ݲ�ѯ��")
                
                #=====Ʊ�ݲ�ѯ���ӡ��ʽ====
                txt = """\
                        
                        
                                 %(BESBNM)sƱ�ݲ�ѯ��
                                 
          |-----------------------------------------------------------------------------|
          | ��ѯ����:     | %(BJEDTE)s                                                    |
          |-----------------------------------------------------------------------------|
          | Ʊ�ݲ�ѯ���: | %(BSPSQN)s                                                | 
          |-----------------------------------------------------------------------------|
          | �������к�:   | %(SNDBNKCO)s                                                  |
          |-----------------------------------------------------------------------------|
          | �������к�:   | %(RCVBNKCO)s                                                  |
          |-----------------------------------------------------------------------------|
          | Ʊ������:     | %(BILDAT)s                                                    |
          |-----------------------------------------------------------------------------|
          | Ʊ�ݵ�����:   | %(BILENDDT)s                                                    |
          |-----------------------------------------------------------------------------|
          | Ʊ�ݺ���:     | %(BILNO)s                                            |
          |-----------------------------------------------------------------------------|
          | ��Ʊ������:   | %(BILPNAM)s|                                                
          |-----------------------------------------------------------------------------|
          | ����������:   | %(HONBNKNM)s|                                               
          |-----------------------------------------------------------------------------|
          | ��ѯ����:     |                                                             |
          |-----------------------------------------------------------------------------|
          |                                                                             |
          |   %(CONT1)s      |                                                          
          |                                                                             |
          |   %(CONT2)s    |                                                            
          |                                                                             |
          |   %(CONT3)s    |                                                            
          |                                                                             |
          |   %(CONT4)s    |                                                            
          |                                                                             |
          |-----------------------------------------------------------------------------|
          ��ӡ����: %(BJEDTE)s      ��Ȩ:                       ����:
                """
                
                #====д�ļ�����====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8532'
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BILDAT':(records[0]['BILDAT']).ljust(8,' '),\
                                         'BILENDDT':(records[0]['BILENDDT']).ljust(8,' '),\
                                         'BILNO':(records[0]['BILNO']).ljust(16,' '),\
                                         'BILPNAM':(records[0]['BILPNAM']).ljust(60,' '),\
                                         'HONBNKNM':(records[0]['HONBNKNM']).ljust(60,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���
                
                AfaLoggerFunc.tradeDebug("�������ɴ�ӡ�ı�")
            #=====Ʊ�ݲ鸴��====
            elif(TradeContext.TRCCO=='9900521'):               
                AfaLoggerFunc.tradeInfo(">>>ҵ������ΪƱ�ݲ鸴��")
                
                #=====��ѯԭ������Ϣ====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                
                ret=rccpsDBTrcc_pjcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','��ѯԭ��Ϣʧ��' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','δ����ԭ��Ϣ' )
                
                #=====Ʊ�ݲ鸴���ӡ��ʽ====
                txt = """\
                        
                        
                                       %(BESBNM)sƱ�ݲ鸴��
                                  
           |---------------------------------------------------------------------------------------|
           | �鸴����:               | %(BJEDTE)s                                                    |
           |---------------------------------------------------------------------------------------|
           | Ʊ�ݲ鸴���:           | %(BSPSQN)s                                                |
           |---------------------------------------------------------------------------------------|
           | �������к�:             | %(SNDBNKCO)s                                                  |
           |---------------------------------------------------------------------------------------|
           | �������к�:             | %(RCVBNKCO)s                                                  |
           |---------------------------------------------------------------------------------------|
           | Ʊ������:               | %(BILDAT)s                                                    |
           |---------------------------------------------------------------------------------------|
           | Ʊ�ݵ�����:             | %(BILENDDT)s                                                    |
           |---------------------------------------------------------------------------------------|
           | Ʊ�ݺ���:               | %(BILNO)s                                            |
           |---------------------------------------------------------------------------------------|
           | ��Ʊ������:             | %(BILPNAM)s|                               
           |---------------------------------------------------------------------------------------|
           | �տ�������:             | %(PYENAM)s|                                
           |---------------------------------------------------------------------------------------|
           | ����������:             | %(HONBNKNM)s|                              
           |---------------------------------------------------------------------------------------|
           | ԭƱ�ݲ�ѯ����:         | %(BOJEDT)s                                                    |
           |---------------------------------------------------------------------------------------|
           | ԭƱ�ݲ�ѯ�������к�:   | %(ORSNDBNKCO)s                                                  |
           |---------------------------------------------------------------------------------------|
           | ԭƱ�ݲ�ѯ���:         | %(BOSPSQ)s                                                |
           |---------------------------------------------------------------------------------------|
           | �鸴����:               |                                                             |
           |---------------------------------------------------------------------------------------|
           |                                                                                       |
           |        %(CONT1)s           |                                            
           |                                                                                       |
           |        %(CONT2)s         |                                              
           |                                                                                       |
           |        %(CONT3)s         |                                              
           |                                                                                       |
           |        %(CONT4)s         |                                              
           |                                                                                       |
           |---------------------------------------------------------------------------------------|
           ��ӡ����: %(BJEDTE)s      ��Ȩ:                       ����:
                """
                
                #====д�ļ�����====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8532'
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BILDAT':(records[0]['BILDAT']).ljust(8,' '),\
                                         'BILENDDT':(records[0]['BILENDDT']).ljust(8,' '),\
                                         'BILNO':(records[0]['BILNO']).ljust(16,' '),\
                                         'BILPNAM':(records[0]['BILPNAM']).ljust(60,' '),\
                                         'PYENAM':(records[0]['PYENAM']).ljust(60,' '),\
                                         'HONBNKNM':(records[0]['HONBNKNM']).ljust(60,' '),\
                                         'BOJEDT':(records[0]['BOJEDT']).ljust(8,' '),\
                                         'ORSNDBNKCO':(ret['SNDBNKCO']).ljust(10,' '),\
                                         'BOSPSQ':(records[0]['BOSPSQ']).ljust(12,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���
                
                AfaLoggerFunc.tradeDebug("�������ɴ�ӡ�ı�")                            
            else:
                return AfaFlowControl.ExitThisFlow("S999", "ҵ�����ͷǷ�")   
    
        TradeContext.RECCOUNT='1'           #��ѯ����
        TradeContext.RECALLCOUNT='1'        #�ܱ���
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
      
    else:
        return AfaFlowControl.ExitThisFlow("S999", "��ӡ��־�Ƿ�")  

    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
                
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8532]�˳�***' )
    return True
