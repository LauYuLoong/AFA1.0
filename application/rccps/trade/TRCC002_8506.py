# -*- coding: gbk -*-
###################################################################
#    ũ����ϵͳ.���˷��ͽ���
#==================================================================
#    �����ļ���  TRCC002_8506.py
#    �޸�ʱ�䣺  2008-6-5
#    ��    �ߣ�  ������
#==================================================================
#    �޸�ʱ�䣺
#    �޸���  ��
#==================================================================
#    ��    �ܣ�  ������˽����ύ�󣬽��б�Ҫ�Լ�顢��¼�����ݿ���
#		 ��������������ˣ����˺�����mfe
###################################################################
import TradeContext,AfaLoggerFunc, rccpsDBFunc, AfaFlowControl ,AfaDBFunc
import TransBillFunc, AfaFunc, rccpsHostFunc,rccpsMap8506CTradeContext2Ddict
import rccpsDBTrcc_sstlog,rccpsState,rccpsDBTrcc_trcbka,rccpsDBTrcc_spbsta,rccpsEntries
import miya,os,time
from rccpsConst import *
from types import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).���˷���[TRCC002_8506]����***' )
    
    #====begin ������ 20110215 ����====
    #��Ʊ�ݺ���16λ����Ҫȡ��8λ���汾��Ϊ02��ͬʱҪ������Ʊ�ݺ�8λ���汾��Ϊ01
    if len(TradeContext.BILNO) == 16:
        TradeContext.TMP_BILNO = TradeContext.BILNO[-8:]
    else:
        TradeContext.TMP_BILNO = TradeContext.BILNO
    #============end============
    
    AfaLoggerFunc.tradeInfo('>>>RCVSTLBIN: '+TradeContext.RCVSTLBIN)
    AfaLoggerFunc.tradeInfo('>>>SNDSTLBIN: '+TradeContext.SNDSTLBIN)
    #=====�ж��Ƿ�Ϊͬһ��Ա����====
    if TradeContext.RCVSTLBIN == TradeContext.SNDSTLBIN:
        return AfaFlowControl.ExitThisFlow('M999','ͬһ��Ա���ڽ�ֹ����ҵ��')
     
    ##===== �ź�  ��������,������֧����У���ظ�����. �������ѱ�־������ֶθ�ֵ 20091109 ========##
    if (TradeContext.existVariable( "CHSHTP" ) and len(TradeContext.CHSHTP) != 0):          #��������ȡ��ʽ
        TradeContext.CHRGTYP      =      TradeContext.CHSHTP 
    else:
        TradeContext.CHRGTYP      =      '2'                                                #Ĭ��Ϊ����
    if (TradeContext.existVariable( "CUSCHRG" ) and len(TradeContext.CUSCHRG) != 0):        #�����ѽ��
        TradeContext.LOCCUSCHRG   =      TradeContext.CUSCHRG  
    else :
        TradeContext.LOCCUSCHRG   =      '0.00'                                             #Ĭ��Ϊ0.00
    TradeContext.CUSCHRG          =      '0.00'                                             #�����������0
    
    if str(TradeContext.OPRATTNO) != '12':                                                  #����֧��
    ##=====END=====================================================================================##
    
        #=====������ݿ��Ƿ�����ͬ����====
        sql = "BJEDTE = '" + TradeContext.BJEDTE + "'"                                      #����
        sql = sql + " and BESBNO ='" + TradeContext.BESBNO + "'"                            #������
        if (TradeContext.existVariable( "PYRACC" ) and len(TradeContext.PYRACC) != 0):      #�������˺�
            sql = sql + " and PYRACC ='" + TradeContext.PYRACC + "'"
        if (TradeContext.existVariable( "RCVBNKCO" ) and len(TradeContext.RCVBNKCO) != 0):  #�տ����к�
            sql = sql + " and RCVBNKCO = '" + TradeContext.RCVBNKCO + "'"
        if (TradeContext.existVariable( "PYEACC" ) and len(TradeContext.PYEACC) != 0):      #�տ����˺�
            sql = sql + " and PYEACC ='" + TradeContext.PYEACC + "'"
        if (TradeContext.existVariable( "OCCAMT" ) and len(TradeContext.OCCAMT) != 0):      #���
            sql = sql + " and OCCAMT ="  + TradeContext.OCCAMT + ""
        if (TradeContext.existVariable( "OPRNO" ) and len(TradeContext.OPRNO) != 0):        #ҵ������
            sql = sql + " and OPRNO  ='" + TradeContext.OPRNO  + "'"
        if (TradeContext.existVariable( "OPRATTNO" ) and len(TradeContext.OPRATTNO) != 0):  #ҵ������
            sql = sql + " and OPRATTNO ='" + TradeContext.OPRATTNO + "'"
        if (TradeContext.existVariable( "BBSSRC" ) and len(TradeContext.BBSSRC) != 0):      #�ʽ���Դ
            sql = sql + " and BBSSRC ='" + TradeContext.BBSSRC + "'"
        if (TradeContext.existVariable( "DASQ" ) and len(TradeContext.DASQ) != 0):          #�������
            sql = sql + " and DASQ   ='" + TradeContext.DASQ + "'"
        if (TradeContext.existVariable( "BILTYP" ) and len(TradeContext.BILTYP) != 0):      #Ʊ������
            sql = sql + " and BILTYP = '" + TradeContext.BILTYP  + "'"
        if (TradeContext.existVariable( "BILDAT" ) and len(TradeContext.BILDAT) != 0):      #Ʊ������
            sql = sql + " and BILDAT = '" + TradeContext.BILDAT  + "'"
        if (TradeContext.existVariable( "BILNO" ) and len(TradeContext.BILNO) != 0):        #Ʊ�ݺ���
            sql = sql + " and BILNO  = '" + TradeContext.BILNO   + "'"
        if (TradeContext.existVariable( "NOTE1" ) and len(TradeContext.NOTE1) != 0):        #��ע1
            sql = sql + " and NOTE1  = '" + TradeContext.NOTE1   + "'"

        #=====���ú������ж�ʲ�ѯ====
        AfaLoggerFunc.tradeInfo( '>>>�жϱ�Ҫ���ֶ��Ƿ��ظ����ظ����ش���')
        record = rccpsDBTrcc_trcbka.selectm(1,10,sql,"")
        if record == None:
            return AfaFlowControl.ExitThisFlow('D000','���ݿ����ʧ��')
        if len(record) > 0:
            #====�жϱ�Ҫ���ֶ��Ƿ��ظ����ظ����ش���====
            for next in range(0, len(record)):
                spbsta = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':record[next]['BSPSQN']}
                rep = rccpsDBTrcc_spbsta.selectu(spbsta)
                if rep == None:
                    return AfaFlowControl.ExitThisFlow('D000', '���ݿ��������')
                elif len(rep) <= 0:
                    return AfaFlowControl.ExitThisFlow('D001', '���ݿ��ѯ��ͬҵ�����')
                else:
                    if rep['BDWFLG'] != PL_BDWFLG_FAIL:
                        return AfaFlowControl.ExitThisFlow('S000', '��ͬҵ����¼�룬�������ظ��ύ')
    AfaLoggerFunc.tradeInfo( '>>>��ʼ����˱�ҵ��' )
    #=====�ʽ���ԴΪ1-���˽��㻧ʱ����Ҫ����8811У��֧������====
    if TradeContext.BBSSRC == '1':
        TradeContext.HostCode = '8811'
        TradeContext.ACCNO    = TradeContext.PYRACC     #�������˻�

        rccpsHostFunc.CommHost( '8811' )
       
        if TradeContext.errorCode != '0000':
            return AfaFlowControl.ExitThisFlow('S999','��ѯƾ֤��Ϣ����')
        else:
            if TradeContext.PAYTYP != TradeContext.HPAYTYP:
                return AfaFlowControl.ExitThisFlow('S999','֧����������')

    #=====��ʼ������Ѻ������====
    SEAL = '          '
    SNDBANKCO  = TradeContext.SNDBNKCO
    RCVBANKCO  = TradeContext.RCVBNKCO
    SNDBANKCO = SNDBANKCO.rjust(12,'0')
    RCVBANKCO = RCVBANKCO.rjust(12,'0')
    AMOUNT = TradeContext.OCCAMT.split('.')[0] + TradeContext.OCCAMT.split('.')[1]
    AMOUNT = AMOUNT.rjust(15,'0')
    
    AfaLoggerFunc.tradeDebug('AMOUNT=' + str(AMOUNT) )
    AfaLoggerFunc.tradeDebug('SNDBANKCO=' + str(SNDBANKCO) )
    AfaLoggerFunc.tradeDebug('RCVBANKCO=' + str(RCVBANKCO) )
    AfaLoggerFunc.tradeDebug('���ͣ�' + str(PL_SEAL_ENC) )
    AfaLoggerFunc.tradeDebug('ҵ�����ͣ�' + str(PL_TYPE_DZHD) )
    AfaLoggerFunc.tradeDebug('����' + TradeContext.TRCDAT )
    AfaLoggerFunc.tradeDebug('��ˮ' + TradeContext.SerialNo )
    AfaLoggerFunc.tradeDebug('��Ѻo[' + SEAL + ']')
    
    ret = miya.DraftEncrypt(PL_SEAL_ENC,PL_TYPE_DZHD,TradeContext.TRCDAT,TradeContext.SerialNo,AMOUNT,SNDBANKCO,RCVBANKCO,'',SEAL)
    AfaLoggerFunc.tradeDebug("ret[" + str(ret) + "]")
    AfaLoggerFunc.tradeDebug('��Ѻ[' + SEAL + ']')
    if ret != 0:
        return AfaFlowControl.ExitThisFlow('M9999','������Ѻ������ʧ��')
    else:
        TradeContext.SEAL = SEAL
        AfaLoggerFunc.tradeDebug('��Ѻnew[' + TradeContext.SEAL + ']')   

    #=====��ʼ���ֵ丳ֵ====
    TradeContext.DCFLG = PL_DCFLG_CRE
    dict = {}
    if not rccpsMap8506CTradeContext2Ddict.map(dict):
        return AfaFlowControl.ExitThisFlow('M999', '�ֵ丳ֵ����')

    #=====��ʼ�������ݿ�====
    if not rccpsDBFunc.insTransTrc(dict):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D002', '�������ݿ����,RollBack�ɹ�')

    #=====commit����====
    if not AfaDBFunc.CommitSql():
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D011', '���ݿ�Commitʧ��')
    else:
        AfaLoggerFunc.tradeDebug('COMMIT�ɹ�')

    #====���������ֶ������տ��������ֶ�  ===
    if (TradeContext.existVariable( "PYRNAM" ) and len(TradeContext.PYRNAM) != 0):       #����������
         TradeContext.ACNM     = TradeContext.PYRNAM
    else:
         TradeContext.ACNM     = ''
    if (TradeContext.existVariable( "PYENAM" ) and len(TradeContext.PYENAM) != 0):       #�տ�������
        TradeContext.OTNM      = TradeContext.PYENAM
    else:
        TradeContext.OTNM      = ''
        
    #������ʼ����ֵ丳ֵ
    input_dict = {}
    input_dict['CHRGTYP']     = TradeContext.CHRGTYP                        #��������ȡ��ʽ
    input_dict['LOCCUSCHRG']  = TradeContext.LOCCUSCHRG                     #�����ѽ��
    input_dict['PYRACC']      = TradeContext.PYRACC                         #�������˺�
    input_dict['BBSSRC']      = TradeContext.BBSSRC                         #�ʽ���Դ
    input_dict['OCCAMT']      = TradeContext.OCCAMT                         #���׽��
    input_dict['ACNM']        = TradeContext.ACNM                           #����������
    input_dict['OTNM']        = TradeContext.OTNM                           #�տ�������
    input_dict['BESBNO']      = TradeContext.BESBNO
    #���û�Ҽ��˽ӿ�
    rccpsEntries.HDWZJZ(input_dict)

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(1.���ز���).���˷���[TRCC002_8506]�˳�***' )
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.��������).���˷���[TRCC002_8506]����***' )
    AfaLoggerFunc.tradeInfo( '>>>��ʼ�����������ؽ����Ϣ' )
    
    #=====������������Ϣȡ������˺ź�����������Ϣ====
    sstlog = {}
    sstlog["BJEDTE"] = TradeContext.BJEDTE      #��������
    sstlog["BSPSQN"] = TradeContext.BSPSQN      #�������
    sstlog["SBAC"] = TradeContext.SBAC          #�跽�˺�
    sstlog["ACNM"] = TradeContext.PYRNAM        #�跽����
    sstlog["RBAC"] = TradeContext.RBAC          #�����˺�
    sstlog["OTNM"] = '0651��Ŀ'                 #��������

    #=====�ж��������ؽ��====
    if TradeContext.errorCode != '0000':
        sstlog['BCSTAT'] = PL_BCSTAT_ACC
        sstlog['BDWFLG'] = PL_BDWFLG_FAIL
        sstlog["MGID"] = TradeContext.errorCode     #����������
        sstlog["STRINFO"] = TradeContext.errorMsg   #����������Ϣ
    elif TradeContext.errorCode == '0000':
        sstlog['BCSTAT'] = PL_BCSTAT_ACC
        sstlog['BDWFLG'] = PL_BDWFLG_SUCC
        sstlog["TRDT"] = TradeContext.TRDT    #��������
        sstlog["TLSQ"] = TradeContext.TLSQ    #������ˮ��
        sstlog["MGID"] = TradeContext.MGID    #����������Ϣ
        sstlog["DASQ"] = TradeContext.DASQ    #�������
    #������
    AfaLoggerFunc.tradeInfo( 'TradeContext.__status__ ='+TradeContext.__status__)
    
    if TradeContext.__status__=='2':            #�쳣���
        #====��Ҫ��������Ĩ�˽���===
        #�������Ĩ���ֵ丳ֵ
        input_dict = {}
        input_dict['BJEDTE']     = TradeContext.BJEDTE
        input_dict['BSPSQN']     = TradeContext.BSPSQN
        input_dict['PYRACC']     = TradeContext.PYRACC                         #�������˺�
        input_dict['OCCAMT']     = str(TradeContext.OCCAMT)
        input_dict['BBSSRC']     = TradeContext.BBSSRC
        input_dict['BESBNO']     = TradeContext.BESBNO

        #���û������Ĩ��
        rccpsEntries.HDWZMZ(input_dict) 

        #=====����������������Ĩ��
        rccpsHostFunc.CommHost( TradeContext.HostCode )
 
        #=====�ж���������ֵ====
        if TradeContext.errorCode == '0000':
            sstlog['BCSTAT'] = PL_BCSTAT_ACC
            sstlog['BDWFLG'] = PL_BDWFLG_FAIL
            TradeContext.errorCode = 'D011'         #��ֵ���ش���
            TradeContext.errorMsg  = '����ʧ�ܣ�ϵͳ�Զ������ɹ�'
        else:
            sstlog['BCSTAT'] = PL_BCSTAT_ACC
            sstlog['BDWFLG'] = PL_BDWFLG_WAIT
            TradeContext.errorCode = 'D011'         #��ֵ���ش���
            TradeContext.errorMsg  = '����ʧ�ܣ�ϵͳ�Զ�����ʧ��'

    #=====�޸�sstlog��������====
    AfaLoggerFunc.tradeInfo( '�ֵ䣺' + str(sstlog) )

    if not rccpsState.setTransState(sstlog):
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit�ɹ�')

    #=====�ж��������أ����ɹ����ش���ǰ̨====
    if TradeContext.errorCode != '0000':
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)

    #=====��ֵũ����������Ҫ�ֶ�====
    TradeContext.TRANTYP   = '0'   #��������
    TradeContext.OPRTYPNO  = '20'  #ҵ������
    #TradeContext.BJEDTE    = TradeContext.NCCworkDate
    #TradeContext.TRCDAT    = TradeContext.NCCworkDate

    #=====����sstlog����״̬Ϊ��Ĩ��-������====
    TradeContext.BCSTAT  = PL_BCSTAT_SND
    TradeContext.BDWFLG  = PL_BDWFLG_WAIT

    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
        #=====RollBack����====
        if not AfaDBFunc.RollbackSql():
            return AfaFlowControl.ExitThisFlow('M999', '����ũ��������ʧ��,����״̬ʧ��,ϵͳ�Զ��ع�')
    else:
        #=====commit����====
        if not AfaDBFunc.CommitSql():
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('M999', '����ũ��������ʧ��,����״̬ʧ��,ϵͳ�Զ��ع�')

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(2.��������).���˷���[TRCC002_8506]�˳�***' )
    return True
def SubModuleDoTrd():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(3.���ļ���).���˷���[TRCC002_8506]����***' )
    AfaLoggerFunc.tradeInfo( '>>>�жϷ���ũ�������ķ��ؽ��' )

    #=====���ü��˺����ӿ�====
    sstlog_dict = {}
    sstlog_dict["BJEDTE"] = TradeContext.BJEDTE   #��������
    sstlog_dict["BSPSQN"] = TradeContext.BSPSQN     #�������

    #=====�жϵ���������ֵ,���سɹ�ʱ====
    if TradeContext.errorCode == '0000':
        sstlog_dict['BCSTAT'] = PL_BCSTAT_SND
        sstlog_dict['BDWFLG'] = PL_BDWFLG_SUCC

        #=====����״̬Ϊ���ͳɹ�====
        if not rccpsState.setTransState(sstlog_dict):
            #=====RollBack����====
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
        else:
            #=====commit����====
            AfaDBFunc.CommitSql()
            TradeContext.errorCode = '0000'
            TradeContext.errorMsg  = '����ũ�������ĳɹ�'
    #=====�жϵ���������ֵ,����ʧ��ʱ====
    else:
        sstlog_dict['BCSTAT'] = PL_BCSTAT_SND
        sstlog_dict['BDWFLG'] = PL_BDWFLG_FAIL
        #=====����״̬Ϊ����ʧ��====
        if not rccpsState.setTransState(sstlog_dict):
            #=====RollBack����====
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
        else:
            #=====commit����====
            AfaDBFunc.CommitSql()
            AfaLoggerFunc.tradeDebug( '>>>commit send succ' )

        #=====����������������Ĩ��====
        AfaLoggerFunc.tradeInfo('>>>��ʼĨ�˴���')

        #=====����sstlog����״̬Ϊ��Ĩ��-������====
        TradeContext.BOSPSQ  = TradeContext.BSPSQN
        TradeContext.BOJEDT  = TradeContext.BJEDTE
        TradeContext.BCSTAT  = PL_BCSTAT_HCAC
        TradeContext.BDWFLG  = PL_BDWFLG_WAIT

        if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
            #=====RollBack����====
            if not AfaDBFunc.RollbackSql():
                return AfaFlowControl.ExitThisFlow('M999', '����ũ��������ʧ��,����״̬ʧ��,ϵͳ�Զ��ع�')
        else:
            #=====commit����====
            if not AfaDBFunc.CommitSql():
                AfaDBFunc.RollbackSql()
                return AfaFlowControl.ExitThisFlow('M999', '����ũ��������ʧ��,����״̬ʧ��,ϵͳ�Զ��ع�')

        #=====�ֵ丳ֵ==== 
        sstlog_new = {}
        sstlog_new["BJEDTE"] = TradeContext.BJEDTE                                   #��������
        sstlog_new["BSPSQN"] = TradeContext.BSPSQN                                   #�������
        
        #�������Ĩ���ֵ丳ֵ
        input_dict = {}
        input_dict['BJEDTE']     = TradeContext.BJEDTE
        input_dict['BSPSQN']     = TradeContext.BSPSQN
        input_dict['PYRACC']     = TradeContext.PYRACC                         #�������˺�
        input_dict['OCCAMT']     = str(TradeContext.OCCAMT)
        input_dict['BBSSRC']     = TradeContext.BBSSRC
        input_dict['BESBNO']     = TradeContext.BESBNO

        #���û������Ĩ��
        rccpsEntries.HDWZMZ(input_dict) 

        #=====���ü��˺����ӿ�====
        rccpsHostFunc.CommHost( TradeContext.HostCode )
            
        if TradeContext.errorCode == '0000':
            sstlog_new['DASQ']   = TradeContext.DASQ
            sstlog_new['PRTCNT'] = 1                     #��ӡ����
            sstlog_new['BCSTAT'] = PL_BCSTAT_HCAC
            sstlog_new['BDWFLG'] = PL_BDWFLG_SUCC
            sstlog_new['SBAC']   = TradeContext.SBAC
            sstlog_new['RBAC']   = TradeContext.RBAC      
            sstlog_new["MGID"]   = TradeContext.errorCode       #����������
            sstlog_new["STRINFO"]= TradeContext.errorMsg        #����������Ϣ
            sstlog_new["TRDT"]   = TradeContext.TRDT            #��������
            sstlog_new["TLSQ"]   = TradeContext.TLSQ            #������ˮ��
            
            TradeContext.errorCode = 'D011'             #��ֵ���ش���
            TradeContext.errorMsg  = '����ũ��������ʧ�ܣ�ϵͳ�Զ������ɹ�'
        else:
            sstlog_new['BCSTAT'] = PL_BCSTAT_HCAC
            sstlog_new['BDWFLG'] = PL_BDWFLG_FAIL
            TradeContext.errorCode = 'D011'             #��ֵ���ش���
            TradeContext.errorMsg  = '����ũ��������ʧ�ܣ�ϵͳ�Զ�����ʧ��'

        #=====�޸�sstlog���м�¼״̬Ϊ��Ĩ��-�ɹ�/ʧ��====
        if not rccpsState.setTransState(sstlog_new):
            return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
        else:
            #=====commit����====
            AfaDBFunc.CommitSql()
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ������.���������(3.���ļ���).���˷���[TRCC002_8506]�˳�***' )
    return True
