# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Ҳ鸴�鷢��
#===============================================================================
#   �����ļ�:   TRCC003_8512.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-15
################################################################################
#   �޸���  ��  ������
#   �޸�ʱ�䣺  2008-07-11
#   �޸Ĺ��ܣ�  ���佻�׹��ܣ��жϲ�ѯ���Ƿ��ѱ��鸴
#               �޸Ĳ�ѯԭ��ҽ���ʱ�������뱨�����˳��
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc,os
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra
import rccpsMap8512CTradeContext2Dhdcbka


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).��Ҳ鸴�鷢��[TRC003_8512]����***' )
    
    #=================��ѯԭ�鸴��Ϣ============================================
    
    if not TradeContext.existVariable('ORQYDAT'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭ��ѯ���ڲ���Ϊ��")
    
    if not TradeContext.existVariable('OQTNO'):
        return AfaFlowControl.ExitThisFlow("S999", "ԭ��ѯ�Ų���Ϊ��")
        
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯԭ��ѯ����Ϣ")
    
    hdcbka_dict = {}
    hdcbka_where_dict = {'BJEDTE':TradeContext.ORQYDAT,'BSPSQN':TradeContext.OQTNO}
    #ret = rccpsDBFunc.getTransTrc(TradeContext.ORQYDAT,TradeContext.OQTNO,hdcbka_dict)
    hdcbka_dict = rccpsDBTrcc_hdcbka.selectu(hdcbka_where_dict)
    if hdcbka_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","���ݿ����ʧ��")
    if len(hdcbka_dict) > 0:
        if hdcbka_dict['ISDEAL']  == PL_ISDEAL_ISDO:        #PL_ISDEAL_ISDO  �Ѳ鸴���Ѵ���
            return AfaFlowControl.ExitThisFlow("S999","�ò�ѯ�ѱ��鸴")
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯ���ԭ������Ϣ")
    trcbka_dict = {}
    ret = rccpsDBFunc.getTransTrc(hdcbka_dict['BOJEDT'],hdcbka_dict['BOSPSQ'],trcbka_dict)
    
    if not ret:
        return False
    
    AfaLoggerFunc.tradeInfo(">>>������ѯ���ݿ���Ϣ")
    #=================�Ǽǲ鸴����Ϣ============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ��ҵ��鸴����Ϣ")
    
    RCVBNKCO=TradeContext.RCVBNKCO #add by pgt 0724
    
#    TradeContext.RCVBNKCO = hdcbka_dict['SNDBNKCO']
#    TradeContext.RCVBNKNM = hdcbka_dict['SNDBNKNM']    ע����0724 by pgt
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.ISDEAL   = PL_ISDEAL_ISDO            #�鸴��ʶΪ�Ѵ���
    TradeContext.BOJEDT   = TradeContext.ORQYDAT      #ԭ��������
    TradeContext.BOSPSQ   = TradeContext.OQTNO        #ԭ�������
    TradeContext.ORTRCCO  = hdcbka_dict['TRCCO']      #ԭ������
    TradeContext.CUR      = hdcbka_dict['CUR']        #����
    TradeContext.OCCAMT   = str(trcbka_dict['OCCAMT']) #���׽��
    TradeContext.PYRACC   = trcbka_dict['PYRACC']     #�������˺�
    TradeContext.PYEACC   = trcbka_dict['PYEACC']     #�տ����˺�
    TradeContext.NOTE1    = hdcbka_dict['NOTE1']
    TradeContext.NOTE2    = hdcbka_dict['NOTE2']
    TradeContext.NOTE3    = hdcbka_dict['NOTE3']
    TradeContext.NOTE4    = hdcbka_dict['NOTE4']
    
    TradeContext.PRT_OROCCAMT = trcbka_dict['OCCAMT']
    
    hdcbka_insert_dict = {}
    if not rccpsMap8512CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ���ҵ���ѯ�鸴�Ǽǲ���ֵ�쳣")
        
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "�Ǽǻ��ҵ��鸴����Ϣ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ��ҵ��鸴����Ϣ")
    
    
    
    #=================Ϊ��Ҳ�ѯ�鱨�ĸ�ֵ======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Ҳ鸴�鱨�ĸ�ֵ")
    
    TradeContext.TRCCO      = '9900512'
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN      = TradeContext.RCVSTLBIN + hdcbka_dict['TRCDAT'] + hdcbka_dict['TRCNO']
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '99'
    TradeContext.TRANTYP    = '0'
    TradeContext.TRCDAT     = TradeContext.TRCDAT
    TradeContext.TRCNO      = TradeContext.SerialNo
    TradeContext.ORTRCDAT   = trcbka_dict['TRCDAT']
    TradeContext.ORTRCNO    = trcbka_dict['TRCNO']
    TradeContext.ORSNDBNK   = trcbka_dict['SNDBNKCO']
    TradeContext.ORRCVBNK   = trcbka_dict['RCVBNKCO']
    TradeContext.ORTRCCO    = hdcbka_dict['TRCCO']
    TradeContext.ORCUR      = TradeContext.CUR
    TradeContext.OROCCAMT   = str(hdcbka_dict['OCCAMT'])
    TradeContext.ORQYDAT    = hdcbka_dict['BJEDTE']
    TradeContext.OQTSBNK    = hdcbka_dict['SNDBNKCO']
    TradeContext.OQTNO      = hdcbka_dict['TRCNO']
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ��Ҳ鸴�鱨�ĸ�ֵ")
    
    return True
    
    
    
#=====================���׺���================================================
def SubModuleDoSnd():
    #=================�ж�afe�Ƿ��ͳɹ�=======================================
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo('>>>���ͳɹ�')
    #=====������  2008-07-11  �����޸�ԭ��ѯ���¼Ϊ�Ѳ鸴====
    update_wdict = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
    update       = {'ISDEAL':PL_ISDEAL_ISDO}                   #�Ѳ鸴
    ret = rccpsDBTrcc_hdcbka.update(update,update_wdict)
    if (ret <= 0):
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow("S999","����ԭ��ѯҵ����Ϣ�쳣")

    AfaDBFunc.CommitSql()
    AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
    
    #=====��ѯ������====
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ������ʧ��' )
        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','û����Ӧ�Ļ�����' )

    #=====���ɴ�ӡ�ı�====
    AfaLoggerFunc.tradeInfo("��ʼ���ɴ�ӡ�ı�")
    
    txt = """\
            
            
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

    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_' + '_8512'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'BOJEDT':(TradeContext.BOJEDT).ljust(8,' '),\
                             'BOSPSQ':(TradeContext.BOSPSQ).ljust(12,' '),\
                             'OROCCAMT':(TradeContext.PRT_OROCCAMT),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close()
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    
    return True
