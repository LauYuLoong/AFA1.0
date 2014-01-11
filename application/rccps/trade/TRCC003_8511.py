# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Ҳ�ѯ�鷢��
#===============================================================================
#   �����ļ�:   TRCC003_8511.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra
import rccpsMap8511CTradeContext2Dhdcbka


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    #=================��ѯԭ������Ϣ============================================
    
    if not TradeContext.existVariable('BOJEDT'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭ�������ڲ���Ϊ��")
    
    if not TradeContext.existVariable('BOSPSQ'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭ������Ų���Ϊ��")
        
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ���ҵ������Ϣ")
    
    trcbka_dict = {}
    ret = rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka_dict)
    
    if not ret:
        return False
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ���ҵ������Ϣ")
    #=================�Ǽǲ�ѯ����Ϣ============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ��ҵ���ѯ����Ϣ")
    
    #TradeContext.RCVBNKCO = trcbka_dict['RCVBNKCO']
    #TradeContext.RCVBNKNM = trcbka_dict['RCVBNKNM']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_UNDO            #�鸴��ʶΪδ�鸴
    
    #=====������ 20080701 �������ҵ���ѯ�鸴�Ǽǲ���Ϣ====
    TradeContext.TRCNO    = TradeContext.SerialNo       #������ˮ��
    TradeContext.ORTRCCO    = trcbka_dict['TRCCO']      #ԭ���״���
    TradeContext.CUR      = trcbka_dict['CUR']          #ԭ����
    TradeContext.OCCAMT   = str(trcbka_dict['OCCAMT'])  #ԭ���׽��
    TradeContext.PYRACC   = trcbka_dict['PYRACC']       #ԭ�������˺�
    TradeContext.PYEACC   = trcbka_dict['PYEACC']       #ԭ�տ����˺�
    #TradeContext.PRCCO    = trcbka_dict['PRCCO']        #���ķ��ش���   �ر�� ɾ�� 20080728
    TradeContext.NOTE1    = trcbka_dict['NOTE1']        #��ע1
    TradeContext.NOTE2    = trcbka_dict['NOTE2']        #��ע2
    TradeContext.NOTE3    = trcbka_dict['NOTE3']        #��ע3
    TradeContext.NOTE4    = trcbka_dict['NOTE4']        #��ע4
    
    TradeContext.PRT_OROCCAMT = trcbka_dict['OCCAMT']
    
    hdcbka_insert_dict = {}
    if not rccpsMap8511CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ���ҵ���ѯ�鸴�Ǽǲ���ֵ�쳣")
        
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "�Ǽǻ��ҵ���ѯ����Ϣ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ��ҵ���ѯ����Ϣ")
    
    #=====��ֵ����ӡ���еı���====
    TradeContext.OROCCAMT=str(trcbka_dict['OCCAMT'])
    TradeContext.ORSNDBNKCO=trcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNKCO=trcbka_dict['RCVBNKCO']
    
    
    #=================Ϊ��Ҳ�ѯ�鱨�ĸ�ֵ=====================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Ҳ�ѯ�鱨�ĸ�ֵ")
    
    TradeContext.TRCCO      = '9900511'
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN      = trcbka_dict['SNDMBRCO'] + trcbka_dict['TRCDAT'] + trcbka_dict['TRCNO']
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '20'
    TradeContext.TRANTYP    = '0'
    TradeContext.TRCDAT     = TradeContext.TRCDAT
    TradeContext.TRCNO      = TradeContext.SerialNo
    TradeContext.ORTRCDAT   = trcbka_dict['TRCDAT']
    TradeContext.ORTRCNO    = trcbka_dict['TRCNO']
    TradeContext.ORSNDBNK   = trcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNK   = trcbka_dict['RCVBNKCO']
    TradeContext.ORCUR      = trcbka_dict['CUR']
    TradeContext.OROCCAMT   = str(trcbka_dict['OCCAMT'])
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ��Ҳ�ѯ�鱨�ĸ�ֵ")
    
    
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    #=================�ж�afe�Ƿ��ͳɹ�=======================================
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8511'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'OROCCAMT':(TradeContext.PRT_OROCCAMT),\
                             'ORSNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'ORRCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    
    AfaLoggerFunc.tradeInfo('���ͳɹ�')
    
    return True
    
