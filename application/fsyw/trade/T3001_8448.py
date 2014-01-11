# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8448.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):

    #=====刘雨龙  20080811  新增查找fa15表中财政区划内码,条件为单位内码====
    AfaLoggerFunc.tradeInfo( ">>>AFA050=" + TradeContext.busiNo)
    sql = "select AAA010 from fs_fa22 where busino='" + TradeContext.busiNo + "'"

    #begin 20100629 蔡永贵增加查询条件
    sql = sql + " and afa101 = '" + TradeContext.bankbm + "'"
    AfaLoggerFunc.tradeInfo( sql )
    #end

    ret = AfaDBFunc.SelectSql( sql )
    if ret == None:
        return AfaFlowControl.ExitThisFlow('0001','通过单位内码查找财政区划内码失败')
    elif len(ret) <= 0:
        return AfaFlowControl.ExitThisFlow('0001','通过单位内码查找财政区划内码无满足条件记录')
    else:
        TradeContext.AAA010  =  ret[0][0]
        
    TradeContext.__agentEigen__  = '0'   #从表标志
    
    AfaLoggerFunc.tradeInfo( "中台查找数据库开始" )
        
    #在中台数据库中查询
    #=====刘雨龙  20080811  新增条件财政区划内码====
    #sqlstr = "select AFC306,AAA010,AFA050,AFC041,AFC061,AFC062,AFC063,AFC064,AAZ016,AAZ015 from FS_FC06 where AFC060='" + TradeContext.AFC060 + "'"
    
    sqlstr = "select AFC306,AAA010,AFA050,AFC041,AFC061,AFC062,AFC063,AFC064,AAZ016,AAZ015 from FS_FC06 where AFC060='" + TradeContext.AFC060 + "'"
    sqlstr = sqlstr + " AND AAA010 = '" + TradeContext.AAA010 + "'"
    
    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找退付信息失败"
        AfaLoggerFunc.tradeInfo( "***************中台查找数据库结束*******************" )
        return False

    elif ( len( records )==1 ):

        #将查找到的信息赋值到TradeContext中
        TradeContext.AFC306     =   records[0][0]
        TradeContext.AAA010     =   records[0][1]
        TradeContext.AFA050     =   records[0][2]
        TradeContext.AFC041     =   records[0][3]
        TradeContext.AFC061     =   records[0][4]
        TradeContext.AFC062     =   records[0][5]
        TradeContext.AFC063     =   records[0][6]
        TradeContext.AFC064     =   records[0][7]
        TradeContext.AAZ016     =   records[0][8]
        TradeContext.AAZ015     =   records[0][9]
        
        if not (TradeContext.AAZ015.strip()  == '1') :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "该退付编号不能退付"
            return False 
        
        #根据财政区划内码查询财政区划
        
        if TradeContext.AAA010 :
            sqlstr  =   ""
            sqlstr  =   "select aaa012 from fs_aa11 where aaa010='" + TradeContext.AAA010 + "'"
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None or len( records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "查找财政区划失败"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:   
                TradeContext.AAA012     =   records[0][0]
        else:
            TradeContext.AAA012         =   ''
            
        #根据执收单位内码查询征收单位名称
        if TradeContext.AFA050:
            sqlstr  =   ""
            sqlstr  =   "select afa052 from fs_fa15 where afa050='" + TradeContext.AFA050 + "'"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None or len( records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "查找执收单位名称失败"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:   
                TradeContext.AFA052     =   records[0][0]
        else:
            TradeContext.AFA052         =   ''
            
        #根据收费项目内码查询收费项目名称
        if TradeContext.AFC041 :
            sqlstr  =   ""
            sqlstr  =   "select afa032 from fs_fa13 where afa030='" + TradeContext.AFC041 + "'"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None or len( records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "查找项目名称名称失败"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:   
                TradeContext.AFA032     =   records[0][0]
        else:
            TradeContext.AFA032         =   ''       
        
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "查找退付信息成功"
        AfaLoggerFunc.tradeInfo( "********************中台查找数据库结束***************" )
        return True
        
    else:
        TradeContext.errorCode  =   "9999"
        TradeContext.errorMsg   =   "发现多条退付记录,不能进行退付操作(请检查数据)"
        return False
