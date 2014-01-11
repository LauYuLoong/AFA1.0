# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.���ҵ���ѯ�������ɸ�ʽ�ǼǱ���ѯ
#=================================================================
#   �����ļ�:   TRCC001_8531.py
#   �޸�ʱ��:   2008-06-06
#   ���ߣ�      �˹�ͨ
##################################################################
import os
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_trcbka,rccpsDBTrcc_subbra,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8531]����***' )
    
    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099','��ʼ����[STRDAT]������' )
    
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099','��ֹ����[ENDDAT]������' ) 
    
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099','��ʼ����[RECSTRNO]������' )

    #=====���ɲ�ѯ���====
    wheresql=""
    wheresql = wheresql + "BESBNO='"        + TradeContext.BESBNO + "' " 
    wheresql=wheresql   + " AND BJEDTE>='"  + TradeContext.STRDAT + "'"
    wheresql=wheresql   + " AND BJEDTE<='"  + TradeContext.ENDDAT + "'"
    
    #=====�жϽ��״����Ƿ�Ϊ��====
    if(TradeContext.TRCCO != ""):
        wheresql = wheresql + " AND TRCCO='"  + TradeContext.TRCCO   + "'"
        
    #=====�ж�������ʶ�Ƿ�Ϊ��====
    if(TradeContext.BRSFLG != ""):
        wheresql = wheresql + " AND BRSFLG='" + TradeContext.BRSFLG  + "'"

    #=====�жϲ鸴��ʶ�Ƿ�Ϊ�ջ���9-ȫ��====        
    if(TradeContext.ISDEAL != "9" and TradeContext.ISDEAL!=""):
        wheresql = wheresql + " AND ISDEAL='" + TradeContext.ISDEAL  + "'"
        
    AfaLoggerFunc.tradeDebug(">>>���ɲ�ѯ���sql="+wheresql)

    #=====��ѯ������====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ������ʧ��' )        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','û����Ӧ�Ļ�����' )
    
    #=====�жϴ�ӡ����====
    #=====0 ����ӡ====
    if TradeContext.PRTTYPE=='0':
        AfaLoggerFunc.tradeInfo(">>>���벻��ӡ����")
        #=====�жϱ�������Ƿ�Ϊ��====
        if(TradeContext.BSPSQN!=""):    
            wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN  + "'"
        
        #=====�õ��ܼ�¼��====
        allcount=rccpsDBTrcc_hdcbka.count(wheresql)

        if(allcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','�����ܼ�¼��ʧ��' )
        
        #=====��ѯ���ݿ�====
        ordersql=" order by BJEDTE DESC,BSPSQN DESC"
        records=rccpsDBTrcc_hdcbka.selectm(TradeContext.RECSTRNO,10,wheresql,ordersql)
        
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )        
        elif( len(records)<=0 ):
            return AfaFlowControl.ExitThisFlow('A099','δ���ҵ�����' )        
        else:
            #=====�����ļ�====
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
            
            if(f==None):
                return AfaFlowControl.ExitThisFlow('A099','���ļ�ʧ��' )

            filecontext=""           
            #=====д�ļ�����====
            for i in range(0,len(records)):
                filecontext=records[i]['BJEDTE']  + "|" \
                           +records[i]['BSPSQN']  + "|" \
                           +records[i]['BRSFLG']  + "|" \
                           +records[i]['BESBNO']  + "|" \
                           +records[i]['BETELR']  + "|" \
                           +records[i]['BEAUUS']  + "|" \
                           +records[i]['NCCWKDAT']+ "|" \
                           +records[i]['TRCCO']   + "|" \
                           +records[i]['TRCDAT']  + "|" \
                           +records[i]['TRCNO']   + "|" \
                           +records[i]['SNDBNKCO']+ "|" \
                           +records[i]['SNDBNKNM']+ "|" \
                           +records[i]['RCVBNKCO']+ "|" \
                           +records[i]['RCVBNKNM']+ "|" \
                           +records[i]['BOJEDT']  + "|" \
                           +records[i]['BOSPSQ']  + "|" \
                           +records[i]['ORTRCCO'] + "|" \
                           +records[i]['CONT']    + "|" \
                           +records[i]['ISDEAL']  + "|" \
                           +records[i]['CUR']     + "|" \
                           +str(records[i]['OCCAMT'])+ "|" \
                           +records[i]['PYRACC']  + "|" \
                           +records[i]['PYEACC']  + "|" \
                           +records[i]['PRCCO']   + "|" \
                           +records[i]['STRINFO'] + "|" \
                           +records[i]['PYRNAM']  + "|" \
                           +records[i]['PYENAM']  + "|" 
                f.write(filecontext+"\n")
            AfaLoggerFunc.tradeInfo("�����ļ�����")
            f.close()
            
            #=====����ӿڸ�ֵ====
            TradeContext.RECCOUNT=str(len(records))     #��ѯ����
            TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
            TradeContext.PBDAFILE=filename              #�ļ���
            TradeContext.errorCode="0000"
            TradeContext.errorMsg="��ѯ�ɹ�"
    #=====1 ��ӡ====
    elif TradeContext.PRTTYPE=='1':
        #=====�жϱ�������Ƿ�Ϊ��====
        if(TradeContext.BSPSQN!=""):    
            wheresql = wheresql + " AND BSPSQN='" + TradeContext.BSPSQN  + "'"
        else:
            return AfaFlowControl.ExitThisFlow('S999','�������[BSPSQN]������Ϊ��' )
            
        #=====��ѯ���ݿ�====
        records=rccpsDBTrcc_hdcbka.selectm(TradeContext.RECSTRNO,10,wheresql,"")
        
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )        
        elif( len(records)<=0 ):
            return AfaFlowControl.ExitThisFlow('A099','δ���ҵ�����' )        
        else:
            #=====��ѯ��====
            if(TradeContext.TRCCO=='9900511'):                
                AfaLoggerFunc.tradeInfo(">>>ҵ������Ϊ��ѯ��")
                
                #=====��ѯԭ������Ϣ====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                
                ret=rccpsDBTrcc_trcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','��ѯԭ��Ϣʧ��' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','δ����ԭ��Ϣ' )
                    
                AfaLoggerFunc.tradeDebug(">>>��ʼ���ɲ�ѯ���ӡ�ı�")
                
                #=====��ѯ���ӡ��ʽ====
                txt="""\
                
                                           %(BESBNM)s���ӻ�Ҳ�ѯ��
                               
                |-----------------------------------------------------------------------------|
                | ��ѯ����:     |      %(BJEDTE)s                                               |
                |-----------------------------------------------------------------------------|
                | ��ѯ���:     |      %(BSPSQN)s                                           |
                |-----------------------------------------------------------------------------|
                | �������к�:   |      %(SNDBNKCO)s                                             |
                |-----------------------------------------------------------------------------|
                | �������к�:   |      %(RCVBNKCO)s                                             |
                |-----------------------------------------------------------------------------|
                | ԭ���׽��:   |      %(OROCCAMT)-15.2f                                        |
                |-----------------------------------------------------------------------------|
                | ԭ�������к�: |      %(ORSNDBNKCO)s                                             |
                |-----------------------------------------------------------------------------|
                | ԭ�������к�: |      %(ORRCVBNKCO)s                                             |
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
                
                #=====д�ļ�����====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'    
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "�����ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'OROCCAMT':(records[0]['OCCAMT']),\
                                         'ORSNDBNKCO':(ret['SNDBNKCO']).ljust(10,' '),\
                                         'ORRCVBNKCO':(ret['RCVBNKCO']).ljust(10,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���
                
                AfaLoggerFunc.tradeDebug(">>>�������ɴ�ӡ�ı�")            
            #=====�鸴��====
            elif(TradeContext.TRCCO=='9900512'):
                AfaLoggerFunc.tradeInfo(">>>ҵ������Ϊ�鸴��")
                
                #=====��ѯԭ������Ϣ====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                    
                ret=rccpsDBTrcc_hdcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','��ѯԭ��Ϣʧ��' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','δ����ԭ��Ϣ' )

                #=====�鸴���ӡ��ʽ====
                txt="""\
                
                                            %(BESBNM)s���ӻ�Ҳ鸴��
                                           
                    |-----------------------------------------------------------------------------|
                    | �鸴����:     |      %(BJEDTE)s                                               |
                    |-----------------------------------------------------------------------------|
                    | �鸴���:     |      %(BSPSQN)s                                           |
                    |-----------------------------------------------------------------------------|
                    | �������к�:   |      %(RCVBNKCO)s                                             |
                    |-----------------------------------------------------------------------------|
                    | ԭ��ѯ����:   |      %(BOJEDT)s                                               |
                    |-----------------------------------------------------------------------------|
                    | ԭ��ѯ���:   |      %(BOSPSQ)s                                           |
                    |-----------------------------------------------------------------------------|
                    | ԭ���:       |      %(OROCCAMT)-15.2f                                        |
                    |-----------------------------------------------------------------------------|
                    | ԭ����:       |      �����                                                 |
                    |-----------------------------------------------------------------------------|
                    | �鸴����:     |                                                             |
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
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'                
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "�����ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BOJEDT':(records[0]['BOJEDT']).ljust(8,' '),\
                                         'BOSPSQ':(records[0]['BOSPSQ']).ljust(12,' '),\
                                         'OROCCAMT':(ret['OCCAMT']),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name   #�ļ���
                
                AfaLoggerFunc.tradeDebug("�������ɴ�ӡ�ı�")
            #=====���ɸ�ʽ��====
            elif(TradeContext.TRCCO=='9900513'):            
                AfaLoggerFunc.tradeInfo(">>>ҵ������Ϊ���ɸ�ʽ��")
                
                #=====���ɸ�ʽ���ӡ��ʽ====
                txt="""\
                 
                                            %(BESBNM)s���ɸ�ʽ��
                                           
                    |-----------------------------------------------------------------------------|
                    | ����:          |      %(BJEDTE)s                                              |
                    |-----------------------------------------------------------------------------|
                    | ���ɸ�ʽ���:  |      %(BSPSQN)s                                          |
                    |-----------------------------------------------------------------------------|
                    | �������к�:    |      %(SNDBNKCO)s                                            |
                    |-----------------------------------------------------------------------------|
                    | �������к�:    |      %(RCVBNKCO)s                                            |
                    |-----------------------------------------------------------------------------|
                    | ����:          |                                                            |
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
                
                #=====д�ļ�����====            
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'    
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "�����ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���
                
                AfaLoggerFunc.tradeDebug("�������ɴ�ӡ�ı�")
            #=====��Լ��Ҳ�ѯ��====
            elif(TradeContext.TRCCO=='9900522'):
                AfaLoggerFunc.tradeInfo(">>>ҵ������Ϊ��Լ��Ҳ�ѯ��")
                
                #=====��ѯԭ������Ϣ====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                    
                ret=rccpsDBTrcc_trcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','��ѯԭ��Ϣʧ��' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','δ����ԭ��Ϣ' )
  
                #=====��Լ���ӻ�Ҳ�ѯ���ӡ��ʽ====
                txt="""\
                            
                                      %(BESBNM)sȫ����Լ���ӻ�Ҳ�ѯ��
                                           
                    |-----------------------------------------------------------------------------|
                    | ��ѯ����:         |      %(BJEDTE)s                                           |
                    |-----------------------------------------------------------------------------|
                    | ��Լ��Ҳ�ѯ���: |      %(BSPSQN)s                                       |
                    |-----------------------------------------------------------------------------|
                    | �������к�:       |      %(SNDBNKCO)s                                         |
                    |-----------------------------------------------------------------------------|
                    | �������к�:       |      %(RCVBNKCO)s                                         |
                    |-----------------------------------------------------------------------------|  
                    | ԭ������:         |      %(BOSPSQ)s                                       |
                    |-----------------------------------------------------------------------------|  
                    | ԭ���:           |      %(OROCCAMT)-15.2f                                    |
                    |-----------------------------------------------------------------------------|
                    | ԭί������:       |      %(ORTRCDAT)s                                           |
                    |-----------------------------------------------------------------------------|
                    | ԭ�������к�:     |      %(ORSNDBNKCO)s                                         |
                    |-----------------------------------------------------------------------------|
                    | ��ѯ����:         |                                                         |
                    |-----------------------------------------------------------------------------|
                    |                                                                             |
                    |     %(CONT1)s    |
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
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BOSPSQ':(records[0]['BOSPSQ']).ljust(10,' '),\
                                         'OROCCAMT':(ret['OCCAMT']),\
                                         'ORTRCDAT':(ret['TRCDAT']).ljust(8,' '),\
                                         'ORSNDBNKCO':(ret['SNDBNKCO']).ljust(10,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���
                
                AfaLoggerFunc.tradeDebug("�������ɴ�ӡ�ı�")
            #=====��Լ��Ҳ鸴��====
            elif(TradeContext.TRCCO=='9900523'):                
                AfaLoggerFunc.tradeInfo(">>>ҵ������Ϊ��Լ��Ҳ鸴��")
                
                #=====��ѯԭ������Ϣ====
                where_dict={'BJEDTE':records[0]['BOJEDT'],'BSPSQN':records[0]['BOSPSQ']}
                    
                ret=rccpsDBTrcc_hdcbka.selectu(where_dict)
                if(ret==None):
                    return AfaFlowControl.ExitThisFlow('A099','��ѯԭ��Ϣʧ��' )                    
                if(len(ret)==0):
                    return AfaFlowControl.ExitThisFlow('A099','δ����ԭ��Ϣ' )
                    
                #=====��Լ���ӻ�Ҳ鸴���ӡ��ʽ====
                txt="""\
                
                                 
                                           %(BESBNM)sȫ����Լ���ӻ�Ҳ鸴��
                                           
                    |-----------------------------------------------------------------------------|
                    | �鸴����:             |      %(BJEDTE)s                                       |
                    |-----------------------------------------------------------------------------|
                    | ��Լ��Ҳ鸴���:     |      %(BSPSQN)s                                   |
                    |-----------------------------------------------------------------------------|
                    | �������к�:           |      %(SNDBNKCO)s                                     |
                    |-----------------------------------------------------------------------------|
                    | �������к�:           |      %(RCVBNKCO)s                                     |
                    |-----------------------------------------------------------------------------|
                    | ԭ��Լ��ѯ�������к�: |      %(ORSNDBNKCO)s                                     |
                    |-----------------------------------------------------------------------------|
                    | ԭ��Լ��ѯ����:       |      %(BOJEDT)s                                       |
                    |-----------------------------------------------------------------------------|
                    | ԭ���:               |      %(OROCCAMT)-15.2f                                |
                    |-----------------------------------------------------------------------------|
                    | ԭί������:           |      %(ORTRCDAT)s                                       |
                    |-----------------------------------------------------------------------------|
                    | ԭ��Լ��ѯ������ˮ��: |      %(ORTRCNO)s                                   |
                    |-----------------------------------------------------------------------------|
                    | ��ѯ����:             |                                                     |
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
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'               
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'ORSNDBNKCO':(ret['SNDBNKCO']).ljust(10,' '),\
                                         'BOJEDT':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'OROCCAMT':(ret['OCCAMT']),\
                                         'ORTRCDAT':(ret['TRCDAT']).ljust(8,' '),\
                                         'ORTRCNO':(ret['TRCNO']).ljust(12,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���
                
                AfaLoggerFunc.tradeDebug("�������ɴ�ӡ�ı�")
            #=====��Լ������ɸ�ʽ��====
            elif(TradeContext.TRCCO=='9900524'):                
                AfaLoggerFunc.tradeInfo(">>>ҵ������Ϊ��Լ������ɸ�ʽ��")
                
                #=====��Լ���ӻ�����ɸ�ʽ���ӡ��ʽ====
                txt="""\
                
                                             %(BESBNM)sȫ����Լ���ӻ�����ɸ�ʽ��
                                           
                    |-----------------------------------------------------------------------------|
                    | ����:                  |      %(BJEDTE)s                                      |
                    |-----------------------------------------------------------------------------|
                    | ��Լ������ɸ�ʽ���:  |      %(BSPSQN)s                                  |
                    |-----------------------------------------------------------------------------|
                    | �������к�:            |      %(SNDBNKCO)s                                    |
                    |-----------------------------------------------------------------------------|
                    | �������к�:            |      %(RCVBNKCO)s                                    |
                    |-----------------------------------------------------------------------------|
                    | ����:                  |                                                    |
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
                
                #=====д�ļ�����====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8531'                
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "�����ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���                
                AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")                    
            else:
                return AfaFlowControl.ExitThisFlow('A099','û����ص�ҵ������' )    
        
        
        TradeContext.RECCOUNT="1"           #��ѯ����
        TradeContext.RECALLCOUNT="1"        #�ܱ���
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
              
    elif( len(TradeContext.PRTTYPE) == 0 ):
        return AfaFlowControl.ExitThisFlow('A099','��ӡ��־Ϊ������' )  
    else:
        return AfaFlowControl.ExitThisFlow('A099','��ӡ��־�Ƿ�' )
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8531]�˳�***' )
    return True