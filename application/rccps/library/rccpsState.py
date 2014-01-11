# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ ״̬��غ���
#==============================================================================
#   ��    �ߣ�  �ر��
#   �����ļ�:   rccpsStat.py
#   �޸�ʱ��:   2008-06-05
###############################################################################

import AfaLoggerFunc,AfaDBFunc,AfaUtilTools,TradeContext,AfaFlowControl
from types import *
import rccpsDBTrcc_spbsta,rccpsDBTrcc_sstlog
import rccpsMap0000Dstat_dict2Dsstlog,rccpsMap0000Dstat_dict2Dspbsta
import rccpsDBTrcc_bilbka,rccpsDBTrcc_bilinf
import rccpsMap0000Dsstlog2Dstat_dict

################################################################################
# ������:    setTransState
# ����:      stat_dict:״̬�ֵ�
#            {BJEDTE:��������(����),BSPSQN:�������(����),BCSTAT:ҵ��״̬(����),BDWFLG:��ת�����ʶ(����),
#             BESBNO:������,BEACSB:�������,BETELR:��Ա��,BEAUUS:��Ȩ��Ա,EFDT:ǰ������,RBSQ:ǰ����ˮ��,TRDT:��������,TLSQ:������ˮ��,
#             SBAC:�跽�˺�,ACNM:�跽����,RBAC:�����˺�,OTNM:��������,DASQ:�������,MGID:����������,PRCCO:���ķ�����,}
# ����ֵ��   True  �ɹ�    False  ʧ��
# ����˵���� ���õ��ʽ��׵�ǰҵ��״̬�������Ϣ
################################################################################
def setTransState(stat_dict):
    AfaLoggerFunc.tradeInfo(">>>����setTransState")
    
    AfaLoggerFunc.tradeDebug("stat_dict = " + str(stat_dict))
    #==========����spbsta���Ƿ���ڴ�ҵ��״̬=================================
    spbsta_where_dict = {}
    if stat_dict.has_key("BJEDTE"):
        spbsta_where_dict["BJEDTE"] = stat_dict["BJEDTE"]
        
    if stat_dict.has_key("BSPSQN"):
        spbsta_where_dict["BSPSQN"] = stat_dict["BSPSQN"]
        
    spbsta_dict = rccpsDBTrcc_spbsta.selectu(spbsta_where_dict)
    if spbsta_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ����[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]��ǰ״̬�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ���׵�ǰ״̬�쳣' )
        
    elif len(spbsta_dict) <= 0:
        AfaLoggerFunc.tradeFatal("��ǰ״̬�Ǽǲ����޽���[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]״̬��Ϣ")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ǰ״̬�Ǽǲ����޴˽���״̬' )
    
    #===========����sstlog���Ƿ���ڴ�ҵ��״̬================================
    sstlog_where_dict = {}
    if spbsta_dict.has_key("BJEDTE"):
        sstlog_where_dict["BJEDTE"] = spbsta_dict["BJEDTE"]
        
    if spbsta_dict.has_key("BSPSQN"):
        sstlog_where_dict["BSPSQN"] = spbsta_dict["BSPSQN"]
        
    if spbsta_dict.has_key("BCURSQ"):
        sstlog_where_dict["BCURSQ"] = str(spbsta_dict["BCURSQ"])
    
    sstlog_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
    
    if sstlog_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ����[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]��ǰ״̬��ϸ��Ϣ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ���׵�ǰ״̬��ϸ��Ϣ�쳣' )
        
    elif len(sstlog_dict) == 0:
        AfaLoggerFunc.tradeFatal("��ˮ״̬�Ǽǲ����޽���[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]��ǰ״̬��ϸ��Ϣ")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ˮ״̬�Ǽǲ����޴˽��׵�ǰ״̬��ϸ��Ϣ' )
    
    #============����Ĭ��ֵ=====================================================
    stat_dict["PRTCNT"] = 0
    stat_dict["NOTE2"] = AfaUtilTools.GetSysDate() + AfaUtilTools.GetSysTime()
    #AfaLoggerFunc.tradeInfo(stat_dict["NOTE2"])
    #============���±�sstlog===================================================
    sstlog_update_dict = {}
    
    if not rccpsMap0000Dstat_dict2Dsstlog.map(stat_dict,sstlog_update_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', 'Ϊ���׵�ǰ״̬��ϸ��Ϣ��ֵ�쳣' )
        
    sstlog_where_dict = {}
    if spbsta_dict.has_key("BJEDTE"):
        sstlog_where_dict["BJEDTE"] = spbsta_dict["BJEDTE"]
        
    if spbsta_dict.has_key("BSPSQN"):
        sstlog_where_dict["BSPSQN"] = spbsta_dict["BSPSQN"]
        
    if spbsta_dict.has_key("BCURSQ"):
        sstlog_where_dict["BCURSQ"] = str(spbsta_dict["BCURSQ"])
        
    #AfaLoggerFunc.tradeInfo("update_dict = " + str(sstlog_update_dict))
    #AfaLoggerFunc.tradeInfo("where_dict = " + str(sstlog_where_dict))
    
    ret = rccpsDBTrcc_sstlog.update(sstlog_update_dict,sstlog_where_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("�Ǽǽ���[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]")
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǽ��׵�ǰ״̬��ϸ��Ϣ�쳣' )
    
    #============���±�spbsta===================================================
    spbsta_update_dict = {}
    
    if not rccpsMap0000Dstat_dict2Dspbsta.map(stat_dict,spbsta_update_dict):
        return AfaFlowControl.ExitThisFlow( 'S999', 'Ϊ���׵�ǰ״̬��ֵ�쳣' )
    
    spbsta_where_dict = {}
    if stat_dict.has_key("BJEDTE"):
        spbsta_where_dict["BJEDTE"] = stat_dict["BJEDTE"]
    if stat_dict.has_key("BSPSQN"):
        spbsta_where_dict["BSPSQN"] = stat_dict["BSPSQN"]
    
    ret = rccpsDBTrcc_spbsta.update(spbsta_update_dict,spbsta_where_dict)
    if (ret <= 0):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("�Ǽǽ���[" + stat_dict['BJEDTE'] + "][" + stat_dict['BSPSQN'] + "]��ǰ״̬�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǽ��׵�ǰ״̬�쳣' )
        
    AfaLoggerFunc.tradeInfo(">>>����setTransState")
    
    return True

################################################################################
# ������:    newTransState
# ����:      BJEDTE:��������(����),BSPSQN:�������(����),BCSTAT:ҵ��״̬(����),BDWFLG:��ת�����ʶ(����)
# ����ֵ��   True  �ɹ�    False  ʧ��
# ����˵���� �½����ʽ���ҵ��״̬�������Ϣ
################################################################################
def newTransState(BJEDTE,BSPSQN,BCSTAT,BDWFLG):
    AfaLoggerFunc.tradeInfo(">>>����newTransState")
    
    stat_dict = {}
    stat_dict["BJEDTE"] = BJEDTE;
    stat_dict["BSPSQN"] = BSPSQN;
    stat_dict["BCSTAT"] = BCSTAT;
    stat_dict["BDWFLG"] = BDWFLG;
    
    #==========����spbsta���Ƿ���ڴ�ҵ��״̬=================================
    spbsta_where_dict = {}
    if stat_dict.has_key("BJEDTE"):
        spbsta_where_dict["BJEDTE"] = stat_dict["BJEDTE"]
    if stat_dict.has_key("BSPSQN"):
        spbsta_where_dict["BSPSQN"] = stat_dict["BSPSQN"]
        
    spbsta_dict = rccpsDBTrcc_spbsta.selectu(spbsta_where_dict)
    
    if spbsta_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ѯ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ѯ���׵�ǰ״̬�쳣' )
        
    elif len(spbsta_dict) <= 0:
        AfaLoggerFunc.tradeInfo("��ǰ״̬�Ǽǲ����޴�ҵ��״̬,������һ��ҵ��״̬")
        MaxBCURSQ = 1
        
    else:
        MaxBCURSQ = int(spbsta_dict["BCURSQ"]) + 1
            
    #===========����Ĭ��ֵ======================================================
    if TradeContext.existVariable('BESBNO'):            #������
        stat_dict["BESBNO"] = TradeContext.BESBNO
        
    if TradeContext.existVariable('BEACSB'):            #���������
        stat_dict["BEACSB"] = TradeContext.BEACSB
        
    if TradeContext.existVariable('BETELR'):            #��Ա��
        stat_dict["BETELR"] = TradeContext.BETELR
        
    if TradeContext.existVariable('BEAUUS'):            #��Ȩ��Ա��
        stat_dict["BEAUUS"] = TradeContext.BEAUUS
        
    if TradeContext.existVariable('TERMID'):            #�ն˺�
        stat_dict['TERMID'] = TradeContext.TERMID
        
    if TradeContext.existVariable('NOTE3'):             #����ԭ��
        stat_dict['NOTE3']  = TradeContext.NOTE3
        
    if TradeContext.existVariable('FEDT') and TradeContext.FEDT != '' and TradeContext.existVariable('HostCode') and TradeContext.HostCode != '8820':              #ǰ������
        stat_dict['FEDT'] = TradeContext.FEDT
    else:
        stat_dict['FEDT'] = BJEDTE

    if TradeContext.existVariable('RBSQ') and TradeContext.RBSQ != '' and TradeContext.existVariable('HostCode') and TradeContext.HostCode != '8820':              #ǰ����ˮ��
        stat_dict['RBSQ']  = TradeContext.RBSQ
    else:
        stat_dict['RBSQ'] = BSPSQN
    
    stat_dict["PRTCNT"] = 0
    stat_dict["BJETIM"] = AfaUtilTools.GetSysDate() + AfaUtilTools.GetSysTime()
    #AfaLoggerFunc.tradeInfo(">>>>time:" + stat_dict["BJETIM"])
    
    #===========�ڱ�sstlog������һ��ҵ��״̬====================================
    sstlog_insert_dict = {}
    stat_dict["BCURSQ"] = MaxBCURSQ
    
    if not rccpsMap0000Dstat_dict2Dsstlog.map(stat_dict,sstlog_insert_dict):
        AfaLoggerFunc.tradeFatal("Ϊ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬��ϸ��Ϣ��ֵ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', 'Ϊ���׵�ǰ״̬��ϸ��Ϣ��ֵ�쳣' )
    
    ret = rccpsDBTrcc_sstlog.insert(sstlog_insert_dict)
    
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("�Ǽǽ���[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬��ϸ��Ϣ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǽ��׵�ǰ״̬��ϸ��Ϣ�쳣' )
        
    if MaxBCURSQ == 1:    
        #========��spbsta������һ��ҵ��״̬=====================================
        spbsta_insert_dict = {}
        stat_dict["BCURSQ"] = MaxBCURSQ
        
        if not rccpsMap0000Dstat_dict2Dspbsta.map(stat_dict,spbsta_insert_dict):
            AfaLoggerFunc.tradeFatal("Ϊ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬��ֵ�쳣")
            return AfaFlowControl.ExitThisFlow( 'S999', 'Ϊ���׵�ǰ״̬��ֵ�쳣' )
            
        ret = rccpsDBTrcc_spbsta.insert(spbsta_insert_dict)
        if ret <= 0:
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeFatal("�Ǽǽ���[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬�쳣")
            return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǽ��׵�ǰ״̬�쳣' )
    else:
        #========�޸�spbsta�ж�Ӧҵ��״̬=======================================
        spbsta_update_dict = {}
        stat_dict["BCURSQ"] = MaxBCURSQ
        
        if not rccpsMap0000Dstat_dict2Dspbsta.map(stat_dict,spbsta_update_dict):
            AfaLoggerFunc.tradeFatal("Ϊ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬��ֵ�쳣")
            return AfaFlowControl.ExitThisFlow( 'S999', 'Ϊ���׵�ǰ״̬��ֵ�쳣' )
        
        spbsta_where_dict = {}
        spbsta_where_dict["BJEDTE"] = stat_dict["BJEDTE"]
        spbsta_where_dict["BSPSQN"] = stat_dict["BSPSQN"]
        
        ret = rccpsDBTrcc_spbsta.update(spbsta_update_dict,spbsta_where_dict)
        if (ret <= 0):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeFatal("�Ǽǽ���[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬�쳣")
            return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǽ��׵�ǰ״̬�쳣' )
    AfaLoggerFunc.tradeInfo(">>>����newTransState")
    return True
    
################################################################################
# ������:    getTransStateCur
# ����:      BJEDTE:��������(����),BSPSQN:�������(����),stat_dict(ҵ��״̬��ϸ��Ϣ)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ��ѯ���׵�ǰҵ��״̬�������Ϣ
################################################################################
def getTransStateCur(BJEDTE,BSPSQN,stat_dict):
    AfaLoggerFunc.tradeDebug(">>>����getTransStateCur")
    
    #==========��ȡspbsta��ǰ״̬��Ϣ�����=====================================
    spbsta_where_dict = {}
    spbsta_where_dict["BJEDTE"] = BJEDTE
    spbsta_where_dict["BSPSQN"] = BSPSQN
    
    spbsta_dict = rccpsDBTrcc_spbsta.selectu(spbsta_where_dict)
    
    if spbsta_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ���׵�ǰ״̬�쳣' )
        
    elif len(spbsta_dict) <= 0:
        AfaLoggerFunc.tradeFatal("��ǰ״̬�Ǽǲ����޴˽���[" + BJEDTE + "][" + BSPSQN + "]״̬")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ǰ״̬�Ǽǲ����޴˽���״̬' )
        return False
        
    #===========��ȡsstlog��Ӧ״̬����Ϣ========================================
    sstlog_where_dict = {}
    sstlog_where_dict["BJEDTE"] = spbsta_dict["BJEDTE"]
    sstlog_where_dict["BSPSQN"] = spbsta_dict["BSPSQN"]
    sstlog_where_dict["BCURSQ"] = str(spbsta_dict["BCURSQ"])
    
    sstlog_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
    
    if sstlog_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬��ϸ��Ϣ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ���׵�ǰ״̬��ϸ��Ϣ�쳣' )
        
    if len(sstlog_dict) <= 0:
        AfaLoggerFunc.tradeFatal("��ˮ״̬�Ǽǲ����޴˽���[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬��ϸ��Ϣ")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ˮ״̬�Ǽǲ����޴˽��׵�ǰ״̬��ϸ��Ϣ' )
        
    if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_dict,stat_dict):
        AfaLoggerFunc.tradeFatal("����ѯ���Ľ���[" + BJEDTE + "][" + BSPSQN + "]ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
        
    AfaLoggerFunc.tradeDebug(">>>����getTransStateCur")
    return True

################################################################################
# ������:    getTransStateSet
# ����:      BJEDTE:��������,BSPSQN:�������,BCSTAT:��ǰҵ��״̬,BDWFLG:��ǰ��ת�����ʶ,sstlog_dict(ҵ��״̬��ϸ��Ϣ)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ��ѯ����ָ��ҵ��״̬�������Ϣ
################################################################################
def getTransStateSet(BJEDTE,BSPSQN,BCSTAT,BDWFLG,stat_dict):
    AfaLoggerFunc.tradeInfo(">>>����getTransStateSet")
    
    #==========��ȡsstlog��Ӧ״̬����Ϣ=========================================
    sstlog_where_dict = {}
    sstlog_where_dict["BJEDTE"] = BJEDTE
    sstlog_where_dict["BSPSQN"] = BSPSQN
    sstlog_where_dict["BCSTAT"] = BCSTAT
    sstlog_where_dict["BDWFLG"] = BDWFLG
    
    sstlog_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
    
    if sstlog_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ����[" + BJEDTE + "][" + BSPSQN + "]ָ��״̬��ϸ��Ϣ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ����ָ��״̬��ϸ��Ϣ�쳣' )
        
    if len(sstlog_dict) <= 0:
        AfaLoggerFunc.tradeFatal("��ˮ״̬�Ǽǲ����޴˽���" + BJEDTE + "][" + BSPSQN + "]ָ��״̬[" + BCSTAT + "][" + BDWFLG + "]��ϸ��Ϣ")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ˮ״̬�Ǽǲ����޴˽���ָ��״̬��ϸ��Ϣ' )
        
    if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_dict,stat_dict):
        AfaLoggerFunc.tradeFatal("����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo(">>>����getTransStateSet")
    return True
    
################################################################################
# ������:    getTransStateAll
# ����:      BJEDTE:��������(����),BSPSQN:�������(����),sstlog_list(ҵ��״̬��ϸ��Ϣ)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ��ѯ��������ҵ��״̬�������Ϣ
################################################################################
def getTransStateAll(BJEDTE,BSPSQN,stat_list):
    AfaLoggerFunc.tradeInfo(">>>����getTransStateAll")
    #===========��ȡsstlog����״̬�������Ϣ====================================
    sstlog_where_sql = "BJEDTE = '" + BJEDTE + "' and BSPSQN = '" + BSPSQN + "'"
    sstlog_order_sql = " order by BCURSQ desc "
    
    sstlog_list = rccpsDBTrcc_sstlog.selectm(1,0,sstlog_where_sql,sstlog_order_sql)
    
    if sstlog_list == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ����[" + BJEDTE + "][" + BSPSQN + "]����״̬��ϸ��Ϣ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ��������״̬��ϸ��Ϣ�쳣' )
        
    if len(sstlog_list) <= 0:
        AfaLoggerFunc.tradeFatal("��ˮ״̬�Ǽǲ����޴˽���[" + BJEDTE + "][" + BSPSQN + "]״̬��ϸ��Ϣ")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ˮ״̬�Ǽǲ����޴˽���״̬��ϸ��Ϣ' )
    
    
    for i in xrange(0,len(sstlog_list)):
        stat_dict = {}
        if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_list[i],stat_dict):
            AfaLoggerFunc.tradeFatal("����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣")
            return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
        stat_list.append(stat_dict)
    
    AfaLoggerFunc.tradeInfo(">>>����getTransStateAll")
    return True

################################################################################
# ������:    newBilState
# ����:      BJEDTE:��������(����),BSPSQN:�������(����),HPSTAT:ҵ��״̬(����)}
# ����ֵ��   False  ʧ��    True  �ɹ�
# ����˵���� �½���Ʊ״̬
################################################################################
def newBilState(BJEDTE,BSPSQN,HPSTAT):
    AfaLoggerFunc.tradeInfo(">>>����newBilState")
    #===========����bilbka���Ƿ���ڴ�ҵ��====================================
    bilbka_where_dict = {}
    bilbka_where_dict["BJEDTE"] = BJEDTE
    bilbka_where_dict["BSPSQN"] = BSPSQN
        
    bilbka_dict = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)
    
    if bilbka_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ��Ʊҵ��Ǽǲ��н���[" + BJEDTE + "][" + BSPSQN + "]��ϸ��Ϣ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ��Ʊҵ��Ǽǲ��н�����ϸ��Ϣ�쳣' )
        
    elif len(bilbka_dict) <= 0:
        AfaLoggerFunc.tradeFatal("��Ʊҵ��Ǽǲ����޴˽���[" + BJEDTE + "][" + BSPSQN + "]��ϸ��Ϣ")
        return AfaFlowControl.ExitThisFlow( 'S999', '��Ʊҵ��Ǽǲ����޴˽�����ϸ��Ϣ' )
        
    else:
        MaxHPCUSQ = int(bilbka_dict["HPCUSQ"]) + 1
    
    #===========���±�bilbka��ҵ���Ӧ��Ʊ״̬===================================
    bilbka_update_dict = {}
    bilbka_update_dict["HPCUSQ"] = MaxHPCUSQ
    bilbka_update_dict["HPSTAT"] = HPSTAT
    
    bilbka_where_dict = {}
    bilbka_where_dict["BJEDTE"] = BJEDTE
    bilbka_where_dict["BSPSQN"] = BSPSQN
    
    ret = rccpsDBTrcc_bilbka.update(bilbka_update_dict,bilbka_where_dict)
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("�Ǽǻ�Ʊҵ��Ǽǲ��н���[" + BJEDTE + "][" + BSPSQN + "]��Ӧ��ǰ��Ʊ״̬[" + HPSTAT + "]�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǻ�Ʊҵ��Ǽǲ��е�ǰ��Ʊ״̬�쳣' )
    
    #===========���±�bilinf�л�Ʊ��Ӧ״̬========================================
    bilinf_update_dict = {}
    bilinf_update_dict["HPCUSQ"] = MaxHPCUSQ
    bilinf_update_dict["HPSTAT"] = HPSTAT
    
    bilinf_where_dict = {}
    bilinf_where_dict["BILVER"] = bilbka_dict["BILVER"]
    bilinf_where_dict["BILNO"] = bilbka_dict["BILNO"]
    bilinf_where_dict["BILRS"] = bilbka_dict["BILRS"]
    
    ret = rccpsDBTrcc_bilinf.update(bilinf_update_dict,bilinf_where_dict)
    if ret <= 0:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("�Ǽǻ�Ʊҵ��Ǽǲ��е�ǰ��Ʊ[" + bilbka_dict['BILVER'] + "][" + bilbka_dict['BILVER'] + "]״̬[" + HPSTAT + "]�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '�Ǽǻ�Ʊ��Ϣ�Ǽǲ��е�ǰ��Ʊ״̬�쳣' )
    
    AfaLoggerFunc.tradeInfo(">>>����newBilState")
    return True


################################################################################
# ������:    getTransStateDes
# ����:      BJEDTE:��������,BSPSQN:�������,sstlog_dict(ҵ��״̬��ϸ��Ϣ),Number:��������(Ĭ��Ϊ0,����ǰ״̬)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ��ѯ���׵�ǰҵ��״̬ǰ��N��ҵ�������Ϣ
################################################################################
def getTransStateDes(BJEDTE,BSPSQN,stat_dict,DesNumber=0):
    AfaLoggerFunc.tradeInfo(">>>����getTransStateDes")
    
    if not DesNumber:
        Number = 0
    else:
        Number = int(DesNumber)
        
    #==========��ȡ��ǰҵ��״̬����Ϣ==========================================
    cur_stat_dict = {}
    if not getTransStateCur(BJEDTE,BSPSQN,cur_stat_dict):
        return AfaFlowControl.ExitThisFlow("S999","��ȡ����[" + BJEDTE + "][" + BSPSQN + "]��ǰ״̬��ϸ��Ϣ�쳣")
    
    BCURSQ = cur_stat_dict['BCURSQ'] - Number
    
    if BCURSQ <= 0:
        return AfaFlowControl.ExitThisFlow("S999","��ǰ������ǰ��[" + str(Number) + "]��״̬")
        
    #==========��ȡsstlog��Ӧ״̬����Ϣ=========================================
    sstlog_where_dict = {}
    sstlog_where_dict["BJEDTE"] = BJEDTE
    sstlog_where_dict["BSPSQN"] = BSPSQN
    sstlog_where_dict["BCURSQ"] = BCURSQ
    
    sstlog_dict = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
    
    if sstlog_dict == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ����[" + BJEDTE + "][" + BSPSQN + "]ָ��״̬��ϸ��Ϣ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ���׵�[' + str(BCURSQ) + ']״̬��ϸ��Ϣ�쳣' )
        
    if len(sstlog_dict) <= 0:
        AfaLoggerFunc.tradeFatal("��ˮ״̬�Ǽǲ����޴˽���" + BJEDTE + "][" + BSPSQN + "]ָ��״̬[" + BCSTAT + "][" + BDWFLG + "]��ϸ��Ϣ")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ˮ״̬�Ǽǲ����޴˽��׵�[' + str(BCURSQ) + ']��״̬��ϸ��Ϣ' )
        
    if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_dict,stat_dict):
        AfaLoggerFunc.tradeFatal("����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
    
    AfaLoggerFunc.tradeInfo(">>>����getTransStateDes")
    return True
    
################################################################################
# ������:    getTransStateSetm
# ����:      BJEDTE:��������,BSPSQN:�������,BCSTAT:��ǰҵ��״̬,BDWFLG:��ǰ��ת�����ʶ,sstlog_list(ҵ��״̬��ϸ��Ϣ)
# ����ֵ��   �ɹ�    True
#            ʧ��    False
# ����˵���� ��ѯ����ָ��ҵ��״̬�������Ϣ
################################################################################
def getTransStateSetm(BJEDTE,BSPSQN,BCSTAT,BDWFLG,stat_list):
    AfaLoggerFunc.tradeInfo(">>>����getTransStateSetm")
    
    #==========��ȡsstlog��Ӧ״̬����Ϣ=========================================
    sstlog_where_sql = "BJEDTE LIKE '" + BJEDTE + "' and BSPSQN LIKE '" + BSPSQN + "' and BCSTAT LIKE '" + BCSTAT + "' and BDWFLG LIKE '" + BDWFLG + "'"
    
    sstlog_order_sql = 'order by BCURSQ desc'
    
    sstlog_list = rccpsDBTrcc_sstlog.selectm(1,0,sstlog_where_sql,sstlog_order_sql)
    
    if sstlog_list == None:
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeFatal("��ȡ����[" + BJEDTE + "][" + BSPSQN + "]ָ��״̬��ϸ��Ϣ�쳣")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ȡ����ָ��״̬��ϸ��Ϣ�쳣' )
        
    if len(sstlog_list) <= 0:
        AfaLoggerFunc.tradeFatal("��ˮ״̬�Ǽǲ����޴˽���" + BJEDTE + "][" + BSPSQN + "]ָ��״̬[" + BCSTAT + "][" + BDWFLG + "]��ϸ��Ϣ")
        return AfaFlowControl.ExitThisFlow( 'S999', '��ˮ״̬�Ǽǲ����޴˽���ָ��״̬��ϸ��Ϣ' )
        
    for i in xrange(0,len(sstlog_list)):
        stat_dict = {}
        if not rccpsMap0000Dsstlog2Dstat_dict.map(sstlog_list[i],stat_dict):
            AfaLoggerFunc.tradeFatal("����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣")
            return AfaFlowControl.ExitThisFlow( 'S999', '����ѯ����ҵ��״̬��ϸ��Ϣ��ֵ������ֵ��쳣' )
        stat_list.append(stat_dict)
    
    AfaLoggerFunc.tradeInfo(">>>����getTransStateSetm")
    return True
