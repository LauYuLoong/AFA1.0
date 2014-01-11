# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Լ���ӻ�Ҳ�ѯ�鷢��
#===============================================================================
#   �����ļ�:   TRCC003_8518.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra
import rccpsMap8518CTradeContext2Dhdcbka


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Լ���ӻ�Ҳ�ѯ�鷢��[TRC003_8518]����***' )
    
    #=================��ѯԭ������Ϣ============================================
    
    if not TradeContext.existVariable('BOJEDT'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭ�������ڲ���Ϊ��")
    
    if not TradeContext.existVariable('BOSPSQ'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭ������Ų���Ϊ��")

    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ��Լ���ӻ��ҵ������Ϣ")
    
    trcbka_dict = {}
    ret = rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka_dict)
    
    if not ret:
        return False

    #====������ 20080701 �����Ƿ�����ҵ���ж�====
    if trcbka_dict['BRSFLG'] != PL_BRSFLG_RCV:
        return AfaFlowControl.ExitThisFlow('S999','ԭ���׷�����ҵ����������ҵ��')
    
    #====������ 20080701 �����Ƿ���Լ���ҵ���ж�====
    if trcbka_dict['TRCCO'] != '2000009':
        return AfaFlowControl.ExitThisFlow('S999','ԭ���׷���Լ���ҵ���������˽���')

    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ��Լ���ӻ��ҵ������Ϣ")
    #=================�Ǽǲ�ѯ����Ϣ============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ���Լ���ӻ��ҵ���ѯ����Ϣ")
    
    TradeContext.RCVBNKCO = trcbka_dict['SNDBNKCO']
    TradeContext.RCVBNKNM = trcbka_dict['SNDBNKNM']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_UNDO            #�鸴��ʶΪδ�鸴

    #=====������ 20080701 ���ӻ��ҵ���ѯ�鸴�Ǽǲ���Ϣ====
    TradeContext.RCVSTLBIN= '9999999997'              #��Լҵ�����������
    TradeContext.BRSFLG   = PL_BRSFLG_SND             #������־
    TradeContext.ORTRCCO  = trcbka_dict['TRCCO']      #ԭ���״���
    TradeContext.CUR      = trcbka_dict['CUR']        #����
    TradeContext.OCCAMT   = trcbka_dict['OCCAMT']     #���׽��
    TradeContext.PYRACC   = trcbka_dict['PYRACC']     #�������˺�
    TradeContext.PYEACC   = trcbka_dict['PYEACC']     #�տ����˺�
    TradeContext.PRCCO    = trcbka_dict['PRCCO']      #���ķ�����
    TradeContext.NOTE1    = trcbka_dict['NOTE1']      #��ע1
    TradeContext.NOTE2    = trcbka_dict['NOTE2']      #��ע2
    TradeContext.NOTE3    = trcbka_dict['NOTE3']      #��ע3
    TradeContext.NOTE4    = trcbka_dict['NOTE4']      #��ע4
    
    #=====PGT 20080728 ��ӡ����е��ֶ�====
    TradeContext.OR_TRCDAT   = trcbka_dict['TRCDAT']    
    TradeContext.OR_SNDBNKCO = trcbka_dict['SNDBNKCO']
    TradeContext.OR_OCCAMT  = trcbka_dict['OCCAMT']
    
    hdcbka_insert_dict = {}
    if not rccpsMap8518CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ��Լ���ӻ��ҵ���ѯ�鸴�Ǽǲ���ֵ�쳣")
        
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "�Ǽ���Լ���ӻ��ҵ���ѯ����Ϣ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ���Լ���ӻ��ҵ���ѯ����Ϣ")
    
    
    #=================Ϊ��Լ���ӻ�Ҳ�ѯ�鱨�ĸ�ֵ======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Լ���ӻ�Ҳ�ѯ�鱨�ĸ�ֵ")
    
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
    TradeContext.ORTRCCO    = trcbka_dict['TRCCO']
    TradeContext.ORCUR      = trcbka_dict['CUR']
    TradeContext.OROCCAMT   = str(trcbka_dict['OCCAMT'])
    TradeContext.PYENAM     = trcbka_dict['PYENAM']
    TradeContext.PYRNAM     = trcbka_dict['PYRNAM']
       
    AfaLoggerFunc.tradeInfo(">>>����Ϊ��Լ���ӻ�Ҳ�ѯ�鱨�ĸ�ֵ")
    
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
            
            
                               %(BESBNM)sȫ����Լ���ӻ�Ҳ�ѯ��
                               
        |-----------------------------------------------------------------------------|
        | ��ѯ����:             |      %(BJEDTE)s                                       |
        |-----------------------------------------------------------------------------|
        | ��Լ��Ҳ�ѯ���:     |      %(BSPSQN)s                                   |
        |-----------------------------------------------------------------------------|
        | �������к�:           |      %(SNDBNKCO)s                                     |
        |-----------------------------------------------------------------------------|
        | �������к�:           |      %(RCVBNKCO)s                                     |
        |-----------------------------------------------------------------------------|
        | ԭ���:               |      %(OROCCAMT)-15.2f                                |
        |-----------------------------------------------------------------------------|
        | ԭί������:           |      %(ORTRCDAT)s                                       |
        |-----------------------------------------------------------------------------|
        | ԭ�������к�:         |      %(ORSNDBNKCO)s                                     |
        |-----------------------------------------------------------------------------|
        | ��ѯ����:             |                                                     |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8518'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'OROCCAMT':(TradeContext.OR_OCCAMT),\
                             'ORTRCDAT':(TradeContext.OR_TRCDAT).ljust(8,' '),\
                             'ORSNDBNKCO':(TradeContext.OR_SNDBNKCO).ljust(10,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    return True
