# -*- coding: gbk -*-
##################################################################
#   中间业务平台.行内资金清算
#   功能描述：将各县联社资金清算到付款行（11家）
#=================================================================
#   程序文件:   003001_0331112.py
#   修改时间:   2007-8-18 13:43
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools, AfaFlowControll, AfaDBFunc
#,AfaHostFunc,AfaFlowControl,TransDtlFunc
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('财税库行_行内资金清算开始[T003001_0331112]' )
    TradeContext.TransCode='0331112'
    try:
        #=============获取当前系统时间====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        #============系统标识============
        sqlStr = "SELECT * FROM AFA_UNITADM WHERE APPNO = '" + TradeContext.appNo + "' AND "
        #============商户代码============
        sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' "
        AfaLoggerFunc.tradeInfo( sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            return AfaFlowControll.ExitThisFlow( 'A0002', '商户信息表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            AfaLoggerFunc.tradeError( sqlStr )
            return AfaFlowControll.ExitThisFlow( 'A0003', '无此商户信息' )
        else:
            records=UtilTools.ListFilterNone( records )
            ##=============商户名称=============
            #TradeContext.unitName = records[0][2]
            ##=============商户简称=============
            #TradeContext.unitSName = records[0][3]
            #
            ##===============判断商户状态============================
            #if( records[0][4]=="0" ):
            #    return AfaFlowControll.ExitThisFlow( 'A0004', '该商户处于关闭状态,不能做交易' )
            #elif( records[0][4]=="2" ):
            #    return AfaFlowControll.ExitThisFlow( 'A0005', '该商户处于暂停状态,不能做交易' )
            #elif( records[0][4]=="3" ):
            #    return AfaFlowControll.ExitThisFlow( 'A0005', '该商户处于未启用状态,不能做交易' )
            ##=============银行角色=============
            #TradeContext.__bankMode__ = records[0][5]
            #=============业务模式=============
            TradeContext.__busiMode__ = records[0][6]
            #=============账户模式=============
            TradeContext.__accMode__ = records[0][7]
            AfaLoggerFunc.tradeInfo( '业务模式:'+TradeContext.__busiMode__+'  账户模式:'+ TradeContext.__accMode__)
            ##===============业务模式============================
            #if( TradeContext.__busiMode__!="2" ): 
            #======================账户模式============================
            if( TradeContext.__accMode__ !="2" ):   #无分支商户单位，不需行内清算
                return True
                ##===============银行商户代码（商户号）============================
                #TradeContext.bankUnitno = records[0][8]
                ##===============主办分行号============================
                #if(len(records[0][9])>0):
                #    TradeContext.mainZoneno = records[0][9]
                ##===============主办网点号============================
                #if(len(records[0][10])>0):
                #    TradeContext.mainBrno = records[0][10]
                ##===============银行编码============================
                #TradeContext.bankno = records[0][16]
                ##=============单位账号=============
                #TradeContext.__agentAccno__ = records[0][17]
                ##=============摘要代码（帐务核心系统需要）=============
                #TradeContext.__zhaiYaoCode__ = records[0][32]
                ##=============摘要（帐务核心系统需要）=============
                #TradeContext.__zhaiYao__ = records[0][33]
            if( TradeContext.__accMode__ == '2' ):
                #=============贷方账号（清算行帐号）=============
                TradeContext.agentAccno = records[0][17]
                #=========商户分支单位=============
                #============系统标识============
                sqlStr = "SELECT * FROM AFA_SUBUNITADM WHERE APPNO = '" + TradeContext.appNo + "' AND "
                #============商户代码============
                sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' "
                AfaLoggerFunc.tradeInfo( sqlStr )
                subRecords = AfaDBFunc.SelectSql( sqlStr )
                if(subRecords == None ):
                    # AfaLoggerFunc.tradeFatal( sqlStr )
                    return AfaFlowControll.ExitThisFlow( 'A0002', '商户分支单位信息表操作异常:'+AfaDBFunc.sqlErrMsg )
                elif( len( subRecords )==0 ):
                    return AfaFlowControll.ExitThisFlow( 'A0002', '商户分支单位中无记录，参数设置有误' )
                else:
                    subRecords=UtilTools.ListFilterNone( subRecords )
                    for i in range( 0, len( subRecords ) ):
                        subUnitno = subRecords[i][2]
                        AfaLoggerFunc.tradeInfo( 'subunitno:'+subUnitno )
                        #=============摘要代码=============
                        TradeContext.__zhaiYaoCode__ = subRecords[i][32]
                        #=============摘要=============
                        TradeContext.__zhaiYao__    = subRecords[i][33]
                        #=============清算：出现清算金额大于银行发生额，需要联社1391科目垫款====================
                        #统计县联社对账差异金额作为转账金额
                        if not DoSumAmountDiff(subUnitno):
                            return AfaFlowControll.ExitThisFlow( 'A0027', '汇总发生额失败' )
                        #TradeContext.amount='1'
                        TradeContext.amount     =str(long(float(TradeContext.amountDiff)))
                        if long(TradeContext.amount)>0 :
                            #检查是否已经清算
                            sqlStr_qs = "SELECT COUNT(*) FROM AFA_MAINTRANSDTL WHERE APPNO = '" + TradeContext.appNo + "'"
                            sqlStr_qs = sqlStr_qs + "AND  UNITNO = '" + TradeContext.unitno + "' "
                            sqlStr_qs = sqlStr_qs + "AND  SUBUNITNO = '" + subUnitno + "' "
                            sqlStr_qs = sqlStr_qs + "AND  USERNO = '-' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE2 = '" + TradeContext.ChkDate + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE3 = '" + TradeContext.ChkAcctOrd + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE4 = '" + TradeContext.PayBkCode.strip()   + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE5 = '" + TradeContext.PayeeBankNo.strip() + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE6 = '0'" 
                            AfaLoggerFunc.tradeInfo( sqlStr_qs )
                            Records_qs = AfaDBFunc.SelectSql( sqlStr_qs )
                            if(Records_qs == None ):
                                # AfaLoggerFunc.tradeFatal( sqlStr )
                                return AfaFlowControll.ExitThisFlow( 'A0002', '流水表操作异常:'+AfaDBFunc.sqlErrMsg )
                            elif (len(Records_qs)=0): 
                                TradeContext.__chkAccPwdCtl__='0'   
                                TradeContext.channelCode='009'
                                TradeContext.accType    ='001'
                                TradeContext.tellerno   ='999986'                   #
                                TradeContext.cashTelno  ='999986'                   #
                                TradeContext.termId     ='tips'
                                TradeContext.brno       =subUnitno                  #unitno作为记账网点号
                                TradeContext.zoneno     =TradeContext.brno[0:3]
                                TradeContext.accno      =subRecords[i][18]          #联社1391账户作为借方账户
                                TradeContext.__agentAccno__=subRecords[i][17]       #联社2013账户作为贷方账户
                                AfaLoggerFunc.tradeInfo( '借方:'+TradeContext.accno+'贷方:' +TradeContext.__agentAccno__)
                                TradeContext.userno      ='-'
                                TradeContext.tradeType   ='T'                       #转账类交易
                                TradeContext.userName    =subRecords[i][3]+'.清算流水'
                                AfaFlowControl.GetBranchInfo(TradeContext.brno)
                                TradeContext.note1      =TradeContext.__mngZoneno__ #上级管理机构
                                TradeContext.note2      =TradeContext.ChkDate            
                                TradeContext.note3      =TradeContext.ChkAcctOrd         
                                TradeContext.note4      =TradeContext.PayBkCode.strip()  
                                TradeContext.note5      =TradeContext.PayeeBankNo.strip()
                                TradeContext.note6      ='0' #垫款流水
                                TradeContext.revTranF   ='0'
                                #TradeContext.tradeType  ='T' #转账类交易
                                TradeContext.workTime   =UtilTools.GetSysTime( )
                                #=============获取平台流水号====================
                                if AfaFlowControl.GetSerialno( ) == -1 :
                                    AfaLoggerFunc.tradeInfo('>>>处理结果:获取平台流水号异常' )
                                    return AfaFlowControll.ExitThisFlow( 'A0027', '获取流水号失败' )
                                #
                                TradeContext.subUnitno  =subUnitno       #流水中分支商户代码
                                #=============插入流水表====================
                                if not TransDtlFunc.InsertDtl( ) :
                                    return AfaFlowControll.ExitThisFlow( 'A0027', '插入流水表失败' )
                                
                                #=============与主机通讯====================
                                AfaHostFunc.AfaCommHost('705050') 
                                #if TradeContext.errorCode!='0000':
                                #    return False
                                #=============更新主机返回状态====================
                                TransDtlFunc.UpdateDtl( 'TRADE' )
                            
                        #=============清算：从联社2013进清算行2621====================
                        ##统计县联社总发生额作为转账金额
                        #if not DoSumAmount(subUnitno):
                        #    return AfaFlowControll.ExitThisFlow( 'A0027', '汇总发生额失败' )
                        #TradeContext.amount='1'
                        TradeContext.amount     =str(long(float(TradeContext.amountQS)))
                        if long(TradeContext.amount)>0 :
                            #检查是否已经清算
                            sqlStr_qs = "SELECT COUNT(*) FROM AFA_MAINTRANSDTL WHERE APPNO = '" + TradeContext.appNo + "'"
                            sqlStr_qs = sqlStr_qs + "AND  UNITNO = '" + TradeContext.unitno + "' "
                            sqlStr_qs = sqlStr_qs + "AND  SUBUNITNO = '" + subUnitno + "' "
                            sqlStr_qs = sqlStr_qs + "AND  USERNO = '-' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE2 = '" + TradeContext.ChkDate + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE3 = '" + TradeContext.ChkAcctOrd + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE4 = '" + TradeContext.PayBkCode.strip()   + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE5 = '" + TradeContext.PayeeBankNo.strip() + "' "
                            sqlStr_qs = sqlStr_qs + "AND  NOTE6 = '1'" 
                            AfaLoggerFunc.tradeInfo( sqlStr_qs )
                            Records_qs = AfaDBFunc.SelectSql( sqlStr_qs )
                            if(Records_qs == None ):
                                # AfaLoggerFunc.tradeFatal( sqlStr )
                                return AfaFlowControll.ExitThisFlow( 'A0002', '流水表操作异常:'+AfaDBFunc.sqlErrMsg )
                            elif (len(Records_qs)=0): 
                                TradeContext.__chkAccPwdCtl__='0'   
                                TradeContext.channelCode='009'
                                TradeContext.accType    ='001'
                                TradeContext.tellerno   ='999986'                   #
                                TradeContext.cashTelno  ='999986'                   #
                                TradeContext.termId     ='tips'
                                TradeContext.brno       =TradeContext.unitno        #unitno作为记账网点号
                                TradeContext.zoneno     =TradeContext.brno[0:3]
                                TradeContext.accno      =subRecords[i][17]          #联社2013结算账户作为借方账户
                                TradeContext.__agentAccno__=TradeContext.agentAccno #清算行2621作为贷方
                                AfaLoggerFunc.tradeInfo( '借方:'+TradeContext.accno+'贷方:' +TradeContext.__agentAccno__)
                                if TradeContext.accno==TradeContext.__agentAccno__: #无需清算
                                    continue
                                TradeContext.userno      ='-'
                                TradeContext.tradeType   ='T'                       #转账类交易
                                TradeContext.userName    =subRecords[i][3]+'.清算流水'
                                AfaFlowControl.GetBranchInfo(TradeContext.brno)
                                TradeContext.note1      =TradeContext.__mngZoneno__ #上级管理机构
                                TradeContext.note2      =TradeContext.ChkDate            
                                TradeContext.note3      =TradeContext.ChkAcctOrd         
                                TradeContext.note4      =TradeContext.PayBkCode.strip()  
                                TradeContext.note5      =TradeContext.PayeeBankNo.strip()
                                TradeContext.note6      ='1' #清算流水
                                TradeContext.revTranF   ='0'
                                TradeContext.workTime   =UtilTools.GetSysTime( )
                                #=============获取平台流水号====================
                                if AfaFlowControl.GetSerialno( ) == -1 :
                                    AfaLoggerFunc.tradeInfo('>>>处理结果:获取平台流水号异常' )
                                    return AfaFlowControll.ExitThisFlow( 'A0027', '获取流水号失败' )
                                #
                                TradeContext.subUnitno  =TradeContext.unitno       #流水中分支商户代码=商户代码
                                #=============插入流水表====================
                                if not TransDtlFunc.InsertDtl( ) :
                                    return AfaFlowControll.ExitThisFlow( 'A0027', '插入流水表失败' )
                                
                                #=============与主机通讯====================
                                AfaHostFunc.AfaCommHost('705050') 
                                #if TradeContext.errorCode!='0000':
                                #    return False
                                #=============更新主机返回状态====================
                                TransDtlFunc.UpdateDtl( 'TRADE' )
                            
        #TradeContext.errorCode='0000'
        #TradeContext.errorMsg='交易成功'
        AfaLoggerFunc.tradeInfo('财税库行_行内资金清算结束[T003001_0331112]' )
        return True
    except Exception, e:
        AfaFlowControll.exitMainFlow(str(e))
#汇总成功发生额 
def DoSumAmount(psSubUnitno):
    sSqlStr="SELECT SUM(AMOUNT) FROM AFA_MAINTRANSDTL WHERE  APPNO='"+TradeContext.appNo+"'"
    sSqlStr=sSqlStr+" AND UNITNO='"+TradeContext.unitno+"'"
    sSqlStr=sSqlStr+" AND SUBUNITNO='"+psSubUnitno+"'"
    sSqlStr=sSqlStr+" AND NOTE9='"+TradeContext.ChkDate+"'"
    sSqlStr=sSqlStr+" AND NOTE10='"+TradeContext.ChkAcctOrd+"'"
    sSqlStr=sSqlStr+" AND CHKFLAG='0' AND CORPCHKFLAG='0'"
    AfaLoggerFunc.tradeInfo( sSqlStr )
    SumRecords = AfaDBFunc.SelectSql( sSqlStr )
    if(SumRecords == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControll.ExitThisFlow( 'A0002', '流水表表操作异常:'+AfaDBFunc.sqlErrMsg )
    else:
        SumRecords=UtilTools.ListFilterNone( SumRecords ,'0')
        TradeContext.amount=SumRecords[0][0]
        AfaLoggerFunc.tradeInfo( '汇总联社发生额'+str(TradeContext.amount) )
    return True

#汇总差异发生额 
def DoSumAmountDiff(psSubUnitno):
    sSqlStr="SELECT SUM(AMOUNT) FROM AFA_MAINTRANSDTL WHERE  APPNO='"+TradeContext.appNo+"'"
    sSqlStr=sSqlStr+" AND UNITNO='"+TradeContext.unitno+"'"
    sSqlStr=sSqlStr+" AND SUBUNITNO='"+psSubUnitno+"'"
    sSqlStr=sSqlStr+" AND NOTE9='"+TradeContext.ChkDate+"'"
    sSqlStr=sSqlStr+" AND NOTE10='"+TradeContext.ChkAcctOrd+"'"
    sSqlStr=sSqlStr+" AND CHKFLAG='0'"
    AfaLoggerFunc.tradeInfo( sSqlStr )
    SumRecords = AfaDBFunc.SelectSql( sSqlStr )
    if(SumRecords == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControll.ExitThisFlow( 'A0002', '流水表表操作异常:'+AfaDBFunc.sqlErrMsg )
    else:
        SumRecords=UtilTools.ListFilterNone( SumRecords ,'0')
        TradeContext.amount=str(SumRecords[0][0])
        AfaLoggerFunc.tradeInfo( '汇总联社发生额'+str(TradeContext.amount) )    

    sSqlStr="SELECT SUM(AMOUNT)*100 FROM CHECK_TRANSDTL WHERE  APPNO='"+TradeContext.appNo+"'"
    sSqlStr=sSqlStr+" AND UNITNO='"+TradeContext.unitno+"'"
    sSqlStr=sSqlStr+" AND SUBUNITNO='"+psSubUnitno+"'"
    sSqlStr=sSqlStr +" and workDate  = '" + TradeContext.ChkDate            + "'"
    sSqlStr=sSqlStr +" and Batchno   = '" + TradeContext.ChkAcctOrd         + "'"
    sSqlStr=sSqlStr +" AND NOTE3     ='"  + TradeContext.PayBkCode.strip()  + "'"   
    sSqlStr=sSqlStr +" AND NOTE2     ='"  + TradeContext.PayeeBankNo.strip()  + "'"
    #sSqlStr=sSqlStr+" AND CHKFLAG!='0' AND CORPCHKFLAG='0'"
    AfaLoggerFunc.tradeInfo( sSqlStr )
    SumRecords = AfaDBFunc.SelectSql( sSqlStr )
    if(SumRecords == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControll.ExitThisFlow( 'A0002', '流水表表操作异常:'+AfaDBFunc.sqlErrMsg )
    else:
        SumRecords=UtilTools.ListFilterNone( SumRecords ,'0')
        TradeContext.amountQS=str(SumRecords[0][0])
        AfaLoggerFunc.tradeInfo( '汇总联社清算额'+str(TradeContext.amount) )
    TradeContext.amountDiff=str(long(float(TradeContext.amountQS)) - long(float(TradeContext.amount)))
    
    return True
    