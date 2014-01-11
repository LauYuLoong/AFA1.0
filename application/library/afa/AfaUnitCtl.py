# -*- coding: gbk -*-
##################################################################
#   中间业务平台.商户状态控制
#=================================================================
#   程序文件:   AfaUnitCtl.py
#   修改时间:   2006-09-26
##################################################################
import os
from types import *
import exceptions, TradeContext, AfaDBFunc, TradeException, AfaUtilTools
import ConfigParser, time, Party3Context,AfaLoggerFunc,AfaFlowControl

#获取商户参数
def GetUnitStatus():
    AfaLoggerFunc.tradeInfo('获取商户参数' )
    #============系统标识============
    sqlStr = "SELECT * FROM AFA_UNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND "
    #============商户代码============
    sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' "
    AfaLoggerFunc.tradeInfo( sqlStr )
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，商户信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
        TradeContext.__busiMode__ = records[0][6]   #=============业务模式=============
        if( TradeContext.__busiMode__!="2" ):
            TradeContext.__unitStatus__ = records[0][4]         #=============业务状态=============
            TradeContext.__unitLoginStatus__ = records[0][27]   #=============签到务状态=============
            TradeContext.__unitDayendStatus__ = records[0][28]  #=============日终状态=============
            TradeContext.__unitCheckStatus__ = records[0][30]   #=============对账业务状态=============
        if( TradeContext.__busiMode__=="2" ):
            AfaLoggerFunc.tradeInfo('获取子商户参数' )
            #============系统标识============
            sqlStr = "SELECT * FROM AFA_SUBUNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND "
            #============商户代码============
            sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' AND "
            #============子商户代码============
            sqlStr = sqlStr+"SUBUNITNO = '" + TradeContext.subUnitno + "' "
            subRecords = AfaDBFunc.SelectSql( sqlStr )
            if(subRecords == None ):
                return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，商户分支单位信息表操作异常:'+AfaDBFunc.sqlErrMsg )
            elif( len( subRecords )!=0 ):
                AfaUtilTools.ListFilterNone( subRecords )
                TradeContext.__unitStatus__ = subRecords[0][4]         #=============业务状态=============
                TradeContext.__unitLoginStatus__ = subRecords[0][27]   #=============签到务状态=============
                TradeContext.__unitDayendStatus__ = subRecords[0][28]  #=============日终状态=============
                TradeContext.__unitCheckStatus__ = subRecords[0][30]   #=============对账业务状态=============
    return True
#修改商户状态
def UpdUnitStatus(flag):
    AfaLoggerFunc.tradeInfo('修改商户状态' )
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET STATUS='"+flag+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET STATUS='"+flag+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，商户信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    return True

#修改商户签到状态
def UpdUnitLoginStatus(flag):
    AfaLoggerFunc.tradeInfo('修改商户签到状态' )
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET LOGINSTATUS='"+flag+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET LOGINSTATUS='"+flag+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，商户信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
#修改商户日终状态
def UpdUnitDayendStatus(flag):
    AfaLoggerFunc.tradeInfo('修改商户日终状态' )
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET DAYENDSTATUS='"+flag+"',dayendtime='"+TradeContext.workTime+\
            "' WHERE SYSID='"+TradeContext.sysId+"'and UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET DAYENDSTATUS='"+flag+"' , dayendtime='"+TradeContext.workTime+\
            "' WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，商户信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
#修改商户对账状态
def UpdUnitCheckStatus(flag):
    AfaLoggerFunc.tradeInfo('修改商户对账状态' )
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET TRXCHKSTATUS='"+flag+"', trxchktime="+TradeContext.workTime+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET TRXCHKSTATUS='"+flag+"', trxchktime="+TradeContext.workTime+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，商户信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
#修改商户当前工作日期
def UpdUnitWorkDate():
    AfaLoggerFunc.tradeInfo('修改商户当前工作日期' )
    curworkdate=TradeContext.workDate
    if(  TradeContext.existVariable( "nextWorkDate" ) ):
        curworkdate=TradeContext.nextWorkDate
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET  PREWORKDATE=WORKDATE,WORKDATE='"+curworkdate+"'"+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET PREWORKDATE=WORKDATE,WORKDATE='"+curworkdate+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，商户信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
#插入启运停运流水
def InsertOnOffDTL():
    sql="insert into afa_UnitOnOffDTL(SYSID,UNITNO,SUBUNITNO,STATUS,OPERFLAG,STOPTIME,STARTTIME,NOTE1,NOTE2)"
    sql=sql+" values"
    sql=sql+"('"+TradeContext.sysId       +"'"
    sql=sql+",'"+TradeContext.unitno      +"'"
    sql=sql+",'"+TradeContext.TaxOrgName     +"'"
    sql=sql+",'"+'1'                         +"'"
    sql=sql+",'"+TradeContext.operFlag      +"'"
    sql=sql+",'"+TradeContext.stopTime      +"'"
    sql=sql+",'"+TradeContext.startTime      +"'"
    sql=sql+",'"+TradeContext.NOTE1           +"'"
    sql=sql+",'"+TradeContext.NOTE2           +"'"
    sql=sql+")"
    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
        AfaLoggerFunc.tradeFatal(sql)
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    return True


#获取商户参数
#def GetUnitStatus():
#    AfaLoggerFunc.tradeInfo('获取商户参数' )
#    #============系统标识============
#    sqlStr = "SELECT * FROM AFA_UNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND "
#    #============商户代码============
#    sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' "
#    AfaLoggerFunc.tradeInfo( sqlStr )
#    records = AfaDBFunc.SelectSql( sqlStr )
#    if( records == None ):
#        AfaLoggerFunc.tradeFatal( sqlStr )
#        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，商户信息表操作异常:'+AfaDBFunc.sqlErrMsg )
#    elif( len( records )!=0 ):
#        AfaUtilTools.ListFilterNone( records )
#        TradeContext.__busiMode__ = records[0][6]   #=============业务模式=============