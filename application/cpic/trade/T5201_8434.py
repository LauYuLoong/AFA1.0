# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   4201_8434.py
#   程序说明:   [8434--6000811]当日单证重打
#   修改时间:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc,AfaAhAdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #begin  20091120  蔡永贵  增加
    #校验保险公司代码和凭证种类是否合法
    if not AfaAhAdb.ADBCheckCert( ):
        return False
    #end

    AfaLoggerFunc.tradeInfo( '初始化交易变量' )
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    #险种
    if( TradeContext.existVariable( "ProCode" ) ):
        if ( TradeContext.ProCode == "1" ):
            TradeContext.ProCodeStr = "EL5612"
            TradeContext.PlanName   = "安贷宝"
            TradeContext.OCpicType  = "002"
        elif ( TradeContext.ProCode == "2" ):
            TradeContext.ProCodeStr = "211610"
            TradeContext.PlanName   = "华夏借款人意外伤害保险"

    try:
        #查询保单号
        sql = ""
        sql = "select note5,note4,note2,note8,amount,bankserno,acctype,agentserialno from afa_maintransdtl where agentserialno = '"+TradeContext.PreSerialno+"'"
        sql = sql + " and userno = '"+TradeContext.OCpicNo+"'"
        sql = sql + " and bankstatus = '0' and corpstatus = '0' and revtranf = '0'"
        AfaLoggerFunc.tradeInfo('当日单证重打查询语句'+ sql)
        records = AfaDBFunc.SelectSql( sql )
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此交易"
            return False
        else:
            AfaLoggerFunc.tradeDebug("records=" + str(records))
            TradeContext.PolNumber = records[0][0]
            #note1 : "贷款合同编号"+"|"+"贷款凭证编号"
            arrayList = ""
            arrayList = (records[0][1]).split("|")
            TradeContext.CreBarNo = arrayList[0].strip()
            TradeContext.CreVouNo = arrayList[1].strip()
            #note2 : "借款日期"+"|"+"借款到期日"
            arrayList = ""
            arrayList = (records[0][2]).split("|")
            TradeContext.LoanDate    = arrayList[0].strip()
            TradeContext.LoanEndDate = arrayList[1].strip()
            #note8 : "投保份数"+"|"+"险种代码"+"|"+"险种名称"
            arrayList = ""
            arrayList = (records[0][3]).split("|")
            TradeContext.IntialNum    = arrayList[0].strip()
            TradeContext.ProCodeStr   = arrayList[1].strip()
            TradeContext.PlanName     = arrayList[2].strip()
            #amount : "缴费金额"
            TradeContext.amount      = records[0][4].strip()
            #bankserno : "主机柜员流水号"
            TradeContext.hostserialno = records[0][5].strip()
            #acctype : "账户类型"
            if records[0][6].strip() == '000':
                TradeContext.AccType = "0"
            else:
                TradeContext.AccType = "4"
            #agentSerialno: "中间业务流水号"
            TradeContext.agentserialno = records[0][7].strip()
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('进入查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
    try:
        
        Party3Context.agentSerialno = TradeContext.agentserialno
        Party3Context.workDate      = TradeContext.workDate
        Party3Context.workTime      = TradeContext.workTime
        Party3Context.amount        = TradeContext.amount
        Party3Context.hostserialno  = TradeContext.hostserialno
        Party3Context.CreBarNo      = TradeContext.CreBarNo  
        Party3Context.CreVouNo      = TradeContext.CreVouNo  
        Party3Context.LoanDate      = TradeContext.LoanDate
        Party3Context.LoanEndDate   = TradeContext.LoanEndDate
        Party3Context.ProCode       = TradeContext.ProCode
        Party3Context.ProCodeStr    = TradeContext.ProCodeStr
        Party3Context.PlanName      = TradeContext.PlanName  
        Party3Context.AccType       = TradeContext.AccType   
        
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            setattr( TradeContext, name, value )
            #AfaLoggerFunc.tradeInfo("字段名称  ["+str(name)+"] =  "+str(value))
        if( TradeContext.errorCode == '0000' ):
            #if( TradeContext.existVariable( "ProCodeStr" ) ):
            #    if (TradeContext.ProCodeStr == "EL5602"):
            #        TradeContext.ProCode == "1"
            #    else:
            #        TradeContext.ProCode == "0"
            #责任起始日期日期
            if ( TradeContext.existVariable( "EffDate" )):
                if ( len(str(TradeContext.EffDate)) == 14 ):
                    TradeContext.EffDate = TradeContext.EffDate[0:4]+TradeContext.EffDate[6:8]+TradeContext.EffDate[10:12]
            if ( TradeContext.existVariable( "TermDate" )):
                if ( len(str(TradeContext.TermDate)) == 14 ):
                    TradeContext.TermDate = TradeContext.TermDate[0:4]+TradeContext.TermDate[6:8]+TradeContext.TermDate[10:12]
            update_sql = "update afa_maintransdtl set "
            update_sql = update_sql + " userno = '" + TradeContext.NCpicNo + "'"
            update_sql = update_sql + " where userno = '" + TradeContext.OCpicNo + "'"
            if not AfaDBFunc.UpdateSqlCmt(update_sql):
                return AfaFlowControl.exitThisFlow("A999","更新投保单号失败")

        AfaLoggerFunc.tradeInfo('退出查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']与第三方通讯后处理' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
