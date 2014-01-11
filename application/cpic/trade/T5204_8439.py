# -*- coding: gbk -*-
##################################################################
#   �м�ҵ��ƽ̨.
#=================================================================
#   �����ļ�:   5204_8439.py
#   ����˵��:   [���ݱ����Ų�ѯ�ɷ���Ϣ]
#   �޸�ʱ��:   2009-04-07
##################################################################
import TradeContext, AfaLoggerFunc, AfaUtilTools, AfaFunc, Party3Context,AfaAfeFunc,AfaFlowControl,AfaDBFunc
import AfaHostFunc
from types import *

def SubModuleDoFst( ):
    AfaLoggerFunc.tradeInfo( '��ʼ�����ױ���' )
    AfaLoggerFunc.tradeInfo( '�ɷ���Ϣ��ѯ����ֵ����Ч��У��' )
    if( not TradeContext.existVariable( "CpicNo" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '���յ���[CpicNo]ֵ������!' )
    if( not TradeContext.existVariable( "channelCode" ) ):
        return AfaFlowControl.ExitThisFlow( 'A0001', '��������[channelCode]ֵ������!' )
    if( TradeContext.channelCode == '005' ):
        if( not TradeContext.existVariable( "tellerno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[tellerno]ֵ������!' )
        if( not TradeContext.existVariable( "brno" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '�����[brno]ֵ������!' )
        if( not TradeContext.existVariable( "termid" ) ):
            return AfaFlowControl.ExitThisFlow( 'A0001', '��Ա��[termid]ֵ������!' )
    return True
def SubModuleDoSnd():
    AfaLoggerFunc.tradeInfo('�ɷ���Ϣ��ѯ����[T'+TradeContext.TemplateCode+'_'+TradeContext.TransCode+']' )
    try:
        sql = "select agentserialno,"
        sql = sql + "userno,username,idcode,amount,usernameb,idcodeb,loandate,loanenddate,crevouno,crebarno,procode,cpicteller,note1 "
        sql = sql + " from afa_adbinfo where userno = '" + TradeContext.CpicNo.strip() + "' and note3 = '" + TradeContext.unitno.strip() + "'"
        sql = sql + " and workdate = '"+TradeContext.workDate + "'"
        sql = sql + " and tellerno = '"+TradeContext.tellerno + "'"
        sql = sql + " and dtlstatus = '0' "
        sql = sql + " order by agentserialno desc"
        AfaLoggerFunc.tradeInfo('�ɷ���Ϣ��ѯ���'+ sql)
        records = AfaDBFunc.SelectSql( sql )
        if(len(records) < 1):
            TradeContext.errorCode,TradeContext.errorMsg = "0001","�޴�Ͷ����Ϣ"
            return False
        else:
            #�û����(���յ���)
            TradeContext.CpicNo = records[0][1]
            #Ͷ��������
            TradeContext.UserName = records[0][2]
            #Ͷ�������֤����
            TradeContext.GovtID = records[0][3]
            #���
            TradeContext.PaymentAmt = records[0][4]
            #����������
            TradeContext.UserNameB = records[0][5]
            #���������֤����
            TradeContext.GovtIDB = records[0][6]
            #�������
            TradeContext.LoanDate = records[0][7]
            #������
            TradeContext.LoanEndDate = records[0][8]
            #���ƾ֤���
            TradeContext.CreVouNo = records[0][9]
            #�����ͬ���
            TradeContext.CreBarNo = records[0][10]
            #��������
            TradeContext.ProCode = records[0][11]
            #̫��ҵ��Ա����
            TradeContext.CpicTeller = records[0][12]
            #������
            TradeContext.CpciPNo = records[0][13]
            #���׷�����
            TradeContext.errorCode = '0000'
        AfaLoggerFunc.tradeInfo('�˳��ɷ���Ϣ��ѯ����' )
        return True
    except Exception, e:
        AfaFlowControl.exitMainFlow(str(e))
