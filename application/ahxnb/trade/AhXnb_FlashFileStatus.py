# -*- coding: gbk -*-
###############################################################################
# 文件名称：AhXnb_FlashFileStatus.py
# 文件标识：
# 作    者：胡友
# 摘    要：依据批量撤销信息实时更新新农保撤销信息
###############################################################################
import TradeContext

TradeContext.sysType = 'ahxnb'     
                                   
import AfaDBFunc,AfaUtilTools,AfaLoggerFunc,sys
from types import *

#######################################主函数###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************批量撤销信息实时更新到新农保撤销信息开始********************')
    
    try:
        #=====================获取系统日期时间==================================
        TradeContext.WorkDate=AfaUtilTools.GetSysDate( )
        TradeContext.WorkTime=AfaUtilTools.GetSysTime( )
        
        sql = ""
        sql = sql + "select BATCHNO,APPNO,BUSINO,PROCMSG,STATUS"
        sql = sql + " from abdt_batchInfo"
        sql = sql + " where INDATE = '"+ TradeContext.WorkDate +"'"   #申请日期
        sql = sql + " and STATUS = '40'"                              #文件状态
        sql = sql + " and note5 <> '1'"                               #更新状态
        
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql( sql ) 
        
        if records==None:
            AfaLoggerFunc.tradeInfo('查询abdt_batchInfo失败')
            TradeContext.errorCode,TradeContext.errorMsg = 'D001','查询abdt_batchInfo失败'
            sys.exit(-1)
            
        elif(len(records) == 0):
            AfaLoggerFunc.tradeInfo('查询abdt_batchInfo无此信息')
            TradeContext.errorCode,TradeContext.errorMsg = 'D001','查询abdt_batchInfo无此信息'
            sys.exit(-1)
            
        else:
            for i in range(0,len(records)):
                sql = ""
                sql = sql + "select STATUS"
                sql = sql + " from ahnx_file"
                sql = sql + " where APPNO = '"+ records[i][1] +"'"  #业务编号
                sql = sql + " and BUSINO = '"+ records[i][2] +"'"   #单位编号
                sql = sql + " and BATCHNO = '"+ records[i][0] +"'"  #批次号
                
                AfaLoggerFunc.tradeInfo(sql)
                record = AfaDBFunc.SelectSql( sql )
                
                if record==None:
                    AfaLoggerFunc.tradeInfo('查询ahnx_file失败')
                    TradeContext.errorCode,TradeContext.errorMsg = 'D001','查询ahnx_file失败'
                    sys.exit(-1)
                    
                elif(len(record) == 0):
                    AfaLoggerFunc.tradeInfo('查询ahnx_file无此信息')
                    #TradeContext.errorCode,TradeContext.errorMsg = 'D001','查询ahnx_file无此信息'
                    #sys.exit(-1)
                    continue
 
                else:
                    if( record[0][0].strip() != '2' and record[0][0].strip() != '0' and record[0][0].strip() != '1' ):
                        try:
                            sql = ""
                            sql = sql + "update ahnx_file set"
                            sql = sql + " STATUS = '2',"
                            sql = sql + " PROCMSG = '批量已撤销,原因为"+ records[i][3][0:32] +"'"
                            sql = sql + " where APPNO = '"+ records[i][1] +"'"  #业务编号
                            sql = sql + " and BUSINO = '"+ records[i][2] +"'"   #单位编号
                            sql = sql + " and BATCHNO = '"+ records[i][0] +"'"  #批次号
                            
                            AfaLoggerFunc.tradeInfo(sql)
                            result = AfaDBFunc.UpdateSql( sql ) 
                            
                            if( result <0 ):
                                AfaLoggerFunc.tradeInfo('更新ahnx_file表失败，批次号为：'+records[i][0])
                                continue
                                
                            sql = ""
                            sql = sql + "update abdt_batchInfo set"
                            sql = sql + " note5 = '1'"
                            sql = sql + " where APPNO = '"+ records[i][1] +"'"  #业务编号
                            sql = sql + " and BUSINO = '"+ records[i][2] +"'"   #单位编号
                            sql = sql + " and BATCHNO = '"+ records[i][0] +"'"  #批次号
                            
                            AfaLoggerFunc.tradeInfo(sql)
                            result = AfaDBFunc.UpdateSql( sql ) 
                            
                            if( result <0 ):
                                AfaLoggerFunc.tradeInfo('更新abdt_batchInfo表失败，批次号为：'+records[i][0])
                                continue
                            
                            #事务提交
                            if not AfaDBFunc.CommitSql( ):
                                AfaLoggerFunc.tradeInfo('事务提交失败')
                                sys.exit(-1)
                            AfaLoggerFunc.tradeInfo('事务提交成功')

                        except Exception, e:
                            AfaLoggerFunc.tradeInfo( str(e) )

                            #事务回滚
                            if not AfaDBFunc.RollbackSql( ):
                                AfaLoggerFunc.tradeInfo('事务回滚失败')
                                sys.exit(-1)
                            AfaLoggerFunc.tradeInfo('事务回滚成功')
  
                    else:
                        AfaLoggerFunc.tradeInfo('该批次已撤销或状态不符，不能撤销')
                
            AfaLoggerFunc.tradeInfo('共有'+ str(i+1) +'条记录')
        sys.exit(0)
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        sys.exit(-1)
