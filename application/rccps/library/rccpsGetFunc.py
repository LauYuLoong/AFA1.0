# -*- coding: gbk -*-
##################################################################
#   农信银系统.状态函数操作类
#=================================================================
#   程序文件:   rccpsGetFunc.py
#   修改时间:   2006-03-31
##################################################################
import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,AfaFlowControl,TransBillFunc,AfaFunc
import exceptions,os,time,rccpsDBTrcc_subbra,rccpsDBTrcc_paybnk
from types import *
from rccpsConst import *


#=======================获取平台流水号DB2=======================================
def GetSerialno( BRSFLG, seqName="RCCPS_SEQ" ):

    AfaLoggerFunc.tradeDebug( '>>>获取平台流水号' )
    #=====是否为往账业务====
    if BRSFLG == PL_BRSFLG_SND:
        #=====判断机构号是否存在====
        if( not TradeContext.existVariable( "BESBNO" ) ):
            raise AfaFlowControl.ExitThisFlow('M999','无机构号，处理失败' )

    #=====往账机构号取第3－6位====
    TradeContext.Serialno = TradeContext.BESBNO[2:6]

    AfaLoggerFunc.tradeInfo('>>>开始判断交易代码')
    #====判断交易代码是否存在（中心7位代码）====
    if( not TradeContext.existVariable( "TRCCO" ) ):
        raise AfaFlowControl.ExitThisFlow('M999','交易代码[TRCCO]字段值不存在' )
    #=====判断业务类型,根据交易取不同类型====
    AfaLoggerFunc.tradeInfo('>>>开始判断业务类型')
    if not GetTRCCO():
        raise AfaFlowControl.ExitThisFlow('M999','取业务类型失败' )
    #=====生成流水号====
    AfaLoggerFunc.tradeInfo('>>>开始生成交易流水号')
    sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
    #左补"0"(6位)
    #=====流水号规则：4位机构号+1位业务类型+1位往来账标志+6位顺序号
    TradeContext.BSPSQN=TradeContext.Serialno+BRSFLG+str(records[0][0]).rjust(6,'0' )

    AfaLoggerFunc.tradeInfo( '平台流水号' + TradeContext.BSPSQN )

    return str( records[0][0] )

################################################################################
# 函数名:    GetTRCCO()
# 参数:      无
# 返回值：    True  设置状态成功    False 设置状态失败
# 函数说明：  根据交易代码查找业务类型
# 编写时间：   2008-6-5
# 作者：       刘雨龙
################################################################################
def GetTRCCO():
    #=====汇兑业务，业务类型为1====
    if( TradeContext.TRCCO=='2000001' or TradeContext.TRCCO=='2000002' or
       TradeContext.TRCCO=='2000003' or TradeContext.TRCCO=='2000004' or
       TradeContext.TRCCO=='2000009'):
        TradeContext.Serialno = TradeContext.Serialno + '1'
    #=====汇票业务，业务类型为2====
    #elif( TradeContext.TRCCO=='2100001' or TradeContext.TRCCO=='2100100' or
    #   TradeContext.TRCCO=='2100101' or TradeContext.TRCCO=='2100102' or
    #   TradeContext.TRCCO=='2100103'):
    # 关彬捷 20080913 增加2100104解挂业务
    elif( TradeContext.TRCCO=='2100001' or TradeContext.TRCCO=='2100100' or
       TradeContext.TRCCO=='2100101' or TradeContext.TRCCO=='2100102' or
       TradeContext.TRCCO=='2100103' or TradeContext.TRCCO=='2100104'):
        TradeContext.Serialno = TradeContext.Serialno + '2'
    #=====通存通兑业务，业务类型为3====
    elif( TradeContext.TRCCO=='3000001' or TradeContext.TRCCO=='3000100' or
       TradeContext.TRCCO=='3000101' or TradeContext.TRCCO=='3000500' or
       TradeContext.TRCCO=='3000002' or TradeContext.TRCCO=='3000003' or
       TradeContext.TRCCO=='3000102' or TradeContext.TRCCO=='3000103' or
       TradeContext.TRCCO=='3000501' or TradeContext.TRCCO=='3000004' or
       TradeContext.TRCCO=='3000005' or TradeContext.TRCCO=='3000104' or
       TradeContext.TRCCO=='3000105' or TradeContext.TRCCO=='3000502' or
       TradeContext.TRCCO=='3000503' or TradeContext.TRCCO=='3000504' or
       TradeContext.TRCCO=='3000505' or TradeContext.TRCCO=='3000506' or
       TradeContext.TRCCO=='3000507' ):
        TradeContext.Serialno = TradeContext.Serialno + '3'
    #=====汇兑查询查复自由格式，业务类型为4====
    elif( TradeContext.TRCCO=='9900511' or TradeContext.TRCCO=='9900512' or
       TradeContext.TRCCO=='9900513' or TradeContext.TRCCO=='9900520' or
       TradeContext.TRCCO=='9900521' or TradeContext.TRCCO=='9900522' or
       TradeContext.TRCCO=='9900523' or TradeContext.TRCCO=='9900524'):
        TradeContext.Serialno = TradeContext.Serialno + '4'
    #=====汇票查询查复,撤销申请，业务类型为5====
    elif( TradeContext.TRCCO=='9900526' or TradeContext.TRCCO=='9900527' or
       TradeContext.TRCCO=='9900501' or TradeContext.TRCCO=='9900502' or
       TradeContext.TRCCO=='9900506' or TradeContext.TRCCO=='9900507'):
        TradeContext.Serialno = TradeContext.Serialno + '5'
    else:
        TradeContext.Serialno = TradeContext.Serialno + '6'

    return TradeContext.Serialno
################################################################################
# 函数名:    GetRccSerialno()
# 参数:      TRCCO
# 返回值：    True  设置状态成功    False 设置状态失败
# 函数说明：  根据交易代码生成流水号
# 编写时间：   2008-6-5
# 作者：       刘雨龙
################################################################################
def GetRccSerialno( seqName="RCC_SEQ" ):
    AfaLoggerFunc.tradeDebug( '>>>开始生成交易流水号' )
    #=====判断交易代码是否存在====
    if not TradeContext.existVariable("TRCCO"):
        return AfaFlowControl.ExitThisFlow('M999', '交易代码不存在')
    elif (TradeContext.TRCCO=='2000009' or TradeContext.TRCCO=='9900522'
        or TradeContext.TRCCO=='9900523' or TradeContext.TRCCO=='9900524'):
        #=====生成4位的流水号====
        sqlStr = "SELECT NEXTVAL FOR TYHD_SEQ FROM SYSIBM.SYSDUMMY1"
        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
        TradeContext.SerialNo=str( records[0][0] ).rjust( 8, '0' )
    else:
        #=====生成流水号====
        sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
        TradeContext.SerialNo=str( records[0][0] ).rjust( 8, '0' )

    AfaLoggerFunc.tradeInfo( '交易流水号' + TradeContext.SerialNo )

    return TradeContext.SerialNo



################################################################################
# 函数名:    GetRcvBnkCo()
# 参数:      RCVBNKCO
# 返回值：    True  设置状态成功    False 设置状态失败
# 函数说明：  根据接收行号取接收行发起行成员号
# 编写时间：   2008-6-15
# 作者：       刘雨龙
################################################################################
def GetRcvBnkCo(RCVBNKCO):
    #=====通过接收行号取接收行成员行号====
    if (TradeContext.existVariable("RCVBNKCO") and len(RCVBNKCO)!=0):
        rcvstl = {'BANKBIN':TradeContext.RCVBNKCO}
        rcvpyb = rccpsDBTrcc_paybnk.selectu(rcvstl)
        if (rcvpyb == None or len(rcvpyb) == 0):
            return AfaFlowControl.ExitThisFlow('M999','接收行号取接收成员行号无相应记录')
        else:
            TradeContext.RCVSTLBIN = rcvpyb['STLBANKBIN']
            TradeContext.RCVBNKNM  = rcvpyb['BANKNAM']
    else:
        return False

    return TradeContext.RCVSTLBIN
################################################################################
# 函数名:    GetSndBnkCo()
# 参数:      SNDBNKCO
# 返回值：    True  设置状态成功    False 设置状态失败
# 函数说明：  根据接收行号取接收行发起行成员号
# 编写时间：   2008-6-15
# 作者：       刘雨龙
################################################################################
def GetSndBnkCo(SNDBNKCO):
    #=====通过接收行号取接收行成员行号====
    if (TradeContext.existVariable("SNDBNKCO") and len(SNDBNKCO)!=0):
        rcvstl = {'BANKBIN':TradeContext.SNDBNKCO}
        rcvpyb = rccpsDBTrcc_paybnk.selectu(rcvstl)
        if (rcvpyb == None or len(rcvpyb) == 0):
            return AfaFlowControl.ExitThisFlow('M999','接收行号取接收成员行号无相应记录')
        else:
            TradeContext.SNDSTLBIN = rcvpyb['STLBANKBIN']
            TradeContext.SNDBNKNM  = rcvpyb['BANKNAM']
    else:
        return False

    return TradeContext.SNDSTLBIN
    
    
#=======================获取前置流水号DB2=======================================
def GetRBSQ( BRSFLG, seqName="RCCPS_SEQ" ):

    AfaLoggerFunc.tradeDebug( '>>>获取前置流水号' )
    #=====是否为往账业务====
    if BRSFLG == PL_BRSFLG_SND:
        #=====判断机构号是否存在====
        if( not TradeContext.existVariable( "BESBNO" ) ):
            raise AfaFlowControl.ExitThisFlow('M999','无机构号，处理失败' )

    #=====往账机构号取第3－6位====
    TradeContext.Serialno = TradeContext.BESBNO[2:6]

    AfaLoggerFunc.tradeDebug('>>>开始判断交易代码')
    #====判断交易代码是否存在（中心7位代码）====
    if( not TradeContext.existVariable( "TRCCO" ) ):
        raise AfaFlowControl.ExitThisFlow('M999','交易代码[TRCCO]字段值不存在' )
    #=====判断业务类型,根据交易取不同类型====
    AfaLoggerFunc.tradeDebug('>>>开始判断业务类型')
    if not GetTRCCO():
        raise AfaFlowControl.ExitThisFlow('M999','取业务类型失败' )
    #=====生成流水号====
    AfaLoggerFunc.tradeInfo('>>>开始生成前置流水号')
    sqlStr = "SELECT NEXTVAL FOR " + seqName + " FROM SYSIBM.SYSDUMMY1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        raise AfaFlowControl.ExitThisFlow('A0025', AfaDBFun.sqlErrMsg )
    #左补"0"(6位)
    #=====流水号规则：4位机构号+1位业务类型+1位往来账标志+6位顺序号
    TradeContext.RBSQ=TradeContext.Serialno+BRSFLG+str(records[0][0]).rjust(6,'0' )

    AfaLoggerFunc.tradeInfo( '>>>前置流水号' + TradeContext.RBSQ )

    return str( records[0][0] )
