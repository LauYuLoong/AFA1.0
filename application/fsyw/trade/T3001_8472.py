#-*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8472.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #从表标志

    #如果不是主办行，不能做此交易
    sqlstr      =   "select brno from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.brno + "'"
    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None:
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "操作数据库异常"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False

    if( len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "不是主办行，不能做此交易"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False

    AfaLoggerFunc.tradeInfo( "********************中台待查票据流水查询开始***************" )
    sqlstr          =   "select AFC401,AFC011,AFC001,nofee from fs_fc74 where afc001 like '%" + TradeContext.findNo + "%' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag !='*' "

    #===条件增加银行编码字段,张恒修改===
    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    AfaLoggerFunc.tradeInfo(sqlstr)
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len( records)==0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "没有查到待查票据流水信息"
        AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
        return False
    else:
        recCnt                  =   len(records)            #记录条数
        TradeContext.RECCNT     =   str ( recCnt )

        #保存数据
        serNoMap                =   {}          #流水号字典，保存流水号码和流水金额的键值对
        NoMap                   =   {}          #缴款书编号字典，保存缴款书编号和缴款书金额的键值对
        for i in range(recCnt):
            if records[i][0] not in serNoMap :
                serNoMap[records[i][0]] =   records[i][1]

            if records[i][2] not in NoMap :
                NoMap[records[i][2]] =   records[i][3]

        #四个用于存放返回前台数据
        AFC401List              =   []
        AFC011List              =   []
        AFC001List              =   []
        NOFEEList               =   []

        #获取流水号码序列
        for item in serNoMap.keys():
            AFC401List.append(item)
            AFC011List.append(serNoMap[item])

        #获取缴款书号码序列
        for item in NoMap.keys():
            AFC001List.append(item)
            NOFEEList.append(NoMap[item])


        AfaLoggerFunc.tradeInfo(serNoMap)
        AfaLoggerFunc.tradeInfo(NoMap)
        #拼字段返回前台
        TradeContext.AFC401     =   ':'.join(AFC401List)
        TradeContext.AFC011     =   ':'.join(AFC011List)
        TradeContext.AFC001     =   ':'.join(AFC001List)
        TradeContext.NOFEE      =   ':'.join(NOFEEList)


        #fields                  =   "AFC401,AFC011,AFC001,NOFEE"
        #
        #index                   =   0                       #字段名下标
        #for field  in fields.split(","):
        #    item                =   []
        #    for i in range(recCnt):
        #        if (field == 'AFC401' or field == 'AFC001' or field == 'NOFEE') and ( records[i][index] in item ):           #流水号码列和缴款书编号列中的项目不能相同
        #            #if (field == 'AFC011' or field == 'NOFEE') and ( records[i][index] in item) :
        #            pass
        #        else:
        #             item.append(records[i][index])
        #
        #    AfaLoggerFunc.tradeInfo( item )
        #    if item == None :
        #        TradeContext.errorCode  =   "0000"
        #        TradeContext.errorMsg   =   "中台待查票据流水查询成功"
        #        return False
        #
        #    value               =   ":".join(item)
        #    setattr(TradeContext,field,value)
        #    index               =   index + 1           #开始下一个字段
        #
        #    AfaLoggerFunc.tradeInfo( "TradeContext." + field + " = " + value )

        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "中台待查票据流水查询成功"

    AfaLoggerFunc.tradeInfo( "********************中台待查票据流水查询结束***************" )
    return True
