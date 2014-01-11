# -*- coding: gbk -*-
###################################################################
#    ũ����ϵͳ.������˽��ս���.ί���տ����
#==================================================================
#    �����ļ���  TRCC005_1102.py
#    �޸�ʱ�䣺  2008-6-5
#    ��    �ߣ�  ������
#==================================================================
#    �޸�ʱ�䣺  20080730
#    �޸���  ��  �ر��
#    �޸�����:   �����ε�ģ����TRCDATʱ��,�����ⷢ��ί�����ڴ�BJEDTEȡ
#==================================================================
#    ��    �ܣ�  �յ�������˽��׺󣬽��б�Ҫ�Լ�顢��¼�����ݿ���
#		 ��������������ˣ�����afe����ͨѶ��ִ
###################################################################
import TradeContext,AfaLoggerFunc, AfaFlowControl,miya,AfaAfeFunc,HostContext
import TransBillFunc, AfaFunc, rccpsDBFunc,rccpsHostFunc,rccpsEntries
import rccpsMap1101CTradeContext2Dtrcbka_dict,rccpsMap0000Dout_context2CTradeContext
import rccpsDBTrcc_trcbka,AfaDBFunc,rccpsState,rccpsGetFunc,rccpsDBTrcc_subbra

from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( "====��ʼ������˽��մ���====" )

    #=====�ж��Ƿ��ظ�����====
    sel_dict = {'TRCNO':TradeContext.TRCNO,'TRCDAT':TradeContext.TRCDAT,'SNDBNKCO':TradeContext.SNDBNKCO}
    record = rccpsDBTrcc_trcbka.selectu(sel_dict)
    if record == None:
        return AfaFlowControl.ExitThisFlow('S999','�ж��Ƿ��ظ����ģ���ѯ���ҵ��Ǽǲ���ͬ�����쳣')
    elif len(record) > 0:
        AfaLoggerFunc.tradeInfo('���ҵ��Ǽǲ��д�����ͬ����,�ظ�����,������һ����')
        #=====ΪͨѶ��ִ���ĸ�ֵ====
        out_context_dict = {}
        out_context_dict['sysType']  = 'rccpst'
        out_context_dict['TRCCO']    = '9900503'
        out_context_dict['MSGTYPCO'] = 'SET008'
        out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
        out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
        out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
        out_context_dict['SNDCLKNO'] = TradeContext.BETELR
        out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
        out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
        out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
        out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
        out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
        out_context_dict['OPRTYPNO'] = '99'
        out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
        out_context_dict['TRANTYP']  = '0'
        out_context_dict['ORTRCCO']  = TradeContext.TRCCO
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ظ�����'

        rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

        #=====����afe====
        AfaAfeFunc.CommAfe()

        return AfaFlowControl.ExitThisFlow('S999','�ظ����ģ��˳���������')

    AfaLoggerFunc.tradeInfo(">>>�����ж��Ƿ��ظ�����")

    #=====����ת��====
    if TradeContext.CUR == 'CNY':
        TradeContext.CUR  = '01'

    #====��ʼ���ֵ丳ֵ====
    trcbka_dict = {}
    if not rccpsMap1101CTradeContext2Dtrcbka_dict.map(trcbka_dict):
        return AfaFlowControl.ExitThisFlow('M999', '�ֵ丳ֵ����')

    trcbka_dict['DCFLG'] = PL_DCFLG_CRE                  #�����ʶ
    trcbka_dict['OPRNO'] = '01'                          #ҵ������

    #=====��ʼ�������ݿ�====
    if not rccpsDBFunc.insTransTrc(trcbka_dict):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('D002', '�������ݿ����,RollBack�ɹ�')
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('������ҵ��Ǽǲ���COMMIT�ɹ�')

    #=====����״̬Ϊ����====
    sstlog   = {}
    sstlog['BSPSQN']   = TradeContext.BSPSQN
    sstlog['BJEDTE']   = TradeContext.BJEDTE
    sstlog['BCSTAT']   = PL_BCSTAT_BNKRCV
    sstlog['BDWFLG']   = PL_BDWFLG_SUCC

    #=====����״̬Ϊ ����-�ɹ� ====
    if not rccpsState.setTransState(sstlog):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeInfo('>>>commit�ɹ�')
        
    ##========================= START �ź� ������20091011 ��������������ʹ��˴���  =====================##
    #��ʼ���ǹ��˱�ʶ,����.0,����.1,Ĭ�ϼ���
    accflag = 0
    #���ջ����ݴ�
    TradeContext.BESBNOFIRST = TradeContext.BESBNO
    
    if accflag == 0:
        AfaLoggerFunc.tradeInfo(">>>��ʼУ����Ѻ")
        #=====��ʼ������Ѻ���������к�Ѻ====
        SNDBANKCO  = TradeContext.SNDBNKCO
        RCVBANKCO  = TradeContext.RCVBNKCO
        SNDBANKCO = SNDBANKCO.rjust(12,'0')
        RCVBANKCO = RCVBANKCO.rjust(12,'0')
        AMOUNT = TradeContext.OCCAMT.split('.')[0] + TradeContext.OCCAMT.split('.')[1]
        AMOUNT = AMOUNT.rjust(15,'0')
        
        AfaLoggerFunc.tradeDebug('AMOUNT=' + str(AMOUNT) )
        AfaLoggerFunc.tradeDebug('SNDBANKCO=' + str(SNDBANKCO) )
        AfaLoggerFunc.tradeDebug('RCVBANKCO=' + str(RCVBANKCO) )

        ret = miya.DraftEncrypt(PL_SEAL_DEC,PL_TYPE_DZHD,TradeContext.TRCDAT,TradeContext.TRCNO,AMOUNT,SNDBANKCO,RCVBANKCO,'',TradeContext.SEAL)

        if ret != 0:
            #��Ѻ��,����
            AfaLoggerFunc.tradeInfo("��ѺУ��δͨ��,ret=[" + str(ret) + "]")
            accflag = 1
            TradeContext.NOTE3 = "��Ѻ��,����!"
        else:
            #��ѺУ��ͨ��
            AfaLoggerFunc.tradeInfo("��ѺУ��ͨ��")
            
        AfaLoggerFunc.tradeInfo(">>>����У����Ѻ")
        
    #У���˺��Ƿ�Ƿ�
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("��ʼУ���˺��Ƿ�Ƿ�")  
        
        if (len(TradeContext.PYEACC) != 23) and (len(TradeContext.PYEACC) != 19) :
            accflag = 1
            TradeContext.NOTE3 = '���˺Ų��ǶԹ����˽�˺�,����!'
            
        AfaLoggerFunc.tradeInfo("����У���˺��Ƿ�Ƿ�")

    #���������ӿڲ�ѯ�˻���Ϣ
    if accflag == 0:
        #����8810��ѯ�˻���Ϣ
        AfaLoggerFunc.tradeInfo("��ʼ��ѯ�˻���Ϣ")
        
        TradeContext.ACCNO = TradeContext.PYEACC      
        TradeContext.HostCode = '8810'                  
        rccpsHostFunc.CommHost( '8810' )   
        
        if TradeContext.errorCode != '0000':
            accflag = 1
            TradeContext.NOTE3 = '��ѯ�տ�����Ϣʧ��,����!'
        elif TradeContext.errorCode == '0000' and len(TradeContext.ACCSO) == 0 :
            accflag = 1
            TradeContext.NOTE3 = '��ѯ�տ��˿�������ʧ��,����!'
            
        AfaLoggerFunc.tradeInfo("������ѯ�˻���Ϣ")
        
    #У���˻�״̬�Ƿ�����
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("��ʼУ���Ƿ�編��")     
         
        if TradeContext.ACCSO[0:6] != TradeContext.BESBNO[0:6] :
            accflag = 1
            TradeContext.NOTE3 = '���������˻������п編��,����!'
            
        AfaLoggerFunc.tradeInfo("����У���Ƿ�編��")
        
    #У�鿪�������Ƿ��������ϵ
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("��ʼУ��������뿪�������Ƿ�Ϊͬһ����")
        
        if TradeContext.ACCSO != TradeContext.BESBNOFIRST:
            khjg = {}
            khjg['BESBNO'] = TradeContext.ACCSO
            khjg['BTOPSB'] = TradeContext.BESBNOFIRST
            khjg['SUBFLG'] = PL_SUBFLG_SUB                                 
            rec = rccpsDBTrcc_subbra.selectu(khjg)
            if rec == None:
                accflag = 1
                TradeContext.NOTE3 = '��ѯ�˻������ϵʧ��,����!'
            elif len(rec) <= 0:
                accflag = 1
                TradeContext.NOTE3 = '�˻�δ���������ϵ,����!'
            else:
                #���ջ����뿪���������ڴ����ϵ,���û�����Ϊ����������
                TradeContext.BESBNO  =  TradeContext.ACCSO
                
        AfaLoggerFunc.tradeInfo("����У��������뿪�������Ƿ�Ϊͬһ����")
        
    #У���˺�״̬�Ƿ�����
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("��ʼУ���˺�״̬�Ƿ�����")
        
        if TradeContext.ACCST != '0' and  TradeContext.ACCST != '2':
           accflag = 1
           TradeContext.NOTE3 = '�˻�״̬������,����!'
           
           #�ڽ��������ϵ�������,�˻�״̬������,ͬ������
           TradeContext.BESBNO  = TradeContext.BESBNOFIRST
           
        AfaLoggerFunc.tradeInfo("����У���˺�״̬�Ƿ�����")

    #У���տ��˻����Ƿ�һ��
    if accflag == 0:
        AfaLoggerFunc.tradeInfo("��ʼУ���տ��˻����Ƿ�һ��")
        
        if TradeContext.ACCNM != TradeContext.PYENAM :
             accflag = 1
             TradeContext.NOTE3 = '�տ��˻�������,����!'
             
             #�ڽ��������ϵ�������,�˻�״̬������,ͬ������
             TradeContext.BESBNO  = TradeContext.BESBNOFIRST
           
        AfaLoggerFunc.tradeInfo("����У���տ��˻����Ƿ�һ��")

    if (TradeContext.existVariable( "PYEACC" ) and len(TradeContext.PYEACC) != 0):       #�տ�������
        TradeContext.PYEACC      = TradeContext.PYEACC
    else:
        TradeContext.PYEACC      = ''
         
    if (TradeContext.existVariable( "PYENAM" ) and len(TradeContext.PYENAM) != 0):       #�տ�������
        TradeContext.OTNM      = TradeContext.PYENAM
    else:
        TradeContext.OTNM      = ''
        
    #������ʼ����ֵ丳ֵ
    input_dict = {}
    
    if (TradeContext.existVariable( "PYRNAM" ) and len(TradeContext.PYRNAM) != 0):          #�����˻���
        TradeContext.SBACACNM      =      TradeContext.PYRNAM
        
    input_dict['accflag']     = str(accflag)                                #�ǹұ�־
    input_dict['OCCAMT']      = TradeContext.OCCAMT                         #���׽��
    input_dict['PYEACC']      = TradeContext.PYEACC                         #�տ����˺�
    input_dict['OTNM']        = TradeContext.OTNM                           #�տ�������
    input_dict['BESBNO']      = TradeContext.BESBNO
        
    #���û�Ҽ��˽ӿ�
    rccpsEntries.HDLZJZ(input_dict)
    
    TradeContext.accflag    = accflag                                    #�����־

    #=====��ʼ������ƴ�����˺ŵ�25λУ��λ====
    TradeContext.HostCode = '8813'                                   #����8813�����ӿ�
    TradeContext.RCCSMCD  = PL_RCCSMCD_HDLZ                          #����ժҪ���룺�������
    TradeContext.ACUR = '1'
    ##========================= END �ź� ������20091011 ��������������ʹ��˴���  =====================##

    #=====����sstlog��״̬��¼====
    if not rccpsState.newTransState(TradeContext.BJEDTE,TradeContext.BSPSQN,TradeContext.BCSTAT,TradeContext.BDWFLG):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow('M999', '����״̬['+TradeContext.BCSTAT+']['+TradeContext.BDWFLG+']ʧ��,ϵͳ�Զ��ع�')
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()

    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('>>>�������˺���')
   
    #=====��ʼ���ֵ丳ֵ====
    sst_dict = {}
    sst_dict['BSPSQN']  = TradeContext.BSPSQN            #�������
    sst_dict['BJEDTE']  = TradeContext.BJEDTE            #��������
    sst_dict['SBAC']    = TradeContext.SBAC              #�跽�˺�
    sst_dict['BESBNO']  = TradeContext.BESBNO            #������
    if (TradeContext.existVariable( "NOTE3" ) and len(TradeContext.NOTE3) != 0):  
        sst_dict['NOTE3']   = TradeContext.NOTE3         #��ע3
        AfaLoggerFunc.tradeDebug('>>>test  NOTE3 =['+TradeContext.NOTE3 +']')
    sst_dict['BJETIM']  = TradeContext.BJETIM            #����ʱ��
    sst_dict['MGID']     = TradeContext.errorCode         #�������ش���
    sst_dict['STRINFO']  = TradeContext.errorMsg          #����������Ϣ
    sst_dict['BETELR']  = TradeContext.BETELR            #��Ա��

    #=====��ʼ�ж��������ؽ��====
    out_context_dict = {}
    
    if TradeContext.errorCode == '0000' :
        AfaLoggerFunc.tradeDebug('>>>����ͨѶ�ɹ�,���±�״̬��ʼ')
        trcbka_jgh = {}
        trcbka_where = {}
        trcbka_jgh['BESBNO'] = TradeContext.BESBNO  
        trcbka_where['BSPSQN'] = TradeContext.BSPSQN 
        trcbka_where['BJEDTE'] = TradeContext.BJEDTE
        
        if not rccpsDBTrcc_trcbka.updateCmt( trcbka_jgh,trcbka_where ):
            #=====RollBack����====
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('D002', '�������ݿ����,RollBack�ɹ�')
        else:
            #=====commit����====
            AfaDBFunc.CommitSql()
            AfaLoggerFunc.tradeInfo('���µǼǲ���COMMIT�ɹ�')
            
        if (TradeContext.existVariable( "RBAC" ) and len(TradeContext.RBAC) != 0):  
            sst_dict['RBAC']   = TradeContext.RBAC                 
            AfaLoggerFunc.tradeDebug('>>>test  RBAC =['+TradeContext.RBAC +']')
        if (TradeContext.existVariable( "REAC" ) and len(TradeContext.REAC) != 0):  
            sst_dict['REAC']   = TradeContext.REAC                 
            AfaLoggerFunc.tradeDebug('>>>test  REAC =['+TradeContext.REAC +']')

        #�Զ�����
        if TradeContext.accflag == 1 :
            sst_dict['BCSTAT']  = PL_BCSTAT_HANG                #�Զ�����
            AfaLoggerFunc.tradeDebug('>>>test  BCSTAT=['+str(sst_dict['BCSTAT']) +']')
        #�Զ�����
        elif TradeContext.accflag == 0 :
            sst_dict['BCSTAT']  = PL_BCSTAT_AUTO                 #�Զ����� 
            AfaLoggerFunc.tradeDebug('>>>test  BCSTAT=['+str(sst_dict['BCSTAT']) +']')
        if (TradeContext.existVariable( "DASQ" ) and len(TradeContext.DASQ) != 0):  
           sst_dict['DASQ']    = TradeContext.DASQ              #�������
           AfaLoggerFunc.tradeDebug('>>>test  DASQ  =['+TradeContext.DASQ +']')
        sst_dict['BDWFLG']  = PL_BDWFLG_SUCC                 #�ɹ�
        AfaLoggerFunc.tradeDebug('>>>test  BDWFLG=['+str(sst_dict['BDWFLG']) +']')
        sst_dict['TRDT']    = TradeContext.TRDT              #��������
        AfaLoggerFunc.tradeDebug('>>>test  TRDT  =['+TradeContext.TRDT   +']')
        sst_dict['TLSQ']    = TradeContext.TLSQ              #������ˮ
        AfaLoggerFunc.tradeDebug('>>>test  TLSQ  =['+TradeContext.TLSQ   +']')
        
        AfaLoggerFunc.tradeDebug('>>>����ͨѶ�ɹ�,���±�״̬����')
        
        out_context_dict['PRCCO']    = 'RCCI0000'
        out_context_dict['STRINFO']  = '�ɹ�'
        
    else :    
        if TradeContext.accflag == 1 :
            sst_dict['BCSTAT']  = PL_BCSTAT_HANG                            #�Զ�����
            sst_dict['BDWFLG']  = PL_BDWFLG_FAIL                            #����ʧ��
            
            out_context_dict['PRCCO']    = 'RCCI1056'
            out_context_dict['STRINFO']  = '����ʧ��,����ʧ��'
        
        elif TradeContext.accflag == 0 :
            #����ʧ��,�Ҵ��������
            TradeContext.BESBNO = TradeContext.BESBNOFIRST
            #������ʹ����ֵ丳ֵ
            input_dict = {}
            input_dict['accflag']     = str(TradeContext.accflag)                   #�ǹұ�־
            input_dict['OCCAMT']      = TradeContext.OCCAMT                         #���׽��
            input_dict['BESBNO']      = TradeContext.BESBNOFIRST
                
            #���û�Ҽ��˽ӿ�
            rccpsEntries.HDLZGZ(input_dict)
            
            rccpsHostFunc.CommHost( '8813' )
            
            sst_dict = {}
            sst_dict['BSPSQN']  = TradeContext.BSPSQN            #�������
            AfaLoggerFunc.tradeDebug('>>>test  BSPSQN=['+TradeContext.BSPSQN+']')
            sst_dict['BJEDTE']  = TradeContext.BJEDTE            #��������
            AfaLoggerFunc.tradeDebug('>>>test  BJEDTE=['+TradeContext.BJEDTE+']')
            sst_dict['SBAC']    = TradeContext.SBAC              #�跽�˺�
            AfaLoggerFunc.tradeDebug('>>>test  SBAC=['+TradeContext.SBAC+']')
            sst_dict['BESBNO']  = TradeContext.BESBNO            #������
            AfaLoggerFunc.tradeDebug('>>>test  BESBNO=['+TradeContext.BESBNO+']')
            if (TradeContext.existVariable( "NOTE3" ) and len(TradeContext.NOTE3) != 0):  
                sst_dict['NOTE3']   = TradeContext.NOTE3         #��ע3
                AfaLoggerFunc.tradeDebug('>>>test  NOTE3 =['+TradeContext.NOTE3 +']')
            sst_dict['BJETIM']  = TradeContext.BJETIM            #����ʱ��
            AfaLoggerFunc.tradeDebug('>>>test  BJETIM=['+TradeContext.BJETIM+']')
            sst_dict['MGID']     = TradeContext.errorCode        #�������ش���
            sst_dict['STRINFO']  = TradeContext.errorMsg         #����������Ϣ
            sst_dict['BETELR']  = TradeContext.BETELR            #��Ա��
            
            if TradeContext.errorCode == '0000':
                AfaLoggerFunc.tradeDebug(">>>SubModuleDoSnd--���ʳɹ�")            
                sst_dict['BCSTAT']  = PL_BCSTAT_HANG          
                sst_dict['BDWFLG']  = PL_BDWFLG_SUCC
                
                out_context_dict['PRCCO']    = 'RCCI0000'
                out_context_dict['STRINFO']  = '�ɹ�'
                
            else:
                AfaLoggerFunc.tradeDebug(">>>SubModuleDoSnd--����ʧ��")
                sst_dict['BCSTAT']  = PL_BCSTAT_HANG             
                sst_dict['BDWFLG']  = PL_BDWFLG_FAIL
                out_context_dict['PRCCO']    = 'RCCI1056'
                out_context_dict['STRINFO']  = '����ʧ��,����ʧ��'


    AfaLoggerFunc.tradeDebug('>>>��ǰҵ��״̬[' + str(sst_dict['BCSTAT']) + ']')
    AfaLoggerFunc.tradeDebug('>>>��ǰ��ת��־[' + str(sst_dict['BDWFLG']) + ']')
            
    #=====����״̬Ϊ ����/����-�ɹ� ====
    if not rccpsState.setTransState(sst_dict):
        #=====RollBack����====
        AfaDBFunc.RollbackSql()
        return AfaFlowControl.ExitThisFlow(TradeContext.errorCode, TradeContext.errorMsg)
    else:
        #=====commit����====
        AfaDBFunc.CommitSql()
        AfaLoggerFunc.tradeDebug('>>>commit�ɹ�')

    #=====��ʼ����ͨѶ��ִ������Ϣ====
    AfaLoggerFunc.tradeInfo('>>>��ʼ��֯ͨѶ��ִ����')

    out_context_dict['sysType']  = 'rccpst'
    out_context_dict['TRCCO']    = '9900503'
    out_context_dict['MSGTYPCO'] = 'SET008'
    out_context_dict['RCVMBRCO'] = TradeContext.SNDMBRCO
    out_context_dict['SNDMBRCO'] = TradeContext.RCVMBRCO
    out_context_dict['SNDBRHCO'] = TradeContext.BESBNO
    out_context_dict['SNDCLKNO'] = TradeContext.BETELR
    out_context_dict['SNDTRDAT'] = TradeContext.BJEDTE
    out_context_dict['SNDTRTIM'] = TradeContext.BJETIM
    out_context_dict['MSGFLGNO'] = out_context_dict['SNDMBRCO'] + TradeContext.BJEDTE + TradeContext.SerialNo
    out_context_dict['ORMFN']    = TradeContext.MSGFLGNO
    out_context_dict['NCCWKDAT'] = TradeContext.NCCworkDate
    out_context_dict['OPRTYPNO'] = '99'
    out_context_dict['ROPRTPNO'] = TradeContext.OPRTYPNO
    out_context_dict['TRANTYP']  = '0'
    out_context_dict['ORTRCCO']  = TradeContext.TRCCO

    rccpsMap0000Dout_context2CTradeContext.map(out_context_dict)

    return True
def SubModuleDoTrd():
    #=====�ж�afe���ؽ��====
    if TradeContext.errorCode == '0000':
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ���ĳɹ�')
    else:
        AfaLoggerFunc.tradeInfo('>>>���ͻ�ִ����ʧ��')

    return True
