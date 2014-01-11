# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8478.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaLoggerFunc, AfaDBFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #从表标志

    AfaLoggerFunc.tradeInfo( "中台单位编码信息维护开始" )

    #判断操作类型
    if TradeContext.opType == '1':
        AfaLoggerFunc.tradeInfo( "新增" )

        sqlstr  =   "select * from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
        sqlstr  =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        if records == None :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "查找单位编码信息异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        if len(records) >=1 :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "已经查找到单位编码信息，不能再次新建"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        #首先校验输入账户和名称是否正确
        #张恒修改AG2012
        sqlstr  =   "select accno,businame from abdt_unitinfo where appno ='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"
        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None or len( records)==0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "没有查找到单位编码账户信息"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        else:
            if records[0][0].strip() != TradeContext.accno  or records[0][1].strip() and records[0][1].strip() != TradeContext.name :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "单位编码账户信息不符"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

        #校验输入银行编码和银行名称是否正确
        sqlstr  =   "select afa102 from fs_fa22 where afa101='" + TradeContext.bankNo + "'"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "查找到单位编码账户信息异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        if len(records) == 0:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "银行编码不存在"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        else:
            #=====刘雨龙  20080815  新增关于处理银行编码相同多条记录的处理====
            for i in range(0,len(records)):
                if records[i][0].strip() != TradeContext.bankName :
                    TradeContext.errorCode = '0011'
                    TradeContext.errorMsg  = '银行编码与银行名称不符'
                    AfaLoggerFunc.tradeInfo('>>>银行名称['+str(records[i][0])+']与柜员上送银行名称['+TradeContext.bankName+']不符')
                    if int(len(records)-1) == i:
                        return False
                else:
                    AfaLoggerFunc.tradeInfo('>>>银行名称['+str(records[i][0])+']与柜员上送银行名称['+TradeContext.bankName+']相符')
                    break

            #if records[0][0].strip() != TradeContext.bankName :
            #    TradeContext.errorCode  =   "0001"
            #    TradeContext.errorMsg   =   "银行编码与银行名字不符"
            #    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            #    return False

        #校验财政区划信息
        sqlstr  =   "select aaa012 from fs_aa11 where aaa010='" + TradeContext.AAA010 + "'"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        records = AfaDBFunc.SelectSql( sqlstr )
        AfaLoggerFunc.tradeInfo(str(records))
        if( records == None ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "查找到单位编码财政区划信息异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        if len(records) == 0:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "财政区划内码不存在"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        else:
            if records[0][0].strip() != TradeContext.AAA012 :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "财政区划内码与财政区划名称不符"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( records[0][0].strip() )
                return False

        #通过校验，插入到数据库中
        sqlstr  =   "insert into fs_businoinfo ( BUSINO,ACCNO,NAME,AAA010,AAA012,BANKNO,BANKNAME,BANKBRNO,BRNO,TELLER,DATE,TIME,CTRYBANKNO,CTRYBANKNAME ) values("

        sqlstr  =   sqlstr + "'" + TradeContext.busiNo      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.accno       + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.name        + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.AAA010      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.AAA012      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.bankNo      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.bankName    + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.busiNo[0:10]+ "',"
        sqlstr  =   sqlstr + "'" + TradeContext.brno        + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.teller      + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.workDate    + "',"
        sqlstr  =   sqlstr + "'" + TradeContext.workTime    + "',"
        sqlstr  =   sqlstr + "'',"
        sqlstr  =   sqlstr + "'')"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        if( AfaDBFunc.InsertSql( sqlstr ) < 1 ):
                AfaDBFunc.RollbackSql( )
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'插入单位编码信息表失败' + sqlstr
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

        AfaDBFunc.CommitSql( )

    #修改
    elif TradeContext.opType == '2':
        AfaLoggerFunc.tradeInfo( "修改" )

        sqlstr  =   "update fs_businoinfo set accno='" + TradeContext.accno + "',name='" + TradeContext.name + "',"  + \
        "aaa010='" + TradeContext.AAA010 + "',aaa012='" + TradeContext.AAA012 + "',date='" + TradeContext.workDate + "'," + \
        "time='" + TradeContext.workTime + "',brno='" + TradeContext.brno + "',teller='" + TradeContext.teller + "'," + \
        "bankno = '" + TradeContext.bankNo + "' where busino='" + TradeContext.busiNo + "'"
        #=====刘雨龙 20080821 新增修改参数====

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        if( AfaDBFunc.UpdateSql( sqlstr ) < 1 ):
                AfaDBFunc.RollbackSql( )
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'更新单位编码信息表失败' + sqlstr
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

        AfaDBFunc.CommitSql( )

    #删除
    elif TradeContext.opType == '3':
        AfaLoggerFunc.tradeInfo( "删除" )

        sqlstr = "delete from fs_businoinfo where busino='" + TradeContext.busiNo + "'"

        AfaLoggerFunc.tradeInfo('>>>sql=' + sqlstr)

        if( AfaDBFunc.DeleteSql( sqlstr ) < 1 ):
                AfaDBFunc.RollbackSql( )
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'删除单位编码信息表失败' + sqlstr
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

        AfaDBFunc.CommitSql( )

    TradeContext.errorCode,TradeContext.errorMsg    =   "0000",'操作单位编码信息表成功'
    AfaLoggerFunc.tradeInfo( "********************中台单位编码信息维护结束***************" )
    return True
