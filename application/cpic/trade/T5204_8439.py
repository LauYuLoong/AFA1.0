# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   5204_8439.py
#   程序说明:   [根据保单号查询缴费信息]
#   修改时间:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    AfaLoggerFunc.tradeInfo( '初始化交易变量' )
    AfaLoggerFunc.tradeInfo( '缴费信息查询变量值的有效性校验' )
    if( not TradeContext.existVariable( "CpicNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '保险单号[CpicNo]值不存在!' )
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[tellerno]值不存在!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '网点号[brno]值不存在!' )
        if( not TradeContext.existVariable( "termid" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[termid]值不存在!' )
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('缴费信息查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        sql = "select agentserialno,"
        sql = sql + "userno,username,idcode,amount,usernameb,idcodeb,loandate,loanenddate,crevouno,crebarno,procode,cpicteller,note1 "
        sql = sql + " from afa_adbinfo where userno = '" + TradeContext.CpicNo.strip() + "' and note3 = '" + TradeContext.unitno.strip() + "'"
        sql = sql + " and workdate = '"+TradeContext.workDate + "'"
        sql = sql + " and tellerno = '"+TradeContext.tellerno + "'"
        sql = sql + " and dtlstatus = '0' "
        sql = sql + " order by agentserialno desc"
        AfaLoggerFunc.tradeInfo('缴费信息查询语句'+ sql)
        records = AfaDBFunc.SelectSql( sql )
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此投保信息"
            return False
        else:
            #用户编号(保险单号)
            TradeContext.CpicNo = records[0][1]
            #投保人名称
            TradeContext.UserName = records[0][2]
            #投保人身份证号码
            TradeContext.GovtID = records[0][3]
            #金额
            TradeContext.PaymentAmt = records[0][4]
            #被保人姓名
            TradeContext.UserNameB = records[0][5]
            #被保人身份证号码
            TradeContext.GovtIDB = records[0][6]
            #借款日期
            TradeContext.LoanDate = records[0][7]
            #借款到期日
            TradeContext.LoanEndDate = records[0][8]
            #借款凭证编号
            TradeContext.CreVouNo = records[0][9]
            #贷款合同编号
            TradeContext.CreBarNo = records[0][10]
            #保险种类
            TradeContext.ProCode = records[0][11]
            #太保业务员代码
            TradeContext.CpicTeller = records[0][12]
            #保单号
            TradeContext.CpciPNo = records[0][13]
            #交易返回码
            TradeContext.errorCode = '0000'
        AfaLoggerFunc.tradeInfo('退出缴费信息查询交易' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
