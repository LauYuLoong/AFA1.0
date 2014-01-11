# -*- coding: gbk -*-
##################################################################
#   ���մ���ƽ̨.��˰���к�������.������Ϣά��
#       opType  0 ��ѯ
#       opType  1 ����
#       opType  2 �޸�
#       opType  3 ɾ��
#=================================================================
#   �����ļ�:   TTPS001_8467.py
#   �޸�ʱ��:   2008-10-23
##################################################################

import TradeContext, AfaLoggerFunc,  AfaFlowControl, AfaDBFunc
#import HostComm,TipsFunc,UtilTools, os,TradeFunc,HostContext

def SubModuleMainFst( ):
    AfaLoggerFunc.tradeInfo('>>>������Ϣά��')
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
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������֧��ϵͳ�к�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[����������к�]:����Ϊ��')
        
        sql="SELECT PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len(records) ==0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', 'δ��������Ϣ' )
        elif( len(records) > 1 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', 'TIPS_LIQUIDATE_ADM�����ô���' )
        else:
            if records[0][7]=='0':
                return AfaFlowControl.ExitThisFlow( 'A0027', 'ҵ����ֹͣ' )
            if records[0][7]=='2':
                return AfaFlowControl.ExitThisFlow( 'A0027', 'ҵ������ͣ' )
            TradeContext.PAYEEBANKNO    = records[0][0]
            TradeContext.TRECODE        = records[0][1]
            TradeContext.TRENAME        = records[0][2]
            TradeContext.PAYEEACCT      = records[0][3]
            TradeContext.PAYEEACCTNAME  = records[0][4]
            TradeContext.PAYBKCODE      = records[0][5]
            TradeContext.PAYBKNAME      = records[0][6]
            TradeContext.LIQUIDATEMODE  = records[0][7]
            TradeContext.BRNO           = records[0][8]
            TradeContext.TELLERNO       = records[0][10]
            
            
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
        
#����
def Insert():
    try:
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������֧��ϵͳ�к�]:����Ϊ��')
        if( TradeContext.existVariable( "TRECODE" ) and len(TradeContext.TRECODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[����������]:����Ϊ��')
        if( TradeContext.existVariable( "TRENAME" ) and len(TradeContext.TRENAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�����������]:����Ϊ��')
        if( TradeContext.existVariable( "PAYEEACCT" ) and len(TradeContext.PAYEEACCT)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������տ��˺�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYEEACCTNAME" ) and len(TradeContext.PAYEEACCTNAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������տ��˻�����]:����Ϊ��')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[����������к�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYBKNAME" ) and len(TradeContext.PAYBKNAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������������]:����Ϊ��')
        if( TradeContext.existVariable( "LIQUIDATEMODE" ) and len(TradeContext.LIQUIDATEMODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[����ģʽ]:����Ϊ��')
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������]:����Ϊ��')
        if( TradeContext.existVariable( "TELLERNO" ) and len(TradeContext.TELLERNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[���׹�Ա]:����Ϊ��')

        sql="SELECT PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len(records) > 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '�Ѵ��ڴ�������Ϣ' )

            
        sql="INSERT INTO  TIPS_LIQUIDATE_ADM(PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO) "
        sql=sql+" VALUES "
        sql=sql+"('"+ TradeContext.PAYEEBANKNO  +"'"
        sql=sql+",'"+ TradeContext.TRECODE      +"'"
        sql=sql+",'"+ TradeContext.TRENAME      +"'"
        sql=sql+",'"+ TradeContext.PAYEEACCT    +"'"
        sql=sql+",'"+ TradeContext.PAYEEACCTNAME+"'"
        sql=sql+",'"+ TradeContext.PAYBKCODE    +"'"
        sql=sql+",'"+ TradeContext.PAYBKNAME    +"'"
        sql=sql+",'"+ TradeContext.LIQUIDATEMODE+"'"
        sql=sql+",'"+ '1'                       +"'"
        sql=sql+",'"+ TradeContext.BRNO         +"'"
        sql=sql+",'"+ TradeContext.TELLERNO     +"'"
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
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������֧��ϵͳ�к�]:����Ϊ��')
        if( TradeContext.existVariable( "TRECODE" ) and len(TradeContext.TRECODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[����������]:����Ϊ��')
        if( TradeContext.existVariable( "TRENAME" ) and len(TradeContext.TRENAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�����������]:����Ϊ��')
        if( TradeContext.existVariable( "PAYEEACCT" ) and len(TradeContext.PAYEEACCT)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������տ��˺�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYEEACCTNAME" ) and len(TradeContext.PAYEEACCTNAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������տ��˻�����]:����Ϊ��')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[����������к�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYBKNAME" ) and len(TradeContext.PAYBKNAME)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������������]:����Ϊ��')
        if( TradeContext.existVariable( "LIQUIDATEMODE" ) and len(TradeContext.LIQUIDATEMODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[����ģʽ]:����Ϊ��')
        if( TradeContext.existVariable( "BRNO" ) and len(TradeContext.BRNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[��������]:����Ϊ��')
        if( TradeContext.existVariable( "TELLERNO" ) and len(TradeContext.TELLERNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[���׹�Ա]:����Ϊ��')
            
        sql="SELECT PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len(records) == 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '�����ڴ�������Ϣ' )

        sql="UPDATE TIPS_LIQUIDATE_ADM SET "
        sql=sql+"TRECODE='"+ TradeContext.TRECODE+"',"
        sql=sql+"TRENAME='"+ TradeContext.TRENAME+"',"
        sql=sql+"PAYEEACCT='"+ TradeContext.PAYEEACCT+"',"
        sql=sql+"PAYEEACCTNAME='"+ TradeContext.PAYEEACCTNAME+"',"
        sql=sql+"LIQUIDATEMODE='"+ TradeContext.LIQUIDATEMODE+"',"
        sql=sql+"BRNO='"+ TradeContext.BRNO+"',"
        sql=sql+"TELLERNO='"+ TradeContext.TELLERNO+"',"
        sql=sql+"PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"',"
        sql=sql+"PAYBKCODE='"+ TradeContext.PAYBKCODE+"' ,"
        sql=sql+"PAYBKNAME='"+ TradeContext.PAYBKNAME+"' "
        sql=sql+"WHERE "
        sql=sql+"(PAYEEBANKNO = '"+ TradeContext.PAYEEBANKNO+"') AND "
        sql=sql+"(PAYBKCODE = '"+ TradeContext.PAYBKCODE+"') "
                
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.UpdateSqlCmt(sql)
                 
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', 'δ����������Ϣ:'+AfaDBFunc.sqlErrMsg )
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
        if( TradeContext.existVariable( "PAYEEBANKNO" ) and len(TradeContext.PAYEEBANKNO)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[�������֧��ϵͳ�к�]:����Ϊ��')
        if( TradeContext.existVariable( "PAYBKCODE" ) and len(TradeContext.PAYBKCODE)<=0):
            return AfaFlowControl.ExitThisFlow( 'A0027', '[����������к�]:����Ϊ��')
            
        sql="SELECT PAYEEBANKNO,TRECODE,TRENAME,PAYEEACCT,PAYEEACCTNAME,PAYBKCODE,PAYBKNAME,LIQUIDATEMODE,STATUS,BRNO,TELLERNO,NOTE1,NOTE2,NOTE3,NOTE4,NOTE5 "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.SelectSql(sql)
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        elif( len(records) == 0 ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '�����ڴ�������Ϣ' )

        sql="DELETE "
        sql=sql+" FROM TIPS_LIQUIDATE_ADM WHERE 1=1 "
        sql=sql+"AND PAYEEBANKNO='"+ TradeContext.PAYEEBANKNO+"'"
        sql=sql+"AND PAYBKCODE='"+ TradeContext.PAYBKCODE+"'"
        AfaLoggerFunc.tradeInfo(sql)
        records = AfaDBFunc.DeleteSqlCmt(sql)
        
        if( records <=0  ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0027', '�޴�������Ϣ:'+AfaDBFunc.sqlErrMsg )
        if( records == None ):
            AfaLoggerFunc.tradeFatal(sql)
            return AfaFlowControl.ExitThisFlow( 'A0002', '���ݿ�����쳣:'+AfaDBFunc.sqlErrMsg )
        return True
    except Exception, e:
        AfaLoggerFunc.tradeInfo(e)
        return AfaFlowControl.ExitThisFlow('9999', '�������쳣'+str(e))
