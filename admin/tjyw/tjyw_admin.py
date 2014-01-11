# -*- coding: gbk -*-
###############################################################################
# 文件名称：tjyw_admin.py
# 摘    要：全省通缴业务对账
# 当前版本：1.0
# 作    者：CYG
# 完成日期：2010年01月06日
###############################################################################
import TradeContext

TradeContext.sysType = 'tjyw'

import ConfigParser, sys, AfaDBFunc, os, AfaAdminFunc,HostContext,YbtFunc,AfaUtilTools
from types import *

###########################################主函数###########################################
if __name__=='__main__':


    print('**********全省通缴业务操作开始**********')

    if ( len(sys.argv) != 4 ):
        print( '用法: jtfk_Proc sysid unitno dateoffset')
        sys.exit(-1)

    sSysId      = sys.argv[1]
    sUnitno     = sys.argv[2]
    sOffSet     = sys.argv[3]
    sTrxDate   = AfaAdminFunc.getTimeFromNow(int(sOffSet))

    print '   系统编码 = ' + sSysId
    print '   单位编码 = ' + sUnitno
    print '   交易日期 = ' + sTrxDate

    #读取配置文件
    if ( not AfaAdminFunc.GetAdminConfig( ) ) :
        sys.exit(-1)

    AfaAdminFunc.WrtLog('>>>与主机对帐')
    if not AfaAdminFunc.MatchData(sSysId,sUnitno,sTrxDate):
        sys.exit(-1)

    print '**********全省通缴业务操作结束**********'

    sys.exit(0)
