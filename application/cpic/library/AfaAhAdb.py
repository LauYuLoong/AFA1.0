# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.�������ɷ����ݿ������
#=================================================================
#   �����ļ�:   AfaShebaoFunc.py
#   �޸�ʱ��:   2009-04-16
#    ��  �� :   Agree
##################################################################
import TradeContext,AfaLoggerFunc,AfaDBFunc,AfaUtilTools,AfaFlowControl,TransBillFunc,AfaFunc
from types import *

################################################################################
# �� �� ��: ADBUpdateTransdtl
# ����˵��: �ɷѽ��׵��������سɹ�����¼�¼
# �޸ļ�¼: 
# ��    ע: 
# ��    ��: 
###############################################################################
def ADBUpdateTransdtl( ):
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ����ԭ�ɷѽ���<<<<<<<')
    sqlupdate = ""
    TradeContext.note2 = ""
    TradeContext.note3 = ""
    TradeContext.note4 = ""
    TradeContext.note6 = ""
    TradeContext.note7 = ""
    TradeContext.note8 = ""
    TradeContext.note9 = ""
    TradeContext.note10 = ""
    sqlupdate = sqlupdate + "update afa_maintransdtl set "

    #Third Serailno
    #corpSerno:��������ˮ��
    if TradeContext.existVariable( "corpSerno" ):
        sqlupdate = sqlupdate + " corpSerno = '" + TradeContext.corpSerno.strip() + "' "
    else:
        sqlupdate = sqlupdate + " corpSerno = '' "

    #BaoDanNo:������
    if TradeContext.existVariable( "BaoDanNo" ):
        sqlupdate = sqlupdate + " ,note5 = '" + TradeContext.BaoDanNo.strip() + "' "

    #Ͷ����Ϣ
    #note2:�������|����������
    if( TradeContext.existVariable( "LoanDate" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.LoanDate.strip()
    TradeContext.note2 = TradeContext.note2 + "|"

    if( TradeContext.existVariable( "LoanEndDate" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.LoanEndDate.strip()

    #note3:������ʼ����|���ν�������
    if( TradeContext.existVariable( "EffDate" ) ):
        TradeContext.note3 = TradeContext.note3 + TradeContext.EffDate.strip()
    TradeContext.note3 = TradeContext.note3 + "|"

    if ( TradeContext.existVariable( "TermDate" ) ):
        TradeContext.note3 = TradeContext.note3 + TradeContext.TermDate.strip()

    #note4:�����ͬ����|����ƾ֤���
    if( TradeContext.existVariable( "CreBarNo" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.CreBarNo.strip()
    TradeContext.note4 = TradeContext.note4 + "|"

    if ( TradeContext.existVariable( "CreVouNo" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.CreVouNo.strip()

    #note6:̫��ҵ����Ա����
    if ( TradeContext.existVariable( "CpicTeller" ) ):
        TradeContext.note6 = TradeContext.CpicTeller.strip()

    #note7:�������
    if ( TradeContext.existVariable( "ProCode" ) ):
        TradeContext.note7 = TradeContext.note7 + TradeContext.ProCode.strip()

    #note8:Ͷ������|���ִ���|��������
    if ( TradeContext.existVariable( "IntialNum" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.IntialNum.strip()
    TradeContext.note8 = TradeContext.note8 + "|"

    if ( TradeContext.existVariable( "ProCodeStr" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.ProCodeStr.strip()
    TradeContext.note8 = TradeContext.note8 + "|"

    if ( TradeContext.existVariable( "PlanName" ) ):
        TradeContext.note8 = TradeContext.note8 + TradeContext.PlanName.strip()

    #Ͷ������|���֤|Ͷ���˵�ַ|�ɷѵ绰|�ʱ�
    if ( TradeContext.existVariable( "UserName" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.UserName.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "TGovtID" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.TGovtID.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "line1" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.line1.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    if ( TradeContext.existVariable( "DialNumber" ) ):
        TradeContext.note9 = TradeContext.note9 + TradeContext.DialNumber.strip()
    TradeContext.note9 = TradeContext.note9 + "|"

    #if ( TradeContext.existVariable( "Zip" ) ):
    #    TradeContext.note9 = TradeContext.note9 + TradeContext.Zip.strip()

    #�뱻���˹�ϵ����|����������|���������֤
    if ( TradeContext.existVariable( "RelationShip" ) ):
        TradeContext.note10 = TradeContext.note10 + TradeContext.RelationShip.strip() 
    TradeContext.note10 = TradeContext.note10 + "|"

    if ( TradeContext.existVariable( "UserNameB" ) ):
        TradeContext.note10 = TradeContext.note10 + TradeContext.UserNameB.strip()
    TradeContext.note10 = TradeContext.note10 + "|"

    if ( TradeContext.existVariable( "GovtIDB" ) ):
        TradeContext.note10 = TradeContext.note10 + TradeContext.GovtIDB.strip()
    
    #AfaLoggerFunc.tradeInfo( 'TradeContext.note8 = [' + str(TradeContext.note8) + ']')
    #AfaLoggerFunc.tradeInfo( 'TradeContext.note9 = [' + str(TradeContext.note9) + ']')
    #AfaLoggerFunc.tradeInfo( 'TradeContext.note10 = [' + str(TradeContext.note10) + ']')

    if ( len(str(TradeContext.note2.strip())) > 0):
        sqlupdate = sqlupdate + ",note2 = '"+TradeContext.note2+"' "
    if ( len(str(TradeContext.note3.strip())) > 0):
        sqlupdate = sqlupdate + ",note3 = '"+TradeContext.note3+"' "
    if ( len(str(TradeContext.note4.strip())) > 0):
        sqlupdate = sqlupdate + ",note4 = '"+TradeContext.note4+"' "
    if ( len(str(TradeContext.note6.strip())) > 0):
        sqlupdate = sqlupdate + ",note6 = '"+TradeContext.note6+"' "
    if ( len(str(TradeContext.note7.strip())) > 0):
        sqlupdate = sqlupdate + ",note7 = '"+TradeContext.note7+"' "
    if ( len(str(TradeContext.note8.strip())) > 0):
        sqlupdate = sqlupdate + ",note8 = '"+TradeContext.note8+"' "
    if ( len(str(TradeContext.note9.strip())) > 0):
        sqlupdate = sqlupdate + ",note9 = '"+TradeContext.note9+"' "
    if ( len(str(TradeContext.note10.strip())) > 0):
        sqlupdate = sqlupdate + ",note10 = '"+TradeContext.note10+"' "
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�ɷѽ��׳ɹ�<<<<<<<')
        return True
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�ɷѽ���ʧ��<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','δ����ԭʼ����'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�ɷѽ���ʧ��<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '����ԭ����״̬ʧ��' + AfaDBFunc.sqlErrMsg
        return False
################################################################################
# �� �� ��: ADBUpdateTransdtlRev
# ����˵��: �����ɷѽ��׵��������سɹ�����·��ؽ����Ϣ
# �޸ļ�¼: 
# ��    ע: ֻ���ڳ���ʧ�ܵ�����²ż�¼ʧ����Ϣ
# ��    ��: 
###############################################################################
def ADBUpdateTransdtlRev( ):
    sqlupdate = ""
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ����ԭ�������׽����Ϣ<<<<<<<')
    sqlupdate = sqlupdate + "update afa_maintransdtl set "
    sqlupdate = sqlupdate + " corpcode = '"+TradeContext.errorCode.strip()+"' "
    sqlupdate = sqlupdate + ", errorMsg = '"+TradeContext.errorMsg.strip()+"' "
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣ�ɹ�<<<<<<<')
        return True
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣʧ��<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','δ����ԭʼ����'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>����ԭ�������׽����Ϣʧ��<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '����ԭ����״̬ʧ��' + AfaDBFunc.sqlErrMsg
        return False
################################################################################
# �� �� ��: AdbInsertQueDtl
# ����˵��: ������ �±����㽻�׵Ǽ���ˮ
# �޸ļ�¼��
# ����ֵ��    True  ������ˮ��ɹ�    False ������ˮ��ʧ��
# ����˵����  ����ˮ��Ϣ������ˮ��
################################################################################
def AdbInsertQueDtl( ):
    AfaLoggerFunc.tradeInfo( '>>>>>>>��ʼ���밲������Ϣ��: [ afa_adbinfo ]<<<<<<<')
    
    #��ˮ�������-1
    count=39
    TransDtl=[[]]*( count+1 )
    TransDtl[0] = TradeContext.agentSerialno                    # AGENTSERIALNO ����ҵ����ˮ��
    TransDtl[1] = TradeContext.sysId                            # SYSID         ϵͳ��ʶ
    TransDtl[2] = TradeContext.workDate                         # WORKDATE      ��������
    TransDtl[3] = TradeContext.workTime                         # WORKTIME      ����ʱ��
    TransDtl[4] = TradeContext.brno                             # BRNO          �����
    TransDtl[5] = TradeContext.tellerno                         # TELLERNO      ��Ա��
    
    if( TradeContext.existVariable( "IdType" ) ) :
        TransDtl[6] = TradeContext.IdType                       # IdType        ֤������
    else:
        TransDtl[6] = ''
    
    TransDtl[7]= TradeContext.IdCode                            # IdCode        ֤������
    TransDtl[8]= TradeContext.UserNo                            # UserNo        ������/�û����
    TransDtl[9]= TradeContext.UserName                          # UserName      �û�����
    
    if( TradeContext.existVariable( "TelePhone" ) ) :
        TransDtl[10] = TradeContext.TelePhone                   # TelePhone     �绰����
    else:
        TransDtl[10] = ''
    
    if( TradeContext.existVariable( "Address" ) ) :
        TransDtl[11] = TradeContext.Address                     # Address        ��ַ
    else:
        TransDtl[11] = ''
    
    if( TradeContext.existVariable( "ZipCode" ) ) :
        TransDtl[12] = TradeContext.ZipCode                     # ZipCode        �ʱ�
    else:
        TransDtl[12] = ''
    
    if( TradeContext.existVariable( "Email" ) ) :
        TransDtl[13] = TradeContext.Email                        # Email        �ʼ���ַ
    else:
        TransDtl[13] = ''
    
    if( TradeContext.existVariable( "ProCode" ) ) :
        # ProCode =1 --------ProCodeStr = EL5602
        # ProCode =0 --------ProCodeStr = EL5601
        TransDtl[14] = TradeContext.ProCode                     # ProCode        ���ִ���
    else:
        TransDtl[14] = ''
    
    if( TradeContext.existVariable( "SubmisDate" ) ) :
        TransDtl[15] = TradeContext.SubmisDate                  # SubmisDate        Ͷ������
    else:
        TransDtl[15] = ''
    
    if( TradeContext.existVariable( "IntialNum" ) ) :
        TransDtl[16] = TradeContext.IntialNum                   # IntialNum        Ͷ������
    else:
        TransDtl[16] = ''
    
    TransDtl[17] = TradeContext.EffDate                         # EffDate      ������ʼ����
    TransDtl[18] = TradeContext.TermDate                        # TermDate     ���ν�������
    TransDtl[19] = TradeContext.LoanDate                        # LoanDate     �������
    TransDtl[20] = TradeContext.LoanEndDate                     # LoanEndDate  ������

    if( TradeContext.existVariable( "LoanContractNo" ) ) :
        TransDtl[21] = TradeContext.LoanContractNo                  # CreBarNo     �����ͬ���
    else:
        TransDtl[21] = ''

    if( TradeContext.existVariable( "LoanInvoiceNo" ) ) :
        TransDtl[22] = TradeContext.LoanInvoiceNo                   # CreVouNo     ����ƾ֤���
    else:
        TransDtl[22] = ''
    
    if( TradeContext.existVariable( "PayoutDur" ) ) :
        TransDtl[23] = TradeContext.PayoutDur                   # PayoutDur        �ɷ�����
    else:
        TransDtl[23] = ''
    
    if( TradeContext.existVariable( "BenficName1" ) ) :
        TransDtl[24] = TradeContext.BenficName1                 # BenficName1      ��һ����������
    else:
        TransDtl[24] = ''
    
    if( TradeContext.existVariable( "BenficType" ) ) :
        TransDtl[25] = TradeContext.BenficType                  # BenficType        �ڶ�����������
    else:
        TransDtl[25] = ''
    
    if( TradeContext.existVariable( "BenficName2" ) ) :
        TransDtl[26] = TradeContext.BenficName2                 # BenficName2        ָ������������
    else:
        TransDtl[26] = ''
    
    TransDtl[27] =  TradeContext.CpicTeller.strip()             # CPICTELLER        ̫��ҵ��Ա����(���׳ɹ��󷵻� ����)
    
    if( TradeContext.errorCode.strip() == "0000"):
        TradeContext.DTLSTATUS = "0"
    else:
        TradeContext.DTLSTATUS = "1"
    TransDtl[28] = TradeContext.DTLSTATUS                       # DTLSTATUS        ����״̬(���׳ɹ������Ϊ"0")
    
    if( TradeContext.existVariable( "PaymentAmt" ) ) :
        TradeContext.AMOUNT = TradeContext.PaymentAmt
    else:
        TradeContext.AMOUNT = ''
    TransDtl[29] = TradeContext.AMOUNT                          # AMOUNT        ���ѽ��(���׳ɹ��󷵻� ����)
    
    if( TradeContext.existVariable( "GovtIDB" ) ) :
        TransDtl[30] = TradeContext.GovtIDB                     # IdCodeB        ������֤������(���׳ɹ��󷵻� ����)
    else:
        TransDtl[30] = ''
    
    if( TradeContext.existVariable( "FullNameB" ) ) :
        TransDtl[31] = TradeContext.FullNameB                   # UserNameB        ���������� (���׳ɹ��󷵻� ����)
    else:
        TransDtl[31] = ''
    
    if( TradeContext.existVariable( "PolNumber" ) ):            # NOTE1         ��ע1(���չ�˾���صı�����)
        TransDtl[32] = TradeContext.PolNumber
    else:
        TransDtl[32] = ''
    if( TradeContext.existVariable( "ProCode" ) ):              # NOTE2         ��ע2(��������)
        TransDtl[33] = TradeContext.ProCode
    else:
        TransDtl[33] = ''
    if( TradeContext.existVariable( "unitno" ) ):                # NOTE3         ��ע3(��λ����)
        TransDtl[34] = TradeContext.unitno
    else:
        TransDtl[34] = ''
    if( TradeContext.existVariable( "note4" ) ):                # NOTE4         ��ע4
        TransDtl[35] = TradeContext.note4
    else:
        TransDtl[35] = ''
    if( TradeContext.existVariable( "note5" ) ):                # NOTE5         ��ע5
        TransDtl[36] = TradeContext.note5
    else:
        TransDtl[36] = ''
    if( TradeContext.existVariable( "note6" ) ):                # NOT6         ��ע6
        TransDtl[37] = TradeContext.note6
    else:
        TransDtl[37] = ''
    if( TradeContext.existVariable( "note7" ) ):                # NOTE7         ��ע7
        TransDtl[38] = TradeContext.note7
    else:
        TransDtl[38] = ''
    if( TradeContext.existVariable( "errorMsg" ) ):                # NOTE8         ��ע8
        TransDtl[39] = TradeContext.errorMsg
    else:
        TransDtl[39] = ''
    sql = "INSERT INTO AFA_ADBINFO ("
    sql = sql + "AGENTSERIALNO,SYSID,WORKDATE,WORKTIME,BRNO,TELLERNO,IDTYPE,IDCODE,USERNO,USERNAME,TELEPHONE,"
    sql = sql + "ADDRESS,ZIPCODE,EMAIL,PROCODE,SUBMISDATE,INTIALNUM,EFFDATE,TERMDATE,LOANDATE,LOANENDDATE,CREBARNO,"
    sql = sql + "CREVOUNO,PAYOUTDUR,BENFICNAME1,BENFICTYPE,BENFICNAME2,CPICTELLER,DTLSTATUS,AMOUNT,IDCODEB,USERNAMEB,"
    sql = sql + "NOTE1,NOTE2,NOTE3,NOTE4,NOTE5,NOTE6,NOTE7,NOTE8) VALUES("
    
    i=0
    for i in range( 0, count ):
        if( type( TransDtl[i] ) is int ):
            sql=sql+str( TransDtl[i] )+","
        else:
            sql=sql+"'"+ TransDtl[i]+"',"
    
    sql=sql+"'"+TransDtl[count]+"')"
    
    AfaLoggerFunc.tradeInfo( '>>>>>>>�±����㽻�׵Ǽ���ˮ<<<<<<< ' + str(sql))
    
    result=AfaDBFunc.InsertSqlCmt( sql )
        
    if( result < 1 ):
        TradeContext.errorCode, TradeContext.errorMsg='A0044', '������ˮ����ʧ��'+AfaDBFunc.sqlErrMsg
        return False
    else:
        return True
################################################################################
# �� �� ��: ADBUpdateQueDtl
# ����˵��: �±�����ɹ����ظ��½��׳ɹ���ʶ��������
# �޸ļ�¼: 
# ��    ע: 
# ��    ��: 
###############################################################################
def ADBUpdateQueDtl( ):
    sqlupdate = ""
    AfaLoggerFunc.tradeInfo( '>>>>>>>�±��������ԭ������ˮ<<<<<<<')
    sqlupdate = sqlupdate + "update afa_adbinfo set "
    sqlupdate = sqlupdate + " note8 = '"+TradeContext.errorMsg.strip()+"' "
    if( TradeContext.errorCode.strip() == "0000"):
        sqlupdate = sqlupdate + ", dtlstatus = '0' "
        sqlupdate = sqlupdate + ", amount = '"+TradeContext.PaymentAmt.strip()+"' "
    #̫��ҵ��Ա����
    if( TradeContext.existVariable( "CpicTeller" ) and len(TradeContext.CpicTeller.strip()) > 0):
        sqlupdate = sqlupdate + ", CpicTeller = '"+TradeContext.CpicTeller.strip()+"'"
    #����������
    if( TradeContext.existVariable( "FullNameB" ) and len(TradeContext.FullNameB.strip()) > 0):
        sqlupdate = sqlupdate + ", UserNameB = '"+TradeContext.FullNameB.strip()+"'"
    #������֤������
    if( TradeContext.existVariable( "GovtIDB" ) and len(TradeContext.GovtIDB.strip()) > 0):
        sqlupdate = sqlupdate + ", IdCodeB = '"+TradeContext.GovtIDB.strip()+"'"
    sqlupdate = sqlupdate + " where sysid = '"+TradeContext.sysId+"' and agentserialno = '"+TradeContext.agentSerialno+"'"
    AfaLoggerFunc.tradeInfo( 'sqlupdate = ' + str(sqlupdate))
    record=AfaDBFunc.UpdateSqlCmt( sqlupdate )
    if( record > 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>�����±�����ԭ������ˮ�ɹ�<<<<<<<')
        return True
    if( record == 0 ):
        AfaLoggerFunc.tradeInfo( '>>>>>>>�����±�����ԭ������ˮʧ��<<<<<<<')
        TradeContext.errorCode,TradeContext.errorMsg='A0100','δ����ԭʼ����'
        return False
    else :
        AfaLoggerFunc.tradeInfo( '>>>>>>>�����±�����ԭ������ˮʧ��<<<<<<<')
        TradeContext.errorCode, TradeContext.errorMsg='A0100', '����ԭ����״̬ʧ��' + AfaDBFunc.sqlErrMsg
        return False

################################################################################
# �� �� ��: ADBCheckCert
# ����˵��: ���ƾ֤�����뱣�չ�˾�Ƿ��Ӧ
# �޸ļ�¼: 20091120  ������  ����
# ��    ע:
# ��    ��:
###############################################################################
def ADBCheckCert( ):
    AfaLoggerFunc.tradeInfo('>>>>��ȡ���չ�˾[' + TradeContext.unitno + ']ƾ֤�ţ���У��<<<<')
    sql = ""
    sql = sql + " select certtype from afa_adbpam where "
    sql = sql + " unitno='" + TradeContext.unitno + "'"                       #��λ���ƣ����ݱ��չ�˾�����
                                                                              #��ѯƾ֤���ࣩ
    sql = sql + " and certtype='" + TradeContext.I1CETY + "'"

    AfaLoggerFunc.tradeInfo( sql )

    record = AfaDBFunc.SelectSql( sql )

    if ( record==None ):
        AfaLoggerFunc.tradeInfo( '>>>>��ѯƾ֤�����쳣<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg = 'A0100', '��ѯƾ֤�����쳣'
        return False

    if ( len(record) <= 0):
        AfaLoggerFunc.tradeInfo( '>>>>���չ�˾�����ƾ֤����Ƿ�<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg = 'A0100', '���չ�˾�����ƾ֤����Ƿ�'
        return False

    return True

################################################################################
# �� �� ��: ADBGetInfoByUnitno
# ����˵��: ��ȡ���չ�˾�����Ϣ
# �޸ļ�¼: 1. �ر�� 2009-11-24 ����
# ��    ע:
# ��    ��:
###############################################################################
def ADBGetInfoByUnitno():
    AfaLoggerFunc.tradeInfo( '>>>>��ȡ���չ�˾�����Ϣ<<<<' )
    AfaLoggerFunc.tradeInfo("���չ�˾����[" + TradeContext.unitno + "]")
    #��ʼ�����ִ������������
    TradeContext.ProCodeStr = ''
    TradeContext.PlanName   = ''
    sql = ""
    sql = "select NOTE2 from afa_unitadm where sysid = '" + TradeContext.sysId + "' and unitno = '" + TradeContext.unitno + "'"
    record = AfaDBFunc.SelectSql( sql )
    if ( record == None ):
        AfaLoggerFunc.tradeInfo( '>>>>��ȡ���չ�˾�����Ϣ�쳣<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg='A0100','��ȡ���չ�˾�����Ϣ�쳣'
        return False

    if ( len(record) <= 0):
        AfaLoggerFunc.tradeInfo( '>>>>δ�鵽��ر��չ�˾��Ϣ<<<<' )
        TradeContext.errorCode,TradeContext.errorMsg='A0100','δ�鵽��ر��չ�˾��Ϣ'
        return False

    else:
        tmplist = record[0][0].split("|")
        if len(tmplist) < 2:
            AfaLoggerFunc.tradeInfo(">>>>���չ�˾������Ϣ�Ƿ�<<<<")
            TradeContext.errorCode,TradeContext.errorMsg='A0100','���չ�˾������Ϣ�Ƿ�'
            return False

        TradeContext.ProCodeStr = tmplist[0]
        TradeContext.PlanName = tmplist[1]

        AfaLoggerFunc.tradeInfo( '>>>>���ݿ��������ִ���[' + TradeContext.ProCodeStr + ']' )
        AfaLoggerFunc.tradeInfo( '>>>>���ݿ�������������[' + TradeContext.PlanName + ']' )

        return True
