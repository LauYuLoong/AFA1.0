# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AbdtQyIn.py
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

def AbdtQyIn():

    AfaLoggerFunc.tradeInfo('**********����ǩԼ��ʱ���� ����**********')
                 
    try: 
     
        AfaLoggerFunc.tradeInfo('>>>�ж������ļ��Ƿ����')    
        sql = ""       
        sql = "SELECT FILENAME,APPNO,BUSINO,WORKDATE,TELLERNO FROM AHNX_FILE WHERE "
        sql = sql + "FILETYPE="    + "'7'" + " AND "        #7-����ǩԼ
        sql = sql + "STATUS="   + "'0'"                     #δ����
       
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
              
                FileName = '/home/maps/afa/data/batch/batch_qy/' + TradeContext.prefileName
                               
                if (os.path.exists(FileName)): 
                    AfaLoggerFunc.tradeInfo( '>>>���ļ��� fileName ��' + TradeContext.prefileName ) 
                                                                        
                    AfaLoggerFunc.tradeInfo('**********���������ļ�**********')                                                             
                    sfp = open(FileName,'r')            
                    AfaLoggerFunc.tradeInfo("��ȡ�����ļ�:" + FileName)
                                    
                    #���ɴ������������ļ�
                    serrorFile = '/home/maps/afa/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + TradeContext.prefileName[-7:-4] + "_WF.TXT"           
                    #errorFile = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + "_WF.TXT"
                    AfaLoggerFunc.tradeInfo('errorFile�ļ���=' + serrorFile)
                    if os.path.exists(serrorFile):
                        os.system("rm -f " + serrorFile)
                        
                        
                    errorFile = os.environ['AFAP_HOME'] + '/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + TradeContext.prefileName[-7:-4]+ "_WF.TXT"    
                    
                               
                    #��ȡһ�� ��ȡ���ļ���ʽΪ��ѧ��ѧ��|���֤|����|���ۺŻ򿨺�|ƾ֤��|
                    linebuff = sfp.readline( )            
                    lineCount = 0            
                    while( len(linebuff)>0 ):
                        swapbuff = linebuff.split("|")              
                        
                        if len(swapbuff) != 6:
                            TradeContext.errorCode, TradeContext.errorMsg='E7777', "��[" + str(lineCount+1) + "]�����ݸ�ʽ���Ϸ�,����������" + str(len(swapbuff)) + "��"                        
                            AfaLoggerFunc.tradeInfo("��" + str(lineCount+1) + "�����ݸ�ʽ���Ϸ�,����������" + str(len(swapbuff)) + "��")   
                            
                            #��¼ǩԼʧ�� ��Ϣ
                            FalseMsg( )
                                
                                            
                            linebuff = sfp.readline( )
                            lineCount = lineCount + 1
                            continue
                            
                        TradeContext.USERNO      = swapbuff[0].lstrip().rstrip()          #ѧ��ѧ��
                        if len(TradeContext.USERNO) != 9:
                            TradeContext.errorCode, TradeContext.errorMsg='E7777', "��[" + str(lineCount+1) + "]�����ݸ�ʽ���Ϸ�,ѧ��ѧ��λ������ȷ��"                        
                            AfaLoggerFunc.tradeInfo("��" + str(lineCount+1) + "�����ݸ�ʽ���Ϸ�,ѧ��ѧ��λ������ȷ��")
                            
                            #��¼ǩԼʧ�� ��Ϣ
                            FalseMsg( ) 
                            
                            linebuff = sfp.readline( )
                            lineCount = lineCount + 1
                            continue  
                        
                        TradeContext.IDENTITYNO  = swapbuff[1].lstrip().rstrip()          #���֤
                        if ((len(TradeContext.IDENTITYNO) != 18) and (len(TradeContext.IDENTITYNO) != 15) ):
                            TradeContext.errorCode, TradeContext.errorMsg='E7777', "��[" + str(lineCount+1) + "]�����ݸ�ʽ���Ϸ�,���֤λ������ȷ��"                        
                            AfaLoggerFunc.tradeInfo("��" + str(lineCount+1) + "�����ݸ�ʽ���Ϸ�,���֤λ������ȷ��")
                            
                            #��¼ǩԼʧ�� ��Ϣ
                            FalseMsg( )  
                            
                            linebuff = sfp.readline( )
                            lineCount = lineCount + 1
                            continue 
                        
                        TradeContext.USERNAME    = swapbuff[2].lstrip().rstrip()          #����(�ֿ�������)
                                                                            
                        if ((len(swapbuff[3].lstrip().rstrip()) != 23) and (len(swapbuff[3].lstrip().rstrip()) != 19)):
                             TradeContext.errorCode, TradeContext.errorMsg='E7777', "��[" + str(lineCount+1) + "]�����ݸ�ʽ���Ϸ�,�ʺŻ򿨺�λ������ȷ��"                        
                             AfaLoggerFunc.tradeInfo("��" + str(lineCount+1) + "�����ݸ�ʽ���Ϸ�,�ʺŻ򿨺�λ������ȷ��")  
                             
                             #��¼ǩԼʧ�� ��Ϣ
                             FalseMsg( )  
                            
                             linebuff = sfp.readline( )
                             lineCount = lineCount + 1
                             continue    
                            
                        
                        if len(swapbuff[3].lstrip().rstrip()) == 23:                      #��Ϊ23λ
                            #��                                                         
                            TradeContext.ACCNO     = swapbuff[3].lstrip().rstrip()
                            TradeContext.VOUHNO    = swapbuff[4].lstrip().rstrip()        #ƾ֤��
                            TradeContext.VOUHTYPE  = '49'                                 #ƾ֤����
                                                                                                                                                    
                        if len(swapbuff[3].lstrip().rstrip()) == 19:                      #��Ϊ19λ
                            #��                                                        
                            TradeContext.ACCNO     = swapbuff[3].lstrip().rstrip()
                            TradeContext.VOUHNO    = TradeContext.ACCNO[8:18]             #ƾ֤��
                            TradeContext.VOUHTYPE  = TradeContext.ACCNO[6:8]              #ƾ֤����
                            
                        if ( not CrtCustInfo( ) ):
                        
                            #��¼ǩԼʧ�� ��Ϣ
                            FalseMsg( )
                                
                                
                            linebuff = sfp.readline( )
                            lineCount = lineCount + 1
                            continue
                            
                        lineCount = lineCount + 1
                        linebuff = sfp.readline( )
                        continue            
                     
                        mfp.close( )     
                        sfp.close( )
                    
                    #���� AHNX_FILE �е� STATUS = 1
                    sql = ""
                    sql = " update AHNX_FILE set"
                    sql = sql + " STATUS   = '1',"  
                    sql = sql + " PROCMSG  = '������������ɣ��������ػ����ļ�'"
                    sql = sql + " where filename = '" + records[i][0] + "'" 
                    AfaLoggerFunc.tradeInfo('��ѯ��� sql: ' +sql)
                    
                    if AfaDBFunc.UpdateSqlCmt( sql ) == -1:
                        TradeContext.errorCode,TradeContext.errorMsg = "E9999","���� AHNX_FILE ���ݿ� STATUS ʧ��!"
                        raise AfaFlowControl.flowException( )                                                           
                    
                else:
                    TradeContext.errorCode,TradeContext.errorMsg = "E9999","�����ļ�������!"
                    continue 
                                    
            AfaLoggerFunc.tradeInfo('**********����ǩԼ��ʱ���� �˳�**********' )       
            
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        AfaFlowControl.flowException( )
    
#------------------------------------------------------------------
#ǩ������Э��
#------------------------------------------------------------------
def CrtCustInfo( ):
    #������Э���Ƿ����
    if ( not ChkCustInfo( ) ):
        return False
        
    #�Զ����ɸ���Э����
    if ( AfaFunc.GetSerialno() < 0 ):
        return ExitSubTrade( '9000', '���ɸ���Э����ʧ��' )


    #��֯����Э�����(�������� + �м�ҵ����ˮ��)
    TradeContext.PROTOCOLNO = TradeContext.workDate + TradeContext.agentSerialno
        
    #����Э�鲻���ڣ��ǼǸ���Э����Ϣ
    if ( not InsertCustInfo( ) ):
        return False
        
    return True
    
        
#------------------------------------------------------------------
#�жϸ���Э���Ƿ����
#------------------------------------------------------------------
def ChkCustInfo( ):

    AfaLoggerFunc.tradeInfo('>>>�жϸ���Э���Ƿ����')

    try:
        sql = ""
        sql = "SELECT PROTOCOLNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO="      + "'" + TradeContext.sysId        + "'" + " AND "        #ҵ����
        sql = sql + "BUSINO="     + "'" + TradeContext.busiNo       + "'" + " AND ("       #��λ���
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.USERNO       + "'" + " OR "         #�̻��ͻ����
        sql = sql + "ACCNO="      + "'" + TradeContext.ACCNO        + "'" + " )AND "       #�����˺�
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                  #״̬

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ����Э����Ϣ�쳣' )
    
        if ( len(records) > 0 ):
            return ExitSubTrade( '9000', 'ѧ��' +TradeContext.USERNO+ '�ø���Э���Ѿ���ע��,�����ٴν���ע��')

        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�жϸ���Э����Ϣ�Ƿ�����쳣')

#------------------------------------------------------------------
#���Ӹ���Э����Ϣ
#------------------------------------------------------------------
def InsertCustInfo( ):

    AfaLoggerFunc.tradeInfo('>>>���Ӹ���Э����Ϣ')

    try:

        sql = ""

        sql = "INSERT INTO ABDT_CUSTINFO("
        sql = sql + "APPNO,"
        sql = sql + "BUSINO,"
        sql = sql + "BUSIUSERNO,"
        sql = sql + "BUSIUSERAPPNO,"
        sql = sql + "BANKUSERNO,"
        sql = sql + "VOUHTYPE,"
        sql = sql + "VOUHNO,"
        sql = sql + "ACCNO,"
        sql = sql + "SUBACCNO,"
        sql = sql + "CURRTYPE,"
        sql = sql + "LIMITAMT,"
        sql = sql + "PARTFLAG,"
        sql = sql + "PROTOCOLNO,"
        sql = sql + "CONTRACTDATE,"
        sql = sql + "STARTDATE,"
        sql = sql + "ENDDATE,"
        sql = sql + "PASSCHKFLAG,"
        sql = sql + "PASSWD,"
        sql = sql + "IDCHKFLAG,"
        sql = sql + "IDTYPE,"
        sql = sql + "IDCODE,"
        sql = sql + "NAMECHKFLAG,"
        sql = sql + "USERNAME,"
        sql = sql + "TEL,"
        sql = sql + "ADDRESS,"
        sql = sql + "ZIPCODE,"
        sql = sql + "EMAIL,"
        sql = sql + "STATUS,"
        sql = sql + "ZONENO,"
        sql = sql + "BRNO,"
        sql = sql + "TELLERNO,"
        sql = sql + "INDATE,"
        sql = sql + "INTIME,"
        sql = sql + "NOTE1,"
        sql = sql + "NOTE2,"
        sql = sql + "NOTE3,"
        sql = sql + "NOTE4,"
        sql = sql + "NOTE5)"

        sql = sql + " VALUES ("

        sql = sql + "'" + TradeContext.sysId           + "',"        #ҵ����
        sql = sql + "'" + TradeContext.busiNo          + "',"        #��λ���
        sql = sql + "'" + TradeContext.USERNO          + "',"        #�̻��ͻ����
        sql = sql + "'" + TradeContext.USERNO          + "',"        #�̻��ͻ�Ӧ�ñ��
        sql = sql + "'" + TradeContext.VOUHNO          + "',"        #���пͻ���ţ�ǰ̨�ṩ�Ŀ����ļ���û�д��ʹ��ƾ֤�Ŵ��棩
        sql = sql + "'" + TradeContext.VOUHTYPE        + "',"        #ƾ֤����
        sql = sql + "'" + TradeContext.VOUHNO          + "',"        #ƾ֤��
        sql = sql + "'" + TradeContext.ACCNO           + "',"        #���ڴ���ʺ�
        sql = sql + "'',"                                            #���ʺ�
        sql = sql + "'01',"                                          #����
        sql = sql + "'0',"                                           #�����޶�
        sql = sql + "'A',"                                           #���ֿۿ��־  ��ΪA ��ʾȫ��ۿ� �۵�1���
        sql = sql + "'" + TradeContext.PROTOCOLNO      + "',"        #Э����
        sql = sql + "'" + TradeContext.workDate        + "',"        #ǩԼ����(��ͬ����)
        sql = sql + "'" + TradeContext.workDate        + "',"        #��Ч����
        sql = sql + "'20990101',"                                    #ʧЧ����
        sql = sql + "'0',"                                           #������֤��־
        sql = sql + "'" + "****************"           + "',"        #����
        sql = sql + "'0',"                                           #֤����֤��־
        sql = sql + "'01',"                                          #֤������
        sql = sql + "'" + TradeContext.IDENTITYNO      + "',"        #֤������
        sql = sql + "'0',"                                           #������֤��־
        sql = sql + "'" + TradeContext.USERNAME        + "',"        #�ͻ�����
        sql = sql + "'',"                                            #��ϵ�绰
        sql = sql + "'',"                                            #��ϵ��ַ
        sql = sql + "'',"                                            #�ʱ�
        sql = sql + "'',"                                            #��������
        sql = sql + "'1',"                                           #״̬
        sql = sql + "'" + TradeContext.busiNo[0:4]     + "',"        #������
        sql = sql + "'" + TradeContext.busiNo[0:10]    + "',"        #�����(��������)
        sql = sql + "'" + TradeContext.tellerno        + "',"        #��Ա��
        sql = sql + "'" + TradeContext.workDate        + "',"        #¼������
        sql = sql + "'" + TradeContext.workTime        + "',"        #¼��ʱ��
        sql = sql + "'',"                                            #��ע1
        sql = sql + "'',"                                            #��ע2
        sql = sql + "'',"                                            #��ע3
        sql = sql + "'',"                                            #��ע4
        sql = sql + "'')"                                            #��ע5

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', 'ѧ��Ϊ' +TradeContext.USERNO+ '���Ӹ���Э����Ϣ����ʧ��')
            
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '���Ӹ���Э����Ϣ�쳣')
        
#------------------------------------------------------------------
#�׳�����ӡ��ʾ��Ϣ
#------------------------------------------------------------------
def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg  = errorMsg
        AfaLoggerFunc.tradeInfo( errorMsg )

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        
        
#------------------------------------------------------------------
#����ǩԼʧ�� �ͻ���Ϣ
#------------------------------------------------------------------
def FalseMsg():

    AfaLoggerFunc.tradeInfo('>>>��ŵ��������Ϣ...') 
    
    try:
        
        errorFile = '/home/maps/afa/data/batch/down/' + TradeContext.sysId + TradeContext.busiNo[6:] + TradeContext.workDate + TradeContext.prefileName[-7:-4]+ "_WF.TXT"
        
        mfp = open( errorFile, 'a' ) 
        AfaLoggerFunc.tradeInfo("������Ϣ���ļ�Ϊ��"  + errorFile) 
        TradeContext.errorFile = TradeContext.errorMsg                                                           
        mfp = open( errorFile, 'a' )                
        mfp.write( TradeContext.errorFile + "\n")
        mfp.close()  
        
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )                                  
      
              
#######################################������###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('***************����ǩԼ��ʱ���ȿ�ʼ********************')
    
    TradeContext.workTime=AfaUtilTools.GetSysTime( )
        
    if ( len(sys.argv) in (1,2)):
    
        if ( len(sys.argv) == 1 ):
            sTrxDate = AfaUtilTools.GetSysDate( ) 
        else:
            sTrxDate = sys.argv[1]         #��ʱ��������
            
        AbdtQyIn()
        
    else:
        print( '�÷�1: jtfk_Proc sysid1  date')
        sys.exit(-1)    
    
    AfaLoggerFunc.tradeInfo('****************����ǩԼ��ʱ���Ƚ���********************')
            
     