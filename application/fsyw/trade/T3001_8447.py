# -*- coding: gbk -*-
##################################################################
#   代收代付平台.报表打印
#=================================================================
#   程序文件:   T3001_8447.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaDBFunc, AfaLoggerFunc, sys, os
from types import *

def printZhou_yuebiao():

    if TradeContext.qryType     ==   '1' :
        fileName    =   TradeContext.busiNo + "_zhoubaobiao.txt"

    elif TradeContext.qryType   ==   '2':
        fileName    =   TradeContext.busiNo + "_yuebaobiao.txt"


    sqlstr  =   "select date from fs_remain where busino='" + TradeContext.busiNo + "' order by date desc"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len(records) == 0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找最后一次对账日期失败"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if TradeContext.edDate > records[0][0].strip():
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "%s没有对账，请先对账" %TradeContext.edDate
        return False

    sqlstr  =   "select * from fs_remain where busino='" + TradeContext.busiNo + "' and date<'" + TradeContext.bgDate + "' order by date desc"
    records = AfaDBFunc.SelectSql( sqlstr )
    if (records==None or len(records) == 0):
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","获取上期余额失败,数据库异常"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

    TradeContext.lastBanlance   =   records[0][2].strip()       #上期余额
    fileDirName     =   os.environ['AFAP_HOME'] + "/data/ahfs/" + fileName

    #统计正常收入
    #sqlStr  = "select date,sum(cast(afc157 as decimal(17,2))),count(date) from fs_fc76 where flag='0' and busino='" + TradeContext.busiNo + "'"
    #sqlStr  = sqlStr + " and date between '" + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by date"

    sqlStr  = "select workdate,sum(cast(amount as decimal(17,2))),count(workdate) from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"
    sqlStr  = sqlStr + " AND NOTE2='1' AND BANKSTATUS='0' and REVTRANF='0'"
    sqlStr  = sqlStr + " and workdate between '" + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by workdate"

    AfaLoggerFunc.tradeInfo(sqlStr)
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None  ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查询正常收入失败"
        AfaLoggerFunc.tradeInfo( "查询正常收入失败"+sqlStr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeInfo( "***************中台报表打印结束*******************" )
        fOutRpt.close()
        return False

    normal_map  =   {}          #正常收入统计表
    for i in range(len(records)):
        normal_map[records[i][0]]   =   [str(records[i][1]),str(records[i][2])]

    AfaLoggerFunc.tradeInfo( '正常数据：' )
    AfaLoggerFunc.tradeInfo( normal_map )

    #统计退付支出
    #sqlStr  = "select date,sum(cast(afc064 as decimal(17,2))),count(date) from fs_fc75 where flag='0' and busino='" + TradeContext.busiNo + "'"
    #sqlStr  = sqlStr + " and date between '" + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by date"

    sqlStr = "SELECT workdate,sum(cast(amount as decimal(17,2))),count(workdate) FROM fs_maintransdtl WHERE APPNO='"    + TradeContext.appNo    + "'  AND BUSINO='"   + TradeContext.busiNo   + "'"
    sqlStr = sqlStr + " and NOTE2='2' AND BANKSTATUS='0' and REVTRANF='0' and chkflag='0' "
    sqlStr  = sqlStr + " and workdate between '" + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by workdate"

    AfaLoggerFunc.tradeInfo( sqlStr )
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None  ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查询退付数据库失败"
        AfaLoggerFunc.tradeInfo( "查询退付数据库失败"+sqlStr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeInfo( "***************中台报表打印结束*******************" )
        fOutRpt.close()
        return False

    tuifu_map   =   {}
    for i in range(len(records)):
        tuifu_map[records[i][0]]   =   [str(records[i][1]).replace('-',''),str(records[i][2])]

    AfaLoggerFunc.tradeInfo( '退付数据：' )
    AfaLoggerFunc.tradeInfo( tuifu_map )

    #统计待查收入
    sqlStr  =   ""
    sqlStr  = "select date,sum(cast(afc011 as decimal(17,2))),count(date) from fs_fc74 where flag!='*' and busino='" + TradeContext.busiNo + "'  "

    #===条件增加银行编码字段,张恒修改===
    sqlStr = sqlStr + " and afa101 = '" + TradeContext.bankbm + "'"

    sqlStr  = sqlStr + "  and date between '"    + TradeContext.bgDate   + "' and '" + TradeContext.edDate + "' group by date"
    AfaLoggerFunc.tradeInfo( "待查数据:" + sqlStr )
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None  ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查询待查数据库失败"
        AfaLoggerFunc.tradeInfo( "查询待查数据库失败"+sqlStr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        AfaLoggerFunc.tradeInfo( "***************中台报表打印结束*******************" )
        fOutRpt.close()
        return False

    daicha_map  =   {}
    for i in range(len(records)):
        daicha_map[records[i][0]]   =   [str(records[i][1]),str(records[i][2])]

    AfaLoggerFunc.tradeInfo( '待查数据：' )
    AfaLoggerFunc.tradeInfo( daicha_map )
    AfaLoggerFunc.tradeInfo( "********************开始画报表***************" )

    #将三个报表中的日期合成，方便打印
    tmpList =   []                      #日期列表
    for item in normal_map.keys():
        if not item in tmpList:
            tmpList.append(item)

    for item in tuifu_map.keys():
        if not item in tmpList:
            tmpList.append(item)

    for item in daicha_map.keys():
        if not item in tmpList:
            tmpList.append(item)

    fOutRpt         =   open(fileDirName,"w")

    lineWidth       =   144             #报表列表宽度
    WidthList       =   [8,14,6,14,6,14,6,14,6,14,6,14]

    #----------------------------------空三行--------------------------------
    fOutRpt.write('\n')
    fOutRpt.write('\n')
    fOutRpt.write('\n')

    if TradeContext.qryType     ==   '1' :
        fOutRpt.write('非税周报表'.center(lineWidth))
    elif TradeContext.qryType   ==   '2':
        fOutRpt.write('非税月报表'.center(lineWidth))

    #----------------------------------空两行---------------------------------------
    fOutRpt.write('\n')
    fOutRpt.write('\n')

    fOutRpt.write( '     制表日期：' + TradeContext.workDate + '\t\t\t' ) #busiAccno
    fOutRpt.write('      上期余额：'  + str(TradeContext.lastBanlance) + '\t\t\t' )
    fOutRpt.write('收款人帐号：' + TradeContext.busiAccno )
    fOutRpt.write('\n')
    fOutRpt.write('     ┌────┬───────────┬───────────┬───────────┬───────────┬───────────┬───────┐'+'\n')
    fOutRpt.write('     │        │       正常收入       │       待查收入       │       退付收入       │       上缴国库       │       上缴专户       │              │'+'\n')
    fOutRpt.write('     │  日期  ├───────┬───┼───────┬───┼───────┬───┼───────┬───┼───────┬───┤    合计      │'+'\n')
    fOutRpt.write('     │        │    金额      │ 笔数 │    金额      │ 笔数 │    金额      │ 笔数 │    金额      │ 笔数 │    金额      │ 笔数 │              │'+'\n')
    fOutRpt.write('     ├────┼───────┼───┼───────┼───┼───────┼───┼───────┼───┼───────┼───┼───────┤'+'\n')

    tmpList.sort()
    banlance    =   float(TradeContext.lastBanlance)
    AfaLoggerFunc.tradeInfo( tmpList )
    for date in tmpList:
        fOutRpt.write( '     │' )
        fOutRpt.write( date.ljust(8) )                      #报表日期
        fOutRpt.write( '│' )


        #如果正常数据中没有当天数据类型，则赋值空
        if  not normal_map.has_key(date):
            fOutRpt.write( ''.ljust(14) )
            fOutRpt.write( '│' )
            fOutRpt.write( ''.ljust(6) )
            fOutRpt.write( '│' )
        else:
            fOutRpt.write( normal_map[date][0].ljust(14) )
            fOutRpt.write( '│' )
            fOutRpt.write( normal_map[date][1].ljust(6) )
            fOutRpt.write( '│' )

            banlance    =   banlance + float( normal_map[date][0] )         #累加金额

        #如果待查数据中没有当天数据类型，则赋值空
        if not daicha_map.has_key(date):
            fOutRpt.write( ''.ljust(14) )
            fOutRpt.write( '│' )
            fOutRpt.write( ''.ljust(6) )
            fOutRpt.write( '│' )
        else:
            fOutRpt.write( daicha_map[date][0].ljust(14) )
            fOutRpt.write( '│' )
            fOutRpt.write( daicha_map[date][1].ljust(6) )
            fOutRpt.write( '│' )

            banlance    =   banlance + float( daicha_map[date][0] )         #累加金额

        #如果退付数据中没有当天数据类型，则赋值空
        if not tuifu_map.has_key(date):
            fOutRpt.write( ''.ljust(14) )
            fOutRpt.write( '│' )
            fOutRpt.write( ''.ljust(6) )
            fOutRpt.write( '│' )
        else:
            fOutRpt.write( tuifu_map[date][0].ljust(14) )
            fOutRpt.write( '│' )
            fOutRpt.write( tuifu_map[date][1].ljust(6) )
            fOutRpt.write( '│' )

            banlance    =   banlance - float( tuifu_map[date][0] )         #累加金额

        #上缴国库
        fOutRpt.write( ''.ljust(14) )
        fOutRpt.write( '│' )
        fOutRpt.write( ''.ljust(6) )
        fOutRpt.write( '│' )

        #上缴专户
        fOutRpt.write( ''.ljust(14) )
        fOutRpt.write( '│' )
        fOutRpt.write( ''.ljust(6) )
        fOutRpt.write( '│' )

        #从余额表中取出余额
        sqlstr  =   "select this from fs_remain where busino='" + TradeContext.busiNo + "' and date='" + date + "'"

        #begin 20100701 蔡永贵增加银行编码
        sqlstr  =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"
        #end

        AfaLoggerFunc.tradeInfo( sqlstr )
        records = AfaDBFunc.SelectSql( sqlstr )
        if( records == None or len( records)==0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "没有查找到%s的余额" %date
            return False

        #fOutRpt.write( str(banlance).ljust(14) )
        fOutRpt.write( records[0][0].rjust(14) )
        fOutRpt.write( '│' )
        fOutRpt.write( '\n' )

        if date != tmpList[len(tmpList)-1] :
            fOutRpt.write('     ├────┼───────┼───┼───────┼───┼───────┼───┼───────┼───┼───────┼───┼───────┤'+'\n')

    fOutRpt.write('     └────┴───────┴───┴───────┴───┴───────┴───┴───────┴───┴───────┴───┴───────┘'+'\n')
    fOutRpt.write('     打印：' + TradeContext.teller + '\t\t\t' + '复核：' + '' + '\n')
    fOutRpt.close()
    TradeContext.FileName       =   fileName
    return True

#柜面缴费表
def printPaybiao():
    fileName        =   "JK" + "_" + TradeContext.busiNo + ".txt"

    #如果是主办行
    if TradeContext.isMainBank  :

        #查询机构不空,查询输入机构
        if TradeContext.fdBrno :
            sqlstr          =   "select bankserno, accno, username,amount,userno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.fdBrno + "' and note2='1' and bankstatus='0' and revtranf='0'  "
            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"
        else:
            sqlstr          =   "select bankserno, accno, username,amount,userno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and note2='1' and bankstatus='0' and revtranf='0' "
            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #如果不是主办行,只能查询当前机构交易
    else:
        sqlstr          =   "select bankserno, accno, username,amount,userno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.brno + "' and note2='1' and bankstatus='0' and revtranf='0' "
        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    AfaLoggerFunc.tradeInfo( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找到缴款信息异常"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False


    #将报表写到文件中去
    if len( records)>=0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        try:
            fileHead    =   ['业务流水号','缴款人账号','缴款人姓名','缴费金额','缴款书编号']
            fileWidth   =   [15,25,40,17,13]
            nWidth      =   130                         #整个文件宽度
            nPageRow    =   50                          #每个文件打印的行数
            needPage    =   len(records)/nWidth         #需要打印的页数  比实际上少一
            hp          =   open(lDir+fileName,"w")

            #------------------空三行--------------------------
            hp.write('\n')
            hp.write('\n')
            hp.write('\n')
            hp.write( '非税柜面缴费流水明细表'.center(nWidth) + '\n' )

            #------------------空两行--------------------------
            hp.write('\n')
            hp.write('\n')

            hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
            hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
            hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )


            #打印表头
            for i in range( len(fileHead) ) :
                hp.write(fileHead[i].ljust( fileWidth[i]) )
            else:
                hp.write('\n')

            #打印横线
            for i in range(nWidth/2):
                hp.write('─')
            else:
                hp.write('\n')

            for i in range( len(records) ):

                tmpList =   list(records[i])
                #如果不需要换页
                if not needPage :
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].ljust(fileWidth[j]))
                    else:
                        hp.write('\n')

                #如果需要换页
                else:

                    #如果当前记录数是50整数倍，则插入换页符
                    if not i % nPageRow :
                        #首先画结束页最后一条横线
                        for j in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                        #换到新的一页，下面开始画新的一页，首先也是固定的表头
                        hp.write( chr(12) )

                        #------------------空三行--------------------------
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '非税柜面缴费流水明细表'.center(nWidth) + '\n' )

                        #------------------空两行--------------------------
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
                        hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )


                        #打印表头
                        for j in range( len(fileHead) ) :
                            hp.write(fileHead[j].ljust( fileWidth[j]) )
                        else:
                            hp.write('\n')

                        #打印横线
                        for j in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].center(fileWidth[j]))
                    else:
                        hp.write('\n')

            else:
                #打印横线
                for j in range(nWidth/2):
                    hp.write('─')
                else:
                    hp.write('\n')

                hp.write('打印：' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('复核：' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "查询柜面缴费信息成功"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "写文件异常"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

#待查表
def printDaichabiao():
    fileName        =   "DC" + "_" + TradeContext.busiNo + ".txt"

    #如果是主办行
    if TradeContext.isMainBank  :

        #查询机构不空,查询输入机构
        if TradeContext.fdBrno :
            sqlstr          =   "select  afc401,afc008,afc006,afc011 from fs_fc74 where flag !='*' and afc016='" + TradeContext.fdBrno + "' and busino='" + TradeContext.busiNo + "'"

            #===条件增加银行编码字段,张恒修改===
            sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and date=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

        #查询机构为空，
        else:
            sqlstr          =   "select  afc401,afc008,afc006,afc011 from fs_fc74 where flag !='*' and busino='" + TradeContext.busiNo + "'"

            #===条件增加银行编码字段,张恒修改===
            sqlstr          =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and date=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + " and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #如果不是主办行,只能查询当前机构交易
    else:
        sqlstr              =   "select  afc401,afc008,afc006,afc011 from fs_fc74 where flag !='*' and afc016='" + TradeContext.brno + "' and busino='" + TradeContext.busiNo + "'"

        #===条件增加银行编码字段,张恒修改===
        sqlstr              =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        if TradeContext.edDate  ==  '00000000':
            sqlstr          =   sqlstr + " and date=" + TradeContext.bgDate + "'"
        else:
            sqlstr          =   sqlstr + "and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找待查信息异常"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if len( records)>=0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        try:
            fileHead    =   ['流水号','缴款人账号','缴款人姓名','缴费金额']
            fileWidth   =   [15,25,25,40,20]
            nWidth      =   130                         #整个文件宽度
            nPageRow    =   50                          #每个文件打印的行数
            needPage    =   len(records)/nWidth         #需要打印的页数  比实际上少一
            hp          =   open(lDir+fileName,"w")
            #----------------空三行---------------
            hp.write('\n')
            hp.write('\n')
            hp.write('\n')
            hp.write( '非税待查流水明细表'.center(nWidth) + '\n' )
            hp.write('\n')
            hp.write('\n')

            hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
            hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
            hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )


            #打印表头
            for i in range( len(fileHead) ) :
                hp.write(fileHead[i].ljust( fileWidth[i]) )
            else:
                hp.write('\n')

            for i in range(nWidth/2):
                hp.write('─')
            else:
                hp.write('\n')


            for i in range(len(records)):
                tmpList =   list(records[i])

                #如果不需要换页
                if not needPage :
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].ljust(fileWidth[j]))
                    else:
                        hp.write('\n')
                #如果需要换页
                else:

                    #如果当前记录数是50整数倍，则插入换页符
                    if not i % nPageRow :

                        #首先画一条横线
                        for i in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                        #换到新的一页，下面开始画新的一页，首先也是固定的表头
                        hp.write( chr(12) )

                        #----------------空三行
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '非税待查流水明细表'.center(nWidth) + '\n' )
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
                        hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )


                        #打印表头
                        for i in range( len(fileHead) ) :
                            hp.write(fileHead[i].ljust( fileWidth[i]) )
                        else:
                            hp.write('\n')

                        for i in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                    #画一条数据
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].center(fileWidth[j]))
                    else:
                        hp.write('\n')

            else:
                #打印下面的横线
                for j in range(nWidth/2):
                    hp.write('─')
                else:
                    hp.write('\n')

                hp.write('打印：' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('复核：' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "查询待查信息成功"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "写文件异常"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

#退付表
def printTuifubiao():
    fileName        =   "TF" + "_" + TradeContext.busiNo + ".txt"

    #查询机构不空,查询输入机构
    if TradeContext.fdBrno :
        sqlstr          =   "select bankserno, userno,username,accno,amount from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' brno='" + TradeContext.fdBrno + "' and note2='2' and bankstatus='0' and revtranf='0'  "
        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"
    else:
        sqlstr          =   "select bankserno, userno,username,accno,amount from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and note2='2' and bankstatus='0' and revtranf='0'  "
        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找到缴款信息异常"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if len( records)>=0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        try:
            fileHead    =   ['业务流水号','退付通知书编号','领款人姓名','领款人帐号','退付金额']
            fileWidth   =   [15,25,40,25,20]
            nWidth      =   130                         #整个文件宽度
            nPageRow    =   50                          #每个文件打印的行数
            needPage    =   len(records)/nWidth         #需要打印的页数  比实际上少一
            hp          =   open(lDir+fileName,"w")

            #----------------空三行
            hp.write('\n')
            hp.write('\n')
            hp.write('\n')
            hp.write( '非税退付流水明细表'.center(nWidth) + '\n' )
            hp.write('\n')
            hp.write('\n')

            hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
            hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
            hp.write( '付款人帐号：' + TradeContext.busiAccno  + '\n' )


            #打印表头
            for i in range( len(fileHead) ) :
                hp.write(fileHead[i].ljust( fileWidth[i]) )
            else:
                hp.write('\n')

            for i in range(nWidth/2):
                hp.write('─')
            else:
                hp.write('\n')


            for i in range(len(records)):
                tmpList =   list(records[i])
                #如果不需要换页
                if not needPage :
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].ljust(fileWidth[j]))
                    else:
                        hp.write('\n')
                #如果需要换页
                else:

                    #如果当前记录数是50整数倍，则插入换页符
                    if not i % nPageRow :

                        #首先画结束页最后一条横线
                        for i in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                        #换到新的一页，下面开始画新的一页，首先也是固定的表头
                        hp.write( chr(12) )

                        #----------------空三行
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '非税待查流水明细表'.center(nWidth) + '\n' )
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
                        hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )


                        #打印表头
                        for i in range( len(fileHead) ) :
                            hp.write(fileHead[i].ljust( fileWidth[i]) )
                        else:
                            hp.write('\n')

                        for i in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                    #画一条数据
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].center(fileWidth[j]))
                    else:
                        hp.write('\n')

            else:
                #打印下面的横线
                for j in range(nWidth/2):
                    hp.write('─')
                else:
                    hp.write('\n')

                hp.write('打印：' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('复核：' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "查询柜面退付信息成功"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "写文件异常"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

#补录表
def printBulubiao():
    #查询机构不空,查询输入机构
    if TradeContext.fdBrno :
        sqlstr          =   "select distinct afc001,afc401,afc008,afc006,amount  from fs_fc84 where busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.fdBrno + "' and flag = '0' "

        #===条件增加银行编码字段,张恒修改===
        sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and date=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #查询所有机构交易
    else:
        sqlstr          =   "select distinct afc001,afc401,afc008,afc006,amount from fs_fc84 where busino='" + TradeContext.busiNo + "' and flag='0' "

        #===条件增加银行编码字段,张恒修改===
        sqlstr = sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and date=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and date between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找补录信息异常"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    fileName    =   "BL_" + TradeContext.busiNo + ".txt"
    if len( records) >= 0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        fileHead    =   ['缴款书编号','业务流水号','缴款人帐号','缴款人姓名','缴费金额']
        fileWidth   =   [15,15,25,40,20]
        nWidth      =   130                         #整个文件宽度
        nPageRow    =   50                          #每个文件打印的行数,这里暂定为50行就换页
        needPage    =   len(records)/nWidth         #需要打印的页数  比实际上少一
        try:
            hp          =   open(lDir+fileName,"w")
            #----------------空三行
            #hp.write('\n')
            #hp.write('\n')
            #hp.write('\n')
            #hp.write( '非税补录流水明细表'.center(nWidth) + '\n' )
            #hp.write('\n')
            #hp.write('\n')
            #
            #hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
            #hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
            #hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )

            i       =   0                           #记录数
            LineNum =   0                           #行数
            for i in range ( len(records) ):
                tmpList     =   list(records[i])

                #首先将数据整理到列表dataList中
                serNoNum    =   len( tmpList[1].strip().split(':') )      #多少流水号码对应一个缴款书编号
                dataList    =   [[]]
                for j in range( serNoNum):
                    tmp     =   tmpList[:]          #列表拷贝
                    tmp[1]  =   (tmpList[1].split(':'))[j]

                    if j != 0:
                        tmp[0]  =   ''
                        tmp[2]  =   ''
                        tmp[3]  =   ''
                        tmp[4]  =   ''

                    dataList.insert(j,tmp)
                else:
                    dataList.pop()

                AfaLoggerFunc.tradeInfo( dataList )

                for j in range( len(dataList) ):
                    if not LineNum % nPageRow :
                        if LineNum != 0:
                            #首先画结束页最后一条横线
                            for i in range(nWidth/2):
                                hp.write('─')
                            else:
                                hp.write('\n')
                            hp.write( chr(12) )


                        #换到新的一页，下面开始画新的一页，首先也是固定的表头

                        #----------------空三行
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '非税补录流水明细表'.center(nWidth) + '\n' )
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
                        hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )


                        #打印表头
                        for i in range( len(fileHead) ) :
                            hp.write(fileHead[i].ljust( fileWidth[i]) )
                        else:
                            hp.write('\n')

                        for i in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                    #画一条数据
                    for k in range( len(fileHead) ):
                        hp.write(dataList[j][k].ljust(fileWidth[k]))

                    else:
                        hp.write('\n')
                    LineNum =   LineNum + 1
            else:
                #打印下面的横线
                for j in range(nWidth/2):
                    hp.write('─')
                else:
                    hp.write('\n')

                hp.write('打印：' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('复核：' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "查询补录信息成功"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "写文件异常"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

#冲正表
def printCZbiao():
    fileName        =   "CZ" + "_" + TradeContext.busiNo + ".txt"

    #如果是主办行
    if TradeContext.isMainBank  :

        #查询机构不空,查询输入机构
        if TradeContext.fdBrno :
            sqlstr          =   "select revagentserno, userno,accno,username,amount,serialno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'and brno='" + TradeContext.fdBrno + "' and bankstatus='0' and revtranf='1' "
            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"
        else:
            sqlstr          =   "select revagentserno, userno,accno,username,amount,serialno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and bankstatus='0' and revtranf='1' "
            if TradeContext.edDate  ==  '00000000':
                sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
            else:
                sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #如果不是主办行,只能查询当前机构交易
    else:
        sqlstr          =   "select revagentserno, userno,accno,username,amount,serialno from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'and brno='" + TradeContext.brno + "' and bankstatus='0' and revtranf='1' "
        if TradeContext.edDate  ==  '00000000':
            sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
        else:
            sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"

    #sqlstr          =   "select revagentserno, accno, userno,amount,worktime,userno,serialno,note3 from fs_maintransdtl where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and note2='2'"
    #if TradeContext.edDate  ==  '00000000':
    #    sqlstr      =   sqlstr + " and workdate=" + TradeContext.bgDate + "'"
    #else:
    #    sqlstr      =   sqlstr + "and workdate between '" + TradeContext.bgDate + "' and '" + TradeContext.edDate + "'"
    #    fileName    =   fileName + "_" + TradeContext.edDate

    AfaLoggerFunc.tradeInfo( sqlstr )

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找冲正信息异常"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if len( records)>=0:
        lDir        =   os.environ['AFAP_HOME'] + '/data/ahfs/'
        try:
            fileHead    =   ['业务流水号','缴款（退付）编号','缴款（领款）人帐号','缴款（领款）人姓名','缴费金额','冲正流水号']
            fileWidth   =   [15,20,25,40,17,8]
            nWidth      =   130                         #整个文件宽度
            nPageRow    =   50                          #每个文件打印的行数
            needPage    =   len(records)/nWidth         #需要打印的页数  比实际上少一
            hp          =   open(lDir+fileName,"w")

            #----------------空三行
            hp.write('\n')
            hp.write('\n')
            hp.write('\n')
            hp.write( '非税冲正流水明细表'.center(nWidth) + '\n' )
            hp.write('\n')
            hp.write('\n')

            hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
            hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
            hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )

            #打印表头
            for i in range( len(fileHead) ) :
                hp.write(fileHead[i].ljust( fileWidth[i]) )
            else:
                hp.write('\n')

            for i in range(nWidth/2):
                hp.write('─')
            else:
                hp.write('\n')


            for i in range(len(records)):
                tmpList =   list(records[i])

                #如果不需要换页
                if not needPage :
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].ljust(fileWidth[j]))
                    else:
                        hp.write('\n')
                #如果需要换页
                else:

                    #如果当前记录数是50整数倍，则插入换页符
                    if not i % nPageRow :
                        #首先画结束页最后一条横线
                        for i in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                        #换到新的一页，下面开始画新的一页，首先也是固定的表头
                        hp.write( chr(12) )

                        #----------------空三行-----------------------
                        hp.write('\n')
                        hp.write('\n')
                        hp.write('\n')
                        hp.write( '非税待查流水明细表'.center(nWidth) + '\n' )
                        hp.write('\n')
                        hp.write('\n')

                        hp.write( '机构名称：'   + TradeContext.I1SBNM + '\t' )
                        hp.write( '制表日期：'   + TradeContext.workDate + '\t' )
                        hp.write( '收款人帐号：' + TradeContext.busiAccno  + '\n' )


                        #打印表头
                        for i in range( len(fileHead) ) :
                            hp.write(fileHead[i].ljust( fileWidth[i]) )
                        else:
                            hp.write('\n')

                        for i in range(nWidth/2):
                            hp.write('─')
                        else:
                            hp.write('\n')

                    #画一条数据
                    for j in range( len(fileHead) ) :
                        hp.write(tmpList[j].center(fileWidth[j]))
                    else:
                        hp.write('\n')
            else:
                #打印下面的横线
                for j in range(nWidth/2):
                    hp.write('─')
                else:
                    hp.write('\n')

                hp.write('打印：' + TradeContext.teller + '\t\t\t\t\t' )
                hp.write('复核：' + '\n' )
                hp.close()
                TradeContext.FileName   =   fileName
                TradeContext.errorCode  =   "0000"
                TradeContext.errorMsg   =   "查询冲正信息成功"
                return True

        except Exception, e:
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "写文件异常"
            AfaLoggerFunc.tradeInfo( str( e ) )
            return False

def SubModuleMainFst( ):
    TradeContext.__agentEigen__  = '0'   #从表标志
    TradeContext.errorCode, TradeContext.errorMsg='0000', '报表查询成功'
    AfaLoggerFunc.tradeInfo( "********************中台报表打印开始***************" )

    #--------------转化日期格式---------------------
    #TradeContext.bgDate =   TradeContext.bgDate[0:4] + '-' + TradeContext.bgDate[4:6] + '-' + TradeContext.bgDate[6:]
    #TradeContext.edDate =   TradeContext.edDate[0:4] + '-' + TradeContext.edDate[4:6] + '-' + TradeContext.edDate[6:]

    #查询日期不能早于签约日期，不能晚于最后一次对账的日期

    #===修改如果为村镇银行则appno为AG2012,张恒修改===
    #if TradeContext.bankbm == '012' :
    #    sqlstr  =   "select startdate from abdt_unitinfo where appno='AG2008' and busino='" + TradeContext.busiNo + "'"
    #else:
    #    sqlstr  =   "select startdate from abdt_unitinfo where appno='AG2012' and busino='" + TradeContext.busiNo + "'"
    sqlstr  =   "select startdate from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len(records) == 0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找有效日期失败"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    if TradeContext.bgDate < records[0][0].strip():
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查询开始日期早于签约开始日期"
        return False



    #查询对公户账户
    sqlstr          =   "select accno from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if( records == None or len(records) == 0 ):
        TradeContext.errorCode  =   "0001"
        TradeContext.errorMsg   =   "查找到对公账户异常"
        AfaLoggerFunc.tradeInfo( sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False

    TradeContext.busiAccno      =   records[0][0]

    AfaLoggerFunc.tradeInfo( "查询当前机构是否是开户行机构" )
    #首先查询当前机构是否是开户行机构
    sqlstr  =   "select brno from abdt_unitinfo where appno='" + TradeContext.appNo + "' and  busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.brno + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records  == None :
        TradeContext.errorCode,TradeContext.errorMsg    =   '0001','查询数据库异常：客户信息表'
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        return False

    if len(records) == 0 :
        TradeContext.isMainBank =   False       #是否是开户行机构
        AfaLoggerFunc.tradeInfo( '不是开户行机构' )
    else:
        TradeContext.isMainBank =   True
        AfaLoggerFunc.tradeInfo( '开户行机构' )

    if TradeContext.qryType == '1' or TradeContext.qryType == '2':
        if TradeContext.isMainBank  :
            return printZhou_yuebiao()
        else:
            TradeContext.errorCode, TradeContext.errorMsg   =   '0001', '不是主办行，不能办理此业务'
            return False

    elif TradeContext.qryType == '3':
        return printPaybiao()
    elif TradeContext.qryType == '4':
        return printDaichabiao()
    elif TradeContext.qryType == '5':
        if TradeContext.isMainBank  :
            return printTuifubiao()
        else:
            TradeContext.errorCode, TradeContext.errorMsg   =   '0001', '不是主办行，不能办理此业务'
            return False
    elif TradeContext.qryType == '6':
        if TradeContext.isMainBank  :
            return printBulubiao()
        else:
            TradeContext.errorCode, TradeContext.errorMsg   =   '0001', '不是主办行，不能办理此业务'
            return False
    elif TradeContext.qryType == '7':
        return printCZbiao()
    else:
        TradeContext.errorCode,TradeContext.errorMsg  =   '0001','选项序号错误'
        return False
