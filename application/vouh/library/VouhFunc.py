# -*- coding: gbk -*-
########################################################################
#    ��    ��:    VouhFunc.py
#    ˵    ��:    ƾ֤����ϵͳ���ܿ�
#    ��    ��:    �м�ҵ����ƽ̨��AFA��--- UNIX: AIX 5.3 python
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11��
#    ά����¼:
########################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools,  AfaFlowControl, AfaDBFunc,os��ConfigParser
import time
from types import *
#AfaFunc,,ftplib,ConfigParser

########################################################################
#    ��    ��:    VouhModify( )
#    ��    ��:    �Ǽ�ƾ֤����Ǽǲ�
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11��
#    ��    ��:    ͨ���ڲ���������
#    �� �� ֵ:    0    �ɹ�
#                 -1   ���в�����
########################################################################
def VouhModify( ):
    #�жϱ��ı����Ƿ���ڣ���������ֵ���ڲ����������ڲ������ݿ�
    if( TradeContext.existVariable( "sLstTrxDay" ) ):
        _sWorkDate_    = TradeContext.sLstTrxDay       #��������
    else:
        _sWorkDate_    = ''
    if( TradeContext.existVariable( "sLstTrxTime" ) ):
        _sWorkTime_    = TradeContext.sLstTrxTime      #����ʱ��
    else:
        _sWorkTime_    = ''
    if( TradeContext.existVariable( "sBesbNo" ) ):
        _sBESBNO_      = TradeContext.sBesbNo          #������
    else:
        _sBESBNO_      = ''
    if( TradeContext.existVariable( "sCur" ) ):
        _sCur_      = TradeContext.sCur          #���Ҵ���
    else:
        _sCur_      = ''
    if( TradeContext.existVariable( "sTellerTailNo" ) ):
        _sTellerTailNo_    = TradeContext.sTellerTailNo        #���׹�Աβ���
    else:
        _sTellerNo_    = ''
    if( TradeContext.existVariable( "sVouhSerial" ) ):
        _sVouhSerial_    = TradeContext.sVouhSerial    #������ˮ��
    else:
        _sVouhSerial_    = GetVouhSerial( )
    if( TradeContext.existVariable( "sRivTeller" ) ):
        _sRivTeller_   = TradeContext.sRivTeller       #�Է���Աβ���
    else:
        _sRivTeller_   = ''
    if( TradeContext.existVariable( "sDepository" ) ):
        _sDepository_  = TradeContext.sDepository      #�����־
    else:
        _sDepository_  = ''
    if( TradeContext.existVariable( "sExDepos" ) ):
        _sExDepos_     = TradeContext.sExDepos         #ԭ�����־
    else:
        _sExDepos_     = ''
    if( TradeContext.existVariable( "sVouhStatus" ) ):
        _sVouhStatus_  = TradeContext.sVouhStatus      #״̬
    else:
        _sVouhStatus_  = ''
    if( TradeContext.existVariable( "sExStatus" ) ):
        _sExStatus_    = TradeContext.sExStatus        #ԭ״̬
    else:
        _sExStatus_    = ''
    if( TradeContext.existVariable( "sAuthTeller" ) ):
        _sAuthTeller_     = TradeContext.sAuthTeller         #��Ȩ��Ա
    else:
        _sAuthTeller_     = ''
    if( TradeContext.existVariable( "sTransType" ) ):
        _sTransType_  = TradeContext.sTransType      #ƾ֤״̬
    else:
        _sTransType_  = ''
    if(not TradeContext.existVariable( "sNum" ) ):
        TradeContext.sNum = 1      #�ظ�����

        
    for i in range(TradeContext.sNum):
        if( TradeContext.existVariable( "sVouhType" ) ):
            _sVouhType_    = TradeContext.sVouhType[i]        #ƾ֤����
        else:
            _sVouhType_    = ''
        if( TradeContext.existVariable( "sStartNo" ) ):
            _sStartNo_     = TradeContext.sStartNo[i]         #��ʼ����
        else:
            _sStartNo_     = ''
        if( TradeContext.existVariable( "sEndNo" ) ):
            _sEndNo_       = TradeContext.sEndNo[i]           #��ֹ����
        else:
            _sEndNo_       = ''
        if( TradeContext.existVariable( "sVouhNum" ) ):
            _sVouhNum_       = TradeContext.sVouhNum[i]           #ƾ֤����
        else:
            _sVouhNum_       = ''
           
        #���ڲ�����ƴ�������ݿ�SQL
        sqlStrInsert = "insert into VOUH_MODIFY ( VOUHSERIAL, WORKDATE, WORKTIME,VOUHNUM, BESBNO, TELLERNO, CUR ,\
        VOUHTYPE, STARTNO, ENDNO, RIVTELLER, DEPOSITORY, EXDEPOS, VOUHSTATUS, EXSTATUS,TRANSTYPE) \
        VALUES ('" + _sVouhSerial_ + "','" + _sWorkDate_ + "','" + _sWorkTime_ + "','"+ _sVouhNum_ + "','" + _sBESBNO_ +  "','" \
            + _sTellerTailNo_ + "','" + _sCur_+ "','" + _sVouhType_+"','" \
            + _sStartNo_ + "','" + _sEndNo_ + "','" + _sRivTeller_ + "','" + _sDepository_ + "','" \
            + _sExDepos_ + "','" + _sVouhStatus_ + "','" + _sExStatus_ + "','" + _sTransType_  + "')"
        AfaLoggerFunc.tradeInfo( sqlStrInsert )
        records = AfaDBFunc.InsertSql( sqlStrInsert )
        if records == -1 :
            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
            record = AfaDBFunc.RollbackSql( )
            tradeExit('A005061', '����[ƾ֤��ˮ��]�����쳣!')
            raise AfaFlowControl.flowException( )
            return -1

    return 0

########################################################################
#    ��    ��:    ModifyVouhModify( )
#    ��    ��:    ����ƾ֤����Ǽǲ�
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11��
#    ��    ��:    ͨ���ڲ���������
#    �� �� ֵ:    0    �ɹ�
#                 -1   ���в�����
########################################################################
def ModifyVouhModify():
    if(not TradeContext.existVariable( "HostDate" )):
                TradeContext.HostDate = '' 

    #������ˮ��
    sqlUpdate = "update VOUH_MODIFY SET TRANSTATUS = '" + TradeContext.sTranStatus + "',\
                HOSTDATE = '" + TradeContext.HostDate + "',\
                HOSTSERIAL = '" + TradeContext.HostSerno + "' where VOUHSERIAL = '" + TradeContext.sVouhSerial + "'"
    record = AfaDBFunc.UpdateSqlCmt( sqlUpdate )
    if record == -1 or record == 0 :
        tradeExit('A005062', '������ˮ��ʧ��!')
        raise AfaFlowControl.flowException( )

########################################################################
#    ��    ��:    GetVouhSerial( )
#    ��    ��:    ȡƾ֤�������к�
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11��
#    ��    ��:    ��
#    �� �� ֵ:    0    �ɹ�
#                 -1   ���в�����
########################################################################
def GetVouhSerial( ):
    sqlStr = "SELECT NEXTVAL for VOUH_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1 "
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        TradeContext.errorCode = 'A000001'
        TradeContext.errorMsg = AfaDBFunc.sqlErrMsg
    else:
        TradeContext.sVouhSerial = str( records[0][0] )
    return str( records[0][0] )



######################################################################
#    ��    ��:    DelSpace( a )
#    ��    ��:    ȥ��list�еĿ��ֶ�
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11��
#    ��    ��:    list
#    �� �� ֵ:    0    �ɹ�
#                 -1   ���в�����
#####################################################################
def DelSpace( a ):
    b=[]
    for i in range(len(a)):
        if( len(a[i]) <> 0 ):
            b.append(a[i])
    return b
    
######################################################################
#    ��    ��:    AddSplit( a )
#    ��    ��:    listװ���ַ���
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ˾:    ������ͬ�Ƽ�
#    ������ַ:    ����
#    ����ʱ��:    2008��6��11��
#    ��    ��:    list
#    �� �� ֵ:    0    �ɹ�
#                 -1   ���в�����
#####################################################################
def AddSplit( a ):
    b=''
    for i in range(len(a)):
        if(i==0):
            splitStr=''
        else:
            splitStr='|'
        b = b + splitStr + a[i]
    return b
    
##################################################################
#   ƾ֤����ϵͳ.FTP����ģ��
#=================================================================
#   ��    ��:   getVouh()
#   ��    ��:   ���ǽ�
#   �޸�ʱ��:   2008-06-11
##################################################################

#def getVouh(file_path):
#    try:
#        host_home="run/ftr"
#        local_home = os.environ['AFAP_HOME'] + "/data/vouh/"
#        
#        config = ConfigParser.ConfigParser( )
#        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
#        config.readfp( open( configFileName ) )
#        
#        ftp_p=ftplib.FTP(config.get('host','ip'),config.get('host','username'),config.get('host','password' ))
#        ftp_p.cwd(host_home)
#        file_handler = open(local_home + file_path,'wb')
#        ftp_p.retrbinary("RETR " + file_path,file_handler.write)
#        file_handler.close()
#        ftp_p.quit()
#        
#        if not os.path.exists(local_home + file_path):
#            raise Exception,"�ļ�[" + local_home + file_path + "]����ʧ��"
#        
#        return True
#        
#    except Exception, e:
#        AfaLoggerFunc.tradeInfo(e)
#        return False
#
    
def putHost(file_path):
    try:
        host_home="textlib"
        local_home = os.environ['AFAP_HOME'] + "/data/vouh/"
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open( configFileName ) )
        
        if not os.path.exists(local_home + file_path):
            raise Exception,"�ϴ��ļ�[" + local_home + file_path + "]������"
            
        ftp_p=ftplib.FTP(config.get('HOST_DZ','HOSTIP'),config.get('HOST_DZ','USERNO'),config.get('HOST_DZ','PASSWD' ))
        ftp_p.cwd(host_home)
        file_handler = open(local_home + file_path,'rb')
        ftp_p.storbinary("STOR " + file_path,file_handler)
        file_handler.close()
        ftp_p.quit()
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
        
##################################################################
#   ƾ֤����ϵͳ.��ʽ���ļ�
#=================================================================
#   ��    ��:   FormatFile(ProcType, sFileName, dFileName)
#   ��    ��:   ���ǽ�
#   �޸�ʱ��:   2008-06-11
##################################################################
#��ʽ���ļ�
def FormatFile(ProcType, sFileName, dFileName):

#    WrtLog('>>>��ʽ���ļ�:' + ProcType + ' ' + sFileName + ' ' + dFileName)

    try:

        srcFileName    = os.environ['AFAP_HOME'] + '/data/vouh/' + sFileName
        dstFileName    = os.environ['AFAP_HOME'] + '/data/vouh/' + dFileName

        if (ProcType == "1"):
            #ascii->ebcd
            #���ø�ʽ:cvt2ebcdic -T Դ�ı��ļ� -P Ŀ�������ļ� -F fld��ʽ�ļ� [-D ����� ]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ebcdic'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/vouh/cvt/TPCZA.fld'
            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName + " -D '|'"

        else:
            #ebcd->ascii
            #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D ���-��] [-S] [-R]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/vouh/cvt/vouh02.fld'
            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName

        AfaLoggerFunc.tradeInfo('>>>' + cmdstr)
        #ret = -1
        AfaLoggerFunc.tradeInfo('>>>�����ʽת������ʼ============')   #2007824
        ret = os.system(cmdstr)                         #2007824
        if ( ret != 0 ):                                #2007824
            ret = False                                 #2007824
        else:                                           #2007824
            ret = True                                  #2007824
        #return 0                                       #2007824
        AfaLoggerFunc.tradeInfo('>>>�����ʽת���������============')   #2007824

        return ret
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        AfaLoggerFunc.tradeInfo('��ʽ���ļ��쳣')
        return False
        
########################################################################
#    ��    ��:    SelectBesbSty( sBesbNo)
#    ��    ��:    ��ѯ��������
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ��:    sBesbNo   - ������ 
#    ������ַ:    ����
#    ����ʱ��:    2008��6��18��
#    
#    �� �� ֵ:    
#                 
########################################################################
def SelectBesbSty( sBesbNo):
    #=============ǰ̨��������====================
    #TradeContext.sBESBNO           ������
    #TradeContext.sBesbSty          ��������
    
    try:
        
        sqlStr = "SELECT SBSBCH FROM VOUH_FRONT_CRSBA WHERE SBSBNO ='" + sBesbNo + "'"
     
        records = AfaDBFunc.SelectSql( sqlStr)
        if( records == None ):
            tradeExit('A005067', '��ѯ[������]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '����������!' )
            raise AfaFlowControl.flowException( )

        return str(records[0][0])
            
            
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
        
########################################################################
#    ��    ��:    SelectSBTPAC( sBesbNo)
#    ��    ��:    ��ѯ�����ϼ�
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ��:    sBesbNo   - ������ 
#    ������ַ:    ����
#    ����ʱ��:    2008��6��18��
#    
#    �� �� ֵ:    
#                 
########################################################################
def SelectSBTPAC( sBesbNo):
    #=============ǰ̨��������====================
    #TradeContext.sBESBNO           ������
    #TradeContext.sSBTPAC           �����ϼ�
    
    try:
        
        sqlStr = "SELECT SBTPAC FROM VOUH_FRONT_CRSBA WHERE SBSBNO ='" + sBesbNo + "'"
     
        records = AfaDBFunc.SelectSql( sqlStr)
        if( records == None ):
            tradeExit('A005067', '��ѯ[������]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '����������!' )
            raise AfaFlowControl.flowException( )

        return str(records[0][0])
            
            
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
        
########################################################################
#    ��    ��:    SelectBesbName( sBesbNo)
#    ��    ��:    ��ѯ��������
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ��:    sBesbNo   - ������ 
#    ������ַ:    ����
#    ����ʱ��:    2008��6��18��
#    
#    �� �� ֵ:    
#                 
########################################################################
def SelectBesbName( sBesbNo):
    #=============ǰ̨��������====================
    #TradeContext.sBESBNO           ������
    #TradeContext.sBesbSty          ��������
    
    try:
        
        sqlStr = "SELECT SBSBNM FROM VOUH_FRONT_CRSBA WHERE SBSBNO ='" + sBesbNo + "'"
     
        records = AfaDBFunc.SelectSql( sqlStr)
        if( records == None ):
            tradeExit('A005067', '��ѯ[������]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):
            tradeExit('A005068', '����������!' )
            raise AfaFlowControl.flowException( )

        return str(records[0][0])
            
            
    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( )
    except AfaFlowControl.accException:
        AfaFlowControl.exitMainFlow( )
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
        
#=============���ش�����,������Ϣ===================================
def tradeExit( code, msg ):
    TradeContext.errorCode, TradeContext.errorMsg=code, msg
    if code != '0000':
        return False
    return True
    
########################################################################
#    ��    ��:    VouhTrans( )
#    ��    ��:    ���׹�������
#    ��    ��:    �м�ҵ��ƽ̨�� ---  python
#    ��    ��:    ���ǽ�
#    ��    ��:    �� 
#    ������ַ:    ����
#    ����ʱ��:    2008��6��18��
#    
#    �� �� ֵ:    
#                 
########################################################################
def VouhTrans( ):
    #===��������������ƾ֤����������״̬Ϊ��1��(�ѳ�δ��)��ƾ֤�����������־======
    #sFlagContinue:continue:ǰ������;
    #sFlagContinue:FrontContinue:ǰ����;
    #sFlagContinue:BackContinue:������;
    sFlagContinue = ''
    
    #=============����ƾ֤���⽻��==========================
    
    #1.��ѯ��Ҫ�����ƾ֤��ֹ�����Ƿ��ڿ��������δ����ƾ֤���뷶Χ��
    #2.�����Ҫ�����ƾ֤��ֹ�����ڿ���пɳ����ƾ֤���뷶Χ��,��ô��Ҫ
    #  �жϿ��������ƾ֤״̬Ϊ�ѷ�δ��,��������ǩ����Ա���ڵ���һ���⼸�������ļ�¼
    #�������ƾ֤�����Ƿ���������ϵ
    #3.�����������ϵ,��ô��Ҫ�ж������ƾ֤��ֹ������������Ӧ��ƾ֤��������Ĺ�ϵ
    #  1)�������ʼ�������������ʼ������ͬ. 2)�������ֹ����������Ľ���������ͬ
    #  3)�������ʼ�������ֹ������������ʼ�ͽ������붼��ͬ. 4)�������ֹ������ȫ������֮��
    #4.�����������ϵ,��ô��Ҫ�ж������ƾ֤��ֹ����������ƾ֤״̬Ϊ�ѷ�δ���
    #ƾ֤����֮��Ĺ�ϵ  1) ǰ���� 2)������  3)ǰ������
    
    for i in range(TradeContext.sNum):
        
        #beginƾ֤�Ż�201202 ������
        Len=''
        Len = int(len(TradeContext.sStartNo[i]))
        
        #=============���������ƾ֤����==========================
        sStartNoMulti = str(int( TradeContext.sStartNo[i] ) - 1).rjust(Len,'0')
        sEndNoAdd = str(int( TradeContext.sEndNo[i] ) + 1).rjust(Len,'0')
        #end
        
        #��ѯ���ݿ�[ƾ֤�ǼǱ�],ȷ���Ƿ������ƾ֤��ʼ����,��ֹ�����ڸù�Ա��½����
        #�Ǽ�δ��״̬��ƾ֤�������
        sqlStr = "select STARTNO,ENDNO,LSTTRXDAY,LSTTRXTIME,RIVTELLER,TELLERNO \
            from VOUH_REGISTER \
            where VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
            and BESBNO = '" + TradeContext.sBesbNo + "'\
            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
            and CUR = '" + TradeContext.sCur + "'\
            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
            and ( ENDNO >= '" + TradeContext.sEndNo[i] + "' and STARTNO <= '" + TradeContext.sStartNo[i] + "' )"
        records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeDebug(sqlStr)
        if( records == None ):          #��ѯƾ֤�ǼǱ��쳣
            if( i > 0 ):
                AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                AfaDBFunc.RollbackSql( )
            tradeExit('A005061', '��ѯ[ƾ֤�ǼǱ�]�����쳣!')
            raise AfaFlowControl.flowException( )
        elif( len( records ) == 0 ):    #���ƾ֤�ǼǱ����޶�Ӧ��¼
            if( i > 0 ):
                AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                AfaDBFunc.RollbackSql( )
            tradeExit('A005067', 'ƾ֤����ʧ��,ƾ֤���в����ڱ��β�����ƾ֤!')
            raise AfaFlowControl.flowException( )
        else :
            records = AfaUtilTools.ListFilterNone( records )
            sTempStartNo = records[0][0]           #���������ƾ֤�������ڵ�������ʼƾ֤����
            sTempEndNo   = records[0][1]           #���������ƾ֤�������ڵ�������ֹƾ֤����
            sTempLstTrxDay   = records[0][2]       #���������ƾ֤�������ڵ��������������
            sTempLstTrxTime  = records[0][3]       #���������ƾ֤�������ڵ����������ʱ��
            sTempRivTeller   = records[0][4]       #���������ƾ֤�������ڵ�����Է���Ա
            sTempTellerNo   = records[0][5]        #���������ƾ֤�������ڵ�����Է���Ա
        
            #�������ƾ֤��ֹ����Ϊ�Ϸ�����ʱ,��ѯ���������״̬Ϊ�ѷ�δ��,
            #��Ա�ŵ�������ǩ����Ա���ڵ���һ�µ������ļ�¼�������ƾ֤�����Ƿ���������ϵ
            sqlStr = "select STARTNO,ENDNO from VOUH_REGISTER \
                    where VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                    and BESBNO = '" + TradeContext.sInBesbNo + "'\
                    and TELLERNO = '" + TradeContext.sInTellerTailNo + "'\
                    and CUR = '" + TradeContext.sCur + "'\
                    and DEPOSITORY = '" + TradeContext.sDepository + "'\
                    and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                    and ( ENDNO = '" + sStartNoMulti + "' \
                    OR STARTNO = '" + sEndNoAdd + "' )"
    
            AfaLoggerFunc.tradeDebug(sqlStr)
            records = AfaDBFunc.SelectSql( sqlStr )
            records = AfaUtilTools.ListFilterNone( records )
            if( records == None ):          #��ѯƾ֤�ǼǱ��쳣
                if( i > 0 ):
                    AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                    AfaDBFunc.RollbackSql( )
                tradeExit('A005061', '��ѯ[ƾ֤�ǼǱ�]�����쳣!')
                raise AfaFlowControl.flowException( )
        
            #�����ƾ֤����������Ѵ��ڵ�״̬Ϊ�Ǽ�δ����ƾ֤������������ϵ
            elif( len( records ) == 0 ):
                #�������ʼ�������ֹ������������ʼ�ͽ������붼��ͬ
                if ( int( TradeContext.sEndNo[i] ) == int( sTempEndNo ) \
                    and int( TradeContext.sStartNo[i] ) == int( sTempStartNo ) ):
                    #ֱ�Ӹ��¶�Ӧ��¼
                    sqlStr = "update VOUH_REGISTER set \
                           DEPOSITORY = '"+TradeContext.sDepository+"',\
                           VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "',\
                           BESBNO = '" + TradeContext.sInBesbNo + "', \
                           TELLERNO = '" + TradeContext.sInTellerTailNo + "', \
                           RIVTELLER = '" + TradeContext.sTellerTailNo + "', \
                           LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                           LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + TradeContext.sStartNo[i] + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR = '"+ TradeContext.sCur+"'"
    
                    AfaLoggerFunc.tradeDebug('1'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
                    else:
                        tradeExit('0000', TradeContext.sTransType+'�ɹ�')
        
                #�������ֹ����������Ľ���������ͬ
                elif ( int( TradeContext.sEndNo[i] ) == int( sTempEndNo ) ):
                    #�������ݿ����Ѵ��¼,���³ɹ��������������¼
                    sqlStr = "update VOUH_REGISTER set \
                      VOUHNUM = '"+ ( str( int( TradeContext.sStartNo[i] ) - int( sTempStartNo ) ) )+ "',\
                      ENDNO = '" + sStartNoMulti + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + sTempStartNo + "' \
                       and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                       and BESBNO = '" + TradeContext.sBesbNo + "'\
                       and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                       and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                       and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                       and CUR ='"+ TradeContext.sCur+"'"
    
                    AfaLoggerFunc.tradeDebug('2'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
                    else:
                        #���³ɹ��������������¼
                        sqlStr = "insert into VOUH_REGISTER \
                         (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,\
                          VOUHSTATUS,VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                          values \
                          ('" + TradeContext.sInBesbNo + "',\
                           '" + TradeContext.sInTellerTailNo + "','"+TradeContext.sDepository+"','"+ TradeContext.sCur+"',\
                           '"+ TradeContext.sVouhType[i] + "',\
                           '" + TradeContext.sStartNo[i] + "','" + sTempEndNo + "',\
                           '" + TradeContext.sTellerTailNo +"','"+ TradeContext.sVouhStatus+ "',\
                           '" + TradeContext.sVouhNum[i] + "',\
                           '" + TradeContext.sLstTrxDay + "','" + TradeContext.sLstTrxTime + "')"
                        record = AfaDBFunc.InsertSql( sqlStr )
                        if record == -1 or record == 0:
                            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                            raise AfaFlowControl.flowException( )
                        else: #����ɹ�
                            tradeExit('0000', TradeContext.sTransType+'�ɹ�')
        
                #�������ʼ�������������ʼ������ͬ
                elif ( int( TradeContext.sStartNo[i] ) == int( sTempStartNo ) ):
                    #�������ݿ����Ѵ��¼,���³ɹ��������������¼
                    sqlStr = "update VOUH_REGISTER set \
                        VOUHNUM = '" + str( int( sTempEndNo ) - int ( TradeContext.sEndNo[i] ) )+ "',\
                        STARTNO = '" + sEndNoAdd + "'"
                    sqlStr = sqlStr + " where ENDNO = '" + sTempEndNo + "' \
                        and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                        and BESBNO = '" + TradeContext.sBesbNo + "'\
                        and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                        and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                        and CUR ='"+ TradeContext.sCur+"'"
    
                    AfaLoggerFunc.tradeDebug('3'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
                    else:
                        #���³ɹ��������������¼
                        sqlStr = "insert into VOUH_REGISTER \
                           (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,\
                            VOUHSTATUS,VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                            values \
                            ('" + TradeContext.sInBesbNo + "',\
                             '" + TradeContext.sInTellerTailNo + "','"+TradeContext.sDepository+"',\
                             '" + TradeContext.sCur+"',\
                             '" + TradeContext.sVouhType[i]+"',\
                             '" + sTempStartNo + "',\
                             '" + TradeContext.sEndNo[i] + "','"+TradeContext.sTellerTailNo+"',\
                             '" + TradeContext.sVouhStatus+ "','" + TradeContext.sVouhNum[i] + "',\
                             '" + TradeContext.sLstTrxDay + "',\
                             '" + TradeContext.sLstTrxTime + "')"
                        AfaLoggerFunc.tradeDebug('1'+sqlStr)
                        record = AfaDBFunc.InsertSql( sqlStr )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                            raise AfaFlowControl.flowException( )
                        else: #����ɹ�
                            tradeExit('0000', TradeContext.sTransType+'�ɹ�')
                #�������ֹ������ȫ����������֮��
                else:
                    #1�������ݿ����Ѵ��¼,���³ɹ��������������¼����Ӧ�Ǽ�δ��״̬��¼
                    sqlStr = "update VOUH_REGISTER set \
                       VOUHNUM = '" + str( int( TradeContext.sStartNo[i] ) - int( sTempStartNo ) ) + "',\
                       ENDNO = '" + sStartNoMulti + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + sTempStartNo + "' \
                        and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                        and BESBNO = '" + TradeContext.sBesbNo + "'\
                        and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                        and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                        and CUR ='"+ TradeContext.sCur+"'"
    
                    AfaLoggerFunc.tradeDebug('4'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', '����[ƾ֤�ǼǱ�]������Ϣʧ��!')
                        raise AfaFlowControl.flowException( )
    
                    #2##############���³ɹ��������������¼###########################################
                    sqlStr = "insert into VOUH_REGISTER \
                       (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,\
                        VOUHSTATUS,VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                        values \
                        ('" + TradeContext.sInBesbNo + "',\
                         '" + TradeContext.sInTellerTailNo + "','"+TradeContext.sDepository+"',\
                         '" + TradeContext.sCur+"',\
                         '" + TradeContext.sVouhType[i]+"',\
                         '" + TradeContext.sStartNo[i] + "',\
                         '" + TradeContext.sEndNo[i] + "','"+TradeContext.sTellerTailNo+"',\
                         '" + TradeContext.sVouhStatus+ "','" + TradeContext.sVouhNum[i] + "',\
                         '" + TradeContext.sLstTrxDay + "',\
                         '" + TradeContext.sLstTrxTime + "')"
                    AfaLoggerFunc.tradeDebug('2'+sqlStr)
                    record = AfaDBFunc.InsertSql( sqlStr )
                    if record == -1 or record == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
    
                    #3�������������¼�ɹ���,������Ӧ�Ǽ�δ��״̬��¼
                    sqlStr = "insert into VOUH_REGISTER \
                      (BESBNO,TELLERNO,DEPOSITORY,CUR,VOUHTYPE,STARTNO,ENDNO,RIVTELLER,\
                        VOUHSTATUS,VOUHNUM,LSTTRXDAY,LSTTRXTIME) \
                       values \
                       ('" + TradeContext.sBesbNo + "',\
                        '" + sTempTellerNo + "','"+TradeContext.sExDepos+ "','"+TradeContext.sCur+"',\
                        '" + TradeContext.sVouhType[i]+"',\
                        '" + sEndNoAdd + "',\
                        '" + sTempEndNo + "','"+sTempRivTeller+"',\
                        '"+ TradeContext.sExStatus+ "',\
                        '" + str( int( sTempEndNo ) - int ( TradeContext.sEndNo[i] ) )+ "',\
                        '" + sTempLstTrxDay + "',\
                        '" + sTempLstTrxTime + "')"
                    AfaLoggerFunc.tradeDebug('3'+sqlStr)
                    record = AfaDBFunc.InsertSql( sqlStr )
                    if record == -1 or record == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
                    #�����ɹ�
                    tradeExit('0000', '�����ɹ�')
        
            else:      #�ж�ǰ��������ϵ
                #continue:ǰ��������ʶ;
                #FrontContinue:ǰ������ʶ;
                #BackContinue:��������ʶ;
                for x in range( len(records) ):
                    if ( ( int( TradeContext.sStartNo[i] ) - 1 )  == int( records[x][1] ) ): #ǰ����
                        sTempStart = records[x][0] #records[x][0]:���ݿ��������ѯ������ƾ֤��ʼ����
                        if ( sFlagContinue == 'BackContinue' ):
                            sFlagContinue = 'Continue'
                        else:
                            sFlagContinue = 'FrontContinue'
                    if ( (int( TradeContext.sEndNo[i]) + 1 )  == int( records[x][0] ) ):  #������
                        sTempEnd   = records[x][1] #records[x][1]:���ݿ��������ѯ������ƾ֤��ֹ����
                        if ( sFlagContinue == 'FrontContinue' ):
                            sFlagContinue = 'Continue'
                        else:
                            sFlagContinue = 'BackContinue'
        
                #�����ƾ֤����������ͬƾ֤״̬Ϊ�Ǽ�δ���ļ�¼���ں�������ϵ,
                #������Ӧ�ļ�¼�������鲢
                if (  sFlagContinue == 'BackContinue' ):
                    #1������:������Ӧ���ݿ���[ƾ֤�ǼǱ�]��Ӧ��¼
                    sqlStr = "update VOUH_REGISTER set \
                      VOUHNUM = '" + str( int( sTempEnd ) - int( TradeContext.sStartNo[i] ) + 1 ) + "',\
                      LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                      LSTTRXTIME = '" + TradeContext.sLstTrxTime + "',\
                      STARTNO = '" + TradeContext.sStartNo[i] + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + sEndNoAdd  + "'\
                      and TELLERNO = '" + TradeContext.sInTellerTailNo + "' \
                      and BESBNO = '" + TradeContext.sInBesbNo + "'\
                      and CUR = '" + TradeContext.sCur + "'\
                      and DEPOSITORY = '" + TradeContext.sDepository + "'\
                      and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                      and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'"
                    AfaLoggerFunc.tradeDebug('5'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
    
                        #2���³ɹ���,ɾ����ʼ����ΪsTempStartNo��ԭ��¼,����ƾ֤����Ϊ1
                    if ( int( sTempStartNo ) == int( TradeContext.sStartNo[i] ) ) :
                        sqlDel = "delete from VOUH_REGISTER \
                            where STARTNO = '" + sTempStartNo + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
                        AfaLoggerFunc.tradeDebug(sqlDel)
                        record = AfaDBFunc.DeleteSql( sqlDel )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                            raise AfaFlowControl.flowException( )
                        else:
                            tradeExit('0000', TradeContext.sTransType+'�ɹ�')
                    else:
                        #���³ɹ���,������ֹ����ΪTradeContext.sEndNo��ԭ��¼,����ƾ֤��������1
                        sqlStr = "update VOUH_REGISTER set \
                          VOUHNUM = '" + str( int( TradeContext.sStartNo[i] ) - int( sTempStartNo ) )+ "',\
                          LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                          LSTTRXTIME = '" + TradeContext.sLstTrxTime + "',\
                          ENDNO = '" +  sStartNoMulti  + "'"
                        sqlStr = sqlStr + " where ENDNO = '" + TradeContext.sEndNo[i] + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
    
                        AfaLoggerFunc.tradeDebug('6'+sqlStr)
                        record = AfaDBFunc.UpdateSql( sqlStr )
                        if record == -1 or record == 0:
                            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                            record = AfaDBFunc.RollbackSql( )  #�ع�
                            tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                            raise AfaFlowControl.flowException( )
                        else:
                            tradeExit('0000', '�����ɹ�')
        
                #�����ƾ֤����������ͬƾ֤״̬Ϊ�Ǽ�δ������ǰ������ϵ,
                #������Ӧ�ļ�¼������ǰ�鲢
                elif ( sFlagContinue == 'FrontContinue' ):
                    #ǰ����:������Ӧ���ݿ���[ƾ֤�ǼǱ�]��Ӧ��¼
                    sqlStr = "update VOUH_REGISTER set \
                       VOUHNUM = '" + str( int( TradeContext.sEndNo[i] ) - int( sTempStart ) + 1 ) + "',\
                       LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                       LSTTRXTIME = '" + TradeContext.sLstTrxTime + "',\
                       ENDNO = '" + ( TradeContext.sEndNo[i] ) + "'"
                    sqlStr = sqlStr + " where ENDNO = '" + sStartNoMulti + "'\
                        and TELLERNO = '" + TradeContext.sInTellerTailNo + "' \
                        and BESBNO = '" + TradeContext.sInBesbNo + "'\
                        and CUR = '" + TradeContext.sCur + "'\
                        and DEPOSITORY = '" + TradeContext.sDepository + "'\
                        and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'"
    
                    AfaLoggerFunc.tradeDebug('7'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        AfaDBFunc.RollbackSql( )  #�ع�
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
    
                    #2���³ɹ���,ɾ����ʼ����ΪsTempStartNo��ԭ��¼,����ƾ֤����Ϊ1
                    if ( int( sTempEndNo ) == int( TradeContext.sEndNo[i] ) ) :
                        sqlDel = "delete from VOUH_REGISTER \
                            where STARTNO = '" + sTempStartNo + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
    
                        AfaLoggerFunc.tradeDebug(sqlDel)
                        record = AfaDBFunc.DeleteSql( sqlDel )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                            raise AfaFlowControl.flowException( )
                        else:    #���³ɹ�
                            tradeExit('0000', '�����ɹ�')
                    else:
                        #���³ɹ���,������ʼ����ΪTradeContext.sStartNo��ԭ��¼,����ƾ֤��������1
                        sqlStr = "update VOUH_REGISTER set \
                           VOUHNUM = '" + str( int( sTempEndNo ) - int( TradeContext.sEndNo[i] ) ) + "',\
                           LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                           LSTTRXTIME = '" + TradeContext.sLstTrxTime + "',\
                           STARTNO = '" + sEndNoAdd  + "'"
                        sqlStr = sqlStr + " where STARTNO = '" + TradeContext.sStartNo[i] + "' \
                           and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
    
                        AfaLoggerFunc.tradeDebug('8'+sqlStr)
                        record = AfaDBFunc.UpdateSql( sqlStr )
                        if record == -1 or record == 0 :
                            AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                            record = AfaDBFunc.RollbackSql( )
                            tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                            raise AfaFlowControl.flowException( )
                        else:   #���³ɹ�
                            tradeExit('0000', '�����ɹ�')
        
            #�����ƾ֤����������ͬƾ֤״̬Ϊ�Ǽ�δ������ǰ��������ϵ,
            #������Ӧ�ļ�¼����ǰ��鲢
                elif (  sFlagContinue == 'Continue' ):
                    sTemVouhNum = str( int(sTempEnd) - int(sTempStart) + 1 )
                    #�������ݿ��[ƾ֤�ǼǱ�]����Ӧ��¼
                    sqlStr = "update VOUH_REGISTER set \
                       ENDNO = '" + sTempEnd + "', \
                       VOUHNUM = '" + sTemVouhNum + "',\
                       LSTTRXDAY = '" + TradeContext.sLstTrxDay + "',\
                       LSTTRXTIME = '" + TradeContext.sLstTrxTime + "'"
                    sqlStr = sqlStr + " where STARTNO = '" + sTempStart + "' \
                       and TELLERNO = '" + TradeContext.sInTellerTailNo + "' \
                        and BESBNO = '" + TradeContext.sInBesbNo + "'\
                        and CUR = '" + TradeContext.sCur + "'\
                        and DEPOSITORY = '" + TradeContext.sDepository + "'\
                        and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'"
    
                    AfaLoggerFunc.tradeDebug('9'+sqlStr)
                    records = AfaDBFunc.UpdateSql( sqlStr )
                    if records == -1 or records == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
    
                    #2�鲢�ɹ���,ɾ���鲢������һ��
                    sqlDel = "delete from VOUH_REGISTER \
                       where STARTNO = '" + TradeContext.sStartNo[i] + "' \
                            and DEPOSITORY = '" + TradeContext.sExDepos + "'\
                            and BESBNO = '" + TradeContext.sBesbNo + "'\
                            and TELLERNO = '" + TradeContext.sTellerTailNo + "'\
                            and VOUHSTATUS = '" + TradeContext.sExStatus+ "' \
                            and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "' \
                            and CUR ='"+ TradeContext.sCur+"'"
                    AfaLoggerFunc.tradeDebug(sqlDel)
                    record = AfaDBFunc.DeleteSql( sqlDel )
                    if record == -1 or record == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
                    # 3
                    sqlDel = "delete from VOUH_REGISTER \
                      where STARTNO = '" + sEndNoAdd + "' \
                        and TELLERNO = '" + TradeContext.sInTellerTailNo + "' \
                        and BESBNO = '" + TradeContext.sInBesbNo + "'\
                        and CUR = '" + TradeContext.sCur + "'\
                        and DEPOSITORY = '" + TradeContext.sDepository + "'\
                        and VOUHSTATUS = '"+ TradeContext.sVouhStatus+ "' \
                        and VOUHTYPE = '" + TradeContext.sVouhType[i]+ "'"
                    AfaLoggerFunc.tradeDebug(sqlDel)
                    record = AfaDBFunc.DeleteSql( sqlDel )
                    if record == -1 or record == 0 :
                        AfaLoggerFunc.tradeInfo( '���ݿ�ع�' )
                        record = AfaDBFunc.RollbackSql( )
                        tradeExit('A005062', TradeContext.sTransType+'ʧ��!')
                        raise AfaFlowControl.flowException( )
    
                    tradeExit('0000', '�����ɹ�')
                        
    return True
                        
#=========================��־==================================================
def WrtLog(logstr):

    #Ĭ�����ļ�����Ļͬʱ���
    AfaLoggerFunc.tradeInfo(logstr)
    print logstr

    return True             
                        
                        

if __name__=='__main__':

#    TradeContext.sLstTrxDay      = '1'   #��������
#    TradeContext.sLstTrxTime     = '1'   #����ʱ��
#    TradeContext.sZoneNo         = '1'   #���к�
#    TradeContext.sBraNo          = '1'   #������
#    TradeContext.sTellerNo       = '1'   #��Ա��
#    TradeContext.sVouhType       = '1'   #ƾ֤����
#    TradeContext.sHeadStr        = '1'   #���ֺ�
#    TradeContext.sStartNo        = '1'   #��ʼ����
#    TradeContext.sEndNo          = '1'   #��ֹ����
#    TradeContext.sRivTeller      = '1'   #�Է���Ա
#    TradeContext.sDepository     = '1'   #�����־
#    TradeContext.sExDepos        = '1'   #ԭ�����־
#    TradeContext.sVouhStatus     = '1'   #״̬
#    TradeContext.sExStatus       = '1'   #ԭ״̬
#    TradeContext.sSummary        = '1'   #ժҪ
#    AfaLoggerFunc.afa_SendStruct()
#    x = VouhModify()
#    print x
    print time.strftime( '%m%d%y%H%M%S', time.localtime( ) )
    sPid = "%08d"%( os.getpid( ))
    print sPid
