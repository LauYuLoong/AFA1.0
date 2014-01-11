# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ.�������ݿ����ģ��
#===============================================================================
#   �����ļ�:   rccpsDBFunc.py
#   ��    ��:   �ر��
#   �޸�ʱ��:   2006-03-31
################################################################################

import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,TradeContext,AfaFlowControl
from types import *
from rccpsConst import *
import rccpsDBTrcc_trcbka,rccpsDBTrcc_bilbka,rccpsDBTrcc_bilinf,rccpsDBTrcc_errinf,rccpsDBTrcc_wtrbka,rccpsDBTrcc_mpcbka,rccpsDBTrcc_pamtbl
import rccpsState
import rccpsMap0000Dtrcbka2Dtrc_dict,rccpsMap0000Dstat_dict2Dtrc_dict
import rccpsMap0000Dtrc_dict2Dtrcbka
import rccpsMap0000Dbilbka2Dbil_dict,rccpsMap0000Dstat_dict2Dbil_dict
import rccpsMap0000Dbil_dict2Dbilbka    
import rccpsMap0000Dbilinf2Dbil_dict
import rccpsMap0000Dbil_dict2Dbilinf
import rccpsMap0000Dwtrbka2Dwtr_dict,rccpsMap0000Dstat_dict2Dwtr_dict,rccpsMap0000Dwtr_dict2Dwtrbka,rccpsMap0000Dmpcbka2Dmpc_dict

################################################################################
# ������:    getTransTrc                                             
# ����:      BJEDTE:��������(����),BSPSQN:�������(����)             
# ����ֵ��   �ɹ�    trc_dict(���ҵ������ϸ��Ϣ,��trcbka������+sstlog������)
#            ʧ��    False                                           
# ����˵���� ��ѯ���ҵ��Ǽǲ�����ǰ״̬�����Ϣ                    
################################################################################
                                                                     
def getTransTrc(BJEDTE,BSPSQN,trc_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ���ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
                                                                     
    #==========��֯��ѯ����=====================================================
    trcbka_where_dict = {'BJEDTE':BJEDTE,'BSPSQN':BSPSQN}            
                                                                     
    #==========��ѯ��ҵǼǲ����ҵ����Ϣ=======================================
    trcbka_dict = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict)  
    
    if trcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ѯ���ҵ��Ǽǲ�������Ϣ�쳣' )
        
    if len(trcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '���ҵ��Ǽǲ����޴˽�����Ϣ' )
    
    #==========����ѯ���Ļ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ�===================
    if not rccpsMap0000Dtrcbka2Dtrc_dict.map(trcbka_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ���Ļ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )
        
    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )
    
    stat_dict = {}
    
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dtrc_dict.map(stat_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ���ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True

################################################################################
# ������:    insTransTrc
# ����:      trc_dict(���ҵ������ϸ��Ϣ)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� �Ǽǻ��ҵ��Ǽǲ���״̬�����Ϣ
################################################################################
def insTransTrc(trc_dict):
    
    AfaLoggerFunc.tradeInfo( ">>>��ʼ�Ǽǻ��ҵ��Ǽǲ�[" + trc_dict["BJEDTE"] + "][" + trc_dict["BSPSQN"] + "]������Ϣ�����״̬" )
    
    if not trc_dict.has_key("BJEDTE"):
        return AfaFlowControl.ExitThisFlow( 'S999',"�Ǽǻ��ҵ��Ǽǲ�,BJEDTE����Ϊ��")
        
    if not trc_dict.has_key("BSPSQN"):
        return AfaFlowControl.ExitThisFlow( 'S999',"�Ǽǻ��ҵ��Ǽǲ�,BSPSQN����Ϊ��")
        
    
    #==========�������ֵ丳ֵ�����ҵ��Ǽǲ��ֵ�==============================
    trcbka_dict = {}
    
    if not rccpsMap0000Dtrc_dict2Dtrcbka.map(trc_dict,trcbka_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '�������ֵ丳ֵ�����ҵ��Ǽǲ��ֵ��쳣' )
        
    #==========�Ǽ���Ϣ����ҵǼǲ�============================================
    ret = rccpsDBTrcc_trcbka.insert(trcbka_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǻ��ҵ����ϸ��Ϣ�����ҵ��Ǽǲ��쳣' )
        
    AfaLoggerFunc.tradeInfo("����ɹ�")
    #==========�Ǽǳ�ʼ״̬====================================================
    if not rccpsState.newTransState(trc_dict["BJEDTE"],trc_dict["BSPSQN"],PL_BCSTAT_INIT,PL_BDWFLG_SUCC):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>�����Ǽǻ��ҵ��Ǽǲ�[" + trc_dict["BJEDTE"] + "][" + trc_dict["BSPSQN"] + "]������Ϣ�����״̬" )
    return True
    
    
################################################################################
# ������:    GetTransBil
# ����:      BJEDTE:��������(����),BSPSQN:�������(����)
# ����ֵ��   �ɹ�    bil_dict(��Ʊҵ������ϸ��Ϣ,��bilbka������+sstlog������)
#            ʧ��    False
# ����˵���� ��ѯ��Ʊҵ��Ǽǲ�����ǰ״̬�����Ϣ
################################################################################

def getTransBil(BJEDTE,BSPSQN,bil_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ��Ʊҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    
    #==========��֯��ѯ����=====================================================
    bilbka_where_dict = {'BJEDTE':BJEDTE,'BSPSQN':BSPSQN}

    #==========��ѯ��Ʊҵ��Ǽǲ����ҵ����Ϣ===================================
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    
    if bilbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ��Ʊҵ��Ǽǲ���ϸ��Ϣ�쳣' )
        
    if len(bilbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '���ҵ��Ǽǲ����޴˽�����ϸ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯ��Ʊҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )

    #==========����ѯ���Ļ�Ʊҵ��Ǽǲ����ҵ����Ϣ��ֵ������ֵ�===============
    if not rccpsMap0000Dbilbka2Dbil_dict.map(bilbka_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ���Ļ�Ʊҵ��Ǽǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )

    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰҵ��״̬" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰҵ��״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dbil_dict.map(stat_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ��Ʊҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True

################################################################################
# ������:    insTransBil
# ����:      bil_dict(��Ʊҵ������ϸ��Ϣ)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� �Ǽǻ�Ʊҵ��Ǽǲ���״̬�����Ϣ
################################################################################
def insTransBil(bil_dict):
    
    AfaLoggerFunc.tradeInfo( ">>>��ʼ�Ǽǻ�Ʊҵ��Ǽǲ�[" + bil_dict["BJEDTE"] + "][" + bil_dict["BSPSQN"] + "]������Ϣ�����״̬" )
    if not bil_dict.has_key("BJEDTE"):
        return AfaFlowControl.ExitThisFlow( 'S999',"�Ǽǻ�Ʊҵ��Ǽǲ�,BJEDTE����Ϊ��")
        
    if not bil_dict.has_key("BSPSQN"):
        return AfaFlowControl.ExitThisFlow( 'S999',"�Ǽǻ�Ʊҵ��Ǽǲ�,BSPSQN����Ϊ��")
        
    
    #==========�������ֵ丳ֵ����Ʊҵ��Ǽǲ��ֵ�===============================
    bilbka_dict = {}
    
    if not rccpsMap0000Dbil_dict2Dbilbka.map(bil_dict,bilbka_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '�������ֵ丳ֵ����Ʊҵ��Ǽǲ��ֵ��쳣' )
        
    #==========�Ǽ���Ϣ����Ʊҵ��Ǽǲ�=========================================
    ret = rccpsDBTrcc_bilbka.insert(bilbka_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǻ�Ʊҵ��Ǽǲ���Ʊҵ����ϸ��Ϣ�쳣' )
    
    #==========�Ǽǳ�ʼ״̬=====================================================
    if not rccpsState.newTransState(bil_dict["BJEDTE"],bil_dict["BSPSQN"],PL_BCSTAT_INIT,PL_BDWFLG_SUCC):
        return False
        
    AfaLoggerFunc.tradeInfo( ">>>�����Ǽǻ�Ʊҵ��Ǽǲ�[" + bil_dict["BJEDTE"] + "][" + bil_dict["BSPSQN"] + "]������Ϣ�����״̬" )
    return True


################################################################################
# ������:    getInfoBil
# ����:      BILVER:��Ʊ�汾��,BILNO:��Ʊ����,BILRS:��Ʊ���������ʶ
# ����ֵ��   �ɹ�    bilinf_dict(�����Ϣ������ϸ��Ϣ,��bilinf������)
#            ʧ��    False
# ����˵���� ��ѯ��Ʊ��Ϣ�Ǽǲ������Ϣ
################################################################################
def getInfoBil(BILVER,BILNO,BILRS,bil_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ��Ʊ��Ϣ�Ǽǲ�[" + BILVER + "][" + BILNO + "][" + BILRS + "]������Ϣ" )
    
    #===========��֯��ѯ����=====================================================
    bilinf_where_dict = {'BILVER':BILVER,'BILNO':BILNO,'BILRS':BILRS}

    #===========��ѯ��Ʊ��Ϣ�Ǽǲ������Ϣ=======================================
    bilinf_dict = rccpsDBTrcc_bilinf.selectu(bilinf_where_dict)
    
    if bilinf_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ��Ʊ��Ϣ�Ǽǲ���Ʊ��Ϣ�쳣' )
    
    if len(bilinf_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '��Ʊ��Ϣ�Ǽǲ����޴˻�Ʊ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯ��Ʊ��Ϣ�Ǽǲ�[" + BILVER + "][" + BILNO + "][" + BILRS + "]������Ϣ" )

    #===========����ѯ���Ļ�Ʊ��Ϣ�Ǽǲ������Ϣ��ֵ������ֵ�===================
    if not rccpsMap0000Dbilinf2Dbil_dict.map(bilinf_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ���Ļ�Ʊ��Ϣ�Ǽǲ������Ϣ��ֵ������ֵ��쳣' )
    
    return True
    
    
################################################################################
# ������:    insInfoBil
# ����:      bil_dict(��Ʊ��Ϣ��ϸ��Ϣ)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� �Ǽǻ�Ʊ��Ϣ�Ǽǲ������Ϣ
################################################################################
def insInfoBil(bil_dict):
    
    AfaLoggerFunc.tradeInfo( ">>>��ʼ�Ǽǻ�Ʊ��Ϣ�Ǽǲ�[" + bil_dict["BILVER"] + "][" + bil_dict["BILNO"] + "][" + bil_dict["BILRS"] + "]������Ϣ�����״̬" )
    if not bil_dict.has_key("BILVER"):
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǻ�Ʊ��Ϣ�Ǽǲ�,BILVER����Ϊ��")
        
    if not bil_dict.has_key("BILNO"):
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǻ�Ʊ��Ϣ�Ǽǲ�,BILNO����Ϊ��")
    
    if not bil_dict.has_key("BILRS"):
        return AfaFlowControl.ExitThisFlow("S999","�Ǽǻ�Ʊ��Ϣ�Ǽǲ�,BILRS����Ϊ��")
        
    
    
    #===========�������ֵ丳ֵ����Ʊ��Ϣ�Ǽǲ��ֵ�==============================
    bilinf_dict = {}
    
    if not rccpsMap0000Dbil_dict2Dbilinf.map(bil_dict,bilinf_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '�������ֵ丳ֵ����Ʊ��Ϣ�Ǽǲ��ֵ��쳣' )
    
    
    bilinf_where_dict = {}
    bilinf_where_dict['BILRS']  = bil_dict['BILRS']
    bilinf_where_dict['BILVER'] = bil_dict['BILVER']
    bilinf_where_dict['BILNO']  = bil_dict['BILNO']
    
    tmp_bilinf_dict = rccpsDBTrcc_bilinf.selectu(bilinf_where_dict)
    if tmp_bilinf_dict == None:
        return AfaFlowControl.ExitThisFlow( 'S999', 'У���Ʊ��Ϣ�Ǽǲ��Ƿ������ͬ��Ʊ�쳣' )
    
    if len(tmp_bilinf_dict) <= 0:
        AfaLoggerFunc.tradeError("��Ʊ��Ϣ�Ǽǲ������ڴ˻�Ʊ,�����Ʊ��Ϣ")
    
        #===========�Ǽ���Ϣ����Ʊ��Ϣ�Ǽǲ�========================================
        ret = rccpsDBTrcc_bilinf.insert(bilinf_dict)
        if ret <= 0:
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǻ�Ʊ��ϸ��Ϣ�쳣' )
        
        return True
    else:
        AfaLoggerFunc.tradeError("��Ʊ��Ϣ�Ǽǲ����ڴ˻�Ʊ,���»�Ʊ��Ϣ")
    
        #===========�Ǽ���Ϣ����Ʊ��Ϣ�Ǽǲ�========================================
        ret = rccpsDBTrcc_bilinf.update(bilinf_dict,bilinf_where_dict)
        if ret <= 0:
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǻ�Ʊ��ϸ��Ϣ�쳣' )
        
        return True
    
################################################################################
# ������:    getTransTrcPK
# ����:      SNDMBRCO:���ͳ�Ա�к�,TRCDAT:ί������,TRCNO:������ˮ��,trc_dict(���ҵ������ϸ��Ϣ,��trcbka������+sstlog������)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ���ݷ��ͳ�Ա�к�,ί������,������ˮ�Ų�ѯ���ҵ��Ǽǲ�����ǰ״̬�����Ϣ
################################################################################
def getTransTrcPK(SNDMBRCO,TRCDAT,TRCNO,trc_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ���ҵ��Ǽǲ�[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )
    
    #===========��֯��ѯ����====================================================
    trcbka_where_dict = {'SNDMBRCO':SNDMBRCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #===========��ѯ��ҵǼǲ����ҵ����Ϣ======================================
    trcbka_dict = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict)
    
    if trcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ���ҵ����ϸ��Ϣ�쳣' )
    
    if len(trcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '���ҵ��Ǽǲ����޴˻��ҵ����ϸ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯ���ҵ��Ǽǲ�[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )

    #==========����ѯ���Ļ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ�===================
    if not rccpsMap0000Dtrcbka2Dtrc_dict.map(trcbka_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ���Ļ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )

    BJEDTE = trcbka_dict["BJEDTE"]
    BSPSQN = trcbka_dict["BSPSQN"]
    
    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dtrc_dict.map(stat_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ���ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True
    
################################################################################
# ������:    GetTransBilPK
# ����:      SNDMBRCO:���ͳ�Ա�к�,TRCDAT:ί������,TRCNO:������ˮ��,bil_dict(��Ʊҵ������ϸ��Ϣ,��bilbka������+sstlog������)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ���ݷ��ͳ�Ա�к�,ί������,������ˮ�Ų�ѯ��Ʊҵ��Ǽǲ�����ǰ״̬�����Ϣ
################################################################################

def getTransBilPK(SNDMBRCO,TRCDAT,TRCNO,bil_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ��Ʊҵ��Ǽǲ�[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )
    
    #==========��֯��ѯ����=====================================================
    bilbka_where_dict = {'SNDMBRCO':SNDMBRCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #==========��ѯ��Ʊҵ��Ǽǲ����ҵ����Ϣ===================================
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    
    if bilbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ��Ʊҵ����ϸ��Ϣ�쳣' )
        
    if len(bilbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '��Ʊҵ��Ǽǲ����޴˻�Ʊҵ����ϸ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯ��Ʊҵ��Ǽǲ�[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )

    #==========����ѯ���Ļ�Ʊҵ��Ǽǲ����ҵ����Ϣ��ֵ������ֵ�===============
    if not rccpsMap0000Dbilbka2Dbil_dict.map(bilbka_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ���Ļ�Ʊҵ��Ǽǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )

    BJEDTE = bilbka_dict["BJEDTE"]
    BSPSQN = bilbka_dict["BSPSQN"]
    
    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰҵ��״̬" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰҵ��״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dbil_dict.map(stat_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ��Ʊҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True

################################################################################
# ������:    getTransTrcAK
# ����:      SNDBNKCO:�����к�,TRCDAT:ί������,TRCNO:������ˮ��,trc_dict(���ҵ������ϸ��Ϣ,��trcbka������+sstlog������)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ���ݷ����к�,ί������,������ˮ�Ų�ѯ���ҵ��Ǽǲ�����ǰ״̬�����Ϣ
################################################################################
def getTransTrcAK(SNDBNKCO,TRCDAT,TRCNO,trc_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ���ҵ��Ǽǲ�[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )
    
    #===========��֯��ѯ����====================================================
    trcbka_where_dict = {'SNDBNKCO':SNDBNKCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #===========��ѯ��ҵǼǲ����ҵ����Ϣ======================================
    trcbka_dict = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict)
    
    if trcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ���ҵ����ϸ��Ϣ�쳣' )
    
    if len(trcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '���ҵ��Ǽǲ����޴˻��ҵ����ϸ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯ���ҵ��Ǽǲ�[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )

    #==========����ѯ���Ļ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ�===================
    if not rccpsMap0000Dtrcbka2Dtrc_dict.map(trcbka_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ���Ļ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )

    BJEDTE = trcbka_dict["BJEDTE"]
    BSPSQN = trcbka_dict["BSPSQN"]
    
    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dtrc_dict.map(stat_dict,trc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ���ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True
    
################################################################################
# ������:    getTransBilAK
# ����:      SNDBNKCO:���ͳ�Ա�к�,TRCDAT:ί������,TRCNO:������ˮ��,bil_dict(��Ʊҵ������ϸ��Ϣ,��bilbka������+sstlog������)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ���ݷ��ͳ�Ա�к�,ί������,������ˮ�Ų�ѯ��Ʊҵ��Ǽǲ�����ǰ״̬�����Ϣ
################################################################################

def getTransBilAK(SNDBNKCO,TRCDAT,TRCNO,bil_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ��Ʊҵ��Ǽǲ�[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )
    
    #==========��֯��ѯ����=====================================================
    bilbka_where_dict = {'SNDBNKCO':SNDBNKCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #==========��ѯ��Ʊҵ��Ǽǲ����ҵ����Ϣ===================================
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    
    if bilbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ��Ʊҵ����ϸ��Ϣ�쳣' )
        
    if len(bilbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', '��Ʊҵ��Ǽǲ����޴˻�Ʊҵ����ϸ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯ��Ʊҵ��Ǽǲ�[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )

    #==========����ѯ���Ļ�Ʊҵ��Ǽǲ����ҵ����Ϣ��ֵ������ֵ�===============
    if not rccpsMap0000Dbilbka2Dbil_dict.map(bilbka_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ���Ļ�Ʊҵ��Ǽǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )

    BJEDTE = bilbka_dict["BJEDTE"]
    BSPSQN = bilbka_dict["BSPSQN"]
    
    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰҵ��״̬" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰҵ��״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dbil_dict.map(stat_dict,bil_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ��Ʊҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True
    
###############################################################################
# ������:    getErrInfo
# ����:      ERRKEY:�������
# ����ֵ:    �ɹ�:ERRSTR:������Ϣ
#            ʧ��:False
# ����˵��:  ���ݴ�������ѯ��Ӧ�Ĵ�����Ϣ
###############################################################################

def getErrInfo(ERRKEY):
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡ���ķ��ش���[" + ERRKEY + "]��Ӧ��Ϣ")
    
    errinf_where_dict = {}
    if ERRKEY[:2] != 'NN':
        errinf_where_dict['MBRTYP'] = '1'
        errinf_where_dict['ERRKEY'] = ERRKEY[:8]
    else:
        errinf_where_dict['MBRTYP'] = '2'
        errinf_where_dict['ERRKEY'] = ERRKEY[4:8]
    
    ERRSTR = ""
    
    errinf_dict = rccpsDBTrcc_errinf.selectu(errinf_where_dict)
    
    if errinf_dict == None:
        AfaLoggerFunc.tradeInfo("��ѯ���ķ�����Ϣ���ݿ��쳣")
        
    if len(errinf_dict) <= 0:
        ERRSTR = "δ֪����"
        AfaLoggerFunc.tradeInfo("�޴˷��ش����Ӧ��Ϣ,�������ķ�����Ϣ[δ֪����]")
    else:
        ERRSTR = errinf_dict['ERRSTR']
        AfaLoggerFunc.tradeInfo("�ҵ��˷��ش����Ӧ��Ϣ,�������ķ�����Ϣ[" + ERRSTR + "]")
    
    AfaLoggerFunc.tradeInfo(">>>������ȡ���ķ��ش���[" + ERRKEY + "]��Ӧ��Ϣ")
    
    return ERRSTR
    
    
###############################################################################
# ������:    HostErr2RccErr
# ����:      HostErr:�����������
# ����ֵ:    RccErr: ���Ĵ������
# ����˵��:  ����������������ѯ��Ӧ�����Ĵ������
###############################################################################

def HostErr2RccErr(HostErr):
    AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡ����������[" + HostErr + "]��Ӧ�����ķ�����")
    
    errinf_where_dict = {}
    errinf_where_dict['NOTE3'] = "%" + HostErr + "%"
    
    errinf_dict = rccpsDBTrcc_errinf.selectu(errinf_where_dict)
    
    RccErr = ""
    
    if errinf_dict == None:
        RccErr = "NN1IA999"
        AfaLoggerFunc.tradeInfo("��ѯ���ķ�����Ϣ���ݿ��쳣")
        
    if len(errinf_dict) <= 0:
        RccErr = "NN1IA999"
        AfaLoggerFunc.tradeInfo("�޴������������Ӧ��Ϣ,�������Ĵ�����[NN1IA999]")
    else:
        RccErr = "NN1I" + errinf_dict['ERRKEY']
        AfaLoggerFunc.tradeInfo("�ҵ��������������Ӧ��Ϣ,�������Ĵ�����[" + RccErr + "]")
    
    AfaLoggerFunc.tradeInfo(">>>������ȡ����������[" + HostErr + "]��Ӧ�����ķ�����")
    
    return RccErr

################################################################################
# ������:    getTransWtr                                             
# ����:      BJEDTE:��������(����),BSPSQN:�������(����)             
# ����ֵ��   �ɹ�    wtr_dict(ͨ��ͨ��ҵ������ϸ��Ϣ,��wtrbka������+sstlog������)
#            ʧ��    False                                           
# ����˵���� ��ѯͨ��ͨ��ҵ��Ǽǲ�����ǰ״̬�����Ϣ                    
################################################################################
                                                                     
def getTransWtr(BJEDTE,BSPSQN,wtr_dict):
    AfaLoggerFunc.tradeDebug( ">>>��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
                                                                     
    #==========��֯��ѯ����=====================================================
    wtrbka_where_dict = {'BJEDTE':BJEDTE,'BSPSQN':BSPSQN}            
                                                                     
    #==========��ѯ��ҵǼǲ����ҵ����Ϣ=======================================
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)  
    
    if wtrbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ѯͨ��ͨ��ҵ��Ǽǲ�������Ϣ�쳣' )
        
    if len(wtrbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', 'ͨ��ͨ��ҵ��Ǽǲ����޴˽�����Ϣ' )
    
    #==========����ѯ����ͨ��ͨ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ�==============
    if not rccpsMap0000Dwtrbka2Dwtr_dict.map(wtrbka_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ͨ��ͨ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )
        
    #==========��ѯ��ǰҵ��״̬================================================
    AfaLoggerFunc.tradeDebug( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )
    
    stat_dict = {}
    
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
        
    AfaLoggerFunc.tradeDebug( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�========================
    if not rccpsMap0000Dstat_dict2Dwtr_dict.map(stat_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeDebug( ">>>������ѯͨ��ͨ��ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True

###############################################################################
# ������:    insTransWtr
# ����:      trc_dict(ͨ��ͨ��ҵ������ϸ��Ϣ)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� �Ǽ�ͨ��ͨ��ҵ��Ǽǲ���״̬�����Ϣ
###############################################################################
def insTransWtr(wtr_dict):
    
    AfaLoggerFunc.tradeInfo( ">>>��ʼ�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�[" + wtr_dict["BJEDTE"] + "][" + wtr_dict["BSPSQN"] + "]������Ϣ�����״̬" )
    
    if not wtr_dict.has_key("BJEDTE"):
        return AfaFlowControl.ExitThisFlow( 'S999',"�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�,BJEDTE����Ϊ��")
        
    if not wtr_dict.has_key("BSPSQN"):
        return AfaFlowControl.ExitThisFlow( 'S999',"�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�,BSPSQN����Ϊ��")
        
    
    #==========�������ֵ丳ֵ��ͨ��ͨ��ҵ��Ǽǲ��ֵ�==========================
    wtrbka_dict = {}
    
    if not rccpsMap0000Dwtr_dict2Dwtrbka.map(wtr_dict,wtrbka_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '�������ֵ丳ֵ��ͨ��ͨ��ҵ��Ǽǲ��ֵ��쳣' )
        
    #==========�Ǽ���Ϣ����ҵǼǲ�============================================
    AfaLoggerFunc.tradeInfo(wtrbka_dict)
    ret = rccpsDBTrcc_wtrbka.insert(wtrbka_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽ�ͨ��ͨ��ҵ����ϸ��Ϣ��ͨ��ͨ��ҵ��Ǽǲ��쳣' )
        
    AfaLoggerFunc.tradeInfo("����ɹ�")
    #==========�Ǽǳ�ʼ״̬====================================================
    if not rccpsState.newTransState(wtr_dict["BJEDTE"],wtr_dict["BSPSQN"],PL_BCSTAT_INIT,PL_BDWFLG_SUCC):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>�����Ǽ�ͨ��ͨ��ҵ��Ǽǲ�[" + wtr_dict["BJEDTE"] + "][" + wtr_dict["BSPSQN"] + "]������Ϣ�����״̬" )
    return True
    
################################################################################
# ������:    getTransWtrPK
# ����:      SNDMBRCO:���ͳ�Ա�к�,TRCDAT:ί������,TRCNO:������ˮ��,wtr_dict(���ҵ������ϸ��Ϣ,��wtrbka������+sstlog������)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ���ݷ��ͳ�Ա�к�,ί������,������ˮ�Ų�ѯͨ��ͨ��ҵ��Ǽǲ�����ǰ״̬�����Ϣ
################################################################################
def getTranswtrPK(SNDMBRCO,TRCDAT,TRCNO,wtr_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )
    
    #===========��֯��ѯ����====================================================
    wtrbka_where_dict = {'SNDMBRCO':SNDMBRCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #===========��ѯ��ҵǼǲ����ҵ����Ϣ======================================
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
    
    if wtrbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡͨ��ͨ��ҵ����ϸ��Ϣ�쳣' )
    
    if len(wtrbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', 'ͨ��ͨ��ҵ��Ǽǲ����޴�ͨ��ͨ��ҵ����ϸ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯͨ��ͨ��ҵ��Ǽǲ�[" + SNDMBRCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )

    #==========����ѯ����ͨ��ͨ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ�===================
    if not rccpsMap0000Dwtrbka2Dwtr_dict.map(wtrbka_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ͨ��ͨ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )

    BJEDTE = wtrbka_dict["BJEDTE"]
    BSPSQN = wtrbka_dict["BSPSQN"]
    
    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dwtr_dict.map(stat_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ���ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True
    
###############################################################################
# ������:    getTransWtrAK
# ����:      SNDBNKCO:�����к�,TRCDAT:ί������,TRCNO:������ˮ��,wtr_dict(ͨ��ͨ��ҵ������ϸ��Ϣ,��wtrbka������+sstlog������)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ���ݷ����к�,ί������,������ˮ�Ų�ѯͨ��ͨ��ҵ��Ǽǲ�����ǰ״̬�����Ϣ
###############################################################################
def getTransWtrAK(SNDBNKCO,TRCDAT,TRCNO,wtr_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )
    
    #===========��֯��ѯ����===================================================
    wtrbka_where_dict = {'SNDBNKCO':SNDBNKCO,'TRCDAT':TRCDAT,'TRCNO':TRCNO}

    #===========��ѯͨ��ͨ�ҵǼǲ����ҵ����Ϣ=================================
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
    
    if wtrbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡͨ��ͨ��ҵ����ϸ��Ϣ�쳣' )
    
    if len(wtrbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', 'ͨ��ͨ��ҵ��Ǽǲ����޴�ͨ��ͨ��ҵ����ϸ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯͨ��ͨ��ҵ��Ǽǲ�[" + SNDBNKCO + "][" + TRCDAT + "][" + TRCNO + "]������Ϣ" )

    #==========����ѯ����ͨ��ͨ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ�==============
    if not rccpsMap0000Dwtrbka2Dwtr_dict.map(wtrbka_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ͨ��ͨ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )

    BJEDTE = wtrbka_dict["BJEDTE"]
    BSPSQN = wtrbka_dict["BSPSQN"]
    
    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dwtr_dict.map(stat_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯͨ��ͨ��ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True
    
###############################################################################
# ������:    getTransWtrCK
# ����:      SNDBNKCO:�����к�,COTRCDAT:���ȷ��ί������,COTRCNO:���ȷ�Ͻ�����ˮ��,wtr_dict(ͨ��ͨ��ҵ������ϸ��Ϣ,��wtrbka������+sstlog������)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ���ݷ����к�,���ȷ��ί������,���ȷ�Ͻ�����ˮ�Ų�ѯͨ��ͨ��ҵ��Ǽǲ�����ǰ״̬�����Ϣ
###############################################################################
def getTransWtrCK(SNDBNKCO,COTRCDAT,COTRCNO,wtr_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯͨ��ͨ��ҵ��Ǽǲ�[" + SNDBNKCO + "][" + COTRCDAT + "][" + COTRCNO + "]������Ϣ" )
    
    #===========��֯��ѯ����===================================================
    wtrbka_where_dict = {'SNDBNKCO':SNDBNKCO,'COTRCDAT':COTRCDAT,'COTRCNO':COTRCNO}

    #===========��ѯͨ��ͨ�ҵǼǲ����ҵ����Ϣ=================================
    wtrbka_dict = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
    
    if wtrbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡͨ��ͨ��ҵ����ϸ��Ϣ�쳣' )
    
    if len(wtrbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', 'ͨ��ͨ��ҵ��Ǽǲ����޴�ͨ��ͨ��ҵ����ϸ��Ϣ' )
        
    AfaLoggerFunc.tradeInfo( ">>>������ѯͨ��ͨ��ҵ��Ǽǲ�[" + SNDBNKCO + "][" + COTRCDAT + "][" + COTRCNO + "]������Ϣ" )

    #==========����ѯ����ͨ��ͨ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ�==============
    if not rccpsMap0000Dwtrbka2Dwtr_dict.map(wtrbka_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ͨ��ͨ�ҵǼǲ����ҵ����Ϣ��ֵ������ֵ��쳣' )

    BJEDTE = wtrbka_dict["BJEDTE"]
    BSPSQN = wtrbka_dict["BSPSQN"]
    
    #==========��ѯ��ǰҵ��״̬=================================================
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )
    
    stat_dict = {}
    if not rccpsState.getTransStateCur(BJEDTE,BSPSQN,stat_dict):
        return False
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬" )

    #==========����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ�=========================
    if not rccpsMap0000Dstat_dict2Dwtr_dict.map(stat_dict,wtr_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯͨ��ͨ��ҵ��Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True

################################################################################
# ������:    getTransMpc                                             
# ����:      BJEDTE:��������(����),BSPSQN:�������(����)             
# ����ֵ��   �ɹ�    mpc_dict(ͨ��ͨ�ҳ���������ϸ��Ϣ,��mpcbka������)
#            ʧ��    False                                           
# ����˵���� ��ѯͨ��ͨ�ҳ����Ǽǲ�
################################################################################
                                                                     
def getTransMpc(BJEDTE,BSPSQN,mpc_dict):
    AfaLoggerFunc.tradeInfo( ">>>��ʼ��ѯͨ��ͨ�ҳ����Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
                                                                     
    #==========��֯��ѯ����=====================================================
    mpcbka_where_dict = {'BJEDTE':BJEDTE,'BSPSQN':BSPSQN}            
                                                                     
    #==========��ѯ�����Ǽǲ����ҵ����Ϣ=======================================
    mpcbka_dict = rccpsDBTrcc_mpcbka.selectu(mpcbka_where_dict)  
    
    if mpcbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        return AfaFlowControl.ExitThisFlow( 'S999', '��ѯͨ��ͨ�ҳ����Ǽǲ�������Ϣ�쳣' )
        
    if len(mpcbka_dict) <= 0:
        return AfaFlowControl.ExitThisFlow( 'S999', 'ͨ��ͨ�ҳ����Ǽǲ����޴˽�����Ϣ' )
    
    #==========����ѯ����ͨ��ͨ�ҳ����Ǽǲ������Ϣ��ֵ������ֵ�==============
    if not rccpsMap0000Dmpcbka2Dmpc_dict.map(mpcbka_dict,mpc_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ͨ��ͨ�ҳ����Ǽǲ������Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo( ">>>������ѯͨ��ͨ�ҳ����Ǽǲ�[" + BJEDTE + "][" + BSPSQN + "]������Ϣ" )
    return True

################################################################################
# ������:    chkTDBESAuth                                             
# ����:      BESBNO ������
# ����ֵ��   �ɹ�    True
#            ʧ��    False                                           
# ����˵���� �������Ƿ���ͨ��ͨ��Ȩ��
################################################################################
def chkTDBESAuth(BESBNO):
    AfaLoggerFunc.tradeInfo(">>>��ʼ������[" + BESBNO + "]�Ƿ���ͨ��ͨ��ҵ��Ȩ��")
    
    where_sql = "BPATPE = '3' and BPARAD = '" + BESBNO + "'"
    
    ret = rccpsDBTrcc_pamtbl.count(where_sql)
    
    if ret < 0:
        return AfaFlowControl.ExitThisFlow("S999","��ѯ����[" + BESBNO + "]ͨ��ͨ��ҵ��Ȩ���쳣")
        
    if ret > 0:
        return AfaFlowControl.ExitThisFlow("S999","����[" + BESBNO + "]��ͨ��ͨ��ҵ��Ȩ��")
    
    AfaLoggerFunc.tradeInfo(">>>����������[" + BESBNO + "]�Ƿ���ͨ��ͨ��ҵ��Ȩ��")
    
    return True
    
################################################################################
# ������:    chkLimited
# ����:      BJEDTE ��������,PYRACC �������˺�,OCCAMT ��ǰ���׽��
# ����ֵ��   �ɹ�    True
#            ʧ��    False                                           
# ����˵���� ��鵱ǰ���׽���Ƿ��޶�
################################################################################
def chkLimited(BJEDTE,PYRACC,OCCAMT):
    AfaLoggerFunc.tradeInfo(">>>��ʼ��鵱ǰ���׽���Ƿ��޶�")
    
    pamtbl_where_dict = {'BPATPE':'4','BPARAD':'TDLZXE'}
    
    pamtbl_dict = {}
    pamtbl_dict = rccpsDBTrcc_pamtbl.selectu(pamtbl_where_dict)
    
    if pamtbl_dict == None:
        return AfaFlowControl.ExitThisFlow("S999","��ѯͨ�����˽����޶��쳣")
        
    if len(pamtbl_dict) <= 0:
        return AfaFlowControl.ExitThisFlow("S999","����������ͨ�����˲���")
    else:
        AfaLoggerFunc.tradeInfo("���׽���޶�Ϊ[" + str(pamtbl_dict['BPADAT'])+ "]")
    
    where_sql = "select count(*),sum(a.occamt) from rcc_wtrbka as a,rcc_spbsta as b where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.PYRACC = '" + PYRACC + "' and a.BJEDTE = '" + BJEDTE + "' and b.bcstat in ('70','72') and b.bdwflg = '1'"
    
    records = AfaDBFunc.SelectSql(where_sql)
    
    if records == None:
        return AfaFlowControl.ExitThisFlow('S999','ͳ���˻����ս����ܽ���쳣')
    
    else:
        rec_count = records[0][0]
        rec_sum   = records[0][1] 
        
    if records[0][0] <= 0:
        rec_count = 0
        rec_sum   = 0.00
    
    AfaLoggerFunc.tradeInfo("������ʷ���׽���ܺ�Ϊ[" + str(rec_sum) + "],���ν��׽��Ϊ[" + str(OCCAMT) + "]")
    
    if float(rec_sum) + float(OCCAMT) > float(pamtbl_dict['BPADAT']):
        return AfaFlowControl.ExitThisFlow("S999","���˻����׽���")
    
    AfaLoggerFunc.tradeInfo(">>>������鵱ǰ���׽���Ƿ��޶�")
    
    return True
