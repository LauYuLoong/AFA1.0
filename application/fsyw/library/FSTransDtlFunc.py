# -*- coding: gbk -*-
##################################################################
#   代收代付平台.交易流水表操作类
#=================================================================
#   程序文件:   TransDtlFunc.py
#   修改时间:   2006-03-31
##################################################################
import TradeContext, AfaLoggerFunc, AfaDBFunc, AfaUtilTools
from types import *

################################################################################
# 函数名:    InsertDtl
# 参数:      无
# 返回值：    True  插入流水表成功    False 插入流水表失败
# 函数说明：  将流水信息插入流水表
################################################################################
def InsertDtl( ):

    AfaLoggerFunc.tradeInfo( '插入流水表' )

    # count 流水表的列数-1
    count=47
    TransDtl=[[]]*( count+1 )
    TransDtl[0] = TradeContext.agentSerialno    # SERIALNO 代理业务流水号
    TransDtl[1] = TradeContext.workDate         # WORKDATE   交易日期 yyyymmdd
    TransDtl[2] = TradeContext.workDate[4:6]    # MONTH      交易月份
    TransDtl[3] = TradeContext.workTime         # WORKTIME   交易时间
    TransDtl[4] = TradeContext.appNo            # APPNO  代理业务代码
    TransDtl[5] = TradeContext.busiNo           # BUSINO  代理业务方式
    TransDtl[6] = TradeContext.TransCode        # TRXCODE    交易码
    TransDtl[7] = TradeContext.zoneno           # ZONENO   代理业务地区号
    TransDtl[8] = TradeContext.brno             # BRNO       网点号
    TransDtl[9] = TradeContext.teller           # TELLERNO   柜员号
    if( TradeContext.existVariable( "authTeller" ) ) :
        TransDtl[10] = TradeContext.authTeller  # AUTHTELLERNO  授权柜员号
    else:
        TransDtl[10] = ''

    TransDtl[11] = TradeContext.channelCode     # CHANNELCODE   渠道代码

    if( TradeContext.existVariable( "termId" ) ):
        TransDtl[12] = TradeContext.termId      # TERMID     终端号
    else:
        TransDtl[12]=''

    TransDtl[13] = TradeContext.catrFlag        #CATRFLAG 现转标志

    if( TradeContext.existVariable("vouhType") ): #VOUHTPYE 凭证类型
        TransDtl[14] = TradeContext.vouhType
    else:
        TransDtl[14]=''

    if( TradeContext.existVariable("vouhNo")):   #VOUHNO 凭证号码
        TransDtl[15] = TradeContext.vouhNo
    else:
        TransDtl[15] = ''

    if (TradeContext.existVariable( "accno" )):       #ACCNO 银行帐号
        TransDtl[16] = TradeContext.accno
    else:
        TransDtl[16] = ''

    if (TradeContext.existVariable ("subAccno")):     #SUBACCNO 子帐号
        TransDtl[17] = TradeContext.subAccno
    else:
        TransDtl[17] = ''

    TransDtl[18] = AfaUtilTools.lrtrim(TradeContext.userNo)          # userNo     用户号

    if( TradeContext.existVariable( "subuserNo" ) ):
        TransDtl[19] = TradeContext.subuserNo   # SUBuserNo  附加用户号
    else:
        TransDtl[19] = ''

    if( TradeContext.existVariable( "userName" ) ):
        TransDtl[20] = TradeContext.userName    # USERNAME   用户名称
    else:
        TransDtl[20] = ''

    if( TradeContext.existVariable( "contractno" ) ):
        TransDtl[21] = TradeContext.contractno  # CONTRACTNO  合同号
    else:
        TransDtl[21] = ''

    TransDtl[22] = AfaUtilTools.lrtrim(TradeContext.amount)         # AMOUNT       交易金额

    if( TradeContext.existVariable( "subAmount" ) ):
        TransDtl[23] = TradeContext.subAmount  # SUBAMOUNT    附加金额
    else:
        TransDtl[23] = ''

    TransDtl[24] = TradeContext.revTranF       # REVTRANF    反交易标志
                                               # 0:正交易、1:反交易、2.自动冲正

    if( int( TradeContext.revTranF ) != 0 ):
        TransDtl[25] = TradeContext.revTrxDate  #REVTRXDATE    原交易日期
    else:
        TransDtl[25] = ''

    if( int( TradeContext.revTranF ) != 0 ):
        TransDtl[26] = TradeContext.preAgentSerno  #PREAGENTSERNO    原平台流水号
    else:
        TransDtl[26] = ''

    TransDtl[27] = '2'                   # BANKSTATUS     银行交易状态
    TransDtl[28] = ''                    # BANKCODE       银行.交易返回码
    TransDtl[29] = ''                    # BANKSERNO      银行.交易流水号

    TransDtl[30] = '2'                   # CORPSTATUS     第三方交易状态
    TransDtl[31] = ''                    # CORPCODE       第三方.交易返回码
    TransDtl[32] = ''                    # CORPSERNO      第三方.交易流水号
    TransDtl[33] = ''                    # CORPTIME       第三方.交易日期时间戳

    TransDtl[34] = ''                    # ERRORMSG       交易返回信息
    TransDtl[35] = '9'                   # CHKFLAG        主机对帐标志

    #=======张恒增加,如果字段没有值取空值====
    if( TradeContext.existVariable( "__agentEigen__" ) ) :
        TransDtl[36] = TradeContext.__agentEigen__     # APPENDFLAG         从表标志
    else:
        TransDtl[36] = ""     # APPENDFLAG         从表标志


    if( TradeContext.existVariable( "ifTrxSerno" ) != 0 ):
        TransDtl[37] = TradeContext.ifTrxSerno    # IFTRXSERNO    外围交易流水号
    else:
        TransDtl[37] = ''

    if( TradeContext.existVariable( "unitno" ) ):
        TransDtl[38] = TradeContext.unitno        # NOTE1          备注1(单位代码)
    elif( TradeContext.existVariable( "note1" ) ):
        TransDtl[38] = TradeContext.note1
    else:
        TransDtl[38] = ''

    if( TradeContext.existVariable( "note2" ) ):
        TransDtl[39] = TradeContext.note2         # NOTE2          备注2
    else:
        TransDtl[39] = ''

    if( TradeContext.existVariable( "note3" ) ):
        TransDtl[40] = TradeContext.note3         # NOTE3          备注3
    else:
        TransDtl[40] = ''

    if( TradeContext.existVariable( "note4" ) ):
        TransDtl[41] = TradeContext.note4         # NOTE4          备注4
    else:
        TransDtl[41] = ''

    if( TradeContext.existVariable( "note5" ) ):
        TransDtl[42] = TradeContext.note5         # NOTE5          备注5
    else:
        TransDtl[42] = ''

    if( TradeContext.existVariable( "note6" ) ):
        TransDtl[43] = TradeContext.note6         # NOTE6          备注6
    else:
        TransDtl[43] = ''

    if( TradeContext.existVariable( "note7" ) ):
        TransDtl[44] = TradeContext.note7         # NOTE7          备注7
    else:
        TransDtl[44] = ''

    if( TradeContext.existVariable( "note8" ) ):
        TransDtl[45] = TradeContext.note8         # NOTE8          备注8
    else:
        TransDtl[45] = ''

    if( TradeContext.existVariable( "note9" ) ):
        TransDtl[46] = TradeContext.note9         # NOTE9          备注9
    else:
        TransDtl[46] = ''

    if( TradeContext.existVariable( "note10" ) ):
        TransDtl[47] = TradeContext.note10        # NOTE10          备注10
    else:
        TransDtl[47] = ''

    sql="INSERT INTO FS_MAINTRANSDTL(SERIALNO,WORKDATE,MONTH, \
         WORKTIME,APPNO,BUSINO,TRXCODE,ZONENO,BRNO,TELLERNO, \
         AUTHTELLERNO,CHANNELCODE,TERMID,CATRFLAG,VOUHTYPE,VOUHNO,ACCNO, \
         SUBACCNO,userNo,SUBuserNo,USERNAME,CONTRACTNO,AMOUNT,SUBAMOUNT, \
         REVTRANF,REVTRXDATE,REVAGENTSERNO,BANKSTATUS,BANKCODE,BANKSERNO, \
         CORPSTATUS,CORPCODE,CORPSERNO,CORPTIME,ERRORMSG,CHKFLAG, APPENDFLAG, \
         IFTRXSERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9, \
         NOTE10) VALUES("
    i=0
    for i in range( 0, count ):
        if( type( TransDtl[i] ) is int ):
            sql=sql+str( TransDtl[i] )+","
        else:
            sql=sql+"'"+ TransDtl[i]+"',"

    sql=sql+"'"+TransDtl[count]+"')"

    result=AfaDBFunc.InsertSqlCmt( sql )
    if( result < 1 ):
        # AfaLoggerFunc.tradeFatal( sql )
        TradeContext.errorCode, TradeContext.errorMsg='A0044', '插入流水主表失败'+AfaDBFunc.sqlErrMsg
        return False
    else:
        TradeContext.errorCode, TradeContext.errorMsg='0000', 'TransOk'
        AfaLoggerFunc.tradeInfo( '插入流水表完成' )
        return True

################################################################################
# 函数名:    UpdatePreDtl
# 参数:      action  可以是 'BANK','CORP','TRADE'
#                   'BANK'  更新银行的业务状态
#                   'CORP'  更新企业的业务状态
#                   'TRADE' 更新整个交易的业务状态。主要用于只有第三方或者只有银行主机的交易
# 返回值：    True  更新原交易流水成功    False 更新原交易流水失败
# 函数说明：  更新原交易流水，根据入口参数更新不同的状态标识。
################################################################################
def UpdatePreDtl( action ):

    AfaLoggerFunc.tradeInfo( '更新原交易流水' )
    sql="UPDATE FS_MAINTRANSDTL SET "
    if( action == 'BANK' ):
        sql=sql+" BANKSTATUS='3' "
    elif( action == 'CORP' ):
        sql=sql+" CORPSTATUS='3' "
    elif( action == 'TRADE' ):
        sql=sql+" BANKSTATUS='3' ,CORPSTATUS='3'"
    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0041', '入口参数条件不符，没有这种类型的操作'
        return False

    sql=sql+" WHERE SERIALNO='"+TradeContext.preAgentSerno+ \
    "' AND WORKDATE='"+TradeContext.workDate+"' AND REVTRANF='0'"

    ret=AfaDBFunc.UpdateSql( sql )
    if( ret >0 ):
        return True

    AfaLoggerFunc.tradeFatal( sql )
    if( ret == 0 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '未发现原始交易'
    else :
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新流水主表原交易记录失败'+AfaDBFunc.sqlErrMsg

    return False

################################################################################
# 函数名:    UpdateDtl
# 参数:      action  可以是 'BANK','CORP','TRADE'
#                   'BANK'  更新银行的业务状态
#                   'CORP'  更新企业的业务状态
#                   'TRADE' 更新整个交易的业务状态。主要用于只有第三方或者只有银行主机的交易
# 返回值：    True  更新当前交易流水成功    False 更新当前交易流水失败
# 函数说明：  更新当前交易流水，根据入口参数更新不同的状态标识。
################################################################################
def UpdateDtl( action ):

    AfaLoggerFunc.tradeInfo( '更新本交易流水[begin]['+ action + ']' )
    sql="UPDATE FS_MAINTRANSDTL SET "
    if( TradeContext.existVariable( "errorMsg" ) ):
        sql=sql+"ERRORMSG='"+TradeContext.errorMsg+"',"

    if( action == 'BANK' ):
        sql=sql+"BANKSTATUS='"+TradeContext.__status__+"',BANKCODE='"+ \
        TradeContext.errorCode+"'"
        if( TradeContext.existVariable( "bankSerno" ) ):
            sql=sql+",BANKSERNO='"+TradeContext.bankSerno+"'"

    elif( action == 'CORP' ):
        sql=sql+"CORPSTATUS='"+TradeContext.__status__+"',CORPCODE='"+ \
        TradeContext.errorCode+"'"
        if( TradeContext.existVariable( "corpSerno" ) ):
            sql=sql+",CORPSERNO='"+TradeContext.corpSerno+"'"
        if( TradeContext.existVariable( "corpTime" ) ):
            sql=sql+",CORPTIME='"+TradeContext.corpTime+"'"

    elif( action == 'TRADE' ):
        sql=sql+"CORPSTATUS='"+TradeContext.__status__+"',BANKSTATUS='"+ \
        TradeContext.__status__+"',CORPCODE='"+TradeContext.errorCode+ \
        "',BANKCODE='"+TradeContext.errorCode+"'"
        if( TradeContext.existVariable( "bankSerno" ) ):
            sql=sql+",BANKSERNO='"+TradeContext.bankSerno+"'"
        if( TradeContext.existVariable( "corpSerno" ) ):
            sql=sql+",CORPSERNO='"+TradeContext.corpSerno+"'"
        if( TradeContext.existVariable( "corpTime" ) ):
            sql=sql+",CORPTIME='"+TradeContext.corpTime+"'"

    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0041', '入口参数条件不符，没有这种类型的操作'
        return False

    if( TradeContext.existVariable( "unitno" ) ):
        sql=sql+",NOTE1='"+  TradeContext.unitno+"'"      # NOTE1          备注1(单位代码)

    elif( TradeContext.existVariable( "note1" ) ):
        sql=sql+",NOTE1='"+  TradeContext.note1+"'"

    if( TradeContext.existVariable( "note2" ) ):
        sql=sql+",NOTE2='"+  TradeContext.note2+"'"       # NOTE2          备注2

    if( TradeContext.existVariable( "note3" ) ):
        sql=sql+",NOTE3='"+  TradeContext.note3+"'"

    if( TradeContext.existVariable( "note4" ) ):
        sql=sql+",NOTE4='"+  TradeContext.note4+"'"        # NOTE4          备注4

    if( TradeContext.existVariable( "note5" ) ):
        sql=sql+",NOTE5='"+  TradeContext.note5+"'"         # NOTE5          备注5

    if( TradeContext.existVariable( "note6" ) ):
        sql=sql+",NOTE6='"+  TradeContext.note6+"'"         # NOTE6          备注6

    if( TradeContext.existVariable( "note7" ) ):
        sql=sql+",NOTE7='"+  TradeContext.note7+"'"         # NOTE7          备注7

    if( TradeContext.existVariable( "note8" ) ):
        sql=sql+",NOTE8='"+  TradeContext.note8+"'"         # NOTE8          备注8

    if( TradeContext.existVariable( "note9" ) ):
        sql=sql+",NOTE9='"+  TradeContext.note9+"'"         # NOTE9          备注9

    if( TradeContext.existVariable( "note10" ) ):
        sql=sql+",NOTE10='"+  TradeContext.note10+"'"        # NOTE10          备注10

    sql=sql+" WHERE SERIALNO='"+TradeContext.agentSerialno+ \
    "' AND WORKDATE='"+TradeContext.workDate+ \
    "' AND REVTRANF='"+TradeContext.revTranF+"'"

    if( int( TradeContext.revTranF )!=0 and TradeContext.errorCode == '0000'):
        if( not UpdatePreDtl( action ) ):
            return False

    if( AfaDBFunc.UpdateSqlCmt( sql )<1 ):
        # AfaLoggerFunc.tradeFatal( sql )
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新流水主表失败'+AfaDBFunc.sqlErrMsg
        return False

    if( TradeContext.errorCode != '0000' ):
        return  False

    AfaLoggerFunc.tradeInfo( '更新本交易流水[end]['+ action + ']' )

    return True
