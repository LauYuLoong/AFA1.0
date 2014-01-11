# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   5204_8438.py
#   程序说明:   [反交易查询]
#   修改时间:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    AfaLoggerFunc.tradeInfo( '初始化交易变量' )
    AfaLoggerFunc.tradeInfo( '反交易变量值的有效性校验' )
    if( not TradeContext.existVariable( "PreSerialno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '原交易流水号[PreSerialno]值不存在!' )
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
    AfaLoggerFunc.tradeInfo('进入反查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        sql = "select userno,username,amount,draccno,tellerno,craccno,subuserno,note8,note9,note10,note1,unitno,note7 "
        sql = sql + "from afa_maintransdtl where agentserialno = '"+TradeContext.PreSerialno+"'"
        sql = sql + "and workdate = '"+TradeContext.workDate+"'"
        sql = sql + " and revtranf = '0' and bankstatus = '0' and corpstatus = '0' and chkflag = '9'"
        AfaLoggerFunc.tradeInfo('反交易查询语句'+ sql)
        records = AfaDBFunc.SelectSql( sql )
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此交易"
            return False
        else:
            #if(records[0][4] != TradeContext.tellerno):
            #    TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本柜员所做，不能做此交易"
            #    return False
            #用户编号(保险单号)
            TradeContext.CpicNo = records[0][0]
            AfaLoggerFunc.tradeInfo("保险单号"+str(TradeContext.CpicNo))
            #用户名称
            #TradeContext.UserName = records[0][1]
            #金额
            TradeContext.Amount = records[0][2]
            AfaLoggerFunc.tradeInfo("金额"+str(TradeContext.Amount))
            #缴费类型(反款类型)/帐号
            if(type(records[0][3]) is str):
                TradeContext.Accno = records[0][3]
                #TradeContext.backtype = "1"
            else:
                TradeContext.Accno = ""
                #TradeContext.backtype = "0"
            #贷方帐号
            TradeContext.crAccno = records[0][5]
            #投保身份证
            #TradeContext.GovtID = records[0][6]
            #投保份数|保险类型
            arrayList = ""
            arrayList = (records[0][7]).split("|")
            TradeContext.IntialNum = arrayList[0].strip()
            TradeContext.ProCodeStr = arrayList[1].strip()
            #投保人姓名|投保人身份证号码
            arrayList = ""
            arrayList = (records[0][8]).split("|")
            TradeContext.UserName = arrayList[0].strip()
            TradeContext.GovtID   = arrayList[1].strip()
            AfaLoggerFunc.tradeInfo("投保人姓名"+str(TradeContext.UserName))
            #被保人名称|被保人身份证
            arrayList = ""
            arrayList = (records[0][9]).split("|")
            TradeContext.FullName = arrayList[1].strip()
            TradeContext.GovtIDF  = arrayList[2].strip()
            AfaLoggerFunc.tradeInfo("被保人名称"+str(TradeContext.FullName))
            #保单号
            TradeContext.CpciPNo  = records[0][10].strip()
            #单位编码
            TradeContext.unitno  = records[0][11].strip()
            #险种
            TradeContext.ProCode = records[0][12].strip()
            #交易返回码
            TradeContext.errorCode = '0000'
        AfaLoggerFunc.tradeInfo('退出反查询交易' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
