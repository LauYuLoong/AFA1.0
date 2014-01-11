# -*- coding: gbk -*-
##################################################################

#   中间业务平台.
#=================================================================
#   程序文件:   TYBT010_8621.py
#   程序说明:   [单证重打联动子查询]
#   修改时间:   2010-08-11
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    
    
    AfaLoggerFunc.tradeInfo( '单证重打查询变量值的有效性校验' )
    
    if( not TradeContext.existVariable( "unitno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '单位编号[unitno]值不存在!' )
    
    if( not TradeContext.existVariable( "policy" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '投保单号[policy]值不存在!' )
    
    if( not TradeContext.existVariable( "userno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '原保单印刷号[userno]值不存在!' )
    
    if( not TradeContext.existVariable( "userno1" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '新保单印刷号[userno1]值不存在!' )    
    
    if( not TradeContext.existVariable( "transrno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '原交易流水号[transrno]值不存在!' ) 
    
    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '原交易金额[amount]值不存在!' )  
   
    if( not TradeContext.existVariable( "I1CETY" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '原保单凭证[I1CETY]值不存在!' )  
           
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '渠道代码[channelCode]值不存在!' )
    
    if( TradeContext.channelCode == '005' ):
        
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '柜员号[tellerno]值不存在!' )
        
        if( not TradeContext.existVariable( "brno" ) ): 
            return AfaFlowControl.ExitThisFlow( 'A0001', '网点号[brno]值不存在!' )
        
        if( not TradeContext.existVariable( "termId" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '终端号[termId]值不存在!' )
   
    return True

def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('单证重打子查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']进入' )
    
    try:
        sql = "select unitno,amount,userno,note4,note5,note8,note9,note10,craccno,note7 from afa_maintransdtl"
        sql = sql + " where agentserialno = '" + TradeContext.transrno.strip() + "'"
        sql = sql + " and   workdate      = '" + TradeContext.workDate.strip() + "'"
        sql = sql + " and   bankstatus    = '0' and corpstatus = '0' and revtranf = '0'"
        
        AfaLoggerFunc.tradeInfo('单证重打信息查询语句'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        if records == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询银保通数据库失败"
            raise AfaFlowControl.flowException( )
        
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此缴费信息"
            return False
        
        else:
            if(records[0][0]!=TradeContext.unitno):
                TradeContext.errorCode,TradeContext.errorMsg='E9999',"单位编号不符"
                return False
            
            if(records[0][1].split()!=TradeContext.amount.split()):
                TradeContext.errorCode,TradeContext.errorMsg='E9999',"与原交易金额不符"
                return False
            
            if(records[0][2]!=TradeContext.userno):
                TradeContext.errorCode,TradeContext.errorMsg='E9999',"与原保单印刷号不符"
                return False
           
            note9=records[0][6].split('|')
            AfaLoggerFunc.tradeInfo(note9[2] + "||"+TradeContext.policy)
            if(note9[2]!=TradeContext.policy):
                TradeContext.errorCode,TradeContext.errorMsg='E9999',"与原保险单号不符"  
                return False
            
            #note9保险单号
            TradeContext.policy=note9[2]
            
            #note8主险险种和附加险种      
            note8= records[0][5].split('|') 
            TradeContext.productid=note8[0]
            TradeContext.productid1=note8[2] 
            
            #note4:投保人姓名|投保人证件号码|与投保人关系        
            note4= records[0][3].split('|') 
            TradeContext.tbr_name=note4[0]
            TradeContext.tbr_idno=note4[1]
            TradeContext.tbr_bbr_rela=note4[2] 
          
            #note5:被保人姓名|被保人证件号码|与被保险人关系 
            note5= records[0][4].split('|') 
            TradeContext.bbr_name=note5[0]
            TradeContext.bbr_idno=note5[1]
            TradeContext.syr_bbr_rela=note5[2] 
            TradeContext.payacc=records[0][8] 

            #note7:交费方式|缴费期次|交费期间
            TradeContext.paymethod = records[0][9].split('|')[0]
            
        #查询受益人信息
        sql = "select syr_info1,syr_info2,syr_info3,syr_info4,syr_info5 from ybt_info"
        sql = sql + " where submino  = '" + note9[1]                    + "'"            #投保单号
        sql = sql + " and   cpicno   = '" + TradeContext.unitno         + "'"            #保险公司代码
        sql = sql + " and   workdate = '" + TradeContext.workDate       + "'"            #交易日期
        sql = sql + " and   tellerno = '" + TradeContext.tellerno       + "'"            #交易柜员
        
        AfaLoggerFunc.tradeInfo('查询受益人信息：'+ sql)
        
        results = AfaDBFunc.SelectSql( sql )
        
        if results == None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询受益人信息异常"
            return False
        
        if(len(results) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","没有找到相关的受益人信息"
            return False
            
        else:
            TradeContext.syr_1 = results[0][0]                        #受益人1信息
            TradeContext.syr_2 = results[0][1]                        #受益人2信息
            TradeContext.syr_3 = results[0][2]                        #受益人3信息
            TradeContext.syr_4 = results[0][3]                        #受益人4信息
            TradeContext.syr_5 = results[0][4]                        #受益人5信息
            
        TradeContext.errorCode = '0000'
        AfaLoggerFunc.tradeInfo('单证重打子查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']退出' )
        return True
    
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
