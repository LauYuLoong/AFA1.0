# -*- coding: gbk -*-
################################################################################
#   代收代付.柜员轧帐模板
#===============================================================================
#   模板文件:   003102.py
#   修改时间:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc,os
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******代收代付.通用轧帐模板[' + TradeContext.TemplateCode + ']进入******' )

    try:

        #=====================初始化返回报文变量================================
        TradeContext.tradeResponse=[]

        #=====================获取当前系统时间==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================判断应用系统状态==================================
        #if not AfaFunc.ChkSysStatus( ) :
        #    raise AfaFlowControl.flowException( )
                
        #=====================校验公共节点的有效性==============================
        if( not TradeContext.existVariable( "statType" ) ):
            raise AfaFlowControl.flowException( 'A0001', '轧帐类型[statType]值不存在,不能进行轧帐' )

        if( not TradeContext.existVariable( "TransType" ) ):
            raise AfaFlowControl.flowException( 'A0001', '传输类型[TransType]值不存在,不能进行轧帐' )

        AfaLoggerFunc.tradeInfo( '>>>statType  = ' + TradeContext.statType )
        AfaLoggerFunc.tradeInfo( '>>>TransType = ' + TradeContext.TransType)

        #=====================轧帐操作==========================================
        if not StatAccountInfo( TradeContext.statType ) :
            raise AfaFlowControl.flowException( )

        #=====================自动打包==========================================
        TradeContext.tradeResponse.append( ['errorCode',     '0000'] )
        TradeContext.tradeResponse.append( ['errorMsg',      '交易成功'] )

        AfaFunc.autoPackData()

        #=====================退出模板==========================================
        AfaLoggerFunc.tradeInfo( '******代收代付.通用轧帐模板[' + TradeContext.TemplateCode + ']退出******' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )



#=======================汇总统计帐务信息===========================
def StatAccountInfo( statType='0' ):

    AfaLoggerFunc.tradeInfo( '>>>汇总统计帐务信息' )

    tableName="AFA_MAINTRANSDTL"

    #判断轧帐类型(1-按网点轧帐 2-按柜员轧帐)
    if( int( statType )<1 and int( statType )>2 ):
        return AfaFlowControl.ExitThisFlow( 'A0019', '非法的轧帐类型' )

    #=====================变量值的有效性校验====================================
    if( not TradeContext.existVariable( "tradeDate" ) and len(TradeContext.tradeDate)==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '交易日期[tradeDate]值不存在,不能进行轧帐' )

    if( not TradeContext.existVariable( "zoneno" ) and len(TradeContext.zoneno)==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '地区号[zoneno]值不存在,不能进行轧帐' )

    if( not TradeContext.existVariable( "brno" ) and len(TradeContext.brno)==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '网点号[brno]值不存在,不能进行轧帐' )


    #=====================基本条件组合==========================================
    accSqlStr  = " AND WORKDATE='" + TradeContext.tradeDate + "'"

    if(int( statType )==1):                                 #根据网点查询
        accSqlStr = accSqlStr   + " AND ZONENO='"   + TradeContext.zoneno  + "'"
        accSqlStr = accSqlStr   + " AND BRNO='"     + TradeContext.brno    + "'"

    else:                                                   #根据柜员查询
        if( not TradeContext.existVariable( "tellerno" ) and len(TradeContext.tellerno)==0 ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[tellerno]值不存在!' )

        accSqlStr  = accSqlStr  + " AND ZONENO='"   + TradeContext.zoneno   + "'"
        accSqlStr  = accSqlStr  + " AND BRNO='"     + TradeContext.brno     + "'"
        accSqlStr  = accSqlStr  + " AND TELLERNO='" + TradeContext.tellerno + "'"



    #查询系统信息
    sqlStr = "SELECT SYSID,SYSCNAME,SYSENAME FROM AFA_SYSTEM WHERE SUBSTR(SYSID,1,3)='AG2'"

    records = AfaDBFunc.SelectSql( sqlStr )

    AfaLoggerFunc.tradeInfo( sqlStr )

    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0027', '系统表操作异常:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0028', '该地区没有任何系统信息,无需轧帐' )


#    TradeContext.sysId              =[]             #系统标识
#    TradeContext.agentFlag          =[]             #业务方式
#    TradeContext.unitno             =[]             #商户标识
#    TradeContext.subUnitno          =[]             #子商户标识
#    TradeContext.tradeNums          =[]             #交易笔数
#    TradeContext.tradeAmt           =[]             #交易金额
#    TradeContext.tradeNums_acc      =[]             #交易笔数(转帐)
#    TradeContext.tradeAmt_acc       =[]             #交易金额(转帐)
#    TradeContext.tradeNumsOfFail    =[]             #失败笔数
#    TradeContext.tradeNumsOfObnormal=[]             #异常笔数
    queryCount=0


    #过滤records中的所有None数据
    records=AfaUtilTools.ListFilterNone( records )


    AfaLoggerFunc.tradeInfo( '>>>记录数=' + str(len(records)) )

   
    if ( TradeContext.TransType != '0' ):
        MxFileName = os.environ['AFAP_HOME'] + '/tmp/MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'

        AfaLoggerFunc.tradeInfo('>>>轧帐文件:['+MxFileName+']')

        if (os.path.exists(MxFileName) and os.path.isfile(MxFileName)):
            #文件存在,先删除-再创建
            os.system("rm " + MxFileName)

        #创建明细文件
        sfp = open(MxFileName, "w")

        
    for i in range( 0, len( records ) ):

        #########################################################################################
        AfaLoggerFunc.tradeInfo( '>>>成功统计-现金::' )

        sqlStr = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE REVTRANF='0' AND SYSID='" + str(records[i][0]).strip() +  "' AND ACCTYPE='000' AND BANKSTATUS='0' AND CORPSTATUS='0'"
        sqlStr = sqlStr + accSqlStr
        
        AfaLoggerFunc.tradeInfo( sqlStr )

        accRecordsSucc = AfaDBFunc.SelectSql( sqlStr )

        if ( accRecordsSucc == None ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '流水主表操作异常:'+AfaDBFunc.sqlErrMsg )


        #########################################################################################
        AfaLoggerFunc.tradeInfo( '>>>成功统计-转帐::' )

        sqlStr = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE REVTRANF='0' AND SYSID='" + str(records[i][0]).strip() +  "' AND ACCTYPE<>'000' AND BANKSTATUS='0' AND CORPSTATUS='0'"
        sqlStr = sqlStr + accSqlStr

        AfaLoggerFunc.tradeInfo( sqlStr )

        accRecordsSucc_acc = AfaDBFunc.SelectSql( sqlStr )

        if( accRecordsSucc_acc == None ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '流水主表操作异常:'+AfaDBFunc.sqlErrMsg )


        #########################################################################################
        AfaLoggerFunc.tradeInfo( '>>>失败统计::' )
        sqlStr = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE REVTRANF='0' AND SYSID='" + str(records[i][0]).strip() +  "' AND ((AGENTFLAG='01' AND BANKSTATUS='1') OR (AGENTFLAG='02' AND CORPSTATUS='1'))"
        sqlStr = sqlStr + accSqlStr

        accRecordsFail = AfaDBFunc.SelectSql( sqlStr )

        AfaLoggerFunc.tradeInfo( sqlStr )

        if( accRecordsFail == None ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '流水主表操作异常:'+AfaDBFunc.sqlErrMsg )


        #########################################################################################
        AfaLoggerFunc.tradeInfo( '>>>异常统计::' )
        sqlStr = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE REVTRANF='0' AND SYSID='" + str(records[i][0]).strip() +  "' AND ((AGENTFLAG='01' AND BANKSTATUS='0' AND CORPSTATUS<>'0') OR (AGENTFLAG='02' AND CORPSTATUS='0' AND BANKSTATUS<>'0'))"
        sqlStr = sqlStr + accSqlStr

        AfaLoggerFunc.tradeInfo( sqlStr )

        accRecordsObnormal = AfaDBFunc.SelectSql( sqlStr )

        if( accRecordsObnormal == None ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '流水主表操作异常:'+AfaDBFunc.sqlErrMsg )

        if ( TradeContext.TransType=='0' ):
            TradeContext.tradeResponse.append(['sysId',records[i][0]])                                      #系统标识
                
            TradeContext.tradeResponse.append(['sysName',records[i][1]])                                    #系统名称

            TradeContext.tradeResponse.append(['tradeNums', str(accRecordsSucc[0][0])])                     #交易笔数(现金)
            if accRecordsSucc[0][1] == None:
                TradeContext.tradeResponse.append(['tradeAmt','0.00'])                                      #交易金额(现金)
            else:
                TradeContext.tradeResponse.append(['tradeAmt', str(accRecordsSucc[0][1])])


            TradeContext.tradeResponse.append(['tradeNums_acc',str(accRecordsSucc_acc[0][0])])              #交易笔数(转帐)
            if accRecordsSucc_acc[0][1] == None:
                TradeContext.tradeResponse.append(['tradeAmt_acc', '0.00'])                                 #交易金额(转帐)
            else:
                TradeContext.tradeResponse.append(['tradeAmt_acc', str(accRecordsSucc_acc[0][1])])



            TradeContext.tradeResponse.append(['tradeNumsFail', str(accRecordsFail[0][0])])                 #失败笔数
            if accRecordsFail[0][1] == None:
                TradeContext.tradeResponse.append(['tradeAmtFail', '0.00'])                                 #失败金额
            else:
                TradeContext.tradeResponse.append(['tradeAmtFail', str(accRecordsFail[0][1])])


            TradeContext.tradeResponse.append(['tradeNumsObnormal', str(accRecordsObnormal[0][0])])         #异常笔数
            if accRecordsObnormal[0][1] == None:
                TradeContext.tradeResponse.append(['tradeAmtObnormal', '0.00'])                             #异常金额
            else:
                TradeContext.tradeResponse.append(['tradeAmtObnormal', str(accRecordsObnormal[0][1])])

        else:
            wBuffer = ""
            wBuffer = wBuffer + records[i][0]                       + "|"               #系统标识
            wBuffer = wBuffer + records[i][1]                       + "|"               #系统名称


            wBuffer = wBuffer + str(accRecordsSucc[0][0])           + "|"               #交易笔数(现金)
            if accRecordsSucc[0][1] == None:                                            #交易金额(现金)
                wBuffer = wBuffer + '0'                             + "|"
            else:
                wBuffer = wBuffer + str(accRecordsSucc[0][1])       + "|"



            wBuffer = wBuffer + str(accRecordsSucc_acc[0][0])       + "|"               #交易笔数(转帐)
            if accRecordsSucc_acc[0][1] == None:                                        #交易金额(转帐)
                wBuffer = wBuffer + '0'                             + "|"
            else:
                wBuffer = wBuffer + str(accRecordsSucc_acc[0][1])   + "|"



            wBuffer = wBuffer + str(accRecordsFail[0][0])           + "|"               #失败笔数
            if accRecordsFail[0][1] == None:                                            #失败金额
                wBuffer = wBuffer + '0'                             + "|"
            else:
                wBuffer = wBuffer + str(accRecordsFail[0][1])       + "|"


            wBuffer = wBuffer + str(accRecordsObnormal[0][0])       + "|"               #异常笔数
            if accRecordsObnormal[0][1] == None:                                        #异常金额
                wBuffer = wBuffer + '0'                             + "|"
            else:
                wBuffer = wBuffer + str(accRecordsObnormal[0][1])   + "|"

            sfp.write(wBuffer + '\n')
                
        queryCount = queryCount+  1

    if ( TradeContext.TransType != '0' ):
        sfp.close()

        #如果是文件传输方式，则需要返回文件名
        TradeContext.tradeResponse.append(['filename',  'MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'])

    #记录数
    TradeContext.tradeResponse.append(['queryCount',  str(queryCount)])

    return True
