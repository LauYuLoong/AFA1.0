# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.֧��ҵ��״̬��ѯ
#=================================================================
#   �����ļ�:   TRCC003_8529.py
#   �޸�ʱ��:   2008-06-05
#   �޸���  ��  ������
#   �޸�ʱ�䣺  2008-07-02
##################################################################
#   �޸�ʱ�䣺  2008-08-07
#   �޸����ݣ�  ���ӻ�Ʊ���ֵ�ҵ��
#   �޸���  ��  �˹�ͨ
##################################################################
#   �޸�ʱ�䣺  2008-10-24
#   �޸����ݣ�  ����ͨ��ͨ�Ҳ���
#   �޸���  ��  �˹�ͨ
##################################################################
import rccpsDBTrcc_ztcbka,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc,rccpsDBFunc
import rccpsDBTrcc_trcbka,rccpsDBTrcc_wtrbka,rccpsMap8529Dtrcbka_dict2Dztcbka_dict,rccpsMap8529Dbilbka2Dztcbka
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( "�����ѯ ")
    #=====�жϽӿ��Ƿ����====
    if( not TradeContext.existVariable( "BOJEDT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '�ޱ�������,����ʧ��')
    if( not TradeContext.existVariable( "BOSPSQ" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '�޽������,����ʧ��')
    if( not TradeContext.existVariable( "CONT" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '�޲�ѯ����,����ʧ��')
    
    #=====�ж�ҵ������=====
    AfaLoggerFunc.tradeInfo("��ʼ�ж�ҵ������")
    
    if( TradeContext.OPRTYPNO == '20' ):    #���
        AfaLoggerFunc.tradeInfo("�����Ҵ���")
            
        #=====��ѯ���ݿ�====
        trcbka_dict = {}
        res=rccpsDBFunc.getTransTrc(TradeContext.BOJEDT,TradeContext.BOSPSQ,trcbka_dict)
        if(res==False):
            return AfaFlowControl.ExitThisFlow('S999','���ݿ����޼�¼') 
        
        #=====������ 2008-07-21 ���������˱�־�ж�====
        if trcbka_dict['BRSFLG']  ==  PL_BRSFLG_RCV:
            return AfaFlowControl.ExitThisFlow('S999','������ҵ������˲���')
        
        ztcbka_dict={}
        #=====���ò����ֵ�====
        if not rccpsMap8529Dtrcbka_dict2Dztcbka_dict.map(trcbka_dict,ztcbka_dict):
            return AfaFlowControl.ExitThisFlow('M999','�ֵ丳ֵ����')
 
        ztcbka_dict['CONT']=TradeContext.CONT   #�ֹ���ӵ��ֶ�
        #=====������ 20080702 �޸Ľ������ںͱ������====
        ztcbka_dict['BJEDTE']   =  TradeContext.BJEDTE
        ztcbka_dict['BSPSQN']   =  TradeContext.BSPSQN
        ztcbka_dict['ORTRCCO']  =  ztcbka_dict['TRCCO']
        ztcbka_dict['NCCWKDAT'] =  TradeContext.NCCworkDate
        ztcbka_dict['TRCCO']    =  "9900506"             #9900506 ֹ��ҵ��״̬��ѯ
        ztcbka_dict['TRCNO']    =  TradeContext.SerialNo
        ztcbka_dict['SNDMBRCO'] =  TradeContext.SNDSTLBIN
        ztcbka_dict['RCVMBRCO'] =  TradeContext.RCVSTLBIN
        ztcbka_dict['ISDEAL']   =  PL_ISDEAL_UNDO
        ztcbka_dict['BOJEDT']   =  TradeContext.BOJEDT
        ztcbka_dict['BOSPSQ']   =  TradeContext.BOSPSQ
    
        AfaLoggerFunc.tradeInfo("ztcbka_dict:"+str(ztcbka_dict))
        
        #=====�������ݿ�====
        AfaLoggerFunc.tradeInfo("��ʼ�������ݿ�")
        #=====������ 20080702 �޸�insert_dictΪztcbka_dict====
        rowcount=rccpsDBTrcc_ztcbka.insertCmt(ztcbka_dict)
        if(rowcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','�������ݿ�ʧ��' )
    
        #=====������ 20080702 ��������ũ���������ֶ�====
        TradeContext.ORTRCCO  = ztcbka_dict['ORTRCCO']
        TradeContext.ORTRCDAT = ztcbka_dict['TRCDAT']
        TradeContext.ORTRCNO  = ztcbka_dict['TRCNO']
        TradeContext.ORSNDBNK = ztcbka_dict['SNDBNKCO']
        TradeContext.ORRCVBNK = ztcbka_dict['RCVBNKCO']
        TradeContext.OROCCAMT = str(ztcbka_dict['OCCAMT'])
        #TradeContext.OPRTYPNO = TradeContext.OPRTYPNO[0:2]
        TradeContext.OPRTYPNO = '99'
        TradeContext.ROPRTPNO = TradeContext.ORTRCCO[0:2]
        
        
    elif( TradeContext.OPRTYPNO == '21' ):    #��Ʊ
        AfaLoggerFunc.tradeInfo("�����Ʊ����")
        
        #=====��ѯ���ݿ�====
        bilbka_dict = {}
        res = rccpsDBFunc.getTransBil(TradeContext.BOJEDT,TradeContext.BOSPSQ,bilbka_dict)
        if( res == False ):
            return AfaFlowControl.ExitThisFlow('S999','���ݿ����޼�¼')
            
        #=====�ж�������־====
        if( bilbka_dict['BRSFLG'] == PL_BRSFLG_RCV ):
            return AfaFlowControl.ExitThisFlow('S999','������ҵ������˲���')
        
        #=====��ѯ��Ʊ��Ϣ�Ǽǲ�====
        bilinf_dict = {}
        ret = rccpsDBFunc.getInfoBil(bilbka_dict['BILVER'],bilbka_dict['BILNO'],bilbka_dict['BILRS'],bilinf_dict)
        if( ret == False ):
            return AfaFlowControl.ExitThisFlow('S999','��Ʊ��Ϣ�Ǽǲ����޼�¼')
        
        #=====�������ֵ丳ֵ====
#        ztcbka_dict={}
#        if not rccpsMap8529Dbilbka2Dztcbka.map(bilbka_dict,ztcbka_dict):
#            return AfaFlowControl.ExitThisFlow('M999','�ֵ丳ֵ����')
        AfaLoggerFunc.tradeInfo("��ʼ�������ֵ丳ֵ")
        ztcbka_dict = {}
        
        ztcbka_dict['BJEDTE']   = TradeContext.BJEDTE
        ztcbka_dict['BSPSQN']   = TradeContext.BSPSQN
        ztcbka_dict['BRSFLG']   = PL_BRSFLG_SND
        ztcbka_dict['BESBNO']   = TradeContext.BESBNO
        ztcbka_dict['BEACSB']   = ""
        ztcbka_dict['BETELR']   = TradeContext.BETELR
        ztcbka_dict['BEAUUS']   = ""
        ztcbka_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        ztcbka_dict['TRCCO']    = '9900506'
        ztcbka_dict['TRCDAT']   = TradeContext.TRCDAT
        ztcbka_dict['TRCNO']    = TradeContext.SerialNo
        ztcbka_dict['SNDMBRCO'] = bilbka_dict['SNDMBRCO']
        ztcbka_dict['RCVMBRCO'] = bilbka_dict['RCVMBRCO']
        ztcbka_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        ztcbka_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        ztcbka_dict['RCVBNKCO'] = bilbka_dict['RCVBNKCO']
        ztcbka_dict['RCVBNKNM'] = bilbka_dict['RCVBNKNM']
        ztcbka_dict['BOJEDT']   = bilbka_dict['BJEDTE']
        ztcbka_dict['BOSPSQ']   = bilbka_dict['BSPSQN']
        ztcbka_dict['ORTRCCO']  = bilbka_dict['TRCCO']
        ztcbka_dict['CUR']      = bilinf_dict['CUR']
        #=====�ж�ҵ��״̬====
        if( bilbka_dict['HPSTAT'] == PL_HPSTAT_PAYC ):  #�⸶
            ztcbka_dict['OCCAMT'] = bilinf_dict['OCCAMT']
        else:
            ztcbka_dict['OCCAMT'] = bilinf_dict['BILAMT']
        ztcbka_dict['CONT']     = TradeContext.CONT
        ztcbka_dict['NCCTRCST'] = ""
        ztcbka_dict['MBRTRCST'] = ""
        ztcbka_dict['ISDEAL']   = PL_ISDEAL_UNDO
        ztcbka_dict['PRCCO']    = ""
        ztcbka_dict['STRINFO']  = ""
        ztcbka_dict['NOTE1']    = bilbka_dict['NOTE1']
        ztcbka_dict['NOTE2']    = bilbka_dict['NOTE2']
        ztcbka_dict['NOTE3']    = bilbka_dict['NOTE3']
        ztcbka_dict['NOTE4']    = bilbka_dict['NOTE4']
        
        AfaLoggerFunc.tradeInfo("OCCAMT="+str(bilinf_dict['OCCAMT']))
        
        #=====�Ǽ�ҵ��״̬��ѯ�鸴�Ǽǲ�====
        AfaLoggerFunc.tradeInfo("��ʼ����ҵ��״̬��ѯ�鸴�Ǽǲ�")
        rowcount=rccpsDBTrcc_ztcbka.insertCmt(ztcbka_dict)
        if(rowcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','�������ݿ�ʧ��' )
            
        #=====��ҵ��״̬��ѯ���ĸ�ֵ====
        AfaLoggerFunc.tradeInfo("��ʼ��ҵ��״̬��ѯ���ĸ�ֵ")
        #=====����ͷ====
        TradeContext.NCCWKDAT = TradeContext.NCCworkDate
        TradeContext.RCVMBRCO = bilbka_dict['RCVMBRCO']
        TradeContext.RCVSTLBIN = bilbka_dict['RCVMBRCO']
        TradeContext.SNDSTLBIN = TradeContext.SNDSTLBIN
        TradeContext.SNDMBRCO = TradeContext.SNDSTLBIN
        TradeContext.SNDBRHCO = TradeContext.BESBNO
        TradeContext.SNDCLKNO = TradeContext.BETELR
#        TradeContext.SNDTRDAT = TradeContext.BJEDTE
#        TradeContext.SNDTRTIM = TradeContext.BJETIM
        TradeContext.ORMFN    = TradeContext.RCVSTLBIN+TradeContext.BJEDTE+TradeContext.SerialNo
        TradeContext.OPRTYPNO = '99'
        TradeContext.ROPRTPNO = '21'
        TradeContext.TRANTYP  = '0'
        #=====ҵ��Ҫ�ؼ�====
        TradeContext.TRCCO    = '9900506'
#        TradeContext.SNDBNKCO = 
#        TradeContext.SNDBNKNM = 
        TradeContext.RCVBNKCO = bilbka_dict['RCVBNKCO']
        TradeContext.RCVBNKNM = bilbka_dict['RCVBNKNM']
        TradeContext.TRCDAT   = TradeContext.BJEDTE
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.ORTRCCO  = bilbka_dict['TRCCO']
        TradeContext.ORTRCDAT = bilbka_dict['TRCDAT']
        TradeContext.ORTRCNO  = bilbka_dict['TRCNO']
        TradeContext.ORSNDBNK = bilbka_dict['SNDBNKCO']
        TradeContext.ORRCVBNK = bilbka_dict['RCVBNKCO']
        TradeContext.ORCUR    = bilinf_dict['CUR']        #11
        TradeContext.OROCCAMT = str(bilinf_dict['OCCAMT'])
        
        AfaLoggerFunc.tradeInfo("֧��ҵ��״̬��ѯ����Ʊ�������")
        
    #=====ͨ��ͨ��=====
    elif( TradeContext.OPRTYPNO == '30' ):
        AfaLoggerFunc.tradeInfo("��ʼͨ��ͨ�Ҵ���")
        
        #=====�ж�Ҫ��ѯ�Ľ����Ƿ�Ϊ���ս���====
        if( TradeContext.BOJEDT != TradeContext.BJEDTE ):
            return AfaFlowControl.ExitThisFlow('A009','ԭ���ײ��ǵ��ս���')
        
        #=====��ѯͨ��ͨ��ҵ��Ǽǲ�====
        AfaLoggerFunc.tradeInfo("��ѯͨ��ͨ��ҵ��Ǽǲ�")
        where_dict = {'BJEDTE':TradeContext.BOJEDT,'BSPSQN':TradeContext.BOSPSQ}
        wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
        if( wtrbka_dict == None ):
            return AfaFlowControl.ExitThisFlow('A009','��ѯͨ��ͨ��ҵ��Ǽǲ�ʧ��')
            
        if( len(wtrbka_dict) == 0 ):
            return AfaFlowControl.ExitThisFlow('A009','��ѯͨ��ͨ��ҵ��Ǽǲ����Ϊ��') 
            
        #=====�ж�Ҫ��ѯ�Ľ����Ƿ��Ǳ����������====
        AfaLoggerFunc.tradeInfo("�ж�Ҫ��ѯ�Ľ����Ƿ��Ǳ����������")
        if( wtrbka_dict['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('A009','Ҫ��ѯ�Ľ��ײ��Ǳ����������') 
            
        #=====�Ǽ�ҵ��״̬��ѯ�鸴�Ǽǲ�====
        AfaLoggerFunc.tradeInfo("�Ǽ�ҵ��״̬��ѯ�鸴�Ǽǲ�")
        
        #=====�������ֵ丳ֵ====
        AfaLoggerFunc.tradeInfo("�������ֵ丳ֵ")
        ztcbka_dict = {}
        ztcbka_dict['BJEDTE']   = TradeContext.BJEDTE
        ztcbka_dict['BSPSQN']   = TradeContext.BSPSQN
        ztcbka_dict['BRSFLG']   = PL_BRSFLG_SND
        ztcbka_dict['BESBNO']   = TradeContext.BESBNO
        ztcbka_dict['BEACSB']   = ""
        ztcbka_dict['BETELR']   = TradeContext.BETELR
        ztcbka_dict['BEAUUS']   = ""
        ztcbka_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        ztcbka_dict['TRCCO']    = '9900506'
        ztcbka_dict['TRCDAT']   = TradeContext.TRCDAT
        ztcbka_dict['TRCNO']    = TradeContext.SerialNo
        ztcbka_dict['SNDMBRCO'] = wtrbka_dict['SNDMBRCO']
        ztcbka_dict['RCVMBRCO'] = wtrbka_dict['RCVMBRCO']
        ztcbka_dict['SNDBNKCO'] = TradeContext.SNDBNKCO
        ztcbka_dict['SNDBNKNM'] = TradeContext.SNDBNKNM
        ztcbka_dict['RCVBNKCO'] = wtrbka_dict['RCVBNKCO']
        ztcbka_dict['RCVBNKNM'] = wtrbka_dict['RCVBNKNM']
        ztcbka_dict['BOJEDT']   = wtrbka_dict['BJEDTE']
        ztcbka_dict['BOSPSQ']   = wtrbka_dict['BSPSQN']
        ztcbka_dict['ORTRCCO']  = wtrbka_dict['TRCCO']
        ztcbka_dict['CUR']      = wtrbka_dict['CUR']
        ztcbka_dict['OCCAMT']   = wtrbka_dict['OCCAMT']
        ztcbka_dict['CONT']     = TradeContext.CONT
        ztcbka_dict['NCCTRCST'] = ""
        ztcbka_dict['MBRTRCST'] = ""
        ztcbka_dict['ISDEAL']   = PL_ISDEAL_UNDO
        ztcbka_dict['PRCCO']    = ""
        ztcbka_dict['STRINFO']  = ""
        ztcbka_dict['NOTE1']    = wtrbka_dict['NOTE1']
        ztcbka_dict['NOTE2']    = wtrbka_dict['NOTE2']
        ztcbka_dict['NOTE3']    = wtrbka_dict['NOTE3']
        ztcbka_dict['NOTE4']    = wtrbka_dict['NOTE4']
        
        AfaLoggerFunc.tradeInfo("��ʼ����ҵ��״̬��ѯ�鸴�Ǽǲ�")
        rowcount=rccpsDBTrcc_ztcbka.insertCmt(ztcbka_dict)
        if(rowcount==-1):
            return AfaFlowControl.ExitThisFlow('A099','�������ݿ�ʧ��' )
        
        #=====��ʼ��Ҳ��״̬��ѯ���ĸ�ֵ====
        #=====����ͷ====
        TradeContext.MSGTYPCO  = "SET008"
        TradeContext.NCCWKDAT  = TradeContext.NCCworkDate
        TradeContext.RCVMBRCO  = wtrbka_dict['RCVMBRCO']
        TradeContext.RCVSTLBIN = wtrbka_dict['RCVMBRCO']
        TradeContext.SNDSTLBIN = TradeContext.SNDSTLBIN
        TradeContext.SNDMBRCO  = TradeContext.SNDSTLBIN
        TradeContext.SNDBRHCO  = TradeContext.BESBNO
        TradeContext.SNDCLKNO  = TradeContext.BETELR
#        TradeContext.SNDTRDAT  = TradeContext.BJEDTE
#        TradeContext.SNDTRTIM  = TradeContext.BJETIM
        TradeContext.ORMFN     = wtrbka_dict['MSGFLGNO']
        TradeContext.OPRTYPNO  = '99'
        TradeContext.ROPRTPNO  = '30'
        TradeContext.TRANTYP   = '0'
        #=====ҵ��Ҫ�ؼ�====
        TradeContext.TRCCO    = '9900506'
#        TradeContext.SNDBNKCO = 
#        TradeContext.SNDBNKNM = 
        TradeContext.RCVBNKCO = wtrbka_dict['RCVBNKCO']
        TradeContext.RCVBNKNM = wtrbka_dict['RCVBNKNM']
#        TradeContext.TRCDAT   = TradeContext.BJEDTE
        TradeContext.TRCNO    = TradeContext.SerialNo
        TradeContext.ORTRCCO  = wtrbka_dict['TRCCO']
        TradeContext.ORTRCDAT = wtrbka_dict['TRCDAT']
        TradeContext.ORTRCNO  = wtrbka_dict['TRCNO']
        TradeContext.ORSNDBNK = wtrbka_dict['SNDBNKCO']
        TradeContext.ORRCVBNK = wtrbka_dict['RCVBNKCO']
        TradeContext.ORCUR    = wtrbka_dict['CUR']        #11
        TradeContext.OROCCAMT = str(wtrbka_dict['OCCAMT'])
#        TradeContext.CONT     = 
    else:
        return AfaFlowControl.ExitThisFlow('S999','ҵ�����ʹ���')
        
        
    return True

def SubModuleDoSnd():
    #=====�ж�errorCode====
    AfaLoggerFunc.tradeInfo("����ӿ�2")
    if TradeContext.errorCode != "0000":
        AfaLoggerFunc.tradeInfo("AFE����ʧ��")    
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
    
    AfaLoggerFunc.tradeInfo("AFE���ͳɹ�")    
    TradeContext.errorCode = '0000'
    TradeContext.errorMsg  = '���׳ɹ�'

    return True 
