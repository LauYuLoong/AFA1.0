# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ĳ���).������ɸ�ʽ�鷢��
#===============================================================================
#   �����ļ�:   TRCC003_8513.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-06-15
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsGetFunc
import rccpsDBTrcc_hdcbka,rccpsDBTrcc_subbra
import rccpsMap8513CTradeContext2Dhdcbka


#=====================����ǰ����(���ز���,����ǰ����)===========================
def SubModuleDoFst():
    #=================������ɸ�ʽ����============================================
    
    if not TradeContext.existVariable('BOJEDT'):
        return AfaFlowControl.ExitThisFlow("S999", "���ڲ���Ϊ��")
    
    if not TradeContext.existVariable('RCVBNKCO'):
        return AfaFlowControl.ExitThisFlow("S999", "�������кŲ���Ϊ��")
        
    #=================�Ǽǻ�����ɸ�ʽ����Ϣ============================================
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽǻ��ҵ���ѯ����Ϣ")
    
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate
    #=====������ 20080701 ���ӻ��ҵ���ѯ�鸴�Ǽǲ���Ϣ====
    TradeContext.TRCNO    = TradeContext.SerialNo        #������ˮ��
    
    hdcbka_insert_dict = {}
    if not rccpsMap8513CTradeContext2Dhdcbka.map(hdcbka_insert_dict):
        return AfaFlowControl.ExitThisFlow("S999", "Ϊ���ҵ���ѯ�鸴�Ǽǲ���ֵ�쳣")
    
    #AfaLoggerFunc.tradeInfo(hdcbka_insert_dict)  
    ret = rccpsDBTrcc_hdcbka.insertCmt(hdcbka_insert_dict)
    
    if ret <= 0:
        return AfaFlowControl.ExitThisFlow("S999", "�Ǽǻ��ҵ�����ɸ�ʽ��Ϣ�쳣")
    
    AfaLoggerFunc.tradeInfo(">>>�����Ǽǻ��ҵ���ѯ����Ϣ")
    
    
    #=================Ϊ��Ҳ�ѯ�鱨�ĸ�ֵ======================================
    AfaLoggerFunc.tradeInfo(">>>��ʼΪ��Ҳ�ѯ�鱨�ĸ�ֵ")
    
    TradeContext.TRCCO      = '9900513'
    TradeContext.MSGTYPCO   = 'SET008'
    TradeContext.SNDBRHCO   = TradeContext.BESBNO
    TradeContext.SNDCLKNO   = TradeContext.BETELR
    TradeContext.SNDTRDAT   = TradeContext.BJEDTE
    TradeContext.SNDTRTIM   = TradeContext.BJETIM
    #TradeContext.MSGFLGNO   = TradeContext.SNDSTLBIN + TradeContext.TRCDAT + TradeContext.SerialNo
    TradeContext.ORMFN      = hdcbka_insert_dict['SNDMBRCO'] + hdcbka_insert_dict['TRCDAT'] + hdcbka_insert_dict['TRCNO']
    TradeContext.NCCWKDAT   = TradeContext.NCCworkDate
    TradeContext.OPRTYPNO   = '99'
    TradeContext.ROPRTPNO   = '20'
    TradeContext.TRANTYP    = '0'
    #TradeContext.TRCDAT     = TradeContext.BOJEDT
    TradeContext.TRCNO      = TradeContext.SerialNo
    
    
    AfaLoggerFunc.tradeInfo(">>>����Ϊ������ɸ�ʽ�鱨�ĸ�ֵ")
    AfaLoggerFunc.tradeInfo('�����н������ڣ�'+TradeContext.SNDTRDAT)
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).������ɸ�ʽ�鷢��[TRC003_8513]�˳�***' )
    
    return True


#=====================���׺���================================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���Ĳ���).������ɸ�ʽ�鷢��[TRC003_8513]����***' )
    
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
    
    
    #=====���ɴ�ӡ�ı�====
    AfaLoggerFunc.tradeInfo("��ʼ���ɴ�ӡ�ı�")
    txt = """\
            
            
                               %(BESBNM)s���ɸ�ʽ��
                               
        |-----------------------------------------------------------------------------|
        | ����:          |      %(BJEDTE)s                                              |
        |-----------------------------------------------------------------------------|
        | ���ɸ�ʽ���:  |      %(BSPSQN)s                                          |
        |-----------------------------------------------------------------------------|
        | �������к�:    |      %(SNDBNKCO)s                                            |
        |-----------------------------------------------------------------------------|
        | �������к�:    |      %(RCVBNKCO)s                                            |
        |-----------------------------------------------------------------------------|
        | ����:          |                                                            |
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
    
    file_name = 'rccps_' + TradeContext.BJEDTE + '_' + TradeContext.BSPSQN + '_8513'
    
    out_file = open(os.environ['AFAP_HOME'] + '/tmp/' + file_name,"wb")
    
    if out_file == None:
        return AfaFlowControl.ExitThisFlow("S999", "���ɴ�ӡ�ļ��쳣")
    
    print >> out_file,txt % {'BESBNM':(sub['BESBNM']).ljust(10,' '),\
                             'BJEDTE':(TradeContext.BJEDTE).ljust(8,' '),\
                             'BSPSQN':(TradeContext.BSPSQN).ljust(12,' '),\
                             'SNDBNKCO':(TradeContext.SNDBNKCO).ljust(10,' '),\
                             'RCVBNKCO':(TradeContext.RCVBNKCO).ljust(10,' '),\
                             'CONT1':(TradeContext.CONT[:68]).ljust(68,' '),\
                             'CONT2':(TradeContext.CONT[68:138]).ljust(70,' '),\
                             'CONT3':(TradeContext.CONT[138:208]).ljust(70,' '),\
                             'CONT4':(TradeContext.CONT[208:]).ljust(70,' ')}
    
    out_file.close
    
    TradeContext.PBDAFILE = file_name
    
    AfaLoggerFunc.tradeInfo("�������ɴ�ӡ�ı�")
    
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���Ĳ���).������ɸ�ʽ�鷢��[TRC003_8513]�˳�***' )
    
    return True
    
