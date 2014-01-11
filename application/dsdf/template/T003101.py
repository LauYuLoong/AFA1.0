# -*- coding: gbk -*-
################################################################################
#   ���մ���.��ѯ��ϸģ��
#===============================================================================
#   ģ���ļ�:   003101.py
#   �޸�ʱ��:   2006-04-05
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,TradeFunc,AfaFlowControl,AfaFunc,os
from types import *


def main( ):

    sernoFlag = 0
    
    AfaLoggerFunc.tradeInfo( '******���մ���.��ѯ��ϸģ��['+TradeContext.TemplateCode+']����******' )

    try:
        #=====================��ʼ�����ر��ı���================================
        TradeContext.tradeResponse=[]


        #=====================��ȡ��ǰϵͳʱ��==================================
        TradeContext.workDate=AfaUtilTools.GetSysDate( )
        TradeContext.workTime=AfaUtilTools.GetSysTime( )

        #=====================�ж�Ӧ��ϵͳ״̬==================================
        if not AfaFunc.ChkSysStatus( ) :
            raise AfaFlowControl.flowException( )

        #=====================У�鹫���ڵ����Ч��==============================
        if( not TradeContext.existVariable( "zoneno" ) ):
            TradeFunc.exitOnError( 'A0001', '������[zoneno]ֵ������,���ܽ��в�ѯ����' )


        if( not TradeContext.existVariable( "brno" ) ):
            TradeFunc.exitOnError( 'A0001', '�����[brno]ֵ������,���ܽ��в�ѯ����' )


        if( not TradeContext.existVariable( "tellerno" ) ):
            TradeFunc.exitOnError( 'A0001', '�����[tellerno]ֵ������,���ܽ��в�ѯ����' )


        if( not TradeContext.existVariable( "transStatus" ) ):
            TradeFunc.exitOnError( 'A0001', '����״̬[transStatus]ֵ������,���ܽ��в�ѯ����' )


        if( not TradeContext.existVariable( "queryMode" ) ):
            TradeFunc.exitOnError( 'A0001', '��ѯ��ʽ[queryMode]ֵ������,���ܽ��в�ѯ����' )


        if( not TradeContext.existVariable( "orderMode" ) ):
            TradeFunc.exitOnError( 'A0001', '����ʽ[orderMode]ֵ������,���ܽ��в�ѯ����' )


        if( not TradeContext.existVariable( "queryCount" ) ):
            TradeFunc.exitOnError( 'A0001', '��ѯ����[queryCount]ֵ������,���ܽ��в�ѯ����' )


        if( not TradeContext.existVariable( "TransType" ) ):
            TradeFunc.exitOnError( 'A0001', '��������[TransType]ֵ������,���ܽ��в�ѯ����' )


        AfaLoggerFunc.tradeInfo('>>>transStatus   = ' + TradeContext.transStatus)
        AfaLoggerFunc.tradeInfo('>>>queryMode     = ' + TradeContext.queryMode)
        AfaLoggerFunc.tradeInfo('>>>orderMode     = ' + TradeContext.orderMode)
        AfaLoggerFunc.tradeInfo('>>>queryCount    = ' + TradeContext.queryCount)
        AfaLoggerFunc.tradeInfo('>>>TransType     = ' + TradeContext.TransType)
        AfaLoggerFunc.tradeInfo('>>>tradeDate     = ' + TradeContext.tradeDate)


        #=====================����ÿ�η��ص����ݵļ�¼��========================
        queryCount = int( TradeContext.queryCount )


        #=====================���ݴ��ʱʹ��list================================
        names=['agentSerialno', 'sysId', 'unitno', 'subUnitno', 'workDate', 'workTime','agentFlag', 'transCode', 'zoneno', 'brno', 'tellerno', \
        'channelCode', 'accType', 'drAccno', 'crAccno', 'userno', 'subuserno', 'username', 'vouhType', 'vouhno', \
        'vouhDate', 'amount', 'subAmount', 'bankStatus', 'bankSerno', 'corpStatus', 'errormsg', 'note1', \
        'note2', 'note3', 'note4', 'note5', 'note6', 'note7', 'note8', 'note9', 'note10']


        # =====================��ѯ�ֶ������ݴ����listһһ��Ӧ=================
        SqlStr = "SELECT AGENTSERIALNO,SYSID,UNITNO,SUBUNITNO,WORKDATE,WORKTIME,AGENTFLAG,TRXCODE,ZONENO,BRNO,TELLERNO,"
        SqlStr = SqlStr + "CHANNELCODE,ACCTYPE,DRACCNO,CRACCNO,USERNO,SUBUSERNO,USERNAME,VOUHTYPE,VOUHNO,"
        SqlStr = SqlStr + "VOUHDATE,AMOUNT,SUBAMOUNT,BANKSTATUS,BANKSERNO,CORPSTATUS,ERRORMSG,NOTE1,"
        SqlStr = SqlStr + "NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8,NOTE9,NOTE10 FROM AFA_MAINTRANSDTL "


        #=====================ͳ���ܱ������ܽ��================================
        sql_count = "SELECT COUNT(*),SUM(CAST(AMOUNT AS DECIMAL(17,2))) FROM AFA_MAINTRANSDTL"

        sql = ''
        if ( int( TradeContext.queryMode ) == 4 ):              #���ɲ�ѯ��ʽ
            if( not TradeContext.existVariable( "whereClause" ) ):
                TradeFunc.exitOnError( 'A0001', '��ѯ����[whereClause]ֵ������,���ܽ��в�ѯ����' )

            sql= sql + TradeContext.whereClause + " AND REVTRANF='0' "

            AfaLoggerFunc.tradeInfo('>>>whereClause   = ' + TradeContext.whereClause)

        else:
            if( not TradeContext.existVariable( "tradeDate" ) ):
                TradeFunc.exitOnError( 'A0001', '��������[tradeDate]ֵ������,���ܽ��в�ѯ����' )

            if( not TradeContext.existVariable( "channelCode" ) ):
                TradeFunc.exitOnError( 'A0001', '��������[channelCode]ֵ������,���ܽ��в�ѯ����' )

            #����
            sql = sql + " WHERE WORKDATE='"     + TradeContext.tradeDate        + "'"

            #������
            sql = sql + " AND CHANNELCODE='"    + TradeContext.channelCode      + "'"

            #������
            sql = sql + " AND ZONENO='"         + TradeContext.zoneno           + "'"

            #�����
            sql = sql + " AND BRNO='"           + TradeContext.brno             + "'"

            #��Ա
            sql = sql + " AND TELLERNO='"       + TradeContext.tellerno         + "'"

            #��Ա
            sql = sql + " AND REVTRANF='"       + "0"                           + "'"
            
            #�û�
            if( TradeContext.existVariable( "userno" ) and len(TradeContext.userno)>0 ):
                sql = sql + " AND USERNO='"     + TradeContext.userno           + "'"

            #���
            if( TradeContext.existVariable( "amount" ) and int(float(TradeContext.amount)*100)!=0 ):
                sAmount="0.00";
                for i in range(0, len(TradeContext.amount)):
                    if TradeContext.amount[i] == '0':
                        continue
                    sAmount = TradeContext.amount[i:]
                    break

                sql = sql + " AND AMOUNT='"     + sAmount           + "'"

            #�û���
            if( TradeContext.existVariable( "username" ) and len(TradeContext.username)>0 ):
                sql = sql + " AND USERNAME='"   + TradeContext.username         + "'"

            #�ʺ�
            if( TradeContext.existVariable( "accno" ) and len(TradeContext.accno)>0 ):
                sql = sql + " AND (DRACCNO='"   + TradeContext.accno + "' OR CRACCNO='" + TradeContext.accno + "')"

        #transStatus:����״̬(1-����, 2-δ֪, 3-ȫ��)
        if( int( TradeContext.transStatus )   == 1 ):

            #��ѯ��������
            sql = sql + " AND BANKSTATUS='0' AND CORPSTATUS='0'"

        elif( int( TradeContext.transStatus ) == 2 ):

            #��ѯδ֪����
            sql = sql + " AND (AGENTFLAG IN ('01','03') AND (BANKSTATUS='2' OR (BANKSTATUS='0' AND CORPSTATUS IN ('1', '2','3')))) OR"
            sql = sql + " (AGENTFLAG IN ('02','04') AND (CORPSTATUS='2' OR (CORPSTATUS='0' AND BANKSTATUS IN ('1', '2','3')))) "

        elif( int( TradeContext.transStatus ) != 3 ):
            TradeContext.errorCode, TradeContext.errorMsg='A0041', "��ڲ�����������[����״̬]:"+str( TradeContext.transStatus )
            raise AfaFlowControl.flowException( )


        #queryMode:��ѯ��ʽ(1-����ˮ�Ų�ѯ, 2-��ϵͳ�����ѯ, 3-��ѯȫ��������, 4-���ɲ�ѯ��ʽ)
        if( int( TradeContext.queryMode ) == 1 ):

            #����ˮ�Ų�ѯ
            if( not TradeContext.existVariable( "agentSerialno" ) ):
                TradeFunc.exitOnError( 'A0001', '��ˮ��[agentSerialno]ֵ������!' )

            sql = sql + " AND AGENTSERIALNO='"+TradeContext.agentSerialno + "'"
            sernoFlag = 1
            
        elif( int( TradeContext.queryMode ) == 2 ):

            #��ϵͳ�����ѯ
            if( not TradeContext.existVariable( "sysId" ) ):
                TradeFunc.exitOnError( 'A0001', 'ϵͳ����[sysId]ֵ������!' )

            #ϵͳ����
            sql = sql + " AND SYSID='"       + TradeContext.sysId     + "'"


            #����ˮ�Ų�ѯ
            if( TradeContext.existVariable( "agentSerialno" ) and len(TradeContext.agentSerialno)>0 ):
                sql = sql + " AND AGENTSERIALNO='"+TradeContext.agentSerialno + "'"
                sernoFlag = 1

            #ҵ��ʽ
            if( TradeContext.existVariable( "agentFlag" ) and len(TradeContext.agentFlag)>0 ):
                sql=sql + " AND AGENTFLAG='" + TradeContext.agentFlag + "'"


            #��λ����
            if( TradeContext.existVariable( "unitno" ) and len(TradeContext.unitno)>0 ):
                sql=sql + " AND UNITNO='"    + TradeContext.unitno    + "'"


            #�ӵ�λ����
            if( TradeContext.existVariable( "subUnitno" ) and len(TradeContext.subUnitno)>0 ):
                sql=sql + " AND SUBUNITNO='" + TradeContext.subUnitno + "'"


        elif( int( TradeContext.queryMode ) != 3 and int( TradeContext.queryMode ) != 4 ):
            TradeContext.errorCode, TradeContext.errorMsg='A0041', "��ڲ�����������[��ѯ��ʽ]:"+str( TradeContext.queryMode )
            raise AfaFlowControl.flowException( )

        sql_count = sql_count + sql


        #����ˮ��ѯӦ���ǵ��������,û������ı�Ҫ
        if( int( TradeContext.queryMode ) != 1  and sernoFlag==0):

            #orderMode:����ʽ:1-���� 2-����
            if( int( TradeContext.orderMode ) == 1 ):

                #����
                if( (not TradeContext.existVariable( "agentSerialno" )) or TradeContext.agentSerialno=='' ):
                    TradeContext.agentSerialno='0'

                sql = sql + " AND AGENTSERIALNO>'" + TradeContext.agentSerialno + "' ORDER BY AGENTSERIALNO ASC"

            else:

                #����
                if( (not TradeContext.existVariable( "agentSerialno" )) or TradeContext.agentSerialno=='' ):
                    TradeContext.agentSerialno='99999999'

                sql = sql + " AND AGENTSERIALNO<'"+TradeContext.agentSerialno + "' ORDER BY AGENTSERIALNO DESC"


        #��ѯ���ݿ�
        SqlStr = SqlStr + sql

        AfaLoggerFunc.tradeInfo( '>>>��ѯ��ϸ' )

        AfaLoggerFunc.tradeInfo( SqlStr )

        records=AfaDBFunc.SelectSql( SqlStr, queryCount )

        if( records == None ):
            #None ��ѯʧ��
            TradeContext.errorCode, TradeContext.errorMsg='A0025', "���ݿ��������"
            raise AfaFlowControl.flowException( )


        elif( len( records ) == 0 ):
            #�޼�¼
            TradeContext.errorCode, TradeContext.errorMsg='A0025', "û�����������ļ�¼"
            raise AfaFlowControl.flowException( )


        AfaLoggerFunc.tradeInfo( '>>>ͳ������' )


        #ͳ������
        AfaLoggerFunc.tradeInfo( sql_count )


        records_count=AfaDBFunc.SelectSql( sql_count )

        if( records_count == None ):
            TradeContext.errorCode, TradeContext.errorMsg='A0025', "���ݿ��������"
            raise AfaFlowControl.flowException( )

        # ����records�е�����None����
        records=AfaUtilTools.ListFilterNone( records )

        #�ܹ��ķ��ؼ�¼��
        total=len( records )
        AfaLoggerFunc.tradeInfo( '���ؼ�¼��:[' + str(total) + ']' )

        #��������ƴ��
        TradeContext.tradeResponse=[]
        TradeContext.tradeResponse.append( ['errorCode',     '0000'] )
        TradeContext.tradeResponse.append( ['errorMsg',      '���׳ɹ�'] )
        TradeContext.tradeResponse.append( ['retCount',      str( total )] )
        TradeContext.tradeResponse.append( ['retTotalCount', str( records_count[0][0] )])
        TradeContext.tradeResponse.append( ['retTotalAmount',str( records_count[0][1] )])


        if ( TradeContext.TransType == '0' ):
            #���ձ��������
            for i in range( 0, total ):
                k=0
                for name in names:
                    if( int( TradeContext.orderMode ) == 1 ):
                        TradeContext.tradeResponse.append( [name, records[i][k]] )
                    else:
                        TradeContext.tradeResponse.append( [name, records[total-i-1][k]] )
                    k=k+1
        else:
            MxFileName = os.environ['AFAP_HOME'] + '/tmp/MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'
            AfaLoggerFunc.tradeInfo('��ϸ�ļ�:['+MxFileName+']')

            if (os.path.exists(MxFileName) and os.path.isfile(MxFileName)):
                #�ļ�����,��ɾ��-�ٴ���
                os.system("rm " + MxFileName)

            #������ϸ�ļ�
            sfp = open(MxFileName, "w")

            #��ÿ����¼����������߷ָ��ĸ�ʽ
            TradeContext.tradeResponse.append(['filename',  'MX' + TradeContext.zoneno + TradeContext.brno + TradeContext.tellerno + '.TXT'])

            for i in range( 0, total ):
                tmpBuffer = ""
                tmpBuffer = tmpBuffer + str(records[i][0]).strip()   + "|"         #AGENTSERIALNO
                tmpBuffer = tmpBuffer + str(records[i][1]).strip()   + "|"         #SYSID
                tmpBuffer = tmpBuffer + str(records[i][2]).strip()   + "|"         #UNITNO
                tmpBuffer = tmpBuffer + str(records[i][3]).strip()   + "|"         #SUBUNITNO
                tmpBuffer = tmpBuffer + str(records[i][4]).strip()   + "|"         #WORKDATE
                tmpBuffer = tmpBuffer + str(records[i][5]).strip()   + "|"         #WORKTIME
                tmpBuffer = tmpBuffer + str(records[i][6]).strip()   + "|"         #AGENTFLAG
                tmpBuffer = tmpBuffer + str(records[i][7]).strip()   + "|"         #TRXCODE
                tmpBuffer = tmpBuffer + str(records[i][8]).strip()   + "|"         #ZONENO
                tmpBuffer = tmpBuffer + str(records[i][9]).strip()   + "|"         #BRNO
                tmpBuffer = tmpBuffer + str(records[i][10]).strip()  + "|"         #TELLERNO
                tmpBuffer = tmpBuffer + str(records[i][11]).strip()  + "|"         #CHANNELCODE
                tmpBuffer = tmpBuffer + str(records[i][12]).strip()  + "|"         #ACCTYPE
                tmpBuffer = tmpBuffer + str(records[i][13]).strip()  + "|"         #DRACCNO
                tmpBuffer = tmpBuffer + str(records[i][14]).strip()  + "|"         #CRACCNO
                tmpBuffer = tmpBuffer + str(records[i][15]).strip()  + "|"         #USERNO
                tmpBuffer = tmpBuffer + str(records[i][16]).strip()  + "|"         #SUBUSERNO
                tmpBuffer = tmpBuffer + str(records[i][17]).strip()  + "|"         #USERNAME
                tmpBuffer = tmpBuffer + str(records[i][18]).strip()  + "|"         #VOUHTYPE
                tmpBuffer = tmpBuffer + str(records[i][19]).strip()  + "|"         #VOUHNO
                tmpBuffer = tmpBuffer + str(records[i][20]).strip()  + "|"         #VOUHDATE
                tmpBuffer = tmpBuffer + str(records[i][21]).strip()  + "|"         #AMOUNT
                tmpBuffer = tmpBuffer + str(records[i][22]).strip()  + "|"         #SUBAMOUNT
                tmpBuffer = tmpBuffer + str(records[i][23]).strip()  + "|"         #BANKSTATUS
                tmpBuffer = tmpBuffer + str(records[i][24]).strip()  + "|"         #BANKSERNO
                tmpBuffer = tmpBuffer + str(records[i][25]).strip()  + "|"         #CORPSTATUS
                tmpBuffer = tmpBuffer + str(records[i][26]).strip()  + "|"         #ERRORMSG
                tmpBuffer = tmpBuffer + str(records[i][27]).strip()  + "|"         #NOTE1
                tmpBuffer = tmpBuffer + str(records[i][28]).strip()  + "|"         #NOTE2
                tmpBuffer = tmpBuffer + str(records[i][29]).strip()  + "|"         #NOTE3
                tmpBuffer = tmpBuffer + str(records[i][30]).strip()  + "|"         #NOTE4
                tmpBuffer = tmpBuffer + str(records[i][31]).strip()  + "|"         #NOTE5
                tmpBuffer = tmpBuffer + str(records[i][32]).strip()  + "|"         #NOTE6
                tmpBuffer = tmpBuffer + str(records[i][33]).strip()  + "|"         #NOTE7
                tmpBuffer = tmpBuffer + str(records[i][34]).strip()  + "|"         #NOTE8
                tmpBuffer = tmpBuffer + str(records[i][35]).strip()  + "|"         #NOTE9
                tmpBuffer = tmpBuffer + str(records[i][36]).strip()  + "|"         #NOTE10

                sfp.write(tmpBuffer + '\n')
                    
            sfp.close()

        #=====================�Զ����==========================================
        AfaFunc.autoPackData()

        #=====================�˳�ģ��==========================================
        AfaLoggerFunc.tradeInfo( '******���մ���.��ѯ��ϸģ��['+TradeContext.TemplateCode+']�˳�******' )

    except AfaFlowControl.flowException, e:
        AfaFlowControl.exitMainFlow( str(e) )

    except Exception, e:
        AfaFlowControl.exitMainFlow( str(e) )
