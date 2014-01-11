# -*- coding: gbk -*-
##################################################################
#   代收代付平台.财税库行横向联网.查询申报信息
#=================================================================
#   程序文件:   TTPS001_8465.py
#   修改时间:   2007-10-23
##################################################################

import TradeContext,  AfaFlowControl,   AfaLoggerFunc,TipsFunc
import AfaAfeFunc,Party3Context
#LoggerHandler, UtilTools,AfaDBFunc,os,

def StrAdd(a):
    b = ''
    AfaLoggerFunc.tradeInfo('============='+ a)
    if(type(a)==[]):
        for i in range(len(a)):
            b = b + a[i] + '|'
    else:
        b = a
    AfaLoggerFunc.tradeInfo('============='+ b)
    return b

def SubModuleMainFst( ):

    #TradeContext.projectId = ''
    #TradeContext.dn_taxTypeName = ''
    #TradeContext.dn_taxTypeCode = ''
    #TradeContext.dn_taxStartDate = ''
    #TradeContext.dn_taxEndDate = ''
    #TradeContext.dn_taxType = ''
    #TradeContext.dn_detailNum = ''
    #
    #TradeContext.dn_detailNo = ''
    #TradeContext.dn_taxSubjectCode = ''
    #TradeContext.dn_taxNumber = ''
    #TradeContext.dn_taxAmt = ''
    #TradeContext.dn_factTaxAmt = ''
    
    #=============获取平台流水号====================
    if TipsFunc.GetSerialno( ) == -1 :
        raise AfaFlowControl.flowException( )

    #=============与第三方通讯====================
    AfaAfeFunc.CommAfe()
    if( TradeContext.errorCode != '0000' ):
        return False
    
    TradeContext.taxOrgCode = Party3Context.taxOrgCode
    TradeContext.corpCode = Party3Context.corpCode
    TradeContext.taxPayCode = Party3Context.taxPayCode
    TradeContext.outerLevyNo = Party3Context.outerLevyNo
    TradeContext.payOpBkCode = Party3Context.payOpBkCode
    TradeContext.bankName = Party3Context.bankName
    TradeContext.traAmt = Party3Context.traAmt
    TradeContext.detailNum = Party3Context.detailNum
    
        
    TradeContext.PROJECTID = ''
    TradeContext.TAXTYPENAME = ''
    TradeContext.TAXTYPECODE = ''
    TradeContext.TAXSTARTDATE = ''
    TradeContext.TAXENDDATE = ''
    TradeContext.TAXTYPE = ''
    TradeContext.DETAILNUM2 = ''
    
    TradeContext.PROJECTID = StrAdd(Party3Context.projectId)
    TradeContext.TAXTYPENAME = StrAdd(Party3Context.taxTypeName)
    TradeContext.TAXTYPECODE = StrAdd(Party3Context.taxTypeCode)
    TradeContext.TAXSTARTDATE = StrAdd(Party3Context.taxStartDate)
    TradeContext.TAXENDDATE = StrAdd(Party3Context.taxEndDate)
    TradeContext.TAXTYPE = StrAdd(Party3Context.taxType)
    TradeContext.DETAILNUM2 = StrAdd(Party3Context.detailNum2)
    
    TradeContext.detailNo = ''
    TradeContext.taxSubjectCode = ''
    TradeContext.taxNumber = ''
    TradeContext.taxAmt = ''
    TradeContext.factTaxAmt = ''
    
    TradeContext.detailNo = StrAdd(Party3Context.detailNo)
    TradeContext.taxSubjectCode = StrAdd(Party3Context.taxSubjectCode)
    TradeContext.taxNumber = StrAdd(Party3Context.taxNumber)
    TradeContext.taxAmt = StrAdd(Party3Context.taxAmt)
    TradeContext.factTaxAmt = StrAdd(Party3Context.factTaxAmt)
    
    TradeContext.TAXSUBJECTLIST1009 = TradeContext.detailNo + '^' + TradeContext.taxSubjectCode + '^' + TradeContext.taxNumber + '^' + TradeContext.taxAmt + '^' + TradeContext.factTaxAmt
    
    return True
 
def SubModuleMainSnd ():
    return True
