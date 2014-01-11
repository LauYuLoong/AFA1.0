# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   004202_8202.py
#   ����˵��:   [8431--6000113]�±��б�
#   �޸�ʱ��:   2006-04-06
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,HostContext,AfaAhAdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #begin  20091120  ������  ����
    #У�鱣�չ�˾�����ƾ֤�����Ƿ�Ϸ�
    if not AfaAhAdb.ADBCheckCert( ):
        return False
    #end

    AfaLoggerFunc.tradeInfo( '��ʼ�����ױ���' )
    TradeContext.note1,TradeContext.note2,TradeContext.note4 = "","",""
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    # �����ͬ���+����ƾ֤���
    if( TradeContext.existVariable( "CreBarNo" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.CreBarNo +"|"
    if ( TradeContext.existVariable( "CreVouNo" ) ):
        TradeContext.note4 = TradeContext.note4 + TradeContext.CreVouNo
    #�������+������
    if( TradeContext.existVariable( "LoanDate" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.LoanDate +"|"
    if ( TradeContext.existVariable( "LoanEndDate" ) ):
        TradeContext.note2 = TradeContext.note2 + TradeContext.LoanEndDate
    #��֤��
    if( TradeContext.existVariable( "CpciPNo" ) ):
        TradeContext.note1 = TradeContext.note1 + TradeContext.CpciPNo
    #�û����(Ͷ������)
    if( not TradeContext.existVariable( "CpicNo" ) and len(TradeContext.CpicNo.strip()) > 0 ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�û����Ͷ������[CpicNo]ֵ������!' )
    else:
        TradeContext.userno = TradeContext.CpicNo
    #�ɷѽ��
    if( not TradeContext.existVariable( "Amount" ) and len(TradeContext.Amount.strip()) > 0):
        return AfaFlowControl.ExitThisFlow( 'A0001', '�ɷѽ��[Amount]ֵ������!' )
    else:
        TradeContext.amount = TradeContext.Amount
    #�û�����
    if( TradeContext.existVariable( "UserName" ) and len(TradeContext.UserName.strip()) > 0 ):
        TradeContext.userName = TradeContext.UserName
    #�ն˱�ʶ
    if( TradeContext.existVariable( "termid" ) and len(TradeContext.termid.strip()) > 0 ):
        TradeContext.termId = TradeContext.termid
    #������֤��
    if( TradeContext.existVariable( "CpciPNo" ) and len(TradeContext.CpciPNo.strip()) > 0 ):
        TradeContext.CpciPNo = TradeContext.CpciPNo[2:15]
    #�˻�����
    if TradeContext.AccType == "0":
        TradeContext.accType = "000"
    else:
        TradeContext.accno = TradeContext.AccNo
        if TradeContext.PyiTp == "0":
            TradeContext.accType = "003"
        else:
            TradeContext.accType = "001"
    #֧������
    if TradeContext.TradeType == '0':                                    #ƾ����
        TradeContext.accPwd = TradeContext.PassWd
        TradeContext.vouhType = TradeContext.iCreno[:2]
        TradeContext.vouhNo = TradeContext.iCreno[2:]
    elif TradeContext.TradeType == '1':                                  #ƾ֤��
        TradeContext.idType = TradeContext.GovtIDTC
        TradeContext.idno = TradeContext.GovtID
        TradeContext.vouhType = TradeContext.iCreno[:2]
        TradeContext.vouhNo = TradeContext.iCreno[2:]
    elif TradeContext.TradeType == "2":                                  #ƾ����
        TradeContext.vouhType = TradeContext.iCreno[:2]
        TradeContext.vouhNo = TradeContext.iCreno[2:]
    
    #�ر�� 20091124 ���ݵ�λ�����ȡ���չ�˾��Ϣ
    AfaAhAdb.ADBGetInfoByUnitno()
    ##���ִ���
    #if( TradeContext.existVariable( "ProCode" ) and len(TradeContext.ProCode.strip()) > 0 ):
    #    if ( TradeContext.ProCode == "1"):
    #        TradeContext.ProCodeStr = "EL5612"
    #        TradeContext.PlanName   = "������B"
    #    elif ( TradeContext.ProCode == "2"):
    #        TradeContext.ProCodeStr = "211610"
    #        TradeContext.PlanName   = "���Ľ���������˺�����"
    
    
    AfaLoggerFunc.tradeDebug("TradeContext.accType = [" + TradeContext.accType + "]")
    AfaLoggerFunc.tradeInfo( 'TradeContext.note1 = [' + str(TradeContext.note1) + ']')
    AfaLoggerFunc.tradeInfo( 'TradeContext.note2 = [' + str(TradeContext.note2) + ']')
    AfaLoggerFunc.tradeInfo( 'TradeContext.note4 = [' + str(TradeContext.note4) + ']')
    return True
def SubModuleDoSnd( ):
    return True
def SubModuleDoTrd( ):
    AfaLoggerFunc.tradeInfo('����ɷѽ���[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
#    try:
    #AfaLoggerFunc.tradeInfo('status='+TradeContext.__status__+'autoRevTranCtl='+TradeContext.__autoRevTranCtl__)
 
    Party3Context.agentSerialno = TradeContext.agentSerialno
    Party3Context.workDate      = TradeContext.workDate
    Party3Context.workTime      = TradeContext.workTime
    Party3Context.amount        = TradeContext.amount
    Party3Context.ProCode       = TradeContext.ProCode
    Party3Context.ProCodeStr    = TradeContext.ProCodeStr
    Party3Context.PlanName      = TradeContext.PlanName  

    if not Party3Context.existVariable('CpicTeller'):
        AfaLoggerFunc.tradeInfo( '>>>���չ�˾δ����ҵ��Ա��ţ�ϵͳ�Զ�����' )
        TradeContext.errorCode, TradeContext.errorMsg = 'A0100', '���չ�˾δ����ҵ��Ա���'
        return False
 
    names = Party3Context.getNames( )
    for name in names:
        value = getattr( Party3Context, name )
        if ( not name.startswith( '__' ) and type(value) is StringType) :
            setattr( TradeContext, name, value )
        #AfaLoggerFunc.tradeInfo("�ֶ�����  ["+str(name)+"] =  "+str(value))
    if( TradeContext.errorCode == '0000' ):
        TradeContext.errorMsg = '���׳ɹ�'
        if ( TradeContext.existVariable( "EffDate" ) and len(str(TradeContext.EffDate)) == 14):
            TradeContext.EffDate = TradeContext.EffDate[0:4] + TradeContext.EffDate[6:8] + TradeContext.EffDate[10:12]
        if ( TradeContext.existVariable( "TermDate" ) and len(str(TradeContext.TermDate)) == 14):
            TradeContext.TermDate = TradeContext.TermDate[0:4] + TradeContext.TermDate[6:8] + TradeContext.TermDate[10:12]
        if not AfaAhAdb.ADBUpdateTransdtl( ):
            #raise AfaFlowControl.accException()
            return False
    else:
        AfaLoggerFunc.tradeInfo('�����������ʧ��')
        return False
 
    #AfaLoggerFunc.tradeInfo("�����ͬ��ƾ֤��� "+TradeContext.CreBarNo+"$$$$$$$"+TradeContext.CreVouNo)
    #AfaLoggerFunc.tradeInfo("������ˮ"+ str(TradeContext.bankSerno))
    #TradeContext.CreBarNo = TradeContext.CreBarNo
    #TradeContext.CreVouNo = TradeContext.CreVouNo
    #TradeContext.bankSerno = TradeContext.bankSerno
    AfaLoggerFunc.tradeInfo('�˳��ɷѽ����������ͨѶ����' )
    return True
#    except Exception, e:
#        AfaFlowControl.exitMainFlow(str(e))
    
