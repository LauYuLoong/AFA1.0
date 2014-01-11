# -*- coding: gbk -*-
##################################################################
#   中间业务平台.
#=================================================================
#   程序文件:   TTJYW001_8495.py
#   程序说明:   统缴业务缴费交易
#   修改时间:   2011-01-05
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc,AfaFlowControl,HostContext,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    try:
        AfaLoggerFunc.tradeInfo( '>>>>>>>>>>>>>>初始化统缴业务的交易变量开始' )
        
        #缴费人姓名
        if not( TradeContext.existVariable( "userName" ) and len(TradeContext.userName.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费人姓名不存在"
            raise AfaFlowControl.flowException( )
       
        #联系电话
        if not( TradeContext.existVariable( "note1" ) and len(TradeContext.note1.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "联系电话不存在"
            raise AfaFlowControl.flowException( )   
        
        #交易机构名称                                                                                 
        if not( TradeContext.existVariable( "note3" ) and len(TradeContext.note3.strip()) > 0 ):   
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "交易机构名称不存在"               
            raise AfaFlowControl.flowException( )                                                 
            
        #缴费方式
        if not( TradeContext.existVariable( "paymethod" ) and len(TradeContext.paymethod.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "缴费方式不存在"
            raise AfaFlowControl.flowException( )   
            
        #20120709陈浩添加 单位编码 busino    
        #单位编码
        if not( TradeContext.existVariable( "busino" ) and len(TradeContext.busino.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "单位编码不存在"
            raise AfaFlowControl.flowException( )               
            
        TradeContext.note2   =   TradeContext.busino      #将busino放在note2 中
            
        
        #paymethod1付费方式(0现金，1转账)  accType缴费介质代码（000:现金，001：对私账号，002：借记卡，
        #003：贷记卡，004：对公账号，005：公务卡）  paycard卡号
        TradeContext.accType = ''
        
        if TradeContext.paymethod=="0":
            TradeContext.accType="000"
        else:
            TradeContext.vouhType = "81"                            #vouhType 81：金农借记卡
            TradeContext.accType="002"
            TradeContext.accno = TradeContext.paycard               #卡号
            TradeContext.accPwd = TradeContext.password
            TradeContext.vouhNo=TradeContext.paycard[8:18]
        
        #20120706陈浩修改，返回收款人修改为帐户名称
        #begin   
        #sql = "select unitname from afa_unitadm"              
        #sql = sql + " where sysid     = '" + TradeContext.sysId.strip() + "'"
        #sql = sql + " and   unitno    = '" + TradeContext.unitno.strip() + "'"     
        #                                                                            
        #AfaLoggerFunc.tradeInfo('收款人信息查询语句'+ sql)                          
        #                                                                            
        #records = AfaDBFunc.SelectSql( sql )                                        
        #if records == None:                                                         
        #    TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询数据库失败" 
        #    raise AfaFlowControl.flowException( )                                   
        #                                                                            
        #if(len(records) < 1):                                                       
        #    TradeContext.errorCode,TradeContext.errorMsg = "0001","无此信息"        
        #    raise AfaFlowControl.flowException( )                                                             
        #                                                                            
        #else:                                                                       
        #    TradeContext.unitname = records[0][0]             #收款人  
        
        sql = ""
        sql = sql + " select businame,accno from abdt_unitinfo "
        sql = sql + " where appno = '" + TradeContext.sysId.strip()  + "' "
        sql = sql + " and  busino = '" + TradeContext.busino.strip() + "' "
        
        AfaLoggerFunc.tradeInfo('收款人帐户名称信息查询语句'+ sql)                          
                                                                                    
        records = AfaDBFunc.SelectSql( sql )                                        
        if records == None:                                                         
            TradeContext.errorCode,TradeContext.errorMsg = "0001" ,"查询数据库失败" 
            raise AfaFlowControl.flowException( )                                   
                                                                                    
        if(len(records) < 1):                                                       
            TradeContext.errorCode,TradeContext.errorMsg = "0001","该单位没有签约，不能做次业务！"        
            raise AfaFlowControl.flowException( )                                                             
                                                                                    
        else:                                                                       
            TradeContext.businame       = records[0][0]             #收款人帐户名称 
            TradeContext.ACCNO          = records[0][1]             #收款人帐号
                       
            TradeContext.__agentAccno__ = records[0][1]             #帐号
            AfaLoggerFunc.tradeInfo('收款人帐户__agentAccno__ AA：：'+ TradeContext.__agentAccno__) 
        
        #end
                    
        AfaLoggerFunc.tradeInfo( '>>>>>>>>>>>初始化统缴业务的交易变量结束' )
        return True
    except  Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
    
    

