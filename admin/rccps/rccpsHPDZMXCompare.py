# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��Ʊ������ϸ�˹���
#===============================================================================
#   �����ļ�:   rccpsHPDZMXCompare.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-06-27
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
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊ������ϸ�˹���[rccpshpdzMXCompare]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE4'].replace(",","','") + "')"  #��Ҫ���˵���������(���������㹤���պ�֮ǰ�ķ����㹤����)
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #===================����������,������====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hpdzcz (select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.trcco,a.bjedte,a.bspsqn,'01','����������,������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_bilbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.trcco not in ('2100102','2100104') and a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.nccwkdat in " + LNCCWKDAT + " and b.bcstat = '42' and a.brsflg = '0' and not exists "
        temp_sql = temp_sql + "(select * from rcc_hpdzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno ))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��������������,�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #===================����������,������====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hpdzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.trcco,a.bjedte,a.bspsqn,'02','����������,������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_hpdzmx as a where a.sndmbrco = '1340000008' and a.bjedte = '' and a.bspsqn = '' and a.nccwkdat in " + LNCCWKDAT +  ")"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��������������,�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #===================���������Ѽ���,����δ����==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�������������Ѽ���,����δ��������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hpdzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.trcco,a.bjedte,a.bspsqn,'03','���������Ѽ���,����δ����','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_bilbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.trcco in ('2100001') and a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and b.bcstat = '21' and b.bdwflg = '2' and a.brsflg = '0' and a.nccwkdat = '" + NCCWKDAT + "' and not exists "
        temp_sql = temp_sql + "(select * from rcc_hpdzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","�������������Ѽ���,����δ���������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�����������������Ѽ���,����δ��������")
        
        #===================��������δ����,��������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������δ����,������������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hpdzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.trcco,a.bjedte,a.bspsqn,'04','��������δ����,��������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_bilbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.trcco not in ('2100102','2100104') and a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and not (b.bcstat = '42' and b.bdwflg = '1') and a.brsflg = '0' and a.nccwkdat in " + LNCCWKDAT + " and exists "
        temp_sql = temp_sql + "(select * from rcc_hpdzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","������������δ����,�������������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����������������δ����,������������")
        
        #===================����������,������====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hpdzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.trcco,a.bjedte,a.bspsqn,'05','����������,������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_bilbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.brsflg = '1' and b.bcstat in ('70','71') and b.bdwflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and not exists "
        temp_sql = temp_sql + "(select * from rcc_hpdzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��������������,�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #===================����������,������====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hpdzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.trcco,a.bjedte,a.bspsqn,'06','����������,������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_hpdzmx as a "
        temp_sql = temp_sql + "where a.sndmbrco != '1340000008' and a.bjedte = '' and a.bspsqn = '' and a.nccwkdat in " + LNCCWKDAT + ")"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","��������������,�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #===================������������,����δ����==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����������������,����δ��������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hpdzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.trcco,a.bjedte,a.bspsqn,'07','������������,����δ����','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_bilbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and b.bcstat in ('70','71') and b.bdwflg = '1' and a.brsflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and not exists "
        temp_sql = temp_sql + "(select * from rcc_hpdzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","����������������,����δ���������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������������������,����δ��������")
        
        #===================��������δ����,��������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������δ����,������������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hpdzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.trcco,a.bjedte,a.bspsqn,'08','��������δ����,��������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_bilbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and not (b.bcstat in ('70','71') and b.bdwflg = '1') and a.brsflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and exists "
        temp_sql = temp_sql + "(select * from rcc_hpdzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            AfaLoggerFunc.tradeInfo(AfaDBFunc.sqlErrMsg)
            rccpsCronFunc.cronExit("S999","������������δ����,�������������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����������������δ����,������������")
        
        #================�رջ�Ʊ������ϸ�˹���ϵͳ����,�򿪻�Ʊ���˴��˴���ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ʊ������ϸ�˹���ϵͳ����,�򿪻�Ʊ���˴��˴���ϵͳ����")
        if not rccpsCronFunc.closeCron("00043"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�رջ�Ʊ������ϸ�˹���ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00040"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�򿪻�Ʊ���˴��˴���ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ʊ������ϸ�˹���ϵͳ����,�򿪻�Ʊ���˴��˴���ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ʊ������ϸ�˹���[rccpsHPDZMXCompare]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHPDZMXCompare]�����ж�***')

        sys.exit(-1)
