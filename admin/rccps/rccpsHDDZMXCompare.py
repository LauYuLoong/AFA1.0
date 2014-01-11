# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.��Ҷ�����ϸ�˹���
#===============================================================================
#   �����ļ�:   rccpsHDDZMXCompare.py
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
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ҷ�����ϸ�˹���[rccpsHDDZMXCompare]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "20"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT  = mbrifa_dict['NOTE1'][:8]                           #��������
        LNCCWKDAT = "('" + mbrifa_dict['NOTE3'].replace(",","','") + "')"  #��Ҫ���˵���������(���������㹤���պ�֮ǰ�ķ����㹤����)
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #===================����������,������====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz (select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'01','����������,������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.nccwkdat in " + LNCCWKDAT + " and b.bcstat = '42' and a.brsflg = '0' and not exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno ))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������������,�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #===================����������,������====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'02','����������,������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_hddzmx as a where a.sndmbrco = '1340000008' and a.bjedte = '' and a.bspsqn = '' and a.nccwkdat in " + LNCCWKDAT +  ")"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������������,�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #===================������������,����δ����==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�������������Ѽ���,����δ��������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'03','���������Ѽ���,����δ����','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and b.bcstat = '21' and b.bdwflg = '2' and a.brsflg = '0' and a.nccwkdat = '" + NCCWKDAT + "' and not exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","�������������Ѽ���,����δ���������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>�����������������Ѽ���,����δ��������")
        
        #===================��������δ����,��������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������δ����,������������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'04','��������δ����,��������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and not (b.bcstat = '42' and b.bdwflg = '1') and a.brsflg = '0' and a.nccwkdat in " + LNCCWKDAT + " and exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","������������δ����,�������������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����������������δ����,������������")
        
        #===================����������,������====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'05','����������,������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and a.brsflg = '1' and b.bcstat in ('70','71','80') and b.bdwflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and not exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������������,�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #===================����������,������====================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��������������,����������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'06','����������,������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_hddzmx as a "
        temp_sql = temp_sql + "where a.sndmbrco != '1340000008' and a.bjedte = '' and a.bspsqn = '' and a.nccwkdat in " + LNCCWKDAT + ")"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","��������������,�����������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>������������������,����������")
        
        #===================������������,����δ����==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ����������������,����δ��������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'07','������������,����δ����','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and b.bcstat in ('70','71','80') and b.bdwflg = '1' and a.brsflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and not exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","����������������,����δ���������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>��������������������,����δ��������")
        
        #===================��������δ����,��������==============================
        AfaLoggerFunc.tradeInfo(">>>��ʼ������������δ����,������������")
        
        temp_sql = ""
        temp_sql = temp_sql + "insert into rcc_hddzcz(select a.sndbnkco,a.trcdat,a.trcno,a.nccwkdat,a.bjedte,a.bspsqn,'08','��������δ����,��������','" + PL_ISDEAL_UNDO + "','','','','' "
        temp_sql = temp_sql + "from rcc_trcbka as a,rcc_spbsta as b "
        temp_sql = temp_sql + "where a.bjedte = b.bjedte and a.bspsqn = b.bspsqn and not (b.bcstat in ('70','71','80') and b.bdwflg = '1') and a.brsflg = '1' and a.nccwkdat in " + LNCCWKDAT + " and exists "
        temp_sql = temp_sql + "(select * from rcc_hddzmx as c where a.sndbnkco = c.sndbnkco and a.trcdat = c.trcdat and a.trcno = c.trcno))"
        
        AfaLoggerFunc.tradeInfo(temp_sql)
        
        ret = AfaDBFunc.InsertSql(temp_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","������������δ����,�������������쳣")
        
        AfaLoggerFunc.tradeInfo(">>>����������������δ����,������������")
        
        #================�رջ�Ҷ�����ϸ�˹���ϵͳ����,�򿪻�Ҷ��˴��˴���ϵͳ����==
        AfaLoggerFunc.tradeInfo(">>>��ʼ�رջ�Ҷ�����ϸ�˹���ϵͳ����,�򿪻�Ҷ��˴��˴���ϵͳ����")
        if not rccpsCronFunc.closeCron("00033"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�رջ�Ҷ�����ϸ�˹���ϵͳ�����쳣")
            
        if not rccpsCronFunc.openCron("00030"):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","�򿪻�Ҷ��˴��˴���ϵͳ�����쳣")
        
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����رջ�Ҷ�����ϸ�˹���ϵͳ����,�򿪻�Ҷ��˴��˴���ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.��Ҷ�����ϸ�˹���[rccpsHDDZMXCompare]�˳�***")
    
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
            AfaLoggerFunc.tradeInfo('***[rccpsHDDZMXCompare]�����ж�***')

        sys.exit(-1)