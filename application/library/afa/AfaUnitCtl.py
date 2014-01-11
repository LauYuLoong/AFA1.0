# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.�̻�״̬����
#=================================================================
#   �����ļ�:   AfaUnitCtl.py
#   �޸�ʱ��:   2006-09-26
##################################################################
import os
from types import *
import exceptions, TradeContext, AfaDBFunc, TradeException, AfaUtilTools
import ConfigParser, time, Party3Context,AfaLoggerFunc,AfaFlowControl

#��ȡ�̻�����
def GetUnitStatus():
    AfaLoggerFunc.tradeInfo('��ȡ�̻�����' )
    #============ϵͳ��ʶ============
    sqlStr = "SELECT * FROM AFA_UNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND "
    #============�̻�����============
    sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' "
    AfaLoggerFunc.tradeInfo( sqlStr )
    records = AfaDBFunc.SelectSql( sqlStr )
    if( records == None ):
        AfaLoggerFunc.tradeFatal( sqlStr )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����̻���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    elif( len( records )!=0 ):
        AfaUtilTools.ListFilterNone( records )
        TradeContext.__busiMode__ = records[0][6]   #=============ҵ��ģʽ=============
        if( TradeContext.__busiMode__!="2" ):
            TradeContext.__unitStatus__ = records[0][4]         #=============ҵ��״̬=============
            TradeContext.__unitLoginStatus__ = records[0][27]   #=============ǩ����״̬=============
            TradeContext.__unitDayendStatus__ = records[0][28]  #=============����״̬=============
            TradeContext.__unitCheckStatus__ = records[0][30]   #=============����ҵ��״̬=============
        if( TradeContext.__busiMode__=="2" ):
            AfaLoggerFunc.tradeInfo('��ȡ���̻�����' )
            #============ϵͳ��ʶ============
            sqlStr = "SELECT * FROM AFA_SUBUNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND "
            #============�̻�����============
            sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' AND "
            #============���̻�����============
            sqlStr = sqlStr+"SUBUNITNO = '" + TradeContext.subUnitno + "' "
            subRecords = AfaDBFunc.SelectSql( sqlStr )
            if(subRecords == None ):
                return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����̻���֧��λ��Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
            elif( len( subRecords )!=0 ):
                AfaUtilTools.ListFilterNone( subRecords )
                TradeContext.__unitStatus__ = subRecords[0][4]         #=============ҵ��״̬=============
                TradeContext.__unitLoginStatus__ = subRecords[0][27]   #=============ǩ����״̬=============
                TradeContext.__unitDayendStatus__ = subRecords[0][28]  #=============����״̬=============
                TradeContext.__unitCheckStatus__ = subRecords[0][30]   #=============����ҵ��״̬=============
    return True
#�޸��̻�״̬
def UpdUnitStatus(flag):
    AfaLoggerFunc.tradeInfo('�޸��̻�״̬' )
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET STATUS='"+flag+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET STATUS='"+flag+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����̻���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    return True

#�޸��̻�ǩ��״̬
def UpdUnitLoginStatus(flag):
    AfaLoggerFunc.tradeInfo('�޸��̻�ǩ��״̬' )
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET LOGINSTATUS='"+flag+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET LOGINSTATUS='"+flag+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����̻���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    return True
#�޸��̻�����״̬
def UpdUnitDayendStatus(flag):
    AfaLoggerFunc.tradeInfo('�޸��̻�����״̬' )
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET DAYENDSTATUS='"+flag+"',dayendtime='"+TradeContext.workTime+\
            "' WHERE SYSID='"+TradeContext.sysId+"'and UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET DAYENDSTATUS='"+flag+"' , dayendtime='"+TradeContext.workTime+\
            "' WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����̻���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    return True
#�޸��̻�����״̬
def UpdUnitCheckStatus(flag):
    AfaLoggerFunc.tradeInfo('�޸��̻�����״̬' )
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET TRXCHKSTATUS='"+flag+"', trxchktime="+TradeContext.workTime+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET TRXCHKSTATUS='"+flag+"', trxchktime="+TradeContext.workTime+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����̻���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    return True
#�޸��̻���ǰ��������
def UpdUnitWorkDate():
    AfaLoggerFunc.tradeInfo('�޸��̻���ǰ��������' )
    curworkdate=TradeContext.workDate
    if(  TradeContext.existVariable( "nextWorkDate" ) ):
        curworkdate=TradeContext.nextWorkDate
    GetUnitStatus()
    if(TradeContext.__busiMode__!='2'):
        sql="UPDATE AFA_UNITADM SET  PREWORKDATE=WORKDATE,WORKDATE='"+curworkdate+"'"+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"'"
    else:
        sql="UPDATE AFA_SUBUNITADM SET PREWORKDATE=WORKDATE,WORKDATE='"+curworkdate+"' "+\
            " WHERE SYSID='"+TradeContext.sysId+"' AND UNITNO='"+TradeContext.unitno+"' AND "\
            "SUBUNITNO='"+TradeContext.subUnitno+"'"
    AfaLoggerFunc.tradeInfo(sql )
    records=AfaDBFunc.UpdateSqlCmt( sql )
    if( records <0 ):
        AfaLoggerFunc.tradeFatal( sql )
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����̻���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
    return True
#��������ͣ����ˮ
def InsertOnOffDTL():
    sql="insert into afa_UnitOnOffDTL(SYSID,UNITNO,SUBUNITNO,STATUS,OPERFLAG,STOPTIME,STARTTIME,NOTE1,NOTE2)"
    sql=sql+" values"
    sql=sql+"('"+TradeContext.sysId       +"'"
    sql=sql+",'"+TradeContext.unitno      +"'"
    sql=sql+",'"+TradeContext.TaxOrgName     +"'"
    sql=sql+",'"+'1'                         +"'"
    sql=sql+",'"+TradeContext.operFlag      +"'"
    sql=sql+",'"+TradeContext.stopTime      +"'"
    sql=sql+",'"+TradeContext.startTime      +"'"
    sql=sql+",'"+TradeContext.NOTE1           +"'"
    sql=sql+",'"+TradeContext.NOTE2           +"'"
    sql=sql+")"
    if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
        AfaLoggerFunc.tradeFatal(sql)
        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
    return True


#��ȡ�̻�����
#def GetUnitStatus():
#    AfaLoggerFunc.tradeInfo('��ȡ�̻�����' )
#    #============ϵͳ��ʶ============
#    sqlStr = "SELECT * FROM AFA_UNITADM WHERE SYSID = '" + TradeContext.sysId + "' AND "
#    #============�̻�����============
#    sqlStr = sqlStr+"UNITNO = '" + TradeContext.unitno + "' "
#    AfaLoggerFunc.tradeInfo( sqlStr )
#    records = AfaDBFunc.SelectSql( sqlStr )
#    if( records == None ):
#        AfaLoggerFunc.tradeFatal( sqlStr )
#        return AfaFlowControl.ExitThisFlow( 'A0025', '���ݿ�����̻���Ϣ������쳣:'+AfaDBFunc.sqlErrMsg )
#    elif( len( records )!=0 ):
#        AfaUtilTools.ListFilterNone( records )
#        TradeContext.__busiMode__ = records[0][6]   #=============ҵ��ģʽ=============