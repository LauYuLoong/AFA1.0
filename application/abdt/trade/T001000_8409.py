# -*- coding: gbk -*-
################################################################################
#   ����ҵ��ϵͳ��������ҵ����
#===============================================================================
#   �����ļ�:   T001000_8409.py
#   ��˾���ƣ�  ������ͬ�Ƽ����޹�˾
#   ��    �ߣ�  XZH
#   �޸�ʱ��:   2008-06-10
################################################################################
import TradeContext,AfaLoggerFunc,AfaUtilTools,AfaDBFunc,os,AbdtFunc
from types import *


#=====================������ҵ����==============================================
def TrxMain():


    AfaLoggerFunc.tradeInfo('**********������ҵ����(8409)��ʼ**********')



    TradeContext.tradeResponse.append(['O1AFAPDATE', TradeContext.TranDate])    #��������
    TradeContext.tradeResponse.append(['O1AFAPTIME', TradeContext.TranTime])    #����ʱ��

    #�жϵ�λЭ���Ƿ���Ч
    if ( not AbdtFunc.ChkUnitInfo( ) ):
        return False
        
    #######################################################################
    #20090927 ������ ���ӶԹ��˻�У��
    #----------------------------------------------------------------------
    AfaLoggerFunc.tradeInfo( '>>>У��Թ��˻�' )
    
    if ( TradeContext.I1ACCNO != TradeContext.ACCNO ):
        return ExitSubTrade( "9000", "��λ�Թ��˻���һ�£���������ҵ��")
    #######################################################################

    #�ж����������Ƿ��Ѵ���
    if (  not ChkBatchInfo( ) ):
        return False


    #�жϴ��������ļ��Ƿ����(0-����¼��,1-��Χ�ϴ�)
    try:
        if ( TradeContext.I1FTPTYPE == '0' ):
            #����ϵͳ�ϴ�
            sFileName = os.environ['AFAP_HOME'] + '/data/batch/up_vmenu/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO
            dFileName = os.environ['AFAP_HOME'] + '/data/batch/in/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO + "_" + TradeContext.TranDate

        elif ( TradeContext.I1FTPTYPE == '1' ):
            #��Χϵͳ�ϴ�
            
            
            #20120409 �º��޸����--AG07
            #if ( TradeContext.I1APPNO[0:4] == 'AG08' ):
            AfaLoggerFunc.tradeInfo('>>>TradeContext.I1APPNO[0:4] =='+TradeContext.I1APPNO[0:4])
            if ( TradeContext.I1APPNO[0:4] == 'AG08' or TradeContext.I1APPNO[0:4] == 'AG07'):
                #�������⴦��(�޸��ˣ����Һͣ��޸����ڣ�20080402)

                sCZZJDM  = ''
                sCZZJDMMC= ''
                sCZNOTE1 = ''
                sCZNOTE2 = ''

                #��ѯ�ʽ������Ϣ
                sql = "SELECT CZZJDM,ZJDMMC,NOTE1,NOTE2 FROM ABDT_CZDZB WHERE "
                sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO  + "'"        #ҵ����

                AfaLoggerFunc.tradeInfo( '>>>�������⴦������' +sql)
                records = AfaDBFunc.SelectSql( sql )
                if ( records == None ):
                    AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
                    return ExitSubTrade( '9000', '��ѯ�ʽ������Ϣ�쳣' )

                if ( len(records) == 0 ):
                    return ExitSubTrade( '9000', 'û���ʽ���������Ϣ' )

                else:
                    sCZZJDM  = str(records[0][0]).strip()           #�ʽ����
                    sCZZJDMMC= str(records[0][1]).strip()           #��λ����
                    sCZNOTE1 = str(records[0][2]).strip()           #��ע1
                    sCZNOTE2 = str(records[0][3]).strip()           #��ע2

                #�������ʽ��ʺ�(6λ)+�ṹ����(14λ)�������ļ���
                sFileName = os.environ['AFAP_HOME'] + '/data/batch/up_other/' + sCZZJDM + TradeContext.I1BUSINO + TradeContext.I1BTHNO
            else:
                sFileName = os.environ['AFAP_HOME'] + '/data/batch/up_other/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO

            dFileName = os.environ['AFAP_HOME'] + '/data/batch/swap/' + TradeContext.I1APPNO + TradeContext.I1BUSINO + TradeContext.I1BTHNO + "_" + TradeContext.TranDate

        else:
            return ExitSubTrade( '9000', '�ϴ���ʽ����' )
        
        AfaLoggerFunc.tradeInfo("�ϴ��ļ��ǣ�" + sFileName)


        #Դ�ļ���
        TradeContext.S_FILENAME = sFileName
        
        #Ŀ���ļ���
        TradeContext.D_FILENAME = dFileName

        if ( os.path.exists(sFileName) and os.path.isfile(sFileName) ):
            AfaLoggerFunc.tradeInfo("�������������ļ�����")

            if ( TradeContext.I1FTPTYPE == '1' ):
                AfaLoggerFunc.tradeInfo("��Χϵͳ�ϴ�-->ֻ��Ҫ�Ǽ�")

            else:
                AfaLoggerFunc.tradeInfo("����ϵͳ�ϴ�-->��У���ļ�")

                #���ļ�
                bfp = open(sFileName, "r")

                #��ȡһ��
                linebuf = bfp.readline()
                while ( len(linebuf) > 0 ):
                    if ( (len(linebuf) != 100) and (len(linebuf) != 101) ):
                        bfp.close()
                        return ExitSubTrade( '9000', '�������������ļ���ʽ����' )

                    if ( linebuf[0] == "1" ):
                        AfaLoggerFunc.tradeInfo("**********������Ϣ**********")
                        s_rectype    = linebuf[0:1].lstrip().rstrip()          #��¼����
                        s_appno      = linebuf[1:7].lstrip().rstrip()          #ҵ����
                        s_busino     = linebuf[7:21].lstrip().rstrip()         #��λ���
                        s_agenttype  = linebuf[21:22].lstrip().rstrip()        #ί�з�ʽ
                        s_accno      = linebuf[22:45].lstrip().rstrip()        #�Թ��ʺ�
                        s_remark     = linebuf[45:65].lstrip().rstrip()        #����
                        s_status     = linebuf[65:66].lstrip().rstrip()        #״̬
                        s_totalnum   = linebuf[66:76].lstrip().rstrip()        #�ܱ���
                        s_totalamt   = linebuf[76:93].lstrip().rstrip()        #�ܽ��
                        s_retcode    = linebuf[93:100].lstrip().rstrip()       #������

                        AfaLoggerFunc.tradeInfo("��¼���� =" + s_rectype)
                        AfaLoggerFunc.tradeInfo("ҵ���� =" + s_appno)
                        AfaLoggerFunc.tradeInfo("��λ��� =" + s_busino)
                        AfaLoggerFunc.tradeInfo("ί�з�ʽ =" + s_agenttype)
                        AfaLoggerFunc.tradeInfo("�Թ��ʺ� =" + s_accno)
                        AfaLoggerFunc.tradeInfo("��    �� =" + s_remark)
                        AfaLoggerFunc.tradeInfo("״    ̬ =" + s_status)
                        AfaLoggerFunc.tradeInfo("�� �� �� =" + s_totalnum)
                        AfaLoggerFunc.tradeInfo("�� �� �� =" + s_totalamt)
                        AfaLoggerFunc.tradeInfo("�� �� �� =" + s_retcode)
                        AfaLoggerFunc.tradeInfo("**********������Ϣ**********")

                        break

                    linebuf = bfp.readline()

                #�ر��ļ�
                bfp.close()

                #״̬(0:���� 1:����)
                if ( s_status == "0" ):
                    return ExitSubTrade('9000', '�����������ļ��л��ܼ�¼״̬����,��������')


                #У��ҵ�����
                if ( TradeContext.I1APPNO != s_appno ):
                    return ExitSubTrade('9000', '�������ҵ������������ļ���ҵ����벻��,��������')


                #У�鵥λ����
                if ( TradeContext.I1BUSINO != s_busino ):
                    return ExitSubTrade('9000', '������ĵ�λ�����������ļ��ĵ�λ���벻��,��������')


                #У��Թ��ʺ�
                if ( TradeContext.ACCNO != s_accno ):
                    return ExitSubTrade('9000', '�������������ļ��еĶԹ��ʺź͵�λ��Ϣ���еǼǲ���')


                #У��ί�з�ʽ�Ƿ�һ��
                if ( TradeContext.AGENTTYPE != s_agenttype ):
                    return ExitSubTrade('9000', '�������������ļ��е�ί�з�ʽ�͵�λ��Ϣ���еǼǲ���')


                #У��ί�з�ʽ�Ϸ���
                if ( (s_agenttype!='3') and (s_agenttype!='4') ):
                    return ExitSubTrade('9000', '�������������ļ��е�ί�з�ʽ�Ƿ�')


                #У���ܱ���
                if ( TradeContext.I1TOTALNUM != s_totalnum ):
                    return ExitSubTrade('9000', '������������ܱ����������ļ����ܱ�������,��������')


                #У���ܽ��
                if ( TradeContext.I1TOTALAMT != s_totalamt ):
                    return ExitSubTrade('9000', '������������ܽ���������ļ����ܽ���,��������')

        else:
            AfaLoggerFunc.tradeInfo("�ϴ��ļ��� =" + sFileName)
            return ExitSubTrade('9000', '�������������ļ�û���ϴ�,������')


    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade('9999', '�������������ļ������쳣')


    ###############################################################################
    #20090927 ������ ��ȡ�����ļ�����Ϣ���ж�ҵ�������ͣ�0-��ʱ����1-���մ���
    #-----------------------------------------------------------------------------
    batchCfg = AbdtFunc.getBatchConfig( )
    
    #��ֳ�����ҵ������
    APPTRFG = TradeContext.BATCH_APPTRFG.split( '|' )
    
    #�ж������մ����Ǽ�ʱ����
    if ( TradeContext.I1APPNO[0:6] in APPTRFG and int( TradeContext.I1TOTALNUM ) <= int( TradeContext.BATCH_MAXCOUNT ) ):
        TradeContext.I1TRFG = '0'    #��ʱ����
        
        AfaLoggerFunc.tradeInfo( '>>>����ʱ����' )
        
    else:
        TradeContext.I1TRFG = '1'    #���մ���
        
        AfaLoggerFunc.tradeInfo( '>>>�����մ���' )
        
    ################################################################################
    
    #����ί�к�
    if ( not CrtBatchNo( ) ):
        return False


    try:
        #���ļ��Ƶ������ڲ�����Ŀ¼��(in)
        cp_cmd_str="mv " + sFileName + " " + dFileName
        os.system(cp_cmd_str)
        
    except Exception, e:
        AfaLoggerFunc.tradeInfo( str(e) )
        return ExitSubTrade('9999', '���������ļ�ת�Ʋ����쳣')


    #�Ǽ�������Ϣ
    if ( not InsertBatchInfo( ) ):
        return False

    TradeContext.tradeResponse.append(['O1BATCHNO', TradeContext.BATCHNO])        #ί�к�
    TradeContext.tradeResponse.append(['O1ACCNO',   TradeContext.ACCNO])          #�Թ��˻�
    TradeContext.tradeResponse.append(['O1VOUHNO',  TradeContext.VOUHNO])         #ƾ֤��(�ڲ��˻�)


    AfaLoggerFunc.tradeInfo('**********������ҵ����(8409)����**********')


    #����
    TradeContext.tradeResponse.append(['errorCode', '0000'])
    TradeContext.tradeResponse.append(['errorMsg',  '���׳ɹ�'])
    return True




#�ж����������Ƿ��Ѵ���
def ChkBatchInfo( ):

    sql = ""

    AfaLoggerFunc.tradeInfo('>>>�ж����������Ƿ��Ѵ���')

    try:
        sql = "SELECT BATCHNO,STATUS FROM ABDT_BATCHINFO WHERE "
        sql = sql + "APPNO="    + "'" + TradeContext.I1APPNO    + "'" + " AND "        #ҵ����
        sql = sql + "BUSINO="   + "'" + TradeContext.I1BUSINO   + "'" + " AND "        #��λ���
        sql = sql + "ZONENO="   + "'" + TradeContext.I1ZONENO   + "'" + " AND "        #��������
        sql = sql + "BRNO="     + "'" + TradeContext.I1SBNO     + "'" + " AND "        #��������
        sql = sql + "INDATE="   + "'" + TradeContext.TranDate   + "'" + " AND "        #ί������
        sql = sql + "FILENAME=" + "'" + TradeContext.I1FILENAME + "'" + " AND "        #�ļ�����
        sql = sql + "STATUS<>"  + "'" + "40"                    + "'"                  #״̬(����)

        AfaLoggerFunc.tradeInfo(sql)

        records = AfaDBFunc.SelectSql(sql)
        if ( records == None ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '��ѯ������Ϣ���쳣' )

        if ( len(records) > 0 ):
            #�ж�״̬
            if ( str(records[0][1]) == "10" ):
                return ExitSubTrade( '9000', '�û����õ�λ���������ݽ����Ѿ�����,�����ٴ�����' )

            elif ( str(records[0][1]) == "88" ):
                return ExitSubTrade( '9000', '�û����õ�λ�����������ļ��Ѿ��������,�����ٴ�����' )

            else:
                return ExitSubTrade( '9000', '�û����õ�λ�����������ļ����ڴ���,���ܽ����������' )

        else:
            AfaLoggerFunc.tradeInfo('>>>û�з��ָû��������������������ļ�,��������')
            return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�ж����������Ƿ��Ѵ���,���ݿ��쳣' )



#����ί�к�
def CrtBatchNo( ):

    AfaLoggerFunc.tradeInfo('>>>��������ί�к�')

    try:
        sqlStr = "SELECT NEXTVAL FOR ABDT_ONLINE_SEQ FROM SYSIBM.SYSDUMMY1"

        records = AfaDBFunc.SelectSql( sqlStr )
        if records == None :
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )
            return ExitSubTrade( '9000', '����ί�к��쳣' )

        #���κ�
        TradeContext.BATCHNO = TradeContext.TranDate + str(records[0][0]).rjust(8, '0')

        return True

    except Exception, e:
        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '����ί�к��쳣' )



#�Ǽ�������ҵ������Ϣ
def InsertBatchInfo( ):


    AfaLoggerFunc.tradeInfo('>>>�Ǽ�������ҵ������Ϣ')

    try:
        sql = ""
        sql = "INSERT INTO ABDT_BATCHINFO("
        sql = sql + "BATCHNO,"                 #ί�к�(���κ�: Ψһ(����+��ˮ��)
        sql = sql + "APPNO,"                   #ҵ����
        sql = sql + "BUSINO,"                  #��λ���
        sql = sql + "ZONENO,"                  #������
        sql = sql + "BRNO,"                    #�����
        sql = sql + "USERNO,"                  #����Ա
        sql = sql + "ADMINNO,"                 #����Ա
        sql = sql + "TERMTYPE,"                #�ն�����
        sql = sql + "FILENAME,"                #�ϴ��ļ���
        sql = sql + "INDATE,"                  #ί������
        sql = sql + "INTIME,"                  #ί��ʱ��
        sql = sql + "BATCHDATE,"               #�ύ����
        sql = sql + "BATCHTIME,"               #�ύʱ��
        sql = sql + "TOTALNUM,"                #�ܱ���
        sql = sql + "TOTALAMT,"                #�ܽ��
        sql = sql + "SUCCNUM,"                 #�ɹ�����
        sql = sql + "SUCCAMT,"                 #�ɹ����
        sql = sql + "FAILNUM,"                 #ʧ�ܱ���
        sql = sql + "FAILAMT,"                 #ʧ�ܽ��
        sql = sql + "STATUS,"                  #״̬
        sql = sql + "BEGINDATE,"               #��Ч����
        sql = sql + "ENDDATE,"                 #ʧЧ����
        sql = sql + "PROCMSG,"                 #������Ϣ
        sql = sql + "NOTE1,"                   #��ע1
        sql = sql + "NOTE2,"                   #��ע2
        sql = sql + "NOTE3,"                   #��ע3
        sql = sql + "NOTE4,"                   #��ע4
        sql = sql + "NOTE5)"                   #��ע5

        sql = sql + " VALUES ("

        sql = sql + "'" + TradeContext.BATCHNO          + "',"                              #ί�к�(���κ�:Ψһ(����+��ˮ��)
        sql = sql + "'" + TradeContext.I1APPNO          + "',"                              #ҵ����
        sql = sql + "'" + TradeContext.I1BUSINO         + "',"                              #��λ���
        sql = sql + "'" + TradeContext.I1ZONENO         + "',"                              #������
        sql = sql + "'" + TradeContext.I1SBNO           + "',"                              #�����
        sql = sql + "'" + TradeContext.I1USID           + "',"                              #����Ա
        sql = sql + "'" + TradeContext.I1ADMINNO        + "',"                              #����Ա
        sql = sql + "'" + TradeContext.I1FTPTYPE        + "',"                              #�ն�����
        sql = sql + "'" + TradeContext.I1FILENAME       + "',"                              #�����ļ�
        sql = sql + "'" + TradeContext.TranDate         + "',"                              #����ʱ��
        sql = sql + "'" + TradeContext.TranTime         + "',"                              #����ʱ��
        sql = sql + "'" + "00000000"                    + "',"                              #�ύ����
        sql = sql + "'" + "000000"                      + "',"                              #�ύʱ��
        sql = sql + "'" + TradeContext.I1TOTALNUM       + "',"                              #�ܱ���
        sql = sql + "'" + TradeContext.I1TOTALAMT       + "',"                              #�ܽ��
        sql = sql + "'" + "0"                           + "',"                              #�ɹ�����
        sql = sql + "'" + "0"                           + "',"                              #�ɹ����
        sql = sql + "'" + "0"                           + "',"                              #ʧ�ܱ���
        sql = sql + "'" + "0"                           + "',"                              #ʧ�ܽ��
        sql = sql + "'" + "10"                          + "',"                              #״̬(����)
        sql = sql + "'" + TradeContext.I1NOTE1          + "',"                              #��Ч����
        sql = sql + "'" + TradeContext.I1NOTE2          + "',"                              #ʧЧ����
        sql = sql + "'" + TradeContext.I1NOTE5          + "',"                              #������Ϣ
        sql = sql + "'" + ""                            + "',"                              #��ע1
        
        #begin 20091028 �������޸� ����������ţ���ŵ���ע2��
        sql = sql + "'" + TradeContext.I1BTHNO          + "',"                              #��ע2
        #end
        
        #begin 20090927 �������޸� ���Ӵ����־����ŵ���ע3��
        #sql = sql + "'" + TradeContext.I1NOTE3         + "',"                              #��ע3
        sql = sql + "'" + TradeContext.I1TRFG           + "',"                              #��ע3
        #end
        
        sql = sql + "'" + TradeContext.I1NOTE4          + "',"                              #��ע4
        sql = sql + "'" + ""                            + "')"                              #��ע5

        AfaLoggerFunc.tradeInfo(sql)

        result = AfaDBFunc.InsertSqlCmt( sql )
        if( result <= 0 ):
            AfaLoggerFunc.tradeFatal( AfaDBFunc.sqlErrMsg )

            #ɾ���ļ�
            rm_cmd_str="rm " + TradeContext.D_FILENAME
            os.system(rm_cmd_str)

            return ExitSubTrade( '9000', '�Ǽ�������ҵ������Ϣʧ��')
        
        return True

    except Exception, e:
        #ɾ���ļ�
        rm_cmd_str="rm " + TradeContext.D_FILENAME
        os.system(rm_cmd_str)

        AfaLoggerFunc.tradeFatal( str(e) )
        return ExitSubTrade( '9999', '�Ǽ�������ҵ������Ϣ�쳣')


def ExitSubTrade( errorCode, errorMsg ):

    if( len( errorCode )!=0 ):
        TradeContext.tradeResponse.append(['errorCode', errorCode])
        TradeContext.tradeResponse.append(['errorMsg',  errorMsg])

    if( errorCode.isdigit( )==True and long( errorCode )==0 ):
        return True

    else:
        return False
