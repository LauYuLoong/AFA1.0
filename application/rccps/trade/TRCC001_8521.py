# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.����ƾ֤��ӡ
#=================================================================
#   �����ļ�:   TRCC001_8521.py
#   �޸�ʱ��:   2008-06-05
##################################################################
#   �޸���:     �ر��
#   �޸�ʱ��:   20080731
#   �޸�����:   �����ѱ��˻������ҵ��,
#               ���ع���״̬����������,������ˮ��,��������ŵ�
#               
##################################################################
#   �޸���  ��  ������
#   �޸�ʱ�䣺  2008-09-17
#   �޸����ݣ�  ɾ���޸���������ע��,
#               ��ӳ����Ķ���Ҫע��,ʹ������׶�
#
##################################################################
import rccpsDBFunc,rccpsDBTrcc_trcbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_bilinf,TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,AfaDBFunc
from types import *
from rccpsConst import *
import rccpsState

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8521]����***' )

    #=====�ж�����ӿ�ֵ�Ƿ����====
    if(not TradeContext.existVariable("OPRTYPNO")):
        return AfaFlowControl.ExitThisFlow('A099', 'ҵ������[OPRTYPNO]������')
    if(not TradeContext.existVariable("PRTFLG")):
        return AfaFlowControl.ExitThisFlow('A099', '��ӡ��־[PRTFLG]������')
    if(not TradeContext.existVariable("BJEDTE")):
        return AfaFlowControl.ExitThisFlow('A099', '��������[BJEDTE]������')
    if(not TradeContext.existVariable("BSPSQN")):
        return AfaFlowControl.ExitThisFlow('A099', '�������[BSPSQN]������')

    #=====PL_TRCCO_HP 21 ��Ʊ====    
    if(TradeContext.OPRTYPNO==PL_TRCCO_HP):
        AfaLoggerFunc.tradeInfo("�����Ʊ����")
        
        #=====��ѯ���ݿ�====
        records = {}
        ret = rccpsDBFunc.getTransBil(TradeContext.BJEDTE,TradeContext.BSPSQN,records)
        if( ret == False):
            return AfaFlowControl.ExitThisFlow('A099', '�޴�����')
        
        AfaLoggerFunc.tradeInfo("�������ݿ��ѯ")
        
        #=====�ж��Ƿ�Ϊǩ������====
        AfaLoggerFunc.tradeInfo("��ʼ�жϵ�ǰ�����Ƿ�Ϊ���׻���")
        if( records['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('S999', 'δ���ҵ�����')
            
        AfaLoggerFunc.tradeInfo("�����жϵ�ǰ�����Ƿ�Ϊ���׻���")
               
        #=====�жϵ�ǰҵ���Ƿ�Ϊ����====
        AfaLoggerFunc.tradeInfo("��ʼ�жϵ�ǰҵ���Ƿ�Ϊ����")
        if( records['BRSFLG'] == PL_BRSFLG_SND ):
            return AfaFlowControl.ExitThisFlow('S999', '�ñ�ҵ��Ϊ����ҵ��,��ʹ��[8522 ����ƾ֤����]���״�ӡ')
        
        AfaLoggerFunc.tradeInfo("�����жϵ�ǰҵ���Ƿ�Ϊ����")
        
        #=====�жϵ�ǰ״̬====
        AfaLoggerFunc.tradeInfo("��ʼ�жϵ�ǰ״̬")
#        if( records['BCSTAT'] != PL_MBRTRCST_ACSUC and records['BCSTAT'] != PL_BCSTAT_AUTO ):
#            return AfaFlowControl.ExitThisFlow('A099', "��ǰ״̬["+records['BCSTAT']+"]�������ӡ")
        #=====pgt 0925 �����˳ɹ���Ϊ�Զ����ˣ�����û�м��ˣ������жϽ��׳ɹ����ж�====
#        if( records['BCSTAT'] != PL_BCSTAT_HANG and records['BCSTAT'] != PL_BCSTAT_AUTO and records['BDWFLG'] != PL_BDWFLG_SUCC ):
#            return AfaFlowControl.ExitThisFlow('A099', "��ǰ״̬["+records['BCSTAT']+"]�������ӡ")
        if not ((records['BCSTAT'] == PL_BCSTAT_HANG and records['BDWFLG'] == PL_BDWFLG_SUCC) or (records['BCSTAT'] == PL_BCSTAT_AUTO and records['BDWFLG'] == PL_BDWFLG_SUCC)):
            return AfaFlowControl.ExitThisFlow('A099', "��ǰ״̬["+records['BCSTAT']+"]["+records['BDWFLG']+"]�������ӡ")
            
        AfaLoggerFunc.tradeInfo("�����жϵ�ǰ״̬")
        
        #=====�жϴ�ӡ״̬====
        AfaLoggerFunc.tradeInfo("��ʼ�жϵ�ǰҵ��Ĵ�ӡ״̬")
        if(TradeContext.PRTFLG == "0" and int(records['PRTCNT']) > 0):   #��ӡ����ӡ��������0
            return AfaFlowControl.ExitThisFlow('A099','��ӡ��������1����ѡ�񲹴�' )
        
        if(TradeContext.PRTFLG == "1" and int(records['PRTCNT']) == 0):  #���򣬴�ӡ����Ϊ0
            return AfaFlowControl.ExitThisFlow('A099','��ӡ����Ϊ0����ѡ���ӡ' ) 
            
        AfaLoggerFunc.tradeInfo("�����жϵ�ǰҵ��Ĵ�ӡ״̬")
        
        #=====��ѯ��Ʊ��Ϣ�Ǽǲ�====
        AfaLoggerFunc.tradeInfo("��ʼ��ѯ��Ʊ��Ϣ�Ǽǲ�")
        bilinf_record = {}
        ret = rccpsDBFunc.getInfoBil(records['BILVER'],records['BILNO'],records['BILRS'],bilinf_record)
        if( ret == False ):
            return AfaFlowControl.ExitThisFlow('S999','��ѯ��Ʊ��Ϣ�Ǽǲ�ʧ��' ) 
        AfaLoggerFunc.tradeInfo("������ѯ��Ʊ��Ϣ�Ǽǲ�")
        
        #=====����ӿ�====
        AfaLoggerFunc.tradeInfo("��ʼ������ӿڸ�ֵ")
        TradeContext.PRTDAT     = AfaUtilTools.GetHostDate()     #��ӡ����
        TradeContext.PRTTIM     = AfaUtilTools.GetSysTime()      #��ӡʱ��
        TradeContext.BJEDTE     = records['BJEDTE']              #��������
        TradeContext.BSPSQN     = records['BSPSQN']              #�������
        TradeContext.BJETIM     = records['BJETIM']              #����ʱ��
        TradeContext.TRCCO      = records['TRCCO']               #���״���
        TradeContext.OPRATTNO   = records['OPRATTNO']            #ҵ����Ϥ
        TradeContext.TRCDAT     = records['TRCDAT']              #ί������
        TradeContext.TRCNO      = records['TRCNO']               #������ˮ��          
        TradeContext.OCCAMT     = str(bilinf_record['BILAMT'])	 #���׽��        
        TradeContext.BILNO      = records['BILNO']               #��Ʊ����            
        TradeContext.PYRACC     = bilinf_record['PYRACC']        #�������˺�  
        TradeContext.PYRNAM     = bilinf_record['PYRNAM']        #����������      
        TradeContext.PYRADDR    = bilinf_record['PYRADDR']       #�����˵�ַ      
        TradeContext.PYEACC     = bilinf_record['PYEACC']        #�տ����˺�      
        TradeContext.PYENAM     = bilinf_record['PYENAM']        #�տ�������      
        TradeContext.PYEADDR    = bilinf_record['PYEADDR']       #�տ��˵�ַ  
        TradeContext.SEAL       = bilinf_record['SEAL']          #��Ʊ��ѹ            
        TradeContext.TRDT       = records['TRDT']                #��������
        TradeContext.TLSQ       = records['TLSQ']                #������ˮ��
        TradeContext.ACC1       = records['SBAC']                #�跽�˺�
        TradeContext.ACC2       = records['RBAC']                #�����˺�
        TradeContext.ACC3       = ""                             #�����˺�
        TradeContext.DASQ       = records['DASQ']                #�������
        TradeContext.SNDBNKCO   = records['SNDBNKCO']            #�����к�
        TradeContext.SNDBNKNM   = records['SNDBNKNM']            #��������
        TradeContext.RCVBNKCO   = records['RCVBNKCO']            #�����к�
        TradeContext.RCVBNKNM   = records['RCVBNKNM']            #��������
        TradeContext.USE        = bilinf_record['USE']           #��;
        TradeContext.REMARK     = bilinf_record['REMARK']        #��ע
        TradeContext.PRTCNT     = str(int(records['PRTCNT'])+1)  #��ӡ����
        TradeContext.CUR        = bilinf_record['CUR']           #����
        TradeContext.OPRNO      = records['OPRNO']               #ҵ������
        TradeContext.RMNAMT     = str(bilinf_record['RMNAMT'])   #�������
        TradeContext.OCCAMT1    = str(bilinf_record['OCCAMT'])   #ʵ�ʽ�����
        TradeContext.PAYBNKCO   = bilinf_record['PAYBNKCO']      #����Ҹ����к�
        TradeContext.PAYBNKNM   = bilinf_record['PAYBNKNM']      #����Ҹ�������
        
        AfaLoggerFunc.tradeInfo("����������ṹ��ֵ")
        
        #=====���´�ӡ��־====
        AfaLoggerFunc.tradeInfo("��ʼ���´�ӡ��־")
        
        update_dict={'PRTCNT':records['PRTCNT']+1} 
        where_dict={'BJEDTE':records['BJEDTE'],'BSPSQN':records['BSPSQN'],'BCSTAT':records['BCSTAT']}
        
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('A099','���´�ӡ����ʧ��' )        	
        
        AfaDBFunc.CommitSql()
        
        AfaLoggerFunc.tradeInfo("�������´�ӡ��־")         
        AfaLoggerFunc.tradeInfo("������Ʊ����")
        
    #=====PL_TRCCO_HD 20 ���====
    elif(TradeContext.OPRTYPNO==PL_TRCCO_HD):
        AfaLoggerFunc.tradeInfo("�����Ҵ���")
        
        #=====��ѯ���ݿ�====
        records = {}
        ret = rccpsDBFunc.getTransTrc(TradeContext.BJEDTE,TradeContext.BSPSQN,records)
        if(ret==False):
            return AfaFlowControl.ExitThisFlow('A099','�޴�����' )
            
        #=====�ж��Ƿ�Ϊǩ������====
        AfaLoggerFunc.tradeInfo("��ʼ�жϵ�ǰ�����Ƿ�Ϊ���׻���")
        if( records['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('S999', 'Ϊ���ҵ�����')
            
        AfaLoggerFunc.tradeInfo("�����жϵ�ǰ�����Ƿ�Ϊ���׻���")
        
        #=====������ 20080702 �жϵ�ǰҵ���Ƿ�Ϊ����ҵ��====
        if records['BRSFLG'] == PL_BRSFLG_SND:
            return AfaFlowControl.ExitThisFlow('S999','�������['+TradeContext.BSPSQN+']�ñ�ҵ��Ϊ����ҵ�񣬲������ӡ')
        
        #=====�жϵ�ǰ״̬====
        #=====pgt 0925 �����жϽ��׳ɹ����ж�====
#        if records['BCSTAT'] != PL_BCSTAT_HANG and records['BCSTAT'] != PL_BCSTAT_AUTO and records['BCSTAT'] != PL_BCSTAT_QTR and records['BDWFLG'] != PL_BDWFLG_SUCC :
#            return AfaFlowControl.ExitThisFlow('A099',"��ǰ״̬[" + records['BCSTAT'] + "]�������ӡ")
        if not ((records['BCSTAT'] == PL_BCSTAT_HANG and records['BDWFLG'] == PL_BDWFLG_SUCC) or (records['BCSTAT'] == PL_BCSTAT_AUTO and records['BDWFLG'] == PL_BDWFLG_SUCC) or (records['BCSTAT'] == PL_BCSTAT_QTR and records['BDWFLG'] == PL_BDWFLG_SUCC)):
            return AfaFlowControl.ExitThisFlow('A099',"��ǰ״̬[" + records['BCSTAT'] + "]["+records['BDWFLG']+"]�������ӡ")
                
        if(TradeContext.PRTFLG == "0" and int(records['PRTCNT']) > 0):   #��ӡ����ӡ��������0
            return AfaFlowControl.ExitThisFlow('A099','��ӡ��������1����ѡ�񲹴�' )
        
        if(TradeContext.PRTFLG == "1" and int(records['PRTCNT']) == 0):  #���򣬴�ӡ����Ϊ0
            return AfaFlowControl.ExitThisFlow('A099','��ӡ����δ0����ѡ���ӡ' )
        
        AfaLoggerFunc.tradeInfo("�жϴ�ӡ��־����")
        
        #=====����ӿ�====
        TradeContext.PRTDAT   =  AfaUtilTools.GetHostDate()     #��ӡ����
        TradeContext.PRTTIM   =  AfaUtilTools.GetSysTime()      #��ӡʱ��
        TradeContext.BJEDTE   =  records['BJEDTE']              #��������
        TradeContext.BSPSQN   =  records['BSPSQN']              #�������
        TradeContext.BJETIM   =  records['BJETIM']              #����ʱ��
        TradeContext.TRCCO    =  records['TRCCO']               #ҵ������
        TradeContext.OPRATTNO =  records['OPRATTNO']            #ҵ������
        TradeContext.TRCDAT   =  records['TRCDAT']              #ί������
        TradeContext.TRCNO    =  records['TRCNO']               #������ˮ��
        TradeContext.OCCAMT   =  str(records['OCCAMT'])         #���׽��
        TradeContext.BILNO    =  records['BILNO']               #��Ʊ����
        TradeContext.PYRACC   =  records['PYRACC']              #�������˺�
        TradeContext.PYRNAM   =  records['PYRNAM']              #����������
        TradeContext.PYRADDR  =  records['PYRADDR']             #�����˵�ַ
        TradeContext.PYEACC   =  records['PYEACC']              #�տ����˺�
        TradeContext.PYENAM   =  records['PYENAM']              #�տ�������
        TradeContext.PYEADDR  =  records['PYEADDR']             #�տ��˵�ַ
        TradeContext.SEAL     =  records['SEAL']                #��Ʊ��ѹ
        
        #=====PL_BCSTAT_QTR  80 �˻�====
        if records['BCSTAT'] == PL_BCSTAT_QTR:
            #=====�˻�ҵ��,���ع���״̬��״̬��ϸ��Ϣ====
            stat_dict = {}
            if not rccpsState.getTransStateSet(records['BJEDTE'],records['BSPSQN'],PL_BCSTAT_HANG,PL_BDWFLG_SUCC,stat_dict):
                return AfaFlowControl.ExitThisFlow('A099','��ѯ�����Զ�����״̬�쳣' )
            
            TradeContext.TRDT = stat_dict['TRDT']               #��������
            TradeContext.TLSQ = stat_dict['TLSQ']               #������ˮ��
            TradeContext.ACC1 = stat_dict['SBAC']               #�跽�˺�
            TradeContext.ACC2 = stat_dict['RBAC']               #�����˺�
            TradeContext.ACC3 = ""                              #�����˺�
            TradeContext.DASQ = stat_dict['DASQ']               #�������
        else:
            #=====���˻�ҵ��,���ص�ǰ״̬��״̬��ϸ��Ϣ====
            TradeContext.TRDT = records['TRDT']	                #��������
            TradeContext.TLSQ = records['TLSQ']	                #������ˮ��
            TradeContext.ACC1 = records['SBAC']                 #�跽�˺�
            TradeContext.ACC2 = records['RBAC']                 #�����˺�
            TradeContext.ACC3 = ""                              #�����˺�
            TradeContext.DASQ = records['DASQ']                 #�������
            
        TradeContext.SNDBNKCO = records['SNDBNKCO']             #�����к�
        TradeContext.SNDBNKNM = records['SNDBNKNM']             #��������
        TradeContext.RCVBNKCO = records['RCVBNKCO']             #�����к�
        TradeContext.RCVBNKNM = records['RCVBNKNM']             #��������
        TradeContext.USE      = records['USE']                  #��;
        TradeContext.REMARK   = records['REMARK']               #��ע
        TradeContext.PRTCNT   = str(int(records['PRTCNT'])+1)   #��ӡ����
        TradeContext.OPRNO    = records['OPRNO']                #ҵ������
        TradeContext.CUR      = records['CUR']                  #����
        TradeContext.OCCAMT   = str(records['OCCAMT'])          #ҵ������
        
        #=====���´�ӡ��־====
        AfaLoggerFunc.tradeInfo("��ʼ���´�ӡ��־")
        
        update_dict={'PRTCNT':records['PRTCNT']+1}        
        where_dict={'BJEDTE':records['BJEDTE'],'BSPSQN':records['BSPSQN'],'BCSTAT':records['BCSTAT']}
        
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('A099','���´�ӡ����ʧ��' )        	
        
        AfaDBFunc.CommitSql()
    else:
        return AfaFlowControl.ExitThisFlow('A099','ҵ�����ʹ�')
        
    TradeContext.errorCode="0000"
    TradeContext.errorMsg="��ѯ�ɹ�"
    
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8521]�˳�***' )

    return True