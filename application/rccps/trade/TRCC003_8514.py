# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).Ʊ�ݲ�ѯ�鷢��
#===============================================================================
#   �����ļ�:   TRCC003_8514.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�   ������
#   �޸�ʱ��:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_pjcbka,rccpsDBTrcc_subbra
import rccpsMap8514CTradeContext2Dpjcbka


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if len(TradeContext.BILNO) == 16:
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #=================��ѯԭ������Ϣ============================================
    
    if not TradeContext.existVariable('BJEDTE'):
        return AfaFlowControl.ExitThisFlow("S999", "��ѯ���ڲ���Ϊ��")
    
    if not TradeContext.existVariable('RCVBNKCO'):
        return AfaFlowControl.ExitThisFlow("S999", "�������кŲ���Ϊ��")
        
    #=================�Ǽǲ�ѯ����Ϣ============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�Ʊ��ҵ���ѯ����Ϣ")
    
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_UNDO            #�鸴��ʶΪδ�鸴
    
    pjcbka_insert_dict = {}
    if not rccpsMap8514CTradeContext2Dpjcbka.map(pjcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "ΪƱ��ҵ���ѯ�鸴�Ǽǲ���ֵ�쳣")
        
    ret = rccpsDBTrcc_pjcbka.insertCmt(pjcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "�Ǽ�Ʊ��ҵ���ѯ����Ϣ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ�Ʊ��ҵ���ѯ����Ϣ")
    
    #=================ΪƱ�ݲ�ѯ�鱨�ĸ�ֵ======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪƱ�ݲ�ѯ�鱨�ĸ�ֵ")
    
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '20'
    TradeContext.TRANTYP    = '0'
    #TradeContext.TRCDAT     = TradeContext.BJEDTE
    TradeContext.TRCNO      = TradeContext.SerialNo
    #TradeContext.BILPNAM    = TradeContext.PYENAM
    #TradeContext.BILAMT   = str(TradeContext.BILAMT)
    
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
        | ��Ʊ���:     | %(BILAMT)s                                             |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8514'
    
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
                             'BILAMT':(TradeContext.BILAMT).ljust(15,' '),\
                             'BILPNAM':(TradeContext.BILPNAM).ljust(60,' '),\
                             'HONBNKNM':(TradeContext.HONBNKNM).ljust(60,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    return True
    
