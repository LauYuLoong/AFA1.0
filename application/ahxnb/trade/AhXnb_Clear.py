###############################################################################
# -*- coding: gbk -*-
# 摘    要：新农保批量定时清理临时数据
# 当前版本：1.0
# 作    者：蔡永贵
# 完成日期：2010年12月23日
###############################################################################
import TradeContext

TradeContext.sysType = "ahxnb"

import sys, AfaDBFunc,AfaLoggerFunc,AfaAdminFunc

from types import *

if __name__ == '__main__':
    
    AfaLoggerFunc.tradeInfo( '-------------------安徽省新农保数据清理操作开始-------------------' )
    
    if ( len(sys.argv) != 2 ):
        print ( '用法:python procName offsetDays' )
        sys.exit( -1 )
    offsetDays = sys.argv[1]
    DelDate = AfaAdminFunc.getTimeFromNow( int(offsetDays) )
    
    #删除指定日期前的临时数据
    sql = "delete from ahxnb_swap where workdate <= '" + DelDate + "'"
    
    AfaLoggerFunc.tradeInfo( '定时清理sql：' + sql )
    
    ret = AfaDBFunc.DeleteSqlCmt( sql )
    
    if ret < 0:
        AfaLoggerFunc.tradeInfo( '定时清理数据失败' )
        sys.exit( -1 )
    AfaLoggerFunc.tradeInfo( '总共清理【' + str(ret) + "】条记录" )
    
    AfaLoggerFunc.tradeInfo( '-------------------安徽省新农保数据清理操作结束-------------------' )
    
    sys.exit( 0 )
