# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��˰���к�������.�����У��磩����ά��
#       opType  0 ��ѯ
#       opType  1 ����
#       opType  2 �޸�
#       opType  3 ɾ��
#=================================================================
#   �����ļ�:   T3001_8466.py
#   �޸�ʱ��:   2007-10-23
##################################################################

import TradeContext, AfaLoggerFunc,  AfaFlowControl, AfaDBFunc
#, UtilTools,os,TradeFunc,HostContext
#import HostComm,TipsFunc

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('>>>�����У��磩����ά��')
    if TradeContext.opType=='0':
        AfaLoggerFunc.tradeInfo('>>>��ѯ')
        if not Query():
            return False
    elif TradeContext.opType=='1': 
        AfaLoggerFunc.tradeInfo('>>>����')
        if not Insert():
            return False
    elif TradeContext.opType=='2': 
        AfaLoggerFunc.tradeInfo('>>>�޸�')
        if not Update():
            return False
    elif TradeContext.opType=='3': 
        AfaLoggerFunc.tradeInfo('>>>ɾ��')
        if not Delete():
            return False
    else:
        return AfaFlowControl.ExitThisFlow('0001', 'δ����ò�������')    

    TradeContext.errorCode='0000'
    TradeContext.errorMsg='���״���ɹ�'
    return True

#��ѯ
def Query():
    try:
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�����к�]:����Ϊ��')
        sql="SELECT BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records )==0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', 'δ������Ϣ' )
        elif( len( records )>1 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', 'TIPS_BRANCH_ADM�����ô���' )
        else:
            #if records[0][5]=='0':
               # return AfaFlowControl.ExitThisFlow( 'A0027', 'ҵ����ֹͣ' )
          #  if records[0][5]=='2':
           #     return AfaFlowControl.ExitThisFlow( 'A0027', 'ҵ������ͣ' )
            TradeContext.BRNO        = records[0][0]
            TradeContext.PAYBKCODE   = records[0][1]
            TradeContext.BANKNO      = records[0][2]
            TradeContext.BANKACCT    = records[0][3]
            TradeContext.BANKNAME    = records[0][4]
            TradeContext.PAYEEBANKNO = records[0][5]
            TradeContext.STATUS      = records[0][6]
            TradeContext.ACCNO       = records[0][7]
            TradeContext.ACCNAME     = records[0][10]
            
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
#����
def Insert():
    try:
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�����к�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������к�]:����Ϊ��')
        if( TradeContext.existVariable( "STATUS" ) and len(TradeContext.STATUS)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�Ƿ�Ϊ������]:����Ϊ��')
        if( TradeContext.existVariable( "ACCNO" ) and len(TradeContext.ACCNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��˰����ʺ�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������֧��ϵͳ�к�]:����Ϊ��')

        sql="SELECT BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        #sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        #guanbinjie 20090901 ���������к�ΪΨһֵ
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE +"'"
        #�޸����
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records ) > 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '�Ѵ��ڴ���������Ϣ' )

        sql="INSERT INTO  TIPS_BRANCH_ADM(BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE3) "
        sql=sql+" VALUES "
        sql=sql+"('"+ TradeContext.BRNO          +"'"
        sql=sql+",'"+ TradeContext.PAYBKCODE     +"'"
        sql=sql+",'"+ TradeContext.BANKNO        +"'"
        sql=sql+",'"+ TradeContext.BANKACCT      +"'"
        sql=sql+",'"+ TradeContext.BANKNAME      +"'"
        sql=sql+",'"+ TradeContext.PAYEEBANKNO   +"'"
        sql=sql+",'"+ TradeContext.STATUS        +"'"
        sql=sql+",'"+ TradeContext.ACCNO         +"'"
        sql=sql+",'"+ TradeContext.ACCNAME         +"'"
        sql=sql+" ) "              
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.InsertSqlCmt(sql)
        if( records == None or records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))

#�޸�
def Update():
    try:
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�����к�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������к�]:����Ϊ��')
        if( TradeContext.existVariable( "STATUS" ) and len(TradeContext.STATUS)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�Ƿ�Ϊ������]:����Ϊ��')
        if( TradeContext.existVariable( "ACCNO" ) and len(TradeContext.ACCNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������˰���]:����Ϊ��')
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������֧��ϵͳ�к�]:����Ϊ��')

        sql="SELECT BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records ) == 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '�����ڴ���������Ϣ' )

            
        sql="UPDATE TIPS_BRANCH_ADM SET "
        sql=sql+"PAYBKCODE='"+ TradeContext.PAYBKCODE+"',"
        sql=sql+"BANKNO='"+ TradeContext.BANKNO+"',"
        sql=sql+"BANKACCT='"+ TradeContext.BANKACCT+"',"
        sql=sql+"BANKNAME='"+ TradeContext.BANKNAME+"',"
        sql=sql+"PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"',"
        sql=sql+"STATUS='"+ TradeContext.STATUS+"',"
        sql=sql+"ACCNO='"+ TradeContext.ACCNO+"',"
        sql=sql+"NOTE3='"+ TradeContext.ACCNAME+"',"
        sql=sql+"BRNO='"+ TradeContext.BRNO+"' "
        sql=sql+"WHERE "
        sql=sql+"BRNO = '"+ TradeContext.BRNO+"'"
                
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.UpdateSqlCmt(sql)
                 
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', 'δ������Ϣ:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))


#ɾ��
def Delete():
    try:
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�����к�]:����Ϊ��')

        sql="SELECT BRNO,PAYBKCODE,BANKNO,BANKACCT,BANKNAME,PAYEEBANKNO,STATUS,ACCNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len( records ) == 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '�����ڴ���������Ϣ' )

            
        sql="DELETE "
        sql=sql+" FROM TIPS_BRANCH_ADM WHERE 1=1 "
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)>0):
            sql=sql+"AND BRNO='"+ TradeContext.BRNO+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.DeleteSqlCmt(sql)
        if( records == None or records <=0 ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
