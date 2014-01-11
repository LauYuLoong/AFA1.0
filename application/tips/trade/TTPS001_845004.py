# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.TIPS������ϸ����
#=================================================================
#      9  ��ʼ
#      2  ������
#      3  �������������
#      4  ���Ķ������
#      0  ����ɹ�
#      1  ����ʧ��
#   �����ļ�:   TPS001_845004.py
#   �޸�ʱ��:   2008-12-18 9:41
##################################################################
import TradeContext, AfaLoggerFunc, TipsFunc
import AfaDBFunc
#,datetime,ConfigParser,os,UtilTools,
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('��˰����_TIPS������ϸ����_ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        #============����ֵ����Ч��У��============
        if( not TradeContext.existVariable( "chkAcctOrd" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkAcctOrd]ֵ������!' )
        if( not TradeContext.existVariable( "chkDate" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[chkDate]ֵ������!' )
        
        #====�ж�Ӧ��״̬=======
        if not TipsFunc.ChkAppStatus():
            return False
                   
        #��ѯ�Ƿ��ظ�����
        AfaLoggerFunc.tradeInfo( '>>>��ѯ�Ƿ��ظ�����' )
        sqlStr = "SELECT DEALSTATUS,WORKDATE,BATCHNO,PAYBKCODE,PAYEEBANKNO,ERRORCODE,ERRORMSG,NOTE2 FROM TIPS_CHECKADM WHERE "
        sqlStr =sqlStr +"  WORKDATE  = '"       + TradeContext.chkDate.strip()         + "'"
        sqlStr =sqlStr +"and BATCHNO   = '"     + TradeContext.chkAcctOrd.strip()      + "'"
        sqlStr =sqlStr +"and PAYEEBANKNO   = '" + TradeContext.payeeBankNo.strip()      + "'"
        sqlStr =sqlStr +"and PAYBKCODE   = '"   + TradeContext.payBkCode.strip()      + "'"
        sqlStr =sqlStr +"and NOTE3   = '"   + TradeContext.CurPackNo.strip()      + "'"
        
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('�������������쳣:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
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
                TradeContext.tradeResponse.append(['errorMsg','�����Ѵ������'])
                return True
            else: #�ظ��������¶���
                AfaLoggerFunc.tradeInfo( '>>>�ظ��������¶���' )
                if int(TradeContext.pageSerno.strip())==1:
                    #��δ������ظ����Σ��������δ���ɾ��������
                    sqlStr_d_t = "DELETE FROM  TIPS_CHECKDATA WHERE "
                    sqlStr_d_t = sqlStr_d_t +"  workDate  = '"      + TradeContext.chkDate              + "'"
                    sqlStr_d_t = sqlStr_d_t +" and Batchno   = '"   + TradeContext.chkAcctOrd           + "'"
                    sqlStr_d_t = sqlStr_d_t +" AND PAYEEBANKNO ='"  + TradeContext.payeeBankNo.strip()    + "'"   
                    sqlStr_d_t = sqlStr_d_t +" AND PAYBKCODE   ='"  + TradeContext.payBkCode.strip()  + "'"
                    sqlStr_d_t = sqlStr_d_t +" AND NOTE3   = '"     + TradeContext.CurPackNo.strip()  + "'"
                    AfaLoggerFunc.tradeInfo(sqlStr_d_t )
                    if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_t ) <0 ):
                        return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
                    sqlStr_d_b = "DELETE FROM  TIPS_CHECKADM WHERE "
                    sqlStr_d_b =sqlStr_d_b +" WORKDATE  = '"        + TradeContext.chkDate.strip()     + "'"
                    sqlStr_d_b =sqlStr_d_b +"and BATCHNO   = '"     + TradeContext.chkAcctOrd.strip()  + "'"
                    sqlStr_d_b =sqlStr_d_b +"and PAYEEBANKNO   = '" + TradeContext.payeeBankNo.strip() + "'"
                    sqlStr_d_b =sqlStr_d_b +"and PAYBKCODE     = '" + TradeContext.payBkCode.strip()   + "'"
                    sqlStr_d_b =sqlStr_d_b +"and NOTE3     = '"     + TradeContext.CurPackNo.strip()   + "'"
                    AfaLoggerFunc.tradeInfo(sqlStr_d_b )
                    if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_b ) <0 ):
                        return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
                else:
                    if int(TradeContext.pageSerno.strip())!=int(Records[0][7].strip())+1:
                        #ҳ��Ŵ���
                        TradeContext.tradeResponse.append(['errorCode','A0002'])
                        TradeContext.tradeResponse.append(['errorMsg','ҳ��Ŵ���'])
                        return True
            
        #�µ����Σ�������ϸ���
        AfaLoggerFunc.tradeInfo( '>>>�µ����Σ�������ϸ���' )
        recNum=int(TradeContext.pageNum)
        AfaLoggerFunc.tradeInfo(str(recNum))
        for i in range( 0, recNum ):
            sql="insert into TIPS_CHECKDATA(WORKDATE,BATCHNO,CORPSERIALNO,PAYEEBANKNO,PAYBKCODE,TAXVOUNO,ACCNO,AMOUNT,"
            sql=sql+"STATUS,NOTE3)"
            sql=sql+" values"
            if recNum==1:
                sql=sql+"('"+TradeContext.chkDate           +"'"
                sql=sql+",'"+TradeContext.chkAcctOrd            +"'"
                sql=sql+",'"+TradeContext.cNo            +"'"
                sql=sql+",'"+TradeContext.payeeBankNo       +"'"
                sql=sql+",'"+TradeContext.payBkCode         +"'"
                sql=sql+",'"+TradeContext.vNo          +"'"
                sql=sql+",'"+TradeContext.acc           +"'"
                sql=sql+",'"+TradeContext.amt            +"'"
                sql=sql+",'"+'9'                            +"'"
                sql=sql+",'"+TradeContext.CurPackNo         +"'"
            else:
                sql=sql+"('"+TradeContext.chkDate       +"'"
                sql=sql+",'"+TradeContext.chkAcctOrd            +"'"
                sql=sql+",'"+TradeContext.cNo[i]            +"'"
                sql=sql+",'"+TradeContext.payeeBankNo       +"'"
                sql=sql+",'"+TradeContext.payBkCode         +"'"
                sql=sql+",'"+TradeContext.vNo[i]          +"'"
                sql=sql+",'"+TradeContext.acc[i]           +"'"
                sql=sql+",'"+TradeContext.amt[i]            +"'"
                sql=sql+",'"+'9'                            +"'"
                sql=sql+",'"+TradeContext.CurPackNo         +"'"
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
                raise TipsFunc.flowException( ) 
        #���������д��    
        if (len(Records)>0 and Records[0][0]>0  and int(TradeContext.pageSerno.strip())!=1):
            #������������
            sqlStr1 = "UPDATE TIPS_CHECKADM SET NOTE2=char(bigint(NOTE2)+1) WHERE "
            sqlStr1 =sqlStr1 +" WORKDATE  = '"      + TradeContext.chkDate.strip()         + "'"
            sqlStr1 =sqlStr1 +"and BATCHNO   = '"   + TradeContext.chkAcctOrd.strip()      + "'"
            sqlStr1 =sqlStr1 +"and PAYEEBANKNO = '" + TradeContext.payeeBankNo.strip()     + "'"
            sqlStr1 =sqlStr1 +"and PAYBKCODE   = '" + TradeContext.payBkCode.strip()       + "'"
            sqlStr1 =sqlStr1 +"and NOTE3   = '" + TradeContext.CurPackNo.strip()       + "'"
            AfaLoggerFunc.tradeInfo(sqlStr1 )
            records1=AfaDBFunc.UpdateSqlCmt( sqlStr1 )
            if( records1 <0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
        else:    
            sqlStr1="insert into TIPS_CHECKADM(WORKDATE,WORKTIME,BATCHNO,PAYEEBANKNO,PAYBKCODE,CHKACCTTYPE,DEALSTATUS,TOTALNUM,TOTALAMT,SUCCNUM,SUCCAMT,"
            sqlStr1=sqlStr1+"NOTE1,NOTE2,NOTE3)"
            sqlStr1=sqlStr1+" values"
            sqlStr1=sqlStr1+"('"+TradeContext.chkDate           +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.workTime          +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.chkAcctOrd        +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.payeeBankNo       +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.payBkCode         +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.chkAcctType       +"'"
            sqlStr1=sqlStr1+",'"+'9'                            +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.allNum            +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.allAmt            +"'"
            sqlStr1=sqlStr1+",'0'"
            sqlStr1=sqlStr1+",'0'"
            sqlStr1=sqlStr1+",'"+TradeContext.priorChkAcctOrd   +"'"
            sqlStr1=sqlStr1+",'"+TradeContext.pageSerno         +"'"  #ҳ��ţ�AFE��AFA�������ݰ���С�����ƣ�������֣���δ��ݣ�
            sqlStr1=sqlStr1+",'"+TradeContext.CurPackNo         +"'"  #����ţ�TIPS�������ݰ���С�����ƣ�������֣���δ��ݣ�
            sqlStr1=sqlStr1+")"
            AfaLoggerFunc.tradeInfo(sqlStr1)
            if( AfaDBFunc.InsertSqlCmt(sqlStr1) == -1 ):
                AfaLoggerFunc.tradeFatal(sqlStr1)
                return TipsFunc.ExitThisFlow( 'A0027', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','���׳ɹ�'])
        
        #20100113  �ر��  ����  �ж�CHECKDATA�Ǽǲ��м�¼�����뱨���н������Ƿ����,����������������һ�����˲���
        sqlstr = "select count(*) from TIPS_CHECKDATA where "
        sqlstr = sqlstr + ""
        sqlstr = sqlstr +" WORKDATE  = '"        + TradeContext.chkDate.strip()     + "'"
        sqlstr = sqlstr +"and BATCHNO   = '"     + TradeContext.chkAcctOrd.strip()  + "'"
        sqlstr = sqlstr +"and PAYEEBANKNO   = '" + TradeContext.payeeBankNo.strip() + "'"
        sqlstr = sqlstr +"and PAYBKCODE     = '" + TradeContext.payBkCode.strip()   + "'"
        AfaLoggerFunc.tradeInfo(sqlstr)
        records = AfaDBFunc.SelectSql(sqlstr)
        if records == None:
            AfaLoggerFunc.tradeFatal(sqlstr)
            return TipsFunc.ExitThisFlow( 'A0027','���ݿ�����쳣:' + AfaDBFunc.sqlErrMsg)
        else:
            AfaLoggerFunc.tradeInfo(">>>allNum=[" + TradeContext.allNum + "],COUNT=[" + str(records[0][0]) + "]")
            #���TIPS_CHECKDATA��¼������allNum���,�����������һ��������
            if (int(TradeContext.allNum) == records[0][0]):
                TradeContext.tradeResponse.append(['nextStep','1'])  #�������̱�ʶ:1-���������һ����;2-��ֹ������һ����
                AfaLoggerFunc.tradeDebug(">>>���а����ݵǼǽ���,������һ��������")
            else:
                TradeContext.tradeResponse.append(['nextStep','2'])  #�������̱�ʶ:1-���������һ����;2-��ֹ������һ����
                AfaLoggerFunc.tradeDebug(">>>������δ�Ǽǽ���,��������һ��������")
        #20100113  �ر��  �޸Ľ���

        AfaLoggerFunc.tradeInfo('��˰����_TIPS������ϸ����_ǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
        
