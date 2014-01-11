# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).��Ʊ��ѯ��¼��
#===============================================================================
#   �����ļ�:   TRCC003_8516.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �˹�ͨ
#   �޸�ʱ��:   2008-08-01
################################################################################

import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc,os
import rccpsDBTrcc_hpcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_bilinf,rccpsDBTrcc_paybnk
import rccpsMap8516CTradeContext2Dhpcbka_dict

#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("�����Ʊ��ѯ��¼�� 1.���ز��� ")
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if TradeContext.BILVER == '02':
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    #=====��ѯ��Ʊ��Ϣ=====
#    where_dict_bilinf = {'BILVER':TradeContext.BILVER,'BILNO':TradeContext.BILNO,'BILRS':PL_BILRS_OUT}
#    res_bilinf = rccpsDBTrcc_bilinf.selectu(where_dict_bilinf)
#    if( res_bilinf == None ):
#        return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊ��Ϣʧ��")
#        
#    if( len(res_bilinf) == 0 ):
#        return AfaFlowControl.ExitThisFlow("S999", "��ѯ��Ʊ��ϢΪ��")
        

#    #=====��ѯ�����к�====
#    where_dict_paybnk = {'BANKBIN':TradeContext.BESBNO}
#    res_paybnk = rccpsDBTrcc_paybnk.selectu(where_dict_paybnk)
#    if( res_paybnk == None ):
#        return AfaFlowControl.ExitThisFlow("S999", "��ѯ�����к�ʧ��")
#        
#    if( len(res_paybnk) == 0 ):
#        return AfaFlowControl.ExitThisFlow("S999", "��ѯ�����к�Ϊ��")
#        
    #=====�Ǽǲ�ѯ����Ϣ====
    AfaLoggerFunc.tradeInfo("��ʼ�Ǽǲ�ѯ����Ϣ")
    
    TradeContext.BRSFLG      =  PL_BRSFLG_SND
    TradeContext.NCCWKDAT    =  TradeContext.NCCworkDate
    TradeContext.TRCNO       =  TradeContext.SerialNo
#    TradeContext.SNDBNKCO    =  TradeContext.BESBNO
#    TradeContext.SNDBNKNM    =  res_paybnk['BANKNAM']
#    TradeContext.RCVBNKCO    =  res_bilinf['PAYBNKCO']
#    TradeContext.RCVBNKNM    =  res_bilinf['PAYBNKNM']
    TradeContext.BOJEDT      =  ""
    TradeContext.BOSPSQ      =  ""
    TradeContext.ORTRCCO     =  ""
    #TradeContext.TRCDAT      =  TradeContext.BJEDTE
#    TradeContext.BILDAT      =  res_bilinf['BILDAT']
#    TradeContext.PAYWAY      =  res_bilinf['PAYWAY']
#    TradeContext.CUR         =  res_bilinf['CUR']
#    TradeContext.BILAMT      =  str(res_bilinf['BILAMT'])
#    TradeContext.PYRACC      =  res_bilinf['PYRACC']
#    TradeContext.PYRNAM      =  res_bilinf['PYRNAM']
#    TradeContext.PYEACC      =  res_bilinf['PYEACC']
#    TradeContext.PYENAM      =  res_bilinf['PYENAM']
    TradeContext.ISDEAL      =  PL_ISDEAL_UNDO
    TradeContext.PRCCO       =  ""
    TradeContext.SNDMBRCO    =  TradeContext.SNDSTLBIN
    TradeContext.RCVMBRCO    =  TradeContext.RCVSTLBIN

    hpcbka_insert_dict = {}
    if not rccpsMap8516CTradeContext2Dhpcbka_dict.map(hpcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ��Ʊ��ѯ�鸴�ǼǱ���ֵʧ��")
        
    ret = rccpsDBTrcc_hpcbka.insertCmt(hpcbka_insert_dict)
    if( ret <= 0 ):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ��Ʊ��ѯ�鸴�ǼǱ���ֵ�쳣")
    
    AfaLoggerFunc.tradeInfo("�����Ǽǲ�ѯ����Ϣ")
        
    #=====Ϊ��Ʊ��ѯ�鱨�ĸ�ֵ====
    AfaLoggerFunc.tradeInfo("��ʼΪ��Ʊ��ѯ�鱨�ĸ�ֵ")
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
    TradeContext.TRCCO    = '9900526'    
#    TradeContext.BILDAT   = res_bilinf['BILDAT']
#    TradeContext.BILAMT   = str(res_bilinf['BILAMT'])
    
    #=====��ǰ̨�ӿڸ�ֵ====
    TradeContext.BILENDDT = ""  #����ô����
    
    AfaLoggerFunc.tradeInfo("����Ϊ��Ʊ��ѯ�鱨�ĸ�ֵ")
    
    return True
    
#=====================���׺���================================================
def SubModuleDoSnd(): 
    AfaLoggerFunc.tradeInfo("���뽻�׺���")
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
            
            
                               %(BESBNM)s��Ʊ��ѯ��
                               
        |-----------------------------------------------------------------------------|
        | ��ѯ����:     | %(BJEDTE)s                                                    |
        |-----------------------------------------------------------------------------|
        | ��ѯ���:     | %(BSPSQN)s                                                |
        |-----------------------------------------------------------------------------|
        | �������к�:   | %(SNDBNKCO)s                                                  |
        |-----------------------------------------------------------------------------|
        | �������к�:   | %(RCVBNKCO)s                                                  |
        |-----------------------------------------------------------------------------|
        | ��Ʊ����:     | %(BILDAT)s                                                    |
        |-----------------------------------------------------------------------------|
        | ��Ʊ���:     | %(BILAMT)s                                             |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8516'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
    AfaLoggerFunc.tradeInfo(">>>>>>��ʼ��ֵ")
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'BILDAT':(TradeContext.BILDAT).ljust(8,' '),\
                             'BILAMT':(TradeContext.BILAMT).ljust(15,' '),\
                             'BILNO':(TradeContext.BILNO).ljust(16,' '),\
                             'PYRACC':(TradeContext.PYRACC).ljust(32,' '),\
                             'PYRNAM':(TradeContext.PYRNAM).ljust(60,' '),\
                             'PYEACC':(TradeContext.PYEACC).ljust(32,' '),\
                             'PYENAM':(TradeContext.PYENAM).ljust(60,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    AfaLoggerFunc.tradeInfo(">>>>>>������ֵ")
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    AfaLoggerFunc.tradeInfo("�������׺���")
    
    return True