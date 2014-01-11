# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AhXnb_FlashFileStatus.py
# �ļ���ʶ��
# ��    �ߣ�����
# ժ    Ҫ����������������Ϣʵʱ������ũ��������Ϣ
###############################################################################
import TradeContext

TradeContext.sysType = 'ahxnb'     
                                   
import AfaDBFunc,AfaUtilTools,AfaLoggerFunc,sys
from types import *

#######################################������###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************����������Ϣʵʱ���µ���ũ��������Ϣ��ʼ********************')
    
    try:
        #=====================��ȡϵͳ����ʱ��==================================
        TradeContext.WorkDate=AfaUtilTools.GetSysDate( )
        TradeContext.WorkTime=AfaUtilTools.GetSysTime( )
        
        sql = ""
        sql = sql + "select BATCHNO,APPNO,BUSINO,PROCMSG,STATUS"
        sql = sql + " from abdt_batchInfo"
        sql = sql + " where INDATE = '"+ TradeContext.WorkDate +"'"   #��������
        sql = sql + " and STATUS = '40'"                              #�ļ�״̬
        sql = sql + " and note5 <> '1'"                               #����״̬
        
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql( sql ) 
        
        if records==None:
            AfaLoggerFunc.tradeInfo('��ѯabdt_batchInfoʧ��')
            TradeContext.errorCode,TradeContext.errorMsg = 'D001','��ѯabdt_batchInfoʧ��'
            sys.exit(-1)
            
        elif(len(records) == 0):
            AfaLoggerFunc.tradeInfo('��ѯabdt_batchInfo�޴���Ϣ')
            TradeContext.errorCode,TradeContext.errorMsg = 'D001','��ѯabdt_batchInfo�޴���Ϣ'
            sys.exit(-1)
            
        else:
            for i in range(0,len(records)):
                sql = ""
                sql = sql + "select STATUS"
                sql = sql + " from ahnx_file"
                sql = sql + " where APPNO = '"+ records[i][1] +"'"  #ҵ����
                sql = sql + " and BUSINO = '"+ records[i][2] +"'"   #��λ���
                sql = sql + " and BATCHNO = '"+ records[i][0] +"'"  #���κ�
                
                AfaLoggerFunc.tradeInfo(sql)
                record = AfaDBFunc.SelectSql( sql )
                
                if record==None:
                    AfaLoggerFunc.tradeInfo('��ѯahnx_fileʧ��')
                    TradeContext.errorCode,TradeContext.errorMsg = 'D001','��ѯahnx_fileʧ��'
                    sys.exit(-1)
                    
                elif(len(record) == 0):
                    AfaLoggerFunc.tradeInfo('��ѯahnx_file�޴���Ϣ')
                    #TradeContext.errorCode,TradeContext.errorMsg = 'D001','��ѯahnx_file�޴���Ϣ'
                    #sys.exit(-1)
                    continue
 
                else:
                    if( record[0][0].strip() != '2' and record[0][0].strip() != '0' and record[0][0].strip() != '1' ):
                        try:
                            sql = ""
                            sql = sql + "update ahnx_file set"
                            sql = sql + " STATUS = '2',"
                            sql = sql + " PROCMSG = '�����ѳ���,ԭ��Ϊ"+ records[i][3][0:32] +"'"
                            sql = sql + " where APPNO = '"+ records[i][1] +"'"  #ҵ����
                            sql = sql + " and BUSINO = '"+ records[i][2] +"'"   #��λ���
                            sql = sql + " and BATCHNO = '"+ records[i][0] +"'"  #���κ�
                            
                            AfaLoggerFunc.tradeInfo(sql)
                            result = AfaDBFunc.UpdateSql( sql ) 
                            
                            if( result <0 ):
                                AfaLoggerFunc.tradeInfo('����ahnx_file��ʧ�ܣ����κ�Ϊ��'+records[i][0])
                                continue
                                
                            sql = ""
                            sql = sql + "update abdt_batchInfo set"
                            sql = sql + " note5 = '1'"
                            sql = sql + " where APPNO = '"+ records[i][1] +"'"  #ҵ����
                            sql = sql + " and BUSINO = '"+ records[i][2] +"'"   #��λ���
                            sql = sql + " and BATCHNO = '"+ records[i][0] +"'"  #���κ�
                            
                            AfaLoggerFunc.tradeInfo(sql)
                            result = AfaDBFunc.UpdateSql( sql ) 
                            
                            if( result <0 ):
                                AfaLoggerFunc.tradeInfo('����abdt_batchInfo��ʧ�ܣ����κ�Ϊ��'+records[i][0])
                                continue
                            
                            #�����ύ
                            if not AfaDBFunc.CommitSql( ):
                                AfaLoggerFunc.tradeInfo('�����ύʧ��')
                                sys.exit(-1)
                            AfaLoggerFunc.tradeInfo('�����ύ�ɹ�')

                        except Exception, e:
                            AfaLoggerFunc.tradeInfo( str(e) )

                            #����ع�
                            if not AfaDBFunc.RollbackSql( ):
                                AfaLoggerFunc.tradeInfo('����ع�ʧ��')
                                sys.exit(-1)
                            AfaLoggerFunc.tradeInfo('����ع��ɹ�')
  
                    else:
                        AfaLoggerFunc.tradeInfo('�������ѳ�����״̬���������ܳ���')
                
            AfaLoggerFunc.tradeInfo('����'+ str(i+1) +'����¼')
        sys.exit(0)
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        sys.exit(-1)
