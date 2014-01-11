# -*- coding: gbk -*-
##################################################################
#   ũ����.ͨ��ͨ�����˽���.ͨ��ͨ�Ҳ���˲���
#=================================================================
#   �����ļ�:   TRCC001_8572.py
#   �޸�ʱ��:   2008-12-09
#   ���ߣ�      �˹�ͨ
##################################################################

import TradeContext,AfaFlowControl,AfaLoggerFunc,AfaUtilTools,rccpsState,AfaDBFunc,rccpsEntriesErr,rccpsHostFunc,rccpsFunc,rccpsGetFunc,rccpsState
import rccpsDBTrcc_tddzcz,rccpsDBTrcc_wtrbka,rccpsDBTrcc_sstlog,rccpsDBTrcc_tddzmx,rccpsDBTrcc_notbka,rccpsDBTrcc_spbsta
from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.����˲���[8572] ����")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<���Ի�����(���ز���) ����")
    #=====У������ĺϷ���====
    AfaLoggerFunc.tradeInfo("<<<<<<У������ĺϷ���")   
    if not TradeContext.existVariable("SNDBNKCO"):
        return AfaFlowControl.ExitThisFlow('A099','û�з����к�')
        
    if not TradeContext.existVariable("TRCNO"):
        return AfaFlowControl.ExitThisFlow('A099','û�н�����ˮ��')
        
    if not TradeContext.existVariable("TRCDAT"):
        return AfaFlowControl.ExitThisFlow('A099','û��ί������')
        
    AfaLoggerFunc.tradeInfo("<<<<<<У������ĺϷ��Խ���")
    
    #=====����RBSQ,FEDT,BJEDTE,NCCworkDate,BSPSQN====
    TradeContext.FEDT=AfaUtilTools.GetHostDate( )      #FEDT
    
    TradeContext.BJEDTE=AfaUtilTools.GetHostDate( )    #BJEDTE 
    
    if not rccpsFunc.GetNCCDate( ) :                   #NCCworkDate
        raise AfaFlowControl.flowException( )
    
    if rccpsGetFunc.GetRBSQ(PL_BRSFLG_RCV) == -1 :     #RBSQ
        return AfaFlowControl.ExitThisFlow('S999','��������ǰ����ˮ��ʧ��,��������')
        
    if rccpsGetFunc.GetSerialno(PL_BRSFLG_RCV) == -1 : #BSPSQN
        raise AfaFlowControl.flowException( )
        
    #=====�ж�ԭҵ�������˻�������====
    AfaLoggerFunc.tradeInfo("<<<<<<�ж�ԭҵ���������ʾ")
    if(TradeContext.SNDBNKCO == '1340000008'):
        AfaLoggerFunc.tradeInfo("<<<<<<ԭҵ��Ϊ����")
        #=====��ѯԭҵ����Ϣ====
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        wtrbka_record_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
        if(wtrbka_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҵǼǲ�ʧ��')
        
        elif(len(wtrbka_record_dict) == 0):
            return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ�ҵǼǲ�Ϊ��')
            
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<��ѯԭҵ����Ϣ�ɹ�")
            
        #=====��ѯ���˵Ǽǲ�====
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
        if(tddzcz_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ�ʧ��')
        
        elif(len(tddzcz_record_dict) == 0):
            AfaLoggerFunc.tradeInfo("��ѯ���˵Ǽǲ����Ϊ��,Ӧ�����в�����Ӧ�ļ�¼")
            #=====��������˵Ǽǲ����ֵ丳ֵ====
            insert_dict = {}           
            insert_dict['NCCWKDAT']   = wtrbka_record_dict['NCCWKDAT']
            insert_dict['SNDBNKCO']   = wtrbka_record_dict['SNDBNKCO']
            insert_dict['TRCDAT']     = wtrbka_record_dict['TRCDAT']
            insert_dict['TRCNO']      = wtrbka_record_dict['TRCNO']
            insert_dict['RCVBNKCO']   = wtrbka_record_dict['RCVBNKCO']
            insert_dict['SNDMBRCO']   = wtrbka_record_dict['SNDMBRCO']
            insert_dict['RCVMBRCO']   = wtrbka_record_dict['RCVMBRCO']
            insert_dict['TRCCO']      = wtrbka_record_dict['TRCCO']
            if(wtrbka_record_dict['DCFLG'] == '0'):
                insert_dict['DCFLG'] = '1'
            else:
                insert_dict['DCFLG'] = '2'
            insert_dict['PYRACC']     = wtrbka_record_dict['PYRACC']
            insert_dict['PYEACC']     = wtrbka_record_dict['PYEACC']
            insert_dict['CUR']        = 'CNY'
            insert_dict['OCCAMT']     = wtrbka_record_dict['OCCAMT']
            insert_dict['LOCOCCAMT']  = wtrbka_record_dict['OCCAMT']
            if(wtrbka_record_dict['TRCCO'] in ('3000102','3000103','3000104','3000105') and wtrbka_record_dict['CHRGTYP'] == '1'):
                insert_dict['CUSCHRG']    = wtrbka_record_dict['CUSCHRG']
                insert_dict['LOCCUSCHRG'] = wtrbka_record_dict['CUSCHRG']
            else:
                insert_dict['CUSCHRG']    = 0.00
                insert_dict['LOCCUSCHRG'] = 0.00
            insert_dict['ORTRCNO']    = ""
            insert_dict['BJEDTE']     = wtrbka_record_dict['BJEDTE']
            insert_dict['BSPSQN']     = wtrbka_record_dict['BSPSQN']
            insert_dict['EACTYP']     = '02'
            insert_dict['EACINF']     = '�����г�Ա����'
            insert_dict['LOCEACTYP']  = '03'
            insert_dict['LOCEACINF']  = '�����������㣬����δ����'
            insert_dict['ISDEAL']     = '0'
            insert_dict['NOTE1']      = ""
            insert_dict['NOTE2']      = ""
            insert_dict['NOTE3']      = ""
            insert_dict['NOTE4']      = ""
            
            #=====����˵Ǽǲ��в��Ǵ˱ʽ���====
            if not rccpsDBTrcc_tddzcz.insertCmt(insert_dict):
                return AfaFlowControl.ExitThisFlow('A099','����˵Ǽǲ��в��ǽ���ʧ��')
                
            #=====������˵Ǽǲ������ղ�������ݲ����====
            where_dict = {}
            where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
            tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
            if(tddzcz_record_dict == None):
                return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ�ʧ��')
            elif(len(tddzcz_record_dict) == 0):
                return AfaFlowControl.ExitThisFlow('A099','��ѯͨ���˵Ǽǲ����Ϊ��')
            else:
                AfaLoggerFunc.tradeInfo("<<<<<<������˵Ǽǲ��ɹ�")
                 
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<��ѯ���˵Ǽǲ��ɹ�")
                
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<ԭҵ��Ϊ����")
        #=====��ѯ������ϸ�Ǽǲ�====
        AfaLoggerFunc.tradeInfo("<<<<<<��ʼ��ѯ������ϸ�Ǽǲ�")
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        tddzmx_record_dict = rccpsDBTrcc_tddzmx.selectu(where_dict)
        if(tddzmx_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯ������ϸ�Ǽǲ�ʧ��')
            
        elif(len(tddzmx_record_dict) == 0):
            return AfaFlowControl.ExitThisFlow('A099','��ѯ������ϸ�Ǽǲ�Ϊ��')
            
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<��ѯ������ϸ�Ǽǲ��ɹ�")
        
        #=====��ѯ���˵Ǽǲ�====
        AfaLoggerFunc.tradeInfo("<<<<<<��ʼ��ѯ���˵Ǽǲ�")
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
        if(tddzcz_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ�ʧ��')
        
        elif(len(tddzcz_record_dict) == 0):
            AfaLoggerFunc.tradeInfo("��ѯ���˵Ǽǲ����Ϊ��,Ӧ�����в�����Ӧ�ļ�¼")
            #=====��������˵Ǽǲ����ֵ丳ֵ====
            insert_dict = {}
            insert_dict['NCCWKDAT']   = tddzmx_record_dict['NCCWKDAT']
            insert_dict['SNDBNKCO']   = tddzmx_record_dict['SNDBNKCO']
            insert_dict['TRCDAT']     = tddzmx_record_dict['TRCDAT']
            insert_dict['TRCNO']      = tddzmx_record_dict['TRCNO']
            insert_dict['RCVBNKCO']   = tddzmx_record_dict['RCVBNKCO']
            insert_dict['SNDMBRCO']   = tddzmx_record_dict['SNDMBRCO']
            insert_dict['RCVMBRCO']   = tddzmx_record_dict['RCVMBRCO']
            insert_dict['TRCCO']      = tddzmx_record_dict['TRCCO']
            insert_dict['DCFLG']      = tddzmx_record_dict['DCFLG']
            insert_dict['PYRACC']     = tddzmx_record_dict['PYRACC']
            insert_dict['PYEACC']     = tddzmx_record_dict['PYEACC']
            insert_dict['CUR']        = tddzmx_record_dict['CUR']
            insert_dict['OCCAMT']     = tddzmx_record_dict['OCCAMT']
            insert_dict['LOCOCCAMT']  = tddzmx_record_dict['OCCAMT']
            insert_dict['CUSCHRG']    = tddzmx_record_dict['CUSCHRG']
            insert_dict['LOCCUSCHRG'] = tddzmx_record_dict['CUSCHRG']
            insert_dict['ORTRCNO']    = ""
            insert_dict['BJEDTE']     = tddzmx_record_dict['BJEDTE']
            insert_dict['BSPSQN']     = tddzmx_record_dict['BSPSQN']
            insert_dict['EACTYP']     = "02"
            insert_dict['EACINF']     = "�����г�Ա����"
            insert_dict['LOCEACTYP']  = "08"
            insert_dict['LOCEACINF']  = "�����������㣬����δ����"
            insert_dict['ISDEAL']     = "0"
            insert_dict['NOTE1']      = ""
            insert_dict['NOTE2']      = ""
            insert_dict['NOTE3']      = ""
            insert_dict['NOTE4']      = ""
            
            #=====����˵Ǽǲ��в��Ǵ˱ʽ���====
            if not rccpsDBTrcc_tddzcz.insertCmt(insert_dict):
                return AfaFlowControl.ExitThisFlow('A099','����˵Ǽǲ��в��ǽ���ʧ��')
                
            #=====������˵Ǽǲ������ղ�������ݲ����====
            where_dict = {}
            where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
            tddzcz_record_dict = rccpsDBTrcc_tddzcz.selectu(where_dict)
            if(tddzcz_record_dict == None):
                return AfaFlowControl.ExitThisFlow('A099','��ѯ���˵Ǽǲ�ʧ��')
            elif(len(tddzcz_record_dict) == 0):
                return AfaFlowControl.ExitThisFlow('A099','��ѯͨ���˵Ǽǲ����Ϊ��')
            else:
                AfaLoggerFunc.tradeInfo("<<<<<<������˵Ǽǲ��ɹ�")
             
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<��ѯ���˵Ǽǲ��ɹ�")
             
        AfaLoggerFunc.tradeInfo("<<<<<<������ѯ������ϸ�Ǽǲ�")
        
        #=====��ѯԭ������Ϣ====
        AfaLoggerFunc.tradeInfo("<<<<<<��ʼ��ѯԭ������Ϣ")
        where_dict = {}
        where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
        wtrbka_record_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
        if(wtrbka_record_dict == None):
            return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ��ҵ��Ǽǲ�ʧ��')
        
        elif(len(wtrbka_record_dict) == 0):    #ͨ��ͨ�ҵǼǲ����Ϊ�գ�Ӧ�����в�����Ӧ��¼
            AfaLoggerFunc.tradeInfo("<<<<<<ͨ��ͨ��ҵ��Ǽǲ����Ϊ��")
            #=====��ʼ�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�====
            AfaLoggerFunc.tradeInfo("<<<<<<��ʼ�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
            
            #=====�����������׵õ�������====
            AfaLoggerFunc.tradeInfo("<<<<<<��ѯ�˻���������")
            TradeContext.HostCode = '8810'
            if(tddzmx_record_dict['TRCCO'] in ('3000002','3000003','3000004','3000005')):
                TradeContext.ACCNO = tddzmx_record_dict['PYEACC']
            else:
                TradeContext.ACCNO = tddzmx_record_dict['PYRACC']
            
            rccpsHostFunc.CommHost( TradeContext.HostCode )
            if(TradeContext.errorCode != '0000'):
                return AfaFlowControl.ExitThisFlow('A099','��ѯ�˻���������Ϣʧ��')
            
            AfaLoggerFunc.tradeInfo("<<<<<<��ѯ�˻�������Ϣ�ɹ�")
            
            #=====������ͨ��ͨ��ҵ��Ǽǲ����ֵ丳ֵ====
            insert_dict = {}
            insert_dict['BJEDTE']     = tddzmx_record_dict['BJEDTE']
            insert_dict['BSPSQN']     = tddzmx_record_dict['BSPSQN']
            if(tddzmx_record_dict['SNDMBRCO'] == '1340000008'):
                insert_dict['BRSFLG'] = PL_BRSFLG_SND
            else:
                insert_dict['BRSFLG'] = PL_BRSFLG_RCV
            insert_dict['BESBNO']     = TradeContext.ACCSO
            insert_dict['BEACSB']     = ""
            insert_dict['BETELR']     = PL_BETELR_AUTO
            insert_dict['BEAUUS']     = ""
            insert_dict['BEAUPS']     = ""
            insert_dict['TERMID']     = ""
            insert_dict['BBSSRC']     = ""
            insert_dict['DASQ']       = ""
            insert_dict['DCFLG']      = tddzmx_record_dict['DCFLG']
            if(tddzmx_record_dict['TRCCO'] in ('3000002','3000004')):
                insert_dict['OPRNO']  = PL_TDOPRNO_TC
            elif(tddzmx_record_dict['TRCCO'] in ('3000102','3000104')):
                insert_dict['OPRNO']  = PL_TDOPRNO_TD
            elif(tddzmx_record_dict['TRCCO'] in ('3000003','3000005')):
                insert_dict['OPRNO']  = PL_TDOPRNO_BZY
            else:
                insert_dict['OPRNO']  = PL_TDOPRNO_YZB
            insert_dict['OPRATTNO']   = ""
            insert_dict['NCCWKDAT']   = TradeContext.NCCworkDate
            insert_dict['TRCCO']      = tddzmx_record_dict['TRCCO']
            insert_dict['TRCDAT']     = tddzmx_record_dict['TRCDAT']
            insert_dict['TRCNO']      = tddzmx_record_dict['TRCNO']
            insert_dict['MSGFLGNO']   = tddzmx_record_dict['MSGFLGNO']
            insert_dict['COTRCDAT']   = ""
            insert_dict['COTRCNO']    = ""
            insert_dict['COMSGFLGNO'] = ""
            insert_dict['SNDMBRCO']   = tddzmx_record_dict['SNDMBRCO']
            insert_dict['RCVMBRCO']   = tddzmx_record_dict['RCVMBRCO']
            insert_dict['SNDBNKCO']   = tddzmx_record_dict['SNDBNKCO']
            insert_dict['SNDBNKNM']   = tddzmx_record_dict['SNDBNKNM']
            insert_dict['RCVBNKCO']   = tddzmx_record_dict['RCVBNKCO']
            insert_dict['RCVBNKNM']   = tddzmx_record_dict['RCVBNKNM']
            insert_dict['CUR']        = tddzmx_record_dict['CUR']
            insert_dict['OCCAMT']     = tddzmx_record_dict['OCCAMT']
            if(tddzmx_record_dict['CUSCHRG'] == 0.00):
                insert_dict['CHRGTYP']= PL_CHRG_CASH
            else:
                insert_dict['CHRGTYP']= PL_CHRG_TYPE  
            insert_dict['LOCCUSCHRG'] = ""
            insert_dict['CUSCHRG']    = tddzmx_record_dict['CUSCHRG']
            insert_dict['PYRTYP']     = ""
            insert_dict['PYRACC']     = tddzmx_record_dict['PYRACC']
            insert_dict['PYRNAM']     = ""
            insert_dict['PYRADDR']    = ""
            insert_dict['PYETYP']     = ""
            insert_dict['PYEACC']     = tddzmx_record_dict['PYEACC']
            insert_dict['PYENAM']     = ""
            insert_dict['PYEADDR']    = ""
            insert_dict['STRINFO']    = tddzmx_record_dict['STRINFO']
            insert_dict['CERTTYPE']   = ""
            insert_dict['CERTNO']     = ""
            insert_dict['BNKBKNO']    = ""
            insert_dict['BNKBKBAL']   = ""
            
            if not rccpsDBTrcc_wtrbka.insertCmt(insert_dict):
                return AfaFlowControl.ExitThisFlow('A099','�Ǽ�ͨ��ͨ��ҵ��Ǽǲ�ʧ��')
            
            AfaLoggerFunc.tradeInfo("<<<<<<�����Ǽ�ͨ��ͨ��ҵ��Ǽǲ�")
            
            #=====����ͨ��ͨ��ҵ��Ǽǲ������ղŲ�������ݲ����====
            where_dict = {}
            where_dict = {'SNDBNKCO':TradeContext.SNDBNKCO,'TRCDAT':TradeContext.TRCDAT,'TRCNO':TradeContext.TRCNO}
            wtrbka_record_dict = rccpsDBTrcc_wtrbka.selectu(where_dict)
            if(wtrbka_record_dict == None):
                return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ��ҵ��Ǽǲ�ʧ��')
            elif(len(wtrbka_record_dict) == 0):
                return AfaFlowControl.ExitThisFlow('A099','��ѯͨ��ͨ��ҵ��Ǽǲ����Ϊ��')
            else:
                AfaLoggerFunc.tradeInfo("<<<<<<����ͨ��ͨ��ҵ��Ǽǲ��ɹ�")
            
        else:
            AfaLoggerFunc.tradeInfo("<<<<<<��ѯͨ��ͨ��ҵ��Ǽǲ��ɹ�")
        
    #=====�жϴ˱�ҵ���Ƿ��Ѿ�����====
    if(tddzcz_record_dict['ISDEAL'] == PL_ISDEAL_ISDO):
        return AfaFlowControl.ExitThisFlow('A099','�˱������Ѿ������')
        
    #=====��ʼ���ڲ���====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ���ڲ���")
    #=====�ж�ԭ���׵�������ʾ====
    AfaLoggerFunc.tradeInfo("<<<<<<�ж�ԭ���׵�������ʾ")
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_RCV):
        AfaLoggerFunc.tradeInfo("<<<<<<ԭ����Ϊ����")
        
#        if(TradeContext.existVariable("BSPSQN")):
#            TradeContext.BSPSQN = wtrbka_record_dict['BSPSQN']    
        TradeContext.BESBNO   = wtrbka_record_dict['BESBNO']
        TradeContext.BRSFLG   = wtrbka_record_dict['BRSFLG']
        TradeContext.CHRGTYP  = wtrbka_record_dict['CHRGTYP']
        TradeContext.BETELR   = PL_BETELR_AUTO
        input_dict = {}
        input_dict['FEDT']    = TradeContext.FEDT
        input_dict['RBSQ']    = TradeContext.RBSQ
        input_dict['PYRACC']  = wtrbka_record_dict['PYRACC']
        input_dict['PYRNAM']  = wtrbka_record_dict['PYRNAM']
        input_dict['PYEACC']  = wtrbka_record_dict['PYEACC']
        input_dict['PYENAM']  = wtrbka_record_dict['PYENAM']
        input_dict['CHRGTYP'] = wtrbka_record_dict['CHRGTYP']
        input_dict['OCCAMT']  = wtrbka_record_dict['OCCAMT']
        input_dict['CUSCHRG'] = wtrbka_record_dict['CUSCHRG']
        
        if(wtrbka_record_dict['TRCCO'] in ('3000002','3000004')):  
            AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ�����˼���")
            input_dict['RCCSMCD'] = PL_RCCSMCD_XJTCLZ
            rccpsEntriesErr.KZTCLZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000003','3000005')):
            AfaLoggerFunc.tradeDebug("<<<<<<���۱�ת�����˼���")
            input_dict['RCCSMCD'] = PL_RCCSMCD_BZYLZ
            rccpsEntriesErr.KZBZYLZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000102','3000104')):
            AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ�����˼���")
            input_dict['RCCSMCD'] = PL_RCCSMCD_XJTDLZ
            rccpsEntriesErr.KZTDLZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000103','3000105')):
            AfaLoggerFunc.tradeDebug("<<<<<<������ת�����˼���")
            input_dict['RCCSMCD'] = PL_RCCSMCD_YZBLZ
            rccpsEntriesErr.KZYZBLZJZ(input_dict)
            
        else:
            return AfaFlowControl.ExitThisFlow('A099','���״���Ƿ�')
    
    elif(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):
        AfaLoggerFunc.tradeInfo("<<<<<<ԭ����Ϊ����")
         
#        if(TradeContext.existVariable("BSPSQN")):
#            TradeContext.BSPSQN = wtrbka_record_dict['BSPSQN']
        TradeContext.BESBNO   = wtrbka_record_dict['BESBNO']   
        TradeContext.CHRGTYP  = wtrbka_record_dict['CHRGTYP']
        TradeContext.BRSFLG   = wtrbka_record_dict['BRSFLG']    
        TradeContext.BETELR   = PL_BETELR_AUTO
        input_dict = {}
        input_dict['FEDT']    = TradeContext.FEDT
        input_dict['RBSQ']    = TradeContext.RBSQ
        input_dict['PYRACC']  = wtrbka_record_dict['PYRACC']
        input_dict['PYRNAM']  = wtrbka_record_dict['PYRNAM']
        input_dict['PYEACC']  = wtrbka_record_dict['PYEACC']
        input_dict['PYENAM']  = wtrbka_record_dict['PYENAM']
        input_dict['CHRGTYP'] = wtrbka_record_dict['CHRGTYP']
        input_dict['OCCAMT']  = wtrbka_record_dict['OCCAMT']
        input_dict['CUSCHRG'] = wtrbka_record_dict['CUSCHRG']
        
        if(wtrbka_record_dict['TRCCO'] in ('3000002','3000004')):  
            AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ�����˼���")
            input_dict['RCCSMCD'] = PL_RCCSMCD_XJTCWZ
            rccpsEntriesErr.KZTCWZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000003','3000005')):
            AfaLoggerFunc.tradeDebug("<<<<<<���۱�ת�����˼���")
            input_dict['RCCSMCD'] = PL_RCCSMCD_BZYWZ
            rccpsEntriesErr.KZBZYWZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000102','3000104')):
            AfaLoggerFunc.tradeDebug("<<<<<<�����ֽ�ͨ�����˼���")
            input_dict['RCCSMCD'] = PL_RCCSMCD_XJTDWZ
            rccpsEntriesErr.KZTDWZJZ(input_dict)
            
        elif(wtrbka_record_dict['TRCCO'] in ('3000103','3000105')):
            AfaLoggerFunc.tradeDebug("<<<<<<������ת�����˼���")
            input_dict['RCCSMCD'] = PL_RCCSMCD_YZBWZ
            rccpsEntriesErr.KZYZBWZJZ(input_dict)
        
        else:
            return AfaFlowControl.ExitThisFlow('A099','���״���Ƿ�')
        
    else:
        return AfaFlowControl.ExitThisFlow('A099','������ʾ�Ƿ�')
        
    #=====����ǰ����ԭ���׵�״̬====
    bcstat = ''    #״̬����
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):    #����
        bcstat = PL_BCSTAT_ACC
    elif(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_RCV and wtrbka_record_dict['TRCCO'] in ('3000002','3000003','3000004','3000005')):    #����ͨ��
        bcstat = PL_BCSTAT_AUTO
    else:    #����ͨ��
        bcstat = PL_BCSTAT_AUTOPAY
    
    #=====�ж�ԭ�����Ƿ��гɹ�������״̬====
    AfaLoggerFunc.tradeInfo("<<<<<<�ж�ԭ�������Ƿ��гɹ��Ľ���״̬")
    isaccount = 0    #�����������ױ�ʾ��0�����ã�1����
    acc = 0    
    hcac = 0    
    canc = 0
    cancel = 0
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):
        #=====ԭҵ��Ϊ����====
        #=====��ѯ�Ƿ��м��˳ɹ���״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_ACC,PL_BDWFLG_SUCC,sstlog_list):
            acc = len(sstlog_list)
        #=====��ѯ�Ƿ���Ĩ�˵�״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_HCAC,PL_BDWFLG_SUCC,sstlog_list):
            hcac = len(sstlog_list)
        #=====��ѯ�Ƿ��г�����״̬====
        sstlog_list = []
        if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_CANC,PL_BDWFLG_SUCC,sstlog_list):
            canc = len(sstlog_list)
        #=====��ѯ�Ƿ��г�����״̬====
        ssltog_list = []
        if rccpsState.getTransStateSetm(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_CANCEL,PL_BDWFLG_SUCC,sstlog_list):
            cancel = len(sstlog_list)
        
        if(acc - (hcac + canc + cancel) <= 0):
            isaccount = 1
            
    else:
        #======ԭҵ��Ϊ����====
        stat_dict = {}
        res = rccpsState.getTransStateCur(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],stat_dict)
        if(res == False):
            return AfaFlowControl.ExitThisFlow('A099','��ѯҵ��ĵ�ǰ״̬ʧ��')
        else:
            AfaLoggerFunc.tradeInfo("��ѯҵ��ǰ״̬�ɹ�")
            
        if(stat_dict['BCSTAT'] in (PL_BCSTAT_AUTO,PL_BCSTAT_AUTOPAY) and stat_dict['BDWFLG'] == PL_BDWFLG_SUCC):
            isaccount = 0
        else:
            isaccount = 1
            
    AfaLoggerFunc.tradeInfo("<<<<<<�����ж�ԭ�������Ƿ��гɹ��Ľ���״̬")
            
    #=====�ж�ҵ���Ƿ���Ҫ������������====
    if(isaccount == 0):
        return AfaFlowControl.ExitThisFlow('S999','ԭҵ���Ѽ��ˣ���ֹ�ύ')
    
    #=====����ǰ����ԭ����״̬====  
    AfaLoggerFunc.tradeInfo("<<<<<<����ǰ����ԭ����״̬")  
    if not rccpsState.newTransState(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],bcstat,PL_BDWFLG_WAIT):
        return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ���˴������쳣')
    else:
        AfaDBFunc.CommitSql()
        
    #=====��ʼ������������====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������������")
    rccpsHostFunc.CommHost( TradeContext.HostCode )
    AfaLoggerFunc.tradeInfo("<<<<<<����������������")   
        
    AfaLoggerFunc.tradeInfo("<<<<<<�������ڲ���")
    
    #=====��״̬�ֵ丳ֵ====
    state_dict = {}
    state_dict['BJEDTE'] = wtrbka_record_dict['BJEDTE']
    state_dict['BSPSQN'] = wtrbka_record_dict['BSPSQN']
    state_dict['BCSTAT'] = bcstat
    state_dict['MGID']   = TradeContext.errorCode
    if TradeContext.existVariable('TRDT'):
        state_dict['TRDT']   = TradeContext.TRDT
    if TradeContext.existVariable('TLSQ'):
        state_dict['TLSQ']   = TradeContext.TLSQ
    if TradeContext.existVariable('RBSQ'): 
        state_dict['RBSQ'] = TradeContext.RBSQ
    if TradeContext.existVariable('FEDT'):
        state_dict['FEDT'] = TradeContext.FEDT
    
    #=====�ж����������Ƿ�ɹ�====
    AfaLoggerFunc.tradeInfo("<<<<<<�ж����������Ƿ�ɹ�")
    AfaLoggerFunc.tradeDebug("<<<<<<errorCode=" + TradeContext.errorCode)
    if(TradeContext.errorCode != '0000'):
        AfaLoggerFunc.tradeInfo("������������ʧ��")
        #=====���������ԭ����״̬Ϊʧ��====
        state_dict['BDWFLG'] = PL_BDWFLG_FAIL
        state_dict['STRINFO'] = TradeContext.errorMsg
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊʧ���쳣')
        else:
            AfaDBFunc.CommitSql()
       
        return AfaFlowControl.ExitThisFlow('S999','��������ʧ��')
        
    else:
        AfaLoggerFunc.tradeInfo("�����������׳ɹ�")
        #=====���������ԭ����״̬Ϊ�ɹ�====
        state_dict['BDWFLG'] = PL_BDWFLG_SUCC
        state_dict['STRINFO'] = '�����ɹ�'
        if(TradeContext.existVariable("SBAC")):
            state_dict['SBAC'] = TradeContext.SBAC
        if(TradeContext.existVariable("RBAC")):
            state_dict['RBAC'] = TradeContext.RBAC
        if not rccpsState.setTransState(state_dict):
            return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊʧ�ܳɹ�')
        else:
            AfaDBFunc.CommitSql()
            
        #=====���������Ҫ��״̬����Ϊ����ɹ�====
        if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_SND):    #����
            if not rccpsState.newTransState(wtrbka_record_dict['BJEDTE'],wtrbka_record_dict['BSPSQN'],PL_BCSTAT_MFESTL,PL_BDWFLG_SUCC):
                return AfaFlowControl.ExitThisFlow('S999','����ҵ��״̬Ϊ����ɹ��쳣')
            else:
                AfaDBFunc.CommitSql()
        
    #=====���Ĵ��˵Ǽǲ��еĴ����ʾ====
    AfaLoggerFunc.tradeInfo("<<<<<<���Ĵ��˵Ǽǲ��еĴ����ʾ")
    where_dict = {}
    where_dict = {'BJEDTE':tddzcz_record_dict['BJEDTE'],'BSPSQN':tddzcz_record_dict['BSPSQN']}
    update_dict = {}
    update_dict['ISDEAL'] = PL_ISDEAL_ISDO
    update_dict['NOTE3']  = '�˱ʴ����Ѳ���'
    res = rccpsDBTrcc_tddzcz.updateCmt(update_dict,where_dict)
    if(res == -1):
        return AfaFlowControl.ExitThisFlow('S999','���������ѳɹ��������´����ʾʧ�ܣ����ֶ����Ĵ����ʾ')
        
    else:
        AfaLoggerFunc.tradeInfo("<<<<<<���Ĵ��˵Ǽǲ��еĴ����ʾ�ɹ�")

    #=====���·���֪ͨ���в�������====
    AfaLoggerFunc.tradeInfo("<<<<<<��֪ͨ���в�������")
    insert_dict = {}
    insert_dict['NOTDAT']  = TradeContext.BJEDTE
    insert_dict['BESBNO']  = wtrbka_record_dict['BESBNO']
    if(wtrbka_record_dict['BRSFLG'] == PL_BRSFLG_RCV):
        insert_dict['STRINFO'] = "�˱ʴ���["+wtrbka_record_dict['BSPSQN']+"]["+wtrbka_record_dict['BJEDTE']+"]�������Ǵ���"
    else:
        insert_dict['STRINFO'] = "�˱ʴ���["+wtrbka_record_dict['BSPSQN']+"]["+wtrbka_record_dict['BJEDTE']+"]�������Ǵ��� ����8522��������ƾ֤"
    if not rccpsDBTrcc_notbka.insertCmt(insert_dict):
        return AfaFlowControl.ExitThisFlow('S999','���·���֪ͨ���в�������ʧ��')
    AfaLoggerFunc.tradeInfo("<<<<<<��֪ͨ���в������ݳɹ�")
    
    
    #=====������ӿڸ�ֵ====
    AfaLoggerFunc.tradeInfo("<<<<<<��ʼ������ӿڸ�ֵ")
    TradeContext.BOSPSQ     = wtrbka_record_dict['BSPSQN']
    TradeContext.BOJEDT     = wtrbka_record_dict['BJEDTE']
    TradeContext.TLSQ       = TradeContext.TLSQ
    TradeContext.TRCCO      = wtrbka_record_dict['TRCCO']
    TradeContext.BRSFLG     = wtrbka_record_dict['BRSFLG']
    TradeContext.BEACSB     = wtrbka_record_dict['BESBNO']
    TradeContext.OROCCAMT   = str(wtrbka_record_dict['OCCAMT'])
    TradeContext.ORCUR      = wtrbka_record_dict['CUR']
    TradeContext.ORSNDBNK   = wtrbka_record_dict['SNDBNKCO']
    TradeContext.ORSNDBNKNM = wtrbka_record_dict['SNDBNKNM']
    TradeContext.ORRCVBNK   = wtrbka_record_dict['RCVBNKCO']
    TradeContext.ORRCVBNKNM = wtrbka_record_dict['RCVBNKNM']
    TradeContext.ORPYRACC   = wtrbka_record_dict['PYRACC']
    TradeContext.ORPYRNAM   = wtrbka_record_dict['PYRNAM']
    TradeContext.ORPYEACC   = wtrbka_record_dict['PYEACC']
    TradeContext.ORPYENAM   = wtrbka_record_dict['PYENAM']
#    TradeContext.SBAC       = 
#    TradeContext.RBAC       = 
    
    AfaLoggerFunc.tradeInfo("<<<<<<����������ӿڸ�ֵ")
    
    AfaLoggerFunc.tradeInfo("<<<<<<<���Ի�����(���ز���) �˳�")
    
    AfaLoggerFunc.tradeInfo("'***ũ����ϵͳ��ͨ��ͨ�����˽���.����˲���[8572] �˳�")
    
    return True
