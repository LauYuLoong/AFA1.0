# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.��ִ�����ģ��(1.��ִ����).ͨ��_��Ӧ��
#==============================================================================
#   �����ļ�:   TRCC004_1157.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  ������
#   �޸�ʱ��:   2008-11-04
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState,rccpsDBTrcc_atcbka,rccpsHostFunc

#=====================��ִ���Ի�����(���ز���)=================================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�����ֽ�ͨ��_��Ӧ��[TRCC004_1157]����***' )

    #=================��ʼ��������Ϣ============================================
    if AfaUtilTools.trim(TradeContext.STRINFO) == "":
        TradeContext.STRINFO = rccpsDBFunc.getErrInfo(TradeContext.PRCCO)
        
    AfaLoggerFunc.tradeDebug("TradeContext.STRINFO=" + TradeContext.STRINFO)

    #=====���ݲο����ı�ʶ�Ų���ԭ����====
    TradeContext.ORSNDBNKCO = TradeContext.ORMFN[:10]                #ԭ�����к�
    TradeContext.BOJEDT     = TradeContext.ORMFN[10:18]              #ԭ��������
    TradeContext.ORTRCNO    = TradeContext.ORMFN[18:]                #ԭ������ˮ��

    wtr_dict = {}
    if not rccpsDBFunc.getTransWtrAK(TradeContext.ORSNDBNKCO,TradeContext.BOJEDT,TradeContext.ORTRCNO,wtr_dict):
        #=====��ѯԭ����ʧ�ܣ��ȴ�ǰ̨��ʱ��������������˱���====       
        return AfaFlowControl.ExitThisFlow('S999','�ȴ�ǰ̨�����������������') 

    AfaLoggerFunc.tradeInfo( '>>>��ѯԭ���׽���' )

    #=================��Ӧ���Ļظ��ܾ�,������״̬Ϊ�ܾ�,ֹͣ����=============
    if TradeContext.PRCCO != 'RCCI0000':
        AfaLoggerFunc.tradeInfo(">>>�Է����ؾܾ�Ӧ��")
        
        #=============����ҵ��״̬Ϊ�ܾ�������=================================
        
        if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_MFERFE,PL_BDWFLG_WAIT):
            return AfaFlowControl.ExitThisFlow('S999',"����ҵ��״̬Ϊ�ܾ��ɹ��쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
        #=============����ҵ��״̬Ϊ�ܾ��ɹ�===================================
        stat_dict = {}
        stat_dict['BJEDTE']  = wtr_dict['BJEDTE']
        stat_dict['BSPSQN']  = wtr_dict['BSPSQN']
        stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        stat_dict['PRCCO']   = TradeContext.PRCCO
        stat_dict['STRINFO'] = TradeContext.STRINFO
        
        if not rccpsState.setTransState(stat_dict):
            return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ�ܾ��ɹ��쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return AfaFlowControl.ExitThisFlow("S999","Commit�쳣")
            
        return AfaFlowControl.ExitThisFlow('S999',"�Է��ܾ���������ֹ")
            
    #====�����Զ������Ǽǲ��Ƿ���ڱ����׵ĳ���====
    wheresql = ''
    wheresql = wheresql + "BOJEDT = '" + wtr_dict['BJEDTE'] + "'"                #��������
    wheresql = wheresql + "AND BOSPSQ = '" + wtr_dict['BSPSQN'] + "'"                #�������
    
    ret = rccpsDBTrcc_atcbka.count(wheresql)
    if ret == -1:
        return AfaFlowControl.ExitThisFlow('S999','�����Զ������Ǽǲ��쳣') 
    elif ret > 0:
        #=====ԭ�������Զ���������������====
        return AfaFlowControl.ExitThisFlow('S999','ԭ�����ѳ�������������') 

    AfaLoggerFunc.tradeInfo( '>>>��ѯ�����Ǽǲ�����' )

    #=====��������ǰ����====
    TradeContext.BESBNO  =  wtr_dict['BESBNO']      #������
    TradeContext.BETELR  =  wtr_dict['BETELR']      #��Ա��
    TradeContext.BEAUUS  =  wtr_dict['BEAUUS']      #��Ȩ��Ա
    TradeContext.BEAUPS  =  wtr_dict['BEAUPS']      #��Ȩ����
    TradeContext.TERMID  =  wtr_dict['TERMID']      #�ն˺�
    TradeContext.BJEDTE  =  wtr_dict['BJEDTE']      #��������
    TradeContext.BSPSQN  =  wtr_dict['BSPSQN']      #�������
    TradeContext.BRSFLG  =  wtr_dict['BRSFLG']      #�����˱�־
    TradeContext.HostCode=  '8813'                  #����������

    AfaLoggerFunc.tradeInfo( '>>>����ǰ����ֵ����' )

    #=====��ʼ����ԭ����,����״̬���ˣ�������====
    if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_WAIT):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '����״̬ʧ��,ϵͳ�Զ��ع�')
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
    
    AfaLoggerFunc.tradeInfo( '>>>����״̬����-�����н���' )
    
    #=====����ԭ��¼�е���������ȡ��ʽ���ж�������ģʽ====
    if wtr_dict['CHRGTYP'] == '1':
        #=====ת��====
        TradeContext.ACUR    =  '3'                                           #���˴���
        
        #=========���׽��+������===================
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDWZ                              #ժҪ���� 
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS           #�����˺�
        TradeContext.RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
        TradeContext.OTNM    =  'Ӧ����'                                    #��������
        TradeContext.OCCAMT  =  str(wtr_dict['OCCAMT'] + wtr_dict['CUSCHRG']) #������
        TradeContext.PKFG    = 'T'                                            #����֧Ʊ��־
        TradeContext.CTFG    = '9'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.RBAC )
        #=========���׽��============
        TradeContext.I2SMCD  =  PL_RCCSMCD_XJTDWZ                              #ժҪ����
        TradeContext.I2SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I2SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2SBAC,25)
        TradeContext.I2ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I2RBAC  =  ''                                            #�����˺�
        TradeContext.I2OTNM  =  ''                                            #��������
        TradeContext.I2TRAM  =  str(wtr_dict['OCCAMT'])                       #������
        TradeContext.I2CTFG  = '7'                                            #��ת��־ 0 ��ת 1 ����ת
        TradeContext.I2PKFG  = 'T'                                            #����֧Ʊ��־
        #TradeContext.I2WARNTNO = ''
        #TradeContext.I2CERTTYPE = ''
        #TradeContext.I2CERTNO = ''
        TradeContext.I2CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
        #=========�������������뻧===========
        TradeContext.I3SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
        TradeContext.I3SBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
        TradeContext.I3SBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
        TradeContext.I3ACNM  =  'Ӧ����'                                    #�跽����
        TradeContext.I3RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I3RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
        TradeContext.I3OTNM  =  '����������'                                  #��������
        TradeContext.I3TRAM  =  str(wtr_dict['CUSCHRG'])                      #������
        TradeContext.I3CTFG  = '8'                                            #��ת��־ 0 ��ת 1 ����ת
        TradeContext.I3PKFG  = 'T'                                            #����֧Ʊ��־
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I3SBAC )
        AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I3RBAC )

    elif wtr_dict['CHRGTYP'] == '0':
        #=====����====
        TradeContext.ACUR    =  '2'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDWZ                              #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    = rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.ACNM    =  'ũ��������'                                  #�跽����
        TradeContext.RBAC    =  ''                                            #�����˺�
        TradeContext.OTNM    =  ''                                            #��������
        TradeContext.OCCAMT  =  str(wtr_dict['OCCAMT'])                       #���
        TradeContext.CTFG  = '7'
        TradeContext.PKFG  = 'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        TradeContext.CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )
        
        #=====�����Ѽ��˸�ֵ====
        TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
        TradeContext.I2SBAC  =  ''                                            #�跽�˺�
        TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_TCTDSXF          #�����˺�
        TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
        TradeContext.I2OTNM  =  '�����ѿ�Ŀ'                                  #��������
        TradeContext.I2TRAM  =  str(wtr_dict['CUSCHRG'])                      #���
        TradeContext.I2CTFG  =  '8'
        TradeContext.I2PKFG  =  'T'
        TradeContext.I2CATR  =  '0'                                           #��ת��־
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.I2SBAC )
        AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.I2RBAC )
    elif wtr_dict['CHRGTYP'] == '2':
        #=====���շ�====
        TradeContext.ACUR    =  '1'                                           #���˴���
        TradeContext.RCCSMCD =  PL_RCCSMCD_XJTDWZ                                #ժҪ����
        TradeContext.SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSWZ         #�跽�˺�
        TradeContext.SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.SBAC,25)
        TradeContext.RBAC    =  ''                                            #�����˺�
        TradeContext.OTNM    =  ''                                            #��������
        TradeContext.OCCAMT  =  str(wtr_dict['OCCAMT'])                       #���
        TradeContext.CTFG    =  '7'
        TradeContext.PKFG    =  'T'
        TradeContext.WARNTNO = ''
        TradeContext.CERTTYPE = ''
        TradeContext.CERTNO = ''
        TradeContext.CATR  =  '0'                                             #��ת��־
    else:
        #=====����====
        return AfaFlowControl.ExitThisFlow('S999','�������շѷ�ʽ����������') 
    
    AfaLoggerFunc.tradeInfo( '>>>������������ȡ��ʽ���˸�ֵ�������' )
    
    #=====�������˴���====
    rccpsHostFunc.CommHost(TradeContext.HostCode)
    
    #=====��������====
    set_dict = {}
    set_dict['BSPSQN']  =  TradeContext.BSPSQN
    set_dict['BJEDTE']  =  TradeContext.BJEDTE
    set_dict['BCSTAT']  =  PL_BCSTAT_ACC
    set_dict["SBAC"]    =  TradeContext.SBAC          #�跽�˺�
    set_dict["RBAC"]    =  TradeContext.RBAC          #�����˺�
    set_dict["OTNM"]    =  TradeContext.OTNM          #��������
    set_dict['MGID']    =  TradeContext.errorCode     #����������
    set_dict["STRINFO"]= TradeContext.errorMsg    #����������Ϣ
    if TradeContext.errorCode == '0000':
        #=====�������˳ɹ�====
        set_dict['BDWFLG'] = PL_BDWFLG_SUCC
        set_dict['TRDT']   = TradeContext.TRDT
        set_dict['TLSQ']   = TradeContext.TLSQ
    else:
        set_dict['BDWFLG'] = PL_BDWFLG_FAIL
    
    if not rccpsState.setTransState(set_dict):
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
    AfaLoggerFunc.tradeInfo('>>>������������״̬�ɹ�') 
    
    if TradeContext.errorCode == '0000':
        #=====��ʼ����ԭ����,����״̬����ɹ�====
        if not rccpsState.newTransState(wtr_dict['BJEDTE'],wtr_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_SUCC):
            #=====RollBack����====
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('M999', '����״̬ʧ��,ϵͳ�Զ��ع�')
        else:
            #=====commit����====
            AfaDBFunc.CommitSql()

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).�����ֽ�ͨ��_��Ӧ��[TRCC004_1157]�˳�***' )
    
    return True
