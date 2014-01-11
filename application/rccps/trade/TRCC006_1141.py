# -*- coding: gbk -*-
###############################################################################
#   ũ����ϵͳ������.���������(1.���ز��� 2.���Ļ�ִ).����ת������
#==============================================================================
#   �����ļ�:   TRCC006_1141.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  liyj 
#   �޸�ʱ��:   2008-11-05
###############################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaAfeFunc,AfaFunc,jiami
from types import *
from rccpsConst import *
import rccpsDBFunc,rccpsState
import rccpsDBTrcc_wtrbka
import rccpsDBFunc,rccpsState,rccpsHostFunc,rccpsUtilTools,rccpsDBTrcc_pamtbl
import rccpsMap1141CTradeContext2Dwtrbka_dict,rccpsDBTrcc_atcbka


#=====================����ǰ����(�Ǽ���ˮ,����ǰ����)==========================
def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).����ת�����������Ľ���[TRCC006_1141]����***' )
    #��ʼ��������
    TradeContext.PRCCO = 'RCCI0000'
    TradeContext.STRINFO = "�ɹ�"
    
    #�ж��Ƿ��ظ�����
    AfaLoggerFunc.tradeInfo(">>>��ʼ�ж��Ƿ��ظ�����")
    
    sel_dict = {'COTRCNO':TradeContext.TRCNO,'COTRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_wtrbka.selectu(sel_dict)
    
    if record == None:
        AfaLoggerFunc.tradeDebug('>>>�ж��Ƿ��ظ��ۿ�ȷ�ϱ���,��ѯͨ��ͨ��ҵ��Ǽǲ���ͬ�����쳣')
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "���ݿ���������"
        
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('ͨ��ͨ��ҵ��Ǽǲ��д�����ͬ����,�ظ�����,���ؾܾ�Ӧ����')
        TradeContext.PRCCO    = 'NN1ISO999'
        TradeContext.STRINFO  = "�ظ�����"

    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ��ظ�����")
    
    
    #�Ǽ�ͨ��ͨ�ҵǼǲ�
    AfaLoggerFunc.tradeInfo(">>>��ʼ�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
    
    #=====����ת��====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'
        
    #=====��������ȡ��ʽ=====
    if float(TradeContext.CUSCHRG) > 0.001:
        TradeContext.CHRGTYP = '1'
    else:
        TradeContext.CHRGTYP = '0'    
    
    #====��ʼ���ֵ丳ֵ====
    if TradeContext.PRCCO == 'RCCI0000':
        wtrbka_dict = {}
        if not rccpsMap1141CTradeContext2Dwtrbka_dict.map(wtrbka_dict):
            AfaLoggerFunc.tradeDebug('>>>�ֵ丳ֵ����')
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "���ݿ���������"
    
    wtrbka_dict['DCFLG'] = PL_DCFLG_DEB                  #�����ʶ
    wtrbka_dict['OPRNO'] = PL_TDOPRNO_YZB                 #ҵ������
    
    #=====��ʼ�������ݿ�====
    if TradeContext.PRCCO == 'RCCI0000':
        if not rccpsDBFunc.insTransWtr(wtrbka_dict):
            AfaLoggerFunc.tradeDebug('>>>�Ǽ�ͨ��ͨ��ҵ��Ǽǲ��쳣')
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "���ݿ���������"
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "���ݿ���������"
        
    AfaLoggerFunc.tradeInfo(">>>�����Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
    
    #����ҵ��״̬Ϊ�������׳ɹ�
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ���׳ɹ�")
    
    stat_dict   = {}
    stat_dict['BSPSQN']   = TradeContext.BSPSQN
    stat_dict['BJEDTE']   = TradeContext.BJEDTE
    stat_dict['BCSTAT']   = PL_BCSTAT_BNKRCV
    stat_dict['BDWFLG']   = PL_BDWFLG_SUCC
    
    if TradeContext.PRCCO == 'RCCI0000':
        if not rccpsState.setTransState(stat_dict):
            AfaLoggerFunc.tradeDebug('>>>����ҵ��״̬���׳ɹ��쳣')
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "���ݿ���������"
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "���ݿ���������"
        
    AfaLoggerFunc.tradeInfo(">>>��������ҵ��״̬Ϊ���׳ɹ�")
    
    #����ҵ��״̬Ϊ�Զ��ۿ����
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ�Զ��ۿ����")
    
    if TradeContext.PRCCO == 'RCCI0000':
       if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,PL_BCSTAT_AUTOPAY,PL_BDWFLG_WAIT):
            AfaLoggerFunc.tradeDebug('>>>����ҵ��״̬Ϊ�Զ��ۿ�����쳣')
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "���ݿ���������"
    
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "���ݿ���������"
        
    AfaLoggerFunc.tradeInfo(">>>��ʼ����ҵ��״̬Ϊ�Զ��ۿ����")
    
    TradeContext.BCSTAT = PL_BCSTAT_AUTOPAY #״̬:�Զ��ۿ�
    TradeContext.BCSTATNM = "�Զ��ۿ�"
    #���б�Ҫ�Լ��,��У��ͨ��,�򷵻سɹ�Ӧ����,��У��δͨ��,�򷵻ؾܾ�Ӧ����
    AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҫ�Լ��")

    #�������Ǽǲ����Ƿ��д˱�ҵ��ĳ���ҵ��,�����򷵻ؾܾ�Ӧ����,������ҵ��״̬Ϊ����������
    if TradeContext.PRCCO == 'RCCI0000':
        atcbka_where_dict = {}
        atcbka_where_dict['ORMFN'] = TradeContext.MSGFLGNO

        atcbka_dict = rccpsDBTrcc_atcbka.selectu(atcbka_where_dict)
        
        if atcbka_dict == None:
            AfaLoggerFunc.tradeInfo(">>>��ѯ�����Ǽǲ��쳣")
            TradeContext.PRCCO = 'NN1ID999'
            TradeContext.STRINFO = "��ѯ�����Ǽǲ��쳣"
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            TradeContext.BCSTATNM = "�ܾ�"
        
        else:
            if len(atcbka_dict) <= 0:
                AfaLoggerFunc.tradeInfo(">>>�˽���δ������,����У��")

            else:
                AfaLoggerFunc.tradeInfo(">>>�˽����ѱ�����,���ؾܾ�Ӧ����")
                TradeContext.PRCCO = 'NN1IO307'
                TradeContext.STRINFO = "�˽����ѱ�����"
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "�ܾ�"
                
    #���ܿͻ�����
    if TradeContext.PRCCO == 'RCCI0000':
        MIMA = '      '
        PIN  = TradeContext.CURPIN
        ACC  = TradeContext.PYRACC
        AfaLoggerFunc.tradeDebug('����[' + PIN + ']')
        AfaLoggerFunc.tradeDebug('�˺�[' + ACC + ']')
        ret = jiami.secDecryptPin(PIN,ACC,MIMA)
        if ret != 0:
            AfaLoggerFunc.tradeDebug("ret=[" + str(ret) + "]")
            AfaLoggerFunc.tradeDebug('���ü��ܷ�����ʧ��')
            TradeContext.PRCCO = 'NN1IS999'
            TradeContext.STRINFO = "��������ʧ��"
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            TradeContext.BCSTATNM = "�ܾ�"
        else:
            TradeContext.CURPIN = MIMA
            AfaLoggerFunc.tradeDebug('����new[' + TradeContext.CURPIN + ']')
    
    
    #�Ʊ�����#
    sql = "SELECT ischkactname,ischklate FROM rcc_chlabt where transcode='"+TradeContext.TransCode+"' and channelno= '"+(TradeContext.SNDCLKNO)[6:8]+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql( sql)
    if (records == None):
        return False
    elif (len(records) == 0):
        AfaLoggerFunc.tradeDebug("��ѯ���Ϊ��,��ѯ����[" + sql + "]")
        return False
    AfaLoggerFunc.tradeDebug(str(records))
    
    #У���˻�״̬�Ƿ��������˺Ż����Ƿ����
    if TradeContext.PRCCO == 'RCCI0000':
    
        #���������ӿڲ�ѯ�˻���Ϣ
        TradeContext.HostCode = '8810'
        
        TradeContext.ACCNO = TradeContext.PYRACC
        
        AfaLoggerFunc.tradeDebug("gbj test :" + TradeContext.ACCNO)
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        if TradeContext.errorCode != '0000':
            #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
            AfaLoggerFunc.tradeInfo("��ѯ�˻���Ϣ�쳣,����������[" + TradeContext.errorCode + "],����������Ϣ[" + TradeContext.errorMsg +"]")
            TradeContext.PRCCO = rccpsDBFunc.HostErr2RccErr(TradeContext.errorCode)
            TradeContext.STRINFO = TradeContext.errorMsg
            TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            TradeContext.BCSTATNM = "�ܾ�"
        
        else:
            #��ѯ�ɹ�,����ͨ��ͨ�ҵǼǲ����������
            AfaLoggerFunc.tradeInfo(">>>��ѯ�����˻��ɹ�")
            
            #if( TradeContext.BESBNO != PL_BESBNO_BCLRSB ):
            #    AfaLoggerFunc.tradeInfo(">>>" + TradeContext.BESBNO + ">>>" + TradeContext.ACCSO)
            #    if( TradeContext.BESBNO[:6] != TradeContext.ACCSO[:6] ):
            #        AfaLoggerFunc.tradeInfo(">>>����編�����˽���")
            #        TradeContext.PRCCO = 'NN1IO999'
            #        TradeContext.STRINFO = "���������˻������в�����ͬһ����"
            #        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
            #        TradeContext.BCSTATNM = "�ܾ�"
            
            #��鱾�����Ƿ���ͨ��ͨ��ҵ��Ȩ��
            if not rccpsDBFunc.chkTDBESAuth(TradeContext.ACCSO):
                TradeContext.PRCCO = 'NN1IO999'
                TradeContext.STRINFO = "���˻�����������ͨ��ͨ��ҵ��Ȩ��"
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "�ܾ�"
            
            AfaLoggerFunc.tradeInfo(">>>��ʼ���»�����Ϊ��������")
            TradeContext.BESBNO = TradeContext.ACCSO
            wtrbka_update_dict = {'BESBNO':TradeContext.ACCSO}
            wtrbka_where_dict  = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
            ret = rccpsDBTrcc_wtrbka.updateCmt(wtrbka_update_dict,wtrbka_where_dict)
            
            if ret <= 0:
                AfaLoggerFunc.tradeInfo(">>>���»�����Ϊ���������쳣")
                TradeContext.PRCCO = 'NN1ID006'
                TradeContext.STRINFO = "��������������쳣"
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "�ܾ�"
            
            else:
                AfaLoggerFunc.tradeInfo(">>>���»�����Ϊ���������ɹ�")
                AfaLoggerFunc.tradeDebug("�������ػ���ACCNM :[" + TradeContext.ACCNM + "]")
                AfaLoggerFunc.tradeDebug("���Ľ��ջ���PYRNAM:[" + TradeContext.PYRNAM + "]")
                AfaLoggerFunc.tradeDebug("���������˻�״̬ACCST:[" + TradeContext.ACCST + "]")
                AfaLoggerFunc.tradeDebug("֤������ACITY:[" + TradeContext.ACITY + "]")
                AfaLoggerFunc.tradeDebug("֤������ACINO:[" + TradeContext.ACINO + "]")
                
                
                if TradeContext.ACCNM != TradeContext.PYRNAM:
                    #�Ʊ�����#
                    if(records[0][0]=='1'):
                        AfaLoggerFunc.tradeInfo(">>>�˺Ż�������")
                        TradeContext.PRCCO = 'NN1IA102'
                        TradeContext.STRINFO = '�˺Ż�������'
                        TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "�ܾ�"
                
                elif TradeContext.ACCST != '0' and TradeContext.ACCST != '2':
                    AfaLoggerFunc.tradeInfo(">>>�˻�״̬������")
                    TradeContext.PRCCO = 'NN1IA999'
                    TradeContext.STRINFO = '�˻�״̬������'
                    TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "�ܾ�"
                    
                elif not (TradeContext.ACCCD == '0428' and TradeContext.ACCEM == '21111'):
                    AfaLoggerFunc.tradeInfo(">>>���˻��Ǹ��˽��㻧")
                    TradeContext.PRCCO    = 'NN1IA999'
                    TradeContext.STRINFO  = '���˻��Ǹ��˽��㻧'
                    TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "�ܾ�"
                    
                #=====���׽���ж�====
                chk_dict = {}
                chk_dict['BPARAD'] = 'TD001'    #ͨ��ͨ��ƾ֤���У��
                
                dict = rccpsDBTrcc_pamtbl.selectu(chk_dict) 
                AfaLoggerFunc.tradeInfo('dict='+str(dict))
                
                if dict == None:
                    AfaLoggerFunc.tradeInfo(">>>У�齻�׽��ʧ��")
                    TradeContext.PRCCO    = 'NN1ID003'
                    TradeContext.STRINFO  = 'У�齻�׽��ʧ��'
                    TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "�ܾ�"
                if len(dict) == 0:
                    AfaLoggerFunc.tradeInfo(">>>��ѯPAMTBLУ�齻�׽����¼����")
                    TradeContext.PRCCO    = 'NN1ID010'
                    TradeContext.STRINFO  = '��ѯPAMTBLУ�齻�׽����¼����'
                    TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                    TradeContext.BCSTATNM = "�ܾ�"
                
                #=====�ж�ũ�������Ĺ涨У��ƾ֤����====
                if float(TradeContext.OCCAMT) > float(dict['BPADAT']):
                    #=====���׽�����ũ�������Ĺ涨����Ҫ����֤��====
                    if TradeContext.existVariable('CERTTYPE') and len(TradeContext.CERTTYPE) == 0:
                        AfaLoggerFunc.tradeInfo(">>>��ѡ��֤������")
                        TradeContext.PRCCO    = 'NN1IA999'
                        TradeContext.STRINFO  = '��ѡ��֤������'
                        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "�ܾ�"
                    elif(TradeContext.CERTTYPE == '06'):
                        if( TradeContext.ACITY != '06' and TradeContext.ACITY != '07' and TradeContext.ACITY != '08' and TradeContext.ACITY != '09'):
                            AfaLoggerFunc.tradeInfo(">>>֤�����ʹ���")
                            TradeContext.PRCCO    = 'NN1IA999'
                            TradeContext.STRINFO  = '֤�����ʹ���'
                            TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                            TradeContext.BCSTATNM = "�ܾ�"
                    elif( TradeContext.CERTTYPE != TradeContext.ACITY ):
                        AfaLoggerFunc.tradeInfo(">>>֤�����ʹ���")
                        TradeContext.PRCCO    = 'NN1IA999'
                        TradeContext.STRINFO  = '֤�����ʹ���'
                        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "�ܾ�"
                        
                    if TradeContext.existVariable('CERTNO')   and len(TradeContext.CERTNO)   == 0:
                        AfaLoggerFunc.tradeInfo(">>>������֤������")
                        TradeContext.PRCCO    = 'NN1IA999'
                        TradeContext.STRINFO  = '������֤������'
                        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "�ܾ�"
                    elif( TradeContext.CERTNO != TradeContext.ACINO ):
                        AfaLoggerFunc.tradeInfo(">>>֤���������")
                        TradeContext.PRCCO    = 'NN1IA999'
                        TradeContext.STRINFO  = '֤���������'
                        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
                        TradeContext.BCSTATNM = "�ܾ�"
    
    
    #У�齻�׽���Ƿ񳬵����޶�
    if not rccpsDBFunc.chkLimited(TradeContext.BJEDTE,TradeContext.PYRACC,TradeContext.OCCAMT):
        AfaLoggerFunc.tradeInfo(">>>���׽���")
        TradeContext.PRCCO    = 'NN1IA999'
        TradeContext.STRINFO  = '���׽���'
        TradeContext.BCSTAT   = PL_BCSTAT_MFERFE
        TradeContext.BCSTATNM = "�ܾ�"
    
    #У��ŵ���Ϣ
    if TradeContext.PRCCO == 'RCCI0000':
        #�Ʊ�����#
        if(records[0][1]=='1'):
            if (TradeContext.SCTRKINF == ''.rjust(37,'0') or TradeContext.SCTRKINF == ''):
                AfaLoggerFunc.tradeInfo("У��ŵ���Ϣ�쳣,��ҵ���������ŵ���Ϣ")
                TradeContext.PRCCO = 'NN1IA141'
                TradeContext.STRINFO = "У��ŵ���Ϣʧ�� :�޴ŵ���Ϣ" 
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "�ܾ�"
        if TradeContext.SCTRKINF != ''.rjust(37,'0') and TradeContext.SCTRKINF != '':
            #�ŵ���Ϣ�ǿջ�37����,����������ӿ�У��ŵ���Ϣ
            TradeContext.HostCode = '0652'
            
            TradeContext.WARNTNO = TradeContext.PYRACC[6:18]
            
            AfaLoggerFunc.tradeDebug("WARNTNO :" + TradeContext.WARNTNO)
            AfaLoggerFunc.tradeDebug("SCTRKINF :" + TradeContext.SCTRKINF)
            AfaLoggerFunc.tradeDebug("THTRKINF :" + TradeContext.THTRKINF)
            if TradeContext.THTRKINF == ''.rjust(37,'0'):
                TradeContext.THTRKINF = ''
                AfaLoggerFunc.tradeDebug("THTRKINF :" + TradeContext.THTRKINF)
            
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            
            if TradeContext.errorCode != '0000':
                #return AfaFlowControl.ExitThisFlow(TradeContext.errorCode,TradeContext.errorMsg)
                AfaLoggerFunc.tradeInfo("У��ŵ���Ϣ�쳣,����������[" + TradeContext.errorCode + "],����������Ϣ[" + TradeContext.errorMsg +"]")
                TradeContext.PRCCO = 'NN1IA141'
                TradeContext.STRINFO = "У��ŵ���Ϣʧ�� " + TradeContext.errorMsg
                TradeContext.BCSTAT = PL_BCSTAT_MFERFE
                TradeContext.BCSTATNM = "�ܾ�"
                
    AfaLoggerFunc.tradeInfo(">>>������Ҫ�Լ��")
    
    #������������
    AfaLoggerFunc.tradeInfo(">>>��ʼ������������")
    
    TradeContext.sCertType = TradeContext.CERTTYPE
    TradeContext.sCertNo   = TradeContext.CERTNO
    TradeContext.sOccamt  = TradeContext.OCCAMT
    TradeContext.sCuschrg = TradeContext.CUSCHRG
    
    if TradeContext.PRCCO == 'RCCI0000':
        TradeContext.HostCode = '8813'                               #����8813�����ӿ�
        #���˶Է��ֽ���ȡ������
        if( TradeContext.CHRGTYP != '1' ):
        
            TradeContext.RCCSMCD  = PL_RCCSMCD_YZBWZ                      #����ժҪ����
            TradeContext.SBAC = TradeContext.PYRACC                       #�跽�˻�:�������˻�
            TradeContext.ACNM = TradeContext.PYRNAM                       #�跽���� �����˻���
            TradeContext.RBAC = TradeContext.BESBNO + PL_ACC_NXYDQSLZ     #�����˻�:ũ��������������
            TradeContext.RBAC = rccpsHostFunc.CrtAcc(TradeContext.RBAC, 25)
            TradeContext.OTNM = 'ũ��������������'                        #��������:
            TradeContext.CTFG =  '7'                                      #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
            TradeContext.PKFG =  'T'                                      #ͨ��ͨ�ұ�ʶ                                   
            TradeContext.WARNTNO = TradeContext.SBAC[6:18]
            TradeContext.CERTTYPE = ''
            TradeContext.CERTNO = ''
            TradeContext.PASSWD = TradeContext.CURPIN                     #����
            AfaLoggerFunc.tradeInfo( '�跽�˺�:' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '�����˺�:' + TradeContext.RBAC )
            AfaLoggerFunc.tradeInfo( 'ƾ֤����:' + TradeContext.WARNTNO )
        else:
            #�Է�ת����ȡ������ʱs
            TradeContext.ACUR    =  '3'                                           #���˴���
        
            #=========���׽��============
            TradeContext.RCCSMCD  =  PL_RCCSMCD_YZBWZ                               #ժҪ����
            TradeContext.SBAC  =  TradeContext.PYRACC                           #�跽�˺�
            TradeContext.ACNM  =  TradeContext.PYRNAM                           #�跽����
            TradeContext.RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
            TradeContext.RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.RBAC,25)
            TradeContext.OTNM  =  '������ʱ����'                                #��������
            TradeContext.OCCAMT  =  str(TradeContext.sOccamt)                       #������
            TradeContext.CTFG  = '7'                                            #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
            TradeContext.PKFG  = 'T'                                            #ͨ��ͨ�ұ�ʶ                                   
            TradeContext.WARNTNO = TradeContext.SBAC[6:18]
            TradeContext.PASSWD = TradeContext.CURPIN                     #����
            TradeContext.sCertType = TradeContext.CERTTYPE
            TradeContext.sCertNo   = TradeContext.CERTNO
            TradeContext.CERTTYPE = ''
            TradeContext.CERTNO = ''
            AfaLoggerFunc.tradeInfo( '>>>���׽��:�跽�˺�' + TradeContext.SBAC )
            AfaLoggerFunc.tradeInfo( '>>>���׽��:�����˺�' + TradeContext.RBAC )
            AfaLoggerFunc.tradeInfo( '>>>���׽��:ƾ֤����:' + TradeContext.WARNTNO )
            #=========�������������뻧===========
            TradeContext.I2SMCD  =  PL_RCCSMCD_SXF                                #ժҪ����
            TradeContext.I2SBAC  =  TradeContext.PYRACC                           #�跽�˺�
            TradeContext.I2ACNM  =  TradeContext.PYRNAM                           #�跽����
            TradeContext.I2RBAC  =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�����˺�
            TradeContext.I2RBAC  =  rccpsHostFunc.CrtAcc(TradeContext.I2RBAC,25)
            TradeContext.I2OTNM  =  '������ʱ����'                                #��������
            TradeContext.I2TRAM  =  str(TradeContext.sCuschrg)                      #������
            TradeContext.I2CTFG  = '8'                                            #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
            TradeContext.I2PKFG  = 'T'                                            #ͨ��ͨ�ұ�ʶ                                   
            TradeContext.I2WARNTNO = TradeContext.I2SBAC[6:18]
            TradeContext.I2PASSWD = TradeContext.CURPIN                     #����
            AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�跽�˺�' + TradeContext.I2SBAC )
            AfaLoggerFunc.tradeInfo( '>>>�������������뻧:�����˺�' + TradeContext.I2RBAC )
            AfaLoggerFunc.tradeInfo( '>>>�������������뻧:ƾ֤����:' + TradeContext.WARNTNO )
            #=========���׽��+������===================
            TradeContext.I3SMCD    =  PL_RCCSMCD_YZBWZ                               #ժҪ����
            TradeContext.I3SBAC    =  TradeContext.BESBNO + PL_ACC_NXYDJLS          #�跽�˺�
            TradeContext.I3SBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3SBAC,25)
            TradeContext.I3ACNM    =  '������ʱ����'                                #�跽����
            TradeContext.I3RBAC    =  TradeContext.BESBNO + PL_ACC_NXYDQSLZ         #�����˺�
            TradeContext.I3RBAC    =  rccpsHostFunc.CrtAcc(TradeContext.I3RBAC,25)
            TradeContext.I3OTNM    =  'ũ��������'                                  #��������
            TradeContext.I3TRAM    =  rccpsUtilTools.AddDot(TradeContext.OCCAMT,TradeContext.CUSCHRG) #������
            TradeContext.I3CTFG    = '9'                                            #���� �����ѱ�ʶ  7 ���� 8������ 9 ���������� 
            TradeContext.I3PKFG    = 'T'                                            #ͨ��ͨ�ұ�ʶ                                   
            AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�跽�˺�' + TradeContext.I3SBAC )
            AfaLoggerFunc.tradeInfo( '>>>���׽��+������:�����˺�' + TradeContext.I3RBAC )
        
        rccpsHostFunc.CommHost( TradeContext.HostCode )
        
        AfaLoggerFunc.tradeInfo(">>>����������������")
        
        #TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
        
        #��������������,����ҵ��״̬Ϊ�Զ����˳ɹ���ʧ��
        AfaLoggerFunc.tradeInfo(">>>��ʼ���������Ż���,����ҵ��״̬Ϊ�Զ����˳ɹ���ʧ��")
        
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['SBAC']    = TradeContext.SBAC
        stat_dict['ACNM']    = TradeContext.ACNM
        stat_dict['RBAC']    = TradeContext.RBAC
        stat_dict['OTNM']    = TradeContext.OTNM
        #=====modify by pgt 1129====
        stat_dict['MGID']   = TradeContext.errorCode
        if TradeContext.existVariable('TRDT'):
    	    stat_dict['TRDT'] = TradeContext.TRDT
    	if TradeContext.existVariable('TLSQ'):
    		stat_dict['TLSQ'] = TradeContext.TLSQ
        stat_dict['STRINFO'] = TradeContext.errorMsg
        
        AfaLoggerFunc.tradeInfo("����������[" + TradeContext.errorCode + "],����������Ϣ[" + TradeContext.errorMsg +"]")
        if TradeContext.errorCode == '0000':
            #=====����ũ�����ɹ�,����״̬Ϊ�Զ����˳ɹ�====
            stat_dict['BCSTAT']  = PL_BCSTAT_AUTOPAY
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            TradeContext.PRCCO = 'RCCI0000'
            TradeContext.STRINFO = '�ɹ�'
            
            if not rccpsState.setTransState(stat_dict):
                return AfaFlowControl.ExitThisFlow('S999', "����ҵ��״̬Ϊ�Զ����˳ɹ��쳣")
            
            AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ�Զ����˳ɹ����")
        else:
            #=====����ũ����ʧ��,����״̬Ϊ�ܾ��ɹ�====       
            stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
            stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
            TradeContext.PRCCO = rccpsDBFunc.HostErr2RccErr(TradeContext.errorCode)
            TradeContext.STRINFO = TradeContext.errorMsg
            
            if not rccpsState.setTransState(stat_dict):
                AfaLoggerFunc.tradeFatal( '����ҵ��״̬Ϊ�ܾ��ɹ��쳣' )
                TradeContext.PRCCO    = "NN1ID999"
                TradeContext.STRINFO  = "���ݿ���������"
            
            AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ�Զ�����ʧ�����")
    
    else:
        stat_dict = {}
        stat_dict['BJEDTE']  = TradeContext.BJEDTE
        stat_dict['BSPSQN']  = TradeContext.BSPSQN
        stat_dict['BESBNO']  = TradeContext.BESBNO
        stat_dict['BETELR']  = TradeContext.BETELR
        stat_dict['PRCCO']   = TradeContext.PRCCO
        stat_dict['STRINFO'] = TradeContext.STRINFO
        stat_dict['BCSTAT']  = PL_BCSTAT_MFERFE
        stat_dict['BDWFLG']  = PL_BDWFLG_SUCC
        
        if not rccpsState.setTransState(stat_dict):
            AfaLoggerFunc.tradeFatal( '����ҵ��״̬Ϊ�ܾ��ɹ��쳣' )
            TradeContext.PRCCO    = "NN1ID999"
            TradeContext.STRINFO  = "���ݿ���������"
            
        AfaLoggerFunc.tradeInfo(">>>����ҵ��״̬Ϊ�ܾ��ɹ����")
        
    if not AfaDBFunc.CommitSql( ):
        AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
        TradeContext.PRCCO    = "NN1ID999"
        TradeContext.STRINFO  = "���ݿ���������"
    
    AfaLoggerFunc.tradeInfo(">>>��ʼ���������Ż���,����ҵ��״̬Ϊ�Զ����˳ɹ���ʧ��")
        
    #Ϊ���ȷ��Ӧ���ĸ�ֵ
    TradeContext.sysType  = 'rccpst'
    TradeContext.MSGTYPCO = 'SET007'                                          #���������
    #TradeContext.RCVMBRCO = TradeContext.SNDMBRCO                             #���շ���Ա�к�
    TradeContext.RCVSTLBIN = TradeContext.SNDMBRCO                            #�տ��Ա�к�
    TradeContext.SNDSTLBIN = TradeContext.RCVMBRCO                            #�����Ա�к�
    TradeContext.SNDBRHCO = TradeContext.BESBNO                               #�����������
    TradeContext.SNDCLKNO = TradeContext.BETELR                               #�����й�Ա��
    TradeContext.SNDTRDAT = TradeContext.BJEDTE                               #�����н�������
    TradeContext.SNDTRTIM = TradeContext.BJETIM                               #�����н���ʱ��
    TradeContext.ORMFN    = TradeContext.MSGFLGNO                             #�ο����ı�ʶ��
    TradeContext.MSGFLGNO = TradeContext.SNDMBRCO + TradeContext.BJEDTE + TradeContext.SerialNo       #���ı�ʶ��
    TradeContext.NCCWKDAT = TradeContext.NCCworkDate                          #���Ĺ�������
    TradeContext.OPRTYPNO = '30'                                              #ҵ������
    TradeContext.ROPRTPNO = TradeContext.OPRTYPNO                             #�ο�ҵ������
    TradeContext.TRANTYP  = '0'                                               #��������
    TradeContext.CERTTYPE = TradeContext.sCertType
    TradeContext.CERTNO   = TradeContext.sCertNo
    TradeContext.OCCAMT   = TradeContext.sOccamt
    TradeContext.CUSCHRG  = TradeContext.sCuschrg 
    TradeContext.CUR      = 'CNY'                                             #���ҷ���
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).����ת�����������Ľ���[TRCC006_1141]�˳�***' )
    return True


#=====================���׺���===============================================
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).����ת�����������Ľ���[TRCC006_1141]����***' )
    
    #����afe�������ж�Ӧ�����Ƿ��ͳɹ�,��������Ӧҵ��״̬
    AfaLoggerFunc.tradeInfo("TradeContext.errorCode = [" + TradeContext.errorCode + "]")
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ���ĳɹ�')
    else:
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ����ʧ��')
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.���Ļ�ִ).����ת�����������Ľ���[TRCC006_1141]�˳�***' )
    return True
    
