# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.�����ۿ��ִ����
#=================================================================
#   �����ļ�:   003001_032102.py
#   �޸�ʱ��:   2007-5-28 10:28
##################################################################
import TradeContext, AfaLoggerFunc, AfaAfeFunc,TipsFunc
#UtilTools,TipsFunc,time
import AfaDBFunc,os
from types import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('��˰����_�����ۿ��ִ����_ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:

        #====�ж�Ӧ��״̬=======
        if not TipsFunc.ChkAppStatus( ):
            return False
        #=============��ȡƽ̨��ˮ��====================
        if TipsFunc.GetSerialno( ) == -1 :
            AfaLoggerFunc.tradeInfo('>>>������:��ȡƽ̨��ˮ���쳣' )
            return TipsFunc.ExitThisFlow( 'A0027', '��ȡ��ˮ��ʧ��' )

        #===�ź�����NOTE4�ֶ� 20100412===
        sqlStr = "SELECT TOTALNUM,TOTALAMT,SUCCNUM,SUCCAMT,ERRORCODE,ERRORMSG,PAYBKCODE,DEALSTATUS,PAYBKCODE,note3,note4 FROM TIPS_BATCHADM "
        sqlStr =sqlStr +" WHERE WORKDATE = '" + TradeContext.EntrustDate     + "'"
        sqlStr =sqlStr +" and BATCHNO = '"     + TradeContext.PackNo          + "'"
        sqlStr =sqlStr +" and TAXORGCODE = '"  + TradeContext.TaxOrgCode      + "'"
        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None or Records < 0):
            AfaLoggerFunc.tradeFatal('�������������쳣:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
        if( len(Records)==0 ):
            AfaLoggerFunc.tradeFatal('�޴�����:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '�޴�����' )
        elif(len(Records)>0):
            if not(Records[0][7]=='0' or Records[0][7]=='1'):
                AfaLoggerFunc.tradeFatal('������δ������,���ܷ��ͻ�ִ')
                return TipsFunc.ExitThisFlow( 'A0027', '������δ������,���ܷ��ͻ�ִ' )
            elif(Records[0][7]=='1'):
                AfaLoggerFunc.tradeFatal('�����δ���ʧ��,���ܷ��ͻ�ִ')
                return TipsFunc.ExitThisFlow( 'A0027', '�����δ���ʧ��,���ܷ��ͻ�ִ' )
            else: #�����δ���ɹ�����ȡ��ˮ
                iBatchPage=0
                TradeContext.AllNum      =Records[0][0]
                TradeContext.AllAmt      =Records[0][1]
                TradeContext.SuccNum     =Records[0][2]
                TradeContext.SuccAmt     =Records[0][3]
                TradeContext.Tot_Result    =Records[0][4]
                TradeContext.Tot_AddWord   =Records[0][5]
                TradeContext.PayBkCode     =Records[0][8]
                TradeContext.OrMsgRef      = Records[0][9]

                #===�ź�����NOTE4�ֶ� 20100412===
                TradeContext.OrEntrustDate = Records[0][10]

                AfaLoggerFunc.tradeInfo("payBkCode=" + TradeContext.PayBkCode)
                #��ˮ
                sqlStr = "SELECT CORPSERIALNO,AMOUNT,TAXPAYCODE,WORKDATE,ERRORCODE,ERRORMSG FROM TIPS_BATCHDATA WHERE "
                sqlStr =sqlStr +" workDate = '"         + TradeContext.EntrustDate     + "'"
                sqlStr =sqlStr +"and Batchno = '"       + TradeContext.PackNo          + "'"
                sqlStr =sqlStr +"and TAXORGCODE = '"    + TradeContext.TaxOrgCode      + "'"
                sqlStr =sqlStr +" order by SERIALNO"
                Records = AfaDBFunc.SelectSql( sqlStr )
                AfaLoggerFunc.tradeInfo(sqlStr)
                if( Records == None ):
                    AfaLoggerFunc.tradeFatal('�������������쳣:'+AfaDBFunc.sqlErrMsg)
                    return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
                elif(len(Records)>0):
#                    TradeContext.OriTraNo=[]
#                    TradeContext.TraAmt  =[]
#                    TradeContext.TaxVouNo=[]
#                    TradeContext.TaxDate =[]
#                    TradeContext.Result  =[]
#                    TradeContext.AddWord =[]
#                    for i in range(0, len(Records)):
#                        TradeContext.OriTraNo.append(Records[i][0])
#                        TradeContext.TraAmt  .append(Records[i][1])
#                        TradeContext.TaxVouNo.append(Records[i][2])
#                        TradeContext.TaxDate .append(Records[i][3])
#                        TradeContext.Result  .append(Records[i][4])
#                        TradeContext.AddWord .append(Records[i][5])
                    TradeContext.FilePath = os.environ['AFAP_HOME'] + '/data/batch/tips/2102_' + TradeContext.EntrustDate + TradeContext.PackNo
                    fp = open(TradeContext.FilePath,"w")
                    for i in range(0, len(Records)):
                        fp.write(Records[i][0] + '|')
                        fp.write(Records[i][1] + '|')
                        fp.write(Records[i][2] + '|')
                        fp.write(Records[i][3] + '|')
                        fp.write(Records[i][4] + '|')
                        fp.write(Records[i][5] + '|')
                    fp.close()
                #TradeContext.TransCode='2102'
                #=============�������ͨѶ====================
                AfaAfeFunc.CommAfe()

        #TradeContext.errorCode='0000'
        #TradeContext.errorMsg='���׳ɹ�'
        AfaLoggerFunc.tradeInfo('��˰����_�����ۿ��_ǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
