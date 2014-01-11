# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.��˰���к�������.����TIPS�����ۿ����󣺽�������ϸд���BATCH_ADM,TIPS_BATCHDATA
#=================================================================
#       9 - ��ʼ״̬��������
#       1 - ʧ��
#       2 - �����ۿ���
#       0 - �ۿ�ɹ�
#   �����ļ�:   TTPS001_845003.py
#   �޸�ʱ��:   2008-09-04 10:28
##################################################################
import TradeContext, AfaLoggerFunc, TipsFunc
import AfaDBFunc
#,os,UtilTools
from types import *
from tipsConst import *

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('��˰����_����������_ǰ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
    
        #begin 20101130 ���������� �����տ�������ƣ����ں���Ǽ���ˮ
        TradeContext.note10 = TradeContext.payeeName
        #end
        
        #begin  ���������� �������и�ֵ���������������ԭֵ���Ƕ�ȡ������������
        TradeContext.tmp_projectId     = TradeContext.projectId
        TradeContext.tmp_taxTypeName   = TradeContext.taxTypeName
        TradeContext.tmp_taxStartDate  = TradeContext.taxStartDate
        TradeContext.tmp_taxEndDate    = TradeContext.taxEndDate
        TradeContext.tmp_taxTypeAmt    = TradeContext.taxTypeAmt
        #end
        
        AfaLoggerFunc.tradeInfo('>>>����:' + TradeContext.corpTime + "  " + TradeContext.workDate)
        #=============�ж�Ӧ��״̬====================
        if not TipsFunc.ChkAppStatus( ) :
            return False
        #====��ȡ������Ϣ=======
        if not TipsFunc.ChkLiquidStatus():
            return False

        #============����ֵ����Ч��У��============
        AfaLoggerFunc.tradeInfo('>>>����ֵ����Ч��У��')
        if( not TradeContext.existVariable( "taxOrgCode" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[taxOrgCode]ֵ������!' )
        if( not TradeContext.existVariable( "packNo" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[packNo]ֵ������!' )
        if( not TradeContext.existVariable( "entrustDate" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[entrustDate]ֵ������!' )
        if( not TradeContext.existVariable( "corpTime" ) ):
            return TipsFunc.ExitThisFlow( 'A0001', '[corpTime]ֵ������!' )

        #��������Ƿ����
        AfaLoggerFunc.tradeInfo('>>>��������Ƿ����')
        AfaLoggerFunc.tradeInfo('>>>����:' + TradeContext.corpTime + "  " + TradeContext.workDate)
        if (TradeContext.corpTime!=TradeContext.workDate ):
            TradeContext.tradeResponse.append(['errorCode','24020'])
            TradeContext.tradeResponse.append(['errorMsg','�ѹ��ڣ�����'])
            AfaLoggerFunc.tradeInfo('�ѹ��ڣ��������ϡ����Ĺ�������:'+TradeContext.corpTime+'ϵͳ��������:'+TradeContext.workDate)
            return True
        #��ѯ�Ƿ��ظ�����
        AfaLoggerFunc.tradeInfo('>>>��ѯ�Ƿ��ظ�����')
        sqlStr = "SELECT Dealstatus,errorcode,errormsg FROM TIPS_BATCHADM WHERE "
        sqlStr =sqlStr +" WorkDate  = '" + TradeContext.corpTime + "'"
        sqlStr =sqlStr +"and Batchno   = '" + TradeContext.packNo      + "'"
        sqlStr =sqlStr +"and TAXORGCODE= '" + TradeContext.taxOrgCode  + "'"

        Records = AfaDBFunc.SelectSql( sqlStr )
        AfaLoggerFunc.tradeInfo(sqlStr)
        if( Records == None ):
            AfaLoggerFunc.tradeFatal('�������������쳣:'+AfaDBFunc.sqlErrMsg)
            return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )
        elif(len(Records)>0):
            AfaLoggerFunc.tradeInfo('�����Ѵ��ڡ�����״̬:'+Records[0][0]+'����״̬:'+Records[0][1])
            if (Records[0][0]=='0'): #�ظ������������ѳɹ�
                AfaLoggerFunc.tradeInfo('>>>�ظ���������������ɼ��˴���')
                TradeContext.tradeResponse.append(['dealFlag','0'])
                TradeContext.tradeResponse.append(['errorCode','0000'])
                TradeContext.tradeResponse.append(['errorMsg','���׳ɹ�'])
                return True
            elif (Records[0][0]=='1'): #�ظ�������������ʧ��
                AfaLoggerFunc.tradeInfo('>>>�ظ���������������ɼ��˴���')
                TradeContext.tradeResponse.append(['errorCode',Records[0][1]])
                TradeContext.tradeResponse.append(['errorMsg',Records[0][2]])
                return True
            #elif  ( Records[0][0]=='9'): #��δ����
            #    None
            #    #��Ϊ���µ����Σ����½���
            #    #else:
            #    #    if int(TradeContext.pageSerno.strip())!=int(Records[0][2].strip())+1:
            #    #        #ҳ��Ŵ���
            #    #        TradeContext.tradeResponse.append(['errorCode','A0002'])
            #    #        TradeContext.tradeResponse.append(['errorMsg','ҳ��Ŵ���'])
            #    #        return True
            else:
                AfaLoggerFunc.tradeInfo('>>>�ظ��������������ύ�����ܾ���������')
                TradeContext.tradeResponse.append(['errorCode','94052'])
                TradeContext.tradeResponse.append(['errorMsg','���ظ�'])
                return True
        if int(TradeContext.pageSerno.strip())==1:
            AfaLoggerFunc.tradeInfo('>>>��δ������ظ����Σ��������δ���ɾ��������')
            #��δ������ظ����Σ��������δ���ɾ��������
            sqlStr_d_t = "DELETE FROM  TIPS_BATCHDATA WHERE "
            sqlStr_d_t =sqlStr_d_t +" WORKDATE = '"         + TradeContext.corpTime + "'"
            sqlStr_d_t =sqlStr_d_t +"and BATCHNO = '"       + TradeContext.packNo      + "'"
            sqlStr_d_t =sqlStr_d_t +"and TAXORGCODE = '"    + TradeContext.taxOrgCode  + "'"
            AfaLoggerFunc.tradeInfo(sqlStr_d_t )
            if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_t ) <0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '���ݿ��������ϸ������쳣' )
            sqlStr_d_b = "DELETE FROM TIPS_BATCHADM WHERE "
            sqlStr_d_b =sqlStr_d_b +" workDate  = '" + TradeContext.corpTime + "'"
            sqlStr_d_b =sqlStr_d_b +"and Batchno   = '" + TradeContext.packNo      + "'"
            sqlStr_d_b =sqlStr_d_b +"and TAXORGCODE = '"    + TradeContext.taxOrgCode  + "'"
            AfaLoggerFunc.tradeInfo(sqlStr_d_b )
            if( AfaDBFunc.DeleteSqlCmt( sqlStr_d_b ) <0 ):
                return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣' )

        #�µ����λ�ҳ��������ϸ���
        AfaLoggerFunc.tradeInfo('>>>�µ����λ�ҳ��������ϸ���')
        recNum=int(TradeContext.pageNum)
        AfaLoggerFunc.tradeInfo(str(recNum))
        
        #beging  ����������
        localtion = 0                   #ƫ����
        #end
        
        for i in range( 0, recNum ):
            TradeContext.agentSerialno = ''
            #=============��ȡƽ̨��ˮ��====================
            if TipsFunc.GetSerialno( ) == -1 :
                AfaLoggerFunc.tradeInfo('>>>������:��ȡƽ̨��ˮ���쳣' )
                return TipsFunc.ExitThisFlow( 'A0027', '��ȡ��ˮ��ʧ��' )

            AfaLoggerFunc.tradeInfo('>>>��ȡƽ̨��ˮ�Ž���')
            sql="insert into TIPS_BATCHDATA(WORKDATE,BATCHNO,TAXORGCODE,CORPSERIALNO,SERIALNO,ACCNO,TAXPAYCODE,AMOUNT,"
            sql=sql+"STATUS,ERRORCODE,ERRORMSG,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9,NOTE10)"
            sql=sql+" values"

            #��ʼ������
            sStatus    = '9'                              #����״̬
            sErrorCode = '99090'                          #������
            sErrorMsg  = '��δ����'                       #������Ϣ
            TradeContext.teller         = TIPS_TELLERNO_AUTO #�Զ���Ա
            TradeContext.catrFlag       = '1'             #�ֽ�ת�˱�־
            TradeContext.__agentEigen__ = '0'             #�ӱ��־
            TradeContext.revTranF       = '0'
            TradeContext.tradeType      = '8'             #��������
            TradeContext.errorCode      = '0000'

            if recNum==1:
                TradeContext.corpSerno  = TradeContext.tNo        #��������ˮ��
                TradeContext.accno      = TradeContext.acc        #�����ʺ�
                TradeContext.protocolNo = TradeContext.ptlN       #Э�����
                TradeContext.taxVouNo   = TradeContext.vNo
                TradeContext.taxPayName = TradeContext.tPN
                TradeContext.amount     = TradeContext.amt
                TradeContext.brno       = TradeContext.opBk       #�������

                #====����Ƿ�ǩԼ��=======
                TipsFunc.ChkCustSign()
                AfaLoggerFunc.tradeInfo(TradeContext.errorCode)
                if(TradeContext.errorCode == '24009'):
                    sStatus    = '1'             #����״̬
                    sErrorCode = '24009'         #������
                    sErrorMsg  = '�˻�δǩԼ'      #������Ϣ
                else:

                    AfaLoggerFunc.tradeInfo(TradeContext.BDt)
                    billData = (TradeContext.BDt).split('|')
                    
                    #begin 20100902 ������ע�͵��Ĳ��֣�������ƴ��ֱ�ӽ���afe���
                    #TradeContext.taxTypeNum = billData[9]
                    TradeContext.taxTypeNum = TradeContext.TaxTypeNum
                    #
                    #TradeContext.projectId     = []
                    #TradeContext.taxTypeName   = []
                    #TradeContext.taxStartDate  = []
                    #TradeContext.taxEndDate    = []
                    #TradeContext.taxTypeAmt    = []
                    #j = 1
                    #AfaLoggerFunc.tradeInfo('���ݳ��ȣ�' + str(len(billData[9:])))
                    #while(j < len(billData[9:])):
                    #    TradeContext.projectId.append(billData[j+9])
                    #    TradeContext.taxTypeName.append(billData[j+10])
                    #    TradeContext.taxStartDate.append(billData[j+11])
                    #    TradeContext.taxEndDate.append(billData[j+12])
                    #    TradeContext.taxTypeAmt.append(billData[j+13])
                    #    j = j + 5
                    #    i = i + 1
                    #end
                    
                sql=sql+"('"+TradeContext.corpTime          +"'"
                sql=sql+",'"+TradeContext.packNo            +"'"
                sql=sql+",'"+TradeContext.taxOrgCode        +"'"
                sql=sql+",'"+TradeContext.tNo               +"'"
                sql=sql+",'"+TradeContext.agentSerialno     +"'"
                sql=sql+",'"+TradeContext.acc               +"'"
                sql=sql+",'"+TradeContext.vNo               +"'"
                sql=sql+",'"+TradeContext.amt               +"'"
                sql=sql+",'"+sStatus                        +"'"
                sql=sql+",'"+sErrorCode                     +"'"
                sql=sql+",'"+sErrorMsg                      +"'"
                sql=sql+",'"+TradeContext.taxOrgCode        +"'"
                sql=sql+",'"+TradeContext.payeeBankNo       +"'"
                sql=sql+",'"+TradeContext.payeeOrgCode      +"'"
                sql=sql+",'"+TradeContext.payeeAcct         +"'"
                sql=sql+",'"+TradeContext.payeeName         +"'"
                sql=sql+",'"+TradeContext.payBkCode         +"'"
                sql=sql+",'"+TradeContext.opBk              +"'"
                sql=sql+",'"+TradeContext.ptlN              +"'"
                sql=sql+",'"+TradeContext.hON               +"'"
                sql=sql+",'"+TradeContext.tPN               +"'"
                #sql=sql+",'"+TradeContext.bDt               +"'"




            else:
                TradeContext.corpSerno  = TradeContext.tNo[i]        #��������ˮ��
                TradeContext.accno      = TradeContext.acc[i]        #�����ʺ�
                TradeContext.protocolNo = TradeContext.ptlN[i]       #Э�����
                TradeContext.taxVouNo   = TradeContext.vNo[i]
                TradeContext.taxPayName = TradeContext.tPN[i]
                TradeContext.amount     = TradeContext.amt[i]
                TradeContext.brno       = TradeContext.opBk[i]       #�������

                #====����Ƿ�ǩԼ��=======
                TipsFunc.ChkCustSign()
                AfaLoggerFunc.tradeInfo(TradeContext.errorCode)
                if(TradeContext.errorCode == '24009'):
                    sStatus    = '1'             #����״̬
                    sErrorCode = '24009'         #������
                    sErrorMsg  = '�˻�δǩԼ'    #������Ϣ
                    
                    #begin ����������
                    localtion = localtion + int(TradeContext.TaxTypeNum[i])
                    #end
                else:
                    billData = (TradeContext.BDt[i]).split('|')
                    
                    #begin 20100902 ������ע�͵��Ĳ��֣�������ƴ��ֱ�ӽ���afe���
                    #TradeContext.taxTypeNum = billData[9]
                    TradeContext.taxTypeNum = TradeContext.TaxTypeNum[i]
                    #
                    #TradeContext.projectId     = []
                    #TradeContext.taxTypeName   = []
                    #TradeContext.taxStartDate  = []
                    #TradeContext.taxEndDate    = []
                    #TradeContext.taxTypeAmt    = []
                    #
                    #j = 1
                    #while(j < len(billData[9:])):
                    #    TradeContext.projectId.append(billData[j+9])
                    #    TradeContext.taxTypeName.append(billData[j+10])
                    #    TradeContext.taxStartDate.append(billData[j+11])
                    #    TradeContext.taxEndDate.append(billData[j+12])
                    #    TradeContext.taxTypeAmt.append(billData[j+13])
                    #    j=j+ 5
                    #end
                    
                    #begin  ����������
                    TradeContext.projectId     = TradeContext.tmp_projectId[localtion:localtion+int(TradeContext.taxTypeNum)]
                    TradeContext.taxTypeName   = TradeContext.tmp_taxTypeName[localtion:localtion+int(TradeContext.taxTypeNum)]
                    TradeContext.taxStartDate  = TradeContext.tmp_taxStartDate[localtion:localtion+int(TradeContext.taxTypeNum)]
                    TradeContext.taxEndDate    = TradeContext.tmp_taxEndDate[localtion:localtion+int(TradeContext.taxTypeNum)]
                    TradeContext.taxTypeAmt    = TradeContext.tmp_taxTypeAmt[localtion:localtion+int(TradeContext.taxTypeNum)]
                    #AfaLoggerFunc.tradeInfo( "��ǰƫ�ƣ�" + str(localtion) )
                    #AfaLoggerFunc.tradeInfo( "��ǰ˰��������" + TradeContext.taxTypeNum )
                    #AfaLoggerFunc.tradeInfo( TradeContext.projectId)
                    #AfaLoggerFunc.tradeInfo( TradeContext.tmp_projectId )
                    
                    localtion = localtion + int(TradeContext.taxTypeNum)
                    #end


                sql=sql+"('"+TradeContext.corpTime       +"'"
                sql=sql+",'"+TradeContext.packNo            +"'"
                sql=sql+",'"+TradeContext.taxOrgCode        +"'"
                #AfaLoggerFunc.tradeInfo( TradeContext.tNo )
                sql=sql+",'"+TradeContext.tNo[i]            +"'"
                sql=sql+",'"+TradeContext.agentSerialno     +"'"
                sql=sql+",'"+TradeContext.acc[i]            +"'"
                sql=sql+",'"+TradeContext.vNo[i]            +"'"
                sql=sql+",'"+TradeContext.amt[i]            +"'"
                sql=sql+",'"+sStatus                        +"'"
                sql=sql+",'"+sErrorCode                     +"'"
                sql=sql+",'"+sErrorMsg                      +"'"
                sql=sql+",'"+TradeContext.taxOrgCode        +"'"
                sql=sql+",'"+TradeContext.payeeBankNo       +"'"
                sql=sql+",'"+TradeContext.payeeOrgCode      +"'"
                sql=sql+",'"+TradeContext.payeeAcct         +"'"
                sql=sql+",'"+TradeContext.payeeName         +"'"
                sql=sql+",'"+TradeContext.payBkCode         +"'"
                sql=sql+",'"+TradeContext.opBk[i]           +"'"
                sql=sql+",'"+TradeContext.ptlN[i]           +"'"
                sql=sql+",'"+TradeContext.hON[i]            +"'"
                sql=sql+",'"+TradeContext.tPN[i]            +"'"
                #sql=sql+",'"+TradeContext.bDt[i]            +"'"
            sql=sql+")"
            AfaLoggerFunc.tradeInfo(sql)
            if( AfaDBFunc.InsertSqlCmt(sql) == -1 ):
                AfaLoggerFunc.tradeFatal(sql)
                return TipsFunc.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            AfaLoggerFunc.tradeInfo('д��һ��������ϸ')

            AfaLoggerFunc.tradeInfo('errorCode = ' + TradeContext.errorCode)

            #guanbj 20091110 �˻�δǩԼ�򲻵Ǽ�����ˮ��
            if TradeContext.errorCode == '0000':
                #====��ѯ�տ��ʺ�=======  20090917 wqs
                if not TipsFunc.SelectAcc():
                    return TipsFunc.ExitThisFlow( 'A0027', '��ѯ�տ��˺�ʧ��' )

                #=============������ˮ��====================
                if not TipsFunc.InsertDtl( ):
                    return TipsFunc.ExitThisFlow( 'A0027', '������ˮ��ʧ��' )

        if TradeContext.nextFlag=='0':

            #���������д��
            sqlStr1 = "insert into TIPS_BATCHADM(WORKDATE,WORKTIME,BATCHNO,TAXORGCODE,DEALSTATUS,ERRORCODE,ERRORMSG,PAYEEBANKNO,PAYEEACCT,PAYEENAME"
            sqlStr1 = sqlStr1 + ",PAYBKCODE,RETURNTERM,TOTALNUM,TOTALAMT,SUCCNUM,SUCCAMT,"

            #===�ź� ����NOTE4�ֶ� ��������������е�ί�������ֶ� START 20100412===
            sqlStr1 = sqlStr1 + "NOTE1,NOTE3,"
            sqlStr1 = sqlStr1 + "NOTE4)"
            #===�ź� ����NOTE4�ֶ� ��������������е�ί�������ֶ� END  ===

            sqlStr1 = sqlStr1 + " values"
            sqlStr1 = sqlStr1 + "('"+TradeContext.corpTime          +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.workTime          +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.packNo            +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.taxOrgCode        +"'"
            sqlStr1 = sqlStr1 + ",'"+'9'                            +"'"
            sqlStr1 = sqlStr1 + ",'"+'99090'                        +"'"
            sqlStr1 = sqlStr1 + ",'"+'��δ����'                     +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.payeeBankNo       +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.payeeAcct         +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.payeeName         +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.payBkCode         +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.returnTerm        +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.allNum            +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.allAmt            +"'"
            sqlStr1 = sqlStr1 + ",'"+'0'                            +"'"
            sqlStr1 = sqlStr1 + ",'"+'0.00'                            +"'"
            sqlStr1 = sqlStr1 + ",'"+TradeContext.pageSerno       +"'"  #ҳ��ţ�AFE��AFA�������ݰ���С�����ƣ�������֣���δ��ݣ�
            sqlStr1 = sqlStr1 + ",'"+TradeContext.MsgRef          +"'"  #���Ĳο���

            #===�ź� ����NOTE4�ֶ� ��������������е�ί�������ֶ�  START ===
            sqlStr1 = sqlStr1 + ",'"+TradeContext.entrustDate     +"'"  #ί������
            #===�ź� ����NOTE4�ֶ� ��������������е�ί�������ֶ� END  ===

            sqlStr1 = sqlStr1 + ")"
            AfaLoggerFunc.tradeInfo(sqlStr1)
            if( AfaDBFunc.InsertSqlCmt(sqlStr1) == -1 ):
                AfaLoggerFunc.tradeFatal(sqlStr1)
                return TipsFunc.ExitThisFlow( 'A0027', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
            #�������ݼ��
            AfaLoggerFunc.tradeInfo('>>>�������ݼ��')
            sqlStr_dt = "select count(*),sum(cast(amount as decimal(17,2))) FROM  TIPS_BATCHDATA WHERE "
            sqlStr_dt =sqlStr_dt +" workDate = '" + TradeContext.corpTime + "'"
            sqlStr_dt =sqlStr_dt +"and Batchno = '" + TradeContext.packNo      + "'"
            sqlStr_dt =sqlStr_dt +"and TAXORGCODE = '" + TradeContext.taxOrgCode  + "'"
            AfaLoggerFunc.tradeInfo(sqlStr_dt )
            records_dt = AfaDBFunc.SelectSql( sqlStr_dt )
            if records_dt == None :
                return TipsFunc.ExitThisFlow( 'A0027', '���ݿ���������������쳣')
            if long(TradeContext.allNum)!=long(records_dt[0][0]):
                AfaLoggerFunc.tradeInfo('��ϸ�ͻ���У�鲻��;ʵ����ϸ���ܱ�����'+str(records_dt[0][0])+'  �ܱ�����'+TradeContext.allNum)
                return TipsFunc.ExitThisFlow( '24020', '��ϸ�ͻ���У�鲻��' )
            if float(TradeContext.allAmt)!=float(records_dt[0][1]):
                AfaLoggerFunc.tradeInfo('��ϸ�ͻ���У�鲻��;ʵ����ϸ���ܽ�'+str(records_dt[0][1])+'  �ܽ�'+TradeContext.allAmt)
                return TipsFunc.ExitThisFlow( '24020', '��ϸ�ͻ���У�鲻��' )
        TradeContext.tradeResponse.append(['dealFlag','1'])
        TradeContext.tradeResponse.append(['errorCode','0000'])
        TradeContext.tradeResponse.append(['errorMsg','���׳ɹ�'])

        AfaLoggerFunc.tradeInfo('��˰����_����������_ǰ�������[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
        return True
    except Exception, e:
        TipsFunc.exitMainFlow(str(e))
