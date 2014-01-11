# -*- coding: gbk -*-
##################################################################
#   ũ����ϵͳ.״̬����������
#=================================================================
#   �����ļ�:   rccpsGetFunc.py
#   �޸�ʱ��:   2006-03-31
##################################################################
import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,AfaFlowControl,TransBillFunc,AfaFunc
import exceptions,os,time,rccpsDBTrcc_subbra,rccpsDBTrcc_paybnk
from types import *
from rccpsConst import *


#=======================��ȡƽ̨��ˮ��DB2=======================================
def GetSerialno( BRSFLG, seqName="RCCPS_SEQ" ):

    AfaLoggerFunc.tradeDebug( '>>>��ȡƽ̨��ˮ��' )
    #=====�Ƿ�Ϊ����ҵ��====
    if BRSFLG == PL_BRSFLG_SND:
        #=====�жϻ������Ƿ����====
        if( not TradeContext.existVariable( "BESBNO" ) ):
            raise AfaFlowControl.ExitThisFlow('M999','�޻����ţ�����ʧ��' )

    #=====���˻�����ȡ��3��6λ====
    TradeContext.Serialno = TradeContext.BESBNO[2:6]

    AfaLoggerFunc.tradeInfo('>>>��ʼ�жϽ��״���')
    #====�жϽ��״����Ƿ���ڣ�����7λ���룩====
    if( not TradeContext.existVariable( "TRCCO" ) ):
        raise AfaFlowControl.ExitThisFlow('M999','���״���[TRCCO]�ֶ�ֵ������' )
    #=====�ж�ҵ������,���ݽ���ȡ��ͬ����====
    AfaLoggerFunc.tradeInfo('>>>��ʼ�ж�ҵ������')
    if not GetTRCCO():
        raise AfaFlowControl.ExitThisFlow('M999','ȡҵ������ʧ��' )
    #=====������ˮ��====
    AfaLoggerFunc.tradeInfo('>>>��ʼ���ɽ�����ˮ��')
    sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
    #��"0"(6λ)
    #=====��ˮ�Ź���4λ������+1λҵ������+1λ�����˱�־+6λ˳���
    TradeContext.BSPSQN=TradeContext.Serialno+BRSFLG+str(records[0][0]).rjust(6,'0' )

    AfaLoggerFunc.tradeInfo( 'ƽ̨��ˮ��' + TradeContext.BSPSQN )

    return str( records[0][0] )

################################################################################
# ������:    GetTRCCO()
# ����:      ��
# ����ֵ��    True  ����״̬�ɹ�    False ����״̬ʧ��
# ����˵����  ���ݽ��״������ҵ������
# ��дʱ�䣺   2008-6-5
# ���ߣ�       ������
################################################################################
def GetTRCCO():
    #=====���ҵ��ҵ������Ϊ1====
    if( TradeContext.TRCCO=='2000001' or TradeContext.TRCCO=='2000002' or
       TradeContext.TRCCO=='2000003' or TradeContext.TRCCO=='2000004' or
       TradeContext.TRCCO=='2000009'):
        TradeContext.Serialno = TradeContext.Serialno + '1'
    #=====��Ʊҵ��ҵ������Ϊ2====
    #elif( TradeContext.TRCCO=='2100001' or TradeContext.TRCCO=='2100100' or
    #   TradeContext.TRCCO=='2100101' or TradeContext.TRCCO=='2100102' or
    #   TradeContext.TRCCO=='2100103'):
    # �ر�� 20080913 ����2100104���ҵ��
    elif( TradeContext.TRCCO=='2100001' or TradeContext.TRCCO=='2100100' or
       TradeContext.TRCCO=='2100101' or TradeContext.TRCCO=='2100102' or
       TradeContext.TRCCO=='2100103' or TradeContext.TRCCO=='2100104'):
        TradeContext.Serialno = TradeContext.Serialno + '2'
    #=====ͨ��ͨ��ҵ��ҵ������Ϊ3====
    elif( TradeContext.TRCCO=='3000001' or TradeContext.TRCCO=='3000100' or
       TradeContext.TRCCO=='3000101' or TradeContext.TRCCO=='3000500' or
       TradeContext.TRCCO=='3000002' or TradeContext.TRCCO=='3000003' or
       TradeContext.TRCCO=='3000102' or TradeContext.TRCCO=='3000103' or
       TradeContext.TRCCO=='3000501' or TradeContext.TRCCO=='3000004' or
       TradeContext.TRCCO=='3000005' or TradeContext.TRCCO=='3000104' or
       TradeContext.TRCCO=='3000105' or TradeContext.TRCCO=='3000502' or
       TradeContext.TRCCO=='3000503' or TradeContext.TRCCO=='3000504' or
       TradeContext.TRCCO=='3000505' or TradeContext.TRCCO=='3000506' or
       TradeContext.TRCCO=='3000507' ):
        TradeContext.Serialno = TradeContext.Serialno + '3'
    #=====��Ҳ�ѯ�鸴���ɸ�ʽ��ҵ������Ϊ4====
    elif( TradeContext.TRCCO=='9900511' or TradeContext.TRCCO=='9900512' or
       TradeContext.TRCCO=='9900513' or TradeContext.TRCCO=='9900520' or
       TradeContext.TRCCO=='9900521' or TradeContext.TRCCO=='9900522' or
       TradeContext.TRCCO=='9900523' or TradeContext.TRCCO=='9900524'):
        TradeContext.Serialno = TradeContext.Serialno + '4'
    #=====��Ʊ��ѯ�鸴,�������룬ҵ������Ϊ5====
    elif( TradeContext.TRCCO=='9900526' or TradeContext.TRCCO=='9900527' or
       TradeContext.TRCCO=='9900501' or TradeContext.TRCCO=='9900502' or
       TradeContext.TRCCO=='9900506' or TradeContext.TRCCO=='9900507'):
        TradeContext.Serialno = TradeContext.Serialno + '5'
    else:
        TradeContext.Serialno = TradeContext.Serialno + '6'

    return TradeContext.Serialno
################################################################################
# ������:    GetRccSerialno()
# ����:      TRCCO
# ����ֵ��    True  ����״̬�ɹ�    False ����״̬ʧ��
# ����˵����  ���ݽ��״���������ˮ��
# ��дʱ�䣺   2008-6-5
# ���ߣ�       ������
################################################################################
def GetRccSerialno( seqName="RCC_SEQ" ):
    AfaLoggerFunc.tradeDebug( '>>>��ʼ���ɽ�����ˮ��' )
    #=====�жϽ��״����Ƿ����====
    if not TradeContext.existVariable("TRCCO"):
        return AfaFlowControl.ExitThisFlow('M999', '���״��벻����')
    elif (TradeContext.TRCCO=='2000009' or TradeContext.TRCCO=='9900522'
        or TradeContext.TRCCO=='9900523' or TradeContext.TRCCO=='9900524'):
        #=====����4λ����ˮ��====
        sqlStr = "SELECT NEXTVAL FOR TYHD_SEQ FROM SYSIBM.SYSDUMMY1"
        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
        TradeContext.SerialNo=str( records[0][0] ).rjust( 8, '0' )
    else:
        #=====������ˮ��====
        sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
        TradeContext.SerialNo=str( records[0][0] ).rjust( 8, '0' )

    AfaLoggerFunc.tradeInfo( '������ˮ��' + TradeContext.SerialNo )

    return TradeContext.SerialNo



################################################################################
# ������:    GetRcvBnkCo()
# ����:      RCVBNKCO
# ����ֵ��    True  ����״̬�ɹ�    False ����״̬ʧ��
# ����˵����  ���ݽ����к�ȡ�����з����г�Ա��
# ��дʱ�䣺   2008-6-15
# ���ߣ�       ������
################################################################################
def GetRcvBnkCo(RCVBNKCO):
    #=====ͨ�������к�ȡ�����г�Ա�к�====
    if (TradeContext.existVariable("RCVBNKCO") and len(RCVBNKCO)!=0):
        rcvstl = {'BANKBIN':TradeContext.RCVBNKCO}
        rcvpyb = rccpsDBTrcc_paybnk.selectu(rcvstl)
        if (rcvpyb == None or len(rcvpyb) == 0):
            return AfaFlowControl.ExitThisFlow('M999','�����к�ȡ���ճ�Ա�к�����Ӧ��¼')
        else:
            TradeContext.RCVSTLBIN = rcvpyb['STLBANKBIN']
            TradeContext.RCVBNKNM  = rcvpyb['BANKNAM']
    else:
        return False

    return TradeContext.RCVSTLBIN
################################################################################
# ������:    GetSndBnkCo()
# ����:      SNDBNKCO
# ����ֵ��    True  ����״̬�ɹ�    False ����״̬ʧ��
# ����˵����  ���ݽ����к�ȡ�����з����г�Ա��
# ��дʱ�䣺   2008-6-15
# ���ߣ�       ������
################################################################################
def GetSndBnkCo(SNDBNKCO):
    #=====ͨ�������к�ȡ�����г�Ա�к�====
    if (TradeContext.existVariable("SNDBNKCO") and len(SNDBNKCO)!=0):
        rcvstl = {'BANKBIN':TradeContext.SNDBNKCO}
        rcvpyb = rccpsDBTrcc_paybnk.selectu(rcvstl)
        if (rcvpyb == None or len(rcvpyb) == 0):
            return AfaFlowControl.ExitThisFlow('M999','�����к�ȡ���ճ�Ա�к�����Ӧ��¼')
        else:
            TradeContext.SNDSTLBIN = rcvpyb['STLBANKBIN']
            TradeContext.SNDBNKNM  = rcvpyb['BANKNAM']
    else:
        return False

    return TradeContext.SNDSTLBIN
    
    
#=======================��ȡǰ����ˮ��DB2=======================================
def GetRBSQ( BRSFLG, seqName="RCCPS_SEQ" ):

    AfaLoggerFunc.tradeDebug( '>>>��ȡǰ����ˮ��' )
    #=====�Ƿ�Ϊ����ҵ��====
    if BRSFLG == PL_BRSFLG_SND:
        #=====�жϻ������Ƿ����====
        if( not TradeContext.existVariable( "BESBNO" ) ):
            raise AfaFlowControl.ExitThisFlow('M999','�޻����ţ�����ʧ��' )

    #=====���˻�����ȡ��3��6λ====
    TradeContext.Serialno = TradeContext.BESBNO[2:6]

    AfaLoggerFunc.tradeDebug('>>>��ʼ�жϽ��״���')
    #====�жϽ��״����Ƿ���ڣ�����7λ���룩====
    if( not TradeContext.existVariable( "TRCCO" ) ):
        raise AfaFlowControl.ExitThisFlow('M999','���״���[TRCCO]�ֶ�ֵ������' )
    #=====�ж�ҵ������,���ݽ���ȡ��ͬ����====
    AfaLoggerFunc.tradeDebug('>>>��ʼ�ж�ҵ������')
    if not GetTRCCO():
        raise AfaFlowControl.ExitThisFlow('M999','ȡҵ������ʧ��' )
    #=====������ˮ��====
    AfaLoggerFunc.tradeInfo('>>>��ʼ����ǰ����ˮ��')
    sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
    #��"0"(6λ)
    #=====��ˮ�Ź���4λ������+1λҵ������+1λ�����˱�־+6λ˳���
    TradeContext.RBSQ=TradeContext.Serialno+BRSFLG+str(records[0][0]).rjust(6,'0' )

    AfaLoggerFunc.tradeInfo( '>>>ǰ����ˮ��' + TradeContext.RBSQ )

    return str( records[0][0] )
