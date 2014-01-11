# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�T001000_8623.py
# �ļ���ʶ������ǩԼ
# ��    �ߣ��º�  
# �޸�ʱ�䣺2011-07-27
# ժ    Ҫ������ǩԼ ���� 
#
###############################################################################
import ConfigParser, AfaUtilTools, sys, AfaDBFunc,AfaLoggerFunc,AhXnbFunc,TradeContext,AfaFunc,AfaFlowControl,AfaFunc
import os
from types import *

def TrxMain():

    AfaLoggerFunc.tradeInfo('**********����ǩԼ��¼�ļ���(8623)��ʼ**********' )
    
    try:
        
        AfaLoggerFunc.tradeInfo( '��ʼ�����뽻�ױ���' )
        
        #�жϵ�λ����ǩԼ�Ƿ���Ȩ��
        if ( not ChkUnitLimit( )):
            return False        
              
        #�Ƿ񱾻���
        if (TradeContext.I1BUSINO[:10] != TradeContext.I1SBNO):
            TradeContext.errorCode,TradeContext.errorMsg = "E8623" , "�Ǳ��������������˽���!"  
            raise AfaFlowControl.flowException( )                
              
        
        #�ļ�����
        if not( TradeContext.existVariable( "I1FILENAME" ) and len(TradeContext.I1FILENAME.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = "E8623","�����ڴ��ļ���!"
            raise AfaFlowControl.flowException( )
        
        #��λ���
        if not( TradeContext.existVariable( "I1BUSINO" ) and len(TradeContext.I1BUSINO.strip()) > 0 ):
            TradeContext.errorCode,TradeContext.errorMsg = 'E8623', "�����ڴ˵�λ���"
            raise AfaFlowControl.flowException( )      
        
        #����ί�к�
        if ( not CrtBatchNo( ) ):
            return False
        
        AfaLoggerFunc.tradeInfo('**********����ǩԼ���뿪ʼ**********' )
        
        #�жϸõ�λ�Ƿ�ǩԼ
        sql = ""
        sql = sql + " select  * FROM ABDT_UNITINFO "
        sql = sql + " where BUSINO = '" + TradeContext.I1BUSINO + "' "
        sql = sql + " and APPNO  = '"+ TradeContext.sysId +"'"
        sql = sql + " and STATUS = '1' "
        sql = sql + " and AGENTTYPE = '3'"
                   
        AfaLoggerFunc.tradeInfo( '��ѯ���ݿ�sql��' +sql )
        
        recs = AfaDBFunc.SelectSql( sql )
        if recs == None :
            TradeContext.errorCode,TradeContext.errorMsg = "E8623","��ѯ���ݿ��쳣!"
            raise AfaFlowControl.flowException( )
            
        elif(len(recs)==0):
            TradeContext.errorCode,TradeContext.errorMsg = "9999" , "�õ�λû��ǩԼ,�������˽���!"
            raise AfaFlowControl.flowException( ) 
        
                
        #�ж��ļ��Ƿ��Ѿ�����
        sql = ""
        sql = sql + " select  * FROM AHNX_FILE "
        sql = sql + " where busino = '" + TradeContext.I1BUSINO + "' "
        sql = sql + " and appno  = '"+ TradeContext.sysId +"'"
        sql = sql + " and filetype = '7' "
                   
        AfaLoggerFunc.tradeInfo( '��ѯ���ݿ�sql��' +sql )
        
        rec = AfaDBFunc.SelectSql( sql )
        if rec == None :
            TradeContext.errorCode,TradeContext.errorMsg = "E8623","��ѯ���ݿ��쳣!"
            raise AfaFlowControl.flowException( )
            
        if len(rec) > 0:
            for i in range(0,len(rec)):
                if (rec[i][1] == TradeContext.I1FILENAME):        
                    TradeContext.errorCode,TradeContext.errorMsg = "E8623","���ݿ����Ѵ��ڴ��ļ�����˶Ժ��ٵ���!"
                    raise AfaFlowControl.flowException( )        
        
        AfaLoggerFunc.tradeInfo( '>>>��������ǩԼ�ļ�' )             
        #���ļ������浽 AHNX_FILE ��     
        
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
        sql = sql + "'" + TradeContext.BATCHNO     + "',"             #�Ǽ���ˮ��
        sql = sql + "'" + TradeContext.I1FILENAME  + "',"             #�ļ���
        sql = sql + "'" + TradeContext.TranDate    + "',"             #�Ǽ�����
        sql = sql + "'0',"                                            #״̬(0-������1-����ɹ�)
        sql = sql + "'�����ļ��ȴ�������...',"                        #������Ϣ����
        sql = sql + "'" + TradeContext.TranDate    + "',"             #��������
        sql = sql + "'" + TradeContext.sysId       + "',"             #ҵ����
        sql = sql + "'" + TradeContext.I1BUSINO    + "',"             #��λ���
        sql = sql + "'0',"                                            #�ܱ���
        sql = sql + "'0.00',"                                         #�ܽ��
        sql = sql + "'7',"                                            #�ļ����ͣ�0-����������1-�������ۣ�2-����������7--����ǩԼ)
        sql = sql + "'" + TradeContext.I1SBNO      + "',"             #������
        sql = sql + "'" + TradeContext.I1USID      + "',"             #��Ա��
        sql = sql + "'20110101',"                                     #��Ч����
        sql = sql + "'20990101',"                                     #ʧЧ����
        sql = sql + "'" + TradeContext.TranTime    + "',"             #����ʱ��
        sql = sql + "'',"                                             #����1
        sql = sql + "'',"                                             #����2
        sql = sql + "'',"                                             #����3
        sql = sql + "'')"                                             #����4
        
        AfaLoggerFunc.tradeInfo( "�����ļ���¼��" + sql )
        
        ret = AfaDBFunc.InsertSqlCmt(sql)
        
        if ret < 0:
            TradeContext.errorCode,TradeContext.errorMsg = "E8623","��������ʧ��!"
            raise AfaFlowControl.flowException( )              
                   
        TradeContext.FileName =  TradeContext.sysId + TradeContext.I1BUSINO[6:] + TradeContext.TranDate + TradeContext.I1FILENAME[-7:-4]+"_WF.TXT"
        
        TradeContext.errorCode,TradeContext.errorMsg ="0000","���׳ɹ�"
        
        AfaLoggerFunc.tradeInfo('**********����ǩԼ�������**********' )    
        return True
              
           
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )   

##########################################################################################        
#����ί�к�
##########################################################################################
def CrtBatchNo( ):

    AfaLoggerFunc.tradeInfo('>>>��������ί�к�')

    try:
        sqlStr = "SELECT NEXTVAL FOR ABDT_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            TradeContext.errorCode, TradeContext.errorMsg='E8623', "����ί�к��쳣"
            raise AfaFlowControl.flowException( )

        #���κ�
        TradeContext.BATCHNO = TradeContext.TranDate + str(records[0][0]).rjust(8, '0')

        return True

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )  
        
########################################################################################## 
# �жϸõ�λ�Ƿ�������ǩԼ��Ȩ�� 0--��Ȩ�� 1--��Ȩ��
##########################################################################################
def ChkUnitLimit( ):

    try:
        AfaLoggerFunc.tradeInfo('>>>�жϸõ�λ�Ƿ�������ǩԼ��Ȩ��')
        sql = ""
        sql = "SELECT FLAG FROM ABDT_QYFLAG WHERE "
        sql = sql + " SYSID = '" + TradeContext.sysId + "'" 
        sql = sql + " AND STATUS = '1'"
        
        records = AfaDBFunc.SelectSql( sql )
        AfaLoggerFunc.tradeInfo('��ѯ���ݿ� sql: ' +sql)
        
        if(records==None):
            TradeContext.errorCode,TradeContext.errorMsg = "9999" , "��ѯABDT_QYFLAG���ݿ��쳣!"
            raise AfaFlowControl.flowException( ) 
                      
        elif(len(records)==0):
            TradeContext.errorCode,TradeContext.errorMsg = "9999" , "�޸õ�λǩԼȨ����Ϣ!"
            raise AfaFlowControl.flowException( ) 

        else:
            if (records[0][0]=='0'):
                TradeContext.errorCode,TradeContext.errorMsg = "9999" , "�õ�λ��ǩԼȨ��!"
                raise AfaFlowControl.flowException( ) 
                
            if (records[0][0]=='1'):
                AfaLoggerFunc.tradeInfo('>>>�õ�λ��ǩԼȨ��')
                return True 
                         
        return True
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )       
