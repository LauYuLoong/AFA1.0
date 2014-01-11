# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8440.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #从表标志

    TradeContext.AFC001         =   TradeContext.userNo

    AfaLoggerFunc.tradeInfo( "中台查找数据库开始" )

    #fieldList                  =   "AFA031,AFC163,AFC187,AFC183,AFC157,AFC181,AFA040,AFC180,AFA051,AFC166,AFC155,AFC153,AFC154,AFA183,AFA184,AFA185,AFA091,AAA010"

    #在中台数据库中查询
    sqlstr                      =   "select AFA031,AFC181,AFA040,AFC180,   \
                                    AFC163,AFC187,AFC183,AFC157,AFA051,AFC166,AFC155,AFC153,AFC154,  \
                                    AFA183,AFA184,AFA185,AFA091,AAA010 from FS_FC70 where AFC001='" + TradeContext.AFC001 + " ' "
    #增加银行编码字段,张恒修改
    sqlstr = sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "没有查找到缴款书信息"
        AfaLoggerFunc.tradeInfo( "***************中台查找数据库结束*******************" )
        return False
    else:
        TradeContext.AFC163     =   records[0][4]
        TradeContext.AFC187     =   records[0][5]
        TradeContext.AFC183     =   records[0][6]
        TradeContext.AFC157     =   records[0][7]
        TradeContext.AFA051     =   records[0][8]
        TradeContext.AFC166     =   records[0][9]
        TradeContext.AFC155     =   records[0][10]
        TradeContext.AFC153     =   records[0][11]
        TradeContext.AFC154     =   records[0][12]
        TradeContext.AFA183     =   records[0][13]
        TradeContext.AFA184     =   records[0][14]
        TradeContext.AFA185     =   records[0][15]
        TradeContext.AFA091     =   records[0][16]
        TradeContext.AAA010     =   records[0][17]


        recCnt                  =   len(records)
        #这些字段需要生成多个 AFC181	(	金额    ),AFA040	(	计量单位),AFC180	(	数量    ),AFA031	(	项目外码)
        if recCnt == 1:

            #将查找到的信息赋值到TradeContext中
            TradeContext.errorCode  =   "0000"
            TradeContext.errorMsg   =   "查找缴款书信息成功"

            TradeContext.RECCNT     =   str( len(records) )
            TradeContext.AFA031     =   records[0][0]
            TradeContext.AFC181     =   records[0][1]
            TradeContext.AFA040     =   records[0][2]
            TradeContext.AFC180     =   records[0][3]

            AfaLoggerFunc.tradeInfo( "一个缴款书对应一个收费项目" )

        elif recCnt > 1  and recCnt <= 3 :

            #将查找到的信息赋值到TradeContext中
            TradeContext.errorCode  =   "0000"
            TradeContext.errorMsg   =   "查找缴款书信息成功"
            TradeContext.RECCNT     =   str(len(records))

            fields                  =   "AFA031,AFC181,AFA040,AFC180"

            index                   =   0                   #字段名下标
            for field  in fields.split(","):
                item                =   []
                for i in range(recCnt):
                    item.append(records[i][index])

                if item == None :
                    return False

                value               =   "^".join(item)
                setattr(TradeContext,field,value)
                index               =   index + 1           #开始下一个字段

                AfaLoggerFunc.tradeInfo( "一个缴款书对应多个收费项目" )
                AfaLoggerFunc.tradeInfo( field + "***" + value )

        else:
            AfaLoggerFunc.tradeInfo( "一个交款编号对应的缴费项目超过了三个" )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "查找缴款书信息失败"
            return False


    AfaLoggerFunc.tradeInfo( ">>>开始查询执收单位名称" )
    #查询执收单位名称
    sqlstr  =   "select afa052 from fs_fa15 where afa051='" + TradeContext.AFA051 + "' and BUSINO='" + TradeContext.busiNo + "'"
    sqlstr  =   sqlstr + " and aaa010='" + TradeContext.AAA010 + "'"
    #=====刘雨龙 20080827 查询执收单位名称时,增加财政区划内码作为查询条件====

    records = AfaDBFunc.SelectSql( sqlstr )
    if ( records == None or len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "没有查找到执收单位名称"
        return False

    TradeContext.AFA052         =   records[0][0]               #执收单位名称
    AfaLoggerFunc.tradeInfo( ">>>执收单位名称[" + TradeContext.AFA052 + "]")


    AfaLoggerFunc.tradeInfo( ">>>开始查询执收项目名称" )
    #查询执收项目名称
    sqlstr      =   ""
    value       =   []
    AfaLoggerFunc.tradeInfo(TradeContext.RECCNT )

    for i in range( 0,int(TradeContext.RECCNT) ):
        sqlstr  =   "select afa032,afa030 from fs_fa13 where afa031='" + (TradeContext.AFA031.split("^"))[i]  + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"
        AfaLoggerFunc.tradeInfo(sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )

        AfaLoggerFunc.tradeInfo(str(records))

        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "没有查找到执收项目名称"
            return False
        AfaLoggerFunc.tradeInfo(str(i))
        value.append(records[0][0])

        TradeContext.AFA032             =   "^".join(value)
        AfaLoggerFunc.tradeInfo( ">>>执收项目名称[" + TradeContext.AFA032 + "]")

    AfaLoggerFunc.tradeInfo( ">>>开始查询代收银行名称" )
    #查询代收银行名称
    sqlstr      =   ""
    value       =   []
    sqlstr  =   "select afa102 from fs_fa22 where afa101='" + TradeContext.AFC153 + "' and BUSINO='" + TradeContext.busiNo + "'"
    sqlstr  =   sqlstr + " and aaa010='" + TradeContext.AAA010 + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if ( records == None or len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "没有查找到代收银行名称"
        return False

    TradeContext.AFC154         =   records[0][0]               #代收银行名称
    AfaLoggerFunc.tradeInfo( ">>>代收银行名称[" + TradeContext.AFC154 + "]")

    AfaLoggerFunc.tradeInfo(TradeContext.AFA052 + TradeContext.AFA032 + TradeContext.AFC154 +"AAAAAAAAAA")

    AfaLoggerFunc.tradeInfo( "********************中台查找数据库结束***************" )
    return True
