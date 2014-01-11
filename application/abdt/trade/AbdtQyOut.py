# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AbdtQyOut.py
# �ļ���ʶ��
# ��    �ߣ��º�  
# �޸�ʱ�䣺2011-07-27
# ժ    Ҫ������ǩԼ ��ʱ���� ����
#
###############################################################################   
 
import TradeContext                
                                   
TradeContext.sysType = 'abdt' 
                                   
import time ,TradeContext ,AfaDBFunc,os,sys,TradeContext,AfaUtilTools,AbdtManager,AfaLoggerFunc,AfaFlowControl,AfaAdminFunc,sys,AfaFunc
from types import *

def AbdtQyOut():

    AfaLoggerFunc.tradeInfo('**********����ǩԼ��ʱ���ȵ��� ����**********')
                 
    try: 
                       
        AfaLoggerFunc.tradeInfo('**********����ǩԼ������ʼ**********' )                                                  
        AfaLoggerFunc.tradeInfo('**********���������ļ�**********')  
                               
        sql = ""       
        sql = "SELECT FILENAME,APPNO,BUSINO,WORKDATE,TELLERNO,BATCHNO FROM AHNX_FILE WHERE "
        sql = sql + "FILETYPE="    + "'7'" + " AND "        #7-����ǩԼ
        sql = sql + "STATUS="   + "'1'"                     #�Ѵ���
       
        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql(sql)
        if records == None:
            return ExitSubTrade("E9999" ,"��ѯAHNX_FILE���ݿ��쳣")
             
        elif(len(records)==0):
            return ExitSubTrade("E9999" ,"���ݿ�AHNX_FILE��û��Ҫ��ȡ���ļ���")
            
        else:            
            for i in range(0,len(records)):
            
                TradeContext.prefileName = records[i][0]
                TradeContext.sysId       = records[i][1]
                TradeContext.busiNo      = records[i][2]
                TradeContext.workDate    = records[i][3]
                TradeContext.tellerno    = records[i][4]
                TradeContext.batchno     = records[i][5]
                
                #����ǩԼ�ɹ���¼
                sql = ""
                sql = sql + " select  BUSIUSERNO,IDCODE,USERNAME,ACCNO,VOUHTYPE  FROM ABDT_CUSTINFO "
                sql = sql + " where BUSINO = '" + TradeContext.busiNo + "' " 
                sql = sql + " and   APPNO  = '" + TradeContext.sysId  + "' "
                sql = sql + " and status = '1'"      
                
                                  
                AfaLoggerFunc.tradeInfo( sql )
                
                rec = AfaDBFunc.SelectSql( sql )
                if rec == None :
                    return ExitSubTrade("E9999" ,"��ѯ���ݿ��쳣")
                    
                elif len(rec) == 0:
                    TradeContext.errorCode, TradeContext.errorMsg = 'E8623', '���ݿ�������ӦǩԼ��Ϣ'
                    continue
                    
                else:
                    #�����ɹ����ݼ�¼
                    
                    outFileName = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + "_RF.TXT"
                    AfaLoggerFunc.tradeInfo('�ļ���=' + outFileName)
                    
                    if os.path.exists(outFileName):
                        os.system("rm -f " + outFileName)
                    
                    dfp = open( outFileName, 'w' )
                    
                    #�����ݵ�����ָ���ļ�
                    for i in range(0,len(rec)):
                        linebuf = ""
                        linebuf = linebuf + str(rec[i][0]).strip()   + "|"        #ѧ��ѧ��
                        linebuf = linebuf + str(rec[i][1]).strip()   + "|"        #���֤��
                        linebuf = linebuf + str(rec[i][2]).strip()   + "|"        #����
                        linebuf = linebuf + str(rec[i][3]).strip()   + "|"        #�ʺ�
                        linebuf = linebuf + str(rec[i][4]).strip()   + "|"        #ƾ֤����
                        linebuf = linebuf + 'ǩԼ�ɹ�'               + "\n"       #�ɹ����
                        
                        dfp.write( linebuf)
                    
                    dfp.close()
                    if not (os.path.exists(outFileName)):                                                    
                        TradeContext.errorCode, TradeContext.errorMsg='E8623', "�����ɹ�ǩԼ�����ļ�ʧ��"    
                        continue                         
               
                    sqlupdate = "update ahnx_file set status='2' ,procmsg='�����ѵ���' where batchno='"+TradeContext.batchno+"'"                   
            
                    AfaLoggerFunc.tradeInfo("����AHNX_FILE��䣺"+str(sqlupdate))
                    retcode = AfaDBFunc.UpdateSqlCmt( sqlupdate )
    
                    if (retcode < 0):
                    #ʧ����continue����ת����һ���ļ�
                        continue 
                    continue
            AfaLoggerFunc.tradeInfo('**********����ǩԼ��������**********' )   
            
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




        
        
        
#######################################������###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('***************����ǩԼ��ʱ���ȵ�����ʼ********************')
    
    TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
    if ( len(sys.argv) in (1,2)):
    
        if ( len(sys.argv) == 1 ):
            sTrxDate = AfaUtilTools.GetSysDate( ) 
        else:
            sTrxDate = sys.argv[1]         #��ʱ��������
            
        AbdtQyOut()
        
    else:
        print( '�÷�1: jtfk_Proc sysid1  date')
        sys.exit(-1)    
    
    AfaLoggerFunc.tradeInfo('****************����ǩԼ��ʱ���ȵ�������********************')         