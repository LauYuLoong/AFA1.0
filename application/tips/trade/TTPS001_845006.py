# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.ֹ������
#=================================================================
#   �����ļ�:   003001_031123.py
#   �޸�ʱ��:   2007-5-28 10:28
##################################################################
import TradeContext, LoggerFunc, UtilTools,AfaFlowControl,AfaAfeFunc,AfapFunc,DBFunc

#import datetime,TradeException,ConfigParser,os,TipsFunc
from types import *

def SubModuleMainFst( ):
    LoggerFunc.tradeInfo('��˰����_ֹ��������_ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #=============��ȡ��ǰϵͳʱ��====================
        TradeContext.workDate=UtilTools.GetSysDate( )
        TradeContext.workTime=UtilTools.GetSysTime( )
        
        ##============У�鹫���ڵ����Ч��==================
        #if( not AfapFunc.Query_ChkVariableExist( ) ):
        #    raise AfaFlowControl.flowException( )
        ##===============�ж�Ӧ��ϵͳ״̬======================
        #if not AfapFunc.ChkSysStatus( ) :
        #    raise AfaFlowControl.flowException( )
        ##===============�ж��̻�״̬======================
        #if not AfapFunc.ChkUnitStatus( ) :
        #    raise AfaFlowControl.flowException( )
        ##=============�ж�Ӧ��״̬====================
        #if not AfapFunc.ChkAppStatus( ) :
        #    raise AfaFlowControl.flowException( )
        #
                    
        #============����ֵ����Ч��У��============
        if( not TradeContext.existVariable( "TaxOrgCode" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[TaxOrgCode]ֵ������!' )
        if( not TradeContext.existVariable( "OriPackNo" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[OriPackNo]ֵ������!' )
        if( not TradeContext.existVariable( "EntrustDate" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[EntrustDate]ֵ������!' )
        if( not TradeContext.existVariable( "OriEntrustDate" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[OriEntrustDate]ֵ������!' )
        if( not TradeContext.existVariable( "StopReason" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[StopReason]ֵ������!' )
        if( not TradeContext.existVariable( "StopType" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '[StopType]ֵ������!' )
        
        if (TradeContext.StopType=='0'):
            if( not TradeContext.existVariable( "OriTraNo" ) ):
                return AfaFlowControl.ExitThisFlow( 'A0001', '[OriTraNo]ֵ������!' )
            #��ѯ������ˮ����״̬
            sqlStr = "SELECT STATUS FROM BATCH_TRANSDTL WHERE "
            sqlStr =sqlStr +" sysid             = '" + TradeContext.appNo           + "'"
            sqlStr =sqlStr +"and unitno         = '" + TradeContext.unitno          + "'"
            #sqlStr =sqlStr +"and subUnitno      = '" + TradeContext.subUnitno       + "'"
            sqlStr =sqlStr +"and workDate       = '" + TradeContext.OriEntrustDate  + "'"
            sqlStr =sqlStr +"and Batchno        = '" + TradeContext.PackNo          + "'"
            sqlStr =sqlStr +"and CORPSERIALNO   = '" + TradeContext.OriTraNo        + "'"
            sqlStr =sqlStr +"and NOTE1          = '" + TradeContext.TaxOrgCode      + "'"
            Records = DBFunc.SelectSql( sqlStr )
            LoggerFunc.tradeInfo(sqlStr)
            if( Records == None ):
                LoggerFunc.tradeFatal('�������������쳣:'+DBFunc.sqlErrMsg)
                return AfaFlowControl.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
            elif(len(Records)>0):
                if Records[0][0]=='9': #��ˮ��δ����
                    sqlStr = "UPDATE BATCH_TRANSDTL SET STATUS='1',ERRORMSG='��ֹ��' WHERE "
                    sqlStr =sqlStr +" sysid             = '" + TradeContext.appNo           + "'"
                    sqlStr =sqlStr +"and unitno         = '" + TradeContext.unitno          + "'"
                    #sqlStr =sqlStr +"and subUnitno      = '" + TradeContext.subUnitno       + "'"
                    sqlStr =sqlStr +"and workDate       = '" + TradeContext.OriEntrustDate  + "'"
                    sqlStr =sqlStr +"and Batchno        = '" + TradeContext.OriPackNo          + "'"
                    sqlStr =sqlStr +"and CORPSERIALNO   = '" + TradeContext.OriTraNo        + "'"
                    sqlStr =sqlStr +"and NOTE1          = '" + TradeContext.TaxOrgCode      + "'"
                    LoggerFunc.tradeInfo(sqlStr )
                    records=DBFunc.UpdateSqlCmt( sqlStr )
                    if( records <0 ):
                        TradeContext.errorCode='A0027'
                        TradeContext.StopAnswer='3'
                        TradeContext.errorMsg='ֹ��ʧ��,���ݿ��쳣'
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='1'
                    TradeContext.errorMsg='ֹ���ɹ�'
                elif Records[0][0]=='1': #ԭ��ˮ����ʧ�ܣ���ֹ���ɹ�
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='1'
                    TradeContext.errorMsg='ֹ���ɹ�'
                elif Records[0][0]=='0': #ԭ��ˮ����ɹ�����ֹ���ɹ�
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='2'
                    TradeContext.errorMsg='ֹ���ɹ�'
                else:
                    TradeContext.errorCode='A0027'
                    TradeContext.StopAnswer='3'
                    TradeContext.errorMsg='ֹ��ʧ��,�����Ѵ���'
        else:
            #��ѯ��������״̬
            sqlStr = "SELECT DEALSTATUS FROM BATCH_ADM WHERE "
            sqlStr =sqlStr +" sysid     = '" + TradeContext.appNo       + "'"
            sqlStr =sqlStr +"and unitno    = '" + TradeContext.unitno      + "'"
            #sqlStr =sqlStr +"and subUnitno = '" + TradeContext.subUnitno   + "'"
            sqlStr =sqlStr +"and workDate  = '" + TradeContext.OriEntrustDate + "'"
            sqlStr =sqlStr +"and Batchno   = '" + TradeContext.OriPackNo      + "'"
            sqlStr =sqlStr +"and note1     = '" + TradeContext.TaxOrgCode  + "'"
            Records = DBFunc.SelectSql( sqlStr )
            LoggerFunc.tradeInfo(sqlStr)
            if( Records == None ):
                LoggerFunc.tradeFatal('�������������쳣:'+DBFunc.sqlErrMsg)
                return AfaFlowControl.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
            elif(len(Records)>0):
                if Records[0][0]=='9': #ԭ������δ����
                    sqlStr = "UPDATE  BATCH_ADM SET DEALSTATUS='1',ERRORCODE='24020',ERRORMSG='��ֹ��' WHERE "
                    sqlStr =sqlStr +" sysid             = '" + TradeContext.appNo           + "'"
                    sqlStr =sqlStr +"and unitno         = '" + TradeContext.unitno          + "'"
                    #sqlStr =sqlStr +"and subUnitno      = '" + TradeContext.subUnitno       + "'"
                    sqlStr =sqlStr +"and workDate       = '" + TradeContext.OriEntrustDate  + "'"
                    sqlStr =sqlStr +"and Batchno        = '" + TradeContext.OriPackNo          + "'"
                    sqlStr =sqlStr +"and NOTE1          = '" + TradeContext.TaxOrgCode      + "'"
                    LoggerFunc.tradeInfo(sqlStr )
                    records=DBFunc.UpdateSqlCmt( sqlStr )
                    if( records <0 ):
                        TradeContext.errorCode='A0027'
                        TradeContext.StopAnswer='3'
                        TradeContext.errorMsg='ֹ��ʧ��,���ݿ��쳣'
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='1'
                    TradeContext.errorMsg='ֹ���ɹ�'
                elif Records[0][0]=='1': #ԭ���δ���ʧ�ܣ���ֹ���ɹ�
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='1'
                    TradeContext.errorMsg='ֹ���ɹ�'
                elif Records[0][0]=='0': #ԭ���δ���ɹ�����ֹ���ɹ�
                    TradeContext.errorCode='0000'
                    TradeContext.StopAnswer='2'
                    TradeContext.errorMsg='ֹ���ɹ�'
                else:
                    TradeContext.errorCode='A0027'
                    TradeContext.StopAnswer='3'
                    TradeContext.errorMsg='ֹ��ʧ��,�����Ѵ���'
        
        #=============��ȡƽ̨��ˮ��====================
        if AfapFunc.GetSerialno( ) == -1 :
            raise AfaFlowControl.flowException( )
        #=============�������ͨѶ������ֹ��Ӧ��====================
        TradeContext.TransCode='2123' #ֹ��Ӧ��
        AfaAfeFunc.CommAfe()
        
        TradeContext.errorCode='0000'
        TradeContext.errorMsg='���׳ɹ�'
        LoggerFunc.tradeInfo('������:')
        LoggerFunc.tradeInfo('��˰����_ֹ��������_ǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
