# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.������ˮ�������
#=================================================================
#   �����ļ�:   TransDtlFunc.py
#   �޸�ʱ��:   2006-03-31
##################################################################
import TradeContext, AfaLoggerFunc, AfaDBFunc, AfaUtilTools
from types import *

################################################################################
# ������:    InsertDtl
# ����:      ��
# ����ֵ��    True  ������ˮ��ɹ�    False ������ˮ��ʧ��
# ����˵����  ����ˮ��Ϣ������ˮ��
################################################################################
def InsertDtl( ):

    AfaLoggerFunc.tradeInfo( '������ˮ��' )

    # count ��ˮ�������-1
    count=47
    TransDtl=[[]]*( count+1 )
    TransDtl[0] = TradeContext.agentSerialno    # SERIALNO ����ҵ����ˮ��
    TransDtl[1] = TradeContext.workDate         # WORKDATE   �������� yyyymmdd
    TransDtl[2] = TradeContext.workDate[4:6]    # MONTH      �����·�
    TransDtl[3] = TradeContext.workTime         # WORKTIME   ����ʱ��
    TransDtl[4] = TradeContext.appNo            # APPNO  ����ҵ�����
    TransDtl[5] = TradeContext.busiNo           # BUSINO  ����ҵ��ʽ
    TransDtl[6] = TradeContext.TransCode        # TRXCODE    ������
    TransDtl[7] = TradeContext.zoneno           # ZONENO   ����ҵ�������
    TransDtl[8] = TradeContext.brno             # BRNO       �����
    TransDtl[9] = TradeContext.teller           # TELLERNO   ��Ա��
    if( TradeContext.existVariable( "authTeller" ) ) :
        TransDtl[10] = TradeContext.authTeller  # AUTHTELLERNO  ��Ȩ��Ա��
    else:
        TransDtl[10] = ''

    TransDtl[11] = TradeContext.channelCode     # CHANNELCODE   ��������

    if( TradeContext.existVariable( "termId" ) ):
        TransDtl[12] = TradeContext.termId      # TERMID     �ն˺�
    else:
        TransDtl[12]=''

    TransDtl[13] = TradeContext.catrFlag        #CATRFLAG ��ת��־

    if( TradeContext.existVariable("vouhType") ): #VOUHTPYE ƾ֤����
        TransDtl[14] = TradeContext.vouhType
    else:
        TransDtl[14]=''

    if( TradeContext.existVariable("vouhNo")):   #VOUHNO ƾ֤����
        TransDtl[15] = TradeContext.vouhNo
    else:
        TransDtl[15] = ''

    if (TradeContext.existVariable( "accno" )):       #ACCNO �����ʺ�
        TransDtl[16] = TradeContext.accno
    else:
        TransDtl[16] = ''

    if (TradeContext.existVariable ("subAccno")):     #SUBACCNO ���ʺ�
        TransDtl[17] = TradeContext.subAccno
    else:
        TransDtl[17] = ''

    TransDtl[18] = AfaUtilTools.lrtrim(TradeContext.userNo)          # userNo     �û���

    if( TradeContext.existVariable( "subuserNo" ) ):
        TransDtl[19] = TradeContext.subuserNo   # SUBuserNo  �����û���
    else:
        TransDtl[19] = ''

    if( TradeContext.existVariable( "userName" ) ):
        TransDtl[20] = TradeContext.userName    # USERNAME   �û�����
    else:
        TransDtl[20] = ''

    if( TradeContext.existVariable( "contractno" ) ):
        TransDtl[21] = TradeContext.contractno  # CONTRACTNO  ��ͬ��
    else:
        TransDtl[21] = ''

    TransDtl[22] = AfaUtilTools.lrtrim(TradeContext.amount)         # AMOUNT       ���׽��

    if( TradeContext.existVariable( "subAmount" ) ):
        TransDtl[23] = TradeContext.subAmount  # SUBAMOUNT    ���ӽ��
    else:
        TransDtl[23] = ''

    TransDtl[24] = TradeContext.revTranF       # REVTRANF    �����ױ�־
                                               # 0:�����ס�1:�����ס�2.�Զ�����

    if( int( TradeContext.revTranF ) != 0 ):
        TransDtl[25] = TradeContext.revTrxDate  #REVTRXDATE    ԭ��������
    else:
        TransDtl[25] = ''

    if( int( TradeContext.revTranF ) != 0 ):
        TransDtl[26] = TradeContext.preAgentSerno  #PREAGENTSERNO    ԭƽ̨��ˮ��
    else:
        TransDtl[26] = ''

    TransDtl[27] = '2'                   # BANKSTATUS     ���н���״̬
    TransDtl[28] = ''                    # BANKCODE       ����.���׷�����
    TransDtl[29] = ''                    # BANKSERNO      ����.������ˮ��

    TransDtl[30] = '2'                   # CORPSTATUS     ����������״̬
    TransDtl[31] = ''                    # CORPCODE       ������.���׷�����
    TransDtl[32] = ''                    # CORPSERNO      ������.������ˮ��
    TransDtl[33] = ''                    # CORPTIME       ������.��������ʱ���

    TransDtl[34] = ''                    # ERRORMSG       ���׷�����Ϣ
    TransDtl[35] = '9'                   # CHKFLAG        �������ʱ�־

    #=======�ź�����,����ֶ�û��ֵȡ��ֵ====
    if( TradeContext.existVariable( "__agentEigen__" ) ) :
        TransDtl[36] = TradeContext.__agentEigen__     # APPENDFLAG         �ӱ��־
    else:
        TransDtl[36] = ""     # APPENDFLAG         �ӱ��־


    if( TradeContext.existVariable( "ifTrxSerno" ) != 0 ):
        TransDtl[37] = TradeContext.ifTrxSerno    # IFTRXSERNO    ��Χ������ˮ��
    else:
        TransDtl[37] = ''

    if( TradeContext.existVariable( "unitno" ) ):
        TransDtl[38] = TradeContext.unitno        # NOTE1          ��ע1(��λ����)
    elif( TradeContext.existVariable( "note1" ) ):
        TransDtl[38] = TradeContext.note1
    else:
        TransDtl[38] = ''

    if( TradeContext.existVariable( "note2" ) ):
        TransDtl[39] = TradeContext.note2         # NOTE2          ��ע2
    else:
        TransDtl[39] = ''

    if( TradeContext.existVariable( "note3" ) ):
        TransDtl[40] = TradeContext.note3         # NOTE3          ��ע3
    else:
        TransDtl[40] = ''

    if( TradeContext.existVariable( "note4" ) ):
        TransDtl[41] = TradeContext.note4         # NOTE4          ��ע4
    else:
        TransDtl[41] = ''

    if( TradeContext.existVariable( "note5" ) ):
        TransDtl[42] = TradeContext.note5         # NOTE5          ��ע5
    else:
        TransDtl[42] = ''

    if( TradeContext.existVariable( "note6" ) ):
        TransDtl[43] = TradeContext.note6         # NOTE6          ��ע6
    else:
        TransDtl[43] = ''

    if( TradeContext.existVariable( "note7" ) ):
        TransDtl[44] = TradeContext.note7         # NOTE7          ��ע7
    else:
        TransDtl[44] = ''

    if( TradeContext.existVariable( "note8" ) ):
        TransDtl[45] = TradeContext.note8         # NOTE8          ��ע8
    else:
        TransDtl[45] = ''

    if( TradeContext.existVariable( "note9" ) ):
        TransDtl[46] = TradeContext.note9         # NOTE9          ��ע9
    else:
        TransDtl[46] = ''

    if( TradeContext.existVariable( "note10" ) ):
        TransDtl[47] = TradeContext.note10        # NOTE10          ��ע10
    else:
        TransDtl[47] = ''

    sql="INSERT INTO FS_MAINTRANSDTL(SERIALNO,WORKDATE,MONTH, \
         WORKTIME,APPNO,BUSINO,TRXCODE,ZONENO,BRNO,TELLERNO, \
         AUTHTELLERNO,CHANNELCODE,TERMID,CATRFLAG,VOUHTYPE,VOUHNO,ACCNO, \
         SUBACCNO,userNo,SUBuserNo,USERNAME,CONTRACTNO,AMOUNT,SUBAMOUNT, \
         REVTRANF,REVTRXDATE,REVAGENTSERNO,BANKSTATUS,BANKCODE,BANKSERNO, \
         CORPSTATUS,CORPCODE,CORPSERNO,CORPTIME,ERRORMSG,CHKFLAG, APPENDFLAG, \
         IFTRXSERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9, \
         NOTE10) VALUES("
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
        TradeContext.errorCode, TradeContext.errorMsg='0000', 'TransOk'
        AfaLoggerFunc.tradeInfo( '������ˮ�����' )
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
    sql="UPDATE FS_MAINTRANSDTL SET "
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
    sql="UPDATE FS_MAINTRANSDTL SET "
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

    if( int( TradeContext.revTranF )!=0 and TradeContext.errorCode == '0000'):
        if( not UpdatePreDtl( action ) ):
            return False

    if( AfaDBFunc.UpdateSqlCmt( sql )<1 ):
        # AfaLoggerFunc.tradeFatal( sql )
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '������ˮ����ʧ��'+AfaDBFunc.sqlErrMsg
        return False

    if( TradeContext.errorCode != '0000' ):
        return  False

    AfaLoggerFunc.tradeInfo( '���±�������ˮ[end]['+ action + ']' )

    return True
