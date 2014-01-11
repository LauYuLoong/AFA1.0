# -*- coding: gbk -*-
################################################################################
# �ļ����ƣ�AfaTjFunc.py
# �ļ���ʶ��
# ժ    Ҫ���м�ҵ��ͨ��ҵ��
#
################################################################################
import TradeContext, AfaDBFunc, AfaFlowControl, AfaUtilTools
import os, time, AfaLoggerFunc
from types import *

#============================�ж�Ӧ��״̬============================
def ChkUnitInfo( ):

    AfaLoggerFunc.tradeInfo( '�����������ж�Ӧ��״̬��ʼ����������' )

    sqlStr = ''
    sqlStr = sqlStr + "SELECT STATUS,STARTDATE,ENDDATE,STARTTIME,ENDTIME,ACCNO FROM ABDT_UNITINFO "
    sqlStr = sqlStr + " AND WHERE APPNO = '" + TradeContext.sysId + "'"

    #============��λ����============
    sqlStr = sqlStr + " AND BUSINO = '" + TradeContext.busino + "'"

    #============ί�з�ʽ============
    sqlStr = sqlStr + " AND AGENTTYPE IN ('1','2')"
    
    AfaLoggerFunc.tradeFatal( '��ѯ��� ��'+sqlStr )
    
    records = AfaDBFunc.SelectSql( sqlStr )
    
    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0002', '��ѯ��λЭ����Ϣ�쳣')

    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
        
        TradeContext.STATUS        = str(records[0][0])                             #ǩԼ״̬
        TradeContext.STARTDATE     = str(records[0][1])                             #��Ч����
        TradeContext.ENDDATE       = str(records[0][2])                             #ʧЧ����
        TradeContext.STARTTIME     = str(records[0][3])                             #����ʼʱ��
        TradeContext.ENDTIME       = str(records[0][4])                             #������ֹʱ��
        TradeContext.ACCNO         = str(records[0][5])                             #�Թ��˻�
        
        
        if ( (TradeContext.STARTDATE > TradeContext.workDate) or (TradeContext.workDate > TradeContext.ENDDATE) ):
            return AfaFlowControl.ExitThisFlow( '9000', '�õ�λί��Э�黹û����Ч���ѹ���Ч��')

        if ( (TradeContext.STARTTIME > TradeContext.workTime) or (TradeContext.workTime > TradeContext.ENDTIME) ):
            return AfaFlowControl.ExitThisFlow( '9000', '�Ѿ�������ϵͳ�ķ���ʱ��,��ҵ�������[' + s_StartDate + ']-[' + s_EndDate + ']ʱ�������')

        #=============����ҵ���ʺ�=============
        #TradeContext.__agentAccno__ = records[0][5] 
        #AfaLoggerFunc.tradeInfo('�տ����ʻ�__agentAccno__ BB����'+ TradeContext.__agentAccno__)           

        AfaLoggerFunc.tradeInfo( '�����������ж�Ӧ��״̬������������������' )
        return True
    else:
        AfaLoggerFunc.tradeError( sqlStr )
        return AfaFlowControl.ExitThisFlow( 'A0003', '�õ���û�п��Ŵ�ҵ��' )



#============================�ж�ҵ����============================
def ChkSysInfo( ):
    AfaLoggerFunc.tradeInfo( '�����������ж�ҵ���ſ�ʼ����������' )
 
    #�ж�ҵ���� AG2016
    if not( TradeContext.existVariable( "sysId" ) and len(TradeContext.sysId.strip()) > 0):
            TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "ҵ���Ų�����"
            raise AfaFlowControl.flowException( )
            
    if not(TradeContext.sysId == 'AG2016') :
        TradeContext.errorCode,TradeContext.errorMsg = 'E9999', "�Ǵ�ҵ���ţ���������ҵ��!"
        raise AfaFlowControl.flowException( )        
                










