# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ͨ��ͨ��ҵ����ͳ��
#===============================================================================
#   �����ļ�:   rccpsTDProStat.py
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
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ��ҵ����ͳ��[rccpsTDProStat]����***")
        
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
        
        #==================ͨ��ͨ������ͳ��=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼͨ��ͨ������ҵ����ͳ��")
        
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,a.besbno,a.trcco,a.brsflg,'','',count(occamt),sum(occamt),'0','','','','',''"
        tmp_sql = tmp_sql + " from rcc_wtrbka as a,rcc_spbsta as b where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn"
        tmp_sql = tmp_sql + " and b.bcstat = '42' and b.bdwflg = '1' and a.brsflg = '" + PL_BRSFLG_SND + "' and a.nccwkdat in " + LNCCWKDAT
        tmp_sql = tmp_sql + " group by a.nccwkdat,a.besbno,a.trcco,a.brsflg)"
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","ͨ��ͨ������ҵ����ͳ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ͨ��ͨ������ҵ����ͳ��")
        
        #==================ͨ��ͨ������ͳ��=========================================
        AfaLoggerFunc.tradeInfo(">>>��ʼͨ��ͨ������ҵ����ͳ��")
        
        tmp_sql = ""
        tmp_sql = tmp_sql + " insert into rcc_trcsta("
        tmp_sql = tmp_sql + " select a.nccwkdat,a.besbno,a.trcco,a.brsflg,'','',count(occamt),sum(occamt),'0','','','','',''"
        tmp_sql = tmp_sql + " from rcc_wtrbka as a,rcc_spbsta as b where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn"
        tmp_sql = tmp_sql + " and b.bcstat in ('70','72') and b.bdwflg = '1' and a.brsflg = '" + PL_BRSFLG_RCV + "' and a.nccwkdat in " + LNCCWKDAT
        tmp_sql = tmp_sql + " group by a.nccwkdat,a.besbno,a.trcco,a.brsflg)"
        
        AfaLoggerFunc.tradeInfo(tmp_sql)
        
        ret = AfaDBFunc.InsertSql(tmp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","ͨ��ͨ������ҵ����ͳ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����ͨ��ͨ������ҵ����ͳ��")
        
        #================�ر�ͨ��ͨ��ҵ����ͳ��ϵͳ����===========
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ��ҵ����ͳ��ϵͳ����")
        if not rccpsCronFunc.closeCron("00066"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ��ҵ����ͳ�Ƶ����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ��ҵ����ͳ��ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ��ҵ����ͳ��[rccpsTDProStat]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDProStat]�����ж�***')

        sys.exit(-1)
