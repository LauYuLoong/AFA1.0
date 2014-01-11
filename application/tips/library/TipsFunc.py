# -*- coding: gbk -*-
###############################################################################
# 文件名称：TipsFunc.py
# 文件标识：
# 摘    要：财税库行横向联网系统公共函数库
#
# 当前版本：1.0
# 作    者：zzh
# 完成日期：2007-6-7 
#
# 取代版本：
# 原 作 者：
# 完成日期：
###############################################################################
import exceptions, TradeContext, AfaDBFunc, TradeException, UtilTools,HostContext
import os, ConfigParser, time, Party3Context,AfaLoggerFunc,HostComm,AfaFlowControl,ftplib
from types import *

#======================流程执行异常类==========================
class flowException ( exceptions.Exception ): 

    def __init__( self, errorCode = None , errorMsg = None ):
        if errorCode != None and errorMsg != None :
            TradeContext.errorCode = errorCode
            TradeContext.errorMsg = errorMsg
    def __str__( self ):
        if TradeContext.existVariable("errorCode") and TradeContext.existVariable("errorMsg") and TradeContext.errorCode != None :
            return 'FlowException' + ': ' + TradeContext.errorMsg
        else:
            return 'FlowException'

#======================帐务处理异常类===========================
class accException ( exceptions.Exception ): 

    def __init__( self, errorCode = None , errorMsg = None ):
        if errorCode != None and errorMsg != None :
            TradeContext.errorCode = errorCode
            TradeContext.errorMsg = errorMsg
    def __str__( self ):
        if( TradeContext.existVariable("errorCode") and TradeContext.existVariable("errorMsg") and TradeContext.errorCode != None ):
            return 'AccException' + ': ' + TradeContext.errorMsg
        else:
            return 'AccException'

#==================用于交易异常时退出主执行流程=====================
def exitMainFlow( msgStr='' ):
    if( not TradeContext.existVariable( "errorCode" ) or msgStr ):
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg = '系统错误['+msgStr+']'
            
    if TradeContext.errorCode != '0000' :
        AfaLoggerFunc.tradeFatal( 'errorCode=['+TradeContext.errorCode+']' )
        AfaLoggerFunc.tradeFatal( 'errorMsg=['+TradeContext.errorMsg+']' )
        AfaLoggerFunc.tradeFatal(TradeContext.TransCode+'交易中断')
        
    TradeContext.tradeResponse = [[ 'errorCode', TradeContext.errorCode ], [ 'errorMsg', TradeContext.errorMsg ]]
    
    if (TradeContext.existVariable ( 'agentSerialno')):
        TradeContext.tradeResponse.append( ['agentSerialno',TradeContext.agentSerialno] )
        
    raise TradeException.TradeException( TradeContext.errorMsg )

#=======================交易异常时退出本处理流程===========================
def ExitThisFlow( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg = errorMsg
    if( TradeContext.errorCode.isdigit( )==True and long( TradeContext.errorCode )==0 ):
        return True
    else:
        return False

#=======================查询类变量值的有效性校验==========================
def Query_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '查询类变量值的有效性校验[begin]' )
    if( not TradeContext.existVariable( "trxCode" ) ):
        return ExitThisFlow( 'A0001', '交易代码[trxCode]值不存在!' )
                
    if( not TradeContext.existVariable( "channelCode" ) ):
        return ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
    else:
        TradeContext.channelCode=UtilTools.Lfill( TradeContext.channelCode, 3, '0' )
               
    if( TradeContext.channelCode == '001' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return ExitThisFlow( 'A0001', '机构代码[brno]值不存在!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return ExitThisFlow( 'A0001', '柜员号[teller]值不存在!' )
    
    AfaLoggerFunc.tradeInfo( '查询类变量值的有效性校验[end]' )        
    return True

#=======================缴费类变量值的有效性校验==========================
def Pay_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '缴费类变量值的有效性校验[begin]' )
    
    if ( not TradeContext.existVariable( "termId" ) ):
        return ExitThisFlow( 'A0001', '终端号[termId]值不存在!')
    
    if ( not TradeContext.existVariable( "catrFlag") ):
        return ExitThisFlow( 'A0001', '现金转帐标志[catrFlag]不存在!')    
           
    if( not TradeContext.existVariable( "channelCode" ) ):
        return ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
    else:
        TradeContext.channelCode=UtilTools.Lfill( TradeContext.channelCode, 3, '0' )
    if( TradeContext.channelCode == '001' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return ExitThisFlow( 'A0001', '机构号[brno]值不存在!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return ExitThisFlow( 'A0001', '柜员号[teller]值不存在!' )
    if( not TradeContext.existVariable( "amount" ) ):
        return ExitThisFlow( 'A0001', '金额[amount]值不存在!' )
    if( not TradeContext.existVariable( "userno" ) ):
        return ExitThisFlow( 'A0001', '用户号[userno]值不存在!' )
    if( not TradeContext.existVariable( "accno" ) ):
        TradeContext.accno=''
        #TradeContext.accType='000'
        
    TradeContext.revTranF='0' #正交易
    AfaLoggerFunc.tradeInfo( '缴费类变量值的有效性校验[end]' )
    return True

#=======================取消交易变量值的有效性校验==========================
def Cancel_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '取消交易变量值的有效性校验' )
    if( not TradeContext.existVariable( "zoneno" ) ):
        return ExitThisFlow( 'A0001', '地区号[zoneno]值不存在!' )
        
    if( not TradeContext.existVariable( "channelCode" ) ):
        return ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
    else:
        TradeContext.channelCode=UtilTools.Lfill( TradeContext.channelCode, 3, '0' )
    
    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return ExitThisFlow( 'A0001', '网点号[brno]值不存在!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return ExitThisFlow( 'A0001', '柜员号[teller]值不存在!' )
    if( not TradeContext.existVariable( "amount" ) ):
        return ExitThisFlow( 'A0001', '金额[amount]值不存在!' )
        
    if( not TradeContext.existVariable( "preAgentSerno" ) ):
        return ExitThisFlow( 'A0001', '原交易流水号[preAgentSerno]值不存在!' )
        
            
    TradeContext.revTranF='1'
    return True


#校验反交易数据完整性 根据流水号比对用户号，帐号，交易金额
def ChkRevInfo( serialno ):

    AfaLoggerFunc.tradeInfo( '校验反交易数据完整性[begin]' )
    sqlstr="SELECT REVTRANF,TAXPAYCODE,DRACCNO,CRACCNO,AMOUNT,TELLERNO,\
            TAXPAYNAME,TERMID,VOUHTYPE,VOUHNO,TAXVOUNO,CATRFLAG,\
            BANKSERNO, CORPSERNO,CORPTIME,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,\
            NOTE7,NOTE8,NOTE9,NOTE10,CATRFLAG,WORKDATE FROM TIPS_MAINTRANSDTL WHERE SERIALNO=" +\
            "'"+serialno+"' AND WORKDATE='"+TradeContext.workDate+ "'AND BANKSTATUS IN ('0','2')"  # 

    tmp = AfaDBFunc.SelectSql( sqlstr )
    AfaLoggerFunc.tradeInfo( tmp )
    if tmp == None :
        return ExitThisFlow( 'A0025', AfaDBFunc.sqlErrMsg )
    elif len( tmp ) == 0 :
        AfaLoggerFunc.tradeInfo( sqlstr )
        return ExitThisFlow( 'A0045', '未发现原交易' )

    tmp=UtilTools.ListFilterNone( tmp )

    temp=tmp[0]
    if temp[0]!='0':                 #判断反交易标志
        return ExitThisFlow( 'A0020', '无匹配信息反交易标志有误' )
    if temp[5]!=TradeContext.teller: #比较柜员号
        return ExitThisFlow( 'A0020', '柜员号不匹配' )
    if UtilTools.lrtrim(temp[1])!=TradeContext.taxPayCode:
        return ExitThisFlow( 'A0020', '用户号不匹配' )       
    if UtilTools.lrtrim(temp[4])!=TradeContext.amount:   #校验金额#
        AfaLoggerFunc.tradeInfo( temp[4] )
        return ExitThisFlow( 'A0020', '金额不匹配' )
    
    TradeContext.taxPayCode =temp[1]
    TradeContext.__agentAccno__  =temp[2]
    TradeContext.accno      =temp[3]
    TradeContext.taxPayName =temp[6]
    TradeContext.termId     =temp[7]
    TradeContext.vouhType   =temp[8]
    TradeContext.vouhNo     =temp[9]
    TradeContext.catrFlag   =temp[11]
    TradeContext.corpSerno  =temp[13]
    TradeContext.corpTime   =temp[14]
    TradeContext.taxVouNo   =temp[10]
    #TradeContext.note1=temp[16]
    #TradeContext.note2=temp[17]
    TradeContext.note3=temp[17]
    TradeContext.note4=temp[18]
    #TradeContext.note5=temp[20]
    #TradeContext.note6=temp[21]
    #TradeContext.note7=temp[22]
    #TradeContext.note8=temp[23]
    #TradeContext.note9=temp[24]
    #TradeContext.note10=temp[25]
    AfaLoggerFunc.tradeInfo( '校验反交易数据完整性[end]' )
    return True

#==========================获取平台流水号==========================
def GetSerialno( seqName="TIPS_SEQUENCE" ):

    AfaLoggerFunc.tradeInfo( '获取平台流水号' )
    #if seqName=="TIPS_SEQUENCE" :
    #    if not TradeContext.existVariable( "revTranF" ) or TradeContext.revTranF!='2' :
    #        if (TradeContext.existVariable( "agentSerialno" ) and len(TradeContext.agentSerialno)>0):
    #            return 0
    sqlStr = "select nextval for " +seqName+ " from sysibm.sysdummy1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        TradeContext.errorCode = 'A0025'
        TradeContext.errorMsg = AfaDBFunc.sqlErrMsg
        return -1
    if seqName=="TIPS_SEQUENCE" :
        TradeContext.agentSerialno=str( records[0][0] ).rjust( 8, '0' )
    AfaLoggerFunc.tradeInfo( '>>>平台流水号:' +TradeContext.agentSerialno)
    return str( records[0][0] )


################################################################################
# 函数名:    ChkAbnormal
# 参数:      无
# 返回值：    0  无异常交易    1  有异常交易    -1  查询流水表检测异常失败
# 函数说明：  按柜员查询流水表中的主机异常交易 
################################################################################
def ChkAbnormal( ):

    AfaLoggerFunc.tradeInfo( '查询流水表中的主机异常交易' )
    sql="SELECT COUNT(*) FROM TIPS_MAINTRANSDTL WHERE WORKDATE='"+ \
    TradeContext.workDate+"' AND AGENTCODE='"+TradeContext.agentCode+ \
    "' AND AGENTZONENO='"+TradeContext.zoneno+"' AND BRNO='"+TradeContext.brno+\
    "' AND TELLERNO='"+TradeContext.teller+"' AND REVTRANF='0'AND  \
    (BANKSTATUS='2' OR (BANKSTATUS='0' AND CORPSTATUS IN ('1', '2','3')))"
    result=AfaDBFunc.SelectSql( sql )
    if( result == None ):
        # AfaLoggerFunc.tradeFatal( sql )
        return -1
    if( result[0][0]!=0 ):
        return 1
    else:
        AfaLoggerFunc.tradeError( sql )
        return 0


################################################################################
# 函数名:    InsertDtl
# 参数:      无
# 返回值：    True  插入流水表成功    False 插入流水表失败
# 函数说明：  将流水信息插入流水表
################################################################################
def InsertDtl( ):

    AfaLoggerFunc.tradeInfo( '插入流水表' )
    # count 流水表的列数-1
    count=41
    TransDtl=[[]]*( count+1 )
    TransDtl[0] = TradeContext.agentSerialno    # SERIALNO 代理业务流水号
    TransDtl[1] = TradeContext.workDate         # WORKDATE   交易日期 yyyymmdd
    TransDtl[2] = TradeContext.workTime         # WORKTIME   交易时间   
    TransDtl[3] = TradeContext.TransCode        # TRXCODE    交易码
    TransDtl[4] = TradeContext.zoneno           # ZONENO   代理业务地区号  
    TransDtl[5] = TradeContext.brno             # BRNO       网点号  
    TransDtl[6] = TradeContext.teller           # TELLERNO   柜员号 
    if( TradeContext.existVariable( "authTeller" ) ) :
        TransDtl[7] = TradeContext.authTeller  # AUTHTELLERNO  授权柜员号  
    else:
        TransDtl[7] = ''
    if( TradeContext.existVariable( "termId" ) ):
        TransDtl[8] = TradeContext.termId      # TERMID     终端号
    else:
        TransDtl[8]=''
    
    TransDtl[9] = TradeContext.channelCode     # CHANNELCODE   渠道代码
    
    if( TradeContext.existVariable( "tradeType" ) ):
        TransDtl[10] = TradeContext.tradeType      # TRADETYPE 交易类型
    else:
        TransDtl[10]=''
    
    TransDtl[11] = TradeContext.catrFlag        #CATRFLAG 现转标志
    
    if (TradeContext.existVariable( "accno" )):       #ACCNO 银行帐号
        TransDtl[12] = TradeContext.accno
    else:
        TransDtl[12] = ''
    
    if (TradeContext.existVariable ("__agentAccno__")):     #SUBACCNO 子帐号
        TransDtl[13] = TradeContext.__agentAccno__
    else:
        TransDtl[13] = ''
    
    if( TradeContext.existVariable("vouhType") ): #VOUHTPYE 凭证类型
        TransDtl[14] = TradeContext.vouhType
    else:
        TransDtl[14]=''
        
    if( TradeContext.existVariable("vouhNo")):   #VOUHNO 凭证号码
        TransDtl[15] = TradeContext.vouhNo
    else:
        TransDtl[15] = ''    

    if( TradeContext.existVariable("taxVouNo")):   #税票号码
        TransDtl[16] = TradeContext.taxVouNo
    else:
        TransDtl[16] = ''    
    
    if ( TradeContext.existVariable( "taxPayCode" ) ):
        TransDtl[17] = TradeContext.taxPayCode      #纳税人编码
    else:
        TransDtl[17] = ''
      
    
    if( TradeContext.existVariable( "taxPayName" ) ):
        TransDtl[18] = TradeContext.taxPayName    # TAXPAYNAME   纳税人名称  
    else:
        TransDtl[18] = '' 
    
    TransDtl[19] = UtilTools.lrtrim(TradeContext.amount)         # AMOUNT       交易金额 
    
    TransDtl[20] = TradeContext.revTranF       # REVTRANF    反交易标志 
                                               # 0:正交易、1:反交易、2.自动冲正 
    if( int( TradeContext.revTranF ) != 0 ):
        TransDtl[21] = TradeContext.preAgentSerno  #PREAGENTSERNO    原平台流水号  
    else:
        TransDtl[21] = ''    
    
    TransDtl[22] = '2'                   # BANKSTATUS     银行交易状态 
    TransDtl[23] = ''                    # BANKCODE       银行.交易返回码
    TransDtl[24] = ''                    # BANKSERNO      银行.交易流水号
    
    TransDtl[25] = '2'                   # CORPSTATUS     第三方交易状态
    TransDtl[26] = ''                    # CORPCODE       第三方.交易返回码  

    #关彬捷  20091218  修改 登记主流水表时登记第三方日期和流水
    if ( TradeContext.existVariable( "corpSerno" )):
        TransDtl[27] = TradeContext.corpSerno    # CORPSERNO      第三方.交易流水号
    else:
        TransDtl[27] = ''               

    if ( TradeContext.existVariable( "corpTime" ) ):
        TransDtl[28] = TradeContext.corpTime     # CORPTIME       第三方.交易日期时间戳
    else:
        TransDtl[28] = ''           
    #关彬捷  20091218  修改结束
    
    TransDtl[29] = ''                    # ERRORMSG       交易返回信息
    TransDtl[30] = '9'                   # CHKFLAG        主机对帐标志 
    TransDtl[31] = '9'                   # CORPCHKFLAG    人行对帐标志 
            
    if( TradeContext.existVariable( "note1" ) ):
        TransDtl[32] = TradeContext.note1
    else:
        TransDtl[32] = ''
        
    if( TradeContext.existVariable( "note2" ) ):
        TransDtl[33] = TradeContext.note2         # NOTE2          备注2
    else:
        TransDtl[33] = ''
        
    if( TradeContext.existVariable( "note3" ) ):
        TransDtl[34] = TradeContext.note3         # NOTE3          备注3
    else:
        TransDtl[34] = ''
        
    if( TradeContext.existVariable( "note4" ) ):
        TransDtl[35] = TradeContext.note4         # NOTE4          备注4
    else:
        TransDtl[35] = ''
        
    if( TradeContext.existVariable( "note5" ) ):
        TransDtl[36] = TradeContext.note5         # NOTE5          备注5
    else:
        TransDtl[36] = ''
        
    if( TradeContext.existVariable( "note6" ) ):
        TransDtl[37] = TradeContext.note6         # NOTE6          备注6
    else:
        TransDtl[37] = ''
        
    if( TradeContext.existVariable( "note7" ) ):
        TransDtl[38] = TradeContext.note7         # NOTE7          备注7
    else:
        TransDtl[38] = ''
        
    if( TradeContext.existVariable( "note8" ) ):
        TransDtl[39] = TradeContext.note8         # NOTE8          备注8
    else:
        TransDtl[39] = ''
        
    if( TradeContext.existVariable( "note9" ) ):
        TransDtl[40] = TradeContext.note9         # NOTE9          备注9
    else:
        TransDtl[40] = ''
        
    if( TradeContext.existVariable( "note10" ) ):
        TransDtl[41] = TradeContext.note10        # NOTE10          备注10
    else:
        TransDtl[41] = ''
    sql="INSERT INTO TIPS_MAINTRANSDTL(SERIALNO,WORKDATE, \
         WORKTIME,TRXCODE,ZONENO,BRNO,TELLERNO, \
         AUTHTELLERNO,TERMID,CHANNELCODE,TRADETYPE,CATRFLAG,DRACCNO,CRACCNO,VOUHTYPE,VOUHNO, \
         TAXVOUNO,TAXPAYCODE,TAXPAYNAME,AMOUNT,REVTRANF,PRESERNO, \
         BANKSTATUS,BANKCODE,BANKSERNO, \
         CORPSTATUS,CORPCODE,CORPSERNO,CORPTIME,ERRORMSG,CHKFLAG, CORPCHKFLAG, \
         NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9,NOTE10 \
         ) VALUES("
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
        #TradeContext.errorCode, TradeContext.errorMsg='0000', 'TransOk'
        AfaLoggerFunc.tradeInfo( '插入流水表完成' )
        #插入项目明细

        if TradeContext.revTranF =='0':
            if not InsertVouMX() :
                return False
            else:
                return True
        else:
            return True
################################################################################
# 函数名:    InsertVouMX 
# 参数:      无
# 返回值：    True  插入表成功    False 插入表失败
# 函数说明：  将税种明细插入税票明细表
################################################################################
def InsertVouMX( ):

    AfaLoggerFunc.tradeInfo( '插入税票明细表' )
    for index in range(0,int(TradeContext.taxTypeNum)):
        sql="INSERT INTO TIPS_VOU_TAXTYPE(SERIALNO,WORKDATE, \
             TAXVOUNO,PROJECTID,BUDGETSUBJECTCODE,LIMITDATE,TAXTYPENAME, \
             BUDGETLEVELCODE,BUDGETLEVELNAME,TAXSTARTDATE,TAXENDDATE,VICESIGN,TAXTYPE, \
             TAXTYPEAMT,DETAILNUM,TAXSUBJECTLIST,NOTE1 \
             ) VALUES("
        sql=sql+"'"+ TradeContext.agentSerialno +"',"
        sql=sql+"'"+ TradeContext.workDate      +"',"
        sql=sql+"'"+ TradeContext.taxVouNo                   +"',"
        if type(TradeContext.projectId) is list:
            sql=sql+"'"+ TradeContext.projectId[index]           +"'"               #项目序号
        else:
            sql=sql+"'"+ TradeContext.projectId           +"'"               #项目序号
            
        if( TradeContext.existVariable( "budgetSubjectCode" ) ):
            if type(TradeContext.budgetSubjectCode) is list:
                sql=sql+",'"+ TradeContext.budgetSubjectCode[index] +"'"        #预算科目代码 
            else:
                sql=sql+",'"+ TradeContext.budgetSubjectCode +"'"        #预算科目代码 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "limitDate" ) ):
            if type(TradeContext.limitDate) is list:
                sql=sql+",'"+ TradeContext.limitDate[index] +"'"        # 限缴日期
            else:
                sql=sql+",'"+ TradeContext.limitDate +"'"        # 限缴日期
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxTypeName" ) ):
            if type(TradeContext.taxTypeName) is list:
                sql=sql+",'"+ TradeContext.taxTypeName[index] +"'"        # 税种名称
            else:
                sql=sql+",'"+ TradeContext.taxTypeName +"'"        # 税种名称
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "budgetLevelCode" ) ):
            if type(TradeContext.budgetLevelCode) is list:
                sql=sql+",'"+ TradeContext.budgetLevelCode[index] +"'"        #预算级次代码 
            else:
                sql=sql+",'"+ TradeContext.budgetLevelCode +"'"        #预算级次代码 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "budgetLevelName" ) ):
            if type(TradeContext.budgetLevelName) is list:
                sql=sql+",'"+ TradeContext.budgetLevelName[index] +"'"        #预算级次名称 
            else:
                sql=sql+",'"+ TradeContext.budgetLevelName +"'"        #预算级次名称 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxStartDate" ) ):
            if type(TradeContext.taxStartDate) is list:
                sql=sql+",'"+ TradeContext.taxStartDate[index] +"'"        #税款所属日期起 
            else:
                sql=sql+",'"+ TradeContext.taxStartDate +"'"        #税款所属日期起 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxEndDate" ) ):
            if type(TradeContext.taxEndDate) is list:
                sql=sql+",'"+ TradeContext.taxEndDate[index] +"'"        #税款所属日期止 
            else:
                sql=sql+",'"+ TradeContext.taxEndDate +"'"        #税款所属日期止 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "viceSign" ) ):
            if type(TradeContext.viceSign) is list:
                sql=sql+",'"+ TradeContext.viceSign[index] +"'"        #辅助标志 
            else:
                sql=sql+",'"+ TradeContext.viceSign +"'"        #辅助标志 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxType" ) ):
            if type(TradeContext.taxType) is list:
                sql=sql+",'"+ TradeContext.taxType[index] +"'"        #税款类型 
            else:
                sql=sql+",'"+ TradeContext.taxType + "'"        #税款类型 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxTypeAmt" ) ):
            if type(TradeContext.taxTypeAmt) is list:
                sql=sql+",'"+ TradeContext.taxTypeAmt[index] +"'"        #税种金额 
            else:
                sql=sql+",'"+ TradeContext.taxTypeAmt +"'"        #税种金额 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "detailNum" ) ):
            if type(TradeContext.detailNum) is list:
                sql=sql+",'"+ TradeContext.detailNum[index] +"'"        #明细条数 
            else:
                sql=sql+",'"+ TradeContext.detailNum +"'"        #明细条数 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxSubjectList" ) ):
            if type(TradeContext.taxSubjectList) is list:
                sql=sql+",'"+ TradeContext.taxSubjectList[index] +"'"        #税目明细 
            else:
                sql=sql+",'"+ TradeContext.taxSubjectList +"'"        #税目明细 
        else:
            sql=sql+",''"
        sql=sql+",'0')"
        
        AfaLoggerFunc.tradeInfo( sql )
        result=AfaDBFunc.InsertSqlCmt( sql )
        
        if( result < 1 ):
            # AfaLoggerFunc.tradeFatal( sql )
            TradeContext.errorCode, TradeContext.errorMsg='A0044', '插入税票明细表失败'+AfaDBFunc.sqlErrMsg
            return False
    AfaLoggerFunc.tradeInfo( '插入税票明细表完成' )
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
    sql="UPDATE TIPS_MAINTRANSDTL SET "
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
    # print "UpdatePreDtl:"+sql 
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
    sql="UPDATE TIPS_MAINTRANSDTL SET "
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
   
    AfaLoggerFunc.tradeInfo( sql )
    if( int( TradeContext.revTranF )!=0 and TradeContext.errorCode == '0000'):
        if( not UpdatePreDtl( action ) ):
            return False
            
    if( AfaDBFunc.UpdateSqlCmt( sql )<1 ):
        # AfaLoggerFunc.tradeFatal( sql )
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '更新流水主表失败'+AfaDBFunc.sqlErrMsg
        return False
        
    AfaLoggerFunc.tradeInfo( TradeContext.errorCode + "BBBBBB" ) 
    #if( TradeContext.errorCode != '0000' ):
    #    return  False
        
    AfaLoggerFunc.tradeInfo( '更新本交易流水[end]['+ action + ']' )
    return True

#======================自动打包============================
def autoPackData( ):

    AfaLoggerFunc.tradeInfo( '自动打包' )
    if( not TradeContext.existVariable( "tradeResponse" ) or not TradeContext.tradeResponse ):
        TradeContext.tradeResponse=[]
        #=============平台内部报文====================
        names = TradeContext.getNames( )
        for name in names:
            if ( not name.startswith( '__' ) and name != 'tradeResponse' ) :
                value = getattr( TradeContext, name )
                if( type( value ) is StringType ) :
                    TradeContext.tradeResponse.append( [name, value] )
                elif( type( value ) is ListType ) :
                    for elem in value:
                        if type(elem) is not str :
                            AfaLoggerFunc.tradeInfo( 'autoPackData  [value is not sting]')
                            continue
                        TradeContext.tradeResponse.append( [name, elem] )
        #=============第三方返回报文====================
        names = Party3Context.getNames( )
        for name in names:
            if ( name.startswith( 'dn_' ) ) :
                value = getattr( Party3Context, name )
                if( type( value ) is StringType ) :
                    TradeContext.tradeResponse.append( [name, value] )
                elif( type( value ) is ListType ) :
                    for elem in value:
                        TradeContext.tradeResponse.append( [name, elem] )
    return True

#=================初始化主机通讯接口=======================
def InitHostReq(hostType ):
    #初始化函数返回值变量
    AfaLoggerFunc.tradeInfo('初始化map文件信息[InitHostReq]')

    if (hostType =='0'): # 正交易

        AfaLoggerFunc.tradeInfo('>>>正交易8813')

        HostContext.I1TRCD = '8813'
       
        HostContext.I1SBNO = TradeContext.brno
       
        HostContext.I1USID = TradeContext.teller
       
        if TradeContext.existVariable ( 'authTeller'):
            HostContext.I1AUUS = TradeContext.authTeller
            HostContext.I1AUPS = TradeContext.authPwd
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        HostContext.I1WSNO = TradeContext.termId

        HostContext.I2NBBH = []         #代理业务号
        HostContext.I2NBBH.append(TradeContext.appNo)

        HostContext.I2FEDT = []         #前置日期
        HostContext.I2FEDT.append(TradeContext.workDate)

        HostContext.I2RBSQ = []         #前置流水号
        HostContext.I2RBSQ.append(TradeContext.agentSerialno)

        HostContext.I2DATE = []         #外系统帐务日期
        HostContext.I2DATE.append(TradeContext.workDate)

        HostContext.I2RVFG = []         #蓝红字标志
        HostContext.I2RVFG.append('')

        HostContext.I2SBNO = []         #交易机构
        HostContext.I2SBNO.append(TradeContext.brno)

        HostContext.I2TELR = []         #交易柜员
        HostContext.I2TELR.append(TradeContext.teller)

        HostContext.I2TRSQ = []         #组号
        HostContext.I2TRSQ.append('000')
        
        HostContext.I2TINO = []         #组内序号
        HostContext.I2TINO.append('00')

        HostContext.I2OPTY = []         #证件校验标志
        HostContext.I2OPTY.append('0')

        HostContext.I2RBAC = []         #贷方账号
        HostContext.I2RBAC.append(TradeContext.__agentAccno__)

        HostContext.I2CYNO = []         #币种
        HostContext.I2CYNO.append('01')

        HostContext.I2WLBZ = []         #往来帐标志
        HostContext.I2WLBZ.append('0')

        HostContext.I2TRAM = []         #发生额
        HostContext.I2TRAM.append(TradeContext.amount)

        HostContext.I2SMCD = []         #摘要代码
        HostContext.I2SMCD.append(TradeContext.summary_code)

        HostContext.I2NMFG = []         #户名校验标志
        HostContext.I2NMFG.append('0')

        HostContext.I2APX1 = []         #附加信息1
        HostContext.I2APX1.append('')

        #判断现金转帐标志,以便填充不同的数据通讯区
        if (TradeContext.catrFlag == '0'):    #现金

            AfaLoggerFunc.tradeInfo('>>>现金')

            HostContext.I2CFFG = []           #密码校验标志
            HostContext.I2CFFG.append('N')

            #HostContext.I2TRFG = []           #凭证处理标志
            #HostContext.I2TRFG.append('')

            HostContext.I2CATR = []           #现转标志
            HostContext.I2CATR.append(TradeContext.catrFlag)

        else:   #转帐
            AfaLoggerFunc.tradeInfo('>>>转帐')

            HostContext.I2SBAC = []
            HostContext.I2SBAC.append(TradeContext.accno)         #借方帐号

            if (TradeContext.existVariable('accPwd')):
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('Y')                    #密码校验方式
                HostContext.I2PSWD = []
                HostContext.I2PSWD.append(TradeContext.accPwd)

            else:
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('N')                    #密码校验方式

            if (TradeContext.existVariable('vouhType' ) ):
                HostContext.I2CETY = []
                HostContext.I2CETY.append(TradeContext.vouhType)

                HostContext.I2CCSQ = []
                HostContext.I2CCSQ.append(TradeContext.vouhNo)
                
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('N')                          #密码校验方式：支票不校验密码

            HostContext.I2CATR = []                               #现转标志
            HostContext.I2CATR.append(TradeContext.catrFlag)
                    
    else:   #反交易

        AfaLoggerFunc.tradeInfo('>>>反交易8820')

        HostContext.I1TRCD = '8820'
        
        HostContext.I1SBNO = TradeContext.brno
        
        HostContext.I1USID = TradeContext.teller
        
        if TradeContext.existVariable ( 'authTeller'):
            HostContext.I1AUUS = TradeContext.authTeller
            HostContext.I1AUPS = TradeContext.authPwd
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        HostContext.I1WSNO = TradeContext.termId
        HostContext.I1NBBH = TradeContext.appNo
        HostContext.I1FEDT = TradeContext.workDate
        HostContext.I1DATE = TradeContext.workDate
        HostContext.I1RBSQ = TradeContext.agentSerialno
        HostContext.I1TRDT = TradeContext.workDate
        HostContext.I1UNSQ = TradeContext.preAgentSerno
        HostContext.I1OPTY = ''
        HostContext.I1OPFG = '0'                                        #(0.当日,1.隔日)
        HostContext.I1RVSB = '0'                                        #(0不回补-NO, 1	回补-YES)

    AfaLoggerFunc.tradeInfo('初始化map文件信息[InitHostReq]完成')

    return True


#====================与主机数据交换=============================
def CommHost( result = None ):

    # 根据正反交易标志TradeContext.revTranF判断具体选择哪个map文件和主机接口方式
    if not result:
        result=TradeContext.revTranF
        #===================初始化=======================
        if not InitHostReq(result) :
            TradeContext.__status__='1'
            return False
            

    if (result == '0'):
        #单笔记帐交易
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8813.map'
        TradeContext.HostCode = '8813'

    else:
        #单笔抹帐
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8820.map'
        TradeContext.HostCode = '8820'

    AfaLoggerFunc.tradeInfo('执行与主机通讯函数[CommHost]')

    #print mapfile
    #此处交易代码要求10位,右补空格
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )

    if HostContext.host_Error:
        AfaLoggerFunc.tradeFatal( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )

        if HostContext.host_ErrorType != 5 :
            TradeContext.__status__='1'
            TradeContext.errorCode='A0101'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        else :
            TradeContext.__status__='2'
            TradeContext.errorCode='A0102'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        return False

    #================分析主机返回包====================
    return HostParseRet(result )


#================分析主机返回包====================
def HostParseRet( hostType ):

    if (HostContext.host_Error == True):    #主机通讯错误
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '主机通讯错误'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #通讯错误代码
        return False

    if( HostContext.O1MGID == 'AAAAAAA' ): #成功
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '主机成功'
        TradeContext.bankSerno = HostContext.O1TLSQ                               #柜员流水号
        TradeContext.bankCode  = HostContext.O1MGID                               #主机返回代码
        return True

    else:                                  #失败
        TradeContext.__status__='1'
        #result = AfapFunc.RespCodeMsg(HostContext.O1MGID,'0000','100000')
        #if not result :
        #    TradeContext.errorCode, TradeContext.errorMsg = 'A9999', '系统错误[主机未知错误]['+HostContext.ERR+']'
        #else:
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False


#============修改应用运行状态==========
def UpdAppStatus(flag):
    AfaLoggerFunc.tradeInfo('修改单位运行状态' )
    sql="UPDATE TIPS_ADM SET STATUS='"+flag+"' "
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，单位信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    return True
    
#============查询应用运行状态==========
def SelAppStatus():
    AfaLoggerFunc.tradeInfo('查询单位运行状态' )
    sql="SELECT STATUS FROM TIPS_ADM"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.SelectSql( sql )
    if( records <1 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，单位信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    else:
        TradeContext.flag = records[0][0]
        return True

#============修改应用工作日期==========
def UpdAppWorkDate(workDate):
    AfaLoggerFunc.tradeInfo('修改单位工作日期' )
    sql="UPDATE TIPS_ADM SET WORKDATE='"+workDate+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '数据库错误，单位信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    return True

#====判断应用状态==========    
def ChkAppStatus():
    AfaLoggerFunc.tradeInfo( '>>>判断应用状态' )
    sql="SELECT STATUS,WORKDATE,NOTE1 "
    sql=sql+" FROM TIPS_ADM "
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '未定义应用信息' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_ADM表配置错误' )
    else:
        if records[0][0]=='0':
            return ExitThisFlow( 'A0027', '业务已停止' )
        if records[0][0]=='2':
            return ExitThisFlow( 'A0027', '业务已暂停' )
        TradeContext.workDate       = records[0][1]
    AfaLoggerFunc.tradeInfo( '>>>判断应用状态完成' )
    return True
#====获取清算信息==========    
def ChkLiquidStatus():
    AfaLoggerFunc.tradeInfo( '>>>获取清算信息' )
    sql="SELECT PAYEEBANKNO,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,BRNO,TELLERNO,STATUS,LIQUIDATEMODE,NOTE1 "
    sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE PAYEEBANKNO='"+ TradeContext.payeeBankNo+"'"
    sql=sql+"AND PAYBKCODE='"+ TradeContext.payBkCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '未定义清算信息' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_LIQUIDINFO表配置错误' )
    else:
        if records[0][6]=='0':
            return ExitThisFlow( 'A0027', '业务已停止' )
        if records[0][6]=='2':
            return ExitThisFlow( 'A0027', '业务已暂停' )
        TradeContext.payeeBankNo    = records[0][0]
        TradeContext.payeeAcct      = records[0][1]
        TradeContext.payeeName      = records[0][2]
        TradeContext.payBkCode      = records[0][3]
        TradeContext.__mainBrno__   = records[0][4]
        TradeContext.__vmTellerno__ = records[0][5]
        TradeContext.__liquidMode__ = records[0][7]
        #TradeContext.__batchType__  = records[0][12]
        #TradeContext.__protocalFlag__ = records[0][13]
        #TradeContext.workDate       = records[0][11]
        if not( TradeContext.existVariable( "brno" ) and len(TradeContext.brno)>0):
            TradeContext.brno   =records[0][4]
            TradeContext.zoneno =records[0][4][0:4]
        if not( TradeContext.existVariable( "teller" ) and len(TradeContext.teller)>0):
            TradeContext.teller =records[0][5]
    AfaLoggerFunc.tradeInfo( '>>>获取清算信息完成' )
    return True
#====判断机构状态==========    
def ChkBranchStatus():
    AfaLoggerFunc.tradeInfo( '>>>判断机构状态' )
    sql="SELECT STATUS,PAYBKCODE,PAYEEBANKNO,ACCNO,NOTE1,NOTE2 "
    sql=sql+" FROM TIPS_BRANCH_ADM WHERE "
    sql=sql+" BRNO ='" + TradeContext.brno +"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '该机构未开通此项业务' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_BRANCH_ADM表配置错误' )
    else:
        if records[0][0]=='0':
            return ExitThisFlow( 'A0027', '该机构此项业务已停止' )
        if records[0][0]=='2':
            return ExitThisFlow( 'A0027', '该机构此项业务已暂停' )
        if not( TradeContext.existVariable( "payeeBankNo" ) and len(TradeContext.payeeBankNo)>0):
            TradeContext.payeeBankNo       = records[0][2]
        if not( TradeContext.existVariable( "payBkCode" ) and len(TradeContext.payBkCode)>0):
            TradeContext.payBkCode       = records[0][1]
        TradeContext.__agentAccno__  = records[0][3]
        AfaLoggerFunc.tradeInfo('机构状态正常,清算行号：'+TradeContext.payBkCode +' 待清算帐号：'+TradeContext.__agentAccno__)
        AfaLoggerFunc.tradeInfo('收款行号：'+TradeContext.payeeBankNo)
    return True
#====检查征收机关代码==========    
#TaxOrgCode	征收机关代码
#TaxOrgName	征收机关名称
def ChkTaxOrgCode():
    AfaLoggerFunc.tradeInfo( '>>>检查征收机关代码' )
    sql="SELECT TAXORGCODE,TAXORGNAME,ZONENO,BRNO,BANKNO,TELLERNO,ACCNO,ACCNAME,STATUS,WORKDATE "
    sql=sql+" FROM TIPS_APPINFO WHERE "
    sql=sql+" TAXORGCODE='"+ TradeContext.taxOrgCode+"'"
    if( TradeContext.existVariable( "brno" ) and len(TradeContext.brno)>0):
        sql=sql+" AND ZONENO='"+ TradeContext.brno[0:2]+"'"
    if( TradeContext.existVariable( "PayBkCode" ) and len(TradeContext.PayBkCode)>0):
        sql=sql+" AND BANKNO='"+ TradeContext.PayBkCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '本地区尚未开启该征收机关业务' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_APPINFO表业务配置错误' )
    else:
        if records[0][8]=='0':
            return ExitThisFlow( 'A0027', '该征收机关业务已停止' )
        TradeContext.taxOrgName =records[0][1]
        TradeContext.PayBkCode =records[0][4]
        TradeContext.__agentAccno__ =records[0][6]
        #TradeContext.workDate =records[0][9]
        if not( TradeContext.existVariable( "brno" ) and len(TradeContext.brno)>0):
            TradeContext.brno=records[0][3]
            TradeContext.zoneno=records[0][2]
        TradeContext.teller =records[0][5]
        
    return True
    
#======检查客户是否签约===============
def ChkCustSign():
    AfaLoggerFunc.tradeInfo( '>>>检查客户是否签约' )
    if( not TradeContext.existVariable( "accno" ) ):
        return ExitThisFlow( 'A0001', '[accno]值不存在!' )
    if( not TradeContext.existVariable( "protocolNo" ) ):
        return ExitThisFlow( 'A0001', '协议书号[protocolNo]值不存在!' )
    
    sql="SELECT TAXPAYCODE,PAYOPBKCODE"
    sql=sql+" FROM TIPS_CUSTINFO WHERE "
    sql=sql+" PAYACCT='"        +TradeContext.accno         +"'"
    sql=sql+" and PROTOCOLNO='" +TradeContext.protocolNo         +"'"
    sql=sql+" and TAXORGCODE='" +TradeContext.taxOrgCode    +"'"
    sql=sql+" AND STATUS='"     +'1'                        +"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( '24009', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( '24009', '该客户尚未签约' )
    else:
        TradeContext.userno     =records[0][0]
        TradeContext.taxPayCode =records[0][0]
        TradeContext.brno       =records[0][1]
        AfaLoggerFunc.tradeInfo('该客户已签约,编号：'+TradeContext.taxPayCode +' 开户机构：'+TradeContext.brno)
    return True

#====检查节点状态========== 
#当节点状态为故障时，停止对其发起交易   
def ChkNode(nodeCode):
    AfaLoggerFunc.tradeInfo( '>>>检查节点状态' )
    sql="SELECT STATUS,RUNSTATUS "
    sql=sql+" FROM TIPS_NODECODE WHERE "
    sql=sql+" NODECODE='"+ nodeCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '不存在该节点:'+'节点代码['+nodeCode+']' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_NodeCode表错误：多个节点信息' )
    else:
        if records[0][0]=='1':
            return ExitThisFlow( 'A0027', '节点已注销:'+'节点代码['+nodeCode+']'  )
        if records[0][1]=='1':
            return ExitThisFlow( 'A0027', '节点故障，暂停发送业务:'+'节点代码['+nodeCode+']'  )
    return True    
#====检查征收机关==========    
#TaxOrgCode	征收机关代码
#TaxOrgName	征收机关名称
def ChkTaxOrg(taxOrgCode):
    AfaLoggerFunc.tradeInfo( '>>>检查征收机关' )
    sql="SELECT TAXORGNAME,STATUS "
    sql=sql+" FROM TIPS_TAXCODE WHERE "
    sql=sql+" TAXORGCODE='"+ taxOrgCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '没有该征收机关信息:'+'代码['+taxOrgCode+']')
    #elif( len( records )>1 ):
    #    return ExitThisFlow( 'A0027', 'TIPS_APPINFO表业务配置错误' )
    else:
        if records[0][1]=='1':
            return ExitThisFlow( 'A0027', '该征收机关已注销:'+'代码['+taxOrgCode+']' )
        TradeContext.taxOrgName =records[0][0]
    return True    
#====检查国库==========    
def ChkTre(treCode,payBankno):
    AfaLoggerFunc.tradeInfo( '>>>检查国库信息' )
    sql="SELECT STATUS,TRENAME,PAYBANKNO,OFNODECODE "
    sql=sql+" FROM TIPS_TRECODE WHERE 1=1 "
    if len(treCode)>0:
        sql=sql+"AND  TRECODE='"+ treCode+"'"
    if len(payBankno)>0:
        sql=sql+"AND PAYBANKNO='"+ payBankno+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '没有该国库信息:'+'国库代码['+treCode+']行号['+payBankno+']' )
    #elif( len( records )>1 ):
    #    return ExitThisFlow( 'A0027', 'TIPS_APPINFO表业务配置错误' )
    else:
        if records[0][0]=='1':
            return ExitThisFlow( 'A0027', '该国库已注销:'+'国库代码['+treCode+']行号['+payBankno+']' )
        TradeContext.treName =records[0][1]
        TradeContext.treNodeCode =records[0][3]
    return True    
#======根据付款行号获取机构号===============
def GetBrno(pPayBkCode):
    AfaLoggerFunc.tradeInfo( '>>>根据付款行号获取机构号' )
    sql="SELECT BRANCHNO "
    sql=sql+" FROM AFA_BRANCH WHERE BRANCHCODE='"+ pPayBkCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '未定义该付款行号' )
    else:
        #AfaLoggerFunc.tradeInfo('')
        TradeContext.brno=records[0][0]
        #TradeContext.zoneno=TradeContext.brno[0:3]
        #TradeContext.subUnitno=TradeContext.zoneno
        AfaLoggerFunc.tradeInfo('机构号:'+TradeContext.brno)
    return True
   
################################################################################
# 函数名:    GetBranchInfo
# 参数:      branchno
# 返回值：    False  失败;    成功返回list
# 函数说明：  获取行所信息
################################################################################
def GetBranchInfo(branchno=''):
    sqlStr="select upbranchno,branchcode,type,branchnames,branchname,note1,note2 from AFA_BRANCH where branchno='" + branchno + "'"
    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return ExitThisFlow( 'A0002', '查询机构号失败:'+AfaDBFunc.sqlErrMsg )
    elif ( len( records )==0):
        return ExitThisFlow( 'A0002', '无法找到相应的机构号' )
    elif ( len( records )>1):
        return ExitThisFlow( 'A0002', '查到多条机构号' )
    else:
        UtilTools.ListFilterNone( records )
        TradeContext.__mngZoneno__=records[0][0]    #上级管理机构
        TradeContext.__PayBkCode__=records[0][1]    #支付系统行号
        TradeContext.__branchType__=records[0][2]   #机构类型
        TradeContext.__branchNames__=records[0][3]
        TradeContext.__branchName__=records[0][4]
        TradeContext.__mngHsno__=records[0][5]    #上级核算机构
        TradeContext.__QsBkCode__=records[0][6]     #清算行号
        AfaLoggerFunc.tradeInfo('上级管理机构号:['+TradeContext.__mngZoneno__+']')
    return ExitThisFlow( '0000', 'TransOk' )

def GetPayBkCode():
#=============查询网点对应的支付行号，清算行号====================
    sql="SELECT NOTE1,NOTE2,UPBRANCHNO,BRANCHCODE FROM AFA_BRANCH WHERE BRANCHNO='"+TradeContext.brno+"'"
    records = AfaDBFunc.SelectSql(sql)
    AfaLoggerFunc.tradeInfo(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '未定义该机构信息')
    else:
        UtilTools.ListFilterNone( records )
        TradeContext.HSBrno     =records[0][0]  #上级核算机构
        TradeContext.QsBkCode   =records[0][1]  #清算行号
        TradeContext.PayBkCode  =records[0][3]  #支付系统行号
        TradeContext.upBranchno =records[0][2]  #上级管理机构号
        
    #=============查询清算行号对应的机构号====================
    sql="SELECT BRANCHNO,BRANCHNAMES,BRANCHNAME FROM AFA_BRANCH WHERE BRANCHCODE='"+TradeContext.QsBkCode+"'"
    records = AfaDBFunc.SelectSql(sql)
    AfaLoggerFunc.tradeInfo(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '未定义该机构信息')
    else:
        UtilTools.ListFilterNone( records )
        TradeContext.QsBrno     =records[0][0]  #清算机构号
        TradeContext.QsBrNames  =records[0][1]  #
        TradeContext.QsBrName   =records[0][2]  #
        #TradeContext.GkBkCode   =records[0][3]  #国库支付行号    
    return True
################################################################################
# 函数名:    RespCodeMsg
# 参数:      outcode:外部响应码,unitno:
# 返回值：    0  失败    1  成功
# 函数说明：  根据外部响应码获取外部响应信息
################################################################################
def GetRespMsg( outcode,sysid ):
    AfaLoggerFunc.tradeInfo( '转帐外部响应码' )
    AfaLoggerFunc.tradeInfo( '转换前,外部返回码:['+outcode+']['+TradeContext.errorMsg+']' )
    TradeContext.respmsg=''
    sqlStr="select * from AFA_RESPCODE where sysid='"+sysid+\
        "' and orespcode='"+outcode+"'"
    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return ExitThisFlow( 'A0002', '响应码信息表操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )!=0 ):
        UtilTools.ListFilterNone( records )
        #TradeContext.tradeResponse=(['errorCode',records[0][1]],['errorMsg',records[0][3]])
        TradeContext.irespcode=records[0][1]
        TradeContext.respmsg=records[0][3]
        AfaLoggerFunc.tradeInfo( '返回码:['+outcode+']['+TradeContext.irespcode+']['+TradeContext.respmsg+']' )
    else:
        AfaLoggerFunc.tradeInfo( '未找到响应码信息，返回码:['+TradeContext.errorCode+'][未知错误]' )
        return False
        #TradeContext.irespcode=outcode
        #if(len(TradeContext.respmsg)==0):
        #    TradeContext.respmsg = '未知错误'
    return True
#======根据征收机关代码或者征收机关信息===============
def GetTaxOrg(pTaxOrgCode):
    AfaLoggerFunc.tradeInfo( '根据征收机关代码或者征收机关信息' )
    sql="SELECT TAXORGNAME "
    sql=sql+" FROM TIPS_TAXCODE WHERE TAXORGCODE='"+ pTaxOrgCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        TradeContext.taxOrgName=pTaxOrgCode
        #return ExitThisFlow( 'A0027', '未定义该付款行号' )
    else:
        TradeContext.taxOrgName=records[0][0]
    return True


#生成批量委托号
def CrtBatchNo():
    AfaLoggerFunc.tradeInfo('>>>生成委托号')
    try:
        sqlStr = "SELECT NEXTVAL FOR DSDF_BATCH_SEQ FROM SYSIBM.SYSDUMMY1"
        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            return ExitThisFlow('9000', '生成委托号失败')
        TradeContext.BATCHNO = TradeContext.workDate + str(records[0][0]).rjust(8, '0')
        AfaLoggerFunc.tradeInfo('委托号'+TradeContext.BATCHNO)
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return ExitThisFlow('9000', '生成委托号失败')
    return True


#=========================格式化文件=========================
def FormatFile(ProcType, sFileName, dFileName ,fFileFld):

    try:
        srcFileName    = sFileName
        dstFileName    = dFileName
        
        if (ProcType == "1"):
            #ascii->ebcd    编码
            #调用格式:cvt2ebcdic -T 源文本文件 -P 目标物理文件 -F fld格式文件 [-D 间隔符 ]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ebcdic'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/' + fFileFld
            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName + " -D '<fld>'"
        else:
            #   解码
            #调用格式:cvt2ascii -T 生成文本文件 -P 物理文件 -F fld文件 [-D 间隔符] [-S] [-R]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/' + fFileFld
            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName + " -D '<fld>'"

        AfaLoggerFunc.tradeInfo('>>>' + cmdstr)

        ret = os.system(cmdstr)
        if ( ret != 0 ):
            return False
        else:

            #判断文件是否存在
            if ( os.path.exists(dstFileName) and os.path.isfile(dstFileName) ):
                return True
            else:
                WrtLog('>>>格式化文件失败')
                return False

    except Exception, e:
        WrtLog(e)
        WrtLog('格式化文件异常')
        return False

##################################################################
#   财税库行系统.FTP操作模块
#=================================================================
#   函    数:   getHost(),putHost
#   作    者:   李亚杰
#   修改时间:   2008-06-11
##################################################################

def getHost(file_path,host_home):
    #try:
    #    local_home = os.environ['AFAP_HOME'] + "/data/batch/tips/"
    #    
    #    config = ConfigParser.ConfigParser( )
    #    configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
    #    config.readfp( open( configFileName ) )
    #    
    #    ftp_p=ftplib.FTP(config.get('HOST_DZ','HOSTIP'),config.get('HOST_DZ','USERNO'),config.get('HOST_DZ','PASSWD' ))
    #    ftp_p.cwd(host_home)
    #    file_handler = open(local_home + file_path,'wb')
    #    ftp_p.retrbinary("RETR " + file_path,file_handler.write)
    #    file_handler.close()
    #    ftp_p.quit()
    #    
    #    if not os.path.exists(local_home + file_path):
    #        raise Exception,"文件[" + local_home + file_path + "]下载失败"
    #    
    #    return True
    #    
    #except Exception, e:
    #    AfaLoggerFunc.tradeInfo(e)
    #    return False
        
    try:
        local_home = os.environ['AFAP_HOME'] + "/data/batch/tips/"
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open( configFileName ) )
        
        #创建文件
        ftpShell = os.environ['AFAP_HOME'] + '/tmp/ftphost_tips.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + config.get('HOST_DZ','HOSTIP') + '\n')
        ftpFp.write('user ' + config.get('HOST_DZ','USERNO') + ' ' + config.get('HOST_DZ','PASSWD' ) + '\n')

        #下载文件
        ftpFp.write('cd '  + host_home + '\n')
        ftpFp.write('lcd ' + local_home + '\n')
        #ftpFp.write('bin ' + '\n')
        #ftpFp.write('quote to 1383 ' + '\n')
        ftpFp.write('get ' + file_path + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return False
        else:

            #判断文件是否存在
            sFileName = local_home + "/" + file_path
            if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
                return True
            else:
                WrtLog('>>>FTP处理下载文件失败')
                return False

    except Exception, e:
        WrtLog(e)
        WrtLog('>>>FTP处理异常')
        return False

    
def putHost(file_name,host_home,file_path = '/data/batch/tips/'):
    try:
        
        local_home = os.environ['AFAP_HOME'] + file_path
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open( configFileName ) )
        
        if not os.path.exists(local_home + file_name):
            raise Exception,"上传文件[" + local_home + file_name + "]不存在"
            
        ftp_p=ftplib.FTP(config.get('HOST_DZ','HOSTIP'),config.get('HOST_DZ','USERNO'),config.get('HOST_DZ','PASSWD' ))
        AfaLoggerFunc.tradeInfo('HOSTIP = '+config.get('HOST_DZ','HOSTIP') + 'USERNO = '+config.get('HOST_DZ','USERNO')+ 'PASSWD= '+config.get('HOST_DZ','PASSWD' ))
        ftp_p.cwd(host_home)
        file_handler = open(local_home + file_name,'rb')
        ftp_p.storbinary("STOR " + file_name,file_handler)
        file_handler.close()
        ftp_p.quit()
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
        
##################################################################
#   财税库行系统.取TIPS日期
#=================================================================
#   函    数:   GetTipsDate()
#   作    者:   刘雨龙
#   修改时间:   2008-09-09
##################################################################
def GetTipsDate( ):
    sql = "select workdate from tips_adm"
    ret = AfaDBFunc.SelectSql(sql)
    if ret == None:
        return AfaFlowControl.ExitThisFlow('S999','数据库操作失败')
    if len(ret) <= 0:
        return time.strftime( '%Y%m%d', time.localtime( ) )
    else:
        date = ret[0][0]
    return date 
    
    
#=========================日志==================================================
def WrtLog(logstr):

    #默认向文件和屏幕同时输出
    AfaLoggerFunc.tradeInfo(logstr)
    print logstr

    return True    
    
#==============更新批次状态======================================================
def UpdateBatchAdm(status,errorCode,errMsg):
    
    AfaLoggerFunc.tradeInfo('更新批次状态['+status+']'+errorCode+errMsg)
    sqlStr = "UPDATE TIPS_BATCHADM SET dealStatus='"+status+"',errorcode='"+errorCode+"',ERRORMSG='"+errMsg+"'"
    if( TradeContext.existVariable( "succNum" ) ):
        sqlStr =sqlStr +",SUCCNUM        = '" + TradeContext.succNum+ "'"
    if( TradeContext.existVariable( "succAmt" ) ):
        #TradeContext.succAmt=TradeContext.succAmt.rjust( 3, '0' )
        #TradeContext.succAmt=UtilTools.InsDot( TradeContext.succAmt.rjust( 3, '0' ), 2 )
        #TradeContext.succAmt=str(long(TradeContext.succAmt)/100.00)
        sqlStr =sqlStr +",SUCCAMT        = '" + TradeContext.succAmt+ "'"
    if( TradeContext.existVariable( "sFileName" ) ):
        sqlStr =sqlStr +",NOTE2 = '" + TradeContext.sFileName+ "'"
    sqlStr =sqlStr +" WHERE  "
    sqlStr =sqlStr +"WORKDATE  = '" + TradeContext.entrustDate     + "'"
    sqlStr =sqlStr +"and BATCHNO   = '" + TradeContext.packNo          + "'"
    sqlStr =sqlStr +"and TAXORGCODE     = '" + TradeContext.taxOrgCode      + "'"
    AfaLoggerFunc.tradeInfo(sqlStr )
    records=AfaDBFunc.UpdateSqlCmt( sqlStr )
    if( records <0 ):
        return AfaFlowControl.ExitThisFlow( 'A0027', '数据库错误' )
    return True
    
#==============更新批次明细状态======================================================
def UpdateBatchData(status,errorCode,errMsg):
    
    AfaLoggerFunc.tradeInfo('更新批次明细状态['+status+']'+errorCode+errMsg)
    sqlStr = "UPDATE TIPS_BATCHDATA SET STATUS='"+status+"',errorcode='"+errorCode+"',ERRORMSG='"+errMsg+"'"

    sqlStr =sqlStr +" WHERE  "
    sqlStr =sqlStr +"WORKDATE  = '" + TradeContext.entrustDate     + "'"
    sqlStr =sqlStr +"and BATCHNO   = '" + TradeContext.packNo          + "'"
    sqlStr =sqlStr +"and TAXORGCODE     = '" + TradeContext.taxOrgCode      + "'"
    sqlStr =sqlStr +"and SERIALNO       = '" + TradeContext.SerialNo      + "'"
    AfaLoggerFunc.tradeInfo(sqlStr )
    records=AfaDBFunc.UpdateSqlCmt( sqlStr )
    if( records <0 ):
        return AfaFlowControl.ExitThisFlow( 'A0027', '数据库错误' )
    return True
    
#=============查询清算行号对应的机构号====================
def GetBrno():
    sql="SELECT BRNO FROM TIPS_BRANCH_ADM WHERE STATUS = '1' AND PAYEEBANKNO='"+TradeContext.payeeBankNo+"'"
    records = AfaDBFunc.SelectSql(sql)
    AfaLoggerFunc.tradeInfo(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '未定义该机构信息')
    else:
        UtilTools.ListFilterNone( records )
        TradeContext.sBrno =records[0][0]  #收款机构号
    
    return True
    
################################################################################
# 函数名:    SelectAcc
# 参数:      无
# 返回值：    True  成功    False 失败
# 函数说明：  根据清算行号查询收款帐号
################################################################################
def SelectAcc():
    AfaLoggerFunc.tradeInfo( '>>>根据清算行号查询收款信息' )
    sql="SELECT STATUS,PAYBKCODE,PAYEEBANKNO,ACCNO,BANKNAME,BRNO "
    sql=sql+" FROM TIPS_BRANCH_ADM WHERE "
    sql=sql+" PAYBKCODE ='" + TradeContext.payBkCode +"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '数据库操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '该机构未开通此项业务' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_BRANCH_ADM表配置错误' )
    else:
        if records[0][0]=='0':
            return ExitThisFlow( 'A0027', '该机构此项业务已停止' )
        if records[0][0]=='2':
            return ExitThisFlow( 'A0027', '该机构此项业务已暂停' )

        if not( TradeContext.existVariable( "payBkCode" ) and len(TradeContext.payBkCode)>0):
            TradeContext.payBkCode       = records[0][1]
        TradeContext.__agentAccno__  = records[0][3]
        TradeContext.__agentAccname__   = records[0][4]
        TradeContext.qsBrno = records[0][5]            #清算机构
        AfaLoggerFunc.tradeInfo('机构状态正常,清算行号：'+TradeContext.payBkCode +' 待清算帐号：'+TradeContext.__agentAccno__)
        AfaLoggerFunc.tradeInfo('待清算帐户名：' + TradeContext.__agentAccname__) 
    return True
    
################################################################################
# 函数名:    SelCodeMsg
# 参数:      outcode:主机错误码
# 返回值：    错误码，错误信息
# 函数说明：  根据主机错误码获取返回码及返回信息
################################################################################
def SelCodeMsg( outcode):
    AfaLoggerFunc.tradeInfo( '转帐主机错误码' )
    AfaLoggerFunc.tradeInfo( '转换前,主机错误码:['+outcode+']' )
    respcode = ''
    respmsg  = ''
    sqlStr="select RESULTINF,ADDWORD from TIPS_ERRORCODE where ERRORCODE ='" + outcode + "'"
    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return ExitThisFlow( 'A0002', '主机错误码表操作异常:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )!=0 ):
        UtilTools.ListFilterNone( records )
        respcode=records[0][0].rstrip()
        respmsg=records[0][1].rstrip()
    else:
       respcode = '99090'
       respmsg  = '其它错误'
    AfaLoggerFunc.tradeInfo( '返回码:['+outcode+']['+respcode+']['+respmsg+']' )

    return respcode,respmsg


#def getDzFile(file_path,host_home):
#    try:
#        #host_home = "BANKMDS"
#        local_home = os.environ['AFAP_HOME'] + "/data/dz/host/"
#        
#        config = ConfigParser.ConfigParser( )
#        configFileName = os.environ['AFAP_HOME'] + '/conf/ftpconnect.conf'
#        config.readfp( open( configFileName ) )
#        
#        ftp_p = ftplib.FTP(config.get('host','ip'),config.get('host','username'),config.get('host','password' ))
#        ftp_p.cwd(host_home)
#        file_handler = open(local_home + file_path,'wb')
#        ftp_p.retrbinary("RETR " + file_path,file_handler.write)
#        file_handler.close()
#        ftp_p.quit()
#        
#        if not os.path.exists(local_home + file_path):
#            raise Exception,"文件[" + local_home + file_path + "]下载失败"
#        
#        return True
#        
#    except Exception, e:
#        AfaLoggerFunc.tradeInfo(e)
#        return False
#        
##格式化文件
#def FormatFile(ProcType, FLDName, sFileName, dFileName):
#
##    WrtLog('>>>格式化文件:' + ProcType + ' ' + sFileName + ' ' + dFileName)
#
#    try:
#
#        srcFileName    = os.environ['AFAP_HOME'] + '/data/dz/host/' + sFileName
#        dstFileName    = os.environ['AFAP_HOME'] + '/data/dz/host/' + dFileName
#
#        if (ProcType == "1"):
#            #ascii->ebcd
#            #调用格式:cvt2ebcdic -T 源文本文件 -P 目标物理文件 -F fld格式文件 [-D 间隔符 ]
#            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ebcdic'
#            #关彬捷  20081126  参数化设置fld文件
#            #fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/rccps01.fld'
#            fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/' + FLDName
#            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName + " -D '|' "
#
#        else:
#            #ebcd->ascii
#            #调用格式:cvt2ascii -T 生成文本文件 -P 物理文件 -F fld文件 [-D 间隔-符] [-S] [-R]
#            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
#            #关彬捷  20081126  参数化设置fld文件
#            #fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/rccps02.fld'
#            fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/' + FLDName
#            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName + " -D '|' "
#
#        #WrtLog('>>>' + cmdstr)
#        #ret = -1
#        WrtLog('>>>外调格式转换程序开始============')   #2007824
#        WrtLog(cmdstr)
#        ret = os.system(cmdstr)                         #2007824
#        if ( ret != 0 ):                                #2007824
#            ret = False                                 #2007824
#        else:                                           #2007824
#            ret = True                                  #2007824
#        #return 0                                       #2007824
#        WrtLog('>>>外调格式转换程序结束============')   #2007824
#
#        return ret
#        
#    except Exception, e:
#        WrtLog(e)
#        WrtLog('格式化文件异常')
#        return False
