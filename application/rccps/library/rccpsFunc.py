# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ.����������
#===============================================================================
#   �����ļ�:   RccpsFunc.py
#   �޸�ʱ��:   2006-09-26
################################################################################
import exceptions,TradeContext,AfaDBFunc,TradeException,AfaUtilTools,ConfigParser,Party3Context,AfaLoggerFunc,AfaFlowControl,os,time
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_subbra,rccpsDBTrcc_paybnk

from rccpsConst import *
from types import *

#========================================================================
#
#  �������ƣ�ChkPubInfo
#  ��ڲ����� 
#  ���ڲ����� Ture False
#  ��    �ߣ� ������
#  ��    �ڣ� 20080610
#  ��    �ܣ� У�齻�ױ����Ƿ����
#
#========================================================================
def ChkPubInfo(BRSFLG):

    AfaLoggerFunc.tradeInfo( '>>>���ױ���ֵ����Ч��У��' )
    if( not TradeContext.existVariable( "sysId" ) ):
        TradeContext.sysId = 'RCC01'

    AfaLoggerFunc.tradeInfo('ƽ̨���룺' + TradeContext.sysId)
        
    if BRSFLG == PL_BRSFLG_SND:
        if( not TradeContext.existVariable( "BESBNO" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[BESBNO]ֵ������!' )

        if( not TradeContext.existVariable( "BETELR" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[BETELR]ֵ������!' )
    else:    #PL_BRSFLG_RCV   ����
        if( not TradeContext.existVariable( "TRCCO" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '���״���[TRCCO]ֵ������!' )
        if( not TradeContext.existVariable( "BRSFLG" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������ʶ[BRSFLG]ֵ������!' )

    return True
#========================================================================
#
#  �������ƣ�ChkSysInfo
#  ��ڲ����� AFA:�м�ҵ��ƽ̨  RCCPS:�м�ҵ��ƽ̨&ũ����ϵͳ 
#  ���ڲ����� Ture False
#  ��    �ߣ� ������
#  ��    �ڣ� 20080610
#  ��    �ܣ� �������ΪAFAʱ��ֻУ���м�ҵ��ƽ̨״̬�Ƿ�����
#             �������RCCPSʱ��У���м�ҵ��ƽ̨״̬������Ҫ
#             ����У��ũ����ϵͳ״̬�Ƿ�Ϊ�ռ�״̬
#
#========================================================================
def ChkSysInfo( flag ):
   
    AfaLoggerFunc.tradeInfo( '>>>ϵͳƽ̨״̬��Ч��У��' )
    sql = "select status from afa_system where sysid='"
    sql = sql + TradeContext.sysId + "'"
    records=AfaDBFunc.SelectSql( sql )
    if( records == None ):
        return AfaFlowControl.ExitThisFlow('A0025', "�м�ҵ��ƽ̨���ݿ����ʧ��" )
    elif( len( records ) == 0 ):
        return AfaFlowControl.ExitThisFlow('A0025', "�м�ҵ��ƽ̨ũ����ϵͳ�޼�¼" )
    elif( records[0][0] != '1' ):
        return AfaFlowControl.ExitThisFlow('A0025', "�м�ҵ��ƽ̨_ũ����ϵͳ�ѹر�" )
    else:
        if flag == 'RCCPS':
            AfaLoggerFunc.tradeInfo( '>>>ũ����ϵͳ״̬��Ч��У��' )
            if ((not TradeContext.existVariable("TRCCO")) or len(TradeContext.TRCCO) == 0):
                return AfaFlowControl.ExitThisFlow('M999', "�ֶ�[TRCCO]Ϊ�մ���")

            #=====��ѯũ����ϵͳ״̬====
            if((TradeContext.TRCCO[0:2] == PL_TRCCO_HD) or (TradeContext.TRCCO == PL_TRCCO_HP)):
                dict = {'OPRTYPNO':PL_TRCCO_HD}
            #elif((TradeContext.TRCCO[0:2] == PL_TRCCO_TCTD) or (TradeContext.TRCCO == PL_TRCCO_QT)):
            else:
                dict = {'OPRTYPNO':PL_TRCCO_TCTD}

            records=rccpsDBTrcc_mbrifa.selectu( dict )
            AfaLoggerFunc.tradeInfo( 'record=' + str(records) )
            if( records == None ):
                return AfaFlowControl.ExitThisFlow('A0025', "ũ����ϵͳ�������ݿ�ʧ��" )
            if( len(records) <= 0 ):
                return AfaFlowControl.ExitThisFlow('A0025', "ũ����ϵͳû�п�ʼӪҵ" )
            elif( records['NWSYSST'] != '10' ):
                return AfaFlowControl.ExitThisFlow('A0025', "ũ����ϵͳû�п�ʼӪҵ" )
            else:
                AfaLoggerFunc.tradeInfo( '>>>ũ����ϵͳ״̬����' )

    AfaLoggerFunc.tradeInfo( '>>>ϵͳ״̬У������' )
    return True
#========================================================================
#
#  �������ƣ� ChkUnitInfo
#  ��ڲ����� BRSFLG 
#  ���ڲ����� Ture False
#  ��    �ߣ� ������
#  ��    �ڣ� 20080610
#  ��    �ܣ� ���BRSFLG �� 1 ��ʾ���ˣ���Ҫͨ�������к�ȡ������
#                 BRSFLG �� 0 ��ʾ���ˣ���Ҫ���ݻ�����ȡ�����к�
#                 SUBFLG = PL_SUBFLG_AGE   ��ʾ����
#                 SUBFLG = PL_SUBFLG_SUB   ��ʾ������
#
#========================================================================
def ChkUnitInfo( BRSFLG ):
    if BRSFLG == PL_BRSFLG_SND:
        AfaLoggerFunc.tradeInfo( '>>>��ʼͨ��������ȡ�к�' )
        #=====ͨ��ͨ��ҵ��ֱ��ʹ�����������к�====
        if TradeContext.existVariable('TRCCO') and TradeContext.TRCCO[:2] == '30':
            subbra = {'BESBNO':PL_BESBNO_BCLRSB}
        else:            
            #=====��ʼ���ֵ丳ֵ==== 
            subbra = {'BESBNO':TradeContext.BESBNO}
            
        #=====��ѯ�����к�====
        sub = rccpsDBTrcc_subbra.selectu(subbra)
        if sub == None:
            return AfaFlowControl.ExitThisFlow('M999','���ݿ����')
        if len(sub) <= 0:
            #return AfaFlowControl.ExitThisFlow('M999','������ȡ�����к��޶�Ӧ��¼')
            return AfaFlowControl.ExitThisFlow('M999','�Ƿ�����')
        else:
            AfaLoggerFunc.tradeDebug('>>>BTOPSB['+sub['BTOPSB']+']')
            #=====������ 2008-07-25 �������������ѯ====
            if sub['SUBFLG'] == PL_SUBFLG_SUB :     #������,'0' �ź�20091201 �滻0 
                sel_sub = {'BESBNO':sub['BTOPSB']}
                                
                sel = rccpsDBTrcc_subbra.selectu(sel_sub)
                if sel == None:
                    return AfaFlowControl.ExitThisFlow('M999','���ݿ����')
                if len(sel) <= 0:
                    return AfaFlowControl.ExitThisFlow('M999','�Ƿ�����')
                else:
                    TradeContext.SNDBNKCO = sel['BANKBIN']
            else:
                TradeContext.SNDBNKCO = sub['BANKBIN']

            AfaLoggerFunc.tradeInfo( '�����к�[SNDBNKCO]:' + TradeContext.SNDBNKCO )
            #====ͨ�������к�ȡ����====
            paybnk = {'BANKBIN':TradeContext.SNDBNKCO}
            pyb = rccpsDBTrcc_paybnk.selectu(paybnk)
            if pyb == None:
                return AfaFlowControl.ExitThisFlow('M999','���ݿ��������')
            if len(pyb) <= 0:
                #return AfaFlowControl.ExitThisFlow('M999','�к�ȡ������������Ӧ��¼')
                return AfaFlowControl.ExitThisFlow('M999','�Ƿ�����')
            else:
                #if( (TradeContext.BJEDTE < pyb['EFCTDAT'] or pyb['BANKSTATUS'] != '1') and len(TradeContext.SNDBNKCO) == 10 ):
                #�ر��  20081222 �޸��к���ЧʧЧ�ж�
                if( pyb['NOTE1'] != '1' ):
                    return AfaFlowControl.ExitThisFlow('M999','�����к�δ��Ч')
                else:
                    TradeContext.SNDBNKNM = pyb['BANKNAM'] 
                    TradeContext.SNDSTLBIN = pyb['STLBANKBIN']
                    AfaLoggerFunc.tradeDebug( '��������[SNDBNKNM]:' + TradeContext.SNDBNKNM )
                    AfaLoggerFunc.tradeDebug( '���ͳ�Ա�к�[SNDSTLBIN]:' + TradeContext.SNDSTLBIN )

            #=====ͨ�������к�ȡ�����г�Ա�к�====
            if (TradeContext.existVariable("RCVBNKCO") and len(TradeContext.RCVBNKCO) == 10):
            #if len(TradeContext.RCVBNKCO) == 10:
                AfaLoggerFunc.tradeDebug('>>>��ͨ����к�')
                rcvstl = {'BANKBIN':TradeContext.RCVBNKCO}
                rcvpyb = rccpsDBTrcc_paybnk.selectu(rcvstl)
                if rcvpyb == None:
                    return AfaFlowControl.ExitThisFlow('M999','���ݿ��������')
                if len(rcvpyb) <= 0:
                    return AfaFlowControl.ExitThisFlow('M999','�����к�ȡ���ճ�Ա�к�����Ӧ��¼')
                else:
                    TradeContext.RCVSTLBIN = rcvpyb['STLBANKBIN'] 
                    TradeContext.RCVBNKNM  = rcvpyb['BANKNAM'] 
                    AfaLoggerFunc.tradeDebug('>>>��������['+TradeContext.RCVBNKNM+']')
                    AfaLoggerFunc.tradeDebug('>>>���ճ�Ա�к�['+TradeContext.RCVSTLBIN+']')

                #=====ͨ��OPRTYPNO�жϷ�����Ȩ�޺ͽ�����Ȩ��====
                if TradeContext.TRCCO[0:2] == '20':
                    #=====�жϽ����к�====
                    if rcvpyb['PRIVILEGE'][0:1] != '1':
                        return AfaFlowControl.ExitThisFlow('M999','�˽����к���δ�����ҵ��')
                elif TradeContext.TRCCO[0:2] == '21':
                    #=====�жϽ����к�====
                    if rcvpyb['PRIVILEGE'][1:2] != '1':
                        return AfaFlowControl.ExitThisFlow('M999','�˽����к���δ��ͨ��Ʊҵ��')
                elif TradeContext.TRCCO[0:2] == '30':
                    #=====�жϽ����к�====
                    if rcvpyb['PRIVILEGE'][2:3] != '1':
                        return AfaFlowControl.ExitThisFlow('M999','�˽����к���δ��ͨͨ��ͨ��ҵ��')
                AfaLoggerFunc.tradeDebug('>>>���ճ�Ա�к�Ȩ���ж����')
            #elif len(TradeContext.RCVBNKCO) < 10:
            else:
                if not TradeContext.existVariable('RCVBNKCO'):
                    TradeContext.RCVBNKCO = '1000000000'  
                                                                         
                    #=====ͨ���к�������====
                    paybnk_dict = {'BANKBIN':TradeContext.RCVBNKCO}
                    pyba = rccpsDBTrcc_paybnk.selectu(paybnk_dict)
                    if pyba == None:
                        return AfaFlowControl.ExitThisFlow('M999','���ݿ��������')
                    if len(pyba) <= 0:
                        return AfaFlowControl.ExitThisFlow('M999','�к�ȡ������������Ӧ��¼')
                    else:
                        TradeContext.RCVBNKNM = pyba['BANKNAM']
                        AfaLoggerFunc.tradeInfo( '��������[RCVBNKNM]:' + TradeContext.RCVBNKNM )
                         
                        if len(str(pyba['STLBANKBIN'])) == 0:
                            TradeContext.RCVSTLBIN = '9999999997' 
                        else:
                            TradeContext.RCVSTLBIN = pyba['STLBANKBIN']
                        
                        AfaLoggerFunc.tradeInfo( '���ճ�Ա�к�[RCVSTLBIN]:' + TradeContext.RCVSTLBIN )
                elif len(TradeContext.RCVBNKCO) == 0:
                    TradeContext.RCVBNKCO = ' '
                elif len(TradeContext.RCVBNKCO) == 7:
                    #=====ͨ���к�������====
                    paybnk_dict = {'BANKBIN':TradeContext.RCVBNKCO}
                    pyba = rccpsDBTrcc_paybnk.selectu(paybnk_dict)
                    if pyba == None:
                        return AfaFlowControl.ExitThisFlow('M999','���ݿ��������')
                    if len(pyba) <= 0:
                        return AfaFlowControl.ExitThisFlow('M999','�к�ȡ������������Ӧ��¼')
                    else:
                        TradeContext.RCVBNKNM = pyba['BANKNAM']
                        AfaLoggerFunc.tradeInfo( '��������[RCVBNKNM]:' + TradeContext.RCVBNKNM )
                         
                        if len(str(pyba['STLBANKBIN'])) == 0:
                            TradeContext.RCVSTLBIN = '9999999997' 
                        else:
                            TradeContext.RCVSTLBIN = pyba['STLBANKBIN']
                        
                        AfaLoggerFunc.tradeInfo( '���ճ�Ա�к�[RCVSTLBIN]:' + TradeContext.RCVSTLBIN )
                

            #=====ͨ��OPRTYPNO�жϷ�����Ȩ�޺ͽ�����Ȩ��====
            if TradeContext.TRCCO[0:2] == '20':
                #=====�жϷ����к�====
                if pyb['PRIVILEGE'][0:1] != '1':
                    return AfaFlowControl.ExitThisFlow('M999','�˷����к���δ��ͨ���ҵ��')
            #=====������ 20081013 ��������Ʊ�⸶��ͬ���ҵ��Ȩ��====
            elif (TradeContext.TRCCO[0:2] == '21'  and TradeContext.TRCCO != '2100100'):
                #=====�жϷ����к�====
                if pyb['PRIVILEGE'][1:2] != '1':
                    return AfaFlowControl.ExitThisFlow('M999','�˷����к���δ��ͨ��Ʊҵ��')
            elif TradeContext.TRCCO[0:2] == '30':
                #=====�жϷ����к�====
                if pyb['PRIVILEGE'][2:3] != '1':
                    return AfaFlowControl.ExitThisFlow('M999','�˷����к���δ��ͨͨ��ͨ��ҵ��')
            AfaLoggerFunc.tradeDebug('>>>�����Ա�к�Ȩ���ж����')
           
    elif BRSFLG == PL_BRSFLG_RCV:
        AfaLoggerFunc.tradeInfo( '>>>��ʼͨ���к�ȡ������' )
        #=====�жϽ����к��Ƿ����====
        if not TradeContext.existVariable( "RCVBNKCO" ):
            TradeContext.BESBNO = PL_BESBNO_BCLRSB
            TradeContext.BETELR = PL_BETELR_AUTO
            AfaLoggerFunc.tradeInfo( '������[BESBNO]:' + TradeContext.BESBNO )
            return True

        #====��ʼ���ֵ丳ֵ====
        suba = {'BANKBIN':TradeContext.RCVBNKCO}
        suba['SUBFLG'] = PL_SUBFLG_AGE     #����
        subd = rccpsDBTrcc_subbra.selectu(suba)
        if subd == None:
            return AfaFlowControl.ExitThisFlow('M999','���ݿ��������')
        if len(subd) <= 0:
            TradeContext.BESBNO = PL_BESBNO_BCLRSB
            TradeContext.BETELR = PL_BETELR_AUTO
            AfaLoggerFunc.tradeInfo( '������[BESBNO]:' + TradeContext.BESBNO )
        else:
            TradeContext.BESBNO = subd['BESBNO']
            TradeContext.BETELR = PL_BETELR_AUTO
            AfaLoggerFunc.tradeInfo( '������[BESBNO]:' + TradeContext.BESBNO )
    else:
        return AfaFlowControl.ExitThisFlow('M999','������������')
    AfaLoggerFunc.tradeInfo('>>>��������')

    return True
#========================================================================
#
#  �������ƣ� ChkNCCDate
#  ��ڲ����� 
#  ���ڲ����� Ture False
#  ��    �ߣ� ������
#  ��    �ڣ� 20080610
#  ��    �ܣ� ͨ����������ȡ��������
#
#========================================================================
def GetNCCDate():
    #=====��ѯũ����ϵͳ״̬====
    AfaLoggerFunc.tradeInfo( '>>>��ѯNCC��������' )
    if((TradeContext.TRCCO[0:2] == PL_TRCCO_HD) or (TradeContext.TRCCO[0:2] == PL_TRCCO_HP)):
        dict = {'OPRTYPNO':PL_TRCCO_HD}
    #elif((TradeContext.TRCCO[0:2] == PL_TRCCO_TCTD) or (TradeContext.TRCCO == PL_TRCCO_QT)):
    else:
        dict = {'OPRTYPNO':PL_TRCCO_TCTD}

    records=rccpsDBTrcc_mbrifa.selectu( dict )
    
    if( records == None ):
        return AfaFlowControl.ExitThisFlow('A0025', "�������ݿ�ʧ��" )
    elif(len(records) <= 0 ):
        return AfaFlowControl.ExitThisFlow('A0025', "ȡũ������������ʧ��" )
    else:
        TradeContext.NCCworkDate = records['NWWKDAT']
        AfaLoggerFunc.tradeInfo( '�������ڣ�' + TradeContext.NCCworkDate )

    return TradeContext.NCCworkDate
