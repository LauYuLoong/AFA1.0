###############################################################################
# -*- coding: gbk -*-
# ժ    Ҫ����ũ������ҵ��
# ��ǰ�汾��1.0
# ��    �ߣ�������
# ������ڣ�2010��12��15��
###############################################################################
import AfaDBFunc,AfaLoggerFunc,AhXnbFunc,TradeContext
import os
from types import *

#=====================����ʡ��ũ��������ҵ����==============================================
def TrxMain( ):

    AfaLoggerFunc.tradeInfo('---------����ʡ�����������------------')
    
    #----1����������У��
    if TradeContext.I1FTPTYPE in ("0","1"):
        #�жϵ�λЭ���Ƿ���Ч��ֻ�������������۲�У�鵥λЭ�飩
        if ( not AhXnbFunc.ChkUnitInfo( ) ):
            return False
    
    #ת��������������ļ�ʱ����Ҫ��У��
    if TradeContext.I1FTPTYPE != "3":
        #�ж����������Ƿ��Ѵ���
        if (  not ChkBatchInfo( ) ):
            return False
    
    #----2���������봦��
    #��ȡ�����ļ���Ϣ
    if ( not AhXnbFunc.getBatchFile( "AHXNB" ) ):
        return False
    
    #----A��������������-У���ϴ��ļ��Ƿ����ϴ�
    if TradeContext.I1FTPTYPE in ("0","1"):
        TradeContext.swapFile=" "
        filePath = TradeContext.XNB_BSDIR + "/" + TradeContext.I1FILENAME
        if not os.path.exists(filePath):
            return ExitSubTrade( "E0001","�����ļ������ڣ���ȷ���ļ��Ƿ��ϴ�" ) 
        pass
        
    #----B����������-�ϴ��ļ�תתBC�ļ�
    elif TradeContext.I1FTPTYPE == "2":
        if ( not CrtXnbFile( ) ):
            return False
    
    #----XX �������ļ�ת�����⴦��-ֻ���������״̬
    elif TradeContext.I1FTPTYPE == "3":
        if ( not AhXnbFunc.UpdateFileStatus( TradeContext.I1BATCHNO,'4', '���ڴ�������������ļ�����ȴ�...', TradeContext.WorkTime) ):
            return False
        #ת���ɹ���Ӧ��ֱ�ӷ��أ������ߺ�������
        TradeContext.O1AFAPDATE = TradeContext.WorkDate
        TradeContext.O1AFAPTIME = TradeContext.WorkTime
        return ExitSubTrade('0000', '���׳ɹ�')
    
    #20110601����̩�޸� ǰ̨��Ӳ�������Ϊ4 ��ʾ�Ѿ���������ֻ������ǩԼ����
    #begin
    elif TradeContext.I1FTPTYPE == "4":
        if ( not CrtBatchNo( ) ): 
            return False          
        
        if ( not inserXnbFile_for_4() ):
            return False
        #����ahnx_file��ɹ���Ӧ��ֱ�ӷ��أ������ߺ�������
        TradeContext.O1AFAPDATE = TradeContext.WorkDate
        TradeContext.O1AFAPTIME = TradeContext.WorkTime
        return ExitSubTrade('0000', '���׳ɹ�')
    else:
        return ExitSubTrade( "E0001","û�иò�������" )
    
    #end
            
    #����ί�к�
    if ( not CrtBatchNo( ) ):
        return False
    
    #�Ǽ������ļ��ǼǱ�AHNX_FILE
    if ( not inserXnbFile( ) ):
        return False
    TradeContext.O1BATCHNO  = TradeContext.BATCHNO
    TradeContext.O1AFAPDATE = TradeContext.WorkDate
    TradeContext.O1AFAPTIME = TradeContext.WorkTime
    TradeContext.O1FILENAME = TradeContext.swapFile
    TradeContext.errorCode  = "0000"
    TradeContext.errorMsg   = "���׳ɹ�"
    AfaLoggerFunc.tradeInfo('---------����ʡ���������˳�------------')
    
    return ExitSubTrade('0000', '���׳ɹ�')

#------------------------------------------------------------------
#���������ļ���ʽת��
#------------------------------------------------------------------
def CrtXnbFile( ):
    #��ȡһ��3λ�����кţ�����ƴ���ͺ��ĵĿ����ļ���
    CrtSequence( )
    
    try:
        #----2�������ļ�ת��BC�ļ�
        TradeContext.sFileName = TradeContext.XNB_BSDIR + "/" + TradeContext.I1FILENAME
        #���ͺ������������ļ���BC+10������+8����+3���.TXT
        TradeContext.swapFile  = "BC" + TradeContext.I1SBNO + TradeContext.WorkDate + TradeContext.sequenceNo + ".TXT"
        TradeContext.dFileName = TradeContext.XNB_BDDIR + "/" + TradeContext.swapFile
        
        AfaLoggerFunc.tradeInfo(TradeContext.sFileName)
        if not os.path.exists(TradeContext.sFileName):
            return ExitSubTrade( "E0001", "�����ļ�������" )
            
        sfp = open(TradeContext.sFileName,"r")
        dfp = open(TradeContext.dFileName,"w")
        
        line = sfp.readline()
        fileCount = 0
        while( len(line) > 0 ):
            line = sfp.readline()
            fileCount = fileCount + 1
        AfaLoggerFunc.tradeInfo("������������" + str(fileCount))
        sfp.close( )
        
        #----2.1�����Ķ��ڵ������������������ܳ���500��
        if fileCount > 500:
            return ExitSubTrade("E0001","�������������������ܳ���500��")
            
        sfp = open(TradeContext.sFileName,"r")
        #д�����:�ܱ���|���|��ת��־ 0-�ֽ�|�������� 0428-��˽����|||����01|�Ƿ�ͨ��ͨ��1-ͨ��|
        lineinfo = str(fileCount) + "|0.00|0|0428|||01|1|"
        dfp.write(lineinfo + "\n")
        
        #��ȡһ��
        linebuff = sfp.readline( )
        #д���ļ������
        sequenceNO = 0
        
        #begin 20120209 �������� ɾ����ϸ������Ϣ�ļ�
        AhXnbFunc.DelProcmsgFile(TradeContext.I1FILENAME[:-4])
        flag = 0           #�����ʶ
        #end
        
        AfaLoggerFunc.tradeInfo('�����ļ�ת��BC�ļ���ʼ������������')
        
        while( len(linebuff)>0 ):
            sequenceNO = sequenceNO + 1
            swapbuff = linebuff.split("|")
            
            if len(swapbuff) !=5:
                #----2.2�������ļ���ʽУ��
                #begin 20120209 �������� ���ϴ��ļ���ʽ����,����ϸ��Ϣд���ļ�
                AhXnbFunc.WriteInfo(TradeContext.I1FILENAME[:-4] ,"�ϴ��ļ���" + str(sequenceNO) + "�и�ʽ[�ֶ�]����ȷ������")
                flag = 1
                #end
                
                linebuff = sfp.readline( )
                continue
                
            TradeContext.SBNO        = swapbuff[0].lstrip().rstrip()          #�籣���
            TradeContext.NAME        = swapbuff[1].lstrip().rstrip()          #����
            TradeContext.IDENTITYNO  = swapbuff[2].lstrip().rstrip()          #���֤
            TradeContext.XZQHNO      = swapbuff[3].lstrip().rstrip()          #������������
            TradeContext.XZQHNAME    = swapbuff[4].lstrip().rstrip()          #������������
            
            #begin 20120209 �������� ����ʽʧ�ܣ�������Ŀ�������ļ��������鿴��ʽ
            if (flag == 1):
                linebuff = sfp.readline( )
                continue
            #end
            
            #----2.3���ϴ��ļ���Ϣд��BC�ļ�
            #ǰ̨�ṩ�����������ļ���ʽ:���|֤������(01-���֤)|���֤|����|���|2| | | |||
            lineinfo =            str(sequenceNO)          + "|"
            lineinfo = lineinfo + "01"                     + "|"
            lineinfo = lineinfo + TradeContext.IDENTITYNO  + "|"
            lineinfo = lineinfo + TradeContext.NAME        + "|"
            lineinfo = lineinfo + "0.00"                   + "|"
            lieninfo = lineinfo + "2"                      + "|"
            lineinfo = lineinfo + ""                       + "|"
            lineinfo = lineinfo + ""                       + "|"
            lineinfo = lineinfo + ""                       + "|"
            lineinfo = lineinfo + ""                       + "|"
            lineinfo = lineinfo + ""                       + "|"
            
            dfp.write(lineinfo + "\n")
            
            #----2.4���Ǽ���ϸ��Ϣ
            if not insertXnbMac( ):
                return False
            
            linebuff = sfp.readline( )
            
        sfp.close( )
        dfp.close( )
        AfaLoggerFunc.tradeInfo('�����ļ�ת��BC�ļ�����������������')
        
        #begin 20120209 �������Ӵ����ʶΪʧ��ʱ��������һ����
        if (flag == 1):
            AfaLoggerFunc.tradeInfo( "����"+TradeContext.I1FILENAME[:-4]+"�ϴ��ļ���ʽ����,ԭ����д����ϸ�����ļ�")
            TradeContext.errorCode,TradeContext.errorMsg = '9000','�ϴ��ļ���ʽ����,ԭ����д����ϸ�����ļ�'
            
            if ( os.path.exists(TradeContext.dFileName) and os.path.isfile(TradeContext.dFileName) ):
                cmdstr = "rm " + TradeContext.dFileName
                AfaLoggerFunc.tradeInfo('>>>ɾ������:' + cmdstr)
                os.system(cmdstr)
            
            return False
        #end
        
        return True
    except Exception, e:
        sfp.close()
        dfp.close()
        return ExitSubTrade('E0001', str(e))
        
#------------------------------------------------------------------
#�����ļ��ǼǱ�AHNX_FILE 
#------------------------------------------------------------------
def inserXnbFile( ):
    
    sql = ""
    sql = sql + "insert into AHNX_FILE("
    sql = sql + "BATCHNO,"
    sql = sql + "FILENAME,"
    sql = sql + "SWAPFILENAME,"
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
    sql = sql + "'" + TradeContext.swapFile    + "',"             #ת������ļ���
    sql = sql + "'" + TradeContext.WorkDate    + "',"             #�Ǽ�����
    sql = sql + "'0',"                                            #״̬(0-������1-����ɹ�)
    sql = sql + "'�ϴ��ɹ��������ļ��ȴ�������...',"              #������Ϣ����
    sql = sql + "'" + TradeContext.WorkDate    + "',"             #��������
    sql = sql + "'" + TradeContext.I1APPNO     + "',"             #ҵ����
    sql = sql + "'" + TradeContext.I1BUSINO    + "',"             #��λ���
    sql = sql + "'" + TradeContext.I1TOTALNUM  + "',"             #�ܱ���
    sql = sql + "'" + TradeContext.I1TOTALAMT  + "',"             #�ܽ��
    sql = sql + "'" + TradeContext.I1FTPTYPE   + "',"             #�ļ����ͣ�0-����������1-�������ۣ�2-��������)
    sql = sql + "'" + TradeContext.I1SBNO      + "',"             #������
    sql = sql + "'" + TradeContext.I1USID      + "',"             #��Ա��
    sql = sql + "'" + TradeContext.I1STARTDATE + "',"             #��Ч����
    sql = sql + "'" + TradeContext.I1ENDDATE   + "',"             #ʧЧ����
    sql = sql + "'" + TradeContext.WorkTime    + "',"             #����ʱ��
    sql = sql + "'',"                                             #����1
    sql = sql + "'',"                                             #����2
    sql = sql + "'',"                                             #����3
    sql = sql + "'')"                                             #����4
    
    AfaLoggerFunc.tradeInfo( "�����ļ��Ǽǣ�" + sql )
    
    ret = AfaDBFunc.InsertSqlCmt(sql)
    
    if ret < 0:
        return ExitSubTrade('D0001', "��������ʧ��")
        
    return True
    
#------------------------------------------------------------------
#����ũ��������AHXNB_MAC�еǼ�����
#------------------------------------------------------------------
def insertXnbMac( ):

    sql = ""
    sql = sql + " select SBNO,NAME,IDENTITYNO,XZQHNAME,XZQHNO,ACCNO"
    sql = sql + " from AHXNB_MAC "
    sql = sql + " where SBNO = '" + TradeContext.SBNO  + "'" #�籣���
    
    #AfaLoggerFunc.tradeInfo( '��������У��sql��' + sql )
    result = AfaDBFunc.SelectSql( sql )
    
    if result == None:
        return ExitSubTrade('D0001', "У����������ʧ�ܣ����ݿ��쳣")
    elif len(result) > 0:
        
        #���� 20111116 start   ���жϲ�ѯ����ٴ���
        #20110620 ����̩ �޸�  ����ÿͻ��Ѿ���ahxnb_mac���еǼ�ֱ�ӷ���True
        #return True
        #return ExitSubTrade('D0001', "�ÿͻ��Ѿ��Ǽǹ�������������¼")
        
        flag = ( len(result[0][5].strip()) == 0 )
        
        #�˺�Ϊ�գ�ɾ��ԭ��¼�������¼�¼
        if( flag ):
            sql2 = ""
            sql2 = sql2 + "delete"
            sql2 = sql2 + " from ahxnb_mac"
            sql2 = sql2 + " where sbno = '" + TradeContext.SBNO + "'"
            
            #AfaLoggerFunc.tradeInfo( 'ɾ��ϵͳռ���籣���sql2��' + sql2 )
            result2 = AfaDBFunc.DeleteSqlCmt( sql2 )
            
            if( result2 <= 0 ):
                #AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                return ExitSubTrade( '9000', 'ɾ��ϵͳռ���籣���ʧ��')
            
        #�˺Ų�Ϊ������
        else:
            return True
        #end
        
        
    sql = ""
    sql = sql + "insert into AHXNB_MAC("
    sql = sql + "SBNO,"
    sql = sql + "NAME,"
    sql = sql + "IDENTITYNO,"
    sql = sql + "XZQHNO,"
    sql = sql + "XZQHNAME,"
    sql = sql + "ACCNO,"
    sql = sql + "STATUS,"
    sql = sql + "WORKDATE,"
    sql = sql + "BRNO,"
    sql = sql + "NOTE1,"
    sql = sql + "NOTE2,"
    sql = sql + "NOTE3,"
    sql = sql + "NOTE4)"
    sql = sql + " values("
    sql = sql + "'" + TradeContext.SBNO       + "',"             #�籣���
    sql = sql + "'" + TradeContext.NAME       + "',"             #����
    sql = sql + "'" + TradeContext.IDENTITYNO + "',"             #���֤
    sql = sql + "'" + TradeContext.XZQHNO     + "',"             #������������
    sql = sql + "'" + TradeContext.XZQHNAME   + "',"             #������������
    sql = sql + "'',"                                            #�����˺�
    sql = sql + "'1',"                                           #״̬(0-�ѿ�����1-δ������2-��ע��)
    sql = sql + "'',"                                            #��������
    sql = sql + "'',"                                            #��������
    sql = sql + "'',"                                            #����1
    sql = sql + "'',"                                            #����2
    sql = sql + "'',"                                            #����3
    sql = sql + "'')"                                            #����4
    
    #AfaLoggerFunc.tradeInfo( "���������Ǽǣ�" + sql )
    
    ret = AfaDBFunc.InsertSqlCmt(sql)
    
    if ret < 0:
        
        return ExitSubTrade('D0001', "��������ʧ��")
        
    return True
    

#------------------------------------------------------------------
#�ж����������Ƿ��Ѵ���
#------------------------------------------------------------------
def ChkBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>�ж����������Ƿ��Ѵ���')

    try:
        sql = "SELECT BATCHNO,STATUS FROM AHNX_FILE WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO     + "'" + " AND "        #ҵ����
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO    + "'" + " AND "        #��λ���
        sql = sql + "WORKDATE=" + "'" + TradeContext.WorkDate    + "'" + " AND "        #ί������
        sql = sql + "FILENAME=" + "'" + TradeContext.I1FILENAME  + "'" + " AND "        #�����ļ�
        sql = sql + "STATUS<>"  + "'" + "2"                      + "'"                  #״̬(����)

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql(sql)
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ������Ϣ���쳣' )

        if ( len(records) > 0 ):
            #�ж�״̬
            if ( str(records[0][1]) in ('0','3','4')  ):
                return ExitSubTrade( '9000', '�û����õ�λ��������������ļ����ڴ�����,���ܽ����������' )

            elif ( str(records[0][1]) == "1" ):
                return ExitSubTrade( '9000', '�û����õ�λ��������������ļ��Ѿ��������,�����ٴ�����' )

        else:
            AfaLoggerFunc.tradeInfo('>>>û�з��ָû��������������������ļ�,��������')
            return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�ж����������Ƿ��Ѵ���,���ݿ��쳣' )
        
#------------------------------------------------------------------
#����ί�к�
#------------------------------------------------------------------
def CrtBatchNo( ):

    AfaLoggerFunc.tradeInfo('>>>��������ί�к�')

    try:
        sqlStr = "SELECT NEXTVAL FOR ABDT_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '����ί�к��쳣' )

        #���κ�
        TradeContext.BATCHNO = TradeContext.WorkDate + str(records[0][0]).rjust(8, '0')

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '����ί�к��쳣' )
        
        
#------------------------------------------------------------------
#����һ��3λ�����
#------------------------------------------------------------------
def CrtSequence( ):
    
    try:
        sqlStr = "SELECT NEXTVAL FOR AHXNB_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '�������к��쳣' )
        AfaLoggerFunc.tradeInfo( "���кţ�" + str(records[0][0]) )
        
        #���к�
        TradeContext.sequenceNo = str(records[0][0]).rjust(3,'0')
        
        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '����ί�к��쳣' )

#------------------------------------------------------------------
#20110601����̩�޸����
#�ǼǱ�AHNX_FILE��ֻ�Ǽǲ�������Ϊ4�ļ�¼����ֻ������ǩԼ�ļ�¼ 
#------------------------------------------------------------------
#begin
def inserXnbFile_for_4( ):
    
    sql = ""
    sql = sql + "insert into AHNX_FILE("
    sql = sql + "BATCHNO,"
    sql = sql + "FILENAME,"
    sql = sql + "SWAPFILENAME,"
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
    sql = sql + "'',"                                             #ת������ļ���
    sql = sql + "'" + TradeContext.WorkDate    + "',"             #�Ǽ�����
    sql = sql + "'0',"                                            #״̬(0-������1-����ɹ�)
    sql = sql + "'�ϴ��ɹ�,�ȴ�����ǩԼ...',"                     #������Ϣ����
    sql = sql + "'" + TradeContext.WorkDate    + "',"             #��������
    sql = sql + "'" + TradeContext.I1APPNO     + "',"             #ҵ����
    sql = sql + "'" + TradeContext.I1BUSINO    + "',"             #��λ���
    sql = sql + "'" + TradeContext.I1TOTALNUM  + "',"             #�ܱ���
    sql = sql + "'" + TradeContext.I1TOTALAMT  + "',"             #�ܽ��
    sql = sql + "'" + TradeContext.I1FTPTYPE   + "',"             #�ļ����ͣ�0-����������1-�������ۣ�2-����������3-�������ļ�ת����4-����ǩԼ)
    sql = sql + "'" + TradeContext.I1SBNO      + "',"             #������
    sql = sql + "'" + TradeContext.I1USID      + "',"             #��Ա��
    sql = sql + "'" + TradeContext.I1STARTDATE + "',"             #��Ч����
    sql = sql + "'" + TradeContext.I1ENDDATE   + "',"             #ʧЧ����
    sql = sql + "'" + TradeContext.WorkTime    + "',"             #����ʱ��
    sql = sql + "'',"                                             #����1
    sql = sql + "'',"                                             #����2
    sql = sql + "'',"                                             #����3
    sql = sql + "'')"                                             #����4
    
    AfaLoggerFunc.tradeInfo( "�����ļ��Ǽǣ�" + sql )
    
    ret = AfaDBFunc.InsertSqlCmt(sql)
    
    if ret < 0:
        return ExitSubTrade('D0001', "��������ʧ��")
        
    return True
#end

        
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
