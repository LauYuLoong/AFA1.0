# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.TIPS������������
#       9 - ��ʼ״̬��������
#       1 - ʧ��
#       2 - �����ۿ���
#       0 - �ۿ�ɹ�
#=================================================================
#   �����ļ�:   TTPS001_8450031.py
#   �� �� Ա:   liyj
#   �޸�ʱ��:   2008-5-12 10:28
##################################################################
import TradeContext
TradeContext.sysType = 'tips'
import TipsFunc ,AfaUtilTools
import AfaDBFunc,ConfigParser,os,TipsHostFunc
from tipsConst import *
#import time
from types import *
#UtilTools,AfaLoggerFunc,HostContext,HostComm,

#��ȡ���������ļ�����Ϣ
def GetLappConfig( CfgFileName = None ):

    try:
        config = ConfigParser.ConfigParser( )

        if( CfgFileName == None ):
            CfgFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'

        config.readfp( open( CfgFileName ) )

        TradeContext.HOST_HOSTIP   = config.get('HOST_DZ', 'HOSTIP')
        TradeContext.HOST_USERNO   = config.get('HOST_DZ', 'USERNO')
        TradeContext.HOST_PASSWD   = config.get('HOST_DZ', 'PASSWD')
        TradeContext.HOST_LDIR     = config.get('HOST_DZ', 'LDIR')
        TradeContext.HOST_RDIR     = config.get('HOST_DZ', 'RDIR')
        TradeContext.CORP_CDIR     = config.get('HOST_DZ', 'CDIR')
        TradeContext.BANK_CDIR     = config.get('HOST_DZ', 'BDIR')
        TradeContext.TRACE         = config.get('HOST_DZ', 'TRACE')

        return 0

    except Exception, e:
        print str(e)
        return -1

def SubModuleMainFst( ):
    TipsFunc.WrtLog('��˰����_�������˴���ʼ[TTPS001_8450031]' )
    try:
        #��ȡ�����ļ�����Ϣ
        TipsFunc.WrtLog('>>>��ȡ�����ļ�����Ϣ')
        GetLappConfig( )
        
        TradeContext.sTellerNo = TIPS_TELLERNO_AUTO      #���׹�Ա��
        TradeContext.sDAccNo = ''                        #�����ʺ�
        TradeContext.sDAccName = ''                      #��������
        
        #ƴsql���,���ձ����κŵ�����д���ļ���=================================================================
        TipsFunc.WrtLog('>>>���ձ���������д���ļ�')
        
        #20110711 ����̩�޸� ֻ���ϴ�����û�д���������ļ�
        sql = "select workdate from tips_adm where status='1'"
        TipsFunc.WrtLog('��ѯ�������ڵ�sql=' + sql )
        rec = AfaDBFunc.SelectSql(sql)
        if (rec == None):
            TipsFunc.WrtLog('tipsϵͳ���ڱ�����쳣:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '���ݿ��ϵͳ���ڱ�����쳣' )
        elif ( len(rec) <= 0 ):
            TipsFunc.WrtLog( "û�е�������ڣ�����ϵ������Ա")
        else:
            TradeContext.TipsDate = rec[0][0]
            TipsFunc.WrtLog("tips��������Ϊ"+ TradeContext.TipsDate)
        #sql = "select WORKDATE,BATCHNO,TAXORGCODE,PAYEEBANKNO,PAYBKCODE,TOTALNUM,TOTALAMT,DEALSTATUS from TIPS_BATCHADM where DEALSTATUS = '9' "
        sql = "select WORKDATE,BATCHNO,TAXORGCODE,PAYEEBANKNO,PAYBKCODE,TOTALNUM,TOTALAMT,DEALSTATUS from TIPS_BATCHADM where DEALSTATUS = '9' and WORKDATE = '" + TradeContext.TipsDate + "' "
        #end ����̩�޸�
        
        TipsFunc.WrtLog( 'sql=' + sql )
        res = AfaDBFunc.SelectSql( sql )
        if( res == None ):
            TipsFunc.WrtLog('�������������쳣:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
        elif ( len(res) <= 0 ):
            TipsFunc.WrtLog("����Ҫ���������")
        else:
            for j in range(len(res)):
                TradeContext.entrustDate = res[j][0]       #ί������
                TradeContext.packNo = res[j][1]            #����ˮ��
                TradeContext.taxOrgCode = res[j][2]        #���ջ��ش���
                TradeContext.payeeBankNo = res[j][3]       #�տ����к�
                TradeContext.payBkCode = res[j][4]         #�������к�
                TradeContext.sTotal = res[j][5]            #�ܱ���
                TradeContext.sAmount = res[j][6]           #�ܽ��
                TradeContext.sStatus = res[j][7]           #����״̬
                
                TradeContext.sBrNo = TIPS_SBNO_QS                      #���׻�����
                TradeContext.sTeller = TIPS_TELLERNO_AUTO              #���׹�Ա��
                TradeContext.sTermId = '123456'                        #�ն˺�
                TradeContext.sOpeFlag = '0'                             #������־
                TradeContext.sFileName = "JU" + TradeContext.packNo      #�ļ���
                
                #��ѯ������˰��������============================================================================
                TipsFunc.WrtLog('>>>��ѯ������˰��������')
                #sql = "select t2.SERIALNO,t1.ACCNO,t1.HandOrgName,t1.AMOUNT,t1.NOTE7 from TIPS_BATCHDATA t1,tips_maintransdtl t2 where "
                #sql = sql + " t1.workdate ='" + TradeContext.entrustDate + "'"
                #sql = sql + " and t2.workdate ='" + TradeContext.entrustDate + "'"
                #sql = sql + " and t1.CORPSERIALNO =t2.CORPSERNO"
                #sql = sql + " and t1.batchno = '" + TradeContext.packNo + "'"
                #sql = sql + " and t1.taxorgcode = '" + TradeContext.taxOrgCode + "'"
                #sql = sql + " and t1.status  = '9'"
                sql = "select t1.SERIALNO,t1.ACCNO,t1.HandOrgName,t1.AMOUNT,t1.NOTE7 from TIPS_BATCHDATA t1 where "
                sql = sql + " t1.workdate ='" + TradeContext.entrustDate + "'"
                sql = sql + " and t1.batchno = '" + TradeContext.packNo + "'"
                sql = sql + " and t1.taxorgcode = '" + TradeContext.taxOrgCode + "'"
                sql = sql + " and t1.status  = '9'"
                
                TipsFunc.WrtLog( 'sql=' + sql )
                records = AfaDBFunc.SelectSql( sql )
                
                if len( records ) > 0:
                    TipsFunc.WrtLog( '>>>�����δ���δ�����������ϸ����,�ύ������������')
                    #�����������������ļ�============================================================================
                    TipsFunc.WrtLog( '>>>�����������������ļ�')
                    filename = os.environ['AFAP_HOME'] + '/data/batch/tips/TIPS_' + TradeContext.packNo + '.txt'
                    rfp = open( filename, 'w' )
                    
                    Total  = 0
                    Amount = 0
                    records = AfaUtilTools.ListFilterNone(records)
                    for i in range( len( records ) ):
                        TradeContext.accno      = records[i][1]           #�����ʺ�
                        TradeContext.SerialNo   = records[i][0]           #��ˮ��
                        TradeContext.brno       = records[i][4]           #�����л�����
                        
                        #��ȡ�����ʺš���������==========================================================================
                        TipsFunc.WrtLog('>>>��ȡ�����ʺš���������')
                        #====��ѯ�տ��ʺ�=======
                        if not TipsFunc.SelectAcc():
                            TipsFunc.WrtLog( ">>>��ѯ�տ��ʺ��쳣")
                            return TipsFunc.ExitThisFlow( '99090', '��ѯ�տ��ʺ��쳣' )
                            
                        TradeContext.sDAccNo = TradeContext.__agentAccno__             #�����ʺ�
                        TradeContext.sDAccName = TradeContext.__agentAccname__         #��������
                            
                        wbuffer = ''
                        wbuffer = wbuffer +((TradeContext.entrustDate).strip()).ljust(8,' ') + "<fld>"
                        wbuffer = wbuffer +((TradeContext.packNo).strip()).ljust(12,' ') + "<fld>"
                        wbuffer = wbuffer +((TradeContext.entrustDate).strip()).ljust(8,' ') + "<fld>"
                        wbuffer = wbuffer +(records[i][0].strip()).ljust(12,' ') + "<fld>"
                        wbuffer = wbuffer +(TradeContext.brno).ljust(10,' ') + "<fld>"
                        wbuffer = wbuffer +(TradeContext.sTellerNo).ljust(6,' ') + "<fld>"
                        wbuffer = wbuffer +(records[i][1].strip()).ljust(25,' ') + "<fld>"
                        wbuffer = wbuffer +(records[i][2].strip()).ljust(60,' ') + "<fld>"
                        wbuffer = wbuffer +(TradeContext.sDAccNo).ljust(25,' ') + "<fld>"
                        wbuffer = wbuffer +(TradeContext.sDAccName).ljust(60,' ') + "<fld>"
                        wbuffer = wbuffer + "1".ljust(1,' ') + "<fld>"
                        wbuffer = wbuffer +(records[i][3].strip()).ljust(15,' ') + "<fld>"
                        wbuffer = wbuffer + "0".ljust(1,' ')+ "<fld>"
                        #д�뱨���ļ�
                        rfp.write(wbuffer + '\n')
                        
                        Total = Total + 1
                        Amount = Amount + (long)((float)(records[i][3].strip())*100 + 0.1)
                    
                    #�ر��ļ�=========================================================================
                    rfp.close()
            
                    sFileName = '/home/maps/afa/data/batch/tips/TIPS_' + TradeContext.packNo + '.txt'
                    dFileName = '/home/maps/afa/data/batch/tips/TPMPFILE.JU' + TradeContext.packNo
                    fFileFld = 'tpmpa.fld'
                    
                    #ת��=============================================================================
                    TipsFunc.WrtLog(">>>�����ļ�ת��")
                    if not TipsFunc.FormatFile("1",sFileName,dFileName,fFileFld):
                        TipsFunc.WrtLog("ת�������ϴ��ļ������쳣")
                        continue
                        #return TipsFunc.ExitThisFlow( '99090', 'ת�������ϴ��ļ������쳣' )
                    
                    #�ϴ������ļ�=====================================================================
                    TipsFunc.WrtLog(">>>�ϴ������ļ�")
                    if not TipsFunc.putHost('TPMPFILE.JU' + TradeContext.packNo,"TEXTLIB"):
                        TipsFunc.WrtLog("�ϴ������ļ��쳣")
                        continue
                        #return TipsFunc.ExitThisFlow( '99090', '�ϴ������ļ��쳣' )
                    
                    #���������ϴ�����=================================================================
                    TradeContext.sTotal = Total            #�ܱ���
                    if Amount <= 0 :
                        TradeContext.sAmount   = '0'
                   
                    #begin 20110722 ����̩�޸� ������ĵ�λΪ�ֺ�ë�����
                    elif (len(str(Amount)) == 1 ):            #�Է�Ϊ��λ
                        TradeContext.sAmount  = '0.0' + str(Amount)
                    
                    elif (len(str(Amount)) == 2 ):           #��ëΪ��λ
                        TradeContext.sAmount  = '0.' + str(Amount)
                    #end        
                    else:
                        TradeContext.sAmount   = str(Amount)[:-2] + '.' + str(Amount)[-2:]       #�ܽ��
                    TipsFunc.WrtLog(">>>���������ϴ�����8830")
                    if not TipsHostFunc.CommHost('8830'):
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
                        #return TipsFunc.ExitThisFlow( '99090', '��������' )
            
                    #����������������===============================================================
                    TipsFunc.WrtLog( ">>>����������������8831")
                    if not TipsHostFunc.CommHost('8831'):
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
                        #return TipsFunc.ExitThisFlow( '99090', '��������' )
                            
                    #��������״̬--2 - �����ۿ���================================================
                    TipsFunc.WrtLog(">>>��������״̬--2 - �����ۿ���")
                    if(not TipsFunc.UpdateBatchAdm('2','0000','�����ۿ���')):
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
                        #return TipsFunc.ExitThisFlow( '99003', '���ݿ����' )
                else:
                    TipsFunc.WrtLog( '>>>�����β�����δ�����������ϸ����,ֱ�ӷ����������˽��')
                    #��������״̬--0 - �ۿ�ɹ�===========================================================================
                    TipsFunc.WrtLog(">>>��������״̬--0 - �ۿ�ɹ�")
                    if( not TipsFunc.UpdateBatchAdm('0','0000','�ۿ�ɹ�')):
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
                        #raise Exception,TradeContext.errorMsg
                    
                    #�����������˽��===========================================================================
                    TipsFunc.WrtLog('>>>�����������˽��')
                    TradeContext.TemplateCode = 'TPS001'
                    TradeContext.TransCode = '8469'
                    TradeContext.__respFlag__ = '0'
                    subModuleName = 'TTPS001_8469'
                    TradeContext.EntrustDate = TradeContext.entrustDate      #����ί������
                    TradeContext.PackNo = TradeContext.packNo           #����ί�к�
                    TradeContext.TaxOrgCode = TradeContext.taxOrgCode       #���ջ��ش���
                    TradeContext.sysId      ='AG2010'
                    TradeContext.busiNo     ='00000000000001'
                    subModuleHandle=__import__( subModuleName )
                    TipsFunc.WrtLog( 'ִ��['+subModuleName+']ģ��' )
                    if not subModuleHandle.SubModuleMainFst( ) :
                        TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                        continue
               
        #TradeContext.errorCode='0000'
        #TradeContext.errorMsg='���׳ɹ�'
        
        TipsFunc.WrtLog('��˰����_�������˴������[TTPS001_8450031]' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
        
###########################################������###########################################
if __name__=='__main__':

    TipsFunc.WrtLog('********************������˰�ļ��ϴ���ʼ********************')
    
    TradeContext.TransCode = 'TTPS001_8450031'
    SubModuleMainFst( )


    TipsFunc.WrtLog('********************������˰�ļ��ϴ�����********************')

