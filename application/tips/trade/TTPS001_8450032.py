# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�TTPS001_8450032.py
# �ļ���ʶ��
# ժ    Ҫ���������̴������
#       9 - ��ʼ״̬��������
#       1 - ʧ��
#       2 - �����ۿ���
#       0 - �ۿ�ɹ�
# ��ǰ�汾��2.0
# ��    �ߣ�liyj
# ������ڣ�2008��09��10��
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import TradeContext
TradeContext.sysType = 'tips'
import AfaDBFunc,os,TipsFunc,HostContext,TipsHostFunc,ConfigParser
from types import *
from tipsConst import *
#time,AfaAfeFunc,AfaUtilTools,

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

        return True

    except Exception, e:
        print str(e)
        return False

######################################��ʹ�����ˮ#####################################
def MatchData():

    #��ȡ�����ļ�����Ϣ
    TipsFunc.WrtLog('>>>��ȡ�����ļ�����Ϣ')
    if(not GetLappConfig( )):
        return TipsFunc.ExitThisFlow( 'A0027', '��ȡ�����ļ�����Ϣ�쳣' )
        
    TipsFunc.WrtLog('>>>��ʹ�����ˮ')

    try:
        totalnum = 0
        totalamt = 0
        
        succnum = 0
        succamt = 0

        #�����������ļ�
        #sFileName = TradeContext.HOST_LDIR + '/' + 'batch/tips/TIPS_down_' + TradeContext.packNo + '.txt'
        sFileName = '/home/maps/afa/data/batch/tips/JD' + TradeContext.packNo + '.JD'+ TradeContext.packNo
        hFp = open(sFileName, "r")
        #��ȡһ��
        linebuf = hFp.readline()

        while ( len(linebuf) > 0 ):

            #��ֶ�����ˮ
            swapbuf = linebuf.split('<fld>')

            if swapbuf[10].strip() == 'AAAAAAA':
                errorCode = '90000'
                errorMsg = '�ɹ�'
                TradeContext.errorCode='0000'
                TradeContext.errorMsg='�����ɹ�'
                TradeContext.__status__='0'
                TradeContext.bankSerno = swapbuf[5]
            else:
                errorCode,errorMsg = TipsFunc.SelCodeMsg(swapbuf[10]) 
                TradeContext.errorCode=errorCode
                TradeContext.errorMsg=errorMsg
                #TradeContext.errorCode=swapbuf[10]
                #TradeContext.errorMsg="����ʧ��"
                TradeContext.__status__='1'
                TradeContext.bankSerno = swapbuf[5]
            
            #��ѯ�Ƿ��м�¼��֮ƥ��   20090908 wqs
            sql_s="select workdate,corpserialno,note6,note2,serialno from tips_batchdata where workdate='"+ TradeContext.entrustDate + "'"\
                  " and batchno='"+ TradeContext.packNo + "' and TAXORGCODE='"+ TradeContext.taxOrgCode + "' and SERIALNO ='" + swapbuf[3].strip() + "'"
            records_s=AfaDBFunc.SelectSql(sql_s)
            if records_s==None:
                TipsFunc.WrtLog(sql_s )
                TipsFunc.WrtLog('���ݿ��쳣'+AfaDBFunc.sqlErrMsg )
                return False
            elif(len(records_s)==0):
                TipsFunc.WrtLog('��tips_batchdataû��ƥ��ļ�¼' )
                return False
            else:
                TradeContext.corpTime=records_s[0][0]
                TradeContext.corpSerno=records_s[0][1]
                TradeContext.note3=records_s[0][2]
                TradeContext.note4=records_s[0][3]
                TradeContext.agentSerialno=records_s[0][4]
                TradeContext.workDate=TradeContext.corpTime
                TradeContext.revTranF='0'
                TradeContext.TransCode = '845003'
                
                
            
            
            #�޸������ݿ����ƥ��
            updSql = "UPDATE TIPS_BATCHDATA SET ERRORCODE='" + errorCode + "',ERRORMSG = '" + errorMsg + "' WHERE"
            updSql = updSql + " WORKDATE ='" + TradeContext.entrustDate + "'"
            updSql = updSql + " AND BATCHNO ='" + TradeContext.packNo + "'"
            updSql = updSql + " AND TAXORGCODE ='" + TradeContext.taxOrgCode + "'"
            updSql = updSql + " AND SERIALNO ='" + swapbuf[3].strip() + "'"

            TipsFunc.WrtLog(updSql)

            result = AfaDBFunc.UpdateSqlCmt( updSql )
            if ( result <= 0 ):
                TipsFunc.WrtLog( AfaDBFunc.sqlErrMsg )
                TipsFunc.WrtLog('>>>������:�޸���ƥ����ˮ״̬,���ݿ��쳣')
                return False
            
            #=============������������״̬====================
            if( not TipsFunc.UpdateDtl( 'TRADE' ) ):
                raise TipsFunc.exitMainFlow( )
            
            if swapbuf[10].strip() == 'AAAAAAA':
                succnum = succnum + 1
                succamt = succamt + float(swapbuf[9].strip()) 

            totalnum = totalnum + 1
            totalamt = totalamt + float(swapbuf[9].strip())
            
            #��ȡһ��
            linebuf = hFp.readline()

        hFp.close()

        TipsFunc.WrtLog( 'ƥ���¼��=' + str(totalnum) + ",ƥ���ܽ��=" + str(totalamt) )
        
        #TradeContext.succNum = str(totalnum)
        #TradeContext.succAmt = str(totalamt)
        TradeContext.succNum = str(succnum)
        TradeContext.succAmt = str(succamt)
        
        #��������״̬--5-��������ļ�===========================================================================
        TipsFunc.WrtLog(">>>��������״̬--5-��������ļ�")
        if( not TipsFunc.UpdateBatchAdm('5','0000','��������ļ�')):
            TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
            raise Exception,TradeContext.errorMsg

        TipsFunc.WrtLog( '>>>��ʹ�����ˮ ---> �ɹ�' )

        return True

    except Exception, e:
        TipsFunc.WrtLog(str(e))
        TipsFunc.WrtLog('>>>��ʹ�����ˮ ---> �쳣')
        return False


###########################################������###########################################
if __name__=='__main__':

    TipsFunc.WrtLog('********************���������ļ�����ʼ********************')

    #��ѯ���ύ��δ��ص������ļ�=================================================================
    TipsFunc.WrtLog('>>>��ѯ���ύ��δ��ص������ļ�')
    sql = "select WORKDATE,BATCHNO,TAXORGCODE,NOTE2,PAYEEBANKNO,PAYBKCODE,NOTE3 from TIPS_BATCHADM where DEALSTATUS  = '2' "
    TipsFunc.WrtLog( 'sql=' + sql )
    res = AfaDBFunc.SelectSql( sql )
    if( res == None ):
        TipsFunc.WrtLog('�������������쳣:'+AfaDBFunc.sqlErrMsg)
        TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )    
    elif( len(res) == 0):
        TipsFunc.WrtLog('>>>û����Ҫ���������')
        TipsFunc.ExitThisFlow( 'A0027', 'û����Ҫ���������' ) 
    for i in range(len(res)):
        TradeContext.entrustDate = res[i][0]      #����ί������
        TradeContext.packNo = res[i][1]           #����ί�к�
        TradeContext.taxOrgCode = res[i][2]       #���ջ��ش���
        TradeContext.sFileName = res[i][3]         #�ļ���
        TradeContext.payeeBankNo = res[i][4]       #�տ����к�
        TradeContext.payBkCode = res[i][5]         #�������к�
        
        TradeContext.sBrNo = TIPS_SBNO_QS                      #���׻�����
        TradeContext.sTeller = TIPS_TELLERNO_AUTO              #���׹�Ա��
        TradeContext.sTermId = '123456'                        #�ն˺�  
        TradeContext.sOpeFlag = '0'                            #������־0-	�����ռ��������˻����ļ� 1-	�����ռ�����ļ�

        #��ѯ�������˽��===============================================================================
        TipsFunc.WrtLog('>>>8834��ѯ�������˽��')
        if not TipsHostFunc.CommHost('8834'):
            TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
            continue
            #raise Exception,TradeContext.errorMsg
            
        if(HostContext.O1STCD !='2'):
            continue
                  
        if TradeContext.errorCode == "0000":
            TradeContext.sFileName = 'JD' + TradeContext.packNo    #�ļ���
            
            #�������������ļ�===========================================================================
            TipsFunc.WrtLog('>>>8833�������������ļ�')
            if not TipsHostFunc.CommHost('8833'):
                TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                continue
                #raise Exception,TradeContext.errorMsg
                
            #�������������ļ�===========================================================================
            TipsFunc.WrtLog('>>>�������������ļ�')
            #if(not TipsFunc.getHost('TPXCA','BANKMDS')):
            #if(not TipsFunc.getHost('NXSCA','BANKMDS')):
            if(not TipsFunc.getHost('JD'+ TradeContext.packNo + '.JD'+ TradeContext.packNo,'TIPSLIB')):
                TradeContext.errorCode, TradeContext.errorMsg= "S999","���������ļ��쳣"
                TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                #continue
                raise Exception,TradeContext.errorMsg
                
            #sFileName = '/home/maps/afa/data/batch/tips/JD' + TradeContext.packNo + '.JD'+ TradeContext.packNo
            #dFileName = '/home/maps/afa/data/batch/tips/TIPS_JD_' + TradeContext.packNo + '.txt'
            #fFileFld = 'tpxca.fld'
                
            #ת��=======================================================================================
            #TipsFunc.WrtLog('>>>ת��')
            #if not TipsFunc.FormatFile("0",sFileName,dFileName,fFileFld):
            #    TradeContext.errorCode, TradeContext.errorMsg= "S999","ת�����������ļ������쳣"
            #    raise Exception,TradeContext.errorMsg
            
            #ƥ���������̽��===========================================================================
            TipsFunc.WrtLog('>>>ƥ���������̽��')
            if(not MatchData()):
                TipsFunc.WrtLog( ">>>[" + TradeContext.errorCode + "]" + TradeContext.errorMsg)
                continue
                #raise Exception,TradeContext.errorMsg
                
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
                #raise Exception,TradeContext.errorMsg

    TipsFunc.WrtLog('********************���������ļ��������********************')
