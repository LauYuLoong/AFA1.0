# -*- coding: gbk -*-
##################################################################
#   代收代付平台.公共函数类
#=================================================================
#   程序文件:   AfapFunc.py
#   修改时间:   2006-03-31
##################################################################
import TradeContext, AfaDBFunc, AfaFlowControl, AfaUtilTools
import os, time, AfaLoggerFunc
from types import *

#=======================查询类变量值的有效性校验==========================
def Query_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '查询类变量值的有效性校验[begin]' )
    if( not TradeContext.existVariable( "appNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '业务编号[appNo]值不存在!' )
        
    if( not TradeContext.existVariable( "busiNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'busiNo[busiNo]值不存在!' )
        
    if( not TradeContext.existVariable( "trxCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '交易代码[trxCode]值不存在!' )
                
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
    else:
        TradeContext.channelCode=AfaUtilTools.Lfill( TradeContext.channelCode, 3, '0' )
               
    if( TradeContext.channelCode == '001' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '机构代码[brno]值不存在!' )
                
        if( not TradeContext.existVariable( "teller" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[teller]值不存在!' )
    
    AfaLoggerFunc.tradeInfo( '查询类变量值的有效性校验[end]' )        

    return True

#=======================缴费类变量值的有效性校验==========================
def Pay_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '缴费类变量值的有效性校验[begin]' )
    if( not TradeContext.existVariable( "appNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '业务编码[appNo]值不存在!' )
        
    if( not TradeContext.existVariable( "busiNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '商号编号[busiNo]值不存在!' )

    if ( not TradeContext.existVariable( "termId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '终端号[termId]值不存在!')
    
    if ( not TradeContext.existVariable( "catrFlag") ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '现金转帐标志[catrFlag]不存在!')    
           
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
    else:
        TradeContext.channelCode=AfaUtilTools.Lfill( TradeContext.channelCode, 3, '0' )
            
    if( TradeContext.channelCode == '001' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '机构号[brno]值不存在!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[teller]值不存在!' )
                
    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '金额[amount]值不存在!' )
            
    if( not TradeContext.existVariable( "userNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '用户号[userNo]值不存在!' )
            
    if( not TradeContext.existVariable( "accno" ) ):
        TradeContext.accno=''
        
    #正交易
    TradeContext.revTranF='0'
    
    AfaLoggerFunc.tradeInfo( '缴费类变量值的有效性校验[end]' )
        
    return True


#=======================取消交易变量值的有效性校验==========================
def Cancel_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '取消交易变量值的有效性校验' )
        
    if( not TradeContext.existVariable( "appNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '业务代码[appNo]值不存在!' )
          
    if( not TradeContext.existVariable( "busiNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '商户代码[busiNo]值不存在!' )
         
    if( not TradeContext.existVariable( "zoneno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '地区号[zoneno]值不存在!' )
        
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
            
    else:
        TradeContext.channelCode=AfaUtilTools.Lfill( TradeContext.channelCode, 3, '0' )
    
    if( TradeContext.channelCode == '001' ):
        
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '网点号[brno]值不存在!' )
                
        if( not TradeContext.existVariable( "teller" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[teller]值不存在!' )
                
    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '金额[amount]值不存在!' )
        
    if( not TradeContext.existVariable( "preAgentSerno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '原交易流水号[preAgentSerno]值不存在!' )
        
    if( not TradeContext.existVariable( "userNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '用户号[userNo]值不存在!' )
            
    TradeContext.revTranF='1'
    
    return True


#校验反交易数据完整性 根据流水号比对用户号，帐号，交易金额
def ChkRevInfo( serialno ):

    AfaLoggerFunc.tradeInfo( '校验反交易数据完整性[begin]' )
        
    sqlstr="SELECT REVTRANF,USERNO,ACCNO,SUBACCNO,AMOUNT,SUBAMOUNT,TELLERNO,\
            SUBUSERNO,USERNAME,CONTRACTNO,VOUHTYPE,TERMID,\
            VOUHNO,BANKSERNO, CORPSERNO,CORPTIME,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,\
            NOTE7,NOTE8,NOTE9,NOTE10,CATRFLAG,WORKDATE,APPNO,BUSINO FROM FS_MAINTRANSDTL WHERE SERIALNO=" +\
            "'"+serialno+"' AND WORKDATE='"+TradeContext.workDate+ "'AND BANKSTATUS IN ('0','2')"  # 

    tmp = AfaDBFunc.SelectSql( sqlstr )
        
    AfaLoggerFunc.tradeInfo( tmp )
        
    if tmp == None :
        return AfaFlowControl.ExitThisFlow( 'A0025', AfaDBFunc.sqlErrMsg )
            
    elif len( tmp ) == 0 :
        AfaLoggerFunc.tradeInfo( sqlstr )
        return AfaFlowControl.ExitThisFlow( 'A0045', '未发现原交易' )
            
    tmp=AfaUtilTools.ListFilterNone( tmp )

    temp=tmp[0]
    if temp[0]!='0':
        return AfaFlowControl.ExitThisFlow( 'A0020', '无匹配信息反交易标志有误' )
            
    if temp[6]!=TradeContext.teller:
        return AfaFlowControl.ExitThisFlow( 'A0020', '柜员号不匹配' )
      
    #begin 20100624 蔡永贵增加
    if temp[28] != TradeContext.appNo:
        return AfaFlowControl.ExitThisFlow( 'A0020', '业务编号不匹配' )
    
    if temp[29] != TradeContext.busiNo:
        return AfaFlowControl.ExitThisFlow( 'A0020', '单位编号不匹配' )
    #end
        
            
    if AfaUtilTools.lrtrim(temp[1])!=TradeContext.userNo:
        return AfaFlowControl.ExitThisFlow( 'A0020', '用户号不匹配' )      
             
    if AfaUtilTools.lrtrim(temp[4])!=TradeContext.amount:
       AfaLoggerFunc.tradeInfo( temp[4] )
       return AfaFlowControl.ExitThisFlow( 'A0020', '金额不匹配' )
        
    if temp[1]!=TradeContext.userNo:
       return AfaFlowControl.ExitThisFlow( 'A0020', '用户号不匹配' )
    
    TradeContext.accno=temp[2]
    TradeContext.subAccno = temp[3]
    TradeContext.subAmount=temp[5]
    TradeContext.subUserNo=temp[7]   
    TradeContext.userName=temp[8]
    
    TradeContext.contractno=temp[9]
    TradeContext.vouhType=temp[10]
    TradeContext.termId=temp[11]
    TradeContext.vouhNo=temp[12]
    
    TradeContext.bankSerno=temp[13]

    TradeContext.corpSerno=temp[14]
    TradeContext.corpTime=temp[15]
    TradeContext.note1=temp[16]
    TradeContext.note2=temp[17]
    TradeContext.note3=temp[18]
    TradeContext.note4=temp[19]
    TradeContext.note5=temp[20]
    TradeContext.note6=temp[21]
    TradeContext.note7=temp[22]
    TradeContext.note8=temp[23]
    TradeContext.note9=temp[24]
    TradeContext.note10=temp[25]
    TradeContext.catrFlag =temp[26]
    TradeContext.revTrxDate = temp[27]
    AfaLoggerFunc.tradeInfo( '校验反交易数据完整性[end]' )
    return True


################################################################################
# 函数名:    ChkAbnormal
# 参数:      无
# 返回值：    0  无异常交易    1  有异常交易    -1  查询流水表检测异常失败
# 函数说明：  按柜员查询流水表中的主机异常交易 
################################################################################
def ChkAbnormal( ):

    AfaLoggerFunc.tradeInfo( '查询流水表中的主机异常交易' )
    sql="SELECT COUNT(*) FROM FS_MAINTRANSDTL WHERE WORKDATE='"+ \
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

#============================判断应用状态============================
def ChkAppStatus( ):

    AfaLoggerFunc.tradeInfo( '判断应用状态[begin]' )

    #============业务编号============
    sqlStr = "SELECT STATUS,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO FROM ABDT_UNITINFO WHERE APPNO = '" + TradeContext.appNo + "'"

    #============单位编码============
    sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busiNo + "'"

    #============委托方式============
    sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControl.ExitThisFlow( 'A0002', '代收代付_单位信息表:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
        #===============判断业务状态============================
        if( records[0][0]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '该业务处于未启用状态,不能做此交易' )
        elif( records[0][0]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '该业务处于关闭状态,不能做此交易' )
        elif( records[0][0]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0006', '该业务处于停用状态,不能做此交易' )
        
        #===============判断服务时间============================
        if( long( TradeContext.workDate )<long( records[0][1] ) or long( TradeContext.workDate )>long( records[0][2] ) ):
            return AfaFlowControl.ExitThisFlow ('A0008', "该业务已过期,有效期:["+records[0][1] + "-->" + records[0][2] + "]") 

        #================判断有效时间===========================
        if( long(TradeContext.workTime) < long(records[0][3])) or (long(TradeContext.workTime) > long(records[0][4])):
            return AfaFlowControl.ExitThisFlow( 'A0007', "超过业务开放时间,请在["+records[0][3]+"-->"+records[0][4]+"]做此业务" )

        #=============代理业务帐号=============
        TradeContext.__agentAccno__ = records[0][5]            

        TradeContext.Daccno = records[0][5]

        AfaLoggerFunc.tradeInfo( '判断应用状态[end]' )
        return True
    else:
        AfaLoggerFunc.tradeError( sqlStr )
        return AfaFlowControl.ExitThisFlow( 'A0003', '该地区没有开放此业务' )
