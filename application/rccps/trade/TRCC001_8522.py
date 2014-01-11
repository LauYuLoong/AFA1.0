# -*- coding: gbk -*-
##################################################################
#   ũ����.��ѯ��ӡҵ��.����ƾ֤��ӡ
#=================================================================
#   �����ļ�:   TRCC001_8522.py
#   �޸�ʱ��:   2008-06-11
#   ���ߣ�      �˹�ͨ
##################################################################
#   �޸���  ��  ������
#   �޸�ʱ�䣺  2008-09-17
#   �޸����ݣ�  ɾ���޸���������ע��,
#               ��ӳ����Ķ���Ҫע��,ʹ������׶�
#
##################################################################
#   �޸���  ��  �˹�ͨ
#   �޸�ʱ�䣺  2008-10-24
#   �޸����ݣ�  ���ͨ��ͨ�Ҳ���
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBFunc,AfaDBFunc,rccpsDBTrcc_sstlog
from types import *
from rccpsConst import *
import rccpsMap8522DTrans2CTradeContext,rccpsMap8522DInfo2CTradeContext,rccpsMap8522DTransTrc2CTradeContext,rccpsMap8522Drecords2CTradeContext
import rccpsDBTrcc_bilbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_trcbka,rccpsDBTrcc_wtrbka

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8522]����***' )
    
    #=====�жϽӿ��Ƿ����====
    if( not TradeContext.existVariable( "BJEDTE" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��������[BJEDTE]������')        
    if( not TradeContext.existVariable( "BSPSQN" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '�������[BSPSQN]������')       
    if( not TradeContext.existVariable( "OPRTYPNO" ) ):
        return AfaFlowControl.ExitThisFlow('A099', 'ҵ������[OPRTYPNO]������')       
    if( not TradeContext.existVariable( "BCURSQ" ) ):
        return AfaFlowControl.ExitThisFlow('A099', '��ǰ������[BCURSQ]������')
        
    #=====��ѯ��ʷ״̬��õ��������ں�������ˮ��====
    
    where_sql={'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
    
    ret=rccpsDBTrcc_sstlog.selectu(where_sql)
    if(ret==None):
        return AfaFlowControl.ExitThisFlow('A099', '��ѯ��ʷ״̬��ʧ��')
    if(len(ret)==0):
        return AfaFlowControl.ExitThisFlow('A099', '��ѯ��ʷ״̬����Ϊ��')
    if(ret['TRDT']=="" or ret['TLSQ']==""):
        return AfaFlowControl.ExitThisFlow('A099', '�����״̬�ǳɹ�������״̬')
             
    #=====PL_TRCCO_HP 21 ��Ʊ====
    if(TradeContext.OPRTYPNO==PL_TRCCO_HP):
        AfaLoggerFunc.tradeInfo("�����Ʊ����")

        records1={}
        #=====��ѯ��Ʊҵ��Ǽǲ�====
        bilbka_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN} 
        res_bilbka = rccpsDBTrcc_bilbka.selectu(bilbka_where_dict)  
        if( res_bilbka == None):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��Ʊ���׵Ǽǲ�ʧ��')          
        if( len(res_bilbka) == 0 ):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��Ʊ���׵Ǽǲ����Ϊ��')
            
        #=====��ѯ״̬��ϸ��====
        sstlog_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
        res_sstlog = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
        if( res_sstlog == None):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��ʷ״̬�Ǽǲ�ʧ��')            
        if( len(res_sstlog) == 0):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��ʷ״̬�Ǽǲ����Ϊ��')
            
        #=====��resords1��ֵ,�ֵ���Ӹ�ֵ���µ��ֵ�====
        records1.update(res_bilbka)
        records1.update(res_sstlog)
        
        #=====�ж��Ƿ�Ϊǩ������====
        AfaLoggerFunc.tradeInfo("��ʼ�жϵ�ǰ�����Ƿ�Ϊ���׻���")

        if( records1['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('S999', 'Ϊ���ҵ�����')
            
        AfaLoggerFunc.tradeInfo("�����жϵ�ǰ�����Ƿ�Ϊ���׻���")   
        
        #=====�ж��Ƿ�Ϊ����ҵ��====
        if records1['BRSFLG'] != PL_BRSFLG_SND:
            return AfaFlowControl.ExitThisFlow('S999','�������['+TradeContext.BSPSQN+']�ñ�ҵ��Ϊ����ҵ�񣬲������ӡ')
        
#        #=====�жϻ�Ʊ״̬������ǳ������ô�ӡ====
#        if(records1['HPSTAT'] == PL_HPSTAT_CANC ):
#            return AfaFlowControl.ExitThisFlow('S999','�˻�ƱΪ����״̬���������ӡ')
        
        #=====�жϵ�ǰ״̬====
        #=====PL_BCSTAT_ACC  20 ����====
        #=====PL_BCSTAT_HCAC 21 Ĩ��====
        if(records1['BCSTAT']!=PL_BCSTAT_ACC and records1['BCSTAT']!=PL_BCSTAT_HCAC):
            return AfaFlowControl.ExitThisFlow('A009',"��ǰ״̬[" + records1['BCSTAT'] + "]�������ӡ")
                
        records2={}
        #=====��ѯ��Ʊ��Ϣ�Ǽǲ�====
        res=rccpsDBFunc.getInfoBil(records1['BILVER'],records1['BILNO'],records1['BILRS'],records2)
        if(res==False):
            return AfaFlowControl.ExitThisFlow('D003','��Ʊ��Ϣ�Ǽǲ����޼�¼')    
        
        #=====����ӿ�====
        rccpsMap8522DTrans2CTradeContext.map(records1)
        rccpsMap8522DInfo2CTradeContext.map(records2)
        
        TradeContext.PRTDAT  =  AfaUtilTools.GetHostDate()          #��ӡ����
        TradeContext.PRTTIM  =  AfaUtilTools.GetSysTime()           #��ӡʱ��
        TradeContext.PRTCNT  =  str(int(TradeContext.PRTCNT)+1)     #��ӡ����
        TradeContext.BCSTAT  =  ret['BCSTAT']                       #��ǰ״̬
        TradeContext.BDWFLG  =  ret['BDWFLG']                       #��ת�����ʶ
        TradeContext.TRDT    =  ret['TRDT']                         #��������
        TradeContext.TLSQ    =  ret['TLSQ']                         #������ˮ
        TradeContext.OCCAMT  =  str(TradeContext.OCCAMT)            #���׽��
        TradeContext.BILAMT  =  str(TradeContext.BILAMT)            #��Ʊ���
        TradeContext.RMNAMT  =  str(TradeContext.RMNAMT)            #������
                
        #=====���´�ӡ��־====
        AfaLoggerFunc.tradeInfo("��ʼ���´�ӡ��־")
        
        update_dict={'PRTCNT':TradeContext.PRTCNT}
        where_dict={'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCSTAT':TradeContext.BCSTAT}
        
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','�޸����ݿ��ӡ����ʧ��')
        else:
            AfaLoggerFunc.tradeDebug('>>>commit �ɹ�')
        
        AfaDBFunc.CommitSql()
               
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
       
    #=====PL_TRCCO_HD 20 ���====
    elif(TradeContext.OPRTYPNO==PL_TRCCO_HD):
        AfaLoggerFunc.tradeInfo("�����Ҵ���")

        records={}
        #=====��ѯ��ҵǼǲ�====
        trcbka_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        res_trcbka = rccpsDBTrcc_trcbka.selectu(trcbka_where_dict)
        if( res_trcbka == None ):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��ҵǼǲ��쳣')
            
        if( len(res_trcbka) == 0 ):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��ҵǼǲ����Ϊ��')
            
        #=====��ѯ��ʷ״̬��====
        sstlog_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
        res_sstlog = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
        if( res_sstlog == None):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��ʷ״̬�Ǽǲ�ʧ��')            
        if( len(res_sstlog) == 0):
            return AfaFlowControl.ExitThisFlow('S999', '��ѯ��ʷ״̬�Ǽǲ����Ϊ��')
            
        #=====��records��ֵ,�ֵ���Ӹ�ֵ���µ��ֵ�====
        records.update(res_trcbka)
        records.update(res_sstlog)
        
        #=====�ж��Ƿ�Ϊǩ������====
        AfaLoggerFunc.tradeInfo("��ʼ�жϵ�ǰ�����Ƿ�Ϊ���׻���")
        if( records['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('S999', '��ǩ������')
            
        AfaLoggerFunc.tradeInfo("�����жϵ�ǰ�����Ƿ�Ϊ���׻���")
        
        #=====�ж��Ƿ�Ϊ����ҵ��====
        if records['BRSFLG'] != PL_BRSFLG_SND:
            return AfaFlowControl.ExitThisFlow('S999','�������['+TradeContext.BSPSQN+']�ñ�ҵ��Ϊ����ҵ�񣬲������ӡ')
        
        #=====�жϵ�ǰ״̬====
        #=====PL_BCSTAT_ACC  20 ����====
        #=====PL_BCSTAT_HCAC 21 Ĩ��====
        if not (records['BCSTAT']==PL_BCSTAT_ACC or records['BCSTAT'] == PL_BCSTAT_HCAC):
            return AfaFlowControl.ExitThisFlow('A009',"��ǰ״̬[" + records1['BCSTAT'] + "]�������ӡ")
        
        rccpsMap8522DTransTrc2CTradeContext.map(records)
        
        #=====����ӿ�====
        TradeContext.PRTDAT  = AfaUtilTools.GetHostDate()       #��ӡ����
        TradeContext.PRTTIM  = AfaUtilTools.GetSysTime()        #��ӡʱ��
        TradeContext.PRTCNT  = str(int(TradeContext.PRTCNT)+1)  #��ӡ����
        TradeContext.OCCAMT  = str(TradeContext.OCCAMT)         #���׽��
        TradeContext.BILAMT  = str(TradeContext.COMAMT)	        #��Ʊ���
        TradeContext.BCSTAT  = ret['BCSTAT']                    #��ǰ״̬
        TradeContext.BDWFLG  = ret['BDWFLG']                    #��ת�����ʶ
        TradeContext.TRDT    = ret['TRDT']                      #��������
        TradeContext.TLSQ    = ret['TLSQ']                      #������ˮ��
        
        #=====���´�ӡ��־====
        AfaLoggerFunc.tradeInfo("��ʼ���´�ӡ��־")
        update_dict={'PRTCNT':TradeContext.PRTCNT}
        where_dict={'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCSTAT':TradeContext.BCSTAT}
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','�޸����ݿ��ӡ����ʧ��')
        
        AfaDBFunc.CommitSql()
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
    
    #=====30 ͨ��ͨ��====
    elif( TradeContext.OPRTYPNO == PL_TRCCO_TCTD ):
        AfaLoggerFunc.tradeInfo("����ͨ��ͨ�Ҵ���")
        
        records = {}
        #=====��ѯ������Ϣ====
        AfaLoggerFunc.tradeInfo("��ѯ������Ϣ")
        wtrbka_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN}
        res_wtrbka = rccpsDBTrcc_wtrbka.selectu(wtrbka_where_dict)
        if( len(res_wtrbka) == 0 ):
            return AfaFlowControl.ExitThisFlow('A009','��ѯ������Ϣ���Ϊ��')
        if( res_wtrbka == None ):
            return AfaFlowControl.ExitThisFlow('A009','��ѯ������Ϣʧ��')
            
        #=====��ѯ���׵���ʷ״̬====    
        AfaLoggerFunc.tradeInfo("��ѯ���׵���ʷ״̬")
        sstlog_where_dict = {'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
        res_sstlog = rccpsDBTrcc_sstlog.selectu(sstlog_where_dict)
        if( len(res_sstlog) == 0 ):
            return AfaFlowControl.ExitThisFlow('A009','��ѯ������ʷ״̬���Ϊ��')
        if( res_sstlog == None ):
            return AfaFlowControl.ExitThisFlow('A009','��ѯ������ʷ״̬ʧ��')
            
        #=====��records�ֵ丳ֵ���ֵ���ӣ���ֵ���µ��ֵ�====
        records.update(res_wtrbka)
        records.update(res_sstlog)
        
        #=====�ж��Ƿ�Ϊǩ������====
        AfaLoggerFunc.tradeInfo("�ж��Ƿ�Ϊǩ������")
        if( records['BESBNO'] != TradeContext.BESBNO ):
            return AfaFlowControl.ExitThisFlow('A009','�˻�������ǩ������')
        
        #=====�жϴ˽����Ƿ�Ϊ����====
        AfaLoggerFunc.tradeInfo("�жϴ˽����Ƿ�Ϊ����")
        if( records['BRSFLG'] != PL_BRSFLG_SND ):
            return AfaFlowControl.ExitThisFlow('A009','�˽��ײ������˽���')
            
        #=====�жϽ���״̬====
        AfaLoggerFunc.tradeInfo("�жϴ˽���״̬")
        if not ( records['BCSTAT'] == PL_BCSTAT_ACC or records['BCSTAT'] == PL_BCSTAT_HCAC or records['BCSTAT'] == PL_BCSTAT_CANCEL or records['BCSTAT'] == PL_BCSTAT_CANC):
            return AfaFlowControl.ExitThisFlow('A009','��״̬�������ӡ')
        
        if(records['BCSTAT'] == PL_BCSTAT_CANCEL or records['BCSTAT'] == PL_BCSTAT_CANC):
            if(records['TRDT'] == "" or records['TLSQ'] == ""):
                return AfaFlowControl.ExitThisFlow('A009','�˱�ҵ��û�в�����������')
            
            
        rccpsMap8522Drecords2CTradeContext.map(records)
        
        #=====����ӿ�====
        AfaLoggerFunc.tradeInfo("������ӿڸ�ֵ")
        TradeContext.PRTDAT  = AfaUtilTools.GetHostDate()
        TradeContext.PRTTIM  = AfaUtilTools.GetSysTime() 
        TradeContext.PRTCNT  = str(int(records['PRTCNT'])+1) 
        TradeContext.USE     = ""
        TradeContext.BILAMT  = str(records['OCCAMT']) 
        TradeContext.BCSTAT  = ret['BCSTAT']                    #��ǰ״̬
        TradeContext.BDWFLG  = ret['BDWFLG']                    #��ת�����ʶ
        TradeContext.TRDT    = ret['TRDT']                      #��������
        TradeContext.TLSQ    = ret['TLSQ']                      #������ˮ��    
        TradeContext.REMARK  = ""
        TradeContext.DASQ    = records['DASQ']                  #�������
        TradeContext.BNKBKNO = records['BNKBKNO']               #���ۺ���
        TradeContext.CHSHTP  = records['CHRGTYP']               #��������ȡ��ʽ
        if(records['TRCCO'] in ('3000002','30000102')):         #���۱�־
            TradeContext.PYITYP = records['PYETYP']
        else:
            TradeContext.PYITYP = records['PYRTYP']

        #=====���´�ӡ��־====        
        AfaLoggerFunc.tradeInfo("��ʼ���´�ӡ��־")
        update_dict={'PRTCNT':str(int(records['PRTCNT'])+1)}
        where_dict={'BJEDTE':TradeContext.BJEDTE,'BSPSQN':TradeContext.BSPSQN,'BCURSQ':TradeContext.BCURSQ}
        rownum=rccpsDBTrcc_sstlog.update(update_dict,where_dict)
        if(rownum<=0):
            AfaDBFunc.RollbackSql()
            return AfaFlowControl.ExitThisFlow('S999','�޸����ݿ��ӡ����ʧ��')
        
        AfaDBFunc.CommitSql()
        TradeContext.errorCode="0000"
        TradeContext.errorMsg="��ѯ�ɹ�"
         
    else:
        return AfaFlowControl.ExitThisFlow('A009','ҵ������Ƿ�')

    AfaLoggerFunc.tradeInfo( '***ũ����ϵͳ: ����.�������������[RCC001_8522]�˳�***' )
    return True
