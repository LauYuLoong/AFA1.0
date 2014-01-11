# -*- coding: gbk -*-
################################################################################
#   ���մ���.��Ա����ģ��
#===============================================================================
#   ģ���ļ�:   003102.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaFunc,AfaFlowControl,AfaDBFunc,os
from types import *

def main( ):

    AfaLoggerFunc.tradeInfo('******���մ���.ͨ������ģ��[' + TradeContext.TemplateCode + ']����******' )

    try:

        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]

        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================�ж�Ӧ��ϵͳ״̬==================================
        #if not AfaFunc.ChkSysStatus( ) :
        #    raise AfaFlowControl.flowException( )
                
        #=====================У�鹫���ڵ����Ч��==============================
        if( not TradeContext.existVariable( "statType" ) ):
            raise AfaFlowControl.flowException( 'A0001', '��������[statType]ֵ������,���ܽ�������' )

        if( not TradeContext.existVariable( "TransType" ) ):
            raise AfaFlowControl.flowException( 'A0001', '��������[TransType]ֵ������,���ܽ�������' )

        AfaLoggerFunc.tradeInfo( '>>>statType  = ' + TradeContext.statType )
        AfaLoggerFunc.tradeInfo( '>>>TransType = ' + TradeContext.TransType)

        #=====================���ʲ���==========================================
        if not StatAccountInfo( TradeContext.statType ) :
            raise AfaFlowControl.flowException( )

        #=====================�Զ����==========================================
        TradeContext.tradeResponse.append( ['errorCode',     '0000'] )
        TradeContext.tradeResponse.append( ['errorMsg',      '���׳ɹ�'] )

        AfaFunc.autoPackData()

        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo( '******���մ���.ͨ������ģ��[' + TradeContext.TemplateCode + ']�˳�******' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )



#=======================����ͳ��������Ϣ===========================
def StatAccountInfo( statType='0' ):

    AfaLoggerFunc.tradeInfo( '>>>����ͳ��������Ϣ' )

    tableName="AFA_MAINTRANSDTL"

    #�ж���������(1-���������� 2-����Ա����)
    if( int( statType )<1 and int( statType )>2 ):
        return AfaFlowControl.ExitThisFlow( 'A0019', '�Ƿ�����������' )

    #=====================����ֵ����Ч��У��====================================
    if( not TradeContext.existVariable( "tradeDate" ) and len(TradeContext.tradeDate)==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[tradeDate]ֵ������,���ܽ�������' )

    if( not TradeContext.existVariable( "zoneno" ) and len(TradeContext.zoneno)==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '������[zoneno]ֵ������,���ܽ�������' )

    if( not TradeContext.existVariable( "brno" ) and len(TradeContext.brno)==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�����[brno]ֵ������,���ܽ�������' )


    #=====================�����������==========================================
    accSqlStr  = " AND WORKDATE='" + TradeContext.tradeDate + "'"

    if(int( statType )==1):                                 #���������ѯ
        accSqlStr = accSqlStr   + " AND ZONENO='"   + TradeContext.zoneno  + "'"
        accSqlStr = accSqlStr   + " AND BRNO='"     + TradeContext.brno    + "'"

    else:                                                   #���ݹ�Ա��ѯ
        if( not TradeContext.existVariable( "tellerno" ) and len(TradeContext.tellerno)==0 ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������!' )

        accSqlStr  = accSqlStr  + " AND ZONENO='"   + TradeContext.zoneno   + "'"
        accSqlStr  = accSqlStr  + " AND BRNO='"     + TradeContext.brno     + "'"
        accSqlStr  = accSqlStr  + " AND TELLERNO='" + TradeContext.tellerno + "'"



    #��ѯϵͳ��Ϣ
    sqlStr = "SELECT SYSID,SYSCNAME,SYSENAME FROM AFA_SYSTEM WHERE SUBSTR(SYSID,1,3)='AG2'"

    records = AfaDBFunc.SelectSql( sqlStr )

    AfaLoggerFunc.tradeInfo( sqlStr )

    if( records == None ):
        return AfaFlowControl.ExitThisFlow( 'A0027', 'ϵͳ������쳣:'+AfaDBFunc.sqlErrMsg )

    elif( len( records )==0 ):
        return AfaFlowControl.ExitThisFlow( 'A0028', '�õ���û���κ�ϵͳ��Ϣ,��������' )


#    TradeContext.sysId              =[]             #ϵͳ��ʶ
#    TradeContext.agentFlag          =[]             #ҵ��ʽ
#    TradeContext.unitno             =[]             #�̻���ʶ
#    TradeContext.subUnitno          =[]             #���̻���ʶ
#    TradeContext.tradeNums          =[]             #���ױ���
#    TradeContext.tradeAmt           =[]             #���׽��
#    TradeContext.tradeNums_acc      =[]             #���ױ���(ת��)
#    TradeContext.tradeAmt_acc       =[]             #���׽��(ת��)
#    TradeContext.tradeNumsOfFail    =[]             #ʧ�ܱ���
#    TradeContext.tradeNumsOfObnormal=[]             #�쳣����
    queryCount=0


    #����records�е�����None����
    records=AfaUtilTools.ListFilterNone( records )


    AfaLoggerFunc.tradeInfo( '>>>��¼��=' + str(len(records)) )

   
    if ( TradeContext.TransType != '0' ):
        MxFileName = os.environ['AFAP_HOME'] + '/tmp/MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'

        AfaLoggerFunc.tradeInfo('>>>�����ļ�:['+MxFileName+']')

        if (os.path.exists(MxFileName) and os.path.isfile(MxFileName)):
            #�ļ�����,��ɾ��-�ٴ���
            os.system("rm " + MxFileName)

        #������ϸ�ļ�
        sfp = open(MxFileName, "w")

        
    for i in range( 0, len( records ) ):

        #########################################################################################
        AfaLoggerFunc.tradeInfo( '>>>�ɹ�ͳ��-�ֽ�::' )

        sqlStr = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE REVTRANF='0' AND SYSID='" + str(records[i][0]).strip() +  "' AND ACCTYPE='000' AND BANKSTATUS='0' AND CORPSTATUS='0'"
        sqlStr = sqlStr + accSqlStr
        
        AfaLoggerFunc.tradeInfo( sqlStr )

        accRecordsSucc = AfaDBFunc.SelectSql( sqlStr )

        if ( accRecordsSucc == None ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '��ˮ��������쳣:'+AfaDBFunc.sqlErrMsg )


        #########################################################################################
        AfaLoggerFunc.tradeInfo( '>>>�ɹ�ͳ��-ת��::' )

        sqlStr = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE REVTRANF='0' AND SYSID='" + str(records[i][0]).strip() +  "' AND ACCTYPE<>'000' AND BANKSTATUS='0' AND CORPSTATUS='0'"
        sqlStr = sqlStr + accSqlStr

        AfaLoggerFunc.tradeInfo( sqlStr )

        accRecordsSucc_acc = AfaDBFunc.SelectSql( sqlStr )

        if( accRecordsSucc_acc == None ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '��ˮ��������쳣:'+AfaDBFunc.sqlErrMsg )


        #########################################################################################
        AfaLoggerFunc.tradeInfo( '>>>ʧ��ͳ��::' )
        sqlStr = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE REVTRANF='0' AND SYSID='" + str(records[i][0]).strip() +  "' AND ((AGENTFLAG='01' AND BANKSTATUS='1') OR (AGENTFLAG='02' AND CORPSTATUS='1'))"
        sqlStr = sqlStr + accSqlStr

        accRecordsFail = AfaDBFunc.SelectSql( sqlStr )

        AfaLoggerFunc.tradeInfo( sqlStr )

        if( accRecordsFail == None ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '��ˮ��������쳣:'+AfaDBFunc.sqlErrMsg )


        #########################################################################################
        AfaLoggerFunc.tradeInfo( '>>>�쳣ͳ��::' )
        sqlStr = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL WHERE REVTRANF='0' AND SYSID='" + str(records[i][0]).strip() +  "' AND ((AGENTFLAG='01' AND BANKSTATUS='0' AND CORPSTATUS<>'0') OR (AGENTFLAG='02' AND CORPSTATUS='0' AND BANKSTATUS<>'0'))"
        sqlStr = sqlStr + accSqlStr

        AfaLoggerFunc.tradeInfo( sqlStr )

        accRecordsObnormal = AfaDBFunc.SelectSql( sqlStr )

        if( accRecordsObnormal == None ):
            return AfaFlowControl.ExitThisFlow( 'A0027', '��ˮ��������쳣:'+AfaDBFunc.sqlErrMsg )

        if ( TradeContext.TransType=='0' ):
            TradeContext.tradeResponse.append(['sysId',records[i][0]])                                      #ϵͳ��ʶ
                
            TradeContext.tradeResponse.append(['sysName',records[i][1]])                                    #ϵͳ����

            TradeContext.tradeResponse.append(['tradeNums', str(accRecordsSucc[0][0])])                     #���ױ���(�ֽ�)
            if accRecordsSucc[0][1] == None:
                TradeContext.tradeResponse.append(['tradeAmt','0.00'])                                      #���׽��(�ֽ�)
            else:
                TradeContext.tradeResponse.append(['tradeAmt', str(accRecordsSucc[0][1])])


            TradeContext.tradeResponse.append(['tradeNums_acc',str(accRecordsSucc_acc[0][0])])              #���ױ���(ת��)
            if accRecordsSucc_acc[0][1] == None:
                TradeContext.tradeResponse.append(['tradeAmt_acc', '0.00'])                                 #���׽��(ת��)
            else:
                TradeContext.tradeResponse.append(['tradeAmt_acc', str(accRecordsSucc_acc[0][1])])



            TradeContext.tradeResponse.append(['tradeNumsFail', str(accRecordsFail[0][0])])                 #ʧ�ܱ���
            if accRecordsFail[0][1] == None:
                TradeContext.tradeResponse.append(['tradeAmtFail', '0.00'])                                 #ʧ�ܽ��
            else:
                TradeContext.tradeResponse.append(['tradeAmtFail', str(accRecordsFail[0][1])])


            TradeContext.tradeResponse.append(['tradeNumsObnormal', str(accRecordsObnormal[0][0])])         #�쳣����
            if accRecordsObnormal[0][1] == None:
                TradeContext.tradeResponse.append(['tradeAmtObnormal', '0.00'])                             #�쳣���
            else:
                TradeContext.tradeResponse.append(['tradeAmtObnormal', str(accRecordsObnormal[0][1])])

        else:
            wBuffer = ""
            wBuffer = wBuffer + records[i][0]                       + "|"               #ϵͳ��ʶ
            wBuffer = wBuffer + records[i][1]                       + "|"               #ϵͳ����


            wBuffer = wBuffer + str(accRecordsSucc[0][0])           + "|"               #���ױ���(�ֽ�)
            if accRecordsSucc[0][1] == None:                                            #���׽��(�ֽ�)
                wBuffer = wBuffer + '0'                             + "|"
            else:
                wBuffer = wBuffer + str(accRecordsSucc[0][1])       + "|"



            wBuffer = wBuffer + str(accRecordsSucc_acc[0][0])       + "|"               #���ױ���(ת��)
            if accRecordsSucc_acc[0][1] == None:                                        #���׽��(ת��)
                wBuffer = wBuffer + '0'                             + "|"
            else:
                wBuffer = wBuffer + str(accRecordsSucc_acc[0][1])   + "|"



            wBuffer = wBuffer + str(accRecordsFail[0][0])           + "|"               #ʧ�ܱ���
            if accRecordsFail[0][1] == None:                                            #ʧ�ܽ��
                wBuffer = wBuffer + '0'                             + "|"
            else:
                wBuffer = wBuffer + str(accRecordsFail[0][1])       + "|"


            wBuffer = wBuffer + str(accRecordsObnormal[0][0])       + "|"               #�쳣����
            if accRecordsObnormal[0][1] == None:                                        #�쳣���
                wBuffer = wBuffer + '0'                             + "|"
            else:
                wBuffer = wBuffer + str(accRecordsObnormal[0][1])   + "|"

            sfp.write(wBuffer + '\n')
                
        queryCount = queryCount+  1

    if ( TradeContext.TransType != '0' ):
        sfp.close()

        #������ļ����䷽ʽ������Ҫ�����ļ���
        TradeContext.tradeResponse.append(['filename',  'MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'])

    #��¼��
    TradeContext.tradeResponse.append(['queryCount',  str(queryCount)])

    return True
