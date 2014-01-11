# -*- coding: gbk -*-
##################################################################

#   中间业务平台.
#=================================================================
#   程序文件:   TYBT004_8620.py
#   程序说明:   [根据保单号查询缴费信息,新保缴费联动交易]
#   修改时间:   2010-08-11
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    
   
    AfaLoggerFunc.tradeInfo( '缴费信息查询变量值的有效性校验' )
    
    if( not TradeContext.existVariable( "unitno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '单位编号[unitno]值不存在!' )
       
    if( not TradeContext.existVariable( "applno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '投保单号[applno]值不存在!' )
   
    if( not TradeContext.existVariable( "userno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '保单印刷号[userno]值不存在!' )   
    
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
    AfaLoggerFunc.tradeInfo('新保缴费信息查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
   
    try:
        sql = "select agentserialno,amount,payouttype,payoutdur,tbr_name,tbr_idno,bbr_name,bbr_idno,tbr_bbr_rela,"
        sql = sql + " tellerno,xzinfo,syr_info1,syr_info2,syr_info3,syr_info4,syr_info5 from ybt_info"
        sql = sql + " where printno  = '" + TradeContext.userno.strip() + "'"
        sql = sql + " and   submino  = '" + TradeContext.applno.strip() + "'"
        sql = sql + " and   cpicno   = '" + TradeContext.unitno         + "'"
        sql = sql + " and   workdate = '" + TradeContext.workDate       + "'"
        sql = sql + " and   tellerno = '" + TradeContext.tellerno       + "'"
        
        AfaLoggerFunc.tradeInfo('缴费信息查询语句'+ sql)
       
        records = AfaDBFunc.SelectSql( sql )
       
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询YBT_INFO 表失败"
            raise AfaFlowControl.flowException( )
            
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此投保信息"
            return False
        
        else:
            #交易流水号
            TradeContext.transrno = records[0][0]
           
            #应缴保费
            TradeContext.amount = records[0][1]
            
            #缴费方式
            TradeContext.paymethod = records[0][2]
            
            #缴费年限
            TradeContext.paydatelimit = records[0][3]
            
            # 投保人姓名
            TradeContext.tbr_name = records[0][4]
           
            #投保人身份证号码
            TradeContext.tbr_idno= records[0][5]
            
            #被保人姓名
            TradeContext.bbr_name = records[0][6]
            
            #被保人身份证号码
            TradeContext.bbr_idno = records[0][7]
           
            #与投保人关系
            TradeContext.tbr_bbr_rela = records[0][8]
            
            #行所营销人员工号
            TradeContext.salerno = records[0][9]
            
            #主险险种和附加险种
            list=records[0][10].split('|')        
            TradeContext.productid=list[0]
            TradeContext.productid1=list[1]
            
            #受益人信息
            TradeContext.syr_1 = records[0][11]
            TradeContext.syr_2 = records[0][12]
            TradeContext.syr_3 = records[0][13]
            TradeContext.syr_4 = records[0][14]
            TradeContext.syr_5 = records[0][15]
            
            TradeContext.errorCode = '0000'
        
        AfaLoggerFunc.tradeInfo('退出新保缴费信息查询交易' )
        return True
   
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
