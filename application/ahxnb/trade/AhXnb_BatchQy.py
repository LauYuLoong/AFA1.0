# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AhXnb_BatchQy.py
# �ļ���ʶ��
# ��    �ߣ�����̩  
# �޸�ʱ�䣺20110601
# ժ    Ҫ������ǩԼ��ת��Ϊ�籣��Ҫ�ĸ�ʽ
#
###############################################################################
import TradeContext                

TradeContext.sysType = 'ahxnb'

import AfaDBFunc,os,AfaLoggerFunc,sys,AfaFunc,AhXnbFunc,ConfigParser
from types import *

#=========================������==============================================
def file_Pro( ):
    try:
        
        #-----1����ѯδ����������ļ�
        sql = ""
        sql = sql + " select batchno,filename,workdate,busino,WorkTime,tellerno,filename"
        sql = sql + " from ahnx_file"
        sql = sql + " where status='0'"        #�ϴ��ɹ�
        sql = sql + " and filetype='4'"        #�����˺�ǩԼ
        
        AfaLoggerFunc.tradeInfo('>>>>>>>��ʼ��ѯAHNX_FILEԭ���ף�'+ str(sql))
        records = AfaDBFunc.SelectSql( sql )
                  
        if records==None:
            return ExitSubTrade("D0001" ,"��ѯAHNX_FILEʧ��")
        elif(len(records) == 0):
            return ExitSubTrade("D0001" ,"�޴���Ϣ")
            
        else:
            AfaLoggerFunc.tradeInfo("AHNX_FILE���еļ�¼����" +str(len(records)))
            for i in range(len(records)):
                #ί�к�
                TradeContext.batchno      = records[i][0]
                #ȡ������ǩԼ��ת�����ļ���
                TradeContext.FileName = records[i][1]
                #��������
                TradeContext.WorkDate     = records[i][2]
                #��λ���
                TradeContext.I1BUSINO     = records[i][3]
                #ʱ��
                TradeContext.WorkTime     = records[i][4]
                #��Ա��
                TradeContext.I1USID       = records[i][5]
                #ԭʼ�ļ���
                TradeContext.preFilename  = records[i][6]
                #�����������ɹ�������ת�����籣��Ҫ���ļ���ʽ
                if ( not CrtXnbFile_To_Sb( ) ):
                    continue
                
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return False

#------------------------------------------------------------------
#������ǩԼ�ļ�ת�����籣��Ҫ���ļ���ʽ
#------------------------------------------------------------------
def CrtXnbFile_To_Sb( ):
    try:
        #-----1����ȡ�ϴ�ǩԼ�ļ�
        TradeContext.sFileName = TradeContext.FileName
        TradeContext.dFileName = "NBQYFH_" + TradeContext.sFileName[7:-4] + "_S" + ".TXT"      #ǩԼ�ɹ���ϸ�ļ�
        TradeContext.dFileName_fail = "NBQYFH_" + TradeContext.sFileName[7:-4] + "_F" + ".TXT" #ǩԼʧ����ϸ�ļ�
        
        AfaLoggerFunc.tradeInfo("��ת��ǰ���ļ�:" + TradeContext.sFileName)
        AfaLoggerFunc.tradeInfo("��ת����(�ɹ�)���ļ�:" + TradeContext.dFileName)
        AfaLoggerFunc.tradeInfo("��ת����(ʧ��)���ļ�:" + TradeContext.dFileName_fail)
        
        if not os.path.exists(TradeContext.XNB_BDDIR + "/" + TradeContext.sFileName):
            return ExitSubTrade('D0001', "�����ļ�������")
            
        sfp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.sFileName,"r")
        dfp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.dFileName,"w")
        ffp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.dFileName_fail,"w")
        
        #----1.1,����-20120210 �ܱ���У��(<=15w)
        line = sfp.readline()
        fileCount = 0
        while( len(line) > 0 ):
            line = sfp.readline()
            fileCount = fileCount + 1
        sfp.close( )
        AfaLoggerFunc.tradeInfo('�������ϴ��ļ��ܱ���Ϊ��'+str(fileCount))
        
        if fileCount > 150000:
            AhXnbFunc.UpdateBatchInfo(TradeContext.batchno, "2", "�ϴ��ļ��ܱ�������15w��,�봦���������" )
            return False
        
        sfp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.sFileName,"r")
        #end
        
        #��ȡһ�� ��ȡ���ļ���ʽΪ���籣���|���֤|����|���ۺŻ򿨺�|
        linebuff = sfp.readline( )
        lineCount = 0
        
        #begin 20120209 �������� ɾ����ϸ������Ϣ�ļ�
        AhXnbFunc.DelProcmsgFile(TradeContext.batchno)
        flag = 0          #�����ʶ
        #end
        
        AfaLoggerFunc.tradeInfo( '�ϴ��ļ�����ǩԼ��ʼ������������' )
        
        while( len(linebuff)>0 ):
            lineCount = lineCount + 1
            swapbuff = linebuff.split("|")
            
            #20120614����̩�޸�ƾ֤�ſ��Բ���
            #----1.2,�ϴ��ļ���ʽУ��
            if len(swapbuff) != 5:
                #begin 20120209 �������� ���ϴ��ļ���ʽ���󣬸���ahxnb_file��������ϸ��Ϣд���ļ�                                                            
                AhXnbFunc.UpdateBatchInfo(TradeContext.batchno, "2", "�ϴ��ļ���ʽ����,ԭ�����ϸ��Ϣ" ,"�ϴ��ļ���" + str(lineCount) + "�и�ʽ[�ֶ���]����ȷ������")
                flag = 1
                #end
                
                linebuff = sfp.readline( )
                continue
            
            TradeContext.SBNO        = swapbuff[0].lstrip().rstrip()          #�籣���
            TradeContext.IDENTITYNO  = swapbuff[1].lstrip().rstrip()          #���֤
            TradeContext.NAME        = swapbuff[2].lstrip().rstrip()          #����
            if len(swapbuff[3].lstrip().rstrip()) == 23:                      #��Ϊ23λ
                #��
                TradeContext.ACCNO   = swapbuff[3].lstrip().rstrip()
                #TradeContext.VOUHNO  = swapbuff[4].lstrip().rstrip()          #ƾ֤��
                #20120614����̩�޸��������ƾ֤�Ź̶�Ϊ490123456789�������Ա����
                TradeContext.VOUHNO  = "490123456789"                         #ƾ֤��
            else:
                #��
                TradeContext.ACCNO   = swapbuff[3].lstrip().rstrip()
                TradeContext.VOUHNO  = TradeContext.ACCNO[8:18]               #ƾ֤��
            
            #begin 20120209 �������� ����ʽʧ�ܣ�������Ŀ������ļ��������鿴��ʽ
            if (flag == 1):
                linebuff = sfp.readline( )
                continue
            #end
            
            #----1.3ǩԼ
            #----1.3.1,���֤�ֶ�У��
            if len(TradeContext.IDENTITYNO) == 18:
                limitDate = TradeContext.IDENTITYNO[6:14]
            elif len(TradeContext.IDENTITYNO) == 15:
                limitDate = "19" + TradeContext.IDENTITYNO[6:12]
            else:
                failinfo = ""
                failinfo = failinfo + TradeContext.SBNO       + "|"     #�籣���
                failinfo = failinfo + TradeContext.NAME       + "|"     #����
                failinfo = failinfo + TradeContext.IDENTITYNO + "|"     #���֤
                failinfo = failinfo + "ǩԼ�ϴ��ļ���"+str(lineCount)+"���֤�ֶγ��Ȳ��ԣ�����"            #����˵��
                ffp.write(failinfo + "\n")
                
                linebuff = sfp.readline( )
                continue
            
            #----1.3.2���ͻ������ж�
            #----A���ͻ�<60����ǩԼ
            if limitDate > "19491231":
                if ( not CrtCustInfo( ) ):
                
                    #----A,ǩԼʧ�ܵ�д��ʧ����ϸ�ļ�
                    failinfo = ""
                    failinfo = failinfo + TradeContext.SBNO       + "|"     #�籣���
                    failinfo = failinfo + TradeContext.NAME       + "|"     #����
                    failinfo = failinfo + TradeContext.IDENTITYNO + "|"     #���֤
                    
                    if( TradeContext.existVariable('errorMsg') ):
                        failinfo = failinfo + TradeContext.errorMsg         #����˵��
                    else:
                        failinfo = failinfo + "�ÿͻ�����Э��ǩ��ʧ��"+ ""
                    
                    ffp.write(failinfo + "\n")
                    
                    linebuff = sfp.readline( )
                    continue
                
                #----B��ǩԼ�ɹ���д��ɹ���ϸ�ļ�
                lineinfo = ""
                lineinfo = lineinfo + TradeContext.SBNO       + "|"                 #�籣���
                lineinfo = lineinfo + TradeContext.NAME       + "|"                 #����
                lineinfo = lineinfo + TradeContext.IDENTITYNO + "|"                 #���֤
                lineinfo = lineinfo + TradeContext.ACCNO      + ""                  #�˺�
                dfp.write(lineinfo + "\n")
                
                linebuff = sfp.readline( )
            
            #----B���ͻ�>60���겻ǩԼ��д��ǩԼʧ����ϸ�ļ�
            else:
                failinfo = ""
                failinfo = failinfo + TradeContext.SBNO       + "|"     #�籣���
                failinfo = failinfo + TradeContext.NAME       + "|"     #����
                failinfo = failinfo + TradeContext.IDENTITYNO + "|"     #���֤
                failinfo = failinfo + "�ÿͻ��������60���꣬����ǩ������Э��"  + ""      #����˵��
                ffp.write(failinfo + "\n")
                
                linebuff = sfp.readline( )
            
        sfp.close( )
        dfp.close( )
        ffp.close( )
        AfaLoggerFunc.tradeInfo( '�ϴ��ļ�����ǩԼ����������������' )
        
        #begin 20120209 �������Ӵ����ʶΪʧ��ʱ��������һ����
        if (flag == 1):
            AfaLoggerFunc.tradeInfo("����"+TradeContext.batchno+"�ϴ��ļ���ʽ����,ԭ����д����ϸ�����ļ�")
            fileName1 = os.environ['AFAP_HOME'] + '/data/ahxnb/' + TradeContext.dFileName
            fileName2 = os.environ['AFAP_HOME'] + '/data/ahxnb/' + TradeContext.dFileName_fail
                    
            if ( os.path.exists(fileName1) and os.path.isfile(fileName1) ):
                cmdstr = "rm " + fileName1
                AfaLoggerFunc.tradeInfo('>>>ɾ������:' + cmdstr)
                os.system(cmdstr)
                
            if ( os.path.exists(fileName2) and os.path.isfile(fileName2) ):
                cmdstr = "rm " + fileName2
                AfaLoggerFunc.tradeInfo('>>>ɾ������:' + cmdstr)
                os.system(cmdstr)
                
            return False
        #end
        
        #----3,����ahxnb_file��
        if ( not AhXnbFunc.UpdateFileStatus(TradeContext.batchno,'1','����ǩԼ�ɹ�����ת���ɹ�����������',TradeContext.WorkTime) ):
            return False
        
        return True
    except Exception, e:
        sfp.close()
        dfp.close()
        ffp.close()
        return ExitSubTrade('D0001', str(e))

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
    TradeContext.PROTOCOLNO = TradeContext.WorkDate + TradeContext.agentSerialno
        
    #����Э�鲻���ڣ��ǼǸ���Э����Ϣ
    if ( not InsertCustInfo( ) ):
        return False
        
    return True
    
        
#------------------------------------------------------------------
#�жϸ���Э���Ƿ����
#------------------------------------------------------------------
def ChkCustInfo( ):

    #AfaLoggerFunc.tradeInfo('>>>�жϸ���Э���Ƿ����')

    try:
        sql = ""
        sql = "SELECT PROTOCOLNO,BUSIUSERNO,ACCNO FROM ABDT_CUSTINFO WHERE "
        sql = sql + "APPNO='AG1014' AND "                                                  #ҵ����
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO    + "'" + " AND ("        #��λ���
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.SBNO         + "'" + " OR "         #�̻��ͻ����
        sql = sql + "ACCNO="      + "'" + TradeContext.ACCNO        + "'" + " )AND "       #�����˺�
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                  #״̬

        AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ����Э����Ϣ�쳣' )
    
        if ( len(records) > 0 ):
            if records[0][1]== TradeContext.SBNO:
                return ExitSubTrade( '9000', '�ø���Э����籣����Ѿ���ע��,�����ٴν���ע��')
            if records[0][2]== TradeContext.ACCNO: 
                return ExitSubTrade( '9000', '�ø���Э����˺��Ѿ���ע��,�����ٴν���ע��')  
            else:
                return ExitSubTrade( '9000', '�ø���Э���Ѿ���ע��,�����ٴν���ע��')    
        return True


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�жϸ���Э����Ϣ�Ƿ�����쳣')

#------------------------------------------------------------------
#���Ӹ���Э����Ϣ
#------------------------------------------------------------------
def InsertCustInfo( ):

    #AfaLoggerFunc.tradeInfo('>>>���Ӹ���Э����Ϣ')

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

        sql = sql + "'AG1014',"                                      #ҵ����
        sql = sql + "'" + TradeContext.I1BUSINO        + "',"        #��λ���
        sql = sql + "'" + TradeContext.SBNO            + "',"        #�̻��ͻ����
        sql = sql + "'" + TradeContext.SBNO            + "',"        #�̻��ͻ�Ӧ�ñ��
        #20120614����̩�޸ģ���λ�ͻ���Ų�����ƾ֤�ţ�����ǩԼ��ƾ֤���ǹ̶���490123456789ҵ����+��λ���+���пͻ����Ϊ���������ظ�
        sql = sql + "'" + TradeContext.SBNO            + "',"        #���пͻ����
        sql = sql + "'49',"                                          #ƾ֤����
        sql = sql + "'" + TradeContext.VOUHNO          + "',"        #ƾ֤��
        sql = sql + "'" + TradeContext.ACCNO           + "',"        #���ڴ���ʺ�
        sql = sql + "'',"                                            #���ʺ�
        sql = sql + "'01',"                                          #����
        sql = sql + "'0',"                                           #�����޶�
        
        #begin 20111010--����--�޸� ���ֿۿ��־Ϊ��ΪB ��ʾȫ��ۿ� �۵�0���
        sql = sql + "'B',"                                           #���ֿۿ��־
        #end
        
        sql = sql + "'" + TradeContext.PROTOCOLNO      + "',"        #Э����
        sql = sql + "'" + TradeContext.WorkDate        + "',"        #ǩԼ����(��ͬ����)
        sql = sql + "'" + TradeContext.WorkDate        + "',"        #��Ч����
        sql = sql + "'20990101',"                                    #ʧЧ����
        sql = sql + "'0',"                                           #������֤��־
        sql = sql + "'" + "****************"           + "',"        #����
        sql = sql + "'0',"                                           #֤����֤��־
        sql = sql + "'01',"                                          #֤������
        sql = sql + "'" + TradeContext.IDENTITYNO      + "',"        #֤������
        sql = sql + "'0',"                                           #������֤��־
        sql = sql + "'" + TradeContext.NAME            + "',"        #�ͻ�����
        sql = sql + "'',"                                            #��ϵ�绰
        sql = sql + "'',"                                            #��ϵ��ַ
        sql = sql + "'',"                                            #�ʱ�
        sql = sql + "'',"                                            #��������
        sql = sql + "'1',"                                           #״̬
        sql = sql + "'" + TradeContext.I1BUSINO[0:4]   + "',"        #������
        sql = sql + "'" + TradeContext.I1BUSINO[0:10]  + "',"        #�����(��������)
        sql = sql + "'" + TradeContext.I1USID          + "',"        #��Ա��
        sql = sql + "'" + TradeContext.WorkDate        + "',"        #¼������
        sql = sql + "'" + TradeContext.WorkTime        + "',"        #¼��ʱ��
        sql = sql + "'',"                                            #��ע1
        sql = sql + "'',"                                            #��ע2
        sql = sql + "'',"                                            #��ע3
        sql = sql + "'AHXNB',"                                       #��ע4��AHXNB��ʾ��Э����ͨ����ũ������ʱ�������룩
        sql = sql + "'')"                                            #��ע5

        #AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            #AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '���Ӹ���Э����Ϣʧ��')
            
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '���Ӹ���Э����Ϣ�쳣')
        
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
        #AfaLoggerFunc.tradeInfo( errorMsg )

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
               
#######################################������###########################################
if __name__=='__main__':

    AfaLoggerFunc.tradeInfo('********************����ת����ʽ��ʼ********************')
    
    #��ȡ�����ļ���Ϣ
    if ( not getBatchFile( "AHXNB" ) ):
        sys.exit(-1)
    
    #ת������
    file_Pro( )
    
    AfaLoggerFunc.tradeInfo('********************����ת����ʽ����********************')
