# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.��Ʊ��ѯ�鸴�ǼǱ���ѯ
#=================================================================
#   �����ļ�:   TRCC001_8533.py
#   �޸�ʱ��:   2008-07-09
#   ���ߣ�      �˹�ͨ
##################################################################

import rccpsDBTrcc_hpcbka,rccpsDBTrcc_subbra,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc
from types import *
import os

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8533]����***' )
    
    #=====�ж�����ӿ�ֵ�Ƿ����====
    if( not TradeContext.existVariable( "STRDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[STRDAT]������')
        
    if( not TradeContext.existVariable( "ENDDAT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[ENDDAT]������')
        
    if( not TradeContext.existVariable( "RECSTRNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ʼ����[RECSTRNO]������')
    
    if(len(TradeContext.PRTTYPE)==0): 
        return AfaFlowControl.ExitThisFlow('A099','��ӡ��־[PRTTYPE]������Ϊ��' )
 
        
    #=====��ʼ����====
    start_no=TradeContext.RECSTRNO
        
    #=====��֯sql���====
    wheresql=""
    wheresql = wheresql + "BESBNO='" + TradeContext.BESBNO + "' "
    wheresql = wheresql + "and BJEDTE>='" + TradeContext.STRDAT + "'"
    wheresql = wheresql + " AND BJEDTE<='" + TradeContext.ENDDAT + "'"
    
    #=====�жϽ��״����Ƿ�Ϊ��====
    if(TradeContext.TRCCO!=""):
        wheresql=wheresql+" AND TRCCO='"+TradeContext.TRCCO+"'"
        
    #=====�ж�������ʶ�Ƿ�Ϊ��====
    if(TradeContext.BRSFLG!=""):
        wheresql=wheresql+" AND BRSFLG='"+TradeContext.BRSFLG+"'"
    
    #=====�жϲ鸴��ʶ�Ƿ�Ϊ�ջ�Ϊ9-ȫ��====    
    if(TradeContext.ISDEAL!="" and TradeContext.ISDEAL!="9"):
        wheresql=wheresql+" AND ISDEAL='"+TradeContext.ISDEAL+"'"
        
    #=====�жϻ�Ʊ�����Ƿ�Ϊ��====      
    if (TradeContext.BILNO!=""):
        wheresql=wheresql+" AND BILNO='"+TradeContext.BILNO+"'"
        
    #=====��ѯ������====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ������ʧ��' )        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ��������������������¼' )
    
    #=====�жϴ�ӡ���� 0 ����ӡ====    
    if(TradeContext.PRTTYPE=='0'):        
        AfaLoggerFunc.tradeInfo( ">>>���벻��ӡ����")
        
        #=====�жϲ�ѯ�鸴����Ƿ�Ϊ��====
        if (TradeContext.BSPSQN!=""):
            wheresql=wheresql+" AND BSPSQN='"+TradeContext.BSPSQN+"'"
        
        #=====��ѯ�ܼ�¼��====
        allcount=rccpsDBTrcc_hpcbka.count(wheresql)
        if (allcount<0):
            return AfaFlowControl.ExitThisFlow('A099','�����ܼ�¼��ʧ��' )
            
        #=====��ѯ���ݿ�====
        ordersql=" order by BJEDTE DESC,BSPSQN DESC"   #��������ʽ
        records=rccpsDBTrcc_hpcbka.selectm(start_no,10,wheresql,ordersql)
        if (records==None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )
        if (len(records)<=0):
            return AfaFlowControl.ExitThisFlow('A099','û�в��ҵ�����' )            
        else:
            #=====�����ļ�====
            filename="rccps_"+TradeContext.BETELR+"_"+AfaUtilTools.GetHostDate()+"_"+TradeContext.TransCode        
            fpath=os.environ["AFAP_HOME"]+"/tmp/"
            f=open(fpath+filename,"w")
            
            if( f==None ):
                return AfaFlowControl.ExitThisFlow('A099','���ļ�ʧ��' )
                 
            filecontext=""            
            #=====д�ļ�����====
            for i in range(0,len(records)):
                #=====�����ļ�����====
                filecontext=records[i]['BJEDTE']      + "|" \
                           +records[i]['BSPSQN']      + "|" \
                           +records[i]['BRSFLG']      + "|" \
                           +records[i]['BESBNO']      + "|" \
                           +records[i]['BETELR']      + "|" \
                           +records[i]['BEAUUS']      + "|" \
                           +records[i]['NCCWKDAT']    + "|" \
                           +records[i]['TRCCO']       + "|" \
                           +records[i]['TRCDAT']      + "|" \
                           +records[i]['TRCNO']       + "|" \
                           +records[i]['SNDBNKCO']    + "|" \
                           +records[i]['SNDBNKNM']    + "|" \
                           +records[i]['RCVBNKCO']    + "|" \
                           +records[i]['RCVBNKNM']    + "|" \
                           +records[i]['BOJEDT']      + "|" \
                           +records[i]['BOSPSQ']      + "|" \
                           +records[i]['ORTRCCO']     + "|" \
                           +records[i]['CONT']        + "|" \
                           +records[i]['ISDEAL']      + "|" \
                           +records[i]['BILVER']      + "|" \
                           +records[i]['BILNO']       + "|" \
                           +records[i]['BILDAT']      + "|" \
                           +records[i]['PAYWAY']      + "|" \
                           +records[i]['CUR']         + "|" \
                           +str(records[i]['BILAMT']) + "|" \
                           +records[i]['PYRACC']      + "|" \
                           +records[i]['PYRNAM']      + "|" \
                           +records[i]['PYEACC']      + "|" \
                           +records[i]['PYENAM']      + "|" \
                           +records[i]['PRCCO']       + "|" \
                           +records[i]['STRINFO']     + "|" 
            
                f.write(filecontext+"\n")
            f.close()
            
        #=====����ӿڸ�ֵ====
        TradeContext.PBDAFILE=filename              #�ļ���
        TradeContext.RECCOUNT=str(len(records))     #��ѯ����
        TradeContext.RECALLCOUNT=str(allcount)      #�ܱ���
        TradeContext.RECSTRNO=str(start_no)         #��ʼ����
    #=====1 ��ӡ====
    elif(TradeContext.PRTTYPE=='1'):      
        AfaLoggerFunc.tradeInfo(">>>�����ӡ����")
        
        #=====�жϲ�ѯ�鸴����Ƿ�Ϊ��====
        if (TradeContext.BSPSQN!=""):
            wheresql=wheresql+" AND BSPSQN='"+TradeContext.BSPSQN+"'"           
        else:
            return AfaFlowControl.ExitThisFlow('A099','��ѯ�鸴���[BSPSQN]������Ϊ��' )
            
        #=====��ѯ���ݿ�====
        records=rccpsDBTrcc_hpcbka.selectm(start_no,10,wheresql,"")
        
        if(records==None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯʧ��' )       
        elif( len(records)<=0 ):
            return AfaFlowControl.ExitThisFlow('A099','δ���ҵ�����' )        
        else:            
            #=====��Ʊ��ѯ��====
            if(TradeContext.TRCCO=='9900526'):                
                AfaLoggerFunc.tradeInfo(">>>�����Ʊ��ѯ�鴦��")
                
                #=====��Ʊ��ѯ���ӡ��ʽ====
                txt = """\
                        
              
                                     %(BESBNM)s��Ʊ��ѯ��
                                 
          |--------------------------------------------------------------------------------------------|
          | ��ѯ����:     | %(BJEDTE)s                                                                   |
          |--------------------------------------------------------------------------------------------|
          | ��Ʊ��ѯ���: | %(BSPSQN)s                                                               |
          |--------------------------------------------------------------------------------------------|
          | �������к�:   | %(SNDBNKCO)s                                                                 |
          |--------------------------------------------------------------------------------------------|
          | �������к�:   | %(RCVBNKCO)s                                                                 |
          |--------------------------------------------------------------------------------------------|
          | ��Ʊ����:     | %(BILDAT)s                                                                   |
          |--------------------------------------------------------------------------------------------|
          | ��Ʊ���:     | %(BILAMT)-15.2f                                                            |
          |--------------------------------------------------------------------------------------------|
          | ��Ʊ����:     | %(BILNO)s                                                           |
          |--------------------------------------------------------------------------------------------|
          | �������˺�:   | %(PYRACC)s                                           |
          |--------------------------------------------------------------------------------------------|
          | ����������:   | %(PYRNAM)s               |
          |--------------------------------------------------------------------------------------------|
          | �տ����˺�:   | %(PYEACC)s                                           |
          |--------------------------------------------------------------------------------------------|
          | �տ�������:   | %(PYENAM)s               |
          |--------------------------------------------------------------------------------------------|
          | ��ѯ����:     |                                                                            |
          |--------------------------------------------------------------------------------------------|
          |                                                                                            |
          |   %(CONT1)s                     |
          |                                                                                            |
          |   %(CONT2)s                   |
          |                                                                                            |
          |   %(CONT3)s                   |
          |                                                                                            |
          |   %(CONT4)s                   |
          |                                                                                            |
          |--------------------------------------------------------------------------------------------|
          ��ӡ����: %(BJEDTE)s      ��Ȩ:                       ����:
                """
                
                #=====д�ļ�����====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8533'               
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BILDAT':(records[0]['BILDAT']).ljust(8,' '),\
                                         'BILAMT':(records[0]['BILAMT']),\
                                         'BILNO':(records[0]['BILNO']).ljust(16,' '),\
                                         'PYRACC':(records[0]['PYRACC']).ljust(32,' '),\
                                         'PYRNAM':(records[0]['PYRNAM']).ljust(60,' '),\
                                         'PYEACC':(records[0]['PYEACC']).ljust(32,' '),\
                                         'PYENAM':(records[0]['PYENAM']).ljust(60,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���
                
                AfaLoggerFunc.tradeDebug("�������ɴ�ӡ�ı�")           
            #=====��Ʊ�鸴�鴦��====    
            elif(TradeContext.TRCCO=='9900527'):                
                AfaLoggerFunc.tradeInfo(">>>�����Ʊ�鸴�鴦��")
                
                #=====��Ʊ�鸴���ӡ��ʽ====
                txt = """\
                        
                        
                                           %(BESBNM)s��Ʊ�鸴��
                                           
                    |-----------------------------------------------------------------------------|
                    | ��ѯ����:     | %(BJEDTE)s                                                    |
                    |-----------------------------------------------------------------------------|
                    | ��Ʊ�鸴���: | %(BSPSQN)s                                                |
                    |-----------------------------------------------------------------------------|
                    | �������к�:   | %(SNDBNKCO)s                                                  |
                    |-----------------------------------------------------------------------------|
                    | �������к�:   | %(RCVBNKCO)s                                                  |
                    |-----------------------------------------------------------------------------|
                    | ��Ʊ����:     | %(BILDAT)s                                                    |
                    |-----------------------------------------------------------------------------|
                    | ��Ʊ���:     | %(BILAMT)-15.2f                                             |
                    |-----------------------------------------------------------------------------|
                    | ��Ʊ����:     | %(BILNO)s                                            |
                    |-----------------------------------------------------------------------------|
                    | �������˺�:   | %(PYRACC)s                            |
                    |-----------------------------------------------------------------------------|
                    | ����������:   | %(PYRNAM)s|
                    |-----------------------------------------------------------------------------|
                    | �տ����˺�:   | %(PYEACC)s                            |
                    |-----------------------------------------------------------------------------|
                    | �տ�������:   | %(PYENAM)s|
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
                
                #=====д�ļ�����====
                file_name = 'rccps_' + records[0]['BJEDTE'] + '_' + TradeContext.BSPSQN + '_8533'               
                out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
                
                if out_file == None:
                    return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
                
                print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                                         'BJEDTE':(records[0]['BJEDTE']).ljust(8,' '),\
                                         'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                                         'SNDBNKCO':(records[0]['SNDBNKCO']).ljust(10,' '),\
                                         'RCVBNKCO':(records[0]['RCVBNKCO']).ljust(10,' '),\
                                         'BILDAT':(records[0]['BILDAT']).ljust(8,' '),\
                                         'BILAMT':(records[0]['BILAMT']),\
                                         'BILNO':(records[0]['BILNO']).ljust(16,' '),\
                                         'PYRACC':(records[0]['PYRACC']).ljust(32,' '),\
                                         'PYRNAM':(records[0]['PYRNAM']).ljust(60,' '),\
                                         'PYEACC':(records[0]['PYEACC']).ljust(32,' '),\
                                         'PYENAM':(records[0]['PYENAM']).ljust(60,' '),\
                                         'CONT1':(records[0]['CONT'][:68]).ljust(68,' '),\
                                         'CONT2':(records[0]['CONT'][68:138]).ljust(70,' '),\
                                         'CONT3':(records[0]['CONT'][138:208]).ljust(70,' '),\
                                         'CONT4':(records[0]['CONT'][208:]).ljust(70,' ')}
                
                out_file.close()
                
                TradeContext.PBDAFILE = file_name       #�ļ���
                
                AfaLoggerFunc.tradeDebug("�������ɴ�ӡ�ı�")                
            else:
                return AfaFlowControl.ExitThisFlow('A099','�������ͷǷ�' )
                
            TradeContext.RECCOUNT="1"                   #��ѯ����
            TradeContext.RECALLCOUNT="1"                #�ܱ���
            TradeContext.RECSTRNO=str(start_no)         #��ʼ����
       
    else:
        return AfaFlowControl.ExitThisFlow('A099','��ӡ��־�Ƿ�' )
    
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
            
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.�������������[TRC001_8533]�˳�***' )
    return True            