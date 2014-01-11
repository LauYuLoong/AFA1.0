# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Լ���ӻ�Ҳ鸴�鷢��
#===============================================================================
#   �����ļ�:   TRCC003_8519.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra
import rccpsMap8519CTradeContext2Dhdcbka


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    #=================��ѯԭ�鸴��Ϣ============================================
    
    if not TradeContext.existVariable('ORQYDAT'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭ��ѯ���ڲ���Ϊ��")
    
    if not TradeContext.existVariable('OQTNO'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭ��ѯ�Ų���Ϊ��")
        
    #=====������ 20080701 �޸Ĳ�ѯ����====
    #=====ʹ�ô�������Ӧ�ò�ѯ ��ѯ�鸴�Ǽǲ� �й�����Լ��Ҳ�ѯ����Ϣ====
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ��ѯ����Ϣ")
    hdcbka = {}
    hdcbka['BJEDTE']   =  TradeContext.ORQYDAT     #��ѯ����
    hdcbka['BSPSQN']   =  TradeContext.OQTNO       #�������

    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka)

    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow('S999','��ѯ���ݿ����')
    if len(hdcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow('S999','���ݿ�������Ӧ��¼')


    #=====������ 20080702 �����ж��Ƿ��Ѳ鸴====
    if hdcbka_dict['ISDEAL'] == PL_ISDEAL_ISDO:
        return AfaFlowControl.ExitThisFlow('S999','�������['+TradeContext.OQTNO+']�ñ�ҵ���Ѳ鸴')

    #=====������ 20080725 �����ж��Ƿ�����====
    if hdcbka_dict['BRSFLG'] != PL_BRSFLG_RCV:
        return AfaFlowControl.ExitThisFlow('S999','�������['+TradeContext.OQTNO+']�ñ�ҵ��Ϊ���˲�ѯ��')

    #=====������ 20080722 �����ж�ԭ���״����Ƿ�Ϊ:��Լ��Ҳ�ѯ�� 9900522====
    if hdcbka_dict['TRCCO'] != '9900522':
        return AfaFlowControl.ExitThisFlow('S999','�������['+TradeContext.OQTNO+']�ñ�ҵ��Ϊ��Լ��Ҳ�ѯ��')

    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ������Ϣ")
    trcbka_dict = {}
    ret = rccpsDBFunc.getTransTrc(hdcbka_dict['BOJEDT'],hdcbka_dict['BOSPSQ'],trcbka_dict)
    
    if not ret:
        return AfaFlowControl.ExitThisFlow('S999','��ѯԭ������Ϣʧ��') 
    
    AfaLoggerFunc.tradeInfo(">>>������ѯ���ݿ���Ϣ")
    #=================�Ǽǲ鸴����Ϣ============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ���Լ���ӻ��ҵ��鸴����Ϣ")
    
    #TradeContext.RCVBNKCO = hdcbka_dict['SNDBNKCO']
    #TradeContext.RCVBNKNM = hdcbka_dict['SNDBNKNM']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_ISDO            #�鸴��ʶΪ�Ѵ���
    
    #=====������ 20080701 �������ݿ�����====
    TradeContext.CUR      = trcbka_dict['CUR']        #����
    TradeContext.ORTRCCO  = hdcbka_dict['TRCCO']      #ԭ���״���
    TradeContext.OCCAMT   = trcbka_dict['OCCAMT']     #���׽��
    TradeContext.PYRACC   = trcbka_dict['PYRACC']     #�������˺�
    TradeContext.PYEACC   = trcbka_dict['PYEACC']     #�տ����˺�
    TradeContext.NOTE1    = hdcbka_dict['NOTE1']      #��ע1
    TradeContext.NOTE2    = hdcbka_dict['NOTE2']      #��ע2
    TradeContext.NOTE3    = hdcbka_dict['NOTE3']      #��ע3
    TradeContext.NOTE4    = hdcbka_dict['NOTE4']      #��ע4
    TradeContext.BRSFLG   = PL_BRSFLG_SND             #������־
    
    hdcbka_insert_dict = {}
    if not rccpsMap8519CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ��Լ���ӻ��ҵ���ѯ�鸴�Ǽǲ���ֵ�쳣")
  
    #�ر�� 20080728 BJEDTE��BSPSQN��map�������Ѹ�ֵ
    #hdcbka_insert_dict['BJEDTE']  =  TradeContext.BJEDTE
    #hdcbka_insert_dict['BSPSQN']  =  TradeContext.BSPSQN
    
    #=====�˹�ͨ 20080729 ���ɴ�ӡ����е�����====
    TradeContext.OR_SNDBNKCO = trcbka_dict['SNDBNKCO']
    TradeContext.OR_TRCDAT   = trcbka_dict['TRCDAT']
    TradeContext.OR_TRCNO    = trcbka_dict['TRCNO']
    TradeContext.OR_OCCAMT   = trcbka_dict['OCCAMT']
        
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "�Ǽ���Լ���ӻ��ҵ��鸴����Ϣ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ���Լ���ӻ��ҵ��鸴����Ϣ")
    
    #=================Ϊ��Լ���ӻ�Ҳ鸴�鱨�ĸ�ֵ======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Լ���ӻ�Ҳ鸴�鱨�ĸ�ֵ")
    
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    #TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN      = hdcbka_dict['SNDMBRCO'] + hdcbka_dict['TRCDAT'] + hdcbka_dict['TRCNO']
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '99'
    TradeContext.TRANTYP    = '0'
    TradeContext.TRCDAT     = TradeContext.TRCDAT
    TradeContext.TRCNO      = TradeContext.SerialNo
    TradeContext.ORTRCDAT   = hdcbka_dict['TRCDAT']
    TradeContext.ORTRCNO    = hdcbka_dict['TRCNO']
    TradeContext.ORSNDBNK   = hdcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNK   = hdcbka_dict['RCVBNKCO']
    TradeContext.ORTRCCO    = hdcbka_dict['TRCCO']
    TradeContext.ORCUR      = trcbka_dict['CUR']
    TradeContext.OROCCAMT   = str(trcbka_dict['OCCAMT'])
    TradeContext.ORQYDAT    = hdcbka_dict['BJEDTE']
    TradeContext.OQTSBNK    = hdcbka_dict['SNDBNKCO']

    #=====������ 20080701 ������/����������====
    TradeContext.PYENAM     = trcbka_dict['PYENAM']       #�տ�������
    TradeContext.PYRNAM     = trcbka_dict['PYRNAM']       #����������
    TradeContext.OROQTNO    = hdcbka_dict['TRCNO']        #ԭ��Լ��ѯ������ˮ��
    TradeContext.BOJEDT     = hdcbka_dict['BJEDTE']
    TradeContext.BOSPSQ     = hdcbka_dict['BSPSQN']
    
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ��Լ���ӻ�Ҳ鸴�鱨�ĸ�ֵ")
    
   
    return True

#=====================���׺���================================================
def SubModuleDoSnd():
    #=================�ж�afe�Ƿ��ͳɹ�=======================================
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo('���ͳɹ�')
    #=====������ 20080702 �����޸�ԭ��¼״̬Ϊ �Ѳ鸴 ====
    hdcbka_where_dict = {}
    hdcbka_where_dict['BJEDTE'] = TradeContext.BOJEDT
    hdcbka_where_dict['BSPSQN'] = TradeContext.BOSPSQ

    hdcbka_update_dict = {}
    hdcbka_update_dict['ISDEAL']  = PL_ISDEAL_ISDO

    ret = rccpsDBTrcc_hdcbka.update(hdcbka_update_dict,hdcbka_where_dict)
    if ret == None:
        return AfaFlowControl.ExitThisFlow('S999','���ݿ��������')
    if ret <= 0:
        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeError(">>>Rollback�쳣")
        return AfaFlowControl.ExitThisFlow("S999","����ϵͳ״̬�쳣")

    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")

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
        | ԭ���:               |      %(OROCCAMT)-15.2f                         |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8519'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'ORSNDBNKCO':(TradeContext.OR_SNDBNKCO).ljust(10,' '),\
                             'BOJEDT':(TradeContext.ORQYDAT).ljust(8,' '),\
                             'OROCCAMT':(TradeContext.OR_OCCAMT),\
                             'ORTRCDAT':(TradeContext.OR_TRCDAT).ljust(8,' '),\
                             'ORTRCNO':(TradeContext.OR_TRCNO).ljust(12,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    return True
    
