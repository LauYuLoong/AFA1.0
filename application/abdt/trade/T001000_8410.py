# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ������������ҵ
#===============================================================================
#   �����ļ�:   T001000_8410.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AbdtFunc
from types import *


#=====================����������ҵ==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********����������ҵ(8410)��ʼ**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��



    #�жϵ�λЭ���Ƿ���Ч
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False


    #�ж����������Ƿ��Ѵ���
    if (  not ChkBatchInfo( ) ):
        return False


    #�޸����μ�¼Ϊ����״̬
    if ( UpdateBatchInfo() < 0 ):
        return False


    #�ƶ������ļ�������Ŀ¼��
    try:
    
        #begin 20100105 ������ �޸� �ļ��������������ţ�TradeContext.NOTE2��
        sFileName = os.environ['AFAP_HOME'] + '/data/batch/in/'   + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.NOTE2 + "_" + TradeContext.TranDate
        dFileName = os.environ['AFAP_HOME'] + '/data/batch/dust/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.NOTE2 + "_" + TradeContext.TranDate + TradeContext.TranTime
        #end
        
        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            AfaLoggerFunc.tradeInfo('>>>�������������ļ�����')

            cp_cmd_str="mv " + sFileName + " " + dFileName
            os.system(cp_cmd_str)

        else:
            AfaLoggerFunc.tradeInfo('>>>�������������ļ�������,���ѯԭ��')
            return ExitSubTrade( '9999', '�������������ļ�������(ת��),���ѯԭ��' )


    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�������������ļ������쳣(ת��)' )


    AfaLoggerFunc.tradeInfo('**********����������ҵ(8410)����**********')

    
    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True



#�ж����������Ƿ��Ѵ���
def ChkBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>�ж����������Ƿ��Ѵ���')

    try:
    
        #begin 20100105 ������  �޸�   ��ѯ��ʱ���NOTE2Ҳ�����
        #sql = "SELECT BATCHNO,STATUS,NOTE5,USERNO FROM ABDT_BATCHINFO WHERE "
        sql = "SELECT BATCHNO,STATUS,NOTE5,USERNO,NOTE2 FROM ABDT_BATCHINFO WHERE "
        #end
        
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO    + "'" + " AND "        #ҵ����
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO   + "'" + " AND "        #��λ���
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO   + "'" + " AND "        #��������
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO     + "'" + " AND "        #��������
        sql = sql + "INDATE="   + "'" + TradeContext.I1WORKDATE + "'" + " AND "        #ί������
        sql = sql + "BATCHNO="  + "'" + TradeContext.I1BATCHNO  + "'"                  #ί�к�

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql( sql )
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ������Ϣ���쳣' )

        if ( len(records) == 0 ):
                return ExitSubTrade( '9000', 'û�иõ�λ����������Ϣ,���ܳ���' )
                
        #begin ������ ����
        TradeContext.NOTE2 = records[0][4]                #NOTE2(�������)
        #end

        if ( str(records[0][1]) == "40" ):
            return ExitSubTrade('9000', '�õ�λ�����������Ѿ�������:['+ str(records[0][2]) +']')

        elif ( str(records[0][1]) == "88" ):
            return ExitSubTrade('9000', '�õ�λ�����������ļ��Ѿ��������,���ܳ���')

        elif ( str(records[0][1]) == "10" ):
            if ( str(records[0][3]) != TradeContext.I1USID ):
                return ExitSubTrade('9000', 'ֻ�������Ա���ܳ���')

            AfaLoggerFunc.tradeInfo('>>>�õ�λ�����������ļ�Ϊ����״̬,���Գ���')
            return True

        else:
            return ExitSubTrade( '9000', '�õ�λ���������ļ��Ѿ����ύ,���ܳ���' )
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�ж����������Ƿ��Ѵ���,���ݿ��쳣' )




#�޸����μ�¼Ϊ����״̬
def UpdateBatchInfo( ):


    AfaLoggerFunc.tradeInfo('>>>�޸����μ�¼Ϊ����״̬')


    try:
        sql = ""
        sql = "UPDATE ABDT_BATCHINFO SET "
        sql = sql + "STATUS='" + "40"       + "',"                                                #״̬(����)
        sql = sql + "NOTE5='"  + "�ֹ�����" + "'"                                                 #����ԭ��

        sql = sql + " WHERE "

        sql = sql + "APPNO="   + "'" + TradeContext.I1APPNO    + "'" + " AND "                    #ҵ�����
        sql = sql + "BUSINO="  + "'" + TradeContext.I1BUSINO   + "'" + " AND "                    #��λ����
        sql = sql + "ZONENO="  + "'" + TradeContext.I1ZONENO   + "'" + " AND "                    #��������
        sql = sql + "BRNO="    + "'" + TradeContext.I1SBNO     + "'" + " AND "                    #��������
        sql = sql + "BATCHNO=" + "'" + TradeContext.I1BATCHNO  + "'" + " AND "                    #ί�к�
        sql = sql + "INDATE="  + "'" + TradeContext.I1WORKDATE + "'"                              #ί������
 
 
        AfaLoggerFunc.tradeInfo( sql )


        result = AfaDBFunc.UpdateSqlCmt( sql )
        if (result <= 0):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '������������ʧ��' )


        AfaLoggerFunc.tradeInfo(">>>�ܹ��޸�[" + str(result) + "]����¼")

        return True
        
    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '������������ʧ��,���ݿ��쳣' )


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
        
