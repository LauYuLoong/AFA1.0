# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.ͨ��ͨ�Ҷ�����ϸ�˹���
#===============================================================================
#   �����ļ�:   rccpsTDDZMXCompare.py
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
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ�����ϸ�˹���[rccpsTDDZMXCompare]����***")
        
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
        
        #===================����,�����Ѽ�����δĨ��,������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,�����Ѽ�����δĨ��,������")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,case a.dcflg when '1' then '0' else '1' end,a.pyracc,a.pyeacc,'CNY',a.occamt,a.occamt,case when a.chrgtyp='1' and a.trcco in ('3000102','3000103','3000104','3000105') then a.cuschrg else 0.00 end case,case when a.chrgtyp='1' and a.trcco in ('3000102','3000103','3000104','3000105') then a.cuschrg else 0.00 end case,'',a.bjedte,a.bspsqn,'01','�����޳�Ա����','01','����,�����Ѽ�����δĨ��,������','0','','','',''"
        temp_sql = temp_sql + " from rcc_wtrbka as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.brsflg = '0'"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select * from rcc_tddzmx as b"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno)"
        temp_sql = temp_sql + " and exists"
        temp_sql = temp_sql + " (select * "
        temp_sql = temp_sql + " from rcc_sstlog as c"
        temp_sql = temp_sql + " where a.bjedte = c.bjedte and a.bspsqn = c.bspsqn and c.bcstat = '20' and c.bdwflg = '1')"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select *"
        temp_sql = temp_sql + " from rcc_sstlog as d"
        temp_sql = temp_sql + " where a.bjedte = d.bjedte and a.bspsqn = d.bspsqn and d.bcstat in ('21','81','82') and d.bdwflg = '1'))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,�����Ѽ�����δĨ��,�������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,�����Ѽ�����δĨ��,������")
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #===================����,������,������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,������,������")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,a.occamt,a.cuschrg,a.cuschrg,a.ortrcno,'','','02','�����г�Ա����','02','����,������,������','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.sndmbrco = '1340000008' and not exists" 
        temp_sql = temp_sql + " (select * from rcc_wtrbka as b"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,������,�������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,������,������")
        
        #===================����,��������,����δ����==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,��������,����δ����")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'02','�����г�Ա����','03','������������,����δ����','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.sndmbrco = '1340000008' and (c.bcstat != '42' or c.bdwflg != '1')"
        temp_sql = temp_sql + " and ((a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '1') or (a.trcco in ('3000102','3000103','3000104','3000105') and a.confflg = '0')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,��������,����δ�����쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,��������,����δ����")
        
        #===================����,���ĳ���,����δ����==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,���ĳ���,����δ����")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'01','�����޳�Ա����','04','�������ĳ���,����δ����','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '1' and a.sndmbrco = '1340000008' and not (c.bcstat = '81' and c.bdwflg = '1')"
        temp_sql = temp_sql + " and ((a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '1') or (a.trcco in ('3000102','3000103','3000104','3000105') and a.confflg = '0')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,���ĳ���,����δ�����쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,���ĳ���,����δ����")
        
        
        #===================����,ͨ��ҵ��,�����Ѽ�����δĨ��,����δȷ��==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,ͨ��ҵ��,�����Ѽ�����δĨ��,����δȷ��")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'03','��ȷ��','05','����,ͨ��,�����Ѽ�����δĨ��,����δȷ��','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.sndmbrco = '1340000008'"
        temp_sql = temp_sql + " and a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '0'"

        ##########################################################################
        #guanbj 20091012 ��ȷ�ϴ���ֻ����������δĨ�˵Ľ���
        temp_sql = temp_sql + " and exists"
        temp_sql = temp_sql + " (select * "
        temp_sql = temp_sql + " from rcc_sstlog as d"
        temp_sql = temp_sql + " where c.bjedte = d.bjedte and c.bspsqn = d.bspsqn and d.bcstat = '20' and d.bdwflg = '1')"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select *"
        temp_sql = temp_sql + " from rcc_sstlog as e"
        temp_sql = temp_sql + " where c.bjedte = e.bjedte and c.bspsqn = e.bspsqn and e.bcstat in ('21','81','82') and e.bdwflg = '1'))"
        ##########################################################################
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,ͨ��ҵ��,�����Ѽ�����δĨ��,����δȷ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������,ͨ��ҵ��,�����Ѽ�����δĨ��,����δȷ��")
        
        #===================����,ͨ��,����δ����,�����е�δȷ��=========================
        #�ر�� 20091014 ������δȷ��,����δ���˵Ĵ��˹�Ϊ�����������޴�������
        AfaLoggerFunc.tradeInfo(">>>��ʼ����,ͨ��,����δ����,�����е�δȷ��")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'02','�����г�Ա����','11','����,ͨ��,����δ����,�����е�δȷ��','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.sndmbrco = '1340000008'"
        temp_sql = temp_sql + " and a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '0'"
        temp_sql = temp_sql + " and not (exists"
        temp_sql = temp_sql + " (select * "
        temp_sql = temp_sql + " from rcc_sstlog as d"
        temp_sql = temp_sql + " where c.bjedte = d.bjedte and c.bspsqn = d.bspsqn and d.bcstat = '20' and d.bdwflg = '1')"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select *"
        temp_sql = temp_sql + " from rcc_sstlog as e"
        temp_sql = temp_sql + " where c.bjedte = e.bjedte and c.bspsqn = e.bspsqn and e.bcstat in ('21','81','82') and e.bdwflg = '1')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,ͨ��ҵ��,����δ����,�����е�δȷ��")
        
        AfaLoggerFunc.tradeInfo(">>>��������,ͨ��,����δ����,�����е�δȷ��")
        
        #===================����,�����Ѽ�����δĨ��,������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,�����Ѽ�����δĨ��,������")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,case a.dcflg when '1' then '0' else '1' end,a.pyracc,a.pyeacc,'CNY',a.occamt,a.occamt,case when a.chrgtyp='1'and a.trcco in ('3000102','3000103','3000104','3000105') then a.cuschrg else 0.00 end case,case when a.chrgtyp='1'and a.trcco in ('3000102','3000103','3000104','3000105') then a.cuschrg else 0.00 end case,'',a.bjedte,a.bspsqn,'01','�����޳�Ա����','06','����,�����Ѽ�����δĨ��,������','0','','','',''"
        temp_sql = temp_sql + " from rcc_wtrbka as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.brsflg = '1'"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select * from rcc_tddzmx as b"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno)"
        temp_sql = temp_sql + " and exists"
        temp_sql = temp_sql + " (select * from rcc_sstlog as c"
        temp_sql = temp_sql + " where a.bjedte = c.bjedte and a.bspsqn = c.bspsqn and c.bcstat in ('70','72') and c.bdwflg = '1')"
        temp_sql = temp_sql + " and not exists"
        temp_sql = temp_sql + " (select * from rcc_sstlog as d"
        temp_sql = temp_sql + " where a.bjedte = d.bjedte and a.bspsqn = d.bspsqn and d.bcstat in ('21','81','82') and d.bdwflg = '1'))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,�����Ѽ�����δĨ��,�������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,�����Ѽ�����δĨ��,������")
        
        #===================����,������,������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,������,������")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,a.occamt,a.cuschrg,a.cuschrg,a.ortrcno,'','','02','�����г�Ա����','07','����,������,������','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a"
        temp_sql = temp_sql + " where a.nccwkdat in " + LNCCWKDAT + " and a.sndmbrco != '1340000008' and not exists"
        temp_sql = temp_sql + " (select * from rcc_wtrbka as b"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,������,�������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,������,������")
        
        #===================����,��������,����δ����==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,��������,����δ����")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'02','�����г�Ա����','08','������������,����δ����','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"                                                                        
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.rcvmbrco = '1340000008' and not ((c.bcstat in ('70','72')) and c.bdwflg = '1')"
        temp_sql = temp_sql + " and ((a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '1') or (a.trcco in ('3000102','3000103','3000104','3000105') and a.confflg = '0')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,��������,����δ�����쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,��������,����δ����")
        
        #===================����,���ĳ���,����δ����==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,���ĳ���,����δ����")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'01','�����޳�Ա����','09','�������ĳ���,����δ����','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '1' and a.rcvmbrco = '1340000008' and not (c.bcstat = '81' and c.bdwflg = '1')"
        temp_sql = temp_sql + " and ((a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '1') or (a.trcco in ('3000102','3000103','3000104','3000105') and a.confflg = '0')))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,���ĳ���,����δ�����쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,���ĳ���,����δ����")
        
        #===================����,ͨ��ҵ��,����δȷ��==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������,ͨ��ҵ��,����δȷ��")
        
        temp_sql = "insert into rcc_tddzcz"
        temp_sql = temp_sql + " (select a.nccwkdat,a.sndbnkco,a.trcdat,a.trcno,a.rcvbnkco,a.sndmbrco,a.rcvmbrco,a.trcco,a.dcflg,a.pyracc,a.pyeacc,a.cur,a.occamt,b.occamt,a.cuschrg,case when b.chrgtyp='1'and b.trcco in ('3000102','3000103','3000104','3000105') then b.cuschrg else 0.00 end case,a.ortrcno,b.bjedte,b.bspsqn,'04','��ȷ��','10','����,ͨ��,����δȷ��','0','','','',''"
        temp_sql = temp_sql + " from rcc_tddzmx as a,rcc_wtrbka as b,rcc_spbsta as c"
        temp_sql = temp_sql + " where a.sndbnkco = b.sndbnkco and a.trcdat = b.trcdat and a.trcno = b.trcno and b.bjedte = c.bjedte and b.bspsqn = c.bspsqn"
        temp_sql = temp_sql + " and a.nccwkdat in " + LNCCWKDAT + " and a.cancflg = '0' and a.rcvmbrco = '1340000008'"
        temp_sql = temp_sql + " and a.trcco in ('3000002','3000003','3000004','3000005') and a.confflg = '0')"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������,ͨ��ҵ��,����δȷ���쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������,ͨ��ҵ��,����δȷ��")
        
        
        
        #================�ر�ͨ��ͨ�Ҷ�����ϸ�˹���ϵͳ����,��ͨ��ͨ�Ҷ��˲���ļ��ϴ�ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر�ͨ��ͨ�Ҷ�����ϸ�˹���ϵͳ����,��ͨ��ͨ�Ҷ��˴��˴���ϵͳ����")
        if not rccpsCronFunc.closeCron("00063"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�ر�ͨ��ͨ�Ҷ�����ϸ�˹���ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00060"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�Ҷ��˲���ļ��ϴ�ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00065"):
            rccpsCronFunc.cronExit("S999","��ͨ��ͨ�ҽ�ת�ļ����ɼ����͵����������쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر�ͨ��ͨ�Ҷ�����ϸ�˹���ϵͳ����,��ͨ��ͨ�Ҷ��˲���ļ��ϴ�ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.ͨ��ͨ�Ҷ�����ϸ�˹���[rccpsTDDZMXCompare]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsTDDZMXCompare]�����ж�***')

        sys.exit(-1)
