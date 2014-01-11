# -*- coding: gbk -*-
##################################################################
#   中间业务平台.凤台财政-待查询账户维护
#=================================================================
#   程序文件:   TFTCZ001_8656.py
#   程序说明:   查询账户维护
#   作者:       陈浩
#   修改时间:   2012—09-17
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    try:
        #财政帐号
        if not( TradeContext.existVariable( "CzAccNo" ) and len(TradeContext.CzAccNo.strip()) > 0):     
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "财政帐号不存在"                  
            raise AfaFlowControl.flowException( ) 
            
        #帐号开户机构
        if not( TradeContext.existVariable( "OpBkCode" ) and len(TradeContext.OpBkCode.strip()) > 0):     
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "帐号开户机构不存在"                  
            raise AfaFlowControl.flowException( )    
            
            
        #判断此帐户信息是否存在
        sqlstr = ""
        sqlstr = sqlstr + " select accno,sbno,status from FT_CZZH where "
        sqlstr = sqlstr + " accno = '" + TradeContext.CzAccNo.strip()  + "' and"
        sqlstr = sqlstr + " sbno  = '" + TradeContext.OpBkCode.strip() + "' "
        
        #sqlstr = sqlstr + " sbno  = '" + TradeContext.OpBkCode.strip() + "' and"
        #sqlstr = sqlstr + " status= '1' "
        
        AfaLoggerFunc.tradeInfo("===查询结果："+sqlstr)                                                                                                                         
                                                                                                                                                         
        result = AfaDBFunc.SelectSql(sqlstr)                                                                                                              
                                                                                                                                                         
        if (result == None):                                                                                                                                 
            AfaLoggerFunc.tradeInfo('>>>处理结果查询失败,数据库异常')
            TradeContext.errorCode,TradeContext.errorMsg = 'E8888', "处理结果查询失败,数据库异常"                  
            raise AfaFlowControl.flowException( )                                      
                                                             
        #判断操作类型 0--新增，1--删除
        if TradeContext.OptType == '0':
            AfaLoggerFunc.tradeInfo("===帐户操作类型：新增")
            
            if (len(result) > 0): 
                if result[0][2] == '0':
                    AfaLoggerFunc.tradeInfo( "===存在帐户状态为0(已删除)的帐户信息，可更改状态为新增" )
                    sqld = ""
                    sqld = sqld + " update  FT_CZZH set status = '1', "
                    sqld = sqld + " note1 = '"+ TradeContext.workDate.strip() +"' where "      #操作日期
                    sqld = sqld + " accno = '"+ TradeContext.CzAccNo.strip()  +"' and "
                    sqld = sqld + " sbno  = '"+ TradeContext.OpBkCode.strip() +"' and "
                    sqld = sqld + " status= '0' "
                
                    AfaLoggerFunc.tradeInfo("==(新增)更新表信息："+sqld)

                    results = AfaDBFunc.UpdateSqlCmt( sqld )
                    if( results <= 0 ):
                        AfaLoggerFunc.tradeFatal( "===(新增)更新表失败："+AfaDBFunc.sqlErrMsg )
                        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "(新增)更新表失败："                 
                        raise AfaFlowControl.flowException( ) 
             
                    AfaLoggerFunc.tradeInfo("===帐户新增(更新)操作流程结束")
                    
                else:
                    AfaLoggerFunc.tradeFatal( "===已存在相应帐号信息不能重复新增,请核对信息" )
                    TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "已存在相应帐号信息不能重复新增,请核对信息"                 
                    raise AfaFlowControl.flowException( )
            
            if (len(result) == 0):                                                                                                                                                                          
                AfaLoggerFunc.tradeInfo( "===无帐户相应数据,可新增信息" )
                sql = ""
                sql = sql + " insert into FT_CZZH values( "
                sql = sql + " '"+ TradeContext.CzAccNo.strip()  +"', "
                sql = sql + " '"+ TradeContext.OpBkCode.strip() +"', "
                sql = sql + " '1', "
                sql = sql + " '"+ TradeContext.workDate.strip() +"', "      #note1 存在操作日期
                sql = sql + " '', "
                sql = sql + " '', "
                sql = sql + " '', "
                sql = sql + " '') "
                
                AfaLoggerFunc.tradeInfo("==插入表信息："+sql)

                results = AfaDBFunc.InsertSqlCmt( sql )
                if( results <= 0 ):
                    AfaLoggerFunc.tradeFatal( "===插入表失败："+AfaDBFunc.sqlErrMsg )
                    TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "插入表失败："                 
                    raise AfaFlowControl.flowException( ) 
        
                AfaLoggerFunc.tradeInfo("===帐户新增操作流程结束")
        
        if TradeContext.OptType == '1':
            AfaLoggerFunc.tradeInfo("===帐户操作类型：删除")
            
            if (len(result) == 0): 
                AfaLoggerFunc.tradeFatal( "===不存在相应帐号信息不能删除,请核对信息" )
                TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "不存在相应帐号信息不能删除,请核对信息"                 
                raise AfaFlowControl.flowException( )
            
            if (len(result) > 0):
                if result[0][2] == '1':                                                                                                                                                                      
                    AfaLoggerFunc.tradeInfo( "===存在帐户相应数据,可删除信息" )
                    sqld = ""
                    sqld = sqld + " update  FT_CZZH set status = '0', "
                    sqld = sqld + " note1 = '"+ TradeContext.workDate.strip() +"' where "      #操作日期
                    sqld = sqld + " accno = '"+ TradeContext.CzAccNo.strip()  +"' and "
                    sqld = sqld + " sbno  = '"+ TradeContext.OpBkCode.strip() +"' and "
                    sqld = sqld + " status= '1' "
                    
                    AfaLoggerFunc.tradeInfo("==(删除)更新表信息："+sqld)
                    
                    results = AfaDBFunc.UpdateSqlCmt( sqld )
                    if( results <= 0 ):
                        AfaLoggerFunc.tradeFatal( "===(删除)更新表失败："+AfaDBFunc.sqlErrMsg )
                        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "(删除)更新表失败："                 
                        raise AfaFlowControl.flowException( ) 
                    
                    AfaLoggerFunc.tradeInfo("===帐户删除操作流程结束")
                    
                else:
                    AfaLoggerFunc.tradeFatal( "===相应帐号信息已被删除，不能重复删除,请核对信息" )
                    TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "相应帐号信息已被删除，不能重复删除,请核对信息"                 
                    raise AfaFlowControl.flowException( )
                
        TradeContext.errorCode  =   "0000"
        TradeContext.errorMsg   =   "交易成功"
        return True
        
    except  Exception, e:                	   
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )  
                        
