# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   4201_8434.py
#   ����˵��:   [8434--6000811]���յ�֤�ش�
#   �޸�ʱ��:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc,AfaAhAdb
import AfaHostFunc
from types import *

def SubModuleDoFst( ):

    #begin  20091120  ������  ����
    #У�鱣�չ�˾�����ƾ֤�����Ƿ�Ϸ�
    if not AfaAhAdb.ADBCheckCert( ):
        return False
    #end

    AfaLoggerFunc.tradeInfo( '��ʼ�����ױ���' )
    #���״���
    TradeContext.tradeCode = TradeContext.TransCode
    #����
    if( TradeContext.existVariable( "ProCode" ) ):
        if ( TradeContext.ProCode == "1" ):
            TradeContext.ProCodeStr = "EL5612"
            TradeContext.PlanName   = "������"
            TradeContext.OCpicType  = "002"
        elif ( TradeContext.ProCode == "2" ):
            TradeContext.ProCodeStr = "211610"
            TradeContext.PlanName   = "���Ľ���������˺�����"

    try:
        #��ѯ������
        sql = ""
        sql = "select note5,note4,note2,note8,amount,bankserno,acctype,agentserialno from afa_maintransdtl where agentserialno = '"+TradeContext.PreSerialno+"'"
        sql = sql + " and userno = '"+TradeContext.OCpicNo+"'"
        sql = sql + " and bankstatus = '0' and corpstatus = '0' and revtranf = '0'"
        AfaLoggerFunc.tradeInfo('���յ�֤�ش��ѯ���'+ sql)
        records = AfaDBFunc.SelectSql( sql )
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴˽���"
            return False
        else:
            AfaLoggerFunc.tradeDebug("records=" + str(records))
            TradeContext.PolNumber = records[0][0]
            #note1 : "�����ͬ���"+"|"+"����ƾ֤���"
            arrayList = ""
            arrayList = (records[0][1]).split("|")
            TradeContext.CreBarNo = arrayList[0].strip()
            TradeContext.CreVouNo = arrayList[1].strip()
            #note2 : "�������"+"|"+"������"
            arrayList = ""
            arrayList = (records[0][2]).split("|")
            TradeContext.LoanDate    = arrayList[0].strip()
            TradeContext.LoanEndDate = arrayList[1].strip()
            #note8 : "Ͷ������"+"|"+"���ִ���"+"|"+"��������"
            arrayList = ""
            arrayList = (records[0][3]).split("|")
            TradeContext.IntialNum    = arrayList[0].strip()
            TradeContext.ProCodeStr   = arrayList[1].strip()
            TradeContext.PlanName     = arrayList[2].strip()
            #amount : "�ɷѽ��"
            TradeContext.amount      = records[0][4].strip()
            #bankserno : "������Ա��ˮ��"
            TradeContext.hostserialno = records[0][5].strip()
            #acctype : "�˻�����"
            if records[0][6].strip() == '000':
                TradeContext.AccType = "0"
            else:
                TradeContext.AccType = "4"
            #agentSerialno: "�м�ҵ����ˮ��"
            TradeContext.agentserialno = records[0][7].strip()
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('�����ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
    try:
        
        Party3Context.agentSerialno = TradeContext.agentserialno
        Party3Context.workDate      = TradeContext.workDate
        Party3Context.workTime      = TradeContext.workTime
        Party3Context.amount        = TradeContext.amount
        Party3Context.hostserialno  = TradeContext.hostserialno
        Party3Context.CreBarNo      = TradeContext.CreBarNo  
        Party3Context.CreVouNo      = TradeContext.CreVouNo  
        Party3Context.LoanDate      = TradeContext.LoanDate
        Party3Context.LoanEndDate   = TradeContext.LoanEndDate
        Party3Context.ProCode       = TradeContext.ProCode
        Party3Context.ProCodeStr    = TradeContext.ProCodeStr
        Party3Context.PlanName      = TradeContext.PlanName  
        Party3Context.AccType       = TradeContext.AccType   
        
        names = Party3Context.getNames( )
        for name in names:
            value = getattr( Party3Context, name )
            setattr( TradeContext, name, value )
            #AfaLoggerFunc.tradeInfo("�ֶ�����  ["+str(name)+"] =  "+str(value))
        if( TradeContext.errorCode == '0000' ):
            #if( TradeContext.existVariable( "ProCodeStr" ) ):
            #    if (TradeContext.ProCodeStr == "EL5602"):
            #        TradeContext.ProCode == "1"
            #    else:
            #        TradeContext.ProCode == "0"
            #������ʼ��������
            if ( TradeContext.existVariable( "EffDate" )):
                if ( len(str(TradeContext.EffDate)) == 14 ):
                    TradeContext.EffDate = TradeContext.EffDate[0:4]+TradeContext.EffDate[6:8]+TradeContext.EffDate[10:12]
            if ( TradeContext.existVariable( "TermDate" )):
                if ( len(str(TradeContext.TermDate)) == 14 ):
                    TradeContext.TermDate = TradeContext.TermDate[0:4]+TradeContext.TermDate[6:8]+TradeContext.TermDate[10:12]
            update_sql = "update afa_maintransdtl set "
            update_sql = update_sql + " userno = '" + TradeContext.NCpicNo + "'"
            update_sql = update_sql + " where userno = '" + TradeContext.OCpicNo + "'"
            if not AfaDBFunc.UpdateSqlCmt(update_sql):
                return AfaFlowControl.exitThisFlow("A999","����Ͷ������ʧ��")

        AfaLoggerFunc.tradeInfo('�˳���ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']�������ͨѶ����' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
