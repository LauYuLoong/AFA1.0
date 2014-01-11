# -*- coding: gbk -*-
##################################################################
#   代收代付平台.退付交易
#=================================================================
#   程序文件:   4102_8444.py
#   修改时间:   2007-10-11
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc,AfaFlowControl
from types import *

def SubModuleDoFst():

    AfaLoggerFunc.tradeInfo( '退付开始' )


    #=====刘雨龙  20080811  新增查找fa15表中财政区划内码,条件为单位内码====
    #sql = "select AAA010 from fs_fa15 where AFA050='" + TradeContext.busiNo + "'"
    sql = "select AAA010 from fs_fa22 where busino='" + TradeContext.busiNo + "'"
    
    #begin 20100629 蔡永贵增加查询条件
    sql = sql + " and AFA101 = '" + TradeContext.bankbm + "'"
    AfaLoggerFunc.tradeInfo( sql )
    #end

    ret = AfaDBFunc.SelectSql( sql )
    if ret == None:
        return AfaFlowControl.ExitThisFlow('0001','通过单位内码查找财政区划内码失败')
    elif len(ret) <= 0:
        return AfaFlowControl.ExitThisFlow('0001','通过单位内码查找财政区划内码无满足条件记录')
    else:
        TradeContext.AAA010  =  ret[0][0]


    TradeContext.__agentEigen__ = '0'   #从表标志

    #将字段转化为退付交易所使用的字段
    TradeContext.AFC060         =   TradeContext.userNo
    TradeContext.AFA050         =   TradeContext.note1
    TradeContext.AFC064         =   TradeContext.amount
    TradeContext.AFC063         =   TradeContext.accno

    #=====刘雨龙  20080811  新增条件财政区划内码====
    #sqlstr                      =   "select flag from fs_fc75 where afc060='" + TradeContext.AFC060 + "'"
    sqlstr                      =   "select flag from fs_fc75 where afc060='" + TradeContext.AFC060 + "'"

    sqlstr = sqlstr + " and AAA010 = '" + TradeContext.AAA010 + "'"

    #===条件增加银行编码字段,张恒修改===
    sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

    records                     =   AfaDBFunc.SelectSql( sqlstr )

    AfaLoggerFunc.tradeInfo( '退付查询' + sqlstr )

    if ( len(records) > 0 ):
        if records[0][0]   ==  '0':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0001','已经查找到了退付编号，不能再次退付'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False


        elif records[0][0] != '1':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0002',"缴款书状态位异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

    return True


def SubModuleDoFstMore():

    #将借贷放帐号互换
    tmp                         =   TradeContext.accno
    TradeContext.accno          =   TradeContext.__agentAccno__     #借方
    TradeContext.__agentAccno__ =   tmp
    #begin 20100701 蔡永贵增加
    TradeContext.Daccno         =   tmp                             #贷方
    #end
    
    AfaLoggerFunc.tradeInfo("借方账号:" + TradeContext.accno)
    AfaLoggerFunc.tradeInfo("贷方账号:" + TradeContext.__agentAccno__)

    if TradeContext.vouhNo :
        TradeContext.vouhType   =   TradeContext.vouhNo[0:2]
        TradeContext.vouhNo     =   TradeContext.vouhNo[2:]
    else:
        TradeContext.vouhType   =   '99'
    return True


def SubModuledoSnd():

    #在退付信息写到本地数据库里面
    sqlstr  =   "insert into FS_FC75(AAA010,AFC060,AFC041,AFA050,AFC061,AFC062,AFC063,AFC064,FBLRQ,AFA101,BUSINO,TELLER,BRNO,FLAG,DATE,TIME) values("
    FLAG    =   '0'
    sqlstr          =   sqlstr + "'" + TradeContext.AAA010   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC060   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC041   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFA050   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC061   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC062   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC063   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.AFC064   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.FBLRQ    + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.bankbm   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.busiNo   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.teller   + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.brno     + "',"
    sqlstr          =   sqlstr + "'" + FLAG                  + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.workDate + "',"
    sqlstr          =   sqlstr + "'" + TradeContext.workTime + "')"

    TradeContext.errorCode  =   "0000"
    TradeContext.errorMsg   =   "退付成功"

    if( AfaDBFunc.InsertSql( sqlstr ) < 1 ):
        AfaDBFunc.RollbackSql( )
        AfaLoggerFunc.tradeInfo( '插入退付信息表失败' + sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "退付失败"
        return False

    AfaDBFunc.CommitSql( )

    AfaLoggerFunc.tradeInfo( '插入退付信息表结束' )


    #本模块主要是为了填写发票数据
    if (TradeContext.channelCode =='001' ): #柜面交易不计发票
        TradeContext.__billSaveCtl__  = '0'
    else:
        TradeContext.__billSaveCtl__  = '1'

    bill    =   []
    bill.append('1')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')
    bill.append('')

    return bill
