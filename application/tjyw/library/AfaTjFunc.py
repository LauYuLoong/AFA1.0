# -*- coding: gbk -*-
################################################################################
# 文件名称：AfaTjFunc.py
# 文件标识：
# 摘    要：中间业务通缴业务
#
################################################################################
import TradeContext, AfaDBFunc, AfaFlowControl, AfaUtilTools
import os, time, AfaLoggerFunc
from types import *

#============================判断应用状态============================
def ChkUnitInfo( ):

    AfaLoggerFunc.tradeInfo( '＝＝＝＝＝判断应用状态开始＝＝＝＝＝' )

    sqlStr = ''
    sqlStr = sqlStr + "SELECT STATUS,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO FROM ABDT_UNITINFO "
    sqlStr = sqlStr + " AND WHERE APPNO = '" + TradeContext.sysId + "'"

    #============单位编码============
    sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busino + "'"

    #============委托方式============
    sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"
    
    AfaLoggerFunc.tradeFatal( '查询结果 ：'+sqlStr )
    
    records = AfaDBFunc.SelectSql( sqlStr )
    
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '查询单位协议信息异常')

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
        
        TradeContext.STATUS        = str(records[0][0])                             #签约状态
        TradeContext.STARTDATE     = str(records[0][1])                             #生效日期
        TradeContext.ENDDATE       = str(records[0][2])                             #失效日期
        TradeContext.STARTTIME     = str(records[0][3])                             #服务开始时间
        TradeContext.ENDTIME       = str(records[0][4])                             #服务终止时间
        TradeContext.ACCNO         = str(records[0][5])                             #对公账户
        
        
        if ( (TradeContext.STARTDATE > TradeContext.workDate) or (TradeContext.workDate > TradeContext.ENDDATE) ):
            return AfaFlowControl.ExitThisFlow( '9000', '该单位委托协议还没有生效或已过有效期')

        if ( (TradeContext.STARTTIME > TradeContext.workTime) or (TradeContext.workTime > TradeContext.ENDTIME) ):
            return AfaFlowControl.ExitThisFlow( '9000', '已经超过该系统的服务时间,该业务必须在[' + s_StartDate + ']-[' + s_EndDate + ']时间段运行')

        #=============代理业务帐号=============
        #TradeContext.__agentAccno__ = records[0][5] 
        #AfaLoggerFunc.tradeInfo('收款人帐户__agentAccno__ BB：：'+ TradeContext.__agentAccno__)           

        AfaLoggerFunc.tradeInfo( '＝＝＝＝＝判断应用状态结束＝＝＝＝＝＝＝' )
        return True
    else:
        AfaLoggerFunc.tradeError( sqlStr )
        return AfaFlowControl.ExitThisFlow( 'A0003', '该地区没有开放此业务' )



#============================判断业务编号============================
def ChkSysInfo( ):
    AfaLoggerFunc.tradeInfo( '＝＝＝＝＝判断业务编号开始＝＝＝＝＝' )
 
    #判断业务编号 AG2016
    if not( TradeContext.existVariable( "sysId" ) and len(TradeContext.sysId.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "业务编号不存在"
            raise AfaFlowControl.flowException( )
            
    if not(TradeContext.sysId == 'AG2016') :
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "非此业务编号，不能做此业务!"
        raise AfaFlowControl.flowException( )        
                










