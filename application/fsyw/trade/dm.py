# -*- coding: gbk -*-

import TradeContext
TradeContext.sysType = 'fsyw'
import os,AfaLoggerFunc, ConfigParser, AfaUtilTools, sys, AfaDBFunc,AfaAdminFunc,AfaFlowControl
from types import *

###########################################主函数###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo( "*********************统计数据开始********************" )
    sqlstr  = "select busino,name,date from fs_businoinfo order by busino"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        AfaLoggerFunc.tradeInfo("查找单位信息表异常")
        sys.exit(1)
    hp = open( "/home/maps/tjsj.txt","w" )

    for i in range( len(records) ):
        TradeContext.appNo        = 'AG2008'
        TradeContext.busiNo       = records[i][0].strip()
        TradeContext.name         = records[i][1].strip()
        TradeContext.date         = records[i][2].strip()

        records1 = 0
        records2 = 0
        sqlstr1 = "select SUM(DOUBLE(AFC011)) from fs_fc74 where FLAG != '*' and busino='" + TradeContext.busiNo + "' and AFC015 >= '2009-01-01' and AFC015 <= '2009-12-31'"
        records1 = AfaDBFunc.SelectSql( sqlstr1 )
        AfaLoggerFunc.tradeInfo( sqlstr1 )
        sqlstr2 = "select SUM(DOUBLE(AMOUNT)) from fs_maintransdtl where BANKSTATUS = '0' and CORPSTATUS ='0' and CHKFLAG	='0' and busino='" + TradeContext.busiNo + "' and WORKDATE >= '20090101' and WORKDATE <= '20091231'"
        records2 = AfaDBFunc.SelectSql( sqlstr2 )
        AfaLoggerFunc.tradeInfo( sqlstr2 )
        sqlstr3 = "select count(*) from fs_fc74 where FLAG != '*' and busino='" + TradeContext.busiNo + "' and AFC015 >= '2009-01-01' and AFC015 <= '2009-12-31'"
        records3 = AfaDBFunc.SelectSql( sqlstr3 )
        AfaLoggerFunc.tradeInfo( sqlstr3 )
        sqlstr4 = "select count(*) from fs_maintransdtl where BANKSTATUS = '0' and CORPSTATUS ='0' and CHKFLAG	='0' and busino='" + TradeContext.busiNo + "' and WORKDATE >= '20090101' and WORKDATE <= '20091231'"
        records4 = AfaDBFunc.SelectSql( sqlstr4 )
        AfaLoggerFunc.tradeInfo( sqlstr4 )

        AfaLoggerFunc.tradeInfo('str(TradeContext.busiNo)=' +str(TradeContext.busiNo))
        AfaLoggerFunc.tradeInfo('str(TradeContext.name)=' +str(TradeContext.name))
        AfaLoggerFunc.tradeInfo('str(TradeContext.date)=' +str(TradeContext.date))
        AfaLoggerFunc.tradeInfo('str(records1[0][0])=' +str(records1[0][0]))
        AfaLoggerFunc.tradeInfo('str(records2[0][0])=' +str(records2[0][0]))

        hp.write(str(TradeContext.busiNo) + ','+ str(TradeContext.name) + ','+ str(TradeContext.date) + ','+str(records1[0][0]) + ','+ str(records2[0][0]) + ','+str(records3[0][0]) + ','+ str(records4[0][0])+ '\n')
    hp.close()

    AfaLoggerFunc.tradeInfo( "*********************统计数据结束********************" )
    sys.exit(1)

