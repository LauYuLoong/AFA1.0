# -*- coding: GB18030 -*-
###############################################################################
# �ļ����ƣ�AhXnb_SwapToBatch.py
# �ļ���ʶ��
# ��    �ߣ�����̩
# ժ    Ҫ��ת���������۴����ļ�Ϊ����ϵͳ������Ҫ�ĸ�ʽ
#
###############################################################################
import TradeContext                

TradeContext.sysType = 'ahxnb'

import AfaDBFunc,os,AfaLoggerFunc,sys,ConfigParser,AhXnbFunc,AfaFtpFunc
from types import *

#�������������ļ���ʽת��
#------------------------------------------------------------------
def file_To_Batch_Pro( ):
    AfaLoggerFunc.tradeInfo( '�ļ�������ʼ' )
    
    try:
        #-----1,��ѯδ����������ļ�
        sql = ''
        sql = sql + "select filename,batchno,appno,busino,workdate,brno,tellerno,begindate,enddate,worktime,totalnum,totalamt,filetype"
        sql = sql + " from ahnx_file"
        sql = sql + " where status='0'"             #�ϴ��ɹ�
        sql = sql + " and filetype in ('0','1')"    #��������
        
        AfaLoggerFunc.tradeInfo('>>>>>>>��ʼ��ѯAHNX_FILEԭ���ף�'+ str(sql))
        records = AfaDBFunc.SelectSql( sql )
        
        if records==None:
            return ExitSubTrade( 'E0001', "�������ݿ�ʧ��")
            
        elif(len(records) == 0):
            return ExitSubTrade( 'E0001', "�޴���Ϣ")
            
        else:
            AfaLoggerFunc.tradeInfo("AHNX_FILE���еļ�¼����" +str(len(records)))
            
            for i in range(len(records)):
                #����������Ҫת�����ļ�             
                TradeContext.I1FILENAME = records[i][0]
                #ί�к�
                TradeContext.BATCHNO    = records[i][1]
                #ҵ����
                TradeContext.I1APPNO    = records[i][2]
                #��λ���
                TradeContext.I1BUSINO   = records[i][3]
                #��������
                TradeContext.WorkDate   = records[i][4]
                #������
                TradeContext.I1SBNO     = records[i][5]
                #��Ա��
                TradeContext.I1USID     = records[i][6]
                #��Ч����
                TradeContext.I1STARTDATE= records[i][7]
                #ʧЧ����
                TradeContext.I1ENDDATE  = records[i][8]
                #����ʱ��
                TradeContext.WorkTime   = records[i][9]
                #�ܱ���
                TradeContext.I1TOTALNUM = records[i][10]
                #�ܽ��
                TradeContext.I1TOTALAMT = records[i][11]
                #�������۱�־
                TradeContext.FILETYPE   = records[i][12]
                
                #-----2���ϴ��ļ�ת�������������ļ�(������up_other���ļ�,���ϴ�swapĿ¼)
                TradeContext.sFileName = TradeContext.XNB_BSDIR + "/" + TradeContext.I1FILENAME
                TradeContext.swapFile  = TradeContext.I1APPNO + TradeContext.I1BUSINO + "0000"
                TradeContext.dFileName = TradeContext.XNB_BDDIR + "/" + TradeContext.swapFile
                TradeContext.pFileName = TradeContext.ABDT_PDIR + "/" + TradeContext.I1APPNO + TradeContext.I1BUSINO + "0000_" + TradeContext.WorkDate
                
                #20120916 �ϴ�������Ŀ¼�ļ���
                TradeContext.batchFile = TradeContext.I1APPNO + TradeContext.I1BUSINO + "0000_" + TradeContext.WorkDate
                
                AfaLoggerFunc.tradeInfo("ת������������ǰ���ļ�Ϊ��" +TradeContext.sFileName)
                AfaLoggerFunc.tradeInfo("ת���������������ļ�Ϊ��"  +TradeContext.dFileName)
                
                if not os.path.exists(TradeContext.sFileName):
                    AfaLoggerFunc.tradeInfo("��ת���ļ���"  +TradeContext.sFileName + "������")
                    AhXnbFunc.UpdateFileStatus(TradeContext.BATCHNO, '2', '��ת�����ļ�������', TradeContext.WorkTime)
                    continue
                
                sfp = open(TradeContext.sFileName,"r")
                dfp = open(TradeContext.dFileName,"w")
                
                #----2.1,�ܱ���У��(<=15w)
                line = sfp.readline()
                fileCount = 0
                while( len(line) > 0 ):
                    line = sfp.readline()
                    fileCount = fileCount + 1
                sfp.close( )
                AfaLoggerFunc.tradeInfo('�������ϴ��ļ��ܱ���Ϊ��'+str(fileCount))
                
                if fileCount > 150000:
                    AhXnbFunc.UpdateBatchInfo(TradeContext.BATCHNO, "2", "�ϴ��ļ��ܱ�������15w��,�봦���������" )
                    continue
                
                sfp = open(TradeContext.sFileName,"r")
                
                linebuff = sfp.readline( )
                lineCount = 0
                
                #begin 20120209 �������� ɾ����ϸ������Ϣ�ļ�
                AhXnbFunc.DelProcmsgFile(TradeContext.BATCHNO)
                #end
                
                flag = 0           #�����ʶ
                AfaLoggerFunc.tradeInfo('�����ļ�ѭ��У�鿪ʼ������������')
                
                while( len(linebuff)>0 ):
                    lineCount = lineCount + 1
                    swapbuff = linebuff.split("|")
                                        
                    #----2.2,��ʽ����
                    if len(swapbuff) !=7:
                        #begin 20120209 �������� ���ϴ��ļ���ʽ���󣬸���ahxnb_file��������ϸ��Ϣд���ļ�
                        AhXnbFunc.UpdateBatchInfo(TradeContext.BATCHNO, "2", "�ϴ��ļ���ʽ����,ԭ�����ϸ��Ϣ" ,"�ϴ��ļ���" + str(lineCount) + "�и�ʽ[�ֶ���]����ȷ������")
                        flag = 1
                        #end
                        
                        linebuff = sfp.readline( )
                        continue
                    
                    TradeContext.SBNO        = swapbuff[0].lstrip().rstrip()          #�籣���
                    TradeContext.NAME        = swapbuff[1].lstrip().rstrip()          #����
                    TradeContext.IDENTITYNO  = swapbuff[2].lstrip().rstrip()          #���֤
                    TradeContext.AMOUNT      = swapbuff[3].lstrip().rstrip()          #���۽��
                    TradeContext.SBBILLNO    = swapbuff[4].lstrip().rstrip()          #���κ�
                    TradeContext.ACCNO       = swapbuff[5].lstrip().rstrip()          #��Ա�˺�
                    TradeContext.AreaCode    = swapbuff[6].lstrip().rstrip()          #�����������浽ahxnb_swap��note4��
                    
                    #begin 20120209 �������� ����ʽʧ�ܣ���д��Ŀ�������ļ��������鿴��ʽ
                    if(flag == 1):
                        linebuff = sfp.readline( )
                        continue
                    #end
                    
                    #----2.4,�Ǽ���ϸ��Ϣ
                    insertBatch( )
                    
                    #----2.5��ת���ֶ�д���ļ�
                    lineinfo =            TradeContext.SBNO   + "|"
                    lineinfo = lineinfo + TradeContext.ACCNO  + "|"
                    lineinfo = lineinfo + TradeContext.NAME   + "|"
                    lineinfo = lineinfo + TradeContext.AMOUNT + "|"
                    dfp.write(lineinfo + "\n")
                    linebuff = sfp.readline( )
                    
                sfp.close( )
                dfp.close( )
                
                AfaLoggerFunc.tradeInfo('�����ļ�ѭ��У�����������������')
                AfaLoggerFunc.tradeInfo('�ϴ��ļ��ܱ���Ϊ'+str(lineCount))
                
                #----3���ϴ��ļ�У�����
                #----3.1��ʧ��  ɾ�������ļ�����
                if (flag == 1):
                    AfaLoggerFunc.tradeInfo("����"+TradeContext.BATCHNO+"�ϴ��ļ���ʽ����,ԭ����д����ϸ�����ļ�")
                    fileName = os.environ['AFAP_HOME'] + '/data/ahxnb/' + TradeContext.swapFile
                    
                    if ( os.path.exists(fileName) and os.path.isfile(fileName) ):
                        cmdstr = "rm " + fileName
                        AfaLoggerFunc.tradeInfo('>>>ɾ������:' + cmdstr)
                        os.system(cmdstr)
                    continue
                #end
                
                #-----3.2,�ɹ�  ����ahnx_file�����������ļ����Ǽ���������
                #-----3.2.1������ahnx_file��
                sqlupdate = ""
                sqlupdate = sqlupdate + "update ahnx_file set"
                sqlupdate = sqlupdate + " status='3',"
                sqlupdate = sqlupdate + " procmsg='��ʽת����ɣ��ȴ�����ҵ��ϵͳ����������'"
                sqlupdate = sqlupdate + " where batchno = '"+ TradeContext.BATCHNO +"'"
                
                AfaLoggerFunc.tradeInfo("�������ݿ���䣺" + sqlupdate)
                result   = AfaDBFunc.UpdateSqlCmt( sqlupdate )
                
                if( result <0 ):
                    continue
                
                #-----3.2.2�����ļ��Ƶ������ڲ�����Ŀ¼��(swap)
                try:
                    #20120916 �����ز�������Ϊ FTP ����
                    #begin
                    #cp_cmd_str="mv " + TradeContext.dFileName + " " + TradeContext.pFileName
                    #os.system(cp_cmd_str)
                    
                    if not AfaFtpFunc.putFile('AHXNB_PUT',TradeContext.swapFile,TradeContext.batchFile) :
                        AfaLoggerFunc.tradeInfo('ftp�ϴ��ļ�ʧ�� : '+ TradeContext.swapFile)
                        #GridFunc.WriteInfo('Grid_ToBatch'+ TradeContext.gridIds[i][0].strip() + TradeContext.WorkDate,'ftp�ϴ�ʧ��,�ļ���='+ TradeContext.dFileName)
                        continue
                        
                    #end
                    
                except Exception, e:
                    AfaLoggerFunc.tradeInfo( str(e) )
                    continue
                
                #-----3.2.3���Ǽ�������������������Ϣ
                if (  not ChkBatchInfo( ) ):
                    #����AHXNB_FILE
                    sqlupdate = "update ahnx_file set status='2',procmsg='"+ TradeContext.errorMsg +"'"
                    sqlupdate = sqlupdate + "where batchno = '"+ TradeContext.BATCHNO +"'"
                    AfaLoggerFunc.tradeInfo("�������ݿ���䣺" + sqlupdate)
                    result   = AfaDBFunc.UpdateSqlCmt( sqlupdate )
                    continue
                    
                if( not InsertBatchInfo( ) ):
                    continue
                    
            return True
    except Exception, e:
        sfp.close()
        dfp.close()

        return ExitSubTrade('E0001', str(e))


#------------------------------------------------------------------
#��ȡ������Ϣ
#------------------------------------------------------------------
def getBatchFile( ConfigNode ):
    try:
        #��ȡFTP�����ļ�
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        
        config.readfp( open( configFileName ) )
        
        TradeContext.ABDT_PDIR    = config.get(ConfigNode,'ABDT_BDIR')     #�����ϴ��ļ����·��
        TradeContext.ABDT_GDIR    = config.get(ConfigNode,'ABDT_GDIR')     #���������ļ����·��
        TradeContext.XNB_BSDIR    = config.get(ConfigNode,'XNB_BSDIR')     #��ũ��ת��ǰ��·��
        TradeContext.XNB_BDDIR    = config.get(ConfigNode,'XNB_BDDIR')     #��ũ��ת�����·��
        
        
        return True
        
    except Exception, e:
        return ExitSubTrade( 'E0001', "��ȡ�����ļ��쳣��" + str(e))

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
#������ת����AHXNB_SWAP�еǼ���ʱ����
#------------------------------------------------------------------
def insertBatch( ):    
    #�Ȳ�ѯ�����Ƿ����
    sql = ""
    sql = sql + "select IDENTITYNO,SBBILLNO,NAME"
    sql = sql + " from ahxnb_swap"
    sql = sql + " where sbno = '" + TradeContext.SBNO + "'"          #�籣���
    sql = sql + " and workdate = '" + TradeContext.WorkDate + "'"    #��������
    AfaLoggerFunc.tradeInfo(sql) 
    ret = AfaDBFunc.SelectSql( sql )
    
    if ret == None:
        return False
        
    elif( len(ret) == 0 ):
        pass
        
    elif len(ret) > 0:
        #���жϸ������Ƿ����,������-�����룬��������-����
        for j in range(0,len(ret)):
            if( TradeContext.SBBILLNO == ret[j][1].strip() ):
                return False
                
        #һ���ϴ��ļ���ͬһ�ͻ��ж������ʱ��Name��ӱ�ʶ
        TradeContext.NAME = TradeContext.NAME + ";" + str( len(ret) )
        
    sql = ""
    sql = sql + "insert into AHXNB_SWAP("
    sql = sql + "SBNO,"
    sql = sql + "NAME,"
    sql = sql + "IDENTITYNO,"
    sql = sql + "AMOUNT,"
    sql = sql + "SBBILLNO,"
    sql = sql + "ACCNO,"
    sql = sql + "FILENAME,"
    sql = sql + "WORKDATE,"
    sql = sql + "NOTE1,"
    sql = sql + "NOTE2,"
    sql = sql + "NOTE3,"
    sql = sql + "NOTE4)"
    
    sql = sql + " values("
    sql = sql + "'" + TradeContext.SBNO       + "',"             #�籣���
    sql = sql + "'" + TradeContext.NAME       + "',"             #����    
    sql = sql + "'" + TradeContext.IDENTITYNO + "',"             #���֤  
    sql = sql + "'" + TradeContext.AMOUNT     + "',"             #���۽��
    sql = sql + "'" + TradeContext.SBBILLNO   + "',"             #���κ�  
    sql = sql + "'" + TradeContext.ACCNO      + "',"             #��Ա�˺�
    sql = sql + "'" + TradeContext.I1FILENAME + "',"             #�����ļ���
    sql = sql + "'" + TradeContext.WorkDate   + "',"             #�����Ǽ�����
    
    sql = sql + "'',"
    sql = sql + "'',"
    sql = sql + "'',"
    sql = sql + "'" + TradeContext.AreaCode   + "')"             #��������
    AfaLoggerFunc.tradeInfo(sql)    
    ret = AfaDBFunc.InsertSqlCmt(sql)
    
    if ret < 0:
        return ExitSubTrade('D0001', "��������ʧ��")
        
    return True
    
#------------------------------------------------------------------
#�Ǽ�������ҵ������Ϣ
#------------------------------------------------------------------
def InsertBatchInfo( ):
    AfaLoggerFunc.tradeInfo('>>>�Ǽ�������ҵ������Ϣ')

    try:
        sql = ""
        sql = "INSERT INTO ABDT_BATCHINFO("
        sql = sql + "BATCHNO,"                 #ί�к�(���κ�: Ψһ(����+��ˮ��)
        sql = sql + "APPNO,"                   #ҵ����
        sql = sql + "BUSINO,"                  #��λ���
        sql = sql + "ZONENO,"                  #������
        sql = sql + "BRNO,"                    #�����
        sql = sql + "USERNO,"                  #����Ա
        sql = sql + "ADMINNO,"                 #����Ա
        sql = sql + "TERMTYPE,"                #�ն�����
        sql = sql + "FILENAME,"                #�ϴ��ļ���
        sql = sql + "INDATE,"                  #ί������
        sql = sql + "INTIME,"                  #ί��ʱ��
        sql = sql + "BATCHDATE,"               #�ύ����
        sql = sql + "BATCHTIME,"               #�ύʱ��
        sql = sql + "TOTALNUM,"                #�ܱ���
        sql = sql + "TOTALAMT,"                #�ܽ��
        sql = sql + "SUCCNUM,"                 #�ɹ�����
        sql = sql + "SUCCAMT,"                 #�ɹ����
        sql = sql + "FAILNUM,"                 #ʧ�ܱ���
        sql = sql + "FAILAMT,"                 #ʧ�ܽ��
        sql = sql + "STATUS,"                  #״̬
        sql = sql + "BEGINDATE,"               #��Ч����
        sql = sql + "ENDDATE,"                 #ʧЧ����
        sql = sql + "PROCMSG,"                 #������Ϣ
        sql = sql + "NOTE1,"                   #��ע1
        sql = sql + "NOTE2,"                   #��ע2
        sql = sql + "NOTE3,"                   #��ע3
        sql = sql + "NOTE4,"                   #��ע4
        sql = sql + "NOTE5)"                   #��ע5

        sql = sql + " VALUES ("

        sql = sql + "'" + TradeContext.BATCHNO          + "',"                              #ί�к�(���κ�:Ψһ(����+��ˮ��)
        sql = sql + "'" + TradeContext.I1APPNO          + "',"                              #ҵ����
        sql = sql + "'" + TradeContext.I1BUSINO         + "',"                              #��λ���
        sql = sql + "'" + TradeContext.I1SBNO[0:4]      + "',"                              #������
        sql = sql + "'" + TradeContext.I1SBNO           + "',"                              #�����
        sql = sql + "'" + TradeContext.I1USID           + "',"                              #����Ա
        sql = sql + "'0000000000',"                                                         #����Ա
        sql = sql + "'1',"                                                                  #�ն����ͣ�0-�����ϴ���1-��Χ�ϴ���
        sql = sql + "'" + TradeContext.I1FILENAME       + "',"                              #�����ļ�
        sql = sql + "'" + TradeContext.WorkDate         + "',"                              #����ʱ��
        sql = sql + "'" + TradeContext.WorkTime         + "',"                              #����ʱ��
        sql = sql + "'" + "00000000"                    + "',"                              #�ύ����
        sql = sql + "'" + "000000"                      + "',"                              #�ύʱ��
        sql = sql + "'" + TradeContext.I1TOTALNUM       + "',"                              #�ܱ���
        sql = sql + "'" + TradeContext.I1TOTALAMT       + "',"                              #�ܽ��
        sql = sql + "'" + "0"                           + "',"                              #�ɹ�����
        sql = sql + "'" + "0"                           + "',"                              #�ɹ����
        sql = sql + "'" + "0"                           + "',"                              #ʧ�ܱ���
        sql = sql + "'" + "0"                           + "',"                              #ʧ�ܽ��
        sql = sql + "'" + "10"                          + "',"                              #״̬(����)
        sql = sql + "'" + TradeContext.I1STARTDATE      + "',"                              #��Ч����
        sql = sql + "'" + TradeContext.I1ENDDATE        + "',"                              #ʧЧ����
        sql = sql + "'����->δ����',"                                                       #������Ϣ
        sql = sql + "'" + ""                            + "',"                              #��ע1
        sql = sql + "'0000',"                                                               #��ע2���������ţ�����Ĭ��0000
        sql = sql + "'1',"                                                                  #��ע3��Ų�����־��0-ʵʱ����1-���մ���
        sql = sql + "'',"                                                                   #��ע4
        sql = sql + "'" + ""                            + "')"                              #��ע5

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )

            #�ƶ��ļ���/data/ahxnb/dustĿ¼��
            TradeContext.Dustdir = os.environ['AFAP_HOME'] + '/data/ahxnb/dust'
            
            #20120917�޸ģ�ɾ����ũ�������ļ�
            #mv_cmd_str="mv " + TradeContext.pFileName + " " + TradeContext.Dustdir
            mv_cmd_str="mv " + TradeContext.dFileName + " " + TradeContext.Dustdir
            os.system(mv_cmd_str)

            return ExitSubTrade( '9000', '�Ǽ�������ҵ������Ϣʧ��')
        
        return True

    except Exception, e: 
        AfaLoggerFunc.tradeFatal( str(e) )
        #�ƶ��ļ���/data/ahxnb/dustĿ¼��
        TradeContext.Dustdir = os.environ['AFAP_HOME'] + '/data/ahxnb/dust'
        
        #20120917�޸ģ�ɾ����ũ�������ļ�
        #mv_cmd_str="mv " + TradeContext.pFileName + " " + TradeContext.Dustdir
        mv_cmd_str ="mv " + TradeContext.dFileName + " " + TradeContext.Dustdir
        os.system(mv_cmd_str)
        return ExitSubTrade( '9999', '�Ǽ�������ҵ������Ϣ�쳣')

#�ж����������Ƿ��Ѵ���
def ChkBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>�ж����������Ƿ��Ѵ���')

    try:
        sql = "SELECT BATCHNO,STATUS FROM ABDT_BATCHINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO    + "'" + " AND "        #ҵ����
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO   + "'" + " AND "        #��λ���
        sql = sql + "ZONENO="   + "'" + TradeContext.I1SBNO[0:4]+ "'" + " AND "        #��������
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO     + "'" + " AND "        #��������
        sql = sql + "INDATE="   + "'" + TradeContext.WorkDate   + "'" + " AND "        #ί������
        sql = sql + "FILENAME=" + "'" + TradeContext.I1FILENAME + "'" + " AND "        #�ļ�����
        sql = sql + "STATUS<>"  + "'" + "40"                    + "'"                  #״̬(����)

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql(sql)
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ������Ϣ���쳣' )

        if ( len(records) > 0 ):
            #�ж�״̬
            if ( str(records[0][1]) == "10" ):
                return ExitSubTrade( '9000', '�û����õ�λ���������ݽ����Ѿ�����,�����ٴ�����' )

            elif ( str(records[0][1]) == "88" ):
                return ExitSubTrade( '9000', '�û����õ�λ�����������ļ��Ѿ��������,�����ٴ�����' )

            else:
                return ExitSubTrade( '9000', '�û����õ�λ�����������ļ����ڴ���,���ܽ����������' )

        else:
            AfaLoggerFunc.tradeInfo('>>>û�з��ָû��������������������ļ�,��������')
            return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�ж����������Ƿ��Ѵ���,���ݿ��쳣' )
        

        
#######################################������###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************�Ѵ��������ļ�ת�������������ļ���ʽ��ʼ********************')
    
    #��ȡ�����ļ���Ϣ
    if ( not getBatchFile( "AHXNB" ) ):
        AfaLoggerFunc.tradeInfo("��ȡ�����ļ�ʧ��")
        sys.exit(-1)
    
    #ת������
    if ( not file_To_Batch_Pro( ) ):
        AfaLoggerFunc.tradeInfo("ת�������ļ���ʽʧ��")    
        sys.exit(-1)           
        
    AfaLoggerFunc.tradeInfo('********************�Ѵ��������ļ�ת�������������ļ���ʽ����********************')              
