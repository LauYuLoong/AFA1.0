# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.����������
#=================================================================
#   �����ļ�:   AfapFunc.py
#   �޸�ʱ��:   2006-03-31
##################################################################
import TradeContext, AfaDBFunc, AfaFlowControl, AfaUtilTools
import os, time, AfaLoggerFunc
from types import *

#=======================��ѯ�����ֵ����Ч��У��==========================
def Query_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '��ѯ�����ֵ����Ч��У��[begin]' )
    if( not TradeContext.existVariable( "appNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ҵ����[appNo]ֵ������!' )
        
    if( not TradeContext.existVariable( "busiNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'busiNo[busiNo]ֵ������!' )
        
    if( not TradeContext.existVariable( "trxCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '���״���[trxCode]ֵ������!' )
                
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    else:
        TradeContext.channelCode=AfaUtilTools.Lfill( TradeContext.channelCode, 3, '0' )
               
    if( TradeContext.channelCode == '001' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��������[brno]ֵ������!' )
                
        if( not TradeContext.existVariable( "teller" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[teller]ֵ������!' )
    
    AfaLoggerFunc.tradeInfo( '��ѯ�����ֵ����Ч��У��[end]' )        

    return True

#=======================�ɷ������ֵ����Ч��У��==========================
def Pay_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( '�ɷ������ֵ����Ч��У��[begin]' )
    if( not TradeContext.existVariable( "appNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ҵ�����[appNo]ֵ������!' )
        
    if( not TradeContext.existVariable( "busiNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�̺ű��[busiNo]ֵ������!' )

    if ( not TradeContext.existVariable( "termId" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�ն˺�[termId]ֵ������!')
    
    if ( not TradeContext.existVariable( "catrFlag") ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�ֽ�ת�ʱ�־[catrFlag]������!')    
           
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    else:
        TradeContext.channelCode=AfaUtilTools.Lfill( TradeContext.channelCode, 3, '0' )
            
    if( TradeContext.channelCode == '001' ):
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '������[brno]ֵ������!' )
        if( not TradeContext.existVariable( "teller" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[teller]ֵ������!' )
                
    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '���[amount]ֵ������!' )
            
    if( not TradeContext.existVariable( "userNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�û���[userNo]ֵ������!' )
            
    if( not TradeContext.existVariable( "accno" ) ):
        TradeContext.accno=''
        
    #������
    TradeContext.revTranF='0'
    
    AfaLoggerFunc.tradeInfo( '�ɷ������ֵ����Ч��У��[end]' )
        
    return True


#=======================ȡ�����ױ���ֵ����Ч��У��==========================
def Cancel_ChkVariableExist( ):

    AfaLoggerFunc.tradeInfo( 'ȡ�����ױ���ֵ����Ч��У��' )
        
    if( not TradeContext.existVariable( "appNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ҵ�����[appNo]ֵ������!' )
          
    if( not TradeContext.existVariable( "busiNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�̻�����[busiNo]ֵ������!' )
         
    if( not TradeContext.existVariable( "zoneno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '������[zoneno]ֵ������!' )
        
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
            
    else:
        TradeContext.channelCode=AfaUtilTools.Lfill( TradeContext.channelCode, 3, '0' )
    
    if( TradeContext.channelCode == '001' ):
        
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '�����[brno]ֵ������!' )
                
        if( not TradeContext.existVariable( "teller" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[teller]ֵ������!' )
                
    if( not TradeContext.existVariable( "amount" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '���[amount]ֵ������!' )
        
    if( not TradeContext.existVariable( "preAgentSerno" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', 'ԭ������ˮ��[preAgentSerno]ֵ������!' )
        
    if( not TradeContext.existVariable( "userNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�û���[userNo]ֵ������!' )
            
    TradeContext.revTranF='1'
    
    return True


#У�鷴�������������� ������ˮ�űȶ��û��ţ��ʺţ����׽��
def ChkRevInfo( serialno ):

    AfaLoggerFunc.tradeInfo( 'У�鷴��������������[begin]' )
        
    sqlstr="SELECT REVTRANF,USERNO,ACCNO,SUBACCNO,AMOUNT,SUBAMOUNT,TELLERNO,\
            SUBUSERNO,USERNAME,CONTRACTNO,VOUHTYPE,TERMID,\
            VOUHNO,BANKSERNO, CORPSERNO,CORPTIME,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,\
            NOTE7,NOTE8,NOTE9,NOTE10,CATRFLAG,WORKDATE,APPNO,BUSINO FROM FS_MAINTRANSDTL WHERE SERIALNO=" +\
            "'"+serialno+"' AND WORKDATE='"+TradeContext.workDate+ "'AND BANKSTATUS IN ('0','2')"  # 

    tmp = AfaDBFunc.SelectSql( sqlstr )
        
    AfaLoggerFunc.tradeInfo( tmp )
        
    if tmp == None :
        return AfaFlowControl.ExitThisFlow( 'A0025', AfaDBFunc.sqlErrMsg )
            
    elif len( tmp ) == 0 :
        AfaLoggerFunc.tradeInfo( sqlstr )
        return AfaFlowControl.ExitThisFlow( 'A0045', 'δ����ԭ����' )
            
    tmp=AfaUtilTools.ListFilterNone( tmp )

    temp=tmp[0]
    if temp[0]!='0':
        return AfaFlowControl.ExitThisFlow( 'A0020', '��ƥ����Ϣ�����ױ�־����' )
            
    if temp[6]!=TradeContext.teller:
        return AfaFlowControl.ExitThisFlow( 'A0020', '��Ա�Ų�ƥ��' )
      
    #begin 20100624 ����������
    if temp[28] != TradeContext.appNo:
        return AfaFlowControl.ExitThisFlow( 'A0020', 'ҵ���Ų�ƥ��' )
    
    if temp[29] != TradeContext.busiNo:
        return AfaFlowControl.ExitThisFlow( 'A0020', '��λ��Ų�ƥ��' )
    #end
        
            
    if AfaUtilTools.lrtrim(temp[1])!=TradeContext.userNo:
        return AfaFlowControl.ExitThisFlow( 'A0020', '�û��Ų�ƥ��' )      
             
    if AfaUtilTools.lrtrim(temp[4])!=TradeContext.amount:
       AfaLoggerFunc.tradeInfo( temp[4] )
       return AfaFlowControl.ExitThisFlow( 'A0020', '��ƥ��' )
        
    if temp[1]!=TradeContext.userNo:
       return AfaFlowControl.ExitThisFlow( 'A0020', '�û��Ų�ƥ��' )
    
    TradeContext.accno=temp[2]
    TradeContext.subAccno = temp[3]
    TradeContext.subAmount=temp[5]
    TradeContext.subUserNo=temp[7]   
    TradeContext.userName=temp[8]
    
    TradeContext.contractno=temp[9]
    TradeContext.vouhType=temp[10]
    TradeContext.termId=temp[11]
    TradeContext.vouhNo=temp[12]
    
    TradeContext.bankSerno=temp[13]

    TradeContext.corpSerno=temp[14]
    TradeContext.corpTime=temp[15]
    TradeContext.note1=temp[16]
    TradeContext.note2=temp[17]
    TradeContext.note3=temp[18]
    TradeContext.note4=temp[19]
    TradeContext.note5=temp[20]
    TradeContext.note6=temp[21]
    TradeContext.note7=temp[22]
    TradeContext.note8=temp[23]
    TradeContext.note9=temp[24]
    TradeContext.note10=temp[25]
    TradeContext.catrFlag =temp[26]
    TradeContext.revTrxDate = temp[27]
    AfaLoggerFunc.tradeInfo( 'У�鷴��������������[end]' )
    return True


################################################################################
# ������:    ChkAbnormal
# ����:      ��
# ����ֵ��    0  ���쳣����    1  ���쳣����    -1  ��ѯ��ˮ�����쳣ʧ��
# ����˵����  ����Ա��ѯ��ˮ���е������쳣���� 
################################################################################
def ChkAbnormal( ):

    AfaLoggerFunc.tradeInfo( '��ѯ��ˮ���е������쳣����' )
    sql="SELECT COUNT(*) FROM FS_MAINTRANSDTL WHERE WORKDATE='"+ \
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

#============================�ж�Ӧ��״̬============================
def ChkAppStatus( ):

    AfaLoggerFunc.tradeInfo( '�ж�Ӧ��״̬[begin]' )

    #============ҵ����============
    sqlStr = "SELECT STATUS,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO FROM ABDT_UNITINFO WHERE APPNO = '" + TradeContext.appNo + "'"

    #============��λ����============
    sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busiNo + "'"

    #============ί�з�ʽ============
    sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"

    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        # AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControl.ExitThisFlow( 'A0002', '���մ���_��λ��Ϣ��:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
        #===============�ж�ҵ��״̬============================
        if( records[0][0]=="0" ):
            return AfaFlowControl.ExitThisFlow( 'A0004', '��ҵ����δ����״̬,�������˽���' )
        elif( records[0][0]=="2" ):
            return AfaFlowControl.ExitThisFlow( 'A0005', '��ҵ���ڹر�״̬,�������˽���' )
        elif( records[0][0]=="3" ):
            return AfaFlowControl.ExitThisFlow( 'A0006', '��ҵ����ͣ��״̬,�������˽���' )
        
        #===============�жϷ���ʱ��============================
        if( long( TradeContext.workDate )<long( records[0][1] ) or long( TradeContext.workDate )>long( records[0][2] ) ):
            return AfaFlowControl.ExitThisFlow ('A0008', "��ҵ���ѹ���,��Ч��:["+records[0][1] + "-->" + records[0][2] + "]") 

        #================�ж���Чʱ��===========================
        if( long(TradeContext.workTime) < long(records[0][3])) or (long(TradeContext.workTime) > long(records[0][4])):
            return AfaFlowControl.ExitThisFlow( 'A0007', "����ҵ�񿪷�ʱ��,����["+records[0][3]+"-->"+records[0][4]+"]����ҵ��" )

        #=============����ҵ���ʺ�=============
        TradeContext.__agentAccno__ = records[0][5]            

        TradeContext.Daccno = records[0][5]

        AfaLoggerFunc.tradeInfo( '�ж�Ӧ��״̬[end]' )
        return True
    else:
        AfaLoggerFunc.tradeError( sqlStr )
        return AfaFlowControl.ExitThisFlow( 'A0003', '�õ���û�п��Ŵ�ҵ��' )
