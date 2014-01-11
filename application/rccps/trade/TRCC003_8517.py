# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Ʊ�鸴��¼��
#===============================================================================
#   �����ļ�:   TRCC003_8517.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �˹�ͨ
#   �޸�ʱ��:   2008-08-01
################################################################################

import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc,os
import rccpsDBTrcc_hpcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_bilbka,rccpsDBTrcc_bilinf,rccpsMap8517CTradeContext2Dhpcbka_dict

#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("�����Ʊ�鸴��¼�� 1.���ز��� ")
    
    #=====��ѯ��Ʊ��ѯ�鸴�Ǽǲ�====
    where_dict_hpcbka = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
    res_hpcbka = rccpsDBTrcc_hpcbka.selectu(where_dict_hpcbka)
    if( res_hpcbka == None ):
        return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊ��ѯ�鸴�Ǽǲ�ʧ��")
        
    if( len(res_hpcbka) == 0 ):
        return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊ��ѯ�鸴�Ǽǲ����Ϊ��")
        
    if( res_hpcbka['ISDEAL'] == PL_ISDEAL_ISDO ):
        return AfaFlowControl.ExitThisFlow("S999", "�˱ʲ�ѯ�ѱ��鸴����")
    
#    #=====��ѯ��Ʊҵ��Ǽǲ�====
#    where_dict_bilbka = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
#    res_bilbka = rccpsDBTrcc_bilbka.selectu(where_dict_bilbka)
#    if( res_bilbka == None ):
#        return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊҵ��ʧ��")
#        
#    if( len(res_bilbka) == 0 ):
#        return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊҵ����Ϊ��")
#        
#    #=====��ѯ��Ʊ��Ϣ�Ǽǲ�====
#    where_dict_bilinf = {'BILVER':res_bilbka['BILVER'],'BILNO':res_bilbka['BILNO'],'BILRS':res_bilbka['BILRS']}
#    res_bilinf = rccpsDBTrcc_bilinf.selectu(where_dict_bilinf)
#    if( res_bilinf == None ):
#        return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊ��Ϣʧ��")
#        
#    if( len(res_bilinf) == 0 ):
#        return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊ��Ϣ���Ϊ��")
        
#    AfaLoggerFunc.tradeInfo("RCVSTLBIN="+TradeContext.RCVSTLBIN)
#    AfaLoggerFunc.tradeInfo("RCVBNKCO="+TradeContext.RCVBNKCO)
    AfaLoggerFunc.tradeInfo("RCVBNKNM="+TradeContext.RCVBNKNM)
    
    #=====�Ǽǻ�Ʊ�鸴����Ϣ====
    TradeContext.BRSFLG   = PL_BRSFLG_SND
#    TradeContext.BESBNO   = res_hpcbka['BESBNO']
#    TradeContext.BETELR   = res_hpcbka['BETELR']
#    TradeContext.BEAUUS   = res_hpcbka['BEAUUS']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.TRCCO    = '9900527'
    TradeContext.TRCDAT   = TradeContext.BJEDTE
    TradeContext.TRCNO    = TradeContext.SerialNo
#    TradeContext.SNDBNKCO = 
#    TradeContext.SNDBNKNM = 
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
#    TradeContext.RCVBNKCO = res_hpcbka['SNDBNKCO']
#    TradeContext.RCVBNKNM = res_hpcbka['SNDBNKNM']
    TradeContext.ORTRCCO  = '9900526'
    TradeContext.BILVER   = res_hpcbka['BILVER']
    TradeContext.BILNO    = res_hpcbka['BILNO']
    TradeContext.BILDAT   = res_hpcbka['BILDAT']
    TradeContext.PAYWAY   = res_hpcbka['PAYWAY']
    TradeContext.CUR      = res_hpcbka['CUR']
    TradeContext.BILAMT   = str(res_hpcbka['BILAMT'])
    TradeContext.PYRACC   = res_hpcbka['PYRACC']
    TradeContext.PYRNAM   = res_hpcbka['PYRNAM']
    TradeContext.PYEACC   = res_hpcbka['PYEACC']
    TradeContext.PYENAM   = res_hpcbka['PYENAM']
#    TradeContext.CONT     = res_hpcbka['CONT']
    TradeContext.ISDEAL   = PL_ISDEAL_ISDO
    TradeContext.PRCCO    = ""
    TradeContext.BILENDDT = ""
    
    TradeContext.PRT_BILAMT = res_hpcbka['BILAMT']
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if len(TradeContext.BILNO) == 16:
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============

    hpcbka_insert_dict = {}
    if not rccpsMap8517CTradeContext2Dhpcbka_dict.map(hpcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ��Ʊ��ѯ�鸴�ǼǱ���ֵʧ��")
        
    ret = rccpsDBTrcc_hpcbka.insertCmt(hpcbka_insert_dict)
    if( ret <= 0 ):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ��Ʊ��ѯ�鸴�ǼǱ���ֵ�쳣")
    
    AfaLoggerFunc.tradeInfo("�����Ǽǲ�ѯ����Ϣ")
    
    #=====���鸴���ĸ�ֵ====
    AfaLoggerFunc.tradeInfo("��ʼΪ��Ʊ�鸴�鱨�ĸ�ֵ")
    #=====����ͷ====
    TradeContext.MSGTYPCO = 'SET008'
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = '99'
    TradeContext.ROPRTPNO = '21'
    TradeContext.TRANTYP  = '0'
    #=====��չ����====
#    TradeContext.TRCCO    = 
#    TradeContext.SNDBNKCO = 
#    TradeContext.SNDBNKNM = 
#    TradeContext.RCVBNKCO = 
#    TradeContext.RCVBNKNM = 
#    TradeContext.TRCDAT   = 
#    TradeContext.TRCNO    = 
#    TradeContext.BILDAT   = 
#    TradeContext.BILNO    = 
#    TradeContext.BILVER   = 
#    TradeContext.PAYWAY   = 
#    TradeContext.CUR      = 
#    TradeContext.BILAMT   = 
#    TradeContext.PYRACC   = 
#    TradeContext.PYRNAM   = 
#    TradeContext.PYEACC   = 
#    TradeContext.PYENAM   = 
#    TradeContext.CONT     = 
    TradeContext.ORQYDAT  = TradeContext.BOJEDT
    TradeContext.OQTSBNK  = res_hpcbka['SNDBNKCO']
    TradeContext.OQTNO    = res_hpcbka['TRCNO']
    
    AfaLoggerFunc.tradeInfo("����Ϊ��Ʊ��ѯ�鱨�ĸ�ֵ")
    
    return True
    
    
#===================================================================
def SubModuleDoSnd(): 
    AfaLoggerFunc.tradeInfo("���뽻�׺���")
    #=====�ж�afe�Ƿ��ͳɹ�====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
        
    AfaLoggerFunc.tradeInfo('>>>���ͳɹ�')    
    
    #=====���»�Ʊ��ѯ�鸴�Ǽǲ��еĲ鸴��ʶ====
    update_where_dict = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
    update_dict = {'ISDEAL':PL_ISDEAL_ISDO}
    ret = rccpsDBTrcc_hpcbka.update(update_dict,update_where_dict)
    if( ret <= 0 ):
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
        
    AfaLoggerFunc.tradeInfo("��ʼ���ɴ�ӡ�ı�")
    
    txt = """\
            
            
                               %(BESBNM)s��Ʊ�鸴��
                               
        |-----------------------------------------------------------------------------|
        | �鸴����:     | %(BJEDTE)s                                                    |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8517'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")

    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'BILDAT':(TradeContext.BILDAT).ljust(8,' '),\
                             'BILAMT':(TradeContext.PRT_BILAMT),\
                             'BILNO':(TradeContext.BILNO).ljust(16,' '),\
                             'PYRACC':(TradeContext.PYRACC).ljust(32,' '),\
                             'PYRNAM':(TradeContext.PYRNAM).ljust(60,' '),\
                             'PYEACC':(TradeContext.PYEACC).ljust(32,' '),\
                             'PYENAM':(TradeContext.PYENAM).ljust(60,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    AfaLoggerFunc.tradeInfo("�������׺���")
    
    return True