###############################################################################
# -*- coding: gbk -*-
# 文件标识：
# 摘    要：安徽非税
#
# 当前版本：1.0
# 作    者：WJJ
# 完成日期：2007年10月15日
###############################################################################

#表中的状态位 0 待查数据  1非非税
import TradeContext, AfaDBFunc, AfaLoggerFunc, os, sys
from types import *

def SubModuleMainFst( ):

    TradeContext.__agentEigen__  = '0'   #从表标志



    #-----------------------根据单位编码配置获取财政信息----------------------------
    sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
    sqlstr      =   sqlstr + " and bankno ='" + TradeContext.bankbm + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        return False

    elif len(records) > 1:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位信息表异常:一个单位编号对应了多个财政信息"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        return False

    TradeContext.AAA010     =   records[0][0].strip()
    TradeContext.AFA101     =   records[0][1].strip()
    #TradeContext.AAA010 =   '0000000000'
    #TradeContext.AFA101 =   '011'

    try:
        #查询未清分过的
        if TradeContext.opType  ==   '0':

            if( not TradeContext.existVariable( "FileName" ) ):
                TradeContext.errorCode,TradeContext.errorMsg    =   '0001','文件名称为空'
                return False

            fileName = os.environ['AFAP_HOME'] + "/data/ahfs/" + TradeContext.FileName

            AfaLoggerFunc.tradeInfo( '文件名称：' + fileName )
            if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
                AfaLoggerFunc.tradeInfo( '进入查询未清分' )
                fp      =   open(fileName,"r")
                sLine   =   fp.readline()
                while ( sLine ):
                    AfaLoggerFunc.tradeInfo( "********************中台清分查询开始***************" )


                    LineItem    =   sLine.split("<fld>")

                    dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]
                    sqlstr      =   ""
                    sqlstr      =   "select * from fs_fc74 where afc401='" + LineItem[0].strip() + "' and afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "'"
                    sqlstr      =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                    #===条件增加银行编码字段,张恒修改===
                    sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                    AfaLoggerFunc.tradeInfo( sqlstr )
                    records = AfaDBFunc.SelectSql( sqlstr )
                    if( records == None  ):
                        TradeContext.errorCode  =   "0001"
                        TradeContext.errorMsg   =   "查找流水明细表异常"
                        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                        return False

                    #如果没有查到流水号码，则插入一条记录
                    if ( len( records)==0 ):
                        #=====刘雨龙 新增关于收款人账号处理，取businoinfo表中账号====
                        sql2 = "select accno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
                        sql2 = sql2 + " and bankno = '" + TradeContext.bankbm + "'"
                        red = AfaDBFunc.SelectSql( sql2 )
                        if red == None or len(red)==0 :
                            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
                            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                            AfaLoggerFunc.tradeInfo( sql2 )
                            #=====没有则赋空====
                            TradeContext.accno1 = ''

                        #=====赋值====
                        TradeContext.accno1 = red[0][0]

                        AfaLoggerFunc.tradeInfo( '插入流水号码%s' %LineItem[0] )
                        sqlstr      =   ""          #流水号               缴款人名称         缴款人账号  收费金额        银行收款时间
                        sqlstr      =   "insert into fs_fc74 (AFC401,AAA010,AFA101,AFC004,AFC006,AFC007,AFC008,AFC011,AFC015,PAYTIME,AFC016,TELLER,BUSINO,FZPH,AFA091,AFC001,NOFEE,FLAG,DATE,TIME) values ( "

                        dateTmp     =   LineItem[5].strip()
                        dateTmp     =   dateTmp[0:4] + '-' + dateTmp[4:6] + '-' + dateTmp[6:8]

                        sqlstr      =   sqlstr  + "'" +  LineItem[0].strip()         + "',"         #流水号
                        sqlstr      =   sqlstr  + "'" +  TradeContext.AAA010         + "',"         #财政区划内码
                        sqlstr      =   sqlstr  + "'" +  TradeContext.AFA101         + "',"         #银行外码

                        #=====刘雨龙 20080825 修改关于收款人账号的处理====
                        #sqlstr      =   sqlstr  + "'" +  ''                         + "',"         #收款人帐号
                        sqlstr      =   sqlstr  + "'" +  TradeContext.accno1           + "',"         #收款人帐号

                        sqlstr      =   sqlstr  + "'" +  LineItem[1].strip()         + "',"         #交款人名
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #缴款人开户行
                        sqlstr      =   sqlstr  + "'" +  LineItem[2].strip()         + "',"         #缴款人帐号
                        sqlstr      =   sqlstr  + "'" +  LineItem[3].strip()         + "',"         #收费金额
                        sqlstr      =   sqlstr  + "'" +  dateTmp                     + "',"         #收款日期
                        sqlstr      =   sqlstr  + "'" +  LineItem[4].strip()         + "',"         #收款时间
                        sqlstr      =   sqlstr  + "'" +  TradeContext.brno           + "',"         #银行网点

                        sqlstr      =   sqlstr  + "'" +  TradeContext.teller         + "',"         #柜员号
                        sqlstr      =   sqlstr  + "'" +  TradeContext.busiNo         + "',"         #单位编号
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #支票号
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #大厅外码
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #缴款书编号
                        sqlstr      =   sqlstr  + "'" +  ''                          + "',"         #缴款书金额
                        sqlstr      =   sqlstr  + "'" +  '*'                         + "',"         #标志位,初始化为未处理状态
                        sqlstr      =   sqlstr  + "'" +  '00000000'                  + "',"         #日期
                        sqlstr      =   sqlstr  + "'" +  TradeContext.workTime       + "')"         #时间


                        if( AfaDBFunc.InsertSql( sqlstr ) < 1 ):
                            AfaDBFunc.RollbackSql( )
                            AfaLoggerFunc.tradeInfo( "插入数据库失败" )
                            AfaLoggerFunc.tradeInfo(sqlstr)
                            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                            TradeContext.errorCode  =   "0001"
                            TradeContext.errorMsg   =   "插入流水表失败"
                            return False

                        AfaDBFunc.CommitSql( )
                    #else:
                    #    AfaLoggerFunc.tradeInfo('更新流水号码%s日期' %LineItem[0])
                    #    sqlstr      =   "update fs_fc74 set date='" + TradeContext.workDate + "' where afc401='" + LineItem[0].strip() + "'"
                    #    if( AfaDBFunc.UpdateSql( sqlstr ) < 1 ) :
                    #        AfaDBFunc.RollbackSql()
                    #        TradeContext.errorCode, TradeContext.errorMsg='0001', '更新待查数据表失败'
                    #        AfaLoggerFunc.tradeInfo( sqlstr )
                    #        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                    #        return False
                    #
                    #    AfaDBFunc.CommitSql( )

                    sLine   =   fp.readline()

                #从数据库中查询出来数据，写到文件中去
                sqlstr  =   ""
                #sqlstr  =   "select FLAG,SERNO,PAYAMOUNT,PAYACCNO,PAYER,PAYDATE,PAYTIME from fs_detail where date='" + TradeContext.workDate + "' and busino='" + TradeContext.busiNo + "' and flag = '1'"

                dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]

                #当前状态、流水号、收费金额、缴款人账号、缴款人名称、收款日期、银行收款时间
                sqlstr  =   "select flag,afc401,afc011,afc008,afc006,afc015,paytime from fs_fc74 where afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag='*'  and date='00000000' "

                #===条件增加银行编码字段,张恒修改===
                sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

                AfaLoggerFunc.tradeInfo( sqlstr )
                records = AfaDBFunc.SelectSql( sqlstr )
                if( records == None  ):
                    TradeContext.errorCode  =   "0001"
                    TradeContext.errorMsg   =   "查找流水信息失败"
                    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                    AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
                    return False

                else:
                    #将数据写到文件中去
                    lDir        =   os.environ['AFAP_HOME'] + "/data/ahfs/"             #本地目录
                    fName       =   "DOWN_8474_" + TradeContext.busiNo + ".txt"         #文件名称

                    try:
                        hp      =   open(lDir+fName,"w")

                        hp.write( str(len(records)) + "\n" )
                        i       =   0
                        while( i < len(records) ):
                            lineList    =   list(records[i])

                            if lineList[0]   ==  '*':
                                lineList[0]  =   '1'

                            #转化日期格式将0000-00-00转化为00000000
                            lineList[5]  =   lineList[5].replace('-','')

                            hp.write( "|".join( lineList ) )
                            if i != len(records) -1 :
                                hp.write( "\n" )

                            i = i + 1
                        else:
                            hp.close()
                            TradeContext.downFileName   =   fName

                    except Exception, e:
                        AfaLoggerFunc.tradeInfo( str(e) )
                        TradeContext.errorCode  =   "0001"
                        TradeContext.errorMsg   =   "写文件异常"
                        return False

            else:
                AfaLoggerFunc.tradeInfo( "文件" + fileName + "不存在" )
                TradeContext.errorCode  =   "0002"
                TradeContext.errorMsg   =   "没有找到上传文件"
                return False

        #查询已经清分的
        else:
            AfaLoggerFunc.tradeInfo( '进入查询清分' )
            sqlstr  =   ""
            dateTmp     =   TradeContext.serDate[0:4] + '-' + TradeContext.serDate[4:6] + '-' + TradeContext.serDate[6:8]
            sqlstr  =   "select flag,afc401,afc011,afc008,afc006,afc015,paytime from fs_fc74 where afc015='" + dateTmp + "' and busino='" + TradeContext.busiNo + "' and afc016='" + TradeContext.brno + "' and flag='1' "

            #===条件增加银行编码字段,张恒修改===
            sqlstr  =   sqlstr + " and afa101 = '" + TradeContext.bankbm + "'"

            #判断流水号码是否为空,空则返回当天所有记录，不空，只是返回流水号的记录
            if  TradeContext.serNo :
                sqlstr  =   sqlstr + " and afc401='" + TradeContext.serNo + "'"

            AfaLoggerFunc.tradeInfo( '进入查询清分1' )
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "查找流水信息失败"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( sqlstr + AfaDBFunc.sqlErrMsg )
                return False

            else:
                #将数据写到文件中去
                lDir        =   os.environ['AFAP_HOME'] + "/data/ahfs/"         #本地目录
                fName       =   "DOWN_8474_" + TradeContext.busiNo + "_" + TradeContext.teller + ".txt"  #文件名称

                try:
                    hp      =   open(lDir+fName,"w")
                    hp.write(str( len(records) ) + "\n" )
                    i       =   0
                    while( i < len(records) ):
                        tmpList =   list(records[i])
                        if  tmpList[0]   ==  '1':
                            tmpList[0]  =   '0'
                        elif tmpList[0]   ==  '*':
                            tmpList[0]  =   '1'

                        #转化日期格式将0000-00-00转化为00000000
                        tmpList[5]  =   tmpList[5].replace('-','')

                        hp.write( "|".join( tmpList) )
                        if i != len(records) -1 :
                            hp.write( "\n" )

                        i = i + 1
                    else:
                        hp.close()
                        TradeContext.downFileName   =   fName

                except Exception, e:
                    AfaLoggerFunc.tradeInfo( str(e) )
                    TradeContext.errorCode  =   "0001"
                    TradeContext.errorMsg   =   "写文件异常"
                    return False

        AfaLoggerFunc.tradeInfo( "********************中台清分查询结束***************" )
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "清分查询成功"
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode  =   "0003"
        TradeContext.errorMsg   =   "清分查询异常"
        return True

    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        TradeContext.errorCode  =   "0003"
        TradeContext.errorMsg   =   "清分查询异常"
        return False

