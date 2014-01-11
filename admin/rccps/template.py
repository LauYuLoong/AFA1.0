# -*- coding: gbk -*-
################################################################################
#   农信银系统：系统调度类.模板
#===============================================================================
#   交易文件:   template.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  作者
#   修改时间:   YYYY-MM-DD
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,os,AfaFunc,sys
from types import *
from rccpsConst import *
import rccpsCronFunc

if __name__ == '__main__':
    
    try:
        rccpsCronFunc.WrtLog("***农信银系统: 系统调度类.模板[template]进入***")
        
        
        
        rccpsCronFunc.WrtLog("***农信银系统: 系统调度类.模板[template]退出***")
    
    except Exception, e:
        #所有异常

        if not AfaDBFunc.RollbackSql( ):
            rccpsCronFunc.WrtLog( AfaDBFunc.sqlErrMsg )
            rccpsCronFunc.WrtLog(">>>Rollback异常")
        rccpsCronFunc.WrtLog(">>>Rollback成功")

        if( not TradeContext.existVariable( "errorCode" ) or str(e) ):
            TradeContext.errorCode = 'A9999'
            TradeContext.errorMsg = '系统错误['+ str(e) +']'

        if TradeContext.errorCode != '0000' :
            rccpsCronFunc.WrtLog( 'errorCode=['+TradeContext.errorCode+']' )
            rccpsCronFunc.WrtLog( 'errorMsg=['+TradeContext.errorMsg+']' )
            rccpsCronFunc.WrtLog('rccpsHDDZGetFile交易中断')

        sys.exit(-1)