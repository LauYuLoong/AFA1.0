# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��Ʊҵ����ͳ��
#===============================================================================
#   �����ļ�:   rccpsHPProStat.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-07-03
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,AfaDBFunc,rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊҵ����ͳ��[rccpsHPProStat]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE4'].replace(",","','") + "')"
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #==================��Ʊ����ͳ��=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��Ʊ����ҵ����ͳ��")
        
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_SND + "',b.btopsb,b.beacsb,count(a.occamt),sum(a.occamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hpdzmx a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��Ʊ����ҵ����ͳ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������Ʊ����ҵ����ͳ��")
        
        #==================��Ʊ����ͳ��=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��Ʊ����ҵ����ͳ��")
        
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,case when b.besbno is null then '3400008889' else b.besbno end,a.trcco,'" + PL_BRSFLG_RCV + "',case when b.btopsb is null then '3400008889' else b.btopsb end,case when b.beacsb is null then '3400008889' else b.beacsb end,count(a.occamt),sum(a.occamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hpdzmx a left join rcc_subbra b on a.rcvbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.rcvmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��Ʊ����ҵ����ͳ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������Ʊ����ҵ����ͳ��")
        
        #================�رջ�Ʊҵ����ͳ��ϵͳ����===========
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ʊҵ����ͳ��ϵͳ����")
        if not rccpsCronFunc.closeCron("00046"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�رջ�Ʊҵ����ͳ�Ƶ����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ʊҵ����ͳ��ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊҵ����ͳ��[rccpsHPProStat]�˳�***")
    
    except Exception, e:
        #�����쳣

        if not AfaDBFunc.RollbackSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo(">>>Rollback�쳣")
        AfaLoggerFunc.tradeInfo(">>>Rollback�ɹ�")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = 'ϵͳ����['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            AfaLoggerFunc.tradeInfo( 'errorCode=['+TradeContext.errorCode+']' )
            AfaLoggerFunc.tradeInfo( 'errorMsg=['+TradeContext.errorMsg+']' )
            AfaLoggerFunc.tradeInfo('***[rccpsHPProStat]�����ж�***')

        sys.exit(-1)
