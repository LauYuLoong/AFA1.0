# -*- coding: gbk -*-
###############################################################################
# 文件名称：T001000_8623.py
# 文件标识：批量签约
# 作    者：陈浩  
# 修改时间：2011-07-27
# 摘    要：批量签约 导入 
#
###############################################################################
import ConfigParser, AfaUtilTools, sys, AfaDBFunc,AfaLoggerFunc,AhXnbFunc,TradeContext,AfaFunc,AfaFlowControl,AfaFunc
import os
from types import *

def TrxMain():

    AfaLoggerFunc.tradeInfo('**********批量签约记录文件名(8623)开始**********' )
    
    try:
        
        AfaLoggerFunc.tradeInfo( '初始化导入交易变量' )
        
        #判断单位批量签约是否有权限
        if ( not ChkUnitLimit( )):
            return False        
              
        #是否本机构
        if (TradeContext.I1BUSINO[:10] != TradeContext.I1SBNO):
            TradeContext.errorCode,TradeContext.errorMsg = "E8623" , "非本机构，不能做此交易!"  
            raise AfaFlowControl.flowException( )                
              
        
        #文件名称
        if not( TradeContext.existVariable( "I1FILENAME" ) and len(TradeContext.I1FILENAME.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = "E8623","不存在此文件名!"
            raise AfaFlowControl.flowException( )
        
        #单位编号
        if not( TradeContext.existVariable( "I1BUSINO" ) and len(TradeContext.I1BUSINO.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E8623', "不存在此单位编号"
            raise AfaFlowControl.flowException( )      
        
        #生成委托号
        if ( not CrtBatchNo( ) ):
            return False
        
        AfaLoggerFunc.tradeInfo('**********批量签约导入开始**********' )
        
        #判断该单位是否签约
        sql = ""
        sql = sql + " select  * FROM ABDT_UNITINFO "
        sql = sql + " where BUSINO = '" + TradeContext.I1BUSINO + "' "
        sql = sql + " and APPNO  = '"+ TradeContext.sysId +"'"
        sql = sql + " and STATUS = '1' "
        sql = sql + " and AGENTTYPE = '3'"
                   
        AfaLoggerFunc.tradeInfo( '查询数据库sql：' +sql )
        
        recs = AfaDBFunc.SelectSql( sql )
        if recs == None :
            TradeContext.errorCode,TradeContext.errorMsg = "E8623","查询数据库异常!"
            raise AfaFlowControl.flowException( )
            
        elif(len(recs)==0):
            TradeContext.errorCode,TradeContext.errorMsg = "9999" , "该单位没有签约,不能做此交易!"
            raise AfaFlowControl.flowException( ) 
        
                
        #判断文件是否已经导入
        sql = ""
        sql = sql + " select  * FROM AHNX_FILE "
        sql = sql + " where busino = '" + TradeContext.I1BUSINO + "' "
        sql = sql + " and appno  = '"+ TradeContext.sysId +"'"
        sql = sql + " and filetype = '7' "
                   
        AfaLoggerFunc.tradeInfo( '查询数据库sql：' +sql )
        
        rec = AfaDBFunc.SelectSql( sql )
        if rec == None :
            TradeContext.errorCode,TradeContext.errorMsg = "E8623","查询数据库异常!"
            raise AfaFlowControl.flowException( )
            
        if len(rec) > 0:
            for i in range(0,len(rec)):
                if (rec[i][1] == TradeContext.I1FILENAME):        
                    TradeContext.errorCode,TradeContext.errorMsg = "E8623","数据库中已存在此文件，请核对后再导入!"
                    raise AfaFlowControl.flowException( )        
        
        AfaLoggerFunc.tradeInfo( '>>>导入批量签约文件' )             
        #将文件名保存到 AHNX_FILE 中     
        
        sql = ""
        sql = sql + "insert into AHNX_FILE("
        sql = sql + "BATCHNO,"
        sql = sql + "FILENAME,"
        sql = sql + "WORKDATE,"
        sql = sql + "STATUS,"
        sql = sql + "PROCMSG,"
        sql = sql + "APPLYDATE,"
        sql = sql + "APPNO,"
        sql = sql + "BUSINO,"
        sql = sql + "TOTALNUM,"
        sql = sql + "TOTALAMT,"
        sql = sql + "FILETYPE,"
        sql = sql + "BRNO,"
        sql = sql + "TELLERNO,"
        sql = sql + "BEGINDATE,"
        sql = sql + "ENDDATE,"
        sql = sql + "WORKTIME,"
        sql = sql + "NOTE1,"
        sql = sql + "NOTE2,"
        sql = sql + "NOTE3,"
        sql = sql + "NOTE4)"
        sql = sql + " values("
        sql = sql + "'" + TradeContext.BATCHNO     + "',"             #登记流水号
        sql = sql + "'" + TradeContext.I1FILENAME  + "',"             #文件名
        sql = sql + "'" + TradeContext.TranDate    + "',"             #登记日期
        sql = sql + "'0',"                                            #状态(0-待处理，1-处理成功)
        sql = sql + "'批量文件等待处理中...',"                        #处理信息描述
        sql = sql + "'" + TradeContext.TranDate    + "',"             #申请日期
        sql = sql + "'" + TradeContext.sysId       + "',"             #业务编号
        sql = sql + "'" + TradeContext.I1BUSINO    + "',"             #单位编号
        sql = sql + "'0',"                                            #总笔数
        sql = sql + "'0.00',"                                         #总金额
        sql = sql + "'7',"                                            #文件类型（0-批量代发，1-批量代扣，2-批量开户，7--批量签约)
        sql = sql + "'" + TradeContext.I1SBNO      + "',"             #机构号
        sql = sql + "'" + TradeContext.I1USID      + "',"             #柜员号
        sql = sql + "'20110101',"                                     #生效日期
        sql = sql + "'20990101',"                                     #失效日期
        sql = sql + "'" + TradeContext.TranTime    + "',"             #申请时间
        sql = sql + "'',"                                             #备用1
        sql = sql + "'',"                                             #备用2
        sql = sql + "'',"                                             #备用3
        sql = sql + "'')"                                             #备用4
        
        AfaLoggerFunc.tradeInfo( "批量文件记录：" + sql )
        
        ret = AfaDBFunc.InsertSqlCmt(sql)
        
        if ret < 0:
            TradeContext.errorCode,TradeContext.errorMsg = "E8623","插入数据失败!"
            raise AfaFlowControl.flowException( )              
                   
        TradeContext.FileName =  TradeContext.sysId + TradeContext.I1BUSINO[6:] + TradeContext.TranDate + TradeContext.I1FILENAME[-7:-4]+"_WF.TXT"
        
        TradeContext.errorCode,TradeContext.errorMsg ="0000","交易成功"
        
        AfaLoggerFunc.tradeInfo('**********批量签约导入结束**********' )    
        return True
              
           
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )   

##########################################################################################        
#生成委托号
##########################################################################################
def CrtBatchNo( ):

    AfaLoggerFunc.tradeInfo('>>>生成批次委托号')

    try:
        sqlStr = "SELECT NEXTVAL FOR ABDT_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            TradeContext.errorCode, TradeContext.errorMsg='E8623', "生成委托号异常"
            raise AfaFlowControl.flowException( )

        #批次号
        TradeContext.BATCHNO = TradeContext.TranDate + str(records[0][0]).rjust(8, '0')

        return True

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )  
        
########################################################################################## 
# 判断该单位是否有批量签约的权限 0--无权限 1--有权限
##########################################################################################
def ChkUnitLimit( ):

    try:
        AfaLoggerFunc.tradeInfo('>>>判断该单位是否有批量签约的权限')
        sql = ""
        sql = "SELECT FLAG FROM ABDT_QYFLAG WHERE "
        sql = sql + " SYSID = '" + TradeContext.sysId + "'" 
        sql = sql + " AND STATUS = '1'"
        
        records = AfaDBFunc.SelectSql( sql )
        AfaLoggerFunc.tradeInfo('查询数据库 sql: ' +sql)
        
        if(records==None):
            TradeContext.errorCode,TradeContext.errorMsg = "9999" , "查询ABDT_QYFLAG数据库异常!"
            raise AfaFlowControl.flowException( ) 
                      
        elif(len(records)==0):
            TradeContext.errorCode,TradeContext.errorMsg = "9999" , "无该单位签约权限信息!"
            raise AfaFlowControl.flowException( ) 

        else:
            if (records[0][0]=='0'):
                TradeContext.errorCode,TradeContext.errorMsg = "9999" , "该单位无签约权限!"
                raise AfaFlowControl.flowException( ) 
                
            if (records[0][0]=='1'):
                AfaLoggerFunc.tradeInfo('>>>该单位有签约权限')
                return True 
                         
        return True
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )       
