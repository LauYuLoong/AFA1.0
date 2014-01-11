# -*- coding: gbk -*-
################################################################################
#   代收代付.查询明细模板
#===============================================================================
#   模板文件:   003101.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,AfaFunc,os
from types import *


def main( ):

    sernoFlag = 0
    
    AfaLoggerFunc.tradeInfo( '******代收代付.查询明细模板['+TradeContext.TemplateCode+']进入******' )

    try:
        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]


        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================判断应用系统状态==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================校验公共节点的有效性==============================
        if( not TradeContext.existVariable( "zoneno" ) ):
            TradeFunc.exitOnError( 'A0001', '地区号[zoneno]值不存在,不能进行查询操作' )


        if( not TradeContext.existVariable( "brno" ) ):
            TradeFunc.exitOnError( 'A0001', '网点号[brno]值不存在,不能进行查询操作' )


        if( not TradeContext.existVariable( "tellerno" ) ):
            TradeFunc.exitOnError( 'A0001', '网点号[tellerno]值不存在,不能进行查询操作' )


        if( not TradeContext.existVariable( "transStatus" ) ):
            TradeFunc.exitOnError( 'A0001', '交易状态[transStatus]值不存在,不能进行查询操作' )


        if( not TradeContext.existVariable( "queryMode" ) ):
            TradeFunc.exitOnError( 'A0001', '查询方式[queryMode]值不存在,不能进行查询操作' )


        if( not TradeContext.existVariable( "orderMode" ) ):
            TradeFunc.exitOnError( 'A0001', '排序方式[orderMode]值不存在,不能进行查询操作' )


        if( not TradeContext.existVariable( "queryCount" ) ):
            TradeFunc.exitOnError( 'A0001', '查询条数[queryCount]值不存在,不能进行查询操作' )


        if( not TradeContext.existVariable( "TransType" ) ):
            TradeFunc.exitOnError( 'A0001', '传输类型[TransType]值不存在,不能进行查询操作' )


        AfaLoggerFunc.tradeInfo('>>>transStatus   = ' + TradeContext.transStatus)
        AfaLoggerFunc.tradeInfo('>>>queryMode     = ' + TradeContext.queryMode)
        AfaLoggerFunc.tradeInfo('>>>orderMode     = ' + TradeContext.orderMode)
        AfaLoggerFunc.tradeInfo('>>>queryCount    = ' + TradeContext.queryCount)
        AfaLoggerFunc.tradeInfo('>>>TransType     = ' + TradeContext.TransType)
        AfaLoggerFunc.tradeInfo('>>>tradeDate     = ' + TradeContext.tradeDate)


        #=====================定义每次返回的数据的记录数========================
        queryCount = int( TradeContext.queryCount )


        #=====================数据打包时使用list================================
        names=['agentSerialno', 'sysId', 'unitno', 'subUnitno', 'workDate', 'workTime','agentFlag', 'transCode', 'zoneno', 'brno', 'tellerno', \
        'channelCode', 'accType', 'drAccno', 'crAccno', 'userno', 'subuserno', 'username', 'vouhType', 'vouhno', \
        'vouhDate', 'amount', 'subAmount', 'bankStatus', 'bankSerno', 'corpStatus', 'errormsg', 'note1', \
        'note2', 'note3', 'note4', 'note5', 'note6', 'note7', 'note8', 'note9', 'note10']


        # =====================查询字段与数据打包的list一一对应=================
        SqlStr = "SELECT AGENTSERIALNO,SYSID,UNITNO,SUBUNITNO,WORKDATE,WORKTIME,AGENTFLAG,TRXCODE,ZONENO,BRNO,TELLERNO,"
        SqlStr = SqlStr + "CHANNELCODE,ACCTYPE,DRACCNO,CRACCNO,USERNO,SUBUSERNO,USERNAME,VOUHTYPE,VOUHNO,"
        SqlStr = SqlStr + "VOUHDATE,AMOUNT,SUBAMOUNT,BANKSTATUS,BANKSERNO,CORPSTATUS,ERRORMSG,NOTE1,"
        SqlStr = SqlStr + "NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9,NOTE10 FROM AFA_MAINTRANSDTL "


        #=====================统计总笔数和总金额================================
        sql_count = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL"

        sql = ''
        if ( int( TradeContext.queryMode ) == 4 ):              #自由查询方式
            if( not TradeContext.existVariable( "whereClause" ) ):
                TradeFunc.exitOnError( 'A0001', '查询条件[whereClause]值不存在,不能进行查询操作' )

            sql= sql + TradeContext.whereClause + " AND REVTRANF='0' "

            AfaLoggerFunc.tradeInfo('>>>whereClause   = ' + TradeContext.whereClause)

        else:
            if( not TradeContext.existVariable( "tradeDate" ) ):
                TradeFunc.exitOnError( 'A0001', '交易日期[tradeDate]值不存在,不能进行查询操作' )

            if( not TradeContext.existVariable( "channelCode" ) ):
                TradeFunc.exitOnError( 'A0001', '渠道代码[channelCode]值不存在,不能进行查询操作' )

            #日期
            sql = sql + " WHERE WORKDATE='"     + TradeContext.tradeDate        + "'"

            #地区号
            sql = sql + " AND CHANNELCODE='"    + TradeContext.channelCode      + "'"

            #地区号
            sql = sql + " AND ZONENO='"         + TradeContext.zoneno           + "'"

            #网点号
            sql = sql + " AND BRNO='"           + TradeContext.brno             + "'"

            #柜员
            sql = sql + " AND TELLERNO='"       + TradeContext.tellerno         + "'"

            #柜员
            sql = sql + " AND REVTRANF='"       + "0"                           + "'"
            
            #用户
            if( TradeContext.existVariable( "userno" ) and len(TradeContext.userno)>0 ):
                sql = sql + " AND USERNO='"     + TradeContext.userno           + "'"

            #金额
            if( TradeContext.existVariable( "amount" ) and int(float(TradeContext.amount)*100)!=0 ):
                sAmount="0.00";
                for i in range(0, len(TradeContext.amount)):
                    if TradeContext.amount[i] == '0':
                        continue
                    sAmount = TradeContext.amount[i:]
                    break

                sql = sql + " AND AMOUNT='"     + sAmount           + "'"

            #用户名
            if( TradeContext.existVariable( "username" ) and len(TradeContext.username)>0 ):
                sql = sql + " AND USERNAME='"   + TradeContext.username         + "'"

            #帐号
            if( TradeContext.existVariable( "accno" ) and len(TradeContext.accno)>0 ):
                sql = sql + " AND (DRACCNO='"   + TradeContext.accno + "' OR CRACCNO='" + TradeContext.accno + "')"

        #transStatus:交易状态(1-正常, 2-未知, 3-全部)
        if( int( TradeContext.transStatus )   == 1 ):

            #查询正常交易
            sql = sql + " AND BANKSTATUS='0' AND CORPSTATUS='0'"

        elif( int( TradeContext.transStatus ) == 2 ):

            #查询未知交易
            sql = sql + " AND (AGENTFLAG IN ('01','03') AND (BANKSTATUS='2' OR (BANKSTATUS='0' AND CORPSTATUS IN ('1', '2','3')))) OR"
            sql = sql + " (AGENTFLAG IN ('02','04') AND (CORPSTATUS='2' OR (CORPSTATUS='0' AND BANKSTATUS IN ('1', '2','3')))) "

        elif( int( TradeContext.transStatus ) != 3 ):
            TradeContext.errorCode, TradeContext.errorMsg='A0041', "入口参数条件不符[交易状态]:"+str( TradeContext.transStatus )
            raise AfaFlowControl.flowException( )


        #queryMode:查询方式(1-按流水号查询, 2-按系统代码查询, 3-查询全部正交易, 4-自由查询方式)
        if( int( TradeContext.queryMode ) == 1 ):

            #按流水号查询
            if( not TradeContext.existVariable( "agentSerialno" ) ):
                TradeFunc.exitOnError( 'A0001', '流水号[agentSerialno]值不存在!' )

            sql = sql + " AND AGENTSERIALNO='"+TradeContext.agentSerialno + "'"
            sernoFlag = 1
            
        elif( int( TradeContext.queryMode ) == 2 ):

            #按系统代码查询
            if( not TradeContext.existVariable( "sysId" ) ):
                TradeFunc.exitOnError( 'A0001', '系统代码[sysId]值不存在!' )

            #系统代码
            sql = sql + " AND SYSID='"       + TradeContext.sysId     + "'"


            #按流水号查询
            if( TradeContext.existVariable( "agentSerialno" ) and len(TradeContext.agentSerialno)>0 ):
                sql = sql + " AND AGENTSERIALNO='"+TradeContext.agentSerialno + "'"
                sernoFlag = 1

            #业务方式
            if( TradeContext.existVariable( "agentFlag" ) and len(TradeContext.agentFlag)>0 ):
                sql=sql + " AND AGENTFLAG='" + TradeContext.agentFlag + "'"


            #单位代码
            if( TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno)>0 ):
                sql=sql + " AND UNITNO='"    + TradeContext.unitno    + "'"


            #子单位代码
            if( TradeContext.existVariable( "subUnitno" ) and len(TradeContext.subUnitno)>0 ):
                sql=sql + " AND SUBUNITNO='" + TradeContext.subUnitno + "'"


        elif( int( TradeContext.queryMode ) != 3 and int( TradeContext.queryMode ) != 4 ):
            TradeContext.errorCode, TradeContext.errorMsg='A0041', "入口参数条件不符[查询方式]:"+str( TradeContext.queryMode )
            raise AfaFlowControl.flowException( )

        sql_count = sql_count + sql


        #按流水查询应该是单结果集的,没有排序的必要
        if( int( TradeContext.queryMode ) != 1  and sernoFlag==0):

            #orderMode:排序方式:1-正序 2-逆序
            if( int( TradeContext.orderMode ) == 1 ):

                #正序
                if( (not TradeContext.existVariable( "agentSerialno" )) or TradeContext.agentSerialno=='' ):
                    TradeContext.agentSerialno='0'

                sql = sql + " AND AGENTSERIALNO>'" + TradeContext.agentSerialno + "' ORDER BY AGENTSERIALNO ASC"

            else:

                #逆序
                if( (not TradeContext.existVariable( "agentSerialno" )) or TradeContext.agentSerialno=='' ):
                    TradeContext.agentSerialno='99999999'

                sql = sql + " AND AGENTSERIALNO<'"+TradeContext.agentSerialno + "' ORDER BY AGENTSERIALNO DESC"


        #查询数据库
        SqlStr = SqlStr + sql

        AfaLoggerFunc.tradeInfo( '>>>查询明细' )

        AfaLoggerFunc.tradeInfo( SqlStr )

        records=AfaDBFunc.SelectSql( SqlStr, queryCount )

        if( records == None ):
            #None 查询失败
            TradeContext.errorCode, TradeContext.errorMsg='A0025', "数据库操作错误"
            raise AfaFlowControl.flowException( )


        elif( len( records ) == 0 ):
            #无记录
            TradeContext.errorCode, TradeContext.errorMsg='A0025', "没有满足条件的记录"
            raise AfaFlowControl.flowException( )


        AfaLoggerFunc.tradeInfo( '>>>统计总数' )


        #统计总数
        AfaLoggerFunc.tradeInfo( sql_count )


        records_count=AfaDBFunc.SelectSql( sql_count )

        if( records_count == None ):
            TradeContext.errorCode, TradeContext.errorMsg='A0025', "数据库操作错误"
            raise AfaFlowControl.flowException( )

        # 过滤records中的所有None数据
        records=AfaUtilTools.ListFilterNone( records )

        #总共的返回记录数
        total=len( records )
        AfaLoggerFunc.tradeInfo( '返回记录数:[' + str(total) + ']' )

        #公共部分拼包
        TradeContext.tradeResponse=[]
        TradeContext.tradeResponse.append( ['errorCode',     '0000'] )
        TradeContext.tradeResponse.append( ['errorMsg',      '交易成功'] )
        TradeContext.tradeResponse.append( ['retCount',      str( total )] )
        TradeContext.tradeResponse.append( ['retTotalCount', str( records_count[0][0] )])
        TradeContext.tradeResponse.append( ['retTotalAmount',str( records_count[0][1] )])


        if ( TradeContext.TransType == '0' ):
            #按照变量名打包
            for i in range( 0, total ):
                k=0
                for name in names:
                    if( int( TradeContext.orderMode ) == 1 ):
                        TradeContext.tradeResponse.append( [name, records[i][k]] )
                    else:
                        TradeContext.tradeResponse.append( [name, records[total-i-1][k]] )
                    k=k+1
        else:
            MxFileName = os.environ['AFAP_HOME'] + '/tmp/MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'
            AfaLoggerFunc.tradeInfo('明细文件:['+MxFileName+']')

            if (os.path.exists(MxFileName) and os.path.isfile(MxFileName)):
                #文件存在,先删除-再创建
                os.system("rm " + MxFileName)

            #创建明细文件
            sfp = open(MxFileName, "w")

            #将每条记录打包成以竖线分隔的格式
            TradeContext.tradeResponse.append(['filename',  'MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'])

            for i in range( 0, total ):
                tmpBuffer = ""
                tmpBuffer = tmpBuffer + str(records[i][0]).strip()   + "|"         #AGENTSERIALNO
                tmpBuffer = tmpBuffer + str(records[i][1]).strip()   + "|"         #SYSID
                tmpBuffer = tmpBuffer + str(records[i][2]).strip()   + "|"         #UNITNO
                tmpBuffer = tmpBuffer + str(records[i][3]).strip()   + "|"         #SUBUNITNO
                tmpBuffer = tmpBuffer + str(records[i][4]).strip()   + "|"         #WORKDATE
                tmpBuffer = tmpBuffer + str(records[i][5]).strip()   + "|"         #WORKTIME
                tmpBuffer = tmpBuffer + str(records[i][6]).strip()   + "|"         #AGENTFLAG
                tmpBuffer = tmpBuffer + str(records[i][7]).strip()   + "|"         #TRXCODE
                tmpBuffer = tmpBuffer + str(records[i][8]).strip()   + "|"         #ZONENO
                tmpBuffer = tmpBuffer + str(records[i][9]).strip()   + "|"         #BRNO
                tmpBuffer = tmpBuffer + str(records[i][10]).strip()  + "|"         #TELLERNO
                tmpBuffer = tmpBuffer + str(records[i][11]).strip()  + "|"         #CHANNELCODE
                tmpBuffer = tmpBuffer + str(records[i][12]).strip()  + "|"         #ACCTYPE
                tmpBuffer = tmpBuffer + str(records[i][13]).strip()  + "|"         #DRACCNO
                tmpBuffer = tmpBuffer + str(records[i][14]).strip()  + "|"         #CRACCNO
                tmpBuffer = tmpBuffer + str(records[i][15]).strip()  + "|"         #USERNO
                tmpBuffer = tmpBuffer + str(records[i][16]).strip()  + "|"         #SUBUSERNO
                tmpBuffer = tmpBuffer + str(records[i][17]).strip()  + "|"         #USERNAME
                tmpBuffer = tmpBuffer + str(records[i][18]).strip()  + "|"         #VOUHTYPE
                tmpBuffer = tmpBuffer + str(records[i][19]).strip()  + "|"         #VOUHNO
                tmpBuffer = tmpBuffer + str(records[i][20]).strip()  + "|"         #VOUHDATE
                tmpBuffer = tmpBuffer + str(records[i][21]).strip()  + "|"         #AMOUNT
                tmpBuffer = tmpBuffer + str(records[i][22]).strip()  + "|"         #SUBAMOUNT
                tmpBuffer = tmpBuffer + str(records[i][23]).strip()  + "|"         #BANKSTATUS
                tmpBuffer = tmpBuffer + str(records[i][24]).strip()  + "|"         #BANKSERNO
                tmpBuffer = tmpBuffer + str(records[i][25]).strip()  + "|"         #CORPSTATUS
                tmpBuffer = tmpBuffer + str(records[i][26]).strip()  + "|"         #ERRORMSG
                tmpBuffer = tmpBuffer + str(records[i][27]).strip()  + "|"         #NOTE1
                tmpBuffer = tmpBuffer + str(records[i][28]).strip()  + "|"         #NOTE2
                tmpBuffer = tmpBuffer + str(records[i][29]).strip()  + "|"         #NOTE3
                tmpBuffer = tmpBuffer + str(records[i][30]).strip()  + "|"         #NOTE4
                tmpBuffer = tmpBuffer + str(records[i][31]).strip()  + "|"         #NOTE5
                tmpBuffer = tmpBuffer + str(records[i][32]).strip()  + "|"         #NOTE6
                tmpBuffer = tmpBuffer + str(records[i][33]).strip()  + "|"         #NOTE7
                tmpBuffer = tmpBuffer + str(records[i][34]).strip()  + "|"         #NOTE8
                tmpBuffer = tmpBuffer + str(records[i][35]).strip()  + "|"         #NOTE9
                tmpBuffer = tmpBuffer + str(records[i][36]).strip()  + "|"         #NOTE10

                sfp.write(tmpBuffer + '\n')
                    
            sfp.close()

        #=====================自动打包==========================================
        AfaFunc.autoPackData()

        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo( '******代收代付.查询明细模板['+TradeContext.TemplateCode+']退出******' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
