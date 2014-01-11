# -*- coding: gbk -*-
##################################################################
#   中间业务平台.交易流水表操作类
#=================================================================
#   程序文件:   AfaTransDtlFunc.py
#   修改时间:   2006-03-31
##################################################################
import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,AfaFlowControl,TransBillFunc,AfaFunc
from types import *


################################################################################
# 函数名:    InsertDtl
# 参数:      无
# 返回值：    True  插入流水表成功    False 插入流水表失败
# 函数说明：  将流水信息插入流水表
################################################################################
def InsertDtl( ):

    AfaLoggerFunc.tradeInfo( '>>>插入流水表' )

    #流水表的列数-1
    count=52
    TransDtl=[[]]*( count+1 )
    TransDtl[0] = TradeContext.agentSerialno                    # AGENTSERIALNO 代理业务流水号
    TransDtl[1] = TradeContext.workDate                         # WORKDATE      交易日期
    TransDtl[2] = TradeContext.workTime                         # WORKTIME      交易时间
    TransDtl[3] = TradeContext.sysId                            # SYSID         系统标识
    TransDtl[4] = TradeContext.unitno                           # UNITNO        商户单位代码
    TransDtl[5] = TradeContext.subUnitno                        # SUBUNITNO     商户分支单位代码
    TransDtl[6] = TradeContext.agentFlag                        # AGENTFLAG     业务方式
    TransDtl[7] = TradeContext.TransCode                        # TRXCODE       交易码
    TransDtl[8] = TradeContext.zoneno                           # ZONENO        分行号
    TransDtl[9] = TradeContext.brno                             # BRNO          行所号
    TransDtl[10]= TradeContext.tellerno                         # TELLERNO      柜员号
    TransDtl[11]= TradeContext.cashTelno                        # CASHTELNO     出纳员号

    if( TradeContext.existVariable( "authTeller" ) ) :
        TransDtl[12] = TradeContext.authTeller                  # AUTHTELLERNO  授权柜员号  
    else:
        TransDtl[12] = ''

    TransDtl[13] = TradeContext.channelCode                     # CHANNELCODE   渠道代码

    if( TradeContext.existVariable( "channelSerno" ) ):
        TransDtl[14] = TradeContext.channelSerno                # CHANNELSERNO  渠道交易流水号
    else:
        TransDtl[14]=''

    if( TradeContext.existVariable( "termId" ) ):
        TransDtl[15] = TradeContext.termId                      # TERMID        终端号
    else:
        TransDtl[15]=''

    if( TradeContext.existVariable( "customerId" ) ):
        TransDtl[16] = TradeContext.customerId                  # CUSTOMERID    客户注册号
    else:
        TransDtl[16]=''

    TransDtl[17] = TradeContext.userno                          # USERNO        用户号  

    if( TradeContext.existVariable( "subUserno" ) ):
        TransDtl[18] = TradeContext.subUserno                   # SUBUSERNO     附加用户号  
    else:
        TransDtl[18] = ''

    if( TradeContext.existVariable( "userName" ) ):
        TransDtl[19] = TradeContext.userName                    # USERNAME      用户名称  
    else:
        TransDtl[19] = '' 

    if( TradeContext.existVariable( "accType" ) ):
        TransDtl[20] = TradeContext.accType                     # ACCTYPE       帐户类型
    else:
        TransDtl[20] = '000'


    #单位帐号
    if( TradeContext.existVariable( "__agentAccno__" ) ):
        agentAccno = TradeContext.__agentAccno__
    else:
        agentAccno = ''


    #客户帐号
    if( TradeContext.existVariable( "accno" ) ):
        accno = TradeContext.accno
    else:
        accno = ''

 
    if( int( TradeContext.revTranF ) == 0 ):
        #业务方式(01-代收 02-代付 03-批扣 04-批付)
        if( int( TradeContext.agentFlag ) == 1 or int( TradeContext.agentFlag ) == 3 ):
            TransDtl[21] = accno                                # DRACCNO       借方帐号
            TransDtl[22] = agentAccno                           # CRACCNO       贷方帐号 
            TradeContext.__drAccno__ = accno
            TradeContext.__crAccno__ = agentAccno
        else:
            TransDtl[21] = agentAccno
            TransDtl[22] = accno
            TradeContext.__drAccno__ = agentAccno
            TradeContext.__crAccno__ = accno
    else:
        TransDtl[21] = TradeContext.__drAccno__                 # DRACCNO       借方帐号
        TransDtl[22] = TradeContext.__crAccno__                 # DRACCNO       贷方帐号


    if( TradeContext.existVariable( "vouhType" ) ):
        TransDtl[23] = TradeContext.vouhType                    # VOUHTYPE      凭证种类  
    else:
        TransDtl[23] = ''


    if( TradeContext.existVariable( "vouhno" ) ):
        TransDtl[24] = TradeContext.vouhno                      # VOUHNO        凭证号  
    else:
        TransDtl[24] = ''


    if( TradeContext.existVariable( "vouhDate" ) ):
        TransDtl[25] = TradeContext.vouhDate                    # VOUHDATE      凭证日期  
    else:
        TransDtl[25] = ''


    if( TradeContext.existVariable( "currType" ) ):
        TransDtl[26] = TradeContext.currType                    # CURRTYPE      币种
    else:
        TransDtl[26] = '1'

    
    if( TradeContext.existVariable( "currFlag" ) ):
        TransDtl[27] = TradeContext.currFlag                    # CURRFLAG      钞汇标志
    else:
        TransDtl[27] = '0'


    TransDtl[28] = TradeContext.amount                          # AMOUNT        交易金额


    if( TradeContext.existVariable( "subAmount" ) ):
        TransDtl[29] = TradeContext.subAmount                   # SUBAMOUNT     附加金额  
    else:
        TransDtl[29] = ''


    TransDtl[30] = TradeContext.revTranF                        # REVTRANF      反交易标志(0-正交易 1-反交易 2-自动冲正)
                                               
    if( int( TradeContext.revTranF ) != 0 ):
        TransDtl[31] = TradeContext.preAgentSerno               # PREAGENTSERNO 原平台流水号  
    else:
        TransDtl[31] = ''

    TransDtl[32] = '2'                                          # BANKSTATUS    银行.交易状态(0-正常 1-失败 2-异常 3-已冲正)
    TransDtl[33] = ''                                           # BANKCODE      银行.交易返回码
    TransDtl[34] = ''                                           # BANKSERNO     银行.交易流水号

    TransDtl[35] = '2'                                          # CORPSTATUS    企业.交易状态(0-正常 1-失败 2-异常 3-已冲正)
    TransDtl[36] = ''                                           # CORPCODE      企业.交易返回码
    TransDtl[37] = ''                                           # CORPSERNO     企业.交易流水号
    TransDtl[38] = ''                                           # CORPTIME      企业.时间戳

    TransDtl[39] = ''                                           # ERRORMSG      交易返回信息
                                                                
    TransDtl[40] = '9'                                          # CHKFLAG       主机对帐标志(0-已对帐,交易成功 1-已对帐,交易失败, 9-未对帐) 
                                                                
    TransDtl[41] = '9'                                          # CORPCHKFLAG   企业对帐标志(0-已对帐,交易成功 1-已对帐,交易失败, 9-未对帐)

    TransDtl[42] = TradeContext.__agentEigen__[4]               # APPENDFLAG    从表使用标志(0-不使用 1-使用)

    if( TradeContext.existVariable( "note1" ) ):                # NOTE1         备注1
        TransDtl[43] = TradeContext.note1
    else:
        TransDtl[43] = ''

    if( TradeContext.existVariable( "note2" ) ):
        TransDtl[44] = TradeContext.note2                       # NOTE2         备注2
    else:                                                       
        TransDtl[44] = ''                                       
                                                                
    if( TradeContext.existVariable( "note3" ) ):                
        TransDtl[45] = TradeContext.note3                       # NOTE3         备注3
    else:                                                       
        TransDtl[45] = ''                                       
                                                                
    if( TradeContext.existVariable( "note4" ) ):                
        TransDtl[46] = TradeContext.note4                       # NOTE4         备注4
    else:                                                       
        TransDtl[46] = ''                                       
                                                                
    if( TradeContext.existVariable( "note5" ) ):                
        TransDtl[47] = TradeContext.note5                       # NOTE5         备注5
    else:                                                       
        TransDtl[47] = ''                                       
                                                                
    if( TradeContext.existVariable( "note6" ) ):                
        TransDtl[48] = TradeContext.note6                       # NOTE6         备注6
    else:                                                       
        TransDtl[48] = ''                                       
                                                                
    if( TradeContext.existVariable( "note7" ) ):                
        TransDtl[49] = TradeContext.note7                       # NOTE7         备注7
    else:                                                       
        TransDtl[49] = ''                                       
                                                                
    if( TradeContext.existVariable( "note8" ) ):                
        TransDtl[50] = TradeContext.note8                       # NOTE8         备注8
    else:                                                       
        TransDtl[50] = ''                                       
                                                                
    if( TradeContext.existVariable( "note9" ) ):                
        TransDtl[51] = TradeContext.note9                       # NOTE9         备注9
    else:                                                       
        TransDtl[51] = ''                                       
                                                                
    if( TradeContext.existVariable( "note10" ) ):               
        TransDtl[52] = TradeContext.note10                      # NOTE10        备注10
    else:
        TransDtl[52] = ''

    sql = "INSERT INTO AFA_MAINTRANSDTL(AGENTSERIALNO,WORKDATE,"
    sql = sql + "WORKTIME,SYSID,UNITNO,SUBUNITNO,AGENTFLAG,TRXCODE,ZONENO,BRNO,TELLERNO,CASHTELNO,"
    sql = sql + "AUTHTELLERNO,CHANNELCODE,CHANNELSERNO,TERMID,CUSTOMERID,USERNO,SUBUSERNO,USERNAME,"
    sql = sql + "ACCTYPE,DRACCNO,CRACCNO,VOUHTYPE,VOUHNO,VOUHDATE,"
    sql = sql + "CURRTYPE,CURRFLAG,AMOUNT,SUBAMOUNT,REVTRANF,PREAGENTSERNO,BANKSTATUS,BANKCODE,"
    sql = sql + "BANKSERNO,CORPSTATUS,CORPCODE,CORPSERNO,CORPTIME,ERRORMSG,CHKFLAG,CORPCHKFLAG,"
    sql = sql + "APPENDFLAG,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9,"
    sql = sql + "NOTE10) VALUES("
    
    i=0
    for i in range( 0, count ):
        if( type( TransDtl[i] ) is int ):
            sql=sql+str( TransDtl[i] )+","
        else:
            sql=sql+"'"+ TransDtl[i]+"',"
            
    sql=sql+"'"+TransDtl[count]+"')"

    AfaLoggerFunc.tradeInfo( sql )
    
    result=AfaDBFunc.InsertSqlCmt( sql )
        
    if( result < 1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0044', '插入流水主表失败'+AfaDBFunc.sqlErrMsg
        return False

    else:
        #特征码:子表使用标志(反交易忽略)
        if ( TradeContext.__agentEigen__[4]=='1' and TradeContext.revTranF=='0' ):
            if( not SubTransDtlProc( '1' ) ):
                TradeContext.errorCode, TradeContext.errorMsg='A0040', '子表操作失败'
                return False

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

    AfaLoggerFunc.tradeInfo( '>>>更新原交易流水信息' )
        
    sqlstr="UPDATE AFA_MAINTRANSDTL SET "
    
    if( action == 'BANK' ):
        sqlstr=sqlstr+" BANKSTATUS='3' "

    elif( action == 'CORP' ):
        sqlstr=sqlstr+" CORPSTATUS='3' "

    elif( action == 'TRADE' ):
        sqlstr=sqlstr+" BANKSTATUS='3',CORPSTATUS='3'"
        
    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0041', '入口参数条件不符，没有这种类型的操作'
        return False
        
        
    sqlstr = sqlstr + " WHERE "

    #原交易流水号
    if(TradeContext.existVariable( "preAgentSerno" )) :
        sqlstr=sqlstr + " AGENTSERIALNO='"+TradeContext.preAgentSerno+"' AND "
        
    #原渠道流水号
    if(TradeContext.existVariable( "preChannelSerno" )) :
        sqlstr=sqlstr + " CHANNELSERNO='"+TradeContext.preChannelSerno+"' AND "
        
    sqlstr = sqlstr + " WORKDATE='" + TradeContext.workDate + "' AND REVTRANF='0'"

    AfaLoggerFunc.tradeInfo( sqlstr )

    ret=AfaDBFunc.UpdateSqlCmt( sqlstr )
    if( ret > 0 ):
        return True

    if( ret == 0 ):
        TradeContext.errorCode,TradeContext.errorMsg='A0100','未发现原始交易'
        return False

    else :
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新原交易状态失败' + AfaDBFunc.sqlErrMsg    
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

    AfaLoggerFunc.tradeInfo( '>>>更新交易流水状态(' + action + ')' )
        
    sql = "UPDATE AFA_MAINTRANSDTL SET "

    if( TradeContext.existVariable( "errorMsg" ) ):
        sql = sql + "ERRORMSG='" + TradeContext.errorMsg + "',"

    if( action == 'BANK' ):
        sql = sql + "BANKSTATUS='" + TradeContext.__status__+ "',BANKCODE='" + TradeContext.errorCode + "'"
        
        if( TradeContext.existVariable( "bankSerno" ) ):
            sql = sql + ",BANKSERNO='" + TradeContext.bankSerno + "'"

    elif( action == 'CORP' ):
        sql = sql + "CORPSTATUS='" + TradeContext.__status__ + "',CORPCODE='" + TradeContext.errorCode + "'"
        
        if( TradeContext.existVariable( "corpSerno" ) ):
            sql = sql + ",CORPSERNO='" + TradeContext.corpSerno + "'"

        if( TradeContext.existVariable( "corpTime" ) ):
            sql = sql + ",CORPTIME='"  + TradeContext.corpTime  + "'"

    elif( action == 'TRADE' ):
        sql = sql + "CORPSTATUS='" + TradeContext.__status__ + "',BANKSTATUS='" + TradeContext.__status__ + "',CORPCODE='" + TradeContext.errorCode + "',BANKCODE='" + TradeContext.errorCode + "'"
        
        if( TradeContext.existVariable( "bankSerno" ) ):
            sql = sql + ",BANKSERNO='" + TradeContext.bankSerno + "'"

        if( TradeContext.existVariable( "corpSerno" ) ):
            sql = sql + ",CORPSERNO='" + TradeContext.corpSerno + "'"

        if( TradeContext.existVariable( "corpTime" ) ):
            sql = sql + ",CORPTIME='"  + TradeContext.corpTime  + "'"

    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0041', '入口参数条件不符，没有这种类型的操作'
        return False


    if( TradeContext.existVariable( "note1" ) ):
        sql = sql + ",NOTE1='" +  TradeContext.note1 + "'"              # NOTE1         备注1

    if( TradeContext.existVariable( "note2" ) ):
        sql = sql + ",NOTE2='" +  TradeContext.note2 + "'"              # NOTE2         备注2

    if( TradeContext.existVariable( "note3" ) ):
        sql = sql + ",NOTE3='" +  TradeContext.note3 + "'"              # NOTE3         备注3

    if( TradeContext.existVariable( "note4" ) ):
        sql = sql + ",NOTE4='" +  TradeContext.note4 + "'"              # NOTE4         备注4

    if( TradeContext.existVariable( "note5" ) ):
        sql = sql + ",NOTE5='" +  TradeContext.note5 + "'"              # NOTE5         备注5

    if( TradeContext.existVariable( "note6" ) ):
        sql = sql + ",NOTE6='" +  TradeContext.note6 + "'"              # NOTE6         备注6

    if( TradeContext.existVariable( "note7" ) ):
        sql = sql + ",NOTE7='" +  TradeContext.note7 + "'"              # NOTE7         备注7

    if( TradeContext.existVariable( "note8" ) ):
        sql = sql + ",NOTE8='" +  TradeContext.note8 + "'"              # NOTE8         备注8

    if( TradeContext.existVariable( "note9" ) ):
        sql = sql + ",NOTE9='" +  TradeContext.note9 + "'"              # NOTE9         备注9

    if( TradeContext.existVariable( "note10" ) ):
        sql = sql + ",NOTE10='"+  TradeContext.note10+ "'"              # NOTE10        备注10
        
        
    sql = sql + " WHERE AGENTSERIALNO='" + TradeContext.agentSerialno + "' AND WORKDATE='" + TradeContext.workDate + "' AND REVTRANF='" + TradeContext.revTranF + "'"

    #更新原流水状态
    if( int( TradeContext.revTranF )!=0 and TradeContext.errorCode == '0000'):
        if( not UpdatePreDtl( action ) ):
            return False

    AfaLoggerFunc.tradeInfo( sql )


    #更新本流水状态
    AfaLoggerFunc.tradeInfo( '>>>更新本交易流水信息' )
    if( AfaDBFunc.UpdateSqlCmt( sql )<1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新流水主表失败'+AfaDBFunc.sqlErrMsg
        return False


    if( TradeContext.errorCode != '0000' ):
        return  False


    if ( action == 'CORP' ):
        #增加对流水从表的处理
        if ( TradeContext.__agentEigen__[4]=='1' and TradeContext.revTranF=='0' and TradeContext.errorCode=='0000' ):
            if( TradeContext.existVariable( "afe_appendFlag" ) and TradeContext.afe_appendFlag=='1' ):
                if( not SubTransDtlProc( '2' ) ):
                    return False
 
    return True


################################################################################
# 函数名:    SubTransDtlProc
# 参数:      action 1-新增  2-修改
# 返回值：   True  操作当前交易从流水成功    False 操作当前交易从流水失败
# 函数说明： 维护从表信息
################################################################################
def SubTransDtlProc( action ):

    AfaLoggerFunc.tradeInfo( '>>>增加交易流水从表信息' )

    #新增
    if ( action == '1' ):
        sql = "INSERT INTO AFA_SUBTRANSDTL(AGENTSERIALNO,WORKDATE,RECSEQNO,DATA1,DATA2) VALUES("    
        sql = sql + "'"  +  TradeContext.agentSerialno  + "'"
        sql = sql + ",'" +  TradeContext.workDate       + "'"
        sql = sql + ",'" +  '1'                         + "'"

        if( TradeContext.existVariable( "appendData1" ) ):
            sql = sql + ",'" +  TradeContext.appendData1   + "'"
        else:
            sql = sql + ",'" + ""                          + "'"

        if( TradeContext.existVariable( "appendData2" ) ):
            sql = sql + ",'" +  TradeContext.appendData2   + "'"
        else:
            sql = sql + ",'" + ""                          + "'"

        sql = sql + ")"

        AfaLoggerFunc.tradeInfo( sql )
    
        subresult = AfaDBFunc.InsertSqlCmt( sql )

        if( subresult < 1 ):
            TradeContext.errorCode, TradeContext.errorMsg='A0044', '插入流水从表失败'+AfaDBFunc.sqlErrMsg
            return False


    #修改
    if ( action == '2' ):
        sql = "UPDATE AFA_SUBTRANSDTL SET "

        if( TradeContext.existVariable( "afe_appendData1" ) ):
            sql = sql + "DATA1='"  +  TradeContext.afe_appendData1   + "'"

        if( TradeContext.existVariable( "afe_appendData2" ) ):
            sql = sql + ",DATA2='" +  TradeContext.afe_appendData2   + "'"

        sql = sql + " WHERE "

        sql = sql + "AGENTSERIALNO='" +  TradeContext.agentSerialno + "' AND "
        sql = sql + "WORKDATE='"      +  TradeContext.workDate      + "'"

        AfaLoggerFunc.tradeInfo( sql )

        subresult = AfaDBFunc.UpdateSqlCmt( sql )

        if( subresult < 1 ):
            TradeContext.errorCode, TradeContext.errorMsg='A0044', '插入流水从表失败'+AfaDBFunc.sqlErrMsg
            return False

    return True
