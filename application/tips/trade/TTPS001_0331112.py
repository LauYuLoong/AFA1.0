# -*- coding: gbk -*-
##################################################################
#   中间业务平台.行内资金清算
#   功能描述：将各县联社资金清算到付款行（11家）
#=================================================================
#   程序文件:   TTPS001_0331112.py
#   修改时间:   2007-8-18 13:43
##################################################################
import TradeContext, AfaLoggerFunc, UtilTools,AfaDBFunc,TipsFunc,AfaFlowControl
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('财税库行_行内资金清算开始[TTPS001_0331112]' )
    TradeContext.TransCode='0331112'
    try:
        #=============获取当前系统时间====================
        #TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        TradeContext.__agentAccno__ = TradeContext.payeeAcct    #清算行国库待清算专户作为贷方账户
        AfaLoggerFunc.tradeInfo( '待清算专户:'+TradeContext.__agentAccno__)
        sqlStr = "SELECT BRNO,ACCNO FROM TIPS_BRANCH_ADM WHERE PAYBKCODE = '" + TradeContext.payBkCode.strip() + "' AND "
        sqlStr = sqlStr+" PAYEEBANKNO = '" + TradeContext.payeeBankNo.strip() + "' "
        AfaLoggerFunc.tradeInfo( sqlStr )
        records = AfaDBFunc.SelectSql( sqlStr )
        if( records == None ):
            return TipsFunc.ExitThisFlow( 'A0002', '机构信息表操作异常:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            AfaLoggerFunc.tradeError( sqlStr )
            return TipsFunc.ExitThisFlow( 'A0003', '无机构信息' )
        else:
            records=UtilTools.ListFilterNone( records )
            for i in range( 0, len( records ) ):
                AfaLoggerFunc.tradeInfo( 'brno:'+records[i][0] +' accno:'+records[i][1])
                #=============清算：出现清算金额大于银行发生额，需要联社1391科目垫款====================
                #统计县联社对账差异金额作为转账金额
                if not DoSumAmount(records[i][0]):
                    return TipsFunc.ExitThisFlow( 'A0027', '汇总发生额失败' )
                #TradeContext.amount='1'
                
                if (TradeContext.amount)>0 :
                    #检查改机构是否已经清算
                    sqlStr_qs = "SELECT COUNT(*) FROM TIPS_MAINTRANSDTL WHERE TAXPAYCODE = '-' "
                    sqlStr_qs = sqlStr_qs + "AND  DRACCNO = '"+records[i][1]+"' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE1 = '" + TradeContext.chkDate + "' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE2 = '" + TradeContext.chkAcctOrd + "' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE3 = '" + TradeContext.payBkCode.strip()   + "' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE4 = '" + TradeContext.payeeBankNo.strip() + "' "
                    sqlStr_qs = sqlStr_qs + "AND  NOTE6 = '1'" 
                    AfaLoggerFunc.tradeInfo( sqlStr_qs )
                    Records_qs = AfaDBFunc.SelectSql( sqlStr_qs )
                    if(Records_qs == None or Records_qs < 0):
                        return TipsFunc.ExitThisFlow( 'A0002', '流水表操作异常:'+AfaDBFunc.sqlErrMsg )
                    elif (Records_qs[0][0]==0): 
                        TradeContext.channelCode    = '009'
                        TradeContext.catrFlag       = '1'         #现金转账标志
                        TradeContext.tellerno       = '999986'                   #
                        TradeContext.termId         = 'tips'
                        TradeContext.brno           = records[i][0]              #
                        TradeContext.zoneno         = TradeContext.brno[0:3]
                        TradeContext.accno          = records[i][1]              #机构4401账户作为借方账户
                        TradeContext.amount         =str(TradeContext.amount)
                        AfaLoggerFunc.tradeInfo( '借方:'+TradeContext.accno+'贷方:' +TradeContext.__agentAccno__)
                        TradeContext.taxPayCode     = '-'
                        TradeContext.tradeType      = 'T'                       #转账类交易
                        TradeContext.taxPayName     = '清算流水'
                        TradeContext.note1          = TradeContext.chkDate            
                        TradeContext.note2          = TradeContext.chkAcctOrd         
                        TradeContext.note3          = TradeContext.payBkCode.strip()  
                        TradeContext.note4          = TradeContext.payeeBankNo.strip()
                        TradeContext.note6          = '1'       #清算流水
                        TradeContext.revTranF       = '0'
                        TradeContext.workTime       =UtilTools.GetSysTime( )
                        TradeContext.taxTypeNum     = '0'
                        
                        #====获取摘要代码=======
                        if not AfaFlowControl.GetSummaryCode():
                            return False
                        
                        #=============获取平台流水号====================
                        if TipsFunc.GetSerialno( ) == -1 :
                            AfaLoggerFunc.tradeInfo('>>>处理结果:获取平台流水号异常' )
                            return TipsFunc.ExitThisFlow( 'A0027', '获取流水号失败' )
                        #
                        #=============插入流水表====================
                        if not TipsFunc.InsertDtl( ) :
                            return TipsFunc.ExitThisFlow( 'A0027', '插入流水表失败' )
                        
                        #=============与主机通讯====================
                        TipsFunc.CommHost()
                        
                        #=============更新主机返回状态====================
                        TipsFunc.UpdateDtl( 'TRADE' )
                        
                        if TradeContext.errorCode!='0000':
                            AfaLoggerFunc.tradeFatal( '清算记账失败：['+TradeContext.errorCode+']'+ TradeContext.errorMsg)
                            return False
                    else:
                        continue    #已经清算，继续下一个机构
        AfaLoggerFunc.tradeInfo('财税库行_行内资金清算结束[TTPS001_0331112]' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
#汇总成功发生额 
def DoSumAmount(psSubUnitno):
    sSqlStr = "SELECT sum(cast(amount as decimal(17,2))) FROM TIPS_MAINTRANSDTL WHERE  NOTE1 ='"+TradeContext.chkDate+"'"
    sSqlStr = sSqlStr + " AND NOTE2 ='" + TradeContext.chkAcctOrd+"'"
    sSqlStr = sSqlStr + " AND NOTE3 ='" + TradeContext.payBkCode.strip()+"'"
    sSqlStr = sSqlStr + " AND NOTE4 ='" + TradeContext.payeeBankNo.strip()+"'"
    sSqlStr = sSqlStr + " AND CHKFLAG='0' AND CORPCHKFLAG='0'"
    AfaLoggerFunc.tradeInfo( sSqlStr )
    SumRecords = AfaDBFunc.SelectSql( sSqlStr )
    if(SumRecords == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return TipsFunc.ExitThisFlow( 'A0002', '流水表表操作异常:'+AfaDBFunc.sqlErrMsg )
    else:
        SumRecords=UtilTools.ListFilterNone( SumRecords ,'0')
        TradeContext.amount=SumRecords[0][0]
        AfaLoggerFunc.tradeInfo( '汇总机构发生额'+str(TradeContext.amount) )
    return True

