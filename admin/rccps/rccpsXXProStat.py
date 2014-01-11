# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��ѯ�鸴ҵ������Ϣͳ��
#===============================================================================
#   �����ļ�:   rccpsXXProStat.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �˹�ͨ
#   �޸�ʱ��:   2008-12-06
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc,AfaDBFunc,rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��ѯ�鸴ҵ������Ϣͳ��[rccpsXXProStat]����***")
        
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
        
        #==================��ѯ�鸴����ͳ��=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯ�鸴����ҵ����ͳ��")
        #=====��Ҳ�ѯ�鸴����====
        AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҳ�ѯ�鸴����ҵ����ͳ��")
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_SND + "',b.btopsb,b.beacsb,count(a.occamt),sum(a.occamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hdcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�鸴����ҵ����ͳ���쳣")
        AfaLoggerFunc.tradeInfo(">>>������Ҳ�ѯ�鸴����ҵ����ͳ��")
        
        #=====��Ʊ��ѯ�鸴����====
        AfaLoggerFunc.tradeInfo(">>>��ʼ��Ʊ��ѯ�鸴����ҵ����ͳ��")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_SND + "',b.btopsb,b.beacsb,count(a.bilamt),sum(a.bilamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hpcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�鸴����ҵ����ͳ���쳣")
        AfaLoggerFunc.tradeInfo(">>>������Ʊ��ѯ�鸴����ҵ����ͳ��")  
        
        #=====Ʊ�ݲ�ѯ�鸴����====
        AfaLoggerFunc.tradeInfo(">>>��ʼƱ�ݲ�ѯ�鸴����ҵ����ͳ��")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_SND + "',b.btopsb,b.beacsb,count(a.bilamt),sum(a.bilamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_pjcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�鸴����ҵ����ͳ���쳣")
        AfaLoggerFunc.tradeInfo(">>>����Ʊ�ݲ�ѯ�鸴����ҵ����ͳ��")    
        
        AfaLoggerFunc.tradeInfo(">>>������ѯ�鸴����ҵ����ͳ��")
        
        #==================��ѯ�鸴����ͳ��=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ѯ�鸴����ҵ����ͳ��")
        
        #=====��Ҳ�ѯ�鸴����====
        AfaLoggerFunc.tradeInfo(">>>��ʼ��Ҳ�ѯ�鸴����ҵ����ͳ��")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_RCV + "',b.btopsb,b.beacsb,count(a.occamt),sum(a.occamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hdcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�鸴����ҵ����ͳ���쳣")
        AfaLoggerFunc.tradeInfo(">>>������Ҳ�ѯ�鸴����ҵ����ͳ��")    
        
        #=====��Ʊ��ѯ�鸴����====
        AfaLoggerFunc.tradeInfo(">>>��ʼ��Ʊ��ѯ�鸴����ҵ����ͳ��")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_RCV + "',b.btopsb,b.beacsb,count(a.bilamt),sum(a.bilamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_hpcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�鸴����ҵ����ͳ���쳣")
        AfaLoggerFunc.tradeInfo(">>>������Ʊ��ѯ�鸴����ҵ����ͳ��")    
        
        #=====Ʊ�ݲ�ѯ�鸴����====
        AfaLoggerFunc.tradeInfo(">>>��ʼƱ�ݲ�ѯ�鸴����ҵ����ͳ��")    
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,b.besbno,a.trcco,'" + PL_BRSFLG_RCV + "',b.btopsb,b.beacsb,count(a.bilamt),sum(a.bilamt),'" + PL_ISDEAL_UNDO + "','','','','',''"
        tmp_sql = tmp_sql + " from rcc_pjcbka a left join rcc_subbra b on a.sndbnkco = b.bankbin"
        tmp_sql = tmp_sql + " where a.sndmbrco = '1340000008' and nccwkdat in " + LNCCWKDAT + " and a.prcco='RCCI0000'"
        tmp_sql = tmp_sql + " group by a.nccwkdat,b.besbno,a.trcco,b.btopsb,b.beacsb)"   
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��ѯ�鸴����ҵ����ͳ���쳣")
        AfaLoggerFunc.tradeInfo(">>>����Ʊ�ݲ�ѯ�鸴����ҵ����ͳ��")    
        
        AfaLoggerFunc.tradeInfo(">>>������ѯ�鸴����ҵ����ͳ��")
        
        #================�رղ�ѯ�鸴ҵ������Ϣͳ��ϵͳ����===========
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رղ�ѯ�鸴ҵ������Ϣͳ��ϵͳ����")
        if not rccpsCronFunc.closeCron("00067"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�رղ�ѯ�鸴ҵ������Ϣͳ�Ƶ����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رղ�ѯ�鸴ҵ������Ϣͳ��ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��ѯ�鸴ҵ������Ϣͳ��[rccpsXXProStat]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsXXProStat]�����ж�***')

        sys.exit(-1)
