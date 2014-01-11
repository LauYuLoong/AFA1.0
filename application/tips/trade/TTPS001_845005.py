# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.TIPS�������ж˽ɿ���ϸ״̬��ѯ
#=================================================================
#   �����ļ�:   TPS001_845005.py
#   �޸�ʱ��:   2008-9-16 16:05
##################################################################
import TradeContext, AfaLoggerFunc
#, UtilTools,TipsFunc
#import AfaDBFunc,datetime,ConfigParser,os
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('��˰����_TIPS�������ж˽ɿ���ϸ״̬��ѯ_ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    
    try:
        #============����ֵ����Ч��У��============
        if( not TradeContext.existVariable( "PackNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[PackNo]ֵ������!' )
        if( not TradeContext.existVariable( "chkDate" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkDate]ֵ������!' )
            
        #��ѯ�Ƿ��ظ���
        AfaLoggerFunc.tradeInfo( '>>>��ѯ�Ƿ��ظ���' )
        sqlStr = "SELECT DEALSTATUS,WORKDATE,PACKNO,PAYBKCODE,ERRORCODE,ERRORMSG,NOTE2 FROM TIPS_STATCHECKADM WHERE "
        sqlStr =sqlStr +"  WORKDATE  = '"       + TradeContext.ChkDate.strip()        + "'"
        sqlStr =sqlStr +"and PACKNO   = '"      + TradeContext.PackNo.strip()         + "'"
        sqlStr =sqlStr +"and PAYBKCODE   = '"   + TradeContext.PayBkCode.strip()      + "'"
        
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('�����������쳣:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '���ݿ�������������쳣' )
        elif(len(Records)>0):
            if Records[0][0]=='2': #�ظ����������ڴ���
                AfaLoggerFunc.tradeInfo( '>>>�ظ����������ڴ���ֱ�ӷ���94052' )
                TradeContext.tradeResponse.append(['errorCode','94052'])
                TradeContext.tradeResponse.append(['errorMsg','���ظ�'])
                return True
            elif Records[0][0]=='0' : #�Ѵ�����ɣ��ɹ�����ʧ�ܣ�ֱ�ӻ�ִ
                #�����˰��ִ����
                AfaLoggerFunc.tradeInfo( '>>>�Ѵ�����ɣ��ɹ�����ʧ�ܣ�ֱ�ӻ�ִ2111' )
                TradeContext.OriChkDate    =Records[0][1]
                TradeContext.OriChkAcctOrd =Records[0][2]
                TradeContext.OriPayBankNo  =Records[0][3]
                TradeContext.OriPayeeBankNo=Records[0][4]
                TradeContext.Result        =Records[0][5]
                TradeContext.AddWord       =Records[0][6]
                subModuleName = 'TTPS001_032111'
                subModuleHandle=__import__( subModuleName )
                AfaLoggerFunc.tradeInfo( 'ִ��['+subModuleName+']ģ��' )
                if not subModuleHandle.SubModuleMainFst( ) :
                    return TipsFunc.flowException( )
                TradeContext.tradeResponse.append(['errorCode','94052'])
                TradeContext.tradeResponse.append(['errorMsg','���Ѵ������'])
                return True
            else: #�ظ��������µǼ�
                AfaLoggerFunc.tradeInfo( '>>>�ظ��������µǼ�' )
                if int(TradeContext.pageSerno.strip())==1:
                    #��δ������ظ����Σ��������δ���ɾ��������
                    sqlStr_d_t = "DELETE FROM  TIPS_STATCHECKDATA WHERE "
                    sqlStr_d_t = sqlStr_d_t +"  workDate  = '"      + TradeContext.ChkDate              + "'"
                    sqlStr_d_t = sqlStr_d_t +" and PACKNO   = '"    + TradeContext.PackNo               + "'"   
                    sqlStr_d_t = sqlStr_d_t +" AND PAYBKCODE   ='"  + TradeContext.payBkCode.strip()  + "'"
                    AfaLoggerFunc.tradeInfo(sqlStr_d_t )
                    if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_t ) <0 ):
                        return TipsFunc.ExitThisFlow( 'A0027', '���ݿ�������������쳣' )
                    sqlStr_d_b = "DELETE FROM  TIPS_STATCHECKADM WHERE "
                    sqlStr_d_b =sqlStr_d_b +" WORKDATE  = '"        + TradeContext.chkDate.strip()     + "'"
                    sqlStr_d_b =sqlStr_d_b +"and PACKNO   = '"     + TradeContext.PackNo.strip()       + "'"
                    sqlStr_d_b =sqlStr_d_b +"and PAYBKCODE     = '" + TradeContext.payBkCode.strip()   + "'"
                    AfaLoggerFunc.tradeInfo(sqlStr_d_b )
                    if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_b ) <0 ):
                        return TipsFunc.ExitThisFlow( 'A0027', '���ݿ�������������쳣' )
                else:
                    if int(TradeContext.pageSerno.strip())!=int(Records[0][6].strip())+1:
                        #ҳ��Ŵ���
                        TradeContext.tradeResponse.append(['errorCode','A0002'])
                        TradeContext.tradeResponse.append(['errorMsg','ҳ��Ŵ���'])
                        return True
    
    AfaLoggerFunc.tradeInfo('��˰����_TIPS�������ж˽ɿ���ϸ״̬��ѯ_ǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )