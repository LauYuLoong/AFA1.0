# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).ͨ��ͨ�Ҳ�ѯ�鷢��
#===============================================================================
#   �����ļ�:   TRCC003_8583.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �˹�ͨ
#   �޸�ʱ��:   2008-10-29
################################################################################

import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra,rccpsDBTrcc_wtrbka
import rccpsMap8583CTradeContext2Dhdcbka_dict

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.ͨ��ͨ�Ҳ�ѯ�鷢��[8582] ����")
    
    AfaLoggerFunc.tradeInfo("����ǰ����(���ز���,����ǰ����)")
    
    #=====��ѯԭ������Ϣ====
    AfaLoggerFunc.tradeInfo("��ѯԭ������Ϣ")
    if not TradeContext.existVariable('BOSPSQ'):
        return AfaFlowControl.ExitThisFlow('A099','û��ԭ�������')
        
    if not TradeContext.existVariable('BOJEDT'):
        return AfaFlowControl.ExitThisFlow("A099", "û��ԭ��������")
    
    #=====��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�====
    AfaLoggerFunc.tradeInfo("��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�")
    wtrbka_record = {}
    res = rccpsDBFunc.getTransWtr(TradeContext.BOJEDT,TradeContext.BOSPSQ,wtrbka_record)
    if( res == False ):
        return AfaFlowControl.ExitThisFlow('A099','��ѯԭ������Ϣʧ��')
        
    #=====�Ǽǲ�ѯ�鸴���ɸ�ʽ�Ǽǲ�====
    AfaLoggerFunc.tradeInfo("�Ǽǲ�ѯ�鸴�����ɸ�ʽ�ǲ�")
    TradeContext.BRSFLG   = PL_BRSFLG_SND 
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.TRCCO    = '9900511'
#    TradeContext.TRCDAT   = ''
    TradeContext.TRCNO    = TradeContext.SerialNo
#    TradeContext.SNDBNKCO = 
#    TradeContext.SNDBNKNM = 
#    TradeContext.RCVBNKCO = 
#    TradeContext.RCVBNKNM = 
#    TradeContext.BOJEDT   = 
#    TradeContext.BOSPSQ   = 
    TradeContext.ORTRCCO  = wtrbka_record['TRCCO']
    TradeContext.CUR      = wtrbka_record['CUR']
    TradeContext.OCCAMT   = str(wtrbka_record['OCCAMT'])
#    TradeContext.CONT     = 
    TradeContext.PYRACC   = wtrbka_record['PYRACC']
    TradeContext.PYEACC   = wtrbka_record['PYEACC']
    TradeContext.ISDEAL   = PL_ISDEAL_UNDO
#    TradeContext.PRCCO    = 

    #=====�������ֵ丳ֵ====
    AfaLoggerFunc.tradeInfo("�������ֵ丳ֵ")
    hdcbka_insert_dict = {}
    if not rccpsMap8583CTradeContext2Dhdcbka_dict.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow('A099','�������ֵ丳ֵʧ��') 
    
    #=====�Ǽ����ݿ�====
    AfaLoggerFunc.tradeInfo("�Ǽ����ݿ�")
    res = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    if( res == -1 ):
        return AfaFlowControl.ExitThisFlow('A099','�������ֵ丳ֵʧ��') 
    
    #=====��ʼ����ѯ�鱨�ĸ�ֵ====
    AfaLoggerFunc.tradeInfo("��ʼ����ѯ�鱨�ĸ�ֵ")
    #====����ͷ====
    TradeContext.MSGTYPCO = 'SET008'
    TradeContext.RCVMBRCO = TradeContext.RCVSTLBIN
    TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
    TradeContext.SNDBRHCO = TradeContext.BESBNO
    TradeContext.SNDCLKNO = TradeContext.BETELR
    TradeContext.SNDTRDAT = TradeContext.BJEDTE
    TradeContext.SNDTRTIM = TradeContext.BJETIM
    TradeContext.MSGFLGNO = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN    = wtrbka_record['SNDMBRCO'] + wtrbka_record['TRCDAT'] + wtrbka_record['TRCNO']
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO = "99"
    TradeContext.ROPRTPNO = "30"
    TradeContext.TRANTYP  = "0"
    #=====ҵ��Ҫ�ؼ�====
    TradeContext.TRCCO    = "9900511"
#    TradeContext.SNDBNKCO = ""
#    TradeContext.SNDBNKNM = ""
#    TradeContext.RCVBNKCO = ""
#    TradeContext.RCVBNKNM = ""
#    TradeContext.TRCDAT   = ""
#    TradeContext.TRCNO    = ""
    TradeContext.ORTRCCO  = wtrbka_record['TRCCO']
    TradeContext.ORTRCDAT = wtrbka_record['TRCDAT']
    TradeContext.ORTRCNO  = wtrbka_record['TRCNO']
    TradeContext.ORSNDBNK = wtrbka_record['SNDBNKCO']
    TradeContext.ORRCVBNK = wtrbka_record['RCVBNKCO']
    if( wtrbka_record['CUR'] == '01' ):
        TradeContext.ORCUR = 'CNY'
    else:
        TradeContext.ORCUR = wtrbka_record['CUR']
    TradeContext.OROCCAMT = str(wtrbka_record['OCCAMT'])
#    TradeContext.CONT     = ""

    AfaLoggerFunc.tradeInfo("����ǰ����(���ز���,����ǰ����) �˳�")
    
    return True
    
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo("���׺���")
    
    #=====�ж�afe�Ƿ��ͳɹ�====
    AfaLoggerFunc.tradeInfo("�ж�afe�Ƿ��ͳɹ�")
    if TradeContext.errorCode != '0000':
        AfaLoggerFunc.tradeInfo("�ж�afe����ʧ��")
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo("�ж�afe���ͳɹ�")    
    #=====��ѯ������====
    AfaLoggerFunc.tradeInfo("��ѯ������")
    subbra_dict={'BESBNO':TradeContext.BESBNO}
    sub=rccpsDBTrcc_subbra.selectu(subbra_dict)
    if(sub==None):
        return AfaFlowControl.ExitThisFlow('A099','��ѯ������ʧ��' )
        
    if(len(sub)==0):
        return AfaFlowControl.ExitThisFlow('A099','û����Ӧ�Ļ�����' )
    
    #=================���ɴ�ӡ�ı�=============================================
    AfaLoggerFunc.tradeInfo("��ʼ���ɴ�ӡ�ı�")
    
    txt = """\
            
            
                               %(BESBNM)sͨ��ͨ�Ҳ�ѯ��
                               
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
                             'OROCCAMT':float((TradeContext.OROCCAMT)),\
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
    
    AfaLoggerFunc.tradeInfo("���׺��� �˳�")
    
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.ͨ��ͨ�Ҳ�ѯ�鷢��[8582] �˳�")
    
    return True