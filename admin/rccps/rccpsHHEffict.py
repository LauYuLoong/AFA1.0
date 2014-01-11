# -*- coding: gbk -*-
################################################################################
#   ũ����ϵͳ��ϵͳ������.�к���Ч����
#===============================================================================
#   �����ļ�:   rccpsHHEffict.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  �ر��
#   �޸�ʱ��:   2008-09-15
################################################################################
import TradeContext
TradeContext.sysType = 'cron'
import AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys,AfaHostFunc
from types import *
from rccpsConst import *
import rccpsCronFunc,rccpsState,rccpsDBFunc,rccpsHostFunc
import rccpsDBTrcc_mbrifa,rccpsDBTrcc_paybnk

if __name__ == '__main__':
    
    try:
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.�����к���Ч����[rccpsHHEffict]����***")
        
        #==========��ȡ��������================================================
        AfaLoggerFunc.tradeInfo(">>>��ʼ��ȡǰ���Ĺ�������")
        
        mbrifa_where_dict = {}
        mbrifa_where_dict['OPRTYPNO'] = "30"
        
        mbrifa_dict = rccpsDBTrcc_mbrifa.selectu(mbrifa_where_dict)
        
        if mbrifa_dict == None:
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","��ѯ��ǰ���������쳣")
            
        NCCWKDAT = mbrifa_dict['NWWKDAT'][:8]                           #��ǰ���Ĺ�������
        
        AfaLoggerFunc.tradeInfo(">>>������ȡǰ���Ĺ�������")
        
        #========�к���Ч����==================================================
        AfaLoggerFunc.tradeInfo("��ʼ��Ч�к�")
        
        bank_sql = ""
        bank_sql = bank_sql + "update rcc_paybnk set note1 = '1' "
        bank_sql = bank_sql + "where alttype in ('1','2') and bankbin in ("
        bank_sql = bank_sql + "select bankbin from rcc_paybnk "
        bank_sql = bank_sql + "where '" + NCCWKDAT +  "' >= efctdat)"
        
        AfaLoggerFunc.tradeInfo(bank_sql)
        
        ret = AfaDBFunc.executeUpdateCmt(bank_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","�޸�����Ч���к���ЧʧЧ��ʶΪ(1-��Ч)�쳣")
            
        AfaLoggerFunc.tradeInfo("������Ч�к�")
        
        #========�к�ʧЧ����==================================================
        AfaLoggerFunc.tradeInfo("��ʼʧЧ�к�")
        
        bank_sql = ""
        bank_sql = bank_sql + "update rcc_paybnk set note1 = '2' "
        bank_sql = bank_sql + "where alttype in ('3') and bankbin in ("
        bank_sql = bank_sql + "select bankbin from rcc_paybnk "
        bank_sql = bank_sql + "where '" + NCCWKDAT + "' >= efctdat)"
        
        AfaLoggerFunc.tradeInfo(bank_sql)
        
        ret = AfaDBFunc.executeUpdateCmt(bank_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","�޸���ʧЧ���к���ЧʧЧ��ʶΪ(2-ʧЧ)�쳣")
        
        AfaLoggerFunc.tradeInfo("����ʧЧ�к�")
        
        #========ɾ���Ѽ���NCSϵͳ����Լ���ϵͳ�к�===========================
        AfaLoggerFunc.tradeInfo("��ʼɾ���Ѽ���NCSϵͳ����Լ���ϵͳ�к�")
        
        bank_sql = ""
        bank_sql = bank_sql + "delete from rcc_paybnk "
        bank_sql = bank_sql + "where note1 = '2' and newoflg = '2' "
        bank_sql = bank_sql + "and bankbin in ("
        bank_sql = bank_sql + "select bankbin from rcc_paybnk "
        bank_sql = bank_sql + "where '" + NCCWKDAT + "' >= efctdat)"
        
        AfaLoggerFunc.tradeInfo(bank_sql)
        
        ret = AfaDBFunc.executeUpdateCmt(bank_sql)
        
        if ret < 0:
            rccpsCronFunc.cronExit("S999","ɾ���Ѽ���NCSϵͳ����Լ���ϵͳ�к��쳣")
        
        AfaLoggerFunc.tradeInfo("����ɾ���Ѽ���NCSϵͳ����Լ���ϵͳ�к�")
        #================�ر������к���Ч����ϵͳ����==========================
        AfaLoggerFunc.tradeInfo(">>>��ʼ�ر������к���Ч����ϵͳ����")
        if not rccpsCronFunc.closeCron("00050"):
            rccpsCronFunc.cronExit("S999","�ر������к���Ч����ϵͳ�����쳣")
            
        if not AfaDBFunc.CommitSql( ):
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.cronExit("S999","Commit�쳣")
        AfaLoggerFunc.tradeInfo(">>>Commit�ɹ�")
        
        AfaLoggerFunc.tradeInfo(">>>�����ر������к���Ч����ϵͳ����")
        
        AfaLoggerFunc.tradeInfo("***ũ����ϵͳ: ϵͳ������.�����к���Ч����[rccpsHHEffict]�˳�***")
        
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
            AfaLoggerFunc.tradeInfo("***[rccpsHHEffict]�����ж�***")

        sys.exit(-1)
