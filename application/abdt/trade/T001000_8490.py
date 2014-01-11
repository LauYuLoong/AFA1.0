# -*- coding: gbk -*-
################################################################################
#   批量业务系统：批量处理结果查询
#===============================================================================
#   交易文件:   T001000_8490.py
#   公司名称：  北京赞同科技有限公司
#   作    者：  CYG
#   修改时间:   2009-10-29
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,os
from types import *


#=====================批量处理结果查询==============================================
def TrxMain( ):


    AfaLoggerFunc.tradeInfo('**********批量处理多笔查询(8490)开始**********')

    TradeContext.O1AFAPDATE                =           TradeContext.TranDate    #工作日期
    TradeContext.O1AFAPTIME                =           TradeContext.TranTime    #工作日期

    #查询单位信息，获得单位编号
    try:
        sql = ""
        sql = "SELECT BUSINO FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "        #业务编号
        sql = sql + "ACCNO="  + "'" + TradeContext.I1ACCNO  + "'"                  #对公账户
        
        AfaLoggerFunc.tradeInfo( sql )
        
        results = AfaDBFunc.SelectSql( sql )
        
        if ( results == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询单位信息异常' )
        
        if ( len(results) <= 0 ):
            return ExitSubTrade( '9000', '没有单位信息,不能进行此类操作')
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '查询单位信息失败')

    busResult = []
    for i in range( 0, len(results) ):
        TradeContext.I1BUSINO = results[i][0]                               #单位编号
        #判断单位协议是否有效
        if ( ChkUnitInfo( ) ):
            #把校验通过的单位编号保存起来
            busResult.append(results[i][0])
            AfaLoggerFunc.tradeInfo( "[" + results[i][0] + "]单位协议有效，校验通过" )
        else:
            AfaLoggerFunc.tradeInfo( "[" + results[i][0] + "]单位协议无效")

    #begin 20091130 蔡永贵增加 
    if( len(busResult) == 0 ):
        return ExitSubTrade( '9999', '单位协议不存在，不能做此交易')
    #end

    try:
        sql = ""
        sql = "SELECT * FROM (select abdt_batchinfo.*,rownumber() over(order by batchno) as rn from ABDT_BATCHINFO WHERE "
        sql = sql + "APPNO="       + "'" + TradeContext.I1APPNO    + "'"    + " AND "          #业务编号
        sql = sql + "BUSINO in ("
        for busino in busResult:
            sql = sql +  "'" + busino + "',"                                                   #单位编号
        sql = sql[0:-1] + ") AND "
        sql = sql + "BEGINDATE>="   + "'" + TradeContext.I1WORKDATE + "'"    + " AND "         #起始日期
        sql = sql + "ENDDATE<="     + "'" + TradeContext.I1ENDDATE + "') "                     #结束日期
        sql = sql + "as a1 where a1.rn >= " + TradeContext.I1STARTNO

        AfaLoggerFunc.tradeInfo( "查询批次信息sql:" + sql )
        
        #查询笔数
        count = int(TradeContext.I1COUNT)

        records = AfaDBFunc.SelectSql( sql, count )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询批量信息表异常' )

        if ( len(records) == 0 ):
            return ExitSubTrade( '9000', '没有该委托号的批次信息' )

        #过滤None
        AfaUtilTools.ListFilterNone( records )
        TradeContext.O2BATCHNO    = []
        TradeContext.O2APPNO      = []
        TradeContext.O2BUSINO     = []
        TradeContext.O2ZONENO     = []
        TradeContext.O2BRNO       = []
        TradeContext.O2USERNO     = []
        TradeContext.O2ADMINNO    = []
        TradeContext.O2TERMTYPE   = []
        TradeContext.O2FILENAME   = []
        TradeContext.O2INDATE     = []
        TradeContext.O2INTIME     = []
        TradeContext.O2BATCHDATE  = []
        TradeContext.O2BATCHTIME  = []
        TradeContext.O2TOTALNUM   = []
        TradeContext.O2TOTALAMT   = []
        TradeContext.O2SUCCAMT    = []
        TradeContext.O2FAILNUM    = []
        TradeContext.O2FAILAMT    = []
        TradeContext.O2SUCCNUM    = []
        TradeContext.O2UNSETNUM   = []
        TradeContext.O2UNSETAMT   = []
        TradeContext.O2STATUS     = []
        TradeContext.O2BEGINDATE  = []
        TradeContext.O2ENDDATE    = []
        TradeContext.O2PROCMSG    = []
        TradeContext.O2NOTE1      = []
        TradeContext.O2NOTE2      = []
        TradeContext.O2NOTE3      = []
        TradeContext.O2NOTE4      = []
        TradeContext.O2NOTE5      = []
        for i in range(0, len(records)):
            TradeContext.O2BATCHNO.append(         str(records[i][0])  )         #委托号(批次号)
            TradeContext.O2APPNO.append(           str(records[i][1])  )         #业务编号
            TradeContext.O2BUSINO.append(          str(records[i][2])  )         #单位编号
            TradeContext.O2ZONENO.append(          str(records[i][3])  )         #地区号
            TradeContext.O2BRNO.append(            str(records[i][4])  )         #网点号
            TradeContext.O2USERNO.append(          str(records[i][5])  )         #操作员
            TradeContext.O2ADMINNO.append(         str(records[i][6])  )         #管理员
            TradeContext.O2TERMTYPE.append(        str(records[i][7])  )         #终端类型
            TradeContext.O2FILENAME.append(        str(records[i][8])  )         #上传文件名
            TradeContext.O2INDATE.append(          str(records[i][9])  )         #委托日期
            TradeContext.O2INTIME.append(          str(records[i][10]) )         #委托时间
            TradeContext.O2BATCHDATE.append(       str(records[i][11]) )         #提交日期
            TradeContext.O2BATCHTIME.append(       str(records[i][12]) )         #提交时间
            TradeContext.O2TOTALNUM.append(        str(records[i][13]) )         #总笔数
            TradeContext.O2TOTALAMT.append(        str(records[i][14]) )         #总金额
            TradeContext.O2SUCCNUM.append(         str(records[i][15]) )         #成功笔数
            TradeContext.O2SUCCAMT.append(         str(records[i][16]) )         #成功金额
            TradeContext.O2FAILNUM.append(         str(records[i][17]) )         #失败笔数
            TradeContext.O2FAILAMT.append(         str(records[i][18]) )         #失败金额
            TradeContext.O2UNSETNUM.append(        '0')                          #未处理笔数
            TradeContext.O2UNSETAMT.append(        '0.00')                       #未处理金额
            TradeContext.O2STATUS.append(          str(records[i][19]) )         #状态
            TradeContext.O2BEGINDATE.append(       str(records[i][20]) )         #生效日期
            TradeContext.O2ENDDATE.append(         str(records[i][21]) )         #失效日期
            TradeContext.O2PROCMSG.append(         str(records[i][22]) )         #处理信息
            TradeContext.O2NOTE1.append(           str(records[i][23]) )         #备注1
            TradeContext.O2NOTE2.append(           str(records[i][24]) )         #备注2
            TradeContext.O2NOTE3.append(           str(records[i][25]) )         #备注3
            TradeContext.O2NOTE4.append(           str(records[i][26]) )        #备注4
            TradeContext.O2NOTE5.append(           str(records[i][27]) )        #备注5

        TradeContext.O1STARTNO =  TradeContext.I1STARTNO                                  #本次查询起始笔数
        TradeContext.O1COUNT   =   str(len(records))                                      #本次查询笔数
        
        #查询满足条件的笔数
        sql = ""
        sql = sql + "select count(*) from abdt_batchinfo where "
        sql = sql + "APPNO="        + "'" + TradeContext.I1APPNO  + "'"    + " AND "         #业务编号
        sql = sql + "BUSINO in ("
        for busino in busResult:
            sql = sql +  "'" + busino + "',"                                                 #单位编号
        sql = sql[0:-1] + ") AND "
        sql = sql + "BEGINDATE>="   + "'" + TradeContext.I1WORKDATE + "'"  + " AND "         #起始日期
        sql = sql + "ENDDATE<="     + "'" + TradeContext.I1ENDDATE + "' "                    #结束日期
        
        AfaLoggerFunc.tradeInfo( sql )
        
        rcount = AfaDBFunc.SelectSql( sql )
        if ( rcount == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询批量信息表异常' )
        
        if ( rcount[0][0] == None ):
            return ExitSubTrade( '9000', '没有该委托号的批次信息' )
        
        TradeContext.O1TOTALCO = str(rcount[0][0])                                     #满足条件笔数
        

        AfaLoggerFunc.tradeInfo('**********批量处理多笔查询(8490)结束**********')


        #返回
        TradeContext.errorCode = '0000'
        TradeContext.errorMsg = '查询成功'
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '批量处理结果查询,数据库异常' )
        
        
#判断单位协议是否有效
def ChkUnitInfo( ):


    AfaLoggerFunc.tradeInfo('>>>判断单位协议是否有效')


    try:
        sql = ""
        sql = "SELECT SIGNUPMODE,GETUSERNOMODE,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO,AGENTTYPE,VOUHNO FROM ABDT_UNITINFO WHERE "
        sql = sql + "APPNO="  + "'" + TradeContext.I1APPNO  + "'" + " AND "        #业务编号
        sql = sql + "BUSINO=" + "'" + TradeContext.I1BUSINO + "'" + " AND "        #单位编号
        sql = sql + "STATUS=" + "'" + "1"                   + "'"                  #状态

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '查询单位协议信息异常' )
    
        if ( len(records) <= 0 ):
            return ExitSubTrade( '9000', '没有单位协议信息,不能进行此类操作')

        #过滤None
        AfaUtilTools.ListFilterNone( records )

        TradeContext.SIGNUPMODE    = str(records[0][0])                             #签约方式
        TradeContext.GETUSERNOMODE = str(records[0][1])                             #商户客户编号获取方式
        TradeContext.STARTDATE     = str(records[0][2])                             #生效日期
        TradeContext.ENDDATE       = str(records[0][3])                             #失效日期
        TradeContext.STARTTIME     = str(records[0][4])                             #服务开始时间
        TradeContext.ENDTIME       = str(records[0][5])                             #服务终止时间
        TradeContext.ACCNO         = str(records[0][6])                             #对公账户
        TradeContext.AGENTTYPE     = str(records[0][7])                             #委托方式
        TradeContext.VOUHNO        = str(records[0][8])                             #凭证号(内部帐户)

        AfaLoggerFunc.tradeInfo( "TranDate=[" + TradeContext.TranDate + "]" )

        if ( (TradeContext.STARTDATE > TradeContext.TranDate) or (TradeContext.TranDate > TradeContext.ENDDATE) ):
            return ExitSubTrade( '9000', '该单位委托协议还没有生效或已过有效期')

        if ( (TradeContext.STARTTIME > TradeContext.TranTime) or (TradeContext.TranTime > TradeContext.ENDTIME) ):
            return ExitSubTrade( '9000', '已经超过该系统的服务时间,该业务必须在[' + s_StartDate + ']-[' + s_EndDate + ']时间段运行')

        if ((TradeContext.SIGNUPMODE=="1") and (TradeContext.GETUSERNOMODE=="1")):
            #发送到通讯前置并从第三方获取协议
            return True

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '判断单位协议信息是否存在失败')


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        
