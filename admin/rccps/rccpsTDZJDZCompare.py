# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ͨ��ͨ��������ϸ�˹���
#===============================================================================
#   �����ļ�:   rccpsTDZJDZCompare.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-11-20
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc
import rccpsDBTrcc_mbrifa

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ��������ϸ�˹���[rccpsTDZJDZCompare]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT  = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"  #��Ҫ���˵���������(���������㹤���պ�֮ǰ�ķ����㹤����)
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #===================ǰ������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ǰ������")
        
        temp_sql = "insert into rcc_tdzjcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.scfedt,a.scrbsq,'','',a.sctram,0.00,a.sceydt,a.sctlsq,'51','ǰ������','0','','','',''"
        temp_sql = temp_sql + " from rcc_tdzjmx as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT  
        temp_sql = temp_sql + " and not exists ("  
        temp_sql = temp_sql + " select * from rcc_sstlog as b where b.fedt = a.scfedt and b.rbsq = a.scrbsq"  
        temp_sql = temp_sql + " and ((b.bcstat in ('20','70','72') and b.bdwflg = '1' and a.scrvsb = '')"  
        temp_sql = temp_sql + " or (b.bcstat in ('21','81','82') and b.bdwflg = '1' and a.scrvsb != ''))))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","����ǰ�������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ǰ������")
        
        #===================ǰ�ö���==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����ǰ�ö���")
        
        temp_sql = "insert into rcc_tdzjcz"
        temp_sql = temp_sql + " (select a.nccwkdat,'','',b.fedt,b.rbsq,0.00,a.occamt,b.trdt,b.tlsq,'52','ǰ�ö���','0','','','',''"
        temp_sql = temp_sql + " from rcc_wtrbka as a,rcc_sstlog as b"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and ("
        temp_sql = temp_sql + " (b.bcstat in ('20','70','72') and b.bdwflg = '1' and b.trdt != '' and b.tlsq != '' and not exists(select * from rcc_tdzjmx as c where b.fedt = c.scfedt and b.rbsq = c.scrbsq and c.scrvsb = ''))"
        temp_sql = temp_sql + " or (b.bcstat in ('21','81','82') and b.bdwflg = '1' and b.trdt != '' and b.tlsq != '' and not exists(select * from rcc_tdzjmx as c where b.fedt = c.scfedt and b.rbsq = c.scrbsq and c.scrvsb != ''))))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","����ǰ�ö����쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������ǰ�ö���")
        
        
#        #===================����==============================
#        AfaLoggerFunc.tradeInfo(">>>��ʼ���˽���")
#        
#        temp_sql = "insert into rcc_tdzjcz"
#        temp_sql = temp_sql + " (select a.nccwkdat,a.scfedt,a.scrbsq,b.fedt,b.rbsq,a.sctram,case a.scflag when '7' then c.occamt else c.cuschrg end,a.sceydt,a.sctlsq,'53','����','0','','','',''"
#        temp_sql = temp_sql + " from rcc_tdzjmx as a,rcc_sstlog as b,rcc_wtrbka c"            
#        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.scfedt = b.fedt and a.scrbsq = b.rbsq and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
#        temp_sql = temp_sql + " and ((b.bcstat in ('20','70','72') and b.bdwflg = '1' and a.scrvsb = '') or (b.bcstat in ('21','81','82') and b.bdwflg = '1' and a.scrvsb != ''))"
#        #20090512  �޸��жϽ���Ƿ���ȵķ�ʽ
#        #temp_sql = temp_sql + " and ((a.scflag = '7' and a.sctram != c.occamt) or (a.scflag = '8' and a.sctram != c.cuschrg)))"
#        temp_sql = temp_sql + " and ((a.scflag = '7' and abs(a.sctram - c.occamt) > 0.001) or (a.scflag = '8' and abs(a.sctram - c.cuschrg) > 0.001)))"
#        
#        AfaLoggerFunc.tradeInfo(temp_sql)
#        
#        ret = AfaDBFunc.InsertSql(temp_sql)
#        
#        if ret < 0:
#            rccpsCronFunc.cronExit("S999","���˽����쳣")
#        
#        AfaLoggerFunc.tradeInfo(">>>�������˽���")
        
        
        #================�ر�ͨ��ͨ��������ϸ�˹���ϵͳ����,��ͨ��ͨ���������˴���ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ��������ϸ�˹���ϵͳ����,��ͨ��ͨ���������˴���ϵͳ����")
        if not rccpsCronFunc.closeCron("00070"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ��������ϸ�˹���ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00071"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ���������˴���ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ��������ϸ�˹���ϵͳ����,��ͨ��ͨ���������˴���ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ��������ϸ�˹���[rccpsTDZJDZCompare]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDZJDZCompare]�����ж�***')

        sys.exit(-1)
