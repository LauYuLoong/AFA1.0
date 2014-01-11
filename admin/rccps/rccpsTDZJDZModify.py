# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ͨ��ͨ�Ҷ��˴��˴���
#===============================================================================
#   �����ļ�:   rccpsTDZJDZModify.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-12-12
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc,time
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_tdzjcz

if __name__ == '__main__':
    
    try:
        rccpsCronFunc.WrtLog("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ��˴��˴���[rccpstdzjczModify]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
        
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #��ǰ������������,ǰ�ô��ڴ�״̬����ת�����ʶ�ǳɹ���,������ת�����ʶΪ�ɹ�,��������������,������ˮ��
        tdzjcz_where_sql = "nccwkdat in " + LNCCWKDAT + " and errtyp = '51' and isdeal = '" + PL_ISDEAL_UNDO + "'"
        tdzjcz_list = rccpsDBTrcc_tdzjcz.selectm(1,0,tdzjcz_where_sql,"")
        
        if tdzjcz_list == None:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�˴���������ؼ�¼�쳣")
            
        elif len(tdzjcz_list) <= 0:
            AfaLoggerFunc.tradeInfo("�޴˴���������ؼ�¼")
            
        else:
            AfaLoggerFunc.tradeInfo("������ת�����ʶΪ�ɹ�,��������������,������ˮ��")
            for i in xrange(len(tdzjcz_list)):
                AfaLoggerFunc.tradeInfo("��ʼ������ת�����ʶΪ�ɹ�")
                
                #========���½���״̬��ת�����ʶΪ�ɹ�========================
                #�ر�� 20090223  ���Ӽ��˳�ʱ,���ؾܾ�,��ʵ���������˳ɹ��Ĵ���
                
                where_sql = "select a.bjedte,a.bspsqn,a.bcstat,a.bdwflg from rcc_spbsta as a,rcc_sstlog as b,rcc_tdzjcz as c "
                where_sql = where_sql + " where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.bcursq = b.bcursq"
                where_sql = where_sql + " and ((b.bcstat in ('20','21','70','72','81','82') and b.bdwflg != '1') or (b.bcstat = '40'))"
                where_sql = where_sql + " and b.fedt = c.scfedt and b.rbsq = c.scrbsq"
                where_sql = where_sql + " and b.fedt = '" + tdzjcz_list[i]['SCFEDT'] + "' and b.rbsq = '" + tdzjcz_list[i]['SCRBSQ'] + "'"
                
                tmp_list = AfaDBFunc.SelectSql(where_sql)
                
                if tmp_list == None:
                    AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","��ѯ���Ը�����ת�����ʶ�Ľ��ױ������ںͱ�������쳣")
                
                elif len(tmp_list) <= 0:
                    AfaLoggerFunc.tradeInfo("�޿��Ը�����ת�����ʶ�Ľ���")
                    continue
                
                else:
                    stat_dict = {}
                    stat_dict['BJEDTE'] = tmp_list[0][0]
                    stat_dict['BSPSQN'] = tmp_list[0][1]
                    if tmp_list[0][2] == '40':
                        stat_dict['BCSTAT'] = '72'
                    else:
                        stat_dict['BCSTAT'] = tmp_list[0][2]
                    stat_dict['BDWFLG'] = PL_BDWFLG_SUCC
                    stat_dict['TRDT']   = tdzjcz_list[i]['SCTRDT']
                    stat_dict['TLSQ']   = tdzjcz_list[i]['SCTLSQ']
                    
                    if not rccpsState.setTransState(stat_dict):
                        rccpsCronFunc.cronExit('S999', '����״̬�쳣')
                
                AfaLoggerFunc.tradeInfo("����������ת�����ʶΪ�ɹ�")
                
                #========�޸Ĵ��˴����ʶΪ�Ѵ���==============================
                AfaLoggerFunc.tradeInfo("��ʼ�޸Ĵ��˴����ʶΪ�Ѵ���")
                
                tdzjcz_update_sql = "update rcc_tdzjcz set isdeal = '1'"
                tdzjcz_update_sql = tdzjcz_update_sql + " where errtyp = '51' and scfedt = '" + tdzjcz_list[i]['SCFEDT'] + "' and scrbsq = '" + tdzjcz_list[i]['SCRBSQ'] + "'"
                
                ret = AfaDBFunc.UpdateSqlCmt(tdzjcz_update_sql)
                
                if ret <= 0:
                    AfaLoggerFunc.tradeInfo("sqlErrMsg=" + AfaDBFunc.sqlErrMsg)
                    rccpsCronFunc.cronExit("S999","�޸Ĵ˴��˴����ʶ�쳣")
                    
                AfaLoggerFunc.tradeInfo("�����޸Ĵ��˴����ʶΪ�Ѵ���")
        
        #================�ر�ͨ��ͨ�Ҷ��˻�Ҷ��˴��˴���ϵͳ����,��ͨ��ͨ�Ҷ�����ϸ�˹���ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ�Ҷ��˻�Ҷ��˴��˴���ϵͳ����,��ͨ��ͨ�Ҷ�����ϸ�˹���ϵͳ����")
        if not rccpsCronFunc.closeCron("00071"):
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ�Ҷ��˴��˴���ϵͳ�����쳣")
        
        if not rccpsCronFunc.openCron("00063"):
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ�����ϸ�˹���ϵͳ�����쳣")
                
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ�Ҷ��˻�Ҷ��˴��˴���ϵͳ����,��ͨ��ͨ�Ҷ�����ϸ�˹���ϵͳ����")
        
        rccpsCronFunc.WrtLog("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ��˴��˴���[rccpstdzjczModify]�˳�***")
    
    except Exception, e:
        #�����쳣

        if not AfaDBFunc.RollbackSql( ):
            rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.WrtLog(">>>Rollback�쳣")
        rccpsCronFunc.WrtLog(">>>Rollback�ɹ�")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = 'ϵͳ����['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            rccpsCronFunc.WrtLog( 'errorCode=['+TradeContext.errorCode+']' )
            rccpsCronFunc.WrtLog( 'errorMsg=['+TradeContext.errorMsg+']' )
            rccpsCronFunc.WrtLog('***[rccpstdzjczModify]�����ж�***')

        sys.exit(-1)
