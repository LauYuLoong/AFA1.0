# -*- coding: gbk -*-
##################################################################
#   代收代付平台.代收查询交易
#=================================================================
#   程序文件:   T3001_8442.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #从表标志

    #------------------------数据格式转化--------------
    tmpDataList             =   [k for k in TradeContext.AFC001.split(':') if k]     #将前台上送字段AFC001,可能为 1::::2::::3这样的结构，这两行代码将空的去掉，最终变成1:2:3这样的结构
    TradeContext.AFC001     =   ':'.join(tmpDataList)

    tmpDataList             =   [k.strip() for k in TradeContext.NOFEE.split(':') if ( k.strip() != '0.00' and k.strip() != '' )]     #将前台上送字段AFC001,可能为 1::::2::::3这样的结构，这两行代码将空的去掉，最终变成1:2:3这样的结构
    TradeContext.NOFEE      =   ':'.join(tmpDataList)

    tmpDataList             =   [k for k in TradeContext.AFC401.split(':') if k]     #将前台上送字段AFC001,可能为 1::::2::::3这样的结构，这两行代码将空的去掉，最终变成1:2:3这样的结构
    TradeContext.AFC401     =   ':'.join(tmpDataList)

    tmpDataList             =   [k.strip() for k in TradeContext.AFC011.split(':') if ( k.strip() != '0.00' and k.strip() != '' )]     #将前台上送字段AFC001,可能为 1::::2::::3这样的结构，这两行代码将空的去掉，最终变成1:2:3这样的结构
    TradeContext.AFC011      =   ':'.join(tmpDataList)

    AfaLoggerFunc.tradeInfo( '缴款书编号：' + TradeContext.AFC001 )
    AfaLoggerFunc.tradeInfo( '缴款书金额：' + TradeContext.NOFEE )

    AfaLoggerFunc.tradeInfo( '流水号码：' + TradeContext.AFC401 )
    AfaLoggerFunc.tradeInfo( '流水金额：' + TradeContext.AFC011 )

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

    #if ( not TradeContext.AFC401 ):
    #    TradeContext.errorCode,TradeContext.errorMsg    =   "0002","流水号码不能空"
    #    return False

    AfaLoggerFunc.tradeInfo( "********************中台勾对开始***************" )

    #---------------------------勾对之前确定是否清分过，如果没有清分过不允许做勾对交易
    for item in TradeContext.AFC401.split(":"):
        sqlstr  =   "select * from fs_fc74 where afc401 like '%" + item + "%' and flag ='*' and afc015='" + TradeContext.AFC015 + "' and BUSINO='" + TradeContext.busiNo + "'"

        #===条件增加银行编码字段,张恒修改===
        sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        records = AfaDBFunc.SelectSql( sqlstr )
        if records == None:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "操作数据库异常"
            AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
            return False

        if( len( records)>0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "流水号%s没有做清分不能勾对" %item
            AfaLoggerFunc.tradeInfo(sqlstr+AfaDBFunc.sqlErrMsg)
            return False

    #----------------------------勾对之前确定是否缴过费，如果缴过费不允许勾对--------------------
    AfaLoggerFunc.tradeInfo( '判断缴款书编号是否缴过费' )
    for item in TradeContext.AFC001.split(":"):
        sqlstr  =   "select flag from fs_fc76 where afc001='" + item + "'"


        #===条件增加银行编码字段,张恒修改===
        sqlstr  =   sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"

        records = AfaDBFunc.SelectSql( sqlstr )
        if ( len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( "缴款书编号没有缴费%s可以勾对" %item )
            AfaLoggerFunc.tradeInfo( sqlstr )
        else:
            if records[0][0]   ==  '0':
                TradeContext.errorCode,TradeContext.errorMsg  =   '0001','交款书编号%s已经缴费不能勾对' %item
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

    #------------------------------如果操作类型是新建，首先检验是否勾对过，添加到数据库中---------------------
    if TradeContext.opType == '1':
        for item in TradeContext.AFC401.split(":"):
            #-----------------检测流水号码是否勾对过--------------------
            sqlstr = "select afc001 from fs_fc74 where afc401 = '" + item + "' and afc015='" + TradeContext.AFC015 + "' and BUSINO='" + TradeContext.busiNo +  "' and length(afc001)=0 and flag!='*'"

            #===条件增加银行编码字段,张恒修改===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            records = AfaDBFunc.SelectSql( sqlstr )

            if( records == None ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "数据库异常：待查表"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            if(  len( records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "流水号码%s已经勾对过" %item
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( sqlstr )
                return False

        for payNo in TradeContext.AFC001.split(':'):
            #------------------检测缴款书编号是否勾对过--------------------
            sqlstr = "select afc001 from fs_fc74 where afc001 like '%" + payNo + "%' and flag!='*' and BUSINO='" + TradeContext.busiNo +  "'"

            #===条件增加银行编码字段,张恒修改===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            records = AfaDBFunc.SelectSql( sqlstr )

            if( records == None ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "数据库异常：待查表"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            if(  len( records)>0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "缴款书编号%s已经勾对过" %payNo
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

        #-------------------将数据添加到数据库中------------------------------------
        for item in TradeContext.AFC401.split(":"):
            sqlstr      =   "update fs_fc74 set afc001='" + TradeContext.AFC001  + "',nofee='" + TradeContext.NOFEE + "',flag='0' where afc401='" + item + "' and afc015='" + TradeContext.AFC015 + "' and BUSINO='" + TradeContext.busiNo +  "'"

            #===条件增加银行编码字段,张恒修改===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            AfaLoggerFunc.tradeInfo( sqlstr )
            if( AfaDBFunc.UpdateSql( sqlstr ) < 1 ) :
                AfaDBFunc.RollbackSql()
                TradeContext.errorCode, TradeContext.errorMsg='0001', '更新待查数据表失败'
                AfaLoggerFunc.tradeInfo( sqlstr+AfaDBFunc.sqlErrMsg )
                return False

            AfaDBFunc.CommitSql( )

    #-------------操作类型是删除----------------
    elif TradeContext.opType == '2':

        #------------------------------删除待查表中的数据---------------------------
        for item in TradeContext.AFC401.split(":"):
            sqlstr      =   "update fs_fc74 set afc001='',nofee='',flag='1' where afc401='" + item + "' and afc015='" + TradeContext.AFC015 + "'"

            #===条件增加银行编码字段,张恒修改===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            AfaLoggerFunc.tradeInfo( sqlstr )
            if( AfaDBFunc.UpdateSql( sqlstr ) < 1 ) :
                AfaDBFunc.RollbackSql()
                TradeContext.errorCode, TradeContext.errorMsg='0001', '更新待查数据表失败'
                AfaLoggerFunc.tradeInfo( sqlstr+AfaDBFunc.sqlErrMsg )
                return False

            AfaDBFunc.CommitSql( )

        #-----------------------开始删除补录表中的数据-------------------------------
        sqlstr  =   "select afc401,date from fs_fc84 where afc001='"

        for payNo in TradeContext.AFC001.split(':'):
            sqlstr      =   "select afc401,date from fs_fc84 where"
            condition   =    " afc001='" + payNo + "'"

            for serNo in TradeContext.AFC401.split(':'):
                condition  =   condition + " and afc401 like '%" + serNo + "%'"
             
            #begin 20100625 蔡永贵增加查询条件 
            condition   = condition + " and afa101 = '" + TradeContext.bankbm + "'"
            #end
   
            sqlstr      =   sqlstr + condition

            #===条件增加银行编码字段,张恒修改===
            #sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            AfaLoggerFunc.tradeInfo( '数据库长度：' + str( len(records) ) )

            if len(records) == 0:
                AfaLoggerFunc.tradeInfo( '没有查找到补录信息不用删除' )
                continue

            #---------------------------不能删除以前已经上传的补录数据---------------------------
            if records[0][1].strip() < TradeContext.workDate :
                TradeContext.errorCode,TradeContext.errorMsg    =   '0001','该数据已经上传不能删除'
                return False

            #查找到了补录信息则删除流水号
            if( len( records) == 1 ):

                sqlstr  =   "delete from fs_fc84 where " + condition

                #===条件增加银行编码字段,张恒修改===
                #sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                AfaLoggerFunc.tradeInfo( sqlstr )
                if( AfaDBFunc.DeleteSql( sqlstr ) < 1 ) :
                    AfaDBFunc.RollbackSql()
                    TradeContext.errorCode, TradeContext.errorMsg='0001', '删除补录数据失败'
                    AfaLoggerFunc.tradeInfo( sqlstr+AfaDBFunc.sqlErrMsg )
                    return False

                AfaDBFunc.CommitSql( )
                AfaLoggerFunc.tradeInfo( '删除补录数据成功，该缴款书编号:%s' %payNo )

            #如果查找出来的记录条数大于1，则说明补录数据错误
            elif len( records) > 1 :
                AfaLoggerFunc.tradeInfo( '补录数据错误，缴款书编号，流水号码对应了两条以上记录' )
                AfaLoggerFunc.tradeInfo( '缴款书编号' + payNo )
                AfaLoggerFunc.tradeInfo( '流水号码' + TradeContext.AFC401 )
                TradeContext.errorCode, TradeContext.errorMsg='0000', '勾对删除失败'
                return False
    else:
        TradeContext.errorCode, TradeContext.errorMsg='0001', '操作类型异常'
        AfaLoggerFunc.tradeInfo( sqlstr+AfaDBFunc.sqlErrMsg )
        return False

    TradeContext.errorCode, TradeContext.errorMsg='0000', '勾对数据成功'
    AfaLoggerFunc.tradeInfo( "********************中台勾对结束***************" )
    return True
