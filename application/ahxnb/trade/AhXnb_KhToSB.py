# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AhXnb_KhToSB.py
# �ļ���ʶ��
# ��    �ߣ�����̩
# ժ    Ҫ��ת�����������ļ�Ϊ�籣��Ҫ�ĸ�ʽ
#
###############################################################################
import TradeContext

TradeContext.sysType = 'ahxnb'

import AfaDBFunc,os,AfaLoggerFunc,sys,AfaFunc,AhXnbFunc,ConfigParser
from types import *

#=========================������==============================================
def file_Pro( ):
    try:
        #-----1,��ѯδ����������ļ�
        sql = ""
        sql = sql + "select batchno,swapfilename,workdate,busino,WorkTime,tellerno,filename"
        sql = sql + " from ahnx_file"
        sql = sql + " where status='4'"      #�����ϴ��ļ�ת���ɹ�
        sql = sql + " and filetype='2'"      #��������ǰ
        
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
                #ȡ��������������ת�����ļ���
                TradeContext.swapFileName = records[i][1]
                AfaLoggerFunc.tradeInfo( '��ת�����ļ���'+ TradeContext.swapFileName )
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
#�Ѻ��ķ��ص����������ļ�ת�����籣��Ҫ���ļ���ʽ
#------------------------------------------------------------------
def CrtXnbFile_To_Sb( ):
    AfaLoggerFunc.tradeInfo( '�Ѻ��ķ��ص����������ļ�ת�����籣�ļ�������ʼ' )
    
    try:
        #----2�������ļ�ת���籣�ļ�
        TradeContext.sFileName = TradeContext.swapFileName
        
        #begin 20120209 �����޸�
        TradeContext.dFileName = "YHKHFK_" + TradeContext.preFilename[7:-4] + "_S" + ".TXT"      #�����ɹ���ϸ�ļ�
        TradeContext.dFileName_fail = "YHKHFK_" + TradeContext.preFilename[7:-4] + "_F" + ".TXT" #����ʧ����ϸ�ļ�
        #end
        
        if not os.path.exists(TradeContext.XNB_BDDIR + "/" + TradeContext.sFileName):
            return ExitSubTrade('D0001', "�����ļ�������")
            
        sfp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.sFileName,"r")
        dfp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.dFileName,"w")
        ffp = open(TradeContext.XNB_BDDIR + "/" + TradeContext.dFileName_fail,"w")
        
        AfaLoggerFunc.tradeInfo("��ת�����ļ�:" + TradeContext.sFileName)
        AfaLoggerFunc.tradeInfo("�����ļ�(�ɹ���ϸ):" + TradeContext.dFileName)
        AfaLoggerFunc.tradeInfo("�����ļ�(ʧ����ϸ):" + TradeContext.dFileName_fail)
        
        #��ȡһ�� ��ȡ���ļ���ʽΪ�����0|֤������1|���֤2|����3|���4|2(5)|������6|�ɹ�7|���ۺ�8|ƾ֤��9|����10|�ͻ���11|
        linebuff = sfp.readline( )
        lineCount = 0
        
        AfaLoggerFunc.tradeInfo("�����ļ�ת����ʼ������������")
        
        while( len(linebuff)>0 ):
            #������һ�еĻ�����Ϣ
            if lineCount == 0:
                linebuff = sfp.readline( )
                lineCount = lineCount + 1
                continue
            
            swapbuff = linebuff.split("|")
            
            #----2.1��BC�ļ���ʽУ��
            if len(swapbuff) != 13:
                failinfo = ""
                failinfo = "BC�ļ���" + str(lineCount+1) + "�����ݸ�ʽ���Ϸ�,����������" + str(len(swapbuff)) + "��"
                ffp.write(failinfo + "\n")
                
                linebuff = sfp.readline( )
                lineCount = lineCount + 1
                continue
            
            TradeContext.IDENTITYNO  = swapbuff[2].lstrip().rstrip()          #���֤
            TradeContext.NAME        = swapbuff[3].lstrip().rstrip()          #����
            if len(swapbuff[8].lstrip().rstrip()) != 0:
                #��
                TradeContext.ACCNO   = swapbuff[8].lstrip().rstrip()
                TradeContext.VOUHNO  = swapbuff[9].lstrip().rstrip()          #ƾ֤��
            else:
                #��
                TradeContext.ACCNO   = swapbuff[10].lstrip().rstrip()
                TradeContext.VOUHNO  = TradeContext.ACCNO[8:18]               #ƾ֤��
            
            #----2.2�������ɹ�ʧ���ж�
            if( (len(swapbuff[8].strip()) != 0 and len(swapbuff[9].strip()) != 0) or \
                (len(swapbuff[10].strip()) != 0) ):
                
                selectSql = " select SBNO from AHXNB_MAC "
                updateSql = " update AHXNB_MAC set STATUS='0', ACCNO='" + TradeContext.ACCNO + "', WORKDATE='" + TradeContext.WorkDate + "'"
                whereSql  = " where IDENTITYNO = '" + TradeContext.IDENTITYNO + "' and NAME = '" + TradeContext.NAME + "'"
                
                sqlcmd = updateSql + whereSql
                updateRet = AfaDBFunc.UpdateSqlCmt( sqlcmd )
                
                if updateRet <  0:
                    failinfo = ""
                    failinfo = failinfo + "�籣���δ֪"         + "|"      #�籣���
                    failinfo = failinfo + TradeContext.NAME       + "|"      #����
                    failinfo = failinfo + TradeContext.IDENTITYNO + "|"      #���֤
                    failinfo = failinfo + "���Ŀ����ɹ����˺�Ϊ��"+TradeContext.ACCNO+"��������MAC��ʧ��"+ ""    #����˵��
                    ffp.write(failinfo + "\n")
                    
                    linebuff = sfp.readline( )
                    lineCount = lineCount + 1
                    continue
                    
                sqlcmd = selectSql + whereSql
                selectRet = AfaDBFunc.SelectSql( sqlcmd )
                
                if selectRet == None:
                    linebuff = sfp.readline( )
                    lineCount = lineCount + 1
                    continue
                    
                elif len(selectRet) == 0:
                    failinfo = ""
                    failinfo = failinfo + "�籣���δ֪"     + "|"      #�籣���
                    failinfo = failinfo + TradeContext.NAME       + "|"      #����
                    failinfo = failinfo + TradeContext.IDENTITYNO + "|"      #���֤
                    failinfo = failinfo + "���Ŀ����ɹ����˺�Ϊ��"+TradeContext.ACCNO+"����MAC����û�ж�Ӧ�Ŀ�������"+ ""    #����˵��
                    ffp.write(failinfo + "\n")
                    
                    linebuff = sfp.readline( )
                    lineCount = lineCount + 1
                    continue
                    
                else:
                    TradeContext.SBNO = selectRet[0][0].lstrip().rstrip()
                
                #----2.2.3������Э��ǩ��
                if len(TradeContext.IDENTITYNO) == 18:
                    limitDate = TradeContext.IDENTITYNO[6:14]
                elif len(TradeContext.IDENTITYNO) == 15:
                    limitDate = "19" + TradeContext.IDENTITYNO[6:12]
                    
                #----A��<60����ͻ�
                if limitDate > "19491231":
                    if ( not CrtCustInfo( ) ):
                        failinfo = ""
                        failinfo = failinfo + TradeContext.SBNO       + "|"      #�籣���
                        failinfo = failinfo + TradeContext.NAME       + "|"      #����
                        failinfo = failinfo + TradeContext.IDENTITYNO + "|"      #���֤
                        
                        if( TradeContext.existVariable('errorMsg') ):
                            failinfo = failinfo + '���Ŀ����ɹ�,�˺�Ϊ��'+TradeContext.ACCNO+'����'+TradeContext.errorMsg         #����˵��
                        else:
                            failinfo = failinfo + "���Ŀ����ɹ�,�˺�Ϊ��"+TradeContext.ACCNO+"�����ÿͻ�����Э��ǩ��ʧ��"+ ""
                            
                        ffp.write(failinfo + "\n")
                        
                        lineCount = lineCount + 1
                        linebuff = sfp.readline( )
                        continue
                
                #----2.2.4����ǩԼ�ɹ��Ŀͻ���Ϣд������ļ�
                lineinfo = ""
                lineinfo = lineinfo + TradeContext.SBNO       + "|"                 #�籣���
                lineinfo = lineinfo + TradeContext.NAME       + "|"                 #����
                lineinfo = lineinfo + TradeContext.IDENTITYNO + "|"                 #���֤
                lineinfo = lineinfo + TradeContext.ACCNO      + ""                  #�˺�
                dfp.write(lineinfo + "\n")

                linebuff = sfp.readline( )
                lineCount = lineCount + 1
                continue
                
            else:
                selectSql = " select SBNO from AHXNB_MAC "
                whereSql  = " where IDENTITYNO = '" + TradeContext.IDENTITYNO + "' and NAME = '" + TradeContext.NAME + "'"
                
                sqlcmd = selectSql + whereSql
                selectRet = AfaDBFunc.SelectSql( sqlcmd )
                
                if selectRet == None:
                    linebuff = sfp.readline( )
                    lineCount = lineCount + 1
                    continue
                    
                elif len(selectRet) == 0:
                    failinfo = ""
                    failinfo = failinfo + "�籣���δ֪" + "|"      #�籣���
                    failinfo = failinfo + TradeContext.NAME       + "|"      #����
                    failinfo = failinfo + TradeContext.IDENTITYNO + "|"      #���֤
                    failinfo = failinfo + "���Ŀ���ʧ�ܣ���ѯMAC���޴˼�¼"    #����˵��
                    ffp.write(failinfo + "\n")
                    
                else:
                    TradeContext.SBNO = selectRet[0][0].lstrip().rstrip()
                    
                    failinfo = ""
                    failinfo = failinfo + TradeContext.SBNO       + "|"      #�籣���
                    failinfo = failinfo + TradeContext.NAME       + "|"      #����
                    failinfo = failinfo + TradeContext.IDENTITYNO + "|"      #���֤
                    failinfo = failinfo + "���Ŀ���ʧ�ܣ����ķ�����Ϣ"+swapbuff[7].strip()     + ""       #����˵��
                    ffp.write(failinfo + "\n")
                    
                lineCount = lineCount + 1
                linebuff = sfp.readline( )
                
        sfp.close( )
        dfp.close( )
        ffp.close( )
        AfaLoggerFunc.tradeInfo("�����ļ�ת������������������")
        
        #----3,����ahxnb_file��
        if ( not AhXnbFunc.UpdateFileStatus(TradeContext.batchno,'1','����ת���ɹ�����������',TradeContext.WorkTime) ):
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
        sql = sql + "BUSINO="     + "'" + TradeContext.I1BUSINO    + "'" + " AND ("       #��λ���
        sql = sql + "BUSIUSERNO=" + "'" + TradeContext.SBNO         + "'" + " OR "         #�̻��ͻ����
        sql = sql + "ACCNO="      + "'" + TradeContext.ACCNO        + "'" + " )AND "       #�����˺�
        sql = sql + "STATUS="     + "'" + "1"                       + "'"                  #״̬

        #AfaLoggerFunc.tradeInfo( sql )

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            #AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ����Э����Ϣ�쳣' )
        
        if ( len(records) > 0 ):
            #201208 �м�ҵ���Ż� llj �ж����籣����ظ��������˺��ظ�
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
        sql = sql + "'" + TradeContext.SBNO            + "',"        #���пͻ���ţ�201208 �м�ҵ���Ż���Ϊʹ���籣��ţ�
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
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
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
        AfaLoggerFunc.tradeInfo( errorMsg )

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
