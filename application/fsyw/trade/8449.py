###############################################################################
# -*- coding: gbk -*-
# �ļ���ʶ��
# ժ    Ҫ�����շ�˰
#
# ��ǰ�汾��1.0
# ��    �ߣ�
# ������ڣ�2009��07��23��
###############################################################################

#���е�״̬λ 0 �ѹ��Ҵ���  1δ���Ҵ���  *�Ǵ�������
import TradeContext

TradeContext.sysType = 'cron'

import ConfigParser, AfaUtilTools, sys, AfaDBFunc, Party3Context,AfaAdminFunc
import os, HostContext, HostComm, AfaAfeFunc, AfaLoggerFunc, time
from types import *


if __name__=='__main__':

    AfaLoggerFunc.tradeInfo( "********************��̨��ֿ�ʼ***************" )
    #TradeContext.workDate       =   AfaUtilTools.GetSysDate( )

    #begin 20100630 ���������Ӳ���
    if ( len(sys.argv) != 2 ):
        TradeContext.workDate  = AfaAdminFunc.getTimeFromNow(int(-1))
    else:
        sOffSet                =   sys.argv[1]
        TradeContext.workDate  = AfaAdminFunc.getTimeFromNow(int(sOffSet))
    #end

    #TradeContext.workDate  =   '20100319'
    TradeContext.workTime       =   AfaUtilTools.GetSysTime( )
    riqi   =    TradeContext.workDate
    AfaLoggerFunc.tradeInfo( TradeContext.workDate )
    AfaLoggerFunc.tradeInfo( TradeContext.workTime )
    today  =  TradeContext.workDate
    TradeContext.workDate       =   TradeContext.workDate[0:4] + "-" + TradeContext.workDate[4:6] + "-" + TradeContext.workDate[6:]
    AfaLoggerFunc.tradeInfo( TradeContext.workDate )

    #begin 20100609 �������޸�
    #sqlstr_bus  =  "select busino from fs_businoconf"
    sqlstr_bus  =  "select busino, bankno from fs_businoconf"
    #end

    records_bus = AfaDBFunc.SelectSql( sqlstr_bus )
    if records_bus == None or len(records_bus)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","���ҵ�λ��Ϣ���쳣"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr_bus )
        sys.exit(1)
    for i in range( len(records_bus) ):
        TradeContext.busiNo  = records_bus[i][0].strip()

        #begin 20100609 �������޸�
        AfaLoggerFunc.tradeInfo( '>>>>��ʼ��ѯ�������ݱ�FC74' )
        TradeContext.bankbm  = records_bus[i][1].strip()
        sqlstr_fc74   =   ""
        #sqlstr_fc74   =   "select afc401 from fs_fc74 where busino='" + TradeContext.busiNo + "' and afc015='" + TradeContext.workDate + "' and flag='*'"
        sqlstr_fc74   =   sqlstr_fc74 + "select afc401 from fs_fc74 where busino='" + TradeContext.busiNo + "' and afc015='" + TradeContext.workDate + "' and flag='*'"
        sqlstr_fc74   =   sqlstr_fc74 + " and afa101 = '" + TradeContext.bankbm + "'"
        #end

        records_fc74  =   AfaDBFunc.SelectSql( sqlstr_fc74 )
        AfaLoggerFunc.tradeInfo( sqlstr_fc74 )

        #begin 20100609 ����������
        if records_fc74 == None :
            AfaLoggerFunc.tradeInfo( '>>>��ѯ��������Ϣ�쳣' )
            continue
        elif  len( records_fc74 ) == 0:
            AfaLoggerFunc.tradeInfo( '>>>û�д�������Ϣ' )
            continue
        #end

        for k in range( len(records_fc74) ):
            TradeContext.serno   =    records_fc74[k][0].strip()
            AfaLoggerFunc.tradeInfo( '>>>>��ѯ��ˮ��Ϣ:' + TradeContext.serno )
            sqlstr_main          =   "select * from fs_maintransdtl where busino='" + TradeContext.busiNo + "' and workdate='" + today + "' and bankserno='" + TradeContext.serno + "' and bankstatus='0' and corpstatus='0'"
            records_main         =   AfaDBFunc.SelectSql( sqlstr_main )
            AfaLoggerFunc.tradeInfo( '��ѯ����ˮ>>>' + sqlstr_main )
            if len(records_main) == 0:

                #begin 20100609 �������޸�
                sqlstr_up   =   ""
                #sqlstr_up   =   "update fs_fc74  set flag='1',date= '" + riqi + "' where busino='" + TradeContext.busiNo + "' and afc015='" + TradeContext.workDate +  "' and afc401='" + TradeContext.serno + "'"
                sqlstr_up   =   sqlstr_up + "update fs_fc74  set flag='1',date= '" + riqi + "' where busino='" + TradeContext.busiNo + "' and afc015='" + TradeContext.workDate +  "' and afc401='" + TradeContext.serno + "'"
                sqlstr_up   =   sqlstr_up + " and afa101 = '" + TradeContext.bankbm + "'"
                #end

                AfaDBFunc.UpdateSqlCmt( sqlstr_up )
                AfaLoggerFunc.tradeInfo( 'sqlstr_up->' + sqlstr_up )
                continue

    AfaLoggerFunc.tradeInfo( "********************��̨��ֽ���***************" )


