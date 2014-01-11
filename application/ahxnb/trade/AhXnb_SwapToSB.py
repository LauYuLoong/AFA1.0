# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�AhXnb_SwapToSB.py
# �ļ���ʶ��
# ��    �ߣ�����̩
# ժ    Ҫ��ת���������۴����ļ�Ϊ�籣��Ҫ�ĸ�ʽ
#
###############################################################################
import TradeContext

TradeContext.sysType = 'ahxnb'     
                                   
import AfaDBFunc,os,AfaLoggerFunc
import AfaAdminFunc,sys,AfaFtpFunc
from types import *

#=========================������==============================================
def file_Pro( ):
    try:
        #----1����ѯδ����������ļ�
        sql = ""
        sql = sql + "select appno,busino,applydate,filetype ,filename,batchno,swapfilename"
        sql = sql + " from ahnx_file"
        sql = sql + " where status='3'"            #���������ϴ��ļ�ת���ɹ�
        sql = sql + " and filetype in ('0','1')"   #��������
        
        AfaLoggerFunc.tradeInfo('>>>>>>>��ʼ��ѯAHNX_FILEԭ���ף�'+ str(sql))
        records = AfaDBFunc.SelectSql( sql ) 
                  
        if records==None:
            return ExitSubTrade("D0001" ,"��ѯAHNX_FILEʧ��")
        elif(len(records) == 0):
            return ExitSubTrade("D0001" ,"�޴���Ϣ")
            
        else:
            AfaLoggerFunc.tradeInfo("AHNX_FILE���еļ�¼����" +str(len(records)))
            for i in range(len(records)):
                TradeContext.mFileName    = records[i][4]
                TradeContext.swapFileName = records[i][6]
                TradeContext.batchno      = records[i][5]
                
                #----1.1����ѯĳһ���εĴ���״̬(abdt_batchinfo)
                sql = ""
                sql = sql + "select status,procmsg"
                sql = sql + " from abdt_batchinfo"
                sql = sql + " where batchno='"+TradeContext.batchno +"'"   #���κ�(ahxnb_file/abdt_batchinfoһ��)
                
                AfaLoggerFunc.tradeInfo("��ѯABDT_BATCHINFO��"+ str(sql))
                result = AfaDBFunc.SelectSql( sql )
                
                if result==None:
                    continue
                    #return ExitSubTrade("D0001" ,"��ѯ��abdt_batchinfoʧ��")
                elif(len(result) == 0):
                    continue
                    #return ExitSubTrade("D0001" ,"�޴���Ϣ")
                
                AfaLoggerFunc.tradeInfo("״̬Ϊ:"+result[0][0])   
                #����������������Ϣ
                TradeContext.swapprocmsg = result[0][1]
                #��������������״̬����ʼ��Ϊ3��0-�����ļ��ϴ��ɹ�����ת����1-����ɹ���2-����ʧ��3�������ļ�ת���ɹ���������
                TradeContext.swapstatus = "3"
                
                #----2�����ݲ�ѯ��������������״̬�������籣�����ļ� 
                #----2.1����������״̬Ϊ88
                if(result[0][0] =='88'):
                
                    #20120916 ��ũ��FTP�������������ļ�����������ӦĿ¼
                    #����ϵͳ�����ļ�Ŀ¼��/home/maps/data/batch/down/
                    #��ũ������ļ�Ŀ¼  ��/home/maps/afa/data/batch/down/
                    #begin
                    TradeContext.downFile = records[i][0]+records[i][1]+'0000'+ '_' + records[i][2]+'.RET'
                
                    if not AfaFtpFunc.getFile('AHXNB_GET',TradeContext.downFile,TradeContext.downFile) :
                        AfaLoggerFunc.tradeInfo('ftp�������������ļ�ʧ�� : '+ TradeContext.downFile)
                        continue
                    #end
                
                    #״̬��Ϊ�ɹ�
                    TradeContext.swapstatus = "1"
                    TradeContext.swapprocmsg = "������������ɣ��������ػ����ļ�"
                    
                    #----2.1.1�����ɴ��������ļ�
                    if(records[i][3]=='0'):      #�ļ�����0������ 1������
                        AfaLoggerFunc.tradeInfo("�������ɴ��������ļ�")
                        sFileName = os.environ['AFAP_HOME'] + '/data/batch/down/'+ records[i][0]+records[i][1]+'0000'+ '_' + records[i][2]+'.RET' 
                        
                        #����-20120210 �޸�
                        #dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'yhdffk'+TradeContext.mFileName[6:] 
                        dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDFFK'+TradeContext.mFileName[6:-4]+'_F.TXT'       #����ʧ�ܻ����ļ�
                        dFileName_succ = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDFFK'+TradeContext.mFileName[6:-4]+'_S.TXT'  #�����ɹ������ļ�
                        #end
                        
                        AfaLoggerFunc.tradeInfo("ת��ǰ���ļ�Ϊ��"+sFileName)
                        AfaLoggerFunc.tradeInfo("ת����(ʧ��)���ļ�Ϊ��"+dFileName)
                        AfaLoggerFunc.tradeInfo("ת����(�ɹ�)���ļ�Ϊ��"+dFileName_succ)
                        
                        #����-20120210 �޸ģ�����һ������
                        if not batch_DF_FilePro(sFileName,dFileName,dFileName_succ):
                            #ʧ����continue����ת����һ���ļ�
                            continue
                        #end
                        
                    #----2.1.2�����ɴ��ۻ����ļ�
                    if(records[i][3]=='1'):      #�ļ�����0������ 1������
                        AfaLoggerFunc.tradeInfo("���ɴ��ۻ����ļ�")
                        sFileName = os.environ['AFAP_HOME'] + '/data/batch/down/' + records[i][0]+records[i][1]+'0000' + '_'+records[i][2] + '.RET' 
                        
                        #����-20111130 begin
                        dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/' + 'YHDKFK' + TradeContext.mFileName[6:-4]+'_S.TXT'  #���۳ɹ������ļ�
                        dFileName_fail = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDKFK'+TradeContext.mFileName[6:-4]+'_F.TXT' #����ʧ�ܻ����ļ�
                        #end
                        
                        AfaLoggerFunc.tradeInfo("ת��ǰ���ļ�Ϊ��"+sFileName)
                        AfaLoggerFunc.tradeInfo("ת����(�ɹ�)���ļ�Ϊ��"+dFileName)
                        AfaLoggerFunc.tradeInfo("ת����(ʧ��)���ļ�Ϊ��"+dFileName_fail)
                        
                        #����-20120210 �޸ģ�����һ������
                        if not batch_DK_FilePro(sFileName,dFileName,dFileName_fail):
                            #ʧ����continue����ת����һ���ļ�
                            continue
                        #end
                
                #----2.2����������״̬Ϊ40
                elif(result[0][0] =='40'):
                    #���ô���״̬Ϊʧ��
                    TradeContext.swapstatus = "2"
                    TradeContext.swapprocmsg="�����������۲�������ʧ�ܣ��ļ�ת���ɹ�����������"
                    
                    #----2.2.1�����ɴ��������ļ�
                    if(records[i][3]=='0'):      #�ļ�����0������ 1������
                        AfaLoggerFunc.tradeInfo("���ɴ��������ļ�")
                        sFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/'+ TradeContext.mFileName
                        
                        #����-20120210 �޸Ļ����ļ���
                        dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDFFK'+TradeContext.mFileName[6:-4]+'_F.TXT' 
                        dFileName_succ = os.environ['AFAP_HOME'] + '/data/ahxnb/'+'YHDFFK'+TradeContext.mFileName[6:-4]+'_S.TXT' 
                        #end
                        
                        AfaLoggerFunc.tradeInfo("ת��ǰ���ļ�Ϊ��"+sFileName)
                        AfaLoggerFunc.tradeInfo("ת����(�ɹ�)���ļ�Ϊ��"+dFileName_succ)
                        AfaLoggerFunc.tradeInfo("ת����(ʧ��)���ļ�Ϊ��"+dFileName)
                        
                        if not batch_DF_Fail_FilePro(sFileName,dFileName):
                            #ʧ����continue����ת����һ���ļ�
                            continue
                            
                        #�����ɹ�-���ļ�
                        wsfp=open(dFileName_succ,"w")
                        wsfp.write("")
                        wsfp.close( )
                    
                    #----2.2.1�����ɴ��ۻ����ļ�
                    if(records[i][3]=='1'):      #�ļ�����0������ 1������
                        AfaLoggerFunc.tradeInfo("���ɴ��ۻ����ļ�")
                        
                        #����-20120210 �޸Ļ����ļ���
                        sFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/' + TradeContext.mFileName
                        dFileName = os.environ['AFAP_HOME'] + '/data/ahxnb/' + 'YHDKFK' + TradeContext.mFileName[6:-4]+'_S.TXT'       #���۳ɹ������ļ�
                        dFileName_fail = os.environ['AFAP_HOME'] + '/data/ahxnb/' + 'YHDKFK' + TradeContext.mFileName[6:-4]+'_F.TXT'  #����ʧ�ܻ����ļ�
                        
                        if not batch_DK_Fail_FilePro(sFileName,dFileName_fail):
                            continue
                        #end
                        
                        AfaLoggerFunc.tradeInfo("ת��ǰ���ļ�Ϊ��"+sFileName)
                        AfaLoggerFunc.tradeInfo("ת����(�ɹ�)���ļ�Ϊ��"+dFileName)
                        AfaLoggerFunc.tradeInfo("ת����(ʧ��)���ļ�Ϊ��"+dFileName_fail)
                        
                        #���۳ɹ�-���ļ�
                        wfp=open(dFileName,"w")
                        wfp.write("")
                        wfp.close( )
                        
                #----3������ahnx_file��
                sqlupdate = ""
                sqlupdate = sqlupdate + "update ahnx_file"
                sqlupdate = sqlupdate + " set status='"+ TradeContext.swapstatus +"'," #����״̬
                sqlupdate = sqlupdate + "procmsg='"+TradeContext.swapprocmsg+"'"       #������Ϣ
                sqlupdate = sqlupdate + " where batchno='"+TradeContext.batchno+"'"    #���κ�
                
                AfaLoggerFunc.tradeInfo("����AHNX_FILE��䣺"+str(sqlupdate))
                retcode = AfaDBFunc.UpdateSqlCmt( sqlupdate )
                
                if (retcode < 0):
                    #ʧ����continue����ת����һ���ļ�
                    continue 
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return False

#ת���������ʧ�ܵ����ݸ�ʽ
def batch_DF_FilePro(sFileName,dFileName,dFileName_succ):
    try:
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            AfaLoggerFunc.tradeInfo("�������������ļ�����")
            
            bfp = open(sFileName, "r")
            wfp = open(dFileName,"w")
            wsfp = open(dFileName_succ,"w")
            
            count = 0
            linebuf = bfp.readline()
            
            while ( len(linebuf) > 0 ):
                count = count + 1
                linebuf1=linebuf.split('|')
                
                if ( linebuf1[0] == "1" ):
                    #�ӵڶ��п�ʼ��ȡ��ϸ��Ϣ
                    linebuf = bfp.readline()
                    continue
                
                #----1������ʧ����ϸд���ļ�
                if((linebuf1[0] =='2') and (linebuf1[11]!='AAAAAAA')):
                    
                    wbuffer = ''
                    wbuffer = wbuffer + linebuf1[1] + '|'     #�籣���
                    #wbuffer = wbuffer + linebuf1[4] + '|'     #����
                    
                    sql = ""
                    sql = sql + "select identityno,sbbillno,Name"
                    sql = sql + " from ahxnb_swap"
                    sql = sql + " where sbno='" +linebuf1[1].lstrip().rstrip() + "'"  #�籣���
                    sql = sql + " and workdate= '" +  TradeContext.WorkDate + "'"     #��������
                                        
                    records = AfaDBFunc.SelectSql( sql ) 
                    
                    if records==None:
                        linebuf = bfp.readline()
                        continue
                        
                    if(len(records) == 0):
                        wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #����
                        wbuffer = wbuffer + '��ѯahxnb_swap�޴˼�¼'  + '|'    #���֤��
                        wbuffer = wbuffer + linebuf1[7]               + '|'    #�������
                        wbuffer = wbuffer + '��ѯahxnb_swap�޴˼�¼'           #�籣���ݺ�
                        
                    elif(len(records) == 1):
                        wbuffer = wbuffer + linebuf1[4]    + '|'    #����
                        wbuffer = wbuffer + records[0][0]  + '|'    #���֤��
                        wbuffer = wbuffer + linebuf1[7]    + '|'    #�������
                        wbuffer = wbuffer + records[0][1].strip()   #�籣���ݺ�
                        
                    else:
                        Flag = '0'
                        for j in range(0,len(records)):
                            if( records[j][2].strip() == linebuf1[4].strip() ):
                                Flag = '1'
                                wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #����
                                wbuffer = wbuffer + records[j][0]                      + '|'    #���֤��
                                wbuffer = wbuffer + linebuf1[7]                        + '|'    #�������
                                wbuffer = wbuffer + records[j][1].strip()                       #�籣���ݺ�
                        
                        if ( Flag == '0' ):
                            wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')+ '|'    #����
                            wbuffer = wbuffer + 'ͬһ�ͻ�������Σ���ѯahxnb_swap�޴˼�¼'         + '|'    #���֤��
                            wbuffer = wbuffer + linebuf1[7]                      + '|'    #�������
                            wbuffer = wbuffer + 'ͬһ�ͻ�������Σ���ѯahxnb_swap�޴˼�¼'                  #�籣���ݺ�
                            
                    wbuffer = wbuffer + '\n'
                    wfp.write(wbuffer)
                    
                #----2�������ɹ���ϸд���ļ�
                elif((linebuf1[0] =='2') and (linebuf1[11]=='AAAAAAA')):
                    wbuffer = ''
                    wbuffer = wbuffer + linebuf1[1] + '|'     #�籣���
                    #wbuffer = wbuffer + linebuf1[4] + '|'    #����
                    
                    sql = ""
                    sql = sql + "select identityno,sbbillno,Name"
                    sql = sql + " from ahxnb_swap"
                    sql = sql + " where sbno='" +linebuf1[1].lstrip().rstrip() + "'"  #�籣���
                    sql = sql + " and workdate= '" +  TradeContext.WorkDate + "'"     #��������
                    
                    records = AfaDBFunc.SelectSql( sql ) 
                    
                    if records==None:
                        linebuf = bfp.readline()
                        continue
                        
                    if(len(records) == 0):
                        wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #����
                        wbuffer = wbuffer + '��ѯahxnb_swap�޴˼�¼'  + '|'    #���֤��
                        wbuffer = wbuffer + linebuf1[7]               + '|'    #�������
                        wbuffer = wbuffer + '��ѯahxnb_swap�޴˼�¼'           #�籣���ݺ�
                        
                    elif(len(records) == 1):
                        wbuffer = wbuffer + linebuf1[4]    + '|'    #����
                        wbuffer = wbuffer + records[0][0]  + '|'    #���֤��
                        wbuffer = wbuffer + linebuf1[7]    + '|'    #�������
                        wbuffer = wbuffer + records[0][1].strip()     #�籣���ݺ�
                        
                    else:
                        Flag = '0'
                        for j in range(0,len(records)):
                            if( records[j][2].strip() == linebuf1[4].strip() ):
                                Flag = '1'
                                wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #����
                                wbuffer = wbuffer + records[j][0]                      + '|'    #���֤��
                                wbuffer = wbuffer + linebuf1[7]                        + '|'    #�������
                                wbuffer = wbuffer + records[j][1].strip()                         #�籣���ݺ�
                        
                        if ( Flag == '0' ):
                            wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')+ '|'    #����
                            wbuffer = wbuffer + 'ͬһ�ͻ�������Σ���ѯahxnb_swap�޴˼�¼'         + '|'    #���֤��
                            wbuffer = wbuffer + linebuf1[7]                      + '|'    #�������
                            wbuffer = wbuffer + 'ͬһ�ͻ�������Σ���ѯahxnb_swap�޴˼�¼'
                    
                    wbuffer = wbuffer + '\n'
                    wsfp.write(wbuffer)
                            
                else:
                    wbuffer = ""
                    wbuffer = wbuffer + "���������ļ���" + str(count) + "�и�ʽ[�ֶ�]����ȷ������"
                    wbuffer = wbuffer + "\n"
                    wfp.write(wbuffer)
                    
                linebuf = bfp.readline()
            
            #�ر��ļ�
            bfp.close()
            wfp.close()
            wsfp.close()
            return True
        
        else:
            AfaLoggerFunc.tradeInfo("�������������ļ������ڻ����ļ�")
            return False 
                      
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        bfp.close()
        wfp.close()
        wsfp.close()
        return False

#ת�������з����籣���۳ɹ�ʱ���ݸ�ʽ
def batch_DK_FilePro(sFileName,dFileName,dFileName_fail):
    try:
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            AfaLoggerFunc.tradeInfo("�������������ļ�����")
            
            bfp = open(sFileName, "r")
            wfp = open(dFileName,"w")
            ffp = open(dFileName_fail,"w")
            
            count = 0
            linebuf = bfp.readline()
            
            while ( len(linebuf) > 0 ):
                count = count + 1
                linebuf1=linebuf.split('|')
                
                if ( linebuf1[0] == "1" ):
                    #�ӵڶ��п�ʼ��ȡ��ϸ��Ϣ
                    linebuf = bfp.readline()
                    continue
                
                #----1�����۳ɹ���ϸд���ļ�
                if((linebuf1[0] =='2') and (linebuf1[11]=='AAAAAAA')):
                    wbuffer = ''
                    wbuffer = wbuffer + linebuf1[1] + '|'     #�籣���
                    #wbuffer = wbuffer + linebuf1[4] + '|'     #���� 
                    
                    sql = "select identityno,sbbillno,Name"
                    sql = sql + " from ahxnb_swap"
                    sql = sql + " where sbno='" +linebuf1[1].lstrip().rstrip() + "'"
                    sql = sql + " and workdate= '" +  TradeContext.WorkDate + "'"
                    AfaLoggerFunc.tradeInfo(sql)
                    records = AfaDBFunc.SelectSql( sql ) 
                    AfaLoggerFunc.tradeInfo(records)
                    if records==None:
                        linebuf = bfp.readline()
                        continue
                        
                    if(len(records) == 0):
                        wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')            + '|'  #���� 
                        wbuffer = wbuffer + "swap���޴˼�¼"       + '|'  #���֤��
                        wbuffer = wbuffer + linebuf1[7]            + '|'  #���
                        wbuffer = wbuffer + "swap���޴˼�¼"       + '|'  #���κ�
                        
                    elif(len(records) == 1):
                        wbuffer = wbuffer + linebuf1[4]    + '|'    #����
                        wbuffer = wbuffer + records[0][0]  + '|'    #���֤��
                        wbuffer = wbuffer + linebuf1[7]    + '|'    #�������
                        wbuffer = wbuffer + records[0][1].strip()       #�籣���ݺ�
                        
                    else:
                        Flag = '0'
                        for j in range(0,len(records)):
                            if( records[j][2].strip() == linebuf1[4].strip() ):
                                AfaLoggerFunc.tradeInfo(str(j) + records[j][2].strip())
                                AfaLoggerFunc.tradeInfo(linebuf1[4].strip())
                                Flag = '1'
                                wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #����
                                wbuffer = wbuffer + records[j][0]                      + '|'    #���֤��
                                wbuffer = wbuffer + linebuf1[7]                        + '|'    #�������
                                wbuffer = wbuffer + records[j][1].strip()                         #�籣���ݺ�
                        
                        if ( Flag == '0' ):
                            wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')+ '|'    #����
                            wbuffer = wbuffer + 'ͬһ�ͻ�������Σ���ѯahxnb_swap�޴˼�¼'         + '|'    #���֤��
                            wbuffer = wbuffer + linebuf1[7]                      + '|'    #�������
                            wbuffer = wbuffer + 'ͬһ�ͻ�������Σ���ѯahxnb_swap�޴˼�¼'
                    
                    wbuffer = wbuffer + '\n'
                    wfp.write(wbuffer)
                
                #----2������ʧ����ϸд���ļ�
                elif( (linebuf1[0] =='2') and (linebuf1[11]!='AAAAAAA') ):
                    wbuffer = ''
                    wbuffer = wbuffer + linebuf1[1]    + '|'     #�籣���
                    #wbuffer = wbuffer + linebuf1[4]    + '|'     #����
                    
                    sql = ""
                    sql = sql + "select identityno,sbbillno,Name"
                    sql = sql + " from ahxnb_swap"
                    sql = sql + " where sbno='" + linebuf1[1].strip() + "'"      #�籣���
                    sql = sql + " and workdate= '" + TradeContext.WorkDate + "'" #��������
                    
                    records = AfaDBFunc.SelectSql( sql ) 
                    
                    if records==None:
                        linebuf = bfp.readline()
                        continue
                        
                    if(len(records) == 0):
                        wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')            + '|'  #���� 
                        wbuffer = wbuffer + "swap���޴˼�¼"       + '|'  #���֤��
                        wbuffer = wbuffer + linebuf1[7]            + '|'  #���
                        wbuffer = wbuffer + "swap���޴˼�¼"       + '|'  #�籣���ݺ�
                        wbuffer = wbuffer + "�ÿͻ���AHXNB_SWAP�����޼�¼" + ''   #����˵��
                        
                    elif(len(records) == 1):
                        wbuffer = wbuffer + linebuf1[4]    + '|'    #����
                        wbuffer = wbuffer + records[0][0]  + '|'    #���֤��
                        wbuffer = wbuffer + linebuf1[7]    + '|'    #�������
                        wbuffer = wbuffer + records[0][1].strip()  + '|'    #�籣���ݺ�
                        wbuffer = wbuffer + linebuf1[10].strip()    #����˵��
                        
                    else:
                        Flag = '0'
                        for j in range(0,len(records)):
                            if( records[j][2].strip() == linebuf1[4].strip() ):
                                Flag = '1'
                                wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')  + '|'    #����
                                wbuffer = wbuffer + records[j][0]                      + '|'    #���֤��
                                wbuffer = wbuffer + linebuf1[7]                        + '|'    #�������
                                wbuffer = wbuffer + records[j][1].strip()              + '|'    #�籣���ݺ�
                                wbuffer = wbuffer + linebuf1[10].strip()                        #����˵��
                        
                        if ( Flag == '0' ):
                            wbuffer = wbuffer + linebuf1[4].strip().split(';')[0].ljust(20,' ')+ '|'    #����
                            wbuffer = wbuffer + 'ͬһ�ͻ�������Σ���ѯahxnb_swap�޴˼�¼'         + '|'    #���֤��
                            wbuffer = wbuffer + linebuf1[7]                      + '|'    #�������
                            wbuffer = wbuffer + 'ͬһ�ͻ�������Σ���ѯahxnb_swap�޴˼�¼' + '|'
                            wbuffer = wbuffer + linebuf1[10].strip()                      #����˵��
                    
                    wbuffer = wbuffer + '\n'
                    ffp.write(wbuffer)
                
                else:
                    wbuffer = ""
                    wbuffer = wbuffer + "���������ļ���"+str(count)+"�и�ʽ��������"
                    wbuffer = wbuffer + "\n"
                    ffp.write(wbuffer)
                    
                linebuf = bfp.readline()
                
            #�ر��ļ�
            bfp.close()
            wfp.close()
            ffp.close()
            return True
            
        else:
            AfaLoggerFunc.tradeInfo("�������������ļ������ڻ����ļ�")
            return False 
                         
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        bfp.close()
        wfp.close()
        ffp.close()
        return False

#ת�����������ļ����Ǵ���ʧ�ܵ����ݸ�ʽ
def batch_DF_Fail_FilePro(sFileName,dFileName):
    try:
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):  
            AfaLoggerFunc.tradeInfo("�������������ļ�����")
           
            wfp = open(dFileName,"w")
            bfp = open(sFileName, "r")
            
            linebuf = bfp.readline()
            
            while ( len(linebuf) > 0 ):
                linebuf1=linebuf.split('|')

                wbuffer = ''
                wbuffer = wbuffer + linebuf1[0]   + '|'       #�籣���
                wbuffer = wbuffer + linebuf1[1]   + '|'       #����
                wbuffer = wbuffer + linebuf1[2]   + '|'       #���֤��
                wbuffer = wbuffer + linebuf1[3]   + '|'       #�������
                wbuffer = wbuffer + linebuf1[4]               #�籣���ݺ�
                
                wbuffer = wbuffer + '\n'
                wfp.write(wbuffer)
                
                linebuf = bfp.readline() 
                
            #�ر��ļ�
            wfp.close()
            bfp.close()
            return True
        
        else:
            AfaLoggerFunc.tradeInfo("�������������ļ������ڻ����ļ�")
            return False 
                      
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        wfp.close()
        bfp.close()
        return False
        
#ת�����������ļ����Ǵ���ʧ�ܵ����ݸ�ʽ
def batch_DK_Fail_FilePro(sFileName,dFileName_fail):
    try:
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):  
            AfaLoggerFunc.tradeInfo("�������������ļ�����")
           
            wfp = open(dFileName_fail,"w")
            bfp = open(sFileName, "r")
            
            linebuf = bfp.readline()
            
            while ( len(linebuf) > 0 ):                                        
                linebuf1=linebuf.split('|')

                wbuffer = ''
                wbuffer = wbuffer + linebuf1[0]   + '|'       #�籣���
                wbuffer = wbuffer + linebuf1[1]   + '|'       #����    
                wbuffer = wbuffer + linebuf1[2]   + '|'       #���֤��
                wbuffer = wbuffer + linebuf1[3]   + '|'       #�������
                wbuffer = wbuffer + linebuf1[4]   + '|'       #�籣���ݺ�
                wbuffer = wbuffer + "����ϵͳ����ʧ��(40״̬)"   + ''        #����˵��
                
                wbuffer = wbuffer + '\n'
                wfp.write(wbuffer)
                
                linebuf = bfp.readline() 
                    
            #�ر��ļ�
            wfp.close()
            bfp.close()
            return True 
        
        else:
            AfaLoggerFunc.tradeInfo("�������������ļ������ڻ����ļ�")
            return False 
                      
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        wfp.close()
        bfp.close()
        return False

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

    AfaLoggerFunc.tradeInfo('********************����ת����ʽ��ʼ********************')
    #Ĭ��ȡǰһ������ڣ���ת��ǰһ�������
    if ( len(sys.argv) != 2 ):
        TradeContext.WorkDate = AfaAdminFunc.getTimeFromNow(-1)
        
    #ת���������ڵ�����
    else:
        TradeContext.WorkDate =sys.argv[1]
   
    #ת������
    file_Pro( )
    
    AfaLoggerFunc.tradeInfo('********************����ת����ʽ����********************')
