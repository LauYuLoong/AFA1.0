# -*- coding: gbk -*-
###############################################################################
# �ļ����ƣ�TipsFunc.py
# �ļ���ʶ��
# ժ    Ҫ����˰���к�������ϵͳ����������
#
# ��ǰ�汾��1.0
# ��    �ߣ�zzh
# ������ڣ�2007-6-7 
#
# ȡ���汾��
# ԭ �� �ߣ�
# ������ڣ�
###############################################################################
import exceptions, TradeContext, AfaDBFunc, TradeException, UtilTools,HostContext
import os, ConfigParser, time, Party3Context,AfaLoggerFunc,HostComm,AfaFlowControl,ftplib
from types import *

#======================����ִ���쳣��==========================
class flowException ( exceptions.Exception ): 

    def __init__( self, errorCode = None , errorMsg = None ):
        if errorCode != None and errorMsg != None :
            TradeContext.errorCode = errorCode
            TradeContext.errorMsg = errorMsg
    def __str__( self ):
        if TradeContext.existVariable("errorCode") and TradeContext.existVariable("errorMsg") and TradeContext.errorCode != None :
            return 'FlowException' + ': ' + TradeContext.errorMsg
        else:
            return 'FlowException'

#======================�������쳣��===========================
class accException ( exceptions.Exception ): 

    def __init__( self, errorCode = None , errorMsg = None ):
        if errorCode != None and errorMsg != None :
            TradeContext.errorCode = errorCode
            TradeContext.errorMsg = errorMsg
    def __str__( self ):
        if( TradeContext.existVariable("errorCode") and TradeContext.existVariable("errorMsg") and TradeContext.errorCode != None ):
            return 'AccException' + ': ' + TradeContext.errorMsg
        else:
            return 'AccException'

#==================���ڽ����쳣ʱ�˳���ִ������=====================
def exitMainFlow( msgStr='' ):
    if( not TradeContext.existVariable( "errorCode" ) or msgStr ):
        TradeContext.errorCode = 'A9999'
        TradeContext.errorMsg = 'ϵͳ����['+msgStr+']'
            
    if TradeContext.errorCode != '0000' :
        AfaLoggerFunc.tradeFatal( 'errorCode=['+TradeContext.errorCode+']' )
        AfaLoggerFunc.tradeFatal( 'errorMsg=['+TradeContext.errorMsg+']' )
        AfaLoggerFunc.tradeFatal(TradeContext.TransCode+'�����ж�')
        
    TradeContext.tradeResponse = [[ 'errorCode', TradeContext.errorCode ], [ 'errorMsg', TradeContext.errorMsg ]]
    
    if (TradeContext.existVariable ( 'agentSerialno')):
        TradeContext.tradeResponse.append( ['agentSerialno',TradeContext.agentSerialno] )
        
    raise TradeException.TradeException( TradeContext.errorMsg )

#=======================�����쳣ʱ�˳�����������===========================
def ExitThisFlow( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.errorCode = errorCode
        TradeContext.errorMsg = errorMsg
    if( TradeContext.errorCode.isdigit( )==True and long( TradeContext.errorCode )==0 ):
        return True
    else:
        return False

#=======================��ѯ�����ֵ����Ч��У��==========================
def Query_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '��ѯ�����ֵ����Ч��У��[begin]' )
    if( not TradeContext.existVariable( "trxCode" ) ):
        return ExitThisFlow( 'A0001', '���״���[trxCode]ֵ������!' )
                
    if( not TradeContext.existVariable( "channelCode" ) ):
        return ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    else:
        TradeContext.channelCode=UtilTools.Lfill( TradeContext.channelCode, 3, '0' )
               
    if( TradeContext.channelCode == '001' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return ExitThisFlow( 'A0001', '��������[brno]ֵ������!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return ExitThisFlow( 'A0001', '��Ա��[teller]ֵ������!' )
    
    AfaLoggerFunc.tradeInfo( '��ѯ�����ֵ����Ч��У��[end]' )        
    return True

#=======================�ɷ������ֵ����Ч��У��==========================
def Pay_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '�ɷ������ֵ����Ч��У��[begin]' )
    
    if ( not TradeContext.existVariable( "termId" ) ):
        return ExitThisFlow( 'A0001', '�ն˺�[termId]ֵ������!')
    
    if ( not TradeContext.existVariable( "catrFlag") ):
        return ExitThisFlow( 'A0001', '�ֽ�ת�ʱ�־[catrFlag]������!')    
           
    if( not TradeContext.existVariable( "channelCode" ) ):
        return ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    else:
        TradeContext.channelCode=UtilTools.Lfill( TradeContext.channelCode, 3, '0' )
    if( TradeContext.channelCode == '001' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return ExitThisFlow( 'A0001', '������[brno]ֵ������!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return ExitThisFlow( 'A0001', '��Ա��[teller]ֵ������!' )
    if( not TradeContext.existVariable( "amount" ) ):
        return ExitThisFlow( 'A0001', '���[amount]ֵ������!' )
    if( not TradeContext.existVariable( "userno" ) ):
        return ExitThisFlow( 'A0001', '�û���[userno]ֵ������!' )
    if( not TradeContext.existVariable( "accno" ) ):
        TradeContext.accno=''
        #TradeContext.accType='000'
        
    TradeContext.revTranF='0' #������
    AfaLoggerFunc.tradeInfo( '�ɷ������ֵ����Ч��У��[end]' )
    return True

#=======================ȡ�����ױ���ֵ����Ч��У��==========================
def Cancel_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( 'ȡ�����ױ���ֵ����Ч��У��' )
    if( not TradeContext.existVariable( "zoneno" ) ):
        return ExitThisFlow( 'A0001', '������[zoneno]ֵ������!' )
        
    if( not TradeContext.existVariable( "channelCode" ) ):
        return ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    else:
        TradeContext.channelCode=UtilTools.Lfill( TradeContext.channelCode, 3, '0' )
    
    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return ExitThisFlow( 'A0001', '�����[brno]ֵ������!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return ExitThisFlow( 'A0001', '��Ա��[teller]ֵ������!' )
    if( not TradeContext.existVariable( "amount" ) ):
        return ExitThisFlow( 'A0001', '���[amount]ֵ������!' )
        
    if( not TradeContext.existVariable( "preAgentSerno" ) ):
        return ExitThisFlow( 'A0001', 'ԭ������ˮ��[preAgentSerno]ֵ������!' )
        
            
    TradeContext.revTranF='1'
    return True


#У�鷴�������������� ������ˮ�űȶ��û��ţ��ʺţ����׽��
def ChkRevInfo( serialno ):

    AfaLoggerFunc.tradeInfo( 'У�鷴��������������[begin]' )
    sqlstr="SELECT REVTRANF,TAXPAYCODE,DRACCNO,CRACCNO,AMOUNT,TELLERNO,\
            TAXPAYNAME,TERMID,VOUHTYPE,VOUHNO,TAXVOUNO,CATRFLAG,\
            BANKSERNO, CORPSERNO,CORPTIME,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,\
            NOTE7,NOTE8,NOTE9,NOTE10,CATRFLAG,WORKDATE FROM TIPS_MAINTRANSDTL WHERE SERIALNO=" +\
            "'"+serialno+"' AND WORKDATE='"+TradeContext.workDate+ "'AND BANKSTATUS IN ('0','2')"  # 

    tmp = AfaDBFunc.SelectSql( sqlstr )
    AfaLoggerFunc.tradeInfo( tmp )
    if tmp == None :
        return ExitThisFlow( 'A0025', AfaDBFunc.sqlErrMsg )
    elif len( tmp ) == 0 :
        AfaLoggerFunc.tradeInfo( sqlstr )
        return ExitThisFlow( 'A0045', 'δ����ԭ����' )

    tmp=UtilTools.ListFilterNone( tmp )

    temp=tmp[0]
    if temp[0]!='0':                 #�жϷ����ױ�־
        return ExitThisFlow( 'A0020', '��ƥ����Ϣ�����ױ�־����' )
    if temp[5]!=TradeContext.teller: #�ȽϹ�Ա��
        return ExitThisFlow( 'A0020', '��Ա�Ų�ƥ��' )
    if UtilTools.lrtrim(temp[1])!=TradeContext.taxPayCode:
        return ExitThisFlow( 'A0020', '�û��Ų�ƥ��' )       
    if UtilTools.lrtrim(temp[4])!=TradeContext.amount:   #У����#
        AfaLoggerFunc.tradeInfo( temp[4] )
        return ExitThisFlow( 'A0020', '��ƥ��' )
    
    TradeContext.taxPayCode =temp[1]
    TradeContext.__agentAccno__  =temp[2]
    TradeContext.accno      =temp[3]
    TradeContext.taxPayName =temp[6]
    TradeContext.termId     =temp[7]
    TradeContext.vouhType   =temp[8]
    TradeContext.vouhNo     =temp[9]
    TradeContext.catrFlag   =temp[11]
    TradeContext.corpSerno  =temp[13]
    TradeContext.corpTime   =temp[14]
    TradeContext.taxVouNo   =temp[10]
    #TradeContext.note1=temp[16]
    #TradeContext.note2=temp[17]
    TradeContext.note3=temp[17]
    TradeContext.note4=temp[18]
    #TradeContext.note5=temp[20]
    #TradeContext.note6=temp[21]
    #TradeContext.note7=temp[22]
    #TradeContext.note8=temp[23]
    #TradeContext.note9=temp[24]
    #TradeContext.note10=temp[25]
    AfaLoggerFunc.tradeInfo( 'У�鷴��������������[end]' )
    return True

#==========================��ȡƽ̨��ˮ��==========================
def GetSerialno( seqName="TIPS_SEQUENCE" ):

    AfaLoggerFunc.tradeInfo( '��ȡƽ̨��ˮ��' )
    #if seqName=="TIPS_SEQUENCE" :
    #    if not TradeContext.existVariable( "revTranF" ) or TradeContext.revTranF!='2' :
    #        if (TradeContext.existVariable( "agentSerialno" ) and len(TradeContext.agentSerialno)>0):
    #            return 0
    sqlStr = "select nextval for " +seqName+ " from sysibm.sysdummy1"
    records = AfaDBFunc.SelectSql( sqlStr )
    if records == None :
        TradeContext.errorCode = 'A0025'
        TradeContext.errorMsg = AfaDBFunc.sqlErrMsg
        return -1
    if seqName=="TIPS_SEQUENCE" :
        TradeContext.agentSerialno=str( records[0][0] ).rjust( 8, '0' )
    AfaLoggerFunc.tradeInfo( '>>>ƽ̨��ˮ��:' +TradeContext.agentSerialno)
    return str( records[0][0] )


################################################################################
# ������:    ChkAbnormal
# ����:      ��
# ����ֵ��    0  ���쳣����    1  ���쳣����    -1  ��ѯ��ˮ�����쳣ʧ��
# ����˵����  ����Ա��ѯ��ˮ���е������쳣���� 
################################################################################
def ChkAbnormal( ):

    AfaLoggerFunc.tradeInfo( '��ѯ��ˮ���е������쳣����' )
    sql="SELECT COUNT(*) FROM TIPS_MAINTRANSDTL WHERE WORKDATE='"+ \
    TradeContext.workDate+"' AND AGENTCODE='"+TradeContext.agentCode+ \
    "' AND AGENTZONENO='"+TradeContext.zoneno+"' AND BRNO='"+TradeContext.brno+\
    "' AND TELLERNO='"+TradeContext.teller+"' AND REVTRANF='0'AND  \
    (BANKSTATUS='2' OR (BANKSTATUS='0' AND CORPSTATUS IN ('1', '2','3')))"
    result=AfaDBFunc.SelectSql( sql )
    if( result == None ):
        # AfaLoggerFunc.tradeFatal( sql )
        return -1
    if( result[0][0]!=0 ):
        return 1
    else:
        AfaLoggerFunc.tradeError( sql )
        return 0


################################################################################
# ������:    InsertDtl
# ����:      ��
# ����ֵ��    True  ������ˮ��ɹ�    False ������ˮ��ʧ��
# ����˵����  ����ˮ��Ϣ������ˮ��
################################################################################
def InsertDtl( ):

    AfaLoggerFunc.tradeInfo( '������ˮ��' )
    # count ��ˮ�������-1
    count=41
    TransDtl=[[]]*( count+1 )
    TransDtl[0] = TradeContext.agentSerialno    # SERIALNO ����ҵ����ˮ��
    TransDtl[1] = TradeContext.workDate         # WORKDATE   �������� yyyymmdd
    TransDtl[2] = TradeContext.workTime         # WORKTIME   ����ʱ��   
    TransDtl[3] = TradeContext.TransCode        # TRXCODE    ������
    TransDtl[4] = TradeContext.zoneno           # ZONENO   ����ҵ�������  
    TransDtl[5] = TradeContext.brno             # BRNO       �����  
    TransDtl[6] = TradeContext.teller           # TELLERNO   ��Ա�� 
    if( TradeContext.existVariable( "authTeller" ) ) :
        TransDtl[7] = TradeContext.authTeller  # AUTHTELLERNO  ��Ȩ��Ա��  
    else:
        TransDtl[7] = ''
    if( TradeContext.existVariable( "termId" ) ):
        TransDtl[8] = TradeContext.termId      # TERMID     �ն˺�
    else:
        TransDtl[8]=''
    
    TransDtl[9] = TradeContext.channelCode     # CHANNELCODE   ��������
    
    if( TradeContext.existVariable( "tradeType" ) ):
        TransDtl[10] = TradeContext.tradeType      # TRADETYPE ��������
    else:
        TransDtl[10]=''
    
    TransDtl[11] = TradeContext.catrFlag        #CATRFLAG ��ת��־
    
    if (TradeContext.existVariable( "accno" )):       #ACCNO �����ʺ�
        TransDtl[12] = TradeContext.accno
    else:
        TransDtl[12] = ''
    
    if (TradeContext.existVariable ("__agentAccno__")):     #SUBACCNO ���ʺ�
        TransDtl[13] = TradeContext.__agentAccno__
    else:
        TransDtl[13] = ''
    
    if( TradeContext.existVariable("vouhType") ): #VOUHTPYE ƾ֤����
        TransDtl[14] = TradeContext.vouhType
    else:
        TransDtl[14]=''
        
    if( TradeContext.existVariable("vouhNo")):   #VOUHNO ƾ֤����
        TransDtl[15] = TradeContext.vouhNo
    else:
        TransDtl[15] = ''    

    if( TradeContext.existVariable("taxVouNo")):   #˰Ʊ����
        TransDtl[16] = TradeContext.taxVouNo
    else:
        TransDtl[16] = ''    
    
    if ( TradeContext.existVariable( "taxPayCode" ) ):
        TransDtl[17] = TradeContext.taxPayCode      #��˰�˱���
    else:
        TransDtl[17] = ''
      
    
    if( TradeContext.existVariable( "taxPayName" ) ):
        TransDtl[18] = TradeContext.taxPayName    # TAXPAYNAME   ��˰������  
    else:
        TransDtl[18] = '' 
    
    TransDtl[19] = UtilTools.lrtrim(TradeContext.amount)         # AMOUNT       ���׽�� 
    
    TransDtl[20] = TradeContext.revTranF       # REVTRANF    �����ױ�־ 
                                               # 0:�����ס�1:�����ס�2.�Զ����� 
    if( int( TradeContext.revTranF ) != 0 ):
        TransDtl[21] = TradeContext.preAgentSerno  #PREAGENTSERNO    ԭƽ̨��ˮ��  
    else:
        TransDtl[21] = ''    
    
    TransDtl[22] = '2'                   # BANKSTATUS     ���н���״̬ 
    TransDtl[23] = ''                    # BANKCODE       ����.���׷�����
    TransDtl[24] = ''                    # BANKSERNO      ����.������ˮ��
    
    TransDtl[25] = '2'                   # CORPSTATUS     ����������״̬
    TransDtl[26] = ''                    # CORPCODE       ������.���׷�����  

    #�ر��  20091218  �޸� �Ǽ�����ˮ��ʱ�Ǽǵ��������ں���ˮ
    if ( TradeContext.existVariable( "corpSerno" )):
        TransDtl[27] = TradeContext.corpSerno    # CORPSERNO      ������.������ˮ��
    else:
        TransDtl[27] = ''               

    if ( TradeContext.existVariable( "corpTime" ) ):
        TransDtl[28] = TradeContext.corpTime     # CORPTIME       ������.��������ʱ���
    else:
        TransDtl[28] = ''           
    #�ر��  20091218  �޸Ľ���
    
    TransDtl[29] = ''                    # ERRORMSG       ���׷�����Ϣ
    TransDtl[30] = '9'                   # CHKFLAG        �������ʱ�־ 
    TransDtl[31] = '9'                   # CORPCHKFLAG    ���ж��ʱ�־ 
            
    if( TradeContext.existVariable( "note1" ) ):
        TransDtl[32] = TradeContext.note1
    else:
        TransDtl[32] = ''
        
    if( TradeContext.existVariable( "note2" ) ):
        TransDtl[33] = TradeContext.note2         # NOTE2          ��ע2
    else:
        TransDtl[33] = ''
        
    if( TradeContext.existVariable( "note3" ) ):
        TransDtl[34] = TradeContext.note3         # NOTE3          ��ע3
    else:
        TransDtl[34] = ''
        
    if( TradeContext.existVariable( "note4" ) ):
        TransDtl[35] = TradeContext.note4         # NOTE4          ��ע4
    else:
        TransDtl[35] = ''
        
    if( TradeContext.existVariable( "note5" ) ):
        TransDtl[36] = TradeContext.note5         # NOTE5          ��ע5
    else:
        TransDtl[36] = ''
        
    if( TradeContext.existVariable( "note6" ) ):
        TransDtl[37] = TradeContext.note6         # NOTE6          ��ע6
    else:
        TransDtl[37] = ''
        
    if( TradeContext.existVariable( "note7" ) ):
        TransDtl[38] = TradeContext.note7         # NOTE7          ��ע7
    else:
        TransDtl[38] = ''
        
    if( TradeContext.existVariable( "note8" ) ):
        TransDtl[39] = TradeContext.note8         # NOTE8          ��ע8
    else:
        TransDtl[39] = ''
        
    if( TradeContext.existVariable( "note9" ) ):
        TransDtl[40] = TradeContext.note9         # NOTE9          ��ע9
    else:
        TransDtl[40] = ''
        
    if( TradeContext.existVariable( "note10" ) ):
        TransDtl[41] = TradeContext.note10        # NOTE10          ��ע10
    else:
        TransDtl[41] = ''
    sql="INSERT INTO TIPS_MAINTRANSDTL(SERIALNO,WORKDATE, \
         WORKTIME,TRXCODE,ZONENO,BRNO,TELLERNO, \
         AUTHTELLERNO,TERMID,CHANNELCODE,TRADETYPE,CATRFLAG,DRACCNO,CRACCNO,VOUHTYPE,VOUHNO, \
         TAXVOUNO,TAXPAYCODE,TAXPAYNAME,AMOUNT,REVTRANF,PRESERNO, \
         BANKSTATUS,BANKCODE,BANKSERNO, \
         CORPSTATUS,CORPCODE,CORPSERNO,CORPTIME,ERRORMSG,CHKFLAG, CORPCHKFLAG, \
         NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9,NOTE10 \
         ) VALUES("
    i=0
    for i in range( 0, count ):
        if( type( TransDtl[i] ) is int ):
            sql=sql+str( TransDtl[i] )+","
        else:
            sql=sql+"'"+ TransDtl[i]+"',"
        
    sql=sql+"'"+TransDtl[count]+"')"
   
    result=AfaDBFunc.InsertSqlCmt( sql )
    
    if( result < 1 ):
        # AfaLoggerFunc.tradeFatal( sql )
        TradeContext.errorCode, TradeContext.errorMsg='A0044', '������ˮ����ʧ��'+AfaDBFunc.sqlErrMsg
        return False
    else:
        #TradeContext.errorCode, TradeContext.errorMsg='0000', 'TransOk'
        AfaLoggerFunc.tradeInfo( '������ˮ�����' )
        #������Ŀ��ϸ

        if TradeContext.revTranF =='0':
            if not InsertVouMX() :
                return False
            else:
                return True
        else:
            return True
################################################################################
# ������:    InsertVouMX 
# ����:      ��
# ����ֵ��    True  �����ɹ�    False �����ʧ��
# ����˵����  ��˰����ϸ����˰Ʊ��ϸ��
################################################################################
def InsertVouMX( ):

    AfaLoggerFunc.tradeInfo( '����˰Ʊ��ϸ��' )
    for index in range(0,int(TradeContext.taxTypeNum)):
        sql="INSERT INTO TIPS_VOU_TAXTYPE(SERIALNO,WORKDATE, \
             TAXVOUNO,PROJECTID,BUDGETSUBJECTCODE,LIMITDATE,TAXTYPENAME, \
             BUDGETLEVELCODE,BUDGETLEVELNAME,TAXSTARTDATE,TAXENDDATE,VICESIGN,TAXTYPE, \
             TAXTYPEAMT,DETAILNUM,TAXSUBJECTLIST,NOTE1 \
             ) VALUES("
        sql=sql+"'"+ TradeContext.agentSerialno +"',"
        sql=sql+"'"+ TradeContext.workDate      +"',"
        sql=sql+"'"+ TradeContext.taxVouNo                   +"',"
        if type(TradeContext.projectId) is list:
            sql=sql+"'"+ TradeContext.projectId[index]           +"'"               #��Ŀ���
        else:
            sql=sql+"'"+ TradeContext.projectId           +"'"               #��Ŀ���
            
        if( TradeContext.existVariable( "budgetSubjectCode" ) ):
            if type(TradeContext.budgetSubjectCode) is list:
                sql=sql+",'"+ TradeContext.budgetSubjectCode[index] +"'"        #Ԥ���Ŀ���� 
            else:
                sql=sql+",'"+ TradeContext.budgetSubjectCode +"'"        #Ԥ���Ŀ���� 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "limitDate" ) ):
            if type(TradeContext.limitDate) is list:
                sql=sql+",'"+ TradeContext.limitDate[index] +"'"        # �޽�����
            else:
                sql=sql+",'"+ TradeContext.limitDate +"'"        # �޽�����
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxTypeName" ) ):
            if type(TradeContext.taxTypeName) is list:
                sql=sql+",'"+ TradeContext.taxTypeName[index] +"'"        # ˰������
            else:
                sql=sql+",'"+ TradeContext.taxTypeName +"'"        # ˰������
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "budgetLevelCode" ) ):
            if type(TradeContext.budgetLevelCode) is list:
                sql=sql+",'"+ TradeContext.budgetLevelCode[index] +"'"        #Ԥ�㼶�δ��� 
            else:
                sql=sql+",'"+ TradeContext.budgetLevelCode +"'"        #Ԥ�㼶�δ��� 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "budgetLevelName" ) ):
            if type(TradeContext.budgetLevelName) is list:
                sql=sql+",'"+ TradeContext.budgetLevelName[index] +"'"        #Ԥ�㼶������ 
            else:
                sql=sql+",'"+ TradeContext.budgetLevelName +"'"        #Ԥ�㼶������ 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxStartDate" ) ):
            if type(TradeContext.taxStartDate) is list:
                sql=sql+",'"+ TradeContext.taxStartDate[index] +"'"        #˰������������ 
            else:
                sql=sql+",'"+ TradeContext.taxStartDate +"'"        #˰������������ 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxEndDate" ) ):
            if type(TradeContext.taxEndDate) is list:
                sql=sql+",'"+ TradeContext.taxEndDate[index] +"'"        #˰����������ֹ 
            else:
                sql=sql+",'"+ TradeContext.taxEndDate +"'"        #˰����������ֹ 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "viceSign" ) ):
            if type(TradeContext.viceSign) is list:
                sql=sql+",'"+ TradeContext.viceSign[index] +"'"        #������־ 
            else:
                sql=sql+",'"+ TradeContext.viceSign +"'"        #������־ 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxType" ) ):
            if type(TradeContext.taxType) is list:
                sql=sql+",'"+ TradeContext.taxType[index] +"'"        #˰������ 
            else:
                sql=sql+",'"+ TradeContext.taxType + "'"        #˰������ 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxTypeAmt" ) ):
            if type(TradeContext.taxTypeAmt) is list:
                sql=sql+",'"+ TradeContext.taxTypeAmt[index] +"'"        #˰�ֽ�� 
            else:
                sql=sql+",'"+ TradeContext.taxTypeAmt +"'"        #˰�ֽ�� 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "detailNum" ) ):
            if type(TradeContext.detailNum) is list:
                sql=sql+",'"+ TradeContext.detailNum[index] +"'"        #��ϸ���� 
            else:
                sql=sql+",'"+ TradeContext.detailNum +"'"        #��ϸ���� 
        else:
            sql=sql+",''"
        if( TradeContext.existVariable( "taxSubjectList" ) ):
            if type(TradeContext.taxSubjectList) is list:
                sql=sql+",'"+ TradeContext.taxSubjectList[index] +"'"        #˰Ŀ��ϸ 
            else:
                sql=sql+",'"+ TradeContext.taxSubjectList +"'"        #˰Ŀ��ϸ 
        else:
            sql=sql+",''"
        sql=sql+",'0')"
        
        AfaLoggerFunc.tradeInfo( sql )
        result=AfaDBFunc.InsertSqlCmt( sql )
        
        if( result < 1 ):
            # AfaLoggerFunc.tradeFatal( sql )
            TradeContext.errorCode, TradeContext.errorMsg='A0044', '����˰Ʊ��ϸ��ʧ��'+AfaDBFunc.sqlErrMsg
            return False
    AfaLoggerFunc.tradeInfo( '����˰Ʊ��ϸ�����' )
    return True

################################################################################        
# ������:    UpdatePreDtl
# ����:      action  ������ 'BANK','CORP','TRADE'
#                   'BANK'  �������е�ҵ��״̬
#                   'CORP'  ������ҵ��ҵ��״̬
#                   'TRADE' �����������׵�ҵ��״̬����Ҫ����ֻ�е���������ֻ�����������Ľ���
# ����ֵ��    True  ����ԭ������ˮ�ɹ�    False ����ԭ������ˮʧ��
# ����˵����  ����ԭ������ˮ��������ڲ������²�ͬ��״̬��ʶ��
################################################################################
def UpdatePreDtl( action ):

    AfaLoggerFunc.tradeInfo( '����ԭ������ˮ' )
    sql="UPDATE TIPS_MAINTRANSDTL SET "
    if( action == 'BANK' ):
        sql=sql+" BANKSTATUS='3' "
    elif( action == 'CORP' ):
        sql=sql+" CORPSTATUS='3' "
    elif( action == 'TRADE' ):
        sql=sql+" BANKSTATUS='3' ,CORPSTATUS='3'"
    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0041', '��ڲ�������������û���������͵Ĳ���'
        return False
    sql=sql+" WHERE SERIALNO='"+TradeContext.preAgentSerno+ \
    "' AND WORKDATE='"+TradeContext.workDate+"' AND REVTRANF='0'"  
    # print "UpdatePreDtl:"+sql 
    ret=AfaDBFunc.UpdateSql( sql )
    if( ret >0 ):
        return True
    AfaLoggerFunc.tradeFatal( sql )
    if( ret == 0 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0100', 'δ����ԭʼ����'
    else :
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '������ˮ����ԭ���׼�¼ʧ��'+AfaDBFunc.sqlErrMsg    
    return False

################################################################################
# ������:    UpdateDtl
# ����:      action  ������ 'BANK','CORP','TRADE'
#                   'BANK'  �������е�ҵ��״̬
#                   'CORP'  ������ҵ��ҵ��״̬
#                   'TRADE' �����������׵�ҵ��״̬����Ҫ����ֻ�е���������ֻ�����������Ľ���
# ����ֵ��    True  ���µ�ǰ������ˮ�ɹ�    False ���µ�ǰ������ˮʧ��
# ����˵����  ���µ�ǰ������ˮ��������ڲ������²�ͬ��״̬��ʶ��        
################################################################################
def UpdateDtl( action ):

    AfaLoggerFunc.tradeInfo( '���±�������ˮ[begin]['+ action + ']' )
    sql="UPDATE TIPS_MAINTRANSDTL SET "
    if( TradeContext.existVariable( "errorMsg" ) ):
        sql=sql+"ERRORMSG='"+TradeContext.errorMsg+"',"

    if( action == 'BANK' ):
        sql=sql+"BANKSTATUS='"+TradeContext.__status__+"',BANKCODE='"+ \
        TradeContext.errorCode+"'"
        if( TradeContext.existVariable( "bankSerno" ) ):
            sql=sql+",BANKSERNO='"+TradeContext.bankSerno+"'"
    elif( action == 'CORP' ):
        sql=sql+"CORPSTATUS='"+TradeContext.__status__+"',CORPCODE='"+ \
        TradeContext.errorCode+"'"
        if( TradeContext.existVariable( "corpSerno" ) ):
            sql=sql+",CORPSERNO='"+TradeContext.corpSerno+"'"
        if( TradeContext.existVariable( "corpTime" ) ):
            sql=sql+",CORPTIME='"+TradeContext.corpTime+"'"
    elif( action == 'TRADE' ):
        sql=sql+"CORPSTATUS='"+TradeContext.__status__+"',BANKSTATUS='"+ \
        TradeContext.__status__+"',CORPCODE='"+TradeContext.errorCode+ \
        "',BANKCODE='"+TradeContext.errorCode+"'"
        if( TradeContext.existVariable( "bankSerno" ) ):
            sql=sql+",BANKSERNO='"+TradeContext.bankSerno+"'"
        if( TradeContext.existVariable( "corpSerno" ) ):
            sql=sql+",CORPSERNO='"+TradeContext.corpSerno+"'"
        if( TradeContext.existVariable( "corpTime" ) ):
            sql=sql+",CORPTIME='"+TradeContext.corpTime+"'"
    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0041', '��ڲ�������������û���������͵Ĳ���'
        return False
    
    if( TradeContext.existVariable( "unitno" ) ):
        sql=sql+",NOTE1='"+  TradeContext.unitno+"'"      # NOTE1          ��ע1(��λ����)
    elif( TradeContext.existVariable( "note1" ) ):
        sql=sql+",NOTE1='"+  TradeContext.note1+"'"
    
    if( TradeContext.existVariable( "note2" ) ):
        sql=sql+",NOTE2='"+  TradeContext.note2+"'"       # NOTE2          ��ע2
        
    if( TradeContext.existVariable( "note3" ) ):
        sql=sql+",NOTE3='"+  TradeContext.note3+"'"
        
    if( TradeContext.existVariable( "note4" ) ):
        sql=sql+",NOTE4='"+  TradeContext.note4+"'"        # NOTE4          ��ע4
        
    if( TradeContext.existVariable( "note5" ) ):
        sql=sql+",NOTE5='"+  TradeContext.note5+"'"         # NOTE5          ��ע5
        
    if( TradeContext.existVariable( "note6" ) ):
        sql=sql+",NOTE6='"+  TradeContext.note6+"'"         # NOTE6          ��ע6
        
    if( TradeContext.existVariable( "note7" ) ):
        sql=sql+",NOTE7='"+  TradeContext.note7+"'"         # NOTE7          ��ע7
        
    if( TradeContext.existVariable( "note8" ) ):
        sql=sql+",NOTE8='"+  TradeContext.note8+"'"         # NOTE8          ��ע8
        
    if( TradeContext.existVariable( "note9" ) ):
        sql=sql+",NOTE9='"+  TradeContext.note9+"'"         # NOTE9          ��ע9
        
    if( TradeContext.existVariable( "note10" ) ):
        sql=sql+",NOTE10='"+  TradeContext.note10+"'"        # NOTE10          ��ע10
    
    sql=sql+" WHERE SERIALNO='"+TradeContext.agentSerialno+ \
    "' AND WORKDATE='"+TradeContext.workDate+ \
    "' AND REVTRANF='"+TradeContext.revTranF+"'"
   
    AfaLoggerFunc.tradeInfo( sql )
    if( int( TradeContext.revTranF )!=0 and TradeContext.errorCode == '0000'):
        if( not UpdatePreDtl( action ) ):
            return False
            
    if( AfaDBFunc.UpdateSqlCmt( sql )<1 ):
        # AfaLoggerFunc.tradeFatal( sql )
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '������ˮ����ʧ��'+AfaDBFunc.sqlErrMsg
        return False
        
    AfaLoggerFunc.tradeInfo( TradeContext.errorCode + "BBBBBB" ) 
    #if( TradeContext.errorCode != '0000' ):
    #    return  False
        
    AfaLoggerFunc.tradeInfo( '���±�������ˮ[end]['+ action + ']' )
    return True

#======================�Զ����============================
def autoPackData( ):

    AfaLoggerFunc.tradeInfo( '�Զ����' )
    if( not TradeContext.existVariable( "tradeResponse" ) or not TradeContext.tradeResponse ):
        TradeContext.tradeResponse=[]
        #=============ƽ̨�ڲ�����====================
        names = TradeContext.getNames( )
        for name in names:
            if ( not name.startswith( '__' ) and name != 'tradeResponse' ) :
                value = getattr( TradeContext, name )
                if( type( value ) is StringType ) :
                    TradeContext.tradeResponse.append( [name, value] )
                elif( type( value ) is ListType ) :
                    for elem in value:
                        if type(elem) is not str :
                            AfaLoggerFunc.tradeInfo( 'autoPackData  [value is not sting]')
                            continue
                        TradeContext.tradeResponse.append( [name, elem] )
        #=============���������ر���====================
        names = Party3Context.getNames( )
        for name in names:
            if ( name.startswith( 'dn_' ) ) :
                value = getattr( Party3Context, name )
                if( type( value ) is StringType ) :
                    TradeContext.tradeResponse.append( [name, value] )
                elif( type( value ) is ListType ) :
                    for elem in value:
                        TradeContext.tradeResponse.append( [name, elem] )
    return True

#=================��ʼ������ͨѶ�ӿ�=======================
def InitHostReq(hostType ):
    #��ʼ����������ֵ����
    AfaLoggerFunc.tradeInfo('��ʼ��map�ļ���Ϣ[InitHostReq]')

    if (hostType =='0'): # ������

        AfaLoggerFunc.tradeInfo('>>>������8813')

        HostContext.I1TRCD = '8813'
       
        HostContext.I1SBNO = TradeContext.brno
       
        HostContext.I1USID = TradeContext.teller
       
        if TradeContext.existVariable ( 'authTeller'):
            HostContext.I1AUUS = TradeContext.authTeller
            HostContext.I1AUPS = TradeContext.authPwd
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        HostContext.I1WSNO = TradeContext.termId

        HostContext.I2NBBH = []         #����ҵ���
        HostContext.I2NBBH.append(TradeContext.appNo)

        HostContext.I2FEDT = []         #ǰ������
        HostContext.I2FEDT.append(TradeContext.workDate)

        HostContext.I2RBSQ = []         #ǰ����ˮ��
        HostContext.I2RBSQ.append(TradeContext.agentSerialno)

        HostContext.I2DATE = []         #��ϵͳ��������
        HostContext.I2DATE.append(TradeContext.workDate)

        HostContext.I2RVFG = []         #�����ֱ�־
        HostContext.I2RVFG.append('')

        HostContext.I2SBNO = []         #���׻���
        HostContext.I2SBNO.append(TradeContext.brno)

        HostContext.I2TELR = []         #���׹�Ա
        HostContext.I2TELR.append(TradeContext.teller)

        HostContext.I2TRSQ = []         #���
        HostContext.I2TRSQ.append('000')
        
        HostContext.I2TINO = []         #�������
        HostContext.I2TINO.append('00')

        HostContext.I2OPTY = []         #֤��У���־
        HostContext.I2OPTY.append('0')

        HostContext.I2RBAC = []         #�����˺�
        HostContext.I2RBAC.append(TradeContext.__agentAccno__)

        HostContext.I2CYNO = []         #����
        HostContext.I2CYNO.append('01')

        HostContext.I2WLBZ = []         #�����ʱ�־
        HostContext.I2WLBZ.append('0')

        HostContext.I2TRAM = []         #������
        HostContext.I2TRAM.append(TradeContext.amount)

        HostContext.I2SMCD = []         #ժҪ����
        HostContext.I2SMCD.append(TradeContext.summary_code)

        HostContext.I2NMFG = []         #����У���־
        HostContext.I2NMFG.append('0')

        HostContext.I2APX1 = []         #������Ϣ1
        HostContext.I2APX1.append('')

        #�ж��ֽ�ת�ʱ�־,�Ա���䲻ͬ������ͨѶ��
        if (TradeContext.catrFlag == '0'):    #�ֽ�

            AfaLoggerFunc.tradeInfo('>>>�ֽ�')

            HostContext.I2CFFG = []           #����У���־
            HostContext.I2CFFG.append('N')

            #HostContext.I2TRFG = []           #ƾ֤�����־
            #HostContext.I2TRFG.append('')

            HostContext.I2CATR = []           #��ת��־
            HostContext.I2CATR.append(TradeContext.catrFlag)

        else:   #ת��
            AfaLoggerFunc.tradeInfo('>>>ת��')

            HostContext.I2SBAC = []
            HostContext.I2SBAC.append(TradeContext.accno)         #�跽�ʺ�

            if (TradeContext.existVariable('accPwd')):
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('Y')                    #����У�鷽ʽ
                HostContext.I2PSWD = []
                HostContext.I2PSWD.append(TradeContext.accPwd)

            else:
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('N')                    #����У�鷽ʽ

            if (TradeContext.existVariable('vouhType' ) ):
                HostContext.I2CETY = []
                HostContext.I2CETY.append(TradeContext.vouhType)

                HostContext.I2CCSQ = []
                HostContext.I2CCSQ.append(TradeContext.vouhNo)
                
                HostContext.I2CFFG = []
                HostContext.I2CFFG.append('N')                          #����У�鷽ʽ��֧Ʊ��У������

            HostContext.I2CATR = []                               #��ת��־
            HostContext.I2CATR.append(TradeContext.catrFlag)
                    
    else:   #������

        AfaLoggerFunc.tradeInfo('>>>������8820')

        HostContext.I1TRCD = '8820'
        
        HostContext.I1SBNO = TradeContext.brno
        
        HostContext.I1USID = TradeContext.teller
        
        if TradeContext.existVariable ( 'authTeller'):
            HostContext.I1AUUS = TradeContext.authTeller
            HostContext.I1AUPS = TradeContext.authPwd
        else:
            HostContext.I1AUUS = ''
            HostContext.I1AUPS = ''

        HostContext.I1WSNO = TradeContext.termId
        HostContext.I1NBBH = TradeContext.appNo
        HostContext.I1FEDT = TradeContext.workDate
        HostContext.I1DATE = TradeContext.workDate
        HostContext.I1RBSQ = TradeContext.agentSerialno
        HostContext.I1TRDT = TradeContext.workDate
        HostContext.I1UNSQ = TradeContext.preAgentSerno
        HostContext.I1OPTY = ''
        HostContext.I1OPFG = '0'                                        #(0.����,1.����)
        HostContext.I1RVSB = '0'                                        #(0���ز�-NO, 1	�ز�-YES)

    AfaLoggerFunc.tradeInfo('��ʼ��map�ļ���Ϣ[InitHostReq]���')

    return True


#====================���������ݽ���=============================
def CommHost( result = None ):

    # �����������ױ�־TradeContext.revTranF�жϾ���ѡ���ĸ�map�ļ��������ӿڷ�ʽ
    if not result:
        result=TradeContext.revTranF
        #===================��ʼ��=======================
        if not InitHostReq(result) :
            TradeContext.__status__='1'
            return False
            

    if (result == '0'):
        #���ʼ��ʽ���
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8813.map'
        TradeContext.HostCode = '8813'

    else:
        #����Ĩ��
        mapfile=os.environ['AFAP_HOME'] + '/conf/hostconf/AH8820.map'
        TradeContext.HostCode = '8820'

    AfaLoggerFunc.tradeInfo('ִ��������ͨѶ����[CommHost]')

    #print mapfile
    #�˴����״���Ҫ��10λ,�Ҳ��ո�
    HostComm.callHostTrade( mapfile, UtilTools.Rfill(TradeContext.HostCode,10,' ') ,'0002' )

    if HostContext.host_Error:
        AfaLoggerFunc.tradeFatal( 'host_Error:'+str( HostContext.host_ErrorType )+':'+HostContext.host_ErrorMsg )

        if HostContext.host_ErrorType != 5 :
            TradeContext.__status__='1'
            TradeContext.errorCode='A0101'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        else :
            TradeContext.__status__='2'
            TradeContext.errorCode='A0102'
            TradeContext.errorMsg=HostContext.host_ErrorMsg
        return False

    #================�����������ذ�====================
    return HostParseRet(result )


#================�����������ذ�====================
def HostParseRet( hostType ):

    if (HostContext.host_Error == True):    #����ͨѶ����
        TradeContext.__status__='2'
        TradeContext.errorCode, TradeContext.errorMsg = 'A9998', '����ͨѶ����'
        TradeContext.bankCode  = HostContext.host_ErrorType                       #ͨѶ�������
        return False

    if( HostContext.O1MGID == 'AAAAAAA' ): #�ɹ�
        TradeContext.__status__='0'
        TradeContext.errorCode, TradeContext.errorMsg = '0000', '�����ɹ�'
        TradeContext.bankSerno = HostContext.O1TLSQ                               #��Ա��ˮ��
        TradeContext.bankCode  = HostContext.O1MGID                               #�������ش���
        return True

    else:                                  #ʧ��
        TradeContext.__status__='1'
        #result = AfapFunc.RespCodeMsg(HostContext.O1MGID,'0000','100000')
        #if not result :
        #    TradeContext.errorCode, TradeContext.errorMsg = 'A9999', 'ϵͳ����[����δ֪����]['+HostContext.ERR+']'
        #else:
        TradeContext.errorCode, TradeContext.errorMsg = HostContext.O1MGID, HostContext.O1INFO
        return False


#============�޸�Ӧ������״̬==========
def UpdAppStatus(flag):
    AfaLoggerFunc.tradeInfo('�޸ĵ�λ����״̬' )
    sql="UPDATE TIPS_ADM SET STATUS='"+flag+"' "
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ���󣬵�λ��Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    return True
    
#============��ѯӦ������״̬==========
def SelAppStatus():
    AfaLoggerFunc.tradeInfo('��ѯ��λ����״̬' )
    sql="SELECT STATUS FROM TIPS_ADM"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.SelectSql( sql )
    if( records <1 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ���󣬵�λ��Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    else:
        TradeContext.flag = records[0][0]
        return True

#============�޸�Ӧ�ù�������==========
def UpdAppWorkDate(workDate):
    AfaLoggerFunc.tradeInfo('�޸ĵ�λ��������' )
    sql="UPDATE TIPS_ADM SET WORKDATE='"+workDate+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ���󣬵�λ��Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    return True

#====�ж�Ӧ��״̬==========    
def ChkAppStatus():
    AfaLoggerFunc.tradeInfo( '>>>�ж�Ӧ��״̬' )
    sql="SELECT STATUS,WORKDATE,NOTE1 "
    sql=sql+" FROM TIPS_ADM "
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', 'δ����Ӧ����Ϣ' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_ADM�����ô���' )
    else:
        if records[0][0]=='0':
            return ExitThisFlow( 'A0027', 'ҵ����ֹͣ' )
        if records[0][0]=='2':
            return ExitThisFlow( 'A0027', 'ҵ������ͣ' )
        TradeContext.workDate       = records[0][1]
    AfaLoggerFunc.tradeInfo( '>>>�ж�Ӧ��״̬���' )
    return True
#====��ȡ������Ϣ==========    
def ChkLiquidStatus():
    AfaLoggerFunc.tradeInfo( '>>>��ȡ������Ϣ' )
    sql="SELECT PAYEEBANKNO,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,BRNO,TELLERNO,STATUS,LIQUIDATEMODE,NOTE1 "
    sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE PAYEEBANKNO='"+ TradeContext.payeeBankNo+"'"
    sql=sql+"AND PAYBKCODE='"+ TradeContext.payBkCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', 'δ����������Ϣ' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_LIQUIDINFO�����ô���' )
    else:
        if records[0][6]=='0':
            return ExitThisFlow( 'A0027', 'ҵ����ֹͣ' )
        if records[0][6]=='2':
            return ExitThisFlow( 'A0027', 'ҵ������ͣ' )
        TradeContext.payeeBankNo    = records[0][0]
        TradeContext.payeeAcct      = records[0][1]
        TradeContext.payeeName      = records[0][2]
        TradeContext.payBkCode      = records[0][3]
        TradeContext.__mainBrno__   = records[0][4]
        TradeContext.__vmTellerno__ = records[0][5]
        TradeContext.__liquidMode__ = records[0][7]
        #TradeContext.__batchType__  = records[0][12]
        #TradeContext.__protocalFlag__ = records[0][13]
        #TradeContext.workDate       = records[0][11]
        if not( TradeContext.existVariable( "brno" ) and len(TradeContext.brno)>0):
            TradeContext.brno   =records[0][4]
            TradeContext.zoneno =records[0][4][0:4]
        if not( TradeContext.existVariable( "teller" ) and len(TradeContext.teller)>0):
            TradeContext.teller =records[0][5]
    AfaLoggerFunc.tradeInfo( '>>>��ȡ������Ϣ���' )
    return True
#====�жϻ���״̬==========    
def ChkBranchStatus():
    AfaLoggerFunc.tradeInfo( '>>>�жϻ���״̬' )
    sql="SELECT STATUS,PAYBKCODE,PAYEEBANKNO,ACCNO,NOTE1,NOTE2 "
    sql=sql+" FROM TIPS_BRANCH_ADM WHERE "
    sql=sql+" BRNO ='" + TradeContext.brno +"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '�û���δ��ͨ����ҵ��' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_BRANCH_ADM�����ô���' )
    else:
        if records[0][0]=='0':
            return ExitThisFlow( 'A0027', '�û�������ҵ����ֹͣ' )
        if records[0][0]=='2':
            return ExitThisFlow( 'A0027', '�û�������ҵ������ͣ' )
        if not( TradeContext.existVariable( "payeeBankNo" ) and len(TradeContext.payeeBankNo)>0):
            TradeContext.payeeBankNo       = records[0][2]
        if not( TradeContext.existVariable( "payBkCode" ) and len(TradeContext.payBkCode)>0):
            TradeContext.payBkCode       = records[0][1]
        TradeContext.__agentAccno__  = records[0][3]
        AfaLoggerFunc.tradeInfo('����״̬����,�����кţ�'+TradeContext.payBkCode +' �������ʺţ�'+TradeContext.__agentAccno__)
        AfaLoggerFunc.tradeInfo('�տ��кţ�'+TradeContext.payeeBankNo)
    return True
#====������ջ��ش���==========    
#TaxOrgCode	���ջ��ش���
#TaxOrgName	���ջ�������
def ChkTaxOrgCode():
    AfaLoggerFunc.tradeInfo( '>>>������ջ��ش���' )
    sql="SELECT TAXORGCODE,TAXORGNAME,ZONENO,BRNO,BANKNO,TELLERNO,ACCNO,ACCNAME,STATUS,WORKDATE "
    sql=sql+" FROM TIPS_APPINFO WHERE "
    sql=sql+" TAXORGCODE='"+ TradeContext.taxOrgCode+"'"
    if( TradeContext.existVariable( "brno" ) and len(TradeContext.brno)>0):
        sql=sql+" AND ZONENO='"+ TradeContext.brno[0:2]+"'"
    if( TradeContext.existVariable( "PayBkCode" ) and len(TradeContext.PayBkCode)>0):
        sql=sql+" AND BANKNO='"+ TradeContext.PayBkCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '��������δ���������ջ���ҵ��' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_APPINFO��ҵ�����ô���' )
    else:
        if records[0][8]=='0':
            return ExitThisFlow( 'A0027', '�����ջ���ҵ����ֹͣ' )
        TradeContext.taxOrgName =records[0][1]
        TradeContext.PayBkCode =records[0][4]
        TradeContext.__agentAccno__ =records[0][6]
        #TradeContext.workDate =records[0][9]
        if not( TradeContext.existVariable( "brno" ) and len(TradeContext.brno)>0):
            TradeContext.brno=records[0][3]
            TradeContext.zoneno=records[0][2]
        TradeContext.teller =records[0][5]
        
    return True
    
#======���ͻ��Ƿ�ǩԼ===============
def ChkCustSign():
    AfaLoggerFunc.tradeInfo( '>>>���ͻ��Ƿ�ǩԼ' )
    if( not TradeContext.existVariable( "accno" ) ):
        return ExitThisFlow( 'A0001', '[accno]ֵ������!' )
    if( not TradeContext.existVariable( "protocolNo" ) ):
        return ExitThisFlow( 'A0001', 'Э�����[protocolNo]ֵ������!' )
    
    sql="SELECT TAXPAYCODE,PAYOPBKCODE"
    sql=sql+" FROM TIPS_CUSTINFO WHERE "
    sql=sql+" PAYACCT='"        +TradeContext.accno         +"'"
    sql=sql+" and PROTOCOLNO='" +TradeContext.protocolNo         +"'"
    sql=sql+" and TAXORGCODE='" +TradeContext.taxOrgCode    +"'"
    sql=sql+" AND STATUS='"     +'1'                        +"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( '24009', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( '24009', '�ÿͻ���δǩԼ' )
    else:
        TradeContext.userno     =records[0][0]
        TradeContext.taxPayCode =records[0][0]
        TradeContext.brno       =records[0][1]
        AfaLoggerFunc.tradeInfo('�ÿͻ���ǩԼ,��ţ�'+TradeContext.taxPayCode +' ����������'+TradeContext.brno)
    return True

#====���ڵ�״̬========== 
#���ڵ�״̬Ϊ����ʱ��ֹͣ���䷢����   
def ChkNode(nodeCode):
    AfaLoggerFunc.tradeInfo( '>>>���ڵ�״̬' )
    sql="SELECT STATUS,RUNSTATUS "
    sql=sql+" FROM TIPS_NODECODE WHERE "
    sql=sql+" NODECODE='"+ nodeCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '�����ڸýڵ�:'+'�ڵ����['+nodeCode+']' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_NodeCode����󣺶���ڵ���Ϣ' )
    else:
        if records[0][0]=='1':
            return ExitThisFlow( 'A0027', '�ڵ���ע��:'+'�ڵ����['+nodeCode+']'  )
        if records[0][1]=='1':
            return ExitThisFlow( 'A0027', '�ڵ���ϣ���ͣ����ҵ��:'+'�ڵ����['+nodeCode+']'  )
    return True    
#====������ջ���==========    
#TaxOrgCode	���ջ��ش���
#TaxOrgName	���ջ�������
def ChkTaxOrg(taxOrgCode):
    AfaLoggerFunc.tradeInfo( '>>>������ջ���' )
    sql="SELECT TAXORGNAME,STATUS "
    sql=sql+" FROM TIPS_TAXCODE WHERE "
    sql=sql+" TAXORGCODE='"+ taxOrgCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', 'û�и����ջ�����Ϣ:'+'����['+taxOrgCode+']')
    #elif( len( records )>1 ):
    #    return ExitThisFlow( 'A0027', 'TIPS_APPINFO��ҵ�����ô���' )
    else:
        if records[0][1]=='1':
            return ExitThisFlow( 'A0027', '�����ջ�����ע��:'+'����['+taxOrgCode+']' )
        TradeContext.taxOrgName =records[0][0]
    return True    
#====������==========    
def ChkTre(treCode,payBankno):
    AfaLoggerFunc.tradeInfo( '>>>��������Ϣ' )
    sql="SELECT STATUS,TRENAME,PAYBANKNO,OFNODECODE "
    sql=sql+" FROM TIPS_TRECODE WHERE 1=1 "
    if len(treCode)>0:
        sql=sql+"AND  TRECODE='"+ treCode+"'"
    if len(payBankno)>0:
        sql=sql+"AND PAYBANKNO='"+ payBankno+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', 'û�иù�����Ϣ:'+'�������['+treCode+']�к�['+payBankno+']' )
    #elif( len( records )>1 ):
    #    return ExitThisFlow( 'A0027', 'TIPS_APPINFO��ҵ�����ô���' )
    else:
        if records[0][0]=='1':
            return ExitThisFlow( 'A0027', '�ù�����ע��:'+'�������['+treCode+']�к�['+payBankno+']' )
        TradeContext.treName =records[0][1]
        TradeContext.treNodeCode =records[0][3]
    return True    
#======���ݸ����кŻ�ȡ������===============
def GetBrno(pPayBkCode):
    AfaLoggerFunc.tradeInfo( '>>>���ݸ����кŻ�ȡ������' )
    sql="SELECT BRANCHNO "
    sql=sql+" FROM AFA_BRANCH WHERE BRANCHCODE='"+ pPayBkCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', 'δ����ø����к�' )
    else:
        #AfaLoggerFunc.tradeInfo('')
        TradeContext.brno=records[0][0]
        #TradeContext.zoneno=TradeContext.brno[0:3]
        #TradeContext.subUnitno=TradeContext.zoneno
        AfaLoggerFunc.tradeInfo('������:'+TradeContext.brno)
    return True
   
################################################################################
# ������:    GetBranchInfo
# ����:      branchno
# ����ֵ��    False  ʧ��;    �ɹ�����list
# ����˵����  ��ȡ������Ϣ
################################################################################
def GetBranchInfo(branchno=''):
    sqlStr="select upbranchno,branchcode,type,branchnames,branchname,note1,note2 from AFA_BRANCH where branchno='" + branchno + "'"
    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return ExitThisFlow( 'A0002', '��ѯ������ʧ��:'+AfaDBFunc.sqlErrMsg )
    elif ( len( records )==0):
        return ExitThisFlow( 'A0002', '�޷��ҵ���Ӧ�Ļ�����' )
    elif ( len( records )>1):
        return ExitThisFlow( 'A0002', '�鵽����������' )
    else:
        UtilTools.ListFilterNone( records )
        TradeContext.__mngZoneno__=records[0][0]    #�ϼ��������
        TradeContext.__PayBkCode__=records[0][1]    #֧��ϵͳ�к�
        TradeContext.__branchType__=records[0][2]   #��������
        TradeContext.__branchNames__=records[0][3]
        TradeContext.__branchName__=records[0][4]
        TradeContext.__mngHsno__=records[0][5]    #�ϼ��������
        TradeContext.__QsBkCode__=records[0][6]     #�����к�
        AfaLoggerFunc.tradeInfo('�ϼ����������:['+TradeContext.__mngZoneno__+']')
    return ExitThisFlow( '0000', 'TransOk' )

def GetPayBkCode():
#=============��ѯ�����Ӧ��֧���кţ������к�====================
    sql="SELECT NOTE1,NOTE2,UPBRANCHNO,BRANCHCODE FROM AFA_BRANCH WHERE BRANCHNO='"+TradeContext.brno+"'"
    records = AfaDBFunc.SelectSql(sql)
    AfaLoggerFunc.tradeInfo(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', 'δ����û�����Ϣ')
    else:
        UtilTools.ListFilterNone( records )
        TradeContext.HSBrno     =records[0][0]  #�ϼ��������
        TradeContext.QsBkCode   =records[0][1]  #�����к�
        TradeContext.PayBkCode  =records[0][3]  #֧��ϵͳ�к�
        TradeContext.upBranchno =records[0][2]  #�ϼ����������
        
    #=============��ѯ�����кŶ�Ӧ�Ļ�����====================
    sql="SELECT BRANCHNO,BRANCHNAMES,BRANCHNAME FROM AFA_BRANCH WHERE BRANCHCODE='"+TradeContext.QsBkCode+"'"
    records = AfaDBFunc.SelectSql(sql)
    AfaLoggerFunc.tradeInfo(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', 'δ����û�����Ϣ')
    else:
        UtilTools.ListFilterNone( records )
        TradeContext.QsBrno     =records[0][0]  #���������
        TradeContext.QsBrNames  =records[0][1]  #
        TradeContext.QsBrName   =records[0][2]  #
        #TradeContext.GkBkCode   =records[0][3]  #����֧���к�    
    return True
################################################################################
# ������:    RespCodeMsg
# ����:      outcode:�ⲿ��Ӧ��,unitno:
# ����ֵ��    0  ʧ��    1  �ɹ�
# ����˵����  �����ⲿ��Ӧ���ȡ�ⲿ��Ӧ��Ϣ
################################################################################
def GetRespMsg( outcode,sysid ):
    AfaLoggerFunc.tradeInfo( 'ת���ⲿ��Ӧ��' )
    AfaLoggerFunc.tradeInfo( 'ת��ǰ,�ⲿ������:['+outcode+']['+TradeContext.errorMsg+']' )
    TradeContext.respmsg=''
    sqlStr="select * from AFA_RESPCODE where sysid='"+sysid+\
        "' and orespcode='"+outcode+"'"
    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return ExitThisFlow( 'A0002', '��Ӧ����Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )!=0 ):
        UtilTools.ListFilterNone( records )
        #TradeContext.tradeResponse=(['errorCode',records[0][1]],['errorMsg',records[0][3]])
        TradeContext.irespcode=records[0][1]
        TradeContext.respmsg=records[0][3]
        AfaLoggerFunc.tradeInfo( '������:['+outcode+']['+TradeContext.irespcode+']['+TradeContext.respmsg+']' )
    else:
        AfaLoggerFunc.tradeInfo( 'δ�ҵ���Ӧ����Ϣ��������:['+TradeContext.errorCode+'][δ֪����]' )
        return False
        #TradeContext.irespcode=outcode
        #if(len(TradeContext.respmsg)==0):
        #    TradeContext.respmsg = 'δ֪����'
    return True
#======�������ջ��ش���������ջ�����Ϣ===============
def GetTaxOrg(pTaxOrgCode):
    AfaLoggerFunc.tradeInfo( '�������ջ��ش���������ջ�����Ϣ' )
    sql="SELECT TAXORGNAME "
    sql=sql+" FROM TIPS_TAXCODE WHERE TAXORGCODE='"+ pTaxOrgCode+"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        TradeContext.taxOrgName=pTaxOrgCode
        #return ExitThisFlow( 'A0027', 'δ����ø����к�' )
    else:
        TradeContext.taxOrgName=records[0][0]
    return True


#��������ί�к�
def CrtBatchNo():
    AfaLoggerFunc.tradeInfo('>>>����ί�к�')
    try:
        sqlStr = "SELECT NEXTVAL FOR DSDF_BATCH_SEQ FROM SYSIBM.SYSDUMMY1"
        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            return ExitThisFlow('9000', '����ί�к�ʧ��')
        TradeContext.BATCHNO = TradeContext.workDate + str(records[0][0]).rjust(8, '0')
        AfaLoggerFunc.tradeInfo('ί�к�'+TradeContext.BATCHNO)
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return ExitThisFlow('9000', '����ί�к�ʧ��')
    return True


#=========================��ʽ���ļ�=========================
def FormatFile(ProcType, sFileName, dFileName ,fFileFld):

    try:
        srcFileName    = sFileName
        dstFileName    = dFileName
        
        if (ProcType == "1"):
            #ascii->ebcd    ����
            #���ø�ʽ:cvt2ebcdic -T Դ�ı��ļ� -P Ŀ�������ļ� -F fld��ʽ�ļ� [-D ����� ]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ebcdic'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/' + fFileFld
            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName + " -D '<fld>'"
        else:
            #   ����
            #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D �����] [-S] [-R]
            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
            fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/' + fFileFld
            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName + " -D '<fld>'"

        AfaLoggerFunc.tradeInfo('>>>' + cmdstr)

        ret = os.system(cmdstr)
        if ( ret != 0 ):
            return False
        else:

            #�ж��ļ��Ƿ����
            if ( os.path.exists(dstFileName) and os.path.isfile(dstFileName) ):
                return True
            else:
                WrtLog('>>>��ʽ���ļ�ʧ��')
                return False

    except Exception, e:
        WrtLog(e)
        WrtLog('��ʽ���ļ��쳣')
        return False

##################################################################
#   ��˰����ϵͳ.FTP����ģ��
#=================================================================
#   ��    ��:   getHost(),putHost
#   ��    ��:   ���ǽ�
#   �޸�ʱ��:   2008-06-11
##################################################################

def getHost(file_path,host_home):
    #try:
    #    local_home = os.environ['AFAP_HOME'] + "/data/batch/tips/"
    #    
    #    config = ConfigParser.ConfigParser( )
    #    configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
    #    config.readfp( open( configFileName ) )
    #    
    #    ftp_p=ftplib.FTP(config.get('HOST_DZ','HOSTIP'),config.get('HOST_DZ','USERNO'),config.get('HOST_DZ','PASSWD' ))
    #    ftp_p.cwd(host_home)
    #    file_handler = open(local_home + file_path,'wb')
    #    ftp_p.retrbinary("RETR " + file_path,file_handler.write)
    #    file_handler.close()
    #    ftp_p.quit()
    #    
    #    if not os.path.exists(local_home + file_path):
    #        raise Exception,"�ļ�[" + local_home + file_path + "]����ʧ��"
    #    
    #    return True
    #    
    #except Exception, e:
    #    AfaLoggerFunc.tradeInfo(e)
    #    return False
        
    try:
        local_home = os.environ['AFAP_HOME'] + "/data/batch/tips/"
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open( configFileName ) )
        
        #�����ļ�
        ftpShell = os.environ['AFAP_HOME'] + '/tmp/ftphost_tips.sh'
        ftpFp = open(ftpShell, "w")

        ftpFp.write('open ' + config.get('HOST_DZ','HOSTIP') + '\n')
        ftpFp.write('user ' + config.get('HOST_DZ','USERNO') + ' ' + config.get('HOST_DZ','PASSWD' ) + '\n')

        #�����ļ�
        ftpFp.write('cd '  + host_home + '\n')
        ftpFp.write('lcd ' + local_home + '\n')
        #ftpFp.write('bin ' + '\n')
        #ftpFp.write('quote to 1383 ' + '\n')
        ftpFp.write('get ' + file_path + '\n')

        ftpFp.close()

        ftpcmd = 'ftp -n < ' + ftpShell + ' 1>/dev/null 2>/dev/null '

        ret = os.system(ftpcmd)
        if ( ret != 0 ):
            return False
        else:

            #�ж��ļ��Ƿ����
            sFileName = local_home + "/" + file_path
            if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
                return True
            else:
                WrtLog('>>>FTP���������ļ�ʧ��')
                return False

    except Exception, e:
        WrtLog(e)
        WrtLog('>>>FTP�����쳣')
        return False

    
def putHost(file_name,host_home,file_path = '/data/batch/tips/'):
    try:
        
        local_home = os.environ['AFAP_HOME'] + file_path
        
        config = ConfigParser.ConfigParser( )
        configFileName = os.environ['AFAP_HOME'] + '/conf/lapp.conf'
        config.readfp( open( configFileName ) )
        
        if not os.path.exists(local_home + file_name):
            raise Exception,"�ϴ��ļ�[" + local_home + file_name + "]������"
            
        ftp_p=ftplib.FTP(config.get('HOST_DZ','HOSTIP'),config.get('HOST_DZ','USERNO'),config.get('HOST_DZ','PASSWD' ))
        AfaLoggerFunc.tradeInfo('HOSTIP = '+config.get('HOST_DZ','HOSTIP') + 'USERNO = '+config.get('HOST_DZ','USERNO')+ 'PASSWD= '+config.get('HOST_DZ','PASSWD' ))
        ftp_p.cwd(host_home)
        file_handler = open(local_home + file_name,'rb')
        ftp_p.storbinary("STOR " + file_name,file_handler)
        file_handler.close()
        ftp_p.quit()
        
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return False
        
##################################################################
#   ��˰����ϵͳ.ȡTIPS����
#=================================================================
#   ��    ��:   GetTipsDate()
#   ��    ��:   ������
#   �޸�ʱ��:   2008-09-09
##################################################################
def GetTipsDate( ):
    sql = "select workdate from tips_adm"
    ret = AfaDBFunc.SelectSql(sql)
    if ret == None:
        return AfaFlowControl.ExitThisFlow('S999','���ݿ����ʧ��')
    if len(ret) <= 0:
        return time.strftime( '%Y%m%d', time.localtime( ) )
    else:
        date = ret[0][0]
    return date 
    
    
#=========================��־==================================================
def WrtLog(logstr):

    #Ĭ�����ļ�����Ļͬʱ���
    AfaLoggerFunc.tradeInfo(logstr)
    print logstr

    return True    
    
#==============��������״̬======================================================
def UpdateBatchAdm(status,errorCode,errMsg):
    
    AfaLoggerFunc.tradeInfo('��������״̬['+status+']'+errorCode+errMsg)
    sqlStr = "UPDATE TIPS_BATCHADM SET dealStatus='"+status+"',errorcode='"+errorCode+"',ERRORMSG='"+errMsg+"'"
    if( TradeContext.existVariable( "succNum" ) ):
        sqlStr =sqlStr +",SUCCNUM        = '" + TradeContext.succNum+ "'"
    if( TradeContext.existVariable( "succAmt" ) ):
        #TradeContext.succAmt=TradeContext.succAmt.rjust( 3, '0' )
        #TradeContext.succAmt=UtilTools.InsDot( TradeContext.succAmt.rjust( 3, '0' ), 2 )
        #TradeContext.succAmt=str(long(TradeContext.succAmt)/100.00)
        sqlStr =sqlStr +",SUCCAMT        = '" + TradeContext.succAmt+ "'"
    if( TradeContext.existVariable( "sFileName" ) ):
        sqlStr =sqlStr +",NOTE2 = '" + TradeContext.sFileName+ "'"
    sqlStr =sqlStr +" WHERE  "
    sqlStr =sqlStr +"WORKDATE  = '" + TradeContext.entrustDate     + "'"
    sqlStr =sqlStr +"and BATCHNO   = '" + TradeContext.packNo          + "'"
    sqlStr =sqlStr +"and TAXORGCODE     = '" + TradeContext.taxOrgCode      + "'"
    AfaLoggerFunc.tradeInfo(sqlStr )
    records=AfaDBFunc.UpdateSqlCmt( sqlStr )
    if( records <0 ):
        return AfaFlowControl.ExitThisFlow( 'A0027', '���ݿ����' )
    return True
    
#==============����������ϸ״̬======================================================
def UpdateBatchData(status,errorCode,errMsg):
    
    AfaLoggerFunc.tradeInfo('����������ϸ״̬['+status+']'+errorCode+errMsg)
    sqlStr = "UPDATE TIPS_BATCHDATA SET STATUS='"+status+"',errorcode='"+errorCode+"',ERRORMSG='"+errMsg+"'"

    sqlStr =sqlStr +" WHERE  "
    sqlStr =sqlStr +"WORKDATE  = '" + TradeContext.entrustDate     + "'"
    sqlStr =sqlStr +"and BATCHNO   = '" + TradeContext.packNo          + "'"
    sqlStr =sqlStr +"and TAXORGCODE     = '" + TradeContext.taxOrgCode      + "'"
    sqlStr =sqlStr +"and SERIALNO       = '" + TradeContext.SerialNo      + "'"
    AfaLoggerFunc.tradeInfo(sqlStr )
    records=AfaDBFunc.UpdateSqlCmt( sqlStr )
    if( records <0 ):
        return AfaFlowControl.ExitThisFlow( 'A0027', '���ݿ����' )
    return True
    
#=============��ѯ�����кŶ�Ӧ�Ļ�����====================
def GetBrno():
    sql="SELECT BRNO FROM TIPS_BRANCH_ADM WHERE STATUS = '1' AND PAYEEBANKNO='"+TradeContext.payeeBankNo+"'"
    records = AfaDBFunc.SelectSql(sql)
    AfaLoggerFunc.tradeInfo(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', 'δ����û�����Ϣ')
    else:
        UtilTools.ListFilterNone( records )
        TradeContext.sBrno =records[0][0]  #�տ������
    
    return True
    
################################################################################
# ������:    SelectAcc
# ����:      ��
# ����ֵ��    True  �ɹ�    False ʧ��
# ����˵����  ���������кŲ�ѯ�տ��ʺ�
################################################################################
def SelectAcc():
    AfaLoggerFunc.tradeInfo( '>>>���������кŲ�ѯ�տ���Ϣ' )
    sql="SELECT STATUS,PAYBKCODE,PAYEEBANKNO,ACCNO,BANKNAME,BRNO "
    sql=sql+" FROM TIPS_BRANCH_ADM WHERE "
    sql=sql+" PAYBKCODE ='" + TradeContext.payBkCode +"'"
    AfaLoggerFunc.tradeInfo(sql)
    records = AfaDBFunc.SelectSql(sql)
    if( records == None ):
        AfaLoggerFunc.tradeFatal(sql)
        return ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )==0 ):
        return ExitThisFlow( 'A0027', '�û���δ��ͨ����ҵ��' )
    elif( len( records )>1 ):
        return ExitThisFlow( 'A0027', 'TIPS_BRANCH_ADM�����ô���' )
    else:
        if records[0][0]=='0':
            return ExitThisFlow( 'A0027', '�û�������ҵ����ֹͣ' )
        if records[0][0]=='2':
            return ExitThisFlow( 'A0027', '�û�������ҵ������ͣ' )

        if not( TradeContext.existVariable( "payBkCode" ) and len(TradeContext.payBkCode)>0):
            TradeContext.payBkCode       = records[0][1]
        TradeContext.__agentAccno__  = records[0][3]
        TradeContext.__agentAccname__   = records[0][4]
        TradeContext.qsBrno = records[0][5]            #�������
        AfaLoggerFunc.tradeInfo('����״̬����,�����кţ�'+TradeContext.payBkCode +' �������ʺţ�'+TradeContext.__agentAccno__)
        AfaLoggerFunc.tradeInfo('�������ʻ�����' + TradeContext.__agentAccname__) 
    return True
    
################################################################################
# ������:    SelCodeMsg
# ����:      outcode:����������
# ����ֵ��    �����룬������Ϣ
# ����˵����  ���������������ȡ�����뼰������Ϣ
################################################################################
def SelCodeMsg( outcode):
    AfaLoggerFunc.tradeInfo( 'ת������������' )
    AfaLoggerFunc.tradeInfo( 'ת��ǰ,����������:['+outcode+']' )
    respcode = ''
    respmsg  = ''
    sqlStr="select RESULTINF,ADDWORD from TIPS_ERRORCODE where ERRORCODE ='" + outcode + "'"
    records=AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        return ExitThisFlow( 'A0002', '���������������쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )!=0 ):
        UtilTools.ListFilterNone( records )
        respcode=records[0][0].rstrip()
        respmsg=records[0][1].rstrip()
    else:
       respcode = '99090'
       respmsg  = '��������'
    AfaLoggerFunc.tradeInfo( '������:['+outcode+']['+respcode+']['+respmsg+']' )

    return respcode,respmsg


#def getDzFile(file_path,host_home):
#    try:
#        #host_home = "BANKMDS"
#        local_home = os.environ['AFAP_HOME'] + "/data/dz/host/"
#        
#        config = ConfigParser.ConfigParser( )
#        configFileName = os.environ['AFAP_HOME'] + '/conf/ftpconnect.conf'
#        config.readfp( open( configFileName ) )
#        
#        ftp_p = ftplib.FTP(config.get('host','ip'),config.get('host','username'),config.get('host','password' ))
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
##��ʽ���ļ�
#def FormatFile(ProcType, FLDName, sFileName, dFileName):
#
##    WrtLog('>>>��ʽ���ļ�:' + ProcType + ' ' + sFileName + ' ' + dFileName)
#
#    try:
#
#        srcFileName    = os.environ['AFAP_HOME'] + '/data/dz/host/' + sFileName
#        dstFileName    = os.environ['AFAP_HOME'] + '/data/dz/host/' + dFileName
#
#        if (ProcType == "1"):
#            #ascii->ebcd
#            #���ø�ʽ:cvt2ebcdic -T Դ�ı��ļ� -P Ŀ�������ļ� -F fld��ʽ�ļ� [-D ����� ]
#            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ebcdic'
#            #�ر��  20081126  ����������fld�ļ�
#            #fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/rccps01.fld'
#            fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/' + FLDName
#            cmdstr=CvtProg + " -T " + srcFileName + " -P " + dstFileName + " -F " + fldFileName + " -D '|' "
#
#        else:
#            #ebcd->ascii
#            #���ø�ʽ:cvt2ascii -T �����ı��ļ� -P �����ļ� -F fld�ļ� [-D ���-��] [-S] [-R]
#            CvtProg     = os.environ['AFAP_HOME'] + '/data/cvt/cvt2ascii'
#            #�ر��  20081126  ����������fld�ļ�
#            #fldFileName    = os.environ['AFAP_HOME'] + '/data/rccps/cvt/rccps02.fld'
#            fldFileName    = os.environ['AFAP_HOME'] + '/data/cvt/' + FLDName
#            cmdstr=CvtProg + " -T " + dstFileName + " -P " + srcFileName + " -F " + fldFileName + " -D '|' "
#
#        #WrtLog('>>>' + cmdstr)
#        #ret = -1
#        WrtLog('>>>�����ʽת������ʼ============')   #2007824
#        WrtLog(cmdstr)
#        ret = os.system(cmdstr)                         #2007824
#        if ( ret != 0 ):                                #2007824
#            ret = False                                 #2007824
#        else:                                           #2007824
#            ret = True                                  #2007824
#        #return 0                                       #2007824
#        WrtLog('>>>�����ʽת���������============')   #2007824
#
#        return ret
#        
#    except Exception, e:
#        WrtLog(e)
#        WrtLog('��ʽ���ļ��쳣')
#        return False
