# -*- coding: gbk -*-
###############################################################################
# 文件名称：AbdtQyOut.py
# 文件标识：
# 作    者：陈浩  
# 修改时间：2011-07-27
# 摘    要：批量签约 定时调度 导出
#
###############################################################################   
 
import TradeContext                
                                   
TradeContext.sysType = 'abdt' 
                                   
import time ,TradeContext ,AfaDBFunc,os,sys,TradeContext,AfaUtilTools,AbdtManager,AfaLoggerFunc,AfaFlowControl,AfaAdminFunc,sys,AfaFunc
from types import *

def AbdtQyOut():

    AfaLoggerFunc.tradeInfo('**********批量签约定时调度导出 进入**********')
                 
    try: 
                       
        AfaLoggerFunc.tradeInfo('**********批量签约导出开始**********' )                                                  
        AfaLoggerFunc.tradeInfo('**********导出批量文件**********')  
                               
        sql = ""       
        sql = "SELECT FILENAME,APPNO,BUSINO,WORKDATE,TELLERNO,BATCHNO FROM AHNX_FILE WHERE "
        sql = sql + "FILETYPE="    + "'7'" + " AND "        #7-批量签约
        sql = sql + "STATUS="   + "'1'"                     #已处理
       
        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql(sql)
        if records == None:
            return ExitSubTrade("E9999" ,"查询AHNX_FILE数据库异常")
             
        elif(len(records)==0):
            return ExitSubTrade("E9999" ,"数据库AHNX_FILE中没有要读取的文件！")
            
        else:            
            for i in range(0,len(records)):
            
                TradeContext.prefileName = records[i][0]
                TradeContext.sysId       = records[i][1]
                TradeContext.busiNo      = records[i][2]
                TradeContext.workDate    = records[i][3]
                TradeContext.tellerno    = records[i][4]
                TradeContext.batchno     = records[i][5]
                
                #导出签约成功记录
                sql = ""
                sql = sql + " select  BUSIUSERNO,IDCODE,USERNAME,ACCNO,VOUHTYPE  FROM ABDT_CUSTINFO "
                sql = sql + " where BUSINO = '" + TradeContext.busiNo + "' " 
                sql = sql + " and   APPNO  = '" + TradeContext.sysId  + "' "
                sql = sql + " and status = '1'"      
                
                                  
                AfaLoggerFunc.tradeInfo( sql )
                
                rec = AfaDBFunc.SelectSql( sql )
                if rec == None :
                    return ExitSubTrade("E9999" ,"查询数据库异常")
                    
                elif len(rec) == 0:
                    TradeContext.errorCode, TradeContext.errorMsg = 'E8623', '数据库中无相应签约信息'
                    continue
                    
                else:
                    #导出成功数据记录
                    
                    outFileName = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + "_RF.TXT"
                    AfaLoggerFunc.tradeInfo('文件名=' + outFileName)
                    
                    if os.path.exists(outFileName):
                        os.system("rm -f " + outFileName)
                    
                    dfp = open( outFileName, 'w' )
                    
                    #把数据导出到指定文件
                    for i in range(0,len(rec)):
                        linebuf = ""
                        linebuf = linebuf + str(rec[i][0]).strip()   + "|"        #学生学号
                        linebuf = linebuf + str(rec[i][1]).strip()   + "|"        #身份证号
                        linebuf = linebuf + str(rec[i][2]).strip()   + "|"        #姓名
                        linebuf = linebuf + str(rec[i][3]).strip()   + "|"        #帐号
                        linebuf = linebuf + str(rec[i][4]).strip()   + "|"        #凭证种类
                        linebuf = linebuf + '签约成功'               + "\n"       #成功标记
                        
                        dfp.write( linebuf)
                    
                    dfp.close()
                    if not (os.path.exists(outFileName)):                                                    
                        TradeContext.errorCode, TradeContext.errorMsg='E8623', "导出成功签约数据文件失败"    
                        continue                         
               
                    sqlupdate = "update ahnx_file set status='2' ,procmsg='数据已导出' where batchno='"+TradeContext.batchno+"'"                   
            
                    AfaLoggerFunc.tradeInfo("更新AHNX_FILE语句："+str(sqlupdate))
                    retcode = AfaDBFunc.UpdateSqlCmt( sqlupdate )
    
                    if (retcode < 0):
                    #失败则continue跳出转化下一个文件
                        continue 
                    continue
            AfaLoggerFunc.tradeInfo('**********批量签约导出结束**********' )   
            
            return True   
        return True            
                
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )
        
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))   

#------------------------------------------------------------------
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  =errorMsg
        AfaLoggerFunc.tradeInfo( errorMsg )

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False




        
        
        
#######################################主函数###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('***************批量签约定时调度导出开始********************')
    
    TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
    if ( len(sys.argv) in (1,2)):
    
        if ( len(sys.argv) == 1 ):
            sTrxDate = AfaUtilTools.GetSysDate( ) 
        else:
            sTrxDate = sys.argv[1]         #定时调度日期
            
        AbdtQyOut()
        
    else:
        print( '用法1: jtfk_Proc sysid1  date')
        sys.exit(-1)    
    
    AfaLoggerFunc.tradeInfo('****************批量签约定时调度导出结束********************')         