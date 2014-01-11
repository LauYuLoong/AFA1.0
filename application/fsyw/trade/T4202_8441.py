# -*- coding: gbk -*-
##################################################################
#   代收代付平台.缴费交易
#=================================================================
#   程序文件:   4202_8441.py
#   修改时间:   2006-09-11
##################################################################
import TradeContext
TradeContext.sysType = 'fsyw'
import AfaLoggerFunc,AfaDBFunc,AfaFlowControl
import AfaHostFunc,datetime

from types import *

#从表table中取出field根据item的值为value
def GetDataFromDB(item,value,table,field):
    sql = "select " + field + " from " + "FS_" + table + " where " + item + "='" + value +"'"

    #afc163开票日期
    records = AfaDBFunc.SelectSql( sql )
    if ( records == None or len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( sql )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
        return False
    else:
        if not records[0][0]:
            return "null"
        else:
            return records[0][0]

def SubModuleDoFst():

    #=====add by pgt 20090423 验证实际缴费金额是否为0或者空，如果是，则直接退出====
    if(TradeContext.amount == "0" or TradeContext.amount == "0.00" or TradeContext.amount == "0.0" ):
        AfaLoggerFunc.tradeInfo("实际缴费金额为0元")
        TradeContext.errorCode = "A9999"
        TradeContext.errorMsg = "实际缴费金额为0元"
        return False

    if(TradeContext.amount == ""):
        AfaLoggerFunc.tradeInfo("实际缴费金额为空")
        TradeContext.errorCode = "A9999"
        TradeContext.errorMsg = "实际缴费金额为空"
        return False


    TradeContext.__agentEigen__ = '0'                     #从表标志

    TradeContext.accno          =   TradeContext.AFA185   #交款人帐号
    if len(TradeContext.accno) == 0:
        #TradeContext.accno = '0'
        TradeContext.accno = ''


    #如果是卡号需要从卡号中获取凭证号码
    if TradeContext.opkd    == '1':                       #账户类型
        TradeContext.vouhNo =   TradeContext.cardno[6:18]
        TradeContext.AFA185 =   TradeContext.cardno
        TradeContext.accno  =   TradeContext.cardno

    #获取凭证号、凭证种类
    if TradeContext.catrFlag == '1':                      #现转标志
        TradeContext.vouhType   =   TradeContext.vouhNo[0:2]
        TradeContext.vouhNo     =   TradeContext.vouhNo[2:]
        if TradeContext.wdtp=='2': #凭证件
            TradeContext.accPwd=''

    #判断银行编码是否为空值,张恒修改
    AfaLoggerFunc.tradeInfo("=====银行编码 "+TradeContext.bankbm)
    if  len(TradeContext.bankbm) == 0:
            TradeContext.errorCode,TradeContext.errorMsg  =   '0001','银行编码为空值,请重新输入'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

    #首先从库表中查询缴款书编号，如果查找到则返回已经缴费的错误
    sqlstr  =   "select flag from fs_fc76 where afc001='" + TradeContext.userNo + "'"

    #===张恒增加查询增加项目外码字段,银行编码字段,保证查出唯一一条记录===
    sqlstr  =   sqlstr + " and bankno = '" + TradeContext.bankbm + "'"

    records = AfaDBFunc.SelectSql( sqlstr )

    if ( len(records) == 0 ):
        AfaLoggerFunc.tradeInfo( "没有查找到缴款书编号可以缴费\n"+sqlstr )
        AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
    else:
        if records[0][0]   ==  '0':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0001','已经查找到了缴款书编号，不能再缴费'
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
        elif records[0][0]   ==  '1':
            TradeContext.errorCode,TradeContext.errorMsg  =   '0002',"缴款书已冲正，可缴费"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
        else:
            TradeContext.errorCode,TradeContext.errorMsg  =   '0003',"缴款书状态位异常"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False
    #将缴费中afap需要的字段转化为缴款书信息表中字段名
    TradeContext.AFC001         =   TradeContext.userNo
    TradeContext.AFC157         =   TradeContext.amount
    TradeContext.AFA183         =   TradeContext.userName
    TradeContext.AFA185         =   TradeContext.accno
    TradeContext.AFA051         =   TradeContext.note1


    TradeContext.AFA031List     =   []

    #TradeContext.AFA032List     =   []

    TradeContext.AFC181List     =   []
    TradeContext.AFA040List     =   []
    TradeContext.AFC180List     =   []

    #拆开记录
    itemCnt                     =   len( TradeContext.AFA031.split('^') )

    TradeContext.recLen         =   str( itemCnt )

    AfaLoggerFunc.tradeInfo( "AAAAAA[" + TradeContext.recLen + "]AAAA" )

    for i in range(itemCnt):
        TradeContext.AFA031List.append( (TradeContext.AFA031.split('^'))[i] )
        TradeContext.AFC181List.append( (TradeContext.AFC181.split('^'))[i] )
        TradeContext.AFA040List.append( (TradeContext.AFA040.split('^'))[i] )
        TradeContext.AFC180List.append( (TradeContext.AFC180.split('^'))[i] )


    #是否串票的校验
    piaoNo          =   TradeContext.AFC001[0:9]
    aaz010      =   TradeContext.AAA010

    sqlstr      =   "select * from fs_dpz_gl where fczqhnm='" + aaz010 + "'"

    AfaLoggerFunc.tradeInfo( sqlstr )

    records     =   AfaDBFunc.SelectSql(sqlstr)

    #=====根据是否已经交过费和前台传上来的校验标识来决定是否进行串票校验 pgt 20090414====
    if (len(records) > 0  and (TradeContext.CKMD == "1")):    #CKMD校验标示，1校验，0不校验
        AfaLoggerFunc.tradeInfo( "串票校验" )

        #如果大厅内码为空，进入非大厅模式
        if ( not TradeContext.existVariable('AFA091' ) or len(TradeContext.AFA091)==0 ):
            sqlstr  =   "select count(*) from (select distinct b.AFA051 from FS_DPZ_GL a,fs_fa15 b where a.fdwdm=b.AFA050 and a.FQSHM<='" + piaoNo + "' and a.FQZHM>='" + piaoNo +  "'" + \
            " union all select distinct c.AFA051 from FS_DPZ_GL a,fs_fa21 b,fs_fa15 c where a.FQSHM<='" + piaoNo + "' and a.FQZHM>='" + piaoNo + "' and a.fdwdm=b.AFA050 and b.AFA050=c.AFA050) a where locate(a.afa051, '" + TradeContext.AFA051 + "')=1"

            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )

            if( records == None  ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "串票校验失败"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            if  int(records[0][0]) == 0 :
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "非本执收单位票据,请检查票号"
                return False

            AfaLoggerFunc.tradeInfo('>>>串票校验完成')

        #如果是大厅内码不空，则进入大厅模式
        if (TradeContext.existVariable('AFA091' ) and len(TradeContext.AFA091)>0):

            #首先根据大厅外码转化为大厅内码
            sqlstr  =   "select afa090 from fs_fa20 where afa091='" + TradeContext.AFA091 + "' and aaa010='" + TradeContext.AAA010 + "' and BUSINO='" + TradeContext.busiNo + "'"


            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if( records == None ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "大厅内码转换大厅外码异常"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

            if  ( len(records) == 0 ):
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "没有找到%s的大厅内码" %TradeContext.AFA091
                return False

            afa090  =   records[0][0].strip()           #大厅内码
            #根据大厅内码和票据起始和终止号码查询是否有票据领购信息
            sqlstr  =   "select count(*) from fs_dpz_gl where FDWDM='" + afa090 + "' and FQSHM<='" + piaoNo + "' and FQZHM>='" + piaoNo + "'"
            AfaLoggerFunc.tradeInfo( sqlstr )
            records = AfaDBFunc.SelectSql( sqlstr )
            if  int(records[0][0]) > 0 :
                pass
            else:
                TradeContext.errorCode  =   "0001"
                TradeContext.errorMsg   =   "非本执收单位票据,请检查票号--大厅模式"
                AfaLoggerFunc.tradeInfo( sqlstr )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return False

    AfaLoggerFunc.tradeInfo("单位在此开票日期内是否有权收取此项目")

    #单位是否合法
    sql         =   "select aaz006,aaz007,afa050,AAZ002 from fs_fa15 where afa051='" + TradeContext.AFA051 + "' and BUSINO='" + TradeContext.busiNo + "'"
    sql         =   sql + " and aaa010='" + TradeContext.AAA010 + "'"
    sql         =   sql + " and busino='" + TradeContext.busiNo + "'"


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
        for i in range( len(records) ) :
            if (records[0][3]!='1'):
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位不是末级"
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False
            if  (records[i][0] <= TradeContext.AFC163 ) and (len(records[i][1])==0 or records[i][1] >= TradeContext.AFC163)  :
                iFlag=1
        if iFlag==0 :
            TradeContext.errorCode,TradeContext.errorMsg    =   "0001","单位已经无效"
            AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
            return False

        #保存单位内码
        afa050  =   records[0][2]

    for afa031 in TradeContext.AFA031.split( "^" ):
        #项目日期是否合法
        sql         =   "select aaz006,aaz007,AFA030,AAZ002 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"
        AfaLoggerFunc.tradeInfo(sql)
        records     =   AfaDBFunc.SelectSql( sql )

        AfaLoggerFunc.tradeInfo(records)
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
            if  (records[0][0] <= TradeContext.AFC163 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC163)  :
                iFlag=1
            if iFlag==0 :
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001","项目%s已经无效" %afa031
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                return False

            #保存收费内码
            afa030  =   records[0][2]
            AfaLoggerFunc.tradeInfo('>>>收费内码['+afa030+']')

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
                if  (records[0][0] <= TradeContext.AFC163 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC163) :
                    iFlag=1
            AfaLoggerFunc.tradeInfo('-->记录日期' + records[0][0] + '   -->校验日期' + TradeContext.AFC163)
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
                AfaLoggerFunc.tradeInfo(records)
                AfaLoggerFunc.tradeInfo(TradeContext.AFC163)
                for i in range( len(records) ) :
                    if  (records[0][0] <= TradeContext.AFC163 ) and (len(records[0][1])==0 or records[0][1] >= TradeContext.AFC163) :
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

            sqlstr   =  "select afa038,afa039,AFA041 from fs_fa13 where afa031='" + afa031 + "' order by aaz006 desc"
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
                    inputAmt    =   float( (TradeContext.AFC181.split("^"))[i] )    #输入金额
                    maxAmt      =   float( records[0][0] ) * float( (TradeContext.AFC180.split("^"))[i] )    #最大金额
                    minAmt      =   float( records[0][1] ) * float( (TradeContext.AFC180.split("^"))[i] )    #最小金额

                    AfaLoggerFunc.tradeInfo("当前项目上限：" + str(maxAmt))
                    AfaLoggerFunc.tradeInfo("当前项目下限：" + str(minAmt))
                    AfaLoggerFunc.tradeInfo("收入金额：" + str(inputAmt))

                    #=====根据前台传来的校验标示判断是否进行金额判断pgt 20090414====
                    if TradeContext.CKMD == '1':
                        if minAmt <= inputAmt :
                            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','项目%s输入金额错误' %afa031
                            return False
                #2 减免金额必须小于等于本级分成金额
                #3 缴款书缴费时限
                d1 = datetime.datetime(int(TradeContext.workDate[0:4]),int( TradeContext.workDate[4:6]), int(TradeContext.workDate[6:8]))
                d2 = datetime.datetime(int(TradeContext.AFC163[0:4]), int(TradeContext.AFC163[5:7]), int(TradeContext.AFC163[8:10]))
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

            AfaLoggerFunc.tradeInfo( TradeContext.AFA031.split( "^" ) )

            sqlstr   =  "select afa038,afa039 from fs_fa13 where afa031='" + afa031 + "' and BUSINO='" + TradeContext.busiNo + "' order by aaz006 desc"

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
                    AfaLoggerFunc.tradeInfo('>>>不校验金额上限与下限')
                    pass
                else:
                    inputAmt    =   float( (TradeContext.AFC181.split("^"))[i] )    #输入金额

                    AfaLoggerFunc.tradeInfo( '>>>柜员输入上送金额[' + (TradeContext.AFC181.split("^"))[i] + ']')

                    maxAmt      =   float( records[0][0] ) * float( (TradeContext.AFC180.split("^"))[i] )    #最大金额
                    minAmt      =   float( records[0][1] ) * float( (TradeContext.AFC180.split("^"))[i] )    #最小金额

                    AfaLoggerFunc.tradeInfo("当前项目上限：" + str(maxAmt))
                    AfaLoggerFunc.tradeInfo("当前项目下限：" + str(minAmt))
                    AfaLoggerFunc.tradeInfo("收入金额：" + str(inputAmt))

                    AfaLoggerFunc.tradeInfo(records[0][0])
                    AfaLoggerFunc.tradeInfo(records[0][1])
                    AfaLoggerFunc.tradeInfo((TradeContext.AFC181.split("^"))[i])


                    #=====根据前台传上来的校验标志判断是否进行金额校验 pgt 20090414====
                    if TradeContext.CKMD == '1':
                        if minAmt > inputAmt or inputAmt  >  maxAmt :
                            AfaLoggerFunc.tradeInfo(minAmt)
                            AfaLoggerFunc.tradeInfo(inputAmt)
                            AfaLoggerFunc.tradeInfo(maxAmt)
                            TradeContext.errorCode,TradeContext.errorMsg    =   '0001','项目%s输入金额错误' %afa031
                            return False

        AfaLoggerFunc.tradeInfo("输入金额:"  + TradeContext.AFC157 )
        AfaLoggerFunc.tradeInfo("*************--------*****************  "+str(TradeContext.recLen))
    return True


def SubModuledoSnd():
    TradeContext.mima   =   "011"
    TradeContext.user   =   "011"
    return True

def SubModuledoTrd():

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
    AfaLoggerFunc.tradeInfo("*************缴费交易开始*****************")

    try:
        sqlstr      =   ""
        sqlstr      =   "select * from fs_fc76 where afc001='" + TradeContext.userNo + "'"
        #===张恒增加查询增加项银行编码字段,保证查出唯一一条记录===
        sqlstr      =   sqlstr + " and afc153 = '" + TradeContext.bankbm + "'"
        records     =   AfaDBFunc.SelectSql(sqlstr)
        #查找到了缴款书编号,只需要更新状态位
        if ( len(records) > 0 ):
            AfaLoggerFunc.tradeInfo("=====>>>表FS_FC76中有"+TradeContext.userNo+"对应的信息,只需要更新状态位")
            sqlstr      =   ""
            sqlstr      =   "update fs_fc76 set flag='0',afc187='" + TradeContext.AFC187 + "' ,serno='" + TradeContext.agentSerialno + "' where afc001='" + TradeContext.userNo + "'"
            if( AfaDBFunc.UpdateSqlCmt( sqlstr ) < 1 ):
                TradeContext.errorCode,TradeContext.errorMsg  =   '0001','已有缴款记录'
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg +sqlstr)
                return None
            else:
                TradeContext.errorCode,TradeContext.errorMsg    =   "0000",'缴费成功'
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo("*************缴费交易结束*****************")   
                return bill
                
        else:
                AfaLoggerFunc.tradeInfo("=====>>>表FS_FC76中无"+TradeContext.userNo+"对应的信息，插入记录")

        #==如果找到了缴款书编号,需要更新前台送过来的当前记录的所有字段,张恒修改于20100524==
        sqlstr1     =   ""
        #把交费信息写到本地数据库里面
        #增加银行编码字段,张恒修改
        sqlstr  =   "insert into FS_FC76(AFC001,AFA031,AFC163,AFC187,AFC183,AFC157,   \
                                      AFC181,AFA040,AFC180,AFA051,AFC166,AFC155,AFC153,  \
                                      AFC154,AFA183,AFA184,AFA185,AFA091,AFC015,AAA010,FLAG,SERNO,BUSINO,TELLER,BRNO,DATE,TIME,BANKNO) values("

        for i in range( len( (TradeContext.AFA031).split("^") ) ) :
            sqlstr1          =   sqlstr

            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC001                      + "',"
            sqlstr1          =   sqlstr1 + "'" + (TradeContext.AFA031.split("^"))[i]      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC163                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC187                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC183                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC157                      + "',"
            sqlstr1          =   sqlstr1 + "'" + (TradeContext.AFC181.split("^"))[i].strip()   + "',"
            sqlstr1          =   sqlstr1 + "'" + (TradeContext.AFA040.split("^"))[i].strip()   + "',"
            sqlstr1          =   sqlstr1 + "'" + (TradeContext.AFC180.split("^"))[i].strip()   + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA051                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC166                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC155                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC153                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC154                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA183                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA184                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA185                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.AFA091                      + "',"

            sqlstr1=sqlstr1+"'"+TradeContext.workDate[:4]+'-'+TradeContext.workDate[4:6]+'-'+TradeContext.workDate[6:]+"',"
            #=====刘雨龙 20080821 修改银行收款时间为TradeContext.workDate====
            #sqlstr1          =   sqlstr1 + "'" + TradeContext.AFC015                      + "',"

            sqlstr1          =   sqlstr1 + "'" + TradeContext.AAA010                      + "',"
            sqlstr1          =   sqlstr1 + "'" + '0'                                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.agentSerialno               + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.busiNo                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.teller                      + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.brno                        + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.workDate                    + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.workTime                    + "',"
            sqlstr1          =   sqlstr1 + "'" + TradeContext.bankbm                      + "')"

            AfaLoggerFunc.tradeInfo( sqlstr1 )
            if( AfaDBFunc.InsertSql( sqlstr1 ) < 1 ):
                AfaDBFunc.RollbackSql( )
                TradeContext.errorCode,TradeContext.errorMsg    =   "0001",'插入缴费书信息表失败' + sqlstr1
                AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )
                AfaLoggerFunc.tradeInfo( AfaDBFunc.sqlErrMsg )
                return None

            AfaDBFunc.CommitSql( )

        TradeContext.errorCode,TradeContext.errorMsg    =   "0000",'缴费成功'
        AfaLoggerFunc.tradeInfo( TradeContext.errorMsg )

        AfaLoggerFunc.tradeInfo("*************缴费交易结束*****************")
        return bill

    except Exception, e:
        AfaLoggerFunc.tradeInfo(str(e))
        return None

