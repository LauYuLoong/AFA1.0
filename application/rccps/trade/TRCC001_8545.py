# -*- coding: gbk -*-
##################################################################
#   农信银.查询业务.中心状态查询
#=================================================================
#   程序文件:   TRCC001_8554.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  刘雨龙
#   修改时间:   2008-06-12
##################################################################
import TradeContext,AfaLoggerFunc,AfaFlowControl,AfaUtilTools,rccpsDBTrcc_mbrifa
import AfaFlowControl

from types import *
from rccpsConst import *

def SubModuleDoFst():
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8545]进入***' )
    
    #=====判断接口是否存在====
    if not TradeContext.existVariable("OPRTYPNO"):
        return AfaFlowControl.ExitThisFlow('M999','业务类型[OPRTYPNO]不存在')

    #=====判断OPRTYPNO是汇票时查询汇兑业务信息====
    #=====PL_TRCCO_HP 21 汇票====
    #=====PL_TRCCO_HD 20 汇兑====
    #=====PL_TRCCO_TCTD 30 通存通兑====
    
    #=====汇票使用的日期和工作状态同汇兑====
    if TradeContext.OPRTYPNO == PL_TRCCO_HP:
        OPRTYPNO = PL_TRCCO_HD
    elif TradeContext.OPRTYPNO == PL_TRCCO_HD:
        OPRTYPNO = PL_TRCCO_HD
    elif TradeContext.OPRTYPNO == PL_TRCCO_TCTD:
        OPRTYPNO = PL_TRCCO_TCTD
    else:
        return AfaFlowControl.ExitThisFlow('M999','业务类型[OPRTYPNO]错误')
       
    #=====按行号查询====
    sqldic={'OPRTYPNO':OPRTYPNO}
    
    #=====查询数据库，得到查询结果集====
    records=rccpsDBTrcc_mbrifa.selectu(sqldic)  
    if records==None:
        return AfaflowControl.ExitThisFlow('M999','数据库操作失败')
    if len(records) <= 0 :
        return AfaflowControl.ExitThisFlow('M999','无满足条件数据')
 

    TradeContext.NCCworkDate = records['NWWKDAT']       #中心工作日期
    TradeContext.NWSYSST     = records['NWSYSST']       #工作状态
    TradeContext.errorMsg="查询成功"
    TradeContext.errorCode="0000"
    
    AfaLoggerFunc.tradeInfo( '***农信银系统：往账.本地类操作(1.本地操作)交易[TRC001_8545]退出***' )
    return True
