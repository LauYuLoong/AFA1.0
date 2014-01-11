# -*- coding: gbk -*-
##################################################################
#   代收代付平台.
#=================================================================
#   程序文件:   3001_8443.py
#   修改时间:   2007-10-21
##################################################################
import TradeContext, AfaLoggerFunc, AfaDBFunc

from types import *

def SubModuleMainFst():

    TradeContext.__agentEigen__ = '0'   #从表标志

    #如果不是主办行，不能做此交易
    AfaLoggerFunc.tradeInfo('检验是否是主办行')

    sqlstr = "select brno from abdt_unitinfo where appno='" + TradeContext.appNo + "' and busino='" + TradeContext.busiNo + "' and brno='" + TradeContext.brno + "'"

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

    #首先从库表中查询缴款书编号，如果查找到则返回已经缴费的错误
    AfaLoggerFunc.tradeInfo('缴款书是否已经缴费')

    sqlstr = "select flag from fs_fc76 where afc001='" + TradeContext.AFC001 + "'"

    #===条件增加银行编码字段,张恒修改===
    sqlstr = sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )
    if ( len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( "没有查找到缴款书编号可以缴费"+sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )

    else:
        if records[0][0]   ==  '0':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0001','已经查找到了交款书编号，不能再缴费'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        elif records[0][0]   ==  '1':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0002',"缴款书已冲正，可缴费"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        else:
            TradeContext.errorCode,TradeContext.errorMsg  =   '0003',"缴款书状态位异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False


    #查询缴款书标号,还有对应流水是否已经补录过
    AfaLoggerFunc.tradeInfo('是否已经补录过')
    for serNo in TradeContext.AFC401.split(':') :
        sqlstr  =   "select * from fs_fc84 where afc001='" + TradeContext.AFC001 + "' and afc401 like '%" + serNo + "%'"

        AfaLoggerFunc.tradeInfo( sqlstr )
        records = AfaDBFunc.SelectSql( sqlstr )
        if( len( records) > 0 ):
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "该缴款书已经补录，不能再次补录"
            return False

    AfaLoggerFunc.tradeInfo( '********************插入补录数据表开始*******************' )

    #-----------------------根据单位编码配置获取财政信息----------------------------
    sqlstr      =   "select aaa010,bankno from fs_businoinfo where busino='" + TradeContext.busiNo + "'"
    sqlstr      =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"
    records = AfaDBFunc.SelectSql( sqlstr )
    if records == None or len(records)==0 :
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","查找单位信息表异常"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        sys.exit(1)

    elif len(records) > 1:
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位信息表异常:一个单位编号对应了多个财政信息"
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        AfaLoggerFunc.tradeInfo( sqlstr )
        sys.exit(1)

    TradeContext.AAA010     =   records[0][0].strip()
    TradeContext.AFA101     =   records[0][1].strip()

    #TradeContext.AAA010 =   "0000000000"
    TradeContext.AAA011 =   ""
    TradeContext.AFC016 =   TradeContext.brno

    # ----------------------------开始票据信息校验-------------------------------

    #是否串票的校验
    piaoNo      =   TradeContext.AFC001[0:9]
    aaz010      =   TradeContext.AAA010             #财政区划内码
    sqlstr      =   "select * from fs_dpz_gl where fczqhnm='" + aaz010 + "'"
    AfaLoggerFunc.tradeInfo( sqlstr )
    records     =   AfaDBFunc.SelectSql(sqlstr)

    #=====add by pgt 20090423 根据前台传上来的校验标志来判断是否进行校验====
    if (len(records) > 0   and  (TradeContext.CKMD == "1")):

        #大厅模式
        if (TradeContext.existVariable('AFA091' ) and len(TradeContext.AFA091)>0):
            AfaLoggerFunc.tradeInfo( "串票校验--大厅模式" )
            sqlstr  =   "select afa090 from fs_fa20 where afa091='" + TradeContext.AFA091 + "' and BUSINO='" + TradeContext.busiNo + "'"
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None  or len(records)==0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "数据库异常,FS_FA20表"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            afa090  =   records[0][0]           #大厅内码

            sqlstr  =   "select count(*) from fs_dpz_gl where fdwdm='" + afa090 + "' and fqshm<='" + piaoNo + "' and fqzhm>='" + piaoNo + "'"

            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None  ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "串票校验异常"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            if  int(records[0][0]) == 0 :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "非本大厅票据,请检查票号"
                return False

        else:
            #非大厅模式
            AfaLoggerFunc.tradeInfo( "串票校验--非大厅模式" )
            sqlstr  =   "select count(*) from (select distinct b.AFA051 from FS_DPZ_GL a,fs_fa15 b where a.fdwdm=b.AFA050 and a.FQSHM<='" + piaoNo + "' and a.FQZHM>='" + piaoNo +  "'" + \
            " union all select distinct c.AFA051 from FS_DPZ_GL a,fs_fa21 b,fs_fa15 c where a.FQSHM<='" + piaoNo + "' and a.FQZHM>='" + piaoNo + "' and a.fdwdm=b.AFA050 and b.AFA050=c.AFA050) a where locate(a.afa051, '" + TradeContext.AFA051 + "')=1"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None  ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "串票校验异常"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            if  int(records[0][0]) == 0 :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "非本执收单位票据,请检查票号"
                return False

    AfaLoggerFunc.tradeInfo("单位在此开票日期内是否有权收取此项目")


    #单位日期是否合法
    sql         =   "select aaz006,aaz007,afa050,AAZ002 from fs_fa15 where afa051='" + TradeContext.AFA051 + "' and BUSINO='" + TradeContext.busiNo + "'"
    sql  =  sql + " and aaa010='" + TradeContext.AAA010 + "' order by aaz002 desc"

    AfaLoggerFunc.tradeInfo(sql)
    records     =   AfaDBFunc.SelectSql( sql )
    if ( records == None ):
        AfaLoggerFunc.tradeInfo(sql)
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","数据库异常:查询单位信息表"
        AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
        return False

    if ( len(records) == 0 ):
        TradeContext.errorCode,TradeContext.errorMsg    =   "0001","没有此单位"
        AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
        return False
    else:
        iFlag=0
        if (records[0][3]!='1'):
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位不是末级"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        if  (records[0][0] <= TradeContext.AFC005 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC005)  :
            iFlag=1
        if iFlag==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位已经无效"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        #保存单位内码
        afa050  =   records[0][2]
        AfaLoggerFunc.tradeInfo( afa050 )

    for afa031 in TradeContext.AFA031.split( "^" ):
        #项目日期是否合法
        sql         =   "select aaz006,aaz007,AFA030,AAZ002 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo +  "' order by aaz006 desc"
        AfaLoggerFunc.tradeInfo(sql)
        records     =   AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeInfo(sql)
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","数据库异常:查询项目信息表"
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            return False

        if ( len(records) == 0 ):
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","没有此项目%s" %afa031
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            return False
        else:
            iFlag=0
            if  (records[0][0] <= TradeContext.AFC005 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC005)  :
                iFlag=1

            if iFlag==0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","项目%s已经无效" %afa031
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            #保存收费内码
            afa030  =   records[0][2]
            AfaLoggerFunc.tradeInfo( afa030 )

        #单位在此开票日期内是否有权收取此项目
        sql         =   "select aaz006,aaz007 from fs_fa16 where  afa030='" + afa030 + "' and afa050='" + afa050 + "' and BUSINO='" + TradeContext.busiNo + "'"
        AfaLoggerFunc.tradeInfo(sql)
        records     =   AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeInfo(sql)
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","数据库异常:查询单位项目关系信息表"
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            return False

        if ( len(records) == 0 ):
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","没有此单位项目%s关系" %afa031
            AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
            return False
        else:
            iFlag=0
            for i in range( len(records) ) :
                if  (records[0][0] <= TradeContext.AFC005 ) and (len(records[0][1])==0 or records[i][1] >= TradeContext.AFC005) :
                    iFlag=1
            if iFlag==0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位项目%s关系已经无效"  %afa031
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

        #如果为大厅模式，则应将大厅编码录入到系统中，并校验当前开票日期内，此单位项目是否属于此大厅
        if (TradeContext.existVariable('AFA091' ) and len(TradeContext.AFA091)>0):
            #征收大厅与单位项目对照表
            sql         =   "select aaz006,aaz007 from fs_fa21,fs_fa20 where  fs_fa21.AFA090=fs_fa20.AFA090 and   fs_fa20.AFA091='" + TradeContext.AFA091 + "' and fs_fa21.afa030='" + afa030 + "' and fs_fa21.afa050='" + afa050 + "'"
            AfaLoggerFunc.tradeInfo(sql)
            records     =   AfaDBFunc.SelectSql( sql )
            if ( records == None ):
                AfaLoggerFunc.tradeInfo(sql)
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","数据库异常:查询征收大厅与单位项目对照表"
                AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
                return False

            if ( len(records) == 0 ):
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","没有此征收大厅与单位项目对照关系"
                AfaLoggerFunc.tradeInfo(TradeContext.errorMsg)
                return False
            else:
                iFlag=0
                for i in range( len(records) ) :
                    if  (records[0][0] <= TradeContext.AFC005 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC005) :
                        iFlag=1
                if iFlag==0 :
                    TradeContext.errorCode,TradeContext.errorMsg    =   "0001","征收大厅与单位项目关系已经无效"
                    AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                    return False

    #-------------------------检验金额-----------------------------------------------
    AfaLoggerFunc.tradeInfo("检验金额")

    AfaLoggerFunc.tradeInfo("特殊标志AFC187:"+TradeContext.AFC187)

    #减征 :减免为100
    if (TradeContext.AFC187=="100"):
        AfaLoggerFunc.tradeInfo("减征")

        for afa031 in TradeContext.AFA031.split( "^" ):
            i        =   TradeContext.AFA031.split( "^" ).index(afa031)

            sqlstr   =  "select afa038,afa039,AFA041 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if ( records == None  ):
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","数据库异常：查找收费项目表"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            if len(records) == 0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","没有此收费项目信息"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:
                #1 金额<数量*标准下限
                if records[0][0].strip() == '0' and  records[0][1].strip() == '0' :
                    pass
                else:
                    inputAmt    =   float( (TradeContext.AFC011.split("^"))[i] )    #输入金额
                    maxAmt      =   float( records[0][0] ) * float( (TradeContext.AFC010.split("^"))[i] )    #最大金额
                    minAmt      =   float( records[0][1] ) * float( (TradeContext.AFC010.split("^"))[i] )    #最小金额

                    AfaLoggerFunc.tradeInfo("当前项目上限：" + str(maxAmt))
                    AfaLoggerFunc.tradeInfo("当前项目下限：" + str(minAmt))
                    AfaLoggerFunc.tradeInfo("收入金额：" + str(inputAmt))

                    #=====根据前台传来的校验标示判断是否进行金额判断pgt 20090423====
                    if TradeContext.CKMD == '1':
                        if minAmt <= inputAmt :
                            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','项目%s输入金额错误' %afa031
                            return False
                #2 减免金额必须小于等于本级分成金额
                #3 缴款书缴费时限
                d1 = datetime.datetime(int(TradeContext.workDate[0:4]),int( TradeContext.workDate[4:6]), int(TradeContext.workDate[6:8]))
                d2 = datetime.datetime(int(TradeContext.AFC005[0:4]), int(TradeContext.AFC005[5:7]), int(TradeContext.AFC005[8:10]))
                AfaLoggerFunc.tradeInfo(str((d1 - d2).days))
                if (d1 - d2).days >5 or (d1 - d2).days >records[0][2]: #缴款书本身缴费时限为5天
                    TradeContext.errorCode,TradeContext.errorMsg    =   '0001','已经超过缴费时限：项目%s' %afa031
                    return False
                #4 当项目表（FA13）中有多条项目信息时，需根据缴款书的开票日期在项目表中找在开票日期有效的那条项目信息

    #集中汇缴:集中汇缴200
    #因为无法确定其数量，所以不校验其金额。
    #如果为大厅模式，则应将大厅编码录入到系统中，并校验当前开票日期内，此单位项目是否属于此大厅。
    elif (TradeContext.AFC187=="200"):
        AfaLoggerFunc.tradeInfo("集中汇缴")

    #直接缴库默认300
    else:
        for afa031 in TradeContext.AFA031.split( "^" ):
            i        =   TradeContext.AFA031.split( "^" ).index(afa031)
            sqlstr   =  "select afa038,afa039 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo +  "' order by aaz006 desc"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if ( records == None  ):
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","数据库异常：查找收费项目表"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            if len(records) == 0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","没有此收费项目信息"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            else:
                if records[0][0].strip() == '0' and  records[0][1].strip() == '0' :
                    pass
                else:
                    inputAmt    =   float( (TradeContext.AFC011.split("^"))[i] )    #输入金额
                    maxAmt      =   float( records[0][0] ) * float( (TradeContext.AFC010.split("^"))[i] )    #最大金额
                    minAmt      =   float( records[0][1] ) * float( (TradeContext.AFC010.split("^"))[i] )    #最小金额

                    AfaLoggerFunc.tradeInfo("当前项目上限：" + str(maxAmt))
                    AfaLoggerFunc.tradeInfo("当前项目下限：" + str(minAmt))
                    AfaLoggerFunc.tradeInfo("收入金额：" + str(inputAmt))

                    #=====根据前台传上来的校验标志判断是否进行金额校验 pgt 20090414====
                    if TradeContext.CKMD == '1':
                        if minAmt > inputAmt or inputAmt  >  maxAmt  :
                            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','项目%s输入金额错误' %afa031
                            return False

        #AfaLoggerFunc.tradeInfo("输入金额:"  + TradeContext.AFC011 )

    #不能当天补录
    for serno in TradeContext.AFC401.split(":"):
        sqlstr          =   "select date from fs_fc74 where afc401='" + serno + "' and afc015='" + TradeContext.AFC015 + "'"
        records = AfaDBFunc.SelectSql( sqlstr )
        if ( records == None or len(records) == 0 ):
            AfaLoggerFunc.tradeInfo( sqlstr )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "查找补录日期失败"
            return False

        if  records[0][0] == TradeContext.workDate :
            TradeContext.errorCode  =   "0001"
            TradeContext.errorMsg   =   "不能当天补录,请次日补录"
            return False

    #------------------计算总金额-----------------
    amount      =   0.0
    for fee in TradeContext.AFC011.split('^'):
        amount  =   amount + float(fee)

    TradeContext.payAmount  =   str( amount )
    AfaLoggerFunc.tradeInfo( '总金额：' + TradeContext.payAmount )

    sqlstr  =   "insert into FS_FC84(AFC401,AAA010,AFC001,AFA031,AFA051,AFA101,AAA011,AFC002,AFC003,AFC004,  \
    AFC005,AFC006,AFC007,AFC008,AFC009,AFC010,AFC011,AMOUNT,AFC012,AFC013,AFC015,AFC016,TELLER,BUSINO,AFC187,AFA091,FLAG,DATE,TIME) values("

    for j in range( len( (TradeContext.AFA031).split("^") ) ) :
        sqlstr1     =   sqlstr
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC401               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AAA010               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC001               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFA031.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFA051               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFA101               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AAA011               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC002               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC003               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC004               + "',"
        #=====刘雨龙 20080902 修改日期格式====
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC005[:4] + '-' + TradeContext.AFC005[4:6] + '-' + TradeContext.AFC005[6:]+ "',"
        #sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC005               + "',"

        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC006               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC007               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC008               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC009.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC010.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC011.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.payAmount            + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC012               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC013.split("^")[j] + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC015               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC016               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.teller               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.busiNo               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFC187               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.AFA091               + "',"
        sqlstr1     =   sqlstr1 + "'" + '0'                               + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.workDate             + "',"
        sqlstr1     =   sqlstr1 + "'" + TradeContext.workTime             + "')"

        if( AfaDBFunc.InsertSql( sqlstr1 ) < 0 ):
            AfaDBFunc.RollbackSql( )
            AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo( '插入补录数据失败' + sqlstr1 )
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","插入补录数据失败"
            return False

        AfaDBFunc.CommitSql( )

    AfaLoggerFunc.tradeInfo( '********************插入补录数据表结束*******************' )
    TradeContext.errorCode,TradeContext.errorMsg        =   "0000","插入补录数据成功"
    return True
