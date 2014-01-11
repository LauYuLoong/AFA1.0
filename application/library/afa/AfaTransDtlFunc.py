# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.������ˮ�������
#=================================================================
#   �����ļ�:   AfaTransDtlFunc.py
#   �޸�ʱ��:   2006-03-31
##################################################################
import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,AfaFlowControl,TransBillFunc,AfaFunc
from types import *


################################################################################
# ������:    InsertDtl
# ����:      ��
# ����ֵ��    True  ������ˮ��ɹ�    False ������ˮ��ʧ��
# ����˵����  ����ˮ��Ϣ������ˮ��
################################################################################
def InsertDtl( ):

    AfaLoggerFunc.tradeInfo( '>>>������ˮ��' )

    #��ˮ�������-1
    count=52
    TransDtl=[[]]*( count+1 )
    TransDtl[0] = TradeContext.agentSerialno                    # AGENTSERIALNO ����ҵ����ˮ��
    TransDtl[1] = TradeContext.workDate                         # WORKDATE      ��������
    TransDtl[2] = TradeContext.workTime                         # WORKTIME      ����ʱ��
    TransDtl[3] = TradeContext.sysId                            # SYSID         ϵͳ��ʶ
    TransDtl[4] = TradeContext.unitno                           # UNITNO        �̻���λ����
    TransDtl[5] = TradeContext.subUnitno                        # SUBUNITNO     �̻���֧��λ����
    TransDtl[6] = TradeContext.agentFlag                        # AGENTFLAG     ҵ��ʽ
    TransDtl[7] = TradeContext.TransCode                        # TRXCODE       ������
    TransDtl[8] = TradeContext.zoneno                           # ZONENO        ���к�
    TransDtl[9] = TradeContext.brno                             # BRNO          ������
    TransDtl[10]= TradeContext.tellerno                         # TELLERNO      ��Ա��
    TransDtl[11]= TradeContext.cashTelno                        # CASHTELNO     ����Ա��

    if( TradeContext.existVariable( "authTeller" ) ) :
        TransDtl[12] = TradeContext.authTeller                  # AUTHTELLERNO  ��Ȩ��Ա��  
    else:
        TransDtl[12] = ''

    TransDtl[13] = TradeContext.channelCode                     # CHANNELCODE   ��������

    if( TradeContext.existVariable( "channelSerno" ) ):
        TransDtl[14] = TradeContext.channelSerno                # CHANNELSERNO  ����������ˮ��
    else:
        TransDtl[14]=''

    if( TradeContext.existVariable( "termId" ) ):
        TransDtl[15] = TradeContext.termId                      # TERMID        �ն˺�
    else:
        TransDtl[15]=''

    if( TradeContext.existVariable( "customerId" ) ):
        TransDtl[16] = TradeContext.customerId                  # CUSTOMERID    �ͻ�ע���
    else:
        TransDtl[16]=''

    TransDtl[17] = TradeContext.userno                          # USERNO        �û���  

    if( TradeContext.existVariable( "subUserno" ) ):
        TransDtl[18] = TradeContext.subUserno                   # SUBUSERNO     �����û���  
    else:
        TransDtl[18] = ''

    if( TradeContext.existVariable( "userName" ) ):
        TransDtl[19] = TradeContext.userName                    # USERNAME      �û�����  
    else:
        TransDtl[19] = '' 

    if( TradeContext.existVariable( "accType" ) ):
        TransDtl[20] = TradeContext.accType                     # ACCTYPE       �ʻ�����
    else:
        TransDtl[20] = '000'


    #��λ�ʺ�
    if( TradeContext.existVariable( "__agentAccno__" ) ):
        agentAccno = TradeContext.__agentAccno__
    else:
        agentAccno = ''


    #�ͻ��ʺ�
    if( TradeContext.existVariable( "accno" ) ):
        accno = TradeContext.accno
    else:
        accno = ''

 
    if( int( TradeContext.revTranF ) == 0 ):
        #ҵ��ʽ(01-���� 02-���� 03-���� 04-����)
        if( int( TradeContext.agentFlag ) == 1 or int( TradeContext.agentFlag ) == 3 ):
            TransDtl[21] = accno                                # DRACCNO       �跽�ʺ�
            TransDtl[22] = agentAccno                           # CRACCNO       �����ʺ� 
            TradeContext.__drAccno__ = accno
            TradeContext.__crAccno__ = agentAccno
        else:
            TransDtl[21] = agentAccno
            TransDtl[22] = accno
            TradeContext.__drAccno__ = agentAccno
            TradeContext.__crAccno__ = accno
    else:
        TransDtl[21] = TradeContext.__drAccno__                 # DRACCNO       �跽�ʺ�
        TransDtl[22] = TradeContext.__crAccno__                 # DRACCNO       �����ʺ�


    if( TradeContext.existVariable( "vouhType" ) ):
        TransDtl[23] = TradeContext.vouhType                    # VOUHTYPE      ƾ֤����  
    else:
        TransDtl[23] = ''


    if( TradeContext.existVariable( "vouhno" ) ):
        TransDtl[24] = TradeContext.vouhno                      # VOUHNO        ƾ֤��  
    else:
        TransDtl[24] = ''


    if( TradeContext.existVariable( "vouhDate" ) ):
        TransDtl[25] = TradeContext.vouhDate                    # VOUHDATE      ƾ֤����  
    else:
        TransDtl[25] = ''


    if( TradeContext.existVariable( "currType" ) ):
        TransDtl[26] = TradeContext.currType                    # CURRTYPE      ����
    else:
        TransDtl[26] = '1'

    
    if( TradeContext.existVariable( "currFlag" ) ):
        TransDtl[27] = TradeContext.currFlag                    # CURRFLAG      �����־
    else:
        TransDtl[27] = '0'


    TransDtl[28] = TradeContext.amount                          # AMOUNT        ���׽��


    if( TradeContext.existVariable( "subAmount" ) ):
        TransDtl[29] = TradeContext.subAmount                   # SUBAMOUNT     ���ӽ��  
    else:
        TransDtl[29] = ''


    TransDtl[30] = TradeContext.revTranF                        # REVTRANF      �����ױ�־(0-������ 1-������ 2-�Զ�����)
                                               
    if( int( TradeContext.revTranF ) != 0 ):
        TransDtl[31] = TradeContext.preAgentSerno               # PREAGENTSERNO ԭƽ̨��ˮ��  
    else:
        TransDtl[31] = ''

    TransDtl[32] = '2'                                          # BANKSTATUS    ����.����״̬(0-���� 1-ʧ�� 2-�쳣 3-�ѳ���)
    TransDtl[33] = ''                                           # BANKCODE      ����.���׷�����
    TransDtl[34] = ''                                           # BANKSERNO     ����.������ˮ��

    TransDtl[35] = '2'                                          # CORPSTATUS    ��ҵ.����״̬(0-���� 1-ʧ�� 2-�쳣 3-�ѳ���)
    TransDtl[36] = ''                                           # CORPCODE      ��ҵ.���׷�����
    TransDtl[37] = ''                                           # CORPSERNO     ��ҵ.������ˮ��
    TransDtl[38] = ''                                           # CORPTIME      ��ҵ.ʱ���

    TransDtl[39] = ''                                           # ERRORMSG      ���׷�����Ϣ
                                                                
    TransDtl[40] = '9'                                          # CHKFLAG       �������ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����) 
                                                                
    TransDtl[41] = '9'                                          # CORPCHKFLAG   ��ҵ���ʱ�־(0-�Ѷ���,���׳ɹ� 1-�Ѷ���,����ʧ��, 9-δ����)

    TransDtl[42] = TradeContext.__agentEigen__[4]               # APPENDFLAG    �ӱ�ʹ�ñ�־(0-��ʹ�� 1-ʹ��)

    if( TradeContext.existVariable( "note1" ) ):                # NOTE1         ��ע1
        TransDtl[43] = TradeContext.note1
    else:
        TransDtl[43] = ''

    if( TradeContext.existVariable( "note2" ) ):
        TransDtl[44] = TradeContext.note2                       # NOTE2         ��ע2
    else:                                                       
        TransDtl[44] = ''                                       
                                                                
    if( TradeContext.existVariable( "note3" ) ):                
        TransDtl[45] = TradeContext.note3                       # NOTE3         ��ע3
    else:                                                       
        TransDtl[45] = ''                                       
                                                                
    if( TradeContext.existVariable( "note4" ) ):                
        TransDtl[46] = TradeContext.note4                       # NOTE4         ��ע4
    else:                                                       
        TransDtl[46] = ''                                       
                                                                
    if( TradeContext.existVariable( "note5" ) ):                
        TransDtl[47] = TradeContext.note5                       # NOTE5         ��ע5
    else:                                                       
        TransDtl[47] = ''                                       
                                                                
    if( TradeContext.existVariable( "note6" ) ):                
        TransDtl[48] = TradeContext.note6                       # NOTE6         ��ע6
    else:                                                       
        TransDtl[48] = ''                                       
                                                                
    if( TradeContext.existVariable( "note7" ) ):                
        TransDtl[49] = TradeContext.note7                       # NOTE7         ��ע7
    else:                                                       
        TransDtl[49] = ''                                       
                                                                
    if( TradeContext.existVariable( "note8" ) ):                
        TransDtl[50] = TradeContext.note8                       # NOTE8         ��ע8
    else:                                                       
        TransDtl[50] = ''                                       
                                                                
    if( TradeContext.existVariable( "note9" ) ):                
        TransDtl[51] = TradeContext.note9                       # NOTE9         ��ע9
    else:                                                       
        TransDtl[51] = ''                                       
                                                                
    if( TradeContext.existVariable( "note10" ) ):               
        TransDtl[52] = TradeContext.note10                      # NOTE10        ��ע10
    else:
        TransDtl[52] = ''

    sql = "INSERT INTO AFA_MAINTRANSDTL(AGENTSERIALNO,WORKDATE,"
    sql = sql + "WORKTIME,SYSID,UNITNO,SUBUNITNO,AGENTFLAG,TRXCODE,ZONENO,BRNO,TELLERNO,CASHTELNO,"
    sql = sql + "AUTHTELLERNO,CHANNELCODE,CHANNELSERNO,TERMID,CUSTOMERID,USERNO,SUBUSERNO,USERNAME,"
    sql = sql + "ACCTYPE,DRACCNO,CRACCNO,VOUHTYPE,VOUHNO,VOUHDATE,"
    sql = sql + "CURRTYPE,CURRFLAG,AMOUNT,SUBAMOUNT,REVTRANF,PREAGENTSERNO,BANKSTATUS,BANKCODE,"
    sql = sql + "BANKSERNO,CORPSTATUS,CORPCODE,CORPSERNO,CORPTIME,ERRORMSG,CHKFLAG,CORPCHKFLAG,"
    sql = sql + "APPENDFLAG,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9,"
    sql = sql + "NOTE10) VALUES("
    
    i=0
    for i in range( 0, count ):
        if( type( TransDtl[i] ) is int ):
            sql=sql+str( TransDtl[i] )+","
        else:
            sql=sql+"'"+ TransDtl[i]+"',"
            
    sql=sql+"'"+TransDtl[count]+"')"

    AfaLoggerFunc.tradeInfo( sql )
    
    result=AfaDBFunc.InsertSqlCmt( sql )
        
    if( result < 1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0044', '������ˮ����ʧ��'+AfaDBFunc.sqlErrMsg
        return False

    else:
        #������:�ӱ�ʹ�ñ�־(�����׺���)
        if ( TradeContext.__agentEigen__[4]=='1' and TradeContext.revTranF=='0' ):
            if( not SubTransDtlProc( '1' ) ):
                TradeContext.errorCode, TradeContext.errorMsg='A0040', '�ӱ����ʧ��'
                return False

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

    AfaLoggerFunc.tradeInfo( '>>>����ԭ������ˮ��Ϣ' )
        
    sqlstr="UPDATE AFA_MAINTRANSDTL SET "
    
    if( action == 'BANK' ):
        sqlstr=sqlstr+" BANKSTATUS='3' "

    elif( action == 'CORP' ):
        sqlstr=sqlstr+" CORPSTATUS='3' "

    elif( action == 'TRADE' ):
        sqlstr=sqlstr+" BANKSTATUS='3',CORPSTATUS='3'"
        
    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0041', '��ڲ�������������û���������͵Ĳ���'
        return False
        
        
    sqlstr = sqlstr + " WHERE "

    #ԭ������ˮ��
    if(TradeContext.existVariable( "preAgentSerno" )) :
        sqlstr=sqlstr + " AGENTSERIALNO='"+TradeContext.preAgentSerno+"' AND "
        
    #ԭ������ˮ��
    if(TradeContext.existVariable( "preChannelSerno" )) :
        sqlstr=sqlstr + " CHANNELSERNO='"+TradeContext.preChannelSerno+"' AND "
        
    sqlstr = sqlstr + " WORKDATE='" + TradeContext.workDate + "' AND REVTRANF='0'"

    AfaLoggerFunc.tradeInfo( sqlstr )

    ret=AfaDBFunc.UpdateSqlCmt( sqlstr )
    if( ret > 0 ):
        return True

    if( ret == 0 ):
        TradeContext.errorCode,TradeContext.errorMsg='A0100','δ����ԭʼ����'
        return False

    else :
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '����ԭ����״̬ʧ��' + AfaDBFunc.sqlErrMsg    
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

    AfaLoggerFunc.tradeInfo( '>>>���½�����ˮ״̬(' + action + ')' )
        
    sql = "UPDATE AFA_MAINTRANSDTL SET "

    if( TradeContext.existVariable( "errorMsg" ) ):
        sql = sql + "ERRORMSG='" + TradeContext.errorMsg + "',"

    if( action == 'BANK' ):
        sql = sql + "BANKSTATUS='" + TradeContext.__status__+ "',BANKCODE='" + TradeContext.errorCode + "'"
        
        if( TradeContext.existVariable( "bankSerno" ) ):
            sql = sql + ",BANKSERNO='" + TradeContext.bankSerno + "'"

    elif( action == 'CORP' ):
        sql = sql + "CORPSTATUS='" + TradeContext.__status__ + "',CORPCODE='" + TradeContext.errorCode + "'"
        
        if( TradeContext.existVariable( "corpSerno" ) ):
            sql = sql + ",CORPSERNO='" + TradeContext.corpSerno + "'"

        if( TradeContext.existVariable( "corpTime" ) ):
            sql = sql + ",CORPTIME='"  + TradeContext.corpTime  + "'"

    elif( action == 'TRADE' ):
        sql = sql + "CORPSTATUS='" + TradeContext.__status__ + "',BANKSTATUS='" + TradeContext.__status__ + "',CORPCODE='" + TradeContext.errorCode + "',BANKCODE='" + TradeContext.errorCode + "'"
        
        if( TradeContext.existVariable( "bankSerno" ) ):
            sql = sql + ",BANKSERNO='" + TradeContext.bankSerno + "'"

        if( TradeContext.existVariable( "corpSerno" ) ):
            sql = sql + ",CORPSERNO='" + TradeContext.corpSerno + "'"

        if( TradeContext.existVariable( "corpTime" ) ):
            sql = sql + ",CORPTIME='"  + TradeContext.corpTime  + "'"

    else:
        TradeContext.errorCode, TradeContext.errorMsg='A0041', '��ڲ�������������û���������͵Ĳ���'
        return False


    if( TradeContext.existVariable( "note1" ) ):
        sql = sql + ",NOTE1='" +  TradeContext.note1 + "'"              # NOTE1         ��ע1

    if( TradeContext.existVariable( "note2" ) ):
        sql = sql + ",NOTE2='" +  TradeContext.note2 + "'"              # NOTE2         ��ע2

    if( TradeContext.existVariable( "note3" ) ):
        sql = sql + ",NOTE3='" +  TradeContext.note3 + "'"              # NOTE3         ��ע3

    if( TradeContext.existVariable( "note4" ) ):
        sql = sql + ",NOTE4='" +  TradeContext.note4 + "'"              # NOTE4         ��ע4

    if( TradeContext.existVariable( "note5" ) ):
        sql = sql + ",NOTE5='" +  TradeContext.note5 + "'"              # NOTE5         ��ע5

    if( TradeContext.existVariable( "note6" ) ):
        sql = sql + ",NOTE6='" +  TradeContext.note6 + "'"              # NOTE6         ��ע6

    if( TradeContext.existVariable( "note7" ) ):
        sql = sql + ",NOTE7='" +  TradeContext.note7 + "'"              # NOTE7         ��ע7

    if( TradeContext.existVariable( "note8" ) ):
        sql = sql + ",NOTE8='" +  TradeContext.note8 + "'"              # NOTE8         ��ע8

    if( TradeContext.existVariable( "note9" ) ):
        sql = sql + ",NOTE9='" +  TradeContext.note9 + "'"              # NOTE9         ��ע9

    if( TradeContext.existVariable( "note10" ) ):
        sql = sql + ",NOTE10='"+  TradeContext.note10+ "'"              # NOTE10        ��ע10
        
        
    sql = sql + " WHERE AGENTSERIALNO='" + TradeContext.agentSerialno + "' AND WORKDATE='" + TradeContext.workDate + "' AND REVTRANF='" + TradeContext.revTranF + "'"

    #����ԭ��ˮ״̬
    if( int( TradeContext.revTranF )!=0 and TradeContext.errorCode == '0000'):
        if( not UpdatePreDtl( action ) ):
            return False

    AfaLoggerFunc.tradeInfo( sql )


    #���±���ˮ״̬
    AfaLoggerFunc.tradeInfo( '>>>���±�������ˮ��Ϣ' )
    if( AfaDBFunc.UpdateSqlCmt( sql )<1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '������ˮ����ʧ��'+AfaDBFunc.sqlErrMsg
        return False


    if( TradeContext.errorCode != '0000' ):
        return  False


    if ( action == 'CORP' ):
        #���Ӷ���ˮ�ӱ�Ĵ���
        if ( TradeContext.__agentEigen__[4]=='1' and TradeContext.revTranF=='0' and TradeContext.errorCode=='0000' ):
            if( TradeContext.existVariable( "afe_appendFlag" ) and TradeContext.afe_appendFlag=='1' ):
                if( not SubTransDtlProc( '2' ) ):
                    return False
 
    return True


################################################################################
# ������:    SubTransDtlProc
# ����:      action 1-����  2-�޸�
# ����ֵ��   True  ������ǰ���״���ˮ�ɹ�    False ������ǰ���״���ˮʧ��
# ����˵���� ά���ӱ���Ϣ
################################################################################
def SubTransDtlProc( action ):

    AfaLoggerFunc.tradeInfo( '>>>���ӽ�����ˮ�ӱ���Ϣ' )

    #����
    if ( action == '1' ):
        sql = "INSERT INTO AFA_SUBTRANSDTL(AGENTSERIALNO,WORKDATE,RECSEQNO,DATA1,DATA2) VALUES("    
        sql = sql + "'"  +  TradeContext.agentSerialno  + "'"
        sql = sql + ",'" +  TradeContext.workDate       + "'"
        sql = sql + ",'" +  '1'                         + "'"

        if( TradeContext.existVariable( "appendData1" ) ):
            sql = sql + ",'" +  TradeContext.appendData1   + "'"
        else:
            sql = sql + ",'" + ""                          + "'"

        if( TradeContext.existVariable( "appendData2" ) ):
            sql = sql + ",'" +  TradeContext.appendData2   + "'"
        else:
            sql = sql + ",'" + ""                          + "'"

        sql = sql + ")"

        AfaLoggerFunc.tradeInfo( sql )
    
        subresult = AfaDBFunc.InsertSqlCmt( sql )

        if( subresult < 1 ):
            TradeContext.errorCode, TradeContext.errorMsg='A0044', '������ˮ�ӱ�ʧ��'+AfaDBFunc.sqlErrMsg
            return False


    #�޸�
    if ( action == '2' ):
        sql = "UPDATE AFA_SUBTRANSDTL SET "

        if( TradeContext.existVariable( "afe_appendData1" ) ):
            sql = sql + "DATA1='"  +  TradeContext.afe_appendData1   + "'"

        if( TradeContext.existVariable( "afe_appendData2" ) ):
            sql = sql + ",DATA2='" +  TradeContext.afe_appendData2   + "'"

        sql = sql + " WHERE "

        sql = sql + "AGENTSERIALNO='" +  TradeContext.agentSerialno + "' AND "
        sql = sql + "WORKDATE='"      +  TradeContext.workDate      + "'"

        AfaLoggerFunc.tradeInfo( sql )

        subresult = AfaDBFunc.UpdateSqlCmt( sql )

        if( subresult < 1 ):
            TradeContext.errorCode, TradeContext.errorMsg='A0044', '������ˮ�ӱ�ʧ��'+AfaDBFunc.sqlErrMsg
            return False

    return True
