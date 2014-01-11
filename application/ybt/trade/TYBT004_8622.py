# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TYBT004_8622.py
#   程序说明:   撤销子查询
#   修改时间:   2010-8-10
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaAhAdb
import AfaHostFunc,AfaDBFunc
from types import *

def SubModuleDoFst( ):
     
    AfaLoggerFunc.tradeInfo( '反交易变量值的有效性校验' )
   
    #交易代码
    TradeContext.tradeCode = TradeContext.TransCode
    
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
    
   
def SubModuleDoSnd( ):
   
    AfaLoggerFunc.tradeInfo('进入反查询交易[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' ) 
    
    try:
        sql = "select note1,note2,note3,note4,note5,note7,note8,note9,draccno,brno,tellerno,note6,unitno,amount,note9 from afa_maintransdtl "
        sql = sql + " where agentserialno = '"+TradeContext.PreSerialno+"' and workdate = '"+TradeContext.workDate+"'"
        sql = sql + " and revtranf = '0' and bankstatus = '0'  and chkflag = '9'"
        
        AfaLoggerFunc.tradeInfo('撤销子查询语句'+ sql)
        
        records = AfaDBFunc.SelectSql( sql )
        
        AfaLoggerFunc.tradeInfo('撤销子查询语句记录'+str(records))
        
        if records==None:
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询银保通数据库失败"
            raise AfaFlowControl.flowException( )
        
        elif(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","无此交易"
            return False
      
        else:
        
            if(records[0][10] != TradeContext.tellerno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本柜员所做，不能做此交易"
                return False
        
            if(records[0][9] != TradeContext.brno):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","原交易非本网点所做，不能做此交易"
                return False
            
            if(records[0][12].strip() != TradeContext.insuid):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","保险公司选择有误"
                return False
            
            if(records[0][13].strip() != TradeContext.amount.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","输入金额与原金额不符，请检查金额录入项"
                return False
            
            if(records[0][14].split('|')[2] != TradeContext.policy.strip()):
                TradeContext.errorCode,TradeContext.errorMsg = "0001","与原保单号不符，请检查保单号录入项"
                return False
            
            #投保人姓名
            TradeContext.tbr_name=records[0][3].split('|')[0]
            
            #投保人证件号
            TradeContext.tbr_idno=records[0][3].split('|')[1]
            
            #被保险人姓名
            TradeContext.bbr_name=records[0][4].split('|')[0]
            
            #被保险人证件号
            TradeContext.bbr_idno=records[0][4].split('|')[1]
            
            #主险险种
            TradeContext.productid=records[0][6].split('|')[0]
            
            #附加险险种
            TradeContext.productid1=records[0][6].split('|')[2]
            
            #投保份数
            TradeContext.amt_unit =records[0][7].split('|')[0]
            
            #账号
            TradeContext.payacc=records[0][8]
            
            #退款方式
            TradeContext.paymethod1=records[0][11].split('|')[1]
            
            #缴费年限
            TradeContext.paytimelimit=records[0][5].split('|')[2]
            
            #缴费方式
            TradeContext.paymethod=records[0][5].split('|')[0]
            
            #缴费期次
            TradeContext.rev_frequ=records[0][5].split('|')[1]
            
            #受益人1信息
            TradeContext.syr_1=""
            #受益人2信息
            TradeContext.syr_2=""
            #受益人3信息
            TradeContext.syr_3=""
            #受益人4信息
            TradeContext.syr_4=""
            #受益人5信息
            TradeContext.syr_5=""
            
            TradeContext.errorCode= "0000" 
            
            AfaLoggerFunc.tradeInfo('退出反查询交易' )
            return True                               
    except Exception, e:                          
        AfaFlowControl.exitMainFlow(str(e))       
