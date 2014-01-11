# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).Ʊ�ݲ鸴�鷢��
#===============================================================================
#   �����ļ�:   TRCC003_8515.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-15
###############################################################################
#   �޸���  :   ������
#   �޸�ʱ��:   2008-07-21
#   ��    ��:   �޸�ԭ������hpcbka��Ʊ��ѯ�鸴�Ǽǲ�ΪpjcbkaƱ�ݲ�ѯ�鸴�Ǽǲ�
#               �޸Ĳ�ѯԭ������Ϣ����getTransTrcΪrccpsDBTrcc_pjcbka.selectu
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_pjcbka,rccpsDBTrcc_subbra
import rccpsMap8515CTradeContext2Dpjcbka


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).Ʊ�ݲ鸴�鷢��[TRC003_8515]����***' )
    
    #=================��ѯԭ������Ϣ============================================
    
    if not TradeContext.existVariable('BOSPSQ'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭƱ�ݲ�ѯ��Ų���Ϊ��")
    
    if not TradeContext.existVariable('BOJEDT'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭƱ�ݲ�ѯ���ڲ���Ϊ��")
        
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ��ѯ����Ϣ")
    
    pjcbka_dict = {}
    pjcbka_dict['BJEDTE']  =  TradeContext.BOJEDT
    pjcbka_dict['BSPSQN']  =  TradeContext.BOSPSQ
    ret = rccpsDBTrcc_pjcbka.selectu(pjcbka_dict)
    if ret == None:
        return  AfaFlowControl.ExitThisFlow('S999','��ѯƱ�ݲ�ѯ�鸴ҵ��Ǽǲ��쳣') 
        
    TradeContext.OR_BJEDTE=ret['BJEDTE']
    TradeContext.OR_SNDBNKCO=ret['SNDBNKCO']
    
        
    AfaLoggerFunc.tradeInfo(">>>������ѯ���ݿ���Ϣ")
    
    #=================�Ǽǲ�ѯ����Ϣ============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�Ʊ��ҵ���ѯ����Ϣ")
    
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_ISDO            #�鸴��ʶΪδ�鸴
    TradeContext.ORTRCCO  = ret['TRCCO']              #ԭ���״���
    TradeContext.BILNO    = ret['BILNO']              #Ʊ�ݺ���
    TradeContext.BILDAT   = ret['BILDAT']             #Ʊ������
    TradeContext.BILPNAM  = ret['BILPNAM']            #��Ʊ������
    TradeContext.BILENDDT = ret['BILENDDT']           #Ʊ�ݽ�������
    TradeContext.BILAMT   = str(ret['BILAMT'])        #��Ʊ���
    TradeContext.PYENAM   = ret['PYENAM']             #�տ�������
    TradeContext.HONBNKNM = ret['HONBNKNM']           #��Ʊ������
    TradeContext.OQTSBNK  = ret['SNDBNKCO']           #ԭ�����к�
    TradeContext.OQTNO    = ret['TRCNO']              #ԭ������ˮ��
    TradeContext.ORQYDAT  = ret['BJEDTE']             #ԭ��ѯ����
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if len(TradeContext.BILNO) == 16:
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #=====TradeContext���ֵ丳ֵ����====
    pjcbka_insert_dict = {}
    if not rccpsMap8515CTradeContext2Dpjcbka.map(pjcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "ΪƱ��ҵ���ѯ�鸴�Ǽǲ���ֵ�쳣")
        
    #=====����pjcbkaƱ�ݲ�ѯ�鸴�Ǽǲ�====
    ret = rccpsDBTrcc_pjcbka.insertCmt(pjcbka_insert_dict)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "�Ǽ�Ʊ��ҵ���ѯ����Ϣ�쳣")

    AfaLoggerFunc.tradeInfo(">>>�����Ǽ�Ʊ��ҵ���ѯ����Ϣ")

    #=====������ 2008-07-21 ��������ԭ���ײ�ѯ�鸴��־====
    pjcbka_update = {}
    pjcbka_set    = {}
    pjcbka_update['BJEDTE']  =  TradeContext.BOJEDT
    pjcbka_update['BSPSQN']  =  TradeContext.BOSPSQ
    pjcbka_set['ISDEAL']     =  TradeContext.ISDEAL
    ret = rccpsDBTrcc_pjcbka.updateCmt(pjcbka_set,pjcbka_update)
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "����ԭƱ�ݲ�ѯ���ѯ�鸴��ʶ�쳣")
        
        
    
    #=================ΪƱ�ݲ�ѯ�鱨�ĸ�ֵ======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪƱ�ݲ�ѯ�鱨�ĸ�ֵ")
    
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    #TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '20'
    TradeContext.TRANTYP    = '0'
    TradeContext.TRCNO      = TradeContext.SerialNo
    TradeContext.ORPYENAM   = TradeContext.PYENAM
    
    AfaLoggerFunc.tradeInfo(">>>����ΪƱ�ݲ�ѯ�鱨�ĸ�ֵ")
    
    return True
#=====================���׺���================================================
def SubModuleDoSnd():
    #=================�ж�afe�Ƿ��ͳɹ�=======================================
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo('���ͳɹ�')
    
    #=====��ѯ������====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ������ʧ��' )
        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','û����Ӧ�Ļ�����' )
        
    #=================���ɴ�ӡ�ı�=============================================
    AfaLoggerFunc.tradeInfo("��ʼ���ɴ�ӡ�ı�")
    
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
   |   %(CONT1)s                |
   |                                                                                       |
   |   %(CONT2)s              |
   |                                                                                       |
   |   %(CONT3)s              |
   |                                                                                       |
   |   %(CONT4)s              |
   |                                                                                       |
   |---------------------------------------------------------------------------------------|
   ��ӡ����: %(BJEDTE)s      ��Ȩ:                       ����:
    """
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8515'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'BILDAT':(TradeContext.BILDAT).ljust(8,' '),\
                             'BILENDDT':(TradeContext.BILENDDT).ljust(8,' '),\
                             'BILNO':(TradeContext.BILNO).ljust(16,' '),\
                             'BILPNAM':(TradeContext.BILPNAM).ljust(60,' '),\
                             'PYENAM':(TradeContext.PYENAM).ljust(60,' '),\
                             'HONBNKNM':(TradeContext.HONBNKNM).ljust(60,' '),\
                             'BOJEDT':(TradeContext.OR_BJEDTE).ljust(8,' '),\
                             'ORSNDBNKCO':(TradeContext.OR_SNDBNKCO).ljust(10,' '),\
                             'BOSPSQ':(TradeContext.BOSPSQ).ljust(12,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    
    return True
